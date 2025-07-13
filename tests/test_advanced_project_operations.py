"""Test cases for advanced project operations"""

import pytest
import os
import tempfile
from .conftest import call_tool, reaper_available


@pytest.mark.integration
@pytest.mark.skipif(not reaper_available(), reason="REAPER not available")
class TestAdvancedProjectOperations:
    """Test advanced project operations"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, mock_project):
        """Ensure clean state for each test"""
        pass
    
    def test_enum_projects(self, mock_project):
        """Test enumerating open projects"""
        # Get current projects
        result = call_tool("enum_projects", {})
        assert result["success"]
        
        # Should have at least one project (the current one)
        assert "Open projects:" in result["result"] or "No projects open" in result["result"]
        
        # If we have projects, one should be marked as current
        if "Open projects:" in result["result"]:
            assert "(current)" in result["result"]
    
    def test_get_current_project_index(self, mock_project):
        """Test getting current project index"""
        result = call_tool("get_current_project_index", {})
        assert result["success"]
        assert "Current project index:" in result["result"]
        
        # Extract index
        index_str = result["result"].split(": ")[1]
        index = int(index_str)
        assert index >= 0
    
    def test_save_and_open_project(self, mock_project):
        """Test saving and opening a project"""
        # Create a temporary file for the project
        with tempfile.NamedTemporaryFile(suffix=".rpp", delete=False) as tmp:
            project_path = tmp.name
        
        try:
            # Add a track to make the project non-empty
            result = call_tool("insert_track", {"index": 0})
            assert result["success"]
            
            # Set track name for identification
            result = call_tool("set_track_name", {"track_index": 0, "name": "Test Track"})
            assert result["success"]
            
            # Save the project
            result = call_tool("save_project", {})
            assert result["success"]
            
            # Note: We can't easily test opening projects without
            # potentially disrupting the test environment
            
        finally:
            # Clean up
            if os.path.exists(project_path):
                os.unlink(project_path)
    
    def test_project_switching(self, mock_project):
        """Test switching between projects"""
        # Get initial project count
        result = call_tool("enum_projects", {})
        assert result["success"]
        
        # Get current project index
        result = call_tool("get_current_project_index", {})
        assert result["success"]
        current_index = int(result["result"].split(": ")[1])
        
        # If there are multiple projects, we could test switching
        # But in our test environment, we typically have just one
        
        # Try to switch to the same project (should succeed)
        result = call_tool("select_project_instance", {"project_index": current_index})
        assert result["success"]
    
    def test_invalid_project_operations(self, mock_project):
        """Test error handling for invalid project operations"""
        # Try to switch to an invalid project index
        result = call_tool("select_project_instance", {"project_index": 9999})
        assert not result["success"]
        assert "error" in result
    
    def test_project_info_consistency(self, mock_project):
        """Test that project information is consistent"""
        # Get projects list
        result = call_tool("enum_projects", {})
        assert result["success"]
        
        # Get current project index
        result = call_tool("get_current_project_index", {})
        assert result["success"]
        current_index = int(result["result"].split(": ")[1])
        
        # The current index should be valid
        assert current_index >= 0
        
        # If we have the project list, verify the current marker
        result = call_tool("enum_projects", {})
        if "Open projects:" in result["result"]:
            lines = result["result"].split("\n")
            # Find the line with the current index
            for line in lines:
                if line.startswith(f"{current_index}:"):
                    assert "(current)" in line
                    break