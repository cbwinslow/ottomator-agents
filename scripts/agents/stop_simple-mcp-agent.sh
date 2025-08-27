#!/bin/bash

# Stop script for simple-mcp-agent

AGENT_NAME="simple-mcp-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*simple-mcp-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
