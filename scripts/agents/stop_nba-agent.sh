#!/bin/bash

# Stop script for nba-agent

AGENT_NAME="nba-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*nba-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
