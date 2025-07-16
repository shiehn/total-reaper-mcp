"""Non-interactive integration tests that avoid dialogs and popups."""

import pytest
import asyncio
import time


class TestNonInteractiveLoopWorkflows:
    """Test loop-based workflows without UI interaction."""
    
    @pytest.mark.asyncio
    async def test_automated_loop_composition(self, reaper_mcp_client):
        """Test creating a complete loop-based composition programmatically."""
        # Create project structure
        tracks = {}
        instruments = ["Drums", "Bass", "Lead", "Pad"]
        
        for idx, inst in enumerate(instruments):
            result = await reaper_mcp_client.call_tool("insert_track", {
                "index": idx,
                "name": inst
            })
            tracks[inst] = idx
        
        # Set up 8-bar loop
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 0.0,
            "end": 16.0  # 8 bars at 120 BPM
        })
        
        # Generate rhythmic patterns
        await reaper_mcp_client.call_tool("generate_random_rhythm", {
            "track_index": tracks["Drums"],
            "pattern_length": 16.0,
            "density": 0.7,
            "note_length": 0.25
        })
        
        # Create bass pattern with lower density
        await reaper_mcp_client.call_tool("generate_random_rhythm", {
            "track_index": tracks["Bass"],
            "pattern_length": 16.0,
            "density": 0.3,
            "note_length": 0.5
        })
        
        # Apply humanization
        await reaper_mcp_client.call_tool("select_all_items", {})
        await reaper_mcp_client.call_tool("humanize_items", {
            "position_amount": 0.02,
            "velocity_amount": 15,
            "timing_mode": "random"
        })
        
        # Duplicate to create arrangement
        await reaper_mcp_client.call_tool("duplicate_time_selection", {
            "count": 3
        })
        
        # Verify project length
        length_result = await reaper_mcp_client.call_tool("get_project_length", {})
        assert length_result.get("length") >= 64.0
    
    @pytest.mark.asyncio
    async def test_tempo_adaptive_generation(self, reaper_mcp_client):
        """Test generating patterns that adapt to tempo changes."""
        # Create track
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Adaptive Pattern"
        })
        
        # Set initial tempo (this uses existing transport controls)
        await reaper_mcp_client.call_tool("set_edit_cursor_position", {
            "position": 0.0
        })
        
        # Generate pattern at current tempo
        await reaper_mcp_client.call_tool("generate_random_rhythm", {
            "track_index": 0,
            "pattern_length": 8.0,
            "density": 0.5,
            "note_length": 0.25
        })
        
        # Apply different quantization strengths
        await reaper_mcp_client.call_tool("select_all_items", {})
        await reaper_mcp_client.call_tool("quantize_items_to_grid", {
            "strength": 0.8,
            "swing": 0.2
        })
        
        # Create variations
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 0.0,
            "end": 8.0
        })
        
        for i in range(3):
            await reaper_mcp_client.call_tool("duplicate_time_selection", {
                "count": 1
            })
            
            # Shift time selection forward
            await reaper_mcp_client.call_tool("shift_time_selection", {
                "offset": 8.0
            })
            
            # Apply different shuffle to each section
            await reaper_mcp_client.call_tool("apply_shuffle", {
                "amount": 0.1 + (i * 0.1),
                "pattern": "16th"
            })


class TestNonInteractiveMixingWorkflows:
    """Test mixing workflows without dialogs."""
    
    @pytest.mark.asyncio
    async def test_automated_stem_mixing(self, reaper_mcp_client):
        """Test creating and processing stems without rendering dialogs."""
        # Create multi-track session
        track_groups = {
            "Drums": ["Kick", "Snare", "HiHat"],
            "Bass": ["Bass DI"],
            "Keys": ["Piano", "Synth"]
        }
        
        all_tracks = {}
        track_idx = 0
        
        for group, tracks in track_groups.items():
            group_tracks = []
            for track_name in tracks:
                result = await reaper_mcp_client.call_tool("insert_track", {
                    "index": track_idx,
                    "name": track_name
                })
                group_tracks.append(track_idx)
                all_tracks[track_name] = track_idx
                track_idx += 1
            track_groups[group] = group_tracks
        
        # Create stems without rendering
        stems = await reaper_mcp_client.call_tool("create_stem_buses", {
            "stem_groups": track_groups
        })
        
        # Add processing to stems
        for stem in stems.get("stems_created", []):
            # Add EQ
            await reaper_mcp_client.call_tool("track_fx_add_by_name", {
                "track_index": stem["bus_index"],
                "fx_name": "ReaEQ",
                "instantiate": -1
            })
            
            # Add compression
            await reaper_mcp_client.call_tool("track_fx_add_by_name", {
                "track_index": stem["bus_index"],
                "fx_name": "ReaComp",
                "instantiate": -1
            })
        
        # Create parallel compression for drums
        drum_stem = next(s for s in stems.get("stems_created", []) if s["name"] == "Drums")
        pc_result = await reaper_mcp_client.call_tool("create_parallel_compression_bus", {
            "source_track_indices": [drum_stem["bus_index"]],
            "bus_name": "Drum Crush",
            "blend_amount_db": -10.0
        })
        
        # Verify routing
        routing = await reaper_mcp_client.call_tool("analyze_routing_matrix", {})
        assert routing.get("track_count") >= track_idx + len(track_groups) + 1
    
    @pytest.mark.asyncio
    async def test_automated_fx_processing(self, reaper_mcp_client):
        """Test applying effects and processing without dialogs."""
        # Create tracks
        tracks = []
        for i in range(4):
            result = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": f"Track {i+1}"
            })
            tracks.append(i)
        
        # Add effects programmatically
        fx_chains = [
            ["ReaEQ", "ReaComp"],
            ["ReaDelay", "ReaVerbate"],
            ["ReaPitch", "ReaFir"],
            ["ReaGate", "ReaLimit"]
        ]
        
        for track_idx, fx_chain in enumerate(fx_chains):
            for fx in fx_chain:
                await reaper_mcp_client.call_tool("track_fx_add_by_name", {
                    "track_index": track_idx,
                    "fx_name": fx,
                    "instantiate": -1
                })
        
        # Create sends between tracks
        await reaper_mcp_client.call_tool("create_track_send", {
            "source_track_index": 0,
            "dest_track_index": 1
        })
        
        # Set up sidechain routing
        await reaper_mcp_client.call_tool("create_sidechain_routing", {
            "source_track_index": 0,
            "destination_track_index": 2,
            "channel_offset": 2
        })
        
        # Bypass/unbypass effects
        for track_idx in tracks:
            # Get FX count
            fx_count = await reaper_mcp_client.call_tool("track_fx_get_count", {
                "track_index": track_idx
            })
            
            # Toggle bypass on first effect
            if fx_count.get("count", 0) > 0:
                await reaper_mcp_client.call_tool("track_fx_set_enabled", {
                    "track_index": track_idx,
                    "fx_index": 0,
                    "enabled": False
                })
                
                await asyncio.sleep(0.1)
                
                await reaper_mcp_client.call_tool("track_fx_set_enabled", {
                    "track_index": track_idx,
                    "fx_index": 0,
                    "enabled": True
                })


class TestNonInteractiveAutomation:
    """Test automation workflows without dialogs."""
    
    @pytest.mark.asyncio
    async def test_automated_envelope_creation(self, reaper_mcp_client):
        """Test creating and manipulating envelopes programmatically."""
        # Create track
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Automated Track"
        })
        
        # Get volume envelope
        vol_env = await reaper_mcp_client.call_tool("get_track_envelope", {
            "track_index": 0,
            "envelope_name": "Volume"
        })
        
        if not vol_env.get("envelope"):
            # Create visible volume envelope
            await reaper_mcp_client.call_tool("main_on_command", {
                "command": 40406  # Track: Toggle track volume envelope visible
            })
            
            vol_env = await reaper_mcp_client.call_tool("get_track_envelope", {
                "track_index": 0,
                "envelope_name": "Volume"
            })
        
        # Add automation points
        if vol_env.get("envelope"):
            env_handle = vol_env.get("envelope")
            
            # Create fade in
            for i in range(5):
                time = i * 2.0
                value = i / 4.0  # 0 to 1
                await reaper_mcp_client.call_tool("insert_envelope_point", {
                    "envelope": env_handle,
                    "time": time,
                    "value": value,
                    "shape": 0,
                    "tension": 0.0
                })
            
            # Create fade out
            for i in range(5):
                time = 10.0 + (i * 2.0)
                value = 1.0 - (i / 4.0)  # 1 to 0
                await reaper_mcp_client.call_tool("insert_envelope_point", {
                    "envelope": env_handle,
                    "time": time,
                    "value": value,
                    "shape": 0,
                    "tension": 0.0
                })
    
    @pytest.mark.asyncio
    async def test_tempo_automation(self, reaper_mcp_client):
        """Test creating tempo changes programmatically."""
        # Enable tempo envelope
        await reaper_mcp_client.call_tool("main_on_command", {
            "command": 41138  # View: Show tempo envelope
        })
        
        # Get tempo envelope from master track
        master = await reaper_mcp_client.call_tool("get_master_track", {})
        tempo_env = await reaper_mcp_client.call_tool("get_track_envelope", {
            "track_index": -1,  # Master track
            "envelope_name": "Tempo"
        })
        
        if tempo_env.get("envelope"):
            env_handle = tempo_env.get("envelope")
            
            # Create tempo ramp
            tempos = [120, 140, 160, 140, 120]
            for i, bpm in enumerate(tempos):
                time = i * 8.0  # Every 8 seconds
                # Normalize BPM to envelope value (0-1 range)
                value = (bpm - 60) / 200  # Assuming 60-260 BPM range
                
                await reaper_mcp_client.call_tool("insert_envelope_point", {
                    "envelope": env_handle,
                    "time": time,
                    "value": value,
                    "shape": 1,  # Linear
                    "tension": 0.0
                })


class TestNonInteractiveProjectManagement:
    """Test project management without save dialogs."""
    
    @pytest.mark.asyncio
    async def test_track_versions_workflow(self, reaper_mcp_client):
        """Test creating track versions using takes."""
        # Create track
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Multi-version Track"
        })
        
        # Create multiple items as "versions"
        for version in range(3):
            # Add item
            item = await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": 0,
                "position": 0.0,
                "length": 8.0
            })
            
            # Name the take
            if item.get("item"):
                take = await reaper_mcp_client.call_tool("get_active_take", {
                    "item": item.get("item")
                })
                
                if take.get("take"):
                    await reaper_mcp_client.call_tool("set_take_name", {
                        "take": take.get("take"),
                        "name": f"Version {version + 1}"
                    })
        
        # Comp between versions (select different takes)
        item = await reaper_mcp_client.call_tool("get_media_item", {
            "project": 0,
            "item_index": 0
        })
        
        if item.get("item"):
            # Cycle through takes
            for i in range(3):
                await reaper_mcp_client.call_tool("set_active_take", {
                    "item": item.get("item"),
                    "take_index": i
                })
                await asyncio.sleep(0.1)
    
    @pytest.mark.asyncio
    async def test_marker_based_navigation(self, reaper_mcp_client):
        """Test using markers for navigation without dialogs."""
        # Create markers at key positions
        markers = [
            {"time": 0.0, "name": "Intro", "color": 0xFF0000},
            {"time": 16.0, "name": "Verse 1", "color": 0x00FF00},
            {"time": 32.0, "name": "Chorus", "color": 0x0000FF},
            {"time": 48.0, "name": "Verse 2", "color": 0x00FF00},
            {"time": 64.0, "name": "Chorus 2", "color": 0x0000FF},
            {"time": 80.0, "name": "Outro", "color": 0xFF00FF}
        ]
        
        for marker in markers:
            await reaper_mcp_client.call_tool("add_project_marker", {
                "project": 0,
                "is_region": False,
                "position": marker["time"],
                "region_end": 0,
                "name": marker["name"],
                "marker_index": -1,
                "color": marker["color"]
            })
        
        # Navigate between markers
        for i in range(len(markers)):
            # Go to marker
            await reaper_mcp_client.call_tool("go_to_marker", {
                "project": 0,
                "marker_index": i
            })
            
            # Get cursor position to verify
            pos = await reaper_mcp_client.call_tool("get_cursor_position", {})
            expected_pos = markers[i]["time"]
            assert abs(pos.get("position", 0) - expected_pos) < 0.01
    
    @pytest.mark.asyncio
    async def test_region_based_looping(self, reaper_mcp_client):
        """Test creating regions for loop sections."""
        # Create regions for song sections
        regions = [
            {"start": 0.0, "end": 16.0, "name": "Intro Loop"},
            {"start": 16.0, "end": 48.0, "name": "Verse Loop"},
            {"start": 48.0, "end": 80.0, "name": "Chorus Loop"}
        ]
        
        for region in regions:
            await reaper_mcp_client.call_tool("add_project_marker", {
                "project": 0,
                "is_region": True,
                "position": region["start"],
                "region_end": region["end"],
                "name": region["name"],
                "marker_index": -1
            })
        
        # Set time selection to each region
        for region in regions:
            await reaper_mcp_client.call_tool("set_time_selection", {
                "start": region["start"],
                "end": region["end"]
            })
            
            # Enable looping
            await reaper_mcp_client.call_tool("set_loop_enabled", {
                "enabled": True
            })
            
            # Could start playback here if needed
            # await reaper_mcp_client.call_tool("transport_play", {})
            # await asyncio.sleep(2)
            # await reaper_mcp_client.call_tool("transport_stop", {})


class TestNonInteractiveMIDIGeneration:
    """Test MIDI generation without dialogs."""
    
    @pytest.mark.asyncio
    async def test_chord_progression_generation(self, reaper_mcp_client):
        """Test generating chord progressions programmatically."""
        # Create track for chords
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Chord Progression"
        })
        
        # Define chord progression (C-Am-F-G)
        chords = [
            {"root": 60, "notes": [60, 64, 67]},  # C major
            {"root": 57, "notes": [57, 60, 64]},  # A minor
            {"root": 65, "notes": [65, 69, 72]},  # F major
            {"root": 67, "notes": [67, 71, 74]}   # G major
        ]
        
        # Generate chord progression
        for i, chord in enumerate(chords):
            position = i * 4.0  # Each chord lasts 2 bars
            
            # Create MIDI item
            item = await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": 0,
                "position": position,
                "length": 4.0
            })
            
            # Would need CreateNewMIDIItemInProj to add actual notes
            # For now, we create the structure
    
    @pytest.mark.asyncio
    async def test_polyrhythmic_generation(self, reaper_mcp_client):
        """Test generating complex polyrhythms without interaction."""
        # Create tracks for polyrhythm
        tracks = []
        ratios = [3, 4, 5, 7]  # Complex polyrhythm
        
        for i, ratio in enumerate(ratios):
            result = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": f"{ratio}-beat pattern"
            })
            tracks.append(i)
        
        # Generate polyrhythmic patterns
        await reaper_mcp_client.call_tool("create_polyrhythm", {
            "track_indices": tracks,
            "base_division": 0.25,
            "ratios": ratios
        })
        
        # Set loop for one complete cycle
        cycle_length = 16.0  # LCM-based cycle
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 0.0,
            "end": cycle_length
        })
        
        # Apply humanization to make it more musical
        await reaper_mcp_client.call_tool("select_all_items", {})
        await reaper_mcp_client.call_tool("humanize_items", {
            "position_amount": 0.005,
            "velocity_amount": 10,
            "timing_mode": "random"
        })