"""
Media Items & Takes Tools for REAPER MCP

This module contains tools for managing media items and takes.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# Media Item Management (10 tools)
# ============================================================================

async def add_media_item_to_track(track_index: int) -> str:
    """Add a new media item to a track"""
    # Get track first
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    result = await bridge.call_lua("AddMediaItemToTrack", [track_result.get("ret")])
    
    if result.get("ok"):
        item = result.get("ret")
        return f"Added media item to track {track_index}: {item}"
    else:
        raise Exception(f"Failed to add media item: {result.get('error', 'Unknown error')}")


async def count_media_items(project_index: int = 0) -> str:
    """Count the number of media items in the project"""
    result = await bridge.call_lua("CountMediaItems", [project_index])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Project has {count} media items"
    else:
        raise Exception(f"Failed to count media items: {result.get('error', 'Unknown error')}")


async def get_media_item(item_index: int, project_index: int = 0) -> str:
    """Get a media item by index"""
    result = await bridge.call_lua("GetMediaItem", [project_index, item_index])
    
    if result.get("ok"):
        item = result.get("ret")
        if item:
            return f"Media item at index {item_index}: {item}"
        else:
            return f"No media item found at index {item_index}"
    else:
        raise Exception(f"Failed to get media item: {result.get('error', 'Unknown error')}")


async def delete_track_media_item(track_index: int, item_index: int) -> str:
    """Delete a media item from a track"""
    # Get track first
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get item on track
    item_result = await bridge.call_lua("GetTrackMediaItem", [track_result.get("ret"), item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item {item_index} on track {track_index}")
    
    # Delete item
    result = await bridge.call_lua("DeleteTrackMediaItem", [track_result.get("ret"), item_result.get("ret")])
    
    if result.get("ok"):
        return f"Deleted media item {item_index} from track {track_index}"
    else:
        raise Exception(f"Failed to delete media item: {result.get('error', 'Unknown error')}")


async def get_media_item_length(item_index: int) -> str:
    """Get the length of a media item in seconds"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("GetMediaItemInfo_Value", [item_result.get("ret"), "D_LENGTH"])
    
    if result.get("ok"):
        length = result.get("ret", 0.0)
        return f"Media item {item_index} length: {length:.3f} seconds"
    else:
        raise Exception(f"Failed to get media item length: {result.get('error', 'Unknown error')}")


async def set_media_item_length(item_index: int, length: float) -> str:
    """Set the length of a media item in seconds"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("SetMediaItemLength", [item_result.get("ret"), length, True])
    
    if result.get("ok"):
        return f"Set media item {item_index} length to {length:.3f} seconds"
    else:
        raise Exception(f"Failed to set media item length: {result.get('error', 'Unknown error')}")


async def get_media_item_position(item_index: int) -> str:
    """Get the position of a media item in seconds"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("GetMediaItemInfo_Value", [item_result.get("ret"), "D_POSITION"])
    
    if result.get("ok"):
        position = result.get("ret", 0.0)
        return f"Media item {item_index} position: {position:.3f} seconds"
    else:
        raise Exception(f"Failed to get media item position: {result.get('error', 'Unknown error')}")


async def set_media_item_position(item_index: int, position: float) -> str:
    """Set the position of a media item in seconds"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("SetMediaItemPosition", [item_result.get("ret"), position, True])
    
    if result.get("ok"):
        return f"Set media item {item_index} position to {position:.3f} seconds"
    else:
        raise Exception(f"Failed to set media item position: {result.get('error', 'Unknown error')}")


async def set_media_item_selected(item_index: int, selected: bool) -> str:
    """Set the selection state of a media item"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("SetMediaItemSelected", [item_result.get("ret"), selected])
    
    if result.get("ok"):
        state = "selected" if selected else "unselected"
        return f"Media item {item_index} is now {state}"
    else:
        raise Exception(f"Failed to set media item selection: {result.get('error', 'Unknown error')}")


async def count_selected_media_items(project_index: int = 0) -> str:
    """Count the number of selected media items"""
    result = await bridge.call_lua("CountSelectedMediaItems", [project_index])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Project has {count} selected media items"
    else:
        raise Exception(f"Failed to count selected items: {result.get('error', 'Unknown error')}")


async def get_selected_media_item(index: int, project_index: int = 0) -> str:
    """Get a selected media item by index"""
    result = await bridge.call_lua("GetSelectedMediaItem", [project_index, index])
    
    if result.get("ok"):
        item = result.get("ret")
        if item:
            return f"Selected media item at index {index}: {item}"
        else:
            return f"No selected media item at index {index}"
    else:
        raise Exception(f"Failed to get selected item: {result.get('error', 'Unknown error')}")


# ============================================================================
# Media Item Operations (7 tools)
# ============================================================================

async def split_media_item(item_index: int, split_position: float) -> str:
    """Split a media item at the specified position"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("SplitMediaItem", [item_result.get("ret"), split_position])
    
    if result.get("ok"):
        return f"Split media item {item_index} at position {split_position:.3f}"
    else:
        raise Exception(f"Failed to split media item: {result.get('error', 'Unknown error')}")


async def glue_media_items(item_indices: list[int], project_index: int = 0) -> str:
    """Glue multiple media items together"""
    # Implementation would need to select items first then call glue action
    # This is a simplified version
    result = await bridge.call_lua("Main_OnCommand", [40362, 0])  # Glue items
    
    if result.get("ok"):
        return f"Glued {len(item_indices)} media items"
    else:
        raise Exception(f"Failed to glue items: {result.get('error', 'Unknown error')}")


async def duplicate_media_item(item_index: int) -> str:
    """Duplicate a media item"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    # Select the item
    await bridge.call_lua("SetMediaItemSelected", [item_result.get("ret"), True])
    
    # Duplicate selected items
    result = await bridge.call_lua("Main_OnCommand", [41295, 0])  # Duplicate items
    
    if result.get("ok"):
        return f"Duplicated media item {item_index}"
    else:
        raise Exception(f"Failed to duplicate item: {result.get('error', 'Unknown error')}")


async def set_media_item_color(item_index: int, color: int) -> str:
    """Set the color of a media item"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("SetMediaItemInfo_Value", [item_result.get("ret"), "I_CUSTOMCOLOR", color | 0x01000000])
    
    if result.get("ok"):
        return f"Set media item {item_index} color to {color:#08x}"
    else:
        raise Exception(f"Failed to set item color: {result.get('error', 'Unknown error')}")


async def get_media_item_color(item_index: int) -> str:
    """Get the color of a media item"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("GetMediaItemInfo_Value", [item_result.get("ret"), "I_CUSTOMCOLOR"])
    
    if result.get("ok"):
        color = int(result.get("ret", 0))
        if color & 0x01000000:
            color = color & 0xFFFFFF
            return f"Media item {item_index} color: {color:#08x}"
        else:
            return f"Media item {item_index} has no custom color"
    else:
        raise Exception(f"Failed to get item color: {result.get('error', 'Unknown error')}")


async def get_media_item_peak(item_index: int) -> str:
    """Get the peak value of a media item"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    # Get active take
    take_result = await bridge.call_lua("GetActiveTake", [item_result.get("ret")])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception("No active take in media item")
    
    # Get peak
    result = await bridge.call_lua("NF_GetMediaItemMaxPeak", [item_result.get("ret")])
    
    if result.get("ok"):
        peak = result.get("ret", 0.0)
        return f"Media item {item_index} peak: {peak:.3f}"
    else:
        raise Exception(f"Failed to get item peak: {result.get('error', 'Unknown error')}")


async def get_media_item_take_track(item_index: int, take_index: int) -> str:
    """Get the track that contains a media item"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("GetMediaItem_Track", [item_result.get("ret")])
    
    if result.get("ok"):
        track = result.get("ret")
        return f"Media item {item_index} is on track: {track}"
    else:
        raise Exception(f"Failed to get item track: {result.get('error', 'Unknown error')}")


# ============================================================================
# Take Management (11 tools)
# ============================================================================

async def count_takes(item_index: int) -> str:
    """Count the number of takes in a media item"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("CountTakes", [item_result.get("ret")])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Media item {item_index} has {count} takes"
    else:
        raise Exception(f"Failed to count takes: {result.get('error', 'Unknown error')}")


async def get_active_take(item_index: int) -> str:
    """Get the active take of a media item"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    result = await bridge.call_lua("GetActiveTake", [item_result.get("ret")])
    
    if result.get("ok"):
        take = result.get("ret")
        if take:
            # Get take name
            name_result = await bridge.call_lua("GetTakeName", [take])
            take_name = name_result.get("ret", "Unnamed") if name_result.get("ok") else "Unknown"
            return f"Active take: {take_name}"
        else:
            return "No active take in media item"
    else:
        raise Exception(f"Failed to get active take: {result.get('error', 'Unknown error')}")


async def set_active_take(item_index: int, take_index: int) -> str:
    """Set the active take of a media item"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    # Get the specific take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_result.get("ret"), take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take {take_index} in media item")
    
    # Set as active
    result = await bridge.call_lua("SetActiveTake", [take_result.get("ret")])
    
    if result.get("ok"):
        return f"Set take {take_index} as active in media item {item_index}"
    else:
        raise Exception(f"Failed to set active take: {result.get('error', 'Unknown error')}")


async def get_take_name(item_index: int, take_index: int) -> str:
    """Get the name of a take"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    # Get the specific take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_result.get("ret"), take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take {take_index} in media item")
    
    result = await bridge.call_lua("GetTakeName", [take_result.get("ret")])
    
    if result.get("ok"):
        name = result.get("ret", "")
        return f"Take {take_index} name: {name}"
    else:
        raise Exception(f"Failed to get take name: {result.get('error', 'Unknown error')}")


async def set_take_name(item_index: int, take_index: int, name: str) -> str:
    """Set the name of a take"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    # Get the specific take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_result.get("ret"), take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take {take_index} in media item")
    
    result = await bridge.call_lua("GetSetMediaItemTakeInfo_String", [take_result.get("ret"), "P_NAME", name, True])
    
    if result.get("ok"):
        return f"Set take {take_index} name to: {name}"
    else:
        raise Exception(f"Failed to set take name: {result.get('error', 'Unknown error')}")


async def get_media_item_take_source(item_index: int, take_index: int) -> str:
    """Get the source file of a take"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    # Get the specific take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_result.get("ret"), take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take {take_index} in media item")
    
    # Get source
    source_result = await bridge.call_lua("GetMediaItemTake_Source", [take_result.get("ret")])
    if not source_result.get("ok") or not source_result.get("ret"):
        raise Exception("Failed to get take source")
    
    # Get filename
    result = await bridge.call_lua("GetMediaSourceFileName", [source_result.get("ret"), "", 4096])
    
    if result.get("ok"):
        filename = result.get("ret", "")
        return f"Take {take_index} source: {filename}"
    else:
        raise Exception(f"Failed to get source filename: {result.get('error', 'Unknown error')}")


async def set_media_item_take_source(item_index: int, take_index: int, source_file: str) -> str:
    """Set the source file of a take"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    # Get the specific take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_result.get("ret"), take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take {take_index} in media item")
    
    # Create PCM source
    source_result = await bridge.call_lua("PCM_Source_CreateFromFile", [source_file])
    if not source_result.get("ok") or not source_result.get("ret"):
        raise Exception(f"Failed to create source from file: {source_file}")
    
    # Set the source
    result = await bridge.call_lua("SetMediaItemTake_Source", [take_result.get("ret"), source_result.get("ret")])
    
    if result.get("ok"):
        return f"Set take {take_index} source to: {source_file}"
    else:
        raise Exception(f"Failed to set take source: {result.get('error', 'Unknown error')}")


async def get_media_item_take_peaks(item_index: int, take_index: int, channel: int, start_time: float, num_samples: int, num_channels: int, sample_rate: int) -> str:
    """Get peak samples from a take"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    # Get the specific take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_result.get("ret"), take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take {take_index} in media item")
    
    result = await bridge.call_lua("GetMediaItemTake_Peaks", [take_result.get("ret"), sample_rate, start_time, num_channels, num_samples, channel, []])
    
    if result.get("ok"):
        return f"Retrieved {num_samples} peak samples from take {take_index}"
    else:
        raise Exception(f"Failed to get take peaks: {result.get('error', 'Unknown error')}")


async def get_media_item_take_info_value(item_index: int, take_index: int, param_name: str) -> str:
    """Get a parameter value from a take"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    # Get the specific take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_result.get("ret"), take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take {take_index} in media item")
    
    result = await bridge.call_lua("GetMediaItemTakeInfo_Value", [take_result.get("ret"), param_name])
    
    if result.get("ok"):
        value = result.get("ret", 0)
        return f"Take {take_index} {param_name}: {value}"
    else:
        raise Exception(f"Failed to get take info: {result.get('error', 'Unknown error')}")


async def set_media_item_take_info_value(item_index: int, take_index: int, param_name: str, value: float) -> str:
    """Set a parameter value for a take"""
    # Get item first
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    # Get the specific take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_result.get("ret"), take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take {take_index} in media item")
    
    result = await bridge.call_lua("SetMediaItemTakeInfo_Value", [take_result.get("ret"), param_name, value])
    
    if result.get("ok"):
        return f"Set take {take_index} {param_name} to {value}"
    else:
        raise Exception(f"Failed to set take info: {result.get('error', 'Unknown error')}")


async def create_midi_item(track_index: int, position: float, length: float, quantize: Optional[bool] = False) -> str:
    """Create a new MIDI item on a track"""
    # Get track first
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    result = await bridge.call_lua("CreateNewMIDIItemInProj", [track_result.get("ret"), position, position + length, quantize])
    
    if result.get("ok"):
        return f"Created MIDI item on track {track_index} at position {position:.3f} with length {length:.3f}"
    else:
        raise Exception(f"Failed to create MIDI item: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_media_items_tools(mcp) -> int:
    """Register all media items and takes tools with the MCP instance"""
    tools = [
        # Media Item Management
        (add_media_item_to_track, "Add a new media item to a track"),
        (count_media_items, "Count the number of media items in the project"),
        (get_media_item, "Get a media item by index"),
        (delete_track_media_item, "Delete a media item from a track"),
        (get_media_item_length, "Get the length of a media item in seconds"),
        (set_media_item_length, "Set the length of a media item in seconds"),
        (get_media_item_position, "Get the position of a media item in seconds"),
        (set_media_item_position, "Set the position of a media item in seconds"),
        (set_media_item_selected, "Set the selection state of a media item"),
        (count_selected_media_items, "Count the number of selected media items"),
        (get_selected_media_item, "Get a selected media item by index"),
        
        # Media Item Operations
        (split_media_item, "Split a media item at the specified position"),
        (glue_media_items, "Glue multiple media items together"),
        (duplicate_media_item, "Duplicate a media item"),
        (set_media_item_color, "Set the color of a media item"),
        (get_media_item_color, "Get the color of a media item"),
        (get_media_item_peak, "Get the peak value of a media item"),
        (get_media_item_take_track, "Get the track that contains a media item"),
        
        # Take Management
        (count_takes, "Count the number of takes in a media item"),
        (get_active_take, "Get the active take of a media item"),
        (set_active_take, "Set the active take of a media item"),
        (get_take_name, "Get the name of a take"),
        (set_take_name, "Set the name of a take"),
        (get_media_item_take_source, "Get the source file of a take"),
        (set_media_item_take_source, "Set the source file of a take"),
        (get_media_item_take_peaks, "Get peak samples from a take"),
        (get_media_item_take_info_value, "Get a parameter value from a take"),
        (set_media_item_take_info_value, "Set a parameter value for a take"),
        (create_midi_item, "Create a new MIDI item on a track"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)