# business-intelligence-agent

## Overview

Business analysis agent combining market research, data analysis, and reporting

## Component Agents

This combination includes the following agents working together:

- **[small-business-researcher](../agents/small-business-researcher.md)** (research): Author: [Zubair Trabzada](https://www.youtube.com/@AI-GPTWorkshop)...
- **[advanced-web-researcher](../agents/advanced-web-researcher.md)** (research): Author: [Cole Medin](https://www.youtube.com/@ColeMedin)...
- **[genericsuite-app-maker-agent](../agents/genericsuite-app-maker-agent.md)** (content): Author: [Carlos J. Ramirez](https://github.com/tomkat-cr/genericsuite-app-maker)...


## Workflow

```json
{
  "step1": "Research business domain and competitors",
  "step2": "Gather market data and trends",
  "step3": "Generate business intelligence reports"
}
```

## Benefits

- Comprehensive market analysis
- Competitive intelligence
- Automated report generation

## Use Cases

- Market entry analysis
- Competitive analysis
- Business planning

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("business-intelligence-agent", "Your input data here")

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
