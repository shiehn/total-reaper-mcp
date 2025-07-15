"""
Core API and Utility Tools for REAPER MCP

This module contains core API functions and utility tools.
"""

from ..bridge import bridge


# ============================================================================
# Core API Functions
# ============================================================================

async def get_reaper_version() -> str:
    """Get the REAPER version string"""
    result = await bridge.call_lua("GetAppVersion", [])
    
    if result.get("ok"):
        version = result.get("ret", "Unknown")
        return f"REAPER version: {version}"
    else:
        raise Exception(f"Failed to get REAPER version: {result.get('error', 'Unknown error')}")


async def api_exists(function_name: str) -> str:
    """Check if a ReaScript API function exists"""
    result = await bridge.call_lua("APIExists", [function_name])
    
    if result.get("ok"):
        exists = result.get("ret", False)
        return f"API function '{function_name}' {'exists' if exists else 'does not exist'}"
    else:
        raise Exception(f"Failed to check API function: {result.get('error', 'Unknown error')}")


async def get_last_color_theme_file() -> str:
    """Get the last color theme file"""
    result = await bridge.call_lua("GetLastColorThemeFile", [])
    
    if result.get("ok"):
        theme_file = result.get("ret", "")
        if theme_file:
            return f"Last color theme file: {theme_file}"
        else:
            return "No color theme file loaded"
    else:
        raise Exception("Failed to get last color theme file")


async def get_toggle_command_state(command_id: int) -> str:
    """Get toggle command state"""
    result = await bridge.call_lua("GetToggleCommandState", [command_id])
    
    if result.get("ok"):
        state = result.get("ret", -1)
        if state == 1:
            return f"Toggle command {command_id} state: ON"
        elif state == 0:
            return f"Toggle command {command_id} state: OFF"
        else:
            return f"Toggle command {command_id} state: Not found or not a toggle"
    else:
        raise Exception("Failed to get toggle command state")


# ============================================================================
# Conversion Utilities
# ============================================================================

async def db_to_slider(db: float) -> str:
    """Convert dB value to slider value (0.0 to 1.0)"""
    result = await bridge.call_lua("DB2SLIDER", [db])
    
    if result.get("ok") and result.get("ret") is not None:
        return f"{db} dB = {result.get('ret'):.4f} (slider value)"
    else:
        raise Exception("Failed to convert dB to slider")


async def slider_to_db(slider: float) -> str:
    """Convert slider value (0.0 to 1.0) to dB value"""
    result = await bridge.call_lua("SLIDER2DB", [slider])
    
    if result.get("ok") and result.get("ret") is not None:
        return f"{slider} (slider) = {result.get('ret'):.2f} dB"
    else:
        raise Exception("Failed to convert slider to dB")


# ============================================================================
# Time/Tempo Functions
# ============================================================================

async def time_map_qn_to_time(qn: float) -> str:
    """Convert quarter note position to time in seconds"""
    result = await bridge.call_lua("TimeMap2_QNToTime", [0, qn])
    
    if result.get("ok") and result.get("ret") is not None:
        return f"Quarter note {qn} = {result.get('ret'):.3f} seconds"
    else:
        raise Exception("Failed to convert QN to time")


async def time_map_time_to_qn(time: float) -> str:
    """Convert time in seconds to quarter note position"""
    result = await bridge.call_lua("TimeMap2_timeToQN", [0, time])
    
    if result.get("ok") and result.get("ret") is not None:
        return f"{time} seconds = {result.get('ret'):.3f} quarter notes"
    else:
        raise Exception("Failed to convert time to QN")


async def get_tempo_time_sig_marker(marker_index: int) -> str:
    """Get tempo/time signature marker details"""
    result = await bridge.call_lua("GetTempoTimeSigMarker", [0, marker_index])
    
    if result.get("ok"):
        # Result contains: ok, timepos, measurepos, beatpos, bpm, timesig_num, timesig_denom, lineartempo
        if result.get("timepos") is not None:
            return (f"Tempo marker {marker_index}: "
                   f"Time={result.get('timepos', 0):.3f}s, "
                   f"BPM={result.get('bpm', 120):.2f}, "
                   f"Time Sig={result.get('timesig_num', 4)}/{result.get('timesig_denom', 4)}")
        else:
            return f"Tempo marker {marker_index} not found"
    else:
        raise Exception("Failed to get tempo/time signature marker")


async def time_map_get_measure_info(measure: int) -> str:
    """Get measure information (start time, end time, beat info)"""
    result = await bridge.call_lua("TimeMap_GetMeasureInfo", [0, measure])
    
    if result.get("ok"):
        # Result contains: ok, qn_start, qn_end, timesig_num, timesig_denom, tempo
        return (f"Measure {measure}: "
               f"Start QN={result.get('qn_start', 0):.3f}, "
               f"End QN={result.get('qn_end', 0):.3f}, "
               f"Time Sig={result.get('timesig_num', 4)}/{result.get('timesig_denom', 4)}, "
               f"Tempo={result.get('tempo', 120):.2f} BPM")
    else:
        raise Exception("Failed to get measure info")


# ============================================================================
# Audio Source Functions
# ============================================================================

async def get_media_source_sample_rate(item_index: int, take_index: int) -> str:
    """Get the sample rate of a media source"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    # Get take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_result.get("ret"), take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Get source
    source_result = await bridge.call_lua("GetMediaItemTake_Source", [take_result.get("ret")])
    if not source_result.get("ok") or not source_result.get("ret"):
        raise Exception("Failed to get media source")
    
    # Get sample rate
    result = await bridge.call_lua("GetMediaSourceSampleRate", [source_result.get("ret")])
    
    if result.get("ok") and result.get("ret"):
        return f"Sample rate: {result.get('ret')} Hz"
    else:
        raise Exception("Failed to get sample rate")


async def get_media_source_num_channels(item_index: int, take_index: int) -> str:
    """Get the number of channels in a media source"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    # Get take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_result.get("ret"), take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take at index {take_index}")
    
    # Get source
    source_result = await bridge.call_lua("GetMediaItemTake_Source", [take_result.get("ret")])
    if not source_result.get("ok") or not source_result.get("ret"):
        raise Exception("Failed to get media source")
    
    # Get channel count
    result = await bridge.call_lua("GetMediaSourceNumChannels", [source_result.get("ret")])
    
    if result.get("ok") and result.get("ret"):
        channels = result.get("ret")
        if channels == 1:
            return "Channels: 1 (Mono)"
        elif channels == 2:
            return "Channels: 2 (Stereo)"
        else:
            return f"Channels: {channels}"
    else:
        raise Exception("Failed to get channel count")


# ============================================================================
# Project Functions
# ============================================================================

async def mark_project_dirty(project_index: int = 0) -> str:
    """Mark project as having unsaved changes"""
    result = await bridge.call_lua("MarkProjectDirty", [project_index])
    
    if result.get("ok"):
        return "Project marked as having unsaved changes"
    else:
        raise Exception("Failed to mark project dirty")


async def get_project_length() -> str:
    """Get total project length in seconds"""
    result = await bridge.call_lua("GetProjectLength", [0])
    
    if result.get("ok") and result.get("ret") is not None:
        length = result.get("ret")
        minutes = int(length // 60)
        seconds = length % 60
        return f"Project length: {minutes}:{seconds:05.2f} ({length:.2f} seconds)"
    else:
        raise Exception("Failed to get project length")


async def is_in_real_time_audio() -> str:
    """Check if in real-time audio thread"""
    result = await bridge.call_lua("IsInRealTimeAudio", [])
    
    if result.get("ok"):
        in_realtime = result.get("ret", 0)
        return f"In real-time audio thread: {'Yes' if in_realtime else 'No'}"
    else:
        raise Exception("Failed to check real-time audio status")


# ============================================================================
# Registration Function
# ============================================================================

def register_core_api_tools(mcp) -> int:
    """Register all core API and utility tools with the MCP instance"""
    tools = [
        # Core API
        (get_reaper_version, "Get the REAPER version string"),
        (api_exists, "Check if a ReaScript API function exists"),
        (get_last_color_theme_file, "Get the last color theme file"),
        (get_toggle_command_state, "Get toggle command state"),
        
        # Conversions
        (db_to_slider, "Convert dB value to slider value (0.0 to 1.0)"),
        (slider_to_db, "Convert slider value (0.0 to 1.0) to dB value"),
        
        # Time/Tempo
        (time_map_qn_to_time, "Convert quarter note position to time in seconds"),
        (time_map_time_to_qn, "Convert time in seconds to quarter note position"),
        (get_tempo_time_sig_marker, "Get tempo/time signature marker details"),
        (time_map_get_measure_info, "Get measure information"),
        
        # Audio Source
        (get_media_source_sample_rate, "Get the sample rate of a media source"),
        (get_media_source_num_channels, "Get the number of channels in a media source"),
        
        # Project
        (mark_project_dirty, "Mark project as having unsaved changes"),
        (get_project_length, "Get total project length in seconds"),
        (is_in_real_time_audio, "Check if in real-time audio thread"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)