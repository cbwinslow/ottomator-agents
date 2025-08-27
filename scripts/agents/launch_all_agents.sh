#!/bin/bash

# Launch all agents script

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Launching all agents..."

# Launch each agent in background
for script in "$SCRIPTS_DIR"/launch_*.sh; do
    if [ -f "$script" ] && [[ "$(basename "$script")" != "launch_all_agents.sh" ]]; then
        agent_name=$(basename "$script" .sh | sed 's/launch_//')
        echo "Starting $agent_name..."
        "$script" &
        sleep 2
    fi
done

echo "✅ All agents launched"
echo "Use stop_all_agents.sh to stop all agents"
