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


async def render_time_selection(add_to_project: bool = True) -> str:
    """Render time selection to new track or file"""
    if add_to_project:
        # Render to new track (action 42006)
        result = await bridge.call_lua("Main_OnCommand", [42006, 0])
        
        if result.get("ok"):
            return "Rendered time selection to new track"
        else:
            raise Exception(f"Failed to render time selection: {result.get('error', 'Unknown error')}")
    else:
        # Render to file (action 41825)
        result = await bridge.call_lua("Main_OnCommand", [41825, 0])
        
        if result.get("ok"):
            return "Started render dialog for time selection"
        else:
            raise Exception(f"Failed to render time selection: {result.get('error', 'Unknown error')}")


async def apply_fx_to_items(track_index: int) -> str:
    """Apply track FX to items destructively"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Track {track_index} not found")
    
    # Unselect all tracks first
    await bridge.call_lua("Main_OnCommand", [40297, 0])  # Track: Unselect all tracks
    
    # Select only this track
    await bridge.call_lua("SetTrackSelected", [track_index, True])
    
    # Apply track FX to items as new take (action 40209)
    result = await bridge.call_lua("Main_OnCommand", [40209, 0])
    
    if result.get("ok"):
        return f"Applied FX to items on track {track_index}"
    else:
        raise Exception("Failed to apply FX to items")


# ============================================================================
# Freezing Operations (3 tools)
# ============================================================================

async def is_track_frozen(track_index: int) -> str:
    """Check if a track is frozen"""
    # Pass track index directly - the bridge will handle getting the track  
    result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_index, "I_FREEZE"])
    
    if result.get("ok"):
        freeze_value = int(result.get("ret", 0))
        # I_FREEZE: 0 = unfrozen, 1 = frozen
        is_frozen = freeze_value > 0
        return f"Track frozen: {is_frozen}"
    else:
        raise Exception(f"Failed to check freeze state: {result.get('error', 'Unknown error')}")


async def freeze_track(track_index: int) -> str:
    """Freeze a track"""
    # Get track to verify it exists
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Track {track_index} not found")
    
    # Unselect all tracks first
    unselect_result = await bridge.call_lua("Main_OnCommand", [40297, 0])  # Track: Unselect all tracks
    if not unselect_result.get("ok"):
        raise Exception("Failed to unselect tracks")
    
    # Select only this track
    select_result = await bridge.call_lua("SetTrackSelected", [track_index, True])
    if not select_result.get("ok"):
        raise Exception(f"Failed to select track {track_index}")
    
    # Freeze track to stereo
    result = await bridge.call_lua("Main_OnCommand", [41223, 0])  # Track: Freeze to stereo
    
    if result and result.get("ok"):
        # Wait a moment for the freeze to complete
        import asyncio
        await asyncio.sleep(0.5)
        return f"Froze track {track_index}"
    else:
        error_msg = result.get("error", "Unknown error") if result else "No response"
        raise Exception(f"Failed to freeze track: {error_msg}")


async def unfreeze_track(track_index: int) -> str:
    """Unfreeze a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Track {track_index} not found")
    
    # Unselect all tracks first
    await bridge.call_lua("Main_OnCommand", [40297, 0])  # Track: Unselect all tracks
    
    # Select only this track
    await bridge.call_lua("SetTrackSelected", [track_index, True])
    
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
        (render_time_selection, "Render time selection to new track or file"),
        (apply_fx_to_items, "Apply track FX to items destructively"),
        
        # Freezing Operations
        (is_track_frozen, "Check if a track is frozen"),
        (freeze_track, "Freeze a track"),
        (unfreeze_track, "Unfreeze a track"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)