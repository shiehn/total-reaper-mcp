"""
Track Management Extended Tools for REAPER MCP

This module contains extended tools for track management including
track information, control surface operations, and mixer control.
"""

from typing import Optional, Tuple, List, Any, Dict
from ..bridge import bridge


# ============================================================================
# Track Information Extended (6 tools)
# ============================================================================

async def get_set_media_track_info_string(track_index: int, param_name: str, 
                                        value: str = "", set_value: bool = False) -> str:
    """Get or set track string parameter"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get/set info string
    result = await bridge.call_lua("GetSetMediaTrackInfo_String", [track_handle, param_name, value, set_value])
    
    if result.get("ok"):
        ret_value = result.get("ret", "")
        if set_value:
            return f"Set track {param_name} to: {value}"
        else:
            return f"Track {param_name}: {ret_value}"
    else:
        raise Exception(f"Failed to get/set track info string: {result.get('error', 'Unknown error')}")


async def get_track_envelope_by_name(track_index: int, envelope_name: str) -> str:
    """Get track envelope by name"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope by name
    result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
    
    if result.get("ok"):
        envelope = result.get("ret")
        if envelope:
            return f"Found envelope '{envelope_name}' on track {track_index}"
        else:
            return f"No envelope named '{envelope_name}' found on track {track_index}"
    else:
        raise Exception(f"Failed to get envelope by name: {result.get('error', 'Unknown error')}")


async def get_track_midi_lyrics(track_index: int) -> str:
    """Get track MIDI lyrics"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get MIDI lyrics
    result = await bridge.call_lua("GetTrackMIDILyrics", [track_handle, 0, "", 65536])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            success, lyrics = ret[:2]
            if success and lyrics:
                preview = lyrics[:200] + "..." if len(lyrics) > 200 else lyrics
                return f"Track MIDI lyrics: {preview}"
            else:
                return "Track has no MIDI lyrics"
        else:
            return "Failed to get MIDI lyrics"
    else:
        raise Exception(f"Failed to get track MIDI lyrics: {result.get('error', 'Unknown error')}")


async def track_list_adjust_windows(resize_behavior: int = 0) -> str:
    """Adjust track list windows"""
    result = await bridge.call_lua("TrackList_AdjustWindows", [resize_behavior])
    
    if result.get("ok"):
        behavior_names = {0: "normal", 1: "no resize", 2: "force resize"}
        behavior_name = behavior_names.get(resize_behavior, f"mode {resize_behavior}")
        return f"Adjusted track list windows ({behavior_name})"
    else:
        raise Exception(f"Failed to adjust track list windows: {result.get('error', 'Unknown error')}")


async def track_list_update_all_external_surfaces() -> str:
    """Update all external control surfaces"""
    result = await bridge.call_lua("TrackList_UpdateAllExternalSurfaces", [])
    
    if result.get("ok"):
        return "Updated all external control surfaces"
    else:
        raise Exception(f"Failed to update external surfaces: {result.get('error', 'Unknown error')}")


async def bypass_fx_all_tracks(bypass: bool = True) -> str:
    """Bypass FX on all tracks"""
    result = await bridge.call_lua("BypassFxAllTracks", [bypass])
    
    if result.get("ok"):
        action = "Bypassed" if bypass else "Un-bypassed"
        return f"{action} FX on all tracks"
    else:
        raise Exception(f"Failed to bypass FX on all tracks: {result.get('error', 'Unknown error')}")


# ============================================================================
# Control Surface Track Operations (4 tools)
# ============================================================================

async def csurf_num_tracks(include_master: bool = True) -> str:
    """Get number of tracks for control surface"""
    result = await bridge.call_lua("CSurf_NumTracks", [include_master])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        master_str = " (including master)" if include_master else " (excluding master)"
        return f"Control surface track count: {count}{master_str}"
    else:
        raise Exception(f"Failed to get control surface track count: {result.get('error', 'Unknown error')}")


async def csurf_track_from_id(track_id: int, allow_master: bool = True) -> str:
    """Get track from control surface ID"""
    result = await bridge.call_lua("CSurf_TrackFromID", [track_id, allow_master])
    
    if result.get("ok"):
        track = result.get("ret")
        if track:
            # Get track name
            name_result = await bridge.call_lua("GetTrackName", [track, "", 256])
            track_name = name_result.get("ret", "Unnamed") if name_result.get("ok") else "Unknown"
            return f"Control surface track {track_id}: {track_name}"
        else:
            return f"No track found for control surface ID {track_id}"
    else:
        raise Exception(f"Failed to get track from ID: {result.get('error', 'Unknown error')}")


async def csurf_track_to_id(track_index: int, allow_master: bool = True) -> str:
    """Get control surface ID from track"""
    # Get track
    if track_index == -1:  # Master track
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get control surface ID
    result = await bridge.call_lua("CSurf_TrackToID", [track_handle, allow_master])
    
    if result.get("ok"):
        track_id = result.get("ret", 0)
        if track_id > 0:
            return f"Track {track_index} control surface ID: {track_id}"
        else:
            return f"Track {track_index} has no control surface ID"
    else:
        raise Exception(f"Failed to get control surface ID: {result.get('error', 'Unknown error')}")


async def get_mixer_scroll() -> str:
    """Get leftmost track visible in mixer"""
    result = await bridge.call_lua("GetMixerScroll", [])
    
    if result.get("ok"):
        track = result.get("ret")
        if track:
            # Get track index
            idx_result = await bridge.call_lua("CSurf_TrackToID", [track, False])
            track_idx = idx_result.get("ret", 0) if idx_result.get("ok") else 0
            
            # Get track name
            name_result = await bridge.call_lua("GetTrackName", [track, "", 256])
            track_name = name_result.get("ret", "Unnamed") if name_result.get("ok") else "Unknown"
            
            return f"Mixer scroll: Track {track_idx} - {track_name}"
        else:
            return "Mixer scroll: No track visible"
    else:
        raise Exception(f"Failed to get mixer scroll: {result.get('error', 'Unknown error')}")


async def set_mixer_scroll(track_index: int) -> str:
    """Set leftmost track visible in mixer"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set mixer scroll
    result = await bridge.call_lua("SetMixerScroll", [track_handle])
    
    if result.get("ok"):
        track = result.get("ret")
        if track:
            return f"Set mixer scroll to track {track_index}"
        else:
            return f"Failed to set mixer scroll to track {track_index}"
    else:
        raise Exception(f"Failed to set mixer scroll: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_track_management_extended_tools(mcp) -> int:
    """Register all track management extended tools with the MCP instance"""
    tools = [
        # Track Information Extended
        (get_set_media_track_info_string, "Get or set track string parameter"),
        (get_track_envelope_by_name, "Get track envelope by name"),
        (get_track_midi_lyrics, "Get track MIDI lyrics"),
        (track_list_adjust_windows, "Adjust track list windows"),
        (track_list_update_all_external_surfaces, "Update all external control surfaces"),
        (bypass_fx_all_tracks, "Bypass FX on all tracks"),
        
        # Control Surface Track Operations
        (csurf_num_tracks, "Get number of tracks for control surface"),
        (csurf_track_from_id, "Get track from control surface ID"),
        (csurf_track_to_id, "Get control surface ID from track"),
        (get_mixer_scroll, "Get leftmost track visible in mixer"),
        (set_mixer_scroll, "Set leftmost track visible in mixer"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)