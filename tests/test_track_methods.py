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
async def test_get_master_track(reaper_mcp_client):
    """Test getting the master track"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    result = await reaper_mcp_client.call_tool(
        "get_master_track",
        {}
    )
    print(f"Get master track result: {result}")
    assert_response_contains(result, "Master track:")

@pytest.mark.asyncio
async def test_delete_track(reaper_mcp_client):
    """Test deleting a track"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Delete the track
    result = await reaper_mcp_client.call_tool(
        "delete_track",
        {"track_index": track_index}
    )
    print(f"Delete track result: {result}")
    assert_response_contains(result, f"Successfully deleted track at index {track_index}")
    
    # Try to delete non-existent track
    result = await reaper_mcp_client.call_tool(
        "delete_track",
        {"track_index": 999}
    )
    print(f"Delete non-existent track result: {result}")
    assert "Track index 999 out of range" in result.content[0].text

@pytest.mark.asyncio
async def test_track_mute(reaper_mcp_client):
    """Test getting and setting track mute state"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Get initial mute state (should be unmuted)
    result = await reaper_mcp_client.call_tool(
        "get_track_mute",
        {"track_index": track_index}
    )
    print(f"Get track mute result: {result}")
    assert_response_contains(result, "not muted")
    
    # Mute the track
    result = await reaper_mcp_client.call_tool(
        "set_track_mute",
        {"track_index": track_index, "mute": True}
    )
    print(f"Set track mute result: {result}")
    assert_response_contains(result, f"Track {track_index} muted")
    
    # Verify mute state
    result = await reaper_mcp_client.call_tool(
        "get_track_mute",
        {"track_index": track_index}
    )
    assert_response_contains(result, "is muted")
    
    # Unmute the track
    result = await reaper_mcp_client.call_tool(
        "set_track_mute",
        {"track_index": track_index, "mute": False}
    )
    assert_response_contains(result, f"Track {track_index} unmuted")

@pytest.mark.asyncio
async def test_track_solo(reaper_mcp_client):
    """Test getting and setting track solo state"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Get initial solo state (should be not soloed)
    result = await reaper_mcp_client.call_tool(
        "get_track_solo",
        {"track_index": track_index}
    )
    print(f"Get track solo result: {result}")
    assert_response_contains(result, "not soloed")
    
    # Solo the track
    result = await reaper_mcp_client.call_tool(
        "set_track_solo",
        {"track_index": track_index, "solo": True}
    )
    print(f"Set track solo result: {result}")
    assert_response_contains(result, f"Track {track_index} soloed")
    
    # Verify solo state
    result = await reaper_mcp_client.call_tool(
        "get_track_solo",
        {"track_index": track_index}
    )
    # Check for 'soloed' but not 'not soloed'
    assert "soloed" in result.content[0].text and "not soloed" not in result.content[0].text
    
    # Unsolo the track
    result = await reaper_mcp_client.call_tool(
        "set_track_solo",
        {"track_index": track_index, "solo": False}
    )
    assert_response_contains(result, f"Track {track_index} unsoloed")

@pytest.mark.asyncio
async def test_error_handling(reaper_mcp_client):
    """Test error handling for invalid track indices"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Test get_track_mute with invalid index
    result = await reaper_mcp_client.call_tool(
        "get_track_mute",
        {"track_index": 999}
    )
    assert "Track not found at index 999" in result.content[0].text or "Failed to get track mute state" in result.content[0].text
    
    # Test set_track_solo with invalid index
    result = await reaper_mcp_client.call_tool(
        "set_track_solo",
        {"track_index": 999, "solo": True}
    )
    assert "Track not found at index 999" in result.content[0].text or "Failed to set track solo state" in result.content[0].text