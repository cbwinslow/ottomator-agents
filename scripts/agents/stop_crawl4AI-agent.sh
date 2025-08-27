#!/bin/bash

# Stop script for crawl4AI-agent

AGENT_NAME="crawl4AI-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*crawl4AI-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
