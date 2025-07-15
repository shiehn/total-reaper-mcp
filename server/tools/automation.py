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
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
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
    # Get envelope - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
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
    # Get envelope - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
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
    # Get envelope - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
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
    # Get envelope - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
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
    # Get envelope - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
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
# Envelope Extended Operations (12 tools)
# ============================================================================

async def envelope_evaluate(track_index: int, envelope_name: str, time: float) -> str:
    """Evaluate envelope value at a specific time"""
    # Get envelope - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track {track_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Evaluate envelope at time
    result = await bridge.call_lua("Envelope_Evaluate", [envelope_handle, time, 0, 0])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            value = ret[1]
            return f"Envelope '{envelope_name}' value at {time:.3f}s: {value:.3f}"
        else:
            return f"Unable to evaluate envelope at {time:.3f}s"
    else:
        raise Exception(f"Failed to evaluate envelope: {result.get('error', 'Unknown error')}")


async def delete_envelope_point_range(track_index: int, envelope_name: str, 
                                     start_time: float, end_time: float) -> str:
    """Delete all envelope points within a time range"""
    # Get envelope - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track {track_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Delete points in range
    result = await bridge.call_lua("DeleteEnvelopePointRange", [envelope_handle, start_time, end_time])
    
    if result.get("ok"):
        return f"Deleted envelope points between {start_time:.3f}s and {end_time:.3f}s"
    else:
        raise Exception(f"Failed to delete envelope point range: {result.get('error', 'Unknown error')}")


async def envelope_sort_points(track_index: int, envelope_name: str) -> str:
    """Sort envelope points by time"""
    # Get envelope - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track {track_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Sort points
    result = await bridge.call_lua("Envelope_SortPoints", [envelope_handle])
    
    if result.get("ok"):
        return f"Sorted envelope '{envelope_name}' points"
    else:
        raise Exception(f"Failed to sort envelope points: {result.get('error', 'Unknown error')}")


async def get_envelope_name(track_index: int, envelope_index: int) -> str:
    """Get the name of an envelope by index"""
    # Get envelope by index - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_index, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Get envelope name
    result = await bridge.call_lua("GetEnvelopeName", [envelope_handle])
    
    if result.get("ok"):
        name = result.get("ret", "")
        return f"Envelope {envelope_index}: {name}"
    else:
        raise Exception(f"Failed to get envelope name: {result.get('error', 'Unknown error')}")


async def get_envelope_scaling_mode(track_index: int, envelope_name: str) -> str:
    """Get envelope scaling mode"""
    # Get envelope - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track {track_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Get scaling mode
    result = await bridge.call_lua("GetEnvelopeScalingMode", [envelope_handle])
    
    if result.get("ok"):
        mode = result.get("ret", 0)
        mode_names = {0: "Linear", 1: "Fader Scaling"}
        mode_name = mode_names.get(mode, f"Unknown ({mode})")
        return f"Envelope '{envelope_name}' scaling mode: {mode_name}"
    else:
        raise Exception(f"Failed to get envelope scaling mode: {result.get('error', 'Unknown error')}")


async def get_fx_envelope(track_index: int, fx_index: int, param_index: int) -> str:
    """Get parameter envelope for a track FX"""
    # Get FX envelope - pass track index directly
    result = await bridge.call_lua("GetFXEnvelope", [track_index, fx_index, param_index, False])
    
    if result.get("ok"):
        envelope_handle = result.get("ret")
        if envelope_handle:
            # Get envelope name for info
            name_result = await bridge.call_lua("GetEnvelopeName", [envelope_handle])
            env_name = name_result.get("ret", "") if name_result.get("ok") else "Unknown"
            return f"Found FX parameter envelope: {env_name}"
        else:
            return f"No envelope for FX {fx_index} parameter {param_index}"
    else:
        raise Exception(f"Failed to get FX envelope: {result.get('error', 'Unknown error')}")


async def insert_envelope_point_ex(track_index: int, envelope_name: str, time: float, value: float,
                                  shape: int = 0, tension: float = 0.0, selected: bool = False,
                                  no_sort: bool = False) -> str:
    """Insert an automation point with extended parameters"""
    # Get envelope - pass track index directly
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
    
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track {track_index}")
    
    envelope_handle = env_result.get("ret")
    
    # Insert point with extended parameters
    result = await bridge.call_lua("InsertEnvelopePointEx", [
        envelope_handle, -1, time, value, shape, tension, selected, no_sort
    ])
    
    if result.get("ok"):
        return f"Inserted point at {time:.3f}s with value {value:.3f}, shape={shape}, tension={tension:.3f}"
    else:
        raise Exception(f"Failed to insert envelope point: {result.get('error', 'Unknown error')}")


async def get_selected_envelope(project_index: int = 0) -> str:
    """Get the currently selected envelope"""
    result = await bridge.call_lua("GetSelectedEnvelope", [project_index])
    
    if result.get("ok"):
        envelope_handle = result.get("ret")
        if envelope_handle:
            # Get envelope name
            name_result = await bridge.call_lua("GetEnvelopeName", [envelope_handle])
            env_name = name_result.get("ret", "") if name_result.get("ok") else "Unknown"
            return f"Selected envelope: {env_name}"
        else:
            return "No envelope selected"
    else:
        raise Exception(f"Failed to get selected envelope: {result.get('error', 'Unknown error')}")


async def get_track_envelope(track_index: int, envelope_index: int) -> str:
    """Get track envelope by index"""
    # Get envelope by index - pass track index directly
    result = await bridge.call_lua("GetTrackEnvelope", [track_index, envelope_index])
    
    if result.get("ok"):
        envelope_handle = result.get("ret")
        if envelope_handle:
            # Get envelope name
            name_result = await bridge.call_lua("GetEnvelopeName", [envelope_handle])
            env_name = name_result.get("ret", "") if name_result.get("ok") else "Unknown"
            return f"Track {track_index} envelope {envelope_index}: {env_name}"
        else:
            return f"No envelope at index {envelope_index} on track {track_index}"
    else:
        raise Exception(f"Failed to get track envelope: {result.get('error', 'Unknown error')}")


async def count_track_envelopes(track_index: int) -> str:
    """Count the number of envelopes on a track"""
    # Count envelopes - pass track index directly
    result = await bridge.call_lua("CountTrackEnvelopes", [track_index])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Track {track_index} has {count} envelopes"
    else:
        raise Exception(f"Failed to count track envelopes: {result.get('error', 'Unknown error')}")


async def get_track_automation_mode(track_index: int) -> str:
    """Get the automation mode for a track"""
    # Get automation mode - pass track index, not handle
    result = await bridge.call_lua("GetTrackAutomationMode", [track_index])
    
    if result.get("ok"):
        mode = result.get("ret", -1)
        mode_names = {
            -1: "Global",
            0: "Trim/Read",
            1: "Read",
            2: "Touch",
            3: "Write",
            4: "Latch"
        }
        mode_name = mode_names.get(mode, f"Unknown ({mode})")
        return f"Track {track_index} automation mode: {mode_name}"
    else:
        raise Exception(f"Failed to get track automation mode: {result.get('error', 'Unknown error')}")


async def set_track_automation_mode(track_index: int, mode: int) -> str:
    """Set the automation mode for a track"""
    # Validate mode
    mode_names = {
        -1: "Global",
        0: "Trim/Read",
        1: "Read",
        2: "Touch",
        3: "Write",
        4: "Latch"
    }
    
    if mode not in mode_names:
        raise Exception(f"Invalid automation mode: {mode}. Valid modes: {list(mode_names.keys())}")
    
    # Set automation mode - pass track index, not handle
    result = await bridge.call_lua("SetTrackAutomationMode", [track_index, mode])
    
    if result.get("ok"):
        return f"Set track {track_index} automation mode to: {mode_names[mode]}"
    else:
        raise Exception(f"Failed to set track automation mode: {result.get('error', 'Unknown error')}")


async def get_global_automation_override() -> str:
    """Get the global automation override state"""
    result = await bridge.call_lua("GetGlobalAutomationOverride", [])
    
    if result.get("ok"):
        mode = result.get("ret", -1)
        mode_names = {
            -1: "No override",
            0: "No override",
            1: "Bypass all automation",
            2: "Write current values for all writing tracks",
            3: "Write current values for all tracks",
            4: "All tracks set to touch mode",
            5: "All tracks set to read mode",
            6: "All tracks set to latch mode"
        }
        mode_name = mode_names.get(mode, f"Unknown ({mode})")
        return f"Global automation override: {mode_name}"
    else:
        raise Exception(f"Failed to get global automation override: {result.get('error', 'Unknown error')}")


async def set_global_automation_override(mode: int) -> str:
    """Set the global automation override state"""
    # Validate mode
    mode_names = {
        -1: "No override",
        0: "No override", 
        1: "Bypass all automation",
        2: "Write current values for all writing tracks",
        3: "Write current values for all tracks",
        4: "All tracks set to touch mode",
        5: "All tracks set to read mode",
        6: "All tracks set to latch mode"
    }
    
    if mode not in mode_names:
        raise Exception(f"Invalid automation override mode: {mode}. Valid modes: {list(mode_names.keys())}")
    
    # Set global automation override
    result = await bridge.call_lua("SetGlobalAutomationOverride", [mode])
    
    if result.get("ok"):
        return f"Set global automation override to: {mode_names[mode]}"
    else:
        raise Exception(f"Failed to set global automation override: {result.get('error', 'Unknown error')}")


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
        
        # Envelope Extended Operations
        (envelope_evaluate, "Evaluate envelope value at a specific time"),
        (delete_envelope_point_range, "Delete all envelope points within a time range"),
        (envelope_sort_points, "Sort envelope points by time"),
        (get_envelope_name, "Get the name of an envelope by index"),
        (get_envelope_scaling_mode, "Get envelope scaling mode"),
        (get_fx_envelope, "Get parameter envelope for a track FX"),
        (insert_envelope_point_ex, "Insert an automation point with extended parameters"),
        (get_selected_envelope, "Get the currently selected envelope"),
        (get_track_envelope, "Get track envelope by index"),
        (count_track_envelopes, "Count the number of envelopes on a track"),
        (get_track_automation_mode, "Get the automation mode for a track"),
        (set_track_automation_mode, "Set the automation mode for a track"),
        (get_global_automation_override, "Get the global automation override state"),
        (set_global_automation_override, "Set the global automation override state"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)