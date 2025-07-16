"""Integration tests for advanced MIDI generation tools."""

import pytest
import asyncio


class TestAdvancedMIDIGeneration:
    """Test advanced MIDI generation functions."""
    
    @pytest.mark.asyncio
    async def test_create_midi_item(self, reaper_mcp_client):
        """Test creating MIDI items programmatically."""
        # Create track
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "MIDI Track"
        })
        
        # Create MIDI item
        result = await reaper_mcp_client.call_tool("create_new_midi_item", {
            "track_index": 0,
            "start_time": 0.0,
            "end_time": 4.0
        })
        assert result.get("success") is True
        assert "item" in result
        assert "take" in result
        
        # Verify item exists
        count = await reaper_mcp_client.call_tool("count_track_media_items", {
            "track_index": 0
        })
        assert count.get("count") == 1
    
    @pytest.mark.asyncio
    async def test_midi_timing_conversion(self, reaper_mcp_client):
        """Test PPQ position conversions."""
        # Create MIDI item first
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Timing Test"
        })
        
        midi_item = await reaper_mcp_client.call_tool("create_new_midi_item", {
            "track_index": 0,
            "start_time": 0.0,
            "end_time": 8.0
        })
        
        take_handle = midi_item.get("take")
        
        # Convert time to PPQ
        result = await reaper_mcp_client.call_tool("get_ppq_position_from_time", {
            "take_handle": take_handle,
            "time": 2.0  # 2 seconds
        })
        assert result.get("success") is True
        ppq = result.get("ppq_pos")
        # At 120 BPM, 2 seconds = 4 beats = 3840 PPQ
        assert ppq > 0
        
        # Get measure boundaries
        start_result = await reaper_mcp_client.call_tool("get_ppq_pos_start_of_measure", {
            "take_handle": take_handle,
            "ppq_pos": ppq
        })
        assert start_result.get("success") is True
        
        end_result = await reaper_mcp_client.call_tool("get_ppq_pos_end_of_measure", {
            "take_handle": take_handle,
            "ppq_pos": ppq
        })
        assert end_result.get("success") is True
    
    @pytest.mark.asyncio
    async def test_midi_note_insertion(self, reaper_mcp_client):
        """Test inserting MIDI notes."""
        # Create MIDI item
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Note Test"
        })
        
        midi_item = await reaper_mcp_client.call_tool("create_new_midi_item", {
            "track_index": 0,
            "start_time": 0.0,
            "end_time": 4.0
        })
        
        take_handle = midi_item.get("take")
        
        # Insert notes using beat timing
        notes = [
            {"pitch": 60, "start": 0.0, "length": 0.5},  # C
            {"pitch": 64, "start": 0.5, "length": 0.5},  # E
            {"pitch": 67, "start": 1.0, "length": 0.5},  # G
            {"pitch": 72, "start": 1.5, "length": 0.5},  # C
        ]
        
        for note in notes:
            result = await reaper_mcp_client.call_tool("insert_midi_note_extended", {
                "take_handle": take_handle,
                "pitch": note["pitch"],
                "velocity": 80,
                "start_beats": note["start"],
                "length_beats": note["length"],
                "channel": 0
            })
            assert result.get("success") is True
        
        # Verify notes were added
        count_result = await reaper_mcp_client.call_tool("midi_count_events", {
            "take": take_handle
        })
        assert count_result.get("notes", 0) >= len(notes)
    
    @pytest.mark.asyncio
    async def test_chord_progression_generation(self, reaper_mcp_client):
        """Test generating chord progressions."""
        # Create MIDI track
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Chord Progression"
        })
        
        midi_item = await reaper_mcp_client.call_tool("create_new_midi_item", {
            "track_index": 0,
            "start_time": 0.0,
            "end_time": 16.0
        })
        
        take_handle = midi_item.get("take")
        
        # Generate I-V-vi-IV progression in C
        progression = [
            {"root": 60, "type": "major", "duration_beats": 4.0},     # C
            {"root": 67, "type": "major", "duration_beats": 4.0},     # G
            {"root": 69, "type": "minor", "duration_beats": 4.0},     # Am
            {"root": 65, "type": "major", "duration_beats": 4.0},     # F
        ]
        
        result = await reaper_mcp_client.call_tool("generate_chord_progression", {
            "take_handle": take_handle,
            "progression": progression,
            "start_beat": 0.0
        })
        assert result.get("success") is True
        assert result.get("notes_created") > 0
    
    @pytest.mark.asyncio
    async def test_scale_run_generation(self, reaper_mcp_client):
        """Test generating scale runs."""
        # Create MIDI track
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Scale Runs"
        })
        
        midi_item = await reaper_mcp_client.call_tool("create_new_midi_item", {
            "track_index": 0,
            "start_time": 0.0,
            "end_time": 8.0
        })
        
        take_handle = midi_item.get("take")
        
        # Generate ascending major scale
        result = await reaper_mcp_client.call_tool("generate_scale_run", {
            "take_handle": take_handle,
            "scale_type": "major",
            "root": 60,  # C
            "start_beat": 0.0,
            "note_duration": 0.25,  # 16th notes
            "num_octaves": 2,
            "direction": "up"
        })
        assert result.get("success") is True
        assert result.get("notes_created") > 0
        
        # Generate descending pentatonic
        result = await reaper_mcp_client.call_tool("generate_scale_run", {
            "take_handle": take_handle,
            "scale_type": "pentatonic",
            "root": 72,  # C
            "start_beat": 4.0,
            "note_duration": 0.125,  # 32nd notes
            "num_octaves": 1,
            "direction": "down"
        })
        assert result.get("success") is True
    
    @pytest.mark.asyncio
    async def test_midi_note_selection(self, reaper_mcp_client):
        """Test selecting MIDI notes by criteria."""
        # Create MIDI with notes
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Selection Test"
        })
        
        midi_item = await reaper_mcp_client.call_tool("create_new_midi_item", {
            "track_index": 0,
            "start_time": 0.0,
            "end_time": 4.0
        })
        
        take_handle = midi_item.get("take")
        
        # Add notes across range
        for i in range(8):
            await reaper_mcp_client.call_tool("insert_midi_note_extended", {
                "take_handle": take_handle,
                "pitch": 60 + i * 2,  # C, D, E, F#, G#, A#, C, D
                "velocity": 80,
                "start_beats": i * 0.5,
                "length_beats": 0.4
            })
        
        # Get PPQ range for selection
        ppq_start = await reaper_mcp_client.call_tool("get_ppq_position_from_time", {
            "take_handle": take_handle,
            "time": 0.0
        })
        ppq_end = await reaper_mcp_client.call_tool("get_ppq_position_from_time", {
            "take_handle": take_handle,
            "time": 2.0
        })
        
        # Select notes in first 2 seconds, pitch range C-G
        result = await reaper_mcp_client.call_tool("select_midi_notes", {
            "take_handle": take_handle,
            "start_ppq": ppq_start.get("ppq_pos"),
            "end_ppq": ppq_end.get("ppq_pos"),
            "pitch_low": 60,   # C
            "pitch_high": 67   # G
        })
        assert result.get("success") is True
        assert result.get("notes_selected") > 0
    
    @pytest.mark.asyncio
    async def test_track_note_range(self, reaper_mcp_client):
        """Test getting and setting track MIDI note range."""
        # Create track
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Bass Track"
        })
        
        # Set bass range
        result = await reaper_mcp_client.call_tool("set_track_midi_note_range", {
            "track_index": 0,
            "note_low": 28,   # E1
            "note_high": 60   # C4
        })
        assert result.get("success") is True
        
        # Get range
        result = await reaper_mcp_client.call_tool("get_track_midi_note_range", {
            "track_index": 0
        })
        assert result.get("success") is True
        assert result.get("note_low") == 28
        assert result.get("note_high") == 60
    
    @pytest.mark.asyncio
    async def test_midi_grid_settings(self, reaper_mcp_client):
        """Test getting MIDI grid settings."""
        # Create MIDI item
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Grid Test"
        })
        
        midi_item = await reaper_mcp_client.call_tool("create_new_midi_item", {
            "track_index": 0,
            "start_time": 0.0,
            "end_time": 4.0
        })
        
        take_handle = midi_item.get("take")
        
        # Get grid settings
        result = await reaper_mcp_client.call_tool("get_midi_grid", {
            "take_handle": take_handle
        })
        assert result.get("success") is True
        assert "division" in result
        assert "swing" in result
        assert "note_length" in result
    
    @pytest.mark.asyncio
    async def test_midi_hash_versioning(self, reaper_mcp_client):
        """Test MIDI hash for versioning."""
        # Create MIDI item
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Hash Test"
        })
        
        midi_item = await reaper_mcp_client.call_tool("create_new_midi_item", {
            "track_index": 0,
            "start_time": 0.0,
            "end_time": 4.0
        })
        
        take_handle = midi_item.get("take")
        
        # Get initial hash
        hash1 = await reaper_mcp_client.call_tool("get_midi_hash", {
            "take_handle": take_handle
        })
        initial_hash = hash1.get("hash")
        
        # Add a note
        await reaper_mcp_client.call_tool("insert_midi_note_extended", {
            "take_handle": take_handle,
            "pitch": 60,
            "velocity": 80,
            "start_beats": 0.0,
            "length_beats": 1.0
        })
        
        # Get new hash - should be different
        hash2 = await reaper_mcp_client.call_tool("get_midi_hash", {
            "take_handle": take_handle
        })
        new_hash = hash2.get("hash")
        
        assert initial_hash != new_hash


class TestGenerativeMIDIWorkflows:
    """Test complete generative MIDI workflows."""
    
    @pytest.mark.asyncio
    async def test_algorithmic_composition(self, reaper_mcp_client):
        """Test creating an algorithmic composition."""
        # Set tempo
        await reaper_mcp_client.call_tool("set_current_bpm", {"bpm": 140.0})
        
        # Create tracks for different parts
        parts = ["Bass", "Chords", "Melody", "Arp"]
        tracks = {}
        
        for i, part in enumerate(parts):
            track = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": part
            })
            tracks[part] = i
        
        # Create MIDI items
        items = {}
        for part, idx in tracks.items():
            item = await reaper_mcp_client.call_tool("create_new_midi_item", {
                "track_index": idx,
                "start_time": 0.0,
                "end_time": 16.0  # 4 bars
            })
            items[part] = item.get("take")
        
        # Generate bass line (root notes)
        bass_pattern = [
            {"root": 48, "beats": [0, 2, 4, 6]},      # C
            {"root": 43, "beats": [8, 10, 12, 14]},   # G
        ]
        
        for pattern in bass_pattern:
            for beat in pattern["beats"]:
                await reaper_mcp_client.call_tool("insert_midi_note_extended", {
                    "take_handle": items["Bass"],
                    "pitch": pattern["root"],
                    "velocity": 90,
                    "start_beats": beat,
                    "length_beats": 1.5
                })
        
        # Generate chord progression
        await reaper_mcp_client.call_tool("generate_chord_progression", {
            "take_handle": items["Chords"],
            "progression": [
                {"root": 60, "type": "min7", "duration_beats": 8.0},
                {"root": 67, "type": "dom7", "duration_beats": 8.0},
            ]
        })
        
        # Generate melodic line using scale
        await reaper_mcp_client.call_tool("generate_scale_run", {
            "take_handle": items["Melody"],
            "scale_type": "pentatonic",
            "root": 72,
            "start_beat": 0.0,
            "note_duration": 0.5,
            "num_octaves": 1,
            "direction": "both"
        })
        
        # Generate arpeggios
        arp_notes = [60, 64, 67, 72]  # C major arpeggio
        for i in range(32):  # 32 16th notes
            note = arp_notes[i % len(arp_notes)]
            await reaper_mcp_client.call_tool("insert_midi_note_extended", {
                "take_handle": items["Arp"],
                "pitch": note + (12 if i % 8 >= 4 else 0),  # Octave variation
                "velocity": 60 + (i % 4) * 10,  # Velocity pattern
                "start_beats": i * 0.25,
                "length_beats": 0.2
            })
        
        # Set up loop
        await reaper_mcp_client.call_tool("set_loop_time_range", {
            "start": 0.0,
            "end": 16.0
        })
        await reaper_mcp_client.call_tool("set_loop_enabled", {"enabled": True})