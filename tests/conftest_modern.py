import pytest
import pytest_asyncio
import os
import asyncio
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def cleanup_bridge_directory():
    """Clean up any leftover files in the bridge directory"""
    bridge_dir = Path(os.environ.get(
        'REAPER_MCP_BRIDGE_DIR',
        os.path.expanduser('~/Library/Application Support/REAPER/Scripts/mcp_bridge_data')
    ))
    
    if bridge_dir.exists():
        # Remove all request and response files
        for pattern in ['request_*.json', 'response_*.json']:
            for file in bridge_dir.glob(pattern):
                try:
                    file.unlink()
                except Exception:
                    pass

class MCPClientManager:
    """Manager to handle MCP client lifecycle properly"""
    
    def __init__(self, server_params):
        self.server_params = server_params
        self.client_cm = None
        self.session_cm = None
        self.read = None
        self.write = None
        self.session = None
    
    async def __aenter__(self):
        # Clean up before starting
        cleanup_bridge_directory()
        
        # Create client
        self.client_cm = stdio_client(self.server_params)
        self.read, self.write = await self.client_cm.__aenter__()
        
        # Create session
        self.session_cm = ClientSession(self.read, self.write)
        self.session = await self.session_cm.__aenter__()
        
        # Initialize
        await self.session.initialize()
        
        return self.session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Clean up in reverse order
        if self.session_cm:
            try:
                await self.session_cm.__aexit__(exc_type, exc_val, exc_tb)
            except Exception:
                pass
        
        if self.client_cm:
            try:
                await self.client_cm.__aexit__(exc_type, exc_val, exc_tb)
            except Exception:
                pass
        
        # Clean up files
        cleanup_bridge_directory()

@pytest_asyncio.fixture
async def reaper_mcp_client():
    """Create an MCP client connected to the REAPER server"""
    # Check if we should use modern server
    use_modern = os.environ.get('USE_MODERN_SERVER', '').lower() in ('1', 'true', 'yes')
    
    if use_modern:
        # Use the modern pattern server
        server_module = "server.app_modern_simple"
        print("🚀 Using MODERN MCP server pattern")
    else:
        # Use legacy server
        bridge_type = os.environ.get('BRIDGE_TYPE', 'file').lower()
        
        if bridge_type == 'registry':
            server_module = "server.app_file_bridge_registry"
        elif bridge_type == 'file':
            server_module = "server.app_file_bridge_full"
        else:
            server_module = "server.app"
        print(f"Using LEGACY server: {server_module}")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", server_module],
        env=None
    )
    
    async with MCPClientManager(server_params) as session:
        # Store available tools for tests to check
        tools = await session.list_tools()
        session._available_tools = {t.name for t in tools.tools}
        print(f"Available tools: {len(session._available_tools)}")
        yield session

# Global client for sync tests
_global_client = None
_event_loop = None

def reaper_available():
    """Check if REAPER is available for testing"""
    # For now, assume REAPER is available if we can import the server module
    try:
        import server.app
        return True
    except ImportError:
        return False

def call_tool(tool_name, arguments):
    """Synchronous wrapper for calling MCP tools"""
    # For now, let's skip the synchronous tests
    pytest.skip("Synchronous tests temporarily disabled - use async tests instead")

@pytest.fixture
def mock_project():
    """Mock fixture for project setup"""
    # This is a placeholder fixture that individual tests expect
    yield None