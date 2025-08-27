#!/bin/bash

# Stop script for ask-reddit-agent

AGENT_NAME="ask-reddit-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*ask-reddit-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
