#!/usr/bin/env python3
"""Test script to verify which bridge functions are available."""

import asyncio
import sys
sys.path.append('.')
from tests.conftest import get_test_client

async def test_bridge_functions():
    """Test which bridge functions are available in the current bridge."""
    
    client = await get_test_client()
    async with client:
            # Test functions that should work
            test_functions = [
                # Core functions that should always work
                ("get_app_version", {}, "Core function"),
                ("count_tracks", {}, "Core function"),
                
                # Our new functions
                ("get_bridge_version", {}, "New function"),
                ("set_track_volume", {"track_index": 0, "volume_db": 0}, "New index-based function"),
                ("set_media_item_position", {"item_index": 0, "position": 0}, "New index-based function"),
                
                # Functions we know work from test results
                ("undo_begin_block2", {"project_index": 0}, "Working function"),
                ("undo_end_block2", {"desc": "Test", "extra_flags": 0}, "Working function"),
            ]
            
            for tool_name, params, description in test_functions:
                try:
                    result = await client.call_tool(tool_name, params)
                    print(f"✓ {tool_name} ({description}): SUCCESS")
                    if tool_name == "get_bridge_version":
                        print(f"  Bridge version: {result.content[0].text}")
                except Exception as e:
                    error_msg = str(e)
                    if "Unknown function" in error_msg:
                        print(f"✗ {tool_name} ({description}): UNKNOWN FUNCTION")
                    elif "Unknown tool" in error_msg:
                        print(f"✗ {tool_name} ({description}): UNKNOWN TOOL")
                    else:
                        print(f"✗ {tool_name} ({description}): {error_msg}")

if __name__ == "__main__":
    asyncio.run(test_bridge_functions())