# DSL-Production is Now the Default Profile

## What Changed

The default profile for the REAPER MCP Server has been changed from `groq-essential` to `dsl-production`.

## Why This Change?

1. **Better for AI/LLM Integration**: The DSL tools provide a natural language interface that's much easier for AI assistants to use effectively.

2. **Optimal Tool Count**: At ~53 tools, it stays well under the 128 tool limit of most LLMs while providing essential functionality.

3. **Best of Both Worlds**: Combines:
   - 15 natural language DSL tools for easy control
   - Essential MIDI generation tools
   - FX management for instruments
   - Rendering and freezing capabilities

## What This Means

### When you run without specifying a profile:
```bash
python -m server.app
# or
python run_with_relay.py
```

You'll automatically get the `dsl-production` profile with:
- Natural language track control ("bass", "drums", "-6dB")
- MIDI operations and generation
- Effects and instrument management
- Rendering and bouncing tools

### Previous behavior:
```bash
# Old default was groq-essential (146 traditional tools)
python -m server.app  # Would load groq-essential
```

### New behavior:
```bash
# New default is dsl-production (53 natural language + production tools)
python -m server.app  # Now loads dsl-production
```

## For Existing Users

If you prefer the old behavior with traditional ReaScript tools:
```bash
python -m server.app --profile groq-essential
```

## Benefits of the New Default

1. **Easier Commands**: Instead of complex function calls, use natural language
2. **Fewer Tools**: 53 vs 146 means faster processing and less context usage
3. **AI-Optimized**: Designed specifically for LLM interaction
4. **Production Ready**: Includes essential tools for real music production

## Examples with the New Default

```python
# Natural language track management
await dsl_track_create(name="Bass", role="bass")
await dsl_track_volume(track="bass", volume="-6dB")
await dsl_track_pan(track="bass", pan="C")

# Time and loops
await dsl_loop_create(track="drums", time="8 bars")
await dsl_time_select(time="16 bars")

# MIDI operations
await dsl_midi_insert(track="bass", time="8 bars", midi_data={...})
await dsl_quantize(items="selected", strength=0.9)

# Plus access to FX, rendering, and MIDI generation tools
```

## Installation Note

Remember to install the DSL Lua functions for full functionality:
```bash
cp lua/mcp_bridge_dsl_functions.lua ~/Library/Application\ Support/REAPER/Scripts/
```

Then follow the instructions in [DSL_INSTALLATION.md](DSL_INSTALLATION.md).