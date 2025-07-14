import json
import socket
import asyncio
from mcp.server import Server
from mcp import Tool
from mcp.types import TextContent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UDP_HOST = '127.0.0.1'
UDP_PORT = 9000

class ReaperBridge:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5.0)
        # Bind once to receive responses
        self.sock.bind(('127.0.0.1', 9001))
        
    def call_lua(self, fname: str, args: list = None):
        if args is None:
            args = []
        
        message = json.dumps({'call': fname, 'args': args})
        logger.info(f"Sending to Lua: {message}")
        
        try:
            self.sock.sendto(message.encode(), (UDP_HOST, UDP_PORT))
            data, addr = self.sock.recvfrom(65536)
            response = json.loads(data.decode())
            logger.info(f"Received from Lua: {response}")
            return response
        except socket.timeout:
            logger.error("Socket timeout waiting for REAPER response")
            return {"ok": False, "error": "Timeout waiting for REAPER"}
        except Exception as e:
            logger.error(f"Error communicating with REAPER: {e}")
            return {"ok": False, "error": str(e)}

bridge = ReaperBridge()

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
        
        result = bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
        
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
        result = bridge.call_lua("CountTracks", [0])
        
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
        result = bridge.call_lua("GetAppVersion")
        
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
        result = bridge.call_lua("GetTrack", [0, index])
        
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
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        # Then set its selection state
        result = bridge.call_lua("SetTrackSelected", [track_index, selected])
        
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
        
        result = bridge.call_lua("GetTrackName", [track_index])
        
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
        
        result = bridge.call_lua("SetTrackName", [track_index, name])
        
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
        
        result = bridge.call_lua("GetMasterTrack", [0])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Master track: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get master track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "delete_track":
        track_index = arguments["track_index"]
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("DeleteTrack", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track {track_index} deleted successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_mute":
        track_index = arguments["track_index"]
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("GetTrackMute", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track {track_index} mute state: {'muted' if result.get('ret') else 'unmuted'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track mute: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_mute":
        track_index = arguments["track_index"]
        mute = arguments["mute"]
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("SetTrackMute", [track_index, mute])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track {track_index} {'muted' if mute else 'unmuted'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track mute: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_solo":
        track_index = arguments["track_index"]
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("GetTrackSolo", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track {track_index} solo state: {'soloed' if result.get('ret') else 'not soloed'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track solo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_solo":
        track_index = arguments["track_index"]
        solo = arguments["solo"]
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("SetTrackSolo", [track_index, solo])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track {track_index} {'soloed' if solo else 'unsoloed'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track solo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_volume":
        track_index = arguments["track_index"]
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("GetTrackVolume", [track_index])
        
        if result.get("ok"):
            volume_db = result.get("ret", 0.0)
            return [TextContent(
                type="text",
                text=f"Track {track_index} volume: {volume_db:.2f} dB"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track volume: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_volume":
        track_index = arguments["track_index"]
        volume_db = arguments["volume_db"]
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("SetTrackVolume", [track_index, volume_db])
        
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
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("GetTrackPan", [track_index])
        
        if result.get("ok"):
            pan = result.get("ret", 0.0)
            return [TextContent(
                type="text",
                text=f"Track {track_index} pan: {pan:.2f} (L={-pan:.0%} R={pan:.0%})"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track pan: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_pan":
        track_index = arguments["track_index"]
        pan = arguments["pan"]
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("SetTrackPan", [track_index, pan])
        
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
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("AddMediaItemToTrack", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Added media item to track {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add media item: {result.get('error', 'Unknown error')}"
            )]
    elif name == "count_media_items":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("CountMediaItems", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count total media items in project: {result.get('ret', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count_media_items: {result.get('error', 'Unknown error')}"
            )]
    elif name == "get_media_item":
        project_index = arguments.get("project_index", 0)
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("GetMediaItem", [project_index, item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item by index: {result.get('ret', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get_media_item: {result.get('error', 'Unknown error')}"
            )]
    elif name == "delete_track_media_item":
        track_index = arguments["track_index"]
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("DeleteTrackMediaItem", [track_index, item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed delete_track_media_item"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete_track_media_item: {result.get('error', 'Unknown error')}"
            )]
    elif name == "get_media_item_length":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("GetMediaItemLength", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item length: {result.get('ret', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get_media_item_length: {result.get('error', 'Unknown error')}"
            )]
    elif name == "set_media_item_length":
        item_index = arguments["item_index"]
        length = arguments["length"]
        
        result = bridge.call_lua("SetMediaItemLength", [item_index, length])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed set_media_item_length"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set_media_item_length: {result.get('error', 'Unknown error')}"
            )]
    elif name == "get_media_item_position":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("GetMediaItemPosition", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item position: {result.get('ret', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get_media_item_position: {result.get('error', 'Unknown error')}"
            )]
    elif name == "set_media_item_position":
        item_index = arguments["item_index"]
        position = arguments["position"]
        
        result = bridge.call_lua("SetMediaItemPosition", [item_index, position])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed set_media_item_position"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set_media_item_position: {result.get('error', 'Unknown error')}"
            )]
    elif name == "get_project_name":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("GetProjectName", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get the current project name: {result.get('ret', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get_project_name: {result.get('error', 'Unknown error')}"
            )]
    elif name == "get_project_path":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("GetProjectPath", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get the current project path: {result.get('ret', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get_project_path: {result.get('error', 'Unknown error')}"
            )]
    elif name == "save_project":
        project_index = arguments.get("project_index", 0)
        force_save_as = arguments.get("force_save_as", False)
        
        result = bridge.call_lua("Main_SaveProject", [project_index, force_save_as])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed save_project"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to save_project: {result.get('error', 'Unknown error')}"
            )]
    elif name == "get_cursor_position":
        
        result = bridge.call_lua("GetCursorPosition", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get the edit cursor position in seconds: {result.get('ret', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get_cursor_position: {result.get('error', 'Unknown error')}"
            )]
    elif name == "set_edit_cursor_position":
        time = arguments["time"]
        move_view = arguments.get("move_view", True)
        seek_play = arguments.get("seek_play", False)
        
        result = bridge.call_lua("SetEditCurPos", [time, move_view, seek_play])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed set_edit_cursor_position"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set_edit_cursor_position: {result.get('error', 'Unknown error')}"
            )]
    elif name == "get_play_state":
        
        result = bridge.call_lua("GetPlayState", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get current playback state: {result.get('ret', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get_play_state: {result.get('error', 'Unknown error')}"
            )]
    elif name == "play":
        
        result = bridge.call_lua("CSurf_OnPlay", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed play"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to play: {result.get('error', 'Unknown error')}"
            )]
    elif name == "stop":
        
        result = bridge.call_lua("CSurf_OnStop", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed stop"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to stop: {result.get('error', 'Unknown error')}"
            )]
    elif name == "pause":
        
        result = bridge.call_lua("CSurf_OnPause", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed pause"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to pause: {result.get('error', 'Unknown error')}"
            )]
    elif name == "record":
        
        result = bridge.call_lua("Main_OnCommand", [1013, 0])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully started recording"
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
        
        result = bridge.call_lua("CSurf_SetPlayState", [play, pause, record])
        
        if result.get("ok"):
            states = []
            if play: states.append("play")
            if pause: states.append("pause") 
            if record: states.append("record")
            state_str = ", ".join(states) if states else "stopped"
            return [TextContent(
                type="text",
                text=f"Transport state set to: {state_str}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set play state: {result.get('error', 'Unknown error')}"
            )]
    elif name == "set_repeat_state":
        repeat = arguments["repeat"]
        
        result = bridge.call_lua("CSurf_SetRepeatState", [repeat])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Repeat/loop {'enabled' if repeat else 'disabled'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set repeat state: {result.get('error', 'Unknown error')}"
            )]
    elif name == "execute_action":
        command_id = arguments["command_id"]
        flag = arguments.get("flag", 0)
        
        result = bridge.call_lua("Main_OnCommand", [command_id, flag])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed execute_action"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to execute_action: {result.get('error', 'Unknown error')}"
            )]
    elif name == "undo_begin_block":
        
        result = bridge.call_lua("Undo_BeginBlock", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed undo_begin_block"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo_begin_block: {result.get('error', 'Unknown error')}"
            )]
    elif name == "undo_end_block":
        description = arguments["description"]
        flags = arguments.get("flags", -1)
        
        result = bridge.call_lua("Undo_EndBlock", [description, flags])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed undo_end_block"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo_end_block: {result.get('error', 'Unknown error')}"
            )]
    elif name == "update_arrange":
        
        result = bridge.call_lua("UpdateArrange", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed update_arrange"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to update_arrange: {result.get('error', 'Unknown error')}"
            )]
    elif name == "update_timeline":
        
        result = bridge.call_lua("UpdateTimeline", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed update_timeline"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to update_timeline: {result.get('error', 'Unknown error')}"
            )]
    elif name == "add_project_marker":
        is_region = arguments["is_region"]
        position = arguments["position"]
        region_end = arguments.get("region_end", position)
        name = arguments["name"]
        want_index = arguments.get("want_index", -1)
        
        result = bridge.call_lua("AddProjectMarker", [is_region, position, region_end, name, want_index])
        
        if result.get("ok"):
            marker_type = "region" if is_region else "marker"
            index = result.get("ret", -1)
            if index >= 0:
                return [TextContent(
                    type="text",
                    text=f"Successfully added {marker_type} '{name}' at index {index}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Failed to add {marker_type}: unable to create at desired index"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add marker/region: {result.get('error', 'Unknown error')}"
            )]
    elif name == "delete_project_marker":
        marker_index = arguments["marker_index"]
        is_region = arguments["is_region"]
        
        result = bridge.call_lua("DeleteProjectMarker", [marker_index, is_region])
        
        if result.get("ok"):
            marker_type = "region" if is_region else "marker"
            return [TextContent(
                type="text",
                text=f"Successfully deleted {marker_type} at index {marker_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete marker/region: {result.get('error', 'Unknown error')}"
            )]
    elif name == "count_project_markers":
        
        result = bridge.call_lua("CountProjectMarkers", [])
        
        if result.get("ok"):
            count = result.get("ret", 0)
            marker_count = result.get("marker_count", 0)
            region_count = result.get("region_count", 0)
            return [TextContent(
                type="text",
                text=f"Total markers/regions: {count} ({marker_count} markers, {region_count} regions)"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count markers: {result.get('error', 'Unknown error')}"
            )]
    elif name == "enum_project_markers":
        marker_index = arguments["marker_index"]
        
        result = bridge.call_lua("EnumProjectMarkers", [marker_index])
        
        if result.get("ok"):
            if result.get("found"):
                marker_type = "Region" if result.get("is_region") else "Marker"
                name = result.get("name", "")
                position = result.get("position", 0)
                region_end = result.get("region_end", 0)
                number = result.get("number", 0)
                
                text = f"{marker_type} {number}: '{name}' at {position:.3f}s"
                if result.get("is_region"):
                    text += f" to {region_end:.3f}s"
                
                return [TextContent(
                    type="text",
                    text=text
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"No marker/region found at index {marker_index}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get marker info: {result.get('error', 'Unknown error')}"
            )]
    elif name == "get_loop_time_range":
        is_loop = arguments.get("is_loop", False)
        
        result = bridge.call_lua("GetSet_LoopTimeRange", [False, is_loop])
        
        if result.get("ok"):
            start = result.get("start", 0)
            end = result.get("end", 0)
            range_type = "loop" if is_loop else "time selection"
            
            if start == end:
                return [TextContent(
                    type="text",
                    text=f"No {range_type} is set"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Current {range_type}: {start:.3f}s to {end:.3f}s (duration: {end-start:.3f}s)"
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
        
        result = bridge.call_lua("GetSet_LoopTimeRange", [True, is_loop, start, end, allow_autoseek])
        
        if result.get("ok"):
            range_type = "loop" if is_loop else "time selection"
            return [TextContent(
                type="text",
                text=f"Successfully set {range_type} from {start:.3f}s to {end:.3f}s"
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
    
    logger.info("Starting REAPER MCP Server...")
    logger.info(f"Will communicate with REAPER on {UDP_HOST}:{UDP_PORT}")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

def main():
    import sys
    asyncio.run(amain())

if __name__ == "__main__":
    main()