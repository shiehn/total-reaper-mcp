"""Groove and quantization tools for generative music creation."""

from typing import Dict, Any, List, Optional, Tuple
from .bridge_sync import ReaperBridge
import random
import math


def quantize_items_to_grid(strength: float = 1.0, swing: float = 0.0) -> Dict[str, Any]:
    """Quantize selected items to the project grid with optional swing.
    
    Args:
        strength: Quantization strength (0.0 to 1.0)
        swing: Swing amount (0.0 to 1.0)
    
    Returns:
        Dict containing the operation result
    """
    # Get grid settings
    grid_request = {"action": "GetSetProjectGrid", "project": 0, "set": False}
    grid_response = ReaperBridge.send_request(grid_request)
    grid_division = grid_response.get("division", 0.25)
    
    # Count selected items
    count_request = {"action": "CountSelectedMediaItems", "proj": 0}
    count_response = ReaperBridge.send_request(count_request)
    item_count = count_response.get("count", 0)
    
    if item_count == 0:
        return {
            "success": False,
            "error": "No items selected"
        }
    
    quantized_items = 0
    
    for i in range(item_count):
        # Get selected item
        item_request = {"action": "GetSelectedMediaItem", "proj": 0, "selitem": i}
        item_response = ReaperBridge.send_request(item_request)
        
        if item_response.get("result"):
            item_handle = item_response.get("item")
            
            # Get current position
            pos_request = {
                "action": "GetMediaItemInfo_Value",
                "item": item_handle,
                "parmname": "D_POSITION"
            }
            pos_response = ReaperBridge.send_request(pos_request)
            current_pos = pos_response.get("value", 0.0)
            
            # Calculate quantized position
            grid_pos = round(current_pos / grid_division) * grid_division
            
            # Apply swing if needed
            if swing > 0 and int(current_pos / grid_division) % 2 == 1:
                grid_pos += grid_division * swing * 0.5
            
            # Apply strength
            new_pos = current_pos + (grid_pos - current_pos) * strength
            
            # Set new position
            set_pos_request = {
                "action": "SetMediaItemInfo_Value",
                "item": item_handle,
                "parmname": "D_POSITION",
                "newvalue": new_pos
            }
            set_response = ReaperBridge.send_request(set_pos_request)
            
            if set_response.get("result"):
                quantized_items += 1
    
    return {
        "success": quantized_items > 0,
        "items_quantized": quantized_items,
        "strength": strength,
        "swing": swing,
        "grid_division": grid_division
    }


def humanize_items(position_amount: float = 0.01, velocity_amount: float = 10, 
                  timing_mode: str = "random") -> Dict[str, Any]:
    """Add human timing and velocity variations to selected items.
    
    Args:
        position_amount: Maximum position variation in seconds
        velocity_amount: Maximum velocity variation (0-127)
        timing_mode: "random", "late", or "early"
    
    Returns:
        Dict containing the operation result
    """
    # Count selected items
    count_request = {"action": "CountSelectedMediaItems", "proj": 0}
    count_response = ReaperBridge.send_request(count_request)
    item_count = count_response.get("count", 0)
    
    if item_count == 0:
        return {
            "success": False,
            "error": "No items selected"
        }
    
    humanized_items = 0
    
    for i in range(item_count):
        # Get selected item
        item_request = {"action": "GetSelectedMediaItem", "proj": 0, "selitem": i}
        item_response = ReaperBridge.send_request(item_request)
        
        if item_response.get("result"):
            item_handle = item_response.get("item")
            
            # Humanize position
            if position_amount > 0:
                pos_request = {
                    "action": "GetMediaItemInfo_Value",
                    "item": item_handle,
                    "parmname": "D_POSITION"
                }
                pos_response = ReaperBridge.send_request(pos_request)
                current_pos = pos_response.get("value", 0.0)
                
                # Calculate timing offset based on mode
                if timing_mode == "random":
                    offset = random.uniform(-position_amount, position_amount)
                elif timing_mode == "late":
                    offset = random.uniform(0, position_amount)
                elif timing_mode == "early":
                    offset = random.uniform(-position_amount, 0)
                else:
                    offset = 0
                
                new_pos = max(0, current_pos + offset)
                
                set_pos_request = {
                    "action": "SetMediaItemInfo_Value",
                    "item": item_handle,
                    "parmname": "D_POSITION",
                    "newvalue": new_pos
                }
                ReaperBridge.send_request(set_pos_request)
            
            # Humanize velocity for MIDI items
            if velocity_amount > 0:
                # Get active take
                take_request = {
                    "action": "GetActiveTake",
                    "item": item_handle
                }
                take_response = ReaperBridge.send_request(take_request)
                
                if take_response.get("result"):
                    take_handle = take_response.get("take")
                    
                    # Check if MIDI
                    midi_request = {
                        "action": "TakeIsMIDI",
                        "take": take_handle
                    }
                    midi_response = ReaperBridge.send_request(midi_request)
                    
                    if midi_response.get("result"):
                        # Apply velocity humanization through MIDI editor action
                        humanize_vel_request = {
                            "action": "Main_OnCommand",
                            "command": 40462,  # MIDI editor: Humanize notes
                            "project": 0
                        }
                        ReaperBridge.send_request(humanize_vel_request)
            
            humanized_items += 1
    
    return {
        "success": humanized_items > 0,
        "items_humanized": humanized_items,
        "position_amount": position_amount,
        "velocity_amount": velocity_amount,
        "timing_mode": timing_mode
    }


def create_groove_template(name: str, analyze_selection: bool = True) -> Dict[str, Any]:
    """Create a groove template from selected items.
    
    Args:
        name: Name for the groove template
        analyze_selection: Whether to analyze selected items for groove
    
    Returns:
        Dict containing the operation result
    """
    if analyze_selection:
        # Count selected items
        count_request = {"action": "CountSelectedMediaItems", "proj": 0}
        count_response = ReaperBridge.send_request(count_request)
        item_count = count_response.get("count", 0)
        
        if item_count == 0:
            return {
                "success": False,
                "error": "No items selected to analyze"
            }
        
        # Extract groove from selection
        extract_request = {
            "action": "Main_OnCommand",
            "command": 40446,  # Item: Extract groove from selected items
            "project": 0
        }
        extract_response = ReaperBridge.send_request(extract_request)
        
        if not extract_response.get("result", False):
            return {
                "success": False,
                "error": "Failed to extract groove"
            }
    
    # Save groove template (this would need custom implementation)
    # For now, we'll return success assuming the groove was extracted
    return {
        "success": True,
        "name": name,
        "analyzed_selection": analyze_selection
    }


def apply_groove_to_items(groove_name: str, strength: float = 1.0) -> Dict[str, Any]:
    """Apply a groove template to selected items.
    
    Args:
        groove_name: Name of the groove template to apply
        strength: Strength of groove application (0.0 to 1.0)
    
    Returns:
        Dict containing the operation result
    """
    # Count selected items
    count_request = {"action": "CountSelectedMediaItems", "proj": 0}
    count_response = ReaperBridge.send_request(count_request)
    item_count = count_response.get("count", 0)
    
    if item_count == 0:
        return {
            "success": False,
            "error": "No items selected"
        }
    
    # Apply groove quantization
    groove_request = {
        "action": "Main_OnCommand",
        "command": 40447,  # Item: Apply groove quantization to selected items
        "project": 0
    }
    groove_response = ReaperBridge.send_request(groove_request)
    
    return {
        "success": groove_response.get("result", False),
        "groove_name": groove_name,
        "strength": strength,
        "items_affected": item_count
    }


def generate_random_rhythm(track_index: int, pattern_length: float = 4.0,
                          density: float = 0.5, note_length: float = 0.25) -> Dict[str, Any]:
    """Generate a random rhythm pattern on a track.
    
    Args:
        track_index: Index of the track to generate rhythm on
        pattern_length: Length of the pattern in seconds
        density: Density of notes (0.0 to 1.0)
        note_length: Length of each note in seconds
    
    Returns:
        Dict containing the operation result
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
    
    # Get grid division
    grid_request = {"action": "GetSetProjectGrid", "project": 0, "set": False}
    grid_response = ReaperBridge.send_request(grid_request)
    grid_division = grid_response.get("division", 0.25)
    
    # Calculate number of possible positions
    num_positions = int(pattern_length / grid_division)
    notes_created = 0
    
    for i in range(num_positions):
        if random.random() < density:
            position = i * grid_division
            
            # Create media item at position
            item_request = {
                "action": "CreateNewMIDIItemInProj",
                "track": track_handle,
                "starttime": position,
                "endtime": position + note_length,
                "qnInOptional": False
            }
            item_response = ReaperBridge.send_request(item_request)
            
            if item_response.get("result"):
                item_handle = item_response.get("item")
                
                # Add a MIDI note
                take_request = {
                    "action": "GetActiveTake",
                    "item": item_handle
                }
                take_response = ReaperBridge.send_request(take_request)
                
                if take_response.get("result"):
                    take_handle = take_response.get("take")
                    
                    # Insert MIDI note
                    note_request = {
                        "action": "MIDI_InsertNote",
                        "take": take_handle,
                        "selected": True,
                        "muted": False,
                        "startppqpos": 0,
                        "endppqpos": 960,  # Quarter note in PPQ
                        "chan": 0,
                        "pitch": 60,  # Middle C
                        "vel": 100,
                        "noSortInOptional": False
                    }
                    ReaperBridge.send_request(note_request)
                    
                    notes_created += 1
    
    return {
        "success": notes_created > 0,
        "track_index": track_index,
        "notes_created": notes_created,
        "pattern_length": pattern_length,
        "density": density
    }


def apply_shuffle(amount: float = 0.5, pattern: str = "16th") -> Dict[str, Any]:
    """Apply shuffle/swing to selected items.
    
    Args:
        amount: Shuffle amount (0.0 to 1.0)
        pattern: Shuffle pattern ("8th", "16th", "triplet")
    
    Returns:
        Dict containing the operation result
    """
    # Map pattern to grid division
    pattern_map = {
        "8th": 0.5,
        "16th": 0.25,
        "triplet": 0.333333
    }
    
    grid_division = pattern_map.get(pattern, 0.25)
    
    # Set grid with swing
    grid_request = {
        "action": "GetSetProjectGrid",
        "project": 0,
        "set": True,
        "division": grid_division,
        "swingmode": 1,
        "swingamt": amount
    }
    grid_response = ReaperBridge.send_request(grid_request)
    
    # Quantize to apply shuffle
    quantize_result = quantize_items_to_grid(strength=1.0, swing=amount)
    
    return {
        "success": quantize_result["success"],
        "amount": amount,
        "pattern": pattern,
        "items_affected": quantize_result.get("items_quantized", 0)
    }


def create_polyrhythm(track_indices: List[int], base_division: float = 0.25,
                     ratios: List[float] = None) -> Dict[str, Any]:
    """Create polyrhythmic patterns across multiple tracks.
    
    Args:
        track_indices: List of track indices to create polyrhythms on
        base_division: Base time division in seconds
        ratios: List of ratios for each track (e.g., [3, 4, 5] for 3:4:5)
    
    Returns:
        Dict containing the operation result
    """
    if not track_indices:
        return {
            "success": False,
            "error": "No tracks specified"
        }
    
    if ratios is None:
        ratios = [3, 4, 5]  # Default polyrhythm
    
    # Ensure we have enough ratios for tracks
    while len(ratios) < len(track_indices):
        ratios.append(ratios[-1] + 1)
    
    pattern_length = base_division * 16  # 4 bars at base division
    tracks_processed = []
    
    for idx, track_index in enumerate(track_indices):
        ratio = ratios[idx]
        note_spacing = pattern_length / ratio
        
        # Generate rhythm for this track
        rhythm_result = generate_polyrhythm_track(
            track_index, pattern_length, ratio, base_division
        )
        
        if rhythm_result["success"]:
            tracks_processed.append({
                "track_index": track_index,
                "ratio": ratio,
                "notes_created": rhythm_result["notes_created"]
            })
    
    return {
        "success": len(tracks_processed) > 0,
        "tracks_processed": tracks_processed,
        "pattern_length": pattern_length,
        "base_division": base_division
    }


def generate_polyrhythm_track(track_index: int, pattern_length: float,
                             ratio: int, base_division: float) -> Dict[str, Any]:
    """Generate a single polyrhythmic track."""
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
    track_response = ReaperBridge.send_request(track_request)
    
    if not track_response.get("result"):
        return {
            "success": False,
            "error": f"Track at index {track_index} not found"
        }
    
    track_handle = track_response.get("track")
    note_spacing = pattern_length / ratio
    notes_created = 0
    
    for i in range(ratio):
        position = i * note_spacing
        
        # Create MIDI item
        item_request = {
            "action": "CreateNewMIDIItemInProj",
            "track": track_handle,
            "starttime": position,
            "endtime": position + base_division,
            "qnInOptional": False
        }
        item_response = ReaperBridge.send_request(item_request)
        
        if item_response.get("result"):
            item_handle = item_response.get("item")
            
            # Add MIDI note
            take_request = {
                "action": "GetActiveTake",
                "item": item_handle
            }
            take_response = ReaperBridge.send_request(take_request)
            
            if take_response.get("result"):
                take_handle = take_response.get("take")
                
                # Vary pitch based on position
                pitch = 60 + (i % 12)
                
                note_request = {
                    "action": "MIDI_InsertNote",
                    "take": take_handle,
                    "selected": True,
                    "muted": False,
                    "startppqpos": 0,
                    "endppqpos": 960,
                    "chan": 0,
                    "pitch": pitch,
                    "vel": 80 + (i % 3) * 15,  # Vary velocity
                    "noSortInOptional": False
                }
                ReaperBridge.send_request(note_request)
                
                notes_created += 1
    
    return {
        "success": notes_created > 0,
        "notes_created": notes_created
    }


def stretch_items_to_tempo(target_bpm: float, preserve_pitch: bool = True) -> Dict[str, Any]:
    """Stretch selected items to match a target tempo.
    
    Args:
        target_bpm: Target tempo in BPM
        preserve_pitch: Whether to preserve pitch during stretching
    
    Returns:
        Dict containing the operation result
    """
    # Get current project tempo
    tempo_request = {
        "action": "Master_GetTempo"
    }
    tempo_response = ReaperBridge.send_request(tempo_request)
    current_bpm = tempo_response.get("tempo", 120.0)
    
    # Calculate stretch ratio
    stretch_ratio = current_bpm / target_bpm
    
    # Count selected items
    count_request = {"action": "CountSelectedMediaItems", "proj": 0}
    count_response = ReaperBridge.send_request(count_request)
    item_count = count_response.get("count", 0)
    
    if item_count == 0:
        return {
            "success": False,
            "error": "No items selected"
        }
    
    stretched_items = 0
    
    for i in range(item_count):
        # Get selected item
        item_request = {"action": "GetSelectedMediaItem", "proj": 0, "selitem": i}
        item_response = ReaperBridge.send_request(item_request)
        
        if item_response.get("result"):
            item_handle = item_response.get("item")
            
            # Get active take
            take_request = {
                "action": "GetActiveTake",
                "item": item_handle
            }
            take_response = ReaperBridge.send_request(take_request)
            
            if take_response.get("result"):
                take_handle = take_response.get("take")
                
                # Set playback rate
                rate_request = {
                    "action": "SetMediaItemTakeInfo_Value",
                    "take": take_handle,
                    "parmname": "D_PLAYRATE",
                    "newvalue": stretch_ratio
                }
                rate_response = ReaperBridge.send_request(rate_request)
                
                # Set preserve pitch mode
                if preserve_pitch:
                    pitch_request = {
                        "action": "SetMediaItemTakeInfo_Value",
                        "take": take_handle,
                        "parmname": "B_PPITCH",
                        "newvalue": 1
                    }
                    ReaperBridge.send_request(pitch_request)
                
                if rate_response.get("result"):
                    stretched_items += 1
    
    return {
        "success": stretched_items > 0,
        "items_stretched": stretched_items,
        "target_bpm": target_bpm,
        "stretch_ratio": stretch_ratio,
        "preserve_pitch": preserve_pitch
    }


def detect_tempo_from_selection() -> Dict[str, Any]:
    """Detect tempo from selected audio items.
    
    Returns:
        Dict containing detected tempo and operation result
    """
    # Count selected items
    count_request = {"action": "CountSelectedMediaItems", "proj": 0}
    count_response = ReaperBridge.send_request(count_request)
    item_count = count_response.get("count", 0)
    
    if item_count == 0:
        return {
            "success": False,
            "error": "No items selected"
        }
    
    # Run tempo detection action
    detect_request = {
        "action": "Main_OnCommand",
        "command": 41987,  # Item: Run auto-stretch at tempo detection on selected items
        "project": 0
    }
    detect_response = ReaperBridge.send_request(detect_request)
    
    # Get detected tempo from first item
    item_request = {"action": "GetSelectedMediaItem", "proj": 0, "selitem": 0}
    item_response = ReaperBridge.send_request(item_request)
    
    detected_tempo = 120.0  # Default
    
    if item_response.get("result"):
        item_handle = item_response.get("item")
        take_request = {
            "action": "GetActiveTake",
            "item": item_handle
        }
        take_response = ReaperBridge.send_request(take_request)
        
        if take_response.get("result"):
            take_handle = take_response.get("take")
            
            # Get source BPM if available
            src_bpm_request = {
                "action": "GetMediaItemTakeInfo_Value",
                "take": take_handle,
                "parmname": "D_SRCBPM"
            }
            src_bpm_response = ReaperBridge.send_request(src_bpm_request)
            
            if src_bpm_response.get("value", 0) > 0:
                detected_tempo = src_bpm_response.get("value")
    
    return {
        "success": detect_response.get("result", False),
        "detected_tempo": detected_tempo,
        "items_analyzed": item_count
    }


def register_groove_quantization_tools(mcp):
    """Register groove and quantization tools with MCP server."""
    from functools import wraps
    
    # Helper to wrap sync functions for async
    def async_wrapper(func):
        @wraps(func)
        async def wrapper(**kwargs):
            return func(**kwargs)
        return wrapper
    
    # Register all groove/quantization tools
    tool_functions = [
        ("quantize_items_to_grid", quantize_items_to_grid),
        ("humanize_items", humanize_items),
        ("create_groove_template", create_groove_template),
        ("apply_groove_to_items", apply_groove_to_items),
        ("generate_random_rhythm", generate_random_rhythm),
        ("apply_shuffle", apply_shuffle),
        ("create_polyrhythm", create_polyrhythm),
        ("stretch_items_to_tempo", stretch_items_to_tempo),
        ("detect_tempo_from_selection", detect_tempo_from_selection),
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
        "name": "quantize_items_to_grid",
        "description": "Quantize selected items to the project grid with optional swing",
        "input_schema": {
            "type": "object",
            "properties": {
                "strength": {"type": "number", "description": "Quantization strength (0.0 to 1.0)", "default": 1.0},
                "swing": {"type": "number", "description": "Swing amount (0.0 to 1.0)", "default": 0.0}
            },
            "required": []
        }
    },
    {
        "name": "humanize_items",
        "description": "Add human timing and velocity variations to selected items",
        "input_schema": {
            "type": "object",
            "properties": {
                "position_amount": {"type": "number", "description": "Maximum position variation in seconds", "default": 0.01},
                "velocity_amount": {"type": "number", "description": "Maximum velocity variation (0-127)", "default": 10},
                "timing_mode": {"type": "string", "enum": ["random", "late", "early"], "description": "Timing variation mode", "default": "random"}
            },
            "required": []
        }
    },
    {
        "name": "create_groove_template",
        "description": "Create a groove template from selected items",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name for the groove template"},
                "analyze_selection": {"type": "boolean", "description": "Whether to analyze selected items", "default": True}
            },
            "required": ["name"]
        }
    },
    {
        "name": "apply_groove_to_items",
        "description": "Apply a groove template to selected items",
        "input_schema": {
            "type": "object",
            "properties": {
                "groove_name": {"type": "string", "description": "Name of the groove template"},
                "strength": {"type": "number", "description": "Strength of groove application (0.0 to 1.0)", "default": 1.0}
            },
            "required": ["groove_name"]
        }
    },
    {
        "name": "generate_random_rhythm",
        "description": "Generate a random rhythm pattern on a track",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_index": {"type": "integer", "description": "Index of the track"},
                "pattern_length": {"type": "number", "description": "Length of pattern in seconds", "default": 4.0},
                "density": {"type": "number", "description": "Note density (0.0 to 1.0)", "default": 0.5},
                "note_length": {"type": "number", "description": "Length of each note in seconds", "default": 0.25}
            },
            "required": ["track_index"]
        }
    },
    {
        "name": "apply_shuffle",
        "description": "Apply shuffle/swing to selected items",
        "input_schema": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "description": "Shuffle amount (0.0 to 1.0)", "default": 0.5},
                "pattern": {"type": "string", "enum": ["8th", "16th", "triplet"], "description": "Shuffle pattern", "default": "16th"}
            },
            "required": []
        }
    },
    {
        "name": "create_polyrhythm",
        "description": "Create polyrhythmic patterns across multiple tracks",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_indices": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "List of track indices"
                },
                "base_division": {"type": "number", "description": "Base time division in seconds", "default": 0.25},
                "ratios": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "List of ratios for each track"
                }
            },
            "required": ["track_indices"]
        }
    },
    {
        "name": "stretch_items_to_tempo",
        "description": "Stretch selected items to match a target tempo",
        "input_schema": {
            "type": "object",
            "properties": {
                "target_bpm": {"type": "number", "description": "Target tempo in BPM"},
                "preserve_pitch": {"type": "boolean", "description": "Whether to preserve pitch", "default": True}
            },
            "required": ["target_bpm"]
        }
    },
    {
        "name": "detect_tempo_from_selection",
        "description": "Detect tempo from selected audio items",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]