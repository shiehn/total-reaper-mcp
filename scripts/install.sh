#!/usr/bin/env bash
set -e

echo "🎹 REAPER MCP Server Installer for macOS"
echo "======================================="

# Check if REAPER is installed
REAPER_APP="/Applications/REAPER.app"
if [ ! -d "$REAPER_APP" ]; then
    REAPER_APP="/Applications/REAPER64.app"
    if [ ! -d "$REAPER_APP" ]; then
        echo "❌ REAPER not found in /Applications"
        echo "Please install REAPER first: https://www.reaper.fm/download.php"
        exit 1
    fi
fi
echo "✅ Found REAPER at: $REAPER_APP"

# Find REAPER Scripts directory
SCRIPTS_DIR="$HOME/Library/Application Support/REAPER/Scripts"
if [ ! -d "$SCRIPTS_DIR" ]; then
    echo "📁 Creating REAPER Scripts directory..."
    mkdir -p "$SCRIPTS_DIR"
fi

# Get the repository root directory
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "📍 Repository location: $REPO_DIR"

# Copy Lua bridge script
echo "📝 Installing Lua bridge script..."
cp "$REPO_DIR/lua/mcp_bridge.lua" "$SCRIPTS_DIR/"
xattr -rd com.apple.quarantine "$SCRIPTS_DIR/mcp_bridge.lua" 2>/dev/null || true

# Install LuaSocket if not already installed
if [ ! -f "$SCRIPTS_DIR/socket.lua" ] || [ ! -d "$SCRIPTS_DIR/socket" ]; then
    echo "🔌 Installing LuaSocket for REAPER..."
    if [ -f "$REPO_DIR/scripts/install_luasocket.sh" ]; then
        "$REPO_DIR/scripts/install_luasocket.sh"
    else
        echo "⚠️  LuaSocket not found. You may need to install it manually."
        echo "   Run: $REPO_DIR/scripts/install_luasocket.sh"
    fi
else
    echo "✅ LuaSocket already installed"
fi

# Create startup script for REAPER
STARTUP_SCRIPT="$SCRIPTS_DIR/__startup.lua"
if [ -f "$STARTUP_SCRIPT" ]; then
    # Check if mcp_bridge is already in startup
    if ! grep -q "mcp_bridge.lua" "$STARTUP_SCRIPT"; then
        echo "📌 Adding MCP bridge to existing startup script..."
        echo "" >> "$STARTUP_SCRIPT"
        echo "-- REAPER MCP Bridge" >> "$STARTUP_SCRIPT"
        echo "dofile(reaper.GetResourcePath() .. '/Scripts/mcp_bridge.lua')" >> "$STARTUP_SCRIPT"
    else
        echo "✅ MCP bridge already in startup script"
    fi
else
    echo "📌 Creating startup script..."
    cat > "$STARTUP_SCRIPT" << 'EOF'
-- REAPER Startup Script
-- This script runs automatically when REAPER starts

-- REAPER MCP Bridge
dofile(reaper.GetResourcePath() .. '/Scripts/mcp_bridge.lua')
EOF
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install python@3.11
fi

# Create virtual environment and install dependencies
echo "🐍 Setting up Python environment..."
cd "$REPO_DIR"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -e .

# Create launch script
LAUNCH_SCRIPT="$REPO_DIR/launch_mcp_server.sh"
cat > "$LAUNCH_SCRIPT" << EOF
#!/usr/bin/env bash
cd "$REPO_DIR"
source venv/bin/activate
echo "Starting REAPER MCP Server..."
python -m server.app
EOF
chmod +x "$LAUNCH_SCRIPT"

# Create LaunchAgent for auto-start (optional)
read -p "Would you like the MCP server to start automatically on login? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    PLIST_FILE="$HOME/Library/LaunchAgents/com.reaper.mcp.server.plist"
    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.reaper.mcp.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>$LAUNCH_SCRIPT</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/reaper-mcp-server.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/reaper-mcp-server-error.log</string>
</dict>
</plist>
EOF
    launchctl load "$PLIST_FILE"
    echo "✅ MCP server will start automatically on login"
fi

# Create desktop shortcut (optional)
read -p "Would you like a desktop shortcut to start the MCP server? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cat > "$HOME/Desktop/REAPER MCP Server.command" << EOF
#!/usr/bin/env bash
$LAUNCH_SCRIPT
EOF
    chmod +x "$HOME/Desktop/REAPER MCP Server.command"
    echo "✅ Desktop shortcut created"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Start REAPER"
echo "2. The MCP bridge will load automatically on startup"
echo "3. Run the MCP server with: $LAUNCH_SCRIPT"
echo ""
echo "To test the installation:"
echo "  cd $REPO_DIR"
echo "  source venv/bin/activate"
echo "  python scripts/test_manual.py"
echo ""
echo "For MCP clients, connect to: stdio mode using 'python -m server.app'"