"""Test selection operations"""
import pytest
import pytest_asyncio
import asyncio


@pytest.mark.asyncio
async def test_track_selection_operations(reaper_mcp_client):
    """Test track selection operations"""
    # Create some tracks
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Created track" in result.content[0].text
    
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 1, "want_defaults": True}
    )
    assert "Created track" in result.content[0].text
    
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 2, "want_defaults": True}
    )
    assert "Created track" in result.content[0].text
    
    # Count selected tracks (should be 0 initially)
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert "Count selected tracks: 0" in result.content[0].text
    
    # Select first track
    result = await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": 0, "selected": True}
    )
    assert "Set track selected: true" in result.content[0].text
    
    # Count selected tracks (should be 1)
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert "Count selected tracks: 1" in result.content[0].text
    
    # Get selected track
    result = await reaper_mcp_client.call_tool(
        "get_selected_track",
        {"selected_track_index": 0}
    )
    assert "Get selected track:" in result.content[0].text
    
    # Select second track too
    result = await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": 1, "selected": True}
    )
    assert "Set track selected: true" in result.content[0].text
    
    # Count selected tracks (should be 2)
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert "Count selected tracks: 2" in result.content[0].text
    
    # Unselect first track
    result = await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": 0, "selected": False}
    )
    assert "Set track selected: true" in result.content[0].text
    
    # Count selected tracks (should be 1)
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert "Count selected tracks: 1" in result.content[0].text


@pytest.mark.asyncio
async def test_media_item_selection_operations(reaper_mcp_client):
    """Test media item selection operations"""
    # Create a track
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Created track" in result.content[0].text
    
    # Add some media items
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {
            "track_index": 0,
            "start_position": 0.0,
            "length": 2.0
        }
    )
    assert "Added media item" in result.content[0].text
    
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {
            "track_index": 0,
            "start_position": 3.0,
            "length": 2.0
        }
    )
    assert "Added media item" in result.content[0].text
    
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {
            "track_index": 0,
            "start_position": 6.0,
            "length": 2.0
        }
    )
    assert "Added media item" in result.content[0].text
    
    # Count selected items (should be 0 initially)
    result = await reaper_mcp_client.call_tool(
        "count_selected_media_items",
        {}
    )
    assert "Count selected media items: 0" in result.content[0].text
    
    # Select first item
    result = await reaper_mcp_client.call_tool(
        "set_media_item_selected",
        {"item_index": 0, "selected": True}
    )
    assert "Set media item selected: true" in result.content[0].text
    
    # Count selected items (should be 1)
    result = await reaper_mcp_client.call_tool(
        "count_selected_media_items",
        {}
    )
    assert "Count selected media items: 1" in result.content[0].text
    
    # Get selected item
    result = await reaper_mcp_client.call_tool(
        "get_selected_media_item",
        {"selected_item_index": 0}
    )
    assert "Get selected media item:" in result.content[0].text
    
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
    assert "Count selected media items: 3" in result.content[0].text
    
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
    assert "Count selected media items: 0" in result.content[0].text


@pytest.mark.asyncio
async def test_combined_selection_operations(reaper_mcp_client):
    """Test combined track and item selection operations"""
    # Create multiple tracks with items
    for i in range(3):
        result = await reaper_mcp_client.call_tool(
            "insert_track_at_index",
            {"index": i, "want_defaults": True}
        )
        assert "Created track" in result.content[0].text
        
        result = await reaper_mcp_client.call_tool(
            "add_media_item_to_track",
            {
                "track_index": i,
                "start_position": 0.0,
                "length": 2.0
            }
        )
        assert "Added media item" in result.content[0].text
    
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
    assert "Count selected tracks: 2" in result.content[0].text
    
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
    assert "Count selected media items: 2" in result.content[0].text