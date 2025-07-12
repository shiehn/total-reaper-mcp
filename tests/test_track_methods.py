import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_get_master_track(reaper_mcp_client):
    """Test getting the master track"""
    result = await reaper_mcp_client.call_tool(
        "get_master_track",
        {}
    )
    print(f"Get master track result: {result}")
    assert "Master track:" in result.content[0].text

@pytest.mark.asyncio
async def test_delete_track(reaper_mcp_client):
    """Test deleting a track"""
    # First create a track to delete
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Delete the track
    result = await reaper_mcp_client.call_tool(
        "delete_track",
        {"track_index": 0}
    )
    print(f"Delete track result: {result}")
    assert "Track 0 deleted successfully" in result.content[0].text
    
    # Try to delete non-existent track
    result = await reaper_mcp_client.call_tool(
        "delete_track",
        {"track_index": 999}
    )
    print(f"Delete non-existent track result: {result}")
    assert "Failed to find track at index 999" in result.content[0].text

@pytest.mark.asyncio
async def test_track_mute(reaper_mcp_client):
    """Test getting and setting track mute state"""
    # First create a track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Get initial mute state (should be unmuted)
    result = await reaper_mcp_client.call_tool(
        "get_track_mute",
        {"track_index": 0}
    )
    print(f"Get track mute result: {result}")
    assert "unmuted" in result.content[0].text
    
    # Mute the track
    result = await reaper_mcp_client.call_tool(
        "set_track_mute",
        {"track_index": 0, "mute": True}
    )
    print(f"Set track mute result: {result}")
    assert "Track 0 muted" in result.content[0].text
    
    # Verify mute state
    result = await reaper_mcp_client.call_tool(
        "get_track_mute",
        {"track_index": 0}
    )
    assert "muted" in result.content[0].text and "unmuted" not in result.content[0].text
    
    # Unmute the track
    result = await reaper_mcp_client.call_tool(
        "set_track_mute",
        {"track_index": 0, "mute": False}
    )
    assert "Track 0 unmuted" in result.content[0].text

@pytest.mark.asyncio
async def test_track_solo(reaper_mcp_client):
    """Test getting and setting track solo state"""
    # First create a track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Get initial solo state (should be not soloed)
    result = await reaper_mcp_client.call_tool(
        "get_track_solo",
        {"track_index": 0}
    )
    print(f"Get track solo result: {result}")
    assert "not soloed" in result.content[0].text
    
    # Solo the track
    result = await reaper_mcp_client.call_tool(
        "set_track_solo",
        {"track_index": 0, "solo": True}
    )
    print(f"Set track solo result: {result}")
    assert "Track 0 soloed" in result.content[0].text
    
    # Verify solo state
    result = await reaper_mcp_client.call_tool(
        "get_track_solo",
        {"track_index": 0}
    )
    assert "soloed" in result.content[0].text and "not soloed" not in result.content[0].text
    
    # Unsolo the track
    result = await reaper_mcp_client.call_tool(
        "set_track_solo",
        {"track_index": 0, "solo": False}
    )
    assert "Track 0 unsoloed" in result.content[0].text

@pytest.mark.asyncio
async def test_error_handling(reaper_mcp_client):
    """Test error handling for invalid track indices"""
    # Test get_track_mute with invalid index
    result = await reaper_mcp_client.call_tool(
        "get_track_mute",
        {"track_index": 999}
    )
    assert "Failed to find track at index 999" in result.content[0].text
    
    # Test set_track_solo with invalid index
    result = await reaper_mcp_client.call_tool(
        "set_track_solo",
        {"track_index": 999, "solo": True}
    )
    assert "Failed to find track at index 999" in result.content[0].text