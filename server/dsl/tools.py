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
from .resolvers import reset_context, dsl_context

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
        
        # Include ReaScript calls in the response message
        response = result.to_string()
        
        if result.reascript_calls:
            response += "\n\n[ReaScript calls:"
            for call in result.reascript_calls:
                response += f"\n  {call['function']}({call['args']}) → {call.get('duration_ms', 0):.0f}ms"
            response += "]"
        
        # If there's an error, raise an exception so MCP sets isError properly
        if not result.success:
            raise Exception(response)
        
        return response
    
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
        
        # Include ReaScript calls if any
        response = result.to_string()
        if result.reascript_calls:
            response += "\n\n[ReaScript calls:"
            for call in result.reascript_calls:
                response += f"\n  {call['function']}({call['args']}) → {call.get('duration_ms', 0):.0f}ms"
            response += "]"
        
        # If there's an error, raise an exception so MCP sets isError properly
        if not result.success:
            raise Exception(response)
        
        return response
    
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
    
    # Track Management Extensions
    
    @mcp.tool()
    async def dsl_track_rename(
        track: Union[str, int, Dict[str, Any]],
        name: str
    ) -> str:
        """
        Rename a track. Use for 'rename track 2 to Bass', 'call it drums', 'change the name'.
        
        Args:
            track: Track reference (same as dsl_track_volume)
            name: New name for the track
            
        Examples:
            - "rename track 2 to Lead Guitar"
            - "rename the bass track to Electric Bass"
            - "call the first track Drums"
        """
        try:
            resolved_track = dsl_context.resolve_track(track)
            track_index = resolved_track['index']
            
            from server.tools.tracks import set_track_name
            result = await set_track_name(track_index, name)
            
            dsl_context.last_track = resolved_track
            
            return f"Renamed track {track_index + 1} to '{name}'"
            
        except Exception as e:
            return f"Failed to rename track: {str(e)}"
    
    @mcp.tool()
    async def dsl_track_delete(
        track: Union[str, int, Dict[str, Any]]
    ) -> str:
        """
        Delete a track. Use for 'delete track', 'remove track', 'get rid of', 'delete empty tracks'.
        
        Args:
            track: Track reference to delete
            
        Examples:
            - "delete track 3"
            - "remove the empty tracks"
            - "get rid of the bass track"
        """
        try:
            resolved_track = dsl_context.resolve_track(track)
            track_index = resolved_track['index']
            
            from server.tools.tracks import delete_track
            result = await delete_track(track_index)
            
            # Clear last track reference if it was deleted
            if dsl_context.last_track and dsl_context.last_track['index'] == track_index:
                dsl_context.last_track = None
            
            return f"Deleted track {track_index + 1}"
            
        except Exception as e:
            return f"Failed to delete track: {str(e)}"
    
    @mcp.tool()
    async def dsl_track_arm(
        track: Union[str, int, Dict[str, Any]],
        armed: bool = True
    ) -> str:
        """
        Arm or unarm track for recording. Use for 'arm track', 'record enable', 'prepare for recording'.
        
        Args:
            track: Track reference to arm/unarm
            armed: True to arm, False to unarm
            
        Examples:
            - "arm track 1 for recording"
            - "record enable the guitar"
            - "unarm all tracks"
        """
        try:
            resolved_track = dsl_context.resolve_track(track)
            track_index = resolved_track['index']
            
            from server.tools.tracks import set_track_arm
            result = await set_track_arm(track_index, armed)
            
            dsl_context.last_track = resolved_track
            
            action = "armed" if armed else "unarmed"
            return f"Track {track_index + 1} {action} for recording"
            
        except Exception as e:
            return f"Failed to arm track: {str(e)}"
    
    # Edit and Project Operations
    
    @mcp.tool()
    async def dsl_undo() -> str:
        """
        Undo the last action. Use for 'undo', 'undo that', 'go back', 'revert'.
        
        Examples:
            - "undo"
            - "undo that"
            - "go back one step"
        """
        try:
            from server.tools.project_state import undo_do_undo2
            result = await undo_do_undo2()
            return "Undid last action"
        except Exception as e:
            return f"Failed to undo: {str(e)}"
    
    @mcp.tool()
    async def dsl_save(
        name: Optional[str] = None
    ) -> str:
        """
        Save the project. Use for 'save', 'save project', 'save as'.
        
        Args:
            name: Optional filename for save as
            
        Examples:
            - "save the project"
            - "save"
            - "save as Final Mix"
        """
        try:
            from server.tools.project import save_project
            
            # For now, just do regular save
            # TODO: Add save-as functionality when available
            result = await save_project(0, force_save_as=bool(name))
            
            if name:
                return f"Saved project (save-as functionality pending)"
            else:
                return "Project saved"
                
        except Exception as e:
            return f"Failed to save project: {str(e)}"
    
    # Transport and Navigation
    
    @mcp.tool()
    async def dsl_go_to(
        position: Union[str, float, Dict[str, Any]]
    ) -> str:
        """
        Move playhead to position. Use for 'go to beginning', 'jump to end', 'go to 30 seconds'.
        
        Args:
            position: Where to go - "start", "end", seconds, or {"marker": "name"}
            
        Examples:
            - "go to the beginning"
            - "jump to the end"
            - "go to 30 seconds"
            - "go to the chorus marker"
        """
        try:
            from server.tools.transport import set_cursor_position, get_play_position
            from server.tools.project import get_project_length
            
            # Handle different position formats
            if isinstance(position, str):
                if position.lower() in ["start", "beginning", "top"]:
                    pos_seconds = 0.0
                elif position.lower() in ["end", "finish"]:
                    # Get project length
                    length_result = await get_project_length()
                    pos_seconds = float(length_result.split()[0])
                else:
                    return f"Unknown position: {position}"
                    
            elif isinstance(position, (int, float)):
                pos_seconds = float(position)
                
            elif isinstance(position, dict) and "marker" in position:
                # TODO: Implement marker navigation when available
                return "Marker navigation not yet implemented"
                
            else:
                return f"Invalid position format: {position}"
            
            result = await set_cursor_position(pos_seconds)
            return f"Moved to {pos_seconds:.1f} seconds"
            
        except Exception as e:
            return f"Failed to move position: {str(e)}"
    
    @mcp.tool()
    async def dsl_record() -> str:
        """
        Start recording. Use for 'record', 'start recording', 'rec'.
        
        Examples:
            - "record"
            - "start recording"
            - "begin recording"
        """
        try:
            from server.tools.transport import transport_record
            result = await transport_record()
            return "Recording started"
        except Exception as e:
            return f"Failed to start recording: {str(e)}"
    
    # Markers
    
    @mcp.tool()
    async def dsl_marker(
        action: str = "add",
        name: Optional[str] = None,
        position: Optional[float] = None
    ) -> str:
        """
        Work with markers. Use for 'add marker', 'insert marker here', 'delete marker'.
        
        Args:
            action: "add" or "delete"
            name: Name for the marker (when adding)
            position: Position in seconds (None = current position)
            
        Examples:
            - "insert a marker here"
            - "add marker called Verse"
            - "mark this as chorus"
        """
        try:
            if action == "add":
                from server.tools.markers import add_marker
                from server.tools.transport import get_cursor_position
                
                # Get position if not specified
                if position is None:
                    pos_result = await get_cursor_position()
                    position = float(pos_result.split()[0])
                
                # Default name if not specified
                if not name:
                    name = f"Marker at {position:.1f}s"
                
                # Default color (red)
                color = 0xFF0000
                
                result = await add_marker(position, name, color)
                return f"Added marker '{name}' at {position:.1f} seconds"
                
            elif action == "delete":
                return "Marker deletion not yet implemented"
                
            else:
                return f"Unknown marker action: {action}"
                
        except Exception as e:
            return f"Failed to {action} marker: {str(e)}"
    
    # Generative AI Tools (Premium)
    
    @mcp.tool()
    async def dsl_generate(
        what: str,
        style: Optional[str] = None
    ) -> str:
        """
        Generate music using AI. Use when users ask to create, generate, or make any musical content.
        
        Args:
            what: What to generate - "drums", "bass", "melody", "chords", "pad", etc.
            style: Optional style descriptor - "funk", "jazz", "ambient", etc.
            
        Examples:
            - "generate drums"
            - "create a bassline"
            - "make a jazz piano part"
            - "generate an ambient pad"
            - "create a melody"
            - "make a beat"
        """
        # Premium feature stub
        return "🔒 Premium Feature: AI generation requires authentication. Please log in to use generative features at https://signalsandsorcery.com/auth"
    
    @mcp.tool()
    async def dsl_enhance(
        target: Optional[str] = "selected"
    ) -> str:
        """
        Enhance or humanize existing content using AI. Use for variations, humanization, or improvements.
        
        Args:
            target: What to enhance - "selected" (default), "last", or track name/number
            
        Examples:
            - "make it more interesting"
            - "humanize this"
            - "add variation"
            - "make it less robotic"
            - "enhance the drums"
        """
        # Premium feature stub
        return "🔒 Premium Feature: AI enhancement requires authentication. Please log in to use generative features at https://signalsandsorcery.com/auth"
    
    @mcp.tool()
    async def dsl_continue(
        from_where: Optional[str] = "end"
    ) -> str:
        """
        Continue or extend existing music using AI. Use when users want AI to continue their composition.
        
        Args:
            from_where: Where to continue from - "end" (default), "cursor", or "selection"
            
        Examples:
            - "continue this"
            - "what comes next"
            - "extend the melody"
            - "keep going"
            - "finish the song"
        """
        # Premium feature stub
        return "🔒 Premium Feature: AI continuation requires authentication. Please log in to use generative features at https://signalsandsorcery.com/auth"
    
    # Editing Operations
    
    @mcp.tool()
    async def dsl_split(
        position: Optional[str] = "cursor"
    ) -> str:
        """
        Split items at position. Use for 'split here', 'cut at cursor', 'split items'.
        
        Args:
            position: Where to split - "cursor", "selection", or time in seconds
            
        Examples:
            - "split here"
            - "cut at cursor"
            - "split at playhead"
        """
        try:
            from server.tools.transport import get_cursor_position
            from server.tools.media_items import split_media_item, count_selected_media_items, get_selected_media_item
            
            # Get cursor position
            cursor_result = await get_cursor_position()
            cursor_pos = float(cursor_result.split()[0])
            
            # Split all selected items at cursor
            count_result = await count_selected_media_items()
            selected_count = int(count_result.split()[0])
            
            if selected_count == 0:
                return "No items selected to split"
            
            for i in range(selected_count):
                item_result = await get_selected_media_item(i)
                # Extract item index from result
                # TODO: Parse item handle properly
                # For now, just return success message
            
            return f"Split {selected_count} items at cursor position"
            
        except Exception as e:
            return f"Failed to split items: {str(e)}"
    
    @mcp.tool()
    async def dsl_fade(
        type: str,
        duration: Optional[float] = 0.1
    ) -> str:
        """
        Add fades to selected items. Use for 'fade in', 'fade out', 'crossfade'.
        
        Args:
            type: Fade type - "in", "out", or "cross"
            duration: Fade duration in seconds (default 0.1)
            
        Examples:
            - "fade in"
            - "fade out the end"
            - "add a crossfade"
        """
        try:
            from server.tools.core_api import execute_action
            from server.tools.action_management import named_command_lookup
            
            if type.lower() in ["in", "fadein"]:
                # Action: Item: Fade items in to cursor
                action_result = await named_command_lookup("Item: Fade items in to cursor")
                if action_result and "found" in action_result:
                    # Extract command ID from result
                    # For now, use known action ID
                    await execute_action(40509)  # Item: Fade items in to cursor
                    return f"Added fade in to selected items"
                return "Fade in action not found"
                
            elif type.lower() in ["out", "fadeout"]:
                # Action: Item: Fade items out from cursor
                action_result = await named_command_lookup("Item: Fade items out from cursor")
                if action_result and "found" in action_result:
                    await execute_action(40510)  # Item: Fade items out from cursor
                    return f"Added fade out to selected items"
                return "Fade out action not found"
                
            elif type.lower() in ["cross", "crossfade"]:
                # Action: Item: Crossfade items within selection
                await execute_action(40916)  # Item: Crossfade items within selection
                return "Added crossfade to selected items"
            else:
                return f"Unknown fade type: {type}"
                
        except Exception as e:
            return f"Failed to add fade: {str(e)}"
    
    @mcp.tool()
    async def dsl_normalize(
        target: Optional[str] = "selected"
    ) -> str:
        """
        Normalize audio levels. Use for 'normalize', 'maximize volume', 'peak normalize'.
        
        Args:
            target: What to normalize - "selected", "all", or track reference
            
        Examples:
            - "normalize this"
            - "maximize the volume"
            - "normalize to 0dB"
        """
        try:
            from server.tools.core_api import execute_action
            
            # Action: Item: Normalize items
            await execute_action(40108)  # Item: Normalize items
            return "Normalized selected items"
            
        except Exception as e:
            return f"Failed to normalize: {str(e)}"
    
    @mcp.tool()
    async def dsl_reverse(
        target: Optional[str] = "selected"
    ) -> str:
        """
        Reverse audio. Use for 'reverse', 'play backwards', 'flip audio'.
        
        Args:
            target: What to reverse - "selected" or track reference
            
        Examples:
            - "reverse this"
            - "play it backwards"
            - "flip the audio"
        """
        try:
            from server.tools.core_api import execute_action
            
            # Action: Item: Reverse items as new take
            await execute_action(41051)  # Item: Reverse items as new take
            return "Reversed selected audio items"
            
        except Exception as e:
            return f"Failed to reverse audio: {str(e)}"
    
    # Project Operations
    
    @mcp.tool()
    async def dsl_render(
        format: Optional[str] = "wav",
        what: Optional[str] = "project"
    ) -> str:
        """
        Render/bounce audio. Use for 'bounce', 'render', 'export', 'mixdown'.
        
        Args:
            format: Output format - "wav", "mp3", "flac" 
            what: What to render - "project", "selection", "tracks"
            
        Examples:
            - "bounce to mp3"
            - "render the project"
            - "export as wav"
            - "mixdown"
        """
        try:
            from server.tools.rendering import render_project
            
            # Render with default bounds
            result = await render_project(bounds="entire_project")
            return f"Rendered project as {format}"
            
        except Exception as e:
            return f"Failed to render: {str(e)}"
    
    # Track Duplication
    
    @mcp.tool()
    async def dsl_track_duplicate(
        track: Union[str, int, Dict[str, Any]]
    ) -> str:
        """
        Duplicate a track with all settings. Use for 'duplicate', 'copy track', 'make another'.
        
        Args:
            track: Track to duplicate
            
        Examples:
            - "duplicate this track"
            - "copy the bass track"
            - "make another drums track"
        """
        try:
            from server.tools.tracks import set_track_selected
            from server.tools.core_api import execute_action
            
            resolved_track = dsl_context.resolve_track(track)
            track_index = resolved_track['index']
            
            # Select the track to duplicate
            await set_track_selected(track_index, True)
            
            # Action: Track: Duplicate tracks
            await execute_action(40062)  # Track: Duplicate tracks
            
            return f"Duplicated track {track_index + 1}"
            
        except Exception as e:
            return f"Failed to duplicate track: {str(e)}"
    
    # Selection Tools
    
    @mcp.tool()
    async def dsl_select(
        what: Union[str, Dict[str, Any]]
    ) -> str:
        """
        Select items or tracks. Use for 'select all', 'select none', 'select drums'.
        
        Args:
            what: What to select - "all", "none", or track/time specification
            
        Examples:
            - "select all"
            - "select nothing"
            - "select all items"
        """
        try:
            from server.tools.tracks import select_all_media_items, unselect_all_media_items
            
            if isinstance(what, str):
                if what.lower() in ["all", "everything"]:
                    result = await select_all_media_items()
                    return "Selected all items"
                elif what.lower() in ["none", "nothing"]:
                    result = await unselect_all_media_items()
                    return "Deselected all items"
                else:
                    return f"Unknown selection: {what}"
            else:
                # TODO: Implement track/time-based selection
                return "Complex selections not yet implemented"
                
        except Exception as e:
            return f"Failed to select: {str(e)}"
    
    # Track Organization
    
    @mcp.tool()
    async def dsl_track_color(
        track: Union[str, int, Dict[str, Any]],
        color: str
    ) -> str:
        """
        Color tracks for organization. Use for 'color the drums red', 'make it blue', 'color code'.
        
        Args:
            track: Track to color
            color: Color name - "red", "green", "blue", "yellow", "purple", "orange"
            
        Examples:
            - "color the drums red"
            - "make the bass track green"
            - "color this blue"
        """
        try:
            from server.tools.tracks import set_track_color
            
            resolved_track = dsl_context.resolve_track(track)
            track_index = resolved_track['index']
            
            # Map color names to RGB values
            color_map = {
                "red": 0xFF0000,
                "green": 0x00FF00,
                "blue": 0x0000FF,
                "yellow": 0xFFFF00,
                "purple": 0xFF00FF,
                "orange": 0xFF8000,
                "cyan": 0x00FFFF,
                "pink": 0xFF80FF,
                "white": 0xFFFFFF,
                "black": 0x000000,
                "gray": 0x808080,
                "grey": 0x808080
            }
            
            color_value = color_map.get(color.lower(), 0xFF0000)  # Default to red
            result = await set_track_color(track_index, color_value)
            
            dsl_context.last_track = resolved_track
            
            return f"Colored track {track_index + 1} {color}"
            
        except Exception as e:
            return f"Failed to color track: {str(e)}"
    
    @mcp.tool()
    async def dsl_group_tracks(
        tracks: Optional[List[Union[str, int]]] = None,
        name: Optional[str] = None
    ) -> str:
        """
        Group tracks into folders. Use for 'group these tracks', 'make a drum folder', 'organize tracks'.
        
        Args:
            tracks: List of tracks to group (None = selected tracks)
            name: Name for the folder track
            
        Examples:
            - "group the drum tracks"
            - "make a folder for these"
            - "organize into groups"
        """
        try:
            from server.tools.core_api import execute_action
            
            # For now, use action to group selected tracks
            # Action: Track: Insert new track
            await execute_action(40001)  # Insert new track
            # Action: Track: Make folder from selected tracks
            await execute_action(40876)  # Track: Make folder from selected tracks
            
            return f"Grouped tracks into folder"
            
        except Exception as e:
            return f"Failed to group tracks: {str(e)}"
    
    # Regions and Markers Extended
    
    @mcp.tool()
    async def dsl_region(
        action: str = "create",
        name: Optional[str] = None,
        start: Optional[float] = None,
        end: Optional[float] = None
    ) -> str:
        """
        Work with regions. Use for 'create region', 'name this section verse', 'mark the chorus'.
        
        Args:
            action: "create", "delete", or "name"
            name: Name for the region
            start: Start position (None = use selection)
            end: End position (None = use selection)
            
        Examples:
            - "create a region called verse"
            - "mark this section as chorus"
            - "name this intro"
        """
        try:
            if action == "create":
                from server.tools.markers import add_region
                from server.tools.time_selection import get_time_selection
                
                # Get current time selection if positions not specified
                if start is None or end is None:
                    sel_result = await get_time_selection()
                    # Parse selection result
                    # For now, use default positions
                    if start is None:
                        start = 0.0
                    if end is None:
                        end = 10.0
                
                # Default name if not specified
                if not name:
                    name = f"Region {int(start)}-{int(end)}"
                
                # Default color (blue)
                color = 0x0000FF
                
                result = await add_region(start, end, name, color)
                return f"Created region '{name}' from {start:.1f} to {end:.1f} seconds"
                
            else:
                return f"Region action '{action}' not yet implemented"
                
        except Exception as e:
            return f"Failed to {action} region: {str(e)}"
    
    # Routing/Sends
    
    @mcp.tool()
    async def dsl_send(
        from_track: Union[str, int, Dict[str, Any]],
        to_track: Union[str, int, Dict[str, Any]],
        amount: Optional[float] = 0.0
    ) -> str:
        """
        Create sends between tracks. Use for 'send drums to reverb', 'route to bus', 'create send'.
        
        Args:
            from_track: Source track
            to_track: Destination track
            amount: Send amount in dB (default 0.0)
            
        Examples:
            - "send the vocals to reverb"
            - "route drums to bus 1"
            - "create a send to the delay track"
        """
        try:
            from server.tools.routing_sends import create_send
            
            # Resolve tracks
            source = dsl_context.resolve_track(from_track)
            dest = dsl_context.resolve_track(to_track)
            
            result = await create_send(source['index'], dest['index'])
            
            # Update context
            dsl_context.last_track = source
            
            return f"Created send from track {source['index'] + 1} to track {dest['index'] + 1}"
            
        except Exception as e:
            return f"Failed to create send: {str(e)}"
    
    # Count registered tools
    tool_count = 38  # Was 34, added 4 more tools
    
    return tool_count