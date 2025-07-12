# REAPER MCP Server

An MCP (Model Context Protocol) server that exposes REAPER DAW functionality through a clean API interface.

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

- `insert_track`: Insert a new track at specified index
- `get_track_count`: Get the number of tracks in current project  
- `get_reaper_version`: Get REAPER version string

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