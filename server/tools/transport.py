"""
Transport & Playback Tools for REAPER MCP

This module contains tools for transport control and playback.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# Basic Transport Control (6 tools)
# ============================================================================

async def play() -> str:
    """Start playback"""
    result = await bridge.call_lua("Main_OnCommand", [1007, 0])  # Transport: Play
    
    if result.get("ok"):
        return "Started playback"
    else:
        raise Exception(f"Failed to start playback: {result.get('error', 'Unknown error')}")


async def stop() -> str:
    """Stop playback"""
    result = await bridge.call_lua("Main_OnCommand", [1016, 0])  # Transport: Stop
    
    if result.get("ok"):
        return "Stopped playback"
    else:
        raise Exception(f"Failed to stop playback: {result.get('error', 'Unknown error')}")


async def pause() -> str:
    """Pause playback"""
    result = await bridge.call_lua("Main_OnCommand", [1008, 0])  # Transport: Pause
    
    if result.get("ok"):
        return "Paused playback"
    else:
        raise Exception(f"Failed to pause playback: {result.get('error', 'Unknown error')}")


async def record() -> str:
    """Start recording"""
    result = await bridge.call_lua("Main_OnCommand", [1013, 0])  # Transport: Record
    
    if result.get("ok"):
        return "Started recording"
    else:
        raise Exception(f"Failed to start recording: {result.get('error', 'Unknown error')}")


async def get_play_state() -> str:
    """Get current playback state"""
    result = await bridge.call_lua("GetPlayState", [])
    
    if result.get("ok"):
        state = int(result.get("ret", 0))
        state_text = {
            0: "stopped",
            1: "playing",
            2: "paused",
            4: "recording",
            5: "record paused"
        }.get(state, f"unknown ({state})")
        
        return f"playback state: {state}"
    else:
        raise Exception(f"Failed to get play state: {result.get('error', 'Unknown error')}")


async def set_play_state(play: bool, pause: bool, record: bool) -> str:
    """Set the transport play state (play, pause, record)"""
    result = await bridge.call_lua("SetPlayState", [play, pause, record])
    
    if result.get("ok"):
        states = []
        if play: states.append("play")
        if pause: states.append("pause") 
        if record: states.append("record")
        state_str = ", ".join(states) if states else "stopped"
        
        return f"Set play state: {state_str}"
    else:
        raise Exception(f"Failed to set play state: {result.get('error', 'Unknown error')}")


# ============================================================================
# Cursor & Position Control (2 tools)
# ============================================================================

async def get_cursor_position() -> str:
    """Get the edit cursor position in seconds"""
    result = await bridge.call_lua("GetCursorPosition", [])
    
    if result.get("ok"):
        position = result.get("ret", 0.0)
        return f"Edit cursor position: {position:.3f} seconds"
    else:
        raise Exception(f"Failed to get cursor position: {result.get('error', 'Unknown error')}")


async def set_edit_cursor_position(time: float, move_view: bool = True, seek_play: bool = False) -> str:
    """Set the edit cursor position"""
    result = await bridge.call_lua("SetEditCurPos", [time, move_view, seek_play])
    
    if result.get("ok"):
        return f"Set cursor position to {time:.3f} seconds"
    else:
        raise Exception(f"Failed to set cursor position: {result.get('error', 'Unknown error')}")


# ============================================================================
# Loop & Repeat Control (1 tool)
# ============================================================================

async def set_repeat_state(repeat: bool) -> str:
    """Set the repeat/loop state"""
    result = await bridge.call_lua("GetSetRepeat", [1 if repeat else 0])
    
    if result.get("ok"):
        state = "enabled" if repeat else "disabled"
        return f"Repeat {state}"
    else:
        raise Exception(f"Failed to set repeat state: {result.get('error', 'Unknown error')}")


# ============================================================================
# Navigation (planned for future expansion)
# ============================================================================

# Future functions could include:
# - go_to_start() - Go to project start
# - go_to_end() - Go to project end  
# - rewind() - Rewind by measure/beat
# - forward() - Forward by measure/beat
# - go_to_marker() - Navigate to specific marker
# - go_to_time() - Go to specific time
# - get_play_position() - Get current play position
# - set_loop_points() - Set loop start/end
# - get_loop_points() - Get loop start/end


# ============================================================================
# Registration Function
# ============================================================================

def register_transport_tools(mcp) -> int:
    """Register all transport and playback tools with the MCP instance"""
    tools = [
        # Basic Transport Control
        (play, "Start playback"),
        (stop, "Stop playback"),
        (pause, "Pause playback"),
        (record, "Start recording"),
        (get_play_state, "Get current playback state"),
        (set_play_state, "Set the transport play state (play, pause, record)"),
        
        # Cursor & Position Control
        (get_cursor_position, "Get the edit cursor position in seconds"),
        (set_edit_cursor_position, "Set the edit cursor position"),
        
        # Loop & Repeat Control
        (set_repeat_state, "Set the repeat/loop state"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)