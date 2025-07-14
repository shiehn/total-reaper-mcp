"""
Automation & Envelopes Tools for REAPER MCP

This module contains tools for automation and envelope management.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# Envelope Management (6 tools)
# ============================================================================

async def get_track_envelope_by_name(track_index: int, envelope_name: str) -> str:
    """Get a track envelope by name (e.g., 'Volume', 'Pan', 'Mute')"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope by name
    result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
    
    if result.get("ok"):
        envelope_handle = result.get("ret")
        if envelope_handle:
            return f"Found envelope '{envelope_name}' on track {track_index}"
        else:
            return f"Envelope '{envelope_name}' not found on track {track_index}"
    else:
        raise Exception(f"Failed to get envelope: {result.get('error', 'Unknown error')}")


async def count_envelope_points(track_index: int, envelope_name: str) -> str:
    """Count the number of points in an envelope"""
    # Get track and envelope
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
    
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track {track_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Count points
    result = await bridge.call_lua("CountEnvelopePoints", [envelope_handle])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Envelope '{envelope_name}' has {count} points"
    else:
        raise Exception(f"Failed to count envelope points: {result.get('error', 'Unknown error')}")


async def insert_envelope_point(track_index: int, envelope_name: str, time: float, value: float,
                               shape: int = 0, selected: bool = False) -> str:
    """Insert an automation point in an envelope"""
    # Get track and envelope
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
    
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track {track_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Insert point
    result = await bridge.call_lua("InsertEnvelopePoint", [
        envelope_handle, time, value, shape, 0, selected, True
    ])
    
    if result.get("ok"):
        return f"Inserted point at {time:.3f}s with value {value:.3f} in '{envelope_name}' envelope"
    else:
        raise Exception(f"Failed to insert envelope point: {result.get('error', 'Unknown error')}")


async def delete_envelope_point(track_index: int, envelope_name: str, point_index: int) -> str:
    """Delete an automation point from an envelope"""
    # Get track and envelope
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
    
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track {track_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Delete point
    result = await bridge.call_lua("DeleteEnvelopePointEx", [envelope_handle, -1, point_index])
    
    if result.get("ok"):
        return f"Deleted point {point_index} from '{envelope_name}' envelope"
    else:
        raise Exception(f"Failed to delete envelope point: {result.get('error', 'Unknown error')}")


async def get_envelope_point(track_index: int, envelope_name: str, point_index: int) -> str:
    """Get information about an envelope point"""
    # Get track and envelope
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
    
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track {track_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Get point info
    result = await bridge.call_lua("GetEnvelopePoint", [envelope_handle, point_index, 0, 0, 0, 0, 0])
    
    if result.get("ok"):
        ret_values = result.get("ret", [])
        if isinstance(ret_values, list) and len(ret_values) >= 6:
            retval, time, value, shape, tension, selected = ret_values[:6]
            if retval:
                return f"Point {point_index}: time={time:.3f}s, value={value:.3f}, shape={shape}, selected={bool(selected)}"
        return f"Point {point_index} not found"
    else:
        raise Exception(f"Failed to get envelope point: {result.get('error', 'Unknown error')}")


async def set_envelope_point_value(track_index: int, envelope_name: str, point_index: int, 
                                  value: float, time: Optional[float] = None) -> str:
    """Set the value of an existing envelope point"""
    # Get track and envelope
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
    
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track {track_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Get current point info
    get_result = await bridge.call_lua("GetEnvelopePoint", [envelope_handle, point_index, 0, 0, 0, 0, 0])
    
    if get_result.get("ok"):
        ret_values = get_result.get("ret", [])
        if isinstance(ret_values, list) and len(ret_values) >= 6:
            retval, current_time, old_value, shape, tension, selected = ret_values[:6]
            if retval:
                # Use new time if provided, otherwise keep existing
                if time is not None:
                    current_time = time
                
                # Set point value
                result = await bridge.call_lua("SetEnvelopePoint", [
                    envelope_handle, point_index, current_time, value, shape, tension, selected, True
                ])
                
                if result.get("ok"):
                    return f"Set point {point_index} value to {value:.3f}"
                else:
                    raise Exception(f"Failed to set envelope point: {result.get('error', 'Unknown error')}")
        
        return f"Point {point_index} not found"
    else:
        raise Exception(f"Failed to get envelope point: {get_result.get('error', 'Unknown error')}")


# ============================================================================
# Automation Modes & Advanced Features (planned for future expansion)
# ============================================================================

# Future functions could include:
# - get_envelope_state_chunk() - Get envelope state as chunk
# - set_envelope_state_chunk() - Set envelope state from chunk
# - get_envelope_scaling_mode() - Get envelope scaling mode
# - set_envelope_scaling_mode() - Set envelope scaling mode
# - get_track_automation_mode() - Get track automation mode
# - set_track_automation_mode() - Set track automation mode
# - arm_track_envelope() - Arm envelope for recording
# - clear_envelope() - Clear all points from envelope
# - copy_envelope_points() - Copy envelope points
# - paste_envelope_points() - Paste envelope points
# - smooth_envelope() - Smooth envelope points
# - thin_envelope() - Thin envelope points


# ============================================================================
# Registration Function
# ============================================================================

def register_automation_tools(mcp) -> int:
    """Register all automation and envelope tools with the MCP instance"""
    tools = [
        # Envelope Management
        (get_track_envelope_by_name, "Get a track envelope by name (e.g., 'Volume', 'Pan', 'Mute')"),
        (count_envelope_points, "Count the number of points in an envelope"),
        (insert_envelope_point, "Insert an automation point in an envelope"),
        (delete_envelope_point, "Delete an automation point from an envelope"),
        (get_envelope_point, "Get information about an envelope point"),
        (set_envelope_point_value, "Set the value of an existing envelope point"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)