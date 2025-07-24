#!/usr/bin/env python3
"""
Check which version of the bridge is running
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from server.bridge import ReaperFileBridge

async def check_version():
    bridge = ReaperFileBridge()
    
    print("Checking bridge version...")
    
    # The v3 bridge should have DSL functions
    # Test for a DSL-specific function
    try:
        result = await bridge.call_lua("GetAllTracksInfo", [])
        if "Unknown function" in str(result.get("error", "")):
            print("❌ Bridge version: v2 (original) - DSL functions NOT available")
            print("   Please reload the bridge in REAPER:")
            print("   1. Open REAPER")
            print("   2. Open Actions list (Actions menu)")
            print("   3. Find and run 'mcp_bridge_file_v2.lua'")
            print("   OR")
            print("   4. Restart REAPER")
        else:
            print("✅ Bridge version: v3 (with DSL) - DSL functions available")
    except Exception as e:
        print(f"❓ Could not determine version: {e}")
        print("   Is REAPER running with the bridge loaded?")

if __name__ == "__main__":
    asyncio.run(check_version())