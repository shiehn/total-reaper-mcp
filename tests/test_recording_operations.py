"""Test cases for recording operations"""

import pytest
from .conftest import call_tool, reaper_available


@pytest.mark.integration
@pytest.mark.skipif(not reaper_available(), reason="REAPER not available")
class TestRecordingOperations:
    """Test recording-related operations"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, mock_project):
        """Ensure clean state for each test"""
        pass
    
    def test_get_set_track_record_mode(self, mock_project):
        """Test getting and setting track record mode"""
        # Create a track
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        # Get default record mode
        result = call_tool("get_track_record_mode", {"track_index": 0})
        assert result["success"]
        assert "record mode:" in result["result"]
        
        # Set to stereo out mode
        result = call_tool("set_track_record_mode", {"track_index": 0, "mode": 1})
        assert result["success"]
        assert "Stereo out" in result["result"]
        
        # Verify it was set
        result = call_tool("get_track_record_mode", {"track_index": 0})
        assert result["success"]
        assert "Stereo out" in result["result"]
        
        # Set to MIDI overdub mode
        result = call_tool("set_track_record_mode", {"track_index": 0, "mode": 7})
        assert result["success"]
        assert "MIDI overdub" in result["result"]
        
        # Set back to input mode
        result = call_tool("set_track_record_mode", {"track_index": 0, "mode": 0})
        assert result["success"]
        assert "Input" in result["result"]
    
    def test_get_set_track_record_input(self, mock_project):
        """Test getting and setting track record input"""
        # Create a track
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        # Get default record input
        result = call_tool("get_track_record_input", {"track_index": 0})
        assert result["success"]
        assert "record input:" in result["result"]
        
        # Set to none
        result = call_tool("set_track_record_input", {"track_index": 0, "input": -1})
        assert result["success"]
        assert "None" in result["result"]
        
        # Set to mono hardware input 1
        result = call_tool("set_track_record_input", {"track_index": 0, "input": 0})
        assert result["success"]
        assert "Mono hardware input 1" in result["result"]
        
        # Set to stereo hardware input pair 1
        result = call_tool("set_track_record_input", {"track_index": 0, "input": 512})
        assert result["success"]
        assert "Stereo hardware input pair 1" in result["result"]
        
        # Set to ReaRoute/loopback
        result = call_tool("set_track_record_input", {"track_index": 0, "input": 1024})
        assert result["success"]
        assert "ReaRoute/loopback" in result["result"]
    
    def test_get_set_track_record_arm(self, mock_project):
        """Test getting and setting track record arm state"""
        # Create a track
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        # Get default arm state (should be not armed)
        result = call_tool("get_track_record_arm", {"track_index": 0})
        assert result["success"]
        assert "Not armed" in result["result"]
        
        # Arm the track
        result = call_tool("set_track_record_arm", {"track_index": 0, "armed": True})
        assert result["success"]
        assert "Armed" in result["result"]
        
        # Verify it's armed
        result = call_tool("get_track_record_arm", {"track_index": 0})
        assert result["success"]
        assert "Armed" in result["result"]
        assert "Not armed" not in result["result"]
        
        # Disarm the track
        result = call_tool("set_track_record_arm", {"track_index": 0, "armed": False})
        assert result["success"]
        assert "Disarmed" in result["result"]
        
        # Verify it's disarmed
        result = call_tool("get_track_record_arm", {"track_index": 0})
        assert result["success"]
        assert "Not armed" in result["result"]
    
    def test_multiple_track_recording_setup(self, mock_project):
        """Test setting up multiple tracks for recording"""
        # Create multiple tracks
        for i in range(3):
            result = call_tool("insert_track", {"index": i})
            assert result["success"]
        
        # Set up track 0 for stereo recording
        result = call_tool("set_track_record_mode", {"track_index": 0, "mode": 1})
        assert result["success"]
        result = call_tool("set_track_record_input", {"track_index": 0, "input": 512})
        assert result["success"]
        result = call_tool("set_track_record_arm", {"track_index": 0, "armed": True})
        assert result["success"]
        
        # Set up track 1 for MIDI recording
        result = call_tool("set_track_record_mode", {"track_index": 1, "mode": 7})
        assert result["success"]
        result = call_tool("set_track_record_arm", {"track_index": 1, "armed": True})
        assert result["success"]
        
        # Track 2 remains unarmed
        result = call_tool("get_track_record_arm", {"track_index": 2})
        assert result["success"]
        assert "Not armed" in result["result"]
    
    def test_invalid_track_recording_operations(self, mock_project):
        """Test error handling for invalid tracks"""
        # Try to get record mode from non-existent track
        result = call_tool("get_track_record_mode", {"track_index": 999})
        assert not result["success"]
        
        # Try to set record mode on non-existent track
        result = call_tool("set_track_record_mode", {"track_index": 999, "mode": 0})
        assert not result["success"]
        
        # Try to get record input from non-existent track
        result = call_tool("get_track_record_input", {"track_index": 999})
        assert not result["success"]
        
        # Try to arm non-existent track
        result = call_tool("set_track_record_arm", {"track_index": 999, "armed": True})
        assert not result["success"]