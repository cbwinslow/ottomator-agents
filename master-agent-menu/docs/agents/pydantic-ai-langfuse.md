# pydantic-ai-langfuse

## Overview

A powerful multi-agent system built with Pydantic AI and integrated with Langfuse for observability. This project demonstrates how to create a system of specialized AI agents that can perform various ...

**Category:** Experimental
**Main File:** /home/runner/work/ottomator-agents/ottomator-agents/pydantic-ai-langfuse/pydantic_ai_langfuse_agent.py
**Dependencies:** 20 packages
**API Keys Required:** 10

This agent is designed to provide specialized experimental capabilities within the ottomator-agents ecosystem. 
It can be used standalone or combined with other agents to create powerful workflows.

**Key Features:**
- Production-ready implementation
- Configurable parameters and settings
- Integration with the Master Agent Menu system
- Comprehensive monitoring and health checks
- Support for multiple AI models and providers

## Capabilities

- 🤖 AI-powered task execution
- ⚙️ Configurable parameters
- 📊 Performance monitoring
- 🔄 Reliable processing
- 🎯 Domain-specific optimization
- 🔑 External API integration

## Configuration

### Required API Keys
- `LANGFUSE_SECRET`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LLM_API_KEY`
- `BRAVE_API_KEY`
- `AIRTABLE_API_KEY`
- `FIRECRAWL_API_KEY`
- `GITHUB_PERSONAL_ACCESS_TOKEN`
- `GITHUB_TOKEN`
- `SLACK_BOT_TOKEN`

### Supported Models
- `gpt-4.1-mini`
- `, `

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `gpt-4o-mini` | AI model to use for processing |
| `temperature` | float | `0.7` | Controls creativity and randomness in responses |
| `max_tokens` | integer | `2000` | Maximum number of tokens in response |
| `timeout` | integer | `300` | Request timeout in seconds |

## Examples

### Basic Usage

Simple example of using pydantic-ai-langfuse

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the agent
success = launcher.launch_agent("pydantic-ai-langfuse")

if success:
    print("Agent launched successfully!")
    
    # Get agent status
    status = launcher.get_agent_status("pydantic-ai-langfuse")
    print(f"Status: {status['status']}")
    
    # Stop the agent when done
    launcher.stop_agent("pydantic-ai-langfuse")
```

**Expected Output:**
```
Agent launched successfully!
Status: running
```

### Configuration Example

Configuring pydantic-ai-langfuse with custom parameters

```python
# Configure the agent
launcher.configure_agent("pydantic-ai-langfuse", 
    model="gpt-4o",
    temperature=0.5,
    max_tokens=3000
)

# Launch with configuration
launcher.launch_agent("pydantic-ai-langfuse")
```

**Expected Output:**
```
Agent configured and launched with custom settings
```

## API Reference

### launch

**Method:** `launcher.launch_agent(agent_name, **kwargs)`

Launch the agent with optional configuration

**Parameters:**
- `agent_name`: string - Name of the agent to launch
- `**kwargs`: dict - Optional configuration parameters

**Returns:** boolean - True if successful, False otherwise

**Example:**
```python
launcher.launch_agent("pydantic-ai-langfuse", model="gpt-4o")
```

### stop

**Method:** `launcher.stop_agent(agent_name)`

Stop a running agent

**Parameters:**
- `agent_name`: string - Name of the agent to stop

**Returns:** boolean - True if successful, False otherwise

**Example:**
```python
launcher.stop_agent("pydantic-ai-langfuse")
```

### status

**Method:** `launcher.get_agent_status(agent_name)`

Get current status and metrics for the agent

**Parameters:**
- `agent_name`: string - Name of the agent

**Returns:** dict - Status information including PID, uptime, resources

**Example:**
```python
status = launcher.get_agent_status("pydantic-ai-langfuse")
```

### configure

**Method:** `launcher.configure_agent(agent_name, **config)`

Configure agent parameters

**Parameters:**
- `agent_name`: string - Name of the agent
- `**config`: dict - Configuration parameters

**Returns:** boolean - True if successful, False otherwise

**Example:**
```python
launcher.configure_agent("pydantic-ai-langfuse", temperature=0.8)
```

## Performance & Optimization

💡 **Optimization Tips:**
- Use appropriate model size for your use case (gpt-4o for complex tasks, gpt-4o-mini for simple ones)
- Adjust temperature based on desired creativity level
- Monitor memory usage for long-running sessions

⚡ **Performance Benchmarks:**
- Typical startup time: 3-5 seconds
- Average response time: 2-10 seconds (varies by complexity)
- Memory usage: 50-200 MB (depends on model and data)
- Recommended concurrent instances: 1-3

## Troubleshooting

| Problem | Solution | Code Example |
|---------|----------|--------------|
| API authentication errors | Ensure LANGFUSE_SECRET, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LLM_API_KEY, BRAVE_API_KEY, AIRTABLE_API_KEY, FIRECRAWL_API_KEY, GITHUB_PERSONAL_ACCESS_TOKEN, GITHUB_TOKEN, SLACK_BOT_TOKEN are properly configured | `config_manager.set_api_key('service_name', 'your_api_key')` |
| Agent fails to launch | Check API keys configuration and ensure all dependencies are installed | `launcher.validate_agent('pydantic-ai-langfuse')` |
| High memory usage | Reduce max_tokens or restart the agent periodically | `launcher.configure_agent('pydantic-ai-langfuse', max_tokens=1000)` |
| Slow response times | Check system resources or switch to a lighter model | `launcher.configure_agent('pydantic-ai-langfuse', model='gpt-4o-mini')` |
| Connection timeouts | Increase timeout setting or check network connectivity | `launcher.configure_agent('pydantic-ai-langfuse', timeout=600)` |


## Use Cases

- 🤖 General AI task automation
- 📊 Data processing and analysis
- 🔄 Workflow optimization
- 🎯 Task-specific problem solving

## Related Agents

- [ottomarkdown-agent](../agents/ottomarkdown-agent.md)
- [openai-sdk-agent](../agents/openai-sdk-agent.md)
- [pydantic-ai-langgraph-parallelization](../agents/pydantic-ai-langgraph-parallelization.md)

## Best Practices

🔧 **Configuration:**
- Start with default settings and adjust based on results
- Test configuration changes in a development environment
- Keep API keys secure and rotate them regularly

🚀 **Usage:**
- Monitor resource usage during operation
- Implement proper error handling in your applications
- Use appropriate timeouts for your use case

📊 **Monitoring:**
- Regularly check agent health and performance metrics
- Set up alerts for failures or performance degradation
- Keep logs for debugging and optimization

---

*Documentation generated on 2025-08-15 14:58:08*
*Agent last modified: 2025-08-15*
