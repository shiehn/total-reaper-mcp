#!/usr/bin/env python3
"""
REAPER MCP Server - File-based Bridge with Object Registry Support
This version works with the Lua bridge that maintains object handles
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
    # Same tool list as before
    from server.app_file_bridge_full import list_tools as full_list_tools
    return await full_list_tools()

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
            track_ref = result.get("ret")
            if track_ref:
                # With registry, we get a handle object
                if isinstance(track_ref, dict) and "__handle" in track_ref:
                    return [TextContent(
                        type="text",
                        text=f"Track at index {index}: {track_ref['__handle']}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Track at index {index}: {track_ref}"
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
        
        # Just pass the index - the bridge will handle it
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
            master_ref = result.get("ret")
            if isinstance(master_ref, dict) and "__handle" in master_ref:
                return [TextContent(
                    type="text",
                    text=f"Master track: {master_ref['__handle']}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Master track: {master_ref}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get master track: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "delete_track":
        track_index = arguments["track_index"]
        
        # The registry bridge can handle deletion by index
        result = await bridge.call_lua("DeleteTrackByIndex", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully deleted track at index {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=result.get('error', 'Failed to delete track')
            )]
    
    elif name == "get_track_mute":
        track_index = arguments["track_index"]
        
        # First get the track handle
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        # Use the handle for the next call
        track_handle = track_result.get("ret")
        result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_handle, "B_MUTE"])
        
        if result.get("ok"):
            is_muted = bool(result.get("ret", 0))
            state = "muted" if is_muted else "unmuted"
            return [TextContent(
                type="text",
                text=f"Track {track_index} is {state}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track mute state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_mute":
        track_index = arguments["track_index"]
        mute = arguments["mute"]
        
        # Get track handle first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_handle, "B_MUTE", 1 if mute else 0])
        
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
        
        # Get track handle first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        result = await bridge.call_lua("GetMediaTrackInfo_Value", [track_handle, "I_SOLO"])
        
        if result.get("ok"):
            solo_state = int(result.get("ret", 0))
            if solo_state == 0:
                state = "not soloed"
            elif solo_state == 1:
                state = "soloed"
            else:
                state = "soloed in place"
            return [TextContent(
                type="text",
                text=f"Track {track_index} solo state: {state}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track solo state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_track_solo":
        track_index = arguments["track_index"]
        solo = arguments["solo"]
        
        # Get track handle first
        track_result = await bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        track_handle = track_result.get("ret")
        result = await bridge.call_lua("SetMediaTrackInfo_Value", [track_handle, "I_SOLO", 1 if solo else 0])
        
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
    
    elif name == "get_play_state":
        result = await bridge.call_lua("GetPlayState")
        
        if result.get("ok"):
            state = result.get("ret", 0)
            if state == 0:
                state_text = "stopped"
            elif state == 1:
                state_text = "playing"
            elif state == 2:
                state_text = "paused"
            elif state == 4:
                state_text = "recording"
            elif state == 5:
                state_text = "recording and playing"
            elif state == 6:
                state_text = "recording and paused"
            else:
                state_text = f"unknown state ({state})"
            
            return [TextContent(
                type="text",
                text=f"playback state: {state}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get play state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_play_state":
        play = arguments.get("play", False)
        pause = arguments.get("pause", False)
        record = arguments.get("record", False)
        
        result = await bridge.call_lua("SetPlayState", [play, pause, record])
        
        if result.get("ok"):
            if record and play:
                state_text = "play+record"
            elif record:
                state_text = "record"
            elif play:
                state_text = "play"
            elif pause:
                state_text = "pause"
            else:
                state_text = "stopped"
            
            return [TextContent(
                type="text",
                text=f"Transport state set to: {state_text}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set play state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_repeat_state":
        enabled = arguments["repeat"]
        
        result = await bridge.call_lua("GetSetRepeat", [enabled])
        
        if result.get("ok"):
            prev_state = result.get("ret", 0)
            state = "enabled" if enabled else "disabled"
            return [TextContent(
                type="text",
                text=f"Repeat/loop {state}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set repeat state: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "execute_action":
        action_id = arguments["command_id"]
        
        result = await bridge.call_lua("Main_OnCommand", [action_id, 0])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully executed action {action_id}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to execute action: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "add_project_marker":
        position = arguments["position"]
        name = arguments["name"]
        is_region = arguments.get("is_region", False)
        region_end = arguments.get("region_end", position)
        color = arguments.get("color", -1)
        
        result = await bridge.call_lua("AddProjectMarker", [0, is_region, position, region_end, name, -1])
        
        if result.get("ok"):
            marker_type = "region" if is_region else "marker"
            return [TextContent(
                type="text",
                text=f"Successfully added {marker_type} '{name}' at position {position}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add marker: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "set_loop_time_range":
        start_time = arguments["start"]
        end_time = arguments["end"]
        is_loop = arguments.get("is_loop", True)
        
        result = await bridge.call_lua("GetSet_LoopTimeRange", [True, is_loop, start_time, end_time, False])
        
        if result.get("ok"):
            range_type = "loop" if is_loop else "time selection"
            return [TextContent(
                type="text",
                text=f"Successfully set {range_type} from {start_time:.3f}s to {end_time:.3f}s"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set time selection: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "play":
        result = await bridge.call_lua("Main_OnCommand", [1007, 0])  # Play command
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Successfully executed play"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to execute play command: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "stop":
        result = await bridge.call_lua("Main_OnCommand", [1016, 0])  # Stop command
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Successfully executed stop"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to execute stop command: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "pause":
        result = await bridge.call_lua("Main_OnCommand", [1008, 0])  # Pause command
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Successfully executed pause"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to execute pause command: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "record":
        result = await bridge.call_lua("Main_OnCommand", [1013, 0])  # Record command
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Successfully started recording"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to execute record command: {result.get('error', 'Unknown error')}"
            )]
    
    elif name == "count_project_markers":
        # Import from full implementation - complex response handling
        from server.app_file_bridge_full import call_tool as full_call_tool
        return await full_call_tool(name, arguments)
    
    elif name == "enum_project_markers":
        # Import from full implementation - complex response handling  
        from server.app_file_bridge_full import call_tool as full_call_tool
        return await full_call_tool(name, arguments)
    
    elif name == "delete_project_marker":
        # Import from full implementation - needs specific handling
        from server.app_file_bridge_full import call_tool as full_call_tool
        return await full_call_tool(name, arguments)
    
    elif name == "get_loop_time_range":
        # Import from full implementation - complex response
        from server.app_file_bridge_full import call_tool as full_call_tool
        return await full_call_tool(name, arguments)
    
    else:
        # Import the full implementation for other tools
        from server.app_file_bridge_full import call_tool as full_call_tool
        return await full_call_tool(name, arguments)

async def amain():
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting REAPER MCP Server (File-based Bridge with Registry)...")
    logger.info(f"Bridge directory: {BRIDGE_DIR}")
    logger.info("Make sure to run mcp_bridge_with_registry.lua in REAPER!")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

def main():
    import sys
    asyncio.run(amain())

if __name__ == "__main__":
    main()