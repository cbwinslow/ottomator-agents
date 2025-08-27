#!/bin/bash

# Stop script for python-local-ai-agent

AGENT_NAME="python-local-ai-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*python-local-ai-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
