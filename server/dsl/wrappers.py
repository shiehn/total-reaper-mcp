"""
Canonical wrapper functions for DSL operations

These wrappers provide a high-level, natural language friendly interface
to REAPER operations. They use the resolver system to handle flexible inputs
and return consistent, structured responses.
"""

import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

from .resolvers import (
    resolve_track, resolve_time, resolve_items,
    TrackRef, TimeRef, ItemRef,
    ResolverError, DisambiguationNeeded,
    get_context
)

logger = logging.getLogger(__name__)

# Type aliases for clarity
TrackSelector = Union[str, int, Dict[str, Any]]
TimeSelector = Union[str, float, Dict[str, Any]]
ItemSelector = Union[str, Dict[str, Any]]
VolumeValue = Union[float, str, Dict[str, Any]]
PanValue = Union[float, str, Dict[str, Any]]

@dataclass
class OperationResult:
    """Standard result format for all operations"""
    success: bool
    action: str
    message: str
    targets: Optional[List[Dict[str, Any]]] = None
    changes: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    disambiguation_needed: Optional[Dict[str, Any]] = None
    reascript_calls: Optional[List[Dict[str, Any]]] = None
    
    def to_string(self) -> str:
        """Convert to user-friendly string message"""
        if self.success:
            return self.message
        else:
            return f"Error: {self.error or self.message}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "success": self.success,
            "action": self.action,
            "message": self.message,
            "targets": self.targets,
            "changes": self.changes,
            "error": self.error,
            "disambiguation_needed": self.disambiguation_needed,
            "reascript_calls": self.reascript_calls
        }

# Track Operations

async def track_create(bridge, name: Optional[str] = None, 
                      role: Optional[str] = None,
                      position: Optional[int] = None) -> OperationResult:
    """Create a new track with optional name and role"""
    # Start tracking ReaScript calls
    bridge.start_tracking()
    
    try:
        # Determine position
        if position is None:
            result = await bridge.call_lua("GetTrackCount", [])
            position = result.get("ret", 0) if result.get("ok") else 0
        
        # Create track
        result = await bridge.call_lua("InsertTrackAtIndex", [position, True])
        if not result.get("ok"):
            return OperationResult(
                success=False,
                action="track_create",
                message="Failed to create track",
                error=result.get("error"),
                reascript_calls=bridge.stop_tracking()
            )
        
        # Set name if provided
        if name:
            await bridge.call_lua("SetTrackName", [position, name])
        
        # Store role in track notes if provided
        if role:
            await bridge.call_lua("SetTrackNotes", [position, f"role:{role}"])
        
        # Get tracked calls
        reascript_calls = bridge.stop_tracking()
        
        return OperationResult(
            success=True,
            action="track_create",
            message=f"Created track '{name or f'Track {position + 1}'}'" + 
                   (f" with role '{role}'" if role else ""),
            targets=[{"index": position, "name": name or f"Track {position + 1}"}],
            changes={"position": position, "name": name, "role": role},
            reascript_calls=reascript_calls
        )
        
    except Exception as e:
        return OperationResult(
            success=False,
            action="track_create",
            message="Failed to create track",
            error=str(e),
            reascript_calls=bridge.stop_tracking()
        )

async def track_set_volume(bridge, track_sel: TrackSelector, 
                          volume: VolumeValue) -> OperationResult:
    """Set track volume (accepts dB, linear, or relative changes)"""
    # Start tracking ReaScript calls
    bridge.start_tracking()
    
    try:
        track = await resolve_track(bridge, track_sel)
        
        # Get current volume
        result = await bridge.call_lua("GetTrackVolume", [track.index])
        if not result.get("ok"):
            raise Exception("Failed to get current volume")
        
        current_linear = result.get("ret", 1.0)
        current_db = linear_to_db(current_linear)
        
        # Parse volume value
        new_linear = parse_volume_value(volume, current_linear)
        new_db = linear_to_db(new_linear)
        
        # Set new volume
        result = await bridge.call_lua("SetTrackVolume", [track.index, new_linear])
        if not result.get("ok"):
            raise Exception("Failed to set volume")
        
        # Get tracked calls
        reascript_calls = bridge.stop_tracking()
        
        return OperationResult(
            success=True,
            action="track_set_volume",
            message=f"Set {track.name} volume to {new_db:.1f} dB",
            targets=[track.to_dict()],
            changes={
                "old_volume_db": current_db,
                "new_volume_db": new_db,
                "old_volume_linear": current_linear,
                "new_volume_linear": new_linear
            },
            reascript_calls=reascript_calls
        )
        
    except DisambiguationNeeded as e:
        return OperationResult(
            success=False,
            action="track_set_volume",
            message="Multiple tracks found",
            disambiguation_needed={
                "type": "track",
                "candidates": [t.to_dict() for t in e.candidates]
            },
            reascript_calls=bridge.stop_tracking()
        )
    except Exception as e:
        return OperationResult(
            success=False,
            action="track_set_volume",
            message=f"Failed to set track volume",
            error=str(e),
            reascript_calls=bridge.stop_tracking()
        )

async def track_set_pan(bridge, track_sel: TrackSelector, 
                       pan: PanValue) -> OperationResult:
    """Set track pan (-1.0 to 1.0, or L50/R50 format)"""
    try:
        track = await resolve_track(bridge, track_sel)
        
        # Get current pan
        result = await bridge.call_lua("GetTrackPan", [track.index])
        if not result.get("ok"):
            raise Exception("Failed to get current pan")
        
        current_pan = result.get("ret", 0.0)
        
        # Parse pan value
        new_pan = parse_pan_value(pan, current_pan)
        
        # Set new pan
        result = await bridge.call_lua("SetTrackPan", [track.index, new_pan])
        if not result.get("ok"):
            raise Exception("Failed to set pan")
        
        return OperationResult(
            success=True,
            action="track_set_pan",
            message=f"Set {track.name} pan to {format_pan(new_pan)}",
            targets=[track.to_dict()],
            changes={
                "old_pan": current_pan,
                "new_pan": new_pan,
                "old_pan_formatted": format_pan(current_pan),
                "new_pan_formatted": format_pan(new_pan)
            }
        )
        
    except DisambiguationNeeded as e:
        return OperationResult(
            success=False,
            action="track_set_pan",
            message="Multiple tracks found",
            disambiguation_needed={
                "type": "track",
                "candidates": [t.to_dict() for t in e.candidates]
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            action="track_set_pan",
            message=f"Failed to set track pan",
            error=str(e)
        )

async def track_mute(bridge, track_sel: TrackSelector, 
                    mute: bool = True) -> OperationResult:
    """Mute or unmute a track"""
    try:
        track = await resolve_track(bridge, track_sel)
        
        result = await bridge.call_lua("SetTrackMute", [track.index, mute])
        if not result.get("ok"):
            raise Exception("Failed to set mute state")
        
        return OperationResult(
            success=True,
            action="track_mute",
            message=f"{'Muted' if mute else 'Unmuted'} {track.name}",
            targets=[track.to_dict()],
            changes={"muted": mute}
        )
        
    except DisambiguationNeeded as e:
        return OperationResult(
            success=False,
            action="track_mute",
            message="Multiple tracks found",
            disambiguation_needed={
                "type": "track",
                "candidates": [t.to_dict() for t in e.candidates]
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            action="track_mute",
            message=f"Failed to {'mute' if mute else 'unmute'} track",
            error=str(e)
        )

async def track_solo(bridge, track_sel: TrackSelector, 
                    solo: bool = True) -> OperationResult:
    """Solo or unsolo a track"""
    try:
        track = await resolve_track(bridge, track_sel)
        
        result = await bridge.call_lua("SetTrackSolo", [track.index, solo])
        if not result.get("ok"):
            raise Exception("Failed to set solo state")
        
        return OperationResult(
            success=True,
            action="track_solo",
            message=f"{'Soloed' if solo else 'Unsoloed'} {track.name}",
            targets=[track.to_dict()],
            changes={"soloed": solo}
        )
        
    except DisambiguationNeeded as e:
        return OperationResult(
            success=False,
            action="track_solo",
            message="Multiple tracks found",
            disambiguation_needed={
                "type": "track",
                "candidates": [t.to_dict() for t in e.candidates]
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            action="track_solo",
            message=f"Failed to {'solo' if solo else 'unsolo'} track",
            error=str(e)
        )

# Time/Loop Operations

async def time_select(bridge, time_sel: TimeSelector) -> OperationResult:
    """Set time selection"""
    try:
        time_ref = await resolve_time(bridge, time_sel)
        
        result = await bridge.call_lua("SetTimeSelection", [time_ref.start, time_ref.end])
        if not result.get("ok"):
            raise Exception("Failed to set time selection")
        
        # Update context
        get_context().update_time(time_ref)
        
        duration = time_ref.end - time_ref.start
        return OperationResult(
            success=True,
            action="time_select",
            message=f"Selected {duration:.2f} seconds" + 
                   (f" ({time_ref.bars} bars)" if time_ref.bars else ""),
            targets=[time_ref.to_dict()],
            changes={
                "start": time_ref.start,
                "end": time_ref.end,
                "duration": duration
            }
        )
        
    except Exception as e:
        return OperationResult(
            success=False,
            action="time_select",
            message="Failed to set time selection",
            error=str(e)
        )

async def loop_create(bridge, track_sel: TrackSelector, 
                     time_sel: TimeSelector,
                     midi: bool = True) -> OperationResult:
    """Create a loop item on a track"""
    try:
        track = await resolve_track(bridge, track_sel)
        time_ref = await resolve_time(bridge, time_sel)
        
        # Create item
        if midi:
            result = await bridge.call_lua("CreateMIDIItem", 
                                         [track.index, time_ref.start, time_ref.end])
        else:
            result = await bridge.call_lua("CreateAudioItem", 
                                         [track.index, time_ref.start, time_ref.end])
        
        if not result.get("ok"):
            raise Exception(f"Failed to create {'MIDI' if midi else 'audio'} item")
        
        item_index = result.get("item_index", 0)
        
        # Set loop source
        result = await bridge.call_lua("SetItemLoopSource", [track.index, item_index, True])
        
        duration = time_ref.end - time_ref.start
        return OperationResult(
            success=True,
            action="loop_create",
            message=f"Created {duration:.1f}s {'MIDI' if midi else 'audio'} loop on {track.name}" +
                   (f" ({time_ref.bars} bars)" if time_ref.bars else ""),
            targets=[track.to_dict()],
            changes={
                "track": track.name,
                "start": time_ref.start,
                "end": time_ref.end,
                "duration": duration,
                "item_type": "MIDI" if midi else "audio",
                "item_index": item_index
            }
        )
        
    except DisambiguationNeeded as e:
        return OperationResult(
            success=False,
            action="loop_create",
            message="Multiple tracks found",
            disambiguation_needed={
                "type": "track",
                "candidates": [t.to_dict() for t in e.candidates]
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            action="loop_create",
            message="Failed to create loop",
            error=str(e)
        )

# Item Operations

async def item_insert_midi(bridge, track_sel: TrackSelector,
                          time_sel: TimeSelector,
                          midi_data: Dict[str, Any]) -> OperationResult:
    """Insert MIDI data from external source"""
    try:
        track = await resolve_track(bridge, track_sel)
        time_ref = await resolve_time(bridge, time_sel)
        
        # Create MIDI item
        result = await bridge.call_lua("CreateMIDIItem", 
                                     [track.index, time_ref.start, time_ref.end])
        if not result.get("ok"):
            raise Exception("Failed to create MIDI item")
        
        item_index = result.get("item_index", 0)
        
        # Insert MIDI notes
        notes = midi_data.get("notes", [])
        for note in notes:
            await bridge.call_lua("InsertMIDINote", [
                track.index, 
                item_index, 
                note.get("pitch", 60),
                note.get("start", 0.0),
                note.get("length", 1.0),
                note.get("velocity", 100),
                note.get("channel", 0)
            ])
        
        return OperationResult(
            success=True,
            action="item_insert_midi",
            message=f"Inserted {len(notes)} MIDI notes on {track.name}",
            targets=[track.to_dict()],
            changes={
                "track": track.name,
                "start": time_ref.start,
                "end": time_ref.end,
                "notes_count": len(notes),
                "item_index": item_index
            }
        )
        
    except DisambiguationNeeded as e:
        return OperationResult(
            success=False,
            action="item_insert_midi",
            message="Multiple tracks found",
            disambiguation_needed={
                "type": "track",
                "candidates": [t.to_dict() for t in e.candidates]
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            action="item_insert_midi",
            message="Failed to insert MIDI data",
            error=str(e)
        )

async def item_quantize(bridge, item_sel: ItemSelector,
                       strength: float = 1.0,
                       grid: str = "1/16") -> OperationResult:
    """Quantize MIDI notes in items"""
    try:
        items = await resolve_items(bridge, item_sel)
        if not items:
            raise Exception("No items found")
        
        quantized_count = 0
        for item in items:
            if item.is_midi:
                result = await bridge.call_lua("QuantizeItem", [
                    item.track_index,
                    item.index,
                    strength,
                    grid
                ])
                if result.get("ok"):
                    quantized_count += 1
        
        return OperationResult(
            success=True,
            action="item_quantize",
            message=f"Quantized {quantized_count} MIDI items to {grid} grid " +
                   f"({int(strength * 100)}% strength)",
            targets=[i.to_dict() for i in items],
            changes={
                "items_processed": quantized_count,
                "strength": strength,
                "grid": grid
            }
        )
        
    except Exception as e:
        return OperationResult(
            success=False,
            action="item_quantize",
            message="Failed to quantize items",
            error=str(e)
        )

# Transport Operations

async def transport_play(bridge) -> OperationResult:
    """Start playback"""
    try:
        # Note: The DSL Play function needs to be added to the Lua bridge
        # For now, return a helpful error message
        result = await bridge.call_lua("Play", [])
        if not result.get("ok"):
            # Check if it's because the function doesn't exist
            if "Unknown function" in result.get("error", ""):
                return OperationResult(
                    success=False,
                    action="transport_play",
                    message="Play function not available in bridge",
                    error="DSL Lua functions need to be installed. See DSL_INSTALLATION.md"
                )
            raise Exception("Failed to start playback")
        
        return OperationResult(
            success=True,
            action="transport_play",
            message="Started playback"
        )
        
    except Exception as e:
        return OperationResult(
            success=False,
            action="transport_play",
            message="Failed to start playback",
            error=str(e)
        )

async def transport_stop(bridge) -> OperationResult:
    """Stop playback"""
    try:
        # Note: The DSL Stop function needs to be added to the Lua bridge
        # For now, return a helpful error message
        result = await bridge.call_lua("Stop", [])
        if not result.get("ok"):
            # Check if it's because the function doesn't exist
            if "Unknown function" in result.get("error", ""):
                return OperationResult(
                    success=False,
                    action="transport_stop",
                    message="Stop function not available in bridge",
                    error="DSL Lua functions need to be installed. See DSL_INSTALLATION.md"
                )
            raise Exception("Failed to stop playback")
        
        return OperationResult(
            success=True,
            action="transport_stop",
            message="Stopped playback"
        )
        
    except Exception as e:
        return OperationResult(
            success=False,
            action="transport_stop",
            message="Failed to stop playback",
            error=str(e)
        )

async def transport_set_tempo(bridge, bpm: float) -> OperationResult:
    """Set project tempo"""
    try:
        # Get current tempo
        result = await bridge.call_lua("GetTempo", [])
        old_tempo = result.get("ret", 120.0) if result.get("ok") else 120.0
        
        # Set new tempo
        result = await bridge.call_lua("SetTempo", [bpm])
        if not result.get("ok"):
            raise Exception("Failed to set tempo")
        
        return OperationResult(
            success=True,
            action="transport_set_tempo",
            message=f"Set tempo to {bpm} BPM",
            changes={
                "old_tempo": old_tempo,
                "new_tempo": bpm
            }
        )
        
    except Exception as e:
        return OperationResult(
            success=False,
            action="transport_set_tempo",
            message="Failed to set tempo",
            error=str(e)
        )

# Context Operations

async def context_get_tracks(bridge) -> OperationResult:
    """Get summary of all tracks in project"""
    try:
        result = await bridge.call_lua("GetAllTracksInfo", [])
        if not result.get("ok"):
            raise Exception("Failed to get tracks info")
        
        tracks = result.get("tracks", [])
        
        summary = []
        for t in tracks:
            summary.append({
                "index": t.get("index"),
                "name": t.get("name"),
                "role": t.get("role"),
                "has_midi": t.get("has_midi"),
                "has_audio": t.get("has_audio"),
                "fx_count": len(t.get("fx_names", [])),
                "muted": t.get("muted", False),
                "soloed": t.get("soloed", False)
            })
        
        # Build a detailed message with track names
        if not tracks:
            message = "No tracks found in project"
        else:
            track_lines = []
            for i, t in enumerate(summary):
                name = t.get("name", f"Track {i+1}")
                info_parts = []
                if t.get("has_midi"):
                    info_parts.append("MIDI")
                if t.get("has_audio"):
                    info_parts.append("Audio")
                if t.get("fx_count", 0) > 0:
                    info_parts.append(f"{t['fx_count']} FX")
                if t.get("muted"):
                    info_parts.append("Muted")
                if t.get("soloed"):
                    info_parts.append("Solo")
                
                info_str = f" ({', '.join(info_parts)})" if info_parts else ""
                track_lines.append(f"Track {i+1}: {name}{info_str}")
            
            message = f"Found {len(tracks)} tracks:\n" + "\n".join(track_lines)
        
        return OperationResult(
            success=True,
            action="context_get_tracks",
            message=message,
            targets=summary
        )
        
    except Exception as e:
        return OperationResult(
            success=False,
            action="context_get_tracks",
            message="Failed to get tracks info",
            error=str(e)
        )

async def context_get_tempo_info(bridge) -> OperationResult:
    """Get tempo and time signature info"""
    try:
        # Get tempo
        tempo_result = await bridge.call_lua("GetTempo", [])
        tempo = tempo_result.get("ret", 120.0) if tempo_result.get("ok") else 120.0
        
        # Get time signature
        ts_result = await bridge.call_lua("GetTimeSignature", [])
        numerator = ts_result.get("numerator", 4) if ts_result.get("ok") else 4
        denominator = ts_result.get("denominator", 4) if ts_result.get("ok") else 4
        
        return OperationResult(
            success=True,
            action="context_get_tempo_info",
            message=f"Tempo: {tempo} BPM, Time signature: {numerator}/{denominator}",
            changes={
                "tempo": tempo,
                "time_signature": f"{numerator}/{denominator}",
                "numerator": numerator,
                "denominator": denominator
            }
        )
        
    except Exception as e:
        return OperationResult(
            success=False,
            action="context_get_tempo_info",
            message="Failed to get tempo info",
            error=str(e)
        )

# Utility Functions

def linear_to_db(linear: float) -> float:
    """Convert linear volume to dB"""
    import math
    if linear <= 0:
        return -150.0
    return 20 * math.log10(linear)

def db_to_linear(db: float) -> float:
    """Convert dB to linear volume"""
    import math
    return math.pow(10, db / 20)

def parse_volume_value(value: VolumeValue, current: float) -> float:
    """Parse volume value (dB, linear, or relative)"""
    if isinstance(value, (int, float)):
        # Assume dB if > 1.0, linear otherwise
        if abs(value) > 1.0:
            return db_to_linear(value)
        return value
    
    if isinstance(value, str):
        value = value.lower().strip()
        
        # Check for dB notation
        if 'db' in value:
            db_val = float(value.replace('db', '').strip())
            return db_to_linear(db_val)
        
        # Check for relative change
        if value.startswith('+') or value.startswith('-'):
            db_change = float(value)
            current_db = linear_to_db(current)
            return db_to_linear(current_db + db_change)
        
        # Try to parse as number
        return float(value)
    
    if isinstance(value, dict):
        if 'db' in value:
            return db_to_linear(value['db'])
        if 'linear' in value:
            return value['linear']
        if 'relative_db' in value:
            current_db = linear_to_db(current)
            return db_to_linear(current_db + value['relative_db'])
    
    return current

def parse_pan_value(value: PanValue, current: float) -> float:
    """Parse pan value (L50/R50 format or -1 to 1)"""
    if isinstance(value, (int, float)):
        return max(-1.0, min(1.0, value))
    
    if isinstance(value, str):
        value = value.upper().strip()
        
        # L50/R50 format
        if value.startswith('L'):
            percent = float(value[1:]) / 100
            return -percent
        elif value.startswith('R'):
            percent = float(value[1:]) / 100
            return percent
        elif value == 'C' or value == 'CENTER':
            return 0.0
        
        # Try as number
        return max(-1.0, min(1.0, float(value)))
    
    if isinstance(value, dict):
        if 'value' in value:
            return max(-1.0, min(1.0, value['value']))
        if 'relative' in value:
            return max(-1.0, min(1.0, current + value['relative']))
    
    return current

def format_pan(pan: float) -> str:
    """Format pan value for display"""
    if abs(pan) < 0.01:
        return "C"
    elif pan < 0:
        return f"L{int(abs(pan) * 100)}"
    else:
        return f"R{int(pan * 100)}"