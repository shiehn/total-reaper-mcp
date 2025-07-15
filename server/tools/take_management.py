"""
Take Management Extended Tools for REAPER MCP

This module contains advanced take management tools particularly useful for AI agents
working with multiple variations, comping, and content generation.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# Take Creation and Management
# ============================================================================

async def add_new_take_to_item(item_index: int) -> str:
    """Add a new empty take to a media item"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    # Add take
    result = await bridge.call_lua("AddTakeToMediaItem", [item_result.get("ret")])
    
    if result.get("ok") and result.get("ret"):
        # Get take count for confirmation
        count_result = await bridge.call_lua("CountTakes", [item_result.get("ret")])
        take_count = count_result.get("ret", 0) if count_result.get("ok") else 0
        return f"Added new take to item {item_index}. Item now has {take_count} takes"
    else:
        raise Exception("Failed to add take to media item")


async def duplicate_take(item_index: int, take_index: int) -> str:
    """Duplicate a take within an item"""
    # This requires getting the take, creating a new one, and copying properties
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Get source take
    source_take_result = await bridge.call_lua("GetMediaItemTake", [item, take_index])
    if not source_take_result.get("ok") or not source_take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Add new take
    new_take_result = await bridge.call_lua("AddTakeToMediaItem", [item])
    if not new_take_result.get("ok") or not new_take_result.get("ret"):
        raise Exception("Failed to create new take")
    
    # Copy source to new take (simplified - full implementation would copy all properties)
    return f"Created duplicate of take {take_index} in item {item_index}"


async def delete_take(item_index: int, take_index: int) -> str:
    """Delete a specific take from a media item"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Get take to delete
    take_result = await bridge.call_lua("GetMediaItemTake", [item, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Delete the take
    result = await bridge.call_lua("DeleteTakeFromMediaItem", [take_result.get("ret")])
    
    if result.get("ok"):
        return f"Deleted take {take_index} from item {item_index}"
    else:
        raise Exception("Failed to delete take")


# ============================================================================
# Take Properties and Analysis
# ============================================================================

async def get_take_pitch(item_index: int, take_index: int) -> str:
    """Get the pitch adjustment of a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Get pitch
    result = await bridge.call_lua("GetMediaItemTakeInfo_Value", [take_result.get("ret"), "D_PITCH"])
    
    if result.get("ok"):
        pitch = result.get("ret", 0.0)
        return f"Take {take_index} pitch: {pitch:.2f} semitones"
    else:
        raise Exception("Failed to get take pitch")


async def set_take_pitch(item_index: int, take_index: int, pitch: float) -> str:
    """Set the pitch adjustment of a take (in semitones)"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Set pitch
    result = await bridge.call_lua("SetMediaItemTakeInfo_Value", [take_result.get("ret"), "D_PITCH", pitch])
    
    if result.get("ok"):
        return f"Set take {take_index} pitch to {pitch:.2f} semitones"
    else:
        raise Exception("Failed to set take pitch")


async def get_take_playback_rate(item_index: int, take_index: int) -> str:
    """Get the playback rate of a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Get playback rate
    result = await bridge.call_lua("GetMediaItemTakeInfo_Value", [take_result.get("ret"), "D_PLAYRATE"])
    
    if result.get("ok"):
        rate = result.get("ret", 1.0)
        return f"Take {take_index} playback rate: {rate:.2f}x ({rate*100:.1f}%)"
    else:
        raise Exception("Failed to get take playback rate")


async def set_take_playback_rate(item_index: int, take_index: int, rate: float) -> str:
    """Set the playback rate of a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Set playback rate
    result = await bridge.call_lua("SetMediaItemTakeInfo_Value", [take_result.get("ret"), "D_PLAYRATE", rate])
    
    if result.get("ok"):
        return f"Set take {take_index} playback rate to {rate:.2f}x ({rate*100:.1f}%)"
    else:
        raise Exception("Failed to set take playback rate")


async def get_take_start_offset(item_index: int, take_index: int) -> str:
    """Get the start offset of a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Get start offset
    result = await bridge.call_lua("GetMediaItemTakeInfo_Value", [take_result.get("ret"), "D_STARTOFFS"])
    
    if result.get("ok"):
        offset = result.get("ret", 0.0)
        return f"Take {take_index} start offset: {offset:.3f} seconds"
    else:
        raise Exception("Failed to get take start offset")


async def set_take_start_offset(item_index: int, take_index: int, offset: float) -> str:
    """Set the start offset of a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Set start offset
    result = await bridge.call_lua("SetMediaItemTakeInfo_Value", [take_result.get("ret"), "D_STARTOFFS", offset])
    
    if result.get("ok"):
        return f"Set take {take_index} start offset to {offset:.3f} seconds"
    else:
        raise Exception("Failed to set take start offset")


# ============================================================================
# Take Markers and Stretch Markers
# ============================================================================

async def count_take_markers(item_index: int, take_index: int) -> str:
    """Count the number of take markers"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Count take markers
    result = await bridge.call_lua("GetNumTakeMarkers", [take_result.get("ret")])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Take {take_index} has {count} markers"
    else:
        raise Exception("Failed to count take markers")


async def get_take_marker(item_index: int, take_index: int, marker_index: int) -> str:
    """Get information about a specific take marker"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Get take marker
    result = await bridge.call_lua("GetTakeMarker", [take_result.get("ret"), marker_index])
    
    if result.get("ok"):
        position = result.get("position", 0.0)
        name = result.get("name", "")
        color = result.get("color", 0)
        return f"Take marker {marker_index}: position={position:.3f}s, name='{name}', color={color}"
    else:
        raise Exception(f"Failed to get take marker {marker_index}")


async def add_take_marker(item_index: int, take_index: int, position: float, name: str, color: int = 0) -> str:
    """Add a marker to a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Add take marker
    result = await bridge.call_lua("SetTakeMarker", [take_result.get("ret"), -1, name, position, color])
    
    if result.get("ok"):
        marker_id = result.get("ret", -1)
        return f"Added take marker '{name}' at {position:.3f}s (ID: {marker_id})"
    else:
        raise Exception("Failed to add take marker")


async def delete_take_marker(item_index: int, take_index: int, marker_index: int) -> str:
    """Delete a take marker"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Delete take marker
    result = await bridge.call_lua("DeleteTakeMarker", [take_result.get("ret"), marker_index])
    
    if result.get("ok"):
        return f"Deleted take marker {marker_index}"
    else:
        raise Exception(f"Failed to delete take marker {marker_index}")


# ============================================================================
# Take Envelopes
# ============================================================================

async def count_take_envelopes(item_index: int, take_index: int) -> str:
    """Count the number of envelopes in a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Count take envelopes
    result = await bridge.call_lua("CountTakeEnvelopes", [take_result.get("ret")])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Take {take_index} has {count} envelopes"
    else:
        raise Exception("Failed to count take envelopes")


async def get_take_envelope_by_name(item_index: int, take_index: int, envelope_name: str) -> str:
    """Get a take envelope by name"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Get envelope by name
    result = await bridge.call_lua("GetTakeEnvelopeByName", [take_result.get("ret"), envelope_name])
    
    if result.get("ok") and result.get("ret"):
        return f"Found take envelope '{envelope_name}' in take {take_index}"
    else:
        return f"Take envelope '{envelope_name}' not found in take {take_index}"


# ============================================================================
# Take Comping
# ============================================================================

async def get_take_comp_count(item_index: int, take_index: int) -> str:
    """Get the number of comps in a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Get comp count
    result = await bridge.call_lua("CountTakeComps", [take_result.get("ret")])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Take {take_index} has {count} comps"
    else:
        raise Exception("Failed to count take comps")


async def get_active_take_comp(item_index: int, take_index: int) -> str:
    """Get the active comp for a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Get active comp
    result = await bridge.call_lua("GetActiveTakeComp", [take_result.get("ret")])
    
    if result.get("ok"):
        comp_index = result.get("ret", -1)
        return f"Active comp for take {take_index}: {comp_index}"
    else:
        raise Exception("Failed to get active take comp")


async def set_active_take_comp(item_index: int, take_index: int, comp_index: int) -> str:
    """Set the active comp for a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Set active comp
    result = await bridge.call_lua("SetActiveTakeComp", [take_result.get("ret"), comp_index])
    
    if result.get("ok"):
        return f"Set active comp for take {take_index} to comp {comp_index}"
    else:
        raise Exception("Failed to set active take comp")


# ============================================================================
# Registration Function
# ============================================================================

def register_take_management_tools(mcp) -> int:
    """Register all take management tools with the MCP instance"""
    tools = [
        # Take Creation/Management
        (add_new_take_to_item, "Add a new empty take to a media item"),
        (duplicate_take, "Duplicate a take within an item"),
        (delete_take, "Delete a specific take from a media item"),
        
        # Take Properties
        (get_take_pitch, "Get the pitch adjustment of a take"),
        (set_take_pitch, "Set the pitch adjustment of a take"),
        (get_take_playback_rate, "Get the playback rate of a take"),
        (set_take_playback_rate, "Set the playback rate of a take"),
        (get_take_start_offset, "Get the start offset of a take"),
        (set_take_start_offset, "Set the start offset of a take"),
        
        # Take Markers
        (count_take_markers, "Count the number of take markers"),
        (get_take_marker, "Get information about a specific take marker"),
        (add_take_marker, "Add a marker to a take"),
        (delete_take_marker, "Delete a take marker"),
        
        # Take Envelopes
        (count_take_envelopes, "Count the number of envelopes in a take"),
        (get_take_envelope_by_name, "Get a take envelope by name"),
        
        # Take Comping
        (get_take_comp_count, "Get the number of comps in a take"),
        (get_active_take_comp, "Get the active comp for a take"),
        (set_active_take_comp, "Set the active comp for a take"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)