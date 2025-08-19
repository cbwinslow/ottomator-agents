"""
Main CLI Interface for the Master Agent Menu System
"""

import asyncio
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
import argparse
import logging
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.markdown import Markdown

from agent_launcher import AgentLauncher
from agent_registry import AgentInfo
from config_manager import ConfigurationManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('master_agent_menu.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MasterAgentMenu:
    """Main CLI interface for managing AI agents"""
    
    def __init__(self):
        self.console = Console()
        self.launcher = AgentLauncher()
        self.config_manager = self.launcher.config_manager
        
        # Show welcome message
        self._show_welcome()
    
    def _show_welcome(self):
        """Show welcome message and system info"""
        welcome_text = """
# 🤖 Master Agent Menu System

Welcome to the centralized AI agent management system!

This system helps you discover, configure, launch, and manage all available AI agents
in the ottomator-agents repository. You can also create powerful combinations of 
agents to solve complex tasks.
        """
        
        self.console.print(Panel(Markdown(welcome_text), title="Welcome", border_style="green"))
        
        # Show system stats
        system_info = self.launcher.get_system_info()
        stats_table = Table(title="System Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="white")
        
        stats_table.add_row("Total Agents", str(system_info["total_agents"]))
        stats_table.add_row("Running Agents", str(system_info["running_agents"]))
        stats_table.add_row("Total Combinations", str(system_info["total_combinations"]))
        stats_table.add_row("Categories", str(len(system_info["agents_by_category"])))
        
        self.console.print(stats_table)
        self.console.print()
    
    def run(self):
        """Run the main menu loop"""
        while True:
            try:
                choice = self._show_main_menu()
                
                if choice == "1":
                    self._list_agents_menu()
                elif choice == "2":
                    self._manage_agents_menu()
                elif choice == "3":
                    self._combinations_menu()
                elif choice == "4":
                    self._configuration_menu()
                elif choice == "5":
                    self._monitoring_menu()
                elif choice == "6":
                    self._documentation_menu()
                elif choice == "7":
                    self._system_menu()
                elif choice == "0" or choice.lower() == "exit":
                    self._exit_system()
                    break
                else:
                    self.console.print("[red]Invalid choice. Please try again.[/red]")
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interrupted by user[/yellow]")
                if Confirm.ask("Do you want to exit?"):
                    self._exit_system()
                    break
            except Exception as e:
                logger.error(f"Error in main menu: {e}")
                self.console.print(f"[red]An error occurred: {e}[/red]")
    
    def _show_main_menu(self) -> str:
        """Show main menu and get user choice"""
        self.console.print("\n" + "="*60)
        self.console.print("[bold blue]🤖 Master Agent Menu[/bold blue]")
        self.console.print("="*60)
        
        menu_options = [
            ("1", "📋 List & Search Agents"),
            ("2", "🚀 Manage Agents (Launch/Stop/Status)"),
            ("3", "🔗 Agent Combinations"),
            ("4", "⚙️ Configuration Management"),
            ("5", "📊 Monitoring & Health"),
            ("6", "📚 Documentation & Help"),
            ("7", "🛠️ System Management"),
            ("0", "❌ Exit")
        ]
        
        for option, description in menu_options:
            self.console.print(f"  {option}. {description}")
        
        return Prompt.ask("\nSelect an option", choices=[opt[0] for opt, _ in menu_options] + ["exit"])
    
    def _list_agents_menu(self):
        """List and search agents menu"""
        while True:
            self.console.print("\n[bold cyan]📋 Agents List & Search[/bold cyan]")
            
            choice = Prompt.ask(
                "Choose action",
                choices=["list", "search", "categories", "details", "back"],
                default="list"
            )
            
            if choice == "list":
                self._list_all_agents()
            elif choice == "search":
                self._search_agents()
            elif choice == "categories":
                self._show_categories()
            elif choice == "details":
                self._show_agent_details()
            elif choice == "back":
                break
    
    def _list_all_agents(self):
        """List all available agents"""
        category = Prompt.ask(
            "Filter by category (optional)",
            default="all",
            choices=["all"] + list(self.launcher.registry.get_statistics()["agents_by_category"].keys())
        )
        
        if category == "all":
            agents = self.launcher.list_agents()
        else:
            agents = self.launcher.list_agents(category=category)
        
        # Create table
        table = Table(title=f"Available Agents ({len(agents)} total)")
        table.add_column("Name", style="cyan")
        table.add_column("Category", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Description", style="white")
        
        for agent in agents:
            status = "🟢 Running" if agent.name in self.launcher.running_agents else "⚪ Stopped"
            description = agent.description[:60] + "..." if len(agent.description) > 60 else agent.description
            table.add_row(agent.name, agent.category, status, description)
        
        self.console.print(table)
    
    def _search_agents(self):
        """Search agents by query"""
        query = Prompt.ask("Enter search query")
        agents = self.launcher.search_agents(query)
        
        if not agents:
            self.console.print(f"[yellow]No agents found for query: {query}[/yellow]")
            return
        
        table = Table(title=f"Search Results for '{query}' ({len(agents)} found)")
        table.add_column("Name", style="cyan")
        table.add_column("Category", style="green")
        table.add_column("Relevance", style="yellow")
        table.add_column("Description", style="white")
        
        for agent in agents:
            # Simple relevance scoring
            relevance = "High" if query.lower() in agent.name.lower() else "Medium"
            description = agent.description[:50] + "..." if len(agent.description) > 50 else agent.description
            table.add_row(agent.name, agent.category, relevance, description)
        
        self.console.print(table)
    
    def _show_categories(self):
        """Show agent categories"""
        stats = self.launcher.registry.get_statistics()
        
        table = Table(title="Agent Categories")
        table.add_column("Category", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Description", style="white")
        
        category_descriptions = {
            "mcp": "Model Context Protocol based agents",
            "research": "Web research and data gathering agents",
            "knowledge": "RAG and knowledge graph agents",
            "content": "Content creation and generation agents",
            "business": "Business and domain-specific agents",
            "social": "Social media and community agents",
            "web": "Web scraping and crawling agents",
            "media": "Video and multimedia agents",
            "travel": "Travel and booking agents",
            "tech": "Technical and development agents",
            "specialized": "Specialized domain agents",
            "tools": "Utility and tool agents",
            "integration": "Integration and workflow agents",
            "experimental": "Experimental and research agents"
        }
        
        for category, count in stats["agents_by_category"].items():
            description = category_descriptions.get(category, "Specialized AI agent")
            table.add_row(category, str(count), description)
        
        self.console.print(table)
    
    def _show_agent_details(self):
        """Show detailed information about an agent"""
        agent_name = Prompt.ask("Enter agent name")
        agent_info = self.launcher.get_agent_info(agent_name)
        
        if not agent_info:
            self.console.print(f"[red]Agent '{agent_name}' not found[/red]")
            return
        
        # Agent info panel
        info_text = f"""
**Name:** {agent_info.name}
**Category:** {agent_info.category}
**Path:** {agent_info.path}
**Main File:** {agent_info.main_file}
**Last Modified:** {agent_info.last_modified.strftime('%Y-%m-%d %H:%M:%S')}

**Description:**
{agent_info.description}

**Dependencies:** {len(agent_info.dependencies)} packages
{', '.join(agent_info.dependencies[:10])}{'...' if len(agent_info.dependencies) > 10 else ''}

**API Keys Required:**
{', '.join(agent_info.api_keys_required) if agent_info.api_keys_required else 'None'}

**Supported Models:**
{', '.join(agent_info.supported_models) if agent_info.supported_models else 'Not specified'}
        """
        
        self.console.print(Panel(Markdown(info_text), title=f"Agent Details: {agent_name}", border_style="blue"))
        
        # Show current status
        status = self.launcher.get_agent_status(agent_name)
        if status["is_running"]:
            self.console.print(Panel(f"Status: {status['status']}\nPID: {status.get('pid', 'N/A')}", 
                                   title="Current Status", border_style="green"))
        else:
            self.console.print(Panel("Status: Stopped", title="Current Status", border_style="red"))
    
    def _manage_agents_menu(self):
        """Manage agents (launch, stop, restart)"""
        while True:
            self.console.print("\n[bold cyan]🚀 Agent Management[/bold cyan]")
            
            choice = Prompt.ask(
                "Choose action",
                choices=["launch", "stop", "restart", "status", "install", "back"],
                default="status"
            )
            
            if choice == "launch":
                self._launch_agent()
            elif choice == "stop":
                self._stop_agent()
            elif choice == "restart":
                self._restart_agent()
            elif choice == "status":
                self._show_agent_statuses()
            elif choice == "install":
                self._install_dependencies()
            elif choice == "back":
                break
    
    def _launch_agent(self):
        """Launch an agent"""
        agent_name = Prompt.ask("Enter agent name to launch")
        
        # Validate agent exists
        if not self.launcher.get_agent_info(agent_name):
            self.console.print(f"[red]Agent '{agent_name}' not found[/red]")
            return
        
        # Check if already running
        if agent_name in self.launcher.running_agents:
            self.console.print(f"[yellow]Agent '{agent_name}' is already running[/yellow]")
            return
        
        # Validate configuration
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Validating agent...", total=None)
            validation = self.launcher.validate_agent(agent_name)
        
        if not validation["valid"]:
            self.console.print("[red]Agent validation failed:[/red]")
            for error in validation.get("missing_keys", []):
                self.console.print(f"  ❌ Missing API key: {error}")
            for error in validation.get("invalid_values", []):
                self.console.print(f"  ❌ Invalid value: {error}")
            for warning in validation.get("warnings", []):
                self.console.print(f"  ⚠️ Warning: {warning}")
            
            if not Confirm.ask("Continue anyway?"):
                return
        
        # Launch agent
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task(f"Launching {agent_name}...", total=None)
            success = self.launcher.launch_agent(agent_name)
        
        if success:
            self.console.print(f"[green]✅ Agent '{agent_name}' launched successfully[/green]")
        else:
            self.console.print(f"[red]❌ Failed to launch agent '{agent_name}'[/red]")
    
    def _stop_agent(self):
        """Stop a running agent"""
        running_agents = list(self.launcher.running_agents.keys())
        
        if not running_agents:
            self.console.print("[yellow]No agents are currently running[/yellow]")
            return
        
        agent_name = Prompt.ask("Select agent to stop", choices=running_agents + ["all"])
        
        if agent_name == "all":
            if Confirm.ask("Stop all running agents?"):
                results = self.launcher.stop_all_agents()
                for name, success in results.items():
                    status = "✅" if success else "❌"
                    self.console.print(f"{status} {name}")
        else:
            success = self.launcher.stop_agent(agent_name)
            if success:
                self.console.print(f"[green]✅ Agent '{agent_name}' stopped successfully[/green]")
            else:
                self.console.print(f"[red]❌ Failed to stop agent '{agent_name}'[/red]")
    
    def _restart_agent(self):
        """Restart an agent"""
        agent_name = Prompt.ask("Enter agent name to restart")
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task(f"Restarting {agent_name}...", total=None)
            success = self.launcher.restart_agent(agent_name)
        
        if success:
            self.console.print(f"[green]✅ Agent '{agent_name}' restarted successfully[/green]")
        else:
            self.console.print(f"[red]❌ Failed to restart agent '{agent_name}'[/red]")
    
    def _show_agent_statuses(self):
        """Show status of all agents"""
        statuses = self.launcher.get_all_statuses()
        
        table = Table(title="Agent Status Overview")
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("PID", style="yellow")
        table.add_column("Uptime", style="white")
        table.add_column("CPU %", style="magenta")
        table.add_column("Memory MB", style="blue")
        
        for agent_name, status in statuses.items():
            status_icon = "🟢" if status["is_running"] else "⚪"
            status_text = f"{status_icon} {status['status']}"
            
            pid = str(status.get('pid', '-'))
            uptime = status.get('uptime_formatted', '-')
            cpu = f"{status.get('cpu_percent', 0):.1f}" if status["is_running"] else "-"
            memory = f"{status.get('memory_mb', 0):.1f}" if status["is_running"] else "-"
            
            table.add_row(agent_name, status_text, pid, uptime, cpu, memory)
        
        self.console.print(table)
    
    def _install_dependencies(self):
        """Install dependencies for an agent"""
        agent_name = Prompt.ask("Enter agent name to install dependencies")
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task(f"Installing dependencies for {agent_name}...", total=None)
            success = self.launcher.install_dependencies(agent_name)
        
        if success:
            self.console.print(f"[green]✅ Dependencies installed for '{agent_name}'[/green]")
        else:
            self.console.print(f"[red]❌ Failed to install dependencies for '{agent_name}'[/red]")
    
    def _combinations_menu(self):
        """Agent combinations menu"""
        while True:
            self.console.print("\n[bold cyan]🔗 Agent Combinations[/bold cyan]")
            
            choice = Prompt.ask(
                "Choose action",
                choices=["list", "create", "launch", "status", "examples", "back"],
                default="list"
            )
            
            if choice == "list":
                self._list_combinations()
            elif choice == "create":
                self._create_combination()
            elif choice == "launch":
                self._launch_combination()
            elif choice == "status":
                self._combination_status()
            elif choice == "examples":
                self._show_combination_examples()
            elif choice == "back":
                break
    
    def _list_combinations(self):
        """List available combinations"""
        combinations = self.launcher.list_combinations()
        
        table = Table(title=f"Available Agent Combinations ({len(combinations)} total)")
        table.add_column("Name", style="cyan")
        table.add_column("Components", style="green")
        table.add_column("Description", style="white")
        
        for combo in combinations:
            components = ", ".join(combo.component_agents[:3])
            if len(combo.component_agents) > 3:
                components += f" (+{len(combo.component_agents) - 3} more)"
            
            description = combo.description[:60] + "..." if len(combo.description) > 60 else combo.description
            table.add_row(combo.name, components, description)
        
        self.console.print(table)
    
    def _create_combination(self):
        """Create a new agent combination"""
        name = Prompt.ask("Enter combination name")
        description = Prompt.ask("Enter description")
        
        # Select agents
        available_agents = [agent.name for agent in self.launcher.list_agents()]
        selected_agents = []
        
        self.console.print("\nSelect agents for the combination (enter 'done' when finished):")
        while True:
            remaining_agents = [a for a in available_agents if a not in selected_agents]
            if not remaining_agents:
                break
                
            agent = Prompt.ask(
                f"Select agent ({len(selected_agents)} selected)",
                choices=remaining_agents + ["done"],
                default="done"
            )
            
            if agent == "done":
                break
            
            selected_agents.append(agent)
            self.console.print(f"Added: {agent}")
        
        if len(selected_agents) < 2:
            self.console.print("[red]Need at least 2 agents for a combination[/red]")
            return
        
        # Create combination
        success = self.launcher.create_combination(
            name, 
            selected_agents,
            description=description
        )
        
        if success:
            self.console.print(f"[green]✅ Combination '{name}' created successfully[/green]")
        else:
            self.console.print(f"[red]❌ Failed to create combination '{name}'[/red]")
    
    def _launch_combination(self):
        """Launch an agent combination"""
        combinations = [combo.name for combo in self.launcher.list_combinations()]
        
        if not combinations:
            self.console.print("[yellow]No combinations available[/yellow]")
            return
        
        combo_name = Prompt.ask("Select combination to launch", choices=combinations)
        input_data = Prompt.ask("Enter input for the combination", default="")
        
        execution_id = self.launcher.launch_combination(combo_name, input_data)
        
        if execution_id:
            self.console.print(f"[green]✅ Combination '{combo_name}' launched[/green]")
            self.console.print(f"Execution ID: {execution_id}")
        else:
            self.console.print(f"[red]❌ Failed to launch combination '{combo_name}'[/red]")
    
    def _combination_status(self):
        """Show combination execution status"""
        running = self.launcher.combination_engine.list_running_combinations()
        
        if not running:
            self.console.print("[yellow]No combinations currently running[/yellow]")
            return
        
        table = Table(title="Running Combinations")
        table.add_column("Execution ID", style="cyan")
        table.add_column("Combination", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Progress", style="white")
        table.add_column("Current Step", style="magenta")
        
        for combo in running:
            progress = f"{combo['steps_completed']}/{combo['total_steps']}"
            table.add_row(
                combo["execution_id"][:8] + "...",
                combo["combination_name"],
                combo["status"],
                progress,
                combo.get("current_step", "-")
            )
        
        self.console.print(table)
    
    def _show_combination_examples(self):
        """Show example combinations"""
        examples = [
            {
                "name": "Research & Content Pipeline",
                "description": "Research topic → Gather knowledge → Create content",
                "agents": ["web-researcher", "rag-agent", "content-creator"],
                "use_case": "Blog post creation with research"
            },
            {
                "name": "Social Media Intelligence",
                "description": "Analyze Reddit + YouTube → Generate social content",
                "agents": ["reddit-agent", "youtube-agent", "tweet-generator"],
                "use_case": "Social media trend analysis"
            },
            {
                "name": "Business Intelligence Suite",
                "description": "Market research → Competitive analysis → Business plan",
                "agents": ["business-researcher", "web-researcher", "document-generator"],
                "use_case": "Market entry analysis"
            }
        ]
        
        for example in examples:
            example_text = f"""
**{example['name']}**

{example['description']}

**Agents:** {' → '.join(example['agents'])}
**Use Case:** {example['use_case']}
            """
            self.console.print(Panel(Markdown(example_text), border_style="blue"))
    
    def _configuration_menu(self):
        """Configuration management menu"""
        while True:
            self.console.print("\n[bold cyan]⚙️ Configuration Management[/bold cyan]")
            
            choice = Prompt.ask(
                "Choose action",
                choices=["global", "agent", "api_keys", "backup", "restore", "export", "back"],
                default="global"
            )
            
            if choice == "global":
                self._configure_global()
            elif choice == "agent":
                self._configure_agent()
            elif choice == "api_keys":
                self._manage_api_keys()
            elif choice == "backup":
                self._backup_config()
            elif choice == "restore":
                self._restore_config()
            elif choice == "export":
                self._export_config()
            elif choice == "back":
                break
    
    def _configure_global(self):
        """Configure global settings"""
        current_config = self.config_manager.get_global_config()
        
        self.console.print("\nCurrent Global Configuration:")
        config_table = Table()
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="white")
        
        config_table.add_row("Default Model", current_config.default_model)
        config_table.add_row("Default Temperature", str(current_config.default_temperature))
        config_table.add_row("Default Max Tokens", str(current_config.default_max_tokens))
        config_table.add_row("Log Level", current_config.log_level)
        config_table.add_row("Enable Monitoring", str(current_config.enable_monitoring))
        
        self.console.print(config_table)
        
        if Confirm.ask("Update global configuration?"):
            model = Prompt.ask("Default model", default=current_config.default_model)
            temp = float(Prompt.ask("Default temperature", default=str(current_config.default_temperature)))
            tokens = int(Prompt.ask("Default max tokens", default=str(current_config.default_max_tokens)))
            
            self.config_manager.set_global_config(
                default_model=model,
                default_temperature=temp,
                default_max_tokens=tokens
            )
            
            self.console.print("[green]✅ Global configuration updated[/green]")
    
    def _configure_agent(self):
        """Configure a specific agent"""
        agent_name = Prompt.ask("Enter agent name to configure")
        
        if not self.launcher.get_agent_info(agent_name):
            self.console.print(f"[red]Agent '{agent_name}' not found[/red]")
            return
        
        config = self.config_manager.get_agent_config(agent_name)
        
        self.console.print(f"\nCurrent configuration for {agent_name}:")
        config_table = Table()
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="white")
        
        config_table.add_row("Model", config.model)
        config_table.add_row("Temperature", str(config.temperature))
        config_table.add_row("Max Tokens", str(config.max_tokens))
        config_table.add_row("Timeout", str(config.timeout))
        config_table.add_row("Enabled", str(config.enabled))
        
        self.console.print(config_table)
        
        if Confirm.ask(f"Update configuration for {agent_name}?"):
            model = Prompt.ask("Model", default=config.model)
            temp = float(Prompt.ask("Temperature", default=str(config.temperature)))
            tokens = int(Prompt.ask("Max tokens", default=str(config.max_tokens)))
            timeout = int(Prompt.ask("Timeout", default=str(config.timeout)))
            
            self.launcher.configure_agent(
                agent_name,
                model=model,
                temperature=temp,
                max_tokens=tokens,
                timeout=timeout
            )
            
            self.console.print(f"[green]✅ Configuration updated for {agent_name}[/green]")
    
    def _manage_api_keys(self):
        """Manage API keys"""
        services = ["openai", "anthropic", "brave", "github", "google", "slack"]
        
        self.console.print("\nAPI Key Management:")
        
        choice = Prompt.ask("Choose action", choices=["view", "set", "back"], default="view")
        
        if choice == "view":
            configured_keys = self.config_manager._get_configured_api_keys()
            
            table = Table(title="Configured API Keys")
            table.add_column("Service", style="cyan")
            table.add_column("Status", style="green")
            
            for service in services:
                key_name = f"{service.upper()}_API_KEY"
                status = "✅ Configured" if key_name in configured_keys else "❌ Not set"
                table.add_row(service.title(), status)
            
            self.console.print(table)
        
        elif choice == "set":
            service = Prompt.ask("Select service", choices=services)
            api_key = Prompt.ask(f"Enter {service} API key", password=True)
            
            self.config_manager.set_api_key(service, api_key)
            self.console.print(f"[green]✅ API key set for {service}[/green]")
    
    def _backup_config(self):
        """Backup configuration"""
        backup_path = self.config_manager.backup_configs()
        self.console.print(f"[green]✅ Configuration backup created: {backup_path}[/green]")
    
    def _restore_config(self):
        """Restore configuration from backup"""
        backup_file = Prompt.ask("Enter backup file path")
        
        try:
            self.config_manager.restore_configs(backup_file)
            self.console.print(f"[green]✅ Configuration restored from {backup_file}[/green]")
        except Exception as e:
            self.console.print(f"[red]❌ Failed to restore configuration: {e}[/red]")
    
    def _export_config(self):
        """Export configuration"""
        export_path = self.launcher.export_configuration()
        self.console.print(f"[green]✅ Configuration exported to: {export_path}[/green]")
    
    def _monitoring_menu(self):
        """Monitoring and health menu"""
        while True:
            self.console.print("\n[bold cyan]📊 Monitoring & Health[/bold cyan]")
            
            choice = Prompt.ask(
                "Choose action",
                choices=["health", "metrics", "performance", "logs", "back"],
                default="health"
            )
            
            if choice == "health":
                self._show_health_summary()
            elif choice == "metrics":
                self._show_system_metrics()
            elif choice == "performance":
                self._show_performance_report()
            elif choice == "logs":
                self._show_logs()
            elif choice == "back":
                break
    
    def _show_health_summary(self):
        """Show system health summary"""
        health = self.launcher.status_monitor.get_health_summary()
        
        # Health status panel
        status_color = {
            "healthy": "green",
            "warning": "yellow",
            "critical": "red",
            "error": "red"
        }.get(health["overall_status"], "white")
        
        status_text = f"""
**Overall Status:** [{status_color}]{health['overall_status'].upper()}[/{status_color}]

**System Metrics:**
- CPU Usage: {health['system_metrics'].get('cpu_percent', 0):.1f}%
- Memory Usage: {health['system_metrics'].get('memory_percent', 0):.1f}%
- Disk Usage: {health['system_metrics'].get('disk_percent', 0):.1f}%

**Agents:**
- Total: {health['total_agents']}
- Healthy: {health['healthy_agents']}
- Active: {health['system_metrics'].get('active_agents', 0)}
        """
        
        self.console.print(Panel(Markdown(status_text), title="System Health", border_style=status_color))
        
        # Issues
        if health["issues"]:
            issues_text = "\n".join(f"⚠️ {issue}" for issue in health["issues"])
            self.console.print(Panel(issues_text, title="Issues", border_style="yellow"))
    
    def _show_system_metrics(self):
        """Show detailed system metrics"""
        metrics = self.launcher.status_monitor.get_system_metrics()
        
        table = Table(title="System Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("CPU Usage", f"{metrics.get('cpu_percent', 0):.1f}%")
        table.add_row("Memory Usage", f"{metrics.get('memory_percent', 0):.1f}%")
        table.add_row("Available Memory", f"{metrics.get('memory_available_gb', 0):.1f} GB")
        table.add_row("Disk Usage", f"{metrics.get('disk_percent', 0):.1f}%")
        table.add_row("Free Disk Space", f"{metrics.get('disk_free_gb', 0):.1f} GB")
        table.add_row("Active Agents", str(metrics.get('active_agents', 0)))
        
        self.console.print(table)
    
    def _show_performance_report(self):
        """Show performance report"""
        report = self.launcher.status_monitor.get_performance_report()
        
        if "overall_performance" in report:
            perf = report["overall_performance"]
            
            perf_text = f"""
**Overall Performance:**
- Total Agents: {perf['total_agents']}
- Total Requests: {perf['total_requests']}
- Error Rate: {perf['overall_error_rate']:.2f}%
- Average CPU: {perf['avg_cpu_across_agents']:.1f}%
- Total Memory: {perf['total_memory_mb']:.1f} MB
            """
            
            self.console.print(Panel(Markdown(perf_text), title="Performance Report", border_style="blue"))
    
    def _show_logs(self):
        """Show recent logs"""
        log_file = Path("master_agent_menu.log")
        
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    recent_lines = lines[-20:]  # Last 20 lines
                
                log_text = "".join(recent_lines)
                syntax = Syntax(log_text, "log", theme="monokai", word_wrap=True)
                self.console.print(Panel(syntax, title="Recent Logs", border_style="white"))
                
            except Exception as e:
                self.console.print(f"[red]Error reading log file: {e}[/red]")
        else:
            self.console.print("[yellow]No log file found[/yellow]")
    
    def _documentation_menu(self):
        """Documentation and help menu"""
        while True:
            self.console.print("\n[bold cyan]📚 Documentation & Help[/bold cyan]")
            
            choice = Prompt.ask(
                "Choose action",
                choices=["quick_start", "examples", "troubleshooting", "api_docs", "back"],
                default="quick_start"
            )
            
            if choice == "quick_start":
                self._show_quick_start()
            elif choice == "examples":
                self._show_examples()
            elif choice == "troubleshooting":
                self._show_troubleshooting()
            elif choice == "api_docs":
                self._show_api_docs()
            elif choice == "back":
                break
    
    def _show_quick_start(self):
        """Show quick start guide"""
        quick_start = """
# 🚀 Quick Start Guide

## 1. First Time Setup
1. Configure API keys: Menu → Configuration → API Keys
2. Install dependencies for agents you want to use
3. Test with a simple agent launch

## 2. Basic Workflow
1. **Discover agents**: Use "List & Search" to find agents
2. **Configure**: Set up API keys and agent parameters
3. **Launch**: Start agents from "Manage Agents"
4. **Monitor**: Check status and health

## 3. Agent Combinations
1. **Explore existing**: View available combinations
2. **Create custom**: Combine agents for complex tasks
3. **Launch workflows**: Execute multi-agent processes

## 4. Common Commands
- List agents: Menu → List & Search → List
- Launch agent: Menu → Manage → Launch
- Check status: Menu → Manage → Status
- Create combination: Menu → Combinations → Create
        """
        
        self.console.print(Panel(Markdown(quick_start), title="Quick Start Guide", border_style="green"))
    
    def _show_examples(self):
        """Show usage examples"""
        examples = """
# 📝 Usage Examples

## Basic Agent Launch
1. Go to "Manage Agents" → "Launch"
2. Enter agent name (e.g., "ask-reddit-agent")
3. Agent will validate and start

## Research Pipeline
1. Create combination with:
   - advanced-web-researcher
   - foundational-rag-agent
   - linkedin-x-blog-content-creator
2. Launch with topic: "AI trends 2024"
3. Get research → knowledge → content

## Social Media Analysis
1. Use existing "social-media-analytics-agent" combination
2. Input: "gaming trends"
3. Analyzes Reddit + YouTube + generates content

## Configuration Example
1. Go to Configuration → Agent
2. Select "ask-reddit-agent"
3. Set model: "gpt-4o"
4. Set temperature: 0.7
5. Save configuration
        """
        
        self.console.print(Panel(Markdown(examples), title="Usage Examples", border_style="blue"))
    
    def _show_troubleshooting(self):
        """Show troubleshooting guide"""
        troubleshooting = """
# 🔧 Troubleshooting

## Common Issues

### Agent Won't Launch
- ✅ Check API keys are configured
- ✅ Verify dependencies are installed
- ✅ Check agent validation results
- ✅ Review logs for error details

### High Resource Usage
- 🔍 Check system metrics in Monitoring
- 🔧 Adjust agent configurations
- 🛑 Stop unused agents
- 📊 Monitor performance reports

### Combination Failures
- 🔍 Verify all component agents exist
- ⚙️ Check individual agent configurations
- 📝 Review combination workflow definition
- 🔄 Test agents individually first

### API Key Issues
- 🔑 Ensure keys are correctly formatted
- 🔍 Check service-specific requirements
- 🔄 Regenerate keys if needed
- 📁 Verify .env file permissions

### Performance Issues
- 💾 Check available system memory
- 🖥️ Monitor CPU usage
- 📊 Review agent metrics
- 🔧 Adjust timeout settings
        """
        
        self.console.print(Panel(Markdown(troubleshooting), title="Troubleshooting Guide", border_style="yellow"))
    
    def _show_api_docs(self):
        """Show API documentation"""
        api_docs = """
# 📖 API Documentation

## Core Classes

### AgentLauncher
Main interface for agent management
```python
launcher = AgentLauncher()
launcher.list_agents()
launcher.launch_agent("agent-name")
launcher.stop_agent("agent-name")
```

### ConfigurationManager
Handles agent configuration
```python
config_manager.configure_agent("agent-name", model="gpt-4o")
config_manager.set_api_key("openai", "your-key")
```

### CombinationEngine
Creates and executes agent combinations
```python
engine.create_combination("my-combo", ["agent1", "agent2"])
engine.launch_combination("my-combo", input_data)
```

## Command Line Usage
```bash
python main.py                 # Interactive menu
python main.py --list         # List all agents
python main.py --launch agent # Launch specific agent
python main.py --status       # Show status
```
        """
        
        self.console.print(Panel(Markdown(api_docs), title="API Documentation", border_style="cyan"))
    
    def _system_menu(self):
        """System management menu"""
        while True:
            self.console.print("\n[bold cyan]🛠️ System Management[/bold cyan]")
            
            choice = Prompt.ask(
                "Choose action",
                choices=["refresh", "cleanup", "update", "stats", "back"],
                default="stats"
            )
            
            if choice == "refresh":
                self._refresh_registry()
            elif choice == "cleanup":
                self._cleanup_system()
            elif choice == "update":
                self._update_system()
            elif choice == "stats":
                self._show_system_stats()
            elif choice == "back":
                break
    
    def _refresh_registry(self):
        """Refresh agent registry"""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Refreshing agent registry...", total=None)
            self.launcher.registry.discover_agents()
            self.launcher.registry.save_registry()
        
        stats = self.launcher.registry.get_statistics()
        self.console.print(f"[green]✅ Registry refreshed: {stats['total_agents']} agents discovered[/green]")
    
    def _cleanup_system(self):
        """Clean up system resources"""
        if Confirm.ask("Clean up system resources? This will stop all running agents."):
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                task = progress.add_task("Cleaning up system...", total=None)
                self.launcher.cleanup()
            
            self.console.print("[green]✅ System cleanup completed[/green]")
    
    def _update_system(self):
        """Update system components"""
        self.console.print("[yellow]Update functionality not implemented yet[/yellow]")
        self.console.print("To update:")
        self.console.print("1. Pull latest changes from git repository")
        self.console.print("2. Update Python dependencies: pip install -r requirements.txt")
        self.console.print("3. Restart the system")
    
    def _show_system_stats(self):
        """Show comprehensive system statistics"""
        system_info = self.launcher.get_system_info()
        registry_stats = self.launcher.registry.get_statistics()
        
        # System info
        sys_table = Table(title="System Information")
        sys_table.add_column("Property", style="cyan")
        sys_table.add_column("Value", style="white")
        
        sys_table.add_row("Repository Root", str(system_info["repository_root"]))
        sys_table.add_row("Python Version", system_info["python_version"])
        sys_table.add_row("System Time", system_info["system_time"])
        
        self.console.print(sys_table)
        
        # Agent statistics
        agent_table = Table(title="Agent Statistics")
        agent_table.add_column("Category", style="cyan")
        agent_table.add_column("Count", style="green")
        
        for category, count in registry_stats["agents_by_category"].items():
            agent_table.add_row(category, str(count))
        
        self.console.print(agent_table)
        
        # Configuration summary
        config_summary = self.config_manager.get_config_summary()
        config_table = Table(title="Configuration Summary")
        config_table.add_column("Property", style="cyan")
        config_table.add_column("Value", style="white")
        
        config_table.add_row("Configured Agents", str(config_summary["total_agents_configured"]))
        config_table.add_row("API Keys", str(len(config_summary["api_keys_configured"])))
        config_table.add_row("Config Directory", config_summary["config_directory"])
        
        self.console.print(config_table)
    
    def _exit_system(self):
        """Exit the system safely"""
        self.console.print("\n[yellow]Shutting down Master Agent Menu...[/yellow]")
        
        # Stop any running agents
        if self.launcher.running_agents:
            self.console.print("Stopping running agents...")
            self.launcher.stop_all_agents()
        
        # Cleanup resources
        self.launcher.cleanup()
        
        self.console.print("[green]✅ Goodbye![/green]")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Master Agent Menu System")
    parser.add_argument("--list", action="store_true", help="List all agents")
    parser.add_argument("--launch", help="Launch specific agent")
    parser.add_argument("--stop", help="Stop specific agent")
    parser.add_argument("--status", action="store_true", help="Show agent status")
    parser.add_argument("--combinations", action="store_true", help="List combinations")
    
    args = parser.parse_args()
    
    # Handle command line arguments
    if any(vars(args).values()):
        launcher = AgentLauncher()
        console = Console()
        
        if args.list:
            agents = launcher.list_agents()
            table = Table(title="Available Agents")
            table.add_column("Name", style="cyan")
            table.add_column("Category", style="green")
            table.add_column("Description", style="white")
            
            for agent in agents:
                description = agent.description[:60] + "..." if len(agent.description) > 60 else agent.description
                table.add_row(agent.name, agent.category, description)
            
            console.print(table)
        
        elif args.launch:
            success = launcher.launch_agent(args.launch)
            if success:
                console.print(f"[green]✅ Launched {args.launch}[/green]")
            else:
                console.print(f"[red]❌ Failed to launch {args.launch}[/red]")
        
        elif args.stop:
            success = launcher.stop_agent(args.stop)
            if success:
                console.print(f"[green]✅ Stopped {args.stop}[/green]")
            else:
                console.print(f"[red]❌ Failed to stop {args.stop}[/red]")
        
        elif args.status:
            statuses = launcher.get_all_statuses()
            table = Table(title="Agent Status")
            table.add_column("Agent", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("PID", style="yellow")
            
            for name, status in statuses.items():
                status_text = "🟢 Running" if status["is_running"] else "⚪ Stopped"
                pid = str(status.get('pid', '-'))
                table.add_row(name, status_text, pid)
            
            console.print(table)
        
        elif args.combinations:
            combinations = launcher.list_combinations()
            table = Table(title="Available Combinations")
            table.add_column("Name", style="cyan")
            table.add_column("Components", style="green")
            
            for combo in combinations:
                components = ", ".join(combo.component_agents[:3])
                if len(combo.component_agents) > 3:
                    components += f" (+{len(combo.component_agents) - 3} more)"
                table.add_row(combo.name, components)
            
            console.print(table)
        
        launcher.cleanup()
    else:
        # Interactive mode
        try:
            menu = MasterAgentMenu()
            menu.run()
        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:
            logging.error(f"Fatal error: {e}")
            print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()