# educational-content-agent

## Overview

Educational material creation combining research, knowledge graphs, and multimedia generation

## Component Agents

This combination includes the following agents working together:

- **[general-researcher-agent](../agents/general-researcher-agent.md)** (research): Author: [Sam Liu](https://www.youtube.com/@54mliu)...
- **[agentic-rag-knowledge-graph](../agents/agentic-rag-knowledge-graph.md)** (knowledge): Agentic knowledge retrieval redefined with an AI agent system that combines traditional RAG (vector ...
- **[youtube-educator-plus-agent](../agents/youtube-educator-plus-agent.md)** (content): Author: [David Zhu](https://www.linkedin.com/in/david-zhu-704579248/)...


## Workflow

```json
{
  "step1": "Research educational topic comprehensively",
  "step2": "Map knowledge relationships and concepts",
  "step3": "Create multimedia educational content"
}
```

## Benefits

- Comprehensive topic coverage
- Knowledge relationship mapping
- Multi-format content creation

## Use Cases

- Course material development
- Educational video creation
- Training program design

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("educational-content-agent", "Your input data here")

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
