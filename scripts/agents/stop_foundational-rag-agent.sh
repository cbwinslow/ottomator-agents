#!/bin/bash

# Stop script for foundational-rag-agent

AGENT_NAME="foundational-rag-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*foundational-rag-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
