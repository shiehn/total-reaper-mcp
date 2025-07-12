#!/usr/bin/env python3
"""
REAPER MCP Server - File-based Bridge Version with Full API
This version implements all tools from app.py but uses file-based communication
"""

import os
import json
import time
import asyncio
import logging
from pathlib import Path
from mcp import Tool
from mcp.types import TextContent
from mcp.server import Server

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the bridge directory from environment or use default
BRIDGE_DIR = Path(os.environ.get(
    'REAPER_MCP_BRIDGE_DIR',
    os.path.expanduser('~/Library/Application Support/REAPER/Scripts/mcp_bridge_data')
))

# Ensure bridge directory exists
BRIDGE_DIR.mkdir(parents=True, exist_ok=True)

logger.info(f"Bridge directory: {BRIDGE_DIR}")

class ReaperFileBridge:
    """File-based bridge for communicating with REAPER"""
    
    def __init__(self):
        self.bridge_dir = BRIDGE_DIR
        self.request_id = 0
        
    async def call_lua(self, func_name, args=None):
        """Call a Lua function and wait for response"""
        self.request_id += 1
        request_file = self.bridge_dir / f"request_{self.request_id}.json"
        response_file = self.bridge_dir / f"response_{self.request_id}.json"
        
        # Write request
        request_data = {
            "id": self.request_id,
            "func": func_name,
            "args": args or []
        }
        
        try:
            with open(request_file, 'w') as f:
                json.dump(request_data, f)
            
            # Wait for response (with timeout)
            start_time = time.time()
            timeout = 5.0  # 5 second timeout
            
            while time.time() - start_time < timeout:
                if response_file.exists():
                    try:
                        with open(response_file, 'r') as f:
                            response = json.load(f)
                        # Clean up files
                        request_file.unlink(missing_ok=True)
                        response_file.unlink(missing_ok=True)
                        return response
                    except json.JSONDecodeError:
                        # File might be partially written, wait a bit
                        await asyncio.sleep(0.01)
                await asyncio.sleep(0.1)
            
            # Timeout
            logger.error("Timeout waiting for REAPER response")
            return {"ok": False, "error": "Timeout waiting for REAPER"}
            
        except Exception as e:
            logger.error(f"Error communicating with REAPER: {e}")
            return {"ok": False, "error": str(e)}

bridge = ReaperFileBridge()

app = Server("reaper-mcp")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="insert_track",
            description="Insert a new track at the specified index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "The index where the track should be inserted (0-based)",
                        "minimum": 0
                    },
                    "use_defaults": {
                        "type": "boolean",
                        "description": "Whether to use default track settings",
                        "default": True
                    }
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="get_track_count",
            description="Get the number of tracks in the current project",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_reaper_version",
            description="Get the REAPER version string",
            inputSchema={
                "type": "object", 
                "properties": {}
            }
        ),
        Tool(
            name="get_track",
            description="Get a track by index from the current project",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="set_track_selected",
            description="Select or deselect a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Whether to select (true) or deselect (false) the track"
                    }
                },
                "required": ["track_index", "selected"]
            }
        ),
        Tool(
            name="get_track_name",
            description="Get the name of a track by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_name",
            description="Set the name of a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "name": {
                        "type": "string",
                        "description": "The new name for the track"
                    }
                },
                "required": ["track_index", "name"]
            }
        ),
        Tool(
            name="get_master_track",
            description="Get the master track",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="delete_track",
            description="Delete a track by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="get_track_mute",
            description="Get track mute state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_mute",
            description="Set track mute state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "mute": {
                        "type": "boolean",
                        "description": "Whether to mute (true) or unmute (false) the track"
                    }
                },
                "required": ["track_index", "mute"]
            }
        ),
        Tool(
            name="get_track_solo",
            description="Get track solo state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_solo",
            description="Set track solo state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "solo": {
                        "type": "boolean",
                        "description": "Whether to solo (true) or unsolo (false) the track"
                    }
                },
                "required": ["track_index", "solo"]
            }
        ),
        Tool(
            name="get_track_volume",
            description="Get track volume in dB",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ['track_index']
            }
        ),
        Tool(
            name="set_track_volume",
            description="Set track volume in dB",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "volume_db": {
                        "type": "number",
                        "description": "Volume in dB (0.0 = unity gain, -inf = mute)"
                    }
                },
                "required": ['track_index', 'volume_db']
            }
        ),
        Tool(
            name="get_track_pan",
            description="Get track pan position (-1.0 to 1.0)",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ['track_index']
            }
        ),
        Tool(
            name="set_track_pan",
            description="Set track pan position (-1.0 to 1.0)",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "pan": {
                        "type": "number",
                        "description": "Pan position (-1.0 = full left, 0.0 = center, 1.0 = full right)",
                        "minimum": -1.0,
                        "maximum": 1.0
                    }
                },
                "required": ['track_index', 'pan']
            }
        ),
        Tool(
            name="add_media_item_to_track",
            description="Add a new media item to a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index",
                        "minimum": 0
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="count_media_items",
            description="Count total media items in project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "minimum": 0,
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_media_item",
            description="Get media item by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "minimum": 0,
                        "default": 0
                    },
                    "item_index": {
                        "type": "integer",
                        "description": "Item index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="delete_track_media_item",
            description="Delete a media item from track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index",
                        "minimum": 0
                    },
                    "item_index": {
                        "type": "integer",
                        "description": "Item index on track",
                        "minimum": 0
                    }
                },
                "required": ["track_index", "item_index"]
            }
        ),
        Tool(
            name="get_media_item_length",
            description="Get media item length",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index",
                        "minimum": 0
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="set_media_item_length",
            description="Set media item length",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index",
                        "minimum": 0
                    },
                    "length": {
                        "type": "number",
                        "description": "New length in seconds"
                    }
                },
                "required": ["item_index", "length"]
            }
        ),
        Tool(
            name="get_media_item_position",
            description="Get media item position",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index",
                        "minimum": 0
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="set_media_item_position",
            description="Set media item position",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index",
                        "minimum": 0
                    },
                    "position": {
                        "type": "number",
                        "description": "New position in seconds"
                    }
                },
                "required": ["item_index", "position"]
            }
        ),
        Tool(
            name="get_project_name",
            description="Get the current project name",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "minimum": 0,
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_project_path",
            description="Get the current project path",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "minimum": 0,
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="save_project",
            description="Save the current project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "minimum": 0,
                        "default": 0
                    },
                    "force_save_as": {
                        "type": "boolean",
                        "description": "Force save as dialog",
                        "default": False
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_cursor_position",
            description="Get the edit cursor position in seconds",
            inputSchema={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        Tool(
            name="set_edit_cursor_position",
            description="Set the edit cursor position",
            inputSchema={
                "type": "object",
                "properties": {
                    "time": {
                        "type": "number",
                        "description": "Time in seconds"
                    },
                    "move_view": {
                        "type": "boolean",
                        "description": "Move view to cursor",
                        "default": True
                    },
                    "seek_play": {
                        "type": "boolean",
                        "description": "Seek playback to cursor",
                        "default": False
                    }
                },
                "required": ["time"]
            }
        ),
        Tool(
            name="get_play_state",
            description="Get current playback state",
            inputSchema={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        Tool(
            name="play",
            description="Start playback",
            inputSchema={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        Tool(
            name="stop",
            description="Stop playback",
            inputSchema={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        Tool(
            name="pause",
            description="Pause playback",
            inputSchema={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        Tool(
            name="record",
            description="Start recording",
            inputSchema={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        Tool(
            name="set_play_state",
            description="Set the transport play state (play, pause, record)",
            inputSchema={
                "type": "object",
                "properties": {
                    "play": {
                        "type": "boolean",
                        "description": "Set play state"
                    },
                    "pause": {
                        "type": "boolean", 
                        "description": "Set pause state"
                    },
                    "record": {
                        "type": "boolean",
                        "description": "Set record state"
                    }
                },
                "required": ["play", "pause", "record"]
            }
        ),
        Tool(
            name="set_repeat_state",
            description="Set the repeat/loop state",
            inputSchema={
                "type": "object",
                "properties": {
                    "repeat": {
                        "type": "boolean",
                        "description": "Enable or disable repeat/loop"
                    }
                },
                "required": ["repeat"]
            }
        ),
        Tool(
            name="execute_action",
            description="Execute a REAPER action by command ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "command_id": {
                        "type": "integer",
                        "description": "Command ID"
                    },
                    "flag": {
                        "type": "integer",
                        "description": "Flag (0=normal)",
                        "default": 0
                    }
                },
                "required": ["command_id"]
            }
        ),
        Tool(
            name="undo_begin_block",
            description="Begin an undo block",
            inputSchema={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        Tool(
            name="undo_end_block",
            description="End an undo block with description",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Description of the changes"
                    },
                    "flags": {
                        "type": "integer",
                        "description": "Flags (-1 for all)",
                        "default": -1
                    }
                },
                "required": ["description"]
            }
        ),
        Tool(
            name="update_arrange",
            description="Update the arrange view",
            inputSchema={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        Tool(
            name="update_timeline",
            description="Update the timeline display",
            inputSchema={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        Tool(
            name="add_project_marker",
            description="Add a marker or region to the project",
            inputSchema={
                "type": "object",
                "properties": {
                    "is_region": {
                        "type": "boolean",
                        "description": "True for region, false for marker"
                    },
                    "position": {
                        "type": "number",
                        "description": "Position in seconds"
                    },
                    "region_end": {
                        "type": "number",
                        "description": "End position for regions (ignored for markers)"
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of the marker/region"
                    },
                    "want_index": {
                        "type": "integer",
                        "description": "Desired index number (-1 to auto-assign)",
                        "default": -1
                    }
                },
                "required": ["is_region", "position", "name"]
            }
        ),
        Tool(
            name="delete_project_marker",
            description="Delete a marker or region by its displayed number",
            inputSchema={
                "type": "object",
                "properties": {
                    "marker_index": {
                        "type": "integer",
                        "description": "The displayed marker/region number to delete"
                    },
                    "is_region": {
                        "type": "boolean",
                        "description": "True if deleting a region, false for marker"
                    }
                },
                "required": ["marker_index", "is_region"]
            }
        ),
        Tool(
            name="count_project_markers",
            description="Count the number of markers and regions in the project",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="enum_project_markers",
            description="Get information about a specific marker/region by its index",
            inputSchema={
                "type": "object",
                "properties": {
                    "marker_index": {
                        "type": "integer",
                        "description": "The index of the marker/region (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["marker_index"]
            }
        ),
        Tool(
            name="get_loop_time_range",
            description="Get the current time selection or loop range",
            inputSchema={
                "type": "object",
                "properties": {
                    "is_loop": {
                        "type": "boolean",
                        "description": "True to get loop range, false for time selection",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="set_loop_time_range",
            description="Set the time selection or loop range",
            inputSchema={
                "type": "object",
                "properties": {
                    "is_loop": {
                        "type": "boolean",
                        "description": "True to set loop range, false for time selection"
                    },
                    "start": {
                        "type": "number",
                        "description": "Start time in seconds"
                    },
                    "end": {
                        "type": "number",
                        "description": "End time in seconds"
                    },
                    "allow_autoseek": {
                        "type": "boolean",
                        "description": "Allow automatic seeking to the new range",
                        "default": False
                    }
                },
                "required": ["is_loop", "start", "end"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.info(f"Tool called: {name} with args: {arguments}")
    
    if name == "insert_track":
        index = arguments["index"]
        use_defaults = arguments.get("use_defaults", True)
        
        result = await bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully inserted track at index {index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to insert track: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_count":
        result = await bridge.call_lua("CountTracks", [0])
        
        if result.get("ok"):
            count = result.get("ret", 0)
            return [TextContent(
                type="text",
                text=f"Current project has {count} tracks"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track count: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_reaper_version":
        result = await bridge.call_lua("GetAppVersion")
        
        if result.get("ok"):
            version = result.get("ret", "Unknown")
            return [TextContent(
                type="text",
                text=f"REAPER version: {version}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get REAPER version: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track":
        index = arguments["index"]
        result = await bridge.call_lua("GetTrack", [0, index])
        
        if result.get("ok"):
            track_ptr = result.get("ret")
            if track_ptr:
                return [TextContent(
                    type="text",
                    text=f"Track at index {index}: {track_ptr}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"No track found at index {index}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_selected":
        track_index = arguments["track_index"]
        selected = arguments["selected"]
        
        # First get the track pointer
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        # Then set its selection state
        result = await bridge.call_lua("SetTrackSelected", [track_index, selected])
        
        if result.get("ok"):
            action = "selected" if selected else "deselected"
            return [TextContent(
                type="text",
                text=f"Track at index {track_index} has been {action}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track selection: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_name":
        track_index = arguments["track_index"]
        
        result = await bridge.call_lua("GetTrackName", [track_index])
        
        if result.get("ok"):
            track_name = result.get("ret", "")
            if track_name:
                return [TextContent(
                    type="text",
                    text=f"Track {track_index} name: \"{track_name}\""
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Track {track_index} has no name"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track name: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_name":
        track_index = arguments["track_index"]
        name = arguments["name"]
        
        result = await bridge.call_lua("SetTrackName", [track_index, name])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track {track_index} renamed to \"{name}\""
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track name: {result.get('error', 'Unknown error')}"
            )]
            
    elif name == "get_master_track":
        result = await bridge.call_lua("GetMasterTrack", [0])
        
        if result.get("ok"):
            master_track = result.get("ret")
            return [TextContent(
                type="text",
                text=f"Master track: {master_track}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get master track: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "delete_track":
        track_index = arguments["track_index"]
        
        # Use the index-based delete directly
        result = await bridge.call_lua("DeleteTrackByIndex", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully deleted track at index {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete track: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_mute":
        track_index = arguments["track_index"]
        
        # Get track first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_result.get("ret"), "B_MUTE"])
        
        if result.get("ok"):
            is_muted = bool(result.get("ret", 0))
            return [TextContent(
                type="text",
                text=f"Track {track_index} is {'muted' if is_muted else 'unmuted'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track mute state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_mute":
        track_index = arguments["track_index"]
        mute = arguments["mute"]
        
        # Get track first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_result.get("ret"), "B_MUTE", 1 if mute else 0])
        
        if result.get("ok"):
            state = "muted" if mute else "unmuted"
            return [TextContent(
                type="text",
                text=f"Track {track_index} {state}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track mute state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_solo":
        track_index = arguments["track_index"]
        
        # Get track first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_result.get("ret"), "I_SOLO"])
        
        if result.get("ok"):
            solo_state = int(result.get("ret", 0))
            solo_text = "not soloed" if solo_state == 0 else "soloed"
            return [TextContent(
                type="text",
                text=f"Track {track_index} solo state: {solo_text}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track solo state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_solo":
        track_index = arguments["track_index"]
        solo = arguments["solo"]
        
        # Get track first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_result.get("ret"), "I_SOLO", 1 if solo else 0])
        
        if result.get("ok"):
            state = "soloed" if solo else "unsoloed"
            return [TextContent(
                type="text",
                text=f"Track {track_index} {state}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track solo state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_volume":
        track_index = arguments["track_index"]
        
        # Get track first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_result.get("ret"), "D_VOL"])
        
        if result.get("ok"):
            vol_linear = result.get("ret", 1.0)
            # Convert to dB
            import math
            if vol_linear > 0:
                vol_db = 20 * math.log10(vol_linear)
            else:
                vol_db = -math.inf
            return [TextContent(
                type="text",
                text=f"Track {track_index} volume: {vol_db:.2f} dB"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track volume: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_volume":
        track_index = arguments["track_index"]
        volume_db = arguments["volume_db"]
        
        # Get track first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        # Convert dB to linear
        import math
        if volume_db > -150:
            vol_linear = 10 ** (volume_db / 20)
        else:
            vol_linear = 0
        
        result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_result.get("ret"), "D_VOL", vol_linear])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track {track_index} volume set to {volume_db:.2f} dB"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track volume: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_pan":
        track_index = arguments["track_index"]
        
        # Get track first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_result.get("ret"), "D_PAN"])
        
        if result.get("ok"):
            pan = result.get("ret", 0.0)
            return [TextContent(
                type="text",
                text=f"Track {track_index} pan: {pan:.2f}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track pan: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_pan":
        track_index = arguments["track_index"]
        pan = arguments["pan"]
        
        # Get track first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        # Clamp pan value
        pan = max(-1.0, min(1.0, pan))
        
        result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_result.get("ret"), "D_PAN", pan])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track {track_index} pan set to {pan:.2f}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track pan: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "add_media_item_to_track":
        track_index = arguments["track_index"]
        
        # Get track first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = await bridge.call_lua("AddMediaItemToTrack", [track_result.get("ret")])
        
        if result.get("ok"):
            item = result.get("ret")
            return [TextContent(
                type="text",
                text=f"Added media item to track {track_index}: {item}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add media item: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "count_media_items":
        project_index = arguments.get("project_index", 0)
        
        result = await bridge.call_lua("CountMediaItems", [project_index])
        
        if result.get("ok"):
            count = result.get("ret", 0)
            return [TextContent(
                type="text",
                text=f"Project has {count} media items"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count media items: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_media_item":
        project_index = arguments.get("project_index", 0)
        item_index = arguments["item_index"]
        
        result = await bridge.call_lua("GetMediaItem", [project_index, item_index])
        
        if result.get("ok"):
            item = result.get("ret")
            if item:
                return [TextContent(
                    type="text",
                    text=f"Media item at index {item_index}: {item}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"No media item found at index {item_index}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "delete_track_media_item":
        track_index = arguments["track_index"]
        item_index = arguments["item_index"]
        
        # Get track first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        # Get item on track
        item_result = await bridge.call_lua("GetTrackMediaItem", [track_result.get("ret"), item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item {item_index} on track {track_index}"
            )]
        
        # Delete item
        result = await bridge.call_lua("DeleteTrackMediaItem", [track_result.get("ret"), item_result.get("ret")])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Deleted media item {item_index} from track {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete media item: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_media_item_length":
        item_index = arguments["item_index"]
        
        # Get item first
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        result = await bridge.call_lua("GetMediaItemInfo_Value", [item_result.get("ret"), "D_LENGTH"])
        
        if result.get("ok"):
            length = result.get("ret", 0.0)
            return [TextContent(
                type="text",
                text=f"Media item {item_index} length: {length:.3f} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item length: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_media_item_length":
        item_index = arguments["item_index"]
        length = arguments["length"]
        
        # Get item first
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        result = await bridge.call_lua("SetMediaItemLength", [item_result.get("ret"), length, True])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item {item_index} length to {length:.3f} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item length: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_media_item_position":
        item_index = arguments["item_index"]
        
        # Get item first
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        result = await bridge.call_lua("GetMediaItemInfo_Value", [item_result.get("ret"), "D_POSITION"])
        
        if result.get("ok"):
            position = result.get("ret", 0.0)
            return [TextContent(
                type="text",
                text=f"Media item {item_index} position: {position:.3f} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item position: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_media_item_position":
        item_index = arguments["item_index"]
        position = arguments["position"]
        
        # Get item first
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        result = await bridge.call_lua("SetMediaItemPosition", [item_result.get("ret"), position, True])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item {item_index} position to {position:.3f} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item position: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_project_name":
        project_index = arguments.get("project_index", 0)
        
        result = await bridge.call_lua("GetProjectName", [project_index, "", 512])
        
        if result.get("ok"):
            ret = result.get("ret", [])
            if isinstance(ret, list) and len(ret) > 0:
                project_name = ret[0] if len(ret) > 0 else "Untitled"
                return [TextContent(
                    type="text",
                    text=f"Project name: {project_name}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="Project name: Untitled"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project name: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_project_path":
        project_index = arguments.get("project_index", 0)
        
        result = await bridge.call_lua("GetProjectPath", ["", 2048])
        
        if result.get("ok"):
            path = result.get("ret", "")
            return [TextContent(
                type="text",
                text=f"Project path: {path}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project path: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "save_project":
        project_index = arguments.get("project_index", 0)
        force_save_as = arguments.get("force_save_as", False)
        
        result = await bridge.call_lua("Main_SaveProject", [project_index, force_save_as])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Project saved successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to save project: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_cursor_position":
        result = await bridge.call_lua("GetCursorPosition")
        
        if result.get("ok"):
            position = result.get("ret", 0.0)
            return [TextContent(
                type="text",
                text=f"Edit cursor position: {position:.3f} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get cursor position: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_edit_cursor_position":
        time = arguments["time"]
        move_view = arguments.get("move_view", True)
        seek_play = arguments.get("seek_play", False)
        
        result = await bridge.call_lua("SetEditCurPos", [time, move_view, seek_play])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set cursor position to {time:.3f} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set cursor position: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_play_state":
        result = await bridge.call_lua("GetPlayState")
        
        if result.get("ok"):
            state = int(result.get("ret", 0))
            state_text = {
                0: "stopped",
                1: "playing",
                2: "paused",
                4: "recording",
                5: "record paused"
            }.get(state, f"unknown ({state})")
            
            return [TextContent(
                type="text",
                text=f"playback state: {state}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get play state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "play":
        result = await bridge.call_lua("Main_OnCommand", [1007, 0])  # Transport: Play
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Started playback"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to start playback: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "stop":
        result = await bridge.call_lua("Main_OnCommand", [1016, 0])  # Transport: Stop
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Stopped playback"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to stop playback: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "pause":
        result = await bridge.call_lua("Main_OnCommand", [1008, 0])  # Transport: Pause
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Paused playback"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to pause playback: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "record":
        result = await bridge.call_lua("Main_OnCommand", [1013, 0])  # Transport: Record
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Started recording"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to start recording: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_play_state":
        play = arguments["play"]
        pause = arguments["pause"]
        record = arguments["record"]
        
        result = await bridge.call_lua("SetPlayState", [play, pause, record])
        
        if result.get("ok"):
            states = []
            if play: states.append("play")
            if pause: states.append("pause")
            if record: states.append("record")
            state_str = ", ".join(states) if states else "stopped"
            
            return [TextContent(
                type="text",
                text=f"Set play state: {state_str}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set play state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_repeat_state":
        repeat = arguments["repeat"]
        
        result = await bridge.call_lua("GetSetRepeat", [1 if repeat else 0])
        
        if result.get("ok"):
            state = "enabled" if repeat else "disabled"
            return [TextContent(
                type="text",
                text=f"Repeat {state}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set repeat state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "execute_action":
        command_id = arguments["command_id"]
        flag = arguments.get("flag", 0)
        
        result = await bridge.call_lua("Main_OnCommand", [command_id, flag])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Executed action {command_id}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to execute action: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "undo_begin_block":
        result = await bridge.call_lua("Undo_BeginBlock")
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Started undo block"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to begin undo block: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "undo_end_block":
        description = arguments["description"]
        flags = arguments.get("flags", -1)
        
        result = await bridge.call_lua("Undo_EndBlock", [description, flags])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Ended undo block: {description}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to end undo block: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "update_arrange":
        result = await bridge.call_lua("UpdateArrange")
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Updated arrange view"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to update arrange: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "update_timeline":
        result = await bridge.call_lua("UpdateTimeline")
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Updated timeline"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to update timeline: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "add_project_marker":
        is_region = arguments["is_region"]
        position = arguments["position"]
        region_end = arguments.get("region_end", position)
        name = arguments["name"]
        want_index = arguments.get("want_index", -1)
        
        result = await bridge.call_lua("AddProjectMarker", [0, is_region, position, region_end, name, want_index])
        
        if result.get("ok"):
            marker_type = "region" if is_region else "marker"
            index = result.get("ret", want_index)
            return [TextContent(
                type="text",
                text=f"Added {marker_type} '{name}' at {position:.3f}s (index: {index})"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add marker/region: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "delete_project_marker":
        marker_index = arguments["marker_index"]
        is_region = arguments["is_region"]
        
        result = await bridge.call_lua("DeleteProjectMarker", [0, marker_index, is_region])
        
        if result.get("ok"):
            marker_type = "region" if is_region else "marker"
            return [TextContent(
                type="text",
                text=f"Deleted {marker_type} {marker_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete marker/region: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "count_project_markers":
        result = await bridge.call_lua("CountProjectMarkers", [0])
        
        if result.get("ok"):
            ret = result.get("ret", [0, 0])
            if isinstance(ret, list) and len(ret) >= 2:
                num_markers = ret[0]
                num_regions = ret[1]
                return [TextContent(
                    type="text",
                    text=f"Total markers/regions: {num_markers} markers, {num_regions} regions"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="Failed to count markers/regions: Invalid response"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count markers/regions: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "enum_project_markers":
        marker_index = arguments["marker_index"]
        
        result = await bridge.call_lua("EnumProjectMarkers", [marker_index])
        
        if result.get("ok"):
            ret = result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 5:
                is_region = ret[1]
                position = ret[2]
                region_end = ret[3]
                name = ret[4]
                
                if is_region:
                    return [TextContent(
                        type="text",
                        text=f"Region {marker_index}: '{name}' from {position:.3f}s to {region_end:.3f}s"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Marker {marker_index}: '{name}' at {position:.3f}s"
                    )]
            else:
                return [TextContent(
                    type="text",
                    text=f"No marker/region found at index {marker_index}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get marker/region info: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_loop_time_range":
        is_loop = arguments.get("is_loop", False)
        
        result = await bridge.call_lua("GetSet_LoopTimeRange", [False, is_loop, 0, 0, False])
        
        if result.get("ok"):
            ret = result.get("ret", [0, 0])
            if isinstance(ret, list) and len(ret) >= 2:
                start = ret[0]
                end = ret[1]
                range_type = "loop" if is_loop else "time selection"
                return [TextContent(
                    type="text",
                    text=f"Current {range_type}: {start:.3f}s to {end:.3f}s (duration: {end - start:.3f}s)"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="No time range selected"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get time range: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_loop_time_range":
        is_loop = arguments["is_loop"]
        start = arguments["start"]
        end = arguments["end"]
        allow_autoseek = arguments.get("allow_autoseek", False)
        
        result = await bridge.call_lua("GetSet_LoopTimeRange", [True, is_loop, start, end, allow_autoseek])
        
        if result.get("ok"):
            range_type = "loop" if is_loop else "time selection"
            return [TextContent(
                type="text",
                text=f"Set {range_type}: {start:.3f}s to {end:.3f}s"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set time range: {result.get('error', 'Unknown error')}"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def amain():
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting REAPER MCP Server (File-based Bridge)...")
    logger.info(f"Bridge directory: {BRIDGE_DIR}")
    logger.info("Make sure to run mcp_bridge_no_socket.lua in REAPER!")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

def main():
    import sys
    asyncio.run(amain())

if __name__ == "__main__":
    main()