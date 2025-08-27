#!/bin/bash

# Stop script for lead-generator-agent

AGENT_NAME="lead-generator-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*lead-generator-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
