#!/usr/bin/env python3
"""
Batch implementation script for ReaScript methods
This generates the code for multiple methods at once
"""

# Track methods to implement
track_methods = [
    {
        "name": "get_master_track",
        "description": "Get the master track",
        "params": [],
        "lua_func": "GetMasterTrack",
        "lua_args": "[0]",
        "response": 'f"Master track: {result.get(\'ret\')}"',
        "error_check": None
    },
    {
        "name": "delete_track", 
        "description": "Delete a track by index",
        "params": [{"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0}],
        "lua_func": "DeleteTrack",
        "lua_args": "[track_index]",
        "response": 'f"Track {track_index} deleted successfully"',
        "error_check": "track"
    },
    {
        "name": "get_track_mute",
        "description": "Get track mute state",
        "params": [{"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0}],
        "lua_func": "GetTrackMute",
        "lua_args": "[track_index]",
        "response": 'f"Track {track_index} mute state: {\'muted\' if result.get(\'ret\') else \'unmuted\'}"',
        "error_check": "track"
    },
    {
        "name": "set_track_mute",
        "description": "Set track mute state",
        "params": [
            {"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0},
            {"name": "mute", "type": "boolean", "desc": "Whether to mute (true) or unmute (false) the track"}
        ],
        "lua_func": "SetTrackMute",
        "lua_args": "[track_index, mute]",
        "response": 'f"Track {track_index} {\'muted\' if mute else \'unmuted\'}"',
        "error_check": "track"
    },
    {
        "name": "get_track_solo",
        "description": "Get track solo state",
        "params": [{"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0}],
        "lua_func": "GetTrackSolo",
        "lua_args": "[track_index]",
        "response": 'f"Track {track_index} solo state: {\'soloed\' if result.get(\'ret\') else \'not soloed\'}"',
        "error_check": "track"
    },
    {
        "name": "set_track_solo",
        "description": "Set track solo state",
        "params": [
            {"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0},
            {"name": "solo", "type": "boolean", "desc": "Whether to solo (true) or unsolo (false) the track"}
        ],
        "lua_func": "SetTrackSolo",
        "lua_args": "[track_index, solo]",
        "response": 'f"Track {track_index} {\'soloed\' if solo else \'unsoloed\'}"',
        "error_check": "track"
    }
]

# Generate tool definitions
print("# Tool definitions for app.py:")
print()
for method in track_methods:
    print(f'        Tool(')
    print(f'            name="{method["name"]}",')
    print(f'            description="{method["description"]}",')
    print(f'            inputSchema={{')
    print(f'                "type": "object",')
    if method["params"]:
        print(f'                "properties": {{')
        for i, param in enumerate(method["params"]):
            print(f'                    "{param["name"]}": {{')
            print(f'                        "type": "{param["type"]}",')
            print(f'                        "description": "{param["desc"]}"', end='')
            if param.get("min") is not None:
                print(f',')
                print(f'                        "minimum": {param["min"]}', end='')
            print(f'')
            print(f'                    }}', end='')
            if i < len(method["params"]) - 1:
                print(',')
            else:
                print()
        print(f'                }},')
        print(f'                "required": {[p["name"] for p in method["params"]]}')
    else:
        print(f'                "properties": {{}}')
    print(f'            }}')
    print(f'        ),')
print()

# Generate call_tool handlers
print("# Call tool handlers for app.py:")
print()
for method in track_methods:
    print(f'    elif name == "{method["name"]}":')
    for param in method["params"]:
        print(f'        {param["name"]} = arguments["{param["name"]}"]')
    print(f'        ')
    if method["error_check"] == "track":
        print(f'        # First check if track exists')
        print(f'        track_result = bridge.call_lua("GetTrack", [0, track_index])')
        print(f'        if not track_result.get("ok") or not track_result.get("ret"):')
        print(f'            return [TextContent(')
        print(f'                type="text",')
        print(f'                text=f"Failed to find track at index {{track_index}}"')
        print(f'            )]')
        print(f'        ')
    args_str = ", ".join([param["name"] for param in method["params"]])
    print(f'        result = bridge.call_lua("{method["lua_func"]}", {method["lua_args"]})')
    print(f'        ')
    print(f'        if result.get("ok"):')
    print(f'            return [TextContent(')
    print(f'                type="text",')
    print(f'                text={method["response"]}')
    print(f'            )]')
    print(f'        else:')
    print(f'            return [TextContent(')
    print(f'                type="text",')
    print(f'                text=f"Failed to {method["name"].replace("_", " ")}: {{result.get(\'error\', \'Unknown error\')}}"')
    print(f'            )]')
    print()

# Generate Lua handlers
print("# Lua handlers for mcp_bridge.lua:")
print()
for method in track_methods:
    print(f'            elseif fname == "{method["lua_func"]}" then')
    if method["params"]:
        print(f'                if #args >= {len(method["params"])} then')
        if method["error_check"] == "track":
            print(f'                    local track = reaper.GetTrack(0, args[1])')
            print(f'                    if track then')
            if method["lua_func"] == "DeleteTrack":
                print(f'                        reaper.DeleteTrack(track)')
                print(f'                        response.ok = true')
            elif method["lua_func"].startswith("GetTrack"):
                if "Mute" in method["lua_func"]:
                    print(f'                        local muted = reaper.GetMediaTrackInfo_Value(track, "B_MUTE") == 1')
                    print(f'                        response.ok = true')
                    print(f'                        response.ret = muted')
                elif "Solo" in method["lua_func"]:
                    print(f'                        local solo = reaper.GetMediaTrackInfo_Value(track, "I_SOLO") > 0')
                    print(f'                        response.ok = true')
                    print(f'                        response.ret = solo')
            elif method["lua_func"].startswith("SetTrack"):
                if "Mute" in method["lua_func"]:
                    print(f'                        reaper.SetMediaTrackInfo_Value(track, "B_MUTE", args[2] and 1 or 0)')
                    print(f'                        response.ok = true')
                elif "Solo" in method["lua_func"]:
                    print(f'                        reaper.SetMediaTrackInfo_Value(track, "I_SOLO", args[2] and 1 or 0)')
                    print(f'                        response.ok = true')
            print(f'                    else')
            print(f'                        response.error = "Track not found at index " .. tostring(args[1])')
            print(f'                    end')
        else:
            if method["lua_func"] == "GetMasterTrack":
                print(f'                    local master = reaper.GetMasterTrack(0)')
                print(f'                    response.ok = true')
                print(f'                    response.ret = master')
        print(f'                else')
        print(f'                    response.error = "{method["lua_func"]} requires {len(method["params"])} argument(s)"')
        print(f'                end')
    else:
        print(f'                local master = reaper.GetMasterTrack(0)')
        print(f'                response.ok = true')
        print(f'                response.ret = master')
    print()