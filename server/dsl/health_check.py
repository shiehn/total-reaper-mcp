"""
Health check for DSL functions in the Lua bridge

This module checks if required DSL functions are available in the bridge
and provides helpful error messages if they're missing.
"""

import asyncio
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

# List of critical DSL functions that must be available
REQUIRED_DSL_FUNCTIONS = [
    "GetTrackInfo",
    "GetAllTracksInfo", 
    "SetTrackNotes",
    "GetCursorPosition",
    "GetTimeSelection",
    "SetTimeSelection",
    "GetLoopTimeRange",
    "BarsToTime",
    "CreateMIDIItem",
    "SetItemLoopSource",
    "Play",
    "Stop",
]

async def check_dsl_functions(bridge) -> Tuple[bool, List[str]]:
    """
    Check if DSL functions are available in the bridge.
    
    Returns:
        (all_available, missing_functions)
    """
    missing = []
    
    # Test a few critical functions
    test_functions = [
        ("GetAllTracksInfo", []),
        ("GetCursorPosition", []),
        ("BarsToTime", [1, 0.0]),
    ]
    
    for func_name, args in test_functions:
        try:
            result = await bridge.call_lua(func_name, args)
            if not result.get("ok") and "Unknown function" in result.get("error", ""):
                missing.append(func_name)
        except Exception as e:
            # Timeout or other error - assume function is missing
            logger.debug(f"Error checking {func_name}: {e}")
            missing.append(func_name)
    
    # If any test functions are missing, assume all DSL functions are missing
    all_available = len(missing) == 0
    
    return all_available, missing

async def verify_dsl_installation(bridge, profile_name: str, categories: List[str]) -> None:
    """
    Verify DSL functions are installed if using a DSL profile.
    
    Logs warnings if DSL functions are missing.
    """
    # Only check if profile includes DSL
    if categories and "DSL" not in categories:
        return
    
    logger.info("Checking DSL functions availability...")
    
    try:
        all_available, missing = await check_dsl_functions(bridge)
        
        if not all_available:
            logger.warning("=" * 60)
            logger.warning("⚠️  DSL FUNCTIONS NOT INSTALLED")
            logger.warning("=" * 60)
            logger.warning(f"Profile '{profile_name}' requires DSL functions in the Lua bridge.")
            logger.warning("")
            logger.warning("To fix this:")
            logger.warning("1. Copy DSL functions to REAPER:")
            logger.warning("   cp lua/mcp_bridge_dsl_functions.lua ~/Library/Application\\ Support/REAPER/Scripts/")
            logger.warning("")
            logger.warning("2. Update mcp_bridge_file_v2.lua to load DSL functions")
            logger.warning("   See: docs/DSL_INSTALLATION.md")
            logger.warning("")
            logger.warning(f"Missing functions detected: {', '.join(missing)}")
            logger.warning("")
            logger.warning("The server will start but DSL commands will fail!")
            logger.warning("=" * 60)
        else:
            logger.info("✅ DSL functions verified - all required functions available")
            
    except Exception as e:
        logger.warning(f"Could not verify DSL functions: {e}")
        logger.warning("Make sure REAPER is running with the bridge loaded")