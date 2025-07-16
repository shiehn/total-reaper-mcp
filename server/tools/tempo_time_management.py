"""Tempo and time management tools for music production."""

from typing import Dict, Any, List, Optional, Tuple
from .bridge_sync import ReaperBridge


def get_master_tempo() -> Dict[str, Any]:
    """Get the current master tempo of the project.
    
    Returns:
        Dict containing:
        - tempo: Current tempo in BPM
        - success: Operation success status
    """
    request = {"action": "Master_GetTempo"}
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "tempo": response.get("tempo", 120.0)
    }


def set_current_bpm(bpm: float, allow_undo: bool = True) -> Dict[str, Any]:
    """Set the current project tempo.
    
    Args:
        bpm: Tempo in beats per minute
        allow_undo: Whether to create an undo point
    
    Returns:
        Dict containing operation result
    """
    if bpm < 10 or bpm > 960:
        return {
            "success": False,
            "error": "BPM must be between 10 and 960"
        }
    
    request = {
        "action": "SetCurrentBPM",
        "bpm": bpm,
        "wantUndo": allow_undo
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "bpm": bpm
    }


def get_play_position() -> Dict[str, Any]:
    """Get the current playback position.
    
    Returns:
        Dict containing:
        - position: Current play position in seconds
        - is_playing: Whether transport is playing
        - is_recording: Whether transport is recording
    """
    request = {"action": "GetPlayPosition"}
    response = ReaperBridge.send_request(request)
    
    position = response.get("position", 0.0)
    
    # Get play state
    state_request = {"action": "GetPlayState"}
    state_response = ReaperBridge.send_request(state_request)
    play_state = state_response.get("state", 0)
    
    return {
        "success": True,
        "position": position,
        "is_playing": play_state & 1 != 0,
        "is_recording": play_state & 4 != 0,
        "is_paused": play_state & 2 != 0
    }


def get_play_position_ex() -> Dict[str, Any]:
    """Get extended playback position information.
    
    Returns:
        Dict containing:
        - position: Current position in seconds
        - is_playing: Whether playing
        - is_paused: Whether paused
        - is_recording: Whether recording
        - time_since_last_play: Time since last play start
    """
    request = {"action": "GetPlayPosition2"}
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "position": response.get("position", 0.0),
        "is_playing": response.get("isPlaying", False),
        "is_paused": response.get("isPaused", False),
        "is_recording": response.get("isRecording", False),
        "time_since_last_play": response.get("timeSinceLastPlay", 0.0)
    }


def get_project_time_signature(position: float) -> Dict[str, Any]:
    """Get the time signature at a specific position.
    
    Args:
        position: Position in seconds
    
    Returns:
        Dict containing:
        - numerator: Time signature numerator (e.g., 4)
        - denominator: Time signature denominator (e.g., 4)
        - tempo: Tempo at position
    """
    request = {
        "action": "TimeMap_GetTimeSigAtTime",
        "project": 0,
        "time": position
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "numerator": response.get("timesig_num", 4),
        "denominator": response.get("timesig_denom", 4),
        "tempo": response.get("tempo", 120.0)
    }


def time_to_beats(time: float) -> Dict[str, Any]:
    """Convert time in seconds to musical beats.
    
    Args:
        time: Time in seconds
    
    Returns:
        Dict containing:
        - beats: Position in beats
        - measures: Position in measures
        - beats_in_measure: Beats within current measure
    """
    request = {
        "action": "TimeMap2_timeToBeats",
        "project": 0,
        "time": time
    }
    response = ReaperBridge.send_request(request)
    
    beats = response.get("beats", 0.0)
    measures = int(beats / 4)  # Assuming 4/4 time
    beats_in_measure = beats % 4
    
    return {
        "success": response.get("result", False),
        "beats": beats,
        "measures": measures,
        "beats_in_measure": beats_in_measure
    }


def beats_to_time(beats: float) -> Dict[str, Any]:
    """Convert musical beats to time in seconds.
    
    Args:
        beats: Position in beats
    
    Returns:
        Dict containing:
        - time: Time in seconds
    """
    request = {
        "action": "TimeMap2_beatsToTime",
        "project": 0,
        "beats": beats
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "time": response.get("time", 0.0)
    }


def snap_to_grid(position: float) -> Dict[str, Any]:
    """Snap a time position to the project grid.
    
    Args:
        position: Time position in seconds
    
    Returns:
        Dict containing:
        - snapped_position: Grid-snapped position
        - original_position: Original position
    """
    request = {
        "action": "SnapToGrid",
        "project": 0,
        "time": position
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "snapped_position": response.get("snapped_time", position),
        "original_position": position
    }


def get_loop_time_range() -> Dict[str, Any]:
    """Get the current loop time range (simplified version).
    
    Returns:
        Dict containing:
        - start: Loop start time
        - end: Loop end time
        - is_set: Whether loop is set
    """
    request = {
        "action": "GetSet_LoopTimeRange",
        "isSet": False,
        "isLoop": True,
        "startOut": 0.0,
        "endOut": 0.0,
        "allowautoseek": False
    }
    response = ReaperBridge.send_request(request)
    
    start = response.get("startOut", 0.0)
    end = response.get("endOut", 0.0)
    
    return {
        "success": True,
        "start": start,
        "end": end,
        "is_set": end > start
    }


def set_loop_time_range(start: float, end: float) -> Dict[str, Any]:
    """Set the loop time range directly.
    
    Args:
        start: Loop start time in seconds
        end: Loop end time in seconds
    
    Returns:
        Dict containing operation result
    """
    request = {
        "action": "GetSet_LoopTimeRange",
        "isSet": True,
        "isLoop": True,
        "startOut": start,
        "endOut": end,
        "allowautoseek": False
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "start": start,
        "end": end
    }


def add_tempo_marker(position: float, bpm: float, time_sig_num: int = 4, 
                    time_sig_denom: int = 4) -> Dict[str, Any]:
    """Add a tempo/time signature marker.
    
    Args:
        position: Position in seconds
        bpm: Tempo in BPM
        time_sig_num: Time signature numerator
        time_sig_denom: Time signature denominator
    
    Returns:
        Dict containing operation result
    """
    request = {
        "action": "SetTempoTimeSigMarker",
        "project": 0,
        "ptidx": -1,  # Add new
        "timepos": position,
        "measurepos": -1,
        "beatpos": -1,
        "bpm": bpm,
        "timesig_num": time_sig_num,
        "timesig_denom": time_sig_denom,
        "lineartempo": False
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "position": position,
        "bpm": bpm,
        "time_signature": f"{time_sig_num}/{time_sig_denom}"
    }


def delete_tempo_marker(index: int) -> Dict[str, Any]:
    """Delete a tempo/time signature marker.
    
    Args:
        index: Tempo marker index
    
    Returns:
        Dict containing operation result
    """
    request = {
        "action": "DeleteTempoTimeSigMarker",
        "project": 0,
        "markeridx": index
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "deleted_index": index
    }


def count_tempo_markers() -> Dict[str, Any]:
    """Count tempo/time signature markers in project.
    
    Returns:
        Dict containing marker count
    """
    request = {
        "action": "CountTempoTimeSigMarkers",
        "project": 0
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": True,
        "count": response.get("count", 0)
    }


def format_time(seconds: float, format_string: str = "") -> Dict[str, Any]:
    """Format time value as string.
    
    Args:
        seconds: Time in seconds
        format_string: Format string (empty for default)
    
    Returns:
        Dict containing formatted time string
    """
    request = {
        "action": "format_timestr",
        "time": seconds,
        "format": format_string
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "formatted": response.get("formatted", "0:00.000")
    }


def parse_time_string(time_string: str) -> Dict[str, Any]:
    """Parse a time string to seconds.
    
    Args:
        time_string: Time string (e.g., "1:30", "90", "1.5m")
    
    Returns:
        Dict containing time in seconds
    """
    request = {
        "action": "parse_timestr",
        "time_string": time_string
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "seconds": response.get("time", 0.0)
    }


def register_tempo_time_tools(mcp):
    """Register tempo and time management tools with MCP server."""
    from functools import wraps
    
    # Helper to wrap sync functions for async
    def async_wrapper(func):
        @wraps(func)
        async def wrapper(**kwargs):
            return func(**kwargs)
        return wrapper
    
    # Register all tempo/time tools
    tool_functions = [
        ("get_master_tempo", get_master_tempo),
        ("set_current_bpm", set_current_bpm),
        ("get_play_position", get_play_position),
        ("get_play_position_ex", get_play_position_ex),
        ("get_project_time_signature", get_project_time_signature),
        ("time_to_beats", time_to_beats),
        ("beats_to_time", beats_to_time),
        ("snap_to_grid", snap_to_grid),
        ("get_loop_time_range", get_loop_time_range),
        ("set_loop_time_range", set_loop_time_range),
        ("add_tempo_marker", add_tempo_marker),
        ("delete_tempo_marker", delete_tempo_marker),
        ("count_tempo_markers", count_tempo_markers),
        ("format_time", format_time),
        ("parse_time_string", parse_time_string),
    ]
    
    # Find the corresponding tool definition and register
    for tool_name, tool_func in tool_functions:
        tool_def = next((t for t in tools if t["name"] == tool_name), None)
        if tool_def:
            mcp.tool(
                name=tool_name,
                description=tool_def["description"]
            )(async_wrapper(tool_func))
    
    return len(tool_functions)


# Tool definitions for MCP
tools = [
    {
        "name": "get_master_tempo",
        "description": "Get the current master tempo of the project in BPM. Returns the global project tempo setting. Use this to understand the musical timing context before generating patterns or making tempo-relative decisions.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "set_current_bpm",
        "description": "Set the project's master tempo in BPM. Changes the global tempo for the entire project. Valid range is 10-960 BPM. Creates an undo point by default. Use for tempo changes in generative compositions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "bpm": {"type": "number", "description": "Tempo in beats per minute (10-960)"},
                "allow_undo": {"type": "boolean", "description": "Create undo point", "default": True}
            },
            "required": ["bpm"]
        }
    },
    {
        "name": "get_play_position",
        "description": "Get the current playback position and transport state. Returns position in seconds and whether transport is playing, recording, or paused. Essential for reactive/generative systems that respond to playback state.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_play_position_ex",
        "description": "Get extended playback position information including time since last play. Provides more detailed transport state for advanced generative systems. Useful for timing-based triggers and reactive compositions.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_project_time_signature",
        "description": "Get the time signature and tempo at a specific position in the project. Returns numerator, denominator, and tempo. Essential for generating rhythmically appropriate patterns that match the musical context.",
        "input_schema": {
            "type": "object",
            "properties": {
                "position": {"type": "number", "description": "Position in seconds"}
            },
            "required": ["position"]
        }
    },
    {
        "name": "time_to_beats",
        "description": "Convert time in seconds to musical beats based on project tempo. Returns total beats, measures, and beats within measure. Use for musical timing calculations and aligning generated content to bars/beats.",
        "input_schema": {
            "type": "object",
            "properties": {
                "time": {"type": "number", "description": "Time in seconds"}
            },
            "required": ["time"]
        }
    },
    {
        "name": "beats_to_time",
        "description": "Convert musical beats to time in seconds based on project tempo. Inverse of time_to_beats. Use when you need to position items at specific musical locations like 'bar 4, beat 2'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "beats": {"type": "number", "description": "Position in beats"}
            },
            "required": ["beats"]
        }
    },
    {
        "name": "snap_to_grid",
        "description": "Snap a time position to the nearest grid point based on current grid settings. Returns the snapped position. Essential for ensuring generated content aligns with the project grid for clean timing.",
        "input_schema": {
            "type": "object",
            "properties": {
                "position": {"type": "number", "description": "Time position to snap"}
            },
            "required": ["position"]
        }
    },
    {
        "name": "get_loop_time_range",
        "description": "Get the current loop/time selection range. Simplified version that returns start, end, and whether a loop is set. Use to check the current loop region for loop-based generation.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "set_loop_time_range",
        "description": "Set the loop/time selection range directly by specifying start and end times. Creates or updates the loop region. More direct than set_time_selection when you just need basic loop points.",
        "input_schema": {
            "type": "object",
            "properties": {
                "start": {"type": "number", "description": "Loop start in seconds"},
                "end": {"type": "number", "description": "Loop end in seconds"}
            },
            "required": ["start", "end"]
        }
    },
    {
        "name": "add_tempo_marker",
        "description": "Add a tempo and/or time signature change marker at a specific position. Use for creating tempo maps, accelerandos, or metric modulations. Essential for dynamic compositions with varying tempos.",
        "input_schema": {
            "type": "object",
            "properties": {
                "position": {"type": "number", "description": "Position in seconds"},
                "bpm": {"type": "number", "description": "Tempo in BPM"},
                "time_sig_num": {"type": "integer", "description": "Time signature numerator", "default": 4},
                "time_sig_denom": {"type": "integer", "description": "Time signature denominator", "default": 4}
            },
            "required": ["position", "bpm"]
        }
    },
    {
        "name": "delete_tempo_marker",
        "description": "Delete a tempo/time signature marker by index. Use to clean up tempo maps or remove unwanted tempo changes. Get marker count first to know valid indices.",
        "input_schema": {
            "type": "object",
            "properties": {
                "index": {"type": "integer", "description": "Tempo marker index to delete"}
            },
            "required": ["index"]
        }
    },
    {
        "name": "count_tempo_markers",
        "description": "Count the number of tempo/time signature markers in the project. Use before deleting or iterating through tempo markers to know the valid index range.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "format_time",
        "description": "Format a time value in seconds as a human-readable string. Uses project time format by default. Useful for displaying times to users or logging. Returns formatted string like '1:30.000' or '2|1|00'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "seconds": {"type": "number", "description": "Time in seconds to format"},
                "format_string": {"type": "string", "description": "Format string (empty for default)", "default": ""}
            },
            "required": ["seconds"]
        }
    },
    {
        "name": "parse_time_string",
        "description": "Parse a time string to seconds. Accepts various formats like '1:30', '90', '1.5m', '2|1|00'. Useful for converting user input or time representations to seconds for calculations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "time_string": {"type": "string", "description": "Time string to parse"}
            },
            "required": ["time_string"]
        }
    }
]