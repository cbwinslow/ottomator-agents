#!/bin/bash

# Stop script for streambuzz-agent

AGENT_NAME="streambuzz-agent"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*streambuzz-agent" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
