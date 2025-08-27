#!/bin/bash

# Stop script for agentic-rag-knowledge-graph

AGENT_NAME="agentic-rag-knowledge-graph"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*agentic-rag-knowledge-graph" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
