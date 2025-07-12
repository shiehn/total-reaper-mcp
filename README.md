# REAPER MCP Server

An MCP (Model Context Protocol) server that exposes REAPER DAW functionality through a clean API interface.

## Requirements

- REAPER 6.83+ (includes embedded Lua 5.4 and full ReaScript API)
- Python 3.8+
- macOS, Windows, or Linux

## Architecture

This project uses a hybrid Lua-Python approach:
- **Lua Bridge**: Runs inside REAPER, handles API calls using REAPER's built-in Lua interpreter
- **Python MCP Server**: Provides the MCP interface, communicates with REAPER via UDP

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

## Manual Setup

### 1. Install Python dependencies

```bash
pip install -e .
```

### 2. Start REAPER and load the Lua bridge

1. Open REAPER
2. Go to Actions → Show action list
3. Click "Load..." and select `lua/mcp_bridge.lua`
4. Run the action (it will show "REAPER MCP Bridge started on port 9000" in the console)

### 3. Start the MCP server

```bash
python -m server.app
```

## Testing

With both REAPER (running the Lua bridge) and the MCP server running:

```bash
pytest tests/test_integration.py -v
```

## Available Tools

Currently implemented ReaScript methods (13 total):

### Track Management
- `insert_track`: Insert a new track at specified index
- `get_track_count`: Get the number of tracks in current project  
- `get_track`: Get track by index
- `get_master_track`: Get the master track
- `delete_track`: Delete a track by index
- `set_track_selected`: Select or deselect a track
- `get_track_name`: Get track name
- `set_track_name`: Set track name

### Track Controls
- `get_track_mute` / `set_track_mute`: Get/set track mute state
- `get_track_solo` / `set_track_solo`: Get/set track solo state

### System
- `get_reaper_version`: Get REAPER version string

For a complete list of implemented and planned methods, see [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md).

## Communication Flow

1. MCP Client → MCP Server (stdio)
2. MCP Server → REAPER Lua Bridge (UDP port 9000)
3. Lua Bridge executes REAPER API call
4. Lua Bridge → MCP Server (UDP port 9001)
5. MCP Server → MCP Client (stdio)

## Uninstall

```bash
./scripts/uninstall.sh
```

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

See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for details on which methods are currently implemented.

## Contributing

When adding new ReaScript methods:
1. Check the implementation checklist in IMPLEMENTATION_STATUS.md
2. Follow the existing patterns in the codebase
3. Include tests for all new methods
4. Update the implementation status document