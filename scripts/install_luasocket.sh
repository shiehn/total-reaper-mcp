#!/usr/bin/env bash
set -e

echo "🔌 Installing LuaSocket for REAPER"
echo "================================="

# Check if REAPER is installed
REAPER_SCRIPTS="$HOME/Library/Application Support/REAPER/Scripts"
if [ ! -d "$REAPER_SCRIPTS" ]; then
    echo "❌ REAPER Scripts directory not found"
    echo "Please run REAPER at least once to create the directory"
    exit 1
fi

echo "📍 REAPER Scripts directory: $REAPER_SCRIPTS"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Please install Homebrew first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Install lua and luarocks if not present
echo "📦 Checking Lua installation..."
if ! brew list lua &> /dev/null; then
    echo "Installing Lua..."
    brew install lua
fi

if ! brew list luarocks &> /dev/null; then
    echo "Installing LuaRocks..."
    brew install luarocks
fi

# Create a temporary directory for building
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "📥 Downloading LuaSocket..."
# Download LuaSocket source
git clone https://github.com/lunarmodules/luasocket.git
cd luasocket

# REAPER uses Lua 5.4 embedded, so we need to compile for that version
echo "🔨 Compiling LuaSocket for REAPER's Lua 5.4..."

# Build for macOS with Lua 5.4
make macosx LUAV=5.4

# Copy the compiled libraries to REAPER Scripts directory
echo "📋 Installing to REAPER Scripts directory..."
mkdir -p "$REAPER_SCRIPTS/socket"
cp src/socket.lua "$REAPER_SCRIPTS/"
cp src/socket/*.so "$REAPER_SCRIPTS/socket/"
cp src/mime.lua "$REAPER_SCRIPTS/"
cp src/ltn12.lua "$REAPER_SCRIPTS/"

# Remove quarantine attributes
xattr -rd com.apple.quarantine "$REAPER_SCRIPTS/socket.lua" 2>/dev/null || true
xattr -rd com.apple.quarantine "$REAPER_SCRIPTS/socket/"*.so 2>/dev/null || true
xattr -rd com.apple.quarantine "$REAPER_SCRIPTS/mime.lua" 2>/dev/null || true
xattr -rd com.apple.quarantine "$REAPER_SCRIPTS/ltn12.lua" 2>/dev/null || true

# Clean up
cd /
rm -rf "$TEMP_DIR"

echo ""
echo "✅ LuaSocket installed successfully!"
echo ""
echo "The following files were installed:"
echo "  - $REAPER_SCRIPTS/socket.lua"
echo "  - $REAPER_SCRIPTS/socket/*.so"
echo "  - $REAPER_SCRIPTS/mime.lua"
echo "  - $REAPER_SCRIPTS/ltn12.lua"
echo ""
echo "You can now run the MCP bridge script in REAPER!"