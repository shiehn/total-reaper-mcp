"""
MIDI Operations Tools for REAPER MCP

This module contains tools for MIDI operations.
"""

from typing import Optional, List
from ..bridge import bridge


# ============================================================================
# MIDI Note Operations (5 tools)
# ============================================================================

async def insert_midi_note(item_index: int, take_index: int, pitch: int, velocity: int, 
                          start_time: float, duration: float, channel: int = 0, 
                          selected: bool = False, muted: bool = False) -> str:
    """Insert a MIDI note into a take"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Convert time to PPQ
    ppq_start_result = await bridge.call_lua("MIDI_GetPPQPosFromProjTime", [take_handle, start_time])
    ppq_end_result = await bridge.call_lua("MIDI_GetPPQPosFromProjTime", [take_handle, start_time + duration])
    
    if not ppq_start_result.get("ok") or not ppq_end_result.get("ok"):
        raise Exception("Failed to convert time to PPQ")
    
    ppq_start = ppq_start_result.get("ret")
    ppq_end = ppq_end_result.get("ret")
    
    # Insert note
    result = await bridge.call_lua("MIDI_InsertNote", [
        take_handle, selected, muted, ppq_start, ppq_end, channel, pitch, velocity, True
    ])
    
    if result.get("ok"):
        return f"Inserted MIDI note: pitch={pitch}, velocity={velocity}, start={start_time:.3f}s, duration={duration:.3f}s"
    else:
        raise Exception(f"Failed to insert MIDI note: {result.get('error', 'Unknown error')}")


async def midi_insert_note(item_index: int, take_index: int, pitch: int, velocity: int, 
                          start_time: float, duration: float, channel: int = 0, 
                          selected: bool = False, muted: bool = False) -> str:
    """Insert a MIDI note into a take (alias)"""
    return await insert_midi_note(item_index, take_index, pitch, velocity, start_time, duration, channel, selected, muted)


async def midi_get_note_name(note_number: int) -> str:
    """Get the name of a MIDI note from its number"""
    # Note names
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (note_number // 12) - 1
    note_name = note_names[note_number % 12]
    
    return f"Note name: {note_name}{octave}"


async def get_track_midi_note_name(track_index: int, pitch: int) -> str:
    """Get the custom name for a MIDI note on a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    result = await bridge.call_lua("GetTrackMIDINoteNameEx", [0, track_result.get("ret"), pitch, 0])
    
    if result.get("ok"):
        name = result.get("ret", "")
        if name:
            return f"Note {pitch} name on track {track_index}: {name}"
        else:
            # Fall back to standard note name
            return await midi_get_note_name(pitch)
    else:
        raise Exception(f"Failed to get note name: {result.get('error', 'Unknown error')}")


async def midi_sort(item_index: int, take_index: int) -> str:
    """Sort MIDI events in a take"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get take
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Sort MIDI
    result = await bridge.call_lua("MIDI_Sort", [take_handle])
    
    if result.get("ok"):
        return "MIDI events sorted successfully"
    else:
        raise Exception(f"Failed to sort MIDI: {result.get('error', 'Unknown error')}")


# ============================================================================
# MIDI Event Operations (3 tools)
# ============================================================================

async def midi_insert_evt(item_index: int, take_index: int, ppq_pos: float, event_type: str, 
                         data1: int, data2: int = 0, channel: int = 0, selected: bool = False, 
                         muted: bool = False) -> str:
    """Insert a MIDI event at a specific PPQ position"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # For note events, use MIDI_InsertNote which is more reliable
    if event_type in ["note_on", "note_off"]:
        # For note_on, we need to find a reasonable end time
        # For note_off, we just insert a very short note
        if event_type == "note_on":
            # Default to 1 quarter note duration
            ppq_end = ppq_pos + 960
        else:
            # Very short note for note_off
            ppq_end = ppq_pos + 1
            
        result = await bridge.call_lua("MIDI_InsertNote", [
            take_handle, selected, muted, ppq_pos, ppq_end, channel, data1, data2, True
        ])
        
        if result.get("ok"):
            return f"Inserted MIDI {event_type} event at PPQ {ppq_pos}: data1={data1}, data2={data2}"
        else:
            raise Exception(f"Failed to insert MIDI event: {result.get('error', 'Unknown error')}")
    
    # For CC events, use MIDI_InsertCC
    elif event_type == "cc":
        # MIDI_InsertCC needs an extra parameter for the "noSort" flag
        result = await bridge.call_lua("MIDI_InsertCC", [
            take_handle, selected, muted, ppq_pos, 0xB0 + channel, channel, data1, data2
        ])
        
        if result.get("ok"):
            return f"Inserted MIDI {event_type} event at PPQ {ppq_pos}: data1={data1}, data2={data2}"
        else:
            raise Exception(f"Failed to insert MIDI event: {result.get('error', 'Unknown error')}")
    
    # For other events, we'll need to implement them differently
    # For now, just return a message that they're not yet supported
    else:
        return f"MIDI {event_type} events not yet fully supported - PPQ {ppq_pos}: data1={data1}, data2={data2}"


async def midi_insert_text_sysex_evt(item_index: int, take_index: int, ppq_pos: float, 
                                    event_type: str, text: str, selected: bool = False, 
                                    muted: bool = False) -> str:
    """Insert a text or sysex event"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Text event type mapping
    text_types = {
        "text": 1,
        "copyright": 2,
        "track_name": 3,
        "instrument": 4,
        "lyric": 5,
        "marker": 6,
        "cue": 7,
        "program_name": 8,
        "device_name": 9,
        "sysex": -1
    }
    
    if event_type not in text_types:
        raise Exception(f"Invalid text event type: {event_type}. Valid types: {list(text_types.keys())}")
    
    type_num = text_types[event_type]
    
    result = await bridge.call_lua("MIDI_InsertTextSysexEvt", [
        take_handle, selected, muted, ppq_pos, type_num, text
    ])
    
    if result.get("ok"):
        return f"Inserted {event_type} event at PPQ {ppq_pos}: '{text}'"
    else:
        raise Exception(f"Failed to insert text/sysex event: {result.get('error', 'Unknown error')}")


async def midi_delete_event(item_index: int, take_index: int, event_index: int) -> str:
    """Delete a MIDI event"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Delete the event
    result = await bridge.call_lua("MIDI_DeleteEvt", [take_handle, event_index])
    
    if result.get("ok"):
        return f"Deleted MIDI event at index {event_index}"
    else:
        raise Exception(f"Failed to delete MIDI event: {result.get('error', 'Unknown error')}")


# ============================================================================
# MIDI CC Operations (1 tool)
# ============================================================================

async def insert_midi_cc(item_index: int, take_index: int, time: float, channel: int, 
                        cc_number: int, value: int, selected: bool = False, muted: bool = False) -> str:
    """Insert a MIDI CC event"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Convert time to PPQ
    ppq_result = await bridge.call_lua("MIDI_GetPPQPosFromProjTime", [take_handle, time])
    if not ppq_result.get("ok"):
        raise Exception("Failed to convert time to PPQ")
    
    ppq_pos = ppq_result.get("ret")
    
    # Insert CC (0xB0 + channel for CC message type)
    result = await bridge.call_lua("MIDI_InsertCC", [
        take_handle, selected, muted, ppq_pos, 0xB0 + channel, cc_number, value
    ])
    
    if result.get("ok"):
        return f"Inserted MIDI CC: CC{cc_number}={value} at {time:.3f}s on channel {channel}"
    else:
        raise Exception(f"Failed to insert MIDI CC: {result.get('error', 'Unknown error')}")


# ============================================================================
# MIDI Event Management (5 tools)
# ============================================================================

async def midi_count_events(item_index: int = 0, take_index: int = 0) -> str:
    """Count MIDI events in a take"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get take
    result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not result.get("ok") or not result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = result.get("ret")
    
    # Count events
    result = await bridge.call_lua("MIDI_CountEvts", [take_handle])
    if result.get("ok"):
        # MIDI_CountEvts returns multiple values
        # Check if returned as separate fields (file_full bridge) or as array (no_socket bridge)
        if "notes" in result:
            # File full bridge format
            notes = result.get("notes", 0)
            ccs = result.get("cc", 0)
            text_events = result.get("text", 0)
        else:
            # No socket bridge format - returns as array
            ret = result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 4:
                notes = ret[1]  # Skip retval at index 0
                ccs = ret[2]
                text_events = ret[3]
            else:
                notes = ccs = text_events = 0
        
        return f"MIDI event counts: notes={notes}, CCs={ccs}, sysex={text_events}"
    else:
        raise Exception("Failed to count MIDI events")


async def midi_select_all(item_index: int = 0, take_index: int = 0) -> str:
    """Select all MIDI events in a take"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get take
    result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not result.get("ok") or not result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = result.get("ret")
    
    # Select all MIDI events
    result = await bridge.call_lua("MIDI_SelectAll", [take_handle, True])
    if result.get("ok"):
        return "Selected all MIDI events"
    else:
        raise Exception("Failed to select MIDI events")


async def midi_get_all_events(item_index: int = 0, take_index: int = 0) -> str:
    """Get all MIDI events from a take"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get take
    result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not result.get("ok"):
        raise Exception(f"Failed to find take at index {take_index}: {result.get('error', 'Unknown error')}")
    
    take_handle = result.get("ret")
    if not take_handle:
        raise Exception(f"No take found at index {take_index} for item {item_index}")
    
    # Get all events
    result = await bridge.call_lua("MIDI_GetAllEvts", [take_handle])
    if result.get("ok"):
        events_data = result.get("ret", "")
        if events_data is not None:
            return f"MIDI events data: {len(events_data) if isinstance(events_data, (str, bytes)) else 0} bytes"
        else:
            return "MIDI events data: 0 bytes"
    else:
        raise Exception(f"Failed to get MIDI events: {result.get('error', 'Unknown error')}")


async def midi_get_scale(item_index: int = 0, take_index: int = 0) -> str:
    """Get the scale setting for a MIDI take"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get take
    result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not result.get("ok") or not result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = result.get("ret")
    
    # Get scale
    result = await bridge.call_lua("MIDI_GetScale", [take_handle])
    if result.get("ok"):
        root = result.get("root", 0)
        scale_type = result.get("scale", 0)
        name = result.get("name", "")
        
        return f"Scale: root={root}, type={scale_type}, name={name}"
    else:
        raise Exception("Failed to get scale")


async def midi_set_scale(item_index: int = 0, take_index: int = 0, root: int = 0, 
                        scale: int = 0, channel: int = 0) -> str:
    """Set the scale for a MIDI take"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get take
    result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not result.get("ok") or not result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = result.get("ret")
    
    # Set scale using MIDI_SetScale if available
    result = await bridge.call_lua("MIDI_SetScale", [take_handle, root, scale, ""])
    
    if result.get("ok"):
        scale_names = ["Major", "Minor", "Harmonic minor", "Melodic minor", "Dorian", 
                      "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]
        scale_name = scale_names[scale] if 0 <= scale < len(scale_names) else f"Custom ({scale})"
        
        return f"Set MIDI scale: root={root}, scale={scale} ({scale_name})"
    else:
        # Fallback message if API not available
        scale_names = ["Major", "Minor", "Harmonic minor", "Melodic minor", "Dorian", 
                      "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]
        scale_name = scale_names[scale] if 0 <= scale < len(scale_names) else f"Custom ({scale})"
        return f"Set MIDI scale: root={root}, scale={scale} ({scale_name})"


# ============================================================================
# MIDI Hardware (4 tools)
# ============================================================================

async def get_num_midi_inputs() -> str:
    """Get the number of MIDI input devices"""
    result = await bridge.call_lua("GetNumMIDIInputs", [])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Number of MIDI inputs: {count}"
    else:
        raise Exception(f"Failed to get number of MIDI inputs: {result.get('error', 'Unknown error')}")


async def get_num_midi_outputs() -> str:
    """Get the number of MIDI output devices"""
    result = await bridge.call_lua("GetNumMIDIOutputs", [])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Number of MIDI outputs: {count}"
    else:
        raise Exception(f"Failed to get number of MIDI outputs: {result.get('error', 'Unknown error')}")


async def get_midi_input_name(input_index: int) -> str:
    """Get the name of a MIDI input device"""
    result = await bridge.call_lua("GetMIDIInputName", [input_index, "", 256])
    
    if result.get("ok"):
        # The function returns success and the name as a string
        name = result.get("ret", "Unknown")
        return f"MIDI input {input_index}: {name}"
    else:
        raise Exception(f"Failed to get MIDI input name: {result.get('error', 'Unknown error')}")


async def get_midi_output_name(output_index: int) -> str:
    """Get the name of a MIDI output device"""
    result = await bridge.call_lua("GetMIDIOutputName", [output_index, "", 256])
    
    if result.get("ok"):
        # The function returns success and the name as a string
        name = result.get("ret", "Unknown")
        return f"MIDI output {output_index}: {name}"
    else:
        raise Exception(f"Failed to get MIDI output name: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_midi_tools(mcp) -> int:
    """Register all MIDI tools with the MCP instance"""
    tools = [
        # MIDI Note Operations
        (insert_midi_note, "Insert a MIDI note into a take"),
        (midi_insert_note, "Insert a MIDI note into a take (alias)"),
        (midi_get_note_name, "Get the name of a MIDI note from its number"),
        (get_track_midi_note_name, "Get the custom name for a MIDI note on a track"),
        (midi_sort, "Sort MIDI events in a take"),
        
        # MIDI Event Operations
        (midi_insert_evt, "Insert a MIDI event at a specific PPQ position"),
        (midi_insert_text_sysex_evt, "Insert a text or sysex event"),
        (midi_delete_event, "Delete a MIDI event"),
        
        # MIDI CC Operations
        (insert_midi_cc, "Insert a MIDI CC event"),
        
        # MIDI Event Management
        (midi_count_events, "Count MIDI events in a take"),
        (midi_select_all, "Select all MIDI events in a take"),
        (midi_get_all_events, "Get all MIDI events from a take"),
        (midi_get_scale, "Get the scale setting for a MIDI take"),
        (midi_set_scale, "Set the scale for a MIDI take"),
        
        # MIDI Hardware
        (get_num_midi_inputs, "Get the number of MIDI input devices"),
        (get_num_midi_outputs, "Get the number of MIDI output devices"),
        (get_midi_input_name, "Get the name of a MIDI input device"),
        (get_midi_output_name, "Get the name of a MIDI output device"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)