"""
Take FX Tools for REAPER MCP

This module contains tools for managing effects on takes.
"""

from typing import Optional, Tuple
from ..bridge import bridge


# ============================================================================
# Take FX Management (12 tools)
# ============================================================================

async def take_fx_get_count(item_index: int, take_index: int) -> str:
    """Get the number of FX on a take"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get FX count
    result = await bridge.call_lua("TakeFX_GetCount", [take_handle])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Take has {count} FX"
    else:
        raise Exception(f"Failed to get take FX count: {result.get('error', 'Unknown error')}")


async def take_fx_add_by_name(item_index: int, take_index: int, fx_name: str, 
                             instantiate: int = 1) -> str:
    """Add an FX to a take by name"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Add FX
    result = await bridge.call_lua("TakeFX_AddByName", [take_handle, fx_name, instantiate])
    
    if result.get("ok"):
        fx_index = result.get("ret", -1)
        if fx_index >= 0:
            return f"Added FX '{fx_name}' at index {fx_index}"
        else:
            return f"Failed to add FX '{fx_name}'"
    else:
        raise Exception(f"Failed to add take FX: {result.get('error', 'Unknown error')}")


async def take_fx_delete(item_index: int, take_index: int, fx_index: int) -> str:
    """Delete an FX from a take"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Delete FX
    result = await bridge.call_lua("TakeFX_Delete", [take_handle, fx_index])
    
    if result.get("ok"):
        return f"Deleted FX at index {fx_index}"
    else:
        raise Exception(f"Failed to delete take FX: {result.get('error', 'Unknown error')}")


async def take_fx_get_enabled(item_index: int, take_index: int, fx_index: int) -> str:
    """Get the enabled state of a take FX"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get enabled state
    result = await bridge.call_lua("TakeFX_GetEnabled", [take_handle, fx_index])
    
    if result.get("ok"):
        enabled = result.get("ret", False)
        return f"FX {fx_index} is {'enabled' if enabled else 'disabled'}"
    else:
        raise Exception(f"Failed to get take FX enabled state: {result.get('error', 'Unknown error')}")


async def take_fx_set_enabled(item_index: int, take_index: int, fx_index: int, enabled: bool) -> str:
    """Set the enabled state of a take FX"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set enabled state
    result = await bridge.call_lua("TakeFX_SetEnabled", [take_handle, fx_index, enabled])
    
    if result.get("ok"):
        return f"{'Enabled' if enabled else 'Disabled'} FX at index {fx_index}"
    else:
        raise Exception(f"Failed to set take FX enabled state: {result.get('error', 'Unknown error')}")


async def take_fx_get_fx_name(item_index: int, take_index: int, fx_index: int) -> str:
    """Get the name of a take FX"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get FX name
    result = await bridge.call_lua("TakeFX_GetFXName", [take_handle, fx_index, ""])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            success, name = ret[:2]
            if success:
                return f"FX {fx_index}: {name}"
        return f"Failed to get name for FX {fx_index}"
    else:
        raise Exception(f"Failed to get take FX name: {result.get('error', 'Unknown error')}")


async def take_fx_get_preset(item_index: int, take_index: int, fx_index: int) -> str:
    """Get the current preset name of a take FX"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get preset
    result = await bridge.call_lua("TakeFX_GetPreset", [take_handle, fx_index, ""])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, preset_name = ret[:2]
            if retval:
                return f"FX {fx_index} preset: {preset_name}"
        return f"FX {fx_index} has no preset or default preset"
    else:
        raise Exception(f"Failed to get take FX preset: {result.get('error', 'Unknown error')}")


async def take_fx_set_preset(item_index: int, take_index: int, fx_index: int, preset_name: str) -> str:
    """Set the preset of a take FX by name"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set preset
    result = await bridge.call_lua("TakeFX_SetPreset", [take_handle, fx_index, preset_name])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set FX {fx_index} preset to '{preset_name}'"
        else:
            return f"Failed to set preset '{preset_name}' (preset may not exist)"
    else:
        raise Exception(f"Failed to set take FX preset: {result.get('error', 'Unknown error')}")


# ============================================================================
# Take FX Parameters (8 tools)
# ============================================================================

async def take_fx_get_num_params(item_index: int, take_index: int, fx_index: int) -> str:
    """Get the number of parameters for a take FX"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get parameter count
    result = await bridge.call_lua("TakeFX_GetNumParams", [take_handle, fx_index])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"FX {fx_index} has {count} parameters"
    else:
        raise Exception(f"Failed to get take FX parameter count: {result.get('error', 'Unknown error')}")


async def take_fx_get_param_name(item_index: int, take_index: int, fx_index: int, param_index: int) -> str:
    """Get the name of a take FX parameter"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get parameter name
    result = await bridge.call_lua("TakeFX_GetParamName", [take_handle, fx_index, param_index, ""])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, param_name = ret[:2]
            if retval:
                return f"Parameter {param_index}: {param_name}"
        return f"Failed to get name for parameter {param_index}"
    else:
        raise Exception(f"Failed to get take FX parameter name: {result.get('error', 'Unknown error')}")


async def take_fx_get_param(item_index: int, take_index: int, fx_index: int, param_index: int) -> str:
    """Get take FX parameter value"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get parameter value
    result = await bridge.call_lua("TakeFX_GetParam", [take_handle, fx_index, param_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            value, min_val, max_val = ret[:3]
            return f"Parameter {param_index}: value={value:.3f}, range=[{min_val:.3f}, {max_val:.3f}]"
        else:
            return f"Failed to get parameter {param_index} value"
    else:
        raise Exception(f"Failed to get take FX parameter: {result.get('error', 'Unknown error')}")


async def take_fx_set_param(item_index: int, take_index: int, fx_index: int, 
                           param_index: int, value: float) -> str:
    """Set take FX parameter value"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set parameter value
    result = await bridge.call_lua("TakeFX_SetParam", [take_handle, fx_index, param_index, value])
    
    if result.get("ok"):
        return f"Set parameter {param_index} to {value:.3f}"
    else:
        raise Exception(f"Failed to set take FX parameter: {result.get('error', 'Unknown error')}")


async def take_fx_get_param_normalized(item_index: int, take_index: int, fx_index: int, 
                                       param_index: int) -> str:
    """Get normalized take FX parameter value (0-1)"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get normalized parameter value
    result = await bridge.call_lua("TakeFX_GetParamNormalized", [take_handle, fx_index, param_index])
    
    if result.get("ok"):
        value = result.get("ret", 0.0)
        return f"Parameter {param_index} normalized value: {value:.3f}"
    else:
        raise Exception(f"Failed to get take FX normalized parameter: {result.get('error', 'Unknown error')}")


async def take_fx_set_param_normalized(item_index: int, take_index: int, fx_index: int, 
                                       param_index: int, value: float) -> str:
    """Set normalized take FX parameter value (0-1)"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Clamp value to 0-1 range
    value = max(0.0, min(1.0, value))
    
    # Set normalized parameter value
    result = await bridge.call_lua("TakeFX_SetParamNormalized", [take_handle, fx_index, param_index, value])
    
    if result.get("ok"):
        return f"Set parameter {param_index} normalized value to {value:.3f}"
    else:
        raise Exception(f"Failed to set take FX normalized parameter: {result.get('error', 'Unknown error')}")


async def take_fx_copy_to_track(item_index: int, take_index: int, fx_index: int, 
                               track_index: int, track_fx_index: int, move: bool = False) -> str:
    """Copy a take FX to a track"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get destination track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Copy FX
    result = await bridge.call_lua("TakeFX_CopyToTrack", [
        take_handle, fx_index, track_handle, track_fx_index, move
    ])
    
    if result.get("ok"):
        action = "Moved" if move else "Copied"
        return f"{action} take FX {fx_index} to track {track_index} at position {track_fx_index}"
    else:
        raise Exception(f"Failed to copy take FX to track: {result.get('error', 'Unknown error')}")


async def take_fx_copy_to_take(src_item_index: int, src_take_index: int, src_fx_index: int,
                              dst_item_index: int, dst_take_index: int, dst_fx_index: int, 
                              move: bool = False) -> str:
    """Copy a take FX to another take"""
    # Get source media item and take
    src_item_result = await bridge.call_lua("GetMediaItem", [0, src_item_index])
    if not src_item_result.get("ok") or not src_item_result.get("ret"):
        raise Exception(f"Failed to find source media item at index {src_item_index}")
    
    src_item_handle = src_item_result.get("ret")
    
    src_take_result = await bridge.call_lua("GetMediaItemTake", [src_item_handle, src_take_index])
    if not src_take_result.get("ok") or not src_take_result.get("ret"):
        raise Exception(f"Failed to find source take at index {src_take_index}")
    
    src_take_handle = src_take_result.get("ret")
    
    # Get destination media item and take
    dst_item_result = await bridge.call_lua("GetMediaItem", [0, dst_item_index])
    if not dst_item_result.get("ok") or not dst_item_result.get("ret"):
        raise Exception(f"Failed to find destination media item at index {dst_item_index}")
    
    dst_item_handle = dst_item_result.get("ret")
    
    dst_take_result = await bridge.call_lua("GetMediaItemTake", [dst_item_handle, dst_take_index])
    if not dst_take_result.get("ok") or not dst_take_result.get("ret"):
        raise Exception(f"Failed to find destination take at index {dst_take_index}")
    
    dst_take_handle = dst_take_result.get("ret")
    
    # Copy FX
    result = await bridge.call_lua("TakeFX_CopyToTake", [
        src_take_handle, src_fx_index, dst_take_handle, dst_fx_index, move
    ])
    
    if result.get("ok"):
        action = "Moved" if move else "Copied"
        return f"{action} FX from take {src_take_index} to take {dst_take_index}"
    else:
        raise Exception(f"Failed to copy take FX: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_fx_take_tools(mcp) -> int:
    """Register all take FX tools with the MCP instance"""
    tools = [
        # Take FX Management
        (take_fx_get_count, "Get the number of FX on a take"),
        (take_fx_add_by_name, "Add an FX to a take by name"),
        (take_fx_delete, "Delete an FX from a take"),
        (take_fx_get_enabled, "Get the enabled state of a take FX"),
        (take_fx_set_enabled, "Set the enabled state of a take FX"),
        (take_fx_get_fx_name, "Get the name of a take FX"),
        (take_fx_get_preset, "Get the current preset name of a take FX"),
        (take_fx_set_preset, "Set the preset of a take FX by name"),
        
        # Take FX Parameters
        (take_fx_get_num_params, "Get the number of parameters for a take FX"),
        (take_fx_get_param_name, "Get the name of a take FX parameter"),
        (take_fx_get_param, "Get take FX parameter value"),
        (take_fx_set_param, "Set take FX parameter value"),
        (take_fx_get_param_normalized, "Get normalized take FX parameter value (0-1)"),
        (take_fx_set_param_normalized, "Set normalized take FX parameter value (0-1)"),
        (take_fx_copy_to_track, "Copy a take FX to a track"),
        (take_fx_copy_to_take, "Copy a take FX to another take"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)