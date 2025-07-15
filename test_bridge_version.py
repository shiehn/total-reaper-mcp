#!/usr/bin/env python3
"""Quick test to check if bridge is updated."""

import asyncio
from server.bridge import bridge

async def test_bridge_version():
    try:
        result = await bridge.call_lua("GetBridgeVersion", [])
        print(f"Bridge version: {result.get('ret', 'Unknown')}")
        if result.get('ret') == "2024-07-14-20:15":
            print("✓ Bridge has been successfully updated!")
        else:
            print("✗ Bridge is still using old version. Please reload mcp_bridge_file_v2.lua in REAPER")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_bridge_version())