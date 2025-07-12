import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_track_fx_operations(reaper_mcp_client):
    """Test track FX operations"""
    # Create a track first
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    assert "success" in result.content[0].text.lower()
    
    # Add FX to track
    result = await reaper_mcp_client.call_tool(
        "add_fx_to_track",
        {"track_index": 0, "fx_name": "ReaEQ"}
    )
    print(f"Add FX result: {result}")
    assert "success" in result.content[0].text.lower() or "added" in result.content[0].text.lower()
    
    # Count FX on track
    result = await reaper_mcp_client.call_tool(
        "count_track_fx",
        {"track_index": 0}
    )
    print(f"Count FX result: {result}")
    assert "1" in result.content[0].text
    
    # Get FX name
    result = await reaper_mcp_client.call_tool(
        "get_track_fx_name",
        {"track_index": 0, "fx_index": 0}
    )
    print(f"Get FX name result: {result}")
    assert "ReaEQ" in result.content[0].text or "fx" in result.content[0].text.lower()
    
    # Enable/disable FX
    result = await reaper_mcp_client.call_tool(
        "set_track_fx_enabled",
        {"track_index": 0, "fx_index": 0, "enabled": False}
    )
    print(f"Disable FX result: {result}")
    assert "success" in result.content[0].text.lower() or "disabled" in result.content[0].text.lower()
    
    # Get FX enabled state
    result = await reaper_mcp_client.call_tool(
        "get_track_fx_enabled",
        {"track_index": 0, "fx_index": 0}
    )
    print(f"Get FX enabled state result: {result}")
    assert "disabled" in result.content[0].text.lower() or "false" in result.content[0].text.lower()
    
    # Re-enable FX
    result = await reaper_mcp_client.call_tool(
        "set_track_fx_enabled",
        {"track_index": 0, "fx_index": 0, "enabled": True}
    )
    assert "success" in result.content[0].text.lower() or "enabled" in result.content[0].text.lower()
    
    # Delete FX
    result = await reaper_mcp_client.call_tool(
        "delete_track_fx",
        {"track_index": 0, "fx_index": 0}
    )
    print(f"Delete FX result: {result}")
    assert "success" in result.content[0].text.lower() or "deleted" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_fx_error_handling(reaper_mcp_client):
    """Test error handling for FX operations"""
    # Try to add FX to non-existent track
    result = await reaper_mcp_client.call_tool(
        "add_fx_to_track",
        {"track_index": 999, "fx_name": "ReaEQ"}
    )
    assert "failed" in result.content[0].text.lower() or "error" in result.content[0].text.lower()
    
    # Try to get FX from empty track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    result = await reaper_mcp_client.call_tool(
        "get_track_fx_name",
        {"track_index": 0, "fx_index": 0}
    )
    assert "no fx" in result.content[0].text.lower() or "not found" in result.content[0].text.lower() or "error" in result.content[0].text.lower()