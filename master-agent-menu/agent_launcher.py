"""
Agent Launcher - Main interface for launching and managing AI agents
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import logging
from datetime import datetime
import json

from agent_registry import AgentRegistry, AgentInfo, AgentCombination
from config_manager import ConfigurationManager, AgentConfig
from status_monitor import StatusMonitor
from combination_engine import CombinationEngine

logger = logging.getLogger(__name__)

class AgentProcess:
    """Represents a running agent process"""
    
    def __init__(self, agent_name: str, process: subprocess.Popen, config: AgentConfig):
        self.agent_name = agent_name
        self.process = process
        self.config = config
        self.start_time = datetime.now()
        self.status = "running"
        self.error_message = None
    
    def is_running(self) -> bool:
        """Check if the agent process is still running"""
        if self.process:
            return self.process.poll() is None
        return False
    
    def stop(self) -> bool:
        """Stop the agent process"""
        if self.process and self.is_running():
            try:
                self.process.terminate()
                self.process.wait(timeout=10)
                self.status = "stopped"
                return True
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.status = "killed"
                return True
            except Exception as e:
                self.error_message = str(e)
                self.status = "error"
                return False
        return True
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the agent process"""
        return {
            "name": self.agent_name,
            "pid": self.process.pid if self.process else None,
            "status": self.status,
            "start_time": self.start_time.isoformat(),
            "running_time": str(datetime.now() - self.start_time),
            "is_running": self.is_running(),
            "error_message": self.error_message
        }

class AgentLauncher:
    """Main agent launcher and management system"""
    
    def __init__(self, repo_root: str = None):
        if repo_root is None:
            self.repo_root = Path(__file__).parent.parent.absolute()
        else:
            self.repo_root = Path(repo_root).absolute()
        
        # Initialize components
        self.registry = AgentRegistry(self.repo_root)
        self.config_manager = ConfigurationManager()
        self.status_monitor = StatusMonitor()
        self.combination_engine = CombinationEngine(self.registry, self.config_manager)
        
        # Track running agents
        self.running_agents: Dict[str, AgentProcess] = {}
        
        # Initialize registry
        self.registry.discover_agents()
        
        logger.info(f"AgentLauncher initialized with {len(self.registry.agents)} agents")
    
    def list_agents(self, category: str = None, status: str = None) -> List[AgentInfo]:
        """List available agents, optionally filtered by category or status"""
        agents = list(self.registry.agents.values())
        
        if category:
            agents = [agent for agent in agents if agent.category == category]
        
        if status:
            if status == "running":
                agents = [agent for agent in agents if agent.name in self.running_agents]
            elif status == "stopped":
                agents = [agent for agent in agents if agent.name not in self.running_agents]
        
        return agents
    
    def get_agent_info(self, agent_name: str) -> Optional[AgentInfo]:
        """Get detailed information about an agent"""
        return self.registry.get_agent(agent_name)
    
    def search_agents(self, query: str) -> List[AgentInfo]:
        """Search for agents by name or description"""
        return self.registry.search_agents(query)
    
    def configure_agent(self, agent_name: str, **kwargs) -> bool:
        """Configure an agent with custom settings"""
        try:
            self.config_manager.configure_agent(agent_name, **kwargs)
            logger.info(f"Agent {agent_name} configured successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to configure agent {agent_name}: {e}")
            return False
    
    def validate_agent(self, agent_name: str) -> Dict[str, Any]:
        """Validate agent configuration and dependencies"""
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            return {"valid": False, "error": "Agent not found"}
        
        # Check configuration
        validation_result = self.config_manager.validate_agent_config(
            agent_name, 
            agent_info.api_keys_required
        )
        
        # Check if agent files exist
        agent_path = self.repo_root / agent_info.path
        if not agent_path.exists():
            validation_result["valid"] = False
            validation_result["missing_files"] = ["Agent directory not found"]
        else:
            missing_files = []
            if agent_info.main_file and agent_info.main_file != "(no main file found)":
                main_file_path = agent_path / agent_info.main_file
                if not main_file_path.exists():
                    missing_files.append(agent_info.main_file)
            
            if agent_info.requirements_file:
                req_file_path = agent_path / agent_info.requirements_file
                if not req_file_path.exists():
                    missing_files.append(agent_info.requirements_file)
            
            if missing_files:
                validation_result["missing_files"] = missing_files
                validation_result["valid"] = False
        
        return validation_result
    
    def install_dependencies(self, agent_name: str) -> bool:
        """Install dependencies for an agent"""
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            logger.error(f"Agent {agent_name} not found")
            return False
        
        agent_path = self.repo_root / agent_info.path
        
        if agent_info.requirements_file:
            req_file = agent_path / agent_info.requirements_file
            if req_file.exists():
                try:
                    # Install Python dependencies
                    cmd = [sys.executable, "-m", "pip", "install", "-r", str(req_file)]
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=agent_path)
                    
                    if result.returncode == 0:
                        logger.info(f"Dependencies installed for {agent_name}")
                        return True
                    else:
                        logger.error(f"Failed to install dependencies for {agent_name}: {result.stderr}")
                        return False
                except Exception as e:
                    logger.error(f"Error installing dependencies for {agent_name}: {e}")
                    return False
        
        # Check for package.json (Node.js dependencies)
        package_json = agent_path / "package.json"
        if package_json.exists():
            try:
                cmd = ["npm", "install"]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=agent_path)
                
                if result.returncode == 0:
                    logger.info(f"Node.js dependencies installed for {agent_name}")
                    return True
                else:
                    logger.error(f"Failed to install Node.js dependencies for {agent_name}: {result.stderr}")
                    return False
            except Exception as e:
                logger.error(f"Error installing Node.js dependencies for {agent_name}: {e}")
                return False
        
        logger.info(f"No dependencies to install for {agent_name}")
        return True
    
    def launch_agent(self, agent_name: str, **kwargs) -> bool:
        """Launch an agent"""
        if agent_name in self.running_agents:
            logger.warning(f"Agent {agent_name} is already running")
            return False
        
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            logger.error(f"Agent {agent_name} not found")
            return False
        
        # Validate agent before launch
        validation = self.validate_agent(agent_name)
        if not validation["valid"]:
            logger.error(f"Agent {agent_name} validation failed: {validation}")
            return False
        
        # Get agent configuration
        config = self.config_manager.get_agent_config(agent_name)
        
        # Update config with launch parameters
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        # Prepare environment
        env = self.config_manager.get_environment_for_agent(agent_name)
        
        # Determine launch command
        agent_path = self.repo_root / agent_info.path
        
        if agent_info.main_file and agent_info.main_file.endswith('.py'):
            cmd = [sys.executable, agent_info.main_file]
        elif agent_info.main_file and agent_info.main_file.endswith('.js'):
            cmd = ["node", agent_info.main_file]
        else:
            # Try to find a suitable entry point
            python_files = list(agent_path.glob("*.py"))
            if python_files:
                main_file = next((f for f in python_files if 'main' in f.name.lower()), python_files[0])
                cmd = [sys.executable, main_file.name]
            else:
                logger.error(f"No suitable entry point found for {agent_name}")
                return False
        
        try:
            # Launch the agent process
            process = subprocess.Popen(
                cmd,
                cwd=agent_path,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Create agent process object
            agent_process = AgentProcess(agent_name, process, config)
            self.running_agents[agent_name] = agent_process
            
            # Start monitoring
            self.status_monitor.start_monitoring(agent_name, process)
            
            logger.info(f"Agent {agent_name} launched successfully (PID: {process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch agent {agent_name}: {e}")
            return False
    
    def stop_agent(self, agent_name: str) -> bool:
        """Stop a running agent"""
        if agent_name not in self.running_agents:
            logger.warning(f"Agent {agent_name} is not running")
            return False
        
        agent_process = self.running_agents[agent_name]
        success = agent_process.stop()
        
        if success:
            self.status_monitor.stop_monitoring(agent_name)
            del self.running_agents[agent_name]
            logger.info(f"Agent {agent_name} stopped successfully")
        
        return success
    
    def restart_agent(self, agent_name: str, **kwargs) -> bool:
        """Restart an agent"""
        if agent_name in self.running_agents:
            self.stop_agent(agent_name)
        
        return self.launch_agent(agent_name, **kwargs)
    
    def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get status of an agent"""
        if agent_name in self.running_agents:
            agent_process = self.running_agents[agent_name]
            status = agent_process.get_info()
            status.update(self.status_monitor.get_agent_metrics(agent_name))
            return status
        else:
            return {
                "name": agent_name,
                "status": "stopped",
                "is_running": False
            }
    
    def get_all_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all agents"""
        statuses = {}
        
        for agent_name in self.registry.agents.keys():
            statuses[agent_name] = self.get_agent_status(agent_name)
        
        return statuses
    
    def stop_all_agents(self) -> Dict[str, bool]:
        """Stop all running agents"""
        results = {}
        
        for agent_name in list(self.running_agents.keys()):
            results[agent_name] = self.stop_agent(agent_name)
        
        return results
    
    def create_combination(self, combination_name: str, agent_names: List[str], **kwargs) -> bool:
        """Create and launch an agent combination"""
        return self.combination_engine.create_combination(combination_name, agent_names, **kwargs)
    
    def launch_combination(self, combination_name: str, **kwargs) -> bool:
        """Launch a predefined agent combination"""
        return self.combination_engine.launch_combination(combination_name, **kwargs)
    
    def list_combinations(self) -> List[AgentCombination]:
        """List available agent combinations"""
        return list(self.registry.combinations.values())
    
    def export_configuration(self, filepath: str = None) -> str:
        """Export all configurations to a file"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"agent_config_export_{timestamp}.json"
        
        export_data = {
            "agents": self.config_manager.export_config(),
            "registry": {
                "agents": {name: {
                    "name": agent.name,
                    "category": agent.category,
                    "description": agent.description,
                    "path": agent.path,
                    "status": agent.status
                } for name, agent in self.registry.agents.items()},
                "combinations": {name: {
                    "name": combo.name,
                    "description": combo.description,
                    "component_agents": combo.component_agents,
                    "use_cases": combo.use_cases
                } for name, combo in self.registry.combinations.items()}
            },
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Configuration exported to {filepath}")
        return filepath
    
    def import_configuration(self, filepath: str) -> bool:
        """Import configurations from a file"""
        try:
            with open(filepath, 'r') as f:
                import_data = json.load(f)
            
            if "agents" in import_data:
                self.config_manager.import_config(import_data["agents"])
            
            logger.info(f"Configuration imported from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import configuration from {filepath}: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information and statistics"""
        stats = self.registry.get_statistics()
        
        return {
            "repository_root": str(self.repo_root),
            "total_agents": stats["total_agents"],
            "agents_by_category": stats["agents_by_category"],
            "running_agents": len(self.running_agents),
            "total_combinations": stats["total_combinations"],
            "api_keys_configured": len(self.config_manager._get_configured_api_keys()),
            "python_version": sys.version,
            "system_time": datetime.now().isoformat()
        }
    
    def cleanup(self) -> None:
        """Cleanup resources and stop all agents"""
        logger.info("Cleaning up agent launcher...")
        
        # Stop all running agents
        self.stop_all_agents()
        
        # Cleanup monitors
        self.status_monitor.cleanup()
        
        logger.info("Agent launcher cleanup completed")

if __name__ == "__main__":
    # Test the launcher
    launcher = AgentLauncher()
    
    print("=== Agent Launcher System ===")
    print(f"Repository: {launcher.repo_root}")
    
    # Show system info
    system_info = launcher.get_system_info()
    print(f"\nSystem Info:")
    print(f"- Total agents: {system_info['total_agents']}")
    print(f"- Running agents: {system_info['running_agents']}")
    print(f"- Total combinations: {system_info['total_combinations']}")
    
    # Show categories
    print(f"\nAgent Categories:")
    for category, count in system_info["agents_by_category"].items():
        print(f"- {category}: {count} agents")
    
    # Show some example agents
    print(f"\nExample Agents:")
    for agent in list(launcher.list_agents())[:5]:
        print(f"- {agent.name} ({agent.category}): {agent.description[:80]}...")
    
    # Show combinations
    print(f"\nAvailable Combinations:")
    for combo in launcher.list_combinations():
        print(f"- {combo.name}: {combo.description[:80]}...")
        print(f"  Components: {', '.join(combo.component_agents[:3])}...")
    
    launcher.cleanup()