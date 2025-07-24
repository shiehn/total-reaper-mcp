#!/usr/bin/env bash
cd "/Users/stevehiehn/total-reaper-mcp"

# Check if .venv-py310 exists (Python 3.10 required for MCP)
if [ -d ".venv-py310" ]; then
    source .venv-py310/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: No virtual environment found!"
    exit 1
fi

# Get profile from command line or use dsl as default
PROFILE="${1:-dsl}"

echo "Starting REAPER MCP Server with profile: $PROFILE"
python -m server.app --profile "$PROFILE"