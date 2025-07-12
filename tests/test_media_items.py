import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_media_item_workflow(reaper_mcp_client):
    """Test media item creation and manipulation"""
    # Create a track first
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    assert "success" in result.content[0].text.lower()
    
    # Add media item to track
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    print(f"Add media item result: {result}")
    assert "success" in result.content[0].text.lower() or "added" in result.content[0].text.lower()
    
    # Count media items
    result = await reaper_mcp_client.call_tool(
        "count_media_items",
        {}
    )
    print(f"Count media items result: {result}")
    assert "1" in result.content[0].text
    
    # Get media item
    result = await reaper_mcp_client.call_tool(
        "get_media_item",
        {"project_index": 0, "item_index": 0}
    )
    print(f"Get media item result: {result}")
    assert "Media item" in result.content[0].text or "Item" in result.content[0].text
    
    # Set media item position
    result = await reaper_mcp_client.call_tool(
        "set_media_item_position",
        {"item_index": 0, "position": 5.0, "move_edit_cursor": False}
    )
    print(f"Set item position result: {result}")
    assert "success" in result.content[0].text.lower() or "position" in result.content[0].text.lower()
    
    # Get media item position
    result = await reaper_mcp_client.call_tool(
        "get_media_item_position",
        {"item_index": 0}
    )
    print(f"Get item position result: {result}")
    assert "5.0" in result.content[0].text
    
    # Set media item length
    result = await reaper_mcp_client.call_tool(
        "set_media_item_length",
        {"item_index": 0, "length": 10.0, "adjust_takes": True}
    )
    print(f"Set item length result: {result}")
    assert "success" in result.content[0].text.lower() or "length" in result.content[0].text.lower()
    
    # Get media item length
    result = await reaper_mcp_client.call_tool(
        "get_media_item_length",
        {"item_index": 0}
    )
    print(f"Get item length result: {result}")
    assert "10.0" in result.content[0].text
    
    # Delete media item
    result = await reaper_mcp_client.call_tool(
        "delete_track_media_item",
        {"track_index": 0, "item_index": 0}
    )
    print(f"Delete media item result: {result}")
    assert "success" in result.content[0].text.lower() or "deleted" in result.content[0].text.lower()