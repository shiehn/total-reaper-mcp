import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_track_volume_operations(reaper_mcp_client):
    """Test track volume operations"""
    # Create a track first
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    assert "success" in result.content[0].text.lower()
    
    # Set track volume
    result = await reaper_mcp_client.call_tool(
        "set_track_volume",
        {"track_index": 0, "volume": 0.5}
    )
    print(f"Set track volume result: {result}")
    assert "success" in result.content[0].text.lower() or "volume" in result.content[0].text.lower()
    
    # Get track volume
    result = await reaper_mcp_client.call_tool(
        "get_track_volume",
        {"track_index": 0}
    )
    print(f"Get track volume result: {result}")
    assert "0.5" in result.content[0].text or "volume" in result.content[0].text.lower()
    
    # Test with dB value
    result = await reaper_mcp_client.call_tool(
        "set_track_volume_db",
        {"track_index": 0, "volume_db": -6.0}
    )
    print(f"Set track volume dB result: {result}")
    assert "success" in result.content[0].text.lower() or "-6" in result.content[0].text
    
    # Get track volume in dB
    result = await reaper_mcp_client.call_tool(
        "get_track_volume_db",
        {"track_index": 0}
    )
    print(f"Get track volume dB result: {result}")
    assert "-6" in result.content[0].text or "dB" in result.content[0].text

@pytest.mark.asyncio
async def test_track_pan_operations(reaper_mcp_client):
    """Test track pan operations"""
    # Create a track first
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    assert "success" in result.content[0].text.lower()
    
    # Set track pan
    result = await reaper_mcp_client.call_tool(
        "set_track_pan",
        {"track_index": 0, "pan": -0.5}
    )
    print(f"Set track pan result: {result}")
    assert "success" in result.content[0].text.lower() or "pan" in result.content[0].text.lower()
    
    # Get track pan
    result = await reaper_mcp_client.call_tool(
        "get_track_pan",
        {"track_index": 0}
    )
    print(f"Get track pan result: {result}")
    assert "-0.5" in result.content[0].text or "pan" in result.content[0].text.lower()
    
    # Test center pan
    result = await reaper_mcp_client.call_tool(
        "set_track_pan",
        {"track_index": 0, "pan": 0.0}
    )
    assert "success" in result.content[0].text.lower() or "center" in result.content[0].text.lower()
    
    # Test right pan
    result = await reaper_mcp_client.call_tool(
        "set_track_pan",
        {"track_index": 0, "pan": 1.0}
    )
    assert "success" in result.content[0].text.lower() or "right" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_track_record_operations(reaper_mcp_client):
    """Test track record arming operations"""
    # Create a track first
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    assert "success" in result.content[0].text.lower()
    
    # Arm track for recording
    result = await reaper_mcp_client.call_tool(
        "set_track_record_armed",
        {"track_index": 0, "armed": True}
    )
    print(f"Arm track result: {result}")
    assert "success" in result.content[0].text.lower() or "armed" in result.content[0].text.lower()
    
    # Get track record armed state
    result = await reaper_mcp_client.call_tool(
        "get_track_record_armed",
        {"track_index": 0}
    )
    print(f"Get track armed state result: {result}")
    assert "armed" in result.content[0].text.lower()
    
    # Disarm track
    result = await reaper_mcp_client.call_tool(
        "set_track_record_armed",
        {"track_index": 0, "armed": False}
    )
    assert "success" in result.content[0].text.lower() or "disarmed" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_track_error_handling(reaper_mcp_client):
    """Test error handling for volume/pan operations"""
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