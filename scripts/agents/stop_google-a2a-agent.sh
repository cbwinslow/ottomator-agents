#!/bin/bash

# Stop script for google-a2a-agent

AGENT_NAME="google-a2a-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*google-a2a-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
