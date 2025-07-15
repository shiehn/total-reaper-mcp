"""Loop and time selection management tools for generative music creation."""

from typing import Dict, Any, List, Optional, Tuple
from .bridge_sync import ReaperBridge


def get_time_selection() -> Dict[str, Any]:
    """Get the current time selection (loop) in the project.
    
    Returns:
        Dict containing:
        - start: Start time in seconds
        - end: End time in seconds  
        - length: Length in seconds
        - is_set: Whether a time selection exists
    """
    request = {
        "action": "GetSet_LoopTimeRange",
        "isSet": False,
        "isLoop": True,
        "startOut": 0.0,
        "endOut": 0.0,
        "allowautoseek": False
    }
    
    response = ReaperBridge.send_request(request)
    
    if response.get("result"):
        start = response.get("startOut", 0.0)
        end = response.get("endOut", 0.0)
        
        return {
            "start": start,
            "end": end,
            "length": end - start,
            "is_set": end > start
        }
    
    return {
        "start": 0.0,
        "end": 0.0,
        "length": 0.0,
        "is_set": False
    }


def set_time_selection(start: float, end: float) -> Dict[str, Any]:
    """Set the time selection (loop) in the project.
    
    Args:
        start: Start time in seconds
        end: End time in seconds
    
    Returns:
        Dict containing the operation result
    """
    request = {
        "action": "GetSet_LoopTimeRange",
        "isSet": True,
        "isLoop": True,
        "startOut": start,
        "endOut": end,
        "allowautoseek": False
    }
    
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "start": start,
        "end": end
    }


def clear_time_selection() -> Dict[str, Any]:
    """Clear the time selection.
    
    Returns:
        Dict containing the operation result
    """
    return set_time_selection(0.0, 0.0)


def get_loop_points() -> Dict[str, Any]:
    """Get the loop point positions.
    
    Returns:
        Dict containing:
        - enabled: Whether looping is enabled
        - start: Loop start position in seconds
        - end: Loop end position in seconds
    """
    # First check if repeat is enabled
    repeat_request = {"action": "GetSetRepeat", "val": -1}
    repeat_response = ReaperBridge.send_request(repeat_request)
    repeat_enabled = repeat_response.get("val", 0) == 1
    
    # Get loop points (same as time selection in REAPER)
    time_sel = get_time_selection()
    
    return {
        "enabled": repeat_enabled,
        "start": time_sel["start"],
        "end": time_sel["end"],
        "length": time_sel["length"]
    }


def set_loop_enabled(enabled: bool) -> Dict[str, Any]:
    """Enable or disable looping.
    
    Args:
        enabled: Whether to enable looping
    
    Returns:
        Dict containing the operation result
    """
    request = {"action": "GetSetRepeat", "val": 1 if enabled else 0}
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "enabled": enabled
    }


def set_loop_points(start: float, end: float, enable: bool = True) -> Dict[str, Any]:
    """Set loop points and optionally enable looping.
    
    Args:
        start: Loop start position in seconds
        end: Loop end position in seconds
        enable: Whether to enable looping
    
    Returns:
        Dict containing the operation result
    """
    # Set the time selection which defines loop points
    time_result = set_time_selection(start, end)
    
    # Enable/disable looping if requested
    if enable:
        loop_result = set_loop_enabled(True)
        time_result["loop_enabled"] = loop_result["enabled"]
    
    return time_result


def duplicate_time_selection(count: int = 1) -> Dict[str, Any]:
    """Duplicate the contents of the time selection.
    
    Args:
        count: Number of times to duplicate
    
    Returns:
        Dict containing the operation result
    """
    # Get current time selection
    time_sel = get_time_selection()
    
    if not time_sel["is_set"]:
        return {
            "success": False,
            "error": "No time selection set"
        }
    
    # Use the duplicate action
    for i in range(count):
        request = {
            "action": "Main_OnCommand",
            "command": 41296,  # Time selection: Duplicate items
            "project": 0
        }
        response = ReaperBridge.send_request(request)
        
        if not response.get("result", False):
            return {
                "success": False,
                "error": f"Failed to duplicate on iteration {i+1}"
            }
    
    return {
        "success": True,
        "duplications": count,
        "original_start": time_sel["start"],
        "original_end": time_sel["end"]
    }


def shift_time_selection(offset: float) -> Dict[str, Any]:
    """Shift the time selection by an offset.
    
    Args:
        offset: Time offset in seconds (positive = forward, negative = backward)
    
    Returns:
        Dict containing the operation result
    """
    time_sel = get_time_selection()
    
    if not time_sel["is_set"]:
        return {
            "success": False,
            "error": "No time selection set"
        }
    
    new_start = time_sel["start"] + offset
    new_end = time_sel["end"] + offset
    
    # Ensure we don't go negative
    if new_start < 0:
        new_end -= new_start
        new_start = 0
    
    return set_time_selection(new_start, new_end)


def create_loop_from_items() -> Dict[str, Any]:
    """Create a time selection loop from selected items.
    
    Returns:
        Dict containing the operation result
    """
    # Get selected items
    count_request = {"action": "CountSelectedMediaItems", "proj": 0}
    count_response = ReaperBridge.send_request(count_request)
    count = count_response.get("count", 0)
    
    if count == 0:
        return {
            "success": False,
            "error": "No items selected"
        }
    
    # Find bounds of selected items
    min_start = float('inf')
    max_end = float('-inf')
    
    for i in range(count):
        item_request = {"action": "GetSelectedMediaItem", "proj": 0, "selitem": i}
        item_response = ReaperBridge.send_request(item_request)
        
        if item_response.get("result"):
            item_handle = item_response.get("item")
            
            # Get item position
            pos_request = {"action": "GetMediaItemInfo_Value", "item": item_handle, "parmname": "D_POSITION"}
            pos_response = ReaperBridge.send_request(pos_request)
            position = pos_response.get("value", 0.0)
            
            # Get item length
            len_request = {"action": "GetMediaItemInfo_Value", "item": item_handle, "parmname": "D_LENGTH"}
            len_response = ReaperBridge.send_request(len_request)
            length = len_response.get("value", 0.0)
            
            min_start = min(min_start, position)
            max_end = max(max_end, position + length)
    
    if min_start < float('inf') and max_end > float('-inf'):
        return set_time_selection(min_start, max_end)
    
    return {
        "success": False,
        "error": "Could not determine item bounds"
    }


def split_items_at_loop_points() -> Dict[str, Any]:
    """Split all items at the loop point boundaries.
    
    Returns:
        Dict containing the operation result
    """
    time_sel = get_time_selection()
    
    if not time_sel["is_set"]:
        return {
            "success": False,
            "error": "No time selection set"
        }
    
    # Split items at time selection start
    start_request = {
        "action": "SplitMediaItem",
        "item": None,  # null means all items
        "position": time_sel["start"]
    }
    start_response = ReaperBridge.send_request(start_request)
    
    # Split items at time selection end
    end_request = {
        "action": "SplitMediaItem",
        "item": None,  # null means all items
        "position": time_sel["end"]
    }
    end_response = ReaperBridge.send_request(end_request)
    
    return {
        "success": start_response.get("result", False) and end_response.get("result", False),
        "split_at_start": time_sel["start"],
        "split_at_end": time_sel["end"]
    }


def get_grid_division() -> Dict[str, Any]:
    """Get the current grid division setting.
    
    Returns:
        Dict containing grid division info
    """
    request = {"action": "GetSetProjectGrid", "project": 0, "set": False}
    response = ReaperBridge.send_request(request)
    
    return {
        "division": response.get("division", 0.25),
        "swing": response.get("swingamt", 0.0),
        "swing_mode": response.get("swingmode", 0)
    }


def set_grid_division(division: float, swing: float = 0.0) -> Dict[str, Any]:
    """Set the grid division for quantization.
    
    Args:
        division: Grid division (e.g., 0.25 for 1/4 note, 0.125 for 1/8 note)
        swing: Swing amount (0.0 to 1.0)
    
    Returns:
        Dict containing the operation result
    """
    request = {
        "action": "GetSetProjectGrid",
        "project": 0,
        "set": True,
        "division": division,
        "swingmode": 1 if swing > 0 else 0,
        "swingamt": swing
    }
    
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "division": division,
        "swing": swing
    }


def quantize_time_selection(strength: float = 1.0) -> Dict[str, Any]:
    """Quantize items in the time selection to the grid.
    
    Args:
        strength: Quantization strength (0.0 to 1.0)
    
    Returns:
        Dict containing the operation result
    """
    # Apply quantization with strength
    if strength < 1.0:
        # Use action for partial quantization
        request = {
            "action": "Main_OnCommand",
            "command": 40404,  # Item: Quantize item positions to grid...
            "project": 0
        }
    else:
        # Use action for full quantization
        request = {
            "action": "Main_OnCommand", 
            "command": 40316,  # Item: Quantize item positions to grid
            "project": 0
        }
    
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False),
        "strength": strength
    }


def crop_to_time_selection() -> Dict[str, Any]:
    """Crop the project to the time selection.
    
    Returns:
        Dict containing the operation result
    """
    request = {
        "action": "Main_OnCommand",
        "command": 40049,  # Time selection: Crop project to time selection
        "project": 0
    }
    
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False)
    }


def insert_time_at_loop_start(length: float) -> Dict[str, Any]:
    """Insert empty time at the loop start position.
    
    Args:
        length: Length of time to insert in seconds
    
    Returns:
        Dict containing the operation result
    """
    time_sel = get_time_selection()
    
    if not time_sel["is_set"]:
        return {
            "success": False,
            "error": "No time selection set"
        }
    
    # Select time range to insert
    set_time_selection(time_sel["start"], time_sel["start"] + length)
    
    # Insert empty space
    request = {
        "action": "Main_OnCommand",
        "command": 40200,  # Time selection: Insert empty space at time selection
        "project": 0
    }
    response = ReaperBridge.send_request(request)
    
    # Restore original time selection shifted by insert amount
    set_time_selection(time_sel["start"] + length, time_sel["end"] + length)
    
    return {
        "success": response.get("result", False),
        "inserted_at": time_sel["start"],
        "inserted_length": length
    }


def remove_time_selection() -> Dict[str, Any]:
    """Remove the contents of time selection and ripple edit.
    
    Returns:
        Dict containing the operation result
    """
    request = {
        "action": "Main_OnCommand",
        "command": 40201,  # Time selection: Remove contents of time selection (moving later items)
        "project": 0
    }
    
    response = ReaperBridge.send_request(request)
    
    return {
        "success": response.get("result", False)
    }


def register_loop_management_tools(mcp):
    """Register loop management tools with MCP server."""
    from functools import wraps
    
    # Helper to wrap sync functions for async
    def async_wrapper(func):
        @wraps(func)
        async def wrapper(**kwargs):
            return func(**kwargs)
        return wrapper
    
    # Register all loop management tools
    tool_functions = [
        ("get_time_selection", get_time_selection),
        ("set_time_selection", set_time_selection),
        ("clear_time_selection", clear_time_selection),
        ("get_loop_points", get_loop_points),
        ("set_loop_enabled", set_loop_enabled),
        ("set_loop_points", set_loop_points),
        ("duplicate_time_selection", duplicate_time_selection),
        ("shift_time_selection", shift_time_selection),
        ("create_loop_from_items", create_loop_from_items),
        ("split_items_at_loop_points", split_items_at_loop_points),
        ("get_grid_division", get_grid_division),
        ("set_grid_division", set_grid_division),
        ("quantize_time_selection", quantize_time_selection),
        ("crop_to_time_selection", crop_to_time_selection),
        ("insert_time_at_loop_start", insert_time_at_loop_start),
        ("remove_time_selection", remove_time_selection),
    ]
    
    # Find the corresponding tool definition and register
    for tool_name, tool_func in tool_functions:
        tool_def = next((t for t in tools if t["name"] == tool_name), None)
        if tool_def:
            mcp.tool(
                name=tool_name,
                description=tool_def["description"]
            )(async_wrapper(tool_func))
    
    return len(tool_functions)


# Tool definitions for MCP
tools = [
    {
        "name": "get_time_selection",
        "description": "Get the current time selection (loop) in the project",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "set_time_selection", 
        "description": "Set the time selection (loop) in the project",
        "input_schema": {
            "type": "object",
            "properties": {
                "start": {"type": "number", "description": "Start time in seconds"},
                "end": {"type": "number", "description": "End time in seconds"}
            },
            "required": ["start", "end"]
        }
    },
    {
        "name": "clear_time_selection",
        "description": "Clear the time selection",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_loop_points",
        "description": "Get the loop point positions and status",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "set_loop_enabled",
        "description": "Enable or disable looping",
        "input_schema": {
            "type": "object",
            "properties": {
                "enabled": {"type": "boolean", "description": "Whether to enable looping"}
            },
            "required": ["enabled"]
        }
    },
    {
        "name": "set_loop_points",
        "description": "Set loop points and optionally enable looping",
        "input_schema": {
            "type": "object",
            "properties": {
                "start": {"type": "number", "description": "Loop start position in seconds"},
                "end": {"type": "number", "description": "Loop end position in seconds"},
                "enable": {"type": "boolean", "description": "Whether to enable looping", "default": True}
            },
            "required": ["start", "end"]
        }
    },
    {
        "name": "duplicate_time_selection",
        "description": "Duplicate the contents of the time selection",
        "input_schema": {
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "Number of times to duplicate", "default": 1}
            },
            "required": []
        }
    },
    {
        "name": "shift_time_selection",
        "description": "Shift the time selection by an offset",
        "input_schema": {
            "type": "object",
            "properties": {
                "offset": {"type": "number", "description": "Time offset in seconds (positive = forward)"}
            },
            "required": ["offset"]
        }
    },
    {
        "name": "create_loop_from_items",
        "description": "Create a time selection loop from selected items",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "split_items_at_loop_points",
        "description": "Split all items at the loop point boundaries",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_grid_division",
        "description": "Get the current grid division setting",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "set_grid_division",
        "description": "Set the grid division for quantization",
        "input_schema": {
            "type": "object",
            "properties": {
                "division": {"type": "number", "description": "Grid division (e.g., 0.25 for 1/4 note)"},
                "swing": {"type": "number", "description": "Swing amount (0.0 to 1.0)", "default": 0.0}
            },
            "required": ["division"]
        }
    },
    {
        "name": "quantize_time_selection",
        "description": "Quantize items in the time selection to the grid",
        "input_schema": {
            "type": "object",
            "properties": {
                "strength": {"type": "number", "description": "Quantization strength (0.0 to 1.0)", "default": 1.0}
            },
            "required": []
        }
    },
    {
        "name": "crop_to_time_selection",
        "description": "Crop the project to the time selection",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "insert_time_at_loop_start",
        "description": "Insert empty time at the loop start position",
        "input_schema": {
            "type": "object",
            "properties": {
                "length": {"type": "number", "description": "Length of time to insert in seconds"}
            },
            "required": ["length"]
        }
    },
    {
        "name": "remove_time_selection",
        "description": "Remove contents of time selection with ripple edit",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]