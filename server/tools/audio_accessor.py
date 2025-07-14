"""
Audio Accessor & Analysis Tools for REAPER MCP

This module contains tools for audio analysis, peak calculation,
loudness measurement, and audio accessor management.
"""

from typing import Optional, Tuple, List, Any
from ..bridge import bridge


# ============================================================================
# Audio Accessor Management (8 tools)
# ============================================================================

async def create_track_audio_accessor(track_index: int) -> str:
    """Create an audio accessor for a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Create accessor
    result = await bridge.call_lua("CreateTrackAudioAccessor", [track_handle])
    
    if result.get("ok"):
        accessor = result.get("ret")
        if accessor:
            # Store accessor handle for later use
            return f"Created audio accessor for track {track_index}"
        else:
            return "Failed to create audio accessor"
    else:
        raise Exception(f"Failed to create track audio accessor: {result.get('error', 'Unknown error')}")


async def create_take_audio_accessor(item_index: int, take_index: int) -> str:
    """Create an audio accessor for a take"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Create accessor
    result = await bridge.call_lua("CreateTakeAudioAccessor", [take_handle])
    
    if result.get("ok"):
        accessor = result.get("ret")
        if accessor:
            return f"Created audio accessor for take {take_index}"
        else:
            return "Failed to create take audio accessor"
    else:
        raise Exception(f"Failed to create take audio accessor: {result.get('error', 'Unknown error')}")


async def destroy_audio_accessor(accessor_id: str) -> str:
    """Destroy an audio accessor"""
    # Note: In practice, we'd need to maintain accessor handles
    # For now, we'll simulate with a message
    result = await bridge.call_lua("DestroyAudioAccessor", [accessor_id])
    
    if result.get("ok"):
        return f"Destroyed audio accessor"
    else:
        raise Exception(f"Failed to destroy audio accessor: {result.get('error', 'Unknown error')}")


async def audio_accessor_update(accessor_id: str) -> str:
    """Update audio accessor after changes"""
    result = await bridge.call_lua("AudioAccessorUpdate", [accessor_id])
    
    if result.get("ok"):
        return "Updated audio accessor"
    else:
        raise Exception(f"Failed to update audio accessor: {result.get('error', 'Unknown error')}")


async def audio_accessor_state_changed(accessor_id: str) -> str:
    """Check if audio accessor state has changed"""
    result = await bridge.call_lua("AudioAccessorStateChanged", [accessor_id])
    
    if result.get("ok"):
        changed = result.get("ret", False)
        return f"Audio accessor state {'has changed' if changed else 'unchanged'}"
    else:
        raise Exception(f"Failed to check audio accessor state: {result.get('error', 'Unknown error')}")


async def audio_accessor_validate_state(accessor_id: str) -> str:
    """Validate audio accessor state"""
    result = await bridge.call_lua("AudioAccessorValidateState", [accessor_id])
    
    if result.get("ok"):
        valid = result.get("ret", False)
        return f"Audio accessor state is {'valid' if valid else 'invalid'}"
    else:
        raise Exception(f"Failed to validate audio accessor: {result.get('error', 'Unknown error')}")


async def get_audio_accessor_start_time(accessor_id: str) -> str:
    """Get audio accessor start time"""
    result = await bridge.call_lua("GetAudioAccessorStartTime", [accessor_id])
    
    if result.get("ok"):
        start_time = result.get("ret", 0.0)
        return f"Audio accessor start time: {start_time:.3f} seconds"
    else:
        raise Exception(f"Failed to get audio accessor start time: {result.get('error', 'Unknown error')}")


async def get_audio_accessor_end_time(accessor_id: str) -> str:
    """Get audio accessor end time"""
    result = await bridge.call_lua("GetAudioAccessorEndTime", [accessor_id])
    
    if result.get("ok"):
        end_time = result.get("ret", 0.0)
        return f"Audio accessor end time: {end_time:.3f} seconds"
    else:
        raise Exception(f"Failed to get audio accessor end time: {result.get('error', 'Unknown error')}")


# ============================================================================
# Audio Analysis & Loudness (8 tools)
# ============================================================================

async def calc_media_src_loudness(item_index: int, take_index: int) -> str:
    """Calculate loudness of media source"""
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
    
    # Calculate loudness
    result = await bridge.call_lua("CalcMediaSrcLoudness", [source_handle])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            retval, lufs_integrated, lufs_range = ret[:3]
            if retval == 0:
                return f"Loudness: {lufs_integrated:.1f} LUFS integrated, {lufs_range:.1f} LU range"
            else:
                return f"Loudness calculation in progress (status: {retval})"
        else:
            return "Failed to calculate loudness"
    else:
        raise Exception(f"Failed to calculate loudness: {result.get('error', 'Unknown error')}")


async def calculate_normalization(item_index: int, take_index: int, normalize_to_db: float = -23.0) -> str:
    """Calculate normalization values for a take"""
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
    
    # Calculate normalization
    result = await bridge.call_lua("CalculateNormalization", [source_handle, 2, normalize_to_db, 0.0, 0.0, True])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            retval, gain_mul, offset = ret[:3]
            if retval == 0:
                gain_db = 20 * (gain_mul ** 0.5) if gain_mul > 0 else -100
                return f"Normalization: gain={gain_db:.1f}dB, offset={offset:.3f}s"
            else:
                return f"Normalization calculation in progress (status: {retval})"
        else:
            return "Failed to calculate normalization"
    else:
        raise Exception(f"Failed to calculate normalization: {result.get('error', 'Unknown error')}")


async def get_audio_device_info(name: str, attribute: str) -> str:
    """Get audio device information"""
    result = await bridge.call_lua("GetAudioDeviceInfo", [name, attribute])
    
    if result.get("ok"):
        value = result.get("ret", "")
        if value:
            return f"Audio device {name} - {attribute}: {value}"
        else:
            return f"Audio device {name} - {attribute}: (not available)"
    else:
        raise Exception(f"Failed to get audio device info: {result.get('error', 'Unknown error')}")


async def get_output_latency() -> str:
    """Get audio output latency"""
    result = await bridge.call_lua("GetOutputLatency", [])
    
    if result.get("ok"):
        latency = result.get("ret", 0.0)
        latency_ms = latency * 1000
        return f"Audio output latency: {latency_ms:.1f}ms ({latency:.6f} seconds)"
    else:
        raise Exception(f"Failed to get output latency: {result.get('error', 'Unknown error')}")


async def get_num_audio_inputs() -> str:
    """Get number of audio inputs"""
    result = await bridge.call_lua("GetNumAudioInputs", [])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"System has {count} audio inputs"
    else:
        raise Exception(f"Failed to get audio input count: {result.get('error', 'Unknown error')}")


async def get_input_activity_level(input_channel: int) -> str:
    """Get input channel activity level"""
    result = await bridge.call_lua("GetInputActivityLevel", [input_channel])
    
    if result.get("ok"):
        level = result.get("ret", 0.0)
        level_db = 20 * (level ** 0.5) if level > 0 else -100
        return f"Input channel {input_channel} level: {level_db:.1f} dB"
    else:
        raise Exception(f"Failed to get input activity level: {result.get('error', 'Unknown error')}")


async def audio_is_running() -> str:
    """Check if audio engine is running"""
    result = await bridge.call_lua("Audio_IsRunning", [])
    
    if result.get("ok"):
        running = result.get("ret", 0)
        return f"Audio engine is {'running' if running else 'stopped'}"
    else:
        raise Exception(f"Failed to check audio status: {result.get('error', 'Unknown error')}")


async def audio_is_pre_buffer() -> str:
    """Check if audio is pre-buffering"""
    result = await bridge.call_lua("Audio_IsPreBuffer", [])
    
    if result.get("ok"):
        pre_buffer = result.get("ret", 0)
        return f"Audio is {'pre-buffering' if pre_buffer else 'not pre-buffering'}"
    else:
        raise Exception(f"Failed to check pre-buffer status: {result.get('error', 'Unknown error')}")


# ============================================================================
# Peak Analysis (10 tools)
# ============================================================================

async def calculate_peaks(source_filename: str, sample_rate: int = 44100) -> str:
    """Calculate peaks for audio file"""
    # Create source from file
    source_result = await bridge.call_lua("PCM_Source_CreateFromFile", [source_filename])
    if not source_result.get("ok") or not source_result.get("ret"):
        raise Exception(f"Failed to create source from file: {source_filename}")
    
    source_handle = source_result.get("ret")
    
    # Calculate peaks
    result = await bridge.call_lua("CalculatePeaks", [source_handle, sample_rate])
    
    if result.get("ok"):
        ret_code = result.get("ret", -1)
        if ret_code == 0:
            return f"Calculated peaks for {source_filename} at {sample_rate}Hz"
        else:
            return f"Peak calculation in progress (code: {ret_code})"
    else:
        raise Exception(f"Failed to calculate peaks: {result.get('error', 'Unknown error')}")


async def pcm_source_build_peaks(item_index: int, take_index: int, mode: int = 0) -> str:
    """Build peaks for PCM source"""
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
    
    # Build peaks
    result = await bridge.call_lua("PCM_Source_BuildPeaks", [source_handle, mode])
    
    if result.get("ok"):
        status = result.get("ret", 0)
        if status == 0:
            return "Peaks already built or not needed"
        else:
            return f"Building peaks (status: {status})"
    else:
        raise Exception(f"Failed to build peaks: {result.get('error', 'Unknown error')}")


async def get_peak_file_name(source_filename: str) -> str:
    """Get the peak file name for a source file"""
    result = await bridge.call_lua("GetPeakFileName", [source_filename, "", 4096])
    
    if result.get("ok"):
        peak_filename = result.get("ret", "")
        if peak_filename:
            return f"Peak file: {peak_filename}"
        else:
            return "No peak file generated for this source"
    else:
        raise Exception(f"Failed to get peak filename: {result.get('error', 'Unknown error')}")


async def clear_peak_cache() -> str:
    """Clear the peak cache"""
    result = await bridge.call_lua("ClearPeakCache", [])
    
    if result.get("ok"):
        return "Cleared peak cache"
    else:
        raise Exception(f"Failed to clear peak cache: {result.get('error', 'Unknown error')}")


async def get_track_peak_info(track_index: int, channel: int = 0) -> str:
    """Get detailed track peak information"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get peak info
    result = await bridge.call_lua("Track_GetPeakInfo", [track_handle, channel])
    
    if result.get("ok"):
        peak = result.get("ret", 0.0)
        peak_db = 20 * (peak ** 0.5) if peak > 0 else -100
        return f"Track {track_index} channel {channel} peak: {peak_db:.1f} dB"
    else:
        raise Exception(f"Failed to get track peak info: {result.get('error', 'Unknown error')}")


async def track_get_peak_hold_db(track_index: int, channel: int, clear: bool = False) -> str:
    """Get track peak hold in dB"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get peak hold
    result = await bridge.call_lua("Track_GetPeakHoldDB", [track_handle, channel, clear])
    
    if result.get("ok"):
        peak_db = result.get("ret", -150.0)
        action = " (cleared)" if clear else ""
        return f"Track {track_index} channel {channel} peak hold: {peak_db:.1f} dB{action}"
    else:
        raise Exception(f"Failed to get track peak hold: {result.get('error', 'Unknown error')}")


async def get_peaks_bitmap(item_index: int, take_index: int, 
                          width: int, height: int, start_time: float, end_time: float) -> str:
    """Get peaks as bitmap data"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get peaks bitmap
    result = await bridge.call_lua("GetPeaksBitmap", [
        take_handle, 1.0, width, height, start_time, end_time
    ])
    
    if result.get("ok"):
        bitmap_info = result.get("ret", {})
        return f"Generated {width}x{height} peaks bitmap for time range {start_time:.3f}-{end_time:.3f}"
    else:
        raise Exception(f"Failed to get peaks bitmap: {result.get('error', 'Unknown error')}")


async def hires_peaks_from_source(item_index: int, take_index: int) -> str:
    """Generate high-resolution peaks from source"""
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
    
    # Generate hires peaks
    result = await bridge.call_lua("HiresPeaksFromSource", [source_handle, source_handle])
    
    if result.get("ok"):
        return "Generated high-resolution peaks from source"
    else:
        raise Exception(f"Failed to generate hires peaks: {result.get('error', 'Unknown error')}")


async def calculate_peaks_float_src(data_size: int, sample_rate: int, channels: int) -> str:
    """Calculate peaks from float source data"""
    # This would normally work with actual float data
    # For now, we'll simulate the operation
    result = await bridge.call_lua("CalculatePeaksFloatSrcPtr", [0, data_size, sample_rate, channels])
    
    if result.get("ok"):
        ret_code = result.get("ret", -1)
        if ret_code == 0:
            return f"Calculated peaks for {data_size} samples at {sample_rate}Hz, {channels} channels"
        else:
            return f"Peak calculation returned code: {ret_code}"
    else:
        raise Exception(f"Failed to calculate peaks from float source: {result.get('error', 'Unknown error')}")


async def get_audio_accessor_samples(accessor_id: str, sample_rate: int, channels: int, 
                                   start_time: float, samples: int) -> str:
    """Get audio samples from accessor"""
    # Allocate buffer for samples
    buffer_size = samples * channels
    
    result = await bridge.call_lua("GetAudioAccessorSamples", [
        accessor_id, sample_rate, channels, start_time, samples, []
    ])
    
    if result.get("ok"):
        actual_samples = result.get("ret", 0)
        return f"Retrieved {actual_samples} samples from audio accessor"
    else:
        raise Exception(f"Failed to get audio accessor samples: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_audio_accessor_tools(mcp) -> int:
    """Register all audio accessor tools with the MCP instance"""
    tools = [
        # Audio Accessor Management
        (create_track_audio_accessor, "Create an audio accessor for a track"),
        (create_take_audio_accessor, "Create an audio accessor for a take"),
        (destroy_audio_accessor, "Destroy an audio accessor"),
        (audio_accessor_update, "Update audio accessor after changes"),
        (audio_accessor_state_changed, "Check if audio accessor state has changed"),
        (audio_accessor_validate_state, "Validate audio accessor state"),
        (get_audio_accessor_start_time, "Get audio accessor start time"),
        (get_audio_accessor_end_time, "Get audio accessor end time"),
        
        # Audio Analysis & Loudness
        (calc_media_src_loudness, "Calculate loudness of media source"),
        (calculate_normalization, "Calculate normalization values for a take"),
        (get_audio_device_info, "Get audio device information"),
        (get_output_latency, "Get audio output latency"),
        (get_num_audio_inputs, "Get number of audio inputs"),
        (get_input_activity_level, "Get input channel activity level"),
        (audio_is_running, "Check if audio engine is running"),
        (audio_is_pre_buffer, "Check if audio is pre-buffering"),
        
        # Peak Analysis
        (calculate_peaks, "Calculate peaks for audio file"),
        (pcm_source_build_peaks, "Build peaks for PCM source"),
        (get_peak_file_name, "Get the peak file name for a source file"),
        (clear_peak_cache, "Clear the peak cache"),
        (get_track_peak_info, "Get detailed track peak information"),
        (track_get_peak_hold_db, "Get track peak hold in dB"),
        (get_peaks_bitmap, "Get peaks as bitmap data"),
        (hires_peaks_from_source, "Generate high-resolution peaks from source"),
        (calculate_peaks_float_src, "Calculate peaks from float source data"),
        (get_audio_accessor_samples, "Get audio samples from accessor"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)