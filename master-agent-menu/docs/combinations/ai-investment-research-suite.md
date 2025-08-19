# ai-investment-research-suite

## Overview

Comprehensive investment research combining market analysis, news sentiment, and financial modeling

## Component Agents

This combination includes the following agents working together:

- **[advanced-web-researcher](../agents/advanced-web-researcher.md)** (research): Author: [Cole Medin](https://www.youtube.com/@ColeMedin)...
- **[ask-reddit-agent](../agents/ask-reddit-agent.md)** (social): <!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Tem...
- **[youtube-summary-agent](../agents/youtube-summary-agent.md)** (media): Author: [Josh Stephens](https://github.com/josh-stephens/youtube-summary-agent)...
- **[genericsuite-app-maker-agent](../agents/genericsuite-app-maker-agent.md)** (content): Author: [Carlos J. Ramirez](https://github.com/tomkat-cr/genericsuite-app-maker)...
- **[intelligent-invoicing-agent](../agents/intelligent-invoicing-agent.md)** (business): Author: [Tino Joel Muchenje](https://github.com/Tinomuchenje)...


## Workflow

```json
{
  "type": "conditional",
  "steps": [
    {
      "step_id": "market_research",
      "agent_name": "advanced-web-researcher",
      "action": "research",
      "description": "Research market trends and company fundamentals",
      "inputs": {
        "query": "${investment_target} market analysis trends financials"
      },
      "timeout": 400
    },
    {
      "step_id": "sentiment_analysis",
      "agent_name": "ask-reddit-agent",
      "action": "analyze",
      "description": "Analyze retail investor sentiment",
      "inputs": {
        "query": "${investment_target} stock discussion opinion"
      },
      "timeout": 300
    },
    {
      "step_id": "news_summary",
      "agent_name": "youtube-summary-agent",
      "action": "summarize",
      "description": "Summarize financial news and analysis videos",
      "inputs": {
        "query": "${investment_target} financial news analysis"
      },
      "timeout": 350
    },
    {
      "step_id": "financial_model",
      "agent_name": "genericsuite-app-maker-agent",
      "action": "generate",
      "description": "Generate financial analysis models",
      "inputs": {
        "research_data": "${market_research}",
        "sentiment_data": "${sentiment_analysis}",
        "news_data": "${news_summary}"
      },
      "timeout": 500
    },
    {
      "step_id": "cost_analysis",
      "agent_name": "intelligent-invoicing-agent",
      "action": "analyze",
      "description": "Analyze investment costs and fees",
      "inputs": {
        "investment_data": "${financial_model}"
      },
      "timeout": 200
    }
  ]
}
```

## Benefits

- Comprehensive investment analysis from multiple perspectives
- Combines technical analysis with sentiment analysis
- Generates actionable financial models
- Includes cost analysis for informed decisions
- Integrates both professional and retail investor insights

## Use Cases

- Individual stock analysis
- Portfolio optimization research
- Market sector analysis
- Investment thesis validation
- Risk assessment and due diligence

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("ai-investment-research-suite", "Your input data here")

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
