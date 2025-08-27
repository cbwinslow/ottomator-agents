#!/bin/bash

# Stop script for TinyDM-agent

AGENT_NAME="TinyDM-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*TinyDM-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
