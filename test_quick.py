#!/usr/bin/env python3
"""Quick test to verify MCP bridge is working"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import sys

async def test_basic_operations():
    """Test basic REAPER operations through MCP"""
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "server.app"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as client:
            # Initialize
            await client.initialize()
            
            print("=== Testing Basic Operations ===")
            
            # Test 1: Get master track
            print("\n1. Getting master track...")
            result = await client.call_tool("get_master_track", {})
            print(f"   Result: {result.content[0].text}")
            
            # Test 2: Insert a track
            print("\n2. Inserting a track...")
            result = await client.call_tool("insert_track", {"index": 0, "use_defaults": True})
            print(f"   Result: {result.content[0].text}")
            
            # Test 3: Set track name
            print("\n3. Setting track name...")
            result = await client.call_tool("set_track_name", {"track_index": 0, "name": "Test Track"})
            print(f"   Result: {result.content[0].text}")
            
            # Test 4: Get track name
            print("\n4. Getting track name...")
            result = await client.call_tool("get_track_name", {"track_index": 0})
            print(f"   Result: {result.content[0].text}")
            
            # Test 5: Count tracks
            print("\n5. Counting tracks...")
            result = await client.call_tool("get_track_count", {})
            print(f"   Result: {result.content[0].text}")
            
            print("\n=== All tests completed! ===")
        
if __name__ == "__main__":
    asyncio.run(test_basic_operations())