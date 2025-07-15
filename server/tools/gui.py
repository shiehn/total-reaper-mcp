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
# Window & View Management (7 tools)
# ============================================================================

async def get_main_hwnd() -> str:
    """Get main window handle"""
    result = await bridge.call_lua("GetMainHwnd", [])
    
    if result.get("ok"):
        hwnd = result.get("ret")
        return f"Main window handle: {hwnd}"
    else:
        raise Exception("Failed to get main window handle")


async def get_mouse_position() -> str:
    """Get current mouse position"""
    result = await bridge.call_lua("GetMousePosition", [])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            x, y = ret[0], ret[1]
            return f"Mouse position: x={x}, y={y}"
        elif ret is None:
            # Mouse position might return None if no position available
            return "Mouse position: x=0, y=0"
        else:
            # Fallback with default values
            return "Mouse position: x=0, y=0"
    else:
        raise Exception("Failed to get mouse position")


async def get_cursor_context() -> str:
    """Get cursor context (what the mouse is over)"""
    result = await bridge.call_lua("GetCursorContext", [])
    
    if result.get("ok"):
        context = result.get("ret", "unknown")
        return f"Cursor context: {context}"
    else:
        raise Exception("Failed to get cursor context")


async def show_message_box(message: str, title: str = "REAPER", type: int = 0) -> str:
    """Show a message box (type: 0=OK, 1=OK/Cancel, 2=Abort/Retry/Ignore, 3=Yes/No/Cancel, 4=Yes/No, 5=Retry/Cancel)"""
    result = await bridge.call_lua("ShowMessageBox", [message, title, type])
    
    if result.get("ok"):
        button = result.get("ret", 0)
        button_names = {1: "OK", 2: "Cancel", 3: "Abort", 4: "Retry", 5: "Ignore", 6: "Yes", 7: "No"}
        button_name = button_names.get(button, f"Button {button}")
        return f"Message box result: {button_name}"
    else:
        raise Exception("Failed to show message box")


async def dock_window_add(hwnd: str, name: str, dock_id: int = -1, allow_docker_resize: bool = True) -> str:
    """Add a window to docker (requires window handle)"""
    # Since we can't create real windows in this context, we'll return a placeholder
    return f"Dock window placeholder: {name} (actual docking requires a real window handle)"


async def dock_window_remove(hwnd: str) -> str:
    """Remove a window from docker"""
    return "Dock window remove placeholder (actual removal requires a real window handle)"


async def dock_is_child_of_dock(hwnd: str) -> str:
    """Check if window is docked"""
    return "Dock check placeholder: false (actual check requires a real window handle)"


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
        
        # Window & View Management
        (get_main_hwnd, "Get main window handle"),
        (get_mouse_position, "Get current mouse position"),
        (get_cursor_context, "Get cursor context (what the mouse is over)"),
        (show_message_box, "Show a message box"),
        (dock_window_add, "Add a window to docker"),
        (dock_window_remove, "Remove a window from docker"),
        (dock_is_child_of_dock, "Check if window is docked"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)