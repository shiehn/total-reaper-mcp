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
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

def main():
    import sys
    import mcp
    
    logger.info("Starting REAPER MCP Server...")
    logger.info(f"Will communicate with REAPER on {UDP_HOST}:{UDP_PORT}")
    
    mcp.run(app, transport="stdio")

if __name__ == "__main__":
    main()