import pytest
import pytest_asyncio
import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def reaper_mcp_client():
    """Create an MCP client connected to the REAPER server"""
    # Check if we should use the file-based server
    use_file_bridge = os.environ.get('USE_FILE_BRIDGE', 'true').lower() == 'true'
    
    if use_file_bridge:
        server_module = "server.app_file_bridge_full"
    else:
        server_module = "server.app"
    
    server_params = StdioServerParameters(
        command="python",
        args=["-m", server_module],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session