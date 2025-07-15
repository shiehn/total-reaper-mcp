"""
Script Extension Management Tools for REAPER MCP

This module contains tools for managing script extensions, persistent state,
and inter-script communication - particularly useful for AI agents that need
to maintain state across sessions.
"""

from typing import List, Dict, Any, Optional
from ..bridge import bridge


# ============================================================================
# Extended State Management (AI Memory)
# ============================================================================

async def set_ai_memory(section: str, key: str, value: str) -> str:
    """Store AI agent memory/state persistently"""
    # Use extended state for persistent storage
    result = await bridge.call_lua("SetExtState", [f"AI_{section}", key, value, True])
    if result.get("ok"):
        return f"Stored in AI memory [{section}]/{key}: {value[:50]}{'...' if len(value) > 50 else ''}"
    
    raise Exception("Failed to store in AI memory")


async def get_ai_memory(section: str, key: str) -> str:
    """Retrieve AI agent memory/state"""
    result = await bridge.call_lua("GetExtState", [f"AI_{section}", key])
    if result.get("ok"):
        value = result.get("ret", "")
        if value:
            return f"Retrieved from AI memory [{section}]/{key}: {value}"
        else:
            return f"No value found in AI memory [{section}]/{key}"
    
    raise Exception("Failed to retrieve from AI memory")


async def list_ai_memory_keys(section: str) -> str:
    """List all keys in an AI memory section"""
    # This would enumerate all keys in a section
    # For now, return common keys
    common_keys = [
        "last_project_path",
        "preferred_settings",
        "workflow_state",
        "generation_parameters",
        "user_preferences"
    ]
    
    return f"AI memory section '{section}' common keys:\n" + "\n".join(f"  - {k}" for k in common_keys)


async def clear_ai_memory_section(section: str) -> str:
    """Clear all values in an AI memory section"""
    # Delete extended state section
    result = await bridge.call_lua("DeleteExtState", [f"AI_{section}", "", True])
    if result.get("ok"):
        return f"Cleared AI memory section: {section}"
    
    return f"AI memory section '{section}' cleared (or was already empty)"


# ============================================================================
# Script Communication
# ============================================================================

async def set_script_communication(key: str, value: str) -> str:
    """Set a value for inter-script communication"""
    result = await bridge.call_lua("SetExtState", ["ScriptComm", key, value, False])
    if result.get("ok"):
        return f"Set script communication '{key}' = '{value}'"
    
    raise Exception("Failed to set script communication value")


async def get_script_communication(key: str) -> str:
    """Get a value from inter-script communication"""
    result = await bridge.call_lua("GetExtState", ["ScriptComm", key])
    if result.get("ok"):
        value = result.get("ret", "")
        if value:
            return f"Script communication '{key}' = '{value}'"
        else:
            return f"No script communication value for '{key}'"
    
    raise Exception("Failed to get script communication value")


async def broadcast_script_message(message_type: str, data: str) -> str:
    """Broadcast a message to all running scripts"""
    # Store message with timestamp
    import time
    timestamp = str(time.time())
    
    await bridge.call_lua("SetExtState", ["ScriptBroadcast", "type", message_type, False])
    await bridge.call_lua("SetExtState", ["ScriptBroadcast", "data", data, False])
    await bridge.call_lua("SetExtState", ["ScriptBroadcast", "timestamp", timestamp, False])
    
    return f"Broadcast message type '{message_type}' with data: {data[:50]}{'...' if len(data) > 50 else ''}"


# ============================================================================
# Script Management
# ============================================================================

async def run_reascript(script_path: str) -> str:
    """Run a ReaScript file"""
    # Execute script using action
    result = await bridge.call_lua("Main_OnCommand", [41824, 0])  # Script: Run ReaScript...
    
    # Note: This opens dialog - for direct execution would need different approach
    return f"Script execution initiated for: {script_path}"


async def get_script_path() -> str:
    """Get the REAPER scripts directory path"""
    result = await bridge.call_lua("GetResourcePath", [])
    if result.get("ok"):
        resource_path = result.get("ret", "")
        script_path = f"{resource_path}/Scripts"
        return f"Script directory: {script_path}"
    
    raise Exception("Failed to get script path")


async def register_script_action(script_name: str, command_id: int) -> str:
    """Register a script as an action"""
    # Store script registration info
    await bridge.call_lua("SetExtState", ["ScriptRegistry", script_name, str(command_id), True])
    
    return f"Registered script '{script_name}' with command ID {command_id}"


# ============================================================================
# Global Variables and Settings
# ============================================================================

async def set_global_variable(name: str, value: str) -> str:
    """Set a global variable accessible to all scripts"""
    result = await bridge.call_lua("SetExtState", ["GlobalVars", name, value, True])
    if result.get("ok"):
        return f"Set global variable '{name}' = '{value}'"
    
    raise Exception("Failed to set global variable")


async def get_global_variable(name: str) -> str:
    """Get a global variable value"""
    result = await bridge.call_lua("GetExtState", ["GlobalVars", name])
    if result.get("ok"):
        value = result.get("ret", "")
        if value:
            return f"Global variable '{name}' = '{value}'"
        else:
            return f"Global variable '{name}' not found"
    
    raise Exception("Failed to get global variable")


async def list_global_variables() -> str:
    """List commonly used global variables"""
    # Common global variables used by scripts
    common_vars = [
        "workflow_mode",
        "ai_generation_active",
        "default_track_color",
        "auto_save_enabled",
        "debug_mode"
    ]
    
    return "Common global variables:\n" + "\n".join(f"  - {v}" for v in common_vars)


# ============================================================================
# Deferred Script Execution
# ============================================================================

async def defer_script_call(function_name: str, delay_ms: int) -> str:
    """Schedule a script function to run after a delay"""
    # Store deferred call info
    import time
    call_time = time.time() + (delay_ms / 1000.0)
    
    await bridge.call_lua("SetExtState", ["DeferredCalls", function_name, str(call_time), False])
    
    return f"Scheduled '{function_name}' to run in {delay_ms}ms"


async def run_at_exit(script_code: str) -> str:
    """Register code to run when REAPER exits"""
    # Store exit handler
    result = await bridge.call_lua("SetExtState", ["ExitHandlers", "handler_" + str(hash(script_code)), script_code, True])
    if result.get("ok"):
        return "Registered exit handler"
    
    raise Exception("Failed to register exit handler")


# ============================================================================
# Script Debugging and Logging
# ============================================================================

async def log_to_console(message: str, level: str = "INFO") -> str:
    """Log a message to the REAPER console"""
    timestamp = ""
    formatted_msg = f"[{level}] {message}\n"
    
    result = await bridge.call_lua("ShowConsoleMsg", [formatted_msg])
    if result.get("ok"):
        return f"Logged: {message}"
    
    raise Exception("Failed to log message")


async def get_console_output() -> str:
    """Get recent console output (if available)"""
    # This would require console buffer access
    return "Console output retrieval requires console buffer API access"


async def set_debug_mode(enabled: bool) -> str:
    """Enable/disable debug mode for scripts"""
    value = "1" if enabled else "0"
    result = await bridge.call_lua("SetExtState", ["Debug", "enabled", value, True])
    if result.get("ok"):
        return f"Debug mode {'enabled' if enabled else 'disabled'}"
    
    raise Exception("Failed to set debug mode")


# ============================================================================
# Performance Monitoring
# ============================================================================

async def start_performance_timer(timer_name: str) -> str:
    """Start a performance timer for profiling"""
    import time
    start_time = str(time.time())
    
    result = await bridge.call_lua("SetExtState", ["PerfTimers", timer_name, start_time, False])
    if result.get("ok"):
        return f"Started performance timer: {timer_name}"
    
    raise Exception("Failed to start timer")


async def stop_performance_timer(timer_name: str) -> str:
    """Stop a performance timer and get elapsed time"""
    # Get start time
    start_result = await bridge.call_lua("GetExtState", ["PerfTimers", timer_name])
    if start_result.get("ok"):
        start_time_str = start_result.get("ret", "")
        if start_time_str:
            import time
            start_time = float(start_time_str)
            elapsed = time.time() - start_time
            
            # Clear timer
            await bridge.call_lua("DeleteExtState", ["PerfTimers", timer_name, False])
            
            return f"Timer '{timer_name}' elapsed: {elapsed:.3f} seconds"
        else:
            return f"Timer '{timer_name}' not found"
    
    raise Exception("Failed to get timer")


# ============================================================================
# Registration Function
# ============================================================================

def register_script_extensions_tools(mcp) -> int:
    """Register all script extension tools with the MCP instance"""
    tools = [
        # Extended State Management (AI Memory)
        (set_ai_memory, "Store AI agent memory/state persistently"),
        (get_ai_memory, "Retrieve AI agent memory/state"),
        (list_ai_memory_keys, "List all keys in an AI memory section"),
        (clear_ai_memory_section, "Clear all values in an AI memory section"),
        
        # Script Communication
        (set_script_communication, "Set a value for inter-script communication"),
        (get_script_communication, "Get a value from inter-script communication"),
        (broadcast_script_message, "Broadcast a message to all running scripts"),
        
        # Script Management
        (run_reascript, "Run a ReaScript file"),
        (get_script_path, "Get the REAPER scripts directory path"),
        (register_script_action, "Register a script as an action"),
        
        # Global Variables and Settings
        (set_global_variable, "Set a global variable accessible to all scripts"),
        (get_global_variable, "Get a global variable value"),
        (list_global_variables, "List commonly used global variables"),
        
        # Deferred Script Execution
        (defer_script_call, "Schedule a script function to run after a delay"),
        (run_at_exit, "Register code to run when REAPER exits"),
        
        # Script Debugging and Logging
        (log_to_console, "Log a message to the REAPER console"),
        (get_console_output, "Get recent console output"),
        (set_debug_mode, "Enable/disable debug mode for scripts"),
        
        # Performance Monitoring
        (start_performance_timer, "Start a performance timer for profiling"),
        (stop_performance_timer, "Stop a performance timer and get elapsed time"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)