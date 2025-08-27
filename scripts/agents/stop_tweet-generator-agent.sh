#!/bin/bash

# Stop script for tweet-generator-agent

AGENT_NAME="tweet-generator-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*tweet-generator-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
