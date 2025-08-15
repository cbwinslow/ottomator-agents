# global-real-estate-intelligence-network

## Overview

Multi-region real estate analysis combining local expertise with global trends

## Component Agents

This combination includes the following agents working together:

- **[gilbert-real-estate-agent](../agents/gilbert-real-estate-agent.md)** (business): Author: [Ivan Milennyi](https://stellular-halva-641b23.netlify.app/)...
- **[bali-property-agent](../agents/bali-property-agent.md)** (business): Author: [Gaurav Daryanani](https://www.youtube.com/watch?v=P8I8bfrpn_w)...
- **[travel-agent](../agents/travel-agent.md)** (travel): Author: [Sriram Muthu](https://bookedwithai.com)...
- **[advanced-web-researcher](../agents/advanced-web-researcher.md)** (research): Author: [Cole Medin](https://www.youtube.com/@ColeMedin)...
- **[linkedin-x-blog-content-creator](../agents/linkedin-x-blog-content-creator.md)** (content): Author: [Nate Herkelman](https://www.youtube.com/@nateherk)...


## Workflow

```json
{
  "type": "parallel",
  "steps": [
    {
      "step_id": "us_market_analysis",
      "agent_name": "gilbert-real-estate-agent",
      "action": "analyze",
      "description": "Analyze US real estate market",
      "inputs": {
        "location": "${target_location}",
        "property_type": "${property_type}"
      },
      "timeout": 400
    },
    {
      "step_id": "international_analysis",
      "agent_name": "bali-property-agent",
      "action": "analyze",
      "description": "Analyze international property markets",
      "inputs": {
        "region": "${target_region}",
        "investment_type": "${investment_type}"
      },
      "timeout": 400
    },
    {
      "step_id": "location_intelligence",
      "agent_name": "travel-agent",
      "action": "research",
      "description": "Research location amenities and lifestyle factors",
      "inputs": {
        "destination": "${target_location}"
      },
      "timeout": 300
    },
    {
      "step_id": "market_trends",
      "agent_name": "advanced-web-researcher",
      "action": "research",
      "description": "Research global real estate trends",
      "inputs": {
        "query": "real estate trends ${target_location} market analysis"
      },
      "timeout": 350
    }
  ]
}
```

## Benefits

- Global perspective on real estate investments
- Multi-region market comparison
- Lifestyle and amenity analysis
- Investment opportunity identification
- Marketing content for real estate professionals

## Use Cases

- International property investment
- Relocation planning
- Real estate market research
- Investment portfolio diversification
- Property development feasibility

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("global-real-estate-intelligence-network", "Your input data here")

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
