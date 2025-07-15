"""Tests for groove and quantization tools."""

import pytest
from unittest.mock import patch, MagicMock, call


class TestGrooveQuantization:
    """Test groove and quantization functions."""
    
    @pytest.mark.asyncio
    async def test_quantize_items_to_grid(self, reaper_mcp_client):
        """Test quantizing items to grid."""
        # Create track and items
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Quantize Test"
        })
        track_index = track_result.get("track_index")
        
        # Add items slightly off grid
        for i in range(4):
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": track_index,
                "position": i * 1.0 + 0.05,  # Slightly off beat
                "length": 0.5
            })
        
        # Select all items
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        # Quantize with partial strength
        result = await reaper_mcp_client.call_tool("quantize_items_to_grid", {
            "strength": 0.8,
            "swing": 0.2
        })
        
        assert result
        assert result.get("items_quantized") == 4
        assert result.get("strength") == 0.8
        assert result.get("swing") == 0.2
    
    @pytest.mark.asyncio
    async def test_humanize_items(self, reaper_mcp_client):
        """Test humanizing items."""
        # Create track with items
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Humanize Test"
        })
        track_index = track_result.get("track_index")
        
        # Add perfectly timed items
        for i in range(4):
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": track_index,
                "position": i * 1.0,
                "length": 0.5
            })
        
        # Select items
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        # Humanize
        result = await reaper_mcp_client.call_tool("humanize_items", {
            "position_amount": 0.02,
            "velocity_amount": 15,
            "timing_mode": "random"
        })
        
        assert result
        assert result.get("items_humanized") == 4
        assert result.get("timing_mode") == "random"
    
    @pytest.mark.asyncio
    async def test_create_and_apply_groove(self, reaper_mcp_client):
        """Test creating and applying groove templates."""
        # Create source track with groove
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Groove Source"
        })
        
        # Add items with specific timing
        positions = [0.0, 0.48, 1.0, 1.52, 2.0, 2.48, 3.0, 3.52]
        for pos in positions:
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": track_result.get("track_index"),
                "position": pos,
                "length": 0.2
            })
        
        # Select groove source items
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        # Create groove template
        groove_result = await reaper_mcp_client.call_tool("create_groove_template", {
            "name": "Test Groove",
            "analyze_selection": True
        })
        
        assert groove_result
        assert groove_result.get("success") is True
        assert groove_result.get("name") == "Test Groove"
        
        # Create target track
        target_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 1,
            "name": "Groove Target"
        })
        
        # Add straight items
        for i in range(8):
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": target_result.get("track_index"),
                "position": i * 0.5,
                "length": 0.2
            })
        
        # Select target items
        await reaper_mcp_client.call_tool("unselect_all_items", {})
        await reaper_mcp_client.call_tool("select_all_items_on_track", {
            "track_index": target_result.get("track_index")
        })
        
        # Apply groove
        apply_result = await reaper_mcp_client.call_tool("apply_groove_to_items", {
            "groove_name": "Test Groove",
            "strength": 0.75
        })
        
        assert apply_result
        assert apply_result.get("groove_name") == "Test Groove"
        assert apply_result.get("items_affected") > 0
    
    @pytest.mark.asyncio
    async def test_generate_random_rhythm(self, reaper_mcp_client):
        """Test generating random rhythm patterns."""
        # Create track
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Random Rhythm"
        })
        track_index = track_result.get("track_index")
        
        # Generate rhythm
        result = await reaper_mcp_client.call_tool("generate_random_rhythm", {
            "track_index": track_index,
            "pattern_length": 4.0,
            "density": 0.6,
            "note_length": 0.25
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("notes_created") > 0
        assert result.get("pattern_length") == 4.0
    
    @pytest.mark.asyncio
    async def test_apply_shuffle(self, reaper_mcp_client):
        """Test applying shuffle to items."""
        # Create track with straight 16th notes
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Shuffle Test"
        })
        track_index = track_result.get("track_index")
        
        # Add straight 16th notes
        for i in range(16):
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": track_index,
                "position": i * 0.25,
                "length": 0.125
            })
        
        # Select all
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        # Apply shuffle
        result = await reaper_mcp_client.call_tool("apply_shuffle", {
            "amount": 0.67,  # Classic MPC shuffle
            "pattern": "16th"
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("amount") == 0.67
        assert result.get("pattern") == "16th"
    
    @pytest.mark.asyncio
    async def test_create_polyrhythm(self, reaper_mcp_client):
        """Test creating polyrhythmic patterns."""
        # Create multiple tracks
        track_indices = []
        for i in range(3):
            track_result = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": f"Poly Track {i+1}"
            })
            track_indices.append(track_result.get("track_index"))
        
        # Create polyrhythm (3:4:5)
        result = await reaper_mcp_client.call_tool("create_polyrhythm", {
            "track_indices": track_indices,
            "base_division": 0.25,
            "ratios": [3, 4, 5]
        })
        
        assert result
        assert result.get("success") is True
        assert len(result.get("tracks_processed", [])) == 3
        
        # Verify ratios
        for idx, track_info in enumerate(result.get("tracks_processed", [])):
            assert track_info["ratio"] == [3, 4, 5][idx]
            assert track_info["notes_created"] > 0
    
    @pytest.mark.asyncio
    async def test_stretch_items_to_tempo(self, reaper_mcp_client):
        """Test stretching items to match tempo."""
        # Create track with audio item
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Tempo Stretch"
        })
        track_index = track_result.get("track_index")
        
        # Add item (simulating 120 BPM content)
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 0.0,
            "length": 4.0  # 2 bars at 120 BPM
        })
        
        # Select item
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        # Stretch to 140 BPM
        result = await reaper_mcp_client.call_tool("stretch_items_to_tempo", {
            "target_bpm": 140.0,
            "preserve_pitch": True
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("target_bpm") == 140.0
        assert result.get("preserve_pitch") is True
        assert result.get("items_stretched") == 1
    
    @pytest.mark.asyncio
    async def test_detect_tempo_from_selection(self, reaper_mcp_client):
        """Test detecting tempo from audio."""
        # Create track
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Tempo Detection"
        })
        track_index = track_result.get("track_index")
        
        # Add audio item
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 0.0,
            "length": 8.0
        })
        
        # Select item
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        # Detect tempo
        result = await reaper_mcp_client.call_tool("detect_tempo_from_selection", {})
        
        assert result
        assert "detected_tempo" in result
        assert result.get("items_analyzed") == 1


class TestGrooveQuantizationSync:
    """Synchronous tests for groove/quantization using mocked bridge."""
    
    @patch('server.tools.groove_quantization.ReaperBridge.send_request')
    def test_quantize_items_sync(self, mock_send):
        """Test quantizing items with mock."""
        from server.tools.groove_quantization import quantize_items_to_grid
        
        # Mock responses
        mock_send.side_effect = [
            {"result": True, "division": 0.25},  # GetSetProjectGrid
            {"result": True, "count": 2},  # CountSelectedMediaItems
            {"result": True, "item": "item1"},  # GetSelectedMediaItem
            {"result": True, "value": 0.1},  # GetMediaItemInfo_Value (position)
            {"result": True},  # SetMediaItemInfo_Value (new position)
            {"result": True, "item": "item2"},  # GetSelectedMediaItem
            {"result": True, "value": 1.1},  # GetMediaItemInfo_Value (position)
            {"result": True},  # SetMediaItemInfo_Value (new position)
        ]
        
        result = quantize_items_to_grid(strength=0.5, swing=0.0)
        
        assert result["success"] is True
        assert result["items_quantized"] == 2
        assert result["strength"] == 0.5
        assert result["grid_division"] == 0.25
    
    @patch('server.tools.groove_quantization.ReaperBridge.send_request')
    @patch('server.tools.groove_quantization.random.uniform')
    def test_humanize_items_sync(self, mock_random, mock_send):
        """Test humanizing with mock."""
        from server.tools.groove_quantization import humanize_items
        
        # Mock random values
        mock_random.side_effect = [0.01, -0.005, 0.008]
        
        # Mock responses
        mock_send.side_effect = [
            {"result": True, "count": 3},  # CountSelectedMediaItems
            {"result": True, "item": "item1"},  # GetSelectedMediaItem
            {"result": True, "value": 0.0},  # GetMediaItemInfo_Value
            {"result": True},  # SetMediaItemInfo_Value
            {"result": True, "take": "take1"},  # GetActiveTake
            {"result": True},  # TakeIsMIDI
            {"result": True},  # Main_OnCommand (humanize)
            {"result": True, "item": "item2"},  # GetSelectedMediaItem
            {"result": True, "value": 1.0},  # GetMediaItemInfo_Value
            {"result": True},  # SetMediaItemInfo_Value
            {"result": True, "take": "take2"},  # GetActiveTake
            {"result": True},  # TakeIsMIDI
            {"result": True},  # Main_OnCommand (humanize)
            {"result": True, "item": "item3"},  # GetSelectedMediaItem
            {"result": True, "value": 2.0},  # GetMediaItemInfo_Value
            {"result": True},  # SetMediaItemInfo_Value
            {"result": True, "take": "take3"},  # GetActiveTake
            {"result": True},  # TakeIsMIDI
            {"result": True},  # Main_OnCommand (humanize)
        ]
        
        result = humanize_items(position_amount=0.02, velocity_amount=10, timing_mode="random")
        
        assert result["success"] is True
        assert result["items_humanized"] == 3
        assert result["timing_mode"] == "random"