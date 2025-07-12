#!/usr/bin/env bash
cd "/Users/stevehiehn/total-reaper-mcp"
source venv/bin/activate
echo "Starting REAPER MCP Server..."
python -m server.app
