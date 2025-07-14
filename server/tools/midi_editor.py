"""
MIDI Editor & Piano Roll Tools for REAPER MCP

This module contains tools for working with the MIDI editor, piano roll,
and MIDI editor settings.
"""

from typing import Optional, Tuple, List, Any
from ..bridge import bridge


# ============================================================================
# MIDI Editor Window Management (8 tools)
# ============================================================================

async def midi_open_editor(item_index: int, take_index: int) -> str:
    """Open MIDI editor for a take"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Open MIDI editor
    result = await bridge.call_lua("MIDI_Editor_Open", [take_handle, False])
    
    if result.get("ok"):
        editor = result.get("ret")
        if editor:
            return f"Opened MIDI editor for take {take_index}"
        else:
            return "Failed to open MIDI editor"
    else:
        raise Exception(f"Failed to open MIDI editor: {result.get('error', 'Unknown error')}")


async def midi_editor_get_active() -> str:
    """Get the active MIDI editor window"""
    result = await bridge.call_lua("MIDIEditor_GetActive", [])
    
    if result.get("ok"):
        editor = result.get("ret")
        if editor:
            return "Found active MIDI editor"
        else:
            return "No active MIDI editor"
    else:
        raise Exception(f"Failed to get active MIDI editor: {result.get('error', 'Unknown error')}")


async def midi_editor_get_take(editor_id: str = "active") -> str:
    """Get the take from a MIDI editor"""
    # If editor_id is "active", get active editor
    if editor_id == "active":
        editor_result = await bridge.call_lua("MIDIEditor_GetActive", [])
        if not editor_result.get("ok") or not editor_result.get("ret"):
            return "No active MIDI editor"
        editor_handle = editor_result.get("ret")
    else:
        editor_handle = editor_id
    
    # Get take from editor
    result = await bridge.call_lua("MIDIEditor_GetTake", [editor_handle])
    
    if result.get("ok"):
        take = result.get("ret")
        if take:
            return "Found take in MIDI editor"
        else:
            return "MIDI editor has no take"
    else:
        raise Exception(f"Failed to get take from MIDI editor: {result.get('error', 'Unknown error')}")


async def midi_editor_get_setting_int(editor_id: str, setting_name: str) -> str:
    """Get integer setting from MIDI editor"""
    # If editor_id is "active", get active editor
    if editor_id == "active":
        editor_result = await bridge.call_lua("MIDIEditor_GetActive", [])
        if not editor_result.get("ok") or not editor_result.get("ret"):
            return "No active MIDI editor"
        editor_handle = editor_result.get("ret")
    else:
        editor_handle = editor_id
    
    # Get setting
    result = await bridge.call_lua("MIDIEditor_GetSetting_int", [editor_handle, setting_name])
    
    if result.get("ok"):
        value = result.get("ret", 0)
        return f"MIDI editor {setting_name}: {value}"
    else:
        raise Exception(f"Failed to get MIDI editor setting: {result.get('error', 'Unknown error')}")


async def midi_editor_set_setting_int(editor_id: str, setting_name: str, value: int) -> str:
    """Set integer setting in MIDI editor"""
    # If editor_id is "active", get active editor
    if editor_id == "active":
        editor_result = await bridge.call_lua("MIDIEditor_GetActive", [])
        if not editor_result.get("ok") or not editor_result.get("ret"):
            return "No active MIDI editor"
        editor_handle = editor_result.get("ret")
    else:
        editor_handle = editor_id
    
    # Set setting
    result = await bridge.call_lua("MIDIEditor_SetSetting_int", [editor_handle, setting_name, value])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set MIDI editor {setting_name} to {value}"
        else:
            return f"Failed to set MIDI editor setting"
    else:
        raise Exception(f"Failed to set MIDI editor setting: {result.get('error', 'Unknown error')}")


async def midi_editor_get_mode() -> str:
    """Get MIDI editor mode"""
    result = await bridge.call_lua("MIDIEditor_GetMode", [])
    
    if result.get("ok"):
        mode = result.get("ret", -1)
        mode_names = {
            0: "piano roll",
            1: "drum map", 
            2: "event list"
        }
        mode_str = mode_names.get(mode, f"mode {mode}")
        return f"MIDI editor mode: {mode_str}"
    else:
        raise Exception(f"Failed to get MIDI editor mode: {result.get('error', 'Unknown error')}")


async def midi_editor_on_command(command_id: int) -> str:
    """Execute command in active MIDI editor"""
    # Get active editor
    editor_result = await bridge.call_lua("MIDIEditor_GetActive", [])
    if not editor_result.get("ok") or not editor_result.get("ret"):
        return "No active MIDI editor"
    
    editor_handle = editor_result.get("ret")
    
    # Execute command
    result = await bridge.call_lua("MIDIEditor_OnCommand", [editor_handle, command_id])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Executed MIDI editor command {command_id}"
        else:
            return f"Failed to execute MIDI editor command"
    else:
        raise Exception(f"Failed to execute MIDI editor command: {result.get('error', 'Unknown error')}")


async def midi_editor_last_focused() -> str:
    """Get the last focused MIDI editor"""
    result = await bridge.call_lua("MIDIEditor_LastFocused_OnCommand", [40001, False])
    
    if result.get("ok"):
        # This function executes a command in the last focused editor
        # We're using a harmless command (40001 = Transport: Play)
        return "Accessed last focused MIDI editor"
    else:
        raise Exception(f"Failed to access last focused MIDI editor: {result.get('error', 'Unknown error')}")


# ============================================================================
# MIDI Note Selection & Manipulation (10 tools)
# ============================================================================

async def midi_select_notes(item_index: int, take_index: int, 
                           start_ppq: float, end_ppq: float, 
                           pitch_low: int, pitch_high: int) -> str:
    """Select MIDI notes in a range"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Select notes in range
    result = await bridge.call_lua("MIDI_SelectNotes", [
        take_handle, start_ppq, end_ppq, pitch_low, pitch_high
    ])
    
    if result.get("ok"):
        return f"Selected notes in range: PPQ {start_ppq}-{end_ppq}, pitch {pitch_low}-{pitch_high}"
    else:
        raise Exception(f"Failed to select notes: {result.get('error', 'Unknown error')}")


async def midi_get_selected_notes(item_index: int, take_index: int) -> str:
    """Get all selected MIDI notes"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Count notes
    count_result = await bridge.call_lua("MIDI_CountEvts", [take_handle])
    if not count_result.get("ok"):
        raise Exception("Failed to count MIDI events")
    
    ret = count_result.get("ret", [])
    if isinstance(ret, list) and len(ret) >= 4:
        note_count = ret[1]
    else:
        return "No notes in take"
    
    # Get selected notes
    selected_notes = []
    for i in range(note_count):
        note_result = await bridge.call_lua("MIDI_GetNote", [take_handle, i])
        if note_result.get("ok"):
            ret = note_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 8:
                selected = ret[1]
                if selected:
                    pitch = ret[5]
                    ppq_pos = ret[3]
                    selected_notes.append(f"Note {pitch} at PPQ {ppq_pos}")
    
    if selected_notes:
        return f"Selected notes: {', '.join(selected_notes[:5])}{'...' if len(selected_notes) > 5 else ''}"
    else:
        return "No selected notes"


async def midi_set_note_selected(item_index: int, take_index: int, 
                                 note_index: int, selected: bool) -> str:
    """Set MIDI note selection state"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get note info first
    note_result = await bridge.call_lua("MIDI_GetNote", [take_handle, note_index])
    if not note_result.get("ok"):
        raise Exception(f"Failed to get note at index {note_index}")
    
    ret = note_result.get("ret", [])
    if not isinstance(ret, list) or len(ret) < 8:
        raise Exception("Invalid note data")
    
    # Extract note parameters
    _, _, muted, start_ppq, end_ppq, chan, pitch, vel = ret[:8]
    
    # Set note with new selection state
    result = await bridge.call_lua("MIDI_SetNote", [
        take_handle, note_index, selected, muted, start_ppq, end_ppq, chan, pitch, vel, False
    ])
    
    if result.get("ok"):
        state = "selected" if selected else "unselected"
        return f"Note {note_index} {state}"
    else:
        raise Exception(f"Failed to set note selection: {result.get('error', 'Unknown error')}")


async def midi_select_cc(item_index: int, take_index: int, 
                        cc_num: int, channel: int = -1) -> str:
    """Select all CC events of a specific type"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Count CC events
    count_result = await bridge.call_lua("MIDI_CountEvts", [take_handle])
    if not count_result.get("ok"):
        raise Exception("Failed to count MIDI events")
    
    ret = count_result.get("ret", [])
    if isinstance(ret, list) and len(ret) >= 4:
        cc_count = ret[2]
    else:
        return "No CC events in take"
    
    # Select matching CC events
    selected = 0
    for i in range(cc_count):
        cc_result = await bridge.call_lua("MIDI_GetCC", [take_handle, i])
        if cc_result.get("ok"):
            ret = cc_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 7:
                _, _, muted, ppq, msg1, chan_msg, msg2 = ret[:7]
                cc_type = msg1
                cc_chan = chan_msg & 0x0F
                
                if cc_type == cc_num and (channel == -1 or cc_chan == channel):
                    # Set CC as selected
                    await bridge.call_lua("MIDI_SetCC", [
                        take_handle, i, True, muted, ppq, msg1, chan_msg, msg2, False
                    ])
                    selected += 1
    
    chan_str = f" on channel {channel}" if channel >= 0 else ""
    return f"Selected {selected} CC{cc_num} events{chan_str}"


async def midi_get_grid(item_index: int, take_index: int) -> str:
    """Get MIDI grid settings"""
    # Get item and take
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
            swing, note_len = ret[:2]
            return f"MIDI grid: swing={swing:.2f}, note_len={note_len}"
        else:
            return "Failed to get MIDI grid settings"
    else:
        raise Exception(f"Failed to get MIDI grid: {result.get('error', 'Unknown error')}")


async def midi_set_item_extents(item_index: int, take_index: int) -> str:
    """Set media item extents to match MIDI content"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set item extents
    result = await bridge.call_lua("MIDI_SetItemExtents", [item_handle, take_handle])
    
    if result.get("ok"):
        return "Set item extents to match MIDI content"
    else:
        raise Exception(f"Failed to set item extents: {result.get('error', 'Unknown error')}")


async def midi_get_proj_qn_from_ppq(item_index: int, take_index: int, ppq: float) -> str:
    """Convert take PPQ to project QN position"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Convert PPQ to project QN
    result = await bridge.call_lua("MIDI_GetProjQNFromPPQPos", [take_handle, ppq])
    
    if result.get("ok"):
        qn = result.get("ret", 0.0)
        return f"PPQ {ppq} = {qn:.3f} QN in project"
    else:
        raise Exception(f"Failed to convert PPQ to QN: {result.get('error', 'Unknown error')}")


async def midi_get_ppq_from_proj_qn(item_index: int, take_index: int, qn: float) -> str:
    """Convert project QN to take PPQ position"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Convert QN to PPQ
    result = await bridge.call_lua("MIDI_GetPPQPosFromProjQN", [take_handle, qn])
    
    if result.get("ok"):
        ppq = result.get("ret", 0.0)
        return f"{qn:.3f} QN = PPQ {ppq} in take"
    else:
        raise Exception(f"Failed to convert QN to PPQ: {result.get('error', 'Unknown error')}")


async def midi_refresh_editor() -> str:
    """Refresh the active MIDI editor display"""
    # Get active editor
    editor_result = await bridge.call_lua("MIDIEditor_GetActive", [])
    if not editor_result.get("ok") or not editor_result.get("ret"):
        return "No active MIDI editor to refresh"
    
    editor_handle = editor_result.get("ret")
    
    # Refresh display (using a null command)
    result = await bridge.call_lua("MIDIEditor_OnCommand", [editor_handle, 0])
    
    return "Refreshed MIDI editor display"


async def midi_humanize_notes(item_index: int, take_index: int, 
                             strength: float = 0.1, timing: bool = True, 
                             velocity: bool = True) -> str:
    """Humanize MIDI notes (timing and/or velocity)"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Count notes
    count_result = await bridge.call_lua("MIDI_CountEvts", [take_handle])
    if not count_result.get("ok"):
        raise Exception("Failed to count MIDI events")
    
    ret = count_result.get("ret", [])
    if isinstance(ret, list) and len(ret) >= 4:
        note_count = ret[1]
    else:
        return "No notes to humanize"
    
    # Humanize each selected note
    humanized = 0
    for i in range(note_count):
        note_result = await bridge.call_lua("MIDI_GetNote", [take_handle, i])
        if note_result.get("ok"):
            ret = note_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 8:
                _, selected, muted, start_ppq, end_ppq, chan, pitch, vel = ret[:8]
                
                if selected:
                    # Apply humanization
                    if timing:
                        # Random timing offset (in PPQ)
                        import random
                        ppq_offset = random.uniform(-strength * 240, strength * 240)  # 240 PPQ = 1 beat
                        start_ppq += ppq_offset
                        end_ppq += ppq_offset
                    
                    if velocity:
                        # Random velocity adjustment
                        import random
                        vel_offset = int(random.uniform(-strength * 20, strength * 20))
                        vel = max(1, min(127, vel + vel_offset))
                    
                    # Update note
                    await bridge.call_lua("MIDI_SetNote", [
                        take_handle, i, selected, muted, start_ppq, end_ppq, chan, pitch, vel, False
                    ])
                    humanized += 1
    
    # Sort notes after timing changes
    if timing and humanized > 0:
        await bridge.call_lua("MIDI_Sort", [take_handle])
    
    params = []
    if timing:
        params.append("timing")
    if velocity:
        params.append("velocity")
    
    return f"Humanized {humanized} notes ({', '.join(params)}) with strength {strength}"


# ============================================================================
# MIDI Display & Visualization (8 tools)
# ============================================================================

async def midi_get_note_name(note_number: int) -> str:
    """Get note name from MIDI note number"""
    result = await bridge.call_lua("GetNoteName", [note_number])
    
    if result.get("ok"):
        note_name = result.get("ret", "")
        if note_name:
            return f"Note {note_number}: {note_name}"
        else:
            return f"Note {note_number}: Unknown"
    else:
        raise Exception(f"Failed to get note name: {result.get('error', 'Unknown error')}")


async def midi_disablesorting(item_index: int, take_index: int, disable: bool) -> str:
    """Enable/disable automatic MIDI sorting"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set sorting state
    result = await bridge.call_lua("MIDI_DisableSort", [take_handle, disable])
    
    if result.get("ok"):
        state = "disabled" if disable else "enabled"
        return f"MIDI auto-sorting {state}"
    else:
        raise Exception(f"Failed to set MIDI sorting: {result.get('error', 'Unknown error')}")


async def midi_get_recent_input_event(idx: int) -> str:
    """Get recent MIDI input event"""
    result = await bridge.call_lua("MIDI_GetRecentInputEvent", [idx])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 4:
            ts, msg1, msg2, msg3 = ret[:4]
            event_type = (msg1 >> 4) & 0xF
            channel = msg1 & 0xF
            
            event_names = {
                8: "Note Off",
                9: "Note On",
                10: "Aftertouch",
                11: "CC",
                12: "Program Change",
                13: "Channel Pressure",
                14: "Pitch Bend"
            }
            
            event_name = event_names.get(event_type, f"Type {event_type}")
            return f"Input {idx}: {event_name} ch{channel+1} ({msg1:02X} {msg2:02X} {msg3:02X}) @ {ts:.3f}"
        else:
            return f"No input event at index {idx}"
    else:
        raise Exception(f"Failed to get input event: {result.get('error', 'Unknown error')}")


async def midi_get_text_sysex_evt(item_index: int, take_index: int, 
                                  event_index: int) -> str:
    """Get text or sysex event"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get text/sysex event
    result = await bridge.call_lua("MIDI_GetTextSysexEvt", [take_handle, event_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 5:
            retval, selected, muted, ppq, evt_type, msg = ret[:6]
            if retval:
                type_names = {
                    -1: "Sysex",
                    1: "Text",
                    2: "Copyright",
                    3: "Track Name",
                    4: "Instrument",
                    5: "Lyric",
                    6: "Marker",
                    7: "Cue Point"
                }
                type_str = type_names.get(evt_type, f"Type {evt_type}")
                return f"Event {event_index}: {type_str} at PPQ {ppq} - '{msg[:50]}{'...' if len(msg) > 50 else ''}'"
            else:
                return f"No text/sysex event at index {event_index}"
        else:
            return "Failed to get text/sysex event data"
    else:
        raise Exception(f"Failed to get text/sysex event: {result.get('error', 'Unknown error')}")


async def midi_get_cc_shape(item_index: int, take_index: int, cc_index: int) -> str:
    """Get CC shape/curve type"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get CC shape
    result = await bridge.call_lua("MIDI_GetCCShape", [take_handle, cc_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, shape, beztension = ret[:3] if len(ret) >= 3 else ret + [0]
            if retval:
                shape_names = {
                    0: "Linear",
                    1: "Square",
                    2: "Slow start/end",
                    3: "Fast start",
                    4: "Fast end",
                    5: "Bezier"
                }
                shape_str = shape_names.get(shape, f"Shape {shape}")
                tension_str = f" (tension {beztension:.2f})" if shape == 5 else ""
                return f"CC {cc_index} shape: {shape_str}{tension_str}"
            else:
                return f"No CC at index {cc_index}"
        else:
            return "Failed to get CC shape data"
    else:
        raise Exception(f"Failed to get CC shape: {result.get('error', 'Unknown error')}")


async def midi_set_cc_shape(item_index: int, take_index: int, cc_index: int, 
                           shape: int, beztension: float = 0.0) -> str:
    """Set CC shape/curve type"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set CC shape
    result = await bridge.call_lua("MIDI_SetCCShape", [take_handle, cc_index, shape, beztension, False])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            shape_names = {
                0: "Linear",
                1: "Square", 
                2: "Slow start/end",
                3: "Fast start",
                4: "Fast end",
                5: "Bezier"
            }
            shape_str = shape_names.get(shape, f"Shape {shape}")
            tension_str = f" with tension {beztension:.2f}" if shape == 5 else ""
            return f"Set CC {cc_index} to {shape_str}{tension_str}"
        else:
            return f"Failed to set CC shape"
    else:
        raise Exception(f"Failed to set CC shape: {result.get('error', 'Unknown error')}")


async def midi_get_proj_time_from_ppq(item_index: int, take_index: int, ppq: float) -> str:
    """Convert take PPQ to project time"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Convert PPQ to project time
    result = await bridge.call_lua("MIDI_GetProjTimeFromPPQPos", [take_handle, ppq])
    
    if result.get("ok"):
        time = result.get("ret", 0.0)
        return f"PPQ {ppq} = {time:.3f} seconds in project"
    else:
        raise Exception(f"Failed to convert PPQ to time: {result.get('error', 'Unknown error')}")


async def midi_get_ppq_from_proj_time(item_index: int, take_index: int, time: float) -> str:
    """Convert project time to take PPQ"""
    # Get item and take
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
        return f"{time:.3f} seconds = PPQ {ppq} in take"
    else:
        raise Exception(f"Failed to convert time to PPQ: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_midi_editor_tools(mcp) -> int:
    """Register all MIDI editor tools with the MCP instance"""
    tools = [
        # MIDI Editor Window Management
        (midi_open_editor, "Open MIDI editor for a take"),
        (midi_editor_get_active, "Get the active MIDI editor window"),
        (midi_editor_get_take, "Get the take from a MIDI editor"),
        (midi_editor_get_setting_int, "Get integer setting from MIDI editor"),
        (midi_editor_set_setting_int, "Set integer setting in MIDI editor"),
        (midi_editor_get_mode, "Get MIDI editor mode"),
        (midi_editor_on_command, "Execute command in active MIDI editor"),
        (midi_editor_last_focused, "Get the last focused MIDI editor"),
        
        # MIDI Note Selection & Manipulation
        (midi_select_notes, "Select MIDI notes in a range"),
        (midi_get_selected_notes, "Get all selected MIDI notes"),
        (midi_set_note_selected, "Set MIDI note selection state"),
        (midi_select_cc, "Select all CC events of a specific type"),
        (midi_get_grid, "Get MIDI grid settings"),
        (midi_set_item_extents, "Set media item extents to match MIDI content"),
        (midi_get_proj_qn_from_ppq, "Convert take PPQ to project QN position"),
        (midi_get_ppq_from_proj_qn, "Convert project QN to take PPQ position"),
        (midi_refresh_editor, "Refresh the active MIDI editor display"),
        (midi_humanize_notes, "Humanize MIDI notes (timing and/or velocity)"),
        
        # MIDI Display & Visualization
        (midi_get_note_name, "Get note name from MIDI note number"),
        (midi_disablesorting, "Enable/disable automatic MIDI sorting"),
        (midi_get_recent_input_event, "Get recent MIDI input event"),
        (midi_get_text_sysex_evt, "Get text or sysex event"),
        (midi_get_cc_shape, "Get CC shape/curve type"),
        (midi_set_cc_shape, "Set CC shape/curve type"),
        (midi_get_proj_time_from_ppq, "Convert take PPQ to project time"),
        (midi_get_ppq_from_proj_time, "Convert project time to take PPQ"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)