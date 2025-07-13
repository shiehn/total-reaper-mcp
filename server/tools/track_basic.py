"""
Basic Track Operations for REAPER MCP

This module contains basic track operations like insert, delete, count, etc.
"""

from typing import Optional
from ..bridge import bridge


async def insert_track(index: int, use_defaults: bool = True) -> str:
    """Insert a new track at the specified index (0-based)
    
    Args:
        index: The index where the track should be inserted (0-based)
        use_defaults: Whether to use default track settings
        
    Returns:
        Success or error message
    """
    result = await bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
    
    if result.get("ok"):
        return f"Successfully inserted track at index {index}"
    else:
        raise Exception(f"Failed to insert track: {result.get('error', 'Unknown error')}")


async def get_track_count() -> str:
    """Get the number of tracks in the current project
    
    Returns:
        Track count information
    """
    result = await bridge.call_lua("CountTracks", [0])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Current project has {count} tracks"
    else:
        raise Exception(f"Failed to get track count: {result.get('error', 'Unknown error')}")


async def get_track(track_index: int) -> str:
    """Get a track by index from the current project
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        
    Returns:
        Track information
    """
    if track_index == -1:
        result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if result.get("ok") and result.get("ret"):
        return f"Found track at index {track_index}"
    else:
        raise Exception(f"Track not found at index {track_index}")


async def delete_track(track_index: int) -> str:
    """Delete a track by index
    
    Args:
        track_index: The index of the track to delete (0-based)
        
    Returns:
        Success message
    """
    # Get track count first
    count_result = await bridge.call_lua("CountTracks", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to get track count")
    
    track_count = count_result.get("ret", 0)
    if track_index >= track_count:
        raise ValueError(f"Track index {track_index} out of range. Project has {track_count} tracks.")
    
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Delete it
    delete_result = await bridge.call_lua("DeleteTrack", [track_result.get("ret")])
    if not delete_result.get("ok"):
        raise Exception(f"Failed to delete track: {delete_result.get('error', 'Unknown error')}")
    
    return f"Successfully deleted track at index {track_index}"


async def get_master_track() -> str:
    """Get the master track
    
    Returns:
        Master track information
    """
    result = await bridge.call_lua("GetMasterTrack", [0])
    
    if result.get("ok") and result.get("ret"):
        return "Master track found"
    else:
        raise Exception("Failed to get master track")


async def get_track_guid(track_index: int) -> str:
    """Get the GUID of a track
    
    Args:
        track_index: The index of the track (0-based)
        
    Returns:
        Track GUID
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get its GUID
    guid_result = await bridge.call_lua("GetTrackGUID", [track_result.get("ret")])
    if guid_result.get("ok") and guid_result.get("ret"):
        return f"Track GUID: {guid_result.get('ret')}"
    else:
        raise Exception("Failed to get track GUID")


async def get_last_touched_track() -> str:
    """Get the last touched track
    
    Returns:
        Last touched track information
    """
    result = await bridge.call_lua("GetLastTouchedTrack", [])
    
    if result.get("ok") and result.get("ret"):
        # Get track name for better info
        name_result = await bridge.call_lua("GetTrackName", [result.get("ret")])
        if name_result.get("ok") and name_result.get("ret"):
            return f"Last touched track: {name_result.get('ret')}"
        else:
            return "Last touched track found (unnamed)"
    else:
        raise Exception("No track has been touched yet")