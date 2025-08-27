#!/bin/bash

# Stop script for ottomarkdown-agent

AGENT_NAME="ottomarkdown-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*ottomarkdown-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
