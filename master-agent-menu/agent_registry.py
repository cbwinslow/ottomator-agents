"""
Agent Registry - Discovers and catalogs all available agents in the repository
"""

import os
import json
import yaml
import glob
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentInfo:
    """Information about a discovered agent"""
    name: str
    path: str
    category: str
    description: str
    main_file: str
    config_files: List[str]
    requirements_file: Optional[str]
    readme_file: Optional[str]
    dependencies: List[str]
    api_keys_required: List[str]
    supported_models: List[str]
    last_modified: datetime
    status: str = "discovered"  # discovered, configured, active, inactive, error

@dataclass
class AgentCombination:
    """Information about agent combinations"""
    name: str
    description: str
    component_agents: List[str]
    workflow: Dict[str, Any]
    benefits: List[str]
    use_cases: List[str]

class AgentRegistry:
    """Discovers and manages all available agents"""
    
    def __init__(self, repo_root: str = None):
        if repo_root is None:
            # Go up one level from master-agent-menu to the repo root
            self.repo_root = Path(__file__).parent.parent.absolute()
        else:
            self.repo_root = Path(repo_root).absolute()
        
        self.agents: Dict[str, AgentInfo] = {}
        self.combinations: Dict[str, AgentCombination] = {}
        self.agent_categories = {
            "mcp": ["mcp-agent-army", "pydantic-ai-mcp-agent", "simple-mcp-agent", "n8n-mcp-agent", "thirdbrain-mcp-openai-agent"],
            "research": ["advanced-web-researcher", "general-researcher-agent", "small-business-researcher"],
            "knowledge": ["agentic-rag-knowledge-graph", "foundational-rag-agent", "light-rag-agent", "r1-distill-rag", "contextual-retrieval-n8n-agent"],
            "content": ["linkedin-x-blog-content-creator", "tweet-generator-agent", "youtube-educator-plus-agent", "genericsuite-app-maker-agent"],
            "business": ["gilbert-real-estate-agent", "bali-property-agent", "enish-restaurant-booking-agent", "intelligent-invoicing-agent", "lead-generator-agent"],
            "social": ["ask-reddit-agent", "nba-agent"],
            "web": ["crawl4AI-agent", "crawl4AI-agent-v2", "multi-page-scraper-agent", "file-agent"],
            "travel": ["travel-agent"],
            "media": ["youtube-summary-agent", "youtube-video-summarizer", "streambuzz-agent"],
            "tech": ["tech-stack-expert", "n8n-expert", "bolt.diy-expert", "python-local-ai-agent", "local-ai-expert"],
            "specialized": ["indoor-farming-agent", "course-guider-agent", "dynamic-chatbot-agent", "TinyDM-agent"],
            "tools": ["smart-select-multi-tool-agent", "mem0-agent", "graphiti-agent"],
            "integration": ["n8n-github-assistant", "n8n-youtube-agent", "n8n-openwebui-agent", "google-a2a-agent", "pydantic-github-agent"],
            "experimental": ["ottomarkdown-agent", "pydantic-ai-advanced-researcher", "pydantic-ai-langfuse", "pydantic-ai-langgraph-parallelization", "openai-sdk-agent"]
        }
        
    def discover_agents(self) -> None:
        """Discover all agents in the repository"""
        logger.info(f"Discovering agents in {self.repo_root}")
        
        # Get all directories that might contain agents
        potential_agent_dirs = [d for d in self.repo_root.iterdir() 
                              if d.is_dir() and not d.name.startswith('.') 
                              and d.name != 'master-agent-menu']
        
        for agent_dir in potential_agent_dirs:
            try:
                agent_info = self._analyze_agent_directory(agent_dir)
                if agent_info:
                    self.agents[agent_info.name] = agent_info
                    logger.info(f"Discovered agent: {agent_info.name} ({agent_info.category})")
            except Exception as e:
                logger.warning(f"Error analyzing {agent_dir.name}: {e}")
        
        logger.info(f"Discovered {len(self.agents)} agents")
        self._setup_default_combinations()
    
    def _analyze_agent_directory(self, agent_dir: Path) -> Optional[AgentInfo]:
        """Analyze a directory to determine if it contains an agent"""
        
        # Skip certain directories
        skip_dirs = {'__pycache__', '.git', 'node_modules', '.env', 'venv', 'env'}
        if agent_dir.name in skip_dirs or agent_dir.name.startswith('~'):
            return None
        
        # Look for Python files that might be main entry points
        python_files = list(agent_dir.glob("*.py"))
        main_candidates = []
        
        for py_file in python_files:
            name = py_file.stem.lower()
            if any(keyword in name for keyword in ['main', 'app', 'agent', 'run']):
                main_candidates.append(py_file)
        
        # If no obvious main file, take the first Python file or check for specific patterns
        if not main_candidates and python_files:
            main_candidates = [python_files[0]]
        
        if not main_candidates:
            # Check for other indicators of an agent (README, requirements, etc.)
            has_readme = any(agent_dir.glob("README*"))
            has_requirements = any(agent_dir.glob("requirements.txt"))
            if not (has_readme or has_requirements):
                return None
            main_candidates = ["(no main file found)"]
        
        # Determine category
        category = self._categorize_agent(agent_dir.name)
        
        # Get description from README if available
        description = self._extract_description(agent_dir)
        
        # Find configuration files
        config_files = []
        for pattern in ["*.json", "*.yaml", "*.yml", "*.toml", ".env*"]:
            config_files.extend([str(f.relative_to(agent_dir)) for f in agent_dir.glob(pattern)])
        
        # Find README
        readme_file = None
        for readme_pattern in ["README*", "readme*"]:
            readme_files = list(agent_dir.glob(readme_pattern))
            if readme_files:
                readme_file = str(readme_files[0].relative_to(agent_dir))
                break
        
        # Find requirements file
        requirements_file = None
        req_files = list(agent_dir.glob("requirements.txt"))
        if req_files:
            requirements_file = str(req_files[0].relative_to(agent_dir))
        
        # Extract dependencies and API keys
        dependencies, api_keys = self._extract_dependencies_and_keys(agent_dir)
        
        # Get last modified time
        try:
            last_modified = datetime.fromtimestamp(agent_dir.stat().st_mtime)
        except:
            last_modified = datetime.now()
        
        return AgentInfo(
            name=agent_dir.name,
            path=str(agent_dir.relative_to(self.repo_root)),
            category=category,
            description=description,
            main_file=str(main_candidates[0]) if main_candidates and isinstance(main_candidates[0], Path) else str(main_candidates[0]),
            config_files=config_files,
            requirements_file=requirements_file,
            readme_file=readme_file,
            dependencies=dependencies,
            api_keys_required=api_keys,
            supported_models=self._extract_supported_models(agent_dir),
            last_modified=last_modified
        )
    
    def _categorize_agent(self, agent_name: str) -> str:
        """Categorize an agent based on its name and characteristics"""
        agent_name_lower = agent_name.lower()
        
        for category, agents in self.agent_categories.items():
            if agent_name in agents:
                return category
        
        # Fallback categorization based on name patterns
        if any(keyword in agent_name_lower for keyword in ['mcp', 'protocol']):
            return 'mcp'
        elif any(keyword in agent_name_lower for keyword in ['research', 'search', 'web']):
            return 'research'
        elif any(keyword in agent_name_lower for keyword in ['rag', 'knowledge', 'graph']):
            return 'knowledge'
        elif any(keyword in agent_name_lower for keyword in ['content', 'create', 'generate', 'write']):
            return 'content'
        elif any(keyword in agent_name_lower for keyword in ['business', 'real', 'estate', 'booking', 'invoice']):
            return 'business'
        elif any(keyword in agent_name_lower for keyword in ['social', 'reddit', 'twitter', 'linkedin']):
            return 'social'
        elif any(keyword in agent_name_lower for keyword in ['crawl', 'scrape', 'file']):
            return 'web'
        elif any(keyword in agent_name_lower for keyword in ['youtube', 'video', 'media']):
            return 'media'
        elif any(keyword in agent_name_lower for keyword in ['travel', 'trip']):
            return 'travel'
        else:
            return 'specialized'
    
    def _extract_description(self, agent_dir: Path) -> str:
        """Extract description from README or other documentation"""
        readme_files = list(agent_dir.glob("README*")) + list(agent_dir.glob("readme*"))
        
        if readme_files:
            try:
                content = readme_files[0].read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                # Look for the first meaningful description
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and len(line) > 20:
                        return line[:200] + "..." if len(line) > 200 else line
                
                # If no description found, use the first header
                for line in lines:
                    if line.startswith('#'):
                        return line.strip('#').strip()
                
            except Exception:
                pass
        
        return f"AI Agent: {agent_dir.name.replace('-', ' ').title()}"
    
    def _extract_dependencies_and_keys(self, agent_dir: Path) -> tuple[List[str], List[str]]:
        """Extract dependencies and required API keys"""
        dependencies = []
        api_keys = []
        
        # Check requirements.txt
        req_file = agent_dir / "requirements.txt"
        if req_file.exists():
            try:
                content = req_file.read_text(encoding='utf-8', errors='ignore')
                # Extract package names (handle potential encoding issues)
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Handle potential encoding artifacts
                        clean_line = ''.join(c for c in line if c.isprintable())
                        if '==' in clean_line:
                            pkg = clean_line.split('==')[0].strip()
                            if pkg and len(pkg) > 1:
                                dependencies.append(pkg)
            except Exception:
                pass
        
        # Check for common API key patterns in files
        for pattern in ["*.py", "*.env*", "*.json", "*.yaml", "*.yml"]:
            for file_path in agent_dir.glob(pattern):
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    # Look for API key patterns
                    import re
                    key_patterns = [
                        r'(\w+_API_KEY)',
                        r'(\w+_TOKEN)',
                        r'(\w+_SECRET)',
                        r'getenv\(["\']([^"\']*API[^"\']*)["\']',
                        r'getenv\(["\']([^"\']*TOKEN[^"\']*)["\']',
                        r'getenv\(["\']([^"\']*KEY[^"\']*)["\']'
                    ]
                    
                    for pattern in key_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            if isinstance(match, tuple):
                                match = match[0] if match[0] else match[1]
                            if match and match not in api_keys:
                                api_keys.append(match)
                except Exception:
                    continue
        
        return dependencies[:20], api_keys[:10]  # Limit to prevent excessive lists
    
    def _extract_supported_models(self, agent_dir: Path) -> List[str]:
        """Extract supported models from agent code"""
        models = []
        
        for py_file in agent_dir.glob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                
                # Look for common model patterns
                import re
                model_patterns = [
                    r'["\']gpt-[^"\']*["\']',
                    r'["\']claude-[^"\']*["\']',
                    r'["\']anthropic[^"\']*["\']',
                    r'["\']gemini[^"\']*["\']',
                    r'["\']llama[^"\']*["\']',
                    r'MODEL_CHOICE[^"\']*["\']([^"\']*)["\']'
                ]
                
                for pattern in model_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        clean_match = match.strip('\'"')
                        if clean_match and clean_match not in models:
                            models.append(clean_match)
                            
            except Exception:
                continue
        
        return models[:5]  # Limit to prevent excessive lists
    
    def _setup_default_combinations(self):
        """Setup default agent combinations"""
        combinations = [
            AgentCombination(
                name="multi-modal-research-agent",
                description="Comprehensive research agent combining web search, knowledge retrieval, and content generation",
                component_agents=["advanced-web-researcher", "foundational-rag-agent", "linkedin-x-blog-content-creator"],
                workflow={
                    "step1": "Use web researcher to gather current information",
                    "step2": "Use RAG agent to retrieve relevant knowledge",
                    "step3": "Use content creator to synthesize findings"
                },
                benefits=[
                    "Combines real-time web data with stored knowledge",
                    "Produces professional content output",
                    "Comprehensive research coverage"
                ],
                use_cases=[
                    "Market research reports",
                    "Technical documentation",
                    "Content marketing materials"
                ]
            ),
            AgentCombination(
                name="business-intelligence-agent",
                description="Business analysis agent combining market research, data analysis, and reporting",
                component_agents=["small-business-researcher", "advanced-web-researcher", "genericsuite-app-maker-agent"],
                workflow={
                    "step1": "Research business domain and competitors",
                    "step2": "Gather market data and trends",
                    "step3": "Generate business intelligence reports"
                },
                benefits=[
                    "Comprehensive market analysis",
                    "Competitive intelligence",
                    "Automated report generation"
                ],
                use_cases=[
                    "Market entry analysis",
                    "Competitive analysis",
                    "Business planning"
                ]
            ),
            AgentCombination(
                name="social-media-analytics-agent",
                description="Social media intelligence combining Reddit analysis, YouTube research, and content creation",
                component_agents=["ask-reddit-agent", "youtube-summary-agent", "tweet-generator-agent"],
                workflow={
                    "step1": "Analyze Reddit discussions and trends",
                    "step2": "Research YouTube content and engagement",
                    "step3": "Generate social media content strategy"
                },
                benefits=[
                    "Multi-platform social intelligence",
                    "Trend identification",
                    "Content strategy automation"
                ],
                use_cases=[
                    "Social media marketing",
                    "Trend analysis",
                    "Content planning"
                ]
            ),
            AgentCombination(
                name="real-estate-intelligence-agent",
                description="Real estate analysis combining property research, market analysis, and content creation",
                component_agents=["gilbert-real-estate-agent", "bali-property-agent", "advanced-web-researcher"],
                workflow={
                    "step1": "Research property markets and listings",
                    "step2": "Analyze market trends and pricing",
                    "step3": "Generate property reports and marketing materials"
                },
                benefits=[
                    "Multi-market property analysis",
                    "Automated valuation insights",
                    "Marketing material generation"
                ],
                use_cases=[
                    "Property investment analysis",
                    "Market research",
                    "Real estate marketing"
                ]
            ),
            AgentCombination(
                name="educational-content-agent",
                description="Educational material creation combining research, knowledge graphs, and multimedia generation",
                component_agents=["general-researcher-agent", "agentic-rag-knowledge-graph", "youtube-educator-plus-agent"],
                workflow={
                    "step1": "Research educational topic comprehensively",
                    "step2": "Map knowledge relationships and concepts",
                    "step3": "Create multimedia educational content"
                },
                benefits=[
                    "Comprehensive topic coverage",
                    "Knowledge relationship mapping",
                    "Multi-format content creation"
                ],
                use_cases=[
                    "Course material development",
                    "Educational video creation",
                    "Training program design"
                ]
            ),
            AgentCombination(
                name="financial-analysis-agent",
                description="Financial research and analysis combining market research, data analysis, and reporting",
                component_agents=["advanced-web-researcher", "nba-agent", "genericsuite-app-maker-agent"],
                workflow={
                    "step1": "Research financial markets and trends",
                    "step2": "Analyze data patterns and metrics",
                    "step3": "Generate financial reports and insights"
                },
                benefits=[
                    "Real-time market analysis",
                    "Pattern recognition",
                    "Automated reporting"
                ],
                use_cases=[
                    "Investment research",
                    "Financial planning",
                    "Market analysis"
                ]
            )
        ]
        
        for combo in combinations:
            self.combinations[combo.name] = combo
    
    def get_agents_by_category(self, category: str) -> List[AgentInfo]:
        """Get all agents in a specific category"""
        return [agent for agent in self.agents.values() if agent.category == category]
    
    def get_agent(self, name: str) -> Optional[AgentInfo]:
        """Get agent by name"""
        return self.agents.get(name)
    
    def search_agents(self, query: str) -> List[AgentInfo]:
        """Search agents by name or description"""
        query_lower = query.lower()
        results = []
        
        for agent in self.agents.values():
            if (query_lower in agent.name.lower() or 
                query_lower in agent.description.lower() or
                any(query_lower in dep.lower() for dep in agent.dependencies)):
                results.append(agent)
        
        return results
    
    def save_registry(self, filepath: str = None):
        """Save the registry to a JSON file"""
        if filepath is None:
            filepath = self.repo_root / "master-agent-menu" / "agent_registry.json"
        
        data = {
            "agents": {name: asdict(agent) for name, agent in self.agents.items()},
            "combinations": {name: asdict(combo) for name, combo in self.combinations.items()},
            "last_updated": datetime.now().isoformat()
        }
        
        # Convert datetime objects to strings for JSON serialization
        for agent_data in data["agents"].values():
            if isinstance(agent_data["last_modified"], datetime):
                agent_data["last_modified"] = agent_data["last_modified"].isoformat()
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"Registry saved to {filepath}")
    
    def load_registry(self, filepath: str = None):
        """Load the registry from a JSON file"""
        if filepath is None:
            filepath = self.repo_root / "master-agent-menu" / "agent_registry.json"
        
        if not os.path.exists(filepath):
            logger.warning(f"Registry file not found: {filepath}")
            return
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Load agents
        for name, agent_data in data.get("agents", {}).items():
            # Convert string datetime back to datetime object
            if isinstance(agent_data["last_modified"], str):
                agent_data["last_modified"] = datetime.fromisoformat(agent_data["last_modified"])
            self.agents[name] = AgentInfo(**agent_data)
        
        # Load combinations
        for name, combo_data in data.get("combinations", {}).items():
            self.combinations[name] = AgentCombination(**combo_data)
        
        logger.info(f"Registry loaded from {filepath}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics"""
        category_counts = {}
        for agent in self.agents.values():
            category_counts[agent.category] = category_counts.get(agent.category, 0) + 1
        
        return {
            "total_agents": len(self.agents),
            "total_combinations": len(self.combinations),
            "agents_by_category": category_counts,
            "categories": list(category_counts.keys()),
            "api_keys_required": list(set([key for agent in self.agents.values() for key in agent.api_keys_required])),
            "common_dependencies": self._get_common_dependencies()
        }
    
    def _get_common_dependencies(self) -> List[str]:
        """Get most common dependencies across all agents"""
        dep_counts = {}
        for agent in self.agents.values():
            for dep in agent.dependencies:
                dep_counts[dep] = dep_counts.get(dep, 0) + 1
        
        # Return top 10 most common dependencies
        sorted_deps = sorted(dep_counts.items(), key=lambda x: x[1], reverse=True)
        return [dep for dep, count in sorted_deps[:10]]

if __name__ == "__main__":
    # Test the registry
    registry = AgentRegistry()
    registry.discover_agents()
    
    print(f"Discovered {len(registry.agents)} agents")
    print(f"Categories: {list(set(agent.category for agent in registry.agents.values()))}")
    
    # Print some example agents
    for category in ["mcp", "research", "content"]:
        agents = registry.get_agents_by_category(category)
        if agents:
            print(f"\n{category.title()} agents:")
            for agent in agents[:3]:  # Show first 3
                print(f"  - {agent.name}: {agent.description[:100]}...")
    
    # Save registry
    registry.save_registry()
    print(f"\nRegistry saved with {len(registry.agents)} agents and {len(registry.combinations)} combinations")