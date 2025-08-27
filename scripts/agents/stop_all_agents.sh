#!/bin/bash

# Stop all agents script

echo "🛑 Stopping all agents..."

# Stop all agent processes
pkill -f "python.*agent"

echo "✅ All agents stopped"
