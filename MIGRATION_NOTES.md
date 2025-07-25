# Modern MCP Pattern Migration Notes

## Overview
Migrating from legacy MCP pattern (monolithic 7700+ line file with if/elif chains) to modern pattern using @mcp.tool() decorators.

**Branch**: `refactor/modern-mcp-decorators`

## Migration Status (as of 2025-07-13)

### ✅ Migration Complete! 
All tools have been successfully migrated from the legacy pattern to the modern @mcp.tool() decorator pattern.

### Completed Categories
- **Track Management** (65 tools) - `server/tools/tracks.py`
- **Core API & Utilities** (14 tools) - `server/tools/core_api.py`
- **Media Items & Takes** (29 tools) - `server/tools/media_items.py`
- **MIDI Operations** (15 tools) - `server/tools/midi.py`
- **FX & Processing** (19 tools) - `server/tools/fx.py`
- **Project Management** (22 tools) - `server/tools/project.py` (render_project moved to rendering.py)
- **Transport & Playback** (9 tools) - `server/tools/transport.py`
- **Time Selection & Navigation** (2 tools) - `server/tools/time_selection.py`
- **Markers & Regions** (4 tools) - `server/tools/markers.py`
- **Automation & Envelopes** (6 tools) - `server/tools/automation.py`
- **Rendering & Freezing** (4 tools) - `server/tools/rendering.py`
- **GUI & Interface** (4 tools) - `server/tools/gui.py`

### Infrastructure
- Modern server is now the main `server/app.py`
- Legacy servers archived to `legacy_archive/` folder
- Updated `tests/conftest.py` to use modern server exclusively
- All tool modules properly organized by category
- Integration tests passing with new implementation

**Total Migrated**: 193 tools (0 placeholder tools remaining)

## Key Technical Details

### Modern Pattern Structure
```python
from ..bridge import bridge

async def tool_name(param1: type, param2: type = default) -> str:
    """Tool description"""
    result = await bridge.call_lua("LuaFunctionName", [param1, param2])
    
    if result.get("ok"):
        return f"Success message: {result.get('ret')}"
    else:
        raise Exception(f"Error message: {result.get('error', 'Unknown error')}")

def register_category_tools(mcp) -> int:
    """Register all tools in this category"""
    tools = [
        (tool_name, "Tool description"),
        # ... more tools
    ]
    
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)
```

### Testing
```bash
# Run tests (always uses modern server now)
pytest tests/test_integration.py -v

# Run specific test
source venv/bin/activate && pytest tests/test_integration.py::test_insert_track -v
```

### Important Notes
1. **Import paths**: Use relative imports (e.g., `from ..bridge import bridge`)
2. **Error handling**: Modern pattern uses exceptions instead of returning error TextContent
3. **Type hints**: All functions should have proper type annotations
4. **Async/await**: All tool functions must be async
5. **Return types**: Always return strings (will be wrapped in TextContent automatically)
6. **Output differences**: Some tests may fail due to minor wording differences (e.g., "not muted" vs "unmuted")

### Migration Process
1. Find tools in `server/app_file_bridge_full.py` by searching for `elif tool_name ==`
2. Extract the tool implementation
3. Convert to async function with type hints
4. Replace error returns with exceptions
5. Add to appropriate module with registration function
6. Test with `USE_MODERN_SERVER=true`

### File Locations
- Main server: `server/app.py` (formerly app_modern.py)
- Tool modules: `server/tools/*.py`
- Bridge: `server/bridge.py`
- Tests: `tests/test_*.py`
- Legacy implementations: `legacy_archive/` (for historical reference)

### Common Patterns to Convert

**Legacy pattern**:
```python
elif tool_name == "some_tool":
    arg1 = args.get("arg1")
    result = bridge.call_lua("SomeFunction", [arg1])
    if result.get("ok"):
        return [TextContent(text=f"Result: {result.get('ret')}")]
    else:
        return [TextContent(text=f"Error: {result.get('error')}")]
```

**Modern pattern**:
```python
async def some_tool(arg1: str) -> str:
    """Tool description"""
    result = await bridge.call_lua("SomeFunction", [arg1])
    
    if result.get("ok"):
        return f"Result: {result.get('ret')}"
    else:
        raise Exception(f"Error: {result.get('error', 'Unknown error')}")
```

### Next Steps
1. Continue migrating tools category by category
2. Run integration tests after each category
3. Update test expectations for output format differences
4. Consider creating additional test coverage for new tools