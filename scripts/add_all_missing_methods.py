#!/usr/bin/env python3
"""
Add all missing methods to the REAPER MCP Server
This script generates code for all unimplemented methods from IMPLEMENTATION_STATUS.md
"""

import json

# All methods that need to be implemented
MISSING_METHODS = {
    "Media Items": [
        {
            "tool_name": "add_media_item_to_track",
            "description": "Add a new media item to a track",
            "lua_func": "AddMediaItemToTrack",
            "params": [("track_index", "integer", "Track index")],
            "returns": "item",
            "handler_type": "media_item"
        },
        {
            "tool_name": "count_media_items",
            "description": "Count total media items in project",
            "lua_func": "CountMediaItems",
            "params": [("project_index", "integer", "Project index (0=current)", True, 0)],
            "returns": "count"
        },
        {
            "tool_name": "get_media_item",
            "description": "Get media item by index",
            "lua_func": "GetMediaItem",
            "params": [
                ("project_index", "integer", "Project index (0=current)", True, 0),
                ("item_index", "integer", "Item index (0-based)")
            ],
            "returns": "item"
        },
        {
            "tool_name": "delete_track_media_item",
            "description": "Delete a media item from track",
            "lua_func": "DeleteTrackMediaItem",
            "params": [
                ("track_index", "integer", "Track index"),
                ("item_index", "integer", "Item index on track")
            ],
            "returns": None
        },
        {
            "tool_name": "get_media_item_length",
            "description": "Get media item length",
            "lua_func": "GetMediaItemLength",
            "params": [("item_index", "integer", "Item index")],
            "returns": "length"
        },
        {
            "tool_name": "set_media_item_length",
            "description": "Set media item length",
            "lua_func": "SetMediaItemLength",
            "params": [
                ("item_index", "integer", "Item index"),
                ("length", "number", "New length in seconds")
            ],
            "returns": None
        },
        {
            "tool_name": "get_media_item_position",
            "description": "Get media item position",
            "lua_func": "GetMediaItemPosition",
            "params": [("item_index", "integer", "Item index")],
            "returns": "position"
        },
        {
            "tool_name": "set_media_item_position",
            "description": "Set media item position",
            "lua_func": "SetMediaItemPosition",
            "params": [
                ("item_index", "integer", "Item index"),
                ("position", "number", "New position in seconds")
            ],
            "returns": None
        }
    ],
    "Project Management": [
        {
            "tool_name": "get_project_name",
            "description": "Get the current project name",
            "lua_func": "GetProjectName",
            "params": [("project_index", "integer", "Project index (0=current)", True, 0)],
            "returns": "name"
        },
        {
            "tool_name": "get_project_path", 
            "description": "Get the current project path",
            "lua_func": "GetProjectPath",
            "params": [("project_index", "integer", "Project index (0=current)", True, 0)],
            "returns": "path"
        },
        {
            "tool_name": "save_project",
            "description": "Save the current project",
            "lua_func": "Main_SaveProject",
            "params": [
                ("project_index", "integer", "Project index (0=current)", True, 0),
                ("force_save_as", "boolean", "Force save as dialog", True, False)
            ],
            "returns": None
        }
    ],
    "Transport & Playback": [
        {
            "tool_name": "get_cursor_position",
            "description": "Get the edit cursor position in seconds",
            "lua_func": "GetCursorPosition",
            "params": [],
            "returns": "position"
        },
        {
            "tool_name": "set_edit_cursor_position",
            "description": "Set the edit cursor position",
            "lua_func": "SetEditCurPos",
            "params": [
                ("time", "number", "Time in seconds"),
                ("move_view", "boolean", "Move view to cursor", True, True),
                ("seek_play", "boolean", "Seek playback to cursor", True, False)
            ],
            "returns": None
        },
        {
            "tool_name": "get_play_state",
            "description": "Get current playback state",
            "lua_func": "GetPlayState",
            "params": [],
            "returns": "state"
        },
        {
            "tool_name": "play",
            "description": "Start playback",
            "lua_func": "CSurf_OnPlay",
            "params": [],
            "returns": None
        },
        {
            "tool_name": "stop",
            "description": "Stop playback",
            "lua_func": "CSurf_OnStop",
            "params": [],
            "returns": None
        },
        {
            "tool_name": "pause",
            "description": "Pause playback",
            "lua_func": "CSurf_OnPause",
            "params": [],
            "returns": None
        }
    ],
    "Actions & Commands": [
        {
            "tool_name": "execute_action",
            "description": "Execute a REAPER action by command ID",
            "lua_func": "Main_OnCommand",
            "params": [
                ("command_id", "integer", "Command ID"),
                ("flag", "integer", "Flag (0=normal)", True, 0)
            ],
            "returns": None
        }
    ],
    "Undo System": [
        {
            "tool_name": "undo_begin_block",
            "description": "Begin an undo block",
            "lua_func": "Undo_BeginBlock",
            "params": [],
            "returns": None
        },
        {
            "tool_name": "undo_end_block",
            "description": "End an undo block with description",
            "lua_func": "Undo_EndBlock",
            "params": [
                ("description", "string", "Description of the changes"),
                ("flags", "integer", "Flags (-1 for all)", True, -1)
            ],
            "returns": None
        }
    ],
    "UI Updates": [
        {
            "tool_name": "update_arrange",
            "description": "Update the arrange view",
            "lua_func": "UpdateArrange",
            "params": [],
            "returns": None
        },
        {
            "tool_name": "update_timeline",
            "description": "Update the timeline display",
            "lua_func": "UpdateTimeline",
            "params": [],
            "returns": None
        }
    ]
}

def generate_tool_definition(method):
    """Generate a single tool definition"""
    tool_def = f'''        Tool(
            name="{method['tool_name']}",
            description="{method['description']}",
            inputSchema={{
                "type": "object",
                "properties": {{'''
    
    # Add properties for each parameter
    props = []
    required = []
    
    for param in method['params']:
        name = param[0]
        ptype = param[1]
        desc = param[2]
        optional = len(param) > 3 and param[3]
        default = param[4] if len(param) > 4 else None
        
        if not optional:
            required.append(name)
            
        prop = f'''
                    "{name}": {{
                        "type": "{ptype}",
                        "description": "{desc}"'''
        
        if ptype == "integer" and name.endswith("_index"):
            prop += ',\n                        "minimum": 0'
        
        if default is not None:
            if ptype == "string":
                prop += f',\n                        "default": "{default}"'
            else:
                prop += f',\n                        "default": {json.dumps(default)}'
                
        prop += '\n                    }'
        props.append(prop)
    
    if props:
        tool_def += ','.join(props)
        
    tool_def += f'''
                }},
                "required": {json.dumps(required)}
            }}
        )'''
    
    return tool_def

def generate_handler(method):
    """Generate a call_tool handler"""
    handler = f'''\n    elif name == "{method['tool_name']}":'''
    
    # Extract arguments
    for param in method['params']:
        name = param[0]
        optional = len(param) > 3 and param[3]
        default = param[4] if len(param) > 4 else None
        
        if optional and default is not None:
            handler += f'\n        {name} = arguments.get("{name}", {json.dumps(default)})'
        else:
            handler += f'\n        {name} = arguments["{name}"]'
    
    # Special handling for different method types
    if method.get('handler_type') == 'media_item':
        # Media item methods need special handling
        if method['tool_name'] == 'add_media_item_to_track':
            handler += '''
        
        # First check if track exists
        track_result = bridge.call_lua("GetTrack", [0, track_index])
        if not track_result.get("ok") or not track_result.get("ret"):
            return [TextContent(
                type="text",
                text=f"Failed to find track at index {track_index}"
            )]
        
        result = bridge.call_lua("AddMediaItemToTrack", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Added media item to track {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add media item: {result.get('error', 'Unknown error')}"
            )]'''
            
        elif 'item_index' in [p[0] for p in method['params']]:
            # Methods that operate on items by index
            handler += f'''
        
        result = bridge.call_lua("{method['lua_func']}", [{', '.join([p[0] for p in method['params']])}])
        
        if result.get("ok"):'''
            
            if method['returns']:
                handler += f'''
            return [TextContent(
                type="text",
                text=f"{method['description']}: {{result.get('ret', 'Unknown')}}"
            )]'''
            else:
                handler += f'''
            return [TextContent(
                type="text",
                text=f"Successfully executed {method['tool_name']}"
            )]'''
                
            handler += f'''
        else:
            return [TextContent(
                type="text",
                text=f"Failed to {method['tool_name']}: {{result.get('error', 'Unknown error')}}"
            )]'''
    
    else:
        # Standard methods
        args = [p[0] for p in method['params']]
        handler += f'''
        
        result = bridge.call_lua("{method['lua_func']}", [{', '.join(args) if args else ''}])
        
        if result.get("ok"):'''
        
        if method['returns']:
            handler += f'''
            return [TextContent(
                type="text",
                text=f"{method['description']}: {{result.get('ret', 'Unknown')}}"
            )]'''
        else:
            handler += f'''
            return [TextContent(
                type="text",
                text=f"Successfully executed {method['tool_name']}"
            )]'''
            
        handler += f'''
        else:
            return [TextContent(
                type="text",
                text=f"Failed to {method['tool_name']}: {{result.get('error', 'Unknown error')}}"
            )]'''
    
    return handler

def generate_lua_handler(method):
    """Generate Lua bridge handler"""
    handler = f'''            elseif fname == "{method['lua_func']}" then'''
    
    # Check parameter count
    required_args = [p for p in method['params'] if len(p) <= 3 or not p[3]]
    if required_args:
        handler += f'''
                if #args >= {len(required_args)} then'''
        
    # Special handling for different methods
    if method['tool_name'] == 'add_media_item_to_track':
        handler += '''
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local item = reaper.AddMediaItemToTrack(track)
                        response.ok = true
                        response.ret = item
                    else
                        response.error = "Track not found"
                    end'''
                    
    elif method['tool_name'] in ['get_media_item_length', 'set_media_item_length', 
                                'get_media_item_position', 'set_media_item_position']:
        # These operate on media items
        handler += '''
                    local item = reaper.GetMediaItem(0, args[1])
                    if item then'''
        
        if method['tool_name'] == 'get_media_item_length':
            handler += '''
                        local length = reaper.GetMediaItemInfo_Value(item, "D_LENGTH")
                        response.ok = true
                        response.ret = length'''
        elif method['tool_name'] == 'set_media_item_length':
            handler += '''
                        reaper.SetMediaItemInfo_Value(item, "D_LENGTH", args[2])
                        response.ok = true'''
        elif method['tool_name'] == 'get_media_item_position':
            handler += '''
                        local pos = reaper.GetMediaItemInfo_Value(item, "D_POSITION")
                        response.ok = true
                        response.ret = pos'''
        elif method['tool_name'] == 'set_media_item_position':
            handler += '''
                        reaper.SetMediaItemInfo_Value(item, "D_POSITION", args[2])
                        response.ok = true'''
                        
        handler += '''
                    else
                        response.error = "Item not found"
                    end'''
                    
    elif method['tool_name'] == 'delete_track_media_item':
        handler += '''
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local item = reaper.GetTrackMediaItem(track, args[2])
                        if item then
                            reaper.DeleteTrackMediaItem(track, item)
                            response.ok = true
                        else
                            response.error = "Item not found on track"
                        end
                    else
                        response.error = "Track not found"
                    end'''
                    
    elif method['tool_name'] == 'get_project_name':
        handler += '''
                    local retval, projfn = reaper.GetProjectName(args[1] or 0)
                    response.ok = true
                    response.ret = projfn'''
                    
    elif method['tool_name'] == 'get_project_path':
        handler += '''
                    local path = reaper.GetProjectPath(args[1] or 0)
                    response.ok = true
                    response.ret = path'''
                    
    elif method['tool_name'] == 'get_play_state':
        handler += '''
                    local state = reaper.GetPlayState()
                    response.ok = true
                    response.ret = state'''
                    
    else:
        # Standard function call
        args_str = ', '.join([f'args[{i+1}]' for i in range(len(method['params']))])
        if not args_str and method['lua_func'] in ['CSurf_OnPlay', 'CSurf_OnStop', 
                                                    'CSurf_OnPause', 'UpdateArrange', 
                                                    'UpdateTimeline', 'Undo_BeginBlock',
                                                    'GetCursorPosition']:
            # No arguments
            handler += f'''
                    reaper.{method['lua_func']}()
                    response.ok = true'''
            if method['lua_func'] == 'GetCursorPosition':
                handler = handler.replace('reaper.GetCursorPosition()', 
                                        'local pos = reaper.GetCursorPosition()')
                handler = handler.replace('response.ok = true', 
                                        'response.ok = true\n                    response.ret = pos')
        else:
            handler += f'''
                    reaper.{method['lua_func']}({args_str})
                    response.ok = true'''
    
    if required_args:
        handler += f'''
                else
                    response.error = "{method['lua_func']} requires {len(required_args)} argument(s)"
                end'''
                
    return handler

def main():
    print("=== Generating All Missing Methods ===\n")
    
    all_tools = []
    all_handlers = []
    all_lua_handlers = []
    
    for category, methods in MISSING_METHODS.items():
        print(f"\n{category}:")
        for method in methods:
            print(f"  - {method['tool_name']}")
            all_tools.append(generate_tool_definition(method))
            all_handlers.append(generate_handler(method))
            all_lua_handlers.append(generate_lua_handler(method))
    
    print("\n\n=== GENERATED CODE ===\n")
    
    # Write tools to file
    with open('generated_tools.txt', 'w') as f:
        f.write("# Add these tool definitions to @app.list_tools() in server/app.py:\n")
        f.write("# (Add after the last Tool definition, before the closing bracket)\n\n")
        f.write(',\n'.join(all_tools))
    
    # Write handlers to file
    with open('generated_handlers.txt', 'w') as f:
        f.write("# Add these handlers to @app.call_tool() in server/app.py:\n")
        f.write("# (Add before the final 'else' clause)\n\n")
        f.write(''.join(all_handlers))
    
    # Write Lua handlers to file
    with open('generated_lua_handlers.txt', 'w') as f:
        f.write("-- Add these handlers to lua/mcp_bridge.lua:\n")
        f.write("-- (Add before the final 'else' clause)\n\n")
        f.write('\n'.join(all_lua_handlers))
    
    print("Generated code written to:")
    print("  - generated_tools.txt")
    print("  - generated_handlers.txt")
    print("  - generated_lua_handlers.txt")
    
    print(f"\nTotal methods to add: {sum(len(methods) for methods in MISSING_METHODS.values())}")

if __name__ == "__main__":
    main()