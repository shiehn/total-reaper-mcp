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
async def test_media_item_workflow(reaper_mcp_client):
    """Test media item creation and manipulation"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Add media item to track
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": track_index}
    )
    print(f"Add media item result: {result}")
    assert_response_success(result)
    
    # Count media items
    result = await reaper_mcp_client.call_tool(
        "count_media_items",
        {}
    )
    print(f"Count media items result: {result}")
    count = extract_number_from_response(result.content[0].text, r'(\d+) media items?')
    assert count == 1
    
    # Since we added the item, we can assume it's at index 0
    item_index = 0
    
    # Get media item
    result = await reaper_mcp_client.call_tool(
        "get_media_item",
        {"project_index": 0, "item_index": item_index}
    )
    print(f"Get media item result: {result}")
    assert "Media item" in result.content[0].text or "Item" in result.content[0].text
    
    # Set media item position
    result = await reaper_mcp_client.call_tool(
        "set_media_item_position",
        {"item_index": item_index, "position": 5.0}
    )
    print(f"Set item position result: {result}")
    assert_response_success(result)
    
    # Get media item position
    result = await reaper_mcp_client.call_tool(
        "get_media_item_position",
        {"item_index": item_index}
    )
    print(f"Get item position result: {result}")
    assert_response_contains(result, "5.0")
    
    # Set media item length
    result = await reaper_mcp_client.call_tool(
        "set_media_item_length",
        {"item_index": item_index, "length": 10.0}
    )
    print(f"Set item length result: {result}")
    assert_response_success(result)
    
    # Get media item length
    result = await reaper_mcp_client.call_tool(
        "get_media_item_length",
        {"item_index": item_index}
    )
    print(f"Get item length result: {result}")
    assert_response_contains(result, "10.0")
    
    # Delete media item
    result = await reaper_mcp_client.call_tool(
        "delete_track_media_item",
        {"track_index": track_index, "item_index": 0}  # Item index relative to track
    )
    print(f"Delete media item result: {result}")
    assert_response_success(result)