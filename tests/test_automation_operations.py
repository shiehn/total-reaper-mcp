import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_track_automation_mode(reaper_mcp_client):
    """Test track automation mode operations"""
    # Create a track first
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    assert "success" in result.content[0].text.lower()
    
    # Get initial automation mode
    result = await reaper_mcp_client.call_tool(
        "get_track_automation_mode",
        {"track_index": 0}
    )
    print(f"Get automation mode result: {result}")
    assert "mode" in result.content[0].text.lower()
    
    # Set to read mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 1}  # 1 = Read
    )
    print(f"Set automation mode result: {result}")
    assert "success" in result.content[0].text.lower() or "read" in result.content[0].text.lower()
    
    # Set to write mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 3}  # 3 = Write
    )
    assert "success" in result.content[0].text.lower() or "write" in result.content[0].text.lower()
    
    # Set to touch mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 2}  # 2 = Touch
    )
    assert "success" in result.content[0].text.lower() or "touch" in result.content[0].text.lower()
    
    # Set to trim/read mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 0}  # 0 = Trim/Read
    )
    assert "success" in result.content[0].text.lower() or "trim" in result.content[0].text.lower()

@pytest.mark.asyncio 
async def test_global_automation_override(reaper_mcp_client):
    """Test global automation override"""
    # Get current override state
    result = await reaper_mcp_client.call_tool(
        "get_global_automation_override",
        {}
    )
    print(f"Get global automation override result: {result}")
    assert "override" in result.content[0].text.lower() or "mode" in result.content[0].text.lower()
    
    # Set to bypass
    result = await reaper_mcp_client.call_tool(
        "set_global_automation_override",
        {"mode": 1}  # 1 = Bypass
    )
    print(f"Set bypass result: {result}")
    assert "success" in result.content[0].text.lower() or "bypass" in result.content[0].text.lower()
    
    # Set to off (no override)
    result = await reaper_mcp_client.call_tool(
        "set_global_automation_override",
        {"mode": 0}  # 0 = No override
    )
    assert "success" in result.content[0].text.lower() or "off" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_automation_error_handling(reaper_mcp_client):
    """Test error handling for automation operations"""
    # Try to set automation mode on non-existent track
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 999, "mode": 1}
    )
    assert "failed" in result.content[0].text.lower() or "error" in result.content[0].text.lower()
    
    # Try to get automation mode on non-existent track
    result = await reaper_mcp_client.call_tool(
        "get_track_automation_mode",
        {"track_index": 999}
    )
    assert "failed" in result.content[0].text.lower() or "error" in result.content[0].text.lower()