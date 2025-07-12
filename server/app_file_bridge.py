import json
import os
import asyncio
import time
from pathlib import Path
from mcp.server import Server
from mcp import Tool
from mcp.types import TextContent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File-based bridge configuration
BRIDGE_DIR = Path.home() / "Library/Application Support/REAPER/Scripts/mcp_bridge_data"
REQUEST_FILE = BRIDGE_DIR / "request.json"
RESPONSE_FILE = BRIDGE_DIR / "response.json"
LOCK_FILE = BRIDGE_DIR / "lock"

class ReaperFileBridge:
    def __init__(self):
        # Ensure bridge directory exists
        BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Bridge directory: {BRIDGE_DIR}")
        
    async def call_lua(self, fname: str, args: list = None):
        if args is None:
            args = []
        
        # Clean up any old files
        for file in [REQUEST_FILE, RESPONSE_FILE, LOCK_FILE]:
            if file.exists():
                file.unlink()
        
        # Create request
        request = json.dumps({'call': fname, 'args': args})
        logger.info(f"Sending to Lua: {request}")
        
        try:
            # Write request file
            REQUEST_FILE.write_text(request)
            
            # Wait for response (max 5 seconds)
            start_time = time.time()
            while time.time() - start_time < 5.0:
                if RESPONSE_FILE.exists() and not LOCK_FILE.exists():
                    # Read response
                    response_text = RESPONSE_FILE.read_text()
                    RESPONSE_FILE.unlink()  # Clean up
                    
                    response = json.loads(response_text)
                    logger.info(f"Received from Lua: {response}")
                    return response
                
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
                    "want_defaults": {
                        "type": "boolean",
                        "description": "Add default envelopes/FX",
                        "default": True
                    }
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="get_reaper_version",
            description="Get the current REAPER version string",
            inputSchema={
                "type": "object",
                "properties": {}
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
            name="get_track",
            description="Get a track by index",
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
            name="get_track_name",
            description="Get the name of a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track": {
                        "type": "object",
                        "description": "The track object (from get_track)"
                    }
                },
                "required": ["track"]
            }
        ),
        Tool(
            name="set_track_name",
            description="Set the name of a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track": {
                        "type": "object",
                        "description": "The track object (from get_track)"
                    },
                    "name": {
                        "type": "string",
                        "description": "The new name for the track"
                    }
                },
                "required": ["track", "name"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls for REAPER operations"""
    
    if name == "insert_track":
        index = arguments["index"]
        want_defaults = arguments.get("want_defaults", True)
        
        result = await bridge.call_lua("InsertTrackAtIndex", [index, want_defaults])
        
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
    
    elif name == "get_reaper_version":
        result = await bridge.call_lua("GetAppVersion")
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"REAPER version: {result.get('ret', 'Unknown')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get version: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track_count":
        result = await bridge.call_lua("CountTracks", [0])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track count: {result.get('ret', 0)}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track count: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "get_track":
        index = arguments["index"]
        result = await bridge.call_lua("GetTrack", [0, index])
        
        if result.get("ok"):
            track_ptr = result.get("ret")
            if track_ptr:
                return [TextContent(
                    type="text",
                    text=json.dumps({"track": track_ptr})
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
    
    elif name == "get_track_name":
        track = arguments.get("track")
        if isinstance(track, str):
            track = json.loads(track)
        
        if isinstance(track, dict) and "track" in track:
            track_ptr = track["track"]
        else:
            track_ptr = track
        
        result = await bridge.call_lua("GetTrackName", [track_ptr])
        
        if result.get("ok"):
            ret = result.get("ret", [])
            if isinstance(ret, list) and len(ret) >= 2:
                return [TextContent(
                    type="text",
                    text=f"Track name: {ret[1]}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="Failed to get track name: Invalid response"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track name: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_name":
        track = arguments.get("track")
        new_name = arguments.get("name")
        
        if isinstance(track, str):
            track = json.loads(track)
        
        if isinstance(track, dict) and "track" in track:
            track_ptr = track["track"]
        else:
            track_ptr = track
        
        result = await bridge.call_lua("GetSetMediaTrackInfo_String", [track_ptr, "P_NAME", new_name, True])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully set track name to: {new_name}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track name: {result.get('error', 'Unknown error')}"
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