import pytest
import pytest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@pytest_asyncio.fixture
async def reaper_mcp_client():
    """Create an MCP client connected to the REAPER server"""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "server.app"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session

@pytest.mark.asyncio
async def test_full_api_availability(reaper_mcp_client):
    """Test that all ReaScript API methods are available"""
    tools = await reaper_mcp_client.list_tools()
    tool_names = [tool.name for tool in tools]
    
    # Check that we have a substantial number of tools
    assert len(tool_names) > 90, f"Expected 90+ tools, got {len(tool_names)}"
    
    # Check some key methods exist
    essential_methods = [
        "count_tracks", "get_track", "set_track_name",
        "add_media_item_to_track", "create_midi_item",
        "midi_insert_note", "play", "stop",
        "get_project_name", "save_project"
    ]
    
    for method in essential_methods:
        assert method in tool_names, f"Missing essential method: {method}"

@pytest.mark.asyncio
async def test_midi_workflow(reaper_mcp_client):
    """Test complete MIDI workflow"""
    # Create track
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "use_defaults": True}
    )
    assert "Success" in result.content[0].text or "success" in result.content[0].text
    
    # Set track name
    result = await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 0, "name": "Test MIDI Track"}
    )
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "start_time": 0.0, "end_time": 4.0}
    )
    
    print(f"MIDI workflow test completed")
