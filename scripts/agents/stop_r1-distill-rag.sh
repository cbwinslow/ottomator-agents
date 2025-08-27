#!/bin/bash

# Stop script for r1-distill-rag

AGENT_NAME="r1-distill-rag"

echo "🛑 Stopping $AGENT_NAME..."

# Find and kill processes related to this agent
pgrep -f "python.*r1-distill-rag" | xargs -r kill

echo "✅ $AGENT_NAME stopped"
