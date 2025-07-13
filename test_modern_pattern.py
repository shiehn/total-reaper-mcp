#!/usr/bin/env python3
"""
Test script to verify the modern MCP pattern works
"""

import asyncio
import sys
from pathlib import Path

# Add the server directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "server"))

async def test_modern_server():
    """Test that the modern server can be imported and initialized"""
    try:
        # Import the modern server
        from app_modern_simple import mcp, bridge
        
        print("✅ Successfully imported modern MCP server")
        
        # List all registered tools
        tools = []
        if hasattr(mcp, '_tools'):
            tools = list(mcp._tools.keys())
        elif hasattr(mcp, 'list_tools'):
            # Try to get tools through list_tools if available
            tool_list = await mcp.list_tools()
            tools = [t.name for t in tool_list] if tool_list else []
        
        print(f"\n📦 Registered tools ({len(tools)}):")
        for tool in tools:
            print(f"  - {tool}")
        
        # Test bridge connection (without actually calling REAPER)
        print(f"\n🌉 Bridge configured at: {bridge.bridge_dir}")
        
        print("\n✅ Modern pattern validation successful!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nThis might be because FastMCP is not available in the current MCP version.")
        print("You may need to update MCP: pip install mcp>=2.0.0")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_modern_server())