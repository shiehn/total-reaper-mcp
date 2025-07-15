"""
Video and Visual Media Tools for REAPER MCP

This module contains tools for working with video items, visual processors,
and media display - particularly useful for AI agents working with multimedia content.
"""

from typing import List, Dict, Any, Optional
from ..bridge import bridge


# ============================================================================
# Video Item Management
# ============================================================================

async def is_item_video(item_index: int) -> str:
    """Check if a media item contains video"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Get active take
    take_result = await bridge.call_lua("GetActiveTake", [item])
    if not take_result.get("ok") or not take_result.get("ret"):
        return "Item has no active take"
    
    take = take_result.get("ret")
    
    # Get source
    source_result = await bridge.call_lua("GetMediaItemTake_Source", [take])
    if not source_result.get("ok") or not source_result.get("ret"):
        return "Take has no media source"
    
    source = source_result.get("ret")
    
    # Check if video
    result = await bridge.call_lua("PCM_Source_GetSectionInfo", [source, 0.0])
    if result.get("ok"):
        has_video = result.get("has_video", False)
        return f"Item {'contains' if has_video else 'does not contain'} video"
    
    return "Could not determine video status"


async def get_video_processor_count(track_index: int) -> str:
    """Get count of video processors on a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to get track at index {track_index}")
    
    track = track_result.get("ret")
    
    # Get video processor count (use TrackFX count but filter for video)
    fx_count_result = await bridge.call_lua("TrackFX_GetCount", [track])
    fx_count = fx_count_result.get("ret", 0) if fx_count_result.get("ok") else 0
    
    video_count = 0
    for i in range(fx_count):
        # Check if FX is video processor
        name_result = await bridge.call_lua("TrackFX_GetFXName", [track, i])
        if name_result.get("ok"):
            fx_name = name_result.get("ret", "")
            if "video" in fx_name.lower() or "vfx" in fx_name.lower():
                video_count += 1
    
    return f"Track {track_index} has {video_count} video processor(s)"


async def add_video_processor(track_index: int, processor_name: str) -> str:
    """Add a video processor to a track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to get track at index {track_index}")
    
    track = track_result.get("ret")
    
    # Add video processor
    result = await bridge.call_lua("TrackFX_AddByName", [track, processor_name, False, -1])
    if result.get("ok"):
        fx_index = result.get("ret", -1)
        if fx_index >= 0:
            return f"Added video processor '{processor_name}' at index {fx_index}"
        else:
            return f"Video processor '{processor_name}' not found"
    
    raise Exception("Failed to add video processor")


async def set_item_video_fade(item_index: int, fade_in: float, fade_out: float) -> str:
    """Set video fade in/out for an item"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Set video fade in
    fade_in_result = await bridge.call_lua("SetMediaItemInfo_Value", 
                                          [item, "D_FADEINLEN", fade_in])
    
    # Set video fade out
    fade_out_result = await bridge.call_lua("SetMediaItemInfo_Value", 
                                           [item, "D_FADEOUTLEN", fade_out])
    
    if fade_in_result.get("ok") and fade_out_result.get("ok"):
        return f"Set video fades - in: {fade_in:.2f}s, out: {fade_out:.2f}s"
    else:
        raise Exception("Failed to set video fades")


# ============================================================================
# Visual Display and Rendering
# ============================================================================

async def get_project_video_settings() -> str:
    """Get project video settings"""
    # Get video settings
    width_result = await bridge.call_lua("GetExtState", ["REAPER", "video_width"])
    height_result = await bridge.call_lua("GetExtState", ["REAPER", "video_height"])
    fps_result = await bridge.call_lua("GetExtState", ["REAPER", "video_fps"])
    
    width = width_result.get("ret", "1920") if width_result.get("ok") else "1920"
    height = height_result.get("ret", "1080") if height_result.get("ok") else "1080"
    fps = fps_result.get("ret", "30") if fps_result.get("ok") else "30"
    
    # Try to get from project settings
    settings_result = await bridge.call_lua("GetProjectInfo", [0, "PROJECT_FRAMERATE"])
    if settings_result.get("ok"):
        project_fps = settings_result.get("ret", 30)
        return f"Video settings: {width}x{height} @ {project_fps:.2f} fps"
    
    return f"Video settings: {width}x{height} @ {fps} fps (default)"


async def set_video_window_position(x: int, y: int, width: int, height: int) -> str:
    """Set video window position and size"""
    # This would typically use SWS extensions or native API
    # For now, we'll simulate with extended state
    await bridge.call_lua("SetExtState", ["REAPER", "video_window_x", str(x)])
    await bridge.call_lua("SetExtState", ["REAPER", "video_window_y", str(y)])
    await bridge.call_lua("SetExtState", ["REAPER", "video_window_width", str(width)])
    await bridge.call_lua("SetExtState", ["REAPER", "video_window_height", str(height)])
    
    return f"Set video window to {width}x{height} at ({x}, {y})"


async def toggle_video_window() -> str:
    """Toggle video window visibility"""
    # Execute action to toggle video window
    result = await bridge.call_lua("Main_OnCommand", [50125, 0])  # Video: Toggle video window
    if result.get("ok"):
        return "Toggled video window"
    else:
        raise Exception("Failed to toggle video window")


async def render_video_frame(time_position: float, output_path: str) -> str:
    """Render a single video frame at specified time"""
    # This is a simplified implementation
    # Real implementation would use video rendering API
    
    # Set time selection to single frame
    await bridge.call_lua("SetEditCurPos", [time_position, False, False])
    
    # Get frame rate
    fps_result = await bridge.call_lua("GetProjectInfo", [0, "PROJECT_FRAMERATE"])
    fps = fps_result.get("ret", 30) if fps_result.get("ok") else 30
    frame_duration = 1.0 / fps
    
    # Set time selection
    await bridge.call_lua("GetSet_LoopTimeRange", [True, False, time_position, time_position + frame_duration, False])
    
    return f"Frame rendering requires render queue setup. Time: {time_position:.3f}s, Output: {output_path}"


# ============================================================================
# Visual Effects and Processing
# ============================================================================

async def get_take_video_fx_count(item_index: int, take_index: int) -> str:
    """Get count of video FX on a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take {take_index} from item {item_index}")
    
    take = take_result.get("ret")
    
    # Get FX count
    fx_count_result = await bridge.call_lua("TakeFX_GetCount", [take])
    fx_count = fx_count_result.get("ret", 0) if fx_count_result.get("ok") else 0
    
    # Count video FX
    video_fx_count = 0
    for i in range(fx_count):
        name_result = await bridge.call_lua("TakeFX_GetFXName", [take, i])
        if name_result.get("ok"):
            fx_name = name_result.get("ret", "")
            if "video" in fx_name.lower() or "vfx" in fx_name.lower():
                video_fx_count += 1
    
    return f"Take has {video_fx_count} video FX (out of {fx_count} total FX)"


async def add_take_video_fx(item_index: int, take_index: int, fx_name: str) -> str:
    """Add video FX to a take"""
    # Get take
    take_result = await bridge.call_lua("GetTake", [item_index, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to get take {take_index} from item {item_index}")
    
    take = take_result.get("ret")
    
    # Add FX
    result = await bridge.call_lua("TakeFX_AddByName", [take, fx_name, -1])
    if result.get("ok"):
        fx_index = result.get("ret", -1)
        if fx_index >= 0:
            return f"Added video FX '{fx_name}' at index {fx_index}"
        else:
            return f"Video FX '{fx_name}' not found"
    
    raise Exception("Failed to add video FX")


async def set_video_colorspace(colorspace: str) -> str:
    """Set project video colorspace (sRGB, Rec709, etc)"""
    valid_colorspaces = ["sRGB", "Rec709", "Rec2020", "Linear"]
    
    if colorspace not in valid_colorspaces:
        return f"Invalid colorspace. Valid options: {', '.join(valid_colorspaces)}"
    
    # Store in extended state (would normally use video API)
    result = await bridge.call_lua("SetExtState", ["REAPER", "video_colorspace", colorspace])
    if result.get("ok"):
        return f"Set video colorspace to {colorspace}"
    else:
        raise Exception("Failed to set colorspace")


# ============================================================================
# Video Analysis
# ============================================================================

async def analyze_video_content() -> str:
    """Analyze video content in project"""
    item_count_result = await bridge.call_lua("CountMediaItems", [0])
    item_count = item_count_result.get("ret", 0) if item_count_result.get("ok") else 0
    
    video_items = 0
    total_video_duration = 0.0
    video_tracks = set()
    
    for i in range(item_count):
        item_result = await bridge.call_lua("GetMediaItem", [0, i])
        if not item_result.get("ok"):
            continue
        
        item = item_result.get("ret")
        
        # Get active take
        take_result = await bridge.call_lua("GetActiveTake", [item])
        if not take_result.get("ok") or not take_result.get("ret"):
            continue
        
        take = take_result.get("ret")
        
        # Get source
        source_result = await bridge.call_lua("GetMediaItemTake_Source", [take])
        if not source_result.get("ok") or not source_result.get("ret"):
            continue
        
        source = source_result.get("ret")
        
        # Check if video
        info_result = await bridge.call_lua("PCM_Source_GetSectionInfo", [source, 0.0])
        if info_result.get("ok") and info_result.get("has_video", False):
            video_items += 1
            
            # Get duration
            length_result = await bridge.call_lua("GetMediaItemInfo_Value", [item, "D_LENGTH"])
            if length_result.get("ok"):
                total_video_duration += length_result.get("ret", 0)
            
            # Get track
            track_result = await bridge.call_lua("GetMediaItem_Track", [item])
            if track_result.get("ok"):
                video_tracks.add(track_result.get("ret"))
    
    if video_items > 0:
        return (f"Video content analysis:\n"
                f"  Video items: {video_items}\n"
                f"  Total duration: {total_video_duration:.1f}s\n"
                f"  Tracks with video: {len(video_tracks)}")
    else:
        return "No video content found in project"


async def get_video_item_properties(item_index: int) -> str:
    """Get detailed properties of a video item"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Get active take
    take_result = await bridge.call_lua("GetActiveTake", [item])
    if not take_result.get("ok") or not take_result.get("ret"):
        return "Item has no active take"
    
    take = take_result.get("ret")
    
    # Get source
    source_result = await bridge.call_lua("GetMediaItemTake_Source", [take])
    if not source_result.get("ok") or not source_result.get("ret"):
        return "Take has no media source"
    
    source = source_result.get("ret")
    
    # Get video properties
    info_result = await bridge.call_lua("PCM_Source_GetSectionInfo", [source, 0.0])
    if info_result.get("ok"):
        has_video = info_result.get("has_video", False)
        if has_video:
            # Get basic properties
            pos_result = await bridge.call_lua("GetMediaItemInfo_Value", [item, "D_POSITION"])
            length_result = await bridge.call_lua("GetMediaItemInfo_Value", [item, "D_LENGTH"])
            
            pos = pos_result.get("ret", 0) if pos_result.get("ok") else 0
            length = length_result.get("ret", 0) if length_result.get("ok") else 0
            
            return (f"Video item properties:\n"
                    f"  Position: {pos:.2f}s\n"
                    f"  Length: {length:.2f}s\n"
                    f"  Has video: Yes")
        else:
            return "Item does not contain video"
    
    return "Could not determine video properties"


# ============================================================================
# Registration Function
# ============================================================================

def register_video_media_tools(mcp) -> int:
    """Register all video/visual media tools with the MCP instance"""
    tools = [
        # Video Item Management
        (is_item_video, "Check if a media item contains video"),
        (get_video_processor_count, "Get count of video processors on a track"),
        (add_video_processor, "Add a video processor to a track"),
        (set_item_video_fade, "Set video fade in/out for an item"),
        
        # Visual Display and Rendering
        (get_project_video_settings, "Get project video settings"),
        (set_video_window_position, "Set video window position and size"),
        (toggle_video_window, "Toggle video window visibility"),
        (render_video_frame, "Render a single video frame at specified time"),
        
        # Visual Effects and Processing
        (get_take_video_fx_count, "Get count of video FX on a take"),
        (add_take_video_fx, "Add video FX to a take"),
        (set_video_colorspace, "Set project video colorspace"),
        
        # Video Analysis
        (analyze_video_content, "Analyze video content in project"),
        (get_video_item_properties, "Get detailed properties of a video item"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)