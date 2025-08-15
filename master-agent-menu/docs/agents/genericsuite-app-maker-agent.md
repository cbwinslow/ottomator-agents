# genericsuite-app-maker-agent

## Overview

Author: [Carlos J. Ramirez](https://github.com/tomkat-cr/genericsuite-app-maker)

**Category:** Content
**Main File:** /home/runner/work/ottomator-agents/ottomator-agents/genericsuite-app-maker-agent/gsam_ottomator_agent_app.py
**Dependencies:** 20 packages
**API Keys Required:** 10

This agent is designed to provide specialized content capabilities within the ottomator-agents ecosystem. 
It can be used standalone or combined with other agents to create powerful workflows.

**Key Features:**
- Production-ready implementation
- Configurable parameters and settings
- Integration with the Master Agent Menu system
- Comprehensive monitoring and health checks
- Support for multiple AI models and providers

## Capabilities

- ✍️ High-quality content generation
- 🎨 Creative writing and ideation
- 📱 Multi-platform content adaptation
- 🔤 Style and tone customization
- 📊 Content optimization
- 🔑 External API integration

## Configuration

### Required API Keys
- `verify_token`
- `model_config_par_max_token`
- `OPENAI_API_KEY`
- `HUGGINGFACE_API_KEY`
- `TOGETHER_AI_API_KEY`
- `AIMLAPI_API_KEY`
- `GROQ_API_KEY`
- `XAI_API_KEY`
- `OPENROUTER_API_KEY`
- `RHYMES_ARIA_API_KEY`

### Supported Models


### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `gpt-4o-mini` | AI model to use for processing |
| `temperature` | float | `0.7` | Controls creativity and randomness in responses |
| `max_tokens` | integer | `2000` | Maximum number of tokens in response |
| `timeout` | integer | `300` | Request timeout in seconds |
| `creativity_mode` | boolean | `True` | Enable creative writing features |
| `output_format` | string | `markdown` | Output format for generated content |

## Examples

### Basic Usage

Simple example of using genericsuite-app-maker-agent

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the agent
success = launcher.launch_agent("genericsuite-app-maker-agent")

if success:
    print("Agent launched successfully!")
    
    # Get agent status
    status = launcher.get_agent_status("genericsuite-app-maker-agent")
    print(f"Status: {status['status']}")
    
    # Stop the agent when done
    launcher.stop_agent("genericsuite-app-maker-agent")
```

**Expected Output:**
```
Agent launched successfully!
Status: running
```

### Configuration Example

Configuring genericsuite-app-maker-agent with custom parameters

```python
# Configure the agent
launcher.configure_agent("genericsuite-app-maker-agent", 
    model="gpt-4o",
    temperature=0.5,
    max_tokens=3000
)

# Launch with configuration
launcher.launch_agent("genericsuite-app-maker-agent")
```

**Expected Output:**
```
Agent configured and launched with custom settings
```

### Content Generation Example

Generating content with the agent

```python
# Content generation example
topic = "Benefits of AI in healthcare"
style = "professional blog post"

# Agent generates content based on input
# Result includes formatted content, metadata, and suggestions
```

**Expected Output:**
```
Professional blog post about AI in healthcare with proper formatting
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
launcher.launch_agent("genericsuite-app-maker-agent", model="gpt-4o")
```

### stop

**Method:** `launcher.stop_agent(agent_name)`

Stop a running agent

**Parameters:**
- `agent_name`: string - Name of the agent to stop

**Returns:** boolean - True if successful, False otherwise

**Example:**
```python
launcher.stop_agent("genericsuite-app-maker-agent")
```

### status

**Method:** `launcher.get_agent_status(agent_name)`

Get current status and metrics for the agent

**Parameters:**
- `agent_name`: string - Name of the agent

**Returns:** dict - Status information including PID, uptime, resources

**Example:**
```python
status = launcher.get_agent_status("genericsuite-app-maker-agent")
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
launcher.configure_agent("genericsuite-app-maker-agent", temperature=0.8)
```

## Performance & Optimization

💡 **Optimization Tips:**
- Use appropriate model size for your use case (gpt-4o for complex tasks, gpt-4o-mini for simple ones)
- Adjust temperature based on desired creativity level
- Monitor memory usage for long-running sessions
- Use templates for consistent formatting
- Batch similar content requests
- Optimize max_tokens based on content length needs

⚡ **Performance Benchmarks:**
- Typical startup time: 3-5 seconds
- Average response time: 2-10 seconds (varies by complexity)
- Memory usage: 50-200 MB (depends on model and data)
- Recommended concurrent instances: 1-3

## Troubleshooting

| Problem | Solution | Code Example |
|---------|----------|--------------|
| API authentication errors | Ensure verify_token, model_config_par_max_token, OPENAI_API_KEY, HUGGINGFACE_API_KEY, TOGETHER_AI_API_KEY, AIMLAPI_API_KEY, GROQ_API_KEY, XAI_API_KEY, OPENROUTER_API_KEY, RHYMES_ARIA_API_KEY are properly configured | `config_manager.set_api_key('service_name', 'your_api_key')` |
| Agent fails to launch | Check API keys configuration and ensure all dependencies are installed | `launcher.validate_agent('genericsuite-app-maker-agent')` |
| High memory usage | Reduce max_tokens or restart the agent periodically | `launcher.configure_agent('genericsuite-app-maker-agent', max_tokens=1000)` |
| Slow response times | Check system resources or switch to a lighter model | `launcher.configure_agent('genericsuite-app-maker-agent', model='gpt-4o-mini')` |
| Connection timeouts | Increase timeout setting or check network connectivity | `launcher.configure_agent('genericsuite-app-maker-agent', timeout=600)` |


## Use Cases

- 📝 Blog post and article creation
- 📱 Social media content generation
- 📧 Email marketing campaigns
- 📋 Documentation and technical writing
- 🎨 Creative writing and storytelling

## Related Agents

- [small-business-researcher](../agents/small-business-researcher.md)
- [ask-reddit-agent](../agents/ask-reddit-agent.md)
- [youtube-educator-plus-agent](../agents/youtube-educator-plus-agent.md)
- [tweet-generator-agent](../agents/tweet-generator-agent.md)
- [general-researcher-agent](../agents/general-researcher-agent.md)
- [linkedin-x-blog-content-creator](../agents/linkedin-x-blog-content-creator.md)
- [nba-agent](../agents/nba-agent.md)

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

✍️ **Content-Specific:**
- Review generated content for accuracy and tone
- Maintain consistent brand voice across content
- Use content templates for efficiency

---

*Documentation generated on 2025-08-15 14:58:08*
*Agent last modified: 2025-08-15*
