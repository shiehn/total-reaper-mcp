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
    # Use the combined bridge function that handles all operations in one call
    result = await bridge.call_lua("InsertMIDINoteToItemTake", [
        item_index, take_index, pitch, velocity, start_time, duration, 
        channel, selected, muted, None, None
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
    # Use the combined bridge function that gets item, take and counts in one call
    result = await bridge.call_lua("GetItemTakeAndCountMIDI", [item_index, take_index])
    
    if result.get("ok"):
        notes = result.get("notes", 0)
        ccs = result.get("cc", 0)
        text_events = result.get("text", 0)
        return f"MIDI event counts: notes={notes}, CCs={ccs}, sysex={text_events}"
    else:
        raise Exception(f"Failed to count MIDI events: {result.get('error', 'Unknown error')}")


async def midi_select_all(item_index: int = 0, take_index: int = 0) -> str:
    """Select all MIDI events in a take"""
    # Use the combined bridge function
    result = await bridge.call_lua("SelectAllMIDIInItemTake", [item_index, take_index])
    
    if result.get("ok"):
        return "Selected all MIDI events"
    else:
        raise Exception(f"Failed to select MIDI events: {result.get('error', 'Unknown error')}")


async def midi_get_all_events(item_index: int = 0, take_index: int = 0) -> str:
    """Get all MIDI events from a take"""
    # Note: MIDI_GetAllEvts returns binary data that cannot be easily transferred via JSON
    # For now, we'll just count the events instead
    result = await bridge.call_lua("GetItemTakeAndCountMIDI", [item_index, take_index])
    
    if result.get("ok"):
        notes = result.get("notes", 0)
        ccs = result.get("cc", 0)
        text_events = result.get("text", 0)
        total_events = notes + ccs + text_events
        return f"MIDI events data: {total_events} total events (notes={notes}, CCs={ccs}, text={text_events})"
    else:
        raise Exception(f"Failed to get MIDI events: {result.get('error', 'Unknown error')}")


async def midi_get_scale(item_index: int = 0, take_index: int = 0) -> str:
    """Get the scale setting for a MIDI take"""
    # Note: MIDI_GetScale is not available in the current REAPER API
    # This is a placeholder implementation
    return "Scale: root=0, type=0, name= (Note: MIDI scale functions not available in this REAPER version)"


async def midi_set_scale(item_index: int = 0, take_index: int = 0, root: int = 0, 
                        scale: int = 0, channel: int = 0) -> str:
    """Set the scale for a MIDI take"""
    # Note: MIDI_SetScale is not available in the current REAPER API
    # This is a placeholder implementation
    scale_names = ["Major", "Minor", "Harmonic minor", "Melodic minor", "Dorian", 
                  "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]
    scale_name = scale_names[scale] if 0 <= scale < len(scale_names) else f"Custom ({scale})"
    
    return f"Set MIDI scale: root={root}, scale={scale} ({scale_name}) (Note: MIDI scale functions not available in this REAPER version)"


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
# MIDI Extended Operations (8 tools)
# ============================================================================

async def midi_get_evt(item_index: int, take_index: int, event_index: int) -> str:
    """Get a MIDI event by index"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get the event
    result = await bridge.call_lua("MIDI_GetEvt", [take_handle, event_index, False, False, 0, ""])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 5:
            retval, selected, muted, ppq_pos, msg = ret[:5]
            if retval:
                # Try to decode the message
                msg_info = "Unknown event"
                if msg and len(msg) > 0:
                    status = ord(msg[0]) if isinstance(msg, str) else msg[0]
                    event_type = (status & 0xF0) >> 4
                    channel = status & 0x0F
                    
                    type_names = {
                        0x8: "Note Off",
                        0x9: "Note On",
                        0xA: "Aftertouch",
                        0xB: "CC",
                        0xC: "Program Change",
                        0xD: "Channel Pressure",
                        0xE: "Pitch Bend"
                    }
                    msg_info = type_names.get(event_type, f"Type {event_type}")
                    
                return f"Event {event_index}: PPQ={ppq_pos:.1f}, Type={msg_info}, Channel={channel}, Selected={selected}, Muted={muted}"
            else:
                return f"Event {event_index} not found"
        else:
            return f"Invalid response format for event {event_index}"
    else:
        raise Exception(f"Failed to get MIDI event: {result.get('error', 'Unknown error')}")


async def midi_get_grid(item_index: int, take_index: int) -> str:
    """Get MIDI grid settings"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get grid settings
    result = await bridge.call_lua("MIDI_GetGrid", [take_handle])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            qn_grid = ret[0] if len(ret) > 0 else 0
            swing = ret[1] if len(ret) > 1 else 0
            return f"MIDI grid: {qn_grid:.3f} quarter notes, swing={swing:.1f}%"
        else:
            return "MIDI grid: default settings"
    else:
        raise Exception(f"Failed to get MIDI grid: {result.get('error', 'Unknown error')}")


async def midi_get_ppq_pos_from_proj_time(item_index: int, take_index: int, time: float) -> str:
    """Convert project time to PPQ position"""
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
    result = await bridge.call_lua("MIDI_GetPPQPosFromProjTime", [take_handle, time])
    
    if result.get("ok"):
        ppq = result.get("ret", 0.0)
        return f"Time {time:.3f}s = PPQ {ppq:.1f}"
    else:
        raise Exception(f"Failed to convert time to PPQ: {result.get('error', 'Unknown error')}")


async def midi_get_proj_time_from_ppq_pos(item_index: int, take_index: int, ppq_pos: float) -> str:
    """Convert PPQ position to project time"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Convert PPQ to time
    result = await bridge.call_lua("MIDI_GetProjTimeFromPPQPos", [take_handle, ppq_pos])
    
    if result.get("ok"):
        time = result.get("ret", 0.0)
        return f"PPQ {ppq_pos:.1f} = Time {time:.3f}s"
    else:
        raise Exception(f"Failed to convert PPQ to time: {result.get('error', 'Unknown error')}")


async def midi_get_ppq_pos_start_of_measure(item_index: int, take_index: int, ppq_pos: float) -> str:
    """Get PPQ position of the start of measure for a given PPQ position"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get start of measure
    result = await bridge.call_lua("MIDI_GetPPQPos_StartOfMeasure", [take_handle, ppq_pos])
    
    if result.get("ok"):
        measure_start_ppq = result.get("ret", 0.0)
        return f"Start of measure for PPQ {ppq_pos:.1f} is PPQ {measure_start_ppq:.1f}"
    else:
        raise Exception(f"Failed to get start of measure: {result.get('error', 'Unknown error')}")


async def midi_get_ppq_pos_end_of_measure(item_index: int, take_index: int, ppq_pos: float) -> str:
    """Get PPQ position of the end of measure for a given PPQ position"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get end of measure
    result = await bridge.call_lua("MIDI_GetPPQPos_EndOfMeasure", [take_handle, ppq_pos])
    
    if result.get("ok"):
        measure_end_ppq = result.get("ret", 0.0)
        return f"End of measure for PPQ {ppq_pos:.1f} is PPQ {measure_end_ppq:.1f}"
    else:
        raise Exception(f"Failed to get end of measure: {result.get('error', 'Unknown error')}")


async def midi_enum_sel_notes(item_index: int, take_index: int) -> str:
    """Enumerate selected MIDI notes"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Enumerate selected notes
    selected_notes = []
    note_idx = -1
    
    while True:
        result = await bridge.call_lua("MIDI_EnumSelNotes", [take_handle, note_idx])
        if result.get("ok"):
            next_idx = result.get("ret", -1)
            if next_idx == -1:
                break
            
            # Get note info
            note_result = await bridge.call_lua("MIDI_GetNote", [take_handle, next_idx])
            if note_result.get("ok"):
                ret = note_result.get("ret", [])
                if isinstance(ret, list) and len(ret) >= 7:
                    retval, selected, muted, start_ppq, end_ppq, channel, pitch, velocity = ret[:8]
                    if retval and selected:
                        selected_notes.append({
                            "index": next_idx,
                            "pitch": pitch,
                            "velocity": velocity,
                            "start_ppq": start_ppq
                        })
            
            note_idx = next_idx
        else:
            break
    
    if selected_notes:
        notes_info = ", ".join([f"Note {n['index']}: pitch={n['pitch']}" for n in selected_notes[:5]])
        if len(selected_notes) > 5:
            notes_info += f", ... ({len(selected_notes) - 5} more)"
        return f"Selected notes ({len(selected_notes)}): {notes_info}"
    else:
        return "No notes selected"


async def midi_set_item_extents(item_index: int, take_index: int, start_qn: float, end_qn: float) -> str:
    """Set MIDI item extents in quarter notes"""
    # Get media item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set item extents
    result = await bridge.call_lua("MIDI_SetItemExtents", [item_handle, start_qn, end_qn])
    
    if result.get("ok"):
        return f"Set MIDI item extents: start={start_qn:.1f} QN, end={end_qn:.1f} QN"
    else:
        raise Exception(f"Failed to set MIDI item extents: {result.get('error', 'Unknown error')}")


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
        
        # MIDI Extended Operations
        (midi_get_evt, "Get a MIDI event by index"),
        (midi_get_grid, "Get MIDI grid settings"),
        (midi_get_ppq_pos_from_proj_time, "Convert project time to PPQ position"),
        (midi_get_proj_time_from_ppq_pos, "Convert PPQ position to project time"),
        (midi_get_ppq_pos_start_of_measure, "Get PPQ position of the start of measure"),
        (midi_get_ppq_pos_end_of_measure, "Get PPQ position of the end of measure"),
        (midi_enum_sel_notes, "Enumerate selected MIDI notes"),
        (midi_set_item_extents, "Set MIDI item extents in quarter notes"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)