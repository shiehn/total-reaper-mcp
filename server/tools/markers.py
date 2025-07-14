"""
Markers & Regions Tools for REAPER MCP

This module contains tools for managing markers and regions.
"""

from typing import Optional
from ..bridge import bridge


# ============================================================================
# Marker & Region Management (4 tools)
# ============================================================================

async def add_project_marker(is_region: bool, position: float, name: str, 
                            region_end: Optional[float] = None, want_index: int = -1) -> str:
    """Add a marker or region to the project"""
    if region_end is None:
        region_end = position
        
    result = await bridge.call_lua("AddProjectMarker", [0, is_region, position, region_end, name, want_index])
    
    if result.get("ok"):
        marker_type = "region" if is_region else "marker"
        index = result.get("ret", want_index)
        return f"Added {marker_type} '{name}' at {position:.3f}s (index: {index})"
    else:
        raise Exception(f"Failed to add marker/region: {result.get('error', 'Unknown error')}")


async def delete_project_marker(marker_index: int, is_region: bool) -> str:
    """Delete a marker or region by its displayed number"""
    result = await bridge.call_lua("DeleteProjectMarker", [0, marker_index, is_region])
    
    if result.get("ok"):
        marker_type = "region" if is_region else "marker"
        return f"Deleted {marker_type} {marker_index}"
    else:
        raise Exception(f"Failed to delete marker/region: {result.get('error', 'Unknown error')}")


async def count_project_markers() -> str:
    """Count the number of markers and regions in the project"""
    result = await bridge.call_lua("CountProjectMarkers", [0])
    
    if result.get("ok"):
        ret = result.get("ret", [0, 0])
        if isinstance(ret, list) and len(ret) >= 2:
            num_markers = ret[0]
            num_regions = ret[1]
            return f"Total markers/regions: {num_markers} markers, {num_regions} regions"
        else:
            return "Failed to count markers/regions: Invalid response"
    else:
        raise Exception(f"Failed to count markers/regions: {result.get('error', 'Unknown error')}")


async def enum_project_markers(marker_index: int) -> str:
    """Get information about a specific marker/region by its index"""
    result = await bridge.call_lua("EnumProjectMarkers", [marker_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 5:
            is_region = ret[1]
            position = ret[2]
            region_end = ret[3]
            name = ret[4]
            
            if is_region:
                return f"Region {marker_index}: '{name}' from {position:.3f}s to {region_end:.3f}s"
            else:
                return f"Marker {marker_index}: '{name}' at {position:.3f}s"
        else:
            return f"No marker/region found at index {marker_index}"
    else:
        raise Exception(f"Failed to get marker/region info: {result.get('error', 'Unknown error')}")


# ============================================================================
# Tempo & Time Signature Markers (planned for future expansion)
# ============================================================================

# Future functions could include:
# - add_tempo_time_sig_marker() - Add tempo/time signature marker
# - delete_tempo_time_sig_marker() - Delete tempo/time signature marker  
# - enum_tempo_time_sig_markers() - Enumerate tempo/time signature markers
# - find_tempo_time_sig_marker() - Find tempo marker at position
# - set_tempo_time_sig_marker() - Update tempo/time signature marker
# - get_last_marker_and_cur_region() - Get last marker and current region info
# - get_marker_by_name() - Find marker/region by name
# - update_marker_region() - Update existing marker/region
# - go_to_marker() - Navigate to specific marker
# - export_markers() - Export markers to file
# - import_markers() - Import markers from file


# ============================================================================
# Registration Function
# ============================================================================

def register_markers_tools(mcp) -> int:
    """Register all markers and regions tools with the MCP instance"""
    tools = [
        # Marker & Region Management
        (add_project_marker, "Add a marker or region to the project"),
        (delete_project_marker, "Delete a marker or region by its displayed number"),
        (count_project_markers, "Count the number of markers and regions in the project"),
        (enum_project_markers, "Get information about a specific marker/region by its index"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)