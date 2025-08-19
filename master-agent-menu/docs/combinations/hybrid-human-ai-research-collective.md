# hybrid-human-ai-research-collective

## Overview

Experimental combination simulating human research team dynamics with AI agents

## Component Agents

This combination includes the following agents working together:

- **[general-researcher-agent](../agents/general-researcher-agent.md)** (research): Author: [Sam Liu](https://www.youtube.com/@54mliu)...
- **[advanced-web-researcher](../agents/advanced-web-researcher.md)** (research): Author: [Cole Medin](https://www.youtube.com/@ColeMedin)...
- **[agentic-rag-knowledge-graph](../agents/agentic-rag-knowledge-graph.md)** (knowledge): Agentic knowledge retrieval redefined with an AI agent system that combines traditional RAG (vector ...
- **[nba-agent](../agents/nba-agent.md)** (social): Author: [Elo Mukoro](https://nbaagent-production.up.railway.app/)...
- **[tech-stack-expert](../agents/tech-stack-expert.md)** (tech): Author: [Cole Medin](https://www.youtube.com/@ColeMedin)...


## Workflow

```json
{
  "type": "conditional",
  "steps": [
    {
      "step_id": "research_planning",
      "agent_name": "general-researcher-agent",
      "action": "plan",
      "description": "Create research methodology and plan",
      "inputs": {
        "research_question": "${research_question}"
      },
      "timeout": 300
    },
    {
      "step_id": "data_collection",
      "agent_name": "advanced-web-researcher",
      "action": "collect",
      "description": "Collect research data systematically",
      "inputs": {
        "methodology": "${research_planning}"
      },
      "timeout": 500
    },
    {
      "step_id": "statistical_analysis",
      "agent_name": "nba-agent",
      "action": "analyze",
      "description": "Perform statistical analysis (repurposed for general data)",
      "inputs": {
        "data": "${data_collection}"
      },
      "timeout": 350
    },
    {
      "step_id": "knowledge_synthesis",
      "agent_name": "agentic-rag-knowledge-graph",
      "action": "synthesize",
      "description": "Create knowledge synthesis and insights",
      "inputs": {
        "analysis": "${statistical_analysis}",
        "raw_data": "${data_collection}"
      },
      "timeout": 400
    },
    {
      "step_id": "technical_validation",
      "agent_name": "tech-stack-expert",
      "action": "validate",
      "description": "Validate methodology and technical aspects",
      "inputs": {
        "synthesis": "${knowledge_synthesis}"
      },
      "timeout": 250,
      "conditions": {
        "previous_step_success": true
      }
    }
  ]
}
```

## Benefits

- Simulates human research team collaboration
- Combines different analytical perspectives
- Multi-disciplinary approach to research
- Unconventional agent repurposing for creativity
- Hierarchical research validation process

## Use Cases

- Interdisciplinary research projects
- Research methodology validation
- Academic collaboration simulation
- Cross-domain knowledge transfer
- Research process optimization

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("hybrid-human-ai-research-collective", "Your input data here")

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
