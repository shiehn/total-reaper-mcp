#!/usr/bin/env bash
set -e

echo "🎹 REAPER MCP Server Uninstaller"
echo "================================"

# Remove from REAPER Scripts
SCRIPTS_DIR="$HOME/Library/Application Support/REAPER/Scripts"
if [ -f "$SCRIPTS_DIR/mcp_bridge.lua" ]; then
    echo "Removing Lua bridge script..."
    rm "$SCRIPTS_DIR/mcp_bridge.lua"
fi

# Remove from startup script
STARTUP_SCRIPT="$SCRIPTS_DIR/__startup.lua"
if [ -f "$STARTUP_SCRIPT" ]; then
    echo "Removing from startup script..."
    # Remove the MCP bridge lines
    sed -i '' '/-- REAPER MCP Bridge/,+1d' "$STARTUP_SCRIPT"
    # Remove empty file if that was all it contained
    if [ ! -s "$STARTUP_SCRIPT" ]; then
        rm "$STARTUP_SCRIPT"
    fi
fi

# Remove LaunchAgent
PLIST_FILE="$HOME/Library/LaunchAgents/com.reaper.mcp.server.plist"
if [ -f "$PLIST_FILE" ]; then
    echo "Removing auto-start configuration..."
    launchctl unload "$PLIST_FILE" 2>/dev/null || true
    rm "$PLIST_FILE"
fi

# Remove desktop shortcut
if [ -f "$HOME/Desktop/REAPER MCP Server.command" ]; then
    echo "Removing desktop shortcut..."
    rm "$HOME/Desktop/REAPER MCP Server.command"
fi

echo ""
echo "✅ REAPER MCP Server uninstalled"
echo ""
echo "Note: The project files and virtual environment remain in:"
echo "  $(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "You can delete this directory manually if desired."