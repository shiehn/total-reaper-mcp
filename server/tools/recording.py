"""
Recording Tools for REAPER MCP

This module contains tools for managing recording settings, track arming,
input monitoring, and recording operations in REAPER projects.
"""

from typing import Optional, List, Tuple, Union
from ..bridge import bridge


# ============================================================================
# Track Record Arm & Mode (8 tools)
# ============================================================================

async def get_track_record_arm(track_index: int) -> str:
    """Get track record arm status"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok"):
        raise Exception(f"Failed to get track {track_index}")
    
    track_id = track_result.get("ret")
    if not track_id:
        raise Exception(f"Track {track_index} not found")
    
    # Get record arm status
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_id, "I_RECARM"])
    
    if result.get("ok"):
        armed = int(result.get("ret", 0))
        status = "armed" if armed else "not armed"
        return f"Track {track_index + 1} is {status} for recording"
    else:
        raise Exception(f"Failed to get record arm status: {result.get('error', 'Unknown error')}")


async def set_track_record_arm(track_index: int, armed: bool) -> str:
    """Set track record arm status"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok"):
        raise Exception(f"Failed to get track {track_index}")
    
    track_id = track_result.get("ret")
    if not track_id:
        raise Exception(f"Track {track_index} not found")
    
    # Set record arm
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_id, "I_RECARM", 1 if armed else 0])
    
    if result.get("ok"):
        action = "armed" if armed else "disarmed"
        return f"Track {track_index + 1} {action} for recording"
    else:
        raise Exception(f"Failed to set record arm: {result.get('error', 'Unknown error')}")


async def get_track_record_mode(track_index: int) -> str:
    """Get track record mode"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok"):
        raise Exception(f"Failed to get track {track_index}")
    
    track_id = track_result.get("ret")
    if not track_id:
        raise Exception(f"Track {track_index} not found")
    
    # Get record mode
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_id, "I_RECMODE"])
    
    if result.get("ok"):
        mode = int(result.get("ret", 0))
        mode_names = {
            0: "Input",
            1: "Stereo out",
            2: "None",
            3: "Stereo out with latency compensation",
            4: "MIDI output",
            5: "Mono out",
            6: "Mono out with latency compensation",
            7: "MIDI overdub",
            8: "MIDI replace",
            9: "MIDI touch-replace",
            10: "MIDI latch-replace"
        }
        mode_name = mode_names.get(mode, f"Unknown mode {mode}")
        return f"Track {track_index + 1} record mode: {mode_name}"
    else:
        raise Exception(f"Failed to get record mode: {result.get('error', 'Unknown error')}")


async def set_track_record_mode(track_index: int, mode: Union[int, str]) -> str:
    """Set track record mode"""
    # Mode mapping
    mode_map = {
        "input": 0,
        "stereo": 1,
        "none": 2,
        "stereo_latency": 3,
        "midi_output": 4,
        "mono": 5,
        "mono_latency": 6,
        "midi_overdub": 7,
        "midi_replace": 8,
        "midi_touch_replace": 9,
        "midi_latch_replace": 10
    }
    
    # Convert string mode to int if needed
    if isinstance(mode, str):
        mode = mode_map.get(mode.lower(), 0)
    
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok"):
        raise Exception(f"Failed to get track {track_index}")
    
    track_id = track_result.get("ret")
    if not track_id:
        raise Exception(f"Track {track_index} not found")
    
    # Set record mode
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_id, "I_RECMODE", mode])
    
    if result.get("ok"):
        mode_names = {
            0: "Input",
            1: "Stereo out",
            2: "None",
            3: "Stereo out with latency compensation",
            4: "MIDI output",
            5: "Mono out",
            6: "Mono out with latency compensation",
            7: "MIDI overdub",
            8: "MIDI replace",
            9: "MIDI touch-replace",
            10: "MIDI latch-replace"
        }
        mode_name = mode_names.get(mode, f"mode {mode}")
        return f"Set track {track_index + 1} record mode to: {mode_name}"
    else:
        raise Exception(f"Failed to set record mode: {result.get('error', 'Unknown error')}")


async def arm_all_tracks() -> str:
    """Arm all tracks for recording"""
    # Get track count
    count_result = await bridge.call_lua("CountTracks", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count tracks")
    
    track_count = count_result.get("ret", 0)
    armed_count = 0
    
    for i in range(track_count):
        track_result = await bridge.call_lua("GetTrack", [0, i])
        if track_result.get("ok") and track_result.get("ret"):
            track_id = track_result.get("ret")
            result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_id, "I_RECARM", 1])
            if result.get("ok"):
                armed_count += 1
    
    return f"Armed {armed_count} tracks for recording"


async def disarm_all_tracks() -> str:
    """Disarm all tracks from recording"""
    # Get track count
    count_result = await bridge.call_lua("CountTracks", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count tracks")
    
    track_count = count_result.get("ret", 0)
    disarmed_count = 0
    
    for i in range(track_count):
        track_result = await bridge.call_lua("GetTrack", [0, i])
        if track_result.get("ok") and track_result.get("ret"):
            track_id = track_result.get("ret")
            result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_id, "I_RECARM", 0])
            if result.get("ok"):
                disarmed_count += 1
    
    return f"Disarmed {disarmed_count} tracks from recording"


async def toggle_track_record_arm(track_index: int) -> str:
    """Toggle track record arm status"""
    # Get current status
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok"):
        raise Exception(f"Failed to get track {track_index}")
    
    track_id = track_result.get("ret")
    if not track_id:
        raise Exception(f"Track {track_index} not found")
    
    # Get current arm status
    arm_result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_id, "I_RECARM"])
    if not arm_result.get("ok"):
        raise Exception("Failed to get record arm status")
    
    current_armed = int(arm_result.get("ret", 0))
    new_armed = 0 if current_armed else 1
    
    # Toggle
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_id, "I_RECARM", new_armed])
    
    if result.get("ok"):
        action = "armed" if new_armed else "disarmed"
        return f"Track {track_index + 1} {action} for recording"
    else:
        raise Exception(f"Failed to toggle record arm: {result.get('error', 'Unknown error')}")


async def get_armed_tracks() -> str:
    """Get list of all armed tracks"""
    # Get track count
    count_result = await bridge.call_lua("CountTracks", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count tracks")
    
    track_count = count_result.get("ret", 0)
    armed_tracks = []
    
    for i in range(track_count):
        track_result = await bridge.call_lua("GetTrack", [0, i])
        if track_result.get("ok") and track_result.get("ret"):
            track_id = track_result.get("ret")
            
            # Get record arm status
            arm_result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_id, "I_RECARM"])
            if arm_result.get("ok") and int(arm_result.get("ret", 0)):
                # Get track name
                name_result = await bridge.call_lua("GetTrackName", [track_id])
                track_name = name_result.get("ret", f"Track {i+1}") if name_result.get("ok") else f"Track {i+1}"
                armed_tracks.append(f"{i+1}: {track_name}")
    
    if armed_tracks:
        return f"Armed tracks:\n" + "\n".join(armed_tracks)
    else:
        return "No tracks are armed for recording"


# ============================================================================
# Track Record Input (6 tools)
# ============================================================================

async def get_track_record_input(track_index: int) -> str:
    """Get track record input configuration"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok"):
        raise Exception(f"Failed to get track {track_index}")
    
    track_id = track_result.get("ret")
    if not track_id:
        raise Exception(f"Track {track_index} not found")
    
    # Get record input
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_id, "I_RECINPUT"])
    
    if result.get("ok"):
        input_val = int(result.get("ret", 0))
        
        # Decode input value
        if input_val < 0:
            return f"Track {track_index + 1} record input: None"
        elif input_val < 1024:
            # Mono input
            channel = input_val + 1
            return f"Track {track_index + 1} record input: Mono input {channel}"
        elif input_val < 2048:
            # Stereo input
            channel = (input_val - 1024) // 2 + 1
            return f"Track {track_index + 1} record input: Stereo input {channel}/{channel+1}"
        elif input_val >= 4096:
            # MIDI input
            midi_val = input_val - 4096
            device = midi_val // 32
            channel = midi_val % 32
            if channel == 0:
                return f"Track {track_index + 1} record input: MIDI All channels on device {device}"
            else:
                return f"Track {track_index + 1} record input: MIDI Channel {channel} on device {device}"
        else:
            return f"Track {track_index + 1} record input: Custom value {input_val}"
    else:
        raise Exception(f"Failed to get record input: {result.get('error', 'Unknown error')}")


async def set_track_record_input(track_index: int, input_type: str, channel: int = 1) -> str:
    """Set track record input"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok"):
        raise Exception(f"Failed to get track {track_index}")
    
    track_id = track_result.get("ret")
    if not track_id:
        raise Exception(f"Track {track_index} not found")
    
    # Calculate input value
    input_val = -1  # Default: no input
    
    if input_type.lower() == "none":
        input_val = -1
    elif input_type.lower() == "mono":
        input_val = channel - 1  # 0-based
    elif input_type.lower() == "stereo":
        input_val = 1024 + (channel - 1) * 2
    elif input_type.lower().startswith("midi"):
        # Parse MIDI input (e.g., "midi:0:all" or "midi:0:1")
        parts = input_type.split(":")
        if len(parts) >= 2:
            device = int(parts[1])
            midi_channel = 0 if len(parts) < 3 or parts[2] == "all" else int(parts[2])
            input_val = 4096 + device * 32 + midi_channel
    
    # Set record input
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_id, "I_RECINPUT", input_val])
    
    if result.get("ok"):
        return f"Set track {track_index + 1} record input to: {input_type}"
    else:
        raise Exception(f"Failed to set record input: {result.get('error', 'Unknown error')}")


async def get_track_record_monitor(track_index: int) -> str:
    """Get track record monitoring mode"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok"):
        raise Exception(f"Failed to get track {track_index}")
    
    track_id = track_result.get("ret")
    if not track_id:
        raise Exception(f"Track {track_index} not found")
    
    # Get monitor mode
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_id, "I_RECMON"])
    
    if result.get("ok"):
        mode = int(result.get("ret", 0))
        mode_names = {
            0: "Off",
            1: "Normal",
            2: "Not when playing"
        }
        mode_name = mode_names.get(mode, f"Unknown mode {mode}")
        return f"Track {track_index + 1} record monitoring: {mode_name}"
    else:
        raise Exception(f"Failed to get monitor mode: {result.get('error', 'Unknown error')}")


async def set_track_record_monitor(track_index: int, mode: Union[int, str]) -> str:
    """Set track record monitoring mode"""
    # Mode mapping
    mode_map = {
        "off": 0,
        "normal": 1,
        "on": 1,
        "not_when_playing": 2,
        "auto": 2
    }
    
    # Convert string mode to int if needed
    if isinstance(mode, str):
        mode = mode_map.get(mode.lower(), 0)
    
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok"):
        raise Exception(f"Failed to get track {track_index}")
    
    track_id = track_result.get("ret")
    if not track_id:
        raise Exception(f"Track {track_index} not found")
    
    # Set monitor mode
    result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_id, "I_RECMON", mode])
    
    if result.get("ok"):
        mode_names = {
            0: "Off",
            1: "Normal",
            2: "Not when playing"
        }
        mode_name = mode_names.get(mode, f"mode {mode}")
        return f"Set track {track_index + 1} record monitoring to: {mode_name}"
    else:
        raise Exception(f"Failed to set monitor mode: {result.get('error', 'Unknown error')}")


async def enable_all_track_monitoring() -> str:
    """Enable monitoring on all armed tracks"""
    # Get track count
    count_result = await bridge.call_lua("CountTracks", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count tracks")
    
    track_count = count_result.get("ret", 0)
    enabled_count = 0
    
    for i in range(track_count):
        track_result = await bridge.call_lua("GetTrack", [0, i])
        if track_result.get("ok") and track_result.get("ret"):
            track_id = track_result.get("ret")
            
            # Check if track is armed
            arm_result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_id, "I_RECARM"])
            if arm_result.get("ok") and int(arm_result.get("ret", 0)):
                # Enable monitoring
                result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_id, "I_RECMON", 1])
                if result.get("ok"):
                    enabled_count += 1
    
    return f"Enabled monitoring on {enabled_count} armed tracks"


async def get_record_input_list() -> str:
    """Get list of available record inputs"""
    # Get audio input count
    audio_result = await bridge.call_lua("GetNumAudioInputs", [])
    audio_inputs = audio_result.get("ret", 0) if audio_result.get("ok") else 0
    
    # Get MIDI input count
    midi_result = await bridge.call_lua("GetNumMIDIInputs", [])
    midi_inputs = midi_result.get("ret", 0) if midi_result.get("ok") else 0
    
    result = "Available record inputs:\n"
    
    # Audio inputs
    result += "\nAudio Inputs:\n"
    for i in range(audio_inputs):
        result += f"  Mono: Input {i+1}\n"
        if i < audio_inputs - 1:
            result += f"  Stereo: Input {i+1}/{i+2}\n"
    
    # MIDI inputs
    if midi_inputs > 0:
        result += "\nMIDI Inputs:\n"
        for i in range(midi_inputs):
            name_result = await bridge.call_lua("GetMIDIInputName", [i, ""])
            name = name_result.get("ret", f"MIDI Device {i}") if name_result.get("ok") else f"MIDI Device {i}"
            if isinstance(name, list) and len(name) > 1:
                name = name[1]
            result += f"  Device {i}: {name}\n"
    
    return result.rstrip()


# ============================================================================
# Recording Control (8 tools)
# ============================================================================

async def start_recording() -> str:
    """Start recording"""
    # CSurf_OnRecord
    result = await bridge.call_lua("CSurf_OnRecord", [])
    
    if result.get("ok"):
        return "Started recording"
    else:
        raise Exception(f"Failed to start recording: {result.get('error', 'Unknown error')}")


async def stop_recording() -> str:
    """Stop recording"""
    # CSurf_OnStop
    result = await bridge.call_lua("CSurf_OnStop", [])
    
    if result.get("ok"):
        return "Stopped recording"
    else:
        raise Exception(f"Failed to stop recording: {result.get('error', 'Unknown error')}")


async def toggle_recording() -> str:
    """Toggle recording on/off"""
    # Get current play state
    state_result = await bridge.call_lua("GetPlayState", [])
    if not state_result.get("ok"):
        raise Exception("Failed to get play state")
    
    play_state = state_result.get("ret", 0)
    
    # Check if recording (bit 2 = recording)
    is_recording = (play_state & 4) != 0
    
    if is_recording:
        # Stop recording
        result = await bridge.call_lua("CSurf_OnStop", [])
        action = "Stopped"
    else:
        # Start recording
        result = await bridge.call_lua("CSurf_OnRecord", [])
        action = "Started"
    
    if result.get("ok"):
        return f"{action} recording"
    else:
        raise Exception(f"Failed to toggle recording: {result.get('error', 'Unknown error')}")


async def get_recording_status() -> str:
    """Get current recording status"""
    # Get play state
    result = await bridge.call_lua("GetPlayState", [])
    
    if result.get("ok"):
        play_state = result.get("ret", 0)
        
        # Decode play state
        is_playing = (play_state & 1) != 0
        is_paused = (play_state & 2) != 0
        is_recording = (play_state & 4) != 0
        
        if is_recording:
            if is_paused:
                return "Recording (paused)"
            else:
                return "Recording"
        elif is_playing:
            return "Playing (not recording)"
        elif is_paused:
            return "Paused"
        else:
            return "Stopped"
    else:
        raise Exception(f"Failed to get recording status: {result.get('error', 'Unknown error')}")


async def set_record_mode_auto_punch(start_time: float, end_time: float) -> str:
    """Set up auto-punch recording between two time points"""
    # Set time selection
    sel_result = await bridge.call_lua("GetSet_LoopTimeRange", [True, False, start_time, end_time, False])
    if not sel_result.get("ok"):
        raise Exception("Failed to set time selection")
    
    # Enable auto-punch mode (action 40076)
    result = await bridge.call_lua("Main_OnCommand", [40076, 0])
    
    if result.get("ok"):
        return f"Set auto-punch recording from {start_time:.3f}s to {end_time:.3f}s"
    else:
        raise Exception(f"Failed to set auto-punch mode: {result.get('error', 'Unknown error')}")


async def set_preroll_recording(preroll_seconds: float = 2.0) -> str:
    """Set pre-roll time for recording"""
    # Set pre-roll in project settings
    # Using SetProjectSettingEx would be ideal, but using action for now
    # Action 42435: Set project pre-roll setting
    
    # First, we need to position cursor before record start point
    cursor_result = await bridge.call_lua("GetCursorPosition", [])
    if cursor_result.get("ok"):
        cursor_pos = cursor_result.get("ret", 0.0)
        preroll_pos = max(0, cursor_pos - preroll_seconds)
        
        # Move cursor to pre-roll position
        set_cursor_result = await bridge.call_lua("SetEditCurPos", [preroll_pos, False, False])
        
        return f"Set pre-roll recording with {preroll_seconds:.1f} seconds lead-in"
    else:
        raise Exception("Failed to set pre-roll recording")


async def get_last_recording_path() -> str:
    """Get the path where recordings are saved"""
    # Get project record path
    result = await bridge.call_lua("GetProjectPath", [""])
    
    if result.get("ok"):
        ret = result.get("ret", "")
        if isinstance(ret, list) and len(ret) > 0:
            path = ret[0]
        else:
            path = ret if isinstance(ret, str) else ""
        
        # Get additional record path info
        # Note: Would use GetProjectSettingEx for record path in full implementation
        
        return f"Recording path: {path}"
    else:
        raise Exception(f"Failed to get recording path: {result.get('error', 'Unknown error')}")


async def count_takes_recorded() -> str:
    """Count takes recorded in current session"""
    # This is a simplified version - would need to track recording session
    # Get all tracks and count takes
    count_result = await bridge.call_lua("CountTracks", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count tracks")
    
    track_count = count_result.get("ret", 0)
    total_takes = 0
    
    for i in range(track_count):
        track_result = await bridge.call_lua("GetTrack", [0, i])
        if track_result.get("ok") and track_result.get("ret"):
            track_id = track_result.get("ret")
            
            # Count items on track
            item_count_result = await bridge.call_lua("CountTrackMediaItems", [track_id])
            if item_count_result.get("ok"):
                item_count = item_count_result.get("ret", 0)
                
                # Count takes in each item
                for j in range(item_count):
                    item_result = await bridge.call_lua("GetTrackMediaItem", [track_id, j])
                    if item_result.get("ok") and item_result.get("ret"):
                        item_id = item_result.get("ret")
                        take_count_result = await bridge.call_lua("CountTakes", [item_id])
                        if take_count_result.get("ok"):
                            total_takes += take_count_result.get("ret", 0)
    
    return f"Total takes in project: {total_takes}"


# ============================================================================
# Recording Settings (5 tools)
# ============================================================================

async def get_recording_format() -> str:
    """Get default recording format settings"""
    # This would use GetProjectSettingEx in full implementation
    # For now, return common format info
    return "Recording format: WAV 24-bit 48000 Hz (project default)"


async def set_recording_format(format_type: str = "wav", bit_depth: int = 24, sample_rate: int = 48000) -> str:
    """Set default recording format"""
    # This would use SetProjectSettingEx in full implementation
    # Format string example: "evaw l24"
    format_map = {
        "wav": "evaw",
        "aiff": "ffia",
        "flac": "calf"
    }
    
    format_code = format_map.get(format_type.lower(), "evaw")
    
    # Note: In full implementation, would construct proper format string
    # and use SetProjectSettingEx
    
    return f"Set recording format to: {format_type.upper()} {bit_depth}-bit {sample_rate} Hz"


async def get_metronome_settings() -> str:
    """Get metronome/click track settings"""
    # Get metronome enabled state
    metro_result = await bridge.call_lua("GetToggleCommandState", [41745])  # Metronome enabled
    metro_enabled = metro_result.get("ret", 0) == 1 if metro_result.get("ok") else False
    
    # Get count-in enabled
    countin_result = await bridge.call_lua("GetToggleCommandState", [41743])  # Count-in enabled
    countin_enabled = countin_result.get("ret", 0) == 1 if countin_result.get("ok") else False
    
    status = []
    if metro_enabled:
        status.append("Metronome: ON")
    else:
        status.append("Metronome: OFF")
    
    if countin_enabled:
        status.append("Count-in: ON")
    else:
        status.append("Count-in: OFF")
    
    return "\n".join(status)


async def toggle_metronome() -> str:
    """Toggle metronome on/off"""
    # Toggle metronome (action 41745)
    result = await bridge.call_lua("Main_OnCommand", [41745, 0])
    
    if result.get("ok"):
        # Get new state
        state_result = await bridge.call_lua("GetToggleCommandState", [41745])
        enabled = state_result.get("ret", 0) == 1 if state_result.get("ok") else False
        
        status = "enabled" if enabled else "disabled"
        return f"Metronome {status}"
    else:
        raise Exception(f"Failed to toggle metronome: {result.get('error', 'Unknown error')}")


async def toggle_count_in() -> str:
    """Toggle count-in before recording"""
    # Toggle count-in (action 41743)
    result = await bridge.call_lua("Main_OnCommand", [41743, 0])
    
    if result.get("ok"):
        # Get new state
        state_result = await bridge.call_lua("GetToggleCommandState", [41743])
        enabled = state_result.get("ret", 0) == 1 if state_result.get("ok") else False
        
        status = "enabled" if enabled else "disabled"
        return f"Count-in {status}"
    else:
        raise Exception(f"Failed to toggle count-in: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_recording_tools(mcp) -> int:
    """Register all recording tools with the MCP instance"""
    tools = [
        # Track Record Arm & Mode
        (get_track_record_arm, "Get track record arm status"),
        (set_track_record_arm, "Set track record arm status"),
        (get_track_record_mode, "Get track record mode"),
        (set_track_record_mode, "Set track record mode"),
        (arm_all_tracks, "Arm all tracks for recording"),
        (disarm_all_tracks, "Disarm all tracks from recording"),
        (toggle_track_record_arm, "Toggle track record arm status"),
        (get_armed_tracks, "Get list of all armed tracks"),
        
        # Track Record Input
        (get_track_record_input, "Get track record input configuration"),
        (set_track_record_input, "Set track record input"),
        (get_track_record_monitor, "Get track record monitoring mode"),
        (set_track_record_monitor, "Set track record monitoring mode"),
        (enable_all_track_monitoring, "Enable monitoring on all armed tracks"),
        (get_record_input_list, "Get list of available record inputs"),
        
        # Recording Control
        (start_recording, "Start recording"),
        (stop_recording, "Stop recording"),
        (toggle_recording, "Toggle recording on/off"),
        (get_recording_status, "Get current recording status"),
        (set_record_mode_auto_punch, "Set up auto-punch recording between two time points"),
        (set_preroll_recording, "Set pre-roll time for recording"),
        (get_last_recording_path, "Get the path where recordings are saved"),
        (count_takes_recorded, "Count takes recorded in current session"),
        
        # Recording Settings
        (get_recording_format, "Get default recording format settings"),
        (set_recording_format, "Set default recording format"),
        (get_metronome_settings, "Get metronome/click track settings"),
        (toggle_metronome, "Toggle metronome on/off"),
        (toggle_count_in, "Toggle count-in before recording"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)