#!/bin/bash

# Stop script for pydantic-ai-langgraph-parallelization

AGENT_NAME="pydantic-ai-langgraph-parallelization"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*pydantic-ai-langgraph-parallelization" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
