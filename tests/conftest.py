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
    # Check which server to use
    bridge_type = os.environ.get('BRIDGE_TYPE', 'file').lower()
    
    if bridge_type == 'registry':
        server_module = "server.app_file_bridge_registry"
    elif bridge_type == 'file':
        server_module = "server.app_file_bridge_full"
    else:
        server_module = "server.app"
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", server_module],
        env=None
    )
    
    async with MCPClientManager(server_params) as session:
        yield session