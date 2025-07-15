"""
Advanced MIDI Analysis and Generation Tools for REAPER MCP

This module contains advanced MIDI tools for analysis, transformation,
and generation - particularly useful for AI agents creating musical content.
"""

from typing import List, Dict, Any, Optional, Tuple
from ..bridge import bridge


# ============================================================================
# MIDI Pattern Analysis
# ============================================================================

async def analyze_midi_pattern(item_index: int, take_index: int) -> str:
    """Analyze patterns in MIDI data (rhythm, melody, harmony)"""
    # Use the combined bridge function
    result = await bridge.call_lua("AnalyzeMIDIPattern", [item_index, take_index])
    
    if result.get("ok"):
        analysis = result.get("analysis")
        if analysis:
            return analysis
        else:
            notes_analyzed = result.get("notes_analyzed", 0)
            pitch_range = result.get("pitch_range", 0)
            pattern_type = result.get("pattern_type", "unknown")
            avg_velocity = result.get("avg_velocity", 0)
            
            return (f"MIDI pattern analysis:\n"
                    f"  Notes analyzed: {notes_analyzed}\n"
                    f"  Pitch range: {pitch_range} semitones\n"
                    f"  Pattern type: {pattern_type}\n"
                    f"  Average velocity: {avg_velocity:.0f}")
    else:
        raise Exception(f"Failed to analyze MIDI pattern: {result.get('error', 'Unknown error')}")


async def detect_midi_chord_progressions(item_index: int, take_index: int) -> str:
    """Detect chord progressions in MIDI data"""
    # Use the combined bridge function
    result = await bridge.call_lua("DetectMIDIChordProgressions", [item_index, take_index])
    
    if result.get("ok"):
        progression = result.get("progression")
        if progression:
            return progression
        else:
            chords_detected = result.get("chords_detected", 0)
            notes_analyzed = result.get("notes_analyzed", 0)
            chord_list = result.get("chord_list", [])
            
            if chord_list:
                return f"Detected chord progression:\n" + " → ".join(chord_list[:8])
            else:
                return f"Analyzed {notes_analyzed} notes, found {chords_detected} chords but no clear progression"
    else:
        raise Exception(f"Failed to detect chord progressions: {result.get('error', 'Unknown error')}")


async def analyze_midi_rhythm_pattern(item_index: int, take_index: int) -> str:
    """Analyze rhythmic patterns in MIDI"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take {take_index} from item {item_index}")
    
    take = take_result.get("ret")
    
    # Get tempo for PPQ conversion
    tempo_result = await bridge.call_lua("Master_GetTempo", [])
    tempo = tempo_result.get("ret", 120) if tempo_result.get("ok") else 120
    
    # Get notes
    count_result = await bridge.call_lua("MIDI_CountEvts", [take])
    if not count_result.get("ok"):
        return "Failed to count MIDI events"
    
    notes = count_result.get("notes", 0)
    
    # Collect note timings
    note_times = []
    for i in range(min(notes, 100)):  # Analyze up to 100 notes
        note_result = await bridge.call_lua("MIDI_GetNote", [take, i])
        if note_result.get("ok"):
            start_ppq = note_result.get("startppqpos", 0)
            note_times.append(start_ppq)
    
    if len(note_times) < 2:
        return "Not enough notes for rhythm analysis"
    
    # Calculate intervals
    intervals = []
    for i in range(1, len(note_times)):
        intervals.append(note_times[i] - note_times[i-1])
    
    # Find common intervals (rhythm pattern)
    ppq_per_quarter = 960  # Standard MIDI PPQ
    
    # Categorize intervals
    rhythm_types = {
        "16th": 0,
        "8th": 0,
        "quarter": 0,
        "half": 0,
        "whole": 0
    }
    
    for interval in intervals:
        if interval < ppq_per_quarter * 0.3:
            rhythm_types["16th"] += 1
        elif interval < ppq_per_quarter * 0.6:
            rhythm_types["8th"] += 1
        elif interval < ppq_per_quarter * 1.5:
            rhythm_types["quarter"] += 1
        elif interval < ppq_per_quarter * 3:
            rhythm_types["half"] += 1
        else:
            rhythm_types["whole"] += 1
    
    # Find dominant rhythm
    dominant = max(rhythm_types.items(), key=lambda x: x[1])
    
    return (f"Rhythm pattern analysis:\n"
            f"  Notes analyzed: {len(note_times)}\n"
            f"  Dominant rhythm: {dominant[0]} notes\n"
            f"  16th notes: {rhythm_types['16th']}\n"
            f"  8th notes: {rhythm_types['8th']}\n"
            f"  Quarter notes: {rhythm_types['quarter']}")


# ============================================================================
# MIDI Generation Helpers
# ============================================================================

async def generate_midi_scale(item_index: int, take_index: int, 
                            root_note: int, scale_type: str, 
                            octaves: int = 1, note_length: float = 0.25) -> str:
    """Generate a musical scale in MIDI"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take {take_index} from item {item_index}")
    
    take = take_result.get("ret")
    
    # Define scale intervals
    scales = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
        "pentatonic": [0, 2, 4, 7, 9],
        "blues": [0, 3, 5, 6, 7, 10],
        "chromatic": list(range(12))
    }
    
    if scale_type not in scales:
        return f"Unknown scale type. Available: {', '.join(scales.keys())}"
    
    intervals = scales[scale_type]
    
    # Generate notes
    ppq_per_quarter = 960
    current_pos = 0
    notes_added = 0
    
    for octave in range(octaves):
        for interval in intervals:
            pitch = root_note + interval + (octave * 12)
            if pitch > 127:  # MIDI pitch limit
                break
            
            # Insert note
            result = await bridge.call_lua("MIDI_InsertNote", [
                take,
                False,  # selected
                False,  # muted
                current_pos,  # startppqpos
                current_pos + (note_length * ppq_per_quarter),  # endppqpos
                0,  # channel
                pitch,
                80,  # velocity
                False  # noSort
            ])
            
            if result.get("ok"):
                notes_added += 1
            
            current_pos += note_length * ppq_per_quarter
    
    # Sort notes
    await bridge.call_lua("MIDI_Sort", [take])
    
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    root_name = note_names[root_note % 12]
    
    return f"Generated {scale_type} scale: {notes_added} notes starting from {root_name}{root_note // 12 - 1}"


async def generate_midi_chord_sequence(item_index: int, take_index: int,
                                     chord_progression: List[str],
                                     duration: float = 1.0) -> str:
    """Generate a chord progression in MIDI"""
    # Use the combined bridge function
    result = await bridge.call_lua("GenerateMIDIChordSequence", [item_index, take_index, chord_progression, duration])
    
    if result.get("ok"):
        chords_added = result.get("chords_added", 0)
        progression = result.get("progression", " → ".join(chord_progression))
        return f"Generated chord progression: {progression} ({chords_added} chords)"
    else:
        raise Exception(f"Failed to generate chord sequence: {result.get('error', 'Unknown error')}")


async def generate_midi_drum_pattern(item_index: int, take_index: int,
                                   pattern: str, bars: int = 4) -> str:
    """Generate a drum pattern in MIDI"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take {take_index} from item {item_index}")
    
    take = take_result.get("ret")
    
    # GM drum map
    drums = {
        "kick": 36,
        "snare": 38,
        "hihat": 42,
        "open_hihat": 46,
        "crash": 49,
        "ride": 51,
        "tom1": 48,
        "tom2": 45,
        "tom3": 43
    }
    
    # Pattern definitions
    patterns = {
        "basic_rock": {
            "kick": [0, 2],
            "snare": [1, 3],
            "hihat": [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
        },
        "basic_funk": {
            "kick": [0, 0.75, 2, 2.25],
            "snare": [1, 3],
            "hihat": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75]
        },
        "basic_jazz": {
            "ride": [0, 1, 2, 3],
            "kick": [0],
            "hihat": [2]
        }
    }
    
    if pattern not in patterns:
        return f"Unknown pattern. Available: {', '.join(patterns.keys())}"
    
    selected_pattern = patterns[pattern]
    ppq_per_quarter = 960
    notes_added = 0
    
    # Generate pattern for specified bars
    for bar in range(bars):
        bar_offset = bar * 4 * ppq_per_quarter  # 4 quarters per bar
        
        for drum, positions in selected_pattern.items():
            if drum in drums:
                pitch = drums[drum]
                
                for pos in positions:
                    ppq_pos = int(bar_offset + pos * ppq_per_quarter)
                    
                    result = await bridge.call_lua("MIDI_InsertNote", [
                        take,
                        False,  # selected
                        False,  # muted
                        ppq_pos,  # startppqpos
                        ppq_pos + 100,  # endppqpos (short for drums)
                        9,  # channel 10 for drums
                        pitch,
                        100,  # velocity
                        False  # noSort
                    ])
                    
                    if result.get("ok"):
                        notes_added += 1
    
    # Sort notes
    await bridge.call_lua("MIDI_Sort", [take])
    
    return f"Generated {pattern} drum pattern: {notes_added} notes over {bars} bars"


# ============================================================================
# MIDI Transformation
# ============================================================================

async def transpose_midi_notes(item_index: int, take_index: int, 
                             semitones: int, selected_only: bool = False) -> str:
    """Transpose MIDI notes by semitones"""
    # Use the combined bridge function
    result = await bridge.call_lua("TransposeMIDINotes", [item_index, take_index, semitones, selected_only])
    
    if result.get("ok"):
        transposed = result.get("transposed", 0)
        notes = result.get("notes", 0)
        direction = "up" if semitones > 0 else "down"
        return f"Transposed {transposed} notes {abs(semitones)} semitones {direction}"
    else:
        raise Exception(f"Failed to transpose MIDI notes: {result.get('error', 'Unknown error')}")


async def quantize_midi_notes(item_index: int, take_index: int, 
                            grid: str = "1/16", strength: float = 1.0) -> str:
    """Quantize MIDI notes to grid"""
    # Grid values in PPQ
    ppq_per_quarter = 960
    grids = {
        "1/32": ppq_per_quarter / 8,
        "1/16": ppq_per_quarter / 4,
        "1/8": ppq_per_quarter / 2,
        "1/4": ppq_per_quarter,
        "1/2": ppq_per_quarter * 2,
        "1": ppq_per_quarter * 4
    }
    
    if grid not in grids:
        return f"Unknown grid. Available: {', '.join(grids.keys())}"
    
    grid_size = grids[grid]
    
    # Use the combined bridge function
    result = await bridge.call_lua("QuantizeMIDINotes", [item_index, take_index, grid_size, strength])
    
    if result.get("ok"):
        quantized = result.get("quantized", 0)
        return f"Quantized {quantized} notes to {grid} grid at {strength*100:.0f}% strength"
    else:
        raise Exception(f"Failed to quantize MIDI notes: {result.get('error', 'Unknown error')}")


async def humanize_midi_timing(item_index: int, take_index: int,
                             timing_amount: float = 0.05,
                             velocity_amount: float = 0.1) -> str:
    """Add human timing and velocity variations to MIDI"""
    # Use the combined bridge function
    result = await bridge.call_lua("HumanizeMIDITiming", [item_index, take_index, timing_amount, velocity_amount])
    
    if result.get("ok"):
        humanized = result.get("humanized", 0)
        return f"Humanized {humanized} notes (timing: ±{timing_amount*1000:.0f}ms, velocity: ±{velocity_amount*100:.0f}%)"
    else:
        raise Exception(f"Failed to humanize MIDI: {result.get('error', 'Unknown error')}")


# ============================================================================
# MIDI Analysis Utilities
# ============================================================================

async def get_midi_note_distribution(item_index: int, take_index: int) -> str:
    """Get distribution of notes across pitch range"""
    # Use the combined bridge function
    result = await bridge.call_lua("GetMIDINoteDistribution", [item_index, take_index])
    
    if result.get("ok"):
        notes_total = result.get("notes_total", 0)
        distribution = result.get("distribution", [])
        avg_velocity = result.get("avg_velocity", 0)
        
        if not distribution:
            return "No notes found"
        
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        
        dist_lines = []
        for item in distribution[:10]:  # Top 10
            pitch = item.get("pitch", 60)
            count = item.get("count", 0)
            note_name = note_names[pitch % 12]
            octave = pitch // 12 - 1
            percentage = (count / notes_total) * 100 if notes_total > 0 else 0
            dist_lines.append(f"  {note_name}{octave}: {count} ({percentage:.1f}%)")
        
        return (f"MIDI note distribution ({notes_total} total notes):\n" + 
                "\n".join(dist_lines) + 
                f"\n  Average velocity: {avg_velocity:.0f}")
    else:
        raise Exception(f"Failed to get MIDI note distribution: {result.get('error', 'Unknown error')}")


async def detect_midi_key_signature(item_index: int, take_index: int) -> str:
    """Attempt to detect the key signature of MIDI content"""
    # Use the combined bridge function
    result = await bridge.call_lua("DetectMIDIKeySignature", [item_index, take_index])
    
    if result.get("ok"):
        key = result.get("key", "Unknown")
        confidence = result.get("confidence", 0)
        notes_analyzed = result.get("notes_analyzed", 0)
        
        if notes_analyzed == 0:
            return "No notes found to analyze"
        
        return f"Detected key: {key} (confidence: {confidence:.0f}%)"
    else:
        raise Exception(f"Failed to detect key signature: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_midi_advanced_tools(mcp) -> int:
    """Register all advanced MIDI tools with the MCP instance"""
    tools = [
        # MIDI Pattern Analysis
        (analyze_midi_pattern, "Analyze patterns in MIDI data"),
        (detect_midi_chord_progressions, "Detect chord progressions in MIDI"),
        (analyze_midi_rhythm_pattern, "Analyze rhythmic patterns in MIDI"),
        
        # MIDI Generation Helpers
        (generate_midi_scale, "Generate a musical scale in MIDI"),
        (generate_midi_chord_sequence, "Generate a chord progression in MIDI"),
        (generate_midi_drum_pattern, "Generate a drum pattern in MIDI"),
        
        # MIDI Transformation
        (transpose_midi_notes, "Transpose MIDI notes by semitones"),
        (quantize_midi_notes, "Quantize MIDI notes to grid"),
        (humanize_midi_timing, "Add human timing variations to MIDI"),
        
        # MIDI Analysis Utilities
        (get_midi_note_distribution, "Get distribution of notes across pitch range"),
        (detect_midi_key_signature, "Detect the key signature of MIDI content"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)