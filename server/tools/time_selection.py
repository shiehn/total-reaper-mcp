"""
Time Selection & Navigation Tools for REAPER MCP

This module contains tools for time selection and navigation.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# Time Selection & Loop Management (2 tools)
# ============================================================================

async def get_loop_time_range(is_loop: bool = False) -> str:
    """Get the current time selection or loop range"""
    result = await bridge.call_lua("GetSet_LoopTimeRange", [False, is_loop, 0, 0, False])
    
    if result.get("ok"):
        ret = result.get("ret", [0, 0])
        if isinstance(ret, list) and len(ret) >= 2:
            start = ret[0]
            end = ret[1]
            range_type = "loop" if is_loop else "time selection"
            return f"Current {range_type}: {start:.3f}s to {end:.3f}s (duration: {end - start:.3f}s)"
        else:
            return "No time range selected"
    else:
        raise Exception(f"Failed to get time range: {result.get('error', 'Unknown error')}")


async def set_loop_time_range(is_loop: bool, start: float, end: float, allow_autoseek: bool = False) -> str:
    """Set the time selection or loop range"""
    result = await bridge.call_lua("GetSet_LoopTimeRange", [True, is_loop, start, end, allow_autoseek])
    
    if result.get("ok"):
        range_type = "loop" if is_loop else "time selection"
        return f"Set {range_type}: {start:.3f}s to {end:.3f}s"
    else:
        raise Exception(f"Failed to set time range: {result.get('error', 'Unknown error')}")


# ============================================================================
# View & Navigation (planned for future expansion)
# ============================================================================

# Future functions could include:
# - get_arrange_view() - Get current arrange view bounds
# - set_arrange_view() - Set arrange view to specific time range
# - zoom_to_time_selection() - Zoom to current time selection
# - zoom_to_project() - Zoom to full project
# - scroll_to_position() - Scroll view to position
# - center_view_on_cursor() - Center arrange view on edit cursor
# - next_transient() - Navigate to next transient
# - previous_transient() - Navigate to previous transient
# - go_to_measure() - Navigate to specific measure/bar
# - get_time_at_mouse() - Get time position at mouse cursor


# ============================================================================
# Registration Function
# ============================================================================

def register_time_selection_tools(mcp) -> int:
    """Register all time selection and navigation tools with the MCP instance"""
    tools = [
        # Time Selection & Loop Management
        (get_loop_time_range, "Get the current time selection or loop range"),
        (set_loop_time_range, "Set the time selection or loop range"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)