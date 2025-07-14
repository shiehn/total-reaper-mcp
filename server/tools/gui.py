"""
GUI & Interface Tools for REAPER MCP

This module contains tools for GUI and interface operations.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# Display Update Operations (2 tools)
# ============================================================================

async def update_arrange() -> str:
    """Update the arrange view"""
    result = await bridge.call_lua("UpdateArrange", [])
    
    if result.get("ok"):
        return "Updated arrange view"
    else:
        raise Exception(f"Failed to update arrange: {result.get('error', 'Unknown error')}")


async def update_timeline() -> str:
    """Update the timeline display"""
    result = await bridge.call_lua("UpdateTimeline", [])
    
    if result.get("ok"):
        return "Updated timeline"
    else:
        raise Exception(f"Failed to update timeline: {result.get('error', 'Unknown error')}")


# ============================================================================
# Console Operations (2 tools)
# ============================================================================

async def show_console_msg(message: str) -> str:
    """Show message in console"""
    result = await bridge.call_lua("ShowConsoleMsg", [message])
    
    if result.get("ok"):
        return f"Showed message: {message}"
    else:
        raise Exception("Failed to show console message")


async def clear_console() -> str:
    """Clear the console"""
    result = await bridge.call_lua("ClearConsole", [])
    
    if result.get("ok"):
        return "Cleared console"
    else:
        raise Exception("Failed to clear console")


# ============================================================================
# Window & View Management (planned for future expansion)
# ============================================================================

# Future functions could include:
# - get_main_hwnd() - Get main window handle
# - dock_window() - Dock a window
# - show_action_list() - Show action list window
# - show_fx_browser() - Show FX browser
# - show_media_explorer() - Show media explorer
# - show_mixer() - Show mixer window
# - toggle_fullscreen() - Toggle fullscreen mode
# - set_track_height() - Set track height in TCP
# - zoom_in_horizontal() - Zoom in horizontally
# - zoom_out_horizontal() - Zoom out horizontally
# - zoom_in_vertical() - Zoom in vertically
# - zoom_out_vertical() - Zoom out vertically
# - scroll_to_track() - Scroll view to track
# - center_on_cursor() - Center view on edit cursor
# - fit_items_to_window() - Fit selected items to window
# - fit_project_to_window() - Fit entire project to window


# ============================================================================
# Registration Function
# ============================================================================

def register_gui_tools(mcp) -> int:
    """Register all GUI and interface tools with the MCP instance"""
    tools = [
        # Display Update Operations
        (update_arrange, "Update the arrange view"),
        (update_timeline, "Update the timeline display"),
        
        # Console Operations
        (show_console_msg, "Show message in console"),
        (clear_console, "Clear the console"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)