"""Tests for bus routing and mixing workflow tools."""

import pytest
from unittest.mock import patch, MagicMock


class TestBusRouting:
    """Test bus routing and mixing functions."""
    
    @pytest.mark.asyncio
    async def test_create_bus_track(self, reaper_mcp_client):
        """Test creating a bus track."""
        result = await reaper_mcp_client.call_tool("create_bus_track", {
            "name": "Test Bus",
            "num_channels": 2,
            "color": 0xFF0000  # Red
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("name") == "Test Bus"
        assert result.get("num_channels") == 2
        assert "track_index" in result
    
    @pytest.mark.asyncio
    async def test_route_tracks_to_bus(self, reaper_mcp_client):
        """Test routing multiple tracks to a bus."""
        # Create source tracks
        source_indices = []
        for i in range(3):
            track_result = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": f"Source {i+1}"
            })
            source_indices.append(track_result.get("track_index"))
        
        # Create bus
        bus_result = await reaper_mcp_client.call_tool("create_bus_track", {
            "name": "Mix Bus"
        })
        bus_index = bus_result.get("track_index")
        
        # Route tracks to bus
        result = await reaper_mcp_client.call_tool("route_tracks_to_bus", {
            "source_track_indices": source_indices,
            "bus_track_index": bus_index,
            "send_mode": "post-fader",
            "send_level_db": -6.0
        })
        
        assert result
        assert result.get("success") is True
        assert len(result.get("routed_tracks", [])) == 3
        assert result.get("send_mode") == "post-fader"
    
    @pytest.mark.asyncio
    async def test_create_parallel_compression_bus(self, reaper_mcp_client):
        """Test creating parallel compression setup."""
        # Create drum tracks
        drum_indices = []
        for i, name in enumerate(["Kick", "Snare", "HiHat"]):
            track_result = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": name
            })
            drum_indices.append(track_result.get("track_index"))
        
        # Create parallel compression
        result = await reaper_mcp_client.call_tool("create_parallel_compression_bus", {
            "source_track_indices": drum_indices,
            "bus_name": "Drum Crush",
            "blend_amount_db": -10.0
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("bus_name") == "Drum Crush"
        assert result.get("source_tracks") == drum_indices
        assert "compressor_added" in result
    
    @pytest.mark.asyncio
    async def test_create_reverb_send_bus(self, reaper_mcp_client):
        """Test creating reverb send bus."""
        result = await reaper_mcp_client.call_tool("create_reverb_send_bus", {
            "reverb_type": "hall",
            "return_level_db": -12.0
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("reverb_type") == "hall"
        assert result.get("return_level_db") == -12.0
        assert "reverb_added" in result
    
    @pytest.mark.asyncio
    async def test_create_stem_buses(self, reaper_mcp_client):
        """Test creating stem buses for track groups."""
        # Create tracks for different instrument groups
        track_map = {}
        track_idx = 0
        
        # Drums
        drum_indices = []
        for drum in ["Kick", "Snare", "HiHat", "Toms"]:
            track_result = await reaper_mcp_client.call_tool("insert_track", {
                "index": track_idx,
                "name": drum
            })
            drum_indices.append(track_result.get("track_index"))
            track_idx += 1
        
        # Bass
        bass_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": track_idx,
            "name": "Bass"
        })
        bass_indices = [bass_result.get("track_index")]
        track_idx += 1
        
        # Keys
        keys_indices = []
        for key in ["Piano", "Synth"]:
            track_result = await reaper_mcp_client.call_tool("insert_track", {
                "index": track_idx,
                "name": key
            })
            keys_indices.append(track_result.get("track_index"))
            track_idx += 1
        
        # Create stem buses
        result = await reaper_mcp_client.call_tool("create_stem_buses", {
            "stem_groups": {
                "Drums": drum_indices,
                "Bass": bass_indices,
                "Keys": keys_indices
            }
        })
        
        assert result
        assert result.get("success") is True
        assert len(result.get("stems_created", [])) == 3
        
        # Verify stem names
        stem_names = [s["name"] for s in result.get("stems_created", [])]
        assert "Drums" in stem_names
        assert "Bass" in stem_names
        assert "Keys" in stem_names
    
    @pytest.mark.asyncio
    async def test_create_sidechain_routing(self, reaper_mcp_client):
        """Test creating sidechain routing."""
        # Create source (kick) and destination (bass) tracks
        kick_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Kick"
        })
        kick_index = kick_result.get("track_index")
        
        bass_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 1,
            "name": "Bass"
        })
        bass_index = bass_result.get("track_index")
        
        # Create sidechain routing
        result = await reaper_mcp_client.call_tool("create_sidechain_routing", {
            "source_track_index": kick_index,
            "destination_track_index": bass_index,
            "channel_offset": 2  # Channels 3/4
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("source_track") == kick_index
        assert result.get("destination_track") == bass_index
        assert result.get("sidechain_channels") == "3/4"
    
    @pytest.mark.asyncio
    async def test_setup_monitor_mix(self, reaper_mcp_client):
        """Test setting up monitor mix."""
        # Create performer tracks
        performer_indices = []
        for i, name in enumerate(["Vocals", "Guitar", "Keys"]):
            track_result = await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "name": name
            })
            performer_indices.append(track_result.get("track_index"))
        
        # Create click track
        click_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 3,
            "name": "Click"
        })
        click_index = click_result.get("track_index")
        
        # Setup monitor mix
        result = await reaper_mcp_client.call_tool("setup_monitor_mix", {
            "performer_tracks": performer_indices,
            "click_track_index": click_index,
            "output_channel": 2  # Hardware outputs 3/4
        })
        
        assert result
        assert result.get("success") is True
        assert result.get("performer_tracks") == performer_indices
        assert result.get("click_included") is True
        assert result.get("output_channel") == 3  # 1-based display
    
    @pytest.mark.asyncio
    async def test_create_headphone_cue_mixes(self, reaper_mcp_client):
        """Test creating multiple headphone cue mixes."""
        result = await reaper_mcp_client.call_tool("create_headphone_cue_mixes", {
            "num_mixes": 4
        })
        
        assert result
        assert result.get("success") is True
        assert len(result.get("cue_mixes", [])) == 4
        
        # Verify output assignments
        for i, cue in enumerate(result.get("cue_mixes", [])):
            assert cue["name"] == f"Cue Mix {i+1}"
            expected_outputs = f"{i*2+1}/{i*2+2}"
            assert cue["output_channels"] == expected_outputs
    
    @pytest.mark.asyncio
    async def test_analyze_routing_matrix(self, reaper_mcp_client):
        """Test analyzing routing matrix."""
        # Create a simple routing setup
        track1_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "name": "Source"
        })
        
        track2_result = await reaper_mcp_client.call_tool("insert_track", {
            "index": 1,
            "name": "Bus"
        })
        
        # Create send
        await reaper_mcp_client.call_tool("route_tracks_to_bus", {
            "source_track_indices": [track1_result.get("track_index")],
            "bus_track_index": track2_result.get("track_index")
        })
        
        # Analyze routing
        result = await reaper_mcp_client.call_tool("analyze_routing_matrix", {})
        
        assert result
        assert result.get("success") is True
        assert result.get("track_count") >= 2
        
        routing = result.get("routing", [])
        assert len(routing) >= 2
        
        # Verify source track has send
        source_info = next((t for t in routing if t["name"] == "Source"), None)
        assert source_info
        assert source_info["num_sends"] > 0
        
        # Verify bus track has receive
        bus_info = next((t for t in routing if t["name"] == "Bus"), None)
        assert bus_info
        assert bus_info["num_receives"] > 0


class TestBusRoutingSync:
    """Synchronous tests for bus routing using mocked bridge."""
    
    @patch('server.tools.bus_routing.ReaperBridge.send_request')
    def test_create_bus_track_sync(self, mock_send):
        """Test creating bus track with mock."""
        from server.tools.bus_routing import create_bus_track
        
        # Mock responses
        mock_send.side_effect = [
            {"result": True, "count": 5},  # CountTracks
            {"result": True},  # InsertTrackAtIndex
            {"result": True, "track": "bus_handle"},  # GetTrack
            {"result": True},  # GetSetMediaTrackInfo_String (name)
            {"result": True},  # SetMediaTrackInfo_Value (color)
            {"result": True},  # SetMediaTrackInfo_Value (folder)
        ]
        
        result = create_bus_track("Test Bus", color=0xFF0000)
        
        assert result["success"] is True
        assert result["track_index"] == 5
        assert result["name"] == "Test Bus"
    
    @patch('server.tools.bus_routing.ReaperBridge.send_request')
    def test_route_tracks_to_bus_sync(self, mock_send):
        """Test routing tracks with mock."""
        from server.tools.bus_routing import route_tracks_to_bus
        
        # Mock responses
        mock_send.side_effect = [
            {"result": True, "track": "bus_handle"},  # GetTrack (bus)
            {"result": True, "track": "track1"},  # GetTrack (source 1)
            {"result": True, "send_index": 0},  # CreateTrackSend
            {"result": True},  # SetTrackSendInfo_Value (mode)
            {"result": True},  # SetTrackSendInfo_Value (level)
            {"result": True, "track": "track2"},  # GetTrack (source 2)
            {"result": True, "send_index": 0},  # CreateTrackSend
            {"result": True},  # SetTrackSendInfo_Value (mode)
            {"result": True},  # SetTrackSendInfo_Value (level)
        ]
        
        result = route_tracks_to_bus([0, 1], 2, "post-fader", -6.0)
        
        assert result["success"] is True
        assert len(result["routed_tracks"]) == 2
        assert result["send_mode"] == "post-fader"
    
    @patch('server.tools.bus_routing.ReaperBridge.send_request')
    def test_create_stem_buses_sync(self, mock_send):
        """Test creating stem buses with mock."""
        from server.tools.bus_routing import create_stem_buses
        
        # Mock for creating drum stem
        mock_send.side_effect = [
            {"result": True, "count": 10},  # CountTracks
            {"result": True},  # InsertTrackAtIndex
            {"result": True, "track": "drum_bus"},  # GetTrack
            {"result": True},  # GetSetMediaTrackInfo_String (name)
            {"result": True},  # SetMediaTrackInfo_Value (color)
            {"result": True},  # SetMediaTrackInfo_Value (folder)
            {"result": True, "track": "drum_bus"},  # GetTrack (bus)
            {"result": True, "track": "kick"},  # GetTrack (source 1)
            {"result": True, "send_index": 0},  # CreateTrackSend
            {"result": True},  # SetTrackSendInfo_Value (mode)
            {"result": True, "track": "kick"},  # GetTrack (for master send)
            {"result": True},  # SetMediaTrackInfo_Value (remove master)
            {"result": True, "track": "snare"},  # GetTrack (source 2)
            {"result": True, "send_index": 0},  # CreateTrackSend
            {"result": True},  # SetTrackSendInfo_Value (mode)
            {"result": True, "track": "snare"},  # GetTrack (for master send)
            {"result": True},  # SetMediaTrackInfo_Value (remove master)
        ]
        
        result = create_stem_buses({"Drums": [0, 1]})
        
        assert result["success"] is True
        assert len(result["stems_created"]) == 1
        assert result["stems_created"][0]["name"] == "Drums"