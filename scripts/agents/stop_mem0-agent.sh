#!/bin/bash

# Stop script for mem0-agent

AGENT_NAME="mem0-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*mem0-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
