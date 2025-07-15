"""Track bouncing and rendering tools for music production workflows."""

from typing import Dict, Any, List, Optional, Tuple
from .bridge_sync import ReaperBridge


def bounce_track_in_place(track_index: int, tail_length: float = 0.0, 
                         render_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Bounce a track in place, replacing it with rendered audio.
    
    Args:
        track_index: Index of the track to bounce
        tail_length: Additional tail length in seconds for reverb/delay tails
        render_settings: Optional render settings override
    
    Returns:
        Dict containing the operation result
    """
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
    track_response = ReaperBridge.send_request(track_request)
    
    if not track_response.get("result"):
        return {
            "success": False,
            "error": f"Track at index {track_index} not found"
        }
    
    track_handle = track_response.get("track")
    
    # Select only this track
    solo_request = {
        "action": "SetMediaTrackInfo_Value",
        "track": track_handle,
        "parmname": "I_SOLO",
        "newvalue": 2  # Solo in place
    }
    solo_response = ReaperBridge.send_request(solo_request)
    
    # Get time bounds from items on track
    bounds = get_track_item_bounds(track_index)
    if bounds["start"] == float('inf'):
        return {
            "success": False,
            "error": "No items found on track"
        }
    
    # Set render bounds
    render_start = bounds["start"]
    render_end = bounds["end"] + tail_length
    
    # Apply render settings
    if render_settings:
        apply_render_settings(render_settings)
    
    # Set time selection for render
    time_request = {
        "action": "GetSet_LoopTimeRange",
        "isSet": True,
        "isLoop": False,
        "startOut": render_start,
        "endOut": render_end,
        "allowautoseek": False
    }
    ReaperBridge.send_request(time_request)
    
    # Render using selected tracks (stems) to project
    render_request = {
        "action": "Main_OnCommand",
        "command": 41720,  # Render selected tracks to multichannel file  
        "project": 0
    }
    render_response = ReaperBridge.send_request(render_request)
    
    # Unsolo track
    unsolo_request = {
        "action": "SetMediaTrackInfo_Value",
        "track": track_handle,
        "parmname": "I_SOLO",
        "newvalue": 0
    }
    ReaperBridge.send_request(unsolo_request)
    
    return {
        "success": render_response.get("result", False),
        "track_index": track_index,
        "render_start": render_start,
        "render_end": render_end
    }


def bounce_tracks_to_stems(track_indices: List[int], output_directory: str,
                          file_prefix: str = "stem", tail_length: float = 0.0) -> Dict[str, Any]:
    """Bounce multiple tracks to individual stem files.
    
    Args:
        track_indices: List of track indices to bounce
        output_directory: Directory to save stem files
        file_prefix: Prefix for stem filenames
        tail_length: Additional tail length in seconds
    
    Returns:
        Dict containing the operation result and file paths
    """
    stems_created = []
    
    for idx, track_index in enumerate(track_indices):
        # Get track name for filename
        track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
        track_response = ReaperBridge.send_request(track_request)
        
        if track_response.get("result"):
            track_handle = track_response.get("track")
            
            # Get track name
            name_request = {
                "action": "GetSetMediaTrackInfo_String",
                "track": track_handle,
                "parmname": "P_NAME",
                "stringNeedBig": False,
                "setnewvalue": False
            }
            name_response = ReaperBridge.send_request(name_request)
            track_name = name_response.get("str", f"Track_{track_index}")
            
            # Clean track name for filename
            clean_name = "".join(c for c in track_name if c.isalnum() or c in " -_")
            stem_filename = f"{file_prefix}_{idx+1:02d}_{clean_name}.wav"
            
            # Set render path
            render_path = f"{output_directory}/{stem_filename}"
            path_request = {
                "action": "GetSetProjectInfo_String",
                "project": 0,
                "desc": "RENDER_FILE",
                "value": render_path,
                "is_set": True
            }
            ReaperBridge.send_request(path_request)
            
            # Bounce the track
            bounce_result = bounce_track_in_place(track_index, tail_length)
            
            if bounce_result["success"]:
                stems_created.append({
                    "track_index": track_index,
                    "track_name": track_name,
                    "file_path": render_path
                })
    
    return {
        "success": len(stems_created) > 0,
        "stems_created": stems_created,
        "total_tracks": len(track_indices)
    }


def freeze_track(track_index: int, freeze_fx: bool = True) -> Dict[str, Any]:
    """Freeze a track to reduce CPU usage.
    
    Args:
        track_index: Index of the track to freeze
        freeze_fx: Whether to freeze FX (True) or just items (False)
    
    Returns:
        Dict containing the operation result
    """
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
    track_response = ReaperBridge.send_request(track_request)
    
    if not track_response.get("result"):
        return {
            "success": False,
            "error": f"Track at index {track_index} not found"
        }
    
    track_handle = track_response.get("track")
    
    # Select the track
    sel_request = {
        "action": "SetMediaTrackInfo_Value",
        "track": track_handle,
        "parmname": "I_SELECTED",
        "newvalue": 1
    }
    ReaperBridge.send_request(sel_request)
    
    # Choose freeze command based on options
    if freeze_fx:
        # Freeze to stereo (full freeze)
        freeze_command = 41223  # Track: Freeze to stereo
    else:
        # Freeze to multichannel (items only)
        freeze_command = 41224  # Track: Freeze to multichannel
    
    freeze_request = {
        "action": "Main_OnCommand",
        "command": freeze_command,
        "project": 0
    }
    freeze_response = ReaperBridge.send_request(freeze_request)
    
    # Deselect track
    desel_request = {
        "action": "SetMediaTrackInfo_Value",
        "track": track_handle,
        "parmname": "I_SELECTED",
        "newvalue": 0
    }
    ReaperBridge.send_request(desel_request)
    
    return {
        "success": freeze_response.get("result", False),
        "track_index": track_index,
        "freeze_type": "full" if freeze_fx else "items_only"
    }


def unfreeze_track(track_index: int) -> Dict[str, Any]:
    """Unfreeze a previously frozen track.
    
    Args:
        track_index: Index of the track to unfreeze
    
    Returns:
        Dict containing the operation result
    """
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
    track_response = ReaperBridge.send_request(track_request)
    
    if not track_response.get("result"):
        return {
            "success": False,
            "error": f"Track at index {track_index} not found"
        }
    
    track_handle = track_response.get("track")
    
    # Select the track
    sel_request = {
        "action": "SetMediaTrackInfo_Value",
        "track": track_handle,
        "parmname": "I_SELECTED",
        "newvalue": 1
    }
    ReaperBridge.send_request(sel_request)
    
    # Unfreeze track
    unfreeze_request = {
        "action": "Main_OnCommand",
        "command": 41644,  # Track: Unfreeze tracks
        "project": 0
    }
    unfreeze_response = ReaperBridge.send_request(unfreeze_request)
    
    # Deselect track
    desel_request = {
        "action": "SetMediaTrackInfo_Value",
        "track": track_handle,
        "parmname": "I_SELECTED",
        "newvalue": 0
    }
    ReaperBridge.send_request(desel_request)
    
    return {
        "success": unfreeze_response.get("result", False),
        "track_index": track_index
    }


def render_selected_items_to_new_track(normalize: bool = False, 
                                     tail_length: float = 0.0) -> Dict[str, Any]:
    """Render selected items to a new track.
    
    Args:
        normalize: Whether to normalize the rendered audio
        tail_length: Additional tail length in seconds
    
    Returns:
        Dict containing the operation result
    """
    # Count selected items
    count_request = {"action": "CountSelectedMediaItems", "proj": 0}
    count_response = ReaperBridge.send_request(count_request)
    item_count = count_response.get("count", 0)
    
    if item_count == 0:
        return {
            "success": False,
            "error": "No items selected"
        }
    
    # Apply render settings if needed
    if tail_length > 0:
        tail_request = {
            "action": "GetSetProjectInfo",
            "project": 0,
            "desc": "RENDER_TAILMS",
            "value": tail_length * 1000,
            "is_set": True
        }
        ReaperBridge.send_request(tail_request)
    
    # Choose render command
    if normalize:
        render_command = 41717  # Render selected items to new track (normalize)
    else:
        render_command = 40603  # Render selected items to new track
    
    render_request = {
        "action": "Main_OnCommand",
        "command": render_command,
        "project": 0
    }
    render_response = ReaperBridge.send_request(render_request)
    
    return {
        "success": render_response.get("result", False),
        "items_rendered": item_count,
        "normalized": normalize
    }


def glue_selected_items() -> Dict[str, Any]:
    """Glue selected items together.
    
    Returns:
        Dict containing the operation result
    """
    # Count selected items first
    count_request = {"action": "CountSelectedMediaItems", "proj": 0}
    count_response = ReaperBridge.send_request(count_request)
    item_count = count_response.get("count", 0)
    
    if item_count < 2:
        return {
            "success": False,
            "error": "Need at least 2 items selected to glue"
        }
    
    # Glue items
    glue_request = {
        "action": "Main_OnCommand",
        "command": 41588,  # Item: Glue items
        "project": 0
    }
    glue_response = ReaperBridge.send_request(glue_request)
    
    return {
        "success": glue_response.get("result", False),
        "items_glued": item_count
    }


def apply_track_fx_to_items(track_index: int, fx_only: bool = False) -> Dict[str, Any]:
    """Apply track FX to items on the track as a render.
    
    Args:
        track_index: Index of the track
        fx_only: Whether to render FX only (dry signal + FX)
    
    Returns:
        Dict containing the operation result
    """
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
    track_response = ReaperBridge.send_request(track_request)
    
    if not track_response.get("result"):
        return {
            "success": False,
            "error": f"Track at index {track_index} not found"
        }
    
    track_handle = track_response.get("track")
    
    # Select all items on track
    item_count = select_all_items_on_track(track_index)
    
    if item_count == 0:
        return {
            "success": False,
            "error": "No items found on track"
        }
    
    # Apply FX to items
    if fx_only:
        apply_command = 40361  # Item: Apply track FX to items (render FX only)
    else:
        apply_command = 40209  # Item: Apply track FX to items
    
    apply_request = {
        "action": "Main_OnCommand",
        "command": apply_command,
        "project": 0
    }
    apply_response = ReaperBridge.send_request(apply_request)
    
    return {
        "success": apply_response.get("result", False),
        "track_index": track_index,
        "items_processed": item_count,
        "fx_only": fx_only
    }


def create_submix_from_tracks(track_indices: List[int], submix_name: str = "Submix") -> Dict[str, Any]:
    """Create a submix bus from selected tracks and route them to it.
    
    Args:
        track_indices: List of track indices to submix
        submix_name: Name for the submix track
    
    Returns:
        Dict containing the operation result and submix track info
    """
    if not track_indices:
        return {
            "success": False,
            "error": "No tracks specified"
        }
    
    # Insert submix track at the end
    track_count_request = {"action": "CountTracks", "proj": 0}
    track_count_response = ReaperBridge.send_request(track_count_request)
    submix_position = track_count_response.get("count", 0)
    
    # Create submix track
    insert_request = {
        "action": "InsertTrackAtIndex",
        "idx": submix_position,
        "wantDefaults": True
    }
    insert_response = ReaperBridge.send_request(insert_request)
    
    if not insert_response.get("result"):
        return {
            "success": False,
            "error": "Failed to create submix track"
        }
    
    # Get submix track handle
    submix_request = {"action": "GetTrack", "proj": 0, "trackidx": submix_position}
    submix_response = ReaperBridge.send_request(submix_request)
    submix_handle = submix_response.get("track")
    
    # Name the submix track
    name_request = {
        "action": "GetSetMediaTrackInfo_String",
        "track": submix_handle,
        "parmname": "P_NAME",
        "stringNeedBig": False,
        "setnewvalue": True,
        "str": submix_name
    }
    ReaperBridge.send_request(name_request)
    
    # Route all specified tracks to submix
    routed_tracks = []
    for track_index in track_indices:
        # Get track handle
        track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
        track_response = ReaperBridge.send_request(track_request)
        
        if track_response.get("result"):
            track_handle = track_response.get("track")
            
            # Create send to submix
            send_request = {
                "action": "CreateTrackSend",
                "tr": track_handle,
                "desttrInOptional": submix_handle
            }
            send_response = ReaperBridge.send_request(send_request)
            
            if send_response.get("result"):
                # Remove master send from source track
                master_send_request = {
                    "action": "SetMediaTrackInfo_Value",
                    "track": track_handle,
                    "parmname": "B_MAINSEND",
                    "newvalue": 0
                }
                ReaperBridge.send_request(master_send_request)
                
                routed_tracks.append(track_index)
    
    return {
        "success": True,
        "submix_track_index": submix_position,
        "submix_name": submix_name,
        "routed_tracks": routed_tracks
    }


def render_project_to_file(output_path: str, render_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Render the entire project to a file.
    
    Args:
        output_path: Path for the output file
        render_settings: Optional render settings
    
    Returns:
        Dict containing the operation result
    """
    # Set render path
    path_request = {
        "action": "GetSetProjectInfo_String",
        "project": 0,
        "desc": "RENDER_FILE",
        "value": output_path,
        "is_set": True
    }
    ReaperBridge.send_request(path_request)
    
    # Apply render settings if provided
    if render_settings:
        apply_render_settings(render_settings)
    
    # Render project
    render_request = {
        "action": "Main_OnCommand",
        "command": 42230,  # File: Render project to disk...
        "project": 0
    }
    render_response = ReaperBridge.send_request(render_request)
    
    return {
        "success": render_response.get("result", False),
        "output_path": output_path
    }


def render_time_selection(output_path: str, render_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Render only the time selection to a file.
    
    Args:
        output_path: Path for the output file  
        render_settings: Optional render settings
    
    Returns:
        Dict containing the operation result
    """
    # Check if time selection exists
    time_request = {
        "action": "GetSet_LoopTimeRange",
        "isSet": False,
        "isLoop": False,
        "startOut": 0.0,
        "endOut": 0.0,
        "allowautoseek": False
    }
    time_response = ReaperBridge.send_request(time_request)
    
    start = time_response.get("startOut", 0.0)
    end = time_response.get("endOut", 0.0)
    
    if end <= start:
        return {
            "success": False,
            "error": "No time selection set"
        }
    
    # Set render bounds to time selection
    bounds_request = {
        "action": "GetSetProjectInfo",
        "project": 0,
        "desc": "RENDER_BOUNDSFLAG",
        "value": 2,  # Time selection
        "is_set": True
    }
    ReaperBridge.send_request(bounds_request)
    
    # Set output path and render
    result = render_project_to_file(output_path, render_settings)
    result["render_start"] = start
    result["render_end"] = end
    result["render_length"] = end - start
    
    return result


def consolidate_track(track_index: int) -> Dict[str, Any]:
    """Consolidate all items on a track into a single item.
    
    Args:
        track_index: Index of the track to consolidate
    
    Returns:
        Dict containing the operation result
    """
    # Select all items on track
    item_count = select_all_items_on_track(track_index)
    
    if item_count == 0:
        return {
            "success": False,
            "error": "No items found on track"
        }
    
    # Glue items
    glue_result = glue_selected_items()
    
    return {
        "success": glue_result["success"],
        "track_index": track_index,
        "items_consolidated": item_count
    }


# Helper functions
def get_track_item_bounds(track_index: int) -> Dict[str, float]:
    """Get the time bounds of all items on a track."""
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
    track_response = ReaperBridge.send_request(track_request)
    
    if not track_response.get("result"):
        return {"start": float('inf'), "end": float('-inf')}
    
    track_handle = track_response.get("track")
    
    # Get item count on track
    count_request = {
        "action": "CountTrackMediaItems",
        "track": track_handle
    }
    count_response = ReaperBridge.send_request(count_request)
    item_count = count_response.get("count", 0)
    
    min_start = float('inf')
    max_end = float('-inf')
    
    for i in range(item_count):
        # Get item
        item_request = {
            "action": "GetTrackMediaItem",
            "track": track_handle,
            "itemidx": i
        }
        item_response = ReaperBridge.send_request(item_request)
        
        if item_response.get("result"):
            item_handle = item_response.get("item")
            
            # Get position
            pos_request = {
                "action": "GetMediaItemInfo_Value",
                "item": item_handle,
                "parmname": "D_POSITION"
            }
            pos_response = ReaperBridge.send_request(pos_request)
            position = pos_response.get("value", 0.0)
            
            # Get length
            len_request = {
                "action": "GetMediaItemInfo_Value",
                "item": item_handle,
                "parmname": "D_LENGTH"
            }
            len_response = ReaperBridge.send_request(len_request)
            length = len_response.get("value", 0.0)
            
            min_start = min(min_start, position)
            max_end = max(max_end, position + length)
    
    return {"start": min_start, "end": max_end}


def select_all_items_on_track(track_index: int) -> int:
    """Select all items on a track and return count."""
    # Unselect all items first
    unsel_request = {
        "action": "Main_OnCommand",
        "command": 40289,  # Item: Unselect all items
        "project": 0
    }
    ReaperBridge.send_request(unsel_request)
    
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
    track_response = ReaperBridge.send_request(track_request)
    
    if not track_response.get("result"):
        return 0
    
    track_handle = track_response.get("track")
    
    # Get item count
    count_request = {
        "action": "CountTrackMediaItems",
        "track": track_handle
    }
    count_response = ReaperBridge.send_request(count_request)
    item_count = count_response.get("count", 0)
    
    # Select each item
    for i in range(item_count):
        item_request = {
            "action": "GetTrackMediaItem",
            "track": track_handle,
            "itemidx": i
        }
        item_response = ReaperBridge.send_request(item_request)
        
        if item_response.get("result"):
            item_handle = item_response.get("item")
            
            sel_request = {
                "action": "SetMediaItemInfo_Value",
                "item": item_handle,
                "parmname": "B_UISEL",
                "newvalue": 1
            }
            ReaperBridge.send_request(sel_request)
    
    return item_count


def apply_render_settings(settings: Dict[str, Any]) -> None:
    """Apply render settings to the project."""
    # Sample rate
    if "sample_rate" in settings:
        sr_request = {
            "action": "GetSetProjectInfo",
            "project": 0,
            "desc": "RENDER_SRATE",
            "value": settings["sample_rate"],
            "is_set": True
        }
        ReaperBridge.send_request(sr_request)
    
    # Bit depth  
    if "bit_depth" in settings:
        depth_map = {16: 0, 24: 1, 32: 2}
        if settings["bit_depth"] in depth_map:
            depth_request = {
                "action": "GetSetProjectInfo",
                "project": 0,
                "desc": "RENDER_DEPTH",
                "value": depth_map[settings["bit_depth"]],
                "is_set": True
            }
            ReaperBridge.send_request(depth_request)
    
    # Channels
    if "channels" in settings:
        ch_request = {
            "action": "GetSetProjectInfo",
            "project": 0,
            "desc": "RENDER_CHANNELS",
            "value": settings["channels"],
            "is_set": True
        }
        ReaperBridge.send_request(ch_request)
    
    # Dither
    if "dither" in settings:
        dither_request = {
            "action": "GetSetProjectInfo",
            "project": 0,
            "desc": "RENDER_DITHER",
            "value": 1 if settings["dither"] else 0,
            "is_set": True
        }
        ReaperBridge.send_request(dither_request)


def register_bounce_render_tools(mcp):
    """Register bounce and render tools with MCP server."""
    from functools import wraps
    
    # Helper to wrap sync functions for async
    def async_wrapper(func):
        @wraps(func)
        async def wrapper(**kwargs):
            return func(**kwargs)
        return wrapper
    
    # Register all bounce/render tools
    tool_functions = [
        ("bounce_track_in_place", bounce_track_in_place),
        ("bounce_tracks_to_stems", bounce_tracks_to_stems),
        ("freeze_track", freeze_track),
        ("unfreeze_track", unfreeze_track),
        ("render_selected_items_to_new_track", render_selected_items_to_new_track),
        ("glue_selected_items", glue_selected_items),
        ("apply_track_fx_to_items", apply_track_fx_to_items),
        ("create_submix_from_tracks", create_submix_from_tracks),
        ("render_project_to_file", render_project_to_file),
        ("render_time_selection", render_time_selection),
        ("consolidate_track", consolidate_track),
    ]
    
    # Find the corresponding tool definition and register
    for tool_name, tool_func in tool_functions:
        tool_def = next((t for t in tools if t["name"] == tool_name), None)
        if tool_def:
            mcp.tool(
                name=tool_name,
                description=tool_def["description"]
            )(async_wrapper(tool_func))
    
    return len(tool_functions)


# Tool definitions for MCP
tools = [
    {
        "name": "bounce_track_in_place",
        "description": "Bounce a track in place, replacing it with rendered audio",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_index": {"type": "integer", "description": "Index of the track to bounce"},
                "tail_length": {"type": "number", "description": "Additional tail length in seconds", "default": 0.0},
                "render_settings": {
                    "type": "object",
                    "description": "Optional render settings",
                    "properties": {
                        "sample_rate": {"type": "integer"},
                        "bit_depth": {"type": "integer", "enum": [16, 24, 32]},
                        "channels": {"type": "integer"},
                        "dither": {"type": "boolean"}
                    }
                }
            },
            "required": ["track_index"]
        }
    },
    {
        "name": "bounce_tracks_to_stems",
        "description": "Bounce multiple tracks to individual stem files",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_indices": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "List of track indices to bounce"
                },
                "output_directory": {"type": "string", "description": "Directory to save stem files"},
                "file_prefix": {"type": "string", "description": "Prefix for stem filenames", "default": "stem"},
                "tail_length": {"type": "number", "description": "Additional tail length in seconds", "default": 0.0}
            },
            "required": ["track_indices", "output_directory"]
        }
    },
    {
        "name": "freeze_track",
        "description": "Freeze a track to reduce CPU usage",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_index": {"type": "integer", "description": "Index of the track to freeze"},
                "freeze_fx": {"type": "boolean", "description": "Whether to freeze FX", "default": True}
            },
            "required": ["track_index"]
        }
    },
    {
        "name": "unfreeze_track",
        "description": "Unfreeze a previously frozen track",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_index": {"type": "integer", "description": "Index of the track to unfreeze"}
            },
            "required": ["track_index"]
        }
    },
    {
        "name": "render_selected_items_to_new_track",
        "description": "Render selected items to a new track",
        "input_schema": {
            "type": "object",
            "properties": {
                "normalize": {"type": "boolean", "description": "Whether to normalize the rendered audio", "default": False},
                "tail_length": {"type": "number", "description": "Additional tail length in seconds", "default": 0.0}
            },
            "required": []
        }
    },
    {
        "name": "glue_selected_items",
        "description": "Glue selected items together",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "apply_track_fx_to_items",
        "description": "Apply track FX to items on the track as a render",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_index": {"type": "integer", "description": "Index of the track"},
                "fx_only": {"type": "boolean", "description": "Render FX only (dry + FX)", "default": False}
            },
            "required": ["track_index"]
        }
    },
    {
        "name": "create_submix_from_tracks",
        "description": "Create a submix bus from selected tracks",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_indices": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "List of track indices to submix"
                },
                "submix_name": {"type": "string", "description": "Name for the submix track", "default": "Submix"}
            },
            "required": ["track_indices"]
        }
    },
    {
        "name": "render_project_to_file",
        "description": "Render the entire project to a file",
        "input_schema": {
            "type": "object",
            "properties": {
                "output_path": {"type": "string", "description": "Path for the output file"},
                "render_settings": {
                    "type": "object",
                    "description": "Optional render settings",
                    "properties": {
                        "sample_rate": {"type": "integer"},
                        "bit_depth": {"type": "integer", "enum": [16, 24, 32]},
                        "channels": {"type": "integer"},
                        "dither": {"type": "boolean"}
                    }
                }
            },
            "required": ["output_path"]
        }
    },
    {
        "name": "render_time_selection",
        "description": "Render only the time selection to a file",
        "input_schema": {
            "type": "object",
            "properties": {
                "output_path": {"type": "string", "description": "Path for the output file"},
                "render_settings": {
                    "type": "object",
                    "description": "Optional render settings",
                    "properties": {
                        "sample_rate": {"type": "integer"},
                        "bit_depth": {"type": "integer", "enum": [16, 24, 32]},
                        "channels": {"type": "integer"},
                        "dither": {"type": "boolean"}
                    }
                }
            },
            "required": ["output_path"]
        }
    },
    {
        "name": "consolidate_track",
        "description": "Consolidate all items on a track into a single item",
        "input_schema": {
            "type": "object",
            "properties": {
                "track_index": {"type": "integer", "description": "Index of the track to consolidate"}
            },
            "required": ["track_index"]
        }
    }
]