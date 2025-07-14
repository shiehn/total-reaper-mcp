"""
Project State Management Tools for REAPER MCP

This module contains tools for managing project state, undo/redo operations,
and extended state management.
"""

from typing import Optional, Any
from ..bridge import bridge


# ============================================================================
# Undo System (12 tools)
# ============================================================================

async def undo_begin_block2(project_index: int = 0) -> str:
    """Begin a new undo block (enhanced version)"""
    result = await bridge.call_lua("Undo_BeginBlock2", [project_index])
    
    if result.get("ok"):
        return "Started new undo block"
    else:
        raise Exception(f"Failed to begin undo block: {result.get('error', 'Unknown error')}")


async def undo_end_block2(desc: str, extra_flags: int = 0, project_index: int = 0) -> str:
    """End the current undo block with description (enhanced version)"""
    # Extra flags:
    # -1 = all changes
    # 1 = track configurations
    # 2 = FX
    # 4 = items
    # 8 = project states
    # 16 = freeze states
    # 32 = track envelopes
    # 64 = take envelopes
    # 128 = track sends
    result = await bridge.call_lua("Undo_EndBlock2", [project_index, desc, extra_flags])
    
    if result.get("ok"):
        return f"Ended undo block: {desc}"
    else:
        raise Exception(f"Failed to end undo block: {result.get('error', 'Unknown error')}")


async def undo_can_undo2(project_index: int = 0) -> str:
    """Check if undo is available"""
    result = await bridge.call_lua("Undo_CanUndo2", [project_index])
    
    if result.get("ok"):
        desc = result.get("ret", "")
        if desc:
            return f"Can undo: {desc}"
        else:
            return "Nothing to undo"
    else:
        raise Exception(f"Failed to check undo: {result.get('error', 'Unknown error')}")


async def undo_can_redo2(project_index: int = 0) -> str:
    """Check if redo is available"""
    result = await bridge.call_lua("Undo_CanRedo2", [project_index])
    
    if result.get("ok"):
        desc = result.get("ret", "")
        if desc:
            return f"Can redo: {desc}"
        else:
            return "Nothing to redo"
    else:
        raise Exception(f"Failed to check redo: {result.get('error', 'Unknown error')}")


async def undo_do_undo2(project_index: int = 0) -> str:
    """Perform undo"""
    result = await bridge.call_lua("Undo_DoUndo2", [project_index])
    
    if result.get("ok"):
        return "Performed undo"
    else:
        raise Exception(f"Failed to undo: {result.get('error', 'Unknown error')}")


async def undo_do_redo2(project_index: int = 0) -> str:
    """Perform redo"""
    result = await bridge.call_lua("Undo_DoRedo2", [project_index])
    
    if result.get("ok"):
        return "Performed redo"
    else:
        raise Exception(f"Failed to redo: {result.get('error', 'Unknown error')}")


async def undo_on_state_change(desc: str) -> str:
    """Report state change for undo history"""
    result = await bridge.call_lua("Undo_OnStateChange", [desc])
    
    if result.get("ok"):
        return f"Recorded state change: {desc}"
    else:
        raise Exception(f"Failed to record state change: {result.get('error', 'Unknown error')}")


async def undo_on_state_change2(project_index: int, desc: str) -> str:
    """Report state change for undo history (project-specific)"""
    result = await bridge.call_lua("Undo_OnStateChange2", [project_index, desc])
    
    if result.get("ok"):
        return f"Recorded state change: {desc}"
    else:
        raise Exception(f"Failed to record state change: {result.get('error', 'Unknown error')}")


async def undo_on_state_change_ex(desc: str, whichStates: int, trackparm: int) -> str:
    """Report state change with extended info"""
    # whichStates: same flags as undo_end_block2
    result = await bridge.call_lua("Undo_OnStateChangeEx", [desc, whichStates, trackparm])
    
    if result.get("ok"):
        return f"Recorded extended state change: {desc}"
    else:
        raise Exception(f"Failed to record extended state change: {result.get('error', 'Unknown error')}")


async def undo_on_state_change_ex2(project_index: int, desc: str, whichStates: int, trackparm: int) -> str:
    """Report state change with extended info (project-specific)"""
    result = await bridge.call_lua("Undo_OnStateChangeEx2", [project_index, desc, whichStates, trackparm])
    
    if result.get("ok"):
        return f"Recorded extended state change: {desc}"
    else:
        raise Exception(f"Failed to record extended state change: {result.get('error', 'Unknown error')}")


async def undo_on_state_change_item(project_index: int, desc: str, item_index: int) -> str:
    """Report item-specific state change"""
    # Get the item
    item_result = await bridge.call_lua("GetMediaItem", [project_index, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    result = await bridge.call_lua("Undo_OnStateChange_Item", [project_index, desc, item_handle])
    
    if result.get("ok"):
        return f"Recorded item state change: {desc}"
    else:
        raise Exception(f"Failed to record item state change: {result.get('error', 'Unknown error')}")


async def csurf_flush_undo(force: bool = False) -> str:
    """Flush undo buffer"""
    result = await bridge.call_lua("CSurf_FlushUndo", [force])
    
    if result.get("ok"):
        return "Flushed undo buffer"
    else:
        raise Exception(f"Failed to flush undo: {result.get('error', 'Unknown error')}")


# ============================================================================
# Extended State Management (12 tools)
# ============================================================================

async def get_ext_state(section: str, key: str) -> str:
    """Get extended state value"""
    result = await bridge.call_lua("GetExtState", [section, key])
    
    if result.get("ok"):
        value = result.get("ret", "")
        if value:
            return f"[{section}] {key} = {value}"
        else:
            return f"[{section}] {key} = (not set)"
    else:
        raise Exception(f"Failed to get extended state: {result.get('error', 'Unknown error')}")


async def set_ext_state(section: str, key: str, value: str, persist: bool = True) -> str:
    """Set extended state value"""
    result = await bridge.call_lua("SetExtState", [section, key, value, persist])
    
    if result.get("ok"):
        persist_str = "persistent" if persist else "temporary"
        return f"Set {persist_str} state: [{section}] {key} = {value}"
    else:
        raise Exception(f"Failed to set extended state: {result.get('error', 'Unknown error')}")


async def has_ext_state(section: str, key: str) -> str:
    """Check if extended state exists"""
    result = await bridge.call_lua("HasExtState", [section, key])
    
    if result.get("ok"):
        exists = result.get("ret", False)
        if exists:
            return f"State exists: [{section}] {key}"
        else:
            return f"State does not exist: [{section}] {key}"
    else:
        raise Exception(f"Failed to check extended state: {result.get('error', 'Unknown error')}")


async def delete_ext_state(section: str, key: str, persist: bool = True) -> str:
    """Delete extended state value"""
    result = await bridge.call_lua("DeleteExtState", [section, key, persist])
    
    if result.get("ok"):
        persist_str = "persistent" if persist else "temporary"
        return f"Deleted {persist_str} state: [{section}] {key}"
    else:
        raise Exception(f"Failed to delete extended state: {result.get('error', 'Unknown error')}")


async def get_proj_ext_state(section: str, key: str, project_index: int = 0) -> str:
    """Get project-specific extended state"""
    result = await bridge.call_lua("GetProjExtState", [project_index, section, key])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, value = ret[:2]
            if retval > 0:
                return f"Project [{section}] {key} = {value}"
            else:
                return f"Project [{section}] {key} = (not set)"
        else:
            return f"Project [{section}] {key} = (not set)"
    else:
        raise Exception(f"Failed to get project extended state: {result.get('error', 'Unknown error')}")


async def set_proj_ext_state(section: str, key: str, value: str, project_index: int = 0) -> str:
    """Set project-specific extended state"""
    result = await bridge.call_lua("SetProjExtState", [project_index, section, key, value])
    
    if result.get("ok"):
        return f"Set project state: [{section}] {key} = {value}"
    else:
        raise Exception(f"Failed to set project extended state: {result.get('error', 'Unknown error')}")


async def enum_proj_ext_state(section: str, index: int, project_index: int = 0) -> str:
    """Enumerate project extended state keys"""
    result = await bridge.call_lua("EnumProjExtState", [project_index, section, index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            retval, key, value = ret[:3]
            if retval:
                return f"Key {index}: {key} = {value}"
            else:
                return f"No key at index {index}"
        else:
            return f"No key at index {index}"
    else:
        raise Exception(f"Failed to enumerate project extended state: {result.get('error', 'Unknown error')}")


async def get_set_project_author(set: bool = False, author: str = "", project_index: int = 0) -> str:
    """Get or set project author"""
    result = await bridge.call_lua("GetSetProjectAuthor", [project_index, set, author])
    
    if result.get("ok"):
        if set:
            return f"Set project author to: {author}"
        else:
            author_name = result.get("ret", "")
            return f"Project author: {author_name if author_name else '(not set)'}"
    else:
        raise Exception(f"Failed to get/set project author: {result.get('error', 'Unknown error')}")


async def get_set_project_notes(set: bool = False, notes: str = "", project_index: int = 0) -> str:
    """Get or set project notes"""
    result = await bridge.call_lua("GetSetProjectNotes", [project_index, set, notes])
    
    if result.get("ok"):
        if set:
            return f"Set project notes"
        else:
            project_notes = result.get("ret", "")
            return f"Project notes: {project_notes if project_notes else '(empty)'}"
    else:
        raise Exception(f"Failed to get/set project notes: {result.get('error', 'Unknown error')}")


async def get_set_project_info_string(desc: str, value: str = "", set: bool = False, project_index: int = 0) -> str:
    """Get or set project info string"""
    result = await bridge.call_lua("GetSetProjectInfo_String", [project_index, desc, value, set])
    
    if result.get("ok"):
        if set:
            return f"Set project {desc} to: {value}"
        else:
            info_value = result.get("ret", "")
            return f"Project {desc}: {info_value if info_value else '(not set)'}"
    else:
        raise Exception(f"Failed to get/set project info: {result.get('error', 'Unknown error')}")


async def get_project_time_offset(project_index: int = 0) -> str:
    """Get project time offset"""
    result = await bridge.call_lua("GetProjectTimeOffset", [project_index, False])
    
    if result.get("ok"):
        offset = result.get("ret", 0.0)
        return f"Project time offset: {offset:.3f} seconds"
    else:
        raise Exception(f"Failed to get project time offset: {result.get('error', 'Unknown error')}")


async def get_all_project_play_states(project_index: int = 0) -> str:
    """Get play states of all open projects"""
    result = await bridge.call_lua("GetAllProjectPlayStates", [project_index])
    
    if result.get("ok"):
        states = result.get("ret", 0)
        # Decode bit flags
        play_states = []
        if states & 1:
            play_states.append("playing")
        if states & 2:
            play_states.append("paused")
        if states & 4:
            play_states.append("recording")
        
        if play_states:
            return f"Project play states: {', '.join(play_states)}"
        else:
            return "All projects stopped"
    else:
        raise Exception(f"Failed to get project play states: {result.get('error', 'Unknown error')}")


# ============================================================================
# State Chunk Operations (6 tools)
# ============================================================================

async def get_track_state_chunk(track_index: int, flags: int = 0) -> str:
    """Get track state chunk (configuration as text)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get state chunk
    result = await bridge.call_lua("GetTrackStateChunk", [track_handle, "", 65536, False])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, chunk = ret[:2]
            if retval:
                lines = chunk.split('\n')
                return f"Track state chunk ({len(lines)} lines)"
            else:
                return "Failed to get track state chunk"
        else:
            return "Failed to get track state chunk"
    else:
        raise Exception(f"Failed to get track state chunk: {result.get('error', 'Unknown error')}")


async def set_track_state_chunk(track_index: int, chunk: str, undo: bool = True) -> str:
    """Set track state chunk (restore configuration from text)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set state chunk
    result = await bridge.call_lua("SetTrackStateChunk", [track_handle, chunk, undo])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set track state chunk"
        else:
            return "Failed to set track state chunk"
    else:
        raise Exception(f"Failed to set track state chunk: {result.get('error', 'Unknown error')}")


async def get_item_state_chunk(item_index: int, flags: int = 0) -> str:
    """Get media item state chunk"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get state chunk
    result = await bridge.call_lua("GetItemStateChunk", [item_handle, "", 65536, False])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, chunk = ret[:2]
            if retval:
                lines = chunk.split('\n')
                return f"Item state chunk ({len(lines)} lines)"
            else:
                return "Failed to get item state chunk"
        else:
            return "Failed to get item state chunk"
    else:
        raise Exception(f"Failed to get item state chunk: {result.get('error', 'Unknown error')}")


async def set_item_state_chunk(item_index: int, chunk: str, undo: bool = True) -> str:
    """Set media item state chunk"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Set state chunk
    result = await bridge.call_lua("SetItemStateChunk", [item_handle, chunk, undo])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set item state chunk"
        else:
            return "Failed to set item state chunk"
    else:
        raise Exception(f"Failed to set item state chunk: {result.get('error', 'Unknown error')}")


async def get_envelope_state_chunk(track_index: int, envelope_name: str, flags: int = 0) -> str:
    """Get envelope state chunk"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track")
    
    env_handle = env_result.get("ret")
    
    # Get state chunk
    result = await bridge.call_lua("GetEnvelopeStateChunk", [env_handle, "", 65536, False])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, chunk = ret[:2]
            if retval:
                lines = chunk.split('\n')
                return f"Envelope state chunk ({len(lines)} lines)"
            else:
                return "Failed to get envelope state chunk"
        else:
            return "Failed to get envelope state chunk"
    else:
        raise Exception(f"Failed to get envelope state chunk: {result.get('error', 'Unknown error')}")


async def set_envelope_state_chunk(track_index: int, envelope_name: str, chunk: str, undo: bool = True) -> str:
    """Set envelope state chunk"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get envelope
    env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
    if not env_result.get("ok") or not env_result.get("ret"):
        raise Exception(f"Failed to find envelope '{envelope_name}' on track")
    
    env_handle = env_result.get("ret")
    
    # Set state chunk
    result = await bridge.call_lua("SetEnvelopeStateChunk", [env_handle, chunk, undo])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Set envelope state chunk"
        else:
            return "Failed to set envelope state chunk"
    else:
        raise Exception(f"Failed to set envelope state chunk: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_project_state_tools(mcp) -> int:
    """Register all project state tools with the MCP instance"""
    tools = [
        # Undo System
        (undo_begin_block2, "Begin a new undo block (enhanced version)"),
        (undo_end_block2, "End the current undo block with description"),
        (undo_can_undo2, "Check if undo is available"),
        (undo_can_redo2, "Check if redo is available"),
        (undo_do_undo2, "Perform undo"),
        (undo_do_redo2, "Perform redo"),
        (undo_on_state_change, "Report state change for undo history"),
        (undo_on_state_change2, "Report state change for undo history (project-specific)"),
        (undo_on_state_change_ex, "Report state change with extended info"),
        (undo_on_state_change_ex2, "Report state change with extended info (project-specific)"),
        (undo_on_state_change_item, "Report item-specific state change"),
        (csurf_flush_undo, "Flush undo buffer"),
        
        # Extended State Management
        (get_ext_state, "Get extended state value"),
        (set_ext_state, "Set extended state value"),
        (has_ext_state, "Check if extended state exists"),
        (delete_ext_state, "Delete extended state value"),
        (get_proj_ext_state, "Get project-specific extended state"),
        (set_proj_ext_state, "Set project-specific extended state"),
        (enum_proj_ext_state, "Enumerate project extended state keys"),
        (get_set_project_author, "Get or set project author"),
        (get_set_project_notes, "Get or set project notes"),
        (get_set_project_info_string, "Get or set project info string"),
        (get_project_time_offset, "Get project time offset"),
        (get_all_project_play_states, "Get play states of all open projects"),
        
        # State Chunk Operations
        (get_track_state_chunk, "Get track state chunk (configuration as text)"),
        (set_track_state_chunk, "Set track state chunk (restore configuration from text)"),
        (get_item_state_chunk, "Get media item state chunk"),
        (set_item_state_chunk, "Set media item state chunk"),
        (get_envelope_state_chunk, "Get envelope state chunk"),
        (set_envelope_state_chunk, "Set envelope state chunk"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)