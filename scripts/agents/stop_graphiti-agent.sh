#!/bin/bash

# Stop script for graphiti-agent

AGENT_NAME="graphiti-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*graphiti-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
