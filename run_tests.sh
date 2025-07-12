#!/usr/bin/env bash
set -e

echo "🧪 Running REAPER MCP Tests"
echo "=========================="
echo ""
echo "⚠️  IMPORTANT: Before running tests, ensure:"
echo "1. REAPER is running"
echo "2. The file-based bridge (lua/mcp_bridge_no_socket.lua) is loaded and running in REAPER"
echo ""
echo "If you see 'Connection closed' errors, the bridge is not running in REAPER."
echo ""

# Activate virtual environment
source venv/bin/activate

# Use file-based bridge by default
export USE_FILE_BRIDGE=true

# Run tests
echo "Running tests with file-based bridge..."
pytest tests/ -v "$@"