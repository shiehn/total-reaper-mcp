"""
Envelope Extended Tools for REAPER MCP

This module contains extended tools for working with envelopes,
including advanced point manipulation, state management, and formatting.
"""

from typing import Optional, Tuple, List, Any, Dict
from ..bridge import bridge


# ============================================================================
# Envelope Point Range Operations (4 tools)
# ============================================================================

async def delete_envelope_point_range(track_index: int, envelope_index: int, 
                                    start_time: float, end_time: float) -> str:
    """Delete envelope points within a time range"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Delete points in range
    result = await bridge.call_lua("DeleteEnvelopePointRange", [env_handle, start_time, end_time])
    
    if result.get("ok"):
        deleted = result.get("ret", False)
        if deleted:
            return f"Deleted envelope points between {start_time:.3f}s and {end_time:.3f}s"
        else:
            return "No points found in specified range"
    else:
        raise Exception(f"Failed to delete envelope point range: {result.get('error', 'Unknown error')}")


async def delete_envelope_point_range_ex(track_index: int, envelope_index: int,
                                       automation_item_index: int,
                                       start_time: float, end_time: float) -> str:
    """Delete envelope points within a time range (extended for automation items)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Delete points in range (extended)
    result = await bridge.call_lua("DeleteEnvelopePointRangeEx", 
                                 [env_handle, automation_item_index, start_time, end_time])
    
    if result.get("ok"):
        deleted = result.get("ret", False)
        if deleted:
            return f"Deleted envelope points in automation item {automation_item_index} between {start_time:.3f}s and {end_time:.3f}s"
        else:
            return "No points found in specified range"
    else:
        raise Exception(f"Failed to delete envelope point range ex: {result.get('error', 'Unknown error')}")


async def envelope_sort_points(track_index: int, envelope_index: int) -> str:
    """Sort all envelope points by time"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Sort points
    result = await bridge.call_lua("Envelope_SortPoints", [env_handle])
    
    if result.get("ok"):
        sorted_ok = result.get("ret", False)
        if sorted_ok:
            return "Envelope points sorted successfully"
        else:
            return "Envelope points already sorted or sort failed"
    else:
        raise Exception(f"Failed to sort envelope points: {result.get('error', 'Unknown error')}")


async def envelope_sort_points_ex(track_index: int, envelope_index: int, 
                                automation_item_index: int) -> str:
    """Sort envelope points by time (extended for automation items)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Sort points (extended)
    result = await bridge.call_lua("Envelope_SortPointsEx", [env_handle, automation_item_index])
    
    if result.get("ok"):
        sorted_ok = result.get("ret", False)
        if sorted_ok:
            return f"Sorted envelope points in automation item {automation_item_index}"
        else:
            return "Points already sorted or sort failed"
    else:
        raise Exception(f"Failed to sort envelope points ex: {result.get('error', 'Unknown error')}")


# ============================================================================
# Envelope Evaluation & Information (8 tools)
# ============================================================================

async def envelope_evaluate(track_index: int, envelope_index: int, 
                           time: float, sample_rate: int = 0, 
                           get_value_only: bool = True) -> str:
    """Evaluate envelope value at specific time"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Evaluate envelope
    result = await bridge.call_lua("Envelope_Evaluate", [env_handle, time, sample_rate, get_value_only])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 4:
            value, first_point, last_point, details = ret[:4]
            return f"Envelope value at {time:.3f}s: {value:.4f} (points {first_point}-{last_point})"
        else:
            return f"Failed to evaluate envelope at time {time}"
    else:
        raise Exception(f"Failed to evaluate envelope: {result.get('error', 'Unknown error')}")


async def envelope_format_value(track_index: int, envelope_index: int, value: float) -> str:
    """Format envelope value for display"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Format value
    result = await bridge.call_lua("Envelope_FormatValue", [env_handle, value, "", 256])
    
    if result.get("ok"):
        formatted = result.get("ret", "")
        if formatted:
            return f"Formatted value: {formatted}"
        else:
            return f"Value: {value:.4f}"
    else:
        raise Exception(f"Failed to format envelope value: {result.get('error', 'Unknown error')}")


async def get_envelope_info_value(track_index: int, envelope_index: int, param_name: str) -> str:
    """Get envelope parameter value"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Get info value
    result = await bridge.call_lua("GetEnvelopeInfo_Value", [env_handle, param_name])
    
    if result.get("ok"):
        value = result.get("ret", 0.0)
        return f"Envelope {param_name}: {value}"
    else:
        raise Exception(f"Failed to get envelope info value: {result.get('error', 'Unknown error')}")


async def get_envelope_name(track_index: int, envelope_index: int) -> str:
    """Get envelope name"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Get name
    result = await bridge.call_lua("GetEnvelopeName", [env_handle, "", 256])
    
    if result.get("ok"):
        name = result.get("ret", "")
        if name:
            return f"Envelope name: {name}"
        else:
            return "Envelope has no name"
    else:
        raise Exception(f"Failed to get envelope name: {result.get('error', 'Unknown error')}")


async def get_envelope_scaling_mode(track_index: int, envelope_index: int) -> str:
    """Get envelope scaling mode"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Get scaling mode
    result = await bridge.call_lua("GetEnvelopeScalingMode", [env_handle])
    
    if result.get("ok"):
        mode = result.get("ret", 0)
        mode_names = {0: "absolute", 1: "normalized"}
        mode_name = mode_names.get(mode, f"mode {mode}")
        return f"Envelope scaling mode: {mode_name}"
    else:
        raise Exception(f"Failed to get envelope scaling mode: {result.get('error', 'Unknown error')}")


async def envelope_get_parent_track(track_index: int, envelope_index: int) -> str:
    """Get parent track of envelope"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Get parent track
    result = await bridge.call_lua("Envelope_GetParentTrack", [env_handle])
    
    if result.get("ok"):
        parent_track = result.get("ret")
        if parent_track:
            # Get track name
            name_result = await bridge.call_lua("GetTrackName", [parent_track, "", 256])
            track_name = name_result.get("ret", "Unnamed") if name_result.get("ok") else "Unknown"
            return f"Envelope parent track: {track_name}"
        else:
            return "Envelope has no parent track"
    else:
        raise Exception(f"Failed to get envelope parent track: {result.get('error', 'Unknown error')}")


async def envelope_get_parent_take(item_index: int, take_index: int, envelope_index: int) -> str:
    """Get parent take of envelope"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get take envelope
    env_result = await bridge.call_lua("GetTakeEnvelope", [take_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find take envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Get parent take
    result = await bridge.call_lua("Envelope_GetParentTake", [env_handle])
    
    if result.get("ok"):
        parent_take = result.get("ret")
        if parent_take:
            # Get take name
            name_result = await bridge.call_lua("GetTakeName", [parent_take])
            take_name = name_result.get("ret", "Unnamed") if name_result.get("ok") else "Unknown"
            return f"Envelope parent take: {take_name}"
        else:
            return "Envelope has no parent take"
    else:
        raise Exception(f"Failed to get envelope parent take: {result.get('error', 'Unknown error')}")


async def get_track_envelope_by_chunk_name(track_index: int, chunk_name: str) -> str:
    """Get track envelope by chunk name"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope by chunk name
    result = await bridge.call_lua("GetTrackEnvelopeByChunkName", [track_handle, chunk_name])
    
    if result.get("ok"):
        envelope = result.get("ret")
        if envelope:
            # Get envelope name
            name_result = await bridge.call_lua("GetEnvelopeName", [envelope, "", 256])
            env_name = name_result.get("ret", "Unnamed") if name_result.get("ok") else "Unknown"
            return f"Found envelope '{env_name}' with chunk name '{chunk_name}'"
        else:
            return f"No envelope found with chunk name '{chunk_name}'"
    else:
        raise Exception(f"Failed to get envelope by chunk name: {result.get('error', 'Unknown error')}")


# ============================================================================
# Envelope State Management (4 tools)
# ============================================================================

async def get_envelope_state_chunk(track_index: int, envelope_index: int, is_undo: bool = False) -> str:
    """Get envelope state chunk"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Get state chunk
    result = await bridge.call_lua("GetEnvelopeStateChunk", [env_handle, "", 65536, is_undo])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            success, chunk = ret[:2]
            if success and chunk:
                # Return first 200 chars of chunk
                preview = chunk[:200] + "..." if len(chunk) > 200 else chunk
                return f"Envelope state chunk ({len(chunk)} chars): {preview}"
            else:
                return "Failed to get envelope state chunk"
        else:
            return "Invalid envelope state chunk response"
    else:
        raise Exception(f"Failed to get envelope state chunk: {result.get('error', 'Unknown error')}")


async def set_envelope_state_chunk(track_index: int, envelope_index: int, 
                                 chunk: str, is_undo: bool = False) -> str:
    """Set envelope state chunk"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Set state chunk
    result = await bridge.call_lua("SetEnvelopeStateChunk", [env_handle, chunk, is_undo])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set envelope state chunk ({len(chunk)} chars)"
        else:
            return "Failed to set envelope state chunk"
    else:
        raise Exception(f"Failed to set envelope state chunk: {result.get('error', 'Unknown error')}")


async def get_set_envelope_info_string(track_index: int, envelope_index: int,
                                     param_name: str, value: str = "", set_value: bool = False) -> str:
    """Get or set envelope string parameter"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Get/set info string
    result = await bridge.call_lua("GetSetEnvelopeInfo_String", [env_handle, param_name, value, set_value])
    
    if result.get("ok"):
        ret_value = result.get("ret", "")
        if set_value:
            return f"Set envelope {param_name} to: {value}"
        else:
            return f"Envelope {param_name}: {ret_value}"
    else:
        raise Exception(f"Failed to get/set envelope info string: {result.get('error', 'Unknown error')}")


async def get_set_envelope_state(track_index: int, envelope_index: int, 
                               state_data: str = "", set_state: bool = False) -> str:
    """Get or set complete envelope state"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Get/set state
    if set_state:
        result = await bridge.call_lua("GetSetEnvelopeState", [env_handle, state_data, 0])
    else:
        result = await bridge.call_lua("GetSetEnvelopeState", [env_handle, "", 65536])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            success, state = ret[:2]
            if success:
                if set_state:
                    return f"Set envelope state ({len(state_data)} chars)"
                else:
                    preview = state[:200] + "..." if len(state) > 200 else state
                    return f"Envelope state ({len(state)} chars): {preview}"
            else:
                return "Failed to get/set envelope state"
        else:
            return "Invalid envelope state response"
    else:
        raise Exception(f"Failed to get/set envelope state: {result.get('error', 'Unknown error')}")


# ============================================================================
# Envelope Scaling (2 tools)
# ============================================================================

async def scale_from_envelope_mode(track_index: int, envelope_index: int, value: float) -> str:
    """Scale value from envelope mode"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Scale from envelope mode
    result = await bridge.call_lua("ScaleFromEnvelopeMode", [env_handle, 1, value])
    
    if result.get("ok"):
        scaled_value = result.get("ret", value)
        return f"Scaled from envelope mode: {value:.4f} -> {scaled_value:.4f}"
    else:
        raise Exception(f"Failed to scale from envelope mode: {result.get('error', 'Unknown error')}")


async def scale_to_envelope_mode(track_index: int, envelope_index: int, value: float) -> str:
    """Scale value to envelope mode"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Scale to envelope mode
    result = await bridge.call_lua("ScaleToEnvelopeMode", [env_handle, 1, value])
    
    if result.get("ok"):
        scaled_value = result.get("ret", value)
        return f"Scaled to envelope mode: {value:.4f} -> {scaled_value:.4f}"
    else:
        raise Exception(f"Failed to scale to envelope mode: {result.get('error', 'Unknown error')}")


# ============================================================================
# Envelope Point Extended Operations (2 tools)
# ============================================================================

async def set_envelope_point_ex(track_index: int, envelope_index: int, 
                              automation_item_index: int, point_index: int,
                              time: Optional[float] = None, value: Optional[float] = None,
                              shape: Optional[int] = None, tension: Optional[float] = None,
                              selected: Optional[bool] = None) -> str:
    """Set envelope point with extended parameters"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Set point extended
    result = await bridge.call_lua("SetEnvelopePointEx", 
                                 [env_handle, automation_item_index, point_index, 
                                  time, value, shape, tension, selected, True])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            parts = []
            if time is not None: parts.append(f"time={time:.3f}s")
            if value is not None: parts.append(f"value={value:.4f}")
            if shape is not None: parts.append(f"shape={shape}")
            if tension is not None: parts.append(f"tension={tension:.2f}")
            if selected is not None: parts.append(f"selected={'yes' if selected else 'no'}")
            return f"Set envelope point {point_index}: {', '.join(parts)}"
        else:
            return f"Failed to set envelope point {point_index}"
    else:
        raise Exception(f"Failed to set envelope point ex: {result.get('error', 'Unknown error')}")


async def get_set_envelope_state2(track_index: int, envelope_index: int,
                                state_data: str = "", set_state: bool = False) -> str:
    """Get or set envelope state (version 2 with extra features)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelope", [track_handle, envelope_index])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope at index {envelope_index}")
    
    env_handle = env_result.get("ret")
    
    # Get/set state v2
    if set_state:
        result = await bridge.call_lua("GetSetEnvelopeState2", [env_handle, state_data, 0, 1])
    else:
        result = await bridge.call_lua("GetSetEnvelopeState2", [env_handle, "", 65536, 1])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            success, state = ret[:2]
            if success:
                if set_state:
                    return f"Set envelope state v2 ({len(state_data)} chars)"
                else:
                    preview = state[:200] + "..." if len(state) > 200 else state
                    return f"Envelope state v2 ({len(state)} chars): {preview}"
            else:
                return "Failed to get/set envelope state v2"
        else:
            return "Invalid envelope state v2 response"
    else:
        raise Exception(f"Failed to get/set envelope state v2: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_envelope_extended_tools(mcp) -> int:
    """Register all envelope extended tools with the MCP instance"""
    tools = [
        # Envelope Point Range Operations
        (delete_envelope_point_range, "Delete envelope points within a time range"),
        (delete_envelope_point_range_ex, "Delete envelope points within a time range (extended)"),
        (envelope_sort_points, "Sort all envelope points by time"),
        (envelope_sort_points_ex, "Sort envelope points by time (extended)"),
        
        # Envelope Evaluation & Information
        (envelope_evaluate, "Evaluate envelope value at specific time"),
        (envelope_format_value, "Format envelope value for display"),
        (get_envelope_info_value, "Get envelope parameter value"),
        (get_envelope_name, "Get envelope name"),
        (get_envelope_scaling_mode, "Get envelope scaling mode"),
        (envelope_get_parent_track, "Get parent track of envelope"),
        (envelope_get_parent_take, "Get parent take of envelope"),
        (get_track_envelope_by_chunk_name, "Get track envelope by chunk name"),
        
        # Envelope State Management
        (get_envelope_state_chunk, "Get envelope state chunk"),
        (set_envelope_state_chunk, "Set envelope state chunk"),
        (get_set_envelope_info_string, "Get or set envelope string parameter"),
        (get_set_envelope_state, "Get or set complete envelope state"),
        
        # Envelope Scaling
        (scale_from_envelope_mode, "Scale value from envelope mode"),
        (scale_to_envelope_mode, "Scale value to envelope mode"),
        
        # Envelope Point Extended Operations
        (set_envelope_point_ex, "Set envelope point with extended parameters"),
        (get_set_envelope_state2, "Get or set envelope state (v2)"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)