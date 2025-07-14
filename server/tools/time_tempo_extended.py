"""
Time/Tempo Extended Tools for REAPER MCP

This module contains extended tools for working with time signatures,
tempo markers, time mapping, and beat/time conversions.
"""

from typing import Optional, Tuple, List, Any, Dict
from ..bridge import bridge


# ============================================================================
# Tempo/Time Signature Marker Operations (6 tools)
# ============================================================================

async def add_tempo_time_sig_marker(time: float, bpm: float, time_sig_num: int, 
                                  time_sig_denom: int, linear_tempo: bool = False) -> str:
    """Add tempo/time signature marker"""
    result = await bridge.call_lua("AddTempoTimeSigMarker", 
                                 [0, time, bpm, time_sig_num, time_sig_denom, linear_tempo])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Added tempo marker at {time:.3f}s: {bpm:.1f} BPM, {time_sig_num}/{time_sig_denom}"
        else:
            return "Failed to add tempo/time signature marker"
    else:
        raise Exception(f"Failed to add tempo marker: {result.get('error', 'Unknown error')}")


async def delete_tempo_time_sig_marker(marker_index: int) -> str:
    """Delete tempo/time signature marker"""
    result = await bridge.call_lua("DeleteTempoTimeSigMarker", [0, marker_index])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Deleted tempo/time signature marker at index {marker_index}"
        else:
            return f"Failed to delete marker at index {marker_index}"
    else:
        raise Exception(f"Failed to delete tempo marker: {result.get('error', 'Unknown error')}")


async def find_tempo_time_sig_marker(time: float) -> str:
    """Find tempo/time signature marker at time"""
    result = await bridge.call_lua("FindTempoTimeSigMarker", [0, time])
    
    if result.get("ok"):
        marker_index = result.get("ret", -1)
        if marker_index >= 0:
            return f"Found tempo/time signature marker at index {marker_index}"
        else:
            return f"No tempo/time signature marker found at {time:.3f}s"
    else:
        raise Exception(f"Failed to find tempo marker: {result.get('error', 'Unknown error')}")


async def set_tempo_time_sig_marker(marker_index: int, time: Optional[float] = None,
                                  measure_start: Optional[int] = None, beat_start: Optional[float] = None,
                                  bpm: Optional[float] = None, time_sig_num: Optional[int] = None,
                                  time_sig_denom: Optional[int] = None, linear_tempo: Optional[bool] = None) -> str:
    """Set tempo/time signature marker parameters"""
    # First get current values
    get_result = await bridge.call_lua("GetTempoTimeSigMarker", [0, marker_index])
    if not get_result.get("ok") or not get_result.get("ret"):
        raise Exception(f"Failed to find marker at index {marker_index}")
    
    current = get_result.get("ret", [])
    if not isinstance(current, list) or len(current) < 7:
        raise Exception("Invalid marker data")
    
    # Use current values if not specified
    time = time if time is not None else current[1]
    measure_start = measure_start if measure_start is not None else current[2]
    beat_start = beat_start if beat_start is not None else current[3]
    bpm = bpm if bpm is not None else current[4]
    time_sig_num = time_sig_num if time_sig_num is not None else current[5]
    time_sig_denom = time_sig_denom if time_sig_denom is not None else current[6]
    linear_tempo = linear_tempo if linear_tempo is not None else False
    
    # Set marker
    result = await bridge.call_lua("SetTempoTimeSigMarker", 
                                 [0, marker_index, time, measure_start, beat_start, 
                                  bpm, time_sig_num, time_sig_denom, linear_tempo])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Updated tempo marker {marker_index}: {bpm:.1f} BPM, {time_sig_num}/{time_sig_denom} at {time:.3f}s"
        else:
            return f"Failed to update marker {marker_index}"
    else:
        raise Exception(f"Failed to set tempo marker: {result.get('error', 'Unknown error')}")


async def get_tempo_match_play_rate(source_time: float, srcstart: float, srclen: float, 
                                  targetstart: float) -> str:
    """Get tempo match play rate"""
    result = await bridge.call_lua("GetTempoMatchPlayRate", 
                                 [source_time, srcstart, srclen, targetstart])
    
    if result.get("ok"):
        play_rate = result.get("ret", 1.0)
        percentage = (play_rate - 1.0) * 100
        sign = "+" if percentage >= 0 else ""
        return f"Tempo match play rate: {play_rate:.4f} ({sign}{percentage:.1f}%)"
    else:
        raise Exception(f"Failed to get tempo match play rate: {result.get('error', 'Unknown error')}")


async def count_tempo_time_sig_markers() -> str:
    """Count tempo/time signature markers in project"""
    result = await bridge.call_lua("CountTempoTimeSigMarkers", [0])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Project has {count} tempo/time signature markers"
    else:
        raise Exception(f"Failed to count tempo markers: {result.get('error', 'Unknown error')}")


# ============================================================================
# TimeMap2 Functions (6 tools)
# ============================================================================

async def time_map2_beats_to_time(beats: float, measure: Optional[int] = None) -> str:
    """Convert beats to time using TimeMap2"""
    result = await bridge.call_lua("TimeMap2_beatsToTime", [0, beats, measure])
    
    if result.get("ok"):
        time = result.get("ret", 0.0)
        if measure is not None:
            return f"{beats:.3f} beats (from measure {measure}) = {time:.3f} seconds"
        else:
            return f"{beats:.3f} beats = {time:.3f} seconds"
    else:
        raise Exception(f"Failed to convert beats to time: {result.get('error', 'Unknown error')}")


async def time_map2_time_to_beats(time: float) -> str:
    """Convert time to beats using TimeMap2"""
    result = await bridge.call_lua("TimeMap2_timeToBeats", [0, time])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            beats, measures, cml = ret[:3]
            return f"{time:.3f}s = {beats:.3f} beats (measure {measures+1}, {cml:.3f} beats in measure)"
        else:
            return f"Failed to convert {time:.3f}s to beats"
    else:
        raise Exception(f"Failed to convert time to beats: {result.get('error', 'Unknown error')}")


async def time_map2_get_divided_bpm_at_time(time: float) -> str:
    """Get divided BPM at time using TimeMap2"""
    result = await bridge.call_lua("TimeMap2_GetDividedBpmAtTime", [0, time])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            bpm, num, denom = ret[:3]
            return f"BPM at {time:.3f}s: {bpm:.2f} ({num}/{denom} time signature)"
        else:
            return f"Failed to get BPM at {time:.3f}s"
    else:
        raise Exception(f"Failed to get divided BPM: {result.get('error', 'Unknown error')}")


async def time_map2_get_next_change_time(time: float) -> str:
    """Get next tempo change time using TimeMap2"""
    result = await bridge.call_lua("TimeMap2_GetNextChangeTime", [0, time])
    
    if result.get("ok"):
        next_time = result.get("ret", -1.0)
        if next_time >= 0:
            delta = next_time - time
            return f"Next tempo change after {time:.3f}s: at {next_time:.3f}s (+{delta:.3f}s)"
        else:
            return f"No tempo changes after {time:.3f}s"
    else:
        raise Exception(f"Failed to get next change time: {result.get('error', 'Unknown error')}")


async def time_map2_qn_to_time(qn: float) -> str:
    """Convert quarter notes to time using TimeMap2"""
    result = await bridge.call_lua("TimeMap2_QNToTime", [0, qn])
    
    if result.get("ok"):
        time = result.get("ret", 0.0)
        return f"{qn:.3f} quarter notes = {time:.3f} seconds"
    else:
        raise Exception(f"Failed to convert QN to time: {result.get('error', 'Unknown error')}")


async def time_map2_time_to_qn(time: float) -> str:
    """Convert time to quarter notes using TimeMap2"""
    result = await bridge.call_lua("TimeMap2_timeToQN", [0, time])
    
    if result.get("ok"):
        qn = result.get("ret", 0.0)
        return f"{time:.3f} seconds = {qn:.3f} quarter notes"
    else:
        raise Exception(f"Failed to convert time to QN: {result.get('error', 'Unknown error')}")


# ============================================================================
# TimeMap Functions (11 tools)
# ============================================================================

async def time_map_get_time_sig_at_time(time: float) -> str:
    """Get time signature at time"""
    result = await bridge.call_lua("TimeMap_GetTimeSigAtTime", [0, time])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            num, denom, tempo = ret[:3]
            return f"Time signature at {time:.3f}s: {num}/{denom} ({tempo:.2f} BPM)"
        else:
            return f"Failed to get time signature at {time:.3f}s"
    else:
        raise Exception(f"Failed to get time signature: {result.get('error', 'Unknown error')}")


async def time_map_qn_to_time(qn: float) -> str:
    """Convert quarter notes to time"""
    result = await bridge.call_lua("TimeMap_QNToTime", [qn])
    
    if result.get("ok"):
        time = result.get("ret", 0.0)
        return f"{qn:.3f} quarter notes = {time:.3f} seconds"
    else:
        raise Exception(f"Failed to convert QN to time: {result.get('error', 'Unknown error')}")


async def time_map_qn_to_time_abs(qn: float) -> str:
    """Convert quarter notes to absolute time"""
    result = await bridge.call_lua("TimeMap_QNToTime_abs", [0, qn])
    
    if result.get("ok"):
        time = result.get("ret", 0.0)
        return f"{qn:.3f} quarter notes = {time:.3f} seconds (absolute)"
    else:
        raise Exception(f"Failed to convert QN to absolute time: {result.get('error', 'Unknown error')}")


async def time_map_time_to_qn(time: float) -> str:
    """Convert time to quarter notes"""
    result = await bridge.call_lua("TimeMap_timeToQN", [time])
    
    if result.get("ok"):
        qn = result.get("ret", 0.0)
        return f"{time:.3f} seconds = {qn:.3f} quarter notes"
    else:
        raise Exception(f"Failed to convert time to QN: {result.get('error', 'Unknown error')}")


async def time_map_time_to_qn_abs(time: float) -> str:
    """Convert time to absolute quarter notes"""
    result = await bridge.call_lua("TimeMap_timeToQN_abs", [0, time])
    
    if result.get("ok"):
        qn = result.get("ret", 0.0)
        return f"{time:.3f} seconds = {qn:.3f} quarter notes (absolute)"
    else:
        raise Exception(f"Failed to convert time to absolute QN: {result.get('error', 'Unknown error')}")


async def time_map_qn_to_measures(qn: float) -> str:
    """Convert quarter notes to measures"""
    result = await bridge.call_lua("TimeMap_QNToMeasures", [0, qn])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            measures, qn_start, qn_end = ret[:3]
            return f"{qn:.3f} QN = measure {measures+1} (QN range: {qn_start:.3f}-{qn_end:.3f})"
        else:
            return f"Failed to convert {qn:.3f} QN to measures"
    else:
        raise Exception(f"Failed to convert QN to measures: {result.get('error', 'Unknown error')}")


async def time_map_get_measure_info(time: float) -> str:
    """Get measure information at time position"""
    result = await bridge.call_lua("TimeMap_GetMeasureInfo", [0, time])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 4:
            measure, measure_start_qn, measure_end_qn, measure_start_time = ret[:4]
            length_qn = measure_end_qn - measure_start_qn
            return f"Time {time:.3f}s is in measure {measure+1} (starts at {measure_start_time:.3f}s, {length_qn:.3f} QN long)"
        else:
            return f"Failed to get measure info at {time:.3f}s"
    else:
        raise Exception(f"Failed to get measure info: {result.get('error', 'Unknown error')}")


async def time_map_get_divided_bpm_at_time(time: float) -> str:
    """Get divided BPM at time"""
    result = await bridge.call_lua("TimeMap_GetDividedBpmAtTime", [time])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            bpm, num, denom = ret[:3]
            return f"BPM at {time:.3f}s: {bpm:.2f} ({num}/{denom} time signature)"
        else:
            return f"Failed to get BPM at {time:.3f}s"
    else:
        raise Exception(f"Failed to get divided BPM: {result.get('error', 'Unknown error')}")


async def time_map_cur_frame_rate() -> str:
    """Get current frame rate"""
    result = await bridge.call_lua("TimeMap_curFrameRate", [0])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            frame_rate, drop_frame = ret[:2]
            drop_str = " (drop frame)" if drop_frame else ""
            return f"Current frame rate: {frame_rate:.2f} fps{drop_str}"
        else:
            return "Failed to get frame rate"
    else:
        raise Exception(f"Failed to get frame rate: {result.get('error', 'Unknown error')}")


async def time_map_get_metronome_pattern(time: float) -> str:
    """Get metronome pattern at time"""
    result = await bridge.call_lua("TimeMap_GetMetronomePattern", [0, time, "", 256])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            beat_in_measure, pattern = ret[:2]
            if pattern:
                return f"Metronome at {time:.3f}s: beat {beat_in_measure:.1f}, pattern: {pattern}"
            else:
                return f"Metronome at {time:.3f}s: beat {beat_in_measure:.1f}"
        else:
            return f"Failed to get metronome pattern at {time:.3f}s"
    else:
        raise Exception(f"Failed to get metronome pattern: {result.get('error', 'Unknown error')}")


async def edit_tempo_time_sig_marker(marker_index: int) -> str:
    """Open edit dialog for tempo/time signature marker"""
    result = await bridge.call_lua("EditTempoTimeSigMarker", [0, marker_index])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Opened edit dialog for tempo marker {marker_index}"
        else:
            return f"Failed to open edit dialog for marker {marker_index}"
    else:
        raise Exception(f"Failed to edit tempo marker: {result.get('error', 'Unknown error')}")


# ============================================================================
# Clear Functions (2 tools)
# ============================================================================

async def clear_all_rec_armed() -> str:
    """Clear all record armed tracks"""
    result = await bridge.call_lua("ClearAllRecArmed", [])
    
    if result.get("ok"):
        return "Cleared all record armed tracks"
    else:
        raise Exception(f"Failed to clear record armed tracks: {result.get('error', 'Unknown error')}")


async def clear_peak_cache() -> str:
    """Clear peak cache"""
    result = await bridge.call_lua("ClearPeakCache", [])
    
    if result.get("ok"):
        return "Cleared peak cache"
    else:
        raise Exception(f"Failed to clear peak cache: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_time_tempo_extended_tools(mcp) -> int:
    """Register all time/tempo extended tools with the MCP instance"""
    tools = [
        # Tempo/Time Signature Marker Operations
        (add_tempo_time_sig_marker, "Add tempo/time signature marker"),
        (delete_tempo_time_sig_marker, "Delete tempo/time signature marker"),
        (find_tempo_time_sig_marker, "Find tempo/time signature marker at time"),
        (set_tempo_time_sig_marker, "Set tempo/time signature marker parameters"),
        (get_tempo_match_play_rate, "Get tempo match play rate"),
        (count_tempo_time_sig_markers, "Count tempo/time signature markers in project"),
        
        # TimeMap2 Functions
        (time_map2_beats_to_time, "Convert beats to time using TimeMap2"),
        (time_map2_time_to_beats, "Convert time to beats using TimeMap2"),
        (time_map2_get_divided_bpm_at_time, "Get divided BPM at time using TimeMap2"),
        (time_map2_get_next_change_time, "Get next tempo change time using TimeMap2"),
        (time_map2_qn_to_time, "Convert quarter notes to time using TimeMap2"),
        (time_map2_time_to_qn, "Convert time to quarter notes using TimeMap2"),
        
        # TimeMap Functions
        (time_map_get_time_sig_at_time, "Get time signature at time"),
        (time_map_qn_to_time, "Convert quarter notes to time"),
        (time_map_qn_to_time_abs, "Convert quarter notes to absolute time"),
        (time_map_time_to_qn, "Convert time to quarter notes"),
        (time_map_time_to_qn_abs, "Convert time to absolute quarter notes"),
        (time_map_qn_to_measures, "Convert quarter notes to measures"),
        (time_map_get_measure_info, "Get measure information at time position"),
        (time_map_get_divided_bpm_at_time, "Get divided BPM at time"),
        (time_map_cur_frame_rate, "Get current frame rate"),
        (time_map_get_metronome_pattern, "Get metronome pattern at time"),
        (edit_tempo_time_sig_marker, "Open edit dialog for tempo/time signature marker"),
        
        # Clear Functions
        (clear_all_rec_armed, "Clear all record armed tracks"),
        (clear_peak_cache, "Clear peak cache"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)