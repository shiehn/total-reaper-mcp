"""Integration tests for new music production tools."""

import pytest
import asyncio


class TestLoopManagementIntegration:
    """Integration tests for loop management tools."""
    
    @pytest.mark.asyncio
    async def test_full_loop_workflow(self, reaper_mcp_client):
        """Test complete loop-based workflow."""
        # Set up a 4-bar loop
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 0.0,
            "end": 8.0  # 4 bars at 120 BPM
        })
        
        # Create tracks for loop
        # For now, use hardcoded track indices since insert_track returns text
        drum_track_idx = 0
        bass_track_idx = 1
        
        await reaper_mcp_client.call_tool("insert_track", {
            "index": drum_track_idx,
            "use_defaults": True
        })
        await reaper_mcp_client.call_tool("insert_track", {
            "index": bass_track_idx,
            "use_defaults": True
        })
        
        # Generate rhythm on drum track
        rhythm_result = await reaper_mcp_client.call_tool("generate_random_rhythm", {
            "track_index": drum_track_idx,
            "pattern_length": 8.0,
            "density": 0.6,
            "note_length": 0.25
        })
        # For now, just check that the call succeeded
        assert rhythm_result is not None
        
        # Enable looping
        loop_result = await reaper_mcp_client.call_tool("set_loop_enabled", {
            "enabled": True
        })
        assert loop_result.get("success") is True
        
        # Duplicate the loop
        dup_result = await reaper_mcp_client.call_tool("duplicate_time_selection", {
            "count": 3
        })
        assert dup_result.get("success") is True
        
        # Verify project length extended
        project_info = await reaper_mcp_client.call_tool("get_project_length", {})
        assert project_info.get("length") >= 32.0  # Original 8 + 3 duplicates
    
    @pytest.mark.asyncio
    async def test_grid_quantization_workflow(self, reaper_mcp_client):
        """Test grid and quantization workflow."""
        # Set grid to 16th notes
        grid_result = await reaper_mcp_client.call_tool("set_grid_division", {
            "division": 0.25,  # 16th note
            "swing": 0.15
        })
        assert grid_result.get("success") is True
        
        # Create track with unquantized items
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Unquantized"
        })
        
        # Add items slightly off-grid
        positions = [0.05, 0.52, 1.03, 1.48, 2.02, 2.51, 3.05, 3.49]
        for pos in positions:
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": track.get("track_index"),
                "position": pos,
                "length": 0.2
            })
        
        # Select all and quantize
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        quant_result = await reaper_mcp_client.call_tool("quantize_time_selection", {
            "strength": 0.9
        })
        assert quant_result.get("success") is True
    
    @pytest.mark.asyncio
    async def test_polyrhythm_creation(self, reaper_mcp_client):
        """Test creating polyrhythmic patterns."""
        # Create three tracks for polyrhythm
        tracks = []
        for i in range(3):
            track = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": f"Poly {i+1}"
            })
            tracks.append(track.get("track_index"))
        
        # Create 3:4:5 polyrhythm
        poly_result = await reaper_mcp_client.call_tool("create_polyrhythm", {
            "track_indices": tracks,
            "base_division": 0.25,
            "ratios": [3, 4, 5]
        })
        
        assert poly_result.get("success") is True
        assert len(poly_result.get("tracks_processed")) == 3
        
        # Set loop for polyrhythm pattern
        await reaper_mcp_client.call_tool("set_loop_points", {
            "start": 0.0,
            "end": poly_result.get("pattern_length"),
            "enable": True
        })


class TestBounceRenderIntegration:
    """Integration tests for bounce and render tools."""
    
    @pytest.mark.asyncio
    async def test_track_bounce_workflow(self, reaper_mcp_client):
        """Test complete track bouncing workflow."""
        # Create tracks with content
        tracks = []
        for i, name in enumerate(["Kick", "Snare", "HiHat"]):
            track = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": name
            })
            tracks.append(track.get("track_index"))
            
            # Add some items
            for j in range(4):
                await reaper_mcp_client.call_tool("add_media_item", {
                    "track_index": track.get("track_index"),
                    "position": j * 2.0,
                    "length": 0.5
                })
        
        # Create stem bus for drums
        stem_result = await reaper_mcp_client.call_tool("create_stem_buses", {
            "stem_groups": {
                "Drums": tracks
            }
        })
        assert stem_result.get("success") is True
        drum_bus = stem_result.get("stems_created")[0].get("bus_index")
        
        # Bounce the drum bus
        bounce_result = await reaper_mcp_client.call_tool("bounce_track_in_place", {
            "track_index": drum_bus,
            "tail_length": 0.5
        })
        assert bounce_result.get("success") is True
    
    @pytest.mark.asyncio
    async def test_freeze_unfreeze_workflow(self, reaper_mcp_client):
        """Test track freezing workflow."""
        # Create track with heavy processing
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Heavy Synth"
        })
        track_idx = track.get("track_index")
        
        # Add items
        for i in range(8):
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": track_idx,
                "position": i * 1.0,
                "length": 0.8
            })
        
        # Add FX (would normally add heavy synth/effects)
        await reaper_mcp_client.call_tool("track_fx_add_by_name", {
            "track_index": track_idx,
            "fx_name": "ReaSynth",
            "instantiate": -1
        })
        
        # Freeze track
        freeze_result = await reaper_mcp_client.call_tool("freeze_track", {
            "track_index": track_idx,
            "freeze_fx": True
        })
        assert freeze_result.get("success") is True
        
        # Unfreeze track
        unfreeze_result = await reaper_mcp_client.call_tool("unfreeze_track", {
            "track_index": track_idx
        })
        assert unfreeze_result.get("success") is True
    
    @pytest.mark.asyncio
    async def test_stem_export_workflow(self, reaper_mcp_client):
        """Test exporting stems workflow."""
        # Create multiple instrument tracks
        track_groups = {
            "Drums": [],
            "Bass": [],
            "Keys": []
        }
        
        # Create drum tracks
        for drum in ["Kick", "Snare", "HiHat"]:
            track = await reaper_mcp_client.call_tool("insert_track", {
                "index": len(track_groups.get("Drums")),
                "name": drum
            })
            track_groups.get("Drums").append(track.get("track_index"))
        
        # Create bass track
        bass = await reaper_mcp_client.call_tool("insert_track", {
            "index": 3,
            "name": "Bass"
        })
        track_groups.get("Bass").append(bass.get("track_index"))
        
        # Create keys tracks
        for key in ["Piano", "Pad"]:
            track = await reaper_mcp_client.call_tool("insert_track", {
                "index": 4 + len(track_groups.get("Keys")),
                "name": key
            })
            track_groups.get("Keys").append(track.get("track_index"))
        
        # Create stem buses
        stem_result = await reaper_mcp_client.call_tool("create_stem_buses", {
            "stem_groups": track_groups
        })
        assert stem_result.get("success") is True
        assert len(stem_result.get("stems_created")) == 3
        
        # Bounce stems to files
        stem_indices = [s.get("bus_index") for s in stem_result.get("stems_created")]
        bounce_result = await reaper_mcp_client.call_tool("bounce_tracks_to_stems", {
            "track_indices": stem_indices,
            "output_directory": "/tmp/stems",
            "file_prefix": "mix",
            "tail_length": 1.0
        })
        assert bounce_result.get("success") is True


class TestGrooveQuantizationIntegration:
    """Integration tests for groove and quantization tools."""
    
    @pytest.mark.asyncio
    async def test_groove_template_workflow(self, reaper_mcp_client):
        """Test creating and applying groove templates."""
        # Create source track with groove
        source = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Groove Source"
        })
        
        # Add groovy pattern
        groove_positions = [0.0, 0.48, 0.95, 1.52, 2.0, 2.45, 3.03, 3.48]
        for pos in groove_positions:
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": source.get("track_index"),
                "position": pos,
                "length": 0.15
            })
        
        # Select and create groove template
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        groove_result = await reaper_mcp_client.call_tool("create_groove_template", {
            "name": "Funky Groove",
            "analyze_selection": True
        })
        assert groove_result.get("success") is True
        
        # Create target track with straight rhythm
        target = await reaper_mcp_client.call_tool("insert_track", {
            "index": 1,
            "name": "Straight Rhythm"
        })
        
        # Add straight 16ths
        for i in range(16):
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": target.get("track_index"),
                "position": i * 0.25,
                "length": 0.125
            })
        
        # Apply groove to target
        await reaper_mcp_client.call_tool("select_all_items_on_track", {
            "track_index": target.get("track_index")
        })
        
        apply_result = await reaper_mcp_client.call_tool("apply_groove_to_items", {
            "groove_name": "Funky Groove",
            "strength": 0.75
        })
        assert apply_result.get("success") is True
    
    @pytest.mark.asyncio
    async def test_humanization_workflow(self, reaper_mcp_client):
        """Test humanizing robotic patterns."""
        # Create track
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Robotic Pattern"
        })
        
        # Create perfectly timed pattern
        for bar in range(4):
            for beat in range(4):
                pos = bar * 4.0 + beat * 1.0
                await reaper_mcp_client.call_tool("add_media_item", {
                    "track_index": track.get("track_index"),
                    "position": pos,
                    "length": 0.5
                })
        
        # Select all and humanize
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        humanize_result = await reaper_mcp_client.call_tool("humanize_items", {
            "position_amount": 0.03,
            "velocity_amount": 20,
            "timing_mode": "random"
        })
        assert humanize_result.get("success") is True
        assert humanize_result.get("items_humanized") == 16
    
    @pytest.mark.asyncio
    async def test_tempo_detection_stretch(self, reaper_mcp_client):
        """Test tempo detection and stretching."""
        # Create track with audio
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Audio Loop"
        })
        
        # Add audio item (simulating imported loop)
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track.get("track_index"),
            "position": 0.0,
            "length": 4.0  # 2 bars at 120 BPM
        })
        
        # Select and detect tempo
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        detect_result = await reaper_mcp_client.call_tool("detect_tempo_from_selection", {})
        assert "detected_tempo" in detect_result
        
        # Stretch to new tempo
        stretch_result = await reaper_mcp_client.call_tool("stretch_items_to_tempo", {
            "target_bpm": 140.0,
            "preserve_pitch": True
        })
        assert stretch_result.get("success") is True


class TestBusRoutingIntegration:
    """Integration tests for bus routing and mixing."""
    
    @pytest.mark.asyncio
    async def test_parallel_compression_setup(self, reaper_mcp_client):
        """Test setting up parallel compression."""
        # Create drum tracks
        drum_tracks = []
        for drum in ["Kick", "Snare", "Overhead L", "Overhead R"]:
            track = await reaper_mcp_client.call_tool("insert_track", {
                "index": len(drum_tracks),
                "name": drum
            })
            drum_tracks.append(track.get("track_index"))
        
        # Create parallel compression bus
        pc_result = await reaper_mcp_client.call_tool("create_parallel_compression_bus", {
            "source_track_indices": drum_tracks,
            "bus_name": "Drum Smash",
            "blend_amount_db": -10.0
        })
        assert pc_result.get("success") is True
        assert pc_result.get("compressor_added") is True
    
    @pytest.mark.asyncio
    async def test_reverb_send_setup(self, reaper_mcp_client):
        """Test creating reverb sends."""
        # Create reverb bus
        reverb_result = await reaper_mcp_client.call_tool("create_reverb_send_bus", {
            "reverb_type": "hall",
            "return_level_db": -12.0
        })
        assert reverb_result.get("success") is True
        reverb_bus = reverb_result.get("bus_index")
        
        # Create source tracks
        source_tracks = []
        for inst in ["Lead Vocal", "Piano", "Strings"]:
            track = await reaper_mcp_client.call_tool("insert_track", {
                "index": len(source_tracks),
                "name": inst
            })
            source_tracks.append(track.get("track_index"))
        
        # Route to reverb with different send levels
        send_levels = [-6.0, -12.0, -9.0]
        for track_idx, send_level in zip(source_tracks, send_levels):
            route_result = await reaper_mcp_client.call_tool("route_tracks_to_bus", {
                "source_track_indices": [track_idx],
                "bus_track_index": reverb_bus,
                "send_mode": "post-fader",
                "send_level_db": send_level
            })
            assert route_result.get("success") is True
    
    @pytest.mark.asyncio
    async def test_sidechain_setup(self, reaper_mcp_client):
        """Test sidechain routing setup."""
        # Create kick track
        kick = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Kick"
        })
        
        # Create bass track
        bass = await reaper_mcp_client.call_tool("insert_track", {
            "index": 1,
            "name": "Bass"
        })
        
        # Create sidechain routing
        sidechain_result = await reaper_mcp_client.call_tool("create_sidechain_routing", {
            "source_track_index": kick.get("track_index"),
            "destination_track_index": bass.get("track_index"),
            "channel_offset": 2
        })
        assert sidechain_result.get("success") is True
        assert sidechain_result.get("sidechain_channels") == "3/4"
        
        # Add compressor to bass track for sidechain
        await reaper_mcp_client.call_tool("track_fx_add_by_name", {
            "track_index": bass.get("track_index"),
            "fx_name": "ReaComp",
            "instantiate": -1
        })
    
    @pytest.mark.asyncio
    async def test_monitor_mix_setup(self, reaper_mcp_client):
        """Test setting up monitor mixes."""
        # Create performer tracks
        performer_tracks = []
        for inst in ["Vocal", "Guitar", "Keys"]:
            track = await reaper_mcp_client.call_tool("insert_track", {
                "index": len(performer_tracks),
                "name": inst
            })
            performer_tracks.append(track.get("track_index"))
        
        # Create click track
        click = await reaper_mcp_client.call_tool("insert_track", {
            "index": len(performer_tracks),
            "name": "Click"
        })
        
        # Setup monitor mix
        monitor_result = await reaper_mcp_client.call_tool("setup_monitor_mix", {
            "performer_tracks": performer_tracks,
            "click_track_index": click.get("track_index"),
            "output_channel": 2
        })
        assert monitor_result.get("success") is True
        assert monitor_result.get("click_included") is True
        
        # Create headphone cues
        cue_result = await reaper_mcp_client.call_tool("create_headphone_cue_mixes", {
            "num_mixes": 4
        })
        assert cue_result.get("success") is True
        assert len(cue_result.get("cue_mixes")) == 4
    
    @pytest.mark.asyncio
    async def test_full_mix_routing(self, reaper_mcp_client):
        """Test complete mix routing setup."""
        # Create full band setup
        track_groups = {
            "Drums": ["Kick", "Snare", "HiHat", "Toms", "Overheads"],
            "Bass": ["Bass DI", "Bass Amp"],
            "Guitars": ["Guitar L", "Guitar R", "Lead Guitar"],
            "Keys": ["Piano", "Organ", "Synth"],
            "Vocals": ["Lead Vox", "Harmony 1", "Harmony 2"]
        }
        
        all_tracks = {}
        track_idx = 0
        
        # Create all tracks
        for group_name, track_names in track_groups.items():
            all_tracks[group_name] = []
            for track_name in track_names:
                track = await reaper_mcp_client.call_tool("insert_track", {
                    "index": track_idx,
                    "name": track_name
                })
                all_tracks[group_name].append(track.get("track_index"))
                track_idx += 1
        
        # Create stem buses
        stem_result = await reaper_mcp_client.call_tool("create_stem_buses", {
            "stem_groups": all_tracks
        })
        assert stem_result.get("success") is True
        assert len(stem_result.get("stems_created")) == 5
        
        # Analyze routing matrix
        routing_result = await reaper_mcp_client.call_tool("analyze_routing_matrix", {})
        assert routing_result.get("success") is True
        assert routing_result.get("track_count") >= track_idx + 5  # All tracks + stems


class TestCompleteProductionWorkflow:
    """Test complete production workflows using all new tools."""
    
    @pytest.mark.asyncio
    async def test_loop_based_production(self, reaper_mcp_client):
        """Test complete loop-based production workflow."""
        # 1. Set up loop
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 0.0,
            "end": 8.0
        })
        await reaper_mcp_client.call_tool("set_loop_enabled", {"enabled": True})
        
        # 2. Create tracks
        drums = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0, "name": "Drums"
        })
        bass = await reaper_mcp_client.call_tool("insert_track", {
            "index": 1, "name": "Bass"
        })
        keys = await reaper_mcp_client.call_tool("insert_track", {
            "index": 2, "name": "Keys"
        })
        
        # 3. Generate rhythms
        await reaper_mcp_client.call_tool("generate_random_rhythm", {
            "track_index": drums.get("track_index"),
            "pattern_length": 8.0,
            "density": 0.7
        })
        
        # 4. Quantize with groove
        await reaper_mcp_client.call_tool("select_all_items", {})
        await reaper_mcp_client.call_tool("apply_shuffle", {
            "amount": 0.15,
            "pattern": "16th"
        })
        
        # 5. Duplicate loop to build arrangement
        await reaper_mcp_client.call_tool("duplicate_time_selection", {"count": 3})
        
        # 6. Create buses
        bus_result = await reaper_mcp_client.call_tool("create_stem_buses", {
            "stem_groups": {
                "Rhythm": [drums.get("track_index"), bass.get("track_index")],
                "Harmony": [keys.get("track_index")]
            }
        })
        
        # 7. Add reverb send
        reverb = await reaper_mcp_client.call_tool("create_reverb_send_bus", {
            "reverb_type": "room"
        })
        
        # 8. Bounce final mix
        await reaper_mcp_client.call_tool("render_project_to_file", {
            "output_path": "/tmp/loop_production.wav",
            "render_settings": {
                "sample_rate": 48000,
                "bit_depth": 24
            }
        })
    
    @pytest.mark.asyncio 
    async def test_stem_mixing_workflow(self, reaper_mcp_client):
        """Test stem mixing and processing workflow."""
        # Create multi-track session
        tracks = {}
        instruments = ["Kick", "Snare", "Bass", "Lead", "Pad"]
        
        for i, inst in enumerate(instruments):
            track = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": inst
            })
            tracks[inst] = track.get("track_index")
            
            # Add content
            for j in range(8):
                await reaper_mcp_client.call_tool("add_media_item", {
                    "track_index": track.get("track_index"),
                    "position": j * 1.0,
                    "length": 0.8
                })
        
        # Create stem groups
        stems = await reaper_mcp_client.call_tool("create_stem_buses", {
            "stem_groups": {
                "Drums": [tracks.get("Kick"), tracks.get("Snare")],
                "Bass": [tracks.get("Bass")],
                "Synths": [tracks.get("Lead"), tracks.get("Pad")]
            }
        })
        
        # Add parallel compression to drums
        drum_stem = next(s for s in stems.get("stems_created") if s.get("name") == "Drums")
        pc_result = await reaper_mcp_client.call_tool("create_parallel_compression_bus", {
            "source_track_indices": [drum_stem.get("bus_index")],
            "bus_name": "Drum Crush"
        })
        
        # Freeze synth tracks to save CPU
        for synth in ["Lead", "Pad"]:
            await reaper_mcp_client.call_tool("freeze_track", {
                "track_index": tracks[synth],
                "freeze_fx": True
            })
        
        # Bounce stems
        stem_indices = [s.get("bus_index") for s in stems.get("stems_created")]
        await reaper_mcp_client.call_tool("bounce_tracks_to_stems", {
            "track_indices": stem_indices,
            "output_directory": "/tmp/final_stems"
        })