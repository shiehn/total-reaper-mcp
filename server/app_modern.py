#!/usr/bin/env python3
"""
REAPER MCP Server - Modern Pattern with @mcp.tool decorators
This is a proof-of-concept showing the migration to modern MCP patterns
"""

import os
import json
import asyncio
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Union

# Modern MCP imports
from mcp.server import fastmcp
from mcp.types import TextContent

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
mcp = fastmcp.FastMCP("reaper-mcp-modern")

# ============================================================================
# Track Management Tools
# ============================================================================

@mcp.tool()
async def insert_track(
    index: int,
    use_defaults: bool = True
) -> str:
    """Insert a new track at the specified index.
    
    Args:
        index: The index where the track should be inserted (0-based)
        use_defaults: Whether to use default track settings
        
    Returns:
        Success or error message
    """
    result = await bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
    
    if result.get("ok"):
        return f"Successfully inserted track at index {index}"
    else:
        raise Exception(f"Failed to insert track: {result.get('error', 'Unknown error')}")

@mcp.tool()
async def get_track_count(ctx: Context) -> str:
    """Get the number of tracks in the current project.
    
    Args:
        ctx: MCP context
        
    Returns:
        Track count information
    """
    result = await bridge.call_lua("CountTracks", [0])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Current project has {count} tracks"
    else:
        raise Exception(f"Failed to get track count: {result.get('error', 'Unknown error')}")

@mcp.tool()
async def delete_track(track_index: int, ctx: Context) -> str:
    """Delete a track by index.
    
    Args:
        track_index: The index of the track to delete (0-based)
        ctx: MCP context
        
    Returns:
        Success or error message
    """
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
async def get_track_name(track_index: int, ctx: Context) -> str:
    """Get the name of a track.
    
    Args:
        track_index: The index of the track (0-based)
        ctx: MCP context
        
    Returns:
        Track name
    """
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
async def set_track_name(track_index: int, name: str, ctx: Context) -> str:
    """Set the name of a track.
    
    Args:
        track_index: The index of the track (0-based)
        name: The new name for the track
        ctx: MCP context
        
    Returns:
        Success message
    """
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
async def get_track_mute(track_index: int, ctx: Context) -> str:
    """Get the mute state of a track.
    
    Args:
        track_index: The index of the track (0-based)
        ctx: MCP context
        
    Returns:
        Mute state information
    """
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
async def set_track_mute(track_index: int, mute: bool, ctx: Context) -> str:
    """Set the mute state of a track.
    
    Args:
        track_index: The index of the track (0-based)
        mute: True to mute, False to unmute
        ctx: MCP context
        
    Returns:
        Success message
    """
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
async def api_exists(function_name: str, ctx: Context) -> str:
    """Check if a ReaScript API function exists.
    
    Args:
        function_name: Name of the API function to check
        ctx: MCP context
        
    Returns:
        Information about whether the function exists
    """
    result = await bridge.call_lua("APIExists", [function_name])
    
    if result.get("ok"):
        exists = result.get("ret", False)
        return f"API function '{function_name}' {'exists' if exists else 'does not exist'}"
    else:
        raise Exception(f"Failed to check API function: {result.get('error', 'Unknown error')}")

@mcp.tool()
async def db_to_slider(db: float, ctx: Context) -> str:
    """Convert dB value to slider value.
    
    Args:
        db: Value in dB
        ctx: MCP context
        
    Returns:
        Slider value
    """
    result = await bridge.call_lua("DB2SLIDER", [db])
    
    if result.get("ok") and result.get("ret") is not None:
        return f"{db} dB = {result.get('ret'):.4f} (slider value)"
    else:
        raise Exception("Failed to convert dB to slider")

@mcp.tool()
async def slider_to_db(slider: float, ctx: Context) -> str:
    """Convert slider value to dB value.
    
    Args:
        slider: Slider value (0.0 to 1.0)
        ctx: MCP context
        
    Returns:
        dB value
    """
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
        # Use the modern mcp server run method
        await mcp.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())