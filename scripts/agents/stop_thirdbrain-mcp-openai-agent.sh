#!/bin/bash

# Stop script for thirdbrain-mcp-openai-agent

AGENT_NAME="thirdbrain-mcp-openai-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*thirdbrain-mcp-openai-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
