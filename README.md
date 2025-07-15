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
- **Python MCP Server**: Provides the MCP interface, communicates with REAPER via file-based IPC

The communication flow:
1. MCP client sends request → Python server
2. Python server writes JSON file → Bridge directory
3. Lua bridge reads file → Executes REAPER API
4. Lua bridge writes response → Bridge directory  
5. Python server reads response → Returns to MCP client

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

**Note:** The quick install script may reference outdated configurations. For the most reliable setup, follow the manual instructions below.

## Manual Setup

### 1. Install Python dependencies

```bash
pip install -e .
```

### 2. Set up the bridge

Currently, only the **file-based bridge** is fully implemented and tested. The socket-based bridge exists but lacks a corresponding server implementation.

#### File-based Bridge (Recommended)

This method requires no additional dependencies and is the most reliable:

1. Copy the bridge script to REAPER:
   ```bash
   cp lua/mcp_bridge_file_v2.lua ~/Library/Application\ Support/REAPER/Scripts/
   ```

2. Load the bridge in REAPER:
   - Open REAPER
   - Go to Actions → Show action list
   - Click "Load..." and select `mcp_bridge_file_v2.lua`
   - Run the action (check the REAPER console for startup message)

3. Start the MCP server:
   ```bash
   python -m server.app
   ```

**Note:** The server will display "Make sure mcp_bridge_no_socket.lua is running" but you should use `mcp_bridge_file_v2.lua` as documented above.

#### Socket-based Bridge (Not Currently Implemented)

While the Lua script `lua/mcp_bridge.lua` exists for socket-based communication, there is no corresponding Python server implementation. The socket bridge requires LuaSocket and would need a server that listens on UDP port 9000.

### 3. Verify the setup

1. Check REAPER console shows: "MCP Bridge Started"
2. Check Python server shows: "Server ready. Waiting for connections..."
3. The bridge uses file-based communication via `~/Library/Application Support/REAPER/Scripts/mcp_bridge_data/`

## Testing

Make sure you have:
1. REAPER running with `mcp_bridge_file_v2.lua` loaded
2. The MCP server running (`python -m server.app`)

Then run the tests:

```bash
pytest tests/ -v
```

**Note:** Some tests may fail due to timing issues or minor output format differences. The core functionality has been verified to work correctly.

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