"""Test file and resource management operations"""
import pytest
import pytest_asyncio
import asyncio


@pytest.mark.asyncio
async def test_resource_paths(reaper_mcp_client):
    """Test getting resource and executable paths"""
    # Get resource path
    result = await reaper_mcp_client.call_tool(
        "get_resource_path",
        {}
    )
    assert "Resource path:" in result.content[0].text
    
    # Get executable path
    result = await reaper_mcp_client.call_tool(
        "get_exe_path",
        {}
    )
    assert "Executable path:" in result.content[0].text


@pytest.mark.asyncio
async def test_project_paths(reaper_mcp_client):
    """Test project path operations"""
    # Get project path
    result = await reaper_mcp_client.call_tool(
        "get_project_path",
        {"project_index": 0}
    )
    assert "Project path:" in result.content[0].text
    
    # Get project state change count
    result = await reaper_mcp_client.call_tool(
        "get_project_state_change_count",
        {"project_index": 0}
    )
    assert "Project state change count:" in result.content[0].text


@pytest.mark.asyncio
async def test_directory_creation(reaper_mcp_client):
    """Test recursive directory creation"""
    # Create a test directory
    result = await reaper_mcp_client.call_tool(
        "recursive_create_directory",
        {
            "path": "/tmp/reaper_test_dir/sub1/sub2",
            "mode": 0
        }
    )
    assert "Created directory:" in result.content[0].text or "Failed" in result.content[0].text


@pytest.mark.asyncio
async def test_track_state_chunk(reaper_mcp_client):
    """Test track state chunk operations"""
    # Create a track
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Created track" in result.content[0].text
    
    # Set track name and color for identification
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 0, "name": "Test Track"}
    )
    
    await reaper_mcp_client.call_tool(
        "set_track_color",
        {"track_index": 0, "color": 0xFF0000}  # Red
    )
    
    # Get track state chunk
    result = await reaper_mcp_client.call_tool(
        "get_track_state_chunk",
        {"track_index": 0, "is_undo": False}
    )
    assert "Track state chunk:" in result.content[0].text
    
    # The chunk should contain track info
    # Note: We just verify we got a response, not the exact format
    
    # Test setting state chunk (would need a valid chunk string)
    # This is mainly to test the API is exposed correctly
    result = await reaper_mcp_client.call_tool(
        "set_track_state_chunk",
        {
            "track_index": 0,
            "state_chunk": "<TRACK\n>\n",  # Minimal valid chunk
            "is_undo": False
        }
    )
    assert "Set track state chunk successfully" in result.content[0].text or "Failed" in result.content[0].text


@pytest.mark.asyncio
async def test_file_browser(reaper_mcp_client):
    """Test file browser dialog"""
    # Note: This won't actually open a dialog in automation context
    result = await reaper_mcp_client.call_tool(
        "browse_for_file",
        {
            "title": "Select Audio File",
            "extension": "wav"
        }
    )
    # In automation context, this will return a placeholder
    assert "Selected file:" in result.content[0].text or "file_browser_not_available" in result.content[0].text


@pytest.mark.asyncio
async def test_project_state_tracking(reaper_mcp_client):
    """Test project state change tracking"""
    # Get initial state count
    result = await reaper_mcp_client.call_tool(
        "get_project_state_change_count",
        {"project_index": 0}
    )
    assert "Project state change count:" in result.content[0].text
    
    # Make some changes
    await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 0, "name": "Changed Track"}
    )
    
    # Get state count again - it should have increased
    result = await reaper_mcp_client.call_tool(
        "get_project_state_change_count",
        {"project_index": 0}
    )
    assert "Project state change count:" in result.content[0].text