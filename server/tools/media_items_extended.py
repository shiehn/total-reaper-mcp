"""
Media Items Extended Tools for REAPER MCP

This module contains advanced media item operations including item info,
take management, stretch markers, and source operations.
"""

from typing import Optional, Tuple, List, Any
from ..bridge import bridge


# ============================================================================
# Media Item Info Operations (12 tools)
# ============================================================================

async def get_media_item_info_value(item_index: int, param_name: str) -> str:
    """Get media item information value"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get info value
    result = await bridge.call_lua("GetMediaItemInfo_Value", [item_handle, param_name])
    
    if result.get("ok"):
        value = result.get("ret", 0.0)
        return f"Item {param_name}: {value}"
    else:
        raise Exception(f"Failed to get item info: {result.get('error', 'Unknown error')}")


async def set_media_item_info_value(item_index: int, param_name: str, value: float) -> str:
    """Set media item information value"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Set info value
    result = await bridge.call_lua("SetMediaItemInfo_Value", [item_handle, param_name, value])
    
    if result.get("ok"):
        return f"Set item {param_name} to {value}"
    else:
        raise Exception(f"Failed to set item info: {result.get('error', 'Unknown error')}")


async def get_set_media_item_info_string(item_index: int, param_name: str, value: str = "", set_value: bool = False) -> str:
    """Get or set media item string information"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get/set string info
    result = await bridge.call_lua("GetSetMediaItemInfo_String", [item_handle, param_name, value, set_value])
    
    if result.get("ok"):
        if set_value:
            return f"Set item {param_name} to: {value}"
        else:
            info_value = result.get("ret", "")
            return f"Item {param_name}: {info_value if info_value else '(not set)'}"
    else:
        raise Exception(f"Failed to get/set item string info: {result.get('error', 'Unknown error')}")


async def get_media_item_num_takes(item_index: int) -> str:
    """Get the number of takes in a media item"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get take count
    result = await bridge.call_lua("GetMediaItemNumTakes", [item_handle])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Media item has {count} takes"
    else:
        raise Exception(f"Failed to get take count: {result.get('error', 'Unknown error')}")


async def get_media_item_take(item_index: int, take_index: int) -> str:
    """Get a specific take from a media item"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get specific take
    result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    
    if result.get("ok"):
        take = result.get("ret")
        if take:
            # Get take name for info
            name_result = await bridge.call_lua("GetTakeName", [take])
            take_name = name_result.get("ret", "Unnamed") if name_result.get("ok") else "Unknown"
            return f"Take {take_index}: {take_name}"
        else:
            return f"No take at index {take_index}"
    else:
        raise Exception(f"Failed to get take: {result.get('error', 'Unknown error')}")


async def get_media_item_take_item(item_index: int, take_index: int) -> str:
    """Get the parent item of a take"""
    # Get item and take first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get parent item from take
    result = await bridge.call_lua("GetMediaItemTake_Item", [take_handle])
    
    if result.get("ok"):
        parent_item = result.get("ret")
        if parent_item:
            return f"Take {take_index} belongs to item at index {item_index}"
        else:
            return f"Failed to get parent item for take {take_index}"
    else:
        raise Exception(f"Failed to get take parent item: {result.get('error', 'Unknown error')}")


async def get_media_item_take_track(item_index: int, take_index: int) -> str:
    """Get the track that contains a take's parent item"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get track from take
    result = await bridge.call_lua("GetMediaItemTake_Track", [take_handle])
    
    if result.get("ok"):
        track = result.get("ret")
        if track:
            # Get track name for info
            name_result = await bridge.call_lua("GetTrackName", [track])
            if name_result.get("ok") and isinstance(name_result.get("ret"), list):
                _, track_name = name_result.get("ret")[:2]
                return f"Take is on track: {track_name}"
            else:
                return "Take is on track (name unknown)"
        else:
            return "Failed to get track for take"
    else:
        raise Exception(f"Failed to get take track: {result.get('error', 'Unknown error')}")


async def get_media_item_take_info_value(item_index: int, take_index: int, param_name: str) -> str:
    """Get take information value"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get take info value
    result = await bridge.call_lua("GetMediaItemTakeInfo_Value", [take_handle, param_name])
    
    if result.get("ok"):
        value = result.get("ret", 0.0)
        return f"Take {param_name}: {value}"
    else:
        raise Exception(f"Failed to get take info: {result.get('error', 'Unknown error')}")


async def set_media_item_take_info_value(item_index: int, take_index: int, param_name: str, value: float) -> str:
    """Set take information value"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set take info value
    result = await bridge.call_lua("SetMediaItemTakeInfo_Value", [take_handle, param_name, value])
    
    if result.get("ok"):
        return f"Set take {param_name} to {value}"
    else:
        raise Exception(f"Failed to set take info: {result.get('error', 'Unknown error')}")


async def get_set_media_item_take_info_string(item_index: int, take_index: int, param_name: str, 
                                              value: str = "", set_value: bool = False) -> str:
    """Get or set take string information"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get/set take string info
    result = await bridge.call_lua("GetSetMediaItemTakeInfo_String", [take_handle, param_name, value, set_value])
    
    if result.get("ok"):
        if set_value:
            return f"Set take {param_name} to: {value}"
        else:
            info_value = result.get("ret", "")
            return f"Take {param_name}: {info_value if info_value else '(not set)'}"
    else:
        raise Exception(f"Failed to get/set take string info: {result.get('error', 'Unknown error')}")


async def is_item_take_active_for_playback(item_index: int, take_index: int) -> str:
    """Check if a take is active for playback"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Check if active
    result = await bridge.call_lua("TakeIsMIDI", [take_handle])  # Using as proxy, need proper function
    
    if result.get("ok"):
        # For now, check if it's the active take
        active_result = await bridge.call_lua("GetActiveTake", [item_handle])
        if active_result.get("ok"):
            is_active = active_result.get("ret") == take_handle
            return f"Take {take_index} is {'active' if is_active else 'not active'} for playback"
        else:
            return f"Take {take_index} playback status unknown"
    else:
        raise Exception(f"Failed to check take playback status: {result.get('error', 'Unknown error')}")


async def get_displayed_media_item_color(item_index: int) -> str:
    """Get the displayed color of a media item (considering take color)"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get displayed color
    result = await bridge.call_lua("GetDisplayedMediaItemColor", [item_handle])
    
    if result.get("ok"):
        color = result.get("ret", 0)
        return f"Item displayed color: {color:#08x}"
    else:
        raise Exception(f"Failed to get displayed item color: {result.get('error', 'Unknown error')}")


# ============================================================================
# Take Stretch Markers (8 tools)
# ============================================================================

async def get_take_num_stretch_markers(item_index: int, take_index: int) -> str:
    """Get the number of stretch markers in a take"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get stretch marker count
    result = await bridge.call_lua("GetTakeNumStretchMarkers", [take_handle])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Take has {count} stretch markers"
    else:
        raise Exception(f"Failed to get stretch marker count: {result.get('error', 'Unknown error')}")


async def get_take_stretch_marker(item_index: int, take_index: int, marker_index: int) -> str:
    """Get stretch marker information"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get stretch marker
    result = await bridge.call_lua("GetTakeStretchMarker", [take_handle, marker_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            idx, pos, src_pos = ret[:3]
            if idx >= 0:
                return f"Stretch marker {idx}: position={pos:.3f}, source position={src_pos:.3f}"
            else:
                return f"No stretch marker at index {marker_index}"
        else:
            return f"Failed to get stretch marker {marker_index}"
    else:
        raise Exception(f"Failed to get stretch marker: {result.get('error', 'Unknown error')}")


async def set_take_stretch_marker(item_index: int, take_index: int, marker_index: int, 
                                 pos: float, src_pos: Optional[float] = None) -> str:
    """Set stretch marker position"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set stretch marker
    if src_pos is None:
        src_pos = pos  # Default to same as position
    
    result = await bridge.call_lua("SetTakeStretchMarker", [take_handle, marker_index, pos, src_pos])
    
    if result.get("ok"):
        marker_idx = result.get("ret", -1)
        if marker_idx >= 0:
            return f"Set stretch marker {marker_idx} to position {pos:.3f}"
        else:
            return f"Failed to set stretch marker"
    else:
        raise Exception(f"Failed to set stretch marker: {result.get('error', 'Unknown error')}")


async def delete_take_stretch_marker(item_index: int, take_index: int, marker_index: int) -> str:
    """Delete a stretch marker"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Delete by setting to -1
    result = await bridge.call_lua("DeleteTakeStretchMarkers", [take_handle, marker_index, marker_index])
    
    if result.get("ok"):
        return f"Deleted stretch marker {marker_index}"
    else:
        raise Exception(f"Failed to delete stretch marker: {result.get('error', 'Unknown error')}")


async def delete_take_stretch_markers(item_index: int, take_index: int, start_idx: int, end_idx: int) -> str:
    """Delete a range of stretch markers"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Delete range
    result = await bridge.call_lua("DeleteTakeStretchMarkers", [take_handle, start_idx, end_idx])
    
    if result.get("ok"):
        count = end_idx - start_idx + 1
        return f"Deleted {count} stretch markers"
    else:
        raise Exception(f"Failed to delete stretch markers: {result.get('error', 'Unknown error')}")


async def get_take_stretch_marker_slope(item_index: int, take_index: int, marker_index: int) -> str:
    """Get stretch marker slope"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get slope
    result = await bridge.call_lua("GetTakeStretchMarkerSlope", [take_handle, marker_index])
    
    if result.get("ok"):
        slope = result.get("ret", 1.0)
        return f"Stretch marker {marker_index} slope: {slope:.3f}"
    else:
        raise Exception(f"Failed to get stretch marker slope: {result.get('error', 'Unknown error')}")


async def set_take_stretch_marker_slope(item_index: int, take_index: int, marker_index: int, slope: float) -> str:
    """Set stretch marker slope"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set slope
    result = await bridge.call_lua("SetTakeStretchMarkerSlope", [take_handle, marker_index, slope])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set stretch marker {marker_index} slope to {slope:.3f}"
        else:
            return f"Failed to set stretch marker slope"
    else:
        raise Exception(f"Failed to set stretch marker slope: {result.get('error', 'Unknown error')}")


async def get_take_stretch_play_rate(item_index: int, take_index: int) -> str:
    """Get take stretch/playback rate"""
    # Get item and take  
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get play rate (D_PLAYRATE)
    result = await bridge.call_lua("GetMediaItemTakeInfo_Value", [take_handle, "D_PLAYRATE"])
    
    if result.get("ok"):
        rate = result.get("ret", 1.0)
        return f"Take playback rate: {rate:.3f}x"
    else:
        raise Exception(f"Failed to get take play rate: {result.get('error', 'Unknown error')}")


# ============================================================================
# Take Markers (6 tools)
# ============================================================================

async def get_num_take_markers(item_index: int, take_index: int) -> str:
    """Get number of take markers"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get marker count
    result = await bridge.call_lua("GetNumTakeMarkers", [take_handle])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Take has {count} markers"
    else:
        raise Exception(f"Failed to get take marker count: {result.get('error', 'Unknown error')}")


async def get_take_marker(item_index: int, take_index: int, marker_index: int) -> str:
    """Get take marker information"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get marker
    result = await bridge.call_lua("GetTakeMarker", [take_handle, marker_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            position, name, color = ret[:3]
            if position >= 0:
                return f"Take marker {marker_index}: position={position:.3f}, name='{name}', color={color:#08x}"
            else:
                return f"No marker at index {marker_index}"
        else:
            return f"Failed to get marker {marker_index}"
    else:
        raise Exception(f"Failed to get take marker: {result.get('error', 'Unknown error')}")


async def set_take_marker(item_index: int, take_index: int, marker_index: int, 
                         name: str = "", position: float = -1.0, color: int = 0) -> str:
    """Set or add take marker"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set/add marker (-1 to add new)
    result = await bridge.call_lua("SetTakeMarker", [take_handle, marker_index, name, position, color])
    
    if result.get("ok"):
        new_idx = result.get("ret", -1)
        if new_idx >= 0:
            action = "Added" if marker_index == -1 else "Updated"
            return f"{action} marker at index {new_idx}"
        else:
            return "Failed to set take marker"
    else:
        raise Exception(f"Failed to set take marker: {result.get('error', 'Unknown error')}")


async def delete_take_marker(item_index: int, take_index: int, marker_index: int) -> str:
    """Delete a take marker"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Delete marker by setting position to -1
    result = await bridge.call_lua("DeleteTakeMarker", [take_handle, marker_index])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Deleted take marker {marker_index}"
        else:
            return f"Failed to delete take marker {marker_index}"
    else:
        raise Exception(f"Failed to delete take marker: {result.get('error', 'Unknown error')}")


async def count_take_markers_by_name(item_index: int, take_index: int, name: str) -> str:
    """Count take markers with specific name"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get total marker count
    count_result = await bridge.call_lua("GetNumTakeMarkers", [take_handle])
    if not count_result.get("ok"):
        raise Exception("Failed to get marker count")
    
    total_markers = count_result.get("ret", 0)
    matched_count = 0
    
    # Count markers with matching name
    for i in range(total_markers):
        marker_result = await bridge.call_lua("GetTakeMarker", [take_handle, i])
        if marker_result.get("ok"):
            ret = marker_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 2:
                _, marker_name = ret[:2]
                if marker_name == name:
                    matched_count += 1
    
    return f"Found {matched_count} markers named '{name}'"


async def get_all_take_markers(item_index: int, take_index: int) -> str:
    """Get all take markers as a list"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get total marker count
    count_result = await bridge.call_lua("GetNumTakeMarkers", [take_handle])
    if not count_result.get("ok"):
        raise Exception("Failed to get marker count")
    
    total_markers = count_result.get("ret", 0)
    
    if total_markers == 0:
        return "Take has no markers"
    
    # Get all markers
    markers_info = []
    for i in range(total_markers):
        marker_result = await bridge.call_lua("GetTakeMarker", [take_handle, i])
        if marker_result.get("ok"):
            ret = marker_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 3:
                position, name, color = ret[:3]
                if position >= 0:
                    markers_info.append(f"  {i}: {position:.3f}s - '{name}'")
    
    if markers_info:
        return f"Take has {len(markers_info)} markers:\n" + "\n".join(markers_info)
    else:
        return "Failed to retrieve marker information"


# ============================================================================
# Source Operations (4 tools)
# ============================================================================

async def get_media_source_parent(item_index: int, take_index: int) -> str:
    """Get parent source (for reversed/stretched sources)"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get source
    source_result = await bridge.call_lua("GetMediaItemTake_Source", [take_handle])
    if not source_result.get("ok") or not source_result.get("ret"):
        raise Exception("Failed to get take source")
    
    source_handle = source_result.get("ret")
    
    # Get parent source
    result = await bridge.call_lua("GetMediaSourceParent", [source_handle])
    
    if result.get("ok"):
        parent = result.get("ret")
        if parent:
            # Get parent filename
            filename_result = await bridge.call_lua("GetMediaSourceFileName", [parent, "", 4096])
            if filename_result.get("ok"):
                filename = filename_result.get("ret", "")
                return f"Parent source: {filename}"
            else:
                return "Parent source exists but filename unknown"
        else:
            return "No parent source (this is the root source)"
    else:
        raise Exception(f"Failed to get parent source: {result.get('error', 'Unknown error')}")


async def validate_media_source_filename(filename: str) -> str:
    """Validate if a file can be used as a media source"""
    # Check if file exists and is valid media
    result = await bridge.call_lua("PCM_Source_CreateFromFile", [filename])
    
    if result.get("ok"):
        source = result.get("ret")
        if source:
            # Destroy the test source
            await bridge.call_lua("PCM_Source_Destroy", [source])
            return f"File '{filename}' is a valid media source"
        else:
            return f"File '{filename}' is not a valid media source"
    else:
        raise Exception(f"Failed to validate media source: {result.get('error', 'Unknown error')}")


async def get_source_peaks(item_index: int, take_index: int, start_time: float, 
                          num_channels: int, num_samples: int, want_min_max: int = 0) -> str:
    """Get peak samples from source"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get source
    source_result = await bridge.call_lua("GetMediaItemTake_Source", [take_handle])
    if not source_result.get("ok") or not source_result.get("ret"):
        raise Exception("Failed to get take source")
    
    source_handle = source_result.get("ret")
    
    # Get peaks
    result = await bridge.call_lua("PCM_Source_GetPeaks", [
        source_handle, 1000.0, start_time, num_channels, num_samples, want_min_max, []
    ])
    
    if result.get("ok"):
        samples = result.get("ret", 0)
        return f"Retrieved {samples} peak samples"
    else:
        raise Exception(f"Failed to get source peaks: {result.get('error', 'Unknown error')}")


async def build_peak_cache_for_source(item_index: int, take_index: int) -> str:
    """Build peak cache for source if needed"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get source
    source_result = await bridge.call_lua("GetMediaItemTake_Source", [take_handle])
    if not source_result.get("ok") or not source_result.get("ret"):
        raise Exception("Failed to get take source")
    
    source_handle = source_result.get("ret")
    
    # Build peaks if needed
    result = await bridge.call_lua("PCM_Source_BuildPeaks", [source_handle, 0])
    
    if result.get("ok"):
        status = result.get("ret", 0)
        if status == 0:
            return "Peak cache is already built"
        else:
            return f"Building peak cache (status: {status})"
    else:
        raise Exception(f"Failed to build peak cache: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_media_items_extended_tools(mcp) -> int:
    """Register all media items extended tools with the MCP instance"""
    tools = [
        # Media Item Info Operations
        (get_media_item_info_value, "Get media item information value"),
        (set_media_item_info_value, "Set media item information value"),
        (get_set_media_item_info_string, "Get or set media item string information"),
        (get_media_item_num_takes, "Get the number of takes in a media item"),
        (get_media_item_take, "Get a specific take from a media item"),
        (get_media_item_take_item, "Get the parent item of a take"),
        (get_media_item_take_track, "Get the track that contains a take's parent item"),
        (get_media_item_take_info_value, "Get take information value"),
        (set_media_item_take_info_value, "Set take information value"),
        (get_set_media_item_take_info_string, "Get or set take string information"),
        (is_item_take_active_for_playback, "Check if a take is active for playback"),
        (get_displayed_media_item_color, "Get the displayed color of a media item"),
        
        # Take Stretch Markers
        (get_take_num_stretch_markers, "Get the number of stretch markers in a take"),
        (get_take_stretch_marker, "Get stretch marker information"),
        (set_take_stretch_marker, "Set stretch marker position"),
        (delete_take_stretch_marker, "Delete a stretch marker"),
        (delete_take_stretch_markers, "Delete a range of stretch markers"),
        (get_take_stretch_marker_slope, "Get stretch marker slope"),
        (set_take_stretch_marker_slope, "Set stretch marker slope"),
        (get_take_stretch_play_rate, "Get take stretch/playback rate"),
        
        # Take Markers
        (get_num_take_markers, "Get number of take markers"),
        (get_take_marker, "Get take marker information"),
        (set_take_marker, "Set or add take marker"),
        (delete_take_marker, "Delete a take marker"),
        (count_take_markers_by_name, "Count take markers with specific name"),
        (get_all_take_markers, "Get all take markers as a list"),
        
        # Source Operations
        (get_media_source_parent, "Get parent source (for reversed/stretched sources)"),
        (validate_media_source_filename, "Validate if a file can be used as a media source"),
        (get_source_peaks, "Get peak samples from source"),
        (build_peak_cache_for_source, "Build peak cache for source if needed"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)