#!/bin/bash

# Stop script for light-rag-agent

AGENT_NAME="light-rag-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*light-rag-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
