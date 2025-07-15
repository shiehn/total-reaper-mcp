"""
Complete Track Management Tools for REAPER MCP

This module contains all 63 track-related operations migrated to the modern pattern.
Organized into logical groups for better maintainability.
"""

from typing import Optional, Tuple
from ..bridge import bridge
import math


# ============================================================================
# Basic Track Operations (13 tools)
# ============================================================================

async def insert_track(index: int, use_defaults: bool = True) -> str:
    """Insert a new track at the specified index (0-based)"""
    result = await bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
    
    if result.get("ok"):
        return f"Successfully inserted track at index {index}"
    else:
        raise Exception(f"Failed to insert track: {result.get('error', 'Unknown error')}")


async def get_track_count() -> str:
    """Get the number of tracks in the current project"""
    result = await bridge.call_lua("CountTracks", [0])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Current project has {count} tracks"
    else:
        raise Exception(f"Failed to get track count: {result.get('error', 'Unknown error')}")


async def get_track(track_index: int) -> str:
    """Get a track by index from the current project"""
    if track_index == -1:
        result = await bridge.call_lua("GetMasterTrack", [0])
    else:
        result = await bridge.call_lua("GetTrack", [0, track_index])
    
    if result.get("ok") and result.get("ret"):
        return f"Found track at index {track_index}"
    else:
        raise Exception(f"Track not found at index {track_index}")


async def delete_track(track_index: int) -> str:
    """Delete a track by index"""
    # Get track count first
    count_result = await bridge.call_lua("CountTracks", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to get track count")
    
    track_count = count_result.get("ret", 0)
    if track_index >= track_count:
        raise ValueError(f"Track index {track_index} out of range. Project has {track_count} tracks.")
    
    # Use DeleteTrackByIndex directly to avoid pointer issues
    delete_result = await bridge.call_lua("DeleteTrackByIndex", [track_index])
    if not delete_result.get("ok"):
        raise Exception(f"Failed to delete track: {delete_result.get('error', 'Unknown error')}")
    
    return f"Successfully deleted track at index {track_index}"


async def get_master_track() -> str:
    """Get the master track"""
    result = await bridge.call_lua("GetMasterTrack", [0])
    
    if result.get("ok") and result.get("ret"):
        return f"Master track: {result.get('ret')}"
    else:
        raise Exception("Failed to get master track")


async def insert_track_at_index(index: int, want_defaults: bool = True) -> str:
    """Insert a track at a specific index (alias for insert_track)"""
    return await insert_track(index, want_defaults)


async def get_track_guid(track_index: int) -> str:
    """Get the GUID of a track"""
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


async def get_track_from_guid(guid: str) -> str:
    """Get track by GUID"""
    result = await bridge.call_lua("GetTrackByGUID", [guid])
    
    if result.get("ok") and result.get("ret"):
        return f"Found track with GUID: {guid}"
    else:
        raise Exception(f"Track not found with GUID: {guid}")


async def get_last_touched_track() -> str:
    """Get the last touched track"""
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


async def count_selected_tracks() -> str:
    """Count the number of selected tracks"""
    result = await bridge.call_lua("CountSelectedTracks", [0])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"{count} selected tracks"
    else:
        raise Exception(f"Failed to count selected tracks: {result.get('error', 'Unknown error')}")


async def get_selected_track(index: int) -> str:
    """Get a selected track by index"""
    result = await bridge.call_lua("GetSelectedTrack", [0, index])
    
    if result.get("ok"):
        track_handle = result.get("ret")
        if track_handle:
            return f"Selected track handle: {track_handle}"
        else:
            return f"No selected track at index {index}"
    else:
        raise Exception(f"Failed to get selected track: {result.get('error', 'Unknown error')}")


async def set_track_selected(track_index: int, selected: bool) -> str:
    """Select or deselect a track"""
    # First get the track pointer
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Then set its selection state
    result = await bridge.call_lua("SetTrackSelected", [track_index, selected])
    
    if result.get("ok"):
        action = "selected" if selected else "deselected"
        return f"Track at index {track_index} has been {action}"
    else:
        raise Exception(f"Failed to set track selection: {result.get('error', 'Unknown error')}")


async def set_only_track_selected(track_index: int) -> str:
    """Set only one track selected, deselecting all others"""
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to get track at index {track_index}")
    
    # Set only this track selected
    result = await bridge.call_lua("SetOnlyTrackSelected", [track_result.get("ret")])
    if result.get("ok"):
        # Update arrange view
        await bridge.call_lua("UpdateArrange", [])
        return f"Track {track_index} is now the only selected track"
    
    raise Exception("Failed to set track selection")


# ============================================================================
# Track Properties (10 tools)
# ============================================================================

async def get_track_name(track_index: int) -> str:
    """Get the name of a track by index (0-based)"""
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


async def set_track_name(track_index: int, name: str) -> str:
    """Set the name of a track"""
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


async def get_track_mute(track_index: int) -> str:
    """Get track mute state"""
    # Pass track index directly - the bridge will handle getting the track
    mute_result = await bridge.call_lua("GetMediaTrackInfo_Value", 
                                      [track_index, "B_MUTE"])
    if mute_result.get("ok"):
        is_muted = bool(mute_result.get("ret", 0))
        return f"Track {track_index} is {'muted' if is_muted else 'not muted'}"
    else:
        raise Exception("Failed to get track mute state")


async def set_track_mute(track_index: int, mute: bool) -> str:
    """Set track mute state"""
    # Pass track index directly - the bridge will handle getting the track
    mute_result = await bridge.call_lua("SetMediaTrackInfo_Value",
                                      [track_index, "B_MUTE", 1 if mute else 0])
    if mute_result.get("ok"):
        return f"Track {track_index} {'muted' if mute else 'unmuted'}"
    else:
        raise Exception("Failed to set track mute state")


async def get_track_solo(track_index: int) -> str:
    """Get track solo state"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_index, "I_SOLO"])
    
    if result.get("ok"):
        solo_state = int(result.get("ret", 0))
        solo_text = "not soloed" if solo_state == 0 else "soloed"
        return f"Track {track_index} solo state: {solo_text}"
    else:
        raise Exception(f"Failed to get track solo state: {result.get('error', 'Unknown error')}")


async def set_track_solo(track_index: int, solo: bool) -> str:
    """Set track solo state"""
    # Pass track index directly - the bridge will handle getting the track
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_index, "I_SOLO", 1 if solo else 0])
    
    if result.get("ok"):
        state = "soloed" if solo else "unsoloed"
        return f"Track {track_index} {state}"
    else:
        raise Exception(f"Failed to set track solo state: {result.get('error', 'Unknown error')}")


async def get_track_color(track_index: int) -> str:
    """Get the color of a track"""
    result = await bridge.call_lua("GetTrackColor", [track_index])
    
    if result.get("ok"):
        color = result.get("result", 0)
        # Extract RGB components
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        return f"Track {track_index} color: RGB({r}, {g}, {b}) (0x{color:06X})"
    else:
        raise Exception(f"Failed to get track color: {result.get('error', 'Unknown error')}")


async def set_track_color(track_index: int, color: int) -> str:
    """Set the color of a track"""
    result = await bridge.call_lua("SetTrackColor", [track_index, color])
    
    if result.get("ok"):
        if color == 0:
            return f"Set track {track_index} color to default"
        else:
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            return f"Set track {track_index} color to RGB({r}, {g}, {b})"
    else:
        raise Exception(f"Failed to set track color: {result.get('error', 'Unknown error')}")


async def is_track_visible(track_index: int, mixer: bool = False) -> str:
    """Check if a track is visible in TCP or MCP"""
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to get track at index {track_index}")
    
    # Check visibility
    result = await bridge.call_lua("IsTrackVisible", [track_result.get("ret"), mixer])
    if result.get("ok"):
        visible = result.get("ret", False)
        location = "mixer" if mixer else "track control panel"
        return f"Track {track_index} is {'visible' if visible else 'not visible'} in {location}"
    
    raise Exception("Failed to check track visibility")


async def any_track_solo(project_index: int = 0) -> str:
    """Check if any track is soloed"""
    result = await bridge.call_lua("AnyTrackSolo", [project_index])
    
    if result.get("ok"):
        is_soloed = result.get("ret", 0)
        return f"Any track soloed: {'Yes' if is_soloed else 'No'}"
    
    raise Exception("Failed to check if any track is soloed")


# ============================================================================
# Track Volume & Pan (6 tools)
# ============================================================================

async def get_track_volume(track_index: int) -> str:
    """Get track volume in dB"""
    # Get track first
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_result.get("ret"), "D_VOL"])
    
    if result.get("ok"):
        vol_linear = result.get("ret", 1.0)
        # Convert to dB
        if vol_linear > 0:
            vol_db = 20 * math.log10(vol_linear)
        else:
            vol_db = -math.inf
        return f"Track {track_index} volume: {vol_db:.2f} dB"
    else:
        raise Exception(f"Failed to get track volume: {result.get('error', 'Unknown error')}")


async def set_track_volume(track_index: int, volume_db: float) -> str:
    """Set track volume in dB"""
    # Get track first
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Convert dB to linear
    if volume_db > -150:
        vol_linear = 10 ** (volume_db / 20)
    else:
        vol_linear = 0
    
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_result.get("ret"), "D_VOL", vol_linear])
    
    if result.get("ok"):
        return f"Track {track_index} volume set to {volume_db:.2f} dB"
    else:
        raise Exception(f"Failed to set track volume: {result.get('error', 'Unknown error')}")


async def get_track_volume_db(track_index: int) -> str:
    """Get track volume in dB (alias)"""
    return await get_track_volume(track_index)


async def set_track_volume_db(track_index: int, volume_db: float) -> str:
    """Set track volume in dB (alias)"""
    return await set_track_volume(track_index, volume_db)


async def get_track_pan(track_index: int) -> str:
    """Get track pan position (-1.0 to 1.0)"""
    # Get track first
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_result.get("ret"), "D_PAN"])
    
    if result.get("ok"):
        pan = result.get("ret", 0.0)
        return f"Track {track_index} pan: {pan:.2f}"
    else:
        raise Exception(f"Failed to get track pan: {result.get('error', 'Unknown error')}")


async def set_track_pan(track_index: int, pan: float) -> str:
    """Set track pan position (-1.0 to 1.0)"""
    # Get track first
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Clamp pan value
    pan = max(-1.0, min(1.0, pan))
    
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_result.get("ret"), "D_PAN", pan])
    
    if result.get("ok"):
        return f"Track {track_index} pan set to {pan:.2f}"
    else:
        raise Exception(f"Failed to set track pan: {result.get('error', 'Unknown error')}")


# ============================================================================
# Track Recording (6 tools)
# ============================================================================

async def get_track_record_mode(track_index: int) -> str:
    """Get track record mode"""
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_index, "I_RECMODE"])
    
    if result.get("ok"):
        mode = int(result.get("ret", 0))
        mode_names = {
            0: "Input",
            1: "Stereo out",
            2: "None (monitoring only)",
            3: "Stereo out with latency compensation",
            4: "MIDI output",
            5: "Mono out",
            6: "Mono out with latency compensation",
            7: "MIDI overdub",
            8: "MIDI replace"
        }
        mode_name = mode_names.get(mode, f"Unknown mode {mode}")
        return f"Track {track_index} record mode: {mode_name} ({mode})"
    else:
        raise Exception(f"Failed to get track record mode: {result.get('error', 'Unknown error')}")


async def set_track_record_mode(track_index: int, mode: int) -> str:
    """Set track record mode"""
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_index, "I_RECMODE", mode])
    
    if result.get("ok"):
        mode_names = {
            0: "Input",
            1: "Stereo out",
            2: "None (monitoring only)",
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
        raise Exception(f"Failed to set track record mode: {result.get('error', 'Unknown error')}")


async def get_track_record_input(track_index: int) -> str:
    """Get track record input"""
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_index, "I_RECINPUT"])
    
    if result.get("ok"):
        input_val = int(result.get("ret", -1))
        if input_val == -1:
            input_name = "None"
        elif input_val < 512:
            input_name = f"Mono hardware input {input_val + 1}"
        elif input_val < 1024:
            pair = (input_val - 512) // 2 + 1
            input_name = f"Stereo hardware input pair {pair}"
        else:
            input_name = f"ReaRoute/loopback {input_val - 1024 + 1}"
        
        return f"Track {track_index} record input: {input_name} ({input_val})"
    else:
        raise Exception(f"Failed to get track record input: {result.get('error', 'Unknown error')}")


async def set_track_record_input(track_index: int, input: int) -> str:
    """Set track record input"""
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_index, "I_RECINPUT", input])
    
    if result.get("ok"):
        if input == -1:
            input_name = "None"
        elif input < 512:
            input_name = f"Mono hardware input {input + 1}"
        elif input < 1024:
            pair = (input - 512) // 2 + 1
            input_name = f"Stereo hardware input pair {pair}"
        else:
            input_name = f"ReaRoute/loopback {input - 1024 + 1}"
        
        return f"Set track {track_index} record input to: {input_name}"
    else:
        raise Exception(f"Failed to set track record input: {result.get('error', 'Unknown error')}")


async def get_track_record_arm(track_index: int) -> str:
    """Get track record arm state"""
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_index, "I_RECARM"])
    
    if result.get("ok"):
        armed = result.get("ret", 0) > 0
        return f"Track {track_index} record arm: {'Armed' if armed else 'Not armed'}"
    else:
        raise Exception(f"Failed to get track record arm state: {result.get('error', 'Unknown error')}")


async def set_track_record_arm(track_index: int, armed: bool) -> str:
    """Set track record arm state"""
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_index, "I_RECARM", 1 if armed else 0])
    
    if result.get("ok"):
        return f"Track {track_index} record arm: {'Armed' if armed else 'Disarmed'}"
    else:
        raise Exception(f"Failed to set track record arm state: {result.get('error', 'Unknown error')}")


# ============================================================================
# Track FX (6 tools)
# ============================================================================

async def track_fx_get_count(track_index: int) -> str:
    """Get the number of FX on a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get FX count
    result = await bridge.call_lua("TrackFX_GetCount", [track_handle])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Track {track_index} has {count} FX"
    else:
        raise Exception(f"Failed to get FX count: {result.get('error', 'Unknown error')}")


async def track_fx_add_by_name(track_index: int, fx_name: str, instantiate: bool = True) -> str:
    """Add an FX to a track by name"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Add FX
    result = await bridge.call_lua("TrackFX_AddByName", [track_handle, fx_name, False, -1 if instantiate else -1000])
    
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
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Delete FX
    result = await bridge.call_lua("TrackFX_Delete", [track_handle, fx_index])
    
    if result.get("ok"):
        return f"Deleted FX at index {fx_index} from track {track_index}"
    else:
        raise Exception(f"Failed to delete FX: {result.get('error', 'Unknown error')}")


async def track_fx_get_enabled(track_index: int, fx_index: int) -> str:
    """Get whether an FX is enabled"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get enabled state
    result = await bridge.call_lua("TrackFX_GetEnabled", [track_handle, fx_index])
    
    if result.get("ok"):
        enabled = bool(result.get("ret", False))
        return f"FX {fx_index} on track {track_index} is {'enabled' if enabled else 'disabled'}"
    else:
        raise Exception(f"Failed to get FX enabled state: {result.get('error', 'Unknown error')}")


async def track_fx_set_enabled(track_index: int, fx_index: int, enabled: bool) -> str:
    """Enable or disable an FX"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set enabled state
    result = await bridge.call_lua("TrackFX_SetEnabled", [track_handle, fx_index, enabled])
    
    if result.get("ok"):
        return f"FX {fx_index} on track {track_index} {'enabled' if enabled else 'disabled'}"
    else:
        raise Exception(f"Failed to set FX enabled state: {result.get('error', 'Unknown error')}")


async def track_fx_get_name(track_index: int, fx_index: int) -> str:
    """Get the name of an FX on a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get FX name
    result = await bridge.call_lua("TrackFX_GetFXName", [track_handle, fx_index, ""])
    
    if result.get("ok"):
        # The result contains both the return value and the name
        if isinstance(result.get("ret"), list) and len(result.get("ret", [])) > 1:
            fx_name = result.get("ret")[1]
        else:
            fx_name = "Unknown"
        return f"FX {fx_index} on track {track_index}: {fx_name}"
    else:
        raise Exception(f"Failed to get FX name: {result.get('error', 'Unknown error')}")


# ============================================================================
# Track Sends & Routing (7 tools)
# ============================================================================

async def create_track_send(source_track_index: int, dest_track_index: int) -> str:
    """Create a send from one track to another"""
    # Get source and destination tracks
    source_result = await bridge.call_lua("GetTrack", [0, source_track_index])
    if not source_result.get("ok") or not source_result.get("ret"):
        raise Exception(f"Failed to find source track at index {source_track_index}")
    
    dest_result = await bridge.call_lua("GetTrack", [0, dest_track_index])
    if not dest_result.get("ok") or not dest_result.get("ret"):
        raise Exception(f"Failed to find destination track at index {dest_track_index}")
    
    source_track = source_result.get("ret")
    dest_track = dest_result.get("ret")
    
    # Create send
    result = await bridge.call_lua("CreateTrackSend", [source_track, dest_track])
    
    if result.get("ok"):
        send_index = result.get("ret", -1)
        if send_index >= 0:
            return f"Created send from track {source_track_index} to track {dest_track_index} (send index: {send_index})"
        else:
            return f"Failed to create send"
    else:
        raise Exception(f"Failed to create send: {result.get('error', 'Unknown error')}")


async def remove_track_send(track_index: int, send_index: int) -> str:
    """Remove a send from a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Remove send
    result = await bridge.call_lua("RemoveTrackSend", [track_handle, 0, send_index])
    
    if result.get("ok"):
        return f"Removed send {send_index} from track {track_index}"
    else:
        raise Exception(f"Failed to remove send: {result.get('error', 'Unknown error')}")


async def get_track_num_sends(track_index: int) -> str:
    """Get the number of sends on a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get number of sends
    result = await bridge.call_lua("GetTrackNumSends", [track_handle, 0])
    
    if result.get("ok"):
        num_sends = result.get("ret", 0)
        return f"Track {track_index} has {num_sends} sends"
    else:
        raise Exception(f"Failed to get number of sends: {result.get('error', 'Unknown error')}")


async def set_track_send_volume(track_index: int, send_index: int, volume: float) -> str:
    """Set the volume of a track send"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set send volume
    result = await bridge.call_lua("SetTrackSendInfo_Value", [track_handle, 0, send_index, "D_VOL", volume])
    
    if result.get("ok"):
        return f"Set send {send_index} volume to {volume:.3f}"
    else:
        raise Exception(f"Failed to set send volume: {result.get('error', 'Unknown error')}")


async def get_track_send_info(track_index: int, send_index: int) -> str:
    """Get information about a track send"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get send volume
    vol_result = await bridge.call_lua("GetTrackSendInfo_Value", [track_handle, 0, send_index, "D_VOL"])
    
    # Get destination track
    dest_result = await bridge.call_lua("GetTrackSendInfo_Value", [track_handle, 0, send_index, "P_DESTTRACK"])
    
    if vol_result.get("ok"):
        volume = vol_result.get("ret", 0.0)
        dest_info = ""
        if dest_result.get("ok") and dest_result.get("ret"):
            # Try to find destination track index
            for i in range(100):  # Check first 100 tracks
                check_result = await bridge.call_lua("GetTrack", [0, i])
                if check_result.get("ok") and check_result.get("ret") == dest_result.get("ret"):
                    dest_info = f", destination: track {i}"
                    break
        
        return f"Send {send_index}: volume={volume:.3f}{dest_info}"
    else:
        raise Exception(f"Failed to get send info: {vol_result.get('error', 'Unknown error')}")


async def get_track_receive_count(track_index: int) -> str:
    """Get the number of receives on a track"""
    result = await bridge.call_lua("GetTrackNumSends", [track_index, -1])
    
    if result.get("ok"):
        count = result.get("result", 0)
        return f"Track {track_index} has {count} receives"
    else:
        raise Exception(f"Failed to get track receive count: {result.get('error', 'Unknown error')}")


async def get_track_receive_info(track_index: int, receive_index: int) -> str:
    """Get information about a track receive"""
    result = await bridge.call_lua("GetTrackReceiveInfo", [track_index, receive_index])
    
    if result.get("ok"):
        info = result.get("result", {})
        return f"Receive {receive_index} from track {info.get('src_track', 'unknown')} - Volume: {info.get('volume', 0):.2f} dB, Pan: {info.get('pan', 0):.2f}"
    else:
        raise Exception(f"Failed to get track receive info: {result.get('error', 'Unknown error')}")


# ============================================================================
# Note: Track automation functions moved to automation.py
# ============================================================================

# Note: get_track_envelope_by_name is also defined in automation.py
# Keeping this version for now as it may have different behavior
async def get_track_envelope_by_name(track_index: int, envelope_name: str) -> str:
    """Get a track envelope by name (e.g., 'Volume', 'Pan', 'Mute')"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope by name
    result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
    
    if result.get("ok"):
        envelope_handle = result.get("ret")
        if envelope_handle:
            return f"Found envelope '{envelope_name}' on track {track_index}"
        else:
            return f"Envelope '{envelope_name}' not found on track {track_index}"
    else:
        raise Exception(f"Failed to get envelope: {result.get('error', 'Unknown error')}")


# ============================================================================
# Track Media Items (3 tools)
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


async def delete_track_media_item(track_index: int, item_index: int) -> str:
    """Delete a media item from track"""
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


async def get_media_item_take_track(item_index: int) -> str:
    """Get the track of a media item take"""
    result = await bridge.call_lua("GetMediaItemTrack", [item_index])
    
    if result.get("ok"):
        track_info = result.get("result", {})
        return f"Item {item_index} is on track: {track_info.get('name', 'Unnamed')} (index {track_info.get('index', -1)})"
    else:
        raise Exception(f"Failed to get item track: {result.get('error', 'Unknown error')}")


# ============================================================================
# Track Analysis & Monitoring (2 tools)
# ============================================================================

async def get_track_peak(track_index: int, channel: int = 0) -> str:
    """Get the current peak level of a track"""
    result = await bridge.call_lua("Track_GetPeakInfo", [track_index, channel])
    
    if result.get("ok"):
        peak_value = result.get("result", 0.0)
        peak_db = 20 * (peak_value / 0.0000000298023223876953125) if peak_value > 0 else -150.0
        return f"Track {track_index} peak (channel {channel}): {peak_db:.2f} dB ({peak_value:.6f})"
    else:
        raise Exception(f"Failed to get track peak: {result.get('error', 'Unknown error')}")


async def get_track_peak_info(track_index: int) -> str:
    """Get detailed peak information for a track"""
    result = await bridge.call_lua("Track_GetPeakHoldDB", [track_index])
    
    if result.get("ok"):
        peak_data = result.get("result", {})
        left_peak = peak_data.get("left", -150.0)
        right_peak = peak_data.get("right", -150.0)
        return f"Track {track_index} peak info - Left: {left_peak:.2f} dB, Right: {right_peak:.2f} dB"
    else:
        raise Exception(f"Failed to get track peak info: {result.get('error', 'Unknown error')}")


# ============================================================================
# Track Advanced Operations (7 tools)
# ============================================================================

async def freeze_track(track_index: int) -> str:
    """Freeze a track"""
    # Get track
    result = await bridge.call_lua("GetTrack", [0, track_index])
    if not result.get("ok") or not result.get("ret"):
        raise Exception(f"Track {track_index} not found")
    
    track_handle = result["retval"]
    
    # Freeze track
    result = await bridge.call_lua("Main_OnCommandEx", [41223, 0, 0])  # Track: Freeze to stereo
    if result.get("ok"):
        return f"Froze track {track_index}"
    
    raise Exception("Failed to freeze track")


async def unfreeze_track(track_index: int) -> str:
    """Unfreeze a track"""
    # Get track
    result = await bridge.call_lua("GetTrack", [0, track_index])
    if not result.get("ok") or not result.get("ret"):
        raise Exception(f"Track {track_index} not found")
    
    track_handle = result["retval"]
    
    # Unfreeze track
    result = await bridge.call_lua("Main_OnCommandEx", [41644, 0, 0])  # Track: Unfreeze
    if result.get("ok"):
        return f"Unfroze track {track_index}"
    
    raise Exception("Failed to unfreeze track")


async def bounce_tracks(add_to_project: bool = True) -> str:
    """Bounce selected tracks to a new track"""
    # Bounce selected tracks (action 40914)
    result = await bridge.call_lua("Main_OnCommand", [40914, 0])
    
    if result.get("ok"):
        return "Bounced selected tracks" + (" to new track" if add_to_project else "")
    else:
        raise Exception(f"Failed to bounce tracks: {result.get('error', 'Unknown error')}")


async def add_video_to_track(track_index: int, video_file: str) -> str:
    """Add a video file to a track"""
    result = await bridge.call_lua("AddVideoToTrack", [track_index, video_file])
    
    if result.get("ok"):
        return f"Added video '{video_file}' to track {track_index}"
    else:
        raise Exception(f"Failed to add video: {result.get('error', 'Unknown error')}")


async def get_track_state_chunk(track_index: int = 0) -> str:
    """Get the state chunk of a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get state chunk
    result = await bridge.call_lua("GetTrackStateChunk", [track_handle, "", 0])
    if result.get("ok") and result.get("chunk"):
        return result.get("chunk", "")
    
    raise Exception("Failed to get track state chunk")


async def set_track_state_chunk(track_index: int, chunk: str) -> str:
    """Set the state chunk of a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set state chunk
    result = await bridge.call_lua("SetTrackStateChunk", [track_handle, chunk, 0])
    if result.get("ok"):
        return "Successfully set track state chunk"
    
    raise Exception("Failed to set track state chunk")


async def get_track_midi_note_name(track_index: int, pitch: int, channel: int = 0) -> str:
    """Get MIDI note name for a track"""
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to get track at index {track_index}")
    
    # Get MIDI note name
    result = await bridge.call_lua("GetTrackMIDINoteName", [track_result.get("ret"), pitch, channel])
    
    if result.get("ok") and result.get("ret"):
        note_name = result.get("ret")
        return f"MIDI note {pitch} on track {track_index} channel {channel}: {note_name}"
    
    # Default note name if no custom name
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (pitch // 12) - 1
    note = note_names[pitch % 12]
    default_name = f"{note}{octave}"
    
    return f"MIDI note {pitch} on track {track_index} channel {channel}: {default_name} (default)"


# ============================================================================
# Additional Helper Functions
# ============================================================================

async def get_mixer_scroll() -> str:
    """Get the leftmost track visible in the mixer"""
    result = await bridge.call_lua("GetMixerScroll", [])
    
    if result.get("ok") and result.get("ret") is not None:
        leftmost_track = result.get("ret")
        return f"Leftmost track in mixer: {leftmost_track}"
    
    raise Exception("Failed to get mixer scroll position")


async def set_mixer_scroll(leftmost_track: int) -> str:
    """Set the leftmost track visible in the mixer"""
    # Get the track to verify it exists
    track_result = await bridge.call_lua("GetTrack", [0, leftmost_track])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Track {leftmost_track} does not exist")
    
    result = await bridge.call_lua("SetMixerScroll", [track_result.get("ret")])
    
    if result.get("ok"):
        return f"Set mixer scroll to track {leftmost_track}"
    
    raise Exception("Failed to set mixer scroll position")


# ============================================================================
# Registration Function
# ============================================================================

def register_track_tools(mcp) -> int:
    """Register all track management tools with the MCP instance"""
    tools = [
        # Basic Operations (13)
        (insert_track, "Insert a new track at the specified index (0-based)"),
        (get_track_count, "Get the number of tracks in the current project"),
        (get_track, "Get a track by index from the current project"),
        (delete_track, "Delete a track by index"),
        (get_master_track, "Get the master track"),
        (insert_track_at_index, "Insert a track at a specific index"),
        (get_track_guid, "Get the GUID of a track"),
        (get_track_from_guid, "Get track by GUID"),
        (get_last_touched_track, "Get the last touched track"),
        (count_selected_tracks, "Count the number of selected tracks"),
        (get_selected_track, "Get a selected track by index"),
        (set_track_selected, "Select or deselect a track"),
        (set_only_track_selected, "Set only one track selected, deselecting all others"),
        
        # Properties (10)
        (get_track_name, "Get the name of a track by index"),
        (set_track_name, "Set the name of a track"),
        (get_track_mute, "Get track mute state"),
        (set_track_mute, "Set track mute state"),
        (get_track_solo, "Get track solo state"),
        (set_track_solo, "Set track solo state"),
        (get_track_color, "Get the color of a track"),
        (set_track_color, "Set the color of a track"),
        (is_track_visible, "Check if a track is visible in TCP or MCP"),
        (any_track_solo, "Check if any track is soloed"),
        
        # Volume & Pan (6)
        (get_track_volume, "Get track volume in dB"),
        (set_track_volume, "Set track volume in dB"),
        (get_track_volume_db, "Get track volume in dB"),
        (set_track_volume_db, "Set track volume in dB"),
        (get_track_pan, "Get track pan position (-1.0 to 1.0)"),
        (set_track_pan, "Set track pan position (-1.0 to 1.0)"),
        
        # Recording (6)
        (get_track_record_mode, "Get track record mode"),
        (set_track_record_mode, "Set track record mode"),
        (get_track_record_input, "Get track record input"),
        (set_track_record_input, "Set track record input"),
        (get_track_record_arm, "Get track record arm state"),
        (set_track_record_arm, "Set track record arm state"),
        
        # FX (6)
        (track_fx_get_count, "Get the number of FX on a track"),
        (track_fx_add_by_name, "Add an FX to a track by name"),
        (track_fx_delete, "Delete an FX from a track"),
        (track_fx_get_enabled, "Get whether an FX is enabled"),
        (track_fx_set_enabled, "Enable or disable an FX"),
        (track_fx_get_name, "Get the name of an FX on a track"),
        
        # Sends & Routing (7)
        (create_track_send, "Create a send from one track to another"),
        (remove_track_send, "Remove a send from a track"),
        (get_track_num_sends, "Get the number of sends on a track"),
        (set_track_send_volume, "Set the volume of a track send"),
        (get_track_send_info, "Get information about a track send"),
        (get_track_receive_count, "Get the number of receives on a track"),
        (get_track_receive_info, "Get information about a track receive"),
        
        # Automation (1) - others moved to automation.py
        (get_track_envelope_by_name, "Get a track envelope by name"),
        
        # Media Items (3)
        (add_media_item_to_track, "Add a new media item to a track"),
        (delete_track_media_item, "Delete a media item from track"),
        (get_media_item_take_track, "Get the track of a media item take"),
        
        # Analysis (2)
        (get_track_peak, "Get the current peak level of a track"),
        (get_track_peak_info, "Get detailed peak information for a track"),
        
        # Advanced (7)
        (freeze_track, "Freeze a track"),
        (unfreeze_track, "Unfreeze a track"),
        (bounce_tracks, "Bounce selected tracks to a new track"),
        (add_video_to_track, "Add a video file to a track"),
        (get_track_state_chunk, "Get the state chunk of a track"),
        (set_track_state_chunk, "Set the state chunk of a track"),
        (get_track_midi_note_name, "Get MIDI note name for a track"),
        
        # Additional (2)
        (get_mixer_scroll, "Get the leftmost track visible in the mixer"),
        (set_mixer_scroll, "Set the leftmost track visible in the mixer"),
    ]
    
    # Register each tool
    for func, desc in tools:
        # The decorator will use the function's docstring if available,
        # but we can override it with our description
        decorated = mcp.tool()(func)
    
    return len(tools)  # Return count of registered tools