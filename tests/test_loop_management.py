"""Tests for loop and time selection management tools."""

import pytest
from unittest.mock import patch, MagicMock


class TestLoopManagement:
    """Test loop and time selection management functions."""
    
    @pytest.mark.asyncio
    async def test_get_time_selection(self, reaper_mcp_client):
        """Test getting time selection."""
        result = await reaper_mcp_client.call_tool("get_time_selection", {})
        assert result
        assert "start" in result
        assert "end" in result
        assert "length" in result
        assert "is_set" in result
    
    @pytest.mark.asyncio
    async def test_set_time_selection(self, reaper_mcp_client):
        """Test setting time selection."""
        result = await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 1.0,
            "end": 5.0
        })
        assert result
        assert result.get("start") == 1.0
        assert result.get("end") == 5.0
        
        # Verify it was set
        get_result = await reaper_mcp_client.call_tool("get_time_selection", {})
        assert get_result.get("start") == 1.0
        assert get_result.get("end") == 5.0
        assert get_result.get("is_set") is True
    
    @pytest.mark.asyncio
    async def test_clear_time_selection(self, reaper_mcp_client):
        """Test clearing time selection."""
        # First set a selection
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 1.0,
            "end": 5.0
        })
        
        # Clear it
        result = await reaper_mcp_client.call_tool("clear_time_selection", {})
        assert result
        
        # Verify it was cleared
        get_result = await reaper_mcp_client.call_tool("get_time_selection", {})
        assert get_result.get("is_set") is False
    
    @pytest.mark.asyncio
    async def test_get_loop_points(self, reaper_mcp_client):
        """Test getting loop points."""
        result = await reaper_mcp_client.call_tool("get_loop_points", {})
        assert result
        assert "enabled" in result
        assert "start" in result
        assert "end" in result
        assert "length" in result
    
    @pytest.mark.asyncio
    async def test_set_loop_enabled(self, reaper_mcp_client):
        """Test enabling/disabling looping."""
        # Enable looping
        result = await reaper_mcp_client.call_tool("set_loop_enabled", {
            "enabled": True
        })
        assert result
        assert result.get("enabled") is True
        
        # Disable looping
        result = await reaper_mcp_client.call_tool("set_loop_enabled", {
            "enabled": False
        })
        assert result
        assert result.get("enabled") is False
    
    @pytest.mark.asyncio
    async def test_set_loop_points(self, reaper_mcp_client):
        """Test setting loop points."""
        result = await reaper_mcp_client.call_tool("set_loop_points", {
            "start": 2.0,
            "end": 6.0,
            "enable": True
        })
        assert result
        assert result.get("start") == 2.0
        assert result.get("end") == 6.0
        assert result.get("loop_enabled") is True
    
    @pytest.mark.asyncio
    async def test_duplicate_time_selection(self, reaper_mcp_client):
        """Test duplicating time selection contents."""
        # First create some content in time selection
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 0.0,
            "end": 4.0
        })
        
        # Create a track and add an item
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Test Track"
        })
        track_index = track_result.get("track_index")
        
        item_result = await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 0.0,
            "length": 4.0
        })
        
        # Duplicate the time selection
        result = await reaper_mcp_client.call_tool("duplicate_time_selection", {
            "count": 2
        })
        assert result
        assert result.get("success") is True
        assert result.get("duplications") == 2
    
    @pytest.mark.asyncio
    async def test_shift_time_selection(self, reaper_mcp_client):
        """Test shifting time selection."""
        # Set initial selection
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 2.0,
            "end": 6.0
        })
        
        # Shift forward
        result = await reaper_mcp_client.call_tool("shift_time_selection", {
            "offset": 2.0
        })
        assert result
        assert result.get("success") is True
        
        # Verify shift
        get_result = await reaper_mcp_client.call_tool("get_time_selection", {})
        assert get_result.get("start") == 4.0
        assert get_result.get("end") == 8.0
        
        # Shift backward
        result = await reaper_mcp_client.call_tool("shift_time_selection", {
            "offset": -3.0
        })
        assert result
        
        get_result = await reaper_mcp_client.call_tool("get_time_selection", {})
        assert get_result.get("start") == 1.0
        assert get_result.get("end") == 5.0
    
    @pytest.mark.asyncio
    async def test_create_loop_from_items(self, reaper_mcp_client):
        """Test creating loop from selected items."""
        # Create a track
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Test Track"
        })
        track_index = track_result.get("track_index")
        
        # Add items
        item1 = await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 2.0,
            "length": 2.0
        })
        
        item2 = await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 6.0,
            "length": 2.0
        })
        
        # Select all items
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        # Create loop from items
        result = await reaper_mcp_client.call_tool("create_loop_from_items", {})
        assert result
        assert result.get("success") is True
        
        # Verify loop bounds
        get_result = await reaper_mcp_client.call_tool("get_time_selection", {})
        assert get_result.get("start") == 2.0
        assert get_result.get("end") == 8.0
    
    @pytest.mark.asyncio
    async def test_split_items_at_loop_points(self, reaper_mcp_client):
        """Test splitting items at loop boundaries."""
        # Set time selection
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 2.0,
            "end": 6.0
        })
        
        # Create a track with an item that spans the loop
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Test Track"
        })
        track_index = track_result.get("track_index")
        
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 0.0,
            "length": 8.0
        })
        
        # Split at loop points
        result = await reaper_mcp_client.call_tool("split_items_at_loop_points", {})
        assert result
        assert result.get("split_at_start") == 2.0
        assert result.get("split_at_end") == 6.0
    
    @pytest.mark.asyncio
    async def test_grid_division(self, reaper_mcp_client):
        """Test grid division settings."""
        # Get current grid
        result = await reaper_mcp_client.call_tool("get_grid_division", {})
        assert result
        assert "division" in result
        assert "swing" in result
        
        # Set new grid division
        result = await reaper_mcp_client.call_tool("set_grid_division", {
            "division": 0.125,  # 1/8 note
            "swing": 0.15
        })
        assert result
        assert result.get("success") is True
        assert result.get("division") == 0.125
        assert result.get("swing") == 0.15
    
    @pytest.mark.asyncio
    async def test_quantize_time_selection(self, reaper_mcp_client):
        """Test quantizing items in time selection."""
        # Set time selection
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 0.0,
            "end": 4.0
        })
        
        # Create items slightly off grid
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Test Track"
        })
        track_index = track_result.get("track_index")
        
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 0.1,  # Slightly off grid
            "length": 0.5
        })
        
        # Quantize
        result = await reaper_mcp_client.call_tool("quantize_time_selection", {
            "strength": 1.0
        })
        assert result
        assert result.get("success") is True
    
    @pytest.mark.asyncio
    async def test_crop_to_time_selection(self, reaper_mcp_client):
        """Test cropping project to time selection."""
        # Set time selection
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 4.0,
            "end": 8.0
        })
        
        # Crop project
        result = await reaper_mcp_client.call_tool("crop_to_time_selection", {})
        assert result
        assert result.get("success") is True
    
    @pytest.mark.asyncio
    async def test_insert_time_at_loop_start(self, reaper_mcp_client):
        """Test inserting time at loop start."""
        # Set time selection
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 4.0,
            "end": 8.0
        })
        
        # Insert 2 seconds at loop start
        result = await reaper_mcp_client.call_tool("insert_time_at_loop_start", {
            "length": 2.0
        })
        assert result
        assert result.get("success") is True
        assert result.get("inserted_at") == 4.0
        assert result.get("inserted_length") == 2.0
        
        # Verify time selection shifted
        get_result = await reaper_mcp_client.call_tool("get_time_selection", {})
        assert get_result.get("start") == 6.0
        assert get_result.get("end") == 10.0
    
    @pytest.mark.asyncio
    async def test_remove_time_selection(self, reaper_mcp_client):
        """Test removing time selection contents."""
        # Set time selection
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 2.0,
            "end": 4.0
        })
        
        # Create items
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Test Track"
        })
        track_index = track_result.get("track_index")
        
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 0.0,
            "length": 6.0
        })
        
        # Remove time selection
        result = await reaper_mcp_client.call_tool("remove_time_selection", {})
        assert result
        assert result.get("success") is True


class TestLoopManagementSync:
    """Synchronous tests for loop management using mocked bridge."""
    
    @patch('server.tools.loop_management.ReaperBridge.send_request')
    def test_get_time_selection_sync(self, mock_send):
        """Test getting time selection with mock."""
        from server.tools.loop_management import get_time_selection
        
        mock_send.return_value = {
            "result": True,
            "startOut": 2.0,
            "endOut": 6.0
        }
        
        result = get_time_selection()
        
        assert result["start"] == 2.0
        assert result["end"] == 6.0
        assert result["length"] == 4.0
        assert result["is_set"] is True
    
    @patch('server.tools.loop_management.ReaperBridge.send_request')
    def test_set_loop_points_sync(self, mock_send):
        """Test setting loop points with mock."""
        from server.tools.loop_management import set_loop_points
        
        mock_send.side_effect = [
            {"result": True},  # set_time_selection
            {"result": True}   # set_loop_enabled
        ]
        
        result = set_loop_points(1.0, 5.0, enable=True)
        
        assert result["success"] is True
        assert result["start"] == 1.0
        assert result["end"] == 5.0
        assert "loop_enabled" in result
    
    @patch('server.tools.loop_management.ReaperBridge.send_request')
    def test_duplicate_time_selection_sync(self, mock_send):
        """Test duplicating time selection with mock."""
        from server.tools.loop_management import duplicate_time_selection
        
        # First call gets time selection
        mock_send.side_effect = [
            {"result": True, "startOut": 0.0, "endOut": 4.0},  # get_time_selection
            {"result": True},  # duplicate command 1
            {"result": True}   # duplicate command 2
        ]
        
        result = duplicate_time_selection(count=2)
        
        assert result["success"] is True
        assert result["duplications"] == 2
        assert result["original_start"] == 0.0
        assert result["original_end"] == 4.0