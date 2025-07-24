"""
DSL/Macro tools for natural language REAPER control

This module exposes the high-level DSL wrappers as MCP tools.
These tools accept flexible natural language inputs and handle
disambiguation when needed.
"""

from typing import Optional, Union, Dict, Any, List
from ..bridge import bridge
from .wrappers import (
    track_create, track_set_volume, track_set_pan, track_mute, track_solo,
    time_select, loop_create,
    item_insert_midi, item_quantize,
    transport_play, transport_stop, transport_set_tempo,
    context_get_tracks, context_get_tempo_info,
    OperationResult
)
from .resolvers import reset_context

def register_dsl_tools(mcp):
    """Register DSL/Macro tools for natural language control"""
    
    # Track Management Tools
    
    @mcp.tool()
    async def dsl_track_create(
        name: Optional[str] = None,
        role: Optional[str] = None,
        position: Optional[int] = None
    ) -> str:
        """
        Add a new instrument, voice, or sound to your project. Use when users want to add bass, drums, vocals, guitar, synth, or any new element.
        
        Args:
            name: Track name (e.g., "Bass", "Lead Synth")
            role: Track role/type (e.g., "bass", "drums", "keys", "vocals")
            position: Insert position (default: end of track list)
            
        Examples:
            - "I need something for the low end"
            - "add drums"
            - "make a place for my voice"
            - "I want to record my guitar"
        """
        result = await track_create(bridge, name, role, position)
        return result.to_string()
    
    @mcp.tool()
    async def dsl_track_volume(
        track: Union[str, int, Dict[str, Any]],
        volume: Union[float, str, Dict[str, Any]]
    ) -> str:
        """
        Make sounds louder or quieter. Use for 'turn up', 'turn down', 'too loud', 'can't hear', 'boost', 'cut', or any volume-related request.
        
        Args:
            track: Track reference - can be:
                - Index: 0, 1, 2...
                - Name: "Bass", "Drums" (fuzzy matched)
                - Role: "bass", "drums", "keys"
                - Dict: {"name": "Bass"}, {"role": "drums"}, {"has_fx": "Serum"}
                - Special: "last" (last referenced track)
            volume: Volume value - can be:
                - dB: -6, "-6dB", {"db": -6}
                - Linear: 0.5, {"linear": 0.5}
                - Relative: "+3", "-3dB", {"relative_db": -3}
                
        Examples:
            - "turn it down"
            - "too loud"
            - "I can't hear the vocals"
            - "bring up the drums"
        """
        result = await track_set_volume(bridge, track, volume)
        return result.to_string()
    
    @mcp.tool()
    async def dsl_track_pan(
        track: Union[str, int, Dict[str, Any]],
        pan: Union[float, str, Dict[str, Any]]
    ) -> str:
        """
        Move sounds left, right, or center in the stereo field. Use for spatial positioning, spreading sounds out, or creating stereo width.
        
        Args:
            track: Track reference (same as dsl_track_volume)
            pan: Pan value - can be:
                - Numeric: -1.0 to 1.0 (-1=left, 0=center, 1=right)
                - L/R format: "L50", "R30", "C" (center)
                - Dict: {"value": 0.5}, {"relative": -0.2}
                
        Examples:
            - "move it to the left"
            - "put that on the right"
            - "spread them out"
            - "everything sounds in the middle"
        """
        result = await track_set_pan(bridge, track, pan)
        return result.to_string()
    
    @mcp.tool()
    async def dsl_track_mute(
        track: Union[str, int, Dict[str, Any]],
        mute: bool = True
    ) -> str:
        """
        Turn tracks on or off temporarily. Use when users want to silence, disable, or bring back specific sounds.
        
        Args:
            track: Track reference (same as dsl_track_volume)
            mute: True to mute, False to unmute
            
        Examples:
            - "turn that off"
            - "I don't want to hear that"
            - "kill the bass"
            - "bring it back"
        """
        result = await track_mute(bridge, track, mute)
        return result.to_string()
    
    @mcp.tool()
    async def dsl_track_solo(
        track: Union[str, int, Dict[str, Any]],
        solo: bool = True
    ) -> str:
        """
        Isolate one or more tracks to hear them alone. Use for 'just the drums', 'only the bass', or focusing on specific elements.
        
        Args:
            track: Track reference (same as dsl_track_volume)
            solo: True to solo, False to unsolo
            
        Examples:
            - "just the drums"
            - "only the bass"
            - "let me hear that by itself"
            - "isolate the vocals"
        """
        result = await track_solo(bridge, track, solo)
        return result.to_string()
    
    # Time and Loop Tools
    
    @mcp.tool()
    async def dsl_time_select(
        time: Union[str, float, Dict[str, Any]]
    ) -> str:
        """
        Highlight a section of your song. Use for selecting verses, choruses, bars, or any time region for editing.
        
        Args:
            time: Time range - can be:
                - Bars: "8 bars", "4 bars"
                - Seconds: 10.5 (duration from cursor)
                - Special: "selection", "loop", "cursor"
                - Dict: {"bars": 8, "from": "cursor"}, {"start": 0, "end": 10}
                - Region/Marker: {"region": "Chorus"}, {"marker": "Verse 2"}
                
        Examples:
            - "select this part"
            - "grab the chorus"
            - "from here to here"
            - "the next bit"
        """
        result = await time_select(bridge, time)
        return result.to_string()
    
    @mcp.tool()
    async def dsl_loop_create(
        track: Union[str, int, Dict[str, Any]],
        time: Union[str, float, Dict[str, Any]],
        midi: bool = True
    ) -> str:
        """
        Make a repeating section. Use when users want patterns, loops, or repeated musical phrases.
        
        Args:
            track: Track reference (same as dsl_track_volume)
            time: Time range for the loop (same as dsl_time_select)
            midi: True for MIDI item, False for audio item
            
        Examples:
            - "loop this"
            - "make it repeat"
            - "I want this to go on"
            - "repeat that section"
        """
        result = await loop_create(bridge, track, time, midi)
        return result.to_string()
    
    # Item and MIDI Tools
    
    @mcp.tool()
    async def dsl_midi_insert(
        track: Union[str, int, Dict[str, Any]],
        time: Union[str, float, Dict[str, Any]],
        midi_data: Dict[str, Any]
    ) -> str:
        """
        Add musical notes, melodies, or rhythms. Use for 'add notes', 'create melody', 'put down a beat'.
        
        Args:
            track: Track reference (same as dsl_track_volume)
            time: Time range for the MIDI item
            midi_data: MIDI data with notes array:
                {
                    "notes": [
                        {"pitch": 60, "start": 0.0, "length": 0.5, "velocity": 100},
                        {"pitch": 64, "start": 0.5, "length": 0.5, "velocity": 90}
                    ]
                }
                
        The MIDI data format matches common MIDI generation APIs.
        """
        result = await item_insert_midi(bridge, track, time, midi_data)
        return result.to_string()
    
    @mcp.tool()
    async def dsl_quantize(
        items: Union[str, Dict[str, Any]] = "selected",
        strength: float = 1.0,
        grid: str = "1/16"
    ) -> str:
        """
        Fix timing and rhythm issues. Use for 'tighten up', 'on beat', 'fix timing', 'clean up rhythm', or making things more precise.
        
        Args:
            items: Item selection - can be:
                - "selected": Currently selected items
                - "all": All items in project
                - "last": Last referenced items
                - Dict: {"track": "drums", "time": "8 bars"}
            strength: Quantization strength (0.0 to 1.0, default 1.0 = 100%)
            grid: Grid resolution ("1/4", "1/8", "1/16", "1/32", etc.)
            
        Examples:
            - "fix the timing"
            - "it's off beat"
            - "tighten it up"
            - "make it on time"
        """
        result = await item_quantize(bridge, items, strength, grid)
        return result.to_string()
    
    # Transport Tools
    
    @mcp.tool()
    async def dsl_play() -> str:
        """
        Start playing your music. Use for any variation of play, start, go, listen, or hear.
        
        Examples:
            - "play it"
            - "let's hear it"
            - "go"
            - "start"
        """
        result = await transport_play(bridge)
        return result.to_string()
    
    @mcp.tool()
    async def dsl_stop() -> str:
        """
        Stop the music. Use for stop, pause, halt, wait, or cease playback.
        
        Examples:
            - "stop"
            - "hold on"
            - "wait"
            - "pause"
        """
        result = await transport_stop(bridge)
        return result.to_string()
    
    @mcp.tool()
    async def dsl_set_tempo(bpm: float) -> str:
        """
        Change the speed of your song. Use for faster, slower, BPM changes, or energy adjustments.
        
        Args:
            bpm: Tempo in beats per minute (20.0 to 960.0)
            
        Examples:
            - "make it faster"
            - "slow it down"
            - "too slow"
            - "too fast"
        """
        result = await transport_set_tempo(bridge, bpm)
        return result.to_string()
    
    # Context and Query Tools
    
    @mcp.tool()
    async def dsl_list_tracks() -> str:
        """
        Show what's in your project. Use when users ask what tracks exist or want an overview.
        
        Examples:
            - "what do I have?"
            - "show me everything"
            - "list what's here"
            - "what tracks?"
        """
        result = await context_get_tracks(bridge)
        return result.to_string()
    
    @mcp.tool()
    async def dsl_get_tempo_info() -> str:
        """
        Check current speed and time signature. Use when users ask about tempo, BPM, or timing.
        
        Examples:
            - "how fast is this?"
            - "what's the speed?"
            - "tempo?"
            - "BPM?"
        """
        result = await context_get_tempo_info(bridge)
        return result.to_string()
    
    @mcp.tool()
    async def dsl_reset_context() -> str:
        """
        Start fresh with a clean slate. Use when users want to begin again or clear previous references.
        
        Use this if the context gets confused or to start fresh.
        """
        reset_context()
        return "Session context reset"
    
    # Count registered tools
    tool_count = 15
    
    return tool_count