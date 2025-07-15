"""Tests for bounce and render tools."""

import pytest
from unittest.mock import patch, MagicMock


class TestBounceRender:
    """Test bounce and render functions."""
    
    @pytest.mark.asyncio
    async def test_bounce_track_in_place(self, reaper_mcp_client):
        """Test bouncing a track in place."""
        # Create a track first
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Test Track"
        })
        track_index = track_result.get("track_index")
        
        # Add an item to the track
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 0.0,
            "length": 4.0
        })
        
        # Bounce track in place
        result = await reaper_mcp_client.call_tool("bounce_track_in_place", {
            "track_index": track_index,
            "tail_length": 0.5
        })
        
        assert result
        assert result.get("track_index") == track_index
        assert "render_start" in result
        assert "render_end" in result
    
    @pytest.mark.asyncio
    async def test_bounce_tracks_to_stems(self, reaper_mcp_client):
        """Test bouncing multiple tracks to stems."""
        # Create multiple tracks
        track_indices = []
        for i in range(3):
            track_result = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": f"Stem Track {i+1}"
            })
            track_indices.append(track_result.get("track_index"))
            
            # Add item to each track
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": track_result.get("track_index"),
                "position": 0.0,
                "length": 4.0
            })
        
        # Bounce to stems
        result = await reaper_mcp_client.call_tool("bounce_tracks_to_stems", {
            "track_indices": track_indices,
            "output_directory": "/tmp",
            "file_prefix": "test_stem",
            "tail_length": 0.5
        })
        
        assert result
        assert result.get("success") is True
        assert len(result.get("stems_created", [])) > 0
        assert result.get("total_tracks") == 3
    
    @pytest.mark.asyncio
    async def test_freeze_unfreeze_track(self, reaper_mcp_client):
        """Test freezing and unfreezing a track."""
        # Create a track
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Freeze Test Track"
        })
        track_index = track_result.get("track_index")
        
        # Add an item
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 0.0,
            "length": 4.0
        })
        
        # Freeze track
        freeze_result = await reaper_mcp_client.call_tool("freeze_track", {
            "track_index": track_index,
            "freeze_fx": True
        })
        assert freeze_result
        assert freeze_result.get("track_index") == track_index
        assert freeze_result.get("freeze_type") == "full"
        
        # Unfreeze track
        unfreeze_result = await reaper_mcp_client.call_tool("unfreeze_track", {
            "track_index": track_index
        })
        assert unfreeze_result
        assert unfreeze_result.get("track_index") == track_index
    
    @pytest.mark.asyncio
    async def test_render_selected_items_to_new_track(self, reaper_mcp_client):
        """Test rendering selected items to a new track."""
        # Create a track with items
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Source Track"
        })
        track_index = track_result.get("track_index")
        
        # Add multiple items
        for i in range(3):
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": track_index,
                "position": i * 2.0,
                "length": 1.5
            })
        
        # Select all items
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        # Render to new track
        result = await reaper_mcp_client.call_tool("render_selected_items_to_new_track", {
            "normalize": True,
            "tail_length": 0.25
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("items_rendered") == 3
        assert result.get("normalized") is True
    
    @pytest.mark.asyncio
    async def test_glue_selected_items(self, reaper_mcp_client):
        """Test gluing selected items."""
        # Create track with multiple items
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Glue Test Track"
        })
        track_index = track_result.get("track_index")
        
        # Add adjacent items
        for i in range(3):
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": track_index,
                "position": i * 2.0,
                "length": 2.0
            })
        
        # Select all items
        await reaper_mcp_client.call_tool("select_all_items", {})
        
        # Glue items
        result = await reaper_mcp_client.call_tool("glue_selected_items", {})
        
        assert result
        assert result.get("success") is True
        assert result.get("items_glued") == 3
    
    @pytest.mark.asyncio
    async def test_apply_track_fx_to_items(self, reaper_mcp_client):
        """Test applying track FX to items."""
        # Create track
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "FX Test Track"
        })
        track_index = track_result.get("track_index")
        
        # Add items
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_index,
            "position": 0.0,
            "length": 4.0
        })
        
        # Apply track FX to items
        result = await reaper_mcp_client.call_tool("apply_track_fx_to_items", {
            "track_index": track_index,
            "fx_only": False
        })
        
        assert result
        assert result.get("track_index") == track_index
        assert result.get("items_processed") > 0
        assert result.get("fx_only") is False
    
    @pytest.mark.asyncio
    async def test_create_submix_from_tracks(self, reaper_mcp_client):
        """Test creating a submix from multiple tracks."""
        # Create source tracks
        track_indices = []
        for i in range(3):
            track_result = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": f"Source {i+1}"
            })
            track_indices.append(track_result.get("track_index"))
        
        # Create submix
        result = await reaper_mcp_client.call_tool("create_submix_from_tracks", {
            "track_indices": track_indices,
            "submix_name": "Test Submix"
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("submix_name") == "Test Submix"
        assert len(result.get("routed_tracks", [])) == 3
        assert "submix_track_index" in result
    
    @pytest.mark.asyncio
    async def test_render_project_to_file(self, reaper_mcp_client):
        """Test rendering project to file."""
        # Add some content first
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Render Test"
        })
        
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_result.get("track_index"),
            "position": 0.0,
            "length": 4.0
        })
        
        # Render project
        result = await reaper_mcp_client.call_tool("render_project_to_file", {
            "output_path": "/tmp/test_render.wav",
            "render_settings": {
                "sample_rate": 48000,
                "bit_depth": 24,
                "channels": 2
            }
        })
        
        assert result
        assert result.get("output_path") == "/tmp/test_render.wav"
    
    @pytest.mark.asyncio
    async def test_render_time_selection(self, reaper_mcp_client):
        """Test rendering time selection."""
        # Set time selection
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 2.0,
            "end": 6.0
        })
        
        # Add content
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Time Selection Render"
        })
        
        await reaper_mcp_client.call_tool("add_media_item", {
            "track_index": track_result.get("track_index"),
            "position": 0.0,
            "length": 8.0
        })
        
        # Render time selection
        result = await reaper_mcp_client.call_tool("render_time_selection", {
            "output_path": "/tmp/time_selection.wav"
        })
        
        assert result
        assert result.get("render_start") == 2.0
        assert result.get("render_end") == 6.0
        assert result.get("render_length") == 4.0
    
    @pytest.mark.asyncio
    async def test_consolidate_track(self, reaper_mcp_client):
        """Test consolidating track items."""
        # Create track with multiple items
        track_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Consolidate Test"
        })
        track_index = track_result.get("track_index")
        
        # Add multiple items
        for i in range(4):
            await reaper_mcp_client.call_tool("add_media_item", {
                "track_index": track_index,
                "position": i * 1.0,
                "length": 1.0
            })
        
        # Consolidate track
        result = await reaper_mcp_client.call_tool("consolidate_track", {
            "track_index": track_index
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("track_index") == track_index
        assert result.get("items_consolidated") == 4


class TestBounceRenderSync:
    """Synchronous tests for bounce/render using mocked bridge."""
    
    @patch('server.tools.bounce_render.ReaperBridge.send_request')
    def test_bounce_track_in_place_sync(self, mock_send):
        """Test bouncing track with mock."""
        from server.tools.bounce_render import bounce_track_in_place
        
        # Mock responses
        mock_send.side_effect = [
            {"result": True, "track": "track_handle"},  # GetTrack
            {"result": True},  # SetMediaTrackInfo_Value (solo)
            {"result": True, "track": "track_handle"},  # GetTrack for bounds
            {"result": True, "count": 2},  # CountTrackMediaItems
            {"result": True, "item": "item1"},  # GetTrackMediaItem
            {"result": True, "value": 0.0},  # GetMediaItemInfo_Value (position)
            {"result": True, "value": 2.0},  # GetMediaItemInfo_Value (length)
            {"result": True, "item": "item2"},  # GetTrackMediaItem
            {"result": True, "value": 2.0},  # GetMediaItemInfo_Value (position)
            {"result": True, "value": 2.0},  # GetMediaItemInfo_Value (length)
            {"result": True},  # GetSet_LoopTimeRange
            {"result": True},  # Main_OnCommand (render)
            {"result": True},  # SetMediaTrackInfo_Value (unsolo)
        ]
        
        result = bounce_track_in_place(track_index=0, tail_length=0.5)
        
        assert result["success"] is True
        assert result["track_index"] == 0
        assert result["render_start"] == 0.0
        assert result["render_end"] == 4.5  # 4.0 + 0.5 tail
    
    @patch('server.tools.bounce_render.ReaperBridge.send_request')
    def test_freeze_track_sync(self, mock_send):
        """Test freezing track with mock."""
        from server.tools.bounce_render import freeze_track
        
        mock_send.side_effect = [
            {"result": True, "track": "track_handle"},  # GetTrack
            {"result": True},  # SetMediaTrackInfo_Value (select)
            {"result": True},  # Main_OnCommand (freeze)
            {"result": True},  # SetMediaTrackInfo_Value (deselect)
        ]
        
        result = freeze_track(track_index=0, freeze_fx=True)
        
        assert result["success"] is True
        assert result["track_index"] == 0
        assert result["freeze_type"] == "full"
    
    @patch('server.tools.bounce_render.ReaperBridge.send_request')
    def test_create_submix_sync(self, mock_send):
        """Test creating submix with mock."""
        from server.tools.bounce_render import create_submix_from_tracks
        
        mock_send.side_effect = [
            {"result": True, "count": 3},  # CountTracks
            {"result": True},  # InsertTrackAtIndex
            {"result": True, "track": "submix_handle"},  # GetTrack (submix)
            {"result": True},  # GetSetMediaTrackInfo_String (name)
            {"result": True, "track": "track1"},  # GetTrack (source 1)
            {"result": True},  # CreateTrackSend
            {"result": True},  # SetMediaTrackInfo_Value (remove master send)
            {"result": True, "track": "track2"},  # GetTrack (source 2)
            {"result": True},  # CreateTrackSend
            {"result": True},  # SetMediaTrackInfo_Value (remove master send)
        ]
        
        result = create_submix_from_tracks([0, 1], "Test Bus")
        
        assert result["success"] is True
        assert result["submix_track_index"] == 3
        assert result["submix_name"] == "Test Bus"
        assert result["routed_tracks"] == [0, 1]