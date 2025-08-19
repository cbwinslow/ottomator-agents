# nba-agent

## Overview

Author: [Elo Mukoro](https://nbaagent-production.up.railway.app/)

**Category:** Social
**Main File:** /home/runner/work/ottomator-agents/ottomator-agents/nba-agent/nba_agent.py
**Dependencies:** 3 packages
**API Keys Required:** 7

This agent is designed to provide specialized social capabilities within the ottomator-agents ecosystem. 
It can be used standalone or combined with other agents to create powerful workflows.

**Key Features:**
- Production-ready implementation
- Configurable parameters and settings
- Integration with the Master Agent Menu system
- Comprehensive monitoring and health checks
- Support for multiple AI models and providers

## Capabilities

- 👥 Social media analysis
- 📱 Community engagement insights
- 🔍 Trend identification
- 💬 Sentiment analysis
- 📊 Social metrics tracking
- 🔑 External API integration

## Configuration

### Required API Keys
- `BALLDONTLIE_API_KEY`
- `OPENAI_API_KEY`
- `API_BEARER_TOKEN`
- `max_token`
- `verify_token`
- `expected_token`
- `SUPABASE_SERVICE_KEY`

### Supported Models
- `gpt-4-turbo-preview`

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `gpt-4o-mini` | AI model to use for processing |
| `temperature` | float | `0.7` | Controls creativity and randomness in responses |
| `max_tokens` | integer | `2000` | Maximum number of tokens in response |
| `timeout` | integer | `300` | Request timeout in seconds |

## Examples

### Basic Usage

Simple example of using nba-agent

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the agent
success = launcher.launch_agent("nba-agent")

if success:
    print("Agent launched successfully!")
    
    # Get agent status
    status = launcher.get_agent_status("nba-agent")
    print(f"Status: {status['status']}")
    
    # Stop the agent when done
    launcher.stop_agent("nba-agent")
```

**Expected Output:**
```
Agent launched successfully!
Status: running
```

### Configuration Example

Configuring nba-agent with custom parameters

```python
# Configure the agent
launcher.configure_agent("nba-agent", 
    model="gpt-4o",
    temperature=0.5,
    max_tokens=3000
)

# Launch with configuration
launcher.launch_agent("nba-agent")
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
launcher.launch_agent("nba-agent", model="gpt-4o")
```

### stop

**Method:** `launcher.stop_agent(agent_name)`

Stop a running agent

**Parameters:**
- `agent_name`: string - Name of the agent to stop

**Returns:** boolean - True if successful, False otherwise

**Example:**
```python
launcher.stop_agent("nba-agent")
```

### status

**Method:** `launcher.get_agent_status(agent_name)`

Get current status and metrics for the agent

**Parameters:**
- `agent_name`: string - Name of the agent

**Returns:** dict - Status information including PID, uptime, resources

**Example:**
```python
status = launcher.get_agent_status("nba-agent")
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
launcher.configure_agent("nba-agent", temperature=0.8)
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
| API authentication errors | Ensure BALLDONTLIE_API_KEY, OPENAI_API_KEY, API_BEARER_TOKEN, max_token, verify_token, expected_token, SUPABASE_SERVICE_KEY are properly configured | `config_manager.set_api_key('service_name', 'your_api_key')` |
| Agent fails to launch | Check API keys configuration and ensure all dependencies are installed | `launcher.validate_agent('nba-agent')` |
| High memory usage | Reduce max_tokens or restart the agent periodically | `launcher.configure_agent('nba-agent', max_tokens=1000)` |
| Slow response times | Check system resources or switch to a lighter model | `launcher.configure_agent('nba-agent', model='gpt-4o-mini')` |
| Connection timeouts | Increase timeout setting or check network connectivity | `launcher.configure_agent('nba-agent', timeout=600)` |


## Use Cases

- 📱 Social media monitoring
- 💬 Community management
- 📊 Sentiment analysis
- 🔍 Influencer identification
- 📈 Engagement optimization

## Related Agents

- [ask-reddit-agent](../agents/ask-reddit-agent.md)
- [youtube-educator-plus-agent](../agents/youtube-educator-plus-agent.md)
- [tweet-generator-agent](../agents/tweet-generator-agent.md)
- [youtube-video-summarizer](../agents/youtube-video-summarizer.md)
- [youtube-summary-agent](../agents/youtube-summary-agent.md)

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
