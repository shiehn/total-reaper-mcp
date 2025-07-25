"""Test track folders and grouping operations"""
import pytest
import pytest_asyncio
import asyncio
from .test_utils import (
    ensure_clean_project,
    create_track_with_verification,
    assert_response_contains,
    assert_response_success
)


@pytest.mark.asyncio
async def test_track_folder_operations(reaper_mcp_client):
    """Test track folder operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create parent folder track
    folder_track_index = await create_track_with_verification(reaper_mcp_client, 0)
    
    # Set track name for clarity
    result = await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": folder_track_index, "name": "Folder Track"}
    )
    
    # Create child tracks and track their indices
    child_indices = []
    for i in range(1, 4):
        child_index = await create_track_with_verification(reaper_mcp_client, i)
        child_indices.append(child_index)
        
        result = await reaper_mcp_client.call_tool(
            "set_track_name",
            {"track_index": child_index, "name": f"Child Track {i}"}
        )
    
    # Set first track as folder parent
    result = await reaper_mcp_client.call_tool(
        "set_track_folder_state",
        {"track_index": folder_track_index, "folder_state": 1}
    )
    assert_response_contains(result, "Set track folder state:")
    
    # Set last child track as last in folder
    if child_indices:
        last_child_index = child_indices[-1]
        result = await reaper_mcp_client.call_tool(
            "set_track_folder_state",
            {"track_index": last_child_index, "folder_state": -1}
        )
        assert_response_contains(result, "Set track folder state:")
    
    # Get track depth of a child track
    result = await reaper_mcp_client.call_tool(
        "get_track_depth",
        {"track_index": 1}
    )
    assert "Track depth:" in result.content[0].text
    
    # Get parent track of a child
    result = await reaper_mcp_client.call_tool(
        "get_parent_track",
        {"track_index": 1}
    )
    assert "Parent track:" in result.content[0].text


@pytest.mark.asyncio
async def test_track_folder_compact_state(reaper_mcp_client):
    """Test track folder compact state operations"""
    # Create a folder track
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Set as folder
    result = await reaper_mcp_client.call_tool(
        "set_track_folder_state",
        {"track_index": 0, "folder_state": 1}
    )
    
    # Get initial compact state
    result = await reaper_mcp_client.call_tool(
        "get_track_folder_compact_state",
        {"track_index": 0}
    )
    assert "Track folder compact state:" in result.content[0].text
    
    # Set to small (1)
    result = await reaper_mcp_client.call_tool(
        "set_track_folder_compact_state",
        {"track_index": 0, "compact_state": 1}
    )
    assert "Set track folder compact state:" in result.content[0].text
    
    # Set to tiny (2)
    result = await reaper_mcp_client.call_tool(
        "set_track_folder_compact_state",
        {"track_index": 0, "compact_state": 2}
    )
    assert "Set track folder compact state:" in result.content[0].text
    
    # Set back to open (0)
    result = await reaper_mcp_client.call_tool(
        "set_track_folder_compact_state",
        {"track_index": 0, "compact_state": 0}
    )
    assert "Set track folder compact state:" in result.content[0].text


@pytest.mark.asyncio
async def test_track_height_operations(reaper_mcp_client):
    """Test track height operations"""
    # Create a track
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Set track height
    result = await reaper_mcp_client.call_tool(
        "set_track_height",
        {"track_index": 0, "height": 100}
    )
    assert "Set track height:" in result.content[0].text
    
    # Set track height with lock
    result = await reaper_mcp_client.call_tool(
        "set_track_height",
        {"track_index": 0, "height": 150, "lock_height": True}
    )
    assert "Set track height:" in result.content[0].text
    
    # Set track height unlocked
    result = await reaper_mcp_client.call_tool(
        "set_track_height",
        {"track_index": 0, "height": 200, "lock_height": False}
    )
    assert "Set track height:" in result.content[0].text


@pytest.mark.asyncio
async def test_nested_folders(reaper_mcp_client):
    """Test nested folder structures"""
    # Create main folder
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 0, "name": "Main Folder"}
    )
    
    # Create sub-folder
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 1, "want_defaults": True}
    )
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 1, "name": "Sub Folder"}
    )
    
    # Create child tracks
    for i in range(2, 5):
        result = await reaper_mcp_client.call_tool(
            "insert_track_at_index",
            {"index": i, "want_defaults": True}
        )
        await reaper_mcp_client.call_tool(
            "set_track_name",
            {"track_index": i, "name": f"Track {i-1}"}
        )
    
    # Set folder structure
    # Main folder starts
    await reaper_mcp_client.call_tool(
        "set_track_folder_state",
        {"track_index": 0, "folder_state": 1}
    )
    
    # Sub folder starts
    await reaper_mcp_client.call_tool(
        "set_track_folder_state",
        {"track_index": 1, "folder_state": 1}
    )
    
    # Last track ends both folders
    await reaper_mcp_client.call_tool(
        "set_track_folder_state",
        {"track_index": 4, "folder_state": -2}
    )
    
    # Check depths
    result = await reaper_mcp_client.call_tool(
        "get_track_depth",
        {"track_index": 2}
    )
    assert "Track depth:" in result.content[0].text