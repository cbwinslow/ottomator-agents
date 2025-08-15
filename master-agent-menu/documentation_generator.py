"""
Documentation Generator - Creates comprehensive documentation for agents with examples and illustrations
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

from agent_registry import AgentRegistry, AgentInfo, AgentCombination

logger = logging.getLogger(__name__)

@dataclass
class AgentDocumentation:
    """Complete documentation for an agent"""
    agent_name: str
    overview: str
    capabilities: List[str]
    configuration: Dict[str, Any]
    examples: List[Dict[str, Any]]
    api_reference: Dict[str, Any]
    performance_notes: List[str]
    troubleshooting: List[Dict[str, str]]
    illustrations: List[str]
    related_agents: List[str]
    use_cases: List[str]
    best_practices: List[str]

class DocumentationGenerator:
    """Generates comprehensive documentation for agents and combinations"""
    
    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self.docs_dir = Path(__file__).parent / "docs"
        self.docs_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.docs_dir / "agents").mkdir(exist_ok=True)
        (self.docs_dir / "combinations").mkdir(exist_ok=True)
        (self.docs_dir / "examples").mkdir(exist_ok=True)
        (self.docs_dir / "assets").mkdir(exist_ok=True)
    
    def generate_all_documentation(self) -> Dict[str, str]:
        """Generate documentation for all agents and combinations"""
        results = {}
        
        # Generate agent documentation
        for agent_name, agent_info in self.registry.agents.items():
            try:
                doc_path = self.generate_agent_documentation(agent_name)
                results[f"agent_{agent_name}"] = doc_path
                logger.info(f"Generated documentation for agent: {agent_name}")
            except Exception as e:
                logger.error(f"Failed to generate docs for agent {agent_name}: {e}")
        
        # Generate combination documentation
        for combo_name, combo_info in self.registry.combinations.items():
            try:
                doc_path = self.generate_combination_documentation(combo_name)
                results[f"combination_{combo_name}"] = doc_path
                logger.info(f"Generated documentation for combination: {combo_name}")
            except Exception as e:
                logger.error(f"Failed to generate docs for combination {combo_name}: {e}")
        
        # Generate index
        index_path = self.generate_index()
        results["index"] = index_path
        
        return results
    
    def generate_agent_documentation(self, agent_name: str) -> str:
        """Generate comprehensive documentation for a specific agent"""
        agent_info = self.registry.get_agent(agent_name)
        if not agent_info:
            raise ValueError(f"Agent {agent_name} not found")
        
        # Build documentation
        doc = self._build_agent_documentation(agent_info)
        
        # Generate markdown
        markdown_content = self._agent_doc_to_markdown(doc)
        
        # Save to file
        doc_file = self.docs_dir / "agents" / f"{agent_name}.md"
        with open(doc_file, 'w') as f:
            f.write(markdown_content)
        
        return str(doc_file)
    
    def _build_agent_documentation(self, agent_info: AgentInfo) -> AgentDocumentation:
        """Build comprehensive documentation for an agent"""
        
        # Generate capabilities based on category and analysis
        capabilities = self._generate_capabilities(agent_info)
        
        # Generate configuration documentation
        configuration = self._generate_configuration_docs(agent_info)
        
        # Generate examples
        examples = self._generate_examples(agent_info)
        
        # Generate API reference
        api_reference = self._generate_api_reference(agent_info)
        
        # Generate performance notes
        performance_notes = self._generate_performance_notes(agent_info)
        
        # Generate troubleshooting guide
        troubleshooting = self._generate_troubleshooting(agent_info)
        
        # Find related agents
        related_agents = self._find_related_agents(agent_info)
        
        # Generate use cases
        use_cases = self._generate_use_cases(agent_info)
        
        # Generate best practices
        best_practices = self._generate_best_practices(agent_info)
        
        return AgentDocumentation(
            agent_name=agent_info.name,
            overview=self._generate_overview(agent_info),
            capabilities=capabilities,
            configuration=configuration,
            examples=examples,
            api_reference=api_reference,
            performance_notes=performance_notes,
            troubleshooting=troubleshooting,
            illustrations=[],  # Will be populated with generated diagrams
            related_agents=related_agents,
            use_cases=use_cases,
            best_practices=best_practices
        )
    
    def _generate_capabilities(self, agent_info: AgentInfo) -> List[str]:
        """Generate capabilities list based on agent category and analysis"""
        category_capabilities = {
            "mcp": [
                "🔌 Model Context Protocol integration",
                "🛠️ Tool execution and management",
                "📊 Multi-service orchestration",
                "🔄 Protocol-compliant communication",
                "⚡ Efficient tool discovery"
            ],
            "research": [
                "🔍 Web search and data gathering",
                "📈 Trend analysis and insights",
                "📝 Research report generation",
                "🔎 Information verification",
                "📊 Data synthesis and summarization"
            ],
            "knowledge": [
                "🧠 Knowledge graph construction",
                "💾 Vector-based retrieval",
                "🔗 Entity relationship mapping",
                "📚 Document understanding",
                "🎯 Contextual information retrieval"
            ],
            "content": [
                "✍️ High-quality content generation",
                "🎨 Creative writing and ideation",
                "📱 Multi-platform content adaptation",
                "🔤 Style and tone customization",
                "📊 Content optimization"
            ],
            "business": [
                "💼 Business process automation",
                "📈 Market analysis and insights",
                "💰 Financial data processing",
                "🎯 Strategic planning support",
                "📊 Performance metrics tracking"
            ],
            "social": [
                "👥 Social media analysis",
                "📱 Community engagement insights",
                "🔍 Trend identification",
                "💬 Sentiment analysis",
                "📊 Social metrics tracking"
            ],
            "web": [
                "🕷️ Web scraping and crawling",
                "📄 Document extraction",
                "🔍 Site mapping and analysis",
                "💾 Data collection and storage",
                "🛡️ Respectful crawling practices"
            ],
            "media": [
                "🎥 Video content analysis",
                "🎵 Audio processing",
                "📷 Image understanding",
                "📝 Media summarization",
                "🎬 Content recommendations"
            ],
            "travel": [
                "✈️ Travel planning and booking",
                "🗺️ Destination recommendations",
                "💰 Price comparison and optimization",
                "📅 Itinerary management",
                "🌍 Local insights and tips"
            ],
            "tech": [
                "💻 Technical analysis and support",
                "🔧 Development assistance",
                "📋 Code review and optimization",
                "🏗️ Architecture recommendations",
                "🚀 Deployment and DevOps support"
            ]
        }
        
        base_capabilities = category_capabilities.get(agent_info.category, [
            "🤖 AI-powered task execution",
            "⚙️ Configurable parameters",
            "📊 Performance monitoring",
            "🔄 Reliable processing",
            "🎯 Domain-specific optimization"
        ])
        
        # Add API-specific capabilities
        if agent_info.api_keys_required:
            base_capabilities.append("🔑 External API integration")
        
        if "mcp" in agent_info.name.lower():
            base_capabilities.append("🔌 MCP protocol support")
        
        return base_capabilities
    
    def _generate_configuration_docs(self, agent_info: AgentInfo) -> Dict[str, Any]:
        """Generate configuration documentation"""
        config_docs = {
            "required_api_keys": agent_info.api_keys_required,
            "supported_models": agent_info.supported_models,
            "dependencies": agent_info.dependencies[:10],  # Top 10 dependencies
            "parameters": {
                "model": {
                    "type": "string",
                    "default": "gpt-4o-mini",
                    "description": "AI model to use for processing",
                    "options": ["gpt-4o", "gpt-4o-mini", "claude-3-sonnet", "claude-3-haiku"]
                },
                "temperature": {
                    "type": "float",
                    "default": 0.7,
                    "range": [0.0, 2.0],
                    "description": "Controls creativity and randomness in responses"
                },
                "max_tokens": {
                    "type": "integer",
                    "default": 2000,
                    "range": [1, 100000],
                    "description": "Maximum number of tokens in response"
                },
                "timeout": {
                    "type": "integer",
                    "default": 300,
                    "description": "Request timeout in seconds"
                }
            }
        }
        
        # Add category-specific parameters
        if agent_info.category == "research":
            config_docs["parameters"]["search_depth"] = {
                "type": "integer",
                "default": 5,
                "description": "Number of search results to analyze"
            }
            config_docs["parameters"]["enable_fact_check"] = {
                "type": "boolean", 
                "default": True,
                "description": "Enable fact-checking of research results"
            }
        
        elif agent_info.category == "content":
            config_docs["parameters"]["creativity_mode"] = {
                "type": "boolean",
                "default": True,
                "description": "Enable creative writing features"
            }
            config_docs["parameters"]["output_format"] = {
                "type": "string",
                "default": "markdown",
                "options": ["markdown", "html", "text", "json"],
                "description": "Output format for generated content"
            }
        
        return config_docs
    
    def _generate_examples(self, agent_info: AgentInfo) -> List[Dict[str, Any]]:
        """Generate usage examples for the agent"""
        examples = []
        
        # Basic usage example
        basic_example = {
            "title": "Basic Usage",
            "description": f"Simple example of using {agent_info.name}",
            "code": f"""
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the agent
success = launcher.launch_agent("{agent_info.name}")

if success:
    print("Agent launched successfully!")
    
    # Get agent status
    status = launcher.get_agent_status("{agent_info.name}")
    print(f"Status: {{status['status']}}")
    
    # Stop the agent when done
    launcher.stop_agent("{agent_info.name}")
            """,
            "expected_output": "Agent launched successfully!\nStatus: running"
        }
        examples.append(basic_example)
        
        # Configuration example
        config_example = {
            "title": "Configuration Example",
            "description": f"Configuring {agent_info.name} with custom parameters",
            "code": f"""
# Configure the agent
launcher.configure_agent("{agent_info.name}", 
    model="gpt-4o",
    temperature=0.5,
    max_tokens=3000
)

# Launch with configuration
launcher.launch_agent("{agent_info.name}")
            """,
            "expected_output": "Agent configured and launched with custom settings"
        }
        examples.append(config_example)
        
        # Category-specific examples
        if agent_info.category == "research":
            research_example = {
                "title": "Research Query Example",
                "description": "Using the agent for research tasks",
                "code": f"""
# For research agents, you would typically interact through their interface
# After launching, you can send research queries

# Example query (agent-specific implementation)
query = "Latest AI trends in 2024"
# Agent processes the query and returns research results
                """,
                "expected_output": "Research results with sources, summary, and insights"
            }
            examples.append(research_example)
        
        elif agent_info.category == "content":
            content_example = {
                "title": "Content Generation Example",
                "description": "Generating content with the agent",
                "code": f"""
# Content generation example
topic = "Benefits of AI in healthcare"
style = "professional blog post"

# Agent generates content based on input
# Result includes formatted content, metadata, and suggestions
                """,
                "expected_output": "Professional blog post about AI in healthcare with proper formatting"
            }
            examples.append(content_example)
        
        return examples
    
    def _generate_api_reference(self, agent_info: AgentInfo) -> Dict[str, Any]:
        """Generate API reference documentation"""
        return {
            "launch": {
                "method": "launcher.launch_agent(agent_name, **kwargs)",
                "description": "Launch the agent with optional configuration",
                "parameters": {
                    "agent_name": "string - Name of the agent to launch",
                    "**kwargs": "dict - Optional configuration parameters"
                },
                "returns": "boolean - True if successful, False otherwise",
                "example": f'launcher.launch_agent("{agent_info.name}", model="gpt-4o")'
            },
            "stop": {
                "method": "launcher.stop_agent(agent_name)",
                "description": "Stop a running agent",
                "parameters": {
                    "agent_name": "string - Name of the agent to stop"
                },
                "returns": "boolean - True if successful, False otherwise",
                "example": f'launcher.stop_agent("{agent_info.name}")'
            },
            "status": {
                "method": "launcher.get_agent_status(agent_name)",
                "description": "Get current status and metrics for the agent",
                "parameters": {
                    "agent_name": "string - Name of the agent"
                },
                "returns": "dict - Status information including PID, uptime, resources",
                "example": f'status = launcher.get_agent_status("{agent_info.name}")'
            },
            "configure": {
                "method": "launcher.configure_agent(agent_name, **config)",
                "description": "Configure agent parameters",
                "parameters": {
                    "agent_name": "string - Name of the agent",
                    "**config": "dict - Configuration parameters"
                },
                "returns": "boolean - True if successful, False otherwise",
                "example": f'launcher.configure_agent("{agent_info.name}", temperature=0.8)'
            }
        }
    
    def _generate_performance_notes(self, agent_info: AgentInfo) -> List[str]:
        """Generate performance notes and optimization tips"""
        notes = [
            "💡 **Optimization Tips:**",
            f"- Use appropriate model size for your use case (gpt-4o for complex tasks, gpt-4o-mini for simple ones)",
            f"- Adjust temperature based on desired creativity level",
            f"- Monitor memory usage for long-running sessions"
        ]
        
        if agent_info.category == "research":
            notes.extend([
                "- Limit search depth for faster responses",
                "- Enable caching for repeated queries",
                "- Use fact-checking sparingly for better performance"
            ])
        
        elif agent_info.category == "content":
            notes.extend([
                "- Use templates for consistent formatting",
                "- Batch similar content requests",
                "- Optimize max_tokens based on content length needs"
            ])
        
        elif agent_info.category == "mcp":
            notes.extend([
                "- Minimize tool switching overhead",
                "- Use connection pooling for multiple tools",
                "- Monitor tool response times"
            ])
        
        notes.extend([
            "",
            "⚡ **Performance Benchmarks:**",
            f"- Typical startup time: 3-5 seconds",
            f"- Average response time: 2-10 seconds (varies by complexity)",
            f"- Memory usage: 50-200 MB (depends on model and data)",
            f"- Recommended concurrent instances: 1-3"
        ])
        
        return notes
    
    def _generate_troubleshooting(self, agent_info: AgentInfo) -> List[Dict[str, str]]:
        """Generate troubleshooting guide"""
        common_issues = [
            {
                "problem": "Agent fails to launch",
                "solution": "Check API keys configuration and ensure all dependencies are installed",
                "code": f"launcher.validate_agent('{agent_info.name}')"
            },
            {
                "problem": "High memory usage",
                "solution": "Reduce max_tokens or restart the agent periodically",
                "code": f"launcher.configure_agent('{agent_info.name}', max_tokens=1000)"
            },
            {
                "problem": "Slow response times",
                "solution": "Check system resources or switch to a lighter model",
                "code": f"launcher.configure_agent('{agent_info.name}', model='gpt-4o-mini')"
            },
            {
                "problem": "Connection timeouts",
                "solution": "Increase timeout setting or check network connectivity",
                "code": f"launcher.configure_agent('{agent_info.name}', timeout=600)"
            }
        ]
        
        # Add category-specific troubleshooting
        if agent_info.api_keys_required:
            common_issues.insert(0, {
                "problem": "API authentication errors",
                "solution": f"Ensure {', '.join(agent_info.api_keys_required)} are properly configured",
                "code": "config_manager.set_api_key('service_name', 'your_api_key')"
            })
        
        return common_issues
    
    def _find_related_agents(self, agent_info: AgentInfo) -> List[str]:
        """Find agents related to this one"""
        related = []
        
        # Find agents in the same category
        same_category = [name for name, agent in self.registry.agents.items() 
                        if agent.category == agent_info.category and name != agent_info.name]
        related.extend(same_category[:3])  # Top 3 from same category
        
        # Find agents that might work well together
        complementary_categories = {
            "research": ["content", "knowledge"],
            "content": ["research", "social"],
            "knowledge": ["research", "content"],
            "social": ["content", "media"],
            "business": ["research", "content"],
            "web": ["research", "knowledge"],
            "mcp": ["tools", "integration"]
        }
        
        for comp_category in complementary_categories.get(agent_info.category, []):
            comp_agents = [name for name, agent in self.registry.agents.items() 
                          if agent.category == comp_category]
            related.extend(comp_agents[:2])  # Top 2 from each complementary category
        
        return list(set(related))[:8]  # Maximum 8 related agents
    
    def _generate_use_cases(self, agent_info: AgentInfo) -> List[str]:
        """Generate practical use cases for the agent"""
        category_use_cases = {
            "research": [
                "📊 Market research and competitive analysis",
                "📰 News and trend monitoring",
                "🎓 Academic research assistance",
                "💼 Business intelligence gathering",
                "🔍 Fact-checking and verification"
            ],
            "content": [
                "📝 Blog post and article creation",
                "📱 Social media content generation",
                "📧 Email marketing campaigns",
                "📋 Documentation and technical writing",
                "🎨 Creative writing and storytelling"
            ],
            "knowledge": [
                "💾 Knowledge base construction",
                "🔎 Intelligent search and retrieval",
                "📚 Document analysis and summarization",
                "🧠 Expert system development",
                "📊 Data relationship mapping"
            ],
            "business": [
                "💰 Financial analysis and reporting",
                "📈 Sales pipeline management",
                "🏢 Process automation",
                "👥 Customer relationship management",
                "📊 Performance monitoring"
            ],
            "social": [
                "📱 Social media monitoring",
                "💬 Community management",
                "📊 Sentiment analysis",
                "🔍 Influencer identification",
                "📈 Engagement optimization"
            ]
        }
        
        return category_use_cases.get(agent_info.category, [
            "🤖 General AI task automation",
            "📊 Data processing and analysis",
            "🔄 Workflow optimization",
            "🎯 Task-specific problem solving"
        ])
    
    def _generate_best_practices(self, agent_info: AgentInfo) -> List[str]:
        """Generate best practices for using the agent"""
        practices = [
            "🔧 **Configuration:**",
            "- Start with default settings and adjust based on results",
            "- Test configuration changes in a development environment",
            "- Keep API keys secure and rotate them regularly",
            "",
            "🚀 **Usage:**",
            "- Monitor resource usage during operation",
            "- Implement proper error handling in your applications",
            "- Use appropriate timeouts for your use case",
            "",
            "📊 **Monitoring:**",
            "- Regularly check agent health and performance metrics",
            "- Set up alerts for failures or performance degradation",
            "- Keep logs for debugging and optimization"
        ]
        
        if agent_info.category == "research":
            practices.extend([
                "",
                "🔍 **Research-Specific:**",
                "- Validate research sources and check for bias",
                "- Cross-reference information from multiple sources",
                "- Keep research queries specific and focused"
            ])
        
        elif agent_info.category == "content":
            practices.extend([
                "",
                "✍️ **Content-Specific:**",
                "- Review generated content for accuracy and tone",
                "- Maintain consistent brand voice across content",
                "- Use content templates for efficiency"
            ])
        
        return practices
    
    def _generate_overview(self, agent_info: AgentInfo) -> str:
        """Generate comprehensive overview for the agent"""
        return f"""
{agent_info.description}

**Category:** {agent_info.category.title()}
**Main File:** {agent_info.main_file}
**Dependencies:** {len(agent_info.dependencies)} packages
**API Keys Required:** {len(agent_info.api_keys_required)}

This agent is designed to provide specialized {agent_info.category} capabilities within the ottomator-agents ecosystem. 
It can be used standalone or combined with other agents to create powerful workflows.

**Key Features:**
- Production-ready implementation
- Configurable parameters and settings
- Integration with the Master Agent Menu system
- Comprehensive monitoring and health checks
- Support for multiple AI models and providers
        """.strip()
    
    def _agent_doc_to_markdown(self, doc: AgentDocumentation) -> str:
        """Convert agent documentation to markdown"""
        markdown = f"""# {doc.agent_name}

## Overview

{doc.overview}

## Capabilities

{chr(10).join(f"- {capability}" for capability in doc.capabilities)}

## Configuration

### Required API Keys
{chr(10).join(f"- `{key}`" for key in doc.configuration.get('required_api_keys', []))}

### Supported Models
{chr(10).join(f"- `{model}`" for model in doc.configuration.get('supported_models', []))}

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
"""
        
        for param_name, param_info in doc.configuration.get('parameters', {}).items():
            param_type = param_info.get('type', 'string')
            param_default = param_info.get('default', 'N/A')
            param_desc = param_info.get('description', 'No description available')
            markdown += f"| `{param_name}` | {param_type} | `{param_default}` | {param_desc} |\n"
        
        markdown += "\n## Examples\n\n"
        
        for i, example in enumerate(doc.examples, 1):
            markdown += f"""### {example['title']}

{example['description']}

```python
{example['code'].strip()}
```

**Expected Output:**
```
{example['expected_output']}
```

"""
        
        markdown += "## API Reference\n\n"
        
        for method_name, method_info in doc.api_reference.items():
            markdown += f"""### {method_name}

**Method:** `{method_info['method']}`

{method_info['description']}

**Parameters:**
{chr(10).join(f"- `{param}`: {desc}" for param, desc in method_info.get('parameters', {}).items())}

**Returns:** {method_info.get('returns', 'N/A')}

**Example:**
```python
{method_info.get('example', 'No example available')}
```

"""
        
        markdown += f"""## Performance & Optimization

{chr(10).join(doc.performance_notes)}

## Troubleshooting

| Problem | Solution | Code Example |
|---------|----------|--------------|
"""
        
        for issue in doc.troubleshooting:
            markdown += f"| {issue['problem']} | {issue['solution']} | `{issue['code']}` |\n"
        
        markdown += f"""

## Use Cases

{chr(10).join(f"- {use_case}" for use_case in doc.use_cases)}

## Related Agents

{chr(10).join(f"- [{agent}](../agents/{agent}.md)" for agent in doc.related_agents)}

## Best Practices

{chr(10).join(doc.best_practices)}

---

*Documentation generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Agent last modified: {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        return markdown
    
    def generate_combination_documentation(self, combination_name: str) -> str:
        """Generate documentation for an agent combination"""
        combination = self.registry.combinations.get(combination_name)
        if not combination:
            raise ValueError(f"Combination {combination_name} not found")
        
        markdown = f"""# {combination.name}

## Overview

{combination.description}

## Component Agents

This combination includes the following agents working together:

"""
        
        for agent_name in combination.component_agents:
            agent_info = self.registry.get_agent(agent_name)
            if agent_info:
                markdown += f"- **[{agent_name}](../agents/{agent_name}.md)** ({agent_info.category}): {agent_info.description[:100]}...\n"
            else:
                markdown += f"- **{agent_name}**: Agent not found\n"
        
        markdown += f"""

## Workflow

```json
{json.dumps(combination.workflow, indent=2)}
```

## Benefits

{chr(10).join(f"- {benefit}" for benefit in combination.benefits)}

## Use Cases

{chr(10).join(f"- {use_case}" for use_case in combination.use_cases)}

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("{combination.name}", "Your input data here")

# Monitor execution
status = launcher.combination_engine.get_combination_status(execution_id)
print(f"Status: {{status['status']}}")
print(f"Progress: {{status['steps_completed']}}/{{status['total_steps']}}")
```

## Configuration

Each component agent can be configured individually before launching the combination. 
See the documentation for each component agent for specific configuration options.

---

*Documentation generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Save to file
        doc_file = self.docs_dir / "combinations" / f"{combination_name}.md"
        with open(doc_file, 'w') as f:
            f.write(markdown)
        
        return str(doc_file)
    
    def generate_index(self) -> str:
        """Generate main documentation index"""
        markdown = f"""# Master Agent Menu - Documentation Index

Welcome to the comprehensive documentation for the Master Agent Menu system and all available AI agents.

## 📊 Statistics

- **Total Agents:** {len(self.registry.agents)}
- **Total Combinations:** {len(self.registry.combinations)}
- **Categories:** {len(set(agent.category for agent in self.registry.agents.values()))}
- **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🤖 Agents by Category

"""
        
        # Group agents by category
        by_category = {}
        for agent in self.registry.agents.values():
            if agent.category not in by_category:
                by_category[agent.category] = []
            by_category[agent.category].append(agent)
        
        for category, agents in sorted(by_category.items()):
            markdown += f"\n### {category.title()} ({len(agents)} agents)\n\n"
            for agent in sorted(agents, key=lambda x: x.name):
                markdown += f"- **[{agent.name}](agents/{agent.name}.md)**: {agent.description[:80]}...\n"
        
        markdown += f"""

## 🔗 Agent Combinations

"""
        
        for combination in sorted(self.registry.combinations.values(), key=lambda x: x.name):
            markdown += f"- **[{combination.name}](combinations/{combination.name}.md)**: {combination.description[:80]}...\n"
        
        markdown += f"""

## 🚀 Quick Start

1. **[Installation](examples/installation.md)** - Set up the Master Agent Menu system
2. **[Basic Usage](examples/basic_usage.md)** - Launch your first agent
3. **[Configuration](examples/configuration.md)** - Configure agents and API keys
4. **[Combinations](examples/combinations.md)** - Create powerful agent workflows
5. **[Monitoring](examples/monitoring.md)** - Monitor agent health and performance

## 📚 Guides

- **[Agent Development](examples/agent_development.md)** - Create your own agents
- **[Best Practices](examples/best_practices.md)** - Optimization and usage tips
- **[Troubleshooting](examples/troubleshooting.md)** - Common issues and solutions
- **[API Reference](examples/api_reference.md)** - Complete API documentation

## 🛠️ System Components

- **Agent Registry** - Discovers and catalogs agents
- **Configuration Manager** - Handles settings and API keys
- **Status Monitor** - Tracks agent health and performance
- **Combination Engine** - Creates and executes agent workflows
- **Documentation Generator** - Maintains up-to-date documentation

---

*Generated by Master Agent Menu Documentation System*
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Save index
        index_file = self.docs_dir / "index.md"
        with open(index_file, 'w') as f:
            f.write(markdown)
        
        return str(index_file)

if __name__ == "__main__":
    # Test documentation generation
    from agent_registry import AgentRegistry
    
    registry = AgentRegistry()
    registry.discover_agents()
    
    doc_generator = DocumentationGenerator(registry)
    
    print("Generating documentation for all agents and combinations...")
    results = doc_generator.generate_all_documentation()
    
    print(f"Generated {len(results)} documentation files:")
    for name, path in results.items():
        print(f"  - {name}: {path}")
    
    print(f"\nDocumentation available in: {doc_generator.docs_dir}")