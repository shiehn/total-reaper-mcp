"""
Tempo & Time Signature Tools for REAPER MCP

This module contains tools for managing tempo, time signatures, tempo maps,
and musical time calculations in REAPER projects.
"""

from typing import Optional, Tuple, List
from ..bridge import bridge


# ============================================================================
# Tempo Operations (8 tools)
# ============================================================================

async def get_project_tempo() -> str:
    """Get the current project tempo at edit cursor"""
    # Get cursor position
    cursor_result = await bridge.call_lua("GetCursorPosition", [])
    if not cursor_result.get("ok"):
        raise Exception("Failed to get cursor position")
    
    cursor_pos = cursor_result.get("ret", 0.0)
    
    # Get tempo at cursor
    result = await bridge.call_lua("TimeMap_GetDividedBpmAtTime", [cursor_pos])
    
    if result.get("ok"):
        bpm = result.get("ret", 120.0)
        return f"Current tempo: {bpm:.2f} BPM at {cursor_pos:.3f} seconds"
    else:
        raise Exception(f"Failed to get project tempo: {result.get('error', 'Unknown error')}")


async def set_project_tempo(tempo: float, position: Optional[float] = None) -> str:
    """Set project tempo at position (or edit cursor if not specified)"""
    # Get position
    if position is None:
        cursor_result = await bridge.call_lua("GetCursorPosition", [])
        if not cursor_result.get("ok"):
            raise Exception("Failed to get cursor position")
        position = cursor_result.get("ret", 0.0)
    
    # Set tempo using tempo/time signature marker
    result = await bridge.call_lua("SetTempoTimeSigMarker", [
        0,      # project
        -1,     # marker index (-1 = insert new)
        position,
        -1,     # measure position (calculate automatically)
        0.0,    # beat position
        tempo,
        0,      # timesig_num (0 = don't change)
        0,      # timesig_denom (0 = don't change)
        True    # lineartempo
    ])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set tempo to {tempo:.2f} BPM at {position:.3f} seconds"
        else:
            return "Failed to set tempo"
    else:
        raise Exception(f"Failed to set tempo: {result.get('error', 'Unknown error')}")


async def get_tempo_at_time(time: float) -> str:
    """Get tempo at specific time position"""
    result = await bridge.call_lua("TimeMap_GetDividedBpmAtTime", [time])
    
    if result.get("ok"):
        bpm = result.get("ret", 120.0)
        return f"Tempo at {time:.3f} seconds: {bpm:.2f} BPM"
    else:
        raise Exception(f"Failed to get tempo at time: {result.get('error', 'Unknown error')}")


async def count_tempo_markers() -> str:
    """Count tempo/time signature markers in project"""
    result = await bridge.call_lua("CountTempoTimeSigMarkers", [0])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Project has {count} tempo/time signature markers"
    else:
        raise Exception(f"Failed to count tempo markers: {result.get('error', 'Unknown error')}")


async def get_tempo_marker_info(index: int) -> str:
    """Get information about a tempo/time signature marker"""
    result = await bridge.call_lua("GetTempoTimeSigMarker", [0, index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 7:
            retval, timepos, measurepos, beatpos, bpm, timesig_num, timesig_denom, lineartempo = ret[:8]
            if retval:
                return (f"Marker {index}: {bpm:.2f} BPM, "
                       f"{timesig_num}/{timesig_denom} time signature at {timepos:.3f} seconds "
                       f"(measure {measurepos}, beat {beatpos:.2f})")
            else:
                return f"No tempo marker at index {index}"
        else:
            return "Failed to get tempo marker data"
    else:
        raise Exception(f"Failed to get tempo marker: {result.get('error', 'Unknown error')}")


async def delete_tempo_marker(index: int) -> str:
    """Delete a tempo/time signature marker"""
    result = await bridge.call_lua("DeleteTempoTimeSigMarker", [0, index])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Deleted tempo marker at index {index}"
        else:
            return f"Failed to delete tempo marker at index {index}"
    else:
        raise Exception(f"Failed to delete tempo marker: {result.get('error', 'Unknown error')}")


async def find_tempo_marker_at_time(time: float) -> str:
    """Find tempo marker at or before specific time"""
    result = await bridge.call_lua("FindTempoTimeSigMarker", [0, time])
    
    if result.get("ok"):
        index = result.get("ret", -1)
        if index >= 0:
            # Get marker info
            info_result = await bridge.call_lua("GetTempoTimeSigMarker", [0, index])
            if info_result.get("ok") and isinstance(info_result.get("ret"), list):
                ret = info_result.get("ret")
                if len(ret) >= 5:
                    _, timepos, _, _, bpm = ret[:5]
                    return f"Found tempo marker {index} at {timepos:.3f} seconds: {bpm:.2f} BPM"
        return f"No tempo marker found at or before {time:.3f} seconds"
    else:
        raise Exception(f"Failed to find tempo marker: {result.get('error', 'Unknown error')}")


async def update_timeline_for_tempo_changes() -> str:
    """Update timeline display after tempo changes"""
    result = await bridge.call_lua("UpdateTimeline", [])
    
    if result.get("ok"):
        return "Updated timeline for tempo changes"
    else:
        raise Exception(f"Failed to update timeline: {result.get('error', 'Unknown error')}")


# ============================================================================
# Time Signature Operations (6 tools)
# ============================================================================

async def get_time_signature_at_time(time: float) -> str:
    """Get time signature at specific time"""
    # Find tempo marker at time
    find_result = await bridge.call_lua("FindTempoTimeSigMarker", [0, time])
    if not find_result.get("ok"):
        raise Exception("Failed to find tempo marker")
    
    index = find_result.get("ret", -1)
    if index < 0:
        return "No time signature defined at this position (using project default)"
    
    # Get marker info
    result = await bridge.call_lua("GetTempoTimeSigMarker", [0, index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 7:
            retval, timepos, measurepos, beatpos, bpm, timesig_num, timesig_denom = ret[:7]
            if retval:
                return f"Time signature at {time:.3f} seconds: {timesig_num}/{timesig_denom}"
            else:
                return "Failed to get time signature"
        else:
            return "Invalid time signature data"
    else:
        raise Exception(f"Failed to get time signature: {result.get('error', 'Unknown error')}")


async def set_time_signature(numerator: int, denominator: int, position: Optional[float] = None) -> str:
    """Set time signature at position (or edit cursor if not specified)"""
    # Get position
    if position is None:
        cursor_result = await bridge.call_lua("GetCursorPosition", [])
        if not cursor_result.get("ok"):
            raise Exception("Failed to get cursor position")
        position = cursor_result.get("ret", 0.0)
    
    # Get current tempo at position
    tempo_result = await bridge.call_lua("TimeMap_GetDividedBpmAtTime", [position])
    if not tempo_result.get("ok"):
        raise Exception("Failed to get tempo")
    
    tempo = tempo_result.get("ret", 120.0)
    
    # Set time signature using tempo/time signature marker
    result = await bridge.call_lua("SetTempoTimeSigMarker", [
        0,      # project
        -1,     # marker index (-1 = insert new)
        position,
        -1,     # measure position (calculate automatically)
        0.0,    # beat position
        tempo,  # keep current tempo
        numerator,
        denominator,
        True    # lineartempo
    ])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set time signature to {numerator}/{denominator} at {position:.3f} seconds"
        else:
            return "Failed to set time signature"
    else:
        raise Exception(f"Failed to set time signature: {result.get('error', 'Unknown error')}")


async def add_tempo_time_sig_change(position: float, tempo: float, 
                                   numerator: int, denominator: int, 
                                   linear_tempo: bool = False) -> str:
    """Add tempo and time signature change at position"""
    result = await bridge.call_lua("SetTempoTimeSigMarker", [
        0,      # project
        -1,     # marker index (-1 = insert new)
        position,
        -1,     # measure position (calculate automatically)
        0.0,    # beat position
        tempo,
        numerator,
        denominator,
        linear_tempo
    ])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            tempo_type = "linear" if linear_tempo else "jump"
            return (f"Added {tempo_type} tempo change to {tempo:.2f} BPM "
                   f"and {numerator}/{denominator} time signature at {position:.3f} seconds")
        else:
            return "Failed to add tempo/time signature change"
    else:
        raise Exception(f"Failed to add tempo/time signature: {result.get('error', 'Unknown error')}")


async def get_measure_info(measure_index: int) -> str:
    """Get information about a specific measure"""
    # Get measure info
    result = await bridge.call_lua("TimeMap_GetMeasureInfo", [0, measure_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 5:
            retval, qn_start, qn_end, timesig_num, timesig_denom = ret[:5]
            if retval >= 0:
                # Convert QN to time
                time_start_result = await bridge.call_lua("TimeMap2_QNToTime", [0, qn_start])
                time_end_result = await bridge.call_lua("TimeMap2_QNToTime", [0, qn_end])
                
                if time_start_result.get("ok") and time_end_result.get("ok"):
                    time_start = time_start_result.get("ret", 0.0)
                    time_end = time_end_result.get("ret", 0.0)
                    duration = time_end - time_start
                    
                    return (f"Measure {measure_index}: {timesig_num}/{timesig_denom} time, "
                           f"starts at {time_start:.3f}s, duration {duration:.3f}s")
                else:
                    return f"Measure {measure_index}: {timesig_num}/{timesig_denom} time"
            else:
                return f"No measure at index {measure_index}"
        else:
            return "Failed to get measure info"
    else:
        raise Exception(f"Failed to get measure info: {result.get('error', 'Unknown error')}")


async def beats_to_time(beats: float, measures: int = 0) -> str:
    """Convert beats (and measures) to time position"""
    # Calculate total quarter notes
    # First get time signature at start
    timesig_result = await bridge.call_lua("TimeMap_GetMeasureInfo", [0, measures])
    if timesig_result.get("ok") and isinstance(timesig_result.get("ret"), list):
        ret = timesig_result.get("ret")
        if len(ret) >= 5:
            _, qn_start, _, timesig_num, timesig_denom = ret[:5]
            
            # Calculate quarter notes for the beats
            qn_per_beat = 4.0 / timesig_denom
            total_qn = qn_start + (beats * qn_per_beat)
            
            # Convert to time
            result = await bridge.call_lua("TimeMap2_QNToTime", [0, total_qn])
            
            if result.get("ok"):
                time = result.get("ret", 0.0)
                return f"{measures} measures + {beats:.2f} beats = {time:.3f} seconds"
            else:
                raise Exception("Failed to convert QN to time")
        else:
            raise Exception("Invalid measure data")
    else:
        raise Exception("Failed to get measure info")


async def time_to_beats(time: float) -> str:
    """Convert time position to beats and measures"""
    # Convert time to QN
    qn_result = await bridge.call_lua("TimeMap2_timeToQN", [time])
    if not qn_result.get("ok"):
        raise Exception("Failed to convert time to QN")
    
    qn = qn_result.get("ret", 0.0)
    
    # Get measure and beat info
    result = await bridge.call_lua("TimeMap_QNToMeasures", [0, qn])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, measures, cml, fullbeats, cdenom = ret[:5] if len(ret) >= 5 else ret + [0, 0, 0]
            if retval >= 0:
                return f"{time:.3f} seconds = Measure {measures+1}, Beat {fullbeats+1:.2f}"
            else:
                return f"Failed to calculate measures/beats for {time:.3f} seconds"
        else:
            return "Invalid beat calculation data"
    else:
        raise Exception(f"Failed to convert time to beats: {result.get('error', 'Unknown error')}")


# ============================================================================
# Musical Time Calculations (8 tools)
# ============================================================================

async def quarter_notes_to_time(quarter_notes: float) -> str:
    """Convert quarter note position to time"""
    result = await bridge.call_lua("TimeMap2_QNToTime", [0, quarter_notes])
    
    if result.get("ok"):
        time = result.get("ret", 0.0)
        return f"{quarter_notes:.3f} quarter notes = {time:.3f} seconds"
    else:
        raise Exception(f"Failed to convert QN to time: {result.get('error', 'Unknown error')}")


async def time_to_quarter_notes(time: float) -> str:
    """Convert time to quarter note position"""
    result = await bridge.call_lua("TimeMap2_timeToQN", [time])
    
    if result.get("ok"):
        qn = result.get("ret", 0.0)
        return f"{time:.3f} seconds = {qn:.3f} quarter notes"
    else:
        raise Exception(f"Failed to convert time to QN: {result.get('error', 'Unknown error')}")


async def calculate_beat_time(beat: float, measure: int = 0) -> str:
    """Calculate time position of a specific beat in a measure"""
    # Get measure info
    measure_result = await bridge.call_lua("TimeMap_GetMeasureInfo", [0, measure])
    if not measure_result.get("ok"):
        raise Exception("Failed to get measure info")
    
    ret = measure_result.get("ret", [])
    if not isinstance(ret, list) or len(ret) < 5:
        raise Exception("Invalid measure data")
    
    _, qn_start, _, timesig_num, timesig_denom = ret[:5]
    
    # Calculate quarter notes for the beat
    qn_per_beat = 4.0 / timesig_denom
    beat_qn = qn_start + ((beat - 1) * qn_per_beat)  # beat is 1-based
    
    # Convert to time
    result = await bridge.call_lua("TimeMap2_QNToTime", [0, beat_qn])
    
    if result.get("ok"):
        time = result.get("ret", 0.0)
        return f"Measure {measure+1}, Beat {beat} = {time:.3f} seconds"
    else:
        raise Exception(f"Failed to calculate beat time: {result.get('error', 'Unknown error')}")


async def get_measure_from_beat(beat_position: float) -> str:
    """Get measure number from absolute beat position"""
    # Assuming 4/4 time for simplicity (would need to iterate through tempo map for accuracy)
    qn = beat_position - 1.0  # Convert to 0-based quarter notes
    
    result = await bridge.call_lua("TimeMap_QNToMeasures", [0, qn])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, measures = ret[:2]
            if retval >= 0:
                return f"Beat {beat_position:.2f} is in measure {measures + 1}"
            else:
                return f"Failed to calculate measure for beat {beat_position}"
        else:
            return "Invalid measure data"
    else:
        raise Exception(f"Failed to get measure from beat: {result.get('error', 'Unknown error')}")


async def align_time_to_grid(time: float, grid_division: str = "1/4") -> str:
    """Align time position to musical grid"""
    # Parse grid division
    grid_map = {
        "1": 1.0,      # whole note
        "1/2": 0.5,    # half note
        "1/4": 0.25,   # quarter note
        "1/8": 0.125,  # eighth note
        "1/16": 0.0625,  # sixteenth note
        "1/32": 0.03125, # thirty-second note
    }
    
    grid_qn = grid_map.get(grid_division, 0.25) * 4.0  # Convert to quarter notes
    
    # Convert time to QN
    qn_result = await bridge.call_lua("TimeMap2_timeToQN", [time])
    if not qn_result.get("ok"):
        raise Exception("Failed to convert time to QN")
    
    qn = qn_result.get("ret", 0.0)
    
    # Align to grid
    aligned_qn = round(qn / grid_qn) * grid_qn
    
    # Convert back to time
    result = await bridge.call_lua("TimeMap2_QNToTime", [0, aligned_qn])
    
    if result.get("ok"):
        aligned_time = result.get("ret", 0.0)
        return f"Aligned {time:.3f}s to {grid_division} grid: {aligned_time:.3f}s"
    else:
        raise Exception(f"Failed to align to grid: {result.get('error', 'Unknown error')}")


async def get_loop_time_range() -> str:
    """Get current loop/time selection in musical time"""
    result = await bridge.call_lua("GetSet_LoopTimeRange", [False, False, 0, 0, False])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            start_time, end_time = ret[:2]
            
            # Convert to musical time
            start_qn_result = await bridge.call_lua("TimeMap2_timeToQN", [start_time])
            end_qn_result = await bridge.call_lua("TimeMap2_timeToQN", [end_time])
            
            if start_qn_result.get("ok") and end_qn_result.get("ok"):
                start_qn = start_qn_result.get("ret", 0.0)
                end_qn = end_qn_result.get("ret", 0.0)
                duration_qn = end_qn - start_qn
                
                # Get measure info
                start_measure_result = await bridge.call_lua("TimeMap_QNToMeasures", [0, start_qn])
                end_measure_result = await bridge.call_lua("TimeMap_QNToMeasures", [0, end_qn])
                
                if start_measure_result.get("ok") and end_measure_result.get("ok"):
                    start_ret = start_measure_result.get("ret", [])
                    end_ret = end_measure_result.get("ret", [])
                    
                    if len(start_ret) >= 4 and len(end_ret) >= 4:
                        _, start_measure, _, start_beat = start_ret[:4]
                        _, end_measure, _, end_beat = end_ret[:4]
                        
                        return (f"Loop: {start_time:.3f}s to {end_time:.3f}s "
                               f"(Measure {start_measure+1}.{start_beat+1:.1f} to "
                               f"Measure {end_measure+1}.{end_beat+1:.1f}, "
                               f"{duration_qn:.2f} quarter notes)")
                
                return f"Loop: {start_time:.3f}s to {end_time:.3f}s ({duration_qn:.2f} quarter notes)"
            else:
                return f"Loop: {start_time:.3f}s to {end_time:.3f}s"
        else:
            return "No time selection/loop"
    else:
        raise Exception(f"Failed to get loop time range: {result.get('error', 'Unknown error')}")


async def set_loop_to_measures(start_measure: int, end_measure: int) -> str:
    """Set loop points to specific measures"""
    # Get start measure info
    start_result = await bridge.call_lua("TimeMap_GetMeasureInfo", [0, start_measure])
    if not start_result.get("ok"):
        raise Exception("Failed to get start measure info")
    
    start_ret = start_result.get("ret", [])
    if not isinstance(start_ret, list) or len(start_ret) < 2:
        raise Exception("Invalid start measure data")
    
    _, start_qn = start_ret[:2]
    
    # Get end measure info
    end_result = await bridge.call_lua("TimeMap_GetMeasureInfo", [0, end_measure])
    if not end_result.get("ok"):
        raise Exception("Failed to get end measure info")
    
    end_ret = end_result.get("ret", [])
    if not isinstance(end_ret, list) or len(end_ret) < 2:
        raise Exception("Invalid end measure data")
    
    _, end_qn = end_ret[:2]
    
    # Convert to time
    start_time_result = await bridge.call_lua("TimeMap2_QNToTime", [0, start_qn])
    end_time_result = await bridge.call_lua("TimeMap2_QNToTime", [0, end_qn])
    
    if not (start_time_result.get("ok") and end_time_result.get("ok")):
        raise Exception("Failed to convert measures to time")
    
    start_time = start_time_result.get("ret", 0.0)
    end_time = end_time_result.get("ret", 0.0)
    
    # Set loop
    result = await bridge.call_lua("GetSet_LoopTimeRange", [True, True, start_time, end_time, False])
    
    if result.get("ok"):
        return f"Set loop to measures {start_measure+1} through {end_measure+1}"
    else:
        raise Exception(f"Failed to set loop: {result.get('error', 'Unknown error')}")


async def calculate_tempo_from_selection() -> str:
    """Calculate tempo based on time selection and beat count"""
    # Get time selection
    sel_result = await bridge.call_lua("GetSet_LoopTimeRange", [False, False, 0, 0, False])
    if not sel_result.get("ok"):
        raise Exception("Failed to get time selection")
    
    ret = sel_result.get("ret", [])
    if not isinstance(ret, list) or len(ret) < 2:
        return "No time selection"
    
    start_time, end_time = ret[:2]
    duration = end_time - start_time
    
    if duration <= 0:
        return "No time selection or invalid selection"
    
    # Assume selection is 4 beats (1 measure of 4/4)
    # In a real implementation, we'd ask the user for beat count
    beat_count = 4.0
    
    # Calculate tempo
    seconds_per_beat = duration / beat_count
    bpm = 60.0 / seconds_per_beat
    
    return (f"Selection duration: {duration:.3f} seconds\n"
           f"Assuming {beat_count} beats: {bpm:.2f} BPM")


# ============================================================================
# Tempo Map Operations (4 tools)
# ============================================================================

async def get_tempo_map_points(start_time: float = 0.0, end_time: float = 300.0) -> str:
    """Get all tempo changes in time range"""
    # Count tempo markers
    count_result = await bridge.call_lua("CountTempoTimeSigMarkers", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count tempo markers")
    
    count = count_result.get("ret", 0)
    tempo_points = []
    
    for i in range(count):
        marker_result = await bridge.call_lua("GetTempoTimeSigMarker", [0, i])
        if marker_result.get("ok"):
            ret = marker_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 5:
                retval, timepos, measurepos, beatpos, bpm = ret[:5]
                if retval and start_time <= timepos <= end_time:
                    tempo_points.append((timepos, bpm, measurepos))
    
    if tempo_points:
        result = "Tempo map points:\n"
        for time, bpm, measure in tempo_points:
            result += f"  {time:.3f}s (measure {measure}): {bpm:.2f} BPM\n"
        return result.rstrip()
    else:
        return f"No tempo changes found between {start_time:.3f}s and {end_time:.3f}s"


async def smooth_tempo_transition(start_time: float, end_time: float, 
                                 start_bpm: float, end_bpm: float, 
                                 points: int = 10) -> str:
    """Create smooth tempo transition between two points"""
    if points < 2:
        points = 2
    
    created = 0
    time_step = (end_time - start_time) / (points - 1)
    bpm_step = (end_bpm - start_bpm) / (points - 1)
    
    for i in range(points):
        time = start_time + (i * time_step)
        bpm = start_bpm + (i * bpm_step)
        
        result = await bridge.call_lua("SetTempoTimeSigMarker", [
            0,      # project
            -1,     # marker index (-1 = insert new)
            time,
            -1,     # measure position
            0.0,    # beat position
            bpm,
            0,      # timesig_num (don't change)
            0,      # timesig_denom (don't change)
            True    # linear tempo
        ])
        
        if result.get("ok") and result.get("ret"):
            created += 1
    
    return (f"Created smooth tempo transition: {start_bpm:.2f} to {end_bpm:.2f} BPM "
           f"over {end_time - start_time:.3f} seconds with {created} points")


async def clear_tempo_map(start_time: float = 0.0, end_time: Optional[float] = None) -> str:
    """Clear tempo markers in time range"""
    # If no end time, clear all after start time
    if end_time is None:
        end_time = 3600.0  # 1 hour
    
    # Get all tempo markers
    count_result = await bridge.call_lua("CountTempoTimeSigMarkers", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count tempo markers")
    
    count = count_result.get("ret", 0)
    deleted = 0
    
    # Iterate backwards to avoid index shifting
    for i in range(count - 1, -1, -1):
        marker_result = await bridge.call_lua("GetTempoTimeSigMarker", [0, i])
        if marker_result.get("ok"):
            ret = marker_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 2:
                retval, timepos = ret[:2]
                if retval and start_time <= timepos <= end_time:
                    # Delete this marker
                    del_result = await bridge.call_lua("DeleteTempoTimeSigMarker", [0, i])
                    if del_result.get("ok") and del_result.get("ret"):
                        deleted += 1
    
    return f"Deleted {deleted} tempo markers between {start_time:.3f}s and {end_time:.3f}s"


async def export_tempo_map() -> str:
    """Export tempo map as text"""
    # Count tempo markers
    count_result = await bridge.call_lua("CountTempoTimeSigMarkers", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count tempo markers")
    
    count = count_result.get("ret", 0)
    if count == 0:
        return "No tempo markers in project"
    
    tempo_map = "Tempo Map Export:\n"
    tempo_map += "Time (s) | Measure | Beat | BPM | Time Sig | Type\n"
    tempo_map += "-" * 50 + "\n"
    
    for i in range(count):
        marker_result = await bridge.call_lua("GetTempoTimeSigMarker", [0, i])
        if marker_result.get("ok"):
            ret = marker_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 8:
                retval, timepos, measurepos, beatpos, bpm, timesig_num, timesig_denom, lineartempo = ret[:8]
                if retval:
                    tempo_type = "Linear" if lineartempo else "Jump"
                    tempo_map += (f"{timepos:8.3f} | {measurepos:7d} | {beatpos:4.1f} | "
                                 f"{bpm:6.2f} | {timesig_num:2d}/{timesig_denom:<2d} | {tempo_type}\n")
    
    return tempo_map.rstrip()


# ============================================================================
# Registration Function
# ============================================================================

def register_tempo_time_signature_tools(mcp) -> int:
    """Register all tempo & time signature tools with the MCP instance"""
    tools = [
        # Tempo Operations
        (get_project_tempo, "Get the current project tempo at edit cursor"),
        (set_project_tempo, "Set project tempo at position"),
        (get_tempo_at_time, "Get tempo at specific time position"),
        (count_tempo_markers, "Count tempo/time signature markers in project"),
        (get_tempo_marker_info, "Get information about a tempo/time signature marker"),
        (delete_tempo_marker, "Delete a tempo/time signature marker"),
        (find_tempo_marker_at_time, "Find tempo marker at or before specific time"),
        (update_timeline_for_tempo_changes, "Update timeline display after tempo changes"),
        
        # Time Signature Operations
        (get_time_signature_at_time, "Get time signature at specific time"),
        (set_time_signature, "Set time signature at position"),
        (add_tempo_time_sig_change, "Add tempo and time signature change at position"),
        (get_measure_info, "Get information about a specific measure"),
        (beats_to_time, "Convert beats and measures to time position"),
        (time_to_beats, "Convert time position to beats and measures"),
        
        # Musical Time Calculations
        (quarter_notes_to_time, "Convert quarter note position to time"),
        (time_to_quarter_notes, "Convert time to quarter note position"),
        (calculate_beat_time, "Calculate time position of a specific beat in a measure"),
        (get_measure_from_beat, "Get measure number from absolute beat position"),
        (align_time_to_grid, "Align time position to musical grid"),
        (get_loop_time_range, "Get current loop/time selection in musical time"),
        (set_loop_to_measures, "Set loop points to specific measures"),
        (calculate_tempo_from_selection, "Calculate tempo based on time selection and beat count"),
        
        # Tempo Map Operations
        (get_tempo_map_points, "Get all tempo changes in time range"),
        (smooth_tempo_transition, "Create smooth tempo transition between two points"),
        (clear_tempo_map, "Clear tempo markers in time range"),
        (export_tempo_map, "Export tempo map as text"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)