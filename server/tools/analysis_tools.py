"""
Analysis Tools for REAPER MCP

This module contains analysis tools particularly useful for AI agents
to understand project structure, content, and patterns.
"""

from typing import List, Dict, Any
from ..bridge import bridge


# ============================================================================
# Project Analysis
# ============================================================================

async def analyze_project_structure() -> str:
    """Analyze overall project structure"""
    # Get basic counts
    track_count_result = await bridge.call_lua("CountTracks", [0])
    item_count_result = await bridge.call_lua("CountMediaItems", [0])
    marker_count_result = await bridge.call_lua("CountProjectMarkers", [0])
    
    tracks = track_count_result.get("ret", 0) if track_count_result.get("ok") else 0
    items = item_count_result.get("ret", 0) if item_count_result.get("ok") else 0
    markers = marker_count_result.get("num_markers", 0) if marker_count_result.get("ok") else 0
    
    # Get project length
    length_result = await bridge.call_lua("GetProjectLength", [0])
    length = length_result.get("ret", 0) if length_result.get("ok") else 0
    
    minutes = int(length // 60)
    seconds = length % 60
    
    return (f"Project structure: {tracks} tracks, {items} items, {markers} markers/regions, "
            f"length: {minutes}:{seconds:05.2f}")


async def get_track_hierarchy() -> str:
    """Get track folder hierarchy information"""
    result = await bridge.call_lua("CountTracks", [0])
    track_count = result.get("ret", 0) if result.get("ok") else 0
    
    hierarchy = []
    folder_stack = []
    
    for i in range(track_count):
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, i])
        if not track_result.get("ok"):
            continue
        
        # Get folder info
        folder_result = await bridge.call_lua("GetMediaTrackInfo_Value", 
                                             [track_result.get("ret"), "I_FOLDERDEPTH"])
        folder_depth = int(folder_result.get("ret", 0)) if folder_result.get("ok") else 0
        
        # Get track name
        name_result = await bridge.call_lua("GetTrackName", [i])
        name = name_result.get("ret", f"Track {i+1}") if name_result.get("ok") else f"Track {i+1}"
        
        indent = "  " * len(folder_stack)
        
        if folder_depth == 1:  # Folder start
            hierarchy.append(f"{indent}📁 {name}")
            folder_stack.append(i)
        elif folder_depth < 0:  # Folder end
            hierarchy.append(f"{indent}🎵 {name}")
            for _ in range(abs(folder_depth)):
                if folder_stack:
                    folder_stack.pop()
        else:  # Normal track
            hierarchy.append(f"{indent}🎵 {name}")
    
    return "Track hierarchy:\n" + "\n".join(hierarchy)


async def analyze_tempo_map() -> str:
    """Analyze tempo changes in the project"""
    # Count tempo markers
    count_result = await bridge.call_lua("CountTempoTimeSigMarkers", [0])
    count = count_result.get("ret", 0) if count_result.get("ok") else 0
    
    tempo_changes = []
    
    for i in range(min(count, 10)):  # Limit to first 10 for brevity
        marker_result = await bridge.call_lua("GetTempoTimeSigMarker", [0, i])
        if marker_result.get("ok"):
            time = marker_result.get("timepos", 0)
            bpm = marker_result.get("bpm", 120)
            ts_num = marker_result.get("timesig_num", 4)
            ts_denom = marker_result.get("timesig_denom", 4)
            tempo_changes.append(f"  {time:.1f}s: {bpm:.1f} BPM, {ts_num}/{ts_denom}")
    
    if tempo_changes:
        return f"Tempo map ({count} changes):\n" + "\n".join(tempo_changes)
    else:
        return "No tempo changes in project (constant tempo)"


# ============================================================================
# Content Analysis
# ============================================================================

async def analyze_track_content(track_index: int) -> str:
    """Analyze content of a specific track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok"):
        raise Exception(f"Failed to get track {track_index}")
    
    track = track_result.get("ret")
    
    # Get track name
    name_result = await bridge.call_lua("GetTrackName", [track_index])
    track_name = name_result.get("ret", f"Track {track_index + 1}") if name_result.get("ok") else f"Track {track_index + 1}"
    
    # Count items
    item_count_result = await bridge.call_lua("CountTrackMediaItems", [track])
    item_count = item_count_result.get("ret", 0) if item_count_result.get("ok") else 0
    
    # Count envelopes
    env_count_result = await bridge.call_lua("CountTrackEnvelopes", [track])
    env_count = env_count_result.get("ret", 0) if env_count_result.get("ok") else 0
    
    # Count FX
    fx_count_result = await bridge.call_lua("TrackFX_GetCount", [track])
    fx_count = fx_count_result.get("ret", 0) if fx_count_result.get("ok") else 0
    
    # Check if armed
    armed_result = await bridge.call_lua("GetMediaTrackInfo_Value", [track, "I_RECARM"])
    is_armed = bool(armed_result.get("ret", 0)) if armed_result.get("ok") else False
    
    # Get total item length
    total_length = 0
    for i in range(item_count):
        item_result = await bridge.call_lua("GetTrackMediaItem", [track, i])
        if item_result.get("ok"):
            length_result = await bridge.call_lua("GetMediaItemInfo_Value", 
                                                 [item_result.get("ret"), "D_LENGTH"])
            if length_result.get("ok"):
                total_length += length_result.get("ret", 0)
    
    analysis = [
        f"Track '{track_name}' analysis:",
        f"  Items: {item_count}",
        f"  Total content length: {total_length:.1f}s",
        f"  Envelopes: {env_count}",
        f"  FX: {fx_count}",
        f"  Armed: {'Yes' if is_armed else 'No'}"
    ]
    
    return "\n".join(analysis)


async def find_silent_regions(threshold_db: float = -60.0, min_length: float = 1.0) -> str:
    """Find silent regions in the project"""
    # This is a simplified version - full implementation would analyze audio
    return (f"Silent region detection (threshold: {threshold_db}dB, min length: {min_length}s) "
            "requires audio analysis - use render and analyze workflow")


async def analyze_item_overlaps() -> str:
    """Find overlapping media items"""
    item_count_result = await bridge.call_lua("CountMediaItems", [0])
    item_count = item_count_result.get("ret", 0) if item_count_result.get("ok") else 0
    
    overlaps = []
    items_data = []
    
    # Collect all items with their positions
    for i in range(item_count):
        item_result = await bridge.call_lua("GetMediaItem", [0, i])
        if not item_result.get("ok"):
            continue
        
        item = item_result.get("ret")
        
        # Get position and length
        pos_result = await bridge.call_lua("GetMediaItemInfo_Value", [item, "D_POSITION"])
        length_result = await bridge.call_lua("GetMediaItemInfo_Value", [item, "D_LENGTH"])
        track_result = await bridge.call_lua("GetMediaItem_Track", [item])
        
        if pos_result.get("ok") and length_result.get("ok") and track_result.get("ok"):
            pos = pos_result.get("ret", 0)
            length = length_result.get("ret", 0)
            track = track_result.get("ret")
            items_data.append((i, pos, pos + length, track))
    
    # Find overlaps on same track
    for i in range(len(items_data)):
        for j in range(i + 1, len(items_data)):
            if items_data[i][3] == items_data[j][3]:  # Same track
                # Check if items overlap
                if (items_data[i][1] < items_data[j][2] and 
                    items_data[j][1] < items_data[i][2]):
                    overlaps.append(f"Items {items_data[i][0]} and {items_data[j][0]} overlap")
    
    if overlaps:
        return f"Found {len(overlaps)} overlapping items:\n" + "\n".join(overlaps[:10])  # Limit to 10
    else:
        return "No overlapping items found"


# ============================================================================
# Pattern Detection
# ============================================================================

async def detect_loop_regions() -> str:
    """Detect potential loop regions based on item patterns"""
    item_count_result = await bridge.call_lua("CountMediaItems", [0])
    item_count = item_count_result.get("ret", 0) if item_count_result.get("ok") else 0
    
    # Collect items by track
    tracks_items = {}
    
    for i in range(item_count):
        item_result = await bridge.call_lua("GetMediaItem", [0, i])
        if not item_result.get("ok"):
            continue
        
        item = item_result.get("ret")
        
        # Get track
        track_result = await bridge.call_lua("GetMediaItem_Track", [item])
        if not track_result.get("ok"):
            continue
        
        track = track_result.get("ret")
        
        # Get position and length
        pos_result = await bridge.call_lua("GetMediaItemInfo_Value", [item, "D_POSITION"])
        length_result = await bridge.call_lua("GetMediaItemInfo_Value", [item, "D_LENGTH"])
        
        if pos_result.get("ok") and length_result.get("ok"):
            if track not in tracks_items:
                tracks_items[track] = []
            tracks_items[track].append({
                'pos': pos_result.get("ret", 0),
                'length': length_result.get("ret", 0)
            })
    
    # Look for repeating patterns
    patterns = []
    for track, items in tracks_items.items():
        if len(items) < 2:
            continue
        
        # Sort by position
        items.sort(key=lambda x: x['pos'])
        
        # Check for regular spacing
        gaps = []
        for i in range(1, len(items)):
            gap = items[i]['pos'] - (items[i-1]['pos'] + items[i-1]['length'])
            gaps.append(gap)
        
        # If gaps are consistent, we might have a loop
        if gaps and all(abs(g - gaps[0]) < 0.01 for g in gaps):
            patterns.append(f"Potential loop pattern on track (gap: {gaps[0]:.2f}s)")
    
    if patterns:
        return "Detected patterns:\n" + "\n".join(patterns[:5])  # Limit to 5
    else:
        return "No obvious loop patterns detected"


async def analyze_project_rhythm() -> str:
    """Analyze rhythmic structure based on item positions"""
    # Get tempo
    tempo_result = await bridge.call_lua("Master_GetTempo", [])
    tempo = tempo_result.get("ret", 120) if tempo_result.get("ok") else 120
    
    # Get time signature
    ts_result = await bridge.call_lua("GetTempoTimeSigMarker", [0, 0])
    ts_num = ts_result.get("timesig_num", 4) if ts_result.get("ok") else 4
    ts_denom = ts_result.get("timesig_denom", 4) if ts_result.get("ok") else 4
    
    # Calculate beat length
    beat_length = 60.0 / tempo
    measure_length = beat_length * ts_num
    
    # Count items on downbeats
    item_count_result = await bridge.call_lua("CountMediaItems", [0])
    item_count = item_count_result.get("ret", 0) if item_count_result.get("ok") else 0
    
    on_beat_count = 0
    near_beat_count = 0
    
    for i in range(item_count):
        item_result = await bridge.call_lua("GetMediaItem", [0, i])
        if not item_result.get("ok"):
            continue
        
        pos_result = await bridge.call_lua("GetMediaItemInfo_Value", 
                                          [item_result.get("ret"), "D_POSITION"])
        if pos_result.get("ok"):
            pos = pos_result.get("ret", 0)
            
            # Check if near a beat
            beat_offset = pos % beat_length
            if beat_offset < 0.05 or beat_offset > beat_length - 0.05:
                near_beat_count += 1
                
                # Check if on a downbeat
                measure_offset = pos % measure_length
                if measure_offset < 0.05 or measure_offset > measure_length - 0.05:
                    on_beat_count += 1
    
    return (f"Rhythm analysis: {tempo:.1f} BPM, {ts_num}/{ts_denom}\n"
            f"  Items on downbeats: {on_beat_count}\n"
            f"  Items on beats: {near_beat_count}\n"
            f"  Beat-aligned: {near_beat_count/item_count*100:.1f}%" if item_count > 0 else "No items")


# ============================================================================
# MIDI Analysis
# ============================================================================

async def analyze_midi_content_summary() -> str:
    """Get summary of all MIDI content in project"""
    item_count_result = await bridge.call_lua("CountMediaItems", [0])
    item_count = item_count_result.get("ret", 0) if item_count_result.get("ok") else 0
    
    total_notes = 0
    total_midi_items = 0
    pitch_range = [127, 0]  # min, max
    
    for i in range(item_count):
        item_result = await bridge.call_lua("GetMediaItem", [0, i])
        if not item_result.get("ok"):
            continue
        
        # Get active take
        take_result = await bridge.call_lua("GetActiveTake", [item_result.get("ret")])
        if not take_result.get("ok") or not take_result.get("ret"):
            continue
        
        take = take_result.get("ret")
        
        # Check if MIDI
        is_midi_result = await bridge.call_lua("TakeIsMIDI", [take])
        if not is_midi_result.get("ok") or not is_midi_result.get("ret"):
            continue
        
        total_midi_items += 1
        
        # Count events
        count_result = await bridge.call_lua("MIDI_CountEvts", [take])
        if count_result.get("ok"):
            notes = count_result.get("notes", 0)
            total_notes += notes
            
            # Sample first few notes for pitch range
            for n in range(min(notes, 20)):
                note_result = await bridge.call_lua("MIDI_GetNote", [take, n])
                if note_result.get("ok"):
                    pitch = note_result.get("pitch", 60)
                    pitch_range[0] = min(pitch_range[0], pitch)
                    pitch_range[1] = max(pitch_range[1], pitch)
    
    if total_midi_items > 0:
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        low_note = f"{note_names[pitch_range[0] % 12]}{pitch_range[0] // 12 - 1}"
        high_note = f"{note_names[pitch_range[1] % 12]}{pitch_range[1] // 12 - 1}"
        
        return (f"MIDI content summary:\n"
                f"  MIDI items: {total_midi_items}\n"
                f"  Total notes: {total_notes}\n"
                f"  Pitch range: {low_note} to {high_note}")
    else:
        return "No MIDI content found in project"


# ============================================================================
# Registration Function
# ============================================================================

def register_analysis_tools(mcp) -> int:
    """Register all analysis tools with the MCP instance"""
    tools = [
        # Project Analysis
        (analyze_project_structure, "Analyze overall project structure"),
        (get_track_hierarchy, "Get track folder hierarchy information"),
        (analyze_tempo_map, "Analyze tempo changes in the project"),
        
        # Content Analysis
        (analyze_track_content, "Analyze content of a specific track"),
        (find_silent_regions, "Find silent regions in the project"),
        (analyze_item_overlaps, "Find overlapping media items"),
        
        # Pattern Detection
        (detect_loop_regions, "Detect potential loop regions"),
        (analyze_project_rhythm, "Analyze rhythmic structure"),
        
        # MIDI Analysis
        (analyze_midi_content_summary, "Get summary of all MIDI content"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)