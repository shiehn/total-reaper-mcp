"""Test take management extended operations"""
import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_take_creation_and_deletion(reaper_mcp_client):
    """Test creating and deleting takes"""
    # Create a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Add an item
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track", 
        {"track_index": 0}
    )
    
    # Add a new take
    result = await reaper_mcp_client.call_tool(
        "add_new_take_to_item",
        {"item_index": 0}
    )
    assert result is not None
    assert "Added new take" in result.content[0].text
    assert "2 takes" in result.content[0].text  # Should have 2 takes now
    
    # Delete the take
    result = await reaper_mcp_client.call_tool(
        "delete_take",
        {
            "item_index": 0,
            "take_index": 1  # Delete the second take
        }
    )
    assert result is not None
    assert "Deleted take" in result.content[0].text

@pytest.mark.asyncio
async def test_take_pitch_and_playback_rate(reaper_mcp_client):
    """Test take pitch and playback rate adjustments"""
    # Create a track with an item
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    # Set take pitch
    result = await reaper_mcp_client.call_tool(
        "set_take_pitch",
        {
            "item_index": 0,
            "take_index": 0,
            "pitch": 2.0  # Up 2 semitones
        }
    )
    assert result is not None
    assert "Set take" in result.content[0].text
    assert "2.00 semitones" in result.content[0].text
    
    # Get take pitch
    result = await reaper_mcp_client.call_tool(
        "get_take_pitch",
        {
            "item_index": 0,
            "take_index": 0
        }
    )
    assert result is not None
    assert "pitch: 2.00" in result.content[0].text
    
    # Set playback rate
    result = await reaper_mcp_client.call_tool(
        "set_take_playback_rate",
        {
            "item_index": 0,
            "take_index": 0,
            "rate": 1.5  # 150% speed
        }
    )
    assert result is not None
    assert "1.50x" in result.content[0].text
    assert "150.0%" in result.content[0].text

@pytest.mark.asyncio
async def test_take_markers(reaper_mcp_client):
    """Test take marker operations"""
    # Create a track with an item
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    # Add a take marker
    result = await reaper_mcp_client.call_tool(
        "add_take_marker",
        {
            "item_index": 0,
            "take_index": 0,
            "position": 1.0,
            "name": "Chorus Start",
            "color": 0xFF0000  # Red
        }
    )
    assert result is not None
    assert "Added take marker" in result.content[0].text
    assert "Chorus Start" in result.content[0].text
    
    # Count take markers
    result = await reaper_mcp_client.call_tool(
        "count_take_markers",
        {
            "item_index": 0,
            "take_index": 0
        }
    )
    assert result is not None
    assert "has" in result.content[0].text
    assert "markers" in result.content[0].text

@pytest.mark.asyncio
async def test_take_start_offset(reaper_mcp_client):
    """Test take start offset operations"""
    # Create a track with an item
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    # Set start offset
    result = await reaper_mcp_client.call_tool(
        "set_take_start_offset",
        {
            "item_index": 0,
            "take_index": 0,
            "offset": 0.5
        }
    )
    assert result is not None
    assert "Set take" in result.content[0].text
    assert "0.500 seconds" in result.content[0].text
    
    # Get start offset
    result = await reaper_mcp_client.call_tool(
        "get_take_start_offset",
        {
            "item_index": 0,
            "take_index": 0
        }
    )
    assert result is not None
    assert "start offset" in result.content[0].text
    assert "0.500" in result.content[0].text