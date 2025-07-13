"""
Track Management Tools for REAPER MCP

This module contains all track-related operations including:
- Basic track operations (insert, delete, select)
- Track properties (name, color, mute, solo)
- Track volume and pan controls
- Track recording settings
- Track FX management
- Track sends and routing
- Track automation and envelopes
"""

from typing import Optional, List, Dict, Any, Tuple
from ..bridge import bridge

# Import MCP decorators
from mcp.server.fastmcp import FastMCP

# Get the global MCP instance (will be set by main server)
mcp = None

def set_mcp_instance(instance: FastMCP):
    """Set the MCP instance for this module"""
    global mcp
    mcp = instance

# ============================================================================
# Basic Track Operations
# ============================================================================

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
async def insert_track_at_index(index: int, use_defaults: bool = True) -> str:
    """Insert a track at a specific index
    
    Args:
        index: The index where the track should be inserted
        use_defaults: Whether to use default track settings
        
    Returns:
        Success message
    """
    result = await bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
    
    if result.get("ok"):
        return f"Track inserted at index {index}"
    else:
        raise Exception(f"Failed to insert track at index {index}")

@mcp.tool()
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

@mcp.tool()
async def get_track_from_guid(guid: str) -> str:
    """Get track by GUID
    
    Args:
        guid: The GUID of the track
        
    Returns:
        Track information
    """
    result = await bridge.call_lua("GetTrackByGUID", [guid])
    
    if result.get("ok") and result.get("ret"):
        return f"Found track with GUID: {guid}"
    else:
        raise Exception(f"Track not found with GUID: {guid}")

@mcp.tool()
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

@mcp.tool()
async def count_selected_tracks() -> str:
    """Count the number of selected tracks
    
    Returns:
        Selected track count
    """
    result = await bridge.call_lua("CountSelectedTracks", [0])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"{count} tracks selected"
    else:
        raise Exception("Failed to count selected tracks")

@mcp.tool()
async def get_selected_track(index: int) -> str:
    """Get a selected track by index
    
    Args:
        index: The index in the selection (0-based)
        
    Returns:
        Selected track information
    """
    result = await bridge.call_lua("GetSelectedTrack", [0, index])
    
    if result.get("ok") and result.get("ret"):
        # Get track name
        name_result = await bridge.call_lua("GetTrackName", [result.get("ret")])
        if name_result.get("ok") and name_result.get("ret"):
            return f"Selected track {index}: {name_result.get('ret')}"
        else:
            return f"Selected track {index} found (unnamed)"
    else:
        raise Exception(f"No selected track at index {index}")

@mcp.tool()
async def set_track_selected(track_index: int, selected: bool) -> str:
    """Select or deselect a track
    
    Args:
        track_index: The index of the track (0-based)
        selected: True to select, False to deselect
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set selection
    result = await bridge.call_lua("SetTrackSelected", [track_result.get("ret"), selected])
    if result.get("ok"):
        return f"Track {track_index} {'selected' if selected else 'deselected'}"
    else:
        raise Exception("Failed to set track selection")

@mcp.tool()
async def set_only_track_selected(track_index: int) -> str:
    """Set only one track selected, deselecting all others
    
    Args:
        track_index: The index of the track to select (0-based)
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set as only selected
    result = await bridge.call_lua("SetOnlyTrackSelected", [track_result.get("ret")])
    if result.get("ok"):
        return f"Track {track_index} is now the only selected track"
    else:
        raise Exception("Failed to set track as only selected")

# ============================================================================
# Track Properties
# ============================================================================

@mcp.tool()
async def get_track_name(track_index: int) -> str:
    """Get the name of a track by index (0-based)
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        
    Returns:
        Track name
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get its name
    name_result = await bridge.call_lua("GetTrackName", [track_result.get("ret")])
    if name_result.get("ok"):
        name = name_result.get("ret", "")
        if name:
            return f"Track {track_index} name: {name}"
        else:
            return f"Track {track_index} has no name"
    else:
        raise Exception("Failed to get track name")

@mcp.tool()
async def set_track_name(track_index: int, name: str) -> str:
    """Set the name of a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        name: The new name for the track
        
    Returns:
        Success message
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set its name
    set_result = await bridge.call_lua("GetSetMediaTrackInfo_String", 
                                     [track_result.get("ret"), "P_NAME", name, True])
    if set_result.get("ok"):
        return f"Set track {track_index} name to: {name}"
    else:
        raise Exception("Failed to set track name")

@mcp.tool()
async def get_track_mute(track_index: int) -> str:
    """Get track mute state
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        
    Returns:
        Mute state
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get mute state
    mute_result = await bridge.call_lua("GetMediaTrackInfo_Value", 
                                      [track_result.get("ret"), "B_MUTE"])
    if mute_result.get("ok"):
        is_muted = bool(mute_result.get("ret", 0))
        return f"Track {track_index} is {'muted' if is_muted else 'not muted'}"
    else:
        raise Exception("Failed to get track mute state")

@mcp.tool()
async def set_track_mute(track_index: int, mute: bool) -> str:
    """Set track mute state
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        mute: True to mute, False to unmute
        
    Returns:
        Success message
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set mute state
    mute_result = await bridge.call_lua("SetMediaTrackInfo_Value",
                                      [track_result.get("ret"), "B_MUTE", 1 if mute else 0])
    if mute_result.get("ok"):
        return f"Track {track_index} {'muted' if mute else 'unmuted'}"
    else:
        raise Exception("Failed to set track mute state")

@mcp.tool()
async def get_track_solo(track_index: int) -> str:
    """Get track solo state
    
    Args:
        track_index: The index of the track (0-based)
        
    Returns:
        Solo state
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get solo state
    solo_result = await bridge.call_lua("GetMediaTrackInfo_Value",
                                      [track_result.get("ret"), "I_SOLO"])
    if solo_result.get("ok"):
        solo_state = int(solo_result.get("ret", 0))
        if solo_state == 0:
            return f"Track {track_index} is not soloed"
        elif solo_state == 1:
            return f"Track {track_index} is soloed"
        elif solo_state == 2:
            return f"Track {track_index} is soloed in place"
        else:
            return f"Track {track_index} solo state: {solo_state}"
    else:
        raise Exception("Failed to get track solo state")

@mcp.tool()
async def set_track_solo(track_index: int, solo: int) -> str:
    """Set track solo state
    
    Args:
        track_index: The index of the track (0-based)
        solo: Solo state (0=not soloed, 1=soloed, 2=soloed in place)
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set solo state
    solo_result = await bridge.call_lua("SetMediaTrackInfo_Value",
                                      [track_result.get("ret"), "I_SOLO", solo])
    if solo_result.get("ok"):
        if solo == 0:
            return f"Track {track_index} unsoloed"
        elif solo == 1:
            return f"Track {track_index} soloed"
        elif solo == 2:
            return f"Track {track_index} soloed in place"
        else:
            return f"Track {track_index} solo state set to {solo}"
    else:
        raise Exception("Failed to set track solo state")

@mcp.tool()
async def get_track_color(track_index: int) -> str:
    """Get the color of a track
    
    Args:
        track_index: The index of the track (0-based)
        
    Returns:
        Track color in RGB format
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get color
    color_result = await bridge.call_lua("GetTrackColor", [track_result.get("ret")])
    if color_result.get("ok"):
        color = color_result.get("ret", 0)
        if color == 0:
            return f"Track {track_index} has no custom color"
        else:
            # Convert to RGB
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            return f"Track {track_index} color: RGB({r}, {g}, {b})"
    else:
        raise Exception("Failed to get track color")

@mcp.tool()
async def set_track_color(track_index: int, r: int, g: int, b: int) -> str:
    """Set the color of a track
    
    Args:
        track_index: The index of the track (0-based)
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        
    Returns:
        Success message
    """
    # Validate color values
    if not all(0 <= c <= 255 for c in [r, g, b]):
        raise ValueError("Color values must be between 0 and 255")
    
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Convert RGB to color integer
    color = (r << 16) | (g << 8) | b | 0x01000000  # Include alpha flag
    
    # Set color
    color_result = await bridge.call_lua("SetTrackColor", [track_result.get("ret"), color])
    if color_result.get("ok"):
        return f"Set track {track_index} color to RGB({r}, {g}, {b})"
    else:
        raise Exception("Failed to set track color")

@mcp.tool()
async def is_track_visible(track_index: int, mixer: bool) -> str:
    """Check if a track is visible in TCP or MCP
    
    Args:
        track_index: The index of the track (0-based)
        mixer: True to check mixer (MCP), False to check track panel (TCP)
        
    Returns:
        Visibility status
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Check visibility
    result = await bridge.call_lua("IsTrackVisible", [track_result.get("ret"), mixer])
    if result.get("ok"):
        is_visible = result.get("ret", False)
        location = "mixer (MCP)" if mixer else "track panel (TCP)"
        return f"Track {track_index} is {'visible' if is_visible else 'not visible'} in {location}"
    else:
        raise Exception("Failed to check track visibility")

@mcp.tool()
async def any_track_solo() -> str:
    """Check if any track is soloed
    
    Returns:
        Solo status
    """
    result = await bridge.call_lua("AnyTrackSolo", [0])
    
    if result.get("ok"):
        any_solo = result.get("ret", 0)
        if any_solo & 1:
            return "At least one track is soloed"
        elif any_solo & 2:
            return "At least one track is soloed in place"
        else:
            return "No tracks are soloed"
    else:
        raise Exception("Failed to check solo status")

# ============================================================================
# Track Volume & Pan
# ============================================================================

@mcp.tool()
async def get_track_volume(track_index: int) -> str:
    """Get track volume in dB
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        
    Returns:
        Volume in dB
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get volume
    vol_result = await bridge.call_lua("GetMediaTrackInfo_Value",
                                     [track_result.get("ret"), "D_VOL"])
    if vol_result.get("ok") and vol_result.get("ret") is not None:
        vol_linear = vol_result.get("ret")
        # Convert to dB
        if vol_linear > 0:
            import math
            vol_db = 20 * math.log10(vol_linear)
            return f"Track {track_index} volume: {vol_db:.2f} dB"
        else:
            return f"Track {track_index} volume: -inf dB (muted)"
    else:
        raise Exception("Failed to get track volume")

@mcp.tool()
async def set_track_volume(track_index: int, volume_db: float) -> str:
    """Set track volume in dB
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        volume_db: Volume in dB
        
    Returns:
        Success message
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Convert dB to linear
    import math
    vol_linear = 10 ** (volume_db / 20)
    
    # Set volume
    vol_result = await bridge.call_lua("SetMediaTrackInfo_Value",
                                     [track_result.get("ret"), "D_VOL", vol_linear])
    if vol_result.get("ok"):
        return f"Set track {track_index} volume to {volume_db:.2f} dB"
    else:
        raise Exception("Failed to set track volume")

@mcp.tool()
async def get_track_volume_db(track_index: int) -> str:
    """Get track volume in dB
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        
    Returns:
        Volume in dB
    """
    return await get_track_volume(track_index)

@mcp.tool()
async def set_track_volume_db(track_index: int, volume_db: float) -> str:
    """Set track volume in dB
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        volume_db: Volume in dB
        
    Returns:
        Success message
    """
    return await set_track_volume(track_index, volume_db)

@mcp.tool()
async def get_track_pan(track_index: int) -> str:
    """Get track pan position (-1.0 to 1.0)
    
    Args:
        track_index: The index of the track (0-based)
        
    Returns:
        Pan position
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get pan
    pan_result = await bridge.call_lua("GetMediaTrackInfo_Value",
                                     [track_result.get("ret"), "D_PAN"])
    if pan_result.get("ok") and pan_result.get("ret") is not None:
        pan = pan_result.get("ret")
        if pan < 0:
            percent = int(abs(pan) * 100)
            return f"Track {track_index} pan: {percent}% left"
        elif pan > 0:
            percent = int(pan * 100)
            return f"Track {track_index} pan: {percent}% right"
        else:
            return f"Track {track_index} pan: center"
    else:
        raise Exception("Failed to get track pan")

@mcp.tool()
async def set_track_pan(track_index: int, pan: float) -> str:
    """Set track pan position (-1.0 to 1.0)
    
    Args:
        track_index: The index of the track (0-based)
        pan: Pan position (-1.0 = full left, 0.0 = center, 1.0 = full right)
        
    Returns:
        Success message
    """
    # Validate pan value
    if not -1.0 <= pan <= 1.0:
        raise ValueError("Pan value must be between -1.0 and 1.0")
    
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set pan
    pan_result = await bridge.call_lua("SetMediaTrackInfo_Value",
                                     [track_result.get("ret"), "D_PAN", pan])
    if pan_result.get("ok"):
        if pan < 0:
            percent = int(abs(pan) * 100)
            return f"Set track {track_index} pan to {percent}% left"
        elif pan > 0:
            percent = int(pan * 100)
            return f"Set track {track_index} pan to {percent}% right"
        else:
            return f"Set track {track_index} pan to center"
    else:
        raise Exception("Failed to set track pan")

# ============================================================================
# Track Recording
# ============================================================================

@mcp.tool()
async def get_track_record_mode(track_index: int) -> str:
    """Get track record mode
    
    Args:
        track_index: The index of the track (0-based)
        
    Returns:
        Record mode
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get record mode
    mode_result = await bridge.call_lua("GetMediaTrackInfo_Value",
                                      [track_result.get("ret"), "I_RECMODE"])
    if mode_result.get("ok"):
        mode = int(mode_result.get("ret", 0))
        mode_names = {
            0: "Input",
            1: "Stereo out",
            2: "None",
            3: "Stereo out with latency compensation",
            4: "MIDI output",
            5: "Mono out",
            6: "Mono out with latency compensation",
            7: "MIDI overdub",
            8: "MIDI replace"
        }
        mode_name = mode_names.get(mode, f"Unknown mode {mode}")
        return f"Track {track_index} record mode: {mode_name}"
    else:
        raise Exception("Failed to get track record mode")

@mcp.tool()
async def set_track_record_mode(track_index: int, mode: int) -> str:
    """Set track record mode
    
    Args:
        track_index: The index of the track (0-based)
        mode: Record mode (0=input, 1=stereo out, 2=none, 3=stereo out w/latency comp, 4=midi output, 5=mono out, 6=mono out w/latency comp, 7=midi overdub, 8=midi replace)
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set record mode
    mode_result = await bridge.call_lua("SetMediaTrackInfo_Value",
                                      [track_result.get("ret"), "I_RECMODE", mode])
    if mode_result.get("ok"):
        mode_names = {
            0: "Input",
            1: "Stereo out",
            2: "None",
            3: "Stereo out with latency compensation",
            4: "MIDI output",
            5: "Mono out",
            6: "Mono out with latency compensation",
            7: "MIDI overdub",
            8: "MIDI replace"
        }
        mode_name = mode_names.get(mode, f"mode {mode}")
        return f"Set track {track_index} record mode to: {mode_name}"
    else:
        raise Exception("Failed to set track record mode")

@mcp.tool()
async def get_track_record_input(track_index: int) -> str:
    """Get track record input
    
    Args:
        track_index: The index of the track (0-based)
        
    Returns:
        Record input
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get record input
    input_result = await bridge.call_lua("GetMediaTrackInfo_Value",
                                       [track_result.get("ret"), "I_RECINPUT"])
    if input_result.get("ok"):
        input_index = int(input_result.get("ret", -1))
        if input_index < 0:
            return f"Track {track_index} record input: None"
        elif input_index < 512:
            return f"Track {track_index} record input: Input {input_index + 1}"
        elif input_index < 1024:
            return f"Track {track_index} record input: Stereo input {(input_index - 512) // 2 + 1}"
        elif input_index == 1024:
            return f"Track {track_index} record input: None (MIDI)"
        elif input_index < 1024 + 512:
            return f"Track {track_index} record input: MIDI input {input_index - 1024 + 1}"
        else:
            return f"Track {track_index} record input: Virtual MIDI keyboard"
    else:
        raise Exception("Failed to get track record input")

@mcp.tool()
async def set_track_record_input(track_index: int, input_index: int) -> str:
    """Set track record input
    
    Args:
        track_index: The index of the track (0-based)
        input_index: Input index (-1=none, 0-511=audio inputs, 512-1023=stereo pairs, 1024+=MIDI)
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set record input
    input_result = await bridge.call_lua("SetMediaTrackInfo_Value",
                                       [track_result.get("ret"), "I_RECINPUT", input_index])
    if input_result.get("ok"):
        return f"Set track {track_index} record input to index {input_index}"
    else:
        raise Exception("Failed to set track record input")

@mcp.tool()
async def get_track_record_arm(track_index: int) -> str:
    """Get track record arm state
    
    Args:
        track_index: The index of the track (0-based)
        
    Returns:
        Record arm state
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get record arm
    arm_result = await bridge.call_lua("GetMediaTrackInfo_Value",
                                     [track_result.get("ret"), "I_RECARM"])
    if arm_result.get("ok"):
        is_armed = bool(arm_result.get("ret", 0))
        return f"Track {track_index} is {'armed for recording' if is_armed else 'not armed'}"
    else:
        raise Exception("Failed to get track record arm state")

@mcp.tool()
async def set_track_record_arm(track_index: int, arm: bool) -> str:
    """Set track record arm state
    
    Args:
        track_index: The index of the track (0-based)
        arm: True to arm, False to disarm
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set record arm
    arm_result = await bridge.call_lua("SetMediaTrackInfo_Value",
                                     [track_result.get("ret"), "I_RECARM", 1 if arm else 0])
    if arm_result.get("ok"):
        return f"Track {track_index} {'armed for recording' if arm else 'disarmed'}"
    else:
        raise Exception("Failed to set track record arm state")

# ============================================================================
# Track FX
# ============================================================================

@mcp.tool()
async def track_fx_get_count(track_index: int) -> str:
    """Get the number of FX on a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        
    Returns:
        FX count
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get FX count
    count_result = await bridge.call_lua("TrackFX_GetCount", [track_result.get("ret")])
    if count_result.get("ok"):
        count = count_result.get("ret", 0)
        return f"Track {track_index} has {count} FX"
    else:
        raise Exception("Failed to get FX count")

@mcp.tool()
async def track_fx_add_by_name(track_index: int, fx_name: str, instantiate: int = 1) -> str:
    """Add an FX to a track by name
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        fx_name: Name of the FX to add
        instantiate: How to add FX (-1=default, 0=no instant, 1=instant, 1001+=as send)
        
    Returns:
        Success message with FX index
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Add FX
    add_result = await bridge.call_lua("TrackFX_AddByName",
                                     [track_result.get("ret"), fx_name, False, instantiate])
    if add_result.get("ok"):
        fx_index = add_result.get("ret", -1)
        if fx_index >= 0:
            return f"Added FX '{fx_name}' to track {track_index} at index {fx_index}"
        else:
            raise Exception(f"Failed to add FX '{fx_name}'")
    else:
        raise Exception("Failed to add FX")

@mcp.tool()
async def track_fx_delete(track_index: int, fx_index: int) -> str:
    """Delete an FX from a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        fx_index: The index of the FX to delete (0-based)
        
    Returns:
        Success message
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Delete FX
    delete_result = await bridge.call_lua("TrackFX_Delete",
                                        [track_result.get("ret"), fx_index])
    if delete_result.get("ok"):
        return f"Deleted FX at index {fx_index} from track {track_index}"
    else:
        raise Exception("Failed to delete FX")

@mcp.tool()
async def track_fx_get_enabled(track_index: int, fx_index: int) -> str:
    """Get whether an FX is enabled
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        fx_index: The index of the FX (0-based)
        
    Returns:
        Enabled state
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get enabled state
    enabled_result = await bridge.call_lua("TrackFX_GetEnabled",
                                         [track_result.get("ret"), fx_index])
    if enabled_result.get("ok"):
        is_enabled = enabled_result.get("ret", False)
        return f"FX {fx_index} on track {track_index} is {'enabled' if is_enabled else 'disabled'}"
    else:
        raise Exception("Failed to get FX enabled state")

@mcp.tool()
async def track_fx_set_enabled(track_index: int, fx_index: int, enabled: bool) -> str:
    """Enable or disable an FX
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        fx_index: The index of the FX (0-based)
        enabled: True to enable, False to disable
        
    Returns:
        Success message
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set enabled state
    enabled_result = await bridge.call_lua("TrackFX_SetEnabled",
                                         [track_result.get("ret"), fx_index, enabled])
    if enabled_result.get("ok"):
        return f"FX {fx_index} on track {track_index} {'enabled' if enabled else 'disabled'}"
    else:
        raise Exception("Failed to set FX enabled state")

@mcp.tool()
async def track_fx_get_name(track_index: int, fx_index: int) -> str:
    """Get the name of an FX on a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        fx_index: The index of the FX (0-based)
        
    Returns:
        FX name
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get FX name
    name_result = await bridge.call_lua("TrackFX_GetFXName",
                                      [track_result.get("ret"), fx_index])
    if name_result.get("ok") and name_result.get("ret"):
        return f"FX {fx_index} on track {track_index}: {name_result.get('ret')}"
    else:
        raise Exception("Failed to get FX name")

# ============================================================================
# Track Sends & Routing
# ============================================================================

@mcp.tool()
async def create_track_send(src_track_index: int, dest_track_index: int) -> str:
    """Create a send from one track to another
    
    Args:
        src_track_index: Source track index (0-based)
        dest_track_index: Destination track index (0-based)
        
    Returns:
        Success message with send index
    """
    # Get source track
    src_result = await bridge.call_lua("GetTrack", [0, src_track_index])
    if not src_result.get("ok") or not src_result.get("ret"):
        raise Exception(f"Failed to find source track at index {src_track_index}")
    
    # Get destination track
    dest_result = await bridge.call_lua("GetTrack", [0, dest_track_index])
    if not dest_result.get("ok") or not dest_result.get("ret"):
        raise Exception(f"Failed to find destination track at index {dest_track_index}")
    
    # Create send
    send_result = await bridge.call_lua("CreateTrackSend",
                                      [src_result.get("ret"), dest_result.get("ret")])
    if send_result.get("ok"):
        send_index = send_result.get("ret", -1)
        if send_index >= 0:
            return f"Created send from track {src_track_index} to track {dest_track_index} (send index: {send_index})"
        else:
            raise Exception("Failed to create send")
    else:
        raise Exception("Failed to create track send")

@mcp.tool()
async def remove_track_send(track_index: int, send_index: int) -> str:
    """Remove a send from a track
    
    Args:
        track_index: The index of the track (0-based)
        send_index: The index of the send to remove (0-based)
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Remove send
    remove_result = await bridge.call_lua("RemoveTrackSend",
                                        [track_result.get("ret"), 0, send_index])
    if remove_result.get("ok"):
        return f"Removed send {send_index} from track {track_index}"
    else:
        raise Exception("Failed to remove send")

@mcp.tool()
async def get_track_num_sends(track_index: int, category: int = 0) -> str:
    """Get the number of sends on a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        category: Send category (0=sends, -1=receives, 3=hardware outputs)
        
    Returns:
        Send count
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get send count
    count_result = await bridge.call_lua("GetTrackNumSends",
                                       [track_result.get("ret"), category])
    if count_result.get("ok"):
        count = count_result.get("ret", 0)
        category_name = {0: "sends", -1: "receives", 3: "hardware outputs"}.get(category, "sends")
        return f"Track {track_index} has {count} {category_name}"
    else:
        raise Exception("Failed to get send count")

@mcp.tool()
async def set_track_send_volume(track_index: int, send_index: int, volume_db: float) -> str:
    """Set the volume of a track send
    
    Args:
        track_index: The index of the track with the send (0-based)
        send_index: The index of the send (0-based)
        volume_db: Volume in dB
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Convert dB to linear
    import math
    vol_linear = 10 ** (volume_db / 20)
    
    # Set send volume
    vol_result = await bridge.call_lua("SetTrackSendInfo_Value",
                                     [track_result.get("ret"), 0, send_index, "D_VOL", vol_linear])
    if vol_result.get("ok"):
        return f"Set send {send_index} volume to {volume_db:.2f} dB on track {track_index}"
    else:
        raise Exception("Failed to set send volume")

@mcp.tool()
async def get_track_send_info(track_index: int, send_index: int) -> str:
    """Get information about a track send
    
    Args:
        track_index: The index of the track (0-based)
        send_index: The index of the send (0-based)
        
    Returns:
        Send information
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get destination track
    dest_result = await bridge.call_lua("GetTrackSendInfo_Value",
                                      [track_result.get("ret"), 0, send_index, "P_DESTTRACK"])
    if not dest_result.get("ok") or not dest_result.get("ret"):
        raise Exception("Failed to get send destination")
    
    # Get destination track name
    name_result = await bridge.call_lua("GetTrackName", [dest_result.get("ret")])
    dest_name = name_result.get("ret", "Unknown") if name_result.get("ok") else "Unknown"
    
    # Get send volume
    vol_result = await bridge.call_lua("GetTrackSendInfo_Value",
                                     [track_result.get("ret"), 0, send_index, "D_VOL"])
    if vol_result.get("ok") and vol_result.get("ret") is not None:
        vol_linear = vol_result.get("ret")
        if vol_linear > 0:
            import math
            vol_db = 20 * math.log10(vol_linear)
            vol_str = f"{vol_db:.2f} dB"
        else:
            vol_str = "-inf dB"
    else:
        vol_str = "Unknown"
    
    return f"Send {send_index} from track {track_index} to '{dest_name}' at {vol_str}"

@mcp.tool()
async def get_track_receive_count(track_index: int) -> str:
    """Get the number of receives on a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        
    Returns:
        Receive count
    """
    return await get_track_num_sends(track_index, -1)

@mcp.tool()
async def get_track_receive_info(track_index: int, receive_index: int) -> str:
    """Get information about a track receive
    
    Args:
        track_index: The index of the track (0-based)
        receive_index: The index of the receive (0-based)
        
    Returns:
        Receive information
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get source track
    src_result = await bridge.call_lua("GetTrackSendInfo_Value",
                                     [track_result.get("ret"), -1, receive_index, "P_SRCTRACK"])
    if not src_result.get("ok") or not src_result.get("ret"):
        raise Exception("Failed to get receive source")
    
    # Get source track name
    name_result = await bridge.call_lua("GetTrackName", [src_result.get("ret")])
    src_name = name_result.get("ret", "Unknown") if name_result.get("ok") else "Unknown"
    
    return f"Receive {receive_index} on track {track_index} from '{src_name}'"

# ============================================================================
# Track Automation & Envelopes
# ============================================================================

@mcp.tool()
async def get_track_automation_mode(track_index: int) -> str:
    """Get the automation mode for a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        
    Returns:
        Automation mode
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get automation mode
    mode_result = await bridge.call_lua("GetTrackAutomationMode", [track_result.get("ret")])
    if mode_result.get("ok"):
        mode = mode_result.get("ret", 0)
        mode_names = {
            0: "Trim/Read",
            1: "Read",
            2: "Touch",
            3: "Write",
            4: "Latch"
        }
        mode_name = mode_names.get(mode, f"Unknown mode {mode}")
        return f"Track {track_index} automation mode: {mode_name}"
    else:
        raise Exception("Failed to get automation mode")

@mcp.tool()
async def set_track_automation_mode(track_index: int, mode: int) -> str:
    """Set the automation mode for a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        mode: Automation mode (0=trim/read, 1=read, 2=touch, 3=write, 4=latch)
        
    Returns:
        Success message
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set automation mode
    mode_result = await bridge.call_lua("SetTrackAutomationMode",
                                      [track_result.get("ret"), mode])
    if mode_result.get("ok"):
        mode_names = {
            0: "Trim/Read",
            1: "Read",
            2: "Touch",
            3: "Write",
            4: "Latch"
        }
        mode_name = mode_names.get(mode, f"mode {mode}")
        return f"Set track {track_index} automation mode to: {mode_name}"
    else:
        raise Exception("Failed to set automation mode")

@mcp.tool()
async def get_track_envelope_by_name(track_index: int, envelope_name: str) -> str:
    """Get a track envelope by name (e.g., 'Volume', 'Pan', 'Mute')
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        envelope_name: Name of the envelope to find
        
    Returns:
        Envelope information
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelopeByName",
                                     [track_result.get("ret"), envelope_name])
    if env_result.get("ok") and env_result.get("ret"):
        return f"Found envelope '{envelope_name}' on track {track_index}"
    else:
        raise Exception(f"Envelope '{envelope_name}' not found on track {track_index}")

# ============================================================================
# Track Media Items
# ============================================================================

@mcp.tool()
async def add_media_item_to_track(track_index: int, position: float = 0.0, length: float = 1.0) -> str:
    """Add a new media item to a track
    
    Args:
        track_index: The index of the track (0-based)
        position: Position in seconds where the item should be added
        length: Length of the item in seconds
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Add media item
    item_result = await bridge.call_lua("AddMediaItemToTrack", [track_result.get("ret")])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception("Failed to add media item")
    
    # Set position and length
    pos_result = await bridge.call_lua("SetMediaItemInfo_Value",
                                     [item_result.get("ret"), "D_POSITION", position])
    len_result = await bridge.call_lua("SetMediaItemInfo_Value",
                                     [item_result.get("ret"), "D_LENGTH", length])
    
    if pos_result.get("ok") and len_result.get("ok"):
        return f"Added media item to track {track_index} at {position}s, length {length}s"
    else:
        return f"Added media item to track {track_index} (position/length may not be set)"

@mcp.tool()
async def delete_track_media_item(track_index: int, item_index: int) -> str:
    """Delete a media item from track
    
    Args:
        track_index: The index of the track (0-based)
        item_index: The index of the item on the track (0-based)
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get the media item
    item_result = await bridge.call_lua("GetTrackMediaItem", [track_result.get("ret"), item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"No media item at index {item_index} on track {track_index}")
    
    # Delete it
    delete_result = await bridge.call_lua("DeleteTrackMediaItem",
                                        [track_result.get("ret"), item_result.get("ret")])
    if delete_result.get("ok"):
        return f"Deleted media item {item_index} from track {track_index}"
    else:
        raise Exception("Failed to delete media item")

@mcp.tool()
async def get_media_item_take_track(take_index: int) -> str:
    """Get the track of a media item take
    
    Args:
        take_index: Global take index in the project
        
    Returns:
        Track information
    """
    # Get the take
    take_result = await bridge.call_lua("GetTake", [0, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    # Get its track
    track_result = await bridge.call_lua("GetMediaItemTake_Track", [take_result.get("ret")])
    if track_result.get("ok") and track_result.get("ret"):
        # Get track name
        name_result = await bridge.call_lua("GetTrackName", [track_result.get("ret")])
        if name_result.get("ok") and name_result.get("ret"):
            return f"Take {take_index} is on track: {name_result.get('ret')}"
        else:
            return f"Take {take_index} is on an unnamed track"
    else:
        raise Exception("Failed to get take's track")

# ============================================================================
# Track Analysis & Monitoring
# ============================================================================

@mcp.tool()
async def get_track_peak(track_index: int, channel: int = 0) -> str:
    """Get the current peak level of a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        channel: Channel to get peak for (0=left/mono, 1=right)
        
    Returns:
        Peak level in dB
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get peak
    peak_result = await bridge.call_lua("Track_GetPeakInfo", [track_result.get("ret"), channel])
    if peak_result.get("ok") and peak_result.get("ret") is not None:
        peak = peak_result.get("ret")
        if peak > 0:
            import math
            peak_db = 20 * math.log10(peak)
            return f"Track {track_index} channel {channel} peak: {peak_db:.2f} dB"
        else:
            return f"Track {track_index} channel {channel} peak: -inf dB"
    else:
        raise Exception("Failed to get track peak")

@mcp.tool()
async def get_track_peak_info(track_index: int) -> str:
    """Get detailed peak information for a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        
    Returns:
        Peak information for all channels
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get peak for both channels
    left_result = await bridge.call_lua("Track_GetPeakInfo", [track_result.get("ret"), 0])
    right_result = await bridge.call_lua("Track_GetPeakInfo", [track_result.get("ret"), 1])
    
    results = []
    
    if left_result.get("ok") and left_result.get("ret") is not None:
        peak = left_result.get("ret")
        if peak > 0:
            import math
            peak_db = 20 * math.log10(peak)
            results.append(f"Left: {peak_db:.2f} dB")
        else:
            results.append("Left: -inf dB")
    
    if right_result.get("ok") and right_result.get("ret") is not None:
        peak = right_result.get("ret")
        if peak > 0:
            import math
            peak_db = 20 * math.log10(peak)
            results.append(f"Right: {peak_db:.2f} dB")
        else:
            results.append("Right: -inf dB")
    
    if results:
        return f"Track {track_index} peaks - " + ", ".join(results)
    else:
        raise Exception("Failed to get track peak info")

# ============================================================================
# Track Advanced Operations
# ============================================================================

@mcp.tool()
async def freeze_track(track_index: int) -> str:
    """Freeze a track
    
    Args:
        track_index: The index of the track to freeze (0-based)
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Freeze track
    result = await bridge.call_lua("Main_OnCommand", [41223, 0])  # Track: Freeze to stereo
    if result.get("ok"):
        return f"Track {track_index} frozen"
    else:
        raise Exception("Failed to freeze track")

@mcp.tool()
async def unfreeze_track(track_index: int) -> str:
    """Unfreeze a track
    
    Args:
        track_index: The index of the track to unfreeze (0-based)
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Unfreeze track
    result = await bridge.call_lua("Main_OnCommand", [41644, 0])  # Track: Unfreeze
    if result.get("ok"):
        return f"Track {track_index} unfrozen"
    else:
        raise Exception("Failed to unfreeze track")

@mcp.tool()
async def bounce_tracks(output_track_name: str = "Bounced") -> str:
    """Bounce selected tracks to a new track
    
    Args:
        output_track_name: Name for the bounced track
        
    Returns:
        Success message
    """
    # Check if any tracks are selected
    count_result = await bridge.call_lua("CountSelectedTracks", [0])
    if not count_result.get("ok") or count_result.get("ret", 0) == 0:
        raise Exception("No tracks selected for bouncing")
    
    # Bounce tracks
    result = await bridge.call_lua("Main_OnCommand", [40716, 0])  # Track: Bounce tracks to new track
    if result.get("ok"):
        # Set name of new track (it should be the last track)
        count_result = await bridge.call_lua("CountTracks", [0])
        if count_result.get("ok"):
            last_index = count_result.get("ret", 1) - 1
            await set_track_name(last_index, output_track_name)
        return f"Bounced selected tracks to new track '{output_track_name}'"
    else:
        raise Exception("Failed to bounce tracks")

@mcp.tool()
async def add_video_to_track(track_index: int, video_file: str) -> str:
    """Add a video file to a track
    
    Args:
        track_index: The index of the track (0-based)
        video_file: Path to the video file
        
    Returns:
        Success message
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Insert media file
    result = await bridge.call_lua("InsertMedia", [video_file, 3])  # 3 = add to selected track
    if result.get("ok"):
        return f"Added video '{video_file}' to track {track_index}"
    else:
        raise Exception(f"Failed to add video file: {result.get('error', 'Unknown error')}")

@mcp.tool()
async def get_track_state_chunk(track_index: int, is_undo: bool = False) -> str:
    """Get the state chunk of a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        is_undo: Whether this is for undo purposes
        
    Returns:
        Track state chunk
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get state chunk
    chunk_result = await bridge.call_lua("GetTrackStateChunk",
                                       [track_result.get("ret"), "", is_undo])
    if chunk_result.get("ok") and chunk_result.get("ret"):
        chunk = chunk_result.get("ret")
        # Return just first 200 chars for brevity
        if len(chunk) > 200:
            return f"Track {track_index} state chunk (truncated): {chunk[:200]}..."
        else:
            return f"Track {track_index} state chunk: {chunk}"
    else:
        raise Exception("Failed to get track state chunk")

@mcp.tool()
async def set_track_state_chunk(track_index: int, chunk: str, is_undo: bool = False) -> str:
    """Set the state chunk of a track
    
    Args:
        track_index: The index of the track (0-based, or -1 for master track)
        chunk: The state chunk to set
        is_undo: Whether this is for undo purposes
        
    Returns:
        Success message
    """
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set state chunk
    chunk_result = await bridge.call_lua("SetTrackStateChunk",
                                       [track_result.get("ret"), chunk, is_undo])
    if chunk_result.get("ok"):
        return f"Set state chunk for track {track_index}"
    else:
        raise Exception("Failed to set track state chunk")

@mcp.tool()
async def get_track_midi_note_name(track_index: int, note: int, channel: int = 0) -> str:
    """Get MIDI note name for a track
    
    Args:
        track_index: The index of the track (0-based)
        note: MIDI note number (0-127)
        channel: MIDI channel (0-15)
        
    Returns:
        Note name
    """
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get note name
    name_result = await bridge.call_lua("GetTrackMIDINoteName",
                                      [track_result.get("ret"), note, channel])
    if name_result.get("ok") and name_result.get("ret"):
        return f"Note {note} on channel {channel}: {name_result.get('ret')}"
    else:
        # Return standard note name if no custom name
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octave = (note // 12) - 1
        note_name = note_names[note % 12]
        return f"Note {note} on channel {channel}: {note_name}{octave}"