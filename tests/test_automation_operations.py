import pytest
import pytest_asyncio
from .test_utils import (
    ensure_clean_project,
    create_track_with_verification,
    assert_response_contains,
    assert_response_success,
    extract_number_from_response
)

def assert_tools_available(available_tools, required_tools):
    """Assert that all required tools are available, failing with clear message if not"""
    for tool in required_tools:
        assert tool in available_tools, f"MISSING IMPLEMENTATION: Tool '{tool}' is not implemented in the server but is required for automation functionality"

@pytest.mark.asyncio
async def test_track_automation_mode(reaper_mcp_client):
    """Test track automation mode operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    print(f"Created track at index: {track_index}")
    
    # Get initial automation mode
    result = await reaper_mcp_client.call_tool(
        "get_track_automation_mode",
        {"track_index": track_index}
    )
    print(f"Get automation mode result: {result}")
    assert_response_contains(result, "automation mode:")
    
    # Set to read mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": track_index, "mode": 1}  # 1 = Read
    )
    print(f"Set automation mode result: {result}")
    assert_response_contains(result, "to Read mode")
    
    # Set to write mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": track_index, "mode": 3}  # 3 = Write
    )
    assert_response_contains(result, "to Write mode")
    
    # Set to touch mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": track_index, "mode": 2}  # 2 = Touch
    )
    assert_response_contains(result, "to Touch mode")
    
    # Set to trim/read mode
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": track_index, "mode": 0}  # 0 = Trim/Read
    )
    assert_response_contains(result, "to Trim/Read mode")

@pytest.mark.asyncio 
async def test_global_automation_override(reaper_mcp_client):
    """Test global automation override"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Get current override state
    result = await reaper_mcp_client.call_tool(
        "get_global_automation_override",
        {}
    )
    print(f"Get global automation override result: {result}")
    assert_response_contains(result, "Global automation override:")
    
    # Set to bypass
    result = await reaper_mcp_client.call_tool(
        "set_global_automation_override",
        {"mode": 1}  # 1 = Bypass
    )
    print(f"Set bypass result: {result}")
    assert_response_contains(result, "Bypass all automation")
    
    # Set to off (no override)
    result = await reaper_mcp_client.call_tool(
        "set_global_automation_override",
        {"mode": 0}  # 0 = No override
    )
    assert_response_contains(result, "No override")

@pytest.mark.asyncio
async def test_automation_error_handling(reaper_mcp_client):
    """Test error handling for automation operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
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