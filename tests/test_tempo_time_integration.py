"""Integration tests for tempo and time management tools."""

import pytest
import asyncio


class TestTempoTimeManagement:
    """Test tempo and time management functions."""
    
    @pytest.mark.asyncio
    async def test_basic_tempo_operations(self, reaper_mcp_client):
        """Test getting and setting tempo."""
        # Get initial tempo
        initial = await reaper_mcp_client.call_tool("get_master_tempo", {})
        assert initial.get("success") is True
        assert "tempo" in initial
        original_tempo = initial.get("tempo")
        
        # Set new tempo
        new_tempo = 140.0
        result = await reaper_mcp_client.call_tool("set_current_bpm", {
            "bpm": new_tempo,
            "allow_undo": True
        })
        assert result.get("success") is True
        
        # Verify tempo changed
        verify = await reaper_mcp_client.call_tool("get_master_tempo", {})
        assert abs(verify.get("tempo") - new_tempo) < 0.01
        
        # Restore original tempo
        await reaper_mcp_client.call_tool("set_current_bpm", {
            "bpm": original_tempo
        })
    
    @pytest.mark.asyncio
    async def test_play_position_tracking(self, reaper_mcp_client):
        """Test getting play position information."""
        # Get basic position
        pos = await reaper_mcp_client.call_tool("get_play_position", {})
        assert "position" in pos
        assert "is_playing" in pos
        assert "is_recording" in pos
        
        # Get extended position
        pos_ex = await reaper_mcp_client.call_tool("get_play_position_ex", {})
        assert "position" in pos_ex
        assert "is_playing" in pos_ex
        assert "is_paused" in pos_ex
        assert "time_since_last_play" in pos_ex
    
    @pytest.mark.asyncio
    async def test_musical_time_conversion(self, reaper_mcp_client):
        """Test converting between time and beats."""
        # Set known tempo
        await reaper_mcp_client.call_tool("set_current_bpm", {"bpm": 120.0})
        
        # Convert time to beats (at 120 BPM, 2 seconds = 4 beats)
        result = await reaper_mcp_client.call_tool("time_to_beats", {
            "time": 2.0
        })
        assert result.get("success") is True
        assert abs(result.get("beats") - 4.0) < 0.01
        
        # Convert beats to time
        result = await reaper_mcp_client.call_tool("beats_to_time", {
            "beats": 8.0
        })
        assert result.get("success") is True
        assert abs(result.get("time") - 4.0) < 0.01
    
    @pytest.mark.asyncio
    async def test_grid_snapping(self, reaper_mcp_client):
        """Test snapping positions to grid."""
        # Set grid to quarter notes
        await reaper_mcp_client.call_tool("set_grid_division", {
            "division": 0.25
        })
        
        # Test snapping
        result = await reaper_mcp_client.call_tool("snap_to_grid", {
            "position": 1.1  # Should snap to 1.0 at 120 BPM
        })
        assert result.get("success") is True
        # Note: exact snap position depends on tempo and grid
    
    @pytest.mark.asyncio
    async def test_time_signature_management(self, reaper_mcp_client):
        """Test time signature operations."""
        # Get time signature at cursor
        sig = await reaper_mcp_client.call_tool("get_project_time_signature", {
            "position": 0.0
        })
        assert sig.get("success") is True
        assert "numerator" in sig
        assert "denominator" in sig
        assert "tempo" in sig
    
    @pytest.mark.asyncio
    async def test_tempo_markers(self, reaper_mcp_client):
        """Test tempo marker management."""
        # Count initial markers
        initial = await reaper_mcp_client.call_tool("count_tempo_markers", {})
        initial_count = initial.get("count", 0)
        
        # Add tempo marker
        result = await reaper_mcp_client.call_tool("add_tempo_marker", {
            "position": 10.0,
            "bpm": 140.0,
            "time_sig_num": 3,
            "time_sig_denom": 4
        })
        assert result.get("success") is True
        
        # Verify count increased
        after = await reaper_mcp_client.call_tool("count_tempo_markers", {})
        assert after.get("count") == initial_count + 1
        
        # Delete the marker
        await reaper_mcp_client.call_tool("delete_tempo_marker", {
            "index": initial_count  # Last added marker
        })
        
        # Verify restored
        final = await reaper_mcp_client.call_tool("count_tempo_markers", {})
        assert final.get("count") == initial_count
    
    @pytest.mark.asyncio
    async def test_time_formatting(self, reaper_mcp_client):
        """Test time formatting and parsing."""
        # Format time
        result = await reaper_mcp_client.call_tool("format_time", {
            "seconds": 90.5,
            "format_string": ""
        })
        assert result.get("success") is True
        assert "formatted" in result
        
        # Parse time string
        result = await reaper_mcp_client.call_tool("parse_time_string", {
            "time_string": "1:30"
        })
        assert result.get("success") is True
        assert abs(result.get("seconds") - 90.0) < 0.1
    
    @pytest.mark.asyncio
    async def test_loop_range_functions(self, reaper_mcp_client):
        """Test simplified loop range functions."""
        # Set loop range
        result = await reaper_mcp_client.call_tool("set_loop_time_range", {
            "start": 4.0,
            "end": 12.0
        })
        assert result.get("success") is True
        
        # Get loop range
        result = await reaper_mcp_client.call_tool("get_loop_time_range", {})
        assert result.get("success") is True
        assert abs(result.get("start") - 4.0) < 0.01
        assert abs(result.get("end") - 12.0) < 0.01
        assert result.get("is_set") is True
        
        # Clear loop
        await reaper_mcp_client.call_tool("set_loop_time_range", {
            "start": 0.0,
            "end": 0.0
        })


class TestGenerativeTempoWorkflows:
    """Test generative music workflows using tempo tools."""
    
    @pytest.mark.asyncio
    async def test_adaptive_tempo_generation(self, reaper_mcp_client):
        """Test creating adaptive tempo changes."""
        # Create tempo automation for build-up
        positions = [0.0, 8.0, 16.0, 24.0, 32.0]
        tempos = [120.0, 125.0, 130.0, 140.0, 128.0]
        
        for pos, bpm in zip(positions, tempos):
            await reaper_mcp_client.call_tool("add_tempo_marker", {
                "position": pos,
                "bpm": bpm
            })
        
        # Verify tempo at different positions
        for pos, expected_bpm in zip(positions, tempos):
            sig = await reaper_mcp_client.call_tool("get_project_time_signature", {
                "position": pos + 0.1  # Slightly after marker
            })
            # Tempo should be close to expected
            assert abs(sig.get("tempo") - expected_bpm) < 10.0
    
    @pytest.mark.asyncio
    async def test_beat_aligned_generation(self, reaper_mcp_client):
        """Test generating content aligned to musical beats."""
        # Set consistent tempo
        await reaper_mcp_client.call_tool("set_current_bpm", {"bpm": 120.0})
        
        # Create track
        track = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Beat Aligned"
        })
        
        # Generate items on beat boundaries
        beats = [0, 4, 8, 12, 16]  # Every bar at 4/4
        
        for beat in beats:
            # Convert beat to time
            time_result = await reaper_mcp_client.call_tool("beats_to_time", {
                "beats": float(beat)
            })
            time_pos = time_result.get("time", 0.0)
            
            # Create item at beat position
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": 0,
                "position": time_pos,
                "length": 0.5  # Half second
            })
        
        # Verify items are beat-aligned
        count = await reaper_mcp_client.call_tool("count_track_media_items", {
            "track_index": 0
        })
        assert count.get("count") == len(beats)