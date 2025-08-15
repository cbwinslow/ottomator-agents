# omnimedia-content-intelligence-platform

## Overview

Comprehensive content analysis across text, video, and social media platforms

## Component Agents

This combination includes the following agents working together:

- **[youtube-video-summarizer](../agents/youtube-video-summarizer.md)** (media): Author: [Mike Russell](https://n8n.io/creators/mikerussell/)...
- **[ask-reddit-agent](../agents/ask-reddit-agent.md)** (social): <!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Tem...
- **[tweet-generator-agent](../agents/tweet-generator-agent.md)** (content): Author: [Pavel Cherkashin](https://github.com/pcherkashin)...
- **[crawl4AI-agent](../agents/crawl4AI-agent.md)** (web): An intelligent documentation crawler and RAG (Retrieval-Augmented Generation) agent built using Pyda...
- **[agentic-rag-knowledge-graph](../agents/agentic-rag-knowledge-graph.md)** (knowledge): Agentic knowledge retrieval redefined with an AI agent system that combines traditional RAG (vector ...
- **[streambuzz-agent](../agents/streambuzz-agent.md)** (media): Author: [Mohammed Hammaad](https://github.com/hammaadworks)...


## Workflow

```json
{
  "type": "sequential",
  "steps": [
    {
      "step_id": "video_analysis",
      "agent_name": "youtube-video-summarizer",
      "action": "analyze",
      "description": "Analyze video content and trends",
      "inputs": {
        "topic": "${content_topic}"
      },
      "timeout": 400
    },
    {
      "step_id": "discussion_analysis",
      "agent_name": "ask-reddit-agent",
      "action": "analyze",
      "description": "Analyze discussion forums and communities",
      "inputs": {
        "query": "${content_topic}"
      },
      "timeout": 350
    },
    {
      "step_id": "web_content_analysis",
      "agent_name": "crawl4AI-agent",
      "action": "crawl",
      "description": "Crawl and analyze web content",
      "inputs": {
        "search_query": "${content_topic}"
      },
      "timeout": 450
    },
    {
      "step_id": "media_trends",
      "agent_name": "streambuzz-agent",
      "action": "analyze",
      "description": "Analyze streaming and media trends",
      "inputs": {
        "topic": "${content_topic}"
      },
      "timeout": 300
    },
    {
      "step_id": "knowledge_synthesis",
      "agent_name": "agentic-rag-knowledge-graph",
      "action": "synthesize",
      "description": "Create knowledge graph from all sources",
      "inputs": {
        "video_data": "${video_analysis}",
        "discussion_data": "${discussion_analysis}",
        "web_data": "${web_content_analysis}",
        "media_data": "${media_trends}"
      },
      "timeout": 500
    },
    {
      "step_id": "content_generation",
      "agent_name": "tweet-generator-agent",
      "action": "generate",
      "description": "Generate cross-platform content",
      "inputs": {
        "synthesis": "${knowledge_synthesis}"
      },
      "timeout": 250
    }
  ]
}
```

## Benefits

- 360-degree content analysis across all major platforms
- Cross-media trend identification
- Comprehensive knowledge graph creation
- Multi-format content generation
- Real-time media intelligence

## Use Cases

- Brand monitoring and analysis
- Content strategy development
- Trend forecasting
- Competitive intelligence
- Crisis communication planning

## Usage Example

```python
from master_menu import AgentLauncher

# Initialize launcher
launcher = AgentLauncher()

# Launch the combination
execution_id = launcher.launch_combination("omnimedia-content-intelligence-platform", "Your input data here")

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
