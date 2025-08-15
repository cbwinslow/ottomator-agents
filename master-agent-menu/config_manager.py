"""
Configuration Manager - Handles agent parameters, settings, and environment configuration
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class AgentConfig:
    """Configuration for a specific agent"""
    name: str
    enabled: bool = True
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 300
    retry_attempts: int = 3
    environment_vars: Dict[str, str] = None
    custom_settings: Dict[str, Any] = None
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.environment_vars is None:
            self.environment_vars = {}
        if self.custom_settings is None:
            self.custom_settings = {}
        if self.last_updated is None:
            self.last_updated = datetime.now()

@dataclass
class GlobalConfig:
    """Global configuration settings"""
    default_model: str = "gpt-4o-mini"
    default_temperature: float = 0.7
    default_max_tokens: int = 2000
    default_timeout: int = 300
    log_level: str = "INFO"
    enable_monitoring: bool = True
    metrics_endpoint: str = "http://localhost:8080/metrics"
    data_directory: str = "./data"
    cache_enabled: bool = True
    cache_ttl: int = 3600
    max_concurrent_agents: int = 5
    
class ConfigurationManager:
    """Manages configuration for all agents and global settings"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            self.config_dir = Path(__file__).parent / "configs"
        else:
            self.config_dir = Path(config_dir)
        
        self.config_dir.mkdir(exist_ok=True)
        self.agent_configs: Dict[str, AgentConfig] = {}
        self.global_config = GlobalConfig()
        
        # Load existing configurations
        self.load_global_config()
        self.load_all_agent_configs()
    
    def set_global_config(self, **kwargs) -> None:
        """Update global configuration settings"""
        for key, value in kwargs.items():
            if hasattr(self.global_config, key):
                setattr(self.global_config, key, value)
            else:
                logger.warning(f"Unknown global config key: {key}")
        
        self.save_global_config()
    
    def get_global_config(self) -> GlobalConfig:
        """Get global configuration"""
        return self.global_config
    
    def configure_agent(self, agent_name: str, **kwargs) -> None:
        """Configure an agent with custom settings"""
        if agent_name not in self.agent_configs:
            self.agent_configs[agent_name] = AgentConfig(name=agent_name)
        
        config = self.agent_configs[agent_name]
        
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
            elif key.startswith('env_'):
                # Environment variable
                env_key = key[4:].upper()
                config.environment_vars[env_key] = str(value)
            else:
                # Custom setting
                config.custom_settings[key] = value
        
        config.last_updated = datetime.now()
        self.save_agent_config(agent_name)
    
    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """Get configuration for a specific agent"""
        if agent_name not in self.agent_configs:
            # Create default config
            self.agent_configs[agent_name] = AgentConfig(
                name=agent_name,
                model=self.global_config.default_model,
                temperature=self.global_config.default_temperature,
                max_tokens=self.global_config.default_max_tokens,
                timeout=self.global_config.default_timeout
            )
        
        return self.agent_configs[agent_name]
    
    def set_api_key(self, service: str, api_key: str) -> None:
        """Set API key for a service"""
        # Store in environment variables
        os.environ[service.upper() + "_API_KEY"] = api_key
        
        # Also save to a secure config file
        env_file = self.config_dir / ".env"
        env_vars = {}
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        env_vars[key] = value
        
        env_vars[service.upper() + "_API_KEY"] = api_key
        
        with open(env_file, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        logger.info(f"API key set for {service}")
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        key_name = service.upper() + "_API_KEY"
        
        # Check environment variables first
        api_key = os.getenv(key_name)
        if api_key:
            return api_key
        
        # Check .env file
        env_file = self.config_dir / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(key_name + "="):
                        return line.split('=', 1)[1]
        
        return None
    
    def validate_agent_config(self, agent_name: str, required_keys: List[str] = None) -> Dict[str, Any]:
        """Validate agent configuration and return validation results"""
        config = self.get_agent_config(agent_name)
        validation_result = {
            "valid": True,
            "missing_keys": [],
            "invalid_values": [],
            "warnings": []
        }
        
        # Check required API keys
        if required_keys:
            for key in required_keys:
                if not self.get_api_key(key):
                    validation_result["missing_keys"].append(f"{key}_API_KEY")
                    validation_result["valid"] = False
        
        # Validate configuration values
        if config.temperature < 0 or config.temperature > 2:
            validation_result["invalid_values"].append("temperature must be between 0 and 2")
            validation_result["valid"] = False
        
        if config.max_tokens < 1 or config.max_tokens > 100000:
            validation_result["invalid_values"].append("max_tokens must be between 1 and 100000")
            validation_result["valid"] = False
        
        if config.timeout < 1:
            validation_result["invalid_values"].append("timeout must be positive")
            validation_result["valid"] = False
        
        # Check if model is supported
        supported_models = [
            "gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo",
            "claude-3-sonnet", "claude-3-haiku", "claude-3-opus",
            "gemini-pro", "gemini-flash"
        ]
        
        if config.model not in supported_models:
            validation_result["warnings"].append(f"Model '{config.model}' may not be supported")
        
        return validation_result
    
    def create_agent_template(self, agent_name: str, category: str = "general") -> Dict[str, Any]:
        """Create a configuration template for an agent"""
        templates = {
            "mcp": {
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 2000,
                "timeout": 300,
                "custom_settings": {
                    "mcp_servers": [],
                    "enable_tools": True,
                    "tool_timeout": 60
                }
            },
            "research": {
                "model": "gpt-4o",
                "temperature": 0.3,
                "max_tokens": 4000,
                "timeout": 600,
                "custom_settings": {
                    "search_depth": 5,
                    "enable_web_search": True,
                    "max_sources": 10,
                    "fact_check": True
                }
            },
            "content": {
                "model": "gpt-4o",
                "temperature": 0.8,
                "max_tokens": 3000,
                "timeout": 400,
                "custom_settings": {
                    "creativity_mode": True,
                    "style_guidelines": {},
                    "output_formats": ["text", "markdown"]
                }
            },
            "business": {
                "model": "gpt-4o",
                "temperature": 0.4,
                "max_tokens": 2500,
                "timeout": 500,
                "custom_settings": {
                    "formal_tone": True,
                    "include_metrics": True,
                    "data_privacy": True
                }
            },
            "general": {
                "model": self.global_config.default_model,
                "temperature": self.global_config.default_temperature,
                "max_tokens": self.global_config.default_max_tokens,
                "timeout": self.global_config.default_timeout,
                "custom_settings": {}
            }
        }
        
        template = templates.get(category, templates["general"])
        
        # Apply template to agent
        self.configure_agent(agent_name, **template)
        
        return template
    
    def export_config(self, agent_name: str = None) -> Dict[str, Any]:
        """Export configuration(s) to a dictionary"""
        if agent_name:
            config = self.get_agent_config(agent_name)
            return asdict(config)
        else:
            return {
                "global": asdict(self.global_config),
                "agents": {name: asdict(config) for name, config in self.agent_configs.items()}
            }
    
    def import_config(self, config_data: Dict[str, Any], agent_name: str = None) -> None:
        """Import configuration from a dictionary"""
        if agent_name:
            # Import single agent config
            if "name" not in config_data:
                config_data["name"] = agent_name
            
            # Convert datetime string back to datetime object if needed
            if "last_updated" in config_data and isinstance(config_data["last_updated"], str):
                config_data["last_updated"] = datetime.fromisoformat(config_data["last_updated"])
            
            self.agent_configs[agent_name] = AgentConfig(**config_data)
            self.save_agent_config(agent_name)
        else:
            # Import all configs
            if "global" in config_data:
                for key, value in config_data["global"].items():
                    setattr(self.global_config, key, value)
                self.save_global_config()
            
            if "agents" in config_data:
                for name, agent_data in config_data["agents"].items():
                    self.import_config(agent_data, name)
    
    def backup_configs(self, backup_path: str = None) -> str:
        """Create a backup of all configurations"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.config_dir / f"backup_{timestamp}.json"
        
        backup_data = self.export_config()
        
        with open(backup_path, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)
        
        logger.info(f"Configuration backup created: {backup_path}")
        return str(backup_path)
    
    def restore_configs(self, backup_path: str) -> None:
        """Restore configurations from a backup"""
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)
        
        self.import_config(backup_data)
        logger.info(f"Configuration restored from: {backup_path}")
    
    def save_global_config(self) -> None:
        """Save global configuration to file"""
        config_path = self.config_dir / "global.json"
        with open(config_path, 'w') as f:
            json.dump(asdict(self.global_config), f, indent=2)
    
    def load_global_config(self) -> None:
        """Load global configuration from file"""
        config_path = self.config_dir / "global.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    if hasattr(self.global_config, key):
                        setattr(self.global_config, key, value)
    
    def save_agent_config(self, agent_name: str) -> None:
        """Save agent configuration to file"""
        config = self.agent_configs[agent_name]
        config_path = self.config_dir / f"{agent_name}.json"
        
        with open(config_path, 'w') as f:
            json.dump(asdict(config), f, indent=2, default=str)
    
    def load_agent_config(self, agent_name: str) -> None:
        """Load agent configuration from file"""
        config_path = self.config_dir / f"{agent_name}.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                
                # Convert datetime string back to datetime object
                if "last_updated" in data and isinstance(data["last_updated"], str):
                    data["last_updated"] = datetime.fromisoformat(data["last_updated"])
                
                self.agent_configs[agent_name] = AgentConfig(**data)
    
    def load_all_agent_configs(self) -> None:
        """Load all agent configurations from files"""
        for config_file in self.config_dir.glob("*.json"):
            if config_file.name != "global.json":
                agent_name = config_file.stem
                self.load_agent_config(agent_name)
    
    def delete_agent_config(self, agent_name: str) -> None:
        """Delete agent configuration"""
        if agent_name in self.agent_configs:
            del self.agent_configs[agent_name]
        
        config_path = self.config_dir / f"{agent_name}.json"
        if config_path.exists():
            config_path.unlink()
        
        logger.info(f"Configuration deleted for agent: {agent_name}")
    
    def list_configured_agents(self) -> List[str]:
        """List all configured agents"""
        return list(self.agent_configs.keys())
    
    def get_environment_for_agent(self, agent_name: str) -> Dict[str, str]:
        """Get environment variables for an agent"""
        config = self.get_agent_config(agent_name)
        env_vars = dict(os.environ)  # Start with current environment
        
        # Add agent-specific environment variables
        env_vars.update(config.environment_vars)
        
        # Add common API keys if available
        common_keys = [
            "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "BRAVE_API_KEY",
            "GITHUB_TOKEN", "GOOGLE_API_KEY", "SLACK_TOKEN"
        ]
        
        for key in common_keys:
            api_key = self.get_api_key(key.replace("_API_KEY", "").replace("_TOKEN", ""))
            if api_key:
                env_vars[key] = api_key
        
        return env_vars
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of all configurations"""
        return {
            "global_config": asdict(self.global_config),
            "total_agents_configured": len(self.agent_configs),
            "agents_by_model": self._group_agents_by_model(),
            "api_keys_configured": self._get_configured_api_keys(),
            "config_directory": str(self.config_dir),
            "last_backup": self._get_last_backup_time()
        }
    
    def _group_agents_by_model(self) -> Dict[str, List[str]]:
        """Group agents by their configured model"""
        model_groups = {}
        for agent_name, config in self.agent_configs.items():
            model = config.model
            if model not in model_groups:
                model_groups[model] = []
            model_groups[model].append(agent_name)
        return model_groups
    
    def _get_configured_api_keys(self) -> List[str]:
        """Get list of configured API keys"""
        configured_keys = []
        env_file = self.config_dir / ".env"
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key = line.split('=')[0]
                        if key.endswith('_API_KEY') or key.endswith('_TOKEN'):
                            configured_keys.append(key)
        
        return configured_keys
    
    def _get_last_backup_time(self) -> Optional[str]:
        """Get the timestamp of the most recent backup"""
        backup_files = list(self.config_dir.glob("backup_*.json"))
        if backup_files:
            latest_backup = max(backup_files, key=lambda f: f.stat().st_mtime)
            return datetime.fromtimestamp(latest_backup.stat().st_mtime).isoformat()
        return None

if __name__ == "__main__":
    # Test the configuration manager
    config_manager = ConfigurationManager()
    
    # Configure some test agents
    config_manager.configure_agent("test-agent", 
                                  model="gpt-4o",
                                  temperature=0.5,
                                  max_tokens=3000,
                                  env_openai_api_key="test-key")
    
    config_manager.create_agent_template("research-agent", "research")
    config_manager.create_agent_template("content-agent", "content")
    
    # Set some API keys
    config_manager.set_api_key("openai", "sk-test-key")
    config_manager.set_api_key("anthropic", "test-anthropic-key")
    
    # Print summary
    summary = config_manager.get_config_summary()
    print("Configuration Summary:")
    print(f"- Total agents configured: {summary['total_agents_configured']}")
    print(f"- Agents by model: {summary['agents_by_model']}")
    print(f"- API keys configured: {summary['api_keys_configured']}")
    
    # Create backup
    backup_path = config_manager.backup_configs()
    print(f"Backup created: {backup_path}")