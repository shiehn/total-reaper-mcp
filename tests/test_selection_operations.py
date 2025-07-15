"""Test selection operations"""
import pytest
import pytest_asyncio
import asyncio
from .test_utils import (
    ensure_clean_project,
    create_track_with_verification,
    create_media_item_with_verification,
    assert_response_contains,
    assert_response_success,
    extract_number_from_response
)


@pytest.mark.asyncio
async def test_track_selection_operations(reaper_mcp_client):
    """Test track selection operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create some tracks and keep track of their indices
    track1_index = await create_track_with_verification(reaper_mcp_client, 0)
    track2_index = await create_track_with_verification(reaper_mcp_client, 1)
    track3_index = await create_track_with_verification(reaper_mcp_client, 2)
    
    # Count selected tracks (should be 0 initially)
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert_response_contains(result, "0 selected tracks")
    
    # Select first track
    result = await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": track1_index, "selected": True}
    )
    assert_response_contains(result, "has been selected")
    
    # Count selected tracks (should be 1)
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert_response_contains(result, "1 selected track")
    
    # Get selected track
    result = await reaper_mcp_client.call_tool(
        "get_selected_track",
        {"index": 0}
    )
    assert_response_contains(result, "Selected track")
    
    # Select second track too
    result = await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": track2_index, "selected": True}
    )
    assert_response_contains(result, "has been selected")
    
    # Count selected tracks (should be 2)
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert_response_contains(result, "2 selected tracks")
    
    # Unselect first track
    result = await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": track1_index, "selected": False}
    )
    assert_response_contains(result, "has been deselected")
    
    # Count selected tracks (should be 1)
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert_response_contains(result, "1 selected track")


@pytest.mark.asyncio
async def test_media_item_selection_operations(reaper_mcp_client):
    """Test media item selection operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Add first media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in result.content[0].text
    
    # Set position and length for first item
    await reaper_mcp_client.call_tool(
        "set_media_item_position",
        {"item_index": 0, "position": 0.0}
    )
    await reaper_mcp_client.call_tool(
        "set_media_item_length",
        {"item_index": 0, "length": 2.0}
    )
    
    # Add second media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in result.content[0].text
    
    # Set position and length for second item
    await reaper_mcp_client.call_tool(
        "set_media_item_position",
        {"item_index": 1, "position": 3.0}
    )
    await reaper_mcp_client.call_tool(
        "set_media_item_length",
        {"item_index": 1, "length": 2.0}
    )
    
    # Add third media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in result.content[0].text
    
    # Set position and length for third item
    await reaper_mcp_client.call_tool(
        "set_media_item_position",
        {"item_index": 2, "position": 6.0}
    )
    await reaper_mcp_client.call_tool(
        "set_media_item_length",
        {"item_index": 2, "length": 2.0}
    )
    
    # Count selected items (should be 0 initially)
    result = await reaper_mcp_client.call_tool(
        "count_selected_media_items",
        {}
    )
    assert "Project has 0 selected media items" in result.content[0].text
    
    # Select first item
    result = await reaper_mcp_client.call_tool(
        "set_media_item_selected",
        {"item_index": 0, "selected": True}
    )
    assert "Media item 0 is now selected" in result.content[0].text
    
    # Count selected items (should be 1)
    result = await reaper_mcp_client.call_tool(
        "count_selected_media_items",
        {}
    )
    assert "Project has 1 selected media items" in result.content[0].text
    
    # Get selected item
    result = await reaper_mcp_client.call_tool(
        "get_selected_media_item",
        {"index": 0}
    )
    assert "Selected media item at index 0:" in result.content[0].text
    
    # Select all items
    result = await reaper_mcp_client.call_tool(
        "select_all_media_items",
        {}
    )
    assert "Select all media items: true" in result.content[0].text
    
    # Count selected items (should be 3)
    result = await reaper_mcp_client.call_tool(
        "count_selected_media_items",
        {}
    )
    assert "Project has 3 selected media items" in result.content[0].text
    
    # Unselect all items
    result = await reaper_mcp_client.call_tool(
        "unselect_all_media_items",
        {}
    )
    assert "Unselect all media items: true" in result.content[0].text
    
    # Count selected items (should be 0)
    result = await reaper_mcp_client.call_tool(
        "count_selected_media_items",
        {}
    )
    assert "Project has 0 selected media items" in result.content[0].text


@pytest.mark.asyncio
async def test_combined_selection_operations(reaper_mcp_client):
    """Test combined track and item selection operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create multiple tracks with items
    for i in range(3):
        result = await reaper_mcp_client.call_tool(
            "insert_track_at_index",
            {"index": i, "want_defaults": True}
        )
        assert "Successfully inserted track" in result.content[0].text
        
        # Unselect the track after creation
        await reaper_mcp_client.call_tool(
            "set_track_selected",
            {"track_index": i, "selected": False}
        )
        
        result = await reaper_mcp_client.call_tool(
            "add_media_item_to_track",
            {"track_index": i}
        )
        assert "Added media item" in result.content[0].text
        
        # Set position and length
        await reaper_mcp_client.call_tool(
            "set_media_item_position",
            {"item_index": i, "position": 0.0}
        )
        await reaper_mcp_client.call_tool(
            "set_media_item_length",
            {"item_index": i, "length": 2.0}
        )
    
    # Unselect all tracks first
    await reaper_mcp_client.call_tool(
        "unselect_all_tracks",
        {}
    )
    
    # Debug: Check how many tracks are selected after unselect
    debug_result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    print(f"After unselect_all_tracks: {debug_result.content[0].text}")
    
    # Select multiple tracks
    await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": 0, "selected": True}
    )
    await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": 2, "selected": True}
    )
    
    # Verify selection counts
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    print(f"After selecting tracks 0 and 2: {result.content[0].text}")
    assert "2 selected tracks" in result.content[0].text
    
    # Select items on different tracks
    await reaper_mcp_client.call_tool(
        "set_media_item_selected",
        {"item_index": 0, "selected": True}
    )
    await reaper_mcp_client.call_tool(
        "set_media_item_selected",
        {"item_index": 2, "selected": True}
    )
    
    result = await reaper_mcp_client.call_tool(
        "count_selected_media_items",
        {}
    )
    assert "Project has 2 selected media items" in result.content[0].text