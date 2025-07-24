"""Advanced MIDI generation and manipulation tools."""

from typing import Dict, Any, List, Optional, Tuple
from .bridge_sync import ReaperBridge


def create_new_midi_item(track_index: int, start_time: float, end_time: float,
                        start_in_qn: Optional[float] = None) -> Dict[str, Any]:
    """Create a new MIDI item on a track.
    
    Args:
        track_index: Index of the track
        start_time: Start position in seconds
        end_time: End position in seconds
        start_in_qn: Start position in quarter notes (optional)
    
    Returns:
        Dict containing:
        - item: Item handle
        - take: Take handle for the MIDI item
        - success: Operation status
    """
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
    track_response = ReaperBridge.send_request(track_request)
    
    if not track_response.get("result"):
        return {
            "success": False,
            "error": f"Track at index {track_index} not found"
        }
    
    track_handle = track_response.get("track")
    
    # Create MIDI item
    request = {
        "action": "CreateNewMIDIItemInProj",
        "track": track_handle,
        "starttime": start_time,
        "endtime": end_time,
        "qnInOptional": start_in_qn is not None
    }
    
    if start_in_qn is not None:
        request["startInQN"] = start_in_qn
    
    response = ReaperBridge.send_request(request)
    
    if response.get("result"):
        item_handle = response.get("item")
        
        # Get the active take
        take_request = {
            "action": "GetActiveTake",
            "item": item_handle
        }
        take_response = ReaperBridge.send_request(take_request)
        
        return {
            "success": True,
            "item": item_handle,
            "take": take_response.get("take"),
            "track_index": track_index,
            "start_time": start_time,
            "end_time": end_time
        }
    
    return {
        "success": False,
        "error": "Failed to create MIDI item"
    }


def get_midi_hash(take_handle: Any) -> Dict[str, Any]:
    """Get hash of MIDI data for comparison/versioning.
    
    Args:
        take_handle: MIDI take handle
    
    Returns:
        Dict containing:
        - hash: MIDI content hash
        - notes_only: Whether hash includes only notes
    """
    request = {
        "action": "MIDI_GetHash",
        "take": take_handle,
        "notesonly": True
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "hash": response.get("hash", ""),
        "notes_only": True
    }


def get_ppq_position_from_time(take_handle: Any, time: float) -> Dict[str, Any]:
    """Convert time to MIDI PPQ position.
    
    Args:
        take_handle: MIDI take handle
        time: Time in seconds
    
    Returns:
        Dict containing PPQ position
    """
    request = {
        "action": "MIDI_GetPPQPosFromProjTime",
        "take": take_handle,
        "time": time
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "ppq_pos": response.get("ppqpos", 0.0)
    }


def get_ppq_pos_end_of_measure(take_handle: Any, ppq_pos: float) -> Dict[str, Any]:
    """Get PPQ position at the end of the measure containing the given position.
    
    Args:
        take_handle: MIDI take handle
        ppq_pos: PPQ position
    
    Returns:
        Dict containing end of measure PPQ position
    """
    request = {
        "action": "MIDI_GetPPQPos_EndOfMeasure",
        "take": take_handle,
        "ppqpos": ppq_pos
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "ppq_end": response.get("ppq_end", ppq_pos)
    }


def get_ppq_pos_start_of_measure(take_handle: Any, ppq_pos: float) -> Dict[str, Any]:
    """Get PPQ position at the start of the measure containing the given position.
    
    Args:
        take_handle: MIDI take handle  
        ppq_pos: PPQ position
    
    Returns:
        Dict containing start of measure PPQ position
    """
    request = {
        "action": "MIDI_GetPPQPos_StartOfMeasure",
        "take": take_handle,
        "ppqpos": ppq_pos
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "ppq_start": response.get("ppq_start", ppq_pos)
    }


def get_midi_grid(take_handle: Any) -> Dict[str, Any]:
    """Get MIDI editor grid settings for a take.
    
    Args:
        take_handle: MIDI take handle
    
    Returns:
        Dict containing:
        - division: Grid division (e.g., 0.25 for 1/4 note)
        - swing: Swing amount
        - notelen: Default note length
    """
    request = {
        "action": "MIDI_GetGrid",
        "take": take_handle
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "division": response.get("division", 0.25),
        "swing": response.get("swingamt", 0.0),
        "note_length": response.get("notelen", 0.25)
    }


def select_midi_notes(take_handle: Any, start_ppq: float, end_ppq: float,
                     channel: int = -1, pitch_low: int = 0, pitch_high: int = 127) -> Dict[str, Any]:
    """Select MIDI notes within specified criteria.
    
    Args:
        take_handle: MIDI take handle
        start_ppq: Start position in PPQ
        end_ppq: End position in PPQ
        channel: MIDI channel (-1 for all)
        pitch_low: Lowest pitch to select
        pitch_high: Highest pitch to select
    
    Returns:
        Dict containing number of notes selected
    """
    # First deselect all
    desel_request = {
        "action": "MIDI_SelectAll",
        "take": take_handle,
        "select": False
    }
    ReaperBridge.send_request(desel_request)
    
    # Count total notes
    count_request = {
        "action": "MIDI_CountEvts",
        "take": take_handle
    }
    count_response = ReaperBridge.send_request(count_request)
    note_count = count_response.get("notes", 0)
    
    selected = 0
    
    # Select notes matching criteria
    for i in range(note_count):
        note_request = {
            "action": "MIDI_GetNote",
            "take": take_handle,
            "noteidx": i
        }
        note_response = ReaperBridge.send_request(note_request)
        
        if note_response.get("result"):
            note_start = note_response.get("startppqpos", 0)
            note_end = note_response.get("endppqpos", 0)
            note_pitch = note_response.get("pitch", 60)
            note_chan = note_response.get("chan", 0)
            
            # Check if note matches criteria
            if (start_ppq <= note_start < end_ppq and
                pitch_low <= note_pitch <= pitch_high and
                (channel == -1 or channel == note_chan)):
                
                # Select the note
                set_request = {
                    "action": "MIDI_SetNote",
                    "take": take_handle,
                    "noteidx": i,
                    "selectedInOptional": True,
                    "mutedInOptional": note_response.get("muted", False),
                    "startppqposInOptional": note_start,
                    "endppqposInOptional": note_end,
                    "chanInOptional": note_chan,
                    "pitchInOptional": note_pitch,
                    "velInOptional": note_response.get("vel", 80),
                    "noSortInOptional": True
                }
                set_response = ReaperBridge.send_request(set_request)
                
                if set_response.get("result"):
                    selected += 1
    
    return {
        "success": True,
        "notes_selected": selected,
        "total_notes": note_count
    }


def get_track_midi_note_range(track_index: int) -> Dict[str, Any]:
    """Get MIDI note name range for a track.
    
    Args:
        track_index: Track index
    
    Returns:
        Dict containing note range info
    """
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
    track_response = ReaperBridge.send_request(track_request)
    
    if not track_response.get("result"):
        return {
            "success": False,
            "error": f"Track at index {track_index} not found"
        }
    
    track_handle = track_response.get("track")
    
    # Get note range
    range_request = {
        "action": "GetTrackMIDINoteRange",
        "track": track_handle
    }
    range_response = ReaperBridge.send_request(range_request)
    
    return {
        "success": range_response.get("result", False),
        "note_low": range_response.get("note_lo", 0),
        "note_high": range_response.get("note_hi", 127)
    }


def set_track_midi_note_range(track_index: int, note_low: int, note_high: int) -> Dict[str, Any]:
    """Set MIDI note range constraints for a track.
    
    Args:
        track_index: Track index
        note_low: Lowest allowed note (0-127)
        note_high: Highest allowed note (0-127)
    
    Returns:
        Dict containing operation result
    """
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
    track_response = ReaperBridge.send_request(track_request)
    
    if not track_response.get("result"):
        return {
            "success": False,
            "error": f"Track at index {track_index} not found"
        }
    
    track_handle = track_response.get("track")
    
    # Set note range
    range_request = {
        "action": "SetTrackMIDINoteRange",
        "track": track_handle,
        "note_lo": max(0, min(127, note_low)),
        "note_hi": max(0, min(127, note_high))
    }
    range_response = ReaperBridge.send_request(range_request)
    
    return {
        "success": range_response.get("result", False),
        "note_low": note_low,
        "note_high": note_high
    }


def insert_midi_note_extended(take_handle: Any, pitch: int, velocity: int,
                            start_beats: float, length_beats: float,
                            channel: int = 0, selected: bool = False) -> Dict[str, Any]:
    """Insert MIDI note with musical timing (beats instead of PPQ).
    
    Args:
        take_handle: MIDI take handle
        pitch: Note pitch (0-127)
        velocity: Note velocity (0-127)
        start_beats: Start position in beats
        length_beats: Length in beats
        channel: MIDI channel (0-15)
        selected: Whether note is selected
    
    Returns:
        Dict containing operation result
    """
    # Convert beats to PPQ (960 PPQ per quarter note)
    ppq_per_beat = 960
    start_ppq = start_beats * ppq_per_beat
    end_ppq = (start_beats + length_beats) * ppq_per_beat
    
    request = {
        "action": "MIDI_InsertNote",
        "take": take_handle,
        "selected": selected,
        "muted": False,
        "startppqpos": start_ppq,
        "endppqpos": end_ppq,
        "chan": channel,
        "pitch": pitch,
        "vel": velocity,
        "noSortInOptional": False
    }
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "pitch": pitch,
        "velocity": velocity,
        "start_beats": start_beats,
        "length_beats": length_beats,
        "channel": channel
    }


def generate_chord_progression(take_handle: Any, progression: List[Dict[str, Any]],
                             start_beat: float = 0.0) -> Dict[str, Any]:
    """Generate a chord progression in a MIDI take.
    
    Args:
        take_handle: MIDI take handle
        progression: List of chord dicts with 'root', 'type', 'duration_beats'
        start_beat: Starting position in beats
    
    Returns:
        Dict containing number of notes created
    """
    # Chord templates (intervals from root)
    chord_types = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "dim": [0, 3, 6],
        "aug": [0, 4, 8],
        "maj7": [0, 4, 7, 11],
        "min7": [0, 3, 7, 10],
        "dom7": [0, 4, 7, 10],
        "sus2": [0, 2, 7],
        "sus4": [0, 5, 7]
    }
    
    notes_created = 0
    current_beat = start_beat
    
    for chord in progression:
        root = chord.get("root", 60)
        chord_type = chord.get("type", "major")
        duration = chord.get("duration_beats", 4.0)
        velocity = chord.get("velocity", 80)
        
        intervals = chord_types.get(chord_type, chord_types["major"])
        
        # Insert each note of the chord
        for interval in intervals:
            pitch = root + interval
            
            # Keep within MIDI range
            while pitch > 127:
                pitch -= 12
            while pitch < 0:
                pitch += 12
            
            result = insert_midi_note_extended(
                take_handle, pitch, velocity,
                current_beat, duration
            )
            
            if result["success"]:
                notes_created += 1
        
        current_beat += duration
    
    # Sort notes after insertion
    sort_request = {
        "action": "MIDI_Sort",
        "take": take_handle
    }
    ReaperBridge.send_request(sort_request)
    
    return {
        "success": notes_created > 0,
        "notes_created": notes_created,
        "duration_beats": current_beat - start_beat
    }


def generate_scale_run(take_handle: Any, scale_type: str, root: int,
                      start_beat: float, note_duration: float,
                      num_octaves: int = 2, direction: str = "up") -> Dict[str, Any]:
    """Generate a scale run in a MIDI take.
    
    Args:
        take_handle: MIDI take handle
        scale_type: Type of scale (major, minor, etc.)
        root: Root note
        start_beat: Starting position in beats
        note_duration: Duration of each note in beats
        num_octaves: Number of octaves to span
        direction: "up", "down", or "both"
    
    Returns:
        Dict containing notes created
    """
    # Scale intervals
    scales = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "pentatonic": [0, 2, 4, 7, 9],
        "blues": [0, 3, 5, 6, 7, 10],
        "chromatic": list(range(12))
    }
    
    intervals = scales.get(scale_type, scales["major"])
    notes_created = 0
    current_beat = start_beat
    
    # Generate scale notes
    notes = []
    for octave in range(num_octaves):
        for interval in intervals:
            pitch = root + (octave * 12) + interval
            if 0 <= pitch <= 127:
                notes.append(pitch)
    
    # Apply direction
    if direction == "down":
        notes.reverse()
    elif direction == "both":
        notes = notes + notes[-2::-1]  # Up then down, skip repeated top note
    
    # Insert notes
    for pitch in notes:
        result = insert_midi_note_extended(
            take_handle, pitch, 80,
            current_beat, note_duration
        )
        
        if result["success"]:
            notes_created += 1
        
        current_beat += note_duration
    
    return {
        "success": notes_created > 0,
        "notes_created": notes_created,
        "duration_beats": current_beat - start_beat,
        "scale_type": scale_type,
        "direction": direction
    }


def register_advanced_midi_tools(mcp):
    """Register advanced MIDI generation tools with MCP server."""
    from functools import wraps
    
    # Helper to wrap sync functions for async
    def async_wrapper(func):
        @wraps(func)
        async def wrapper(**kwargs):
            return func(**kwargs)
        return wrapper
    
    # Register all advanced MIDI tools
    tool_functions = [
        ("create_new_midi_item", create_new_midi_item),
        ("get_midi_hash", get_midi_hash),
        ("get_ppq_position_from_time", get_ppq_position_from_time),
        ("get_ppq_pos_end_of_measure", get_ppq_pos_end_of_measure),
        ("get_ppq_pos_start_of_measure", get_ppq_pos_start_of_measure),
        ("get_midi_grid", get_midi_grid),
        ("select_midi_notes", select_midi_notes),
        ("get_track_midi_note_range", get_track_midi_note_range),
        ("set_track_midi_note_range", set_track_midi_note_range),
        ("insert_midi_note_extended", insert_midi_note_extended),
        ("generate_chord_progression", generate_chord_progression),
        ("generate_scale_run", generate_scale_run),
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
        "name": "create_new_midi_item",
        "description": "Make a blank canvas for notes. Use when users want to start writing music from scratch.",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_index": {"type": "integer", "description": "Track index"},
                "start_time": {"type": "number", "description": "Start position in seconds"},
                "end_time": {"type": "number", "description": "End position in seconds"},
                "start_in_qn": {"type": "number", "description": "Start in quarter notes (optional)"}
            },
            "required": ["track_index", "start_time", "end_time"]
        }
    },
    {
        "name": "get_midi_hash",
        "description": "Get a hash of MIDI content for comparison and versioning. Useful for detecting changes, creating variations, or implementing version control for generated patterns. Hash changes when MIDI content changes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "take_handle": {"type": "any", "description": "MIDI take handle"}
            },
            "required": ["take_handle"]
        }
    },
    {
        "name": "get_ppq_position_from_time",
        "description": "Convert time in seconds to MIDI PPQ (pulses per quarter note) position. Essential for precise MIDI timing when working with time-based positions. Standard is 960 PPQ per quarter note.",
        "input_schema": {
            "type": "object",
            "properties": {
                "take_handle": {"type": "any", "description": "MIDI take handle"},
                "time": {"type": "number", "description": "Time in seconds"}
            },
            "required": ["take_handle", "time"]
        }
    },
    {
        "name": "get_ppq_pos_end_of_measure",
        "description": "Get the PPQ position at the end of the measure containing the given position. Useful for aligning generated patterns to measure boundaries and ensuring musical phrase completion.",
        "input_schema": {
            "type": "object",
            "properties": {
                "take_handle": {"type": "any", "description": "MIDI take handle"},
                "ppq_pos": {"type": "number", "description": "PPQ position"}
            },
            "required": ["take_handle", "ppq_pos"]
        }
    },
    {
        "name": "get_ppq_pos_start_of_measure",
        "description": "Get the PPQ position at the start of the measure containing the given position. Essential for starting patterns on downbeats and maintaining musical alignment with bar lines.",
        "input_schema": {
            "type": "object",
            "properties": {
                "take_handle": {"type": "any", "description": "MIDI take handle"},
                "ppq_pos": {"type": "number", "description": "PPQ position"}
            },
            "required": ["take_handle", "ppq_pos"]
        }
    },
    {
        "name": "get_midi_grid",
        "description": "Get MIDI editor grid settings including division, swing, and default note length. Use to align generated content with the user's preferred grid settings for consistent timing.",
        "input_schema": {
            "type": "object",
            "properties": {
                "take_handle": {"type": "any", "description": "MIDI take handle"}
            },
            "required": ["take_handle"]
        }
    },
    {
        "name": "select_midi_notes",
        "description": "Highlight specific notes for editing. Use when users want to modify certain pitches or note ranges.",
        "input_schema": {
            "type": "object",
            "properties": {
                "take_handle": {"type": "any", "description": "MIDI take handle"},
                "start_ppq": {"type": "number", "description": "Start position in PPQ"},
                "end_ppq": {"type": "number", "description": "End position in PPQ"},
                "channel": {"type": "integer", "description": "MIDI channel (-1 for all)", "default": -1},
                "pitch_low": {"type": "integer", "description": "Lowest pitch to select", "default": 0},
                "pitch_high": {"type": "integer", "description": "Highest pitch to select", "default": 127}
            },
            "required": ["take_handle", "start_ppq", "end_ppq"]
        }
    },
    {
        "name": "get_track_midi_note_range",
        "description": "Get the MIDI note range constraints for a track. Shows the allowed note range which can be useful for instrument-specific generation (e.g., bass ranges, lead ranges).",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_index": {"type": "integer", "description": "Track index"}
            },
            "required": ["track_index"]
        }
    },
    {
        "name": "set_track_midi_note_range",
        "description": "Set MIDI note range constraints for a track. Limits the notes that can be played, useful for keeping generated content within realistic instrument ranges (e.g., bass guitar, violin).",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_index": {"type": "integer", "description": "Track index"},
                "note_low": {"type": "integer", "description": "Lowest allowed note (0-127)"},
                "note_high": {"type": "integer", "description": "Highest allowed note (0-127)"}
            },
            "required": ["track_index", "note_low", "note_high"]
        }
    },
    {
        "name": "insert_midi_note_extended",
        "description": "Add a single musical note. Use for specific note requests like 'add a C' or 'put a kick drum hit'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "take_handle": {"type": "any", "description": "MIDI take handle"},
                "pitch": {"type": "integer", "description": "Note pitch (0-127)"},
                "velocity": {"type": "integer", "description": "Note velocity (0-127)"},
                "start_beats": {"type": "number", "description": "Start position in beats"},
                "length_beats": {"type": "number", "description": "Length in beats"},
                "channel": {"type": "integer", "description": "MIDI channel (0-15)", "default": 0},
                "selected": {"type": "boolean", "description": "Whether note is selected", "default": False}
            },
            "required": ["take_handle", "pitch", "velocity", "start_beats", "length_beats"]
        }
    },
    {
        "name": "generate_chord_progression",
        "description": "Create chord sequences automatically. Use when users want harmony, chord progressions, or accompaniment.",
        "input_schema": {
            "type": "object",
            "properties": {
                "take_handle": {"type": "any", "description": "MIDI take handle"},
                "progression": {
                    "type": "array",
                    "description": "List of chords with root, type, duration",
                    "items": {
                        "type": "object",
                        "properties": {
                            "root": {"type": "integer", "description": "Root note (0-127)"},
                            "type": {"type": "string", "description": "Chord type"},
                            "duration_beats": {"type": "number", "description": "Duration in beats"},
                            "velocity": {"type": "integer", "description": "Velocity (0-127)"}
                        }
                    }
                },
                "start_beat": {"type": "number", "description": "Starting position in beats", "default": 0.0}
            },
            "required": ["take_handle", "progression"]
        }
    },
    {
        "name": "generate_scale_run",
        "description": "Create melodic runs and scales. Use for solos, arpeggios, or melodic passages.",
        "input_schema": {
            "type": "object",
            "properties": {
                "take_handle": {"type": "any", "description": "MIDI take handle"},
                "scale_type": {
                    "type": "string",
                    "description": "Scale type",
                    "enum": ["major", "minor", "harmonic_minor", "pentatonic", "blues", "chromatic"]
                },
                "root": {"type": "integer", "description": "Root note (0-127)"},
                "start_beat": {"type": "number", "description": "Start position in beats"},
                "note_duration": {"type": "number", "description": "Duration per note in beats"},
                "num_octaves": {"type": "integer", "description": "Number of octaves", "default": 2},
                "direction": {
                    "type": "string",
                    "description": "Direction of scale",
                    "enum": ["up", "down", "both"],
                    "default": "up"
                }
            },
            "required": ["take_handle", "scale_type", "root", "start_beat", "note_duration"]
        }
    }
]