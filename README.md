# REAPER MCP Server

An MCP (Model Context Protocol) server that exposes [REAPER DAW](https://www.reaper.fm/) functionality through a clean API interface.

![REAPER MCP Server](assets/repo-readme-image.png)

## Platform Support

This project is developed and tested on **macOS** but should work on Windows and Linux with minimal adaptation, as REAPER provides consistent cross-platform support.

## Requirements

- [REAPER](https://www.reaper.fm/) 6.83+ (includes embedded Lua 5.4 and full ReaScript API)
- Python 3.8+
- LuaSocket library (optional - only needed for socket-based communication)

## Architecture

This project uses a hybrid Lua-Python approach:
- **Lua Bridge**: Runs inside REAPER, handles API calls using REAPER's built-in Lua interpreter
- **Python MCP Server**: Provides the MCP interface, communicates with REAPER via:
  - **File-based communication** (recommended - no dependencies)
  - **Socket-based communication** (faster but requires LuaSocket)

## Quick Install (macOS)

```bash
./scripts/install.sh
```

This will:
- Install the Lua bridge to REAPER's Scripts folder
- Configure REAPER to load the bridge on startup
- Set up Python virtual environment
- Create launch scripts
- Optionally set up auto-start on login

**Note:** The quick install script sets up socket-based communication. For the recommended file-based approach, follow the manual setup instructions below.

## Manual Setup

### 1. Install Python dependencies

```bash
pip install -e .
```

### 2. Choose a bridge method

#### Option A: File-based Bridge (Recommended - No dependencies)

This method requires no additional dependencies and is the most reliable:

1. Load `lua/mcp_bridge_file_full.lua` in REAPER
2. Start the file-based server: `python -m server.app_file_bridge_full`

#### Option B: Socket-based Bridge (Faster performance, requires LuaSocket)

For better performance, you can use socket-based communication:

1. Install LuaSocket (macOS): `./scripts/install_luasocket.sh`
2. Load `lua/mcp_bridge.lua` in REAPER
3. Start the socket-based server: `python -m server.app`

Note: If you encounter a "socket.core not found" error, use the file-based bridge instead.

### 3. Start REAPER and load the Lua bridge

1. Open REAPER
2. Go to Actions → Show action list
3. Click "Load..." and select either:
   - `lua/mcp_bridge_file_full.lua` (for file-based, recommended)
   - `lua/mcp_bridge.lua` (for socket-based, requires LuaSocket)
4. Run the action (check the REAPER console for startup message)

### 4. Start the MCP server

For file-based bridge (recommended):
```bash
python -m server.app_file_bridge_full
```

For socket-based bridge:
```bash
python -m server.app
```

## Testing

Make sure you have:
1. REAPER running with the appropriate Lua bridge loaded
2. The corresponding MCP server running

Then run the tests:

```bash
pytest tests/ -v
```

For integration tests specifically:
```bash
pytest tests/test_integration.py -v
```

## Available Tools

The REAPER MCP Server implements **169+ ReaScript API methods** across 21 categories including:
- Track Management & Controls
- Media Items & Takes
- MIDI Operations
- Effects/FX Management
- Automation & Envelopes
- Project Management
- Transport & Playback
- And much more

For the complete list of all implemented methods, see [IMPLEMENTATION_MASTER.md](IMPLEMENTATION_MASTER.md).

## Communication Flow

### File-based (Recommended):
1. MCP Client → MCP Server (stdio)
2. MCP Server → REAPER Lua Bridge (via JSON files)
3. Lua Bridge executes REAPER API call
4. Lua Bridge → MCP Server (via JSON files)
5. MCP Server → MCP Client (stdio)

### Socket-based:
1. MCP Client → MCP Server (stdio)
2. MCP Server → REAPER Lua Bridge (UDP port 9000)
3. Lua Bridge executes REAPER API call
4. Lua Bridge → MCP Server (UDP port 9001)
5. MCP Server → MCP Client (stdio)

## Uninstall

```bash
./scripts/uninstall.sh
```

## About REAPER

[REAPER](https://www.reaper.fm/) is a complete digital audio production application for computers, offering a full multitrack audio and MIDI recording, editing, processing, mixing and mastering toolset. REAPER supports Windows, macOS, and Linux, providing consistent functionality across all platforms.

## API Reference

This project implements a subset of the [REAPER ReaScript API](https://www.reaper.fm/sdk/reascript/reascripthelp.html). The ReaScript API provides comprehensive control over REAPER's functionality including:

- Track management and routing
- Media items and takes
- MIDI editing
- Envelopes and automation  
- Effects and plugins
- Project management
- Transport control
- And much more

See [IMPLEMENTATION_MASTER.md](IMPLEMENTATION_MASTER.md) for details on which methods are currently implemented.

## Contributing

When adding new ReaScript methods:
1. Check the implementation checklist in IMPLEMENTATION_MASTER.md
2. Follow the existing patterns in the codebase
3. Include tests for all new methods
4. Update the implementation master list