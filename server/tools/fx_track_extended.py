"""
Track FX Extended Tools for REAPER MCP

This module contains advanced track FX operations including preset management,
parameter extended operations, and FX chain manipulation.
"""

from typing import Optional, Tuple, List
from ..bridge import bridge


# ============================================================================
# Track FX Extended Management (12 tools)
# ============================================================================

async def track_fx_get_num_params(track_index: int, fx_index: int) -> str:
    """Get the number of parameters for a track FX"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get parameter count
    result = await bridge.call_lua("TrackFX_GetNumParams", [track_handle, fx_index])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"FX {fx_index} has {count} parameters"
    else:
        raise Exception(f"Failed to get track FX parameter count: {result.get('error', 'Unknown error')}")


async def track_fx_get_param_name(track_index: int, fx_index: int, param_index: int) -> str:
    """Get the name of a track FX parameter"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get parameter name
    result = await bridge.call_lua("TrackFX_GetParamName", [track_handle, fx_index, param_index, ""])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, param_name = ret[:2]
            if retval:
                return f"Parameter {param_index}: {param_name}"
        return f"Failed to get name for parameter {param_index}"
    else:
        raise Exception(f"Failed to get track FX parameter name: {result.get('error', 'Unknown error')}")


async def track_fx_get_param_normalized(track_index: int, fx_index: int, param_index: int) -> str:
    """Get normalized track FX parameter value (0-1)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get normalized parameter value
    result = await bridge.call_lua("TrackFX_GetParamNormalized", [track_handle, fx_index, param_index])
    
    if result.get("ok"):
        value = result.get("ret", 0.0)
        return f"Parameter {param_index} normalized value: {value:.3f}"
    else:
        raise Exception(f"Failed to get track FX normalized parameter: {result.get('error', 'Unknown error')}")


async def track_fx_set_param_normalized(track_index: int, fx_index: int, param_index: int, value: float) -> str:
    """Set normalized track FX parameter value (0-1)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Clamp value to 0-1 range
    value = max(0.0, min(1.0, value))
    
    # Set normalized parameter value
    result = await bridge.call_lua("TrackFX_SetParamNormalized", [track_handle, fx_index, param_index, value])
    
    if result.get("ok"):
        return f"Set parameter {param_index} normalized value to {value:.3f}"
    else:
        raise Exception(f"Failed to set track FX normalized parameter: {result.get('error', 'Unknown error')}")


async def track_fx_get_preset(track_index: int, fx_index: int) -> str:
    """Get the current preset name of a track FX"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get preset
    result = await bridge.call_lua("TrackFX_GetPreset", [track_handle, fx_index, ""])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, preset_name = ret[:2]
            if retval:
                return f"FX {fx_index} preset: {preset_name}"
        return f"FX {fx_index} has no preset or default preset"
    else:
        raise Exception(f"Failed to get track FX preset: {result.get('error', 'Unknown error')}")


async def track_fx_set_preset(track_index: int, fx_index: int, preset_name: str) -> str:
    """Set the preset of a track FX by name"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set preset
    result = await bridge.call_lua("TrackFX_SetPreset", [track_handle, fx_index, preset_name])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set FX {fx_index} preset to '{preset_name}'"
        else:
            return f"Failed to set preset '{preset_name}' (preset may not exist)"
    else:
        raise Exception(f"Failed to set track FX preset: {result.get('error', 'Unknown error')}")


async def track_fx_get_preset_index(track_index: int, fx_index: int) -> str:
    """Get the current preset index of a track FX"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get preset index and count
    result = await bridge.call_lua("TrackFX_GetPresetIndex", [track_handle, fx_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            preset_idx, num_presets = ret[:2]
            return f"FX {fx_index}: preset {preset_idx} of {num_presets} presets"
        else:
            return f"Failed to get preset index for FX {fx_index}"
    else:
        raise Exception(f"Failed to get track FX preset index: {result.get('error', 'Unknown error')}")


async def track_fx_set_preset_by_index(track_index: int, fx_index: int, preset_index: int) -> str:
    """Set the preset of a track FX by index"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set preset by index
    result = await bridge.call_lua("TrackFX_SetPresetByIndex", [track_handle, fx_index, preset_index])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set FX {fx_index} to preset index {preset_index}"
        else:
            return f"Failed to set preset index {preset_index}"
    else:
        raise Exception(f"Failed to set track FX preset by index: {result.get('error', 'Unknown error')}")


async def track_fx_navigate_presets(track_index: int, fx_index: int, direction: int) -> str:
    """Navigate track FX presets (-1 for previous, 1 for next)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Navigate presets
    result = await bridge.call_lua("TrackFX_NavigatePresets", [track_handle, fx_index, direction])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            nav_str = "next" if direction > 0 else "previous"
            return f"Navigated to {nav_str} preset for FX {fx_index}"
        else:
            return f"No more presets in that direction"
    else:
        raise Exception(f"Failed to navigate track FX presets: {result.get('error', 'Unknown error')}")


async def track_fx_copy_to_track(src_track_index: int, src_fx_index: int, 
                                dst_track_index: int, dst_fx_index: int, move: bool = False) -> str:
    """Copy a track FX to another track"""
    # Get source track
    src_track_result = await bridge.call_lua("GetTrack", [0, src_track_index])
    if not src_track_result.get("ok") or not src_track_result.get("ret"):
        raise Exception(f"Failed to find source track at index {src_track_index}")
    
    src_track_handle = src_track_result.get("ret")
    
    # Get destination track
    dst_track_result = await bridge.call_lua("GetTrack", [0, dst_track_index])
    if not dst_track_result.get("ok") or not dst_track_result.get("ret"):
        raise Exception(f"Failed to find destination track at index {dst_track_index}")
    
    dst_track_handle = dst_track_result.get("ret")
    
    # Copy FX
    result = await bridge.call_lua("TrackFX_CopyToTrack", [
        src_track_handle, src_fx_index, dst_track_handle, dst_fx_index, move
    ])
    
    if result.get("ok"):
        action = "Moved" if move else "Copied"
        return f"{action} FX {src_fx_index} from track {src_track_index} to track {dst_track_index} at position {dst_fx_index}"
    else:
        raise Exception(f"Failed to copy track FX: {result.get('error', 'Unknown error')}")


async def track_fx_copy_to_take(track_index: int, fx_index: int, 
                               item_index: int, take_index: int, take_fx_index: int, move: bool = False) -> str:
    """Copy a track FX to a take"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Copy FX
    result = await bridge.call_lua("TrackFX_CopyToTake", [
        track_handle, fx_index, take_handle, take_fx_index, move
    ])
    
    if result.get("ok"):
        action = "Moved" if move else "Copied"
        return f"{action} track FX {fx_index} to take {take_index} at position {take_fx_index}"
    else:
        raise Exception(f"Failed to copy track FX to take: {result.get('error', 'Unknown error')}")


async def track_fx_get_chain_visible(track_index: int) -> str:
    """Get track FX chain visibility state"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get chain visibility
    result = await bridge.call_lua("TrackFX_GetChainVisible", [track_handle])
    
    if result.get("ok"):
        visible = result.get("ret", 0)
        if visible == -1:
            return "FX chain window is closed"
        elif visible == 0:
            return "FX chain window is open but not focused"
        elif visible == 1:
            return "FX chain window is open and focused"
        elif visible == 2:
            return "FX chain window is open in master track"
        else:
            return f"FX chain visibility state: {visible}"
    else:
        raise Exception(f"Failed to get track FX chain visibility: {result.get('error', 'Unknown error')}")


# ============================================================================
# Track FX Advanced Operations (12 tools)
# ============================================================================

async def track_fx_show(track_index: int, fx_index: int, show_flag: int = 3) -> str:
    """Show/hide track FX window (0=hide, 1=show chain, 2=show floating, 3=show)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Show/hide FX
    result = await bridge.call_lua("TrackFX_Show", [track_handle, fx_index, show_flag])
    
    if result.get("ok"):
        if show_flag == 0:
            return f"Hid FX {fx_index} window"
        elif show_flag == 1:
            return f"Showed FX {fx_index} in chain window"
        elif show_flag == 2:
            return f"Showed FX {fx_index} in floating window"
        else:
            return f"Showed FX {fx_index} window"
    else:
        raise Exception(f"Failed to show/hide track FX: {result.get('error', 'Unknown error')}")


async def track_fx_get_open(track_index: int, fx_index: int) -> str:
    """Get whether track FX window is open"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get open state
    result = await bridge.call_lua("TrackFX_GetOpen", [track_handle, fx_index])
    
    if result.get("ok"):
        is_open = result.get("ret", False)
        return f"FX {fx_index} window is {'open' if is_open else 'closed'}"
    else:
        raise Exception(f"Failed to get track FX open state: {result.get('error', 'Unknown error')}")


async def track_fx_set_open(track_index: int, fx_index: int, open: bool) -> str:
    """Set track FX window open state"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set open state
    result = await bridge.call_lua("TrackFX_SetOpen", [track_handle, fx_index, open])
    
    if result.get("ok"):
        return f"{'Opened' if open else 'Closed'} FX {fx_index} window"
    else:
        raise Exception(f"Failed to set track FX open state: {result.get('error', 'Unknown error')}")


async def track_fx_get_offline(track_index: int, fx_index: int) -> str:
    """Get track FX offline state"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get offline state
    result = await bridge.call_lua("TrackFX_GetOffline", [track_handle, fx_index])
    
    if result.get("ok"):
        is_offline = result.get("ret", False)
        return f"FX {fx_index} is {'offline' if is_offline else 'online'}"
    else:
        raise Exception(f"Failed to get track FX offline state: {result.get('error', 'Unknown error')}")


async def track_fx_set_offline(track_index: int, fx_index: int, offline: bool) -> str:
    """Set track FX offline state"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set offline state
    result = await bridge.call_lua("TrackFX_SetOffline", [track_handle, fx_index, offline])
    
    if result.get("ok"):
        return f"Set FX {fx_index} {'offline' if offline else 'online'}"
    else:
        raise Exception(f"Failed to set track FX offline state: {result.get('error', 'Unknown error')}")


async def track_fx_get_fx_guid(track_index: int, fx_index: int) -> str:
    """Get track FX GUID"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get FX GUID
    result = await bridge.call_lua("TrackFX_GetFXGUID", [track_handle, fx_index])
    
    if result.get("ok"):
        guid = result.get("ret", "")
        if guid:
            return f"FX {fx_index} GUID: {guid}"
        else:
            return f"Failed to get GUID for FX {fx_index}"
    else:
        raise Exception(f"Failed to get track FX GUID: {result.get('error', 'Unknown error')}")


async def track_fx_get_by_name(track_index: int, fx_name: str, instantiate: bool = False) -> str:
    """Get track FX index by name"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get FX by name
    result = await bridge.call_lua("TrackFX_GetByName", [track_handle, fx_name, instantiate])
    
    if result.get("ok"):
        fx_index = result.get("ret", -1)
        if fx_index >= 0:
            return f"Found '{fx_name}' at index {fx_index}"
        else:
            if instantiate:
                return f"Failed to instantiate '{fx_name}'"
            else:
                return f"FX '{fx_name}' not found on track"
    else:
        raise Exception(f"Failed to get track FX by name: {result.get('error', 'Unknown error')}")


async def track_fx_get_io_size(track_index: int, fx_index: int) -> str:
    """Get track FX input/output pin count"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get IO size
    result = await bridge.call_lua("TrackFX_GetIOSize", [track_handle, fx_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            input_pins, output_pins = ret[:2]
            return f"FX {fx_index} has {input_pins} input pins and {output_pins} output pins"
        else:
            return f"Failed to get IO size for FX {fx_index}"
    else:
        raise Exception(f"Failed to get track FX IO size: {result.get('error', 'Unknown error')}")


async def track_fx_format_param_value(track_index: int, fx_index: int, param_index: int, value: float) -> str:
    """Format track FX parameter value for display"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Format parameter value
    result = await bridge.call_lua("TrackFX_FormatParamValue", [track_handle, fx_index, param_index, value, ""])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, formatted_value = ret[:2]
            if retval:
                return f"Parameter {param_index} formatted value: {formatted_value}"
        return f"Failed to format parameter {param_index} value"
    else:
        raise Exception(f"Failed to format track FX parameter value: {result.get('error', 'Unknown error')}")


async def track_fx_format_param_value_normalized(track_index: int, fx_index: int, param_index: int, value: float) -> str:
    """Format normalized track FX parameter value for display"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Format normalized parameter value
    result = await bridge.call_lua("TrackFX_FormatParamValueNormalized", [track_handle, fx_index, param_index, value, ""])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, formatted_value = ret[:2]
            if retval:
                return f"Parameter {param_index} normalized formatted value: {formatted_value}"
        return f"Failed to format normalized parameter {param_index} value"
    else:
        raise Exception(f"Failed to format track FX normalized parameter value: {result.get('error', 'Unknown error')}")


async def track_fx_get_rec_count(track_index: int) -> str:
    """Get the number of FX in the record input chain"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get record FX count
    result = await bridge.call_lua("TrackFX_GetRecCount", [track_handle])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Track has {count} record input FX"
    else:
        raise Exception(f"Failed to get track record FX count: {result.get('error', 'Unknown error')}")


async def track_fx_get_rec_chain_visible(track_index: int) -> str:
    """Get record FX chain visibility state"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get record chain visibility
    result = await bridge.call_lua("TrackFX_GetRecChainVisible", [track_handle])
    
    if result.get("ok"):
        visible = result.get("ret", 0)
        if visible == -1:
            return "Record FX chain window is closed"
        elif visible == 0:
            return "Record FX chain window is open but not focused"
        elif visible == 1:
            return "Record FX chain window is open and focused"
        else:
            return f"Record FX chain visibility state: {visible}"
    else:
        raise Exception(f"Failed to get track record FX chain visibility: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_fx_track_extended_tools(mcp) -> int:
    """Register all track FX extended tools with the MCP instance"""
    tools = [
        # Track FX Extended Management
        (track_fx_get_num_params, "Get the number of parameters for a track FX"),
        (track_fx_get_param_name, "Get the name of a track FX parameter"),
        (track_fx_get_param_normalized, "Get normalized track FX parameter value (0-1)"),
        (track_fx_set_param_normalized, "Set normalized track FX parameter value (0-1)"),
        (track_fx_get_preset, "Get the current preset name of a track FX"),
        (track_fx_set_preset, "Set the preset of a track FX by name"),
        (track_fx_get_preset_index, "Get the current preset index of a track FX"),
        (track_fx_set_preset_by_index, "Set the preset of a track FX by index"),
        (track_fx_navigate_presets, "Navigate track FX presets (-1 for previous, 1 for next)"),
        (track_fx_copy_to_track, "Copy a track FX to another track"),
        (track_fx_copy_to_take, "Copy a track FX to a take"),
        (track_fx_get_chain_visible, "Get track FX chain visibility state"),
        
        # Track FX Advanced Operations
        (track_fx_show, "Show/hide track FX window"),
        (track_fx_get_open, "Get whether track FX window is open"),
        (track_fx_set_open, "Set track FX window open state"),
        (track_fx_get_offline, "Get track FX offline state"),
        (track_fx_set_offline, "Set track FX offline state"),
        (track_fx_get_fx_guid, "Get track FX GUID"),
        (track_fx_get_by_name, "Get track FX index by name"),
        (track_fx_get_io_size, "Get track FX input/output pin count"),
        (track_fx_format_param_value, "Format track FX parameter value for display"),
        (track_fx_format_param_value_normalized, "Format normalized track FX parameter value for display"),
        (track_fx_get_rec_count, "Get the number of FX in the record input chain"),
        (track_fx_get_rec_chain_visible, "Get record FX chain visibility state"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)