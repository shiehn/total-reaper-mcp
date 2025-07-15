"""
FX & Processing Tools for REAPER MCP

This module contains tools for managing effects and processing.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# Track FX Management (6 tools)
# ============================================================================

async def track_fx_get_count(track_index: int) -> str:
    """Get the number of FX on a track"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_GetCount", [track_index])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Track {track_index} has {count} FX"
    else:
        raise Exception(f"Failed to get FX count: {result.get('error', 'Unknown error')}")


async def track_fx_add_by_name(track_index: int, fx_name: str, instantiate: bool = True) -> str:
    """Add an FX to a track by name"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_AddByName", [track_index, fx_name, False, -1 if instantiate else -1000])
    
    if result.get("ok"):
        fx_index = result.get("ret", -1)
        if fx_index >= 0:
            return f"Added {fx_name} to track {track_index} at FX index {fx_index}"
        else:
            return f"Failed to add {fx_name} to track {track_index}"
    else:
        raise Exception(f"Failed to add FX: {result.get('error', 'Unknown error')}")


async def track_fx_delete(track_index: int, fx_index: int) -> str:
    """Delete an FX from a track"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_Delete", [track_index, fx_index])
    
    if result.get("ok"):
        return f"Deleted FX at index {fx_index} from track {track_index}"
    else:
        raise Exception(f"Failed to delete FX: {result.get('error', 'Unknown error')}")


async def track_fx_get_enabled(track_index: int, fx_index: int) -> str:
    """Get whether an FX is enabled"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_GetEnabled", [track_index, fx_index])
    
    if result.get("ok"):
        enabled = bool(result.get("ret", False))
        return f"FX {fx_index} on track {track_index} is {'enabled' if enabled else 'disabled'}"
    else:
        raise Exception(f"Failed to get FX enabled state: {result.get('error', 'Unknown error')}")


async def track_fx_set_enabled(track_index: int, fx_index: int, enabled: bool) -> str:
    """Enable or disable an FX"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_SetEnabled", [track_index, fx_index, enabled])
    
    if result.get("ok"):
        return f"FX {fx_index} on track {track_index} {'enabled' if enabled else 'disabled'}"
    else:
        raise Exception(f"Failed to set FX enabled state: {result.get('error', 'Unknown error')}")


async def track_fx_get_name(track_index: int, fx_index: int) -> str:
    """Get the name of an FX"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_GetFXName", [track_index, fx_index, "", 256])
    
    if result.get("ok"):
        # The API returns the name
        fx_name = result.get("ret", "Unknown")
        return f"FX {fx_index} on track {track_index}: {fx_name}"
    else:
        raise Exception(f"Failed to get FX name: {result.get('error', 'Unknown error')}")


# ============================================================================
# FX Parameter Management (would be added in full implementation)
# ============================================================================

# Note: The full implementation would include:
# - TrackFX_GetParam
# - TrackFX_SetParam
# - TrackFX_GetParamName
# - TrackFX_GetNumParams
# - TrackFX_GetPreset
# - TrackFX_SetPreset
# - TrackFX_GetPresetIndex
# - TrackFX_NavigatePresets
# - TrackFX_GetOpen
# - TrackFX_SetOpen
# - TrackFX_Show
# - TrackFX_GetChainVisible
# - etc.

# For now, we'll include placeholder functions for these

async def track_fx_get_param_count(track_index: int, fx_index: int) -> str:
    """Get the number of parameters for an FX"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_GetNumParams", [track_index, fx_index])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"FX {fx_index} has {count} parameters"
    else:
        raise Exception(f"Failed to get parameter count: {result.get('error', 'Unknown error')}")


async def track_fx_get_param(track_index: int, fx_index: int, param_index: int) -> str:
    """Get an FX parameter value"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_GetParam", [track_index, fx_index, param_index])
    
    if result.get("ok"):
        # Result contains: value, min, max
        value = result.get("value", 0.0)
        min_val = result.get("min", 0.0)
        max_val = result.get("max", 1.0)
        return f"Parameter {param_index}: {value:.3f} (range: {min_val:.3f} to {max_val:.3f})"
    else:
        raise Exception(f"Failed to get parameter: {result.get('error', 'Unknown error')}")


async def track_fx_set_param(track_index: int, fx_index: int, param_index: int, value: float) -> str:
    """Set an FX parameter value"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_SetParam", [track_index, fx_index, param_index, value])
    
    if result.get("ok"):
        return f"Set parameter {param_index} to {value:.3f}"
    else:
        raise Exception(f"Failed to set parameter: {result.get('error', 'Unknown error')}")


async def track_fx_get_param_name(track_index: int, fx_index: int, param_index: int) -> str:
    """Get the name of an FX parameter"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_GetParamName", [track_index, fx_index, param_index, "", 256])
    
    if result.get("ok"):
        param_name = result.get("ret", "Unknown")
        return f"Parameter {param_index}: {param_name}"
    else:
        raise Exception(f"Failed to get parameter name: {result.get('error', 'Unknown error')}")


async def track_fx_get_preset(track_index: int, fx_index: int) -> str:
    """Get the current preset name of an FX"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_GetPreset", [track_index, fx_index, "", 256])
    
    if result.get("ok"):
        preset_name = result.get("ret", "")
        if preset_name:
            return f"Current preset: {preset_name}"
        else:
            return "No preset selected"
    else:
        raise Exception(f"Failed to get preset: {result.get('error', 'Unknown error')}")


async def track_fx_set_preset(track_index: int, fx_index: int, preset_name: str) -> str:
    """Set the preset of an FX by name"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_SetPreset", [track_index, fx_index, preset_name])
    
    if result.get("ok"):
        return f"Set preset to: {preset_name}"
    else:
        raise Exception(f"Failed to set preset: {result.get('error', 'Unknown error')}")


async def track_fx_show(track_index: int, fx_index: int, show: int) -> str:
    """Show/hide/toggle FX window (show: 0=hide, 1=show, 2=toggle, 3=focus)"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_Show", [track_index, fx_index, show])
    
    if result.get("ok"):
        show_states = {0: "hidden", 1: "shown", 2: "toggled", 3: "focused"}
        return f"FX window {show_states.get(show, 'updated')}"
    else:
        raise Exception(f"Failed to show/hide FX: {result.get('error', 'Unknown error')}")


async def track_fx_get_open(track_index: int, fx_index: int) -> str:
    """Check if FX window is open"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_GetOpen", [track_index, fx_index])
    
    if result.get("ok"):
        is_open = bool(result.get("ret", False))
        return f"FX window is {'open' if is_open else 'closed'}"
    else:
        raise Exception(f"Failed to check FX window state: {result.get('error', 'Unknown error')}")


async def track_fx_set_open(track_index: int, fx_index: int, open: bool) -> str:
    """Open or close FX window"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_SetOpen", [track_index, fx_index, open])
    
    if result.get("ok"):
        return f"FX window {'opened' if open else 'closed'}"
    else:
        raise Exception(f"Failed to set FX window state: {result.get('error', 'Unknown error')}")


async def track_fx_get_chain_visible(track_index: int) -> str:
    """Check if FX chain window is visible"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_GetChainVisible", [track_index])
    
    if result.get("ok"):
        visible = result.get("ret", -1)
        if visible == -1:
            return "FX chain window visibility unknown"
        elif visible == 0:
            return "FX chain window is hidden"
        elif visible == 1:
            return "FX chain window is visible (normal)"
        elif visible == 2:
            return "FX chain window is visible (floating)"
        else:
            return f"FX chain window state: {visible}"
    else:
        raise Exception(f"Failed to check FX chain visibility: {result.get('error', 'Unknown error')}")


async def track_fx_copy_to_track(source_track: int, fx_index: int, dest_track: int, dest_fx_index: int = -1, move: bool = False) -> str:
    """Copy or move FX between tracks"""
    # Pass track indices directly - the bridge will handle getting the tracks
    result = await bridge.call_lua("TrackFX_CopyToTrack", [source_track, fx_index, dest_track, dest_fx_index, move])
    
    if result.get("ok"):
        action = "moved" if move else "copied"
        return f"FX {action} from track {source_track} to track {dest_track}"
    else:
        raise Exception(f"Failed to copy/move FX: {result.get('error', 'Unknown error')}")


async def track_fx_get_offline(track_index: int, fx_index: int) -> str:
    """Check if FX is offline"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_GetOffline", [track_index, fx_index])
    
    if result.get("ok"):
        offline = bool(result.get("ret", False))
        return f"FX is {'offline' if offline else 'online'}"
    else:
        raise Exception(f"Failed to check FX offline state: {result.get('error', 'Unknown error')}")


async def track_fx_set_offline(track_index: int, fx_index: int, offline: bool) -> str:
    """Set FX offline state"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("TrackFX_SetOffline", [track_index, fx_index, offline])
    
    if result.get("ok"):
        return f"FX set to {'offline' if offline else 'online'}"
    else:
        raise Exception(f"Failed to set FX offline state: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_fx_tools(mcp) -> int:
    """Register all FX and processing tools with the MCP instance"""
    tools = [
        # Basic FX Management
        (track_fx_get_count, "Get the number of FX on a track"),
        (track_fx_add_by_name, "Add an FX to a track by name"),
        (track_fx_delete, "Delete an FX from a track"),
        (track_fx_get_enabled, "Get whether an FX is enabled"),
        (track_fx_set_enabled, "Enable or disable an FX"),
        (track_fx_get_name, "Get the name of an FX"),
        
        # FX Parameters
        (track_fx_get_param_count, "Get the number of parameters for an FX"),
        (track_fx_get_param, "Get an FX parameter value"),
        (track_fx_set_param, "Set an FX parameter value"),
        (track_fx_get_param_name, "Get the name of an FX parameter"),
        
        # FX Presets
        (track_fx_get_preset, "Get the current preset name of an FX"),
        (track_fx_set_preset, "Set the preset of an FX by name"),
        
        # FX UI
        (track_fx_show, "Show/hide/toggle FX window"),
        (track_fx_get_open, "Check if FX window is open"),
        (track_fx_set_open, "Open or close FX window"),
        (track_fx_get_chain_visible, "Check if FX chain window is visible"),
        
        # FX Operations
        (track_fx_copy_to_track, "Copy or move FX between tracks"),
        (track_fx_get_offline, "Check if FX is offline"),
        (track_fx_set_offline, "Set FX offline state"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)