# real-estate-intelligence-agent

## Overview

Real estate analysis combining property research, market analysis, and content creation

## Component Agents

This combination includes the following agents working together:

- **[gilbert-real-estate-agent](../agents/gilbert-real-estate-agent.md)** (business): Author: [Ivan Milennyi](https://stellular-halva-641b23.netlify.app/)...
- **[bali-property-agent](../agents/bali-property-agent.md)** (business): Author: [Gaurav Daryanani](https://www.youtube.com/watch?v=P8I8bfrpn_w)...
- **[advanced-web-researcher](../agents/advanced-web-researcher.md)** (research): Author: [Cole Medin](https://www.youtube.com/@ColeMedin)...


## Workflow

```json
{
  "step1": "Research property markets and listings",
  "step2": "Analyze market trends and pricing",
  "step3": "Generate property reports and marketing materials"
}
```

## Benefits

- Multi-market property analysis
- Automated valuation insights
- Marketing material generation

## Use Cases

- Property investment analysis
- Market research
- Real estate marketing

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("real-estate-intelligence-agent", "Your input data here")

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
