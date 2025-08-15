# social-media-analytics-agent

## Overview

Social media intelligence combining Reddit analysis, YouTube research, and content creation

## Component Agents

This combination includes the following agents working together:

- **[ask-reddit-agent](../agents/ask-reddit-agent.md)** (social): <!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Tem...
- **[youtube-summary-agent](../agents/youtube-summary-agent.md)** (media): Author: [Josh Stephens](https://github.com/josh-stephens/youtube-summary-agent)...
- **[tweet-generator-agent](../agents/tweet-generator-agent.md)** (content): Author: [Pavel Cherkashin](https://github.com/pcherkashin)...


## Workflow

```json
{
  "step1": "Analyze Reddit discussions and trends",
  "step2": "Research YouTube content and engagement",
  "step3": "Generate social media content strategy"
}
```

## Benefits

- Multi-platform social intelligence
- Trend identification
- Content strategy automation

## Use Cases

- Social media marketing
- Trend analysis
- Content planning

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("social-media-analytics-agent", "Your input data here")

# Monitor execution
status = launcher.combination_engine.get_combination_status(execution_id)
print(f"Status: {status['status']}")
print(f"Progress: {status['steps_completed']}/{status['total_steps']}")
```

## Configuration

Each component agent can be configured individually before launching the combination. 
See the documentation for each component agent for specific configuration options.

---

*Documentation generated on 2025-08-15 14:58:08*
