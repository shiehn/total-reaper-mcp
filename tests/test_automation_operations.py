import pytest
import pytest_asyncio

def assert_tools_available(available_tools, required_tools):
    """Assert that all required tools are available, failing with clear message if not"""
    for tool in required_tools:
        assert tool in available_tools, f"MISSING IMPLEMENTATION: Tool '{tool}' is not implemented in the server but is required for automation functionality"

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
    assert "automation mode:" in result.content[0].text
    
    # Set to read mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 1}  # 1 = Read
    )
    print(f"Set automation mode result: {result}")
    assert "to Read mode" in result.content[0].text
    
    # Set to write mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 3}  # 3 = Write
    )
    assert "to Write mode" in result.content[0].text
    
    # Set to touch mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 2}  # 2 = Touch
    )
    assert "to Touch mode" in result.content[0].text
    
    # Set to trim/read mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 0}  # 0 = Trim/Read
    )
    assert "to Trim/Read mode" in result.content[0].text

@pytest.mark.asyncio 
async def test_global_automation_override(reaper_mcp_client):
    """Test global automation override"""
    # Get current override state
    result = await reaper_mcp_client.call_tool(
        "get_global_automation_override",
        {}
    )
    print(f"Get global automation override result: {result}")
    assert "Global automation override:" in result.content[0].text
    
    # Set to bypass
    result = await reaper_mcp_client.call_tool(
        "set_global_automation_override",
        {"mode": 1}  # 1 = Bypass
    )
    print(f"Set bypass result: {result}")
    assert "Bypass all automation" in result.content[0].text
    
    # Set to off (no override)
    result = await reaper_mcp_client.call_tool(
        "set_global_automation_override",
        {"mode": 0}  # 0 = No override
    )
    assert "No override" in result.content[0].text

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