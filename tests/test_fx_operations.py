import pytest
import pytest_asyncio

def assert_tools_available(available_tools, required_tools):
    """Assert that all required tools are available, failing with clear message if not"""
    for tool in required_tools:
        assert tool in available_tools, f"MISSING IMPLEMENTATION: Tool '{tool}' is not implemented in the server but is required for FX functionality"

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
        "track_fx_add_by_name",
        {"track_index": 0, "fx_name": "ReaEQ"}
    )
    print(f"Add FX result: {result}")
    assert "Added" in result.content[0].text and "to track" in result.content[0].text
    
    # Count FX on track
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_count",
        {"track_index": 0}
    )
    print(f"Count FX result: {result}")
    assert "has 1 FX" in result.content[0].text
    
    # Get FX name
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_name",
        {"track_index": 0, "fx_index": 0}
    )
    print(f"Get FX name result: {result}")
    assert "ReaEQ" in result.content[0].text or "fx" in result.content[0].text.lower()
    
    # Enable/disable FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_set_enabled",
        {"track_index": 0, "fx_index": 0, "enabled": False}
    )
    print(f"Disable FX result: {result}")
    assert "disabled" in result.content[0].text
    
    # Get FX enabled state
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_enabled",
        {"track_index": 0, "fx_index": 0}
    )
    print(f"Get FX enabled state result: {result}")
    assert "disabled" in result.content[0].text.lower() or "false" in result.content[0].text.lower()
    
    # Re-enable FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_set_enabled",
        {"track_index": 0, "fx_index": 0, "enabled": True}
    )
    assert "enabled" in result.content[0].text
    
    # Delete FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_delete",
        {"track_index": 0, "fx_index": 0}
    )
    print(f"Delete FX result: {result}")
    assert "Deleted FX" in result.content[0].text

@pytest.mark.asyncio
async def test_fx_error_handling(reaper_mcp_client):
    """Test error handling for FX operations"""
    # Try to add FX to non-existent track
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 999, "fx_name": "ReaEQ"}
    )
    assert "failed" in result.content[0].text.lower() or "error" in result.content[0].text.lower()
    
    # Try to get FX from empty track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_name",
        {"track_index": 0, "fx_index": 0}
    )
    assert "no fx" in result.content[0].text.lower() or "not found" in result.content[0].text.lower() or "error" in result.content[0].text.lower()