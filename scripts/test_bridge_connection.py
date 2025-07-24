#!/usr/bin/env python3
"""
Quick script to test if the bridge is responding
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from server.bridge import ReaperFileBridge

async def test_bridge():
    bridge = ReaperFileBridge()
    
    print("Testing bridge connection...")
    
    # Test 1: Basic function
    try:
        result = await bridge.call_lua("CountTracks", [0])
        print(f"✓ CountTracks: {result}")
    except Exception as e:
        print(f"✗ CountTracks failed: {e}")
    
    # Test 2: DSL function
    try:
        result = await bridge.call_lua("GetAllTracksInfo", [])
        if result.get("ok"):
            print(f"✓ GetAllTracksInfo: Found {len(result.get('tracks', []))} tracks")
        else:
            print(f"✗ GetAllTracksInfo: {result}")
    except Exception as e:
        print(f"✗ GetAllTracksInfo failed: {e}")
    
    # Test 3: Another DSL function
    try:
        result = await bridge.call_lua("GetCursorPosition", [])
        print(f"✓ GetCursorPosition: {result}")
    except Exception as e:
        print(f"✗ GetCursorPosition failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_bridge())