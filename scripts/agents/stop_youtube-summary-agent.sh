#!/bin/bash

# Stop script for youtube-summary-agent

AGENT_NAME="youtube-summary-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*youtube-summary-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
