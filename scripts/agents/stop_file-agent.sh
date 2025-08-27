#!/bin/bash

# Stop script for file-agent

AGENT_NAME="file-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*file-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
