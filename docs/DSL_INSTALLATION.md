# DSL/Macros Installation Guide

This guide explains how to install the DSL (Domain Specific Language) functions for the REAPER MCP bridge.

## Installation Steps

1. **Backup your existing bridge file**
   ```bash
   cp ~/Library/Application\ Support/REAPER/Scripts/mcp_bridge_file_v2.lua ~/Library/Application\ Support/REAPER/Scripts/mcp_bridge_file_v2.lua.backup
   ```

2. **Copy the DSL functions file to REAPER Scripts directory**
   ```bash
   cp lua/mcp_bridge_dsl_functions.lua ~/Library/Application\ Support/REAPER/Scripts/
   ```

3. **Add DSL functions to the main bridge file**
   
   You need to modify `mcp_bridge_file_v2.lua` in two places:

   a. **Add at the top of the file (after line 10):**
   ```lua
   -- Load DSL functions
   dofile(reaper.GetResourcePath() .. '/Scripts/mcp_bridge_dsl_functions.lua')
   ```

   b. **Add the DSL function handlers before line 3294** (before the `else` that handles unknown functions):
   
   Copy the entire contents of `lua/mcp_bridge_dsl_patch.lua` and paste it at the appropriate location in the bridge file.

## Using the DSL Profile

Once installed, you can use the DSL tools by running the MCP server with the DSL profile:

```bash
# Use only DSL tools (15 tools)
python run_with_relay.py --profile dsl

# Use DSL tools plus essential production tools
python run_with_relay.py --profile dsl-production
```

## Testing the Installation

Run the DSL integration tests to verify everything is working:

```bash
python -m pytest tests/test_dsl_integration.py -v
```

## Features

The DSL layer provides:

- **Natural language track references**: "bass", "drums", "track 3", "last track"
- **Flexible time references**: "8 bars", "selection", "cursor", "loop"
- **Smart volume/pan controls**: "-6dB", "+3", "L50", "R30"
- **Context awareness**: Remembers last referenced tracks/items
- **Disambiguation**: Returns multiple options when unsure

## Troubleshooting

1. **"Unknown function" errors**: Make sure you added the DSL functions before the generic function handler in the Lua bridge file.

2. **"Module not found" errors**: Ensure the `mcp_bridge_dsl_functions.lua` file is in the REAPER Scripts directory.

3. **Bridge not responding**: Check that REAPER is running and the bridge script is active in the Actions list.