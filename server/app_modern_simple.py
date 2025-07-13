#!/usr/bin/env python3
"""
REAPER MCP Server - Modern Pattern with @mcp.tool decorators
Simplified version that works with current MCP 1.11.0
"""

import os
import json
import asyncio
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

# MCP imports - try different import patterns
try:
    # Try modern FastMCP import
    from mcp.server.fastmcp import FastMCP
    FASTMCP_AVAILABLE = True
except ImportError:
    try:
        # Try alternative import
        from mcp.fastmcp import FastMCP
        FASTMCP_AVAILABLE = True
    except ImportError:
        # FastMCP not available, fall back to manual registration
        FASTMCP_AVAILABLE = False
        from mcp import Tool
        from mcp.types import TextContent
        from mcp.server import Server

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bridge setup (reuse existing bridge logic)
BRIDGE_DIR = Path(os.environ.get(
    'REAPER_MCP_BRIDGE_DIR',
    os.path.expanduser('~/Library/Application Support/REAPER/Scripts/mcp_bridge_data')
))
BRIDGE_DIR.mkdir(parents=True, exist_ok=True)

class ReaperFileBridge:
    """File-based bridge for communicating with REAPER"""
    
    def __init__(self):
        self.bridge_dir = BRIDGE_DIR
        self.request_id = 0
        
    async def call_lua(self, func_name: str, args: Optional[List[Any]] = None) -> Dict[str, Any]:
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
            start_time = asyncio.get_event_loop().time()
            timeout = 5.0  # 5 second timeout
            
            while asyncio.get_event_loop().time() - start_time < timeout:
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
            request_file.unlink(missing_ok=True)
            logger.error("Timeout waiting for REAPER response")
            return {"ok": False, "error": "Timeout waiting for REAPER response"}
            
        except Exception as e:
            logger.error(f"Bridge error: {e}")
            return {"ok": False, "error": str(e)}

# Initialize bridge and MCP server
bridge = ReaperFileBridge()

if FASTMCP_AVAILABLE:
    mcp = FastMCP("reaper-mcp-modern")
else:
    # Fall back to manual server creation
    logger.warning("FastMCP not available, using manual tool registration")
    mcp = Server("reaper-mcp-modern")
    tools_list = []

# ============================================================================
# Track Management Tools
# ============================================================================

@mcp.tool()
async def insert_track(index: int, use_defaults: bool = True) -> str:
    """Insert a new track at the specified index (0-based)"""
    result = await bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
    
    if result.get("ok"):
        return f"Successfully inserted track at index {index}"
    else:
        raise Exception(f"Failed to insert track: {result.get('error', 'Unknown error')}")

@mcp.tool()
async def get_track_count() -> str:
    """Get the number of tracks in the current project"""
    result = await bridge.call_lua("CountTracks", [0])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Current project has {count} tracks"
    else:
        raise Exception(f"Failed to get track count: {result.get('error', 'Unknown error')}")

@mcp.tool()
async def delete_track(track_index: int) -> str:
    """Delete a track by index (0-based)"""
    # Get track count first
    count_result = await bridge.call_lua("CountTracks", [0])
    if not count_result.get("ok"):
        raise Exception("Failed to get track count")
    
    track_count = count_result.get("ret", 0)
    if track_index >= track_count:
        raise ValueError(f"Track index {track_index} out of range. Project has {track_count} tracks.")
    
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Delete it
    delete_result = await bridge.call_lua("DeleteTrack", [track_result.get("ret")])
    if not delete_result.get("ok"):
        raise Exception(f"Failed to delete track: {delete_result.get('error', 'Unknown error')}")
    
    return f"Successfully deleted track at index {track_index}"

@mcp.tool()
async def get_track_name(track_index: int) -> str:
    """Get the name of a track by index (0-based)"""
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get its name
    name_result = await bridge.call_lua("GetTrackName", [track_result.get("ret")])
    if name_result.get("ok"):
        name = name_result.get("ret", "")
        if name:
            return f"Track {track_index} name: {name}"
        else:
            return f"Track {track_index} has no name"
    else:
        raise Exception("Failed to get track name")

@mcp.tool()
async def set_track_name(track_index: int, name: str) -> str:
    """Set the name of a track"""
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set its name
    set_result = await bridge.call_lua("GetSetMediaTrackInfo_String", 
                                     [track_result.get("ret"), "P_NAME", name, True])
    if set_result.get("ok"):
        return f"Set track {track_index} name to: {name}"
    else:
        raise Exception("Failed to set track name")

# ============================================================================
# Track Properties Tools
# ============================================================================

@mcp.tool()
async def get_track_mute(track_index: int) -> str:
    """Get the mute state of a track"""
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Get mute state
    mute_result = await bridge.call_lua("GetMediaTrackInfo_Value", 
                                      [track_result.get("ret"), "B_MUTE"])
    if mute_result.get("ok"):
        is_muted = bool(mute_result.get("ret", 0))
        return f"Track {track_index} is {'muted' if is_muted else 'not muted'}"
    else:
        raise Exception("Failed to get track mute state")

@mcp.tool()
async def set_track_mute(track_index: int, mute: bool) -> str:
    """Set the mute state of a track"""
    # Get the track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set mute state
    mute_result = await bridge.call_lua("SetMediaTrackInfo_Value",
                                      [track_result.get("ret"), "B_MUTE", 1 if mute else 0])
    if mute_result.get("ok"):
        return f"Track {track_index} {'muted' if mute else 'unmuted'}"
    else:
        raise Exception("Failed to set track mute state")

# ============================================================================
# Core API Functions
# ============================================================================

@mcp.tool()
async def api_exists(function_name: str) -> str:
    """Check if a ReaScript API function exists"""
    result = await bridge.call_lua("APIExists", [function_name])
    
    if result.get("ok"):
        exists = result.get("ret", False)
        return f"API function '{function_name}' {'exists' if exists else 'does not exist'}"
    else:
        raise Exception(f"Failed to check API function: {result.get('error', 'Unknown error')}")

@mcp.tool()
async def db_to_slider(db: float) -> str:
    """Convert dB value to slider value (0.0 to 1.0)"""
    result = await bridge.call_lua("DB2SLIDER", [db])
    
    if result.get("ok") and result.get("ret") is not None:
        return f"{db} dB = {result.get('ret'):.4f} (slider value)"
    else:
        raise Exception("Failed to convert dB to slider")

@mcp.tool()
async def slider_to_db(slider: float) -> str:
    """Convert slider value (0.0 to 1.0) to dB value"""
    result = await bridge.call_lua("SLIDER2DB", [slider])
    
    if result.get("ok") and result.get("ret") is not None:
        return f"{slider} (slider) = {result.get('ret'):.2f} dB"
    else:
        raise Exception("Failed to convert slider to dB")

# ============================================================================
# Main entry point
# ============================================================================

async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting REAPER MCP Server (Modern Pattern)")
    logger.info(f"Bridge directory: {BRIDGE_DIR}")
    logger.info("Make sure to run mcp_bridge_no_socket.lua in REAPER!")
    
    async with stdio_server() as (read_stream, write_stream):
        # Initialize options for the server
        init_options = mcp.create_initialization_options()
        # Run the server
        await mcp.run(read_stream, write_stream, init_options)

if __name__ == "__main__":
    asyncio.run(main())