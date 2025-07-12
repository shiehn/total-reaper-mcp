#!/usr/bin/env python3
"""
Comprehensive batch implementation script for ReaScript methods
This generates code for a large number of methods at once
"""

# Define all methods to implement
all_methods = [
    # Track Volume/Pan
    {
        "name": "get_track_volume",
        "description": "Get track volume in dB",
        "params": [{"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0}],
        "lua_func": "GetTrackVolume",
        "lua_args": "[track_index]",
        "response": 'f"Track {track_index} volume: {result.get(\'ret\')} dB"',
        "error_check": "track"
    },
    {
        "name": "set_track_volume",
        "description": "Set track volume in dB",
        "params": [
            {"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0},
            {"name": "volume", "type": "number", "desc": "Volume in dB (typically -150 to +12)"}
        ],
        "lua_func": "SetTrackVolume",
        "lua_args": "[track_index, volume]",
        "response": 'f"Track {track_index} volume set to {volume} dB"',
        "error_check": "track"
    },
    {
        "name": "get_track_pan",
        "description": "Get track pan position",
        "params": [{"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0}],
        "lua_func": "GetTrackPan",
        "lua_args": "[track_index]",
        "response": 'f"Track {track_index} pan: {result.get(\'ret\')} (-1=left, 0=center, 1=right)"',
        "error_check": "track"
    },
    {
        "name": "set_track_pan",
        "description": "Set track pan position",
        "params": [
            {"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0},
            {"name": "pan", "type": "number", "desc": "Pan position (-1=left, 0=center, 1=right)"}
        ],
        "lua_func": "SetTrackPan",
        "lua_args": "[track_index, pan]",
        "response": 'f"Track {track_index} pan set to {pan}"',
        "error_check": "track"
    },
    # Media Items
    {
        "name": "add_media_item_to_track",
        "description": "Add a new media item to a track",
        "params": [{"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0}],
        "lua_func": "AddMediaItemToTrack",
        "lua_args": "[track_index]",
        "response": 'f"Media item added to track {track_index}"',
        "error_check": "track"
    },
    {
        "name": "count_media_items",
        "description": "Count total media items in project",
        "params": [],
        "lua_func": "CountMediaItems",
        "lua_args": "[0]",
        "response": 'f"Total media items: {result.get(\'ret\')}"',
        "error_check": None
    },
    {
        "name": "get_media_item",
        "description": "Get media item by index",
        "params": [{"name": "item_index", "type": "integer", "desc": "The media item index (0-based)", "min": 0}],
        "lua_func": "GetMediaItem",
        "lua_args": "[0, item_index]",
        "response": 'f"Media item {item_index}: {result.get(\'ret\')}"',
        "error_check": None
    },
    # Project Info
    {
        "name": "get_project_name",
        "description": "Get the current project name",
        "params": [],
        "lua_func": "GetProjectName",
        "lua_args": "[0]",
        "response": 'f"Project name: {result.get(\'ret\', \'Untitled\')}"',
        "error_check": None
    },
    {
        "name": "get_project_path",
        "description": "Get the current project path",
        "params": [],
        "lua_func": "GetProjectPath",
        "lua_args": "[0]",
        "response": 'f"Project path: {result.get(\'ret\', \'Not saved\')}"',
        "error_check": None
    },
    {
        "name": "save_project",
        "description": "Save the current project",
        "params": [{"name": "force_save_as", "type": "boolean", "desc": "Force 'Save As' dialog"}],
        "lua_func": "Main_SaveProject",
        "lua_args": "[0, force_save_as]",
        "response": '"Project saved successfully"',
        "error_check": None
    },
    # Transport/Playback
    {
        "name": "get_cursor_position",
        "description": "Get the edit cursor position in seconds",
        "params": [],
        "lua_func": "GetCursorPosition",
        "lua_args": "[]",
        "response": 'f"Cursor position: {result.get(\'ret\')} seconds"',
        "error_check": None
    },
    {
        "name": "set_cursor_position",
        "description": "Set the edit cursor position",
        "params": [
            {"name": "time", "type": "number", "desc": "Time in seconds"},
            {"name": "move_view", "type": "boolean", "desc": "Move view to cursor"},
            {"name": "seek_play", "type": "boolean", "desc": "Seek playback to cursor"}
        ],
        "lua_func": "SetEditCurPos",
        "lua_args": "[time, move_view, seek_play]",
        "response": 'f"Cursor moved to {time} seconds"',
        "error_check": None
    },
    {
        "name": "get_play_state",
        "description": "Get current playback state",
        "params": [],
        "lua_func": "GetPlayState",
        "lua_args": "[]",
        "response": 'f"Play state: {[\'stopped\', \'playing\', \'paused\', \'recording\', \'record paused\'][result.get(\'ret\', 0)] if result.get(\'ret\', 0) < 5 else \'unknown\'}"',
        "error_check": None
    },
    {
        "name": "play",
        "description": "Start playback",
        "params": [],
        "lua_func": "CSurf_OnPlay",
        "lua_args": "[]",
        "response": '"Playback started"',
        "error_check": None
    },
    {
        "name": "stop",
        "description": "Stop playback",
        "params": [],
        "lua_func": "CSurf_OnStop",
        "lua_args": "[]",
        "response": '"Playback stopped"',
        "error_check": None
    },
    {
        "name": "pause",
        "description": "Pause playback",
        "params": [],
        "lua_func": "CSurf_OnPause",
        "lua_args": "[]",
        "response": '"Playback paused"',
        "error_check": None
    },
    # Actions
    {
        "name": "run_action",
        "description": "Execute a REAPER action by command ID",
        "params": [
            {"name": "command_id", "type": "integer", "desc": "The action command ID"},
            {"name": "flag", "type": "integer", "desc": "Flag (0 for normal)", "default": 0}
        ],
        "lua_func": "Main_OnCommand",
        "lua_args": "[command_id, flag or 0]",
        "response": 'f"Action {command_id} executed"',
        "error_check": None
    },
    # Undo
    {
        "name": "undo_begin_block",
        "description": "Begin an undo block",
        "params": [],
        "lua_func": "Undo_BeginBlock",
        "lua_args": "[]",
        "response": '"Undo block started"',
        "error_check": None
    },
    {
        "name": "undo_end_block",
        "description": "End an undo block",
        "params": [
            {"name": "description", "type": "string", "desc": "Description for undo history"},
            {"name": "flags", "type": "integer", "desc": "Flags (-1 for all)", "default": -1}
        ],
        "lua_func": "Undo_EndBlock",
        "lua_args": "[description, flags or -1]",
        "response": 'f"Undo block ended: {description}"',
        "error_check": None
    },
    # UI Updates
    {
        "name": "update_arrange",
        "description": "Update the arrange view",
        "params": [],
        "lua_func": "UpdateArrange",
        "lua_args": "[]",
        "response": '"Arrange view updated"',
        "error_check": None
    },
    {
        "name": "update_timeline",
        "description": "Update the timeline display",
        "params": [],
        "lua_func": "UpdateTimeline",
        "lua_args": "[]",
        "response": '"Timeline updated"',
        "error_check": None
    }
]

# Generate everything
import json

def generate_lua_handler(method):
    """Generate Lua handler code for a method"""
    handler = f'            elseif fname == "{method["lua_func"]}" then\n'
    
    if method["params"]:
        handler += f'                if #args >= {len([p for p in method["params"] if "default" not in p])} then\n'
    
    # Implementation based on method
    if method["lua_func"] == "GetTrackVolume":
        handler += '                    local track = reaper.GetTrack(0, args[1])\n'
        handler += '                    if track then\n'
        handler += '                        local vol = reaper.GetMediaTrackInfo_Value(track, "D_VOL")\n'
        handler += '                        local db = 20 * math.log(vol) / math.log(10)\n'
        handler += '                        response.ok = true\n'
        handler += '                        response.ret = db\n'
        handler += '                    else\n'
        handler += '                        response.error = "Track not found at index " .. tostring(args[1])\n'
        handler += '                    end\n'
    elif method["lua_func"] == "SetTrackVolume":
        handler += '                    local track = reaper.GetTrack(0, args[1])\n'
        handler += '                    if track then\n'
        handler += '                        local vol = 10^(args[2]/20)\n'
        handler += '                        reaper.SetMediaTrackInfo_Value(track, "D_VOL", vol)\n'
        handler += '                        response.ok = true\n'
        handler += '                    else\n'
        handler += '                        response.error = "Track not found at index " .. tostring(args[1])\n'
        handler += '                    end\n'
    elif method["lua_func"] == "GetTrackPan":
        handler += '                    local track = reaper.GetTrack(0, args[1])\n'
        handler += '                    if track then\n'
        handler += '                        local pan = reaper.GetMediaTrackInfo_Value(track, "D_PAN")\n'
        handler += '                        response.ok = true\n'
        handler += '                        response.ret = pan\n'
        handler += '                    else\n'
        handler += '                        response.error = "Track not found at index " .. tostring(args[1])\n'
        handler += '                    end\n'
    elif method["lua_func"] == "SetTrackPan":
        handler += '                    local track = reaper.GetTrack(0, args[1])\n'
        handler += '                    if track then\n'
        handler += '                        reaper.SetMediaTrackInfo_Value(track, "D_PAN", args[2])\n'
        handler += '                        response.ok = true\n'
        handler += '                    else\n'
        handler += '                        response.error = "Track not found at index " .. tostring(args[1])\n'
        handler += '                    end\n'
    elif method["lua_func"] == "AddMediaItemToTrack":
        handler += '                    local track = reaper.GetTrack(0, args[1])\n'
        handler += '                    if track then\n'
        handler += '                        local item = reaper.AddMediaItemToTrack(track)\n'
        handler += '                        response.ok = true\n'
        handler += '                        response.ret = item\n'
        handler += '                    else\n'
        handler += '                        response.error = "Track not found at index " .. tostring(args[1])\n'
        handler += '                    end\n'
    elif method["lua_func"] == "CountMediaItems":
        handler += '                    local count = reaper.CountMediaItems(0)\n'
        handler += '                    response.ok = true\n'
        handler += '                    response.ret = count\n'
    elif method["lua_func"] == "GetMediaItem":
        handler += '                    local item = reaper.GetMediaItem(0, args[1])\n'
        handler += '                    response.ok = true\n'
        handler += '                    response.ret = item\n'
    elif method["lua_func"] == "GetProjectName":
        handler += '                    local ret, name = reaper.GetProjectName(0, "")\n'
        handler += '                    response.ok = true\n'
        handler += '                    response.ret = name\n'
    elif method["lua_func"] == "GetProjectPath":
        handler += '                    local path = reaper.GetProjectPath()\n'
        handler += '                    response.ok = true\n'
        handler += '                    response.ret = path\n'
    elif method["lua_func"] == "Main_SaveProject":
        handler += '                    reaper.Main_SaveProject(0, args[1])\n'
        handler += '                    response.ok = true\n'
    elif method["lua_func"] == "GetCursorPosition":
        handler += '                    local pos = reaper.GetCursorPosition()\n'
        handler += '                    response.ok = true\n'
        handler += '                    response.ret = pos\n'
    elif method["lua_func"] == "SetEditCurPos":
        handler += '                    reaper.SetEditCurPos(args[1], args[2], args[3])\n'
        handler += '                    response.ok = true\n'
    elif method["lua_func"] == "GetPlayState":
        handler += '                    local state = reaper.GetPlayState()\n'
        handler += '                    response.ok = true\n'
        handler += '                    response.ret = state\n'
    elif method["lua_func"] in ["CSurf_OnPlay", "CSurf_OnStop", "CSurf_OnPause"]:
        handler += f'                    reaper.{method["lua_func"]}()\n'
        handler += '                    response.ok = true\n'
    elif method["lua_func"] == "Main_OnCommand":
        handler += '                    reaper.Main_OnCommand(args[1], args[2] or 0)\n'
        handler += '                    response.ok = true\n'
    elif method["lua_func"] == "Undo_BeginBlock":
        handler += '                    reaper.Undo_BeginBlock()\n'
        handler += '                    response.ok = true\n'
    elif method["lua_func"] == "Undo_EndBlock":
        handler += '                    reaper.Undo_EndBlock(args[1], args[2] or -1)\n'
        handler += '                    response.ok = true\n'
    elif method["lua_func"] in ["UpdateArrange", "UpdateTimeline"]:
        handler += f'                    reaper.{method["lua_func"]}()\n'
        handler += '                    response.ok = true\n'
    
    if method["params"]:
        handler += '                else\n'
        handler += f'                    response.error = "{method["lua_func"]} requires {len([p for p in method["params"] if "default" not in p])} argument(s)"\n'
        handler += '                end\n'
    
    return handler

output = {
    "tools": [],
    "handlers": [],
    "lua_handlers": []
}

# Generate tool definitions
for method in all_methods:
    tool_def = f'''Tool(
            name="{method["name"]}",
            description="{method["description"]}",
            inputSchema={{
                "type": "object",'''
    
    if method["params"]:
        tool_def += f'''
                "properties": {{'''
        for i, param in enumerate(method["params"]):
            tool_def += f'''
                    "{param["name"]}": {{
                        "type": "{param["type"]}",
                        "description": "{param["desc"]}"'''
            if param.get("min") is not None:
                tool_def += f',\n                        "minimum": {param["min"]}'
            if param.get("default") is not None:
                tool_def += f',\n                        "default": {json.dumps(param["default"])}'
            tool_def += f'''
                    }}'''
            if i < len(method["params"]) - 1:
                tool_def += ','
        
        required_params = [p["name"] for p in method["params"] if "default" not in p]
        tool_def += f'''
                }},
                "required": {json.dumps(required_params)}'''
    else:
        tool_def += f'''
                "properties": {{}}'''
    
    tool_def += f'''
            }}
        )'''
    
    output["tools"].append(tool_def)

# Generate handlers
for method in all_methods:
    handler = f'    elif name == "{method["name"]}":\n'
    
    # Extract arguments
    for param in method["params"]:
        if "default" in param:
            handler += f'        {param["name"]} = arguments.get("{param["name"]}", {json.dumps(param["default"])})\n'
        else:
            handler += f'        {param["name"]} = arguments["{param["name"]}"]\n'
    
    if method["params"]:
        handler += '        \n'
    
    # Add error check if needed
    if method["error_check"] == "track":
        handler += f'        # First check if track exists\n'
        handler += f'        track_result = bridge.call_lua("GetTrack", [0, track_index])\n'
        handler += f'        if not track_result.get("ok") or not track_result.get("ret"):\n'
        handler += f'            return [TextContent(\n'
        handler += f'                type="text",\n'
        handler += f'                text=f"Failed to find track at index {{track_index}}"\n'
        handler += f'            )]\n'
        handler += f'        \n'
    
    # Make the call
    handler += f'        result = bridge.call_lua("{method["lua_func"]}", {method["lua_args"]})\n'
    handler += f'        \n'
    handler += f'        if result.get("ok"):\n'
    handler += f'            return [TextContent(\n'
    handler += f'                type="text",\n'
    handler += f'                text={method["response"]}\n'
    handler += f'            )]\n'
    handler += f'        else:\n'
    handler += f'            return [TextContent(\n'
    handler += f'                type="text",\n'
    handler += f'                text=f"Failed to {method["name"].replace("_", " ")}: {{result.get(\'error\', \'Unknown error\')}}"\n'
    handler += f'            )]'
    
    output["handlers"].append(handler)

# Generate Lua handlers
for method in all_methods:
    lua_handler = generate_lua_handler(method)
    output["lua_handlers"].append(lua_handler)

# Write output
with open('batch_output_v2.txt', 'w') as f:
    f.write("# Tool definitions for app.py:\n\n")
    for tool in output["tools"]:
        f.write(tool + ",\n")
    
    f.write("\n\n# Handlers for app.py:\n\n")
    for handler in output["handlers"]:
        f.write(handler + "\n\n")
    
    f.write("\n\n# Lua handlers for mcp_bridge.lua:\n\n")
    for lua_handler in output["lua_handlers"]:
        f.write(lua_handler)

print("Generated batch_output_v2.txt with all implementations")