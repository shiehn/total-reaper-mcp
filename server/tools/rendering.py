"""
Rendering & Freezing Tools for REAPER MCP

This module contains tools for rendering and freezing operations.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# Rendering Operations (2 tools)
# ============================================================================

async def render_project(bounds: str = "entire_project", filename: Optional[str] = None, 
                        add_to_project: bool = False, close_when_done: bool = True) -> str:
    """Render the entire project to file (opens render dialog)"""
    # Map bounds string to action IDs
    bounds_actions = {
        "entire_project": 41824,    # Render entire project
        "time_selection": 41825,    # Render time selection  
        "selected_items": 41829,    # Render selected media items
        "project_regions": 42230    # Render project regions
    }
    
    action = bounds_actions.get(bounds, 41824)
    
    result = await bridge.call_lua("Main_OnCommand", [action, 0])
    
    if result.get("ok"):
        return f"Started render dialog for: {bounds.replace('_', ' ')}"
    else:
        raise Exception(f"Failed to start render: {result.get('error', 'Unknown error')}")


async def bounce_tracks(add_to_project: bool = True) -> str:
    """Bounce selected tracks to new track"""
    # Bounce selected tracks (action 40914)
    result = await bridge.call_lua("Main_OnCommand", [40914, 0])
    
    if result.get("ok"):
        return "Bounced selected tracks" + (" to new track" if add_to_project else "")
    else:
        raise Exception(f"Failed to bounce tracks: {result.get('error', 'Unknown error')}")


# ============================================================================
# Freezing Operations (2 tools)
# ============================================================================

async def freeze_track(track_index: int) -> str:
    """Freeze a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Track {track_index} not found")
    
    # Select only this track
    await bridge.call_lua("SetOnlyTrackSelected", [track_result.get("ret")])
    
    # Freeze track to stereo
    result = await bridge.call_lua("Main_OnCommand", [41223, 0])  # Track: Freeze to stereo
    
    if result.get("ok"):
        return f"Froze track {track_index}"
    else:
        raise Exception("Failed to freeze track")


async def unfreeze_track(track_index: int) -> str:
    """Unfreeze a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Track {track_index} not found")
    
    # Select only this track
    await bridge.call_lua("SetOnlyTrackSelected", [track_result.get("ret")])
    
    # Unfreeze track
    result = await bridge.call_lua("Main_OnCommand", [41644, 0])  # Track: Unfreeze
    
    if result.get("ok"):
        return f"Unfroze track {track_index}"
    else:
        raise Exception("Failed to unfreeze track")


# ============================================================================
# Advanced Rendering Features (planned for future expansion)
# ============================================================================

# Future functions could include:
# - render_stems() - Render stems/multichannel
# - render_selected_tracks() - Render selected tracks as stems
# - apply_fx_to_items() - Apply track FX to items destructively
# - glue_items() - Glue selected items
# - normalize_items() - Normalize selected items
# - consolidate_tracks() - Consolidate selected tracks
# - freeze_to_multichannel() - Freeze track to multichannel
# - freeze_to_mono() - Freeze track to mono
# - get_render_queue_count() - Get number of items in render queue
# - add_to_render_queue() - Add project to render queue
# - start_render_queue() - Start rendering queue
# - get_render_progress() - Get current render progress
# - cancel_render() - Cancel current render operation


# ============================================================================
# Registration Function
# ============================================================================

def register_rendering_tools(mcp) -> int:
    """Register all rendering and freezing tools with the MCP instance"""
    tools = [
        # Rendering Operations
        (render_project, "Render the entire project to file (opens render dialog)"),
        (bounce_tracks, "Bounce selected tracks to new track"),
        
        # Freezing Operations
        (freeze_track, "Freeze a track"),
        (unfreeze_track, "Unfreeze a track"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)