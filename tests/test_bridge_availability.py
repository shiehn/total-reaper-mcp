import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_bridge_functions_availability(reaper_mcp_client):
    """Test which bridge functions are available in the current bridge."""
    
    # Test functions that should work
    test_functions = [
        # Core functions that should always work
        ("get_app_version", {}, "Core function"),
        ("count_tracks", {}, "Core function"),
        
        # Our new functions - check if bridge was updated
        ("get_bridge_version", {}, "New function - bridge version check"),
        
        # Functions we know work from test results
        ("undo_begin_block2", {"project_index": 0}, "Working function"),
        ("undo_end_block2", {"desc": "Test", "extra_flags": 0}, "Working function"),
        
        # Index-based functions that might not be recognized
        ("set_track_volume", {"track_index": 0, "volume_db": 0}, "New index-based function"),
        ("set_media_item_position", {"item_index": 0, "position": 0}, "New index-based function"),
        ("set_media_item_length", {"item_index": 0, "length": 1}, "New index-based function"),
    ]
    
    results = []
    for tool_name, params, description in test_functions:
        try:
            result = await reaper_mcp_client.call_tool(tool_name, params)
            status = "SUCCESS"
            details = ""
            if tool_name == "get_bridge_version":
                details = f" - Version: {result.content[0].text}"
            results.append(f"✓ {tool_name} ({description}): {status}{details}")
        except Exception as e:
            error_msg = str(e)
            if "Unknown function" in error_msg:
                status = "UNKNOWN FUNCTION IN BRIDGE"
            elif "Unknown tool" in error_msg:
                status = "UNKNOWN TOOL"
            elif "not found" in error_msg.lower():
                status = "RESOURCE NOT FOUND"
            else:
                status = f"ERROR: {error_msg}"
            results.append(f"✗ {tool_name} ({description}): {status}")
    
    # Print all results
    print("\n\nBRIDGE FUNCTION AVAILABILITY TEST RESULTS:")
    print("=" * 60)
    for result in results:
        print(result)
    print("=" * 60)
    
    # Also test a few bridge functions directly via Lua
    print("\n\nDIRECT BRIDGE FUNCTION TESTS:")
    print("=" * 60)
    
    # Test if SetTrackVolumeByIndex exists
    from server.bridge import bridge
    try:
        # Call a function we know exists
        result = await bridge.call_lua("GetAppVersion", [])
        print(f"✓ GetAppVersion (direct): {result}")
    except Exception as e:
        print(f"✗ GetAppVersion (direct): {e}")
    
    try:
        # Test our new function
        result = await bridge.call_lua("GetBridgeVersion", [])
        print(f"✓ GetBridgeVersion (direct): {result}")
    except Exception as e:
        print(f"✗ GetBridgeVersion (direct): {e}")
        
    try:
        # Test SetTrackVolumeByIndex
        result = await bridge.call_lua("SetTrackVolumeByIndex", [0, "D_VOL", 1.0])
        print(f"✓ SetTrackVolumeByIndex (direct): {result}")
    except Exception as e:
        print(f"✗ SetTrackVolumeByIndex (direct): {e}")
    
    print("=" * 60)