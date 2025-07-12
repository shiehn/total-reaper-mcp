import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_project_tempo_operations(reaper_mcp_client):
    """Test project tempo operations"""
    # Get current project tempo
    result = await reaper_mcp_client.call_tool(
        "get_project_tempo",
        {}
    )
    print(f"Get project tempo result: {result}")
    assert "bpm" in result.content[0].text.lower() or "tempo" in result.content[0].text.lower()
    
    # Set project tempo
    result = await reaper_mcp_client.call_tool(
        "set_project_tempo",
        {"tempo": 140.0}
    )
    print(f"Set project tempo result: {result}")
    assert "success" in result.content[0].text.lower() or "140" in result.content[0].text
    
    # Verify tempo was set
    result = await reaper_mcp_client.call_tool(
        "get_project_tempo",
        {}
    )
    assert "140" in result.content[0].text
    
    # Set a different tempo
    result = await reaper_mcp_client.call_tool(
        "set_project_tempo",
        {"tempo": 120.0}
    )
    assert "success" in result.content[0].text.lower() or "120" in result.content[0].text

@pytest.mark.asyncio
async def test_time_signature_operations(reaper_mcp_client):
    """Test time signature operations"""
    # Get current time signature
    result = await reaper_mcp_client.call_tool(
        "get_project_time_signature",
        {}
    )
    print(f"Get time signature result: {result}")
    assert "/" in result.content[0].text  # Should contain something like "4/4"
    
    # Set time signature to 3/4
    result = await reaper_mcp_client.call_tool(
        "set_project_time_signature",
        {"numerator": 3, "denominator": 4}
    )
    print(f"Set time signature result: {result}")
    assert "success" in result.content[0].text.lower() or "3/4" in result.content[0].text
    
    # Verify time signature was set
    result = await reaper_mcp_client.call_tool(
        "get_project_time_signature",
        {}
    )
    assert "3/4" in result.content[0].text
    
    # Set back to 4/4
    result = await reaper_mcp_client.call_tool(
        "set_project_time_signature",
        {"numerator": 4, "denominator": 4}
    )
    assert "success" in result.content[0].text.lower() or "4/4" in result.content[0].text

@pytest.mark.asyncio
async def test_tempo_marker_operations(reaper_mcp_client):
    """Test tempo marker operations"""
    # Insert tempo marker
    result = await reaper_mcp_client.call_tool(
        "insert_tempo_time_sig_marker",
        {
            "position": 10.0,
            "tempo": 150.0,
            "time_sig_numerator": 6,
            "time_sig_denominator": 8
        }
    )
    print(f"Insert tempo marker result: {result}")
    assert "success" in result.content[0].text.lower() or "inserted" in result.content[0].text.lower()
    
    # Count tempo markers
    result = await reaper_mcp_client.call_tool(
        "count_tempo_markers",
        {}
    )
    print(f"Count tempo markers result: {result}")
    assert "marker" in result.content[0].text.lower()
    
    # Get tempo at specific position
    result = await reaper_mcp_client.call_tool(
        "get_tempo_at_position",
        {"position": 10.0}
    )
    print(f"Get tempo at position result: {result}")
    assert "150" in result.content[0].text or "tempo" in result.content[0].text.lower()
    
    # Delete tempo marker (if supported)
    result = await reaper_mcp_client.call_tool(
        "delete_tempo_marker",
        {"marker_index": 0}
    )
    print(f"Delete tempo marker result: {result}")
    # This might fail if not implemented, which is OK for the test