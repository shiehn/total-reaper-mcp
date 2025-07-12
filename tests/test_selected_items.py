import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_selected_items_operations(reaper_mcp_client):
    """Test operations on selected items"""
    # Create a track and add an item first
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    assert "success" in result.content[0].text.lower()
    
    # Add media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "success" in result.content[0].text.lower() or "added" in result.content[0].text.lower()
    
    # Select the item
    result = await reaper_mcp_client.call_tool(
        "set_media_item_selected",
        {"item_index": 0, "selected": True}
    )
    print(f"Select item result: {result}")
    assert "success" in result.content[0].text.lower() or "selected" in result.content[0].text.lower()
    
    # Count selected items
    result = await reaper_mcp_client.call_tool(
        "count_selected_media_items",
        {}
    )
    print(f"Count selected items result: {result}")
    assert "1" in result.content[0].text
    
    # Get first selected item
    result = await reaper_mcp_client.call_tool(
        "get_selected_media_item",
        {"index": 0}
    )
    print(f"Get selected item result: {result}")
    assert "item" in result.content[0].text.lower() or "handle" in result.content[0].text
    
    # Deselect item
    result = await reaper_mcp_client.call_tool(
        "set_media_item_selected",
        {"item_index": 0, "selected": False}
    )
    assert "success" in result.content[0].text.lower() or "deselected" in result.content[0].text.lower()
    
    # Verify no items selected
    result = await reaper_mcp_client.call_tool(
        "count_selected_media_items",
        {}
    )
    assert "0" in result.content[0].text

@pytest.mark.asyncio
async def test_selected_tracks_operations(reaper_mcp_client):
    """Test operations on selected tracks"""
    # Create multiple tracks
    for i in range(3):
        result = await reaper_mcp_client.call_tool(
            "insert_track",
            {"index": i, "use_defaults": True}
        )
        assert "success" in result.content[0].text.lower()
    
    # Select first two tracks
    for i in range(2):
        result = await reaper_mcp_client.call_tool(
            "set_track_selected",
            {"track_index": i, "selected": True}
        )
        assert "success" in result.content[0].text.lower() or "selected" in result.content[0].text.lower()
    
    # Count selected tracks
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    print(f"Count selected tracks result: {result}")
    assert "2" in result.content[0].text
    
    # Get first selected track
    result = await reaper_mcp_client.call_tool(
        "get_selected_track",
        {"index": 0}
    )
    print(f"Get first selected track result: {result}")
    assert "track" in result.content[0].text.lower() or "handle" in result.content[0].text
    
    # Deselect all tracks
    for i in range(3):
        result = await reaper_mcp_client.call_tool(
            "set_track_selected",
            {"track_index": i, "selected": False}
        )
    
    # Verify no tracks selected
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert "0" in result.content[0].text

@pytest.mark.asyncio
async def test_selection_error_handling(reaper_mcp_client):
    """Test error handling for selection operations"""
    # Try to select non-existent item
    result = await reaper_mcp_client.call_tool(
        "set_media_item_selected",
        {"item_index": 999, "selected": True}
    )
    assert "failed" in result.content[0].text.lower() or "error" in result.content[0].text.lower()
    
    # Try to get selected item when none exist
    result = await reaper_mcp_client.call_tool(
        "get_selected_media_item",
        {"index": 0}
    )
    assert "no" in result.content[0].text.lower() or "none" in result.content[0].text.lower() or "error" in result.content[0].text.lower()