"""Test cases for color management operations"""

import pytest
from .conftest import call_tool, reaper_available


@pytest.mark.integration
@pytest.mark.skipif(not reaper_available(), reason="REAPER not available")
class TestColorManagement:
    """Test color management operations"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, mock_project):
        """Ensure clean state for each test"""
        pass
    
    def test_get_set_track_color(self, mock_project):
        """Test getting and setting track color"""
        # Create a track
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        # Get default color
        result = call_tool("get_track_color", {"track_index": 0})
        assert result["success"]
        assert "color:" in result["result"]
        
        # Set to red
        red_color = (255 << 16) | (0 << 8) | 0  # RGB(255, 0, 0)
        result = call_tool("set_track_color", {"track_index": 0, "color": red_color})
        assert result["success"]
        assert "RGB(255, 0, 0)" in result["result"]
        
        # Verify it was set
        result = call_tool("get_track_color", {"track_index": 0})
        assert result["success"]
        assert "RGB(255, 0, 0)" in result["result"]
        
        # Set to green
        green_color = (0 << 16) | (255 << 8) | 0  # RGB(0, 255, 0)
        result = call_tool("set_track_color", {"track_index": 0, "color": green_color})
        assert result["success"]
        assert "RGB(0, 255, 0)" in result["result"]
        
        # Set back to default
        result = call_tool("set_track_color", {"track_index": 0, "color": 0})
        assert result["success"]
        assert "default" in result["result"]
    
    def test_master_track_color(self, mock_project):
        """Test getting and setting master track color"""
        # Get master track color
        result = call_tool("get_track_color", {"track_index": -1})
        assert result["success"]
        
        # Set master track to blue
        blue_color = (0 << 16) | (0 << 8) | 255  # RGB(0, 0, 255)
        result = call_tool("set_track_color", {"track_index": -1, "color": blue_color})
        assert result["success"]
        assert "RGB(0, 0, 255)" in result["result"]
        
        # Verify
        result = call_tool("get_track_color", {"track_index": -1})
        assert result["success"]
        assert "RGB(0, 0, 255)" in result["result"]
    
    def test_get_media_item_color(self, mock_project):
        """Test getting media item color"""
        # Create track and item
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        result = call_tool("add_media_item_to_track", {"track_index": 0})
        assert result["success"]
        
        # Get default item color
        result = call_tool("get_media_item_color", {"item_index": 0})
        assert result["success"]
        
        # Set item color (already tested in test_advanced_item_operations.py)
        # Here we just verify we can get it
        purple_color = (128 << 16) | (0 << 8) | 128  # RGB(128, 0, 128)
        result = call_tool("set_media_item_color", {"item_index": 0, "color": purple_color})
        assert result["success"]
        
        # Get the color we just set
        result = call_tool("get_media_item_color", {"item_index": 0})
        assert result["success"]
        assert "RGB(128, 0, 128)" in result["result"]
    
    def test_multiple_track_colors(self, mock_project):
        """Test setting different colors on multiple tracks"""
        # Create 3 tracks
        colors = [
            ((255 << 16) | (0 << 8) | 0, "RGB(255, 0, 0)"),     # Red
            ((0 << 16) | (255 << 8) | 0, "RGB(0, 255, 0)"),     # Green
            ((0 << 16) | (0 << 8) | 255, "RGB(0, 0, 255)"),     # Blue
        ]
        
        for i in range(3):
            result = call_tool("insert_track", {"index": i})
            assert result["success"]
            
            # Set color
            color_val, color_str = colors[i]
            result = call_tool("set_track_color", {"track_index": i, "color": color_val})
            assert result["success"]
            assert color_str in result["result"]
        
        # Verify all colors are still correct
        for i in range(3):
            result = call_tool("get_track_color", {"track_index": i})
            assert result["success"]
            _, expected_color = colors[i]
            assert expected_color in result["result"]
    
    def test_invalid_track_color_operations(self, mock_project):
        """Test error handling for invalid tracks"""
        # Try to get color from non-existent track
        result = call_tool("get_track_color", {"track_index": 999})
        assert not result["success"]
        
        # Try to set color on non-existent track
        result = call_tool("set_track_color", {"track_index": 999, "color": 255})
        assert not result["success"]
    
    def test_invalid_item_color_operations(self, mock_project):
        """Test error handling for invalid items"""
        # Try to get color from non-existent item
        result = call_tool("get_media_item_color", {"item_index": 999})
        assert not result["success"]