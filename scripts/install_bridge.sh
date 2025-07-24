#!/bin/bash

# Script to install the DSL-enabled bridge to REAPER

REAPER_SCRIPTS_DIR="$HOME/Library/Application Support/REAPER/Scripts"
BRIDGE_FILE="lua/mcp_bridge.lua"
TARGET_NAME="mcp_bridge_file_v2.lua"  # Keep the same name so server doesn't need changes

echo "Installing MCP Bridge to REAPER..."
echo "=============================================="

# Check if bridge file exists
if [ ! -f "$BRIDGE_FILE" ]; then
    echo "Error: Bridge file not found at $BRIDGE_FILE"
    exit 1
fi

# Check if REAPER scripts directory exists
if [ ! -d "$REAPER_SCRIPTS_DIR" ]; then
    echo "Error: REAPER Scripts directory not found at $REAPER_SCRIPTS_DIR"
    echo "Is REAPER installed?"
    exit 1
fi

# Backup existing bridge if it exists
if [ -f "$REAPER_SCRIPTS_DIR/$TARGET_NAME" ]; then
    echo "Backing up existing bridge to ${TARGET_NAME}.backup"
    cp "$REAPER_SCRIPTS_DIR/$TARGET_NAME" "$REAPER_SCRIPTS_DIR/${TARGET_NAME}.backup"
fi

# Copy the new bridge
echo "Installing bridge..."
cp "$BRIDGE_FILE" "$REAPER_SCRIPTS_DIR/$TARGET_NAME"

if [ $? -eq 0 ]; then
    echo "✅ Bridge installed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Restart REAPER (or reload the bridge script)"
    echo "2. The bridge now includes all DSL functions built-in"
    echo "3. Start the server with: python -m server.app"
else
    echo "❌ Failed to install bridge"
    exit 1
fi