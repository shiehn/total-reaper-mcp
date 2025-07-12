import pytest
import pytest_asyncio
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import subprocess
import time

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
async def test_insert_track(reaper_mcp_client):
    """Test inserting a track at index 0"""
    # First, get initial track count
    result = await reaper_mcp_client.call_tool(
        "get_track_count",
        {}
    )
    print(f"Initial track count result: {result}")
    
    # Insert a new track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    print(f"Insert track result: {result}")
    assert result.content[0].text == "Successfully inserted track at index 0"
    
    # Verify track count increased
    result = await reaper_mcp_client.call_tool(
        "get_track_count",
        {}
    )
    print(f"Final track count result: {result}")

@pytest.mark.asyncio
async def test_get_reaper_version(reaper_mcp_client):
    """Test getting REAPER version"""
    result = await reaper_mcp_client.call_tool(
        "get_reaper_version",
        {}
    )
    print(f"REAPER version result: {result}")
    assert "REAPER version:" in result.content[0].text

@pytest.mark.asyncio
async def test_get_track(reaper_mcp_client):
    """Test getting a track by index"""
    # First ensure we have at least one track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Get the track at index 0
    result = await reaper_mcp_client.call_tool(
        "get_track",
        {"index": 0}
    )
    print(f"Get track result: {result}")
    assert "Track at index 0:" in result.content[0].text
    
    # Try to get a non-existent track
    result = await reaper_mcp_client.call_tool(
        "get_track",
        {"index": 999}
    )
    print(f"Get non-existent track result: {result}")
    assert "No track found at index 999" in result.content[0].text

@pytest.mark.asyncio
async def test_list_tools(reaper_mcp_client):
    """Test listing available tools"""
    tools = await reaper_mcp_client.list_tools()
    tool_names = [tool.name for tool in tools]
    
    assert "insert_track" in tool_names
    assert "get_track_count" in tool_names
    assert "get_reaper_version" in tool_names
    assert "get_track" in tool_names
    
    # Verify tool schemas
    insert_track_tool = next(t for t in tools if t.name == "insert_track")
    assert "index" in insert_track_tool.inputSchema["properties"]
    assert "use_defaults" in insert_track_tool.inputSchema["properties"]
    
    get_track_tool = next(t for t in tools if t.name == "get_track")
    assert "index" in get_track_tool.inputSchema["properties"]