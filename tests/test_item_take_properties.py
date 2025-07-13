"""Test item and take property operations"""
import pytest
import pytest_asyncio
import asyncio


@pytest.mark.asyncio
async def test_media_item_properties(reaper_mcp_client):
    """Test media item property operations"""
    # Create a track with item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Add media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in result.content[0].text
    
    # Get item position
    result = await reaper_mcp_client.call_tool(
        "get_media_item_info_value",
        {
            "item_index": 0,
            "param_name": "D_POSITION"
        }
    )
    assert "Item D_POSITION:" in result.content[0].text
    
    # Set item position
    result = await reaper_mcp_client.call_tool(
        "set_media_item_info_value",
        {
            "item_index": 0,
            "param_name": "D_POSITION",
            "value": 2.0
        }
    )
    assert "Set item D_POSITION to 2.0" in result.content[0].text
    
    # Get item length
    result = await reaper_mcp_client.call_tool(
        "get_media_item_info_value",
        {
            "item_index": 0,
            "param_name": "D_LENGTH"
        }
    )
    assert "Item D_LENGTH:" in result.content[0].text
    
    # Set item length
    result = await reaper_mcp_client.call_tool(
        "set_media_item_info_value",
        {
            "item_index": 0,
            "param_name": "D_LENGTH",
            "value": 3.0
        }
    )
    assert "Set item D_LENGTH to 3.0" in result.content[0].text


@pytest.mark.asyncio
async def test_take_properties(reaper_mcp_client):
    """Test take property operations"""
    # Create track with item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Add media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in result.content[0].text
    
    # Get take name
    result = await reaper_mcp_client.call_tool(
        "get_take_name",
        {"take_index": 0}
    )
    assert "Take name:" in result.content[0].text
    
    # Set take name
    result = await reaper_mcp_client.call_tool(
        "set_take_name",
        {
            "take_index": 0,
            "name": "Test Take"
        }
    )
    assert "Set take name to: Test Take" in result.content[0].text
    
    # Get take volume
    result = await reaper_mcp_client.call_tool(
        "get_media_item_take_info_value",
        {
            "take_index": 0,
            "param_name": "D_VOL"
        }
    )
    assert "Take D_VOL:" in result.content[0].text
    
    # Set take volume
    result = await reaper_mcp_client.call_tool(
        "set_media_item_take_info_value",
        {
            "take_index": 0,
            "param_name": "D_VOL",
            "value": 0.5
        }
    )
    assert "Set take D_VOL to 0.5" in result.content[0].text


@pytest.mark.asyncio
async def test_item_state_chunk(reaper_mcp_client):
    """Test item state chunk operations"""
    # Create track with item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Add media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in result.content[0].text
    
    # Get item state chunk
    result = await reaper_mcp_client.call_tool(
        "get_item_state_chunk",
        {
            "item_index": 0,
            "is_undo": False
        }
    )
    assert "Item state chunk:" in result.content[0].text
    
    # Set item state chunk (minimal valid chunk)
    result = await reaper_mcp_client.call_tool(
        "set_item_state_chunk",
        {
            "item_index": 0,
            "state_chunk": "<ITEM\n>\n",
            "is_undo": False
        }
    )
    assert "Set item state chunk successfully" in result.content[0].text or "Failed" in result.content[0].text


@pytest.mark.asyncio
async def test_split_media_item(reaper_mcp_client):
    """Test splitting media items"""
    # Create track with item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Add media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in result.content[0].text
    
    # Split item at 5 seconds
    result = await reaper_mcp_client.call_tool(
        "split_media_item",
        {
            "item_index": 0,
            "position": 5.0
        }
    )
    assert "Split item at position 5.0" in result.content[0].text
    
    # Count items (should be 2 now)
    result = await reaper_mcp_client.call_tool(
        "count_media_items",
        {"project_index": 0}
    )
    assert "Media items in project: 2" in result.content[0].text