#!/bin/bash

# Stop script for pydantic-ai-mcp-agent

AGENT_NAME="pydantic-ai-mcp-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*pydantic-ai-mcp-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
