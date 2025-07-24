# REAPER MCP Server

An MCP (Model Context Protocol) server that exposes [REAPER DAW](https://www.reaper.fm/) functionality through a clean API interface.

![REAPER MCP Server](assets/repo-readme-image.png)

## Platform Support

This project is developed and tested on **macOS** but should work on Windows and Linux with minimal adaptation, as REAPER provides consistent cross-platform support.

## Requirements

- [REAPER](https://www.reaper.fm/) 6.83+ (includes embedded Lua 5.4 and full ReaScript API)
- Python 3.10+ (required for MCP 1.1.2+)
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

## Quick Start


### For AI/LLM Integration (Recommended)

```bash
# Start with default profile (dsl-production: 53 tools)
# Includes natural language DSL + essential production tools
python -m server.app

# Or choose a specific profile:
python -m server.app --profile dsl              # Minimal natural language only (15 tools)
python -m server.app --profile groq-essential   # Traditional ReaScript tools (146 tools)
python -m server.app --profile full             # All tools (600+ tools)
```

The default `dsl-production` profile is optimized for AI/LLM use, providing natural language commands plus essential MIDI, FX, and rendering tools.

### Quick Install (macOS)

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
# Create and activate virtual environment (Python 3.10+ required)
python3.10 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .
```

### 2. Set up the bridge

Currently, only the **file-based bridge** is fully implemented and tested. The socket-based bridge exists but lacks a corresponding server implementation.

#### Bridge Setup

The MCP server communicates with REAPER through a file-based bridge. This requires no additional dependencies and is the most reliable method.

1. Install the bridge:
   ```bash
   ./scripts/install_bridge.sh
   ```

2. Load the bridge in REAPER:
   - Open REAPER
   - Go to Actions → Show action list
   - Click "Load..." and select `mcp_bridge_file_v2.lua` from your Scripts folder
   - Run the action (check the REAPER console for startup message)

3. Start the MCP server:
   ```bash
   # Default profile (dsl-production: 53 tools with natural language interface)
   python -m server.app
   
   # Or with a specific profile
   python -m server.app --profile dsl      # Natural language tools only (15 tools)
   python -m server.app --profile full     # All tools (600+ tools)
   ```

**Important Architecture Note:** 
- There is only ONE bridge script (`lua/mcp_bridge.lua`) that supports ALL profiles
- The bridge includes both traditional ReaScript functions (600+) and DSL functions
- Profile selection happens in the Python MCP server, NOT in the bridge
- The bridge is installed as `mcp_bridge_file_v2.lua` for backward compatibility


#### Socket-based Bridge (Not Currently Implemented)

While the Lua script `lua/mcp_bridge.lua` exists for socket-based communication, there is no corresponding Python server implementation. The socket bridge requires LuaSocket and would need a server that listens on UDP port 9000.

### 3. Verify the setup

1. Check REAPER console shows: "REAPER MCP Bridge (File-based, Full API) started"
2. Check Python server shows: "Server ready. Waiting for connections..."
3. The server will display which profile is active and how many tools were registered
4. The bridge uses file-based communication via `~/Library/Application Support/REAPER/Scripts/mcp_bridge_data/`

## Testing

Make sure you have:
1. REAPER running with `mcp_bridge_file_v2.lua` loaded
2. The MCP server running (`python -m server.app`)

Then run the tests:

```bash
pytest tests/ -v
```

To test specific profiles:
```bash
# Test DSL tools
MCP_TEST_PROFILE=dsl pytest tests/test_dsl_minimal.py -v

# Test with a different profile
MCP_TEST_PROFILE=mixing pytest tests/test_integration.py -v
```

**Note:** Some tests may fail due to timing issues or minor output format differences. The core functionality has been verified to work correctly.

For integration tests specifically:
```bash
pytest tests/test_integration.py -v
```

### Natural Language Testing

The REAPER MCP Server includes comprehensive natural language processing (NLP) tests to ensure the system correctly maps user intent to appropriate tools. These tests are particularly important for AI/LLM integration.

#### Basic NLP Tests
```bash
# From the reaper-chat directory
cd reaper-chat
node test-nlp-mcp-mapping.js
```

This runs tests to verify that natural language inputs correctly map to MCP tools.

#### Enhanced NLP Tests with Conversation Tracking
For comprehensive testing with quality evaluation and improvement tracking:

```bash
# Ensure you have an OpenAI API key set
export OPENAI_API_KEY=your-api-key-here

# Run enhanced tests with conversation tracking
node test-nlp-with-tracking.js
```

This advanced test suite:
- Executes actual REAPER commands through MCP
- Evaluates response quality on multiple dimensions
- Tracks all conversations for pattern analysis
- Generates actionable improvement reports

See [reaper-chat/RUN-TRACKED-TESTS.md](reaper-chat/RUN-TRACKED-TESTS.md) for detailed information on:
- Running the enhanced test suite
- Understanding quality metrics
- Using conversation tracking for continuous improvement
- Implementing suggested improvements

The conversation tracking system creates detailed reports in `reaper-chat/conversation-tracking/` that help identify:
- Common failure patterns
- Specific queries that need improvement
- Progress tracking between test sessions

## Tool Profiles

The REAPER MCP Server supports **tool profiles** to limit which tools are exposed based on your needs or LLM limitations. Many LLMs have tool count restrictions (e.g., Groq: 128, OpenAI: 128), and profiles help you stay within these limits while focusing on the tools you need.

### Available Profiles

| Profile | Tool Count | Description | Use Case |
|---------|------------|-------------|----------|
| `dsl-production` | ~53 | DSL + essential tools | **DEFAULT** - Natural language + core production |
| `dsl` | **15** | Natural language DSL tools | Minimal AI-friendly interface |
| `groq-essential` | ~146 | Core REAPER functionality | Traditional tools, Groq-compatible |
| `groq-extended` | ~200+ | Extended functionality | More tools, may exceed Groq's limit |
| `minimal` | ~100 | Bare minimum tools | Testing and lightweight operations |
| `midi-production` | ~150 | MIDI-focused tools | MIDI composition and editing workflows |
| `mixing` | ~120 | Mixing and mastering tools | Audio mixing, effects, and routing |
| `full` | 600+ | All available tools | Complete access (may overwhelm LLMs) |

### Using Profiles

```bash
# List all available profiles
python -m server.app --list-profiles

# Start with default profile (dsl-production)
python -m server.app

# Start with a specific profile
python -m server.app --profile dsl           # Minimal natural language (15 tools)
python -m server.app --profile groq-essential # Traditional ReaScript interface
python -m server.app --profile mixing         # Mixing-focused tools
python -m server.app --profile full           # All 600+ tools

# Using with the relay script
python run_with_relay.py                      # Uses default (dsl-production)
python run_with_relay.py --profile dsl        # Minimal DSL profile
```

### DSL (Natural Language) Features

The DSL tools (included in the default `dsl-production` profile) provide a natural language friendly interface that understands flexible inputs:

- **Track references**: "bass", "drums", "track 3", "last track"
- **Volume formats**: "-6dB", "+3", "50%"
- **Time references**: "8 bars", "cursor", "selection"
- **Pan formats**: "L50", "R30", "center"

Example DSL usage:
```python
# Instead of complex ReaScript calls:
await dsl_track_create(name="Bass", role="bass")
await dsl_track_volume(track="bass", volume="-6dB")
await dsl_loop_create(track="bass", time="8 bars")
```

### Creating Custom Profiles

Add your own profile in `server/tool_profiles.py`:

```python
"my-workflow": {
    "name": "My Custom Workflow",
    "description": "Tools for my specific needs",
    "categories": [
        "DSL",          # Natural language tools
        "Tracks",       # Track management
        "MIDI",         # MIDI operations
        "FX",           # Effects
    ]
}
```

## Available Tools

The REAPER MCP Server implements **600+ tools** across 40+ categories. The number of tools available depends on the profile you choose (see Tool Profiles section above).

### Core DAW Functions
- Track Management & Controls
- Media Items & Takes  
- MIDI Operations
- Effects/FX Management
- Automation & Envelopes
- Project Management
- Transport & Playback

### Music Production Tools
- **Loop & Time Selection Management** - Loop points, time selection, grid quantization
- **Bounce & Render Operations** - Track bouncing, freezing, stem export
- **Groove & Quantization** - Humanization, swing, polyrhythms, tempo detection
- **Bus Routing & Mixing** - Submixes, parallel compression, sidechain routing

### Advanced Features
- Audio Analysis & Peak Detection
- Video & Visual Media Support
- Color Management
- Layout & Screenset Management
- Script Extension Support
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