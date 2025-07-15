import pytest
import pytest_asyncio
from .test_utils import (
    ensure_clean_project,
    create_track_with_verification,
    create_media_item_with_verification,
    assert_response_contains,
    assert_response_success,
    extract_number_from_response
)

@pytest.mark.asyncio
async def test_selected_items_operations(reaper_mcp_client):
    """Test operations on selected items"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Add media item and get its index
    item_index = await create_media_item_with_verification(reaper_mcp_client, track_index)
    
    # Select the item
    result = await reaper_mcp_client.call_tool(
        "set_media_item_selected",
        {"item_index": item_index, "selected": True}
    )
    print(f"Select item result: {result}")
    assert_response_success(result)
    
    # Count selected items
    result = await reaper_mcp_client.call_tool(
        "count_selected_media_items",
        {}
    )
    print(f"Count selected items result: {result}")
    count = extract_number_from_response(result.content[0].text, r'(\d+)') or 0
    assert count == 1
    
    # Get first selected item
    result = await reaper_mcp_client.call_tool(
        "get_selected_media_item",
        {"index": 0}
    )
    print(f"Get selected item result: {result}")
    assert_response_contains(result, "item")
    
    # Deselect item
    result = await reaper_mcp_client.call_tool(
        "set_media_item_selected",
        {"item_index": item_index, "selected": False}
    )
    assert_response_success(result)
    
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