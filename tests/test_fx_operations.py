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
        assert tool in available_tools, f"MISSING IMPLEMENTATION: Tool '{tool}' is not implemented in the server but is required for FX functionality"

@pytest.mark.asyncio
async def test_track_fx_operations(reaper_mcp_client):
    """Test track FX operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    print(f"Created track at index: {track_index}")
    
    # Add FX to track
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": track_index, "fx_name": "ReaEQ"}
    )
    print(f"Add FX result: {result}")
    
    # Check if FX was added (might fail if ReaEQ not available)
    if "failed to add" in result.content[0].text.lower():
        pytest.skip("ReaEQ not available in test environment")
    
    assert_response_success(result)
    
    # Count FX on track
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_count",
        {"track_index": track_index}
    )
    print(f"Count FX result: {result}")
    fx_count = extract_number_from_response(result.content[0].text, r'has (\d+) FX')
    assert fx_count >= 1, f"Expected at least 1 FX, got {fx_count}"
    
    # Get FX name
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_name",
        {"track_index": track_index, "fx_index": 0}
    )
    print(f"Get FX name result: {result}")
    # FX name might vary, just check it's not an error
    assert "error" not in result.content[0].text.lower()
    
    # Enable/disable FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_set_enabled",
        {"track_index": track_index, "fx_index": 0, "enabled": False}
    )
    print(f"Disable FX result: {result}")
    assert_response_contains(result, "disabled")
    
    # Get FX enabled state
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_enabled",
        {"track_index": track_index, "fx_index": 0}
    )
    print(f"Get FX enabled state result: {result}")
    assert_response_contains(result, "disabled")
    
    # Re-enable FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_set_enabled",
        {"track_index": track_index, "fx_index": 0, "enabled": True}
    )
    assert_response_contains(result, "enabled")
    
    # Delete FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_delete",
        {"track_index": track_index, "fx_index": 0}
    )
    print(f"Delete FX result: {result}")
    assert_response_success(result)
    
    # Verify FX was deleted
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_count",
        {"track_index": track_index}
    )
    fx_count = extract_number_from_response(result.content[0].text, r'has (\d+) FX')
    assert fx_count == 0, f"Expected 0 FX after deletion, got {fx_count}"

@pytest.mark.asyncio
async def test_fx_error_handling(reaper_mcp_client):
    """Test error handling for FX operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Try to add FX to non-existent track
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 999, "fx_name": "ReaEQ"}
    )
    assert "failed" in result.content[0].text.lower() or "error" in result.content[0].text.lower()
    
    # Create a track for further tests
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Try to get FX from empty track
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_name",
        {"track_index": track_index, "fx_index": 0}
    )
    # Should either error or indicate no FX
    assert any(word in result.content[0].text.lower() for word in ["no fx", "not found", "error", "failed"])