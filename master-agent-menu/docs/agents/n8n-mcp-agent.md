# n8n-mcp-agent

## Overview

This repository contains a workflow for n8n that demonstrates how to build an AI agent that leverages the Model Context Protocol (MCP) to access and execute external tools.

**Category:** Mcp
**Main File:** (no main file found)
**Dependencies:** 0 packages
**API Keys Required:** 0

This agent is designed to provide specialized mcp capabilities within the ottomator-agents ecosystem. 
It can be used standalone or combined with other agents to create powerful workflows.

**Key Features:**
- Production-ready implementation
- Configurable parameters and settings
- Integration with the Master Agent Menu system
- Comprehensive monitoring and health checks
- Support for multiple AI models and providers

## Capabilities

- 🔌 Model Context Protocol integration
- 🛠️ Tool execution and management
- 📊 Multi-service orchestration
- 🔄 Protocol-compliant communication
- ⚡ Efficient tool discovery
- 🔌 MCP protocol support

## Configuration

### Required API Keys


### Supported Models


### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `gpt-4o-mini` | AI model to use for processing |
| `temperature` | float | `0.7` | Controls creativity and randomness in responses |
| `max_tokens` | integer | `2000` | Maximum number of tokens in response |
| `timeout` | integer | `300` | Request timeout in seconds |

## Examples

### Basic Usage

Simple example of using n8n-mcp-agent

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the agent
success = launcher.launch_agent("n8n-mcp-agent")

if success:
    print("Agent launched successfully!")
    
    # Get agent status
    status = launcher.get_agent_status("n8n-mcp-agent")
    print(f"Status: {status['status']}")
    
    # Stop the agent when done
    launcher.stop_agent("n8n-mcp-agent")
```

**Expected Output:**
```
Agent launched successfully!
Status: running
```

### Configuration Example

Configuring n8n-mcp-agent with custom parameters

```python
# Configure the agent
launcher.configure_agent("n8n-mcp-agent", 
    model="gpt-4o",
    temperature=0.5,
    max_tokens=3000
)

# Launch with configuration
launcher.launch_agent("n8n-mcp-agent")
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
launcher.launch_agent("n8n-mcp-agent", model="gpt-4o")
```

### stop

**Method:** `launcher.stop_agent(agent_name)`

Stop a running agent

**Parameters:**
- `agent_name`: string - Name of the agent to stop

**Returns:** boolean - True if successful, False otherwise

**Example:**
```python
launcher.stop_agent("n8n-mcp-agent")
```

### status

**Method:** `launcher.get_agent_status(agent_name)`

Get current status and metrics for the agent

**Parameters:**
- `agent_name`: string - Name of the agent

**Returns:** dict - Status information including PID, uptime, resources

**Example:**
```python
status = launcher.get_agent_status("n8n-mcp-agent")
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
launcher.configure_agent("n8n-mcp-agent", temperature=0.8)
```

## Performance & Optimization

💡 **Optimization Tips:**
- Use appropriate model size for your use case (gpt-4o for complex tasks, gpt-4o-mini for simple ones)
- Adjust temperature based on desired creativity level
- Monitor memory usage for long-running sessions
- Minimize tool switching overhead
- Use connection pooling for multiple tools
- Monitor tool response times

⚡ **Performance Benchmarks:**
- Typical startup time: 3-5 seconds
- Average response time: 2-10 seconds (varies by complexity)
- Memory usage: 50-200 MB (depends on model and data)
- Recommended concurrent instances: 1-3

## Troubleshooting

| Problem | Solution | Code Example |
|---------|----------|--------------|
| Agent fails to launch | Check API keys configuration and ensure all dependencies are installed | `launcher.validate_agent('n8n-mcp-agent')` |
| High memory usage | Reduce max_tokens or restart the agent periodically | `launcher.configure_agent('n8n-mcp-agent', max_tokens=1000)` |
| Slow response times | Check system resources or switch to a lighter model | `launcher.configure_agent('n8n-mcp-agent', model='gpt-4o-mini')` |
| Connection timeouts | Increase timeout setting or check network connectivity | `launcher.configure_agent('n8n-mcp-agent', timeout=600)` |


## Use Cases

- 🤖 General AI task automation
- 📊 Data processing and analysis
- 🔄 Workflow optimization
- 🎯 Task-specific problem solving

## Related Agents

- [simple-mcp-agent](../agents/simple-mcp-agent.md)
- [thirdbrain-mcp-openai-agent](../agents/thirdbrain-mcp-openai-agent.md)
- [google-a2a-agent](../agents/google-a2a-agent.md)
- [graphiti-agent](../agents/graphiti-agent.md)
- [mem0-agent](../agents/mem0-agent.md)
- [pydantic-ai-mcp-agent](../agents/pydantic-ai-mcp-agent.md)
- [n8n-openwebui-agent](../agents/n8n-openwebui-agent.md)

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
