# ecosystem-impact-analyzer

## Overview

Analyzes ripple effects and ecosystem impacts of decisions across multiple domains

## Component Agents

This combination includes the following agents working together:

- **[small-business-researcher](../agents/small-business-researcher.md)** (research): Author: [Zubair Trabzada](https://www.youtube.com/@AI-GPTWorkshop)...
- **[travel-agent](../agents/travel-agent.md)** (travel): Author: [Sriram Muthu](https://bookedwithai.com)...
- **[indoor-farming-agent](../agents/indoor-farming-agent.md)** (specialized): Author: [Aditya Prabhu](https://github.com/adityaprabhu16)...
- **[tech-stack-expert](../agents/tech-stack-expert.md)** (tech): Author: [Cole Medin](https://www.youtube.com/@ColeMedin)...
- **[genericsuite-app-maker-agent](../agents/genericsuite-app-maker-agent.md)** (content): Author: [Carlos J. Ramirez](https://github.com/tomkat-cr/genericsuite-app-maker)...


## Workflow

```json
{
  "type": "parallel",
  "steps": [
    {
      "step_id": "economic_ripples",
      "agent_name": "small-business-researcher",
      "action": "analyze",
      "description": "Analyze economic ripple effects",
      "inputs": {
        "decision": "${impact_scenario}"
      },
      "timeout": 350
    },
    {
      "step_id": "environmental_impact",
      "agent_name": "travel-agent",
      "action": "assess",
      "description": "Assess environmental and location impacts",
      "inputs": {
        "scenario": "${impact_scenario}"
      },
      "timeout": 300
    },
    {
      "step_id": "sustainability_analysis",
      "agent_name": "indoor-farming-agent",
      "action": "evaluate",
      "description": "Evaluate sustainability implications",
      "inputs": {
        "impact_type": "${impact_scenario}"
      },
      "timeout": 350
    },
    {
      "step_id": "technology_consequences",
      "agent_name": "tech-stack-expert",
      "action": "analyze",
      "description": "Analyze technology adoption consequences",
      "inputs": {
        "decision": "${impact_scenario}"
      },
      "timeout": 300
    },
    {
      "step_id": "systems_modeling",
      "agent_name": "genericsuite-app-maker-agent",
      "action": "model",
      "description": "Create systems model of all impacts",
      "inputs": {
        "economic": "${economic_ripples}",
        "environmental": "${environmental_impact}",
        "sustainability": "${sustainability_analysis}",
        "technology": "${technology_consequences}"
      },
      "timeout": 450
    }
  ]
}
```

## Benefits

- Holistic impact assessment across domains
- Unintended consequence identification
- Systems thinking approach to decision making
- Multi-dimensional risk analysis
- Sustainability impact quantification

## Use Cases

- Policy impact assessment
- Corporate decision analysis
- Environmental impact studies
- Technology adoption planning
- Urban planning and development

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("ecosystem-impact-analyzer", "Your input data here")

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
