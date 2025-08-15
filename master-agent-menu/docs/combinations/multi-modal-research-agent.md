# multi-modal-research-agent

## Overview

Comprehensive research agent combining web search, knowledge retrieval, and content generation

## Component Agents

This combination includes the following agents working together:

- **[advanced-web-researcher](../agents/advanced-web-researcher.md)** (research): Author: [Cole Medin](https://www.youtube.com/@ColeMedin)...
- **[foundational-rag-agent](../agents/foundational-rag-agent.md)** (knowledge): A simple Retrieval-Augmented Generation (RAG) AI agent using Pydantic AI and Supabase with pgvector ...
- **[linkedin-x-blog-content-creator](../agents/linkedin-x-blog-content-creator.md)** (content): Author: [Nate Herkelman](https://www.youtube.com/@nateherk)...


## Workflow

```json
{
  "step1": "Use web researcher to gather current information",
  "step2": "Use RAG agent to retrieve relevant knowledge",
  "step3": "Use content creator to synthesize findings"
}
```

## Benefits

- Combines real-time web data with stored knowledge
- Produces professional content output
- Comprehensive research coverage

## Use Cases

- Market research reports
- Technical documentation
- Content marketing materials

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("multi-modal-research-agent", "Your input data here")

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
