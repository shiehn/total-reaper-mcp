# Modern MCP Pattern Migration Guide

This document outlines the migration from the legacy MCP pattern to the modern `@mcp.tool()` decorator pattern.

## Overview

The Model Context Protocol (MCP) has evolved to use a more Pythonic decorator-based approach. This migration will transform our monolithic 7700+ line server file into a modular, maintainable architecture.

## Key Benefits

### 1. **Code Organization**
- **Before**: Single file with 228 tools in one massive if/elif chain
- **After**: Tools can be organized into logical modules (tracks.py, midi.py, fx.py, etc.)

### 2. **Type Safety**
- **Before**: Manual parameter extraction from dictionaries
- **After**: Type hints provide automatic validation and better IDE support

### 3. **Documentation**
- **Before**: Separate schema definitions and implementation
- **After**: Docstrings are automatically used for tool descriptions

### 4. **Error Handling**
- **Before**: Manual error response formatting
- **After**: Standard Python exceptions with automatic handling

### 5. **Testing**
- **Before**: Testing requires mocking the entire call_tool function
- **After**: Each tool function can be tested independently

## Pattern Comparison

### Legacy Pattern
```python
@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="insert_track",
            description="Insert a new track at the specified index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "The index where the track should be inserted (0-based)",
                        "minimum": 0
                    },
                    "use_defaults": {
                        "type": "boolean",
                        "description": "Whether to use default track settings",
                        "default": True
                    }
                },
                "required": ["index"]
            }
        ),
        # ... 227 more tools
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "insert_track":
        index = arguments["index"]
        use_defaults = arguments.get("use_defaults", True)
        
        result = await bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully inserted track at index {index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to insert track: {result.get('error', 'Unknown error')}"
            )]
    elif name == "delete_track":
        # ... implementation
    # ... 227 more elif blocks
```

### Modern Pattern
```python
@mcp.tool()
async def insert_track(
    index: int,
    use_defaults: bool = True,
    ctx: Context
) -> str:
    """Insert a new track at the specified index.
    
    Args:
        index: The index where the track should be inserted (0-based)
        use_defaults: Whether to use default track settings
        ctx: MCP context
        
    Returns:
        Success or error message
    """
    result = await bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
    
    if result.get("ok"):
        return f"Successfully inserted track at index {index}"
    else:
        raise Exception(f"Failed to insert track: {result.get('error', 'Unknown error')}")
```

## Migration Strategy

### Phase 1: Infrastructure Setup
1. Update dependencies to ensure FastMCP support
2. Create `app_modern.py` as proof of concept
3. Test compatibility with existing clients

### Phase 2: Tool Migration
1. Create module structure:
   ```
   server/
   ├── tools/
   │   ├── __init__.py
   │   ├── tracks.py      # Track management tools
   │   ├── media_items.py # Media item tools
   │   ├── midi.py        # MIDI tools
   │   ├── fx.py          # Effects tools
   │   ├── project.py     # Project management
   │   └── ...
   ```

2. Migrate tools by category, maintaining backward compatibility

### Phase 3: Testing
1. Update test suite to work with new pattern
2. Ensure all 228 tools maintain identical functionality
3. Performance testing

### Phase 4: Deprecation
1. Mark old pattern as deprecated
2. Update documentation
3. Remove legacy code

## Module Organization Plan

```python
# server/tools/tracks.py
from ..bridge import bridge
from mcp.server.fastmcp import Context

@mcp.tool()
async def insert_track(index: int, use_defaults: bool = True, ctx: Context) -> str:
    """Insert a new track at the specified index."""
    # implementation

@mcp.tool()
async def delete_track(track_index: int, ctx: Context) -> str:
    """Delete a track by index."""
    # implementation

# ... more track tools
```

```python
# server/tools/midi.py
@mcp.tool()
async def midi_insert_note(
    take_index: int,
    channel: int,
    pitch: int,
    velocity: int,
    start_pos: float,
    end_pos: float,
    ctx: Context
) -> str:
    """Insert a MIDI note."""
    # implementation

# ... more MIDI tools
```

## Advantages for AI Consumption

1. **Better Discovery**: Modern AI systems expect the `@mcp.tool()` pattern
2. **Automatic Schema Generation**: Type hints provide schema without manual JSON
3. **Context Awareness**: The Context parameter enables advanced features
4. **Standard Patterns**: Follows Python best practices that AI understands

## Next Steps

1. Review and approve migration plan
2. Set up parallel testing environment
3. Begin incremental migration
4. Update all documentation
5. Notify users of changes

## Timeline Estimate

- Phase 1: 1-2 days
- Phase 2: 3-5 days (migrating 228 tools)
- Phase 3: 2-3 days
- Phase 4: 1 day

Total: ~2 weeks for complete migration