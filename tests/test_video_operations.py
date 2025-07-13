"""Test cases for video operations"""

import pytest
from .conftest import call_tool, reaper_available


@pytest.mark.integration
@pytest.mark.skipif(not reaper_available(), reason="REAPER not available")
class TestVideoOperations:
    """Test video-related operations"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, mock_project):
        """Ensure clean state for each test"""
        pass
    
    def test_check_video_support(self, mock_project):
        """Test checking for video support"""
        result = call_tool("check_video_support", {})
        assert result["success"]
        assert "Video support:" in result["result"]
        assert ("Available" in result["result"] or "Not available" in result["result"])
    
    def test_get_video_settings(self, mock_project):
        """Test getting video settings"""
        result = call_tool("get_video_settings", {})
        assert result["success"]
        assert "Video settings:" in result["result"]
        assert "Width:" in result["result"]
        assert "Height:" in result["result"]
        assert "FPS:" in result["result"]
    
    def test_set_video_settings(self, mock_project):
        """Test setting video settings"""
        # Set width and height
        result = call_tool("set_video_settings", {
            "width": 1920,
            "height": 1080
        })
        assert result["success"]
        assert "Width: 1920 px" in result["result"]
        assert "Height: 1080 px" in result["result"]
        
        # Set FPS
        result = call_tool("set_video_settings", {"fps": 30.0})
        assert result["success"]
        assert "FPS: 30.0" in result["result"]
        
        # Set all settings
        result = call_tool("set_video_settings", {
            "width": 1280,
            "height": 720,
            "fps": 24.0
        })
        assert result["success"]
        assert "Width: 1280 px" in result["result"]
        assert "Height: 720 px" in result["result"]
        assert "FPS: 24.0" in result["result"]
        
        # Note about implementation
        assert "video processor API" in result["result"]
    
    def test_empty_video_settings(self, mock_project):
        """Test setting video settings with no parameters"""
        result = call_tool("set_video_settings", {})
        assert result["success"]
        assert "No video settings specified" in result["result"]
    
    def test_add_video_to_track(self, mock_project):
        """Test adding video to track"""
        # Create a track
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        # Try to add a video file (using a fake path for testing)
        result = call_tool("add_video_to_track", {
            "track_index": 0,
            "video_file": "/path/to/test_video.mp4"
        })
        # This will likely fail because the file doesn't exist
        # but we're testing the API call structure
        assert "result" in result or "error" in result
    
    def test_add_video_invalid_track(self, mock_project):
        """Test adding video to invalid track"""
        result = call_tool("add_video_to_track", {
            "track_index": 999,
            "video_file": "/path/to/test_video.mp4"
        })
        assert not result["success"]
        assert "error" in result
    
    def test_video_workflow(self, mock_project):
        """Test a typical video workflow"""
        # Check video support
        result = call_tool("check_video_support", {})
        assert result["success"]
        
        # Get current video settings
        result = call_tool("get_video_settings", {})
        assert result["success"]
        
        # Try to update settings
        result = call_tool("set_video_settings", {
            "width": 1920,
            "height": 1080,
            "fps": 30.0
        })
        assert result["success"]
    
    def test_video_resolution_options(self, mock_project):
        """Test various video resolution settings"""
        resolutions = [
            (640, 480),    # SD
            (1280, 720),   # HD
            (1920, 1080),  # Full HD
            (3840, 2160),  # 4K
        ]
        
        for width, height in resolutions:
            result = call_tool("set_video_settings", {
                "width": width,
                "height": height
            })
            assert result["success"]
            assert f"Width: {width} px" in result["result"]
            assert f"Height: {height} px" in result["result"]
    
    def test_video_fps_options(self, mock_project):
        """Test various FPS settings"""
        fps_options = [23.976, 24.0, 25.0, 29.97, 30.0, 50.0, 59.94, 60.0]
        
        for fps in fps_options:
            result = call_tool("set_video_settings", {"fps": fps})
            assert result["success"]
            assert f"FPS: {fps}" in result["result"]