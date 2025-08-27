#!/bin/bash

# Stop script for pydantic-ai-advanced-researcher

AGENT_NAME="pydantic-ai-advanced-researcher"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*pydantic-ai-advanced-researcher" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
