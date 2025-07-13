"""Test cases for audio peak analysis operations"""

import pytest
from .conftest import call_tool, reaper_available


@pytest.mark.integration
@pytest.mark.skipif(not reaper_available(), reason="REAPER not available")
class TestPeakAnalysis:
    """Test audio peak analysis operations"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, mock_project):
        """Ensure clean state for each test"""
        pass
    
    def test_get_track_peak(self, mock_project):
        """Test getting track peak level"""
        # Create a test track
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        # Get peak level for channel 0
        result = call_tool("get_track_peak", {"track_index": 0, "channel": 0})
        assert result["success"]
        assert "peak" in result["result"]
        assert "dB" in result["result"]
        
        # Get peak level for channel 1
        result = call_tool("get_track_peak", {"track_index": 0, "channel": 1})
        assert result["success"]
    
    def test_get_master_track_peak(self, mock_project):
        """Test getting master track peak level"""
        # Get master track peak
        result = call_tool("get_track_peak", {"track_index": -1, "channel": 0})
        assert result["success"]
        assert "peak" in result["result"]
        assert "dB" in result["result"]
    
    def test_get_track_peak_info(self, mock_project):
        """Test getting detailed track peak info"""
        # Create a test track
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        # Get peak info
        result = call_tool("get_track_peak_info", {"track_index": 0})
        assert result["success"]
        assert "Left:" in result["result"]
        assert "Right:" in result["result"]
        assert "dB" in result["result"]
    
    def test_get_media_item_peak(self, mock_project):
        """Test getting media item peak value"""
        # Create track and add media item
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        result = call_tool("add_media_item_to_track", {"track_index": 0})
        assert result["success"]
        
        # Get media item peak
        result = call_tool("get_media_item_peak", {"item_index": 0})
        assert result["success"]
        assert "peak" in result["result"]
        assert "dB" in result["result"]
    
    def test_invalid_track_peak(self, mock_project):
        """Test getting peak from invalid track"""
        # Try to get peak from non-existent track
        result = call_tool("get_track_peak", {"track_index": 999, "channel": 0})
        assert not result["success"]
        assert "error" in result
    
    def test_invalid_item_peak(self, mock_project):
        """Test getting peak from invalid media item"""
        # Try to get peak from non-existent item
        result = call_tool("get_media_item_peak", {"item_index": 999})
        assert not result["success"]
        assert "error" in result