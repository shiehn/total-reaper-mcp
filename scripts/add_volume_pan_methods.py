#!/usr/bin/env python3
"""
Add Volume/Pan control methods to the REAPER MCP Server
"""

# Volume/Pan methods to add
VOLUME_PAN_METHODS = [
    {
        "tool_name": "get_track_volume",
        "description": "Get track volume in dB",
        "lua_func": "GetTrackVolume",
        "params": ["track_index"],
        "returns": "volume_db"
    },
    {
        "tool_name": "set_track_volume",
        "description": "Set track volume in dB",
        "lua_func": "SetTrackVolume", 
        "params": ["track_index", "volume_db"],
        "returns": None
    },
    {
        "tool_name": "get_track_pan",
        "description": "Get track pan position (-1.0 to 1.0)",
        "lua_func": "GetTrackPan",
        "params": ["track_index"],
        "returns": "pan"
    },
    {
        "tool_name": "set_track_pan",
        "description": "Set track pan position (-1.0 to 1.0)",
        "lua_func": "SetTrackPan",
        "params": ["track_index", "pan"],
        "returns": None
    }
]

def generate_tool_definitions():
    """Generate tool definitions for list_tools()"""
    tools = []
    
    for method in VOLUME_PAN_METHODS:
        tool_def = f'''        Tool(
            name="{method['tool_name']}",
            description="{method['description']}",
            inputSchema={{
                "type": "object",
                "properties": {{'''
        
        if method['tool_name'] in ['get_track_volume', 'get_track_pan']:
            tool_def += '''
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    }'''
        elif method['tool_name'] == 'set_track_volume':
            tool_def += '''
                    "track_index": {
                        "type": "integer",
                        "description": "The track index (0-based)",
                        "minimum": 0
                    },
                    "volume_db": {
                        "type": "number",
                        "description": "Volume in dB (0.0 = unity gain, -inf = mute)"
                    }'''
        elif method['tool_name'] == 'set_track_pan':
            tool_def += '''
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
                    }'''
        
        tool_def += f'''
                }},
                "required": {str([p for p in method['params']])}
            }}
        )'''
        
        tools.append(tool_def)
    
    return ',\n'.join(tools)

def generate_handlers():
    """Generate call_tool handlers"""
    handlers = []
    
    for method in VOLUME_PAN_METHODS:
        if method['tool_name'] == 'get_track_volume':
            handler = '''
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
            )]'''
            
        elif method['tool_name'] == 'set_track_volume':
            handler = '''
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
            )]'''
            
        elif method['tool_name'] == 'get_track_pan':
            handler = '''
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
            )]'''
            
        elif method['tool_name'] == 'set_track_pan':
            handler = '''
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
            )]'''
        
        handlers.append(handler)
    
    return '\n'.join(handlers)

def generate_lua_handlers():
    """Generate Lua bridge handlers"""
    handlers = []
    
    for method in VOLUME_PAN_METHODS:
        if method['tool_name'] == 'get_track_volume':
            handler = '''            elseif fname == "GetTrackVolume" then
                if #args >= 1 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local vol = reaper.GetMediaTrackInfo_Value(track, "D_VOL")
                        -- Convert linear to dB: 20 * log10(vol)
                        local vol_db = 20 * math.log(vol, 10)
                        response.ok = true
                        response.ret = vol_db
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "GetTrackVolume requires 1 argument(s)"
                end'''
                
        elif method['tool_name'] == 'set_track_volume':
            handler = '''            elseif fname == "SetTrackVolume" then
                if #args >= 2 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        -- Convert dB to linear: 10^(dB/20)
                        local vol_linear = 10^(args[2]/20)
                        reaper.SetMediaTrackInfo_Value(track, "D_VOL", vol_linear)
                        response.ok = true
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "SetTrackVolume requires 2 argument(s)"
                end'''
                
        elif method['tool_name'] == 'get_track_pan':
            handler = '''            elseif fname == "GetTrackPan" then
                if #args >= 1 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local pan = reaper.GetMediaTrackInfo_Value(track, "D_PAN")
                        response.ok = true
                        response.ret = pan
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "GetTrackPan requires 1 argument(s)"
                end'''
                
        elif method['tool_name'] == 'set_track_pan':
            handler = '''            elseif fname == "SetTrackPan" then
                if #args >= 2 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        reaper.SetMediaTrackInfo_Value(track, "D_PAN", args[2])
                        response.ok = true
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "SetTrackPan requires 2 argument(s)"
                end'''
        
        handlers.append(handler)
    
    return '\n'.join(handlers)

if __name__ == "__main__":
    print("=== Volume/Pan Methods Implementation ===\n")
    
    print("1. Add these tool definitions to @app.list_tools() in server/app.py:")
    print("=" * 60)
    print(generate_tool_definitions())
    
    print("\n\n2. Add these handlers to @app.call_tool() in server/app.py:")
    print("=" * 60)
    print(generate_handlers())
    
    print("\n\n3. Add these handlers to lua/mcp_bridge.lua (before the 'else' clause):")
    print("=" * 60)
    print(generate_lua_handlers())
    
    print("\n\nDone! Remember to:")
    print("- Add the tool definitions to the list in @app.list_tools()")
    print("- Add the handlers before the final 'else' in @app.call_tool()")
    print("- Add the Lua handlers before the final 'else' in mcp_bridge.lua")