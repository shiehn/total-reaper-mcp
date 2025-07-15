"""
Action Management Tools for REAPER MCP

This module contains tools for managing REAPER actions, commands, and shortcuts.
"""

from ..bridge import bridge


# ============================================================================
# Action Lookup and Information
# ============================================================================

async def named_command_lookup(command_name: str) -> str:
    """Look up a named command and return its command ID"""
    result = await bridge.call_lua("NamedCommandLookup", [command_name])
    
    if result.get("ok"):
        command_id = result.get("ret", 0)
        if command_id > 0:
            return f"Command '{command_name}' has ID: {command_id}"
        else:
            return f"Command '{command_name}' not found"
    else:
        raise Exception("Failed to look up command")


async def reverse_named_command_lookup(command_id: int, section_id: int = 0) -> str:
    """Get the name of a command from its ID"""
    result = await bridge.call_lua("ReverseNamedCommandLookup", [command_id, section_id])
    
    if result.get("ok"):
        command_name = result.get("ret", "")
        if command_name:
            return f"Command ID {command_id} is: {command_name}"
        else:
            return f"No command name found for ID {command_id}"
    else:
        raise Exception("Failed to reverse lookup command")


async def get_toggle_command_state_ex(section_id: int, command_id: int) -> str:
    """Get toggle command state for a specific section"""
    result = await bridge.call_lua("GetToggleCommandStateEx", [section_id, command_id])
    
    if result.get("ok"):
        state = result.get("ret", -1)
        if state == 1:
            return f"Toggle command {command_id} in section {section_id}: ON"
        elif state == 0:
            return f"Toggle command {command_id} in section {section_id}: OFF"
        else:
            return f"Toggle command {command_id} in section {section_id}: Not found or not a toggle"
    else:
        raise Exception("Failed to get toggle command state")


# ============================================================================
# Keyboard Shortcuts
# ============================================================================

async def count_action_shortcuts(section: int, command_id: int) -> str:
    """Count the number of shortcuts for an action"""
    result = await bridge.call_lua("CountActionShortcuts", [section, command_id])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"Action {command_id} in section {section} has {count} shortcuts"
    else:
        raise Exception("Failed to count action shortcuts")


async def get_action_shortcut_desc(section: int, command_id: int, shortcut_index: int) -> str:
    """Get the description of a specific shortcut for an action"""
    result = await bridge.call_lua("GetActionShortcutDesc", [section, command_id, shortcut_index])
    
    if result.get("ok"):
        desc = result.get("desc", "")
        if desc:
            return f"Shortcut {shortcut_index} for action {command_id}: {desc}"
        else:
            return f"No shortcut found at index {shortcut_index} for action {command_id}"
    else:
        raise Exception("Failed to get action shortcut description")


async def delete_action_shortcut(section: int, command_id: int, shortcut_index: int) -> str:
    """Delete a specific shortcut for an action"""
    result = await bridge.call_lua("DeleteActionShortcut", [section, command_id, shortcut_index])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Deleted shortcut {shortcut_index} for action {command_id}"
        else:
            return f"Failed to delete shortcut {shortcut_index} for action {command_id}"
    else:
        raise Exception("Failed to delete action shortcut")


async def do_action_shortcut_dialog(hwnd: int, section: int, command_id: int, shortcut_index: int) -> str:
    """Open the action shortcut dialog for a specific action"""
    result = await bridge.call_lua("DoActionShortcutDialog", [hwnd, section, command_id, shortcut_index])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Opened shortcut dialog for action {command_id}"
        else:
            return f"Failed to open shortcut dialog for action {command_id}"
    else:
        raise Exception("Failed to open action shortcut dialog")


# ============================================================================
# Toolbar and UI Updates
# ============================================================================

async def refresh_toolbar(command_id: int) -> str:
    """Refresh toolbar button states"""
    result = await bridge.call_lua("RefreshToolbar", [command_id])
    
    if result.get("ok"):
        return f"Refreshed toolbar for command {command_id}"
    else:
        raise Exception("Failed to refresh toolbar")


async def refresh_toolbar2(section_id: int, command_id: int) -> str:
    """Refresh toolbar button states for a specific section"""
    result = await bridge.call_lua("RefreshToolbar2", [section_id, command_id])
    
    if result.get("ok"):
        return f"Refreshed toolbar for command {command_id} in section {section_id}"
    else:
        raise Exception("Failed to refresh toolbar")


# ============================================================================
# Section Information
# ============================================================================

async def section_from_unique_id(unique_id: int) -> str:
    """Get section ID from unique command ID"""
    result = await bridge.call_lua("SectionFromUniqueID", [unique_id])
    
    if result.get("ok"):
        section = result.get("ret", -1)
        section_names = {
            0: "Main",
            100: "Main (alt recording)",
            32060: "MIDI Editor",
            32061: "MIDI Event List Editor",
            32062: "MIDI Inline Editor",
            32063: "Media Explorer"
        }
        section_name = section_names.get(section, f"Section {section}")
        return f"Unique ID {unique_id} belongs to: {section_name}"
    else:
        raise Exception("Failed to get section from unique ID")


# ============================================================================
# Registration Function
# ============================================================================

def register_action_management_tools(mcp) -> int:
    """Register all action management tools with the MCP instance"""
    tools = [
        # Action Lookup
        (named_command_lookup, "Look up a named command and return its command ID"),
        (reverse_named_command_lookup, "Get the name of a command from its ID"),
        (get_toggle_command_state_ex, "Get toggle command state for a specific section"),
        
        # Shortcuts
        (count_action_shortcuts, "Count the number of shortcuts for an action"),
        (get_action_shortcut_desc, "Get the description of a specific shortcut"),
        (delete_action_shortcut, "Delete a specific shortcut for an action"),
        (do_action_shortcut_dialog, "Open the action shortcut dialog"),
        
        # UI Updates
        (refresh_toolbar, "Refresh toolbar button states"),
        (refresh_toolbar2, "Refresh toolbar button states for a specific section"),
        
        # Section Info
        (section_from_unique_id, "Get section ID from unique command ID"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)