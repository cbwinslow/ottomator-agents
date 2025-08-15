# ai-powered-academic-research-pipeline

## Overview

End-to-end academic research from literature review to publication

## Component Agents

This combination includes the following agents working together:

- **[advanced-web-researcher](../agents/advanced-web-researcher.md)** (research): Author: [Cole Medin](https://www.youtube.com/@ColeMedin)...
- **[agentic-rag-knowledge-graph](../agents/agentic-rag-knowledge-graph.md)** (knowledge): Agentic knowledge retrieval redefined with an AI agent system that combines traditional RAG (vector ...
- **[foundational-rag-agent](../agents/foundational-rag-agent.md)** (knowledge): A simple Retrieval-Augmented Generation (RAG) AI agent using Pydantic AI and Supabase with pgvector ...
- **[genericsuite-app-maker-agent](../agents/genericsuite-app-maker-agent.md)** (content): Author: [Carlos J. Ramirez](https://github.com/tomkat-cr/genericsuite-app-maker)...
- **[linkedin-x-blog-content-creator](../agents/linkedin-x-blog-content-creator.md)** (content): Author: [Nate Herkelman](https://www.youtube.com/@nateherk)...


## Workflow

```json
{
  "type": "sequential",
  "steps": [
    {
      "step_id": "literature_search",
      "agent_name": "advanced-web-researcher",
      "action": "research",
      "description": "Comprehensive literature search",
      "inputs": {
        "query": "${research_topic} academic papers research"
      },
      "timeout": 500
    },
    {
      "step_id": "knowledge_mapping",
      "agent_name": "agentic-rag-knowledge-graph",
      "action": "map",
      "description": "Create research knowledge graph",
      "inputs": {
        "literature": "${literature_search}"
      },
      "timeout": 400
    },
    {
      "step_id": "reference_analysis",
      "agent_name": "foundational-rag-agent",
      "action": "analyze",
      "description": "Analyze references and citations",
      "inputs": {
        "knowledge_graph": "${knowledge_mapping}"
      },
      "timeout": 350
    },
    {
      "step_id": "paper_structure",
      "agent_name": "genericsuite-app-maker-agent",
      "action": "structure",
      "description": "Generate paper outline and structure",
      "inputs": {
        "research_data": "${reference_analysis}"
      },
      "timeout": 300
    },
    {
      "step_id": "academic_writing",
      "agent_name": "linkedin-x-blog-content-creator",
      "action": "write",
      "description": "Generate academic content",
      "inputs": {
        "structure": "${paper_structure}",
        "research": "${reference_analysis}"
      },
      "timeout": 600
    }
  ]
}
```

## Benefits

- Automated literature review process
- Knowledge graph visualization of research domain
- Citation analysis and gap identification
- Structured academic writing assistance
- Research methodology recommendations

## Use Cases

- PhD dissertation research
- Systematic literature reviews
- Grant proposal preparation
- Conference paper writing
- Research collaboration

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("ai-powered-academic-research-pipeline", "Your input data here")

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
