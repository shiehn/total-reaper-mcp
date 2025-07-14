"""
Project Management Tools for REAPER MCP

This module contains tools for managing REAPER projects.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# Basic Project Management (6 tools)
# ============================================================================

async def get_project_name(project_index: int = 0) -> str:
    """Get the current project name"""
    result = await bridge.call_lua("GetProjectName", [project_index, "", 512])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) > 0:
            project_name = ret[0] if len(ret) > 0 else "Untitled"
            return f"Project name: {project_name}"
        else:
            return "Project name: Untitled"
    else:
        raise Exception(f"Failed to get project name: {result.get('error', 'Unknown error')}")


async def get_project_path(project_index: int = 0) -> str:
    """Get the current project path"""
    result = await bridge.call_lua("GetProjectPath", ["", 2048])
    
    if result.get("ok"):
        path = result.get("ret", "")
        return f"Project path: {path}"
    else:
        raise Exception(f"Failed to get project path: {result.get('error', 'Unknown error')}")


async def save_project(project_index: int = 0, force_save_as: bool = False) -> str:
    """Save the current project"""
    result = await bridge.call_lua("Main_SaveProject", [project_index, force_save_as])
    
    if result.get("ok"):
        return "Project saved successfully"
    else:
        raise Exception(f"Failed to save project: {result.get('error', 'Unknown error')}")


async def open_project(filename: str, in_new_tab: bool = False) -> str:
    """Open a REAPER project file"""
    # 0 = current tab, 1 = new tab
    mode = 1 if in_new_tab else 0
    result = await bridge.call_lua("Main_openProject", [filename])
    
    if result.get("ok"):
        return f"Opened project: {filename}"
    else:
        raise Exception(f"Failed to open project: {result.get('error', 'Unknown error')}")


async def close_project(save_prompt: bool = True) -> str:
    """Close the current project"""
    # Use the close project action
    result = await bridge.call_lua("Main_OnCommand", [40860, 0])  # File: Close project
    
    if result.get("ok"):
        return "Project closed"
    else:
        raise Exception(f"Failed to close project: {result.get('error', 'Unknown error')}")


async def mark_project_dirty(project_index: int = 0) -> str:
    """Mark the project as having unsaved changes"""
    result = await bridge.call_lua("MarkProjectDirty", [project_index])
    
    if result.get("ok"):
        return "Project marked as dirty (unsaved changes)"
    else:
        raise Exception(f"Failed to mark project dirty: {result.get('error', 'Unknown error')}")


# ============================================================================
# Project Instance Management (3 tools)
# ============================================================================

async def enum_projects() -> str:
    """Get information about all open projects"""
    result = await bridge.call_lua("EnumProjects", [])
    
    if result.get("ok"):
        projects = []
        index = 0
        
        # Get all open projects
        while True:
            proj_result = await bridge.call_lua("EnumProjects", [index])
            if not proj_result.get("ok") or not proj_result.get("ret"):
                break
                
            # Get project name
            name_result = await bridge.call_lua("GetProjectName", [index, "", 512])
            if name_result.get("ok"):
                ret = name_result.get("ret", [])
                if isinstance(ret, list) and len(ret) > 0:
                    project_name = ret[0]
                else:
                    project_name = "Untitled"
            else:
                project_name = "Unknown"
                
            projects.append(f"{index}: {project_name}")
            index += 1
        
        if projects:
            return f"Open projects:\n" + "\n".join(projects)
        else:
            return "No projects open"
    else:
        raise Exception(f"Failed to enumerate projects: {result.get('error', 'Unknown error')}")


async def select_project_instance(project_index: int) -> str:
    """Switch to a specific project by index"""
    result = await bridge.call_lua("SelectProjectInstance", [project_index])
    
    if result.get("ok"):
        return f"Switched to project {project_index}"
    else:
        raise Exception(f"Failed to switch project: {result.get('error', 'Unknown error')}")


async def get_current_project_index() -> str:
    """Get the index of the currently active project"""
    result = await bridge.call_lua("GetCurrentProjectIndex", [])
    
    if result.get("ok"):
        index = result.get("ret", -1)
        return f"Current project index: {index}"
    else:
        raise Exception(f"Failed to get current project index: {result.get('error', 'Unknown error')}")


# ============================================================================
# Project Properties (8 tools)
# ============================================================================

async def get_project_length(project_index: int = 0) -> str:
    """Get the project length in seconds"""
    result = await bridge.call_lua("GetProjectLength", [project_index])
    
    if result.get("ok"):
        length = result.get("ret", 0.0)
        return f"Project length: {length:.3f} seconds"
    else:
        raise Exception(f"Failed to get project length: {result.get('error', 'Unknown error')}")


async def set_project_length(length: float, project_index: int = 0) -> str:
    """Set the project length in seconds"""
    # Get current cursor position
    cursor_result = await bridge.call_lua("GetCursorPosition", [])
    if not cursor_result.get("ok"):
        raise Exception("Failed to get cursor position")
    
    original_pos = cursor_result.get("ret", 0.0)
    
    # Move cursor to the desired length
    await bridge.call_lua("SetEditCurPos", [length, False, False])
    
    # Use action to set project end to cursor
    result = await bridge.call_lua("Main_OnCommand", [40043, 0])  # Transport: Go to end of project
    
    # Restore cursor position
    await bridge.call_lua("SetEditCurPos", [original_pos, False, False])
    
    if result.get("ok"):
        return f"Set project length to {length:.3f} seconds"
    else:
        raise Exception(f"Failed to set project length: {result.get('error', 'Unknown error')}")


async def get_project_tempo() -> str:
    """Get the current project tempo in BPM"""
    # Get master tempo
    result = await bridge.call_lua("Master_GetTempo", [])
    
    if result.get("ok"):
        tempo = result.get("ret", 120.0)
        return f"Project tempo: {tempo:.2f} BPM"
    else:
        raise Exception(f"Failed to get project tempo: {result.get('error', 'Unknown error')}")


async def set_project_tempo(tempo: float, position: Optional[float] = None) -> str:
    """Set the project tempo in BPM"""
    # If position is not specified, use current cursor position
    if position is None:
        pos_result = await bridge.call_lua("GetCursorPosition", [])
        position = pos_result.get("ret", 0.0) if pos_result.get("ok") else 0.0
    
    result = await bridge.call_lua("SetTempoTimeSigMarker", [0, -1, position, -1, -1, tempo, 0, 0, True])
    
    if result.get("ok"):
        return f"Set project tempo to {tempo:.2f} BPM"
    else:
        raise Exception(f"Failed to set project tempo: {result.get('error', 'Unknown error')}")


async def get_project_time_signature() -> str:
    """Get the current project time signature"""
    # Get time signature at edit cursor
    cursor_result = await bridge.call_lua("GetCursorPosition", [])
    if not cursor_result.get("ok"):
        raise Exception("Failed to get cursor position")
    
    position = cursor_result.get("ret", 0.0)
    
    result = await bridge.call_lua("TimeMap_GetTimeSigAtTime", [0, position])
    
    if result.get("ok"):
        # Result should contain numerator and denominator
        tsig_num = result.get("tsig_num", 4)
        tsig_denom = result.get("tsig_denom", 4)
        return f"Time signature: {tsig_num}/{tsig_denom}"
    else:
        raise Exception(f"Failed to get time signature: {result.get('error', 'Unknown error')}")


async def set_project_time_signature(numerator: int, denominator: int, position: Optional[float] = None) -> str:
    """Set the project time signature"""
    # If position is not specified, use current cursor position
    if position is None:
        pos_result = await bridge.call_lua("GetCursorPosition", [])
        position = pos_result.get("ret", 0.0) if pos_result.get("ok") else 0.0
    
    result = await bridge.call_lua("SetTempoTimeSigMarker", [0, -1, position, -1, -1, -1, numerator, denominator, False])
    
    if result.get("ok"):
        return f"Set time signature to {numerator}/{denominator}"
    else:
        raise Exception(f"Failed to set time signature: {result.get('error', 'Unknown error')}")


async def get_project_sample_rate() -> str:
    """Get the project sample rate"""
    result = await bridge.call_lua("GetSetProjectInfo_String", [0, "RENDER_SRATE", "", False])
    
    if result.get("ok"):
        # Parse sample rate from string
        srate_str = result.get("ret", "48000")
        try:
            # Extract numeric part
            srate = float(srate_str.split()[0]) if srate_str else 48000
            
            # If it's a whole number, format without decimals
            if srate.is_integer():
                return f"Project sample rate: {int(srate)} Hz"
            else:
                return f"Project sample rate: {srate} Hz"
        except:
            return f"Project sample rate: {srate_str}"
    else:
        raise Exception(f"Failed to get sample rate: {result.get('error', 'Unknown error')}")


async def set_project_sample_rate(sample_rate: int) -> str:
    """Set the project sample rate"""
    result = await bridge.call_lua("GetSetProjectInfo_String", [0, "RENDER_SRATE", str(sample_rate), True])
    
    if result.get("ok"):
        return f"Set project sample rate to {sample_rate} Hz"
    else:
        raise Exception(f"Failed to set sample rate: {result.get('error', 'Unknown error')}")


# ============================================================================
# Project Grid & Display (2 tools)
# ============================================================================

async def get_project_grid_division() -> str:
    """Get the project grid division"""
    result = await bridge.call_lua("GetSetProjectGrid", [0, False, 0, 0, 0])
    
    if result.get("ok"):
        # Result contains division and swing info
        division = result.get("division", 0.25)
        swing = result.get("swing", 0.0)
        swing_amt = result.get("swing_amt", 1.0)
        
        # Convert division to musical notation
        divisions = {
            4.0: "1 bar",
            2.0: "1/2",
            1.0: "1/4", 
            0.5: "1/8",
            0.25: "1/16",
            0.125: "1/32",
            0.0625: "1/64"
        }
        
        div_text = divisions.get(division, f"{division}")
        swing_text = f", swing: {swing:.0%} ({swing_amt:.2f})" if swing != 0 else ""
        
        return f"Grid division: {div_text}{swing_text}"
    else:
        raise Exception(f"Failed to get grid division: {result.get('error', 'Unknown error')}")


async def set_project_grid_division(division: float, swing: float = 0.0, swing_amt: float = 1.0) -> str:
    """Set the project grid division"""
    result = await bridge.call_lua("GetSetProjectGrid", [0, True, division, swing, swing_amt])
    
    if result.get("ok"):
        # Convert division to musical notation
        divisions = {
            4.0: "1 bar",
            2.0: "1/2",
            1.0: "1/4", 
            0.5: "1/8",
            0.25: "1/16",
            0.125: "1/32",
            0.0625: "1/64"
        }
        
        div_text = divisions.get(division, f"{division}")
        swing_text = f" with swing: {swing:.0%}" if swing != 0 else ""
        
        return f"Set grid division to {div_text}{swing_text}"
    else:
        raise Exception(f"Failed to set grid division: {result.get('error', 'Unknown error')}")


# ============================================================================
# Project Notes & Metadata (2 tools)
# ============================================================================

async def get_project_notes() -> str:
    """Get the project notes"""
    result = await bridge.call_lua("GetSetProjectNotes", [0, False, ""])
    
    if result.get("ok"):
        notes = result.get("ret", "")
        if notes:
            # Limit length for display
            if len(notes) > 500:
                notes = notes[:497] + "..."
            return f"Project notes:\n{notes}"
        else:
            return "Project has no notes"
    else:
        raise Exception(f"Failed to get project notes: {result.get('error', 'Unknown error')}")


async def set_project_notes(notes: str) -> str:
    """Set the project notes"""
    result = await bridge.call_lua("GetSetProjectNotes", [0, True, notes])
    
    if result.get("ok"):
        return "Project notes updated"
    else:
        raise Exception(f"Failed to set project notes: {result.get('error', 'Unknown error')}")


# ============================================================================
# Rendering & Export (2 tools)
# ============================================================================

async def get_project_render_bounds() -> str:
    """Get the project render bounds mode"""
    result = await bridge.call_lua("GetSetProjectInfo", [0, "RENDER_SETTINGS", 0, False])
    
    if result.get("ok"):
        settings = int(result.get("ret", 0))
        
        # Extract render bounds from settings (bits 0-3)
        bounds = settings & 0xF
        
        bounds_names = {
            0: "Custom time range",
            1: "Entire project", 
            2: "Time selection",
            3: "Project regions",
            4: "Selected media items",
            5: "Selected regions"
        }
        
        bounds_name = bounds_names.get(bounds, f"Unknown ({bounds})")
        return f"Render bounds: {bounds_name}"
    else:
        raise Exception(f"Failed to get render bounds: {result.get('error', 'Unknown error')}")




# ============================================================================
# Registration Function
# ============================================================================

def register_project_tools(mcp) -> int:
    """Register all project management tools with the MCP instance"""
    tools = [
        # Basic Project Management
        (get_project_name, "Get the current project name"),
        (get_project_path, "Get the current project path"),
        (save_project, "Save the current project"),
        (open_project, "Open a REAPER project file"),
        (close_project, "Close the current project"),
        (mark_project_dirty, "Mark the project as having unsaved changes"),
        
        # Project Instance Management
        (enum_projects, "Get information about all open projects"),
        (select_project_instance, "Switch to a specific project by index"),
        (get_current_project_index, "Get the index of the currently active project"),
        
        # Project Properties
        (get_project_length, "Get the project length in seconds"),
        (set_project_length, "Set the project length in seconds"),
        (get_project_tempo, "Get the current project tempo in BPM"),
        (set_project_tempo, "Set the project tempo in BPM"),
        (get_project_time_signature, "Get the current project time signature"),
        (set_project_time_signature, "Set the project time signature"),
        (get_project_sample_rate, "Get the project sample rate"),
        (set_project_sample_rate, "Set the project sample rate"),
        
        # Project Grid & Display
        (get_project_grid_division, "Get the project grid division"),
        (set_project_grid_division, "Set the project grid division"),
        
        # Project Notes & Metadata
        (get_project_notes, "Get the project notes"),
        (set_project_notes, "Set the project notes"),
        
        # Rendering & Export
        (get_project_render_bounds, "Get the project render bounds mode"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)