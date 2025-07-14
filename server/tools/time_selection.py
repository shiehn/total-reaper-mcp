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
# Time/Tempo Conversion (4 tools)
# ============================================================================

async def time_map_qn_to_time(qn: float) -> str:
    """Convert quarter note position to time in seconds"""
    result = await bridge.call_lua("TimeMap_QNToTime", [qn])
    
    if result.get("ok"):
        time_seconds = result.get("ret", 0.0)
        return f"Quarter note {qn:.1f} = {time_seconds:.3f} seconds"
    else:
        raise Exception(f"Failed to convert QN to time: {result.get('error', 'Unknown error')}")


async def time_map_time_to_qn(time: float) -> str:
    """Convert time in seconds to quarter note position"""
    result = await bridge.call_lua("TimeMap_timeToQN", [time])
    
    if result.get("ok"):
        qn = result.get("ret", 0.0)
        return f"{time:.3f} seconds = quarter note {qn:.3f}"
    else:
        raise Exception(f"Failed to convert time to QN: {result.get('error', 'Unknown error')}")


async def add_tempo_time_sig_marker(position: float, tempo: float, numerator: int = 4, 
                                   denominator: int = 4, linear_tempo: bool = False) -> str:
    """Add a tempo/time signature marker at a specific position"""
    # Use -1 for measure position to let REAPER calculate it
    result = await bridge.call_lua("AddTempoTimeSigMarker", [
        0, position, tempo, numerator, denominator, linear_tempo
    ])
    
    if result.get("ok"):
        return f"Added tempo marker at {position:.3f}s: {tempo:.2f} BPM, {numerator}/{denominator}"
    else:
        raise Exception(f"Failed to add tempo marker: {result.get('error', 'Unknown error')}")


async def get_tempo_at_time(time_seconds: float) -> str:
    """Get the tempo at a specific time position"""
    result = await bridge.call_lua("TimeMap_GetDividedBpmAtTime", [time_seconds])
    
    if result.get("ok"):
        tempo = result.get("ret", 120.0)
        return f"Tempo at {time_seconds:.3f}s: {tempo:.2f} BPM"
    else:
        raise Exception(f"Failed to get tempo at time: {result.get('error', 'Unknown error')}")


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
        
        # Time/Tempo Conversion
        (time_map_qn_to_time, "Convert quarter note position to time in seconds"),
        (time_map_time_to_qn, "Convert time in seconds to quarter note position"),
        (add_tempo_time_sig_marker, "Add a tempo/time signature marker at a specific position"),
        (get_tempo_at_time, "Get the tempo at a specific time position"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)