# DSL/Macros Layer for REAPER MCP

## Overview

The DSL (Domain Specific Language) layer provides a natural language friendly interface to REAPER operations. Instead of dealing with complex ReaScript functions and parameters, you can use intuitive commands that understand context and flexible inputs.

## Key Features

### 1. Natural Language Track References
- **By name**: `"Bass"`, `"Drums"`, `"Lead Synth"`
- **By role**: `"bass"`, `"drums"`, `"keys"`, `"vocals"`
- **By index**: `0`, `1`, `2` (0-based)
- **By content**: `{"has_fx": "Serum"}`, `{"has_midi": true}`
- **Contextual**: `"last"` (last referenced track)
- **Fuzzy matching**: `"bss"` matches `"Bass"`, `"drm"` matches `"Drums"`

### 2. Flexible Time References
- **Bars**: `"8 bars"`, `"4 bars"`
- **Seconds**: `10.5` (duration from cursor)
- **Special positions**: `"cursor"`, `"selection"`, `"loop"`
- **Complex**: `{"bars": 8, "from": "cursor"}`
- **Regions/Markers**: `{"region": "Chorus"}`, `{"marker": "Verse 2"}`

### 3. Intuitive Value Formats
- **Volume**: `-6dB`, `+3`, `0.5` (linear), `{"relative_db": -3}`
- **Pan**: `"L50"`, `"R30"`, `"C"` (center), `-0.5` to `0.5`

### 4. Context Awareness
- Remembers last referenced tracks, items, and time selections
- Use `"last"` to refer to previously used elements
- Reset context with `dsl_reset_context`

### 5. Smart Disambiguation
- When multiple matches are found, returns candidates
- Confidence scoring helps pick the best match
- Falls back to user choice when uncertain

## Available Tools (15 total)

### Track Management
- `dsl_track_create` - Create track with name and role
- `dsl_track_volume` - Set volume with flexible formats
- `dsl_track_pan` - Set pan with L/R or numeric format
- `dsl_track_mute` - Mute/unmute tracks
- `dsl_track_solo` - Solo/unsolo tracks

### Time and Loops
- `dsl_time_select` - Select time with natural language
- `dsl_loop_create` - Create loop items on tracks

### MIDI and Items
- `dsl_midi_insert` - Insert MIDI from external sources
- `dsl_quantize` - Quantize with strength and grid options

### Transport
- `dsl_play` - Start playback
- `dsl_stop` - Stop playback
- `dsl_set_tempo` - Set project tempo

### Context and Query
- `dsl_list_tracks` - Get all tracks with metadata
- `dsl_get_tempo_info` - Get tempo and time signature
- `dsl_reset_context` - Clear session context

## Usage Examples

### Create a Basic Track Structure
```python
# Create tracks with roles
await dsl_track_create(name="Drums", role="drums")
await dsl_track_create(name="Bass", role="bass")
await dsl_track_create(name="Keys", role="keys")

# Set tempo
await dsl_set_tempo(bpm=120)

# Create 8-bar loops
await dsl_loop_create(track="drums", time="8 bars")
await dsl_loop_create(track="bass", time="8 bars")
```

### Mix with Natural Language
```python
# Set volumes using dB
await dsl_track_volume(track="drums", volume="-3dB")
await dsl_track_volume(track="bass", volume="-6dB")

# Increase volume relatively
await dsl_track_volume(track="keys", volume="+2")

# Pan instruments
await dsl_track_pan(track="keys", pan="R20")
await dsl_track_pan(track="guitar", pan="L30")
```

### Work with Context
```python
# Reference a track
await dsl_track_volume(track="Lead Vocal", volume="-6dB")

# Use "last" to reference it again
await dsl_track_pan(track="last", pan="C")
await dsl_track_mute(track="last", mute=True)
```

### Insert External MIDI
```python
# From an AI music generator
midi_data = {
    "notes": [
        {"pitch": 60, "start": 0.0, "length": 0.5, "velocity": 100},
        {"pitch": 64, "start": 0.5, "length": 0.5, "velocity": 90}
    ]
}

await dsl_midi_insert(
    track="bass", 
    time="8 bars",
    midi_data=midi_data
)
```

## Benefits

1. **Reduced Complexity**: No need to remember ReaScript parameter orders or types
2. **Natural Workflow**: Commands match how musicians think
3. **Fewer Tools**: 15 focused tools vs 600+ low-level functions
4. **AI-Friendly**: Designed for LLMs with token limits
5. **Error Recovery**: Clear messages and disambiguation support

## Installation

See [DSL_INSTALLATION.md](DSL_INSTALLATION.md) for setup instructions.

## Future Enhancements

- Pattern matching for track groups ("all drums", "all bass")
- Batch operations on multiple tracks
- Preset system for common workflows
- Integration with more external MIDI sources
- Advanced time expressions ("next downbeat", "end of bar")