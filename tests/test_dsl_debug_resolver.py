"""
Debug test for DSL track name resolution issue
"""

import pytest
import logging
import asyncio
from server.bridge import bridge
from server.dsl.resolvers import resolve_track, _get_track_info

logger = logging.getLogger(__name__)

async def call_dsl_tool(client, tool_name, params):
    """Helper to call DSL tools and return the text response"""
    result = await client.call_tool(tool_name, params)
    return result.content[0].text if result.content else ""

@pytest.mark.asyncio
async def test_track_resolution_debug(reaper_mcp_client):
    """Debug track name resolution"""
    # Create a track with a unique name
    unique_name = "DebugTestTrack"
    
    create_result = await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": unique_name})
    print(f"\n1. Create result: {create_result}")
    
    # List tracks to confirm it exists
    tracks = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
    print(f"\n2. Track list: {tracks}")
    
    # Try to get track info directly via bridge
    print("\n3. Testing direct bridge calls:")
    
    # Get track count
    count_result = await bridge.call_lua("GetTrackCount", [])
    print(f"   Track count result: {count_result}")
    
    # Get info for first track
    info_result = await bridge.call_lua("GetTrackInfo", [0])
    print(f"   Track 0 info result: {info_result}")
    
    # Get all tracks info
    all_tracks_result = await bridge.call_lua("GetAllTracksInfo", [])
    print(f"   All tracks (first 3): {all_tracks_result.get('tracks', [])[:3] if all_tracks_result.get('ok') else all_tracks_result}")
    
    # Try the resolver's _get_track_info
    print("\n4. Testing resolver functions:")
    track_info = await _get_track_info(bridge, 0)
    print(f"   Resolver track info: {track_info}")
    
    # Try to resolve by name
    print(f"\n5. Trying to resolve track by name '{unique_name}':")
    try:
        resolved = await resolve_track(bridge, unique_name)
        print(f"   Resolved successfully: {resolved}")
    except Exception as e:
        print(f"   Resolution failed: {e}")
        
        # Try different variations
        print("\n6. Trying variations:")
        for variation in [{"name": unique_name}, {"index": 0}, 0]:
            try:
                resolved = await resolve_track(bridge, variation)
                print(f"   Variation {variation} worked: {resolved}")
                break
            except Exception as e:
                print(f"   Variation {variation} failed: {e}")