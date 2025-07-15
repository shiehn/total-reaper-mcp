"""
File I/O and Project Management Tools for REAPER MCP

This module contains tools for file operations, project management, and settings.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# File and Directory Operations
# ============================================================================

async def enumerate_files(path: str, file_index: int) -> str:
    """Enumerate files in a directory"""
    result = await bridge.call_lua("EnumerateFiles", [path, file_index])
    
    if result.get("ok"):
        filename = result.get("ret", "")
        if filename:
            return f"File {file_index}: {filename}"
        else:
            return f"No file at index {file_index} in {path}"
    else:
        raise Exception("Failed to enumerate files")


async def enumerate_subdirectories(path: str, subdirs_index: int) -> str:
    """Enumerate subdirectories in a directory"""
    result = await bridge.call_lua("EnumerateSubdirectories", [path, subdirs_index])
    
    if result.get("ok"):
        dirname = result.get("ret", "")
        if dirname:
            return f"Subdirectory {subdirs_index}: {dirname}"
        else:
            return f"No subdirectory at index {subdirs_index} in {path}"
    else:
        raise Exception("Failed to enumerate subdirectories")


async def file_exists(filename: str) -> str:
    """Check if a file exists"""
    result = await bridge.call_lua("file_exists", [filename])
    
    if result.get("ok"):
        exists = result.get("ret", False)
        return f"File '{filename}' {'exists' if exists else 'does not exist'}"
    else:
        raise Exception("Failed to check file existence")


async def recursive_create_directory(path: str, ignored: int = 0) -> str:
    """Recursively create a directory"""
    result = await bridge.call_lua("RecursiveCreateDirectory", [path, ignored])
    
    if result.get("ok"):
        return f"Created directory: {path}"
    else:
        raise Exception(f"Failed to create directory: {path}")


# ============================================================================
# Project Paths and Information
# ============================================================================

async def get_project_path(project_index: int = 0) -> str:
    """Get the path of a project"""
    result = await bridge.call_lua("GetProjectPath", [project_index])
    
    if result.get("ok"):
        path = result.get("ret", "")
        if path:
            return f"Project path: {path}"
        else:
            return "Project is unsaved (no path)"
    else:
        raise Exception("Failed to get project path")


async def get_project_path_ex(project_index: int = 0) -> str:
    """Get the path of a project with size information"""
    result = await bridge.call_lua("GetProjectPathEx", [project_index])
    
    if result.get("ok"):
        path = result.get("path", "")
        if path:
            return f"Project path: {path}"
        else:
            return "Project is unsaved (no path)"
    else:
        raise Exception("Failed to get project path")


async def get_project_name(project_index: int = 0) -> str:
    """Get the name of a project"""
    result = await bridge.call_lua("GetProjectName", [project_index])
    
    if result.get("ok"):
        name = result.get("ret", "")
        if name:
            return f"Project name: {name}"
        else:
            return "Untitled project"
    else:
        raise Exception("Failed to get project name")


async def is_project_dirty(project_index: int = 0) -> str:
    """Check if project has unsaved changes"""
    result = await bridge.call_lua("IsProjectDirty", [project_index])
    
    if result.get("ok"):
        dirty = result.get("ret", 0)
        if dirty == 0:
            return "Project has no unsaved changes"
        elif dirty == 1:
            return "Project has unsaved changes"
        else:
            return "Undo state has unsaved changes"
    else:
        raise Exception("Failed to check project dirty state")


async def get_project_state_change_count(project_index: int = 0) -> str:
    """Get the project state change count (increments on each change)"""
    result = await bridge.call_lua("GetProjectStateChangeCount", [project_index])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Project state change count: {count}"
    else:
        raise Exception("Failed to get project state change count")


# ============================================================================
# REAPER Paths and Information
# ============================================================================

async def get_resource_path() -> str:
    """Get the REAPER resource path"""
    result = await bridge.call_lua("GetResourcePath", [])
    
    if result.get("ok"):
        path = result.get("ret", "")
        return f"REAPER resource path: {path}"
    else:
        raise Exception("Failed to get resource path")


async def get_exe_dir() -> str:
    """Get the REAPER executable directory"""
    result = await bridge.call_lua("GetExePath", [])
    
    if result.get("ok"):
        path = result.get("ret", "")
        return f"REAPER executable directory: {path}"
    else:
        raise Exception("Failed to get executable directory")


async def get_ini_file() -> str:
    """Get the REAPER.ini file path"""
    result = await bridge.call_lua("get_ini_file", [])
    
    if result.get("ok"):
        path = result.get("ret", "")
        return f"REAPER.ini path: {path}"
    else:
        raise Exception("Failed to get ini file path")


# ============================================================================
# Project Notes
# ============================================================================

async def get_set_project_notes(project_index: int, set_notes: bool, notes: str = "") -> str:
    """Get or set project notes"""
    result = await bridge.call_lua("GetSetProjectNotes", [project_index, set_notes, notes])
    
    if result.get("ok"):
        if set_notes:
            return "Project notes updated"
        else:
            notes = result.get("ret", "")
            if notes:
                return f"Project notes:\n{notes}"
            else:
                return "No project notes"
    else:
        raise Exception("Failed to get/set project notes")


# ============================================================================
# Project Info
# ============================================================================

async def get_set_project_info(project_index: int, desc: str, value: float, is_set: bool) -> str:
    """Get or set project information (numeric values)"""
    result = await bridge.call_lua("GetSetProjectInfo", [project_index, desc, value, is_set])
    
    if result.get("ok"):
        if is_set:
            return f"Set project {desc} to {value}"
        else:
            ret_value = result.get("ret", 0.0)
            return f"Project {desc}: {ret_value}"
    else:
        raise Exception(f"Failed to get/set project info: {desc}")


async def get_set_project_info_string(project_index: int, desc: str, value: str, is_set: bool) -> str:
    """Get or set project information (string values)"""
    result = await bridge.call_lua("GetSetProjectInfo_String", [project_index, desc, value, is_set])
    
    if result.get("ok"):
        if is_set:
            return f"Set project {desc} to: {value}"
        else:
            ret_value = result.get("ret", "")
            return f"Project {desc}: {ret_value}"
    else:
        raise Exception(f"Failed to get/set project info string: {desc}")


# ============================================================================
# User Input/Output
# ============================================================================

async def show_console_msg(message: str) -> str:
    """Show a message in the console"""
    result = await bridge.call_lua("ShowConsoleMsg", [message])
    
    if result.get("ok"):
        return f"Console message: {message}"
    else:
        raise Exception("Failed to show console message")


async def get_user_inputs(title: str, num_inputs: int, captions: str, initial_values: str) -> str:
    """Get multiple user inputs via dialog"""
    result = await bridge.call_lua("GetUserInputs", [title, num_inputs, captions, initial_values])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            values = result.get("values", "")
            return f"User input: {values}"
        else:
            return "User cancelled input dialog"
    else:
        raise Exception("Failed to get user inputs")


# ============================================================================
# Script State Management
# ============================================================================

async def get_ext_state(section: str, key: str) -> str:
    """Get extended state value"""
    result = await bridge.call_lua("GetExtState", [section, key])
    
    if result.get("ok"):
        value = result.get("ret", "")
        if value:
            return f"ExtState [{section}][{key}]: {value}"
        else:
            return f"No ExtState value for [{section}][{key}]"
    else:
        raise Exception("Failed to get extended state")


async def set_ext_state(section: str, key: str, value: str, persist: bool) -> str:
    """Set extended state value"""
    result = await bridge.call_lua("SetExtState", [section, key, value, persist])
    
    if result.get("ok"):
        return f"Set ExtState [{section}][{key}] = {value} (persist: {persist})"
    else:
        raise Exception("Failed to set extended state")


async def has_ext_state(section: str, key: str) -> str:
    """Check if extended state exists"""
    result = await bridge.call_lua("HasExtState", [section, key])
    
    if result.get("ok"):
        exists = result.get("ret", False)
        return f"ExtState [{section}][{key}] {'exists' if exists else 'does not exist'}"
    else:
        raise Exception("Failed to check extended state")


async def delete_ext_state(section: str, key: str, persist: bool) -> str:
    """Delete extended state value"""
    result = await bridge.call_lua("DeleteExtState", [section, key, persist])
    
    if result.get("ok"):
        return f"Deleted ExtState [{section}][{key}] (persist: {persist})"
    else:
        raise Exception("Failed to delete extended state")


# ============================================================================
# Registration Function
# ============================================================================

def register_file_io_tools(mcp) -> int:
    """Register all file I/O and project management tools with the MCP instance"""
    tools = [
        # File Operations
        (enumerate_files, "Enumerate files in a directory"),
        (enumerate_subdirectories, "Enumerate subdirectories in a directory"),
        (file_exists, "Check if a file exists"),
        (recursive_create_directory, "Recursively create a directory"),
        
        # Project Paths
        (get_project_path, "Get the path of a project"),
        (get_project_path_ex, "Get the path of a project with size information"),
        (get_project_name, "Get the name of a project"),
        (is_project_dirty, "Check if project has unsaved changes"),
        (get_project_state_change_count, "Get the project state change count"),
        
        # REAPER Paths
        (get_resource_path, "Get the REAPER resource path"),
        (get_exe_dir, "Get the REAPER executable directory"),
        (get_ini_file, "Get the REAPER.ini file path"),
        
        # Project Notes and Info
        (get_set_project_notes, "Get or set project notes"),
        (get_set_project_info, "Get or set project information (numeric)"),
        (get_set_project_info_string, "Get or set project information (string)"),
        
        # User I/O
        (show_console_msg, "Show a message in the console"),
        (get_user_inputs, "Get multiple user inputs via dialog"),
        
        # Script State
        (get_ext_state, "Get extended state value"),
        (set_ext_state, "Set extended state value"),
        (has_ext_state, "Check if extended state exists"),
        (delete_ext_state, "Delete extended state value"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)