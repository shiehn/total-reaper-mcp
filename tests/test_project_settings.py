import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_project_sample_rate(reaper_mcp_client):
    """Test project sample rate operations"""
    # Get current sample rate
    result = await reaper_mcp_client.call_tool(
        "get_project_sample_rate",
        {}
    )
    print(f"Get sample rate result: {result}")
    assert "hz" in result.content[0].text.lower() or "sample rate" in result.content[0].text.lower()
    
    # Set sample rate to 48000
    result = await reaper_mcp_client.call_tool(
        "set_project_sample_rate",
        {"sample_rate": 48000}
    )
    print(f"Set sample rate result: {result}")
    assert "success" in result.content[0].text.lower() or "48000" in result.content[0].text
    
    # Verify sample rate was set
    result = await reaper_mcp_client.call_tool(
        "get_project_sample_rate",
        {}
    )
    assert "48000" in result.content[0].text
    
    # Set back to 44100
    result = await reaper_mcp_client.call_tool(
        "set_project_sample_rate",
        {"sample_rate": 44100}
    )
    assert "success" in result.content[0].text.lower() or "44100" in result.content[0].text

@pytest.mark.asyncio
async def test_project_length_operations(reaper_mcp_client):
    """Test project length operations"""
    # Get current project length
    result = await reaper_mcp_client.call_tool(
        "get_project_length",
        {}
    )
    print(f"Get project length result: {result}")
    assert "seconds" in result.content[0].text.lower() or "length" in result.content[0].text.lower()
    
    # Set project length
    result = await reaper_mcp_client.call_tool(
        "set_project_length",
        {"length": 300.0}  # 5 minutes
    )
    print(f"Set project length result: {result}")
    assert "success" in result.content[0].text.lower() or "300" in result.content[0].text

@pytest.mark.asyncio
async def test_project_grid_settings(reaper_mcp_client):
    """Test project grid settings"""
    # Get current grid division
    result = await reaper_mcp_client.call_tool(
        "get_project_grid_division",
        {}
    )
    print(f"Get grid division result: {result}")
    assert "grid" in result.content[0].text.lower() or "/" in result.content[0].text
    
    # Set grid to 1/16
    result = await reaper_mcp_client.call_tool(
        "set_project_grid_division",
        {"division": 0.0625}  # 1/16
    )
    print(f"Set grid division result: {result}")
    assert "success" in result.content[0].text.lower() or "1/16" in result.content[0].text or "0.0625" in result.content[0].text

@pytest.mark.asyncio
async def test_project_render_settings(reaper_mcp_client):
    """Test project render settings"""
    # Get render bounds
    result = await reaper_mcp_client.call_tool(
        "get_project_render_bounds",
        {}
    )
    print(f"Get render bounds result: {result}")
    assert "bounds" in result.content[0].text.lower() or "render" in result.content[0].text.lower()
    
    # Set render bounds to time selection
    result = await reaper_mcp_client.call_tool(
        "set_project_render_bounds",
        {"bounds_mode": 1}  # 1 = Time selection
    )
    print(f"Set render bounds result: {result}")
    assert "success" in result.content[0].text.lower() or "time selection" in result.content[0].text.lower()
    
    # Set render bounds to entire project
    result = await reaper_mcp_client.call_tool(
        "set_project_render_bounds",
        {"bounds_mode": 0}  # 0 = Entire project
    )
    assert "success" in result.content[0].text.lower() or "entire project" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_project_notes(reaper_mcp_client):
    """Test project notes operations"""
    # Set project notes
    test_notes = "Test project created for REAPER MCP testing"
    result = await reaper_mcp_client.call_tool(
        "set_project_notes",
        {"notes": test_notes}
    )
    print(f"Set project notes result: {result}")
    assert "success" in result.content[0].text.lower() or "notes" in result.content[0].text.lower()
    
    # Get project notes
    result = await reaper_mcp_client.call_tool(
        "get_project_notes",
        {}
    )
    print(f"Get project notes result: {result}")
    assert test_notes in result.content[0].text or "notes" in result.content[0].text.lower()