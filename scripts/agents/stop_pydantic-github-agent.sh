#!/bin/bash

# Stop script for pydantic-github-agent

AGENT_NAME="pydantic-github-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*pydantic-github-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
