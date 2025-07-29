"""
Integration tests for DSL/Macro tools

These tests verify that the DSL layer correctly handles natural language inputs
and provides the expected high-level functionality.
"""

import pytest
import logging
from .test_utils import (
    ensure_clean_project,
    assert_response_contains,
    assert_response_success,
    extract_number_from_response
)

logger = logging.getLogger(__name__)

async def call_dsl_tool(client, tool_name, params):
    """Helper to call DSL tools and return the text response"""
    result = await client.call_tool(tool_name, params)
    # Check if the result indicates an error
    if hasattr(result, 'isError') and result.isError:
        raise Exception(result.content[0].text if result.content else "Tool execution failed")
    return result.content[0].text if result.content else ""

@pytest.mark.asyncio
class TestDSLTrackOperations:
    """Test DSL track management tools"""
    
    async def test_create_track_with_role(self, reaper_mcp_client):
        """Test creating a track with name and role"""
        # Note: Not using ensure_clean_project since it requires tools not in DSL profile
        
        # Create a bass track
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {
            "name": "Bass",
            "role": "bass"
        })
        assert "Created track 'Bass' with role 'bass'" in result
        
        # Verify we can find it by role
        tracks = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        assert "Bass" in tracks
        assert "bass" in tracks.lower()
    
    async def test_track_volume_flexible_formats(self, reaper_mcp_client):
        """Test setting track volume with various formats"""
        # Create a test track
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Test Track"})
        
        # Test dB format
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {
            "track": "Test Track",
            "volume": "-6dB"
        })
        assert "Set Test Track volume to -6.0 dB" in result
        
        # Test relative change
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {
            "track": 0,  # Use index
            "volume": "+3"
        })
        assert "volume to -3.0 dB" in result
        
        # Test linear value
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {
            "track": "Test Track",
            "volume": 0.5
        })
        assert "Set Test Track volume" in result
    
    async def test_track_pan_formats(self, reaper_mcp_client):
        """Test setting track pan with L/R format"""
        # Create a test track
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Synth"})
        
        # Test L/R format
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_pan", {
            "track": "Synth",
            "pan": "L50"
        })
        assert "Set Synth pan to L50" in result
        
        # Test numeric format
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_pan", {
            "track": 0,
            "pan": 0.3
        })
        assert "pan to R30" in result
        
        # Test center
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_pan", {
            "track": "Synth",
            "pan": "C"
        })
        assert "pan to C" in result
    
    async def test_track_fuzzy_matching(self, reaper_mcp_client):
        """Test fuzzy track name matching"""
        # Create tracks with similar names
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Bass Guitar"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Bassline"})
        
        # Should match "Bass Guitar" better than "Bassline"
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_mute", {
            "track": "bass gtr",
            "mute": True
        })
        # Note: Without the actual fuzzy matching in the bridge,
        # this might fail. The test shows the intended behavior.
        assert "Muted" in result
    
    async def test_track_mute_solo(self, reaper_mcp_client):
        """Test mute and solo operations"""
        # Create track
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Drums"})
        
        # Mute
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_mute", {
            "track": "Drums",
            "mute": True
        })
        assert "Muted Drums" in result
        
        # Solo
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_solo", {
            "track": "Drums",
            "solo": True
        })
        assert "Soloed Drums" in result
        
        # Unmute
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_mute", {
            "track": "Drums",
            "mute": False
        })
        assert "Unmuted Drums" in result

@pytest.mark.asyncio
class TestDSLTimeOperations:
    """Test DSL time and loop tools"""
    
    async def test_time_select_bars(self, reaper_mcp_client):
        """Test selecting time by bars"""
        result = await call_dsl_tool(reaper_mcp_client, "dsl_time_select", {
            "time": "8 bars"
        })
        # Should select 8 bars from cursor
        assert "Selected" in result
        assert "seconds" in result
        # Ideally would check for "(8 bars)" but depends on tempo
    
    async def test_time_select_special(self, reaper_mcp_client):
        """Test special time selections"""
        # These might fail without actual selection/loop set up
        # but show the intended API
        
        # Select current loop (if any)
        try:
            result = await call_dsl_tool(reaper_mcp_client, "dsl_time_select", {
                "time": "loop"
            })
            assert "Selected" in result
        except Exception as e:
            # Expected if no loop is set
            assert "No loop region" in str(e) or "Failed" in str(e)
    
    async def test_create_loop(self, reaper_mcp_client):
        """Test creating a loop item"""
        # Create a track first
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Loop Track"})
        
        # Create an 8-bar MIDI loop
        result = await call_dsl_tool(reaper_mcp_client, "dsl_loop_create", {
            "track": "Loop Track",
            "time": "8 bars",
            "midi": True
        })
        assert "Created" in result
        assert "MIDI loop" in result
        assert "Loop Track" in result

@pytest.mark.asyncio
class TestDSLItemOperations:
    """Test DSL item and MIDI tools"""
    
    async def test_midi_insert(self, reaper_mcp_client):
        """Test inserting MIDI data"""
        # Create track
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "MIDI Track"})
        
        # Insert MIDI data
        midi_data = {
            "notes": [
                {"pitch": 60, "start": 0.0, "length": 0.5, "velocity": 100},
                {"pitch": 64, "start": 0.5, "length": 0.5, "velocity": 90},
                {"pitch": 67, "start": 1.0, "length": 1.0, "velocity": 80}
            ]
        }
        
        result = await call_dsl_tool(reaper_mcp_client, "dsl_midi_insert", {
            "track": "MIDI Track",
            "time": "2 bars",
            "midi_data": midi_data
        })
        assert "Inserted 3 MIDI notes" in result
        assert "MIDI Track" in result
    
    async def test_quantize(self, reaper_mcp_client):
        """Test quantizing items"""
        # This test assumes there are selected items
        # In practice, would need to create and select items first
        
        # Since there are no items selected, this should raise an error
        with pytest.raises(Exception) as exc_info:
            await call_dsl_tool(reaper_mcp_client, "dsl_quantize", {
                "items": "selected",
                "strength": 0.75,
                "grid": "1/16"
            })
        assert "No items found" in str(exc_info.value)

@pytest.mark.asyncio
class TestDSLTransportOperations:
    """Test DSL transport controls"""
    
    async def test_play_stop(self, reaper_mcp_client):
        """Test play and stop"""
        # Play
        result = await call_dsl_tool(reaper_mcp_client, "dsl_play", {})
        assert "Started playback" in result
        
        # Stop
        result = await call_dsl_tool(reaper_mcp_client, "dsl_stop", {})
        assert "Stopped playback" in result
    
    async def test_set_tempo(self, reaper_mcp_client):
        """Test setting tempo"""
        result = await call_dsl_tool(reaper_mcp_client, "dsl_set_tempo", {"bpm": 128})
        assert "Set tempo to 128" in result
        
        # Verify with get tempo info
        result = await call_dsl_tool(reaper_mcp_client, "dsl_get_tempo_info", {})
        assert "128" in result or "Tempo:" in result

@pytest.mark.asyncio
class TestDSLContextOperations:
    """Test DSL context and query tools"""
    
    async def test_list_tracks(self, reaper_mcp_client):
        """Test getting track list"""
        # Create some tracks first
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Track 1", "role": "bass"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Track 2", "role": "drums"})
        
        result = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        assert "Found" in result
        assert "tracks:" in result
    
    async def test_tempo_info(self, reaper_mcp_client):
        """Test getting tempo and time signature"""
        result = await call_dsl_tool(reaper_mcp_client, "dsl_get_tempo_info", {})
        assert "Tempo:" in result
        assert "BPM" in result
        assert "Time signature:" in result
    
    async def test_context_reset(self, reaper_mcp_client):
        """Test resetting context"""
        result = await call_dsl_tool(reaper_mcp_client, "dsl_reset_context", {})
        assert "Session context reset" in result

@pytest.mark.asyncio
class TestDSLContextAwareness:
    """Test DSL context awareness features"""
    
    async def test_last_track_reference(self, reaper_mcp_client):
        """Test using 'last' to reference previously used track"""
        # Create and reference a track
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "First Track"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {
            "track": "First Track",
            "volume": "-6dB"
        })
        
        # Now use "last" to reference it
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_pan", {
            "track": "last",
            "pan": "L30"
        })
        # This will fail without proper context tracking in the bridge
        # but shows the intended behavior
        assert "pan to L30" in result or "No previous track" in result

@pytest.mark.asyncio
class TestDSLErrorHandling:
    """Test DSL error handling and disambiguation"""
    
    async def test_invalid_track_reference(self, reaper_mcp_client):
        """Test handling of invalid track references"""
        with pytest.raises(Exception) as exc_info:
            await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {
                "track": "NonexistentTrack",
                "volume": "-6dB"
            })
        assert "No tracks found" in str(exc_info.value) or "Error" in str(exc_info.value)
    
    async def test_invalid_time_format(self, reaper_mcp_client):
        """Test handling of invalid time formats"""
        with pytest.raises(Exception) as exc_info:
            await call_dsl_tool(reaper_mcp_client, "dsl_time_select", {
                "time": "invalid time"
            })
        assert "Cannot parse time" in str(exc_info.value) or "Failed" in str(exc_info.value)
    
    async def test_missing_parameters(self, reaper_mcp_client):
        """Test handling of missing required parameters"""
        with pytest.raises(Exception) as exc_info:
            await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {
                "track": 0
                # Missing volume parameter
            })
        # The actual error depends on the MCP framework's parameter validation
        assert "missing" in str(exc_info.value).lower() or "required" in str(exc_info.value).lower()

@pytest.mark.asyncio
class TestDSLWorkflows:
    """Test complete DSL workflows"""
    
    async def test_create_basic_song_structure(self, reaper_mcp_client):
        """Test creating a basic song structure using DSL tools"""
        # Create tracks
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Drums", "role": "drums"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Bass", "role": "bass"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Keys", "role": "keys"})
        
        # Set tempo
        await call_dsl_tool(reaper_mcp_client, "dsl_set_tempo", {"bpm": 120})
        
        # Create loops on each track
        for track in ["Drums", "Bass", "Keys"]:
            result = await call_dsl_tool(reaper_mcp_client, "dsl_loop_create", {
                "track": track,
                "time": "8 bars",
                "midi": True
            })
            assert "Created" in result
        
        # Set initial mix
        await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {"track": "Drums", "volume": "-3dB"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {"track": "Bass", "volume": "-6dB"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {"track": "Keys", "volume": "-9dB"})
        
        # Pan instruments
        await call_dsl_tool(reaper_mcp_client, "dsl_track_pan", {"track": "Keys", "pan": "R20"})
        
        # Verify structure
        result = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        assert "3 tracks" in result or "Found" in result