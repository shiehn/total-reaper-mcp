"""Bus routing and mixing workflow tools."""

from typing import Dict, Any, List, Optional, Tuple
from ..reaper_bridge import ReaperBridge


def create_bus_track(name: str, position: Optional[int] = None, 
                    num_channels: int = 2, color: Optional[int] = None) -> Dict[str, Any]:
    """Create a bus track for routing multiple tracks.
    
    Args:
        name: Name for the bus track
        position: Position to insert the bus (None = end)
        num_channels: Number of channels (2 = stereo, 6 = 5.1, etc.)
        color: Optional color (RGB integer)
    
    Returns:
        Dict containing bus track info
    """
    # Determine position
    if position is None:
        count_request = {"action": "CountTracks", "proj": 0}
        count_response = ReaperBridge.send_request(count_request)
        position = count_response.get("count", 0)
    
    # Insert track
    insert_request = {
        "action": "InsertTrackAtIndex",
        "idx": position,
        "wantDefaults": True
    }
    insert_response = ReaperBridge.send_request(insert_request)
    
    if not insert_response.get("result"):
        return {
            "success": False,
            "error": "Failed to create bus track"
        }
    
    # Get track handle
    track_request = {"action": "GetTrack", "proj": 0, "trackidx": position}
    track_response = ReaperBridge.send_request(track_request)
    bus_handle = track_response.get("track")
    
    # Set track name
    name_request = {
        "action": "GetSetMediaTrackInfo_String",
        "track": bus_handle,
        "parmname": "P_NAME",
        "stringNeedBig": False,
        "setnewvalue": True,
        "str": name
    }
    ReaperBridge.send_request(name_request)
    
    # Set channel count
    if num_channels != 2:
        chan_request = {
            "action": "SetMediaTrackInfo_Value",
            "track": bus_handle,
            "parmname": "I_NCHAN",
            "newvalue": num_channels
        }
        ReaperBridge.send_request(chan_request)
    
    # Set color if provided
    if color is not None:
        color_request = {
            "action": "SetMediaTrackInfo_Value",
            "track": bus_handle,
            "parmname": "I_CUSTOMCOLOR",
            "newvalue": color | 0x1000000  # Set custom color flag
        }
        ReaperBridge.send_request(color_request)
    
    # Set as folder track
    folder_request = {
        "action": "SetMediaTrackInfo_Value",
        "track": bus_handle,
        "parmname": "I_FOLDERDEPTH",
        "newvalue": 1
    }
    ReaperBridge.send_request(folder_request)
    
    return {
        "success": True,
        "track_index": position,
        "name": name,
        "num_channels": num_channels
    }


def route_tracks_to_bus(source_track_indices: List[int], bus_track_index: int,
                       send_mode: str = "post-fader", send_level_db: float = 0.0) -> Dict[str, Any]:
    """Route multiple tracks to a bus track.
    
    Args:
        source_track_indices: List of source track indices
        bus_track_index: Index of the bus track
        send_mode: "post-fader", "pre-fader", or "pre-fx"
        send_level_db: Send level in dB
    
    Returns:
        Dict containing routing results
    """
    # Get bus track handle
    bus_request = {"action": "GetTrack", "proj": 0, "trackidx": bus_track_index}
    bus_response = ReaperBridge.send_request(bus_request)
    
    if not bus_response.get("result"):
        return {
            "success": False,
            "error": f"Bus track at index {bus_track_index} not found"
        }
    
    bus_handle = bus_response.get("track")
    
    # Map send mode to value
    send_mode_map = {
        "post-fader": 0,
        "pre-fader": 1,
        "pre-fx": 3
    }
    send_mode_value = send_mode_map.get(send_mode, 0)
    
    routed_tracks = []
    
    for track_index in source_track_indices:
        # Get source track handle
        track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
        track_response = ReaperBridge.send_request(track_request)
        
        if track_response.get("result"):
            track_handle = track_response.get("track")
            
            # Create send
            send_request = {
                "action": "CreateTrackSend",
                "tr": track_handle,
                "desttrInOptional": bus_handle
            }
            send_response = ReaperBridge.send_request(send_request)
            
            if send_response.get("result"):
                send_index = send_response.get("send_index", -1)
                
                # Set send mode
                if send_index >= 0:
                    mode_request = {
                        "action": "SetTrackSendInfo_Value",
                        "tr": track_handle,
                        "category": 0,  # Send
                        "sendidx": send_index,
                        "parmname": "I_SENDMODE",
                        "newvalue": send_mode_value
                    }
                    ReaperBridge.send_request(mode_request)
                    
                    # Set send level
                    if send_level_db != 0.0:
                        # Convert dB to linear
                        level_linear = 10 ** (send_level_db / 20)
                        level_request = {
                            "action": "SetTrackSendInfo_Value",
                            "tr": track_handle,
                            "category": 0,
                            "sendidx": send_index,
                            "parmname": "D_VOL",
                            "newvalue": level_linear
                        }
                        ReaperBridge.send_request(level_request)
                
                routed_tracks.append({
                    "track_index": track_index,
                    "send_index": send_index
                })
    
    return {
        "success": len(routed_tracks) > 0,
        "routed_tracks": routed_tracks,
        "bus_track_index": bus_track_index,
        "send_mode": send_mode
    }


def create_parallel_compression_bus(source_track_indices: List[int], 
                                  bus_name: str = "Parallel Comp",
                                  blend_amount_db: float = -6.0) -> Dict[str, Any]:
    """Create a parallel compression setup with a bus.
    
    Args:
        source_track_indices: Tracks to send to parallel compression
        bus_name: Name for the compression bus
        blend_amount_db: Initial blend amount in dB
    
    Returns:
        Dict containing parallel compression setup info
    """
    # Create the bus track
    bus_result = create_bus_track(bus_name)
    
    if not bus_result["success"]:
        return bus_result
    
    bus_index = bus_result["track_index"]
    
    # Route tracks to bus with pre-fader sends
    route_result = route_tracks_to_bus(
        source_track_indices, 
        bus_index,
        send_mode="pre-fader",
        send_level_db=blend_amount_db
    )
    
    # Add compressor to bus
    bus_request = {"action": "GetTrack", "proj": 0, "trackidx": bus_index}
    bus_response = ReaperBridge.send_request(bus_request)
    bus_handle = bus_response.get("track")
    
    # Add ReaComp
    fx_request = {
        "action": "TrackFX_AddByName",
        "track": bus_handle,
        "fxname": "ReaComp",
        "instantiate": -1
    }
    fx_response = ReaperBridge.send_request(fx_request)
    fx_index = fx_response.get("fx_index", -1)
    
    # Set aggressive compression settings
    if fx_index >= 0:
        # Threshold
        param_request = {
            "action": "TrackFX_SetParam",
            "track": bus_handle,
            "fx": fx_index,
            "param": 0,  # Threshold
            "val": 0.2  # -20dB
        }
        ReaperBridge.send_request(param_request)
        
        # Ratio
        param_request["param"] = 1  # Ratio
        param_request["val"] = 0.8  # 8:1
        ReaperBridge.send_request(param_request)
    
    return {
        "success": True,
        "bus_index": bus_index,
        "bus_name": bus_name,
        "source_tracks": source_track_indices,
        "compressor_added": fx_index >= 0
    }


def create_reverb_send_bus(reverb_type: str = "hall", 
                          return_level_db: float = -12.0) -> Dict[str, Any]:
    """Create a reverb send bus with reverb plugin.
    
    Args:
        reverb_type: Type of reverb ("hall", "room", "plate", "spring")
        return_level_db: Return level in dB
    
    Returns:
        Dict containing reverb bus info
    """
    # Create reverb bus
    bus_name = f"Reverb {reverb_type.capitalize()}"
    bus_result = create_bus_track(bus_name, color=0x00FF00)  # Green
    
    if not bus_result["success"]:
        return bus_result
    
    bus_index = bus_result["track_index"]
    
    # Get bus handle
    bus_request = {"action": "GetTrack", "proj": 0, "trackidx": bus_index}
    bus_response = ReaperBridge.send_request(bus_request)
    bus_handle = bus_response.get("track")
    
    # Add reverb plugin
    fx_request = {
        "action": "TrackFX_AddByName",
        "track": bus_handle,
        "fxname": "ReaVerbate",
        "instantiate": -1
    }
    fx_response = ReaperBridge.send_request(fx_request)
    fx_index = fx_response.get("fx_index", -1)
    
    # Set track volume (return level)
    if return_level_db != 0.0:
        level_linear = 10 ** (return_level_db / 20)
        vol_request = {
            "action": "SetMediaTrackInfo_Value",
            "track": bus_handle,
            "parmname": "D_VOL",
            "newvalue": level_linear
        }
        ReaperBridge.send_request(vol_request)
    
    # Set to 100% wet
    if fx_index >= 0:
        wet_request = {
            "action": "TrackFX_SetParam",
            "track": bus_handle,
            "fx": fx_index,
            "param": 4,  # Wet parameter for ReaVerbate
            "val": 1.0  # 100% wet
        }
        ReaperBridge.send_request(wet_request)
    
    return {
        "success": True,
        "bus_index": bus_index,
        "bus_name": bus_name,
        "reverb_type": reverb_type,
        "reverb_added": fx_index >= 0,
        "return_level_db": return_level_db
    }


def create_stem_buses(stem_groups: Dict[str, List[int]]) -> Dict[str, Any]:
    """Create stem buses for groups of tracks.
    
    Args:
        stem_groups: Dict mapping stem names to track indices
                    e.g., {"Drums": [0, 1, 2], "Bass": [3], "Keys": [4, 5]}
    
    Returns:
        Dict containing created stem buses
    """
    created_stems = []
    
    # Define colors for common stem types
    stem_colors = {
        "drums": 0xFF0000,  # Red
        "bass": 0x00FF00,   # Green
        "keys": 0x0000FF,   # Blue
        "guitar": 0xFF8800, # Orange
        "vocals": 0xFF00FF, # Magenta
        "synth": 0x00FFFF,  # Cyan
    }
    
    for stem_name, track_indices in stem_groups.items():
        # Get color based on stem name
        color = None
        for key, col in stem_colors.items():
            if key in stem_name.lower():
                color = col
                break
        
        # Create stem bus
        bus_result = create_bus_track(stem_name, color=color)
        
        if bus_result["success"]:
            bus_index = bus_result["track_index"]
            
            # Route tracks to stem bus
            route_result = route_tracks_to_bus(
                track_indices,
                bus_index,
                send_mode="post-fader"
            )
            
            # Remove master sends from source tracks
            for track_index in track_indices:
                track_request = {"action": "GetTrack", "proj": 0, "trackidx": track_index}
                track_response = ReaperBridge.send_request(track_request)
                
                if track_response.get("result"):
                    track_handle = track_response.get("track")
                    master_request = {
                        "action": "SetMediaTrackInfo_Value",
                        "track": track_handle,
                        "parmname": "B_MAINSEND",
                        "newvalue": 0
                    }
                    ReaperBridge.send_request(master_request)
            
            created_stems.append({
                "name": stem_name,
                "bus_index": bus_index,
                "source_tracks": track_indices
            })
    
    return {
        "success": len(created_stems) > 0,
        "stems_created": created_stems
    }


def create_sidechain_routing(source_track_index: int, destination_track_index: int,
                           channel_offset: int = 2) -> Dict[str, Any]:
    """Create sidechain routing between tracks.
    
    Args:
        source_track_index: Track providing sidechain signal
        destination_track_index: Track receiving sidechain
        channel_offset: Channel offset for sidechain (usually 3/4)
    
    Returns:
        Dict containing sidechain routing info
    """
    # Get track handles
    source_request = {"action": "GetTrack", "proj": 0, "trackidx": source_track_index}
    source_response = ReaperBridge.send_request(source_request)
    
    dest_request = {"action": "GetTrack", "proj": 0, "trackidx": destination_track_index}
    dest_response = ReaperBridge.send_request(dest_request)
    
    if not (source_response.get("result") and dest_response.get("result")):
        return {
            "success": False,
            "error": "Source or destination track not found"
        }
    
    source_handle = source_response.get("track")
    dest_handle = dest_response.get("track")
    
    # Ensure destination has enough channels
    chan_request = {
        "action": "SetMediaTrackInfo_Value",
        "track": dest_handle,
        "parmname": "I_NCHAN",
        "newvalue": max(4, channel_offset + 2)  # At least 4 channels
    }
    ReaperBridge.send_request(chan_request)
    
    # Create send with channel offset
    send_request = {
        "action": "CreateTrackSend",
        "tr": source_handle,
        "desttrInOptional": dest_handle
    }
    send_response = ReaperBridge.send_request(send_request)
    
    if send_response.get("result"):
        send_index = send_response.get("send_index", -1)
        
        if send_index >= 0:
            # Set destination channels (3/4 for sidechain)
            chan_request = {
                "action": "SetTrackSendInfo_Value",
                "tr": source_handle,
                "category": 0,
                "sendidx": send_index,
                "parmname": "I_DSTCHAN",
                "newvalue": channel_offset
            }
            ReaperBridge.send_request(chan_request)
            
            # Set to post-fader
            mode_request = {
                "action": "SetTrackSendInfo_Value",
                "tr": source_handle,
                "category": 0,
                "sendidx": send_index,
                "parmname": "I_SENDMODE",
                "newvalue": 0
            }
            ReaperBridge.send_request(mode_request)
    
    return {
        "success": send_response.get("result", False),
        "source_track": source_track_index,
        "destination_track": destination_track_index,
        "sidechain_channels": f"{channel_offset+1}/{channel_offset+2}"
    }


def setup_monitor_mix(performer_tracks: List[int], click_track_index: Optional[int] = None,
                     output_channel: int = 2) -> Dict[str, Any]:
    """Setup a monitor mix for performers.
    
    Args:
        performer_tracks: Track indices to include in monitor mix
        click_track_index: Optional click track index
        output_channel: Hardware output channel (0-based)
    
    Returns:
        Dict containing monitor mix setup info
    """
    # Create monitor bus
    bus_result = create_bus_track("Monitor Mix", num_channels=2)
    
    if not bus_result["success"]:
        return bus_result
    
    monitor_bus_index = bus_result["track_index"]
    
    # Get monitor bus handle
    bus_request = {"action": "GetTrack", "proj": 0, "trackidx": monitor_bus_index}
    bus_response = ReaperBridge.send_request(bus_request)
    monitor_handle = bus_response.get("track")
    
    # Set hardware output
    hw_request = {
        "action": "SetMediaTrackInfo_Value",
        "track": monitor_handle,
        "parmname": "I_HWOUT",
        "newvalue": output_channel | 1024  # Enable hardware output
    }
    ReaperBridge.send_request(hw_request)
    
    # Remove master send from monitor bus
    master_request = {
        "action": "SetMediaTrackInfo_Value",
        "track": monitor_handle,
        "parmname": "B_MAINSEND",
        "newvalue": 0
    }
    ReaperBridge.send_request(master_request)
    
    # Route performer tracks to monitor
    all_tracks = performer_tracks.copy()
    if click_track_index is not None:
        all_tracks.append(click_track_index)
    
    route_result = route_tracks_to_bus(
        all_tracks,
        monitor_bus_index,
        send_mode="pre-fader"
    )
    
    return {
        "success": True,
        "monitor_bus_index": monitor_bus_index,
        "performer_tracks": performer_tracks,
        "click_included": click_track_index is not None,
        "output_channel": output_channel + 1  # 1-based for display
    }


def create_headphone_cue_mixes(num_mixes: int = 4) -> Dict[str, Any]:
    """Create multiple headphone cue mixes.
    
    Args:
        num_mixes: Number of cue mixes to create
    
    Returns:
        Dict containing cue mix info
    """
    cue_mixes = []
    
    for i in range(num_mixes):
        # Create cue bus
        bus_name = f"Cue Mix {i+1}"
        bus_result = create_bus_track(bus_name, color=0x888888)  # Gray
        
        if bus_result["success"]:
            bus_index = bus_result["track_index"]
            
            # Get bus handle
            bus_request = {"action": "GetTrack", "proj": 0, "trackidx": bus_index}
            bus_response = ReaperBridge.send_request(bus_request)
            bus_handle = bus_response.get("track")
            
            # Set hardware output (pairs: 1/2, 3/4, 5/6, 7/8)
            output_channel = i * 2
            hw_request = {
                "action": "SetMediaTrackInfo_Value",
                "track": bus_handle,
                "parmname": "I_HWOUT",
                "newvalue": output_channel | 1024
            }
            ReaperBridge.send_request(hw_request)
            
            # Remove master send
            master_request = {
                "action": "SetMediaTrackInfo_Value",
                "track": bus_handle,
                "parmname": "B_MAINSEND",
                "newvalue": 0
            }
            ReaperBridge.send_request(master_request)
            
            cue_mixes.append({
                "name": bus_name,
                "bus_index": bus_index,
                "output_channels": f"{output_channel+1}/{output_channel+2}"
            })
    
    return {
        "success": len(cue_mixes) > 0,
        "cue_mixes": cue_mixes
    }


def analyze_routing_matrix() -> Dict[str, Any]:
    """Analyze and return the current routing matrix.
    
    Returns:
        Dict containing routing analysis
    """
    # Get track count
    count_request = {"action": "CountTracks", "proj": 0}
    count_response = ReaperBridge.send_request(count_request)
    track_count = count_response.get("count", 0)
    
    routing_info = []
    
    for i in range(track_count):
        # Get track info
        track_request = {"action": "GetTrack", "proj": 0, "trackidx": i}
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
            track_name = name_response.get("str", f"Track {i+1}")
            
            # Check master send
            master_request = {
                "action": "GetMediaTrackInfo_Value",
                "track": track_handle,
                "parmname": "B_MAINSEND"
            }
            master_response = ReaperBridge.send_request(master_request)
            has_master_send = master_response.get("value", 1) > 0
            
            # Get send count
            send_count_request = {
                "action": "GetTrackNumSends",
                "tr": track_handle,
                "category": 0  # Regular sends
            }
            send_count_response = ReaperBridge.send_request(send_count_request)
            num_sends = send_count_response.get("count", 0)
            
            # Get receive count
            receive_count_request = {
                "action": "GetTrackNumSends",
                "tr": track_handle,
                "category": -1  # Receives
            }
            receive_count_response = ReaperBridge.send_request(receive_count_request)
            num_receives = receive_count_response.get("count", 0)
            
            track_info = {
                "index": i,
                "name": track_name,
                "has_master_send": has_master_send,
                "num_sends": num_sends,
                "num_receives": num_receives,
                "sends": [],
                "receives": []
            }
            
            # Get send details
            for s in range(num_sends):
                dest_request = {
                    "action": "GetTrackSendInfo_Value",
                    "tr": track_handle,
                    "category": 0,
                    "sendidx": s,
                    "parmname": "P_DESTTRACK"
                }
                dest_response = ReaperBridge.send_request(dest_request)
                
                # Get destination track name
                dest_handle = dest_response.get("value")
                if dest_handle:
                    dest_name_request = {
                        "action": "GetSetMediaTrackInfo_String",
                        "track": dest_handle,
                        "parmname": "P_NAME",
                        "stringNeedBig": False,
                        "setnewvalue": False
                    }
                    dest_name_response = ReaperBridge.send_request(dest_name_request)
                    dest_name = dest_name_response.get("str", "Unknown")
                    
                    track_info["sends"].append({
                        "index": s,
                        "destination": dest_name
                    })
            
            routing_info.append(track_info)
    
    return {
        "success": True,
        "track_count": track_count,
        "routing": routing_info
    }


def register_bus_routing_tools(mcp):
    """Register bus routing tools with MCP server."""
    from functools import wraps
    
    # Helper to wrap sync functions for async
    def async_wrapper(func):
        @wraps(func)
        async def wrapper(**kwargs):
            return func(**kwargs)
        return wrapper
    
    # Register all bus routing tools
    tool_functions = [
        ("create_bus_track", create_bus_track),
        ("route_tracks_to_bus", route_tracks_to_bus),
        ("create_parallel_compression_bus", create_parallel_compression_bus),
        ("create_reverb_send_bus", create_reverb_send_bus),
        ("create_stem_buses", create_stem_buses),
        ("create_sidechain_routing", create_sidechain_routing),
        ("setup_monitor_mix", setup_monitor_mix),
        ("create_headphone_cue_mixes", create_headphone_cue_mixes),
        ("analyze_routing_matrix", analyze_routing_matrix),
    ]
    
    # Find the corresponding tool definition and register
    for tool_name, tool_func in tool_functions:
        tool_def = next((t for t in tools if t["name"] == tool_name), None)
        if tool_def:
            mcp.tool(
                name=tool_name,
                description=tool_def["description"], 
                params=tool_def["input_schema"]
            )(async_wrapper(tool_func))
    
    return len(tool_functions)


# Tool definitions for MCP
tools = [
    {
        "name": "create_bus_track",
        "description": "Create a bus track for routing multiple tracks",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name for the bus track"},
                "position": {"type": "integer", "description": "Position to insert (None = end)"},
                "num_channels": {"type": "integer", "description": "Number of channels", "default": 2},
                "color": {"type": "integer", "description": "RGB color as integer"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "route_tracks_to_bus",
        "description": "Route multiple tracks to a bus track",
        "input_schema": {
            "type": "object",
            "properties": {
                "source_track_indices": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "List of source track indices"
                },
                "bus_track_index": {"type": "integer", "description": "Index of the bus track"},
                "send_mode": {
                    "type": "string",
                    "enum": ["post-fader", "pre-fader", "pre-fx"],
                    "description": "Send mode",
                    "default": "post-fader"
                },
                "send_level_db": {"type": "number", "description": "Send level in dB", "default": 0.0}
            },
            "required": ["source_track_indices", "bus_track_index"]
        }
    },
    {
        "name": "create_parallel_compression_bus",
        "description": "Create a parallel compression setup with a bus",
        "input_schema": {
            "type": "object",
            "properties": {
                "source_track_indices": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Tracks to send to parallel compression"
                },
                "bus_name": {"type": "string", "description": "Name for the compression bus", "default": "Parallel Comp"},
                "blend_amount_db": {"type": "number", "description": "Initial blend amount in dB", "default": -6.0}
            },
            "required": ["source_track_indices"]
        }
    },
    {
        "name": "create_reverb_send_bus",
        "description": "Create a reverb send bus with reverb plugin",
        "input_schema": {
            "type": "object",
            "properties": {
                "reverb_type": {
                    "type": "string",
                    "enum": ["hall", "room", "plate", "spring"],
                    "description": "Type of reverb",
                    "default": "hall"
                },
                "return_level_db": {"type": "number", "description": "Return level in dB", "default": -12.0}
            },
            "required": []
        }
    },
    {
        "name": "create_stem_buses",
        "description": "Create stem buses for groups of tracks",
        "input_schema": {
            "type": "object",
            "properties": {
                "stem_groups": {
                    "type": "object",
                    "description": "Dict mapping stem names to track indices",
                    "additionalProperties": {
                        "type": "array",
                        "items": {"type": "integer"}
                    }
                }
            },
            "required": ["stem_groups"]
        }
    },
    {
        "name": "create_sidechain_routing",
        "description": "Create sidechain routing between tracks",
        "input_schema": {
            "type": "object",
            "properties": {
                "source_track_index": {"type": "integer", "description": "Track providing sidechain signal"},
                "destination_track_index": {"type": "integer", "description": "Track receiving sidechain"},
                "channel_offset": {"type": "integer", "description": "Channel offset for sidechain", "default": 2}
            },
            "required": ["source_track_index", "destination_track_index"]
        }
    },
    {
        "name": "setup_monitor_mix",
        "description": "Setup a monitor mix for performers",
        "input_schema": {
            "type": "object",
            "properties": {
                "performer_tracks": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Track indices to include"
                },
                "click_track_index": {"type": "integer", "description": "Optional click track index"},
                "output_channel": {"type": "integer", "description": "Hardware output channel", "default": 2}
            },
            "required": ["performer_tracks"]
        }
    },
    {
        "name": "create_headphone_cue_mixes",
        "description": "Create multiple headphone cue mixes",
        "input_schema": {
            "type": "object",
            "properties": {
                "num_mixes": {"type": "integer", "description": "Number of cue mixes", "default": 4}
            },
            "required": []
        }
    },
    {
        "name": "analyze_routing_matrix",
        "description": "Analyze and return the current routing matrix",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]