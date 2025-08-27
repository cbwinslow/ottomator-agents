#!/bin/bash

# Stop script for mcp-agent-army

AGENT_NAME="mcp-agent-army"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*mcp-agent-army" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
