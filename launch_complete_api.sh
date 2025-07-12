#!/bin/bash

echo "🚀 Launching REAPER MCP Server with COMPLETE ReaScript API"
echo "=================================================="
echo "✅ 94+ ReaScript methods available"
echo "✅ Full MIDI support"
echo "✅ Complete track, item, and FX control"
echo "✅ Transport, markers, envelopes, and more!"
echo ""
echo "📝 Make sure:"
echo "1. REAPER is running"
echo "2. lua/mcp_bridge_complete.lua is loaded in REAPER"
echo ""
echo "Starting server..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the complete API server
python server/app_complete.py