#!/bin/bash

# Stop script for openai-sdk-agent

AGENT_NAME="openai-sdk-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*openai-sdk-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
