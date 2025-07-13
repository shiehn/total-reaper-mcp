#!/usr/bin/env python3
"""
REAPER MCP Server - Modern Modular Pattern

This is the main server file that uses the modern @mcp.tool() decorator pattern
with a modular structure for better organization and maintainability.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# MCP imports
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server

# Import bridge
from bridge import bridge, BRIDGE_DIR

# Import tool modules
from tools import track_basic

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("reaper-mcp-modern")

# ============================================================================
# Register Track Basic Tools
# ============================================================================

@mcp.tool()
async def insert_track(index: int, use_defaults: bool = True) -> str:
    """Insert a new track at the specified index (0-based)"""
    return await track_basic.insert_track(index, use_defaults)

@mcp.tool()
async def get_track_count() -> str:
    """Get the number of tracks in the current project"""
    return await track_basic.get_track_count()

@mcp.tool()
async def get_track(track_index: int) -> str:
    """Get a track by index from the current project"""
    return await track_basic.get_track(track_index)

@mcp.tool()
async def delete_track(track_index: int) -> str:
    """Delete a track by index"""
    return await track_basic.delete_track(track_index)

@mcp.tool()
async def get_master_track() -> str:
    """Get the master track"""
    return await track_basic.get_master_track()

@mcp.tool()
async def get_track_guid(track_index: int) -> str:
    """Get the GUID of a track"""
    return await track_basic.get_track_guid(track_index)

@mcp.tool()
async def get_last_touched_track() -> str:
    """Get the last touched track"""
    return await track_basic.get_last_touched_track()

# ============================================================================
# Track Properties (inline for demonstration)
# ============================================================================

@mcp.tool()
async def get_track_name(track_index: int) -> str:
    """Get the name of a track by index (0-based)"""
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
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
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
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

@mcp.tool()
async def get_track_mute(track_index: int) -> str:
    """Get track mute state"""
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
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
    """Set track mute state"""
    # Get the track
    if track_index == -1:
        track_result = await bridge.call_lua("GetMasterTrack", [0])
    else:
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
# Time/Tempo Functions
# ============================================================================

@mcp.tool()
async def time_map_qn_to_time(qn: float) -> str:
    """Convert quarter note position to time in seconds"""
    result = await bridge.call_lua("TimeMap2_QNToTime", [0, qn])
    
    if result.get("ok") and result.get("ret") is not None:
        return f"Quarter note {qn} = {result.get('ret'):.3f} seconds"
    else:
        raise Exception("Failed to convert QN to time")

@mcp.tool()
async def time_map_time_to_qn(time: float) -> str:
    """Convert time in seconds to quarter note position"""
    result = await bridge.call_lua("TimeMap2_timeToQN", [0, time])
    
    if result.get("ok") and result.get("ret") is not None:
        return f"{time} seconds = {result.get('ret'):.3f} quarter notes"
    else:
        raise Exception("Failed to convert time to QN")

# ============================================================================
# Main entry point
# ============================================================================

async def main():
    """Run the MCP server"""
    logger.info("Starting REAPER MCP Server (Modern Modular Pattern)")
    logger.info(f"Bridge directory: {BRIDGE_DIR}")
    logger.info("Make sure to run mcp_bridge_no_socket.lua in REAPER!")
    
    async with stdio_server() as (read_stream, write_stream):
        # Initialize options for the server
        init_options = mcp.create_initialization_options()
        # Run the server
        await mcp.run(read_stream, write_stream, init_options)

if __name__ == "__main__":
    asyncio.run(main())