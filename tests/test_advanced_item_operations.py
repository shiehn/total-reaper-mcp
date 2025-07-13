"""Test cases for advanced media item and take operations"""

import pytest
from .conftest import call_tool, reaper_available


@pytest.mark.integration
@pytest.mark.skipif(not reaper_available(), reason="REAPER not available")
class TestAdvancedItemOperations:
    """Test advanced media item and take operations"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, mock_project):
        """Ensure clean state for each test"""
        pass
    
    def test_split_media_item(self, mock_project):
        """Test splitting a media item"""
        # Create track and add item
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        result = call_tool("add_media_item_to_track", {"track_index": 0})
        assert result["success"]
        
        # Set item length to 10 seconds
        result = call_tool("set_media_item_length", {"item_index": 0, "length": 10.0})
        assert result["success"]
        
        # Split at 5 seconds
        result = call_tool("split_media_item", {"item_index": 0, "position": 5.0})
        assert result["success"]
        assert "New item created:" in result["result"]
        
        # Verify we now have 2 items
        result = call_tool("count_media_items", {})
        assert result["success"]
        assert "2" in result["result"]
    
    def test_glue_media_items(self, mock_project):
        """Test gluing media items together"""
        # Create track with multiple items
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        # Add two items
        result = call_tool("add_media_item_to_track", {"track_index": 0})
        assert result["success"]
        result = call_tool("add_media_item_to_track", {"track_index": 0})
        assert result["success"]
        
        # Select all items
        result = call_tool("select_all_media_items", {})
        assert result["success"]
        
        # Glue them
        result = call_tool("glue_media_items", {})
        assert result["success"]
        assert "Glued" in result["result"]
    
    def test_get_media_item_track(self, mock_project):
        """Test getting the parent track of a media item"""
        # Create track with name
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        result = call_tool("set_track_name", {"track_index": 0, "name": "Item Track"})
        assert result["success"]
        
        # Add item
        result = call_tool("add_media_item_to_track", {"track_index": 0})
        assert result["success"]
        
        # Get item's track
        result = call_tool("get_media_item_take_track", {"item_index": 0})
        assert result["success"]
        assert "Item Track" in result["result"]
        assert "index 0" in result["result"]
    
    def test_duplicate_media_item(self, mock_project):
        """Test duplicating a media item"""
        # Create track and item
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        result = call_tool("add_media_item_to_track", {"track_index": 0})
        assert result["success"]
        
        # Duplicate the item
        result = call_tool("duplicate_media_item", {"item_index": 0})
        assert result["success"]
        assert "New item index:" in result["result"]
        
        # Verify we now have 2 items
        result = call_tool("count_media_items", {})
        assert result["success"]
        assert "2" in result["result"]
    
    def test_set_media_item_color(self, mock_project):
        """Test setting media item color"""
        # Create track and item
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        result = call_tool("add_media_item_to_track", {"track_index": 0})
        assert result["success"]
        
        # Set item color (red: RGB(255,0,0) as integer)
        red_color = (255 << 16) | (0 << 8) | 0  # 0xFF0000
        result = call_tool("set_media_item_color", {"item_index": 0, "color": red_color})
        assert result["success"]
        assert f"Set item 0 color to {red_color}" in result["result"]
        
        # Set to default color
        result = call_tool("set_media_item_color", {"item_index": 0, "color": 0})
        assert result["success"]
    
    def test_invalid_item_operations(self, mock_project):
        """Test error handling for invalid items"""
        # Try to split non-existent item
        result = call_tool("split_media_item", {"item_index": 999, "position": 5.0})
        assert not result["success"]
        
        # Try to get track of non-existent item
        result = call_tool("get_media_item_take_track", {"item_index": 999})
        assert not result["success"]
        
        # Try to duplicate non-existent item
        result = call_tool("duplicate_media_item", {"item_index": 999})
        assert not result["success"]
        
        # Try to set color of non-existent item
        result = call_tool("set_media_item_color", {"item_index": 999, "color": 255})
        assert not result["success"]