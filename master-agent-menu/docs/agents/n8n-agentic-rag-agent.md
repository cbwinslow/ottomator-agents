# n8n-agentic-rag-agent

## Overview

**Author:** [Cole Medin](https://www.youtube.com/@ColeMedin)

**Category:** Knowledge
**Main File:** (no main file found)
**Dependencies:** 0 packages
**API Keys Required:** 0

This agent is designed to provide specialized knowledge capabilities within the ottomator-agents ecosystem. 
It can be used standalone or combined with other agents to create powerful workflows.

**Key Features:**
- Production-ready implementation
- Configurable parameters and settings
- Integration with the Master Agent Menu system
- Comprehensive monitoring and health checks
- Support for multiple AI models and providers

## Capabilities

- 🧠 Knowledge graph construction
- 💾 Vector-based retrieval
- 🔗 Entity relationship mapping
- 📚 Document understanding
- 🎯 Contextual information retrieval

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

Simple example of using n8n-agentic-rag-agent

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the agent
success = launcher.launch_agent("n8n-agentic-rag-agent")

if success:
    print("Agent launched successfully!")
    
    # Get agent status
    status = launcher.get_agent_status("n8n-agentic-rag-agent")
    print(f"Status: {status['status']}")
    
    # Stop the agent when done
    launcher.stop_agent("n8n-agentic-rag-agent")
```

**Expected Output:**
```
Agent launched successfully!
Status: running
```

### Configuration Example

Configuring n8n-agentic-rag-agent with custom parameters

```python
# Configure the agent
launcher.configure_agent("n8n-agentic-rag-agent", 
    model="gpt-4o",
    temperature=0.5,
    max_tokens=3000
)

# Launch with configuration
launcher.launch_agent("n8n-agentic-rag-agent")
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
launcher.launch_agent("n8n-agentic-rag-agent", model="gpt-4o")
```

### stop

**Method:** `launcher.stop_agent(agent_name)`

Stop a running agent

**Parameters:**
- `agent_name`: string - Name of the agent to stop

**Returns:** boolean - True if successful, False otherwise

**Example:**
```python
launcher.stop_agent("n8n-agentic-rag-agent")
```

### status

**Method:** `launcher.get_agent_status(agent_name)`

Get current status and metrics for the agent

**Parameters:**
- `agent_name`: string - Name of the agent

**Returns:** dict - Status information including PID, uptime, resources

**Example:**
```python
status = launcher.get_agent_status("n8n-agentic-rag-agent")
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
launcher.configure_agent("n8n-agentic-rag-agent", temperature=0.8)
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
| Agent fails to launch | Check API keys configuration and ensure all dependencies are installed | `launcher.validate_agent('n8n-agentic-rag-agent')` |
| High memory usage | Reduce max_tokens or restart the agent periodically | `launcher.configure_agent('n8n-agentic-rag-agent', max_tokens=1000)` |
| Slow response times | Check system resources or switch to a lighter model | `launcher.configure_agent('n8n-agentic-rag-agent', model='gpt-4o-mini')` |
| Connection timeouts | Increase timeout setting or check network connectivity | `launcher.configure_agent('n8n-agentic-rag-agent', timeout=600)` |


## Use Cases

- 💾 Knowledge base construction
- 🔎 Intelligent search and retrieval
- 📚 Document analysis and summarization
- 🧠 Expert system development
- 📊 Data relationship mapping

## Related Agents

- [foundational-rag-agent](../agents/foundational-rag-agent.md)
- [small-business-researcher](../agents/small-business-researcher.md)
- [agentic-rag-knowledge-graph](../agents/agentic-rag-knowledge-graph.md)
- [youtube-educator-plus-agent](../agents/youtube-educator-plus-agent.md)
- [tweet-generator-agent](../agents/tweet-generator-agent.md)
- [general-researcher-agent](../agents/general-researcher-agent.md)
- [light-rag-agent](../agents/light-rag-agent.md)

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
