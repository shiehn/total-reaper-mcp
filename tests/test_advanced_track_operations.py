"""Test cases for advanced track operations"""

import pytest
from .conftest import call_tool, reaper_available


@pytest.mark.integration
@pytest.mark.skipif(not reaper_available(), reason="REAPER not available")
class TestAdvancedTrackOperations:
    """Test advanced track operations"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, mock_project):
        """Ensure clean state for each test"""
        pass
    
    def test_get_track_receive_count(self, mock_project):
        """Test getting track receive count"""
        # Create two tracks
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        result = call_tool("insert_track", {"index": 1})
        assert result["success"]
        
        # Get receive count (should be 0 initially)
        result = call_tool("get_track_receive_count", {"track_index": 1})
        assert result["success"]
        assert "0 receives" in result["result"]
        
        # Test master track
        result = call_tool("get_track_receive_count", {"track_index": -1})
        assert result["success"]
    
    def test_get_track_receive_info(self, mock_project):
        """Test getting track receive information"""
        # Create tracks and add a send/receive
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        result = call_tool("insert_track", {"index": 1})
        assert result["success"]
        
        # Create a send from track 0 to track 1
        result = call_tool("create_track_send", {"src_track_index": 0, "dest_track_index": 1})
        assert result["success"]
        
        # Get receive info
        result = call_tool("get_track_receive_info", {"track_index": 1, "receive_index": 0})
        assert result["success"]
        assert "Volume:" in result["result"]
        assert "Pan:" in result["result"]
    
    def test_get_track_guid(self, mock_project):
        """Test getting track GUID"""
        # Create a track
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        # Get track GUID
        result = call_tool("get_track_guid", {"track_index": 0})
        assert result["success"]
        assert "GUID:" in result["result"]
        assert len(result["result"].split("GUID: ")[1]) > 0
        
        # Test master track GUID
        result = call_tool("get_track_guid", {"track_index": -1})
        assert result["success"]
        assert "GUID:" in result["result"]
    
    def test_get_track_from_guid(self, mock_project):
        """Test getting track by GUID"""
        # Create a track with a name
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        result = call_tool("set_track_name", {"track_index": 0, "name": "Test Track"})
        assert result["success"]
        
        # Get its GUID
        result = call_tool("get_track_guid", {"track_index": 0})
        assert result["success"]
        guid = result["result"].split("GUID: ")[1]
        
        # Find track by GUID
        result = call_tool("get_track_from_guid", {"guid": guid})
        assert result["success"]
        assert "Test Track" in result["result"]
        assert "index 0" in result["result"]
    
    def test_master_track_guid_lookup(self, mock_project):
        """Test master track GUID lookup"""
        # Get master track GUID
        result = call_tool("get_track_guid", {"track_index": -1})
        assert result["success"]
        guid = result["result"].split("GUID: ")[1]
        
        # Find master track by GUID
        result = call_tool("get_track_from_guid", {"guid": guid})
        assert result["success"]
        assert "Master Track" in result["result"]
        assert "index -1" in result["result"]
    
    def test_invalid_track_operations(self, mock_project):
        """Test error handling for invalid tracks"""
        # Invalid track for receive count
        result = call_tool("get_track_receive_count", {"track_index": 999})
        assert not result["success"]
        
        # Invalid track for GUID
        result = call_tool("get_track_guid", {"track_index": 999})
        assert not result["success"]
        
        # Invalid GUID lookup
        result = call_tool("get_track_from_guid", {"guid": "invalid-guid-123"})
        assert not result["success"]