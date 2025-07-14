"""
Color Management Tools for REAPER MCP

This module contains tools for managing colors of tracks, items, takes,
and markers in REAPER projects.
"""

from typing import Optional, Tuple, List
from ..bridge import bridge


# ============================================================================
# Color Utilities (4 tools)
# ============================================================================

async def color_from_native(native_color: int) -> str:
    """Convert native REAPER color to RGB"""
    result = await bridge.call_lua("ColorFromNative", [native_color])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 3:
            r, g, b = ret[:3]
            return f"RGB({r}, {g}, {b}) from native {native_color}"
        else:
            return f"Failed to convert color {native_color}"
    else:
        raise Exception(f"Failed to convert color: {result.get('error', 'Unknown error')}")


async def color_to_native(r: int, g: int, b: int) -> str:
    """Convert RGB to native REAPER color"""
    result = await bridge.call_lua("ColorToNative", [r, g, b])
    
    if result.get("ok"):
        native = result.get("ret", 0)
        return f"Native color {native} from RGB({r}, {g}, {b})"
    else:
        raise Exception(f"Failed to convert RGB to native: {result.get('error', 'Unknown error')}")


async def gradient_color(start_color: int, end_color: int, position: float) -> str:
    """Calculate gradient color between two colors"""
    # Convert native colors to RGB
    start_result = await bridge.call_lua("ColorFromNative", [start_color])
    end_result = await bridge.call_lua("ColorFromNative", [end_color])
    
    if not (start_result.get("ok") and end_result.get("ok")):
        raise Exception("Failed to convert colors")
    
    start_rgb = start_result.get("ret", [0, 0, 0])
    end_rgb = end_result.get("ret", [0, 0, 0])
    
    if not (isinstance(start_rgb, list) and isinstance(end_rgb, list)):
        raise Exception("Invalid color data")
    
    # Calculate gradient
    position = max(0.0, min(1.0, position))
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * position)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * position)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * position)
    
    # Convert back to native
    result = await bridge.call_lua("ColorToNative", [r, g, b])
    
    if result.get("ok"):
        native = result.get("ret", 0)
        return f"Gradient color {native} at position {position:.2f} (RGB: {r}, {g}, {b})"
    else:
        raise Exception("Failed to convert gradient color")


async def get_theme_color(theme_color_name: str, shade: int = 0) -> str:
    """Get theme color by name"""
    # Map color names to indices
    color_map = {
        "col_main_bg": 0,
        "col_main_text": 1,
        "col_main_text_sel": 2,
        "col_main_editbk": 3,
        "col_tracklistbg": 4,
        "col_itembg": 5,
        "col_tr1_bg": 6,
        "col_tr2_bg": 7,
        "col_tr1_fg": 8,
        "col_tr2_fg": 9,
        "col_seltrack": 10,
        "col_seltrack2": 11,
        "col_arrangebg": 12,
        "col_arrangegrid": 13,
        "col_cursor": 14,
        "col_cursor2": 15,
        "col_timesel": 16,
        "col_timesel2": 17,
    }
    
    idx = color_map.get(theme_color_name.lower(), -1)
    if idx == -1:
        return f"Unknown theme color: {theme_color_name}"
    
    result = await bridge.call_lua("GetThemeColor", [theme_color_name, shade])
    
    if result.get("ok"):
        color = result.get("ret", 0)
        return f"Theme color '{theme_color_name}' (shade {shade}): {color}"
    else:
        # Fallback to a default color
        return f"Theme color '{theme_color_name}' not available, using default"


# ============================================================================
# Track Color Management (6 tools)
# ============================================================================

async def get_track_color(track_index: int) -> str:
    """Get track color"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get color
    result = await bridge.call_lua("GetTrackColor", [track_handle])
    
    if result.get("ok"):
        color = result.get("ret", 0)
        if color == 0:
            return f"Track {track_index} has no custom color"
        else:
            # Convert to RGB for display
            rgb_result = await bridge.call_lua("ColorFromNative", [color])
            if rgb_result.get("ok") and isinstance(rgb_result.get("ret"), list):
                r, g, b = rgb_result.get("ret")[:3]
                return f"Track {track_index} color: {color} (RGB: {r}, {g}, {b})"
            else:
                return f"Track {track_index} color: {color}"
    else:
        raise Exception(f"Failed to get track color: {result.get('error', 'Unknown error')}")


async def set_track_color(track_index: int, color: int) -> str:
    """Set track color"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set color
    result = await bridge.call_lua("SetTrackColor", [track_handle, color])
    
    if result.get("ok"):
        if color == 0:
            return f"Removed custom color from track {track_index}"
        else:
            # Convert to RGB for display
            rgb_result = await bridge.call_lua("ColorFromNative", [color])
            if rgb_result.get("ok") and isinstance(rgb_result.get("ret"), list):
                r, g, b = rgb_result.get("ret")[:3]
                return f"Set track {track_index} color to {color} (RGB: {r}, {g}, {b})"
            else:
                return f"Set track {track_index} color to {color}"
    else:
        raise Exception(f"Failed to set track color: {result.get('error', 'Unknown error')}")


async def set_track_color_rgb(track_index: int, r: int, g: int, b: int) -> str:
    """Set track color using RGB values"""
    # Convert RGB to native
    native_result = await bridge.call_lua("ColorToNative", [r, g, b])
    if not native_result.get("ok"):
        raise Exception("Failed to convert RGB to native color")
    
    native_color = native_result.get("ret", 0)
    
    # Set track color
    return await set_track_color(track_index, native_color)


async def color_tracks_gradient(start_track: int, end_track: int, 
                              start_color: int, end_color: int) -> str:
    """Apply gradient coloring to a range of tracks"""
    if start_track > end_track:
        start_track, end_track = end_track, start_track
    
    track_count = end_track - start_track + 1
    colored = 0
    
    for i in range(track_count):
        track_idx = start_track + i
        position = i / max(1, track_count - 1)
        
        # Calculate gradient color
        gradient_result = await gradient_color(start_color, end_color, position)
        # Extract native color from result string
        import re
        match = re.search(r"Gradient color (\d+)", gradient_result)
        if match:
            color = int(match.group(1))
            try:
                await set_track_color(track_idx, color)
                colored += 1
            except:
                pass  # Skip tracks that don't exist
    
    return f"Applied gradient coloring to {colored} tracks"


async def color_selected_tracks(color: int) -> str:
    """Set color for all selected tracks"""
    # Count selected tracks
    count_result = await bridge.call_lua("CountSelectedTracks", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count selected tracks")
    
    sel_count = count_result.get("ret", 0)
    if sel_count == 0:
        return "No tracks selected"
    
    colored = 0
    for i in range(sel_count):
        # Get selected track
        track_result = await bridge.call_lua("GetSelectedTrack", [0, i])
        if track_result.get("ok") and track_result.get("ret"):
            track_handle = track_result.get("ret")
            
            # Set color
            color_result = await bridge.call_lua("SetTrackColor", [track_handle, color])
            if color_result.get("ok"):
                colored += 1
    
    return f"Set color for {colored} selected tracks"


async def get_track_state_color(track_index: int, auto_mode: bool = False) -> str:
    """Get track color considering automation/state"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get base color
    color_result = await bridge.call_lua("GetTrackColor", [track_handle])
    if not color_result.get("ok"):
        raise Exception("Failed to get track color")
    
    base_color = color_result.get("ret", 0)
    
    if auto_mode:
        # Check automation mode
        auto_result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_handle, "I_AUTOMODE"])
        if auto_result.get("ok"):
            auto_mode_val = int(auto_result.get("ret", 0))
            mode_names = {
                0: "Trim/Read",
                1: "Read",
                2: "Touch", 
                3: "Write",
                4: "Latch"
            }
            mode_str = mode_names.get(auto_mode_val, "Unknown")
            return f"Track {track_index} color: {base_color} (Auto mode: {mode_str})"
    
    return f"Track {track_index} color: {base_color}"


# ============================================================================
# Item & Take Color Management (8 tools)
# ============================================================================

async def get_item_color(item_index: int) -> str:
    """Get media item color"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Get color (I_CUSTOMCOLOR)
    result = await bridge.call_lua("GetMediaItemInfo_Value", [item_handle, "I_CUSTOMCOLOR"])
    
    if result.get("ok"):
        color = int(result.get("ret", 0))
        if color == 0:
            return f"Item {item_index} has no custom color"
        else:
            # Convert to RGB for display
            rgb_result = await bridge.call_lua("ColorFromNative", [color | 0x01000000])
            if rgb_result.get("ok") and isinstance(rgb_result.get("ret"), list):
                r, g, b = rgb_result.get("ret")[:3]
                return f"Item {item_index} color: {color} (RGB: {r}, {g}, {b})"
            else:
                return f"Item {item_index} color: {color}"
    else:
        raise Exception(f"Failed to get item color: {result.get('error', 'Unknown error')}")


async def set_item_color(item_index: int, color: int) -> str:
    """Set media item color"""
    # Get item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    # Set color (I_CUSTOMCOLOR)
    # Note: Item colors need the 0x01000000 flag
    color_value = color | 0x01000000 if color > 0 else 0
    result = await bridge.call_lua("SetMediaItemInfo_Value", [item_handle, "I_CUSTOMCOLOR", color_value])
    
    if result.get("ok"):
        if color == 0:
            return f"Removed custom color from item {item_index}"
        else:
            # Convert to RGB for display
            rgb_result = await bridge.call_lua("ColorFromNative", [color | 0x01000000])
            if rgb_result.get("ok") and isinstance(rgb_result.get("ret"), list):
                r, g, b = rgb_result.get("ret")[:3]
                return f"Set item {item_index} color to {color} (RGB: {r}, {g}, {b})"
            else:
                return f"Set item {item_index} color to {color}"
    else:
        raise Exception(f"Failed to set item color: {result.get('error', 'Unknown error')}")


async def set_item_color_rgb(item_index: int, r: int, g: int, b: int) -> str:
    """Set media item color using RGB values"""
    # Convert RGB to native
    native_result = await bridge.call_lua("ColorToNative", [r, g, b])
    if not native_result.get("ok"):
        raise Exception("Failed to convert RGB to native color")
    
    native_color = native_result.get("ret", 0)
    
    # Set item color
    return await set_item_color(item_index, native_color)


async def color_selected_items(color: int) -> str:
    """Set color for all selected items"""
    # Count selected items
    count_result = await bridge.call_lua("CountSelectedMediaItems", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count selected items")
    
    sel_count = count_result.get("ret", 0)
    if sel_count == 0:
        return "No items selected"
    
    colored = 0
    color_value = color | 0x01000000 if color > 0 else 0
    
    for i in range(sel_count):
        # Get selected item
        item_result = await bridge.call_lua("GetSelectedMediaItem", [0, i])
        if item_result.get("ok") and item_result.get("ret"):
            item_handle = item_result.get("ret")
            
            # Set color
            color_result = await bridge.call_lua("SetMediaItemInfo_Value", [
                item_handle, "I_CUSTOMCOLOR", color_value
            ])
            if color_result.get("ok"):
                colored += 1
    
    return f"Set color for {colored} selected items"


async def get_take_color(item_index: int, take_index: int) -> str:
    """Get take color"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Get color (I_CUSTOMCOLOR)
    result = await bridge.call_lua("GetMediaItemTakeInfo_Value", [take_handle, "I_CUSTOMCOLOR"])
    
    if result.get("ok"):
        color = int(result.get("ret", 0))
        if color == 0:
            return f"Take {take_index} has no custom color"
        else:
            # Convert to RGB for display
            rgb_result = await bridge.call_lua("ColorFromNative", [color | 0x01000000])
            if rgb_result.get("ok") and isinstance(rgb_result.get("ret"), list):
                r, g, b = rgb_result.get("ret")[:3]
                return f"Take {take_index} color: {color} (RGB: {r}, {g}, {b})"
            else:
                return f"Take {take_index} color: {color}"
    else:
        raise Exception(f"Failed to get take color: {result.get('error', 'Unknown error')}")


async def set_take_color(item_index: int, take_index: int, color: int) -> str:
    """Set take color"""
    # Get item and take
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to find media item at index {item_index}")
    
    item_handle = item_result.get("ret")
    
    take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
    if not take_result.get("ok") or not take_result.get("ret"):
        raise Exception(f"Failed to find take at index {take_index}")
    
    take_handle = take_result.get("ret")
    
    # Set color (I_CUSTOMCOLOR)
    color_value = color | 0x01000000 if color > 0 else 0
    result = await bridge.call_lua("SetMediaItemTakeInfo_Value", [take_handle, "I_CUSTOMCOLOR", color_value])
    
    if result.get("ok"):
        if color == 0:
            return f"Removed custom color from take {take_index}"
        else:
            # Convert to RGB for display
            rgb_result = await bridge.call_lua("ColorFromNative", [color | 0x01000000])
            if rgb_result.get("ok") and isinstance(rgb_result.get("ret"), list):
                r, g, b = rgb_result.get("ret")[:3]
                return f"Set take {take_index} color to {color} (RGB: {r}, {g}, {b})"
            else:
                return f"Set take {take_index} color to {color}"
    else:
        raise Exception(f"Failed to set take color: {result.get('error', 'Unknown error')}")


async def color_items_by_source_type(track_index: int, audio_color: int, midi_color: int) -> str:
    """Color items on track based on source type (audio vs MIDI)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Count items on track
    count_result = await bridge.call_lua("CountTrackMediaItems", [track_handle])
    if not count_result.get("ok"):
        raise Exception("Failed to count track items")
    
    item_count = count_result.get("ret", 0)
    audio_colored = 0
    midi_colored = 0
    
    for i in range(item_count):
        # Get item
        item_result = await bridge.call_lua("GetTrackMediaItem", [track_handle, i])
        if item_result.get("ok") and item_result.get("ret"):
            item_handle = item_result.get("ret")
            
            # Get active take
            take_result = await bridge.call_lua("GetActiveTake", [item_handle])
            if take_result.get("ok") and take_result.get("ret"):
                take_handle = take_result.get("ret")
                
                # Check if MIDI
                midi_result = await bridge.call_lua("TakeIsMIDI", [take_handle])
                is_midi = midi_result.get("ok") and midi_result.get("ret", False)
                
                # Set appropriate color
                color = midi_color if is_midi else audio_color
                color_value = color | 0x01000000 if color > 0 else 0
                
                color_result = await bridge.call_lua("SetMediaItemInfo_Value", [
                    item_handle, "I_CUSTOMCOLOR", color_value
                ])
                if color_result.get("ok"):
                    if is_midi:
                        midi_colored += 1
                    else:
                        audio_colored += 1
    
    return f"Colored {audio_colored} audio items and {midi_colored} MIDI items on track {track_index}"


async def inherit_track_color_to_items(track_index: int) -> str:
    """Set all items on track to match track color"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get track color
    color_result = await bridge.call_lua("GetTrackColor", [track_handle])
    if not color_result.get("ok"):
        raise Exception("Failed to get track color")
    
    track_color = color_result.get("ret", 0)
    if track_color == 0:
        return f"Track {track_index} has no custom color to inherit"
    
    # Count items on track
    count_result = await bridge.call_lua("CountTrackMediaItems", [track_handle])
    if not count_result.get("ok"):
        raise Exception("Failed to count track items")
    
    item_count = count_result.get("ret", 0)
    colored = 0
    
    # Apply color to all items
    color_value = track_color | 0x01000000
    
    for i in range(item_count):
        item_result = await bridge.call_lua("GetTrackMediaItem", [track_handle, i])
        if item_result.get("ok") and item_result.get("ret"):
            item_handle = item_result.get("ret")
            
            color_result = await bridge.call_lua("SetMediaItemInfo_Value", [
                item_handle, "I_CUSTOMCOLOR", color_value
            ])
            if color_result.get("ok"):
                colored += 1
    
    return f"Applied track color to {colored} items on track {track_index}"


# ============================================================================
# Marker & Region Color Management (6 tools)
# ============================================================================

async def get_marker_region_color(index: int) -> str:
    """Get marker or region color by index"""
    # Enumerate to find the marker/region
    result = await bridge.call_lua("EnumProjectMarkers3", [0, index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 7:
            retval, is_region, pos, rgnend, name, markrgnidx, color = ret[:7]
            if retval > 0:
                marker_type = "region" if is_region else "marker"
                if color == 0:
                    return f"{marker_type.title()} {markrgnidx} has no custom color"
                else:
                    # Convert to RGB for display
                    rgb_result = await bridge.call_lua("ColorFromNative", [color | 0x01000000])
                    if rgb_result.get("ok") and isinstance(rgb_result.get("ret"), list):
                        r, g, b = rgb_result.get("ret")[:3]
                        return f"{marker_type.title()} {markrgnidx} color: {color} (RGB: {r}, {g}, {b})"
                    else:
                        return f"{marker_type.title()} {markrgnidx} color: {color}"
            else:
                return f"No marker/region at index {index}"
        else:
            return "Failed to get marker/region data"
    else:
        raise Exception(f"Failed to get marker/region: {result.get('error', 'Unknown error')}")


async def set_marker_region_color(index: int, color: int) -> str:
    """Set marker or region color by index"""
    # Get marker/region info first
    enum_result = await bridge.call_lua("EnumProjectMarkers3", [0, index])
    
    if not enum_result.get("ok"):
        raise Exception("Failed to enumerate markers")
    
    ret = enum_result.get("ret", [])
    if not isinstance(ret, list) or len(ret) < 7:
        raise Exception("Invalid marker data")
    
    retval, is_region, pos, rgnend, name, markrgnidx, old_color = ret[:7]
    
    if retval == 0:
        return f"No marker/region at index {index}"
    
    # Set color using SetProjectMarkerByIndex
    color_value = color | 0x01000000 if color > 0 else 0
    result = await bridge.call_lua("SetProjectMarkerByIndex", [
        0, index, is_region, pos, rgnend, markrgnidx, name, color_value
    ])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            marker_type = "region" if is_region else "marker"
            if color == 0:
                return f"Removed custom color from {marker_type} {markrgnidx}"
            else:
                # Convert to RGB for display
                rgb_result = await bridge.call_lua("ColorFromNative", [color | 0x01000000])
                if rgb_result.get("ok") and isinstance(rgb_result.get("ret"), list):
                    r, g, b = rgb_result.get("ret")[:3]
                    return f"Set {marker_type} {markrgnidx} color to {color} (RGB: {r}, {g}, {b})"
                else:
                    return f"Set {marker_type} {markrgnidx} color to {color}"
        else:
            return "Failed to set marker/region color"
    else:
        raise Exception(f"Failed to set marker/region color: {result.get('error', 'Unknown error')}")


async def color_all_markers(color: int) -> str:
    """Set color for all markers (not regions)"""
    # Count markers/regions
    count_result = await bridge.call_lua("CountProjectMarkers", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count markers")
    
    ret = count_result.get("ret", [])
    if not isinstance(ret, list) or len(ret) < 2:
        return "No markers found"
    
    total_count, marker_count = ret[:2]
    colored = 0
    color_value = color | 0x01000000 if color > 0 else 0
    
    for i in range(total_count):
        enum_result = await bridge.call_lua("EnumProjectMarkers3", [0, i])
        if enum_result.get("ok"):
            ret = enum_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 7:
                retval, is_region, pos, rgnend, name, markrgnidx, old_color = ret[:7]
                if retval > 0 and not is_region:  # Only color markers, not regions
                    # Set color
                    set_result = await bridge.call_lua("SetProjectMarkerByIndex", [
                        0, i, is_region, pos, rgnend, markrgnidx, name, color_value
                    ])
                    if set_result.get("ok") and set_result.get("ret"):
                        colored += 1
    
    return f"Set color for {colored} markers"


async def color_all_regions(color: int) -> str:
    """Set color for all regions (not markers)"""
    # Count markers/regions
    count_result = await bridge.call_lua("CountProjectMarkers", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count regions")
    
    ret = count_result.get("ret", [])
    if not isinstance(ret, list) or len(ret) < 3:
        return "No regions found"
    
    total_count, marker_count, region_count = ret[:3]
    colored = 0
    color_value = color | 0x01000000 if color > 0 else 0
    
    for i in range(total_count):
        enum_result = await bridge.call_lua("EnumProjectMarkers3", [0, i])
        if enum_result.get("ok"):
            ret = enum_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 7:
                retval, is_region, pos, rgnend, name, markrgnidx, old_color = ret[:7]
                if retval > 0 and is_region:  # Only color regions, not markers
                    # Set color
                    set_result = await bridge.call_lua("SetProjectMarkerByIndex", [
                        0, i, is_region, pos, rgnend, markrgnidx, name, color_value
                    ])
                    if set_result.get("ok") and set_result.get("ret"):
                        colored += 1
    
    return f"Set color for {colored} regions"


async def color_regions_by_name_pattern(pattern: str, color: int) -> str:
    """Color regions matching name pattern"""
    import re
    
    # Count markers/regions
    count_result = await bridge.call_lua("CountProjectMarkers", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count regions")
    
    ret = count_result.get("ret", [])
    if not isinstance(ret, list) or len(ret) < 3:
        return "No regions found"
    
    total_count = ret[0]
    colored = 0
    color_value = color | 0x01000000 if color > 0 else 0
    
    for i in range(total_count):
        enum_result = await bridge.call_lua("EnumProjectMarkers3", [0, i])
        if enum_result.get("ok"):
            ret = enum_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 7:
                retval, is_region, pos, rgnend, name, markrgnidx, old_color = ret[:7]
                if retval > 0 and is_region and name:
                    # Check if name matches pattern
                    if re.search(pattern, name, re.IGNORECASE):
                        # Set color
                        set_result = await bridge.call_lua("SetProjectMarkerByIndex", [
                            0, i, is_region, pos, rgnend, markrgnidx, name, color_value
                        ])
                        if set_result.get("ok") and set_result.get("ret"):
                            colored += 1
    
    return f"Set color for {colored} regions matching pattern '{pattern}'"


async def generate_region_colors_by_index() -> str:
    """Auto-generate unique colors for regions based on their index"""
    # Count markers/regions
    count_result = await bridge.call_lua("CountProjectMarkers", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to count regions")
    
    ret = count_result.get("ret", [])
    if not isinstance(ret, list) or len(ret) < 3:
        return "No regions found"
    
    total_count = ret[0]
    colored = 0
    region_idx = 0
    
    # Define a palette of colors
    palette = [
        (255, 100, 100),  # Red
        (100, 255, 100),  # Green
        (100, 100, 255),  # Blue
        (255, 255, 100),  # Yellow
        (255, 100, 255),  # Magenta
        (100, 255, 255),  # Cyan
        (255, 150, 100),  # Orange
        (150, 100, 255),  # Purple
    ]
    
    for i in range(total_count):
        enum_result = await bridge.call_lua("EnumProjectMarkers3", [0, i])
        if enum_result.get("ok"):
            ret = enum_result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 7:
                retval, is_region, pos, rgnend, name, markrgnidx, old_color = ret[:7]
                if retval > 0 and is_region:
                    # Get color from palette
                    r, g, b = palette[region_idx % len(palette)]
                    
                    # Convert to native
                    native_result = await bridge.call_lua("ColorToNative", [r, g, b])
                    if native_result.get("ok"):
                        color_value = native_result.get("ret") | 0x01000000
                        
                        # Set color
                        set_result = await bridge.call_lua("SetProjectMarkerByIndex", [
                            0, i, is_region, pos, rgnend, markrgnidx, name, color_value
                        ])
                        if set_result.get("ok") and set_result.get("ret"):
                            colored += 1
                    
                    region_idx += 1
    
    return f"Auto-colored {colored} regions with unique colors"


# ============================================================================
# Registration Function
# ============================================================================

def register_color_management_tools(mcp) -> int:
    """Register all color management tools with the MCP instance"""
    tools = [
        # Color Utilities
        (color_from_native, "Convert native REAPER color to RGB"),
        (color_to_native, "Convert RGB to native REAPER color"),
        (gradient_color, "Calculate gradient color between two colors"),
        (get_theme_color, "Get theme color by name"),
        
        # Track Color Management
        (get_track_color, "Get track color"),
        (set_track_color, "Set track color"),
        (set_track_color_rgb, "Set track color using RGB values"),
        (color_tracks_gradient, "Apply gradient coloring to a range of tracks"),
        (color_selected_tracks, "Set color for all selected tracks"),
        (get_track_state_color, "Get track color considering automation/state"),
        
        # Item & Take Color Management
        (get_item_color, "Get media item color"),
        (set_item_color, "Set media item color"),
        (set_item_color_rgb, "Set media item color using RGB values"),
        (color_selected_items, "Set color for all selected items"),
        (get_take_color, "Get take color"),
        (set_take_color, "Set take color"),
        (color_items_by_source_type, "Color items on track based on source type"),
        (inherit_track_color_to_items, "Set all items on track to match track color"),
        
        # Marker & Region Color Management
        (get_marker_region_color, "Get marker or region color by index"),
        (set_marker_region_color, "Set marker or region color by index"),
        (color_all_markers, "Set color for all markers"),
        (color_all_regions, "Set color for all regions"),
        (color_regions_by_name_pattern, "Color regions matching name pattern"),
        (generate_region_colors_by_index, "Auto-generate unique colors for regions"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)