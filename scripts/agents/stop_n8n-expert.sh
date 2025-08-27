#!/bin/bash

# Stop script for n8n-expert

AGENT_NAME="n8n-expert"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*n8n-expert" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
