import pytest
import pytest_asyncio
from .test_utils import (
    ensure_clean_project,
    create_track_with_verification,
    assert_response_contains,
    assert_response_success
)

@pytest.mark.asyncio
async def test_track_volume_operations(reaper_mcp_client):
    """Test track volume operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Set track volume
    result = await reaper_mcp_client.call_tool(
        "set_track_volume",
        {"track_index": track_index, "volume": 0.5}
    )
    print(f"Set track volume result: {result}")
    assert_response_success(result)
    
    # Get track volume
    result = await reaper_mcp_client.call_tool(
        "get_track_volume",
        {"track_index": track_index}
    )
    print(f"Get track volume result: {result}")
    assert_response_contains(result, "0.5")
    
    # Test with dB value
    result = await reaper_mcp_client.call_tool(
        "set_track_volume_db",
        {"track_index": track_index, "volume_db": -6.0}
    )
    print(f"Set track volume dB result: {result}")
    assert_response_success(result)
    
    # Get track volume in dB
    result = await reaper_mcp_client.call_tool(
        "get_track_volume_db",
        {"track_index": track_index}
    )
    print(f"Get track volume dB result: {result}")
    assert_response_contains(result, "-6")

@pytest.mark.asyncio
async def test_track_pan_operations(reaper_mcp_client):
    """Test track pan operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Set track pan
    result = await reaper_mcp_client.call_tool(
        "set_track_pan",
        {"track_index": track_index, "pan": -0.5}
    )
    print(f"Set track pan result: {result}")
    assert_response_success(result)
    
    # Get track pan
    result = await reaper_mcp_client.call_tool(
        "get_track_pan",
        {"track_index": track_index}
    )
    print(f"Get track pan result: {result}")
    assert_response_contains(result, "-0.5")
    
    # Test center pan
    result = await reaper_mcp_client.call_tool(
        "set_track_pan",
        {"track_index": track_index, "pan": 0.0}
    )
    assert_response_success(result)
    
    # Test right pan
    result = await reaper_mcp_client.call_tool(
        "set_track_pan",
        {"track_index": track_index, "pan": 1.0}
    )
    assert_response_success(result)

@pytest.mark.asyncio
async def test_track_record_operations(reaper_mcp_client):
    """Test track record arming operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Arm track for recording
    result = await reaper_mcp_client.call_tool(
        "set_track_record_armed",
        {"track_index": track_index, "armed": True}
    )
    print(f"Arm track result: {result}")
    assert_response_success(result)
    
    # Get track record armed state
    result = await reaper_mcp_client.call_tool(
        "get_track_record_armed",
        {"track_index": track_index}
    )
    print(f"Get track armed state result: {result}")
    assert_response_contains(result, "armed")
    
    # Disarm track
    result = await reaper_mcp_client.call_tool(
        "set_track_record_armed",
        {"track_index": track_index, "armed": False}
    )
    assert_response_success(result)

@pytest.mark.asyncio
async def test_track_error_handling(reaper_mcp_client):
    """Test error handling for volume/pan operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Test setting volume on non-existent track
    result = await reaper_mcp_client.call_tool(
        "set_track_volume",
        {"track_index": 999, "volume": 0.5}
    )
    assert "failed" in result.content[0].text.lower() or "error" in result.content[0].text.lower()
    
    # Test getting pan on non-existent track
    result = await reaper_mcp_client.call_tool(
        "get_track_pan",
        {"track_index": 999}
    )
    assert "failed" in result.content[0].text.lower() or "error" in result.content[0].text.lower()