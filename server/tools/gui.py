"""
GUI & Interface Tools for REAPER MCP

This module contains tools for GUI and interface operations.
"""

from ..bridge import bridge


# Placeholder - to be implemented
async def placeholder_gui_tool() -> str:
    """Placeholder for GUI tools"""
    return "GUI tools not yet implemented"


# ============================================================================
# Registration Function
# ============================================================================

def register_gui_tools(mcp) -> int:
    """Register all GUI and interface tools with the MCP instance"""
    # TODO: Implement all GUI tools
    tools = [
        (placeholder_gui_tool, "Placeholder for GUI tools"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)