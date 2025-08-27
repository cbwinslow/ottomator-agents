#!/bin/bash

# Stop script for pydantic-ai-langfuse

AGENT_NAME="pydantic-ai-langfuse"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*pydantic-ai-langfuse" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
