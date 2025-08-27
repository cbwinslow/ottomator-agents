#!/bin/bash

# Stop script for genericsuite-app-maker-agent

AGENT_NAME="genericsuite-app-maker-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*genericsuite-app-maker-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
