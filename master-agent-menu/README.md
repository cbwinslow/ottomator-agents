# Master Agent Menu System

A centralized management system for all AI agents in the ottomator-agents repository. This system provides discovery, launch, configuration, and monitoring capabilities for all available agents.

## Features

- **Agent Discovery**: Automatically discovers and catalogs all available agents
- **Centralized Launch**: Launch any agent through a unified interface
- **Configuration Management**: Manage parameters and settings for each agent
- **Health Monitoring**: Monitor agent status and performance
- **Agent Combinations**: Create and manage hybrid agents combining multiple capabilities
- **Documentation Hub**: Comprehensive documentation with examples and illustrations

## Quick Start

```bash
cd master-agent-menu
python -m pip install -r requirements.txt
python main.py
```

## Architecture

### Components

1. **Agent Registry**: Discovers and catalogs available agents
2. **Configuration Manager**: Handles agent parameters and settings
3. **Launch Controller**: Manages agent lifecycle and execution
4. **Status Monitor**: Tracks agent health and performance
5. **Combination Engine**: Creates hybrid agents from existing ones
6. **Documentation Generator**: Builds comprehensive agent documentation

### Agent Categories

- **MCP-based Agents**: Agents using Model Context Protocol
- **Task-Specific Agents**: Specialized functionality agents
- **Knowledge Agents**: RAG and knowledge graph agents
- **Research Agents**: Web scraping and data gathering agents
- **Business Agents**: Domain-specific business logic agents
- **Content Creation Agents**: Text, image, and multimedia generation agents

## Usage

### Basic Agent Launch

```python
from master_menu import AgentLauncher

launcher = AgentLauncher()
agent = launcher.get_agent("ask-reddit-agent")
result = await agent.run("What are the best sci-fi movies?")
```

### Agent Combinations

```python
# Create a hybrid research + content creation agent
hybrid = launcher.create_combination([
    "advanced-web-researcher",
    "linkedin-x-blog-content-creator"
])

result = await hybrid.run("Research AI trends and create a LinkedIn post")
```

### Configuration Management

```python
# Configure agent parameters
launcher.configure_agent("travel-agent", {
    "default_budget": 5000,
    "preferred_airlines": ["Delta", "United"],
    "hotel_rating_min": 4
})
```

## Agent Combinations

### Available Hybrid Agents

1. **Multi-Modal Research Agent**
   - Components: web-researcher + rag-agent + content-creator
   - Use case: Comprehensive research with content generation

2. **Business Intelligence Agent**
   - Components: data-analyst + web-researcher + document-generator
   - Use case: Market research and business reporting

3. **Social Media Analytics Agent**
   - Components: reddit-agent + youtube-agent + content-creator
   - Use case: Social media trends and content strategy

4. **Real Estate Intelligence Agent**
   - Components: property-agent + market-researcher + content-creator
   - Use case: Property analysis and marketing materials

5. **Educational Content Agent**
   - Components: research-agent + knowledge-graph + multimedia-creator
   - Use case: Educational material development

6. **Financial Analysis Agent**
   - Components: market-researcher + data-analyst + reporting-agent
   - Use case: Financial research and analysis

## Configuration

### Environment Variables

```bash
# API Keys for various services
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
BRAVE_API_KEY=your_brave_key
GITHUB_TOKEN=your_github_token

# Default model configurations
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=2000

# Monitoring and logging
LOG_LEVEL=INFO
ENABLE_MONITORING=true
METRICS_ENDPOINT=http://localhost:8080/metrics
```

### Agent-Specific Configuration

Each agent can have custom configuration files in the `configs/` directory:

```yaml
# configs/travel-agent.yaml
default_budget: 5000
preferred_airlines:
  - "Delta"
  - "United"
hotel_rating_min: 4
search_radius_km: 50
```

## Documentation

Each agent includes:
- **Overview**: Purpose and capabilities
- **Configuration**: Available parameters and settings
- **Examples**: Working code examples and use cases
- **API Reference**: Detailed method documentation
- **Performance**: Benchmarks and optimization tips
- **Troubleshooting**: Common issues and solutions

## Contributing

### Adding New Agents

1. Create agent directory in repository root
2. Implement standard agent interface
3. Add configuration schema
4. Include documentation and examples
5. Register with agent registry

### Creating Agent Combinations

1. Define combination schema in `combinations/`
2. Implement coordination logic
3. Add configuration options
4. Include usage examples
5. Document performance characteristics

## License

MIT License - see LICENSE file for details