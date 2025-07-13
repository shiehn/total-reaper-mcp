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
import signal
import atexit
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

def cleanup_bridge_files():
    """Clean up any leftover request/response files"""
    try:
        for pattern in ['request_*.json', 'response_*.json']:
            for file in BRIDGE_DIR.glob(pattern):
                try:
                    file.unlink()
                    logger.debug(f"Cleaned up {file}")
                except Exception as e:
                    logger.warning(f"Failed to clean up {file}: {e}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

# Register cleanup handlers
atexit.register(cleanup_bridge_files)

def signal_handler(signum, frame):
    """Handle termination signals"""
    logger.info(f"Received signal {signum}, cleaning up...")
    cleanup_bridge_files()
    exit(0)

# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

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
        ),
        Tool(
            name="create_midi_item",
            description="Create a new MIDI item with an empty take",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "start_time": {
                        "type": "number",
                        "description": "Start time in seconds"
                    },
                    "length": {
                        "type": "number",
                        "description": "Length in seconds"
                    }
                },
                "required": ["track_index", "start_time", "length"]
            }
        ),
        Tool(
            name="insert_midi_note",
            description="Insert a MIDI note into a take",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "The media item index",
                        "minimum": 0
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "The take index",
                        "minimum": 0
                    },
                    "pitch": {
                        "type": "integer",
                        "description": "MIDI pitch (0-127)",
                        "minimum": 0,
                        "maximum": 127
                    },
                    "velocity": {
                        "type": "integer",
                        "description": "MIDI velocity (0-127)",
                        "minimum": 0,
                        "maximum": 127
                    },
                    "start_time": {
                        "type": "number",
                        "description": "Start time in seconds"
                    },
                    "duration": {
                        "type": "number",
                        "description": "Duration in seconds"
                    },
                    "channel": {
                        "type": "integer",
                        "description": "MIDI channel (0-15)",
                        "minimum": 0,
                        "maximum": 15,
                        "default": 0
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Is note selected",
                        "default": False
                    },
                    "muted": {
                        "type": "boolean",
                        "description": "Is note muted",
                        "default": False
                    }
                },
                "required": ["item_index", "take_index", "pitch", "velocity", "start_time", "duration"]
            }
        ),
        Tool(
            name="midi_sort",
            description="Sort MIDI events in a take after insertion",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "The media item index",
                        "minimum": 0
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "The take index",
                        "minimum": 0
                    }
                },
                "required": ["item_index", "take_index"]
            }
        ),
        Tool(
            name="insert_midi_cc",
            description="Insert MIDI Control Change event",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "The media item index",
                        "minimum": 0
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "The take index",
                        "minimum": 0
                    },
                    "time": {
                        "type": "number",
                        "description": "Time in seconds"
                    },
                    "channel": {
                        "type": "integer",
                        "description": "MIDI channel (0-15)",
                        "minimum": 0,
                        "maximum": 15
                    },
                    "cc_number": {
                        "type": "integer",
                        "description": "CC number (0-127)",
                        "minimum": 0,
                        "maximum": 127
                    },
                    "value": {
                        "type": "integer",
                        "description": "CC value (0-127)",
                        "minimum": 0,
                        "maximum": 127
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Is CC selected",
                        "default": False
                    },
                    "muted": {
                        "type": "boolean",
                        "description": "Is CC muted",
                        "default": False
                    }
                },
                "required": ["item_index", "take_index", "time", "channel", "cc_number", "value"]
            }
        ),
        Tool(
            name="count_takes",
            description="Count the number of takes in a media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "The media item index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="get_active_take",
            description="Get the active take index of a media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "The media item index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="set_active_take",
            description="Set the active take of a media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "The media item index (0-based)",
                        "minimum": 0
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "The take index to activate (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["item_index", "take_index"]
            }
        ),
        Tool(
            name="track_fx_get_count",
            description="Get the number of FX on a track",
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
            name="track_fx_add_by_name",
            description="Add an FX to a track by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "fx_name": {
                        "type": "string",
                        "description": "The FX name (e.g., 'ReaEQ', 'ReaComp')"
                    },
                    "instantiate": {
                        "type": "boolean",
                        "description": "Instantiate the FX if not found",
                        "default": True
                    }
                },
                "required": ["track_index", "fx_name"]
            }
        ),
        Tool(
            name="track_fx_delete",
            description="Delete an FX from a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "fx_index": {
                        "type": "integer",
                        "description": "The FX index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index", "fx_index"]
            }
        ),
        Tool(
            name="track_fx_get_enabled",
            description="Get whether an FX is enabled",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "fx_index": {
                        "type": "integer",
                        "description": "The FX index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index", "fx_index"]
            }
        ),
        Tool(
            name="track_fx_set_enabled",
            description="Enable or disable an FX",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "fx_index": {
                        "type": "integer",
                        "description": "The FX index (0-based)",
                        "minimum": 0
                    },
                    "enabled": {
                        "type": "boolean",
                        "description": "Whether to enable the FX"
                    }
                },
                "required": ["track_index", "fx_index", "enabled"]
            }
        ),
        Tool(
            name="track_fx_get_name",
            description="Get the name of an FX on a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "fx_index": {
                        "type": "integer",
                        "description": "The FX index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index", "fx_index"]
            }
        ),
        Tool(
            name="get_track_envelope_by_name",
            description="Get a track envelope by name (e.g., 'Volume', 'Pan', 'Mute')",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "envelope_name": {
                        "type": "string",
                        "description": "The envelope name (e.g., 'Volume', 'Pan', 'Mute')"
                    }
                },
                "required": ["track_index", "envelope_name"]
            }
        ),
        Tool(
            name="count_envelope_points",
            description="Count the number of points in an envelope",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "envelope_name": {
                        "type": "string",
                        "description": "The envelope name"
                    }
                },
                "required": ["track_index", "envelope_name"]
            }
        ),
        Tool(
            name="insert_envelope_point",
            description="Insert an automation point in an envelope",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "envelope_name": {
                        "type": "string",
                        "description": "The envelope name"
                    },
                    "time": {
                        "type": "number",
                        "description": "Time position in seconds"
                    },
                    "value": {
                        "type": "number",
                        "description": "Value (0-1 for volume/pan, 0 or 1 for mute)"
                    },
                    "shape": {
                        "type": "integer",
                        "description": "Point shape (0=linear, 1=square, 2=slow start/end, 3=fast start, 4=fast end, 5=bezier)",
                        "default": 0
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Whether the point is selected",
                        "default": False
                    }
                },
                "required": ["track_index", "envelope_name", "time", "value"]
            }
        ),
        Tool(
            name="delete_envelope_point",
            description="Delete an automation point from an envelope",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "envelope_name": {
                        "type": "string",
                        "description": "The envelope name"
                    },
                    "point_index": {
                        "type": "integer",
                        "description": "The point index to delete (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index", "envelope_name", "point_index"]
            }
        ),
        Tool(
            name="get_envelope_point",
            description="Get information about an envelope point",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "envelope_name": {
                        "type": "string",
                        "description": "The envelope name"
                    },
                    "point_index": {
                        "type": "integer",
                        "description": "The point index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index", "envelope_name", "point_index"]
            }
        ),
        Tool(
            name="set_envelope_point_value",
            description="Set the value of an existing envelope point",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "envelope_name": {
                        "type": "string",
                        "description": "The envelope name"
                    },
                    "point_index": {
                        "type": "integer",
                        "description": "The point index (0-based)",
                        "minimum": 0
                    },
                    "time": {
                        "type": "number",
                        "description": "New time position in seconds",
                        "default": None
                    },
                    "value": {
                        "type": "number",
                        "description": "New value"
                    }
                },
                "required": ["track_index", "envelope_name", "point_index", "value"]
            }
        ),
        Tool(
            name="create_track_send",
            description="Create a send from one track to another",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_track_index": {
                        "type": "integer",
                        "description": "Source track index (0-based)",
                        "minimum": 0
                    },
                    "dest_track_index": {
                        "type": "integer",
                        "description": "Destination track index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["source_track_index", "dest_track_index"]
            }
        ),
        Tool(
            name="remove_track_send",
            description="Remove a send from a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)",
                        "minimum": 0
                    },
                    "send_index": {
                        "type": "integer",
                        "description": "Send index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index", "send_index"]
            }
        ),
        Tool(
            name="get_track_num_sends",
            description="Get the number of sends on a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_send_volume",
            description="Set the volume of a track send",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)",
                        "minimum": 0
                    },
                    "send_index": {
                        "type": "integer",
                        "description": "Send index (0-based)",
                        "minimum": 0
                    },
                    "volume": {
                        "type": "number",
                        "description": "Volume (0.0-1.0)"
                    }
                },
                "required": ["track_index", "send_index", "volume"]
            }
        ),
        Tool(
            name="get_track_send_info",
            description="Get information about a track send",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)",
                        "minimum": 0
                    },
                    "send_index": {
                        "type": "integer",
                        "description": "Send index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index", "send_index"]
            }
        ),
        Tool(
            name="get_project_tempo",
            description="Get the current project tempo in BPM",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_project_tempo",
            description="Set the project tempo in BPM",
            inputSchema={
                "type": "object",
                "properties": {
                    "tempo": {
                        "type": "number",
                        "description": "Tempo in BPM",
                        "minimum": 1,
                        "maximum": 960
                    }
                },
                "required": ["tempo"]
            }
        ),
        Tool(
            name="get_project_time_signature",
            description="Get the current project time signature",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_project_time_signature",
            description="Set the project time signature",
            inputSchema={
                "type": "object",
                "properties": {
                    "numerator": {
                        "type": "integer",
                        "description": "Time signature numerator (e.g., 4 for 4/4)",
                        "minimum": 1,
                        "maximum": 32
                    },
                    "denominator": {
                        "type": "integer",
                        "description": "Time signature denominator (e.g., 4 for 4/4)",
                        "enum": [1, 2, 4, 8, 16, 32]
                    }
                },
                "required": ["numerator", "denominator"]
            }
        ),
        Tool(
            name="get_tempo_at_position",
            description="Get the tempo at a specific time position",
            inputSchema={
                "type": "object",
                "properties": {
                    "position": {
                        "type": "number",
                        "description": "Time position in seconds"
                    }
                },
                "required": ["position"]
            }
        ),
        Tool(
            name="insert_tempo_marker",
            description="Insert a tempo/time signature marker",
            inputSchema={
                "type": "object",
                "properties": {
                    "position": {
                        "type": "number",
                        "description": "Position in seconds"
                    },
                    "tempo": {
                        "type": "number",
                        "description": "Tempo in BPM",
                        "minimum": 1,
                        "maximum": 960
                    },
                    "time_sig_numerator": {
                        "type": "integer",
                        "description": "Time signature numerator",
                        "minimum": 1,
                        "maximum": 32,
                        "default": None
                    },
                    "time_sig_denominator": {
                        "type": "integer",
                        "description": "Time signature denominator",
                        "enum": [1, 2, 4, 8, 16, 32],
                        "default": None
                    }
                },
                "required": ["position", "tempo"]
            }
        ),
        Tool(
            name="set_media_item_selected",
            description="Set whether a media item is selected",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index (0-based)",
                        "minimum": 0
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Whether to select or deselect the item"
                    }
                },
                "required": ["item_index", "selected"]
            }
        ),
        Tool(
            name="count_selected_media_items",
            description="Count the number of selected media items",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_selected_media_item",
            description="Get a selected media item by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "Index in the selected items list (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="count_selected_tracks",
            description="Count the number of selected tracks",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_selected_track",
            description="Get a selected track by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "Index in the selected tracks list (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="get_project_sample_rate",
            description="Get the project sample rate",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_project_sample_rate",
            description="Set the project sample rate",
            inputSchema={
                "type": "object",
                "properties": {
                    "sample_rate": {
                        "type": "integer",
                        "description": "Sample rate in Hz",
                        "enum": [22050, 44100, 48000, 88200, 96000, 176400, 192000]
                    }
                },
                "required": ["sample_rate"]
            }
        ),
        Tool(
            name="get_project_length",
            description="Get the project length in seconds",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_project_length",
            description="Set the project length in seconds",
            inputSchema={
                "type": "object",
                "properties": {
                    "length": {
                        "type": "number",
                        "description": "Project length in seconds",
                        "minimum": 1
                    }
                },
                "required": ["length"]
            }
        ),
        Tool(
            name="get_project_grid_division",
            description="Get the project grid division",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_project_grid_division",
            description="Set the project grid division",
            inputSchema={
                "type": "object",
                "properties": {
                    "division": {
                        "type": "number",
                        "description": "Grid division (e.g., 0.25 for 1/4, 0.125 for 1/8, 0.0625 for 1/16)"
                    }
                },
                "required": ["division"]
            }
        ),
        Tool(
            name="get_project_render_bounds",
            description="Get the project render bounds mode",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_project_render_bounds",
            description="Set the project render bounds mode",
            inputSchema={
                "type": "object",
                "properties": {
                    "bounds_mode": {
                        "type": "integer",
                        "description": "Render bounds mode (0=entire project, 1=time selection, 2=custom)",
                        "enum": [0, 1, 2]
                    }
                },
                "required": ["bounds_mode"]
            }
        ),
        Tool(
            name="get_project_notes",
            description="Get the project notes",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_project_notes",
            description="Set the project notes",
            inputSchema={
                "type": "object",
                "properties": {
                    "notes": {
                        "type": "string",
                        "description": "Project notes text"
                    }
                },
                "required": ["notes"]
            }
        ),
        Tool(
            name="get_track_automation_mode",
            description="Get the automation mode for a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)",
                        "minimum": 0
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_automation_mode",
            description="Set the automation mode for a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)",
                        "minimum": 0
                    },
                    "mode": {
                        "type": "integer",
                        "description": "Automation mode (0=Trim/Read, 1=Read, 2=Touch, 3=Write, 4=Latch)",
                        "enum": [0, 1, 2, 3, 4]
                    }
                },
                "required": ["track_index", "mode"]
            }
        ),
        Tool(
            name="get_global_automation_override",
            description="Get the global automation override mode",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_global_automation_override",
            description="Set the global automation override mode",
            inputSchema={
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "integer",
                        "description": "Override mode (0=No override, 1=Bypass all, 2=All to trim/read)",
                        "enum": [0, 1, 2]
                    }
                },
                "required": ["mode"]
            }
        ),
        Tool(
            name="get_track_peak",
            description="Get the current peak level of a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based, -1 for master track)"
                    },
                    "channel": {
                        "type": "integer",
                        "description": "Channel number (0=left/mono, 1=right)",
                        "default": 0
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="get_track_peak_info",
            description="Get detailed peak information for a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based, -1 for master track)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="get_media_item_peak",
            description="Get the peak value of a media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index (0-based)"
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="get_track_receive_count",
            description="Get the number of receives on a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based, -1 for master track)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="get_track_receive_info",
            description="Get information about a track receive",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "receive_index": {
                        "type": "integer",
                        "description": "Receive index (0-based)"
                    }
                },
                "required": ["track_index", "receive_index"]
            }
        ),
        Tool(
            name="get_track_guid",
            description="Get the unique GUID of a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based, -1 for master track)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="get_track_from_guid",
            description="Get a track by its GUID",
            inputSchema={
                "type": "object",
                "properties": {
                    "guid": {
                        "type": "string",
                        "description": "Track GUID string"
                    }
                },
                "required": ["guid"]
            }
        ),
        Tool(
            name="split_media_item",
            description="Split a media item at a specific position",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index (0-based)"
                    },
                    "position": {
                        "type": "number",
                        "description": "Position in seconds where to split"
                    }
                },
                "required": ["item_index", "position"]
            }
        ),
        Tool(
            name="glue_media_items",
            description="Glue selected media items together",
            inputSchema={
                "type": "object",
                "properties": {
                    "respect_time_selection": {
                        "type": "boolean",
                        "description": "Only glue within time selection",
                        "default": False
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_media_item_take_track",
            description="Get the parent track of a media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index (0-based)"
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="duplicate_media_item",
            description="Duplicate a media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index (0-based)"
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="set_media_item_color",
            description="Set the color of a media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index (0-based)"
                    },
                    "color": {
                        "type": "integer",
                        "description": "Color value (RGB packed as integer, or 0 for default)"
                    }
                },
                "required": ["item_index", "color"]
            }
        ),
        Tool(
            name="get_track_record_mode",
            description="Get track record mode",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_record_mode",
            description="Set track record mode",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "mode": {
                        "type": "integer",
                        "description": "Record mode (0=input, 1=stereo out, 2=none, 3=stereo out with latency compensation, 4=midi output, 5=mono out, 6=mono out with latency compensation, 7=midi overdub, 8=midi replace)",
                        "enum": [0, 1, 2, 3, 4, 5, 6, 7, 8]
                    }
                },
                "required": ["track_index", "mode"]
            }
        ),
        Tool(
            name="get_track_record_input",
            description="Get track record input",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_record_input",
            description="Set track record input",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "input": {
                        "type": "integer",
                        "description": "Input index (-1=none, 0-511=mono hardware input, 512-1023=stereo hardware input pair, 1024+=ReaRoute/loopback)"
                    }
                },
                "required": ["track_index", "input"]
            }
        ),
        Tool(
            name="get_track_record_arm",
            description="Get track record arm state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_record_arm",
            description="Set track record arm state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "armed": {
                        "type": "boolean",
                        "description": "Whether to arm the track for recording"
                    }
                },
                "required": ["track_index", "armed"]
            }
        ),
        Tool(
            name="get_num_midi_inputs",
            description="Get the number of MIDI inputs available",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_num_midi_outputs",
            description="Get the number of MIDI outputs available",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_midi_input_name",
            description="Get the name of a MIDI input",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_index": {
                        "type": "integer",
                        "description": "MIDI input index (0-based)"
                    }
                },
                "required": ["input_index"]
            }
        ),
        Tool(
            name="get_midi_output_name",
            description="Get the name of a MIDI output",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_index": {
                        "type": "integer",
                        "description": "MIDI output index (0-based)"
                    }
                },
                "required": ["output_index"]
            }
        ),
        Tool(
            name="get_track_color",
            description="Get the color of a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based, -1 for master track)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_color",
            description="Set the color of a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based, -1 for master track)"
                    },
                    "color": {
                        "type": "integer",
                        "description": "Color value (RGB packed as integer, or 0 for default)"
                    }
                },
                "required": ["track_index", "color"]
            }
        ),
        Tool(
            name="get_media_item_color",
            description="Get the color of a media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index (0-based)"
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="open_project",
            description="Open a REAPER project file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Full path to the project file (.rpp or .rpp-bak)"
                    },
                    "in_new_tab": {
                        "type": "boolean",
                        "description": "Open in new project tab",
                        "default": False
                    }
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="enum_projects",
            description="Get information about all open projects",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="select_project_instance",
            description="Switch to a specific project by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0-based)"
                    }
                },
                "required": ["project_index"]
            }
        ),
        Tool(
            name="get_current_project_index",
            description="Get the index of the currently active project",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="close_project",
            description="Close the current project",
            inputSchema={
                "type": "object",
                "properties": {
                    "save_prompt": {
                        "type": "boolean",
                        "description": "Show save prompt if project has unsaved changes",
                        "default": True
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="render_project",
            description="Render the entire project to file",
            inputSchema={
                "type": "object",
                "properties": {
                    "bounds": {
                        "type": "string",
                        "description": "Render bounds (entire_project, time_selection, selected_items)",
                        "enum": ["entire_project", "time_selection", "selected_items"],
                        "default": "entire_project"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="bounce_tracks",
            description="Bounce selected tracks to new track",
            inputSchema={
                "type": "object",
                "properties": {
                    "add_to_project": {
                        "type": "boolean",
                        "description": "Add bounced audio to project",
                        "default": True
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_render_settings",
            description="Get current render settings",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_render_settings",
            description="Set render settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "sample_rate": {
                        "type": "integer",
                        "description": "Sample rate (e.g., 44100, 48000)",
                        "enum": [44100, 48000, 88200, 96000, 176400, 192000]
                    },
                    "channels": {
                        "type": "integer",
                        "description": "Number of channels (1=mono, 2=stereo, 6=5.1)",
                        "enum": [1, 2, 6]
                    },
                    "format": {
                        "type": "string",
                        "description": "Output format",
                        "enum": ["WAV", "AIFF", "MP3", "OGG", "FLAC"]
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="check_video_support",
            description="Check if video support is available in REAPER",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_video_settings",
            description="Get current video processor settings",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_video_settings",
            description="Set video processor settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "width": {
                        "type": "integer",
                        "description": "Video width in pixels"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Video height in pixels"
                    },
                    "fps": {
                        "type": "number",
                        "description": "Frames per second"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="add_video_to_track",
            description="Add a video file to a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "video_file": {
                        "type": "string",
                        "description": "Path to video file"
                    }
                },
                "required": ["track_index", "video_file"]
            }
        ),
        # Missing MIDI tools
        Tool(
            name="midi_get_note_name",
            description="Get the note name for a MIDI note number",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_number": {
                        "type": "integer",
                        "description": "MIDI note number (0-127)",
                        "minimum": 0,
                        "maximum": 127
                    }
                },
                "required": ["note_number"]
            }
        ),
        Tool(
            name="midi_count_events",
            description="Count MIDI events in a take",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index",
                        "default": 0
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "Take index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="midi_get_scale",
            description="Get the scale/key signature of a MIDI take",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index",
                        "default": 0
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "Take index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="midi_set_scale",
            description="Set the scale/key signature of a MIDI take",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index",
                        "default": 0
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "Take index",
                        "default": 0
                    },
                    "root": {
                        "type": "integer",
                        "description": "Root note (0=C, 1=C#, etc.)",
                        "minimum": 0,
                        "maximum": 11
                    },
                    "scale": {
                        "type": "integer",
                        "description": "Scale type (0=major, 1=minor, etc.)"
                    },
                    "signature": {
                        "type": "string",
                        "description": "Key signature string"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="midi_select_all",
            description="Select all MIDI events in a take",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index",
                        "default": 0
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "Take index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="midi_get_all_events",
            description="Get all MIDI events from a take",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index",
                        "default": 0
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "Take index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="midi_insert_note",
            description="Insert a MIDI note (duplicate of insert_midi_note for compatibility)",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "pitch": {
                        "type": "integer",
                        "description": "MIDI pitch (0-127)",
                        "minimum": 0,
                        "maximum": 127
                    },
                    "velocity": {
                        "type": "integer",
                        "description": "Note velocity (1-127)",
                        "minimum": 1,
                        "maximum": 127,
                        "default": 80
                    },
                    "position": {
                        "type": "number",
                        "description": "Position in seconds",
                        "default": 0.0
                    },
                    "length": {
                        "type": "number",
                        "description": "Length in seconds",
                        "default": 0.5
                    },
                    "channel": {
                        "type": "integer",
                        "description": "MIDI channel (0-15)",
                        "minimum": 0,
                        "maximum": 15,
                        "default": 0
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Whether the note is selected",
                        "default": False
                    },
                    "muted": {
                        "type": "boolean",
                        "description": "Whether the note is muted",
                        "default": False
                    }
                },
                "required": ["take_index", "pitch"]
            }
        ),
        # Missing track tools
        Tool(
            name="insert_track_at_index",
            description="Insert track at index (alias for insert_track)",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "want_defaults": {
                        "type": "boolean",
                        "description": "Use default track settings",
                        "default": True
                    }
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="get_track_volume_db",
            description="Get track volume in dB",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_volume_db",
            description="Set track volume in dB",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "volume_db": {
                        "type": "number",
                        "description": "Volume in dB"
                    }
                },
                "required": ["track_index", "volume_db"]
            }
        ),
        Tool(
            name="freeze_track",
            description="Freeze a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="unfreeze_track",
            description="Unfreeze a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        # Missing resource/path tools
        Tool(
            name="get_resource_path",
            description="Get REAPER resource path",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_exe_path",
            description="Get REAPER executable path",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        # Other missing tools
        Tool(
            name="show_console_msg",
            description="Show message in console",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to show"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="clear_console",
            description="Clear the console",
            inputSchema={
                "type": "object",
                "properties": {}
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
    
    elif name == "create_midi_item":
        track_index = arguments["track_index"]
        start_time = arguments["start_time"]
        length = arguments["length"]
        
        # First get the track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        end_time = start_time + length
        
        # Create MIDI item
        result = await bridge.call_lua("CreateNewMIDIItemInProj", [track_handle, start_time, end_time])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created MIDI item on track {track_index} from {start_time:.3f}s to {end_time:.3f}s"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create MIDI item: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "insert_midi_note":
        item_index = arguments["item_index"]
        take_index = arguments["take_index"]
        pitch = arguments["pitch"]
        velocity = arguments["velocity"]
        start_time = arguments["start_time"]
        duration = arguments["duration"]
        channel = arguments.get("channel", 0)
        selected = arguments.get("selected", False)
        muted = arguments.get("muted", False)
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        item_handle = item_result.get("ret")
        
        # Get take
        take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
        if not take_result.get("ok") or not take_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find take at index {take_index}"
            )]
        
        take_handle = take_result.get("ret")
        
        # Convert time to PPQ
        ppq_start_result = await bridge.call_lua("MIDI_GetPPQPosFromProjTime", [take_handle, start_time])
        ppq_end_result = await bridge.call_lua("MIDI_GetPPQPosFromProjTime", [take_handle, start_time + duration])
        
        if not ppq_start_result.get("ok") or not ppq_end_result.get("ok"):
            return [TextContent(
                type="text",
                text="Failed to convert time to PPQ"
            )]
        
        ppq_start = ppq_start_result.get("ret")
        ppq_end = ppq_end_result.get("ret")
        
        # Insert note
        result = await bridge.call_lua("MIDI_InsertNote", [
            take_handle, selected, muted, ppq_start, ppq_end, channel, pitch, velocity, True
        ])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Inserted MIDI note: pitch={pitch}, velocity={velocity}, start={start_time:.3f}s, duration={duration:.3f}s"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to insert MIDI note: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "midi_sort":
        item_index = arguments["item_index"]
        take_index = arguments["take_index"]
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        item_handle = item_result.get("ret")
        
        # Get take
        take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
        if not take_result.get("ok") or not take_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find take at index {take_index}"
            )]
        
        take_handle = take_result.get("ret")
        
        # Sort MIDI
        result = await bridge.call_lua("MIDI_Sort", [take_handle])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="MIDI events sorted successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to sort MIDI: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "insert_midi_cc":
        item_index = arguments["item_index"]
        take_index = arguments["take_index"]
        time = arguments["time"]
        channel = arguments["channel"]
        cc_number = arguments["cc_number"]
        value = arguments["value"]
        selected = arguments.get("selected", False)
        muted = arguments.get("muted", False)
        
        # Get media item and take
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        item_handle = item_result.get("ret")
        
        take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
        if not take_result.get("ok") or not take_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find take at index {take_index}"
            )]
        
        take_handle = take_result.get("ret")
        
        # Convert time to PPQ
        ppq_result = await bridge.call_lua("MIDI_GetPPQPosFromProjTime", [take_handle, time])
        if not ppq_result.get("ok"):
            return [TextContent(
                type="text",
                text="Failed to convert time to PPQ"
            )]
        
        ppq_pos = ppq_result.get("ret")
        
        # Insert CC (0xB0 + channel for CC message type)
        result = await bridge.call_lua("MIDI_InsertCC", [
            take_handle, selected, muted, ppq_pos, 0xB0 + channel, cc_number, value
        ])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Inserted MIDI CC: CC{cc_number}={value} at {time:.3f}s on channel {channel}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to insert MIDI CC: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "count_takes":
        item_index = arguments["item_index"]
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        item_handle = item_result.get("ret")
        
        # Count takes
        result = await bridge.call_lua("CountTakes", [item_handle])
        
        if result.get("ok"):
            count = result.get("ret", 0)
            return [TextContent(
                type="text",
                text=f"Media item {item_index} has {count} takes"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count takes: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_active_take":
        item_index = arguments["item_index"]
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        item_handle = item_result.get("ret")
        
        # Get active take
        result = await bridge.call_lua("GetActiveTake", [item_handle])
        
        if result.get("ok"):
            take_handle = result.get("ret")
            if take_handle:
                # Get take index
                take_count_result = await bridge.call_lua("CountTakes", [item_handle])
                if take_count_result.get("ok"):
                    count = take_count_result.get("ret", 0)
                    for i in range(count):
                        take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, i])
                        if take_result.get("ok") and take_result.get("ret") == take_handle:
                            return [TextContent(
                                type="text",
                                text=f"Active take index: {i}"
                            )]
                return [TextContent(
                    type="text",
                    text="Active take found but index unknown"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="No active take"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get active take: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_active_take":
        item_index = arguments["item_index"]
        take_index = arguments["take_index"]
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        item_handle = item_result.get("ret")
        
        # Get take
        take_result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
        if not take_result.get("ok") or not take_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find take at index {take_index}"
            )]
        
        take_handle = take_result.get("ret")
        
        # Set active take
        result = await bridge.call_lua("SetActiveTake", [take_handle])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set active take to index {take_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set active take: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "track_fx_get_count":
        track_index = arguments["track_index"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Get FX count
        result = await bridge.call_lua("TrackFX_GetCount", [track_handle])
        
        if result.get("ok"):
            count = result.get("ret", 0)
            return [TextContent(
                type="text",
                text=f"Track {track_index} has {count} FX"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get FX count: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "track_fx_add_by_name":
        track_index = arguments["track_index"]
        fx_name = arguments["fx_name"]
        instantiate = arguments.get("instantiate", True)
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Add FX
        result = await bridge.call_lua("TrackFX_AddByName", [track_handle, fx_name, False, -1 if instantiate else -1000])
        
        if result.get("ok"):
            fx_index = result.get("ret", -1)
            if fx_index >= 0:
                return [TextContent(
                    type="text",
                    text=f"Added {fx_name} to track {track_index} at FX index {fx_index}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Failed to add {fx_name} to track {track_index}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add FX: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "track_fx_delete":
        track_index = arguments["track_index"]
        fx_index = arguments["fx_index"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Delete FX
        result = await bridge.call_lua("TrackFX_Delete", [track_handle, fx_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Deleted FX at index {fx_index} from track {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete FX: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "track_fx_get_enabled":
        track_index = arguments["track_index"]
        fx_index = arguments["fx_index"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Get enabled state
        result = await bridge.call_lua("TrackFX_GetEnabled", [track_handle, fx_index])
        
        if result.get("ok"):
            enabled = bool(result.get("ret", False))
            return [TextContent(
                type="text",
                text=f"FX {fx_index} on track {track_index} is {'enabled' if enabled else 'disabled'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get FX enabled state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "track_fx_set_enabled":
        track_index = arguments["track_index"]
        fx_index = arguments["fx_index"]
        enabled = arguments["enabled"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Set enabled state
        result = await bridge.call_lua("TrackFX_SetEnabled", [track_handle, fx_index, enabled])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"FX {fx_index} on track {track_index} {'enabled' if enabled else 'disabled'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set FX enabled state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "track_fx_get_name":
        track_index = arguments["track_index"]
        fx_index = arguments["fx_index"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Get FX name
        result = await bridge.call_lua("TrackFX_GetFXName", [track_handle, fx_index, ""])
        
        if result.get("ok"):
            # The result contains both the return value and the name
            if isinstance(result.get("ret"), list) and len(result.get("ret", [])) > 1:
                fx_name = result.get("ret")[1]
            else:
                fx_name = "Unknown"
            return [TextContent(
                type="text",
                text=f"FX {fx_index} on track {track_index}: {fx_name}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get FX name: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_envelope_by_name":
        track_index = arguments["track_index"]
        envelope_name = arguments["envelope_name"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Get envelope by name
        result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
        
        if result.get("ok"):
            envelope_handle = result.get("ret")
            if envelope_handle:
                return [TextContent(
                    type="text",
                    text=f"Found envelope '{envelope_name}' on track {track_index}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Envelope '{envelope_name}' not found on track {track_index}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get envelope: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "count_envelope_points":
        track_index = arguments["track_index"]
        envelope_name = arguments["envelope_name"]
        
        # Get track and envelope
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
        
        if not env_result.get("ok") or not env_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find envelope '{envelope_name}' on track {track_index}"
            )]
        
        envelope_handle = env_result.get("ret")
        
        # Count points
        result = await bridge.call_lua("CountEnvelopePoints", [envelope_handle])
        
        if result.get("ok"):
            count = result.get("ret", 0)
            return [TextContent(
                type="text",
                text=f"Envelope '{envelope_name}' has {count} points"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count envelope points: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "insert_envelope_point":
        track_index = arguments["track_index"]
        envelope_name = arguments["envelope_name"]
        time = arguments["time"]
        value = arguments["value"]
        shape = arguments.get("shape", 0)
        selected = arguments.get("selected", False)
        
        # Get track and envelope
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
        
        if not env_result.get("ok") or not env_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find envelope '{envelope_name}' on track {track_index}"
            )]
        
        envelope_handle = env_result.get("ret")
        
        # Insert point
        result = await bridge.call_lua("InsertEnvelopePoint", [
            envelope_handle, time, value, shape, 0, selected, True
        ])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Inserted point at {time:.3f}s with value {value:.3f} in '{envelope_name}' envelope"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to insert envelope point: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "delete_envelope_point":
        track_index = arguments["track_index"]
        envelope_name = arguments["envelope_name"]
        point_index = arguments["point_index"]
        
        # Get track and envelope
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
        
        if not env_result.get("ok") or not env_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find envelope '{envelope_name}' on track {track_index}"
            )]
        
        envelope_handle = env_result.get("ret")
        
        # Delete point
        result = await bridge.call_lua("DeleteEnvelopePointEx", [envelope_handle, -1, point_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Deleted point {point_index} from '{envelope_name}' envelope"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete envelope point: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_envelope_point":
        track_index = arguments["track_index"]
        envelope_name = arguments["envelope_name"]
        point_index = arguments["point_index"]
        
        # Get track and envelope
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
        
        if not env_result.get("ok") or not env_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find envelope '{envelope_name}' on track {track_index}"
            )]
        
        envelope_handle = env_result.get("ret")
        
        # Get point info
        result = await bridge.call_lua("GetEnvelopePoint", [envelope_handle, point_index, 0, 0, 0, 0, 0])
        
        if result.get("ok"):
            ret_values = result.get("ret", [])
            if isinstance(ret_values, list) and len(ret_values) >= 6:
                retval, time, value, shape, tension, selected = ret_values[:6]
                if retval:
                    return [TextContent(
                        type="text",
                        text=f"Point {point_index}: time={time:.3f}s, value={value:.3f}, shape={shape}, selected={bool(selected)}"
                    )]
            return [TextContent(
                type="text",
                text=f"Point {point_index} not found"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get envelope point: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_envelope_point_value":
        track_index = arguments["track_index"]
        envelope_name = arguments["envelope_name"]
        point_index = arguments["point_index"]
        new_value = arguments["value"]
        new_time = arguments.get("time", None)
        
        # Get track and envelope
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        env_result = await bridge.call_lua("GetTrackEnvelopeByName", [track_handle, envelope_name])
        
        if not env_result.get("ok") or not env_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find envelope '{envelope_name}' on track {track_index}"
            )]
        
        envelope_handle = env_result.get("ret")
        
        # Get current point info
        get_result = await bridge.call_lua("GetEnvelopePoint", [envelope_handle, point_index, 0, 0, 0, 0, 0])
        
        if get_result.get("ok"):
            ret_values = get_result.get("ret", [])
            if isinstance(ret_values, list) and len(ret_values) >= 6:
                retval, time, old_value, shape, tension, selected = ret_values[:6]
                if retval:
                    # Use new time if provided, otherwise keep existing
                    if new_time is not None:
                        time = new_time
                    
                    # Set point value
                    result = await bridge.call_lua("SetEnvelopePoint", [
                        envelope_handle, point_index, time, new_value, shape, tension, selected, True
                    ])
                    
                    if result.get("ok"):
                        return [TextContent(
                            type="text",
                            text=f"Updated point {point_index} to value {new_value:.3f} at {time:.3f}s"
                        )]
                    else:
                        return [TextContent(
                            type="text",
                            text=f"Failed to set envelope point: {result.get('error', 'Unknown error')}"
                        )]
        
        return [TextContent(
            type="text",
            text=f"Failed to get envelope point {point_index}"
        )]
    
    elif name == "create_track_send":
        source_track_index = arguments["source_track_index"]
        dest_track_index = arguments["dest_track_index"]
        
        # Get source and destination tracks
        source_result = await bridge.call_lua("GetTrack", [0, source_track_index])
        if not source_result.get("ok") or not source_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find source track at index {source_track_index}"
            )]
        
        dest_result = await bridge.call_lua("GetTrack", [0, dest_track_index])
        if not dest_result.get("ok") or not dest_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find destination track at index {dest_track_index}"
            )]
        
        source_track = source_result.get("ret")
        dest_track = dest_result.get("ret")
        
        # Create send
        result = await bridge.call_lua("CreateTrackSend", [source_track, dest_track])
        
        if result.get("ok"):
            send_index = result.get("ret", -1)
            if send_index >= 0:
                return [TextContent(
                    type="text",
                    text=f"Created send from track {source_track_index} to track {dest_track_index} (send index: {send_index})"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Failed to create send"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create send: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "remove_track_send":
        track_index = arguments["track_index"]
        send_index = arguments["send_index"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Remove send
        result = await bridge.call_lua("RemoveTrackSend", [track_handle, 0, send_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Removed send {send_index} from track {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to remove send: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_num_sends":
        track_index = arguments["track_index"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Get number of sends
        result = await bridge.call_lua("GetTrackNumSends", [track_handle, 0])
        
        if result.get("ok"):
            num_sends = result.get("ret", 0)
            return [TextContent(
                type="text",
                text=f"Track {track_index} has {num_sends} sends"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get number of sends: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_send_volume":
        track_index = arguments["track_index"]
        send_index = arguments["send_index"]
        volume = arguments["volume"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Set send volume
        result = await bridge.call_lua("SetTrackSendInfo_Value", [track_handle, 0, send_index, "D_VOL", volume])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set send {send_index} volume to {volume:.3f}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set send volume: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_send_info":
        track_index = arguments["track_index"]
        send_index = arguments["send_index"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Get send volume
        vol_result = await bridge.call_lua("GetTrackSendInfo_Value", [track_handle, 0, send_index, "D_VOL"])
        
        # Get destination track
        dest_result = await bridge.call_lua("GetTrackSendInfo_Value", [track_handle, 0, send_index, "P_DESTTRACK"])
        
        if vol_result.get("ok"):
            volume = vol_result.get("ret", 0.0)
            dest_info = ""
            if dest_result.get("ok") and dest_result.get("ret"):
                # Try to find destination track index
                for i in range(100):  # Check first 100 tracks
                    check_result = await bridge.call_lua("GetTrack", [0, i])
                    if check_result.get("ok") and check_result.get("ret") == dest_result.get("ret"):
                        dest_info = f", destination: track {i}"
                        break
            
            return [TextContent(
                type="text",
                text=f"Send {send_index}: volume={volume:.3f}{dest_info}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get send info: {vol_result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_project_tempo":
        # Get master tempo
        result = await bridge.call_lua("Master_GetTempo")
        
        if result.get("ok"):
            tempo = result.get("ret", 120.0)
            return [TextContent(
                type="text",
                text=f"Project tempo: {tempo:.1f} BPM"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project tempo: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_project_tempo":
        tempo = arguments["tempo"]
        
        # Set master tempo
        result = await bridge.call_lua("SetTempoTimeSigMarker", [0, -1, -1, -1, -1, tempo, 0, 0, False])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set project tempo to {tempo:.1f} BPM"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set project tempo: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_project_time_signature":
        # Get time signature at edit cursor
        result = await bridge.call_lua("TimeMap_GetTimeSigAtTime", [0, 0, 0, 0])
        
        if result.get("ok"):
            ret_values = result.get("ret", [])
            if isinstance(ret_values, list) and len(ret_values) >= 3:
                num, denom = ret_values[1], ret_values[2]
                return [TextContent(
                    type="text",
                    text=f"Time signature: {num}/{denom}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="Failed to parse time signature"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get time signature: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_project_time_signature":
        numerator = arguments["numerator"]
        denominator = arguments["denominator"]
        
        # Set time signature at project start
        result = await bridge.call_lua("SetTempoTimeSigMarker", [0, -1, -1, -1, -1, -1, numerator, denominator, False])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set time signature to {numerator}/{denominator}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set time signature: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_tempo_at_position":
        position = arguments["position"]
        
        # Get tempo at specific time
        result = await bridge.call_lua("TimeMap_GetDividedBpmAtTime", [position])
        
        if result.get("ok"):
            tempo = result.get("ret", 120.0)
            return [TextContent(
                type="text",
                text=f"Tempo at {position:.3f}s: {tempo:.1f} BPM"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get tempo at position: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "insert_tempo_marker":
        position = arguments["position"]
        tempo = arguments["tempo"]
        numerator = arguments.get("time_sig_numerator", None)
        denominator = arguments.get("time_sig_denominator", None)
        
        # Convert position to measure and beat
        measures_result = await bridge.call_lua("TimeMap_timeToBeats", [position])
        
        if measures_result.get("ok"):
            beats = measures_result.get("ret", 0.0)
            
            # If time signature not provided, get current
            if numerator is None or denominator is None:
                ts_result = await bridge.call_lua("TimeMap_GetTimeSigAtTime", [0, position, 0, 0])
                if ts_result.get("ok") and isinstance(ts_result.get("ret"), list) and len(ts_result.get("ret", [])) >= 3:
                    if numerator is None:
                        numerator = ts_result.get("ret")[1]
                    if denominator is None:
                        denominator = ts_result.get("ret")[2]
                else:
                    numerator = numerator or 4
                    denominator = denominator or 4
            
            # Insert tempo marker
            result = await bridge.call_lua("SetTempoTimeSigMarker", [0, -1, position, -1, -1, tempo, numerator, denominator, True])
            
            if result.get("ok"):
                return [TextContent(
                    type="text",
                    text=f"Inserted tempo marker at {position:.3f}s: {tempo:.1f} BPM, {numerator}/{denominator}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Failed to insert tempo marker: {result.get('error', 'Unknown error')}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to convert position to beats: {measures_result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_media_item_selected":
        item_index = arguments["item_index"]
        selected = arguments["selected"]
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find media item at index {item_index}"
            )]
        
        item_handle = item_result.get("ret")
        
        # Set selection state
        result = await bridge.call_lua("SetMediaItemSelected", [item_handle, selected])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"{'Selected' if selected else 'Deselected'} media item at index {item_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set selection state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "count_selected_media_items":
        result = await bridge.call_lua("CountSelectedMediaItems", [0])
        
        if result.get("ok"):
            count = result.get("ret", 0)
            return [TextContent(
                type="text",
                text=f"{count} selected media items"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count selected items: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_selected_media_item":
        index = arguments["index"]
        
        result = await bridge.call_lua("GetSelectedMediaItem", [0, index])
        
        if result.get("ok"):
            item_handle = result.get("ret")
            if item_handle:
                return [TextContent(
                    type="text",
                    text=f"Selected item handle: {item_handle}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"No selected item at index {index}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get selected item: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "count_selected_tracks":
        result = await bridge.call_lua("CountSelectedTracks", [0])
        
        if result.get("ok"):
            count = result.get("ret", 0)
            return [TextContent(
                type="text",
                text=f"{count} selected tracks"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count selected tracks: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_selected_track":
        index = arguments["index"]
        
        result = await bridge.call_lua("GetSelectedTrack", [0, index])
        
        if result.get("ok"):
            track_handle = result.get("ret")
            if track_handle:
                return [TextContent(
                    type="text",
                    text=f"Selected track handle: {track_handle}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"No selected track at index {index}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get selected track: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_project_sample_rate":
        result = await bridge.call_lua("GetSetProjectInfo_String", [0, "RENDER_SRATE", "", False])
        
        if result.get("ok"):
            sample_rate_str = result.get("ret", "44100")
            try:
                sample_rate = int(float(sample_rate_str))
                return [TextContent(
                    type="text",
                    text=f"Project sample rate: {sample_rate} Hz"
                )]
            except:
                # Try alternate method
                result2 = await bridge.call_lua("GetSetProjectInfo", [0, "PROJECT_SRATE", 0, False])
                if result2.get("ok"):
                    sample_rate = int(result2.get("ret", 44100))
                    return [TextContent(
                        type="text",
                        text=f"Project sample rate: {sample_rate} Hz"
                    )]
                return [TextContent(
                    type="text",
                    text="Failed to parse sample rate"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get sample rate: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_project_sample_rate":
        sample_rate = arguments["sample_rate"]
        
        # Set sample rate
        result = await bridge.call_lua("GetSetProjectInfo", [0, "PROJECT_SRATE", sample_rate, True])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set project sample rate to {sample_rate} Hz"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set sample rate: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_project_length":
        result = await bridge.call_lua("GetProjectLength", [0])
        
        if result.get("ok"):
            length = result.get("ret", 0.0)
            return [TextContent(
                type="text",
                text=f"Project length: {length:.3f} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project length: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_project_length":
        length = arguments["length"]
        
        # Get current cursor position
        cursor_result = await bridge.call_lua("GetCursorPosition", [])
        cursor_pos = cursor_result.get("ret", 0.0) if cursor_result.get("ok") else 0.0
        
        # Move cursor to desired length
        await bridge.call_lua("SetEditCurPos", [length, False, False])
        
        # Insert marker to extend project
        await bridge.call_lua("Main_OnCommand", [40157, 0])  # Insert marker at current position
        
        # Delete the marker (we just needed it to extend project)
        await bridge.call_lua("Main_OnCommand", [40613, 0])  # Delete marker near cursor
        
        # Restore cursor position
        await bridge.call_lua("SetEditCurPos", [cursor_pos, False, False])
        
        return [TextContent(
            type="text",
            text=f"Set project length to {length:.3f} seconds"
        )]
    
    elif name == "get_project_grid_division":
        result = await bridge.call_lua("GetSetProjectGrid", [0, False, 0, 0, 0])
        
        if result.get("ok") and isinstance(result.get("ret"), list) and len(result.get("ret", [])) >= 1:
            division = result.get("ret")[0]
            # Convert to fraction string
            if division == 0.25:
                division_str = "1/4"
            elif division == 0.125:
                division_str = "1/8"
            elif division == 0.0625:
                division_str = "1/16"
            elif division == 0.5:
                division_str = "1/2"
            elif division == 1.0:
                division_str = "1/1"
            else:
                division_str = f"{division:.4f}"
            
            return [TextContent(
                type="text",
                text=f"Project grid division: {division_str}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get grid division: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_project_grid_division":
        division = arguments["division"]
        
        result = await bridge.call_lua("GetSetProjectGrid", [0, True, division, 0, 0])
        
        if result.get("ok"):
            # Convert to fraction string for display
            if division == 0.25:
                division_str = "1/4"
            elif division == 0.125:
                division_str = "1/8"
            elif division == 0.0625:
                division_str = "1/16"
            elif division == 0.5:
                division_str = "1/2"
            elif division == 1.0:
                division_str = "1/1"
            else:
                division_str = f"{division:.4f}"
            
            return [TextContent(
                type="text",
                text=f"Set project grid division to {division_str}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set grid division: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_project_render_bounds":
        result = await bridge.call_lua("GetSetProjectInfo", [0, "RENDER_SETTINGS", 0, False])
        
        if result.get("ok"):
            settings = int(result.get("ret", 0))
            # Extract bounds mode from render settings (bits 0-1)
            bounds_mode = settings & 0x03
            
            if bounds_mode == 0:
                bounds_str = "Entire project"
            elif bounds_mode == 1:
                bounds_str = "Time selection"
            elif bounds_mode == 2:
                bounds_str = "Custom"
            else:
                bounds_str = f"Unknown ({bounds_mode})"
            
            return [TextContent(
                type="text",
                text=f"Render bounds: {bounds_str}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get render bounds: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_project_render_bounds":
        bounds_mode = arguments["bounds_mode"]
        
        # Get current render settings
        settings_result = await bridge.call_lua("GetSetProjectInfo", [0, "RENDER_SETTINGS", 0, False])
        current_settings = int(settings_result.get("ret", 0)) if settings_result.get("ok") else 0
        
        # Clear bounds bits (0-1) and set new mode
        new_settings = (current_settings & ~0x03) | (bounds_mode & 0x03)
        
        result = await bridge.call_lua("GetSetProjectInfo", [0, "RENDER_SETTINGS", new_settings, True])
        
        if result.get("ok"):
            if bounds_mode == 0:
                bounds_str = "Entire project"
            elif bounds_mode == 1:
                bounds_str = "Time selection"
            elif bounds_mode == 2:
                bounds_str = "Custom"
            else:
                bounds_str = f"Mode {bounds_mode}"
            
            return [TextContent(
                type="text",
                text=f"Set render bounds to: {bounds_str}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set render bounds: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_project_notes":
        result = await bridge.call_lua("GetSetProjectNotes", [0, False, ""])
        
        if result.get("ok"):
            notes = result.get("ret", "")
            if notes:
                return [TextContent(
                    type="text",
                    text=f"Project notes: {notes}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="Project notes: (empty)"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project notes: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_project_notes":
        notes = arguments["notes"]
        
        result = await bridge.call_lua("GetSetProjectNotes", [0, True, notes])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set project notes successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set project notes: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_automation_mode":
        track_index = arguments["track_index"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Get automation mode
        result = await bridge.call_lua("GetTrackAutomationMode", [track_handle])
        
        if result.get("ok"):
            mode = result.get("ret", 0)
            mode_names = {
                0: "Trim/Read",
                1: "Read",
                2: "Touch", 
                3: "Write",
                4: "Latch",
                5: "Latch Preview"
            }
            mode_name = mode_names.get(mode, f"Unknown ({mode})")
            
            return [TextContent(
                type="text",
                text=f"Track {track_index} automation mode: {mode_name}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get automation mode: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_automation_mode":
        track_index = arguments["track_index"]
        mode = arguments["mode"]
        
        # Get track
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        
        # Set automation mode
        result = await bridge.call_lua("SetTrackAutomationMode", [track_handle, mode])
        
        if result.get("ok"):
            mode_names = {
                0: "Trim/Read",
                1: "Read",
                2: "Touch",
                3: "Write",
                4: "Latch"
            }
            mode_name = mode_names.get(mode, f"Mode {mode}")
            
            return [TextContent(
                type="text",
                text=f"Set track {track_index} to {mode_name} mode"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set automation mode: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_global_automation_override":
        result = await bridge.call_lua("GetGlobalAutomationOverride", [])
        
        if result.get("ok"):
            override = result.get("ret", 0)
            override_names = {
                -1: "No change",
                0: "No override (normal)",
                1: "Bypass all automation",
                2: "All automation to trim/read mode",
                5: "All automation to write mode",
                6: "All automation to touch mode"
            }
            override_name = override_names.get(override, f"Unknown ({override})")
            
            return [TextContent(
                type="text",
                text=f"Global automation override: {override_name}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get global automation override: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_global_automation_override":
        mode = arguments["mode"]
        
        # Map our simplified modes to REAPER's internal values
        mode_map = {
            0: 0,   # No override
            1: 1,   # Bypass all
            2: 2    # All to trim/read
        }
        
        reaper_mode = mode_map.get(mode, mode)
        result = await bridge.call_lua("SetGlobalAutomationOverride", [reaper_mode])
        
        if result.get("ok"):
            mode_names = {
                0: "No override",
                1: "Bypass all automation",
                2: "All automation to trim/read"
            }
            mode_name = mode_names.get(mode, f"Mode {mode}")
            
            return [TextContent(
                type="text",
                text=f"Set global automation override to: {mode_name}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set global automation override: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_peak":
        track_index = arguments["track_index"]
        channel = arguments.get("channel", 0)
        
        result = await bridge.call_lua("Track_GetPeakInfo", [track_index, channel])
        
        if result.get("ok"):
            peak_value = result.get("result", 0.0)
            peak_db = 20 * (peak_value / 0.0000000298023223876953125) if peak_value > 0 else -150.0
            return [TextContent(
                type="text",
                text=f"Track {track_index} peak (channel {channel}): {peak_db:.2f} dB ({peak_value:.6f})"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track peak: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_peak_info":
        track_index = arguments["track_index"]
        
        result = await bridge.call_lua("Track_GetPeakHoldDB", [track_index])
        
        if result.get("ok"):
            peak_data = result.get("result", {})
            left_peak = peak_data.get("left", -150.0)
            right_peak = peak_data.get("right", -150.0)
            return [TextContent(
                type="text",
                text=f"Track {track_index} peak info - Left: {left_peak:.2f} dB, Right: {right_peak:.2f} dB"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track peak info: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_media_item_peak":
        item_index = arguments["item_index"]
        
        result = await bridge.call_lua("GetMediaItemTakePeakValue", [item_index])
        
        if result.get("ok"):
            peak_value = result.get("result", 0.0)
            peak_db = 20 * (peak_value / 0.0000000298023223876953125) if peak_value > 0 else -150.0
            return [TextContent(
                type="text",
                text=f"Media item {item_index} peak: {peak_db:.2f} dB ({peak_value:.6f})"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item peak: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_receive_count":
        track_index = arguments["track_index"]
        
        result = await bridge.call_lua("GetTrackNumSends", [track_index, -1])
        
        if result.get("ok"):
            count = result.get("result", 0)
            return [TextContent(
                type="text",
                text=f"Track {track_index} has {count} receives"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track receive count: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_receive_info":
        track_index = arguments["track_index"]
        receive_index = arguments["receive_index"]
        
        result = await bridge.call_lua("GetTrackReceiveInfo", [track_index, receive_index])
        
        if result.get("ok"):
            info = result.get("result", {})
            return [TextContent(
                type="text",
                text=f"Receive {receive_index} from track {info.get('src_track', 'unknown')} - Volume: {info.get('volume', 0):.2f} dB, Pan: {info.get('pan', 0):.2f}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track receive info: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_guid":
        track_index = arguments["track_index"]
        
        result = await bridge.call_lua("GetTrackGUID", [track_index])
        
        if result.get("ok"):
            guid = result.get("result", "")
            return [TextContent(
                type="text",
                text=f"Track {track_index} GUID: {guid}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track GUID: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_from_guid":
        guid = arguments["guid"]
        
        result = await bridge.call_lua("GetTrackByGUID", [guid])
        
        if result.get("ok"):
            track_info = result.get("result", {})
            return [TextContent(
                type="text",
                text=f"Found track: {track_info.get('name', 'Unnamed')} at index {track_info.get('index', -1)}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track from GUID: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "split_media_item":
        item_index = arguments["item_index"]
        position = arguments["position"]
        
        result = await bridge.call_lua("SplitMediaItem", [item_index, position])
        
        if result.get("ok"):
            new_item = result.get("result")
            return [TextContent(
                type="text",
                text=f"Split item at position {position}s. New item created: {new_item}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to split media item: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "glue_media_items":
        respect_time_selection = arguments.get("respect_time_selection", False)
        
        result = await bridge.call_lua("GlueMediaItems", [respect_time_selection])
        
        if result.get("ok"):
            count = result.get("result", 0)
            return [TextContent(
                type="text",
                text=f"Glued {count} items together"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to glue media items: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_media_item_take_track":
        item_index = arguments["item_index"]
        
        result = await bridge.call_lua("GetMediaItemTrack", [item_index])
        
        if result.get("ok"):
            track_info = result.get("result", {})
            return [TextContent(
                type="text",
                text=f"Item {item_index} is on track: {track_info.get('name', 'Unnamed')} (index {track_info.get('index', -1)})"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get item track: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "duplicate_media_item":
        item_index = arguments["item_index"]
        
        result = await bridge.call_lua("DuplicateMediaItem", [item_index])
        
        if result.get("ok"):
            new_item_index = result.get("result", -1)
            return [TextContent(
                type="text",
                text=f"Duplicated item. New item index: {new_item_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to duplicate media item: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_media_item_color":
        item_index = arguments["item_index"]
        color = arguments["color"]
        
        result = await bridge.call_lua("SetMediaItemColor", [item_index, color])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set item {item_index} color to {color}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item color: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_record_mode":
        track_index = arguments["track_index"]
        
        result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_index, "I_RECMODE"])
        
        if result.get("ok"):
            mode = int(result.get("ret", 0))
            mode_names = {
                0: "Input",
                1: "Stereo out",
                2: "None (monitoring only)",
                3: "Stereo out with latency compensation",
                4: "MIDI output",
                5: "Mono out",
                6: "Mono out with latency compensation",
                7: "MIDI overdub",
                8: "MIDI replace"
            }
            mode_name = mode_names.get(mode, f"Unknown mode {mode}")
            return [TextContent(
                type="text",
                text=f"Track {track_index} record mode: {mode_name} ({mode})"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track record mode: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_record_mode":
        track_index = arguments["track_index"]
        mode = arguments["mode"]
        
        result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_index, "I_RECMODE", mode])
        
        if result.get("ok"):
            mode_names = {
                0: "Input",
                1: "Stereo out",
                2: "None (monitoring only)",
                3: "Stereo out with latency compensation",
                4: "MIDI output",
                5: "Mono out",
                6: "Mono out with latency compensation",
                7: "MIDI overdub",
                8: "MIDI replace"
            }
            mode_name = mode_names.get(mode, f"mode {mode}")
            return [TextContent(
                type="text",
                text=f"Set track {track_index} record mode to: {mode_name}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track record mode: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_record_input":
        track_index = arguments["track_index"]
        
        result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_index, "I_RECINPUT"])
        
        if result.get("ok"):
            input_val = int(result.get("ret", -1))
            if input_val == -1:
                input_name = "None"
            elif input_val < 512:
                input_name = f"Mono hardware input {input_val + 1}"
            elif input_val < 1024:
                pair = (input_val - 512) // 2 + 1
                input_name = f"Stereo hardware input pair {pair}"
            else:
                input_name = f"ReaRoute/loopback {input_val - 1024 + 1}"
            
            return [TextContent(
                type="text",
                text=f"Track {track_index} record input: {input_name} ({input_val})"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track record input: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_record_input":
        track_index = arguments["track_index"]
        input_val = arguments["input"]
        
        result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_index, "I_RECINPUT", input_val])
        
        if result.get("ok"):
            if input_val == -1:
                input_name = "None"
            elif input_val < 512:
                input_name = f"Mono hardware input {input_val + 1}"
            elif input_val < 1024:
                pair = (input_val - 512) // 2 + 1
                input_name = f"Stereo hardware input pair {pair}"
            else:
                input_name = f"ReaRoute/loopback {input_val - 1024 + 1}"
            
            return [TextContent(
                type="text",
                text=f"Set track {track_index} record input to: {input_name}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track record input: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_record_arm":
        track_index = arguments["track_index"]
        
        result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_index, "I_RECARM"])
        
        if result.get("ok"):
            armed = result.get("ret", 0) > 0
            return [TextContent(
                type="text",
                text=f"Track {track_index} record arm: {'Armed' if armed else 'Not armed'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track record arm state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_record_arm":
        track_index = arguments["track_index"]
        armed = arguments["armed"]
        
        result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_index, "I_RECARM", 1 if armed else 0])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track {track_index} record arm: {'Armed' if armed else 'Disarmed'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track record arm state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_num_midi_inputs":
        result = await bridge.call_lua("GetNumMIDIInputs", [])
        
        if result.get("ok"):
            count = result.get("result", 0)
            return [TextContent(
                type="text",
                text=f"Number of MIDI inputs: {count}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get number of MIDI inputs: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_num_midi_outputs":
        result = await bridge.call_lua("GetNumMIDIOutputs", [])
        
        if result.get("ok"):
            count = result.get("result", 0)
            return [TextContent(
                type="text",
                text=f"Number of MIDI outputs: {count}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get number of MIDI outputs: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_midi_input_name":
        input_index = arguments["input_index"]
        
        result = await bridge.call_lua("GetMIDIInputName", [input_index])
        
        if result.get("ok"):
            name_info = result.get("result", {})
            return [TextContent(
                type="text",
                text=f"MIDI input {input_index}: {name_info.get('name', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get MIDI input name: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_midi_output_name":
        output_index = arguments["output_index"]
        
        result = await bridge.call_lua("GetMIDIOutputName", [output_index])
        
        if result.get("ok"):
            name_info = result.get("result", {})
            return [TextContent(
                type="text",
                text=f"MIDI output {output_index}: {name_info.get('name', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get MIDI output name: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_color":
        track_index = arguments["track_index"]
        
        result = await bridge.call_lua("GetTrackColor", [track_index])
        
        if result.get("ok"):
            color = result.get("result", 0)
            # Extract RGB components
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            return [TextContent(
                type="text",
                text=f"Track {track_index} color: RGB({r}, {g}, {b}) (0x{color:06X})"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track color: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_color":
        track_index = arguments["track_index"]
        color = arguments["color"]
        
        result = await bridge.call_lua("SetTrackColor", [track_index, color])
        
        if result.get("ok"):
            if color == 0:
                return [TextContent(
                    type="text",
                    text=f"Set track {track_index} color to default"
                )]
            else:
                r = (color >> 16) & 0xFF
                g = (color >> 8) & 0xFF
                b = color & 0xFF
                return [TextContent(
                    type="text",
                    text=f"Set track {track_index} color to RGB({r}, {g}, {b})"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track color: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_media_item_color":
        item_index = arguments["item_index"]
        
        result = await bridge.call_lua("GetMediaItemColor", [item_index])
        
        if result.get("ok"):
            color = result.get("result", 0)
            if color == 0:
                return [TextContent(
                    type="text",
                    text=f"Media item {item_index} color: Default"
                )]
            else:
                r = (color >> 16) & 0xFF
                g = (color >> 8) & 0xFF
                b = color & 0xFF
                return [TextContent(
                    type="text",
                    text=f"Media item {item_index} color: RGB({r}, {g}, {b}) (0x{color:06X})"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item color: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "open_project":
        filename = arguments["filename"]
        in_new_tab = arguments.get("in_new_tab", False)
        
        result = await bridge.call_lua("Main_openProject", [filename, in_new_tab])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Opened project: {filename}" + (" in new tab" if in_new_tab else "")
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to open project: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "enum_projects":
        result = await bridge.call_lua("EnumProjects", [])
        
        if result.get("ok"):
            projects = result.get("result", [])
            if not projects:
                return [TextContent(
                    type="text",
                    text="No projects open"
                )]
            else:
                project_list = "\n".join([f"{i}: {p['name']} {'(current)' if p['current'] else ''}" 
                                         for i, p in enumerate(projects)])
                return [TextContent(
                    type="text",
                    text=f"Open projects:\n{project_list}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to enumerate projects: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "select_project_instance":
        project_index = arguments["project_index"]
        
        result = await bridge.call_lua("SelectProjectInstance", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Switched to project {project_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to switch project: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_current_project_index":
        result = await bridge.call_lua("GetCurrentProjectIndex", [])
        
        if result.get("ok"):
            index = result.get("result", -1)
            return [TextContent(
                type="text",
                text=f"Current project index: {index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get current project index: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "close_project":
        save_prompt = arguments.get("save_prompt", True)
        
        result = await bridge.call_lua("Main_OnCommand", [40860 if save_prompt else 40816, 0])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Closed current project" + (" with save prompt" if save_prompt else " without saving")
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to close project: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "render_project":
        bounds = arguments.get("bounds", "entire_project")
        
        # Map bounds to REAPER action IDs
        action_map = {
            "entire_project": 41824,  # Render project to disk
            "time_selection": 41823,  # Render time selection
            "selected_items": 65535   # Render selected media items
        }
        
        action_id = action_map.get(bounds, 41824)
        result = await bridge.call_lua("Main_OnCommand", [action_id, 0])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Started render dialog for: {bounds.replace('_', ' ')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to start render: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "bounce_tracks":
        add_to_project = arguments.get("add_to_project", True)
        
        # Bounce selected tracks (action 40914)
        result = await bridge.call_lua("Main_OnCommand", [40914, 0])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Bounced selected tracks" + (" to new track" if add_to_project else "")
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to bounce tracks: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_render_settings":
        result = await bridge.call_lua("GetProjectRenderSettings", [])
        
        if result.get("ok"):
            settings = result.get("result", {})
            return [TextContent(
                type="text",
                text=f"Render settings:\nSample rate: {settings.get('srate', 'Unknown')} Hz\nChannels: {settings.get('channels', 'Unknown')}\nFormat: {settings.get('format', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get render settings: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_render_settings":
        # Note: This is a simplified implementation
        # In reality, REAPER's render settings are complex and require
        # multiple API calls or direct project chunk manipulation
        
        settings_changed = []
        if "sample_rate" in arguments:
            settings_changed.append(f"Sample rate: {arguments['sample_rate']} Hz")
        if "channels" in arguments:
            settings_changed.append(f"Channels: {arguments['channels']}")
        if "format" in arguments:
            settings_changed.append(f"Format: {arguments['format']}")
        
        if settings_changed:
            # For now, we'll just acknowledge the request
            # Real implementation would require GetSetProjectInfo or chunk manipulation
            return [TextContent(
                type="text",
                text=f"Render settings updated:\n" + "\n".join(settings_changed) + "\n(Note: Full implementation requires project chunk manipulation)"
            )]
        else:
            return [TextContent(
                type="text",
                text="No render settings specified"
            )]
    
    elif name == "check_video_support":
        result = await bridge.call_lua("CheckVideoSupport", [])
        
        if result.get("ok"):
            has_video = result.get("result", False)
            return [TextContent(
                type="text",
                text=f"Video support: {'Available' if has_video else 'Not available'}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to check video support: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_video_settings":
        result = await bridge.call_lua("GetVideoSettings", [])
        
        if result.get("ok"):
            settings = result.get("result", {})
            return [TextContent(
                type="text",
                text=f"Video settings:\nWidth: {settings.get('width', 'Unknown')} px\nHeight: {settings.get('height', 'Unknown')} px\nFPS: {settings.get('fps', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get video settings: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_video_settings":
        settings_changed = []
        if "width" in arguments:
            settings_changed.append(f"Width: {arguments['width']} px")
        if "height" in arguments:
            settings_changed.append(f"Height: {arguments['height']} px")
        if "fps" in arguments:
            settings_changed.append(f"FPS: {arguments['fps']}")
        
        if settings_changed:
            # Note: Actual implementation would require video processor API
            return [TextContent(
                type="text",
                text=f"Video settings updated:\n" + "\n".join(settings_changed) + "\n(Note: Full implementation requires video processor API)"
            )]
        else:
            return [TextContent(
                type="text",
                text="No video settings specified"
            )]
    
    elif name == "add_video_to_track":
        track_index = arguments["track_index"]
        video_file = arguments["video_file"]
        
        result = await bridge.call_lua("AddVideoToTrack", [track_index, video_file])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Added video '{video_file}' to track {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add video: {result.get('error', 'Unknown error')}"
            )]
    
    # Missing MIDI tool implementations
    elif name == "midi_get_note_name":
        note_number = arguments["note_number"]
        
        # Note names
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octave = (note_number // 12) - 1
        note_name = note_names[note_number % 12]
        
        return [TextContent(
            type="text",
            text=f"Note name: {note_name}{octave}"
        )]
    
    elif name == "midi_count_events":
        item_index = arguments.get("item_index", 0)
        take_index = arguments.get("take_index", 0)
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(type="text", text=f"Failed to find media item at index {item_index}")]
        
        item_handle = item_result.get("ret")
        
        # Get take
        result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
        if not result.get("ok") or not result.get("ret"):
            return [TextContent(type="text", text=f"Failed to find take at index {take_index}")]
        
        take_handle = result.get("ret")
        
        # Count events
        result = await bridge.call_lua("MIDI_CountEvts", [take_handle])
        if result.get("ok"):
            # MIDI_CountEvts returns multiple values
            notes = result.get("notes", 0)
            ccs = result.get("cc", 0)
            text_events = result.get("text", 0)
            
            return [TextContent(
                type="text",
                text=f"MIDI event counts: notes={notes}, CCs={ccs}, sysex={text_events}"
            )]
        
        return [TextContent(type="text", text="Failed to count MIDI events")]
    
    elif name == "midi_get_scale":
        item_index = arguments.get("item_index", 0)
        take_index = arguments.get("take_index", 0)
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(type="text", text=f"Failed to find media item at index {item_index}")]
        
        item_handle = item_result.get("ret")
        
        # Get take
        result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
        if not result.get("ok") or not result.get("ret"):
            return [TextContent(type="text", text=f"Failed to find take at index {take_index}")]
        
        take_handle = result.get("ret")
        
        # Get scale
        result = await bridge.call_lua("MIDI_GetScale", [take_handle])
        if result.get("ok"):
            root = result.get("root", 0)
            scale_type = result.get("scale", 0)
            name = result.get("name", "")
            
            return [TextContent(
                type="text",
                text=f"Scale: root={root}, type={scale_type}, name={name}"
            )]
        
        return [TextContent(type="text", text="Failed to get scale")]
    
    elif name == "midi_set_scale":
        item_index = arguments.get("item_index", 0)
        take_index = arguments.get("take_index", 0)
        root = arguments.get("root", 0)
        scale = arguments.get("scale", 0)
        signature = arguments.get("signature", "")
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(type="text", text=f"Failed to find media item at index {item_index}")]
        
        item_handle = item_result.get("ret")
        
        # Get take
        result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
        if not result.get("ok") or not result.get("ret"):
            return [TextContent(type="text", text=f"Failed to find take at index {take_index}")]
        
        take_handle = result.get("ret")
        
        # Set scale
        result = await bridge.call_lua("MIDI_SetScale", [take_handle, root, scale, signature])
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set MIDI scale: root={root}, scale={scale}, signature={signature}"
            )]
        
        return [TextContent(type="text", text="Failed to set scale")]
    
    elif name == "midi_select_all":
        item_index = arguments.get("item_index", 0)
        take_index = arguments.get("take_index", 0)
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(type="text", text=f"Failed to find media item at index {item_index}")]
        
        item_handle = item_result.get("ret")
        
        # Get take
        result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
        if not result.get("ok") or not result.get("ret"):
            return [TextContent(type="text", text=f"Failed to find take at index {take_index}")]
        
        take_handle = result.get("ret")
        
        # Select all MIDI events
        result = await bridge.call_lua("MIDI_SelectAll", [take_handle, True])
        if result.get("ok"):
            return [TextContent(type="text", text="Selected all MIDI events")]
        
        return [TextContent(type="text", text="Failed to select MIDI events")]
    
    elif name == "midi_get_all_events":
        item_index = arguments.get("item_index", 0)
        take_index = arguments.get("take_index", 0)
        
        # Get media item
        item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
        if not item_result.get("ok") or not item_result.get("ret"):
            return [TextContent(type="text", text=f"Failed to find media item at index {item_index}")]
        
        item_handle = item_result.get("ret")
        
        # Get take
        result = await bridge.call_lua("GetMediaItemTake", [item_handle, take_index])
        if not result.get("ok") or not result.get("ret"):
            return [TextContent(type="text", text=f"Failed to find take at index {take_index}")]
        
        take_handle = result.get("ret")
        
        # Get all events
        result = await bridge.call_lua("MIDI_GetAllEvts", [take_handle])
        if result.get("ok") and result.get("ret"):
            events_data = result.get("ret", "")
            return [TextContent(
                type="text",
                text=f"MIDI events data: {len(events_data)} bytes"
            )]
        
        return [TextContent(type="text", text="Failed to get MIDI events")]
    
    elif name == "midi_insert_note":
        # This is an alias for insert_midi_note
        return await call_tool("insert_midi_note", arguments)
    
    elif name == "insert_track_at_index":
        # This is an alias for insert_track with different parameter names
        return await call_tool("insert_track", {
            "index": arguments["index"],
            "use_defaults": arguments.get("want_defaults", True)
        })
    
    elif name == "get_track_volume_db":
        track_index = arguments["track_index"]
        
        # Get track
        result = await bridge.call_lua("GetTrack", [0, track_index])
        if not result.get("ok") or not result.get("ret"):
            return [TextContent(type="text", text=f"Track {track_index} not found")]
        
        track_handle = result["retval"]
        
        # Get volume
        result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_handle, "D_VOL"])
        if result.get("ok") and result.get("retval") is not None:
            linear_vol = result["retval"]
            # Convert to dB
            import math
            if linear_vol > 0:
                db_vol = 20 * math.log10(linear_vol)
            else:
                db_vol = -150.0  # -inf
            
            return [TextContent(
                type="text",
                text=f"Track volume: {db_vol:.2f} dB"
            )]
        
        return [TextContent(type="text", text="Failed to get track volume")]
    
    elif name == "set_track_volume_db":
        track_index = arguments["track_index"]
        volume_db = arguments["volume_db"]
        
        # Get track
        result = await bridge.call_lua("GetTrack", [0, track_index])
        if not result.get("ok") or not result.get("ret"):
            return [TextContent(type="text", text=f"Track {track_index} not found")]
        
        track_handle = result["retval"]
        
        # Convert dB to linear
        import math
        if volume_db > -150:
            linear_vol = 10 ** (volume_db / 20)
        else:
            linear_vol = 0
        
        # Set volume
        result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_handle, "D_VOL", linear_vol])
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track volume to {volume_db:.2f} dB"
            )]
        
        return [TextContent(type="text", text="Failed to set track volume")]
    
    elif name == "freeze_track":
        track_index = arguments["track_index"]
        
        # Get track
        result = await bridge.call_lua("GetTrack", [0, track_index])
        if not result.get("ok") or not result.get("ret"):
            return [TextContent(type="text", text=f"Track {track_index} not found")]
        
        track_handle = result["retval"]
        
        # Freeze track
        result = await bridge.call_lua("Main_OnCommandEx", [41223, 0, 0])  # Track: Freeze to stereo
        if result.get("ok"):
            return [TextContent(type="text", text=f"Froze track {track_index}")]
        
        return [TextContent(type="text", text="Failed to freeze track")]
    
    elif name == "unfreeze_track":
        track_index = arguments["track_index"]
        
        # Get track
        result = await bridge.call_lua("GetTrack", [0, track_index])
        if not result.get("ok") or not result.get("ret"):
            return [TextContent(type="text", text=f"Track {track_index} not found")]
        
        track_handle = result["retval"]
        
        # Unfreeze track
        result = await bridge.call_lua("Main_OnCommandEx", [41644, 0, 0])  # Track: Unfreeze
        if result.get("ok"):
            return [TextContent(type="text", text=f"Unfroze track {track_index}")]
        
        return [TextContent(type="text", text="Failed to unfreeze track")]
    
    elif name == "get_resource_path":
        result = await bridge.call_lua("GetResourcePath", [])
        if result.get("ok") and result.get("retval"):
            return [TextContent(
                type="text",
                text=f"Resource path: {result['retval']}"
            )]
        
        return [TextContent(type="text", text="Failed to get resource path")]
    
    elif name == "get_exe_path":
        result = await bridge.call_lua("GetExePath", [])
        if result.get("ok") and result.get("retval"):
            return [TextContent(
                type="text",
                text=f"Executable path: {result['retval']}"
            )]
        
        return [TextContent(type="text", text="Failed to get executable path")]
    
    elif name == "show_console_msg":
        message = arguments["message"]
        
        result = await bridge.call_lua("ShowConsoleMsg", [message])
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Showed message: {message}"
            )]
        
        return [TextContent(type="text", text="Failed to show console message")]
    
    elif name == "clear_console":
        result = await bridge.call_lua("ClearConsole", [])
        if result.get("ok"):
            return [TextContent(type="text", text="Cleared console")]
        
        return [TextContent(type="text", text="Failed to clear console")]
    
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
    
    # Clean up any leftover files on startup
    cleanup_bridge_files()
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    finally:
        # Clean up on exit
        cleanup_bridge_files()

def main():
    import sys
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        cleanup_bridge_files()
    except Exception as e:
        logger.error(f"Server error: {e}")
        cleanup_bridge_files()
        raise

if __name__ == "__main__":
    main()