"""
Project Tab Management Tools for REAPER MCP

This module contains tools for managing project tabs, switching between projects,
and handling multiple project contexts - useful for AI agents working across projects.
"""

from typing import List, Dict, Any, Optional
import os
from ..bridge import bridge


# ============================================================================
# Project Tab Navigation
# ============================================================================

async def get_project_tab_count() -> str:
    """Get the number of open project tabs"""
    # Count project tabs by checking valid projects
    count = 0
    for i in range(100):  # Check up to 100 tabs
        result = await bridge.call_lua("ValidatePtr", [i, "ReaProject*"])
        if result.get("ok") and result.get("ret"):
            count += 1
        else:
            break
    
    return f"Open project tabs: {count}"


async def get_current_project_tab() -> str:
    """Get the current active project tab index"""
    # Get current project
    current_result = await bridge.call_lua("GetCurrentProjectInLoadSave", [])
    if current_result.get("ok"):
        current_proj = current_result.get("ret")
        
        # Find its index
        for i in range(100):
            proj_result = await bridge.call_lua("ValidatePtr", [i, "ReaProject*"])
            if proj_result.get("ok") and proj_result.get("ret") == current_proj:
                return f"Current project tab: {i}"
        
        return "Current project tab: 0 (default)"
    
    raise Exception("Failed to get current project")


async def switch_to_project_tab(tab_index: int) -> str:
    """Switch to a specific project tab"""
    # Use action to switch tabs
    # 40859 + tab_index for tabs 0-9
    if 0 <= tab_index <= 9:
        action_id = 40859 + tab_index
        result = await bridge.call_lua("Main_OnCommand", [action_id, 0])
        if result.get("ok"):
            return f"Switched to project tab {tab_index}"
    else:
        return f"Invalid tab index {tab_index}. Must be 0-9"
    
    raise Exception("Failed to switch project tab")


async def next_project_tab() -> str:
    """Switch to the next project tab"""
    result = await bridge.call_lua("Main_OnCommand", [40861, 0])  # Next project tab
    if result.get("ok"):
        return "Switched to next project tab"
    
    raise Exception("Failed to switch to next tab")


async def previous_project_tab() -> str:
    """Switch to the previous project tab"""
    result = await bridge.call_lua("Main_OnCommand", [40862, 0])  # Previous project tab
    if result.get("ok"):
        return "Switched to previous project tab"
    
    raise Exception("Failed to switch to previous tab")


# ============================================================================
# Project Tab Management
# ============================================================================

async def new_project_tab() -> str:
    """Create a new project tab"""
    result = await bridge.call_lua("Main_OnCommand", [40859, 0])  # File: New project tab
    if result.get("ok"):
        return "Created new project tab"
    
    raise Exception("Failed to create new project tab")


async def close_current_project_tab() -> str:
    """Close the current project tab"""
    result = await bridge.call_lua("Main_OnCommand", [40860, 0])  # File: Close current project tab
    if result.get("ok"):
        return "Closed current project tab"
    
    raise Exception("Failed to close project tab")


async def save_project_tab(tab_index: Optional[int] = None) -> str:
    """Save a specific project tab or current if not specified"""
    if tab_index is not None:
        # Switch to tab first
        await switch_to_project_tab(tab_index)
    
    # Save project
    result = await bridge.call_lua("Main_SaveProject", [0, 0])
    if result.get("ok"):
        return f"Saved project{f' tab {tab_index}' if tab_index is not None else ''}"
    
    raise Exception("Failed to save project")


# ============================================================================
# Project Tab Information
# ============================================================================

async def get_project_tab_name(tab_index: Optional[int] = None) -> str:
    """Get the name/path of a project tab"""
    if tab_index is not None:
        # Switch to tab first
        await switch_to_project_tab(tab_index)
    
    # Get project filename
    result = await bridge.call_lua("GetProjectName", [0, ""])
    if result.get("ok"):
        filename = result.get("ret", "")
        if filename:
            import os
            name = os.path.basename(filename)
            return f"Project tab{f' {tab_index}' if tab_index is not None else ''}: {name}"
        else:
            return f"Project tab{f' {tab_index}' if tab_index is not None else ''}: [Untitled]"
    
    raise Exception("Failed to get project name")


async def get_all_project_tabs_info() -> str:
    """Get information about all open project tabs"""
    tabs_info = []
    
    # Save current project
    current_result = await bridge.call_lua("GetCurrentProjectInLoadSave", [])
    current_proj = current_result.get("ret") if current_result.get("ok") else None
    
    for i in range(10):  # Check first 10 possible tabs
        # Try to validate project pointer
        proj_result = await bridge.call_lua("ValidatePtr", [i, "ReaProject*"])
        if proj_result.get("ok") and proj_result.get("ret"):
            # Get project name
            await switch_to_project_tab(i)
            name_result = await bridge.call_lua("GetProjectName", [0, ""])
            
            if name_result.get("ok"):
                filename = name_result.get("ret", "")
                name = os.path.basename(filename) if filename else "[Untitled]"
                is_current = "→" if i == 0 else " "  # Simple current indicator
                tabs_info.append(f"{is_current} Tab {i}: {name}")
        else:
            break
    
    if tabs_info:
        return "Open project tabs:\n" + "\n".join(tabs_info)
    else:
        return "No project tabs found"


async def is_project_tab_modified(tab_index: Optional[int] = None) -> str:
    """Check if a project tab has unsaved changes"""
    if tab_index is not None:
        # Switch to tab first
        await switch_to_project_tab(tab_index)
    
    # Check if project is dirty
    result = await bridge.call_lua("IsProjectDirty", [0])
    if result.get("ok"):
        is_dirty = result.get("ret", 0)
        status = "has unsaved changes" if is_dirty else "is saved"
        return f"Project tab{f' {tab_index}' if tab_index is not None else ''} {status}"
    
    raise Exception("Failed to check project status")


# ============================================================================
# Cross-Project Operations
# ============================================================================

async def copy_tracks_to_project_tab(source_tab: int, dest_tab: int, 
                                     track_indices: List[int]) -> str:
    """Copy tracks from one project tab to another"""
    # Switch to source tab
    await switch_to_project_tab(source_tab)
    
    # Select tracks
    for idx in track_indices:
        track_result = await bridge.call_lua("GetTrack", [0, idx])
        if track_result.get("ok"):
            await bridge.call_lua("SetTrackSelected", [track_result.get("ret"), True])
    
    # Copy tracks
    await bridge.call_lua("Main_OnCommand", [40210, 0])  # Track: Copy tracks
    
    # Switch to destination tab
    await switch_to_project_tab(dest_tab)
    
    # Paste tracks
    await bridge.call_lua("Main_OnCommand", [40211, 0])  # Track: Paste tracks
    
    return f"Copied {len(track_indices)} tracks from tab {source_tab} to tab {dest_tab}"


async def import_project_as_tab(project_path: str) -> str:
    """Import a project file as a new tab"""
    # Open project in new tab
    result = await bridge.call_lua("Main_openProject", [project_path])
    if result.get("ok"):
        return f"Imported project as new tab: {os.path.basename(project_path)}"
    
    raise Exception(f"Failed to import project: {project_path}")


# ============================================================================
# Project Tab Settings
# ============================================================================

async def set_project_tab_color(tab_index: int, color: int) -> str:
    """Set a color for a project tab (for visual organization)"""
    # Store in extended state
    result = await bridge.call_lua("SetExtState", 
                                  ["ProjectTabs", f"tab_{tab_index}_color", str(color), True])
    if result.get("ok"):
        # Convert color to hex for display
        hex_color = f"#{color:06X}"
        return f"Set project tab {tab_index} color to {hex_color}"
    
    raise Exception("Failed to set tab color")


async def get_project_tab_notes(tab_index: Optional[int] = None) -> str:
    """Get notes/description for a project tab"""
    if tab_index is not None:
        # Switch to tab first
        await switch_to_project_tab(tab_index)
    
    # Get project notes
    result = await bridge.call_lua("GetProjectNotes", [0])
    if result.get("ok"):
        notes = result.get("ret", "")
        if notes:
            return f"Project tab{f' {tab_index}' if tab_index is not None else ''} notes:\n{notes}"
        else:
            return f"Project tab{f' {tab_index}' if tab_index is not None else ''} has no notes"
    
    raise Exception("Failed to get project notes")


async def set_project_tab_notes(notes: str, tab_index: Optional[int] = None) -> str:
    """Set notes/description for a project tab"""
    if tab_index is not None:
        # Switch to tab first
        await switch_to_project_tab(tab_index)
    
    # Set project notes
    result = await bridge.call_lua("SetProjectNotes", [0, notes])
    if result.get("ok"):
        return f"Set project tab{f' {tab_index}' if tab_index is not None else ''} notes"
    
    raise Exception("Failed to set project notes")


# ============================================================================
# Project Tab Workflow
# ============================================================================

async def save_all_project_tabs() -> str:
    """Save all open project tabs"""
    saved_count = 0
    
    for i in range(10):  # Check first 10 tabs
        # Try to switch to tab
        try:
            await switch_to_project_tab(i)
            # Check if project needs saving
            dirty_result = await bridge.call_lua("IsProjectDirty", [0])
            if dirty_result.get("ok") and dirty_result.get("ret"):
                # Save project
                save_result = await bridge.call_lua("Main_SaveProject", [0, 0])
                if save_result.get("ok"):
                    saved_count += 1
        except:
            break  # No more tabs
    
    return f"Saved {saved_count} project tabs"


async def close_all_project_tabs_except_current() -> str:
    """Close all project tabs except the current one"""
    # Get current project
    current_result = await bridge.call_lua("GetCurrentProjectInLoadSave", [])
    current_proj = current_result.get("ret") if current_result.get("ok") else None
    
    closed_count = 0
    
    # Close other tabs (go backwards to avoid index shifting)
    for i in range(9, -1, -1):
        proj_result = await bridge.call_lua("ValidatePtr", [i, "ReaProject*"])
        if proj_result.get("ok") and proj_result.get("ret"):
            if proj_result.get("ret") != current_proj:
                await switch_to_project_tab(i)
                await bridge.call_lua("Main_OnCommand", [40860, 0])  # Close tab
                closed_count += 1
    
    return f"Closed {closed_count} project tabs"


# ============================================================================
# Registration Function
# ============================================================================

def register_project_tabs_tools(mcp) -> int:
    """Register all project tab tools with the MCP instance"""
    tools = [
        # Project Tab Navigation
        (get_project_tab_count, "Get the number of open project tabs"),
        (get_current_project_tab, "Get the current active project tab index"),
        (switch_to_project_tab, "Switch to a specific project tab"),
        (next_project_tab, "Switch to the next project tab"),
        (previous_project_tab, "Switch to the previous project tab"),
        
        # Project Tab Management
        (new_project_tab, "Create a new project tab"),
        (close_current_project_tab, "Close the current project tab"),
        (save_project_tab, "Save a specific project tab"),
        
        # Project Tab Information
        (get_project_tab_name, "Get the name/path of a project tab"),
        (get_all_project_tabs_info, "Get information about all open project tabs"),
        (is_project_tab_modified, "Check if a project tab has unsaved changes"),
        
        # Cross-Project Operations
        (copy_tracks_to_project_tab, "Copy tracks from one project tab to another"),
        (import_project_as_tab, "Import a project file as a new tab"),
        
        # Project Tab Settings
        (set_project_tab_color, "Set a color for a project tab"),
        (get_project_tab_notes, "Get notes/description for a project tab"),
        (set_project_tab_notes, "Set notes/description for a project tab"),
        
        # Project Tab Workflow
        (save_all_project_tabs, "Save all open project tabs"),
        (close_all_project_tabs_except_current, "Close all tabs except current"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)