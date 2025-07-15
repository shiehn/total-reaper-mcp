"""
Regions and Markers Extended Tools for REAPER MCP

This module contains advanced region and marker tools particularly useful for AI agents
analyzing song structure, sections, and navigation points.
"""

from typing import Optional, Tuple
from ..bridge import bridge


# ============================================================================
# Marker and Region Enumeration
# ============================================================================

async def enumerate_project_markers(marker_index: int) -> str:
    """Enumerate project markers and regions"""
    result = await bridge.call_lua("EnumProjectMarkers", [marker_index])
    
    if result.get("ok"):
        is_region = result.get("isrgn", False)
        pos = result.get("pos", -1)
        region_end = result.get("rgnend", -1)
        name = result.get("name", "")
        idx = result.get("markrgnindexnumber", -1)
        
        if pos >= 0:
            if is_region:
                return f"Region {idx}: '{name}' from {pos:.3f}s to {region_end:.3f}s"
            else:
                return f"Marker {idx}: '{name}' at {pos:.3f}s"
        else:
            return f"No marker/region at index {marker_index}"
    else:
        raise Exception("Failed to enumerate project markers")


async def enumerate_project_markers_extended(marker_index: int) -> str:
    """Enumerate project markers with color information"""
    result = await bridge.call_lua("EnumProjectMarkers3", [0, marker_index])
    
    if result.get("ok"):
        is_region = result.get("isrgn", False)
        pos = result.get("pos", -1)
        region_end = result.get("rgnend", -1)
        name = result.get("name", "")
        idx = result.get("markrgnindexnumber", -1)
        color = result.get("color", 0)
        
        if pos >= 0:
            color_str = f" (color: {color})" if color != 0 else ""
            if is_region:
                return f"Region {idx}: '{name}' from {pos:.3f}s to {region_end:.3f}s{color_str}"
            else:
                return f"Marker {idx}: '{name}' at {pos:.3f}s{color_str}"
        else:
            return f"No marker/region at index {marker_index}"
    else:
        raise Exception("Failed to enumerate project markers")


async def count_project_markers() -> str:
    """Count total markers and regions in project"""
    result = await bridge.call_lua("CountProjectMarkers", [0])
    
    if result.get("ok"):
        total_count = result.get("num_markers", 0)
        marker_count = result.get("num_regions", 0)
        return f"Project has {total_count} markers/regions total ({total_count - marker_count} markers, {marker_count} regions)"
    else:
        raise Exception("Failed to count project markers")


# ============================================================================
# Marker/Region Navigation
# ============================================================================

async def go_to_marker(marker_number: int, use_timeline_order: bool = True) -> str:
    """Navigate to a specific marker"""
    result = await bridge.call_lua("GoToMarker", [0, marker_number, use_timeline_order])
    
    if result.get("ok"):
        return f"Navigated to marker {marker_number}"
    else:
        raise Exception(f"Failed to navigate to marker {marker_number}")


async def go_to_region(region_number: int, use_timeline_order: bool = True) -> str:
    """Navigate to start of a specific region"""
    result = await bridge.call_lua("GoToRegion", [0, region_number, use_timeline_order])
    
    if result.get("ok"):
        return f"Navigated to region {region_number}"
    else:
        raise Exception(f"Failed to navigate to region {region_number}")


async def get_marker_and_region_names_from_time(time: float) -> str:
    """Get all markers and regions at a specific time"""
    result = await bridge.call_lua("GetMarkerAndRegionNamesFromTime", [0, time])
    
    if result.get("ok"):
        markers = result.get("markernames", "")
        regions = result.get("regionnames", "")
        
        response = []
        if markers:
            response.append(f"Markers at {time:.3f}s: {markers}")
        if regions:
            response.append(f"Regions at {time:.3f}s: {regions}")
        
        if not response:
            return f"No markers or regions at {time:.3f}s"
        return " | ".join(response)
    else:
        raise Exception("Failed to get markers/regions from time")


async def marker_region_index_from_time(time: float) -> str:
    """Get the index of marker/region at or before a specific time"""
    result = await bridge.call_lua("GetLastMarkerAndCurRegion", [0, time])
    
    if result.get("ok"):
        marker_idx = result.get("markeridx", -1)
        region_idx = result.get("regionidx", -1)
        
        parts = []
        if marker_idx >= 0:
            parts.append(f"Last marker: {marker_idx}")
        if region_idx >= 0:
            parts.append(f"Current region: {region_idx}")
        
        if parts:
            return f"At {time:.3f}s - {', '.join(parts)}"
        else:
            return f"No markers or regions before {time:.3f}s"
    else:
        raise Exception("Failed to get marker/region index from time")


# ============================================================================
# Marker/Region Modification
# ============================================================================

async def set_project_marker(marker_index: int, is_region: bool, position: float, 
                           region_end: float, name: str) -> str:
    """Add or update a project marker/region"""
    result = await bridge.call_lua("SetProjectMarker", [marker_index, is_region, position, region_end, name])
    
    if result.get("ok"):
        if marker_index == -1:
            return f"Added new {'region' if is_region else 'marker'} '{name}' at {position:.3f}s"
        else:
            return f"Updated {'region' if is_region else 'marker'} {marker_index} to '{name}' at {position:.3f}s"
    else:
        raise Exception("Failed to set project marker")


async def set_project_marker_with_color(marker_index: int, is_region: bool, position: float, 
                                       region_end: float, name: str, color: int) -> str:
    """Add or update a project marker/region with color"""
    result = await bridge.call_lua("SetProjectMarker3", [0, marker_index, is_region, position, region_end, name, color])
    
    if result.get("ok"):
        if marker_index == -1:
            return f"Added new {'region' if is_region else 'marker'} '{name}' at {position:.3f}s with color {color}"
        else:
            return f"Updated {'region' if is_region else 'marker'} {marker_index} to '{name}' at {position:.3f}s with color {color}"
    else:
        raise Exception("Failed to set project marker with color")


async def delete_project_marker(marker_index: int, is_region: bool) -> str:
    """Delete a project marker or region"""
    result = await bridge.call_lua("DeleteProjectMarker", [0, marker_index, is_region])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Deleted {'region' if is_region else 'marker'} {marker_index}"
        else:
            return f"Failed to delete {'region' if is_region else 'marker'} {marker_index} - not found"
    else:
        raise Exception("Failed to delete project marker")


async def delete_project_marker_by_index(marker_index: int) -> str:
    """Delete a project marker/region by its enumeration index"""
    result = await bridge.call_lua("DeleteProjectMarkerByIndex", [0, marker_index])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Deleted marker/region at index {marker_index}"
        else:
            return f"Failed to delete marker/region at index {marker_index} - not found"
    else:
        raise Exception("Failed to delete project marker by index")


# ============================================================================
# Time Signature Markers
# ============================================================================

async def find_tempo_time_sig_marker(time: float) -> str:
    """Find tempo/time signature marker at or before a time"""
    result = await bridge.call_lua("FindTempoTimeSigMarker", [0, time])
    
    if result.get("ok"):
        marker_index = result.get("ret", -1)
        if marker_index >= 0:
            return f"Found tempo/time sig marker {marker_index} at or before {time:.3f}s"
        else:
            return f"No tempo/time sig marker found before {time:.3f}s"
    else:
        raise Exception("Failed to find tempo/time sig marker")


async def add_tempo_time_sig_marker(position: float, bpm: float, time_sig_num: int, 
                                   time_sig_denom: int, linear_tempo: bool = False) -> str:
    """Add a tempo/time signature change marker"""
    result = await bridge.call_lua("AddTempoTimeSigMarker", [0, position, bpm, time_sig_num, time_sig_denom, linear_tempo])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Added tempo marker at {position:.3f}s: {bpm} BPM, {time_sig_num}/{time_sig_denom}"
        else:
            return "Failed to add tempo/time signature marker"
    else:
        raise Exception("Failed to add tempo/time sig marker")


async def delete_tempo_time_sig_marker(marker_index: int) -> str:
    """Delete a tempo/time signature marker"""
    result = await bridge.call_lua("DeleteTempoTimeSigMarker", [0, marker_index])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            return f"Deleted tempo/time sig marker {marker_index}"
        else:
            return f"Failed to delete tempo/time sig marker {marker_index}"
    else:
        raise Exception("Failed to delete tempo/time sig marker")


# ============================================================================
# Region Rendering
# ============================================================================

async def get_region_render_matrix() -> str:
    """Get the current region render matrix settings"""
    result = await bridge.call_lua("GetProjectInfo", [0, "RENDER_MATRIX"])
    
    if result.get("ok"):
        matrix = int(result.get("ret", 0))
        if matrix == 0:
            return "Region render matrix: Master mix"
        elif matrix == 1:
            return "Region render matrix: Stems (selected tracks)"
        else:
            return f"Region render matrix: Custom ({matrix})"
    else:
        raise Exception("Failed to get region render matrix")


async def set_region_render_matrix(matrix_type: int) -> str:
    """Set the region render matrix (0=master, 1=stems)"""
    result = await bridge.call_lua("SetProjectInfo", [0, "RENDER_MATRIX", float(matrix_type)])
    
    if result.get("ok"):
        return f"Set region render matrix to: {matrix_type}"
    else:
        raise Exception("Failed to set region render matrix")


# ============================================================================
# Registration Function
# ============================================================================

def register_regions_markers_extended_tools(mcp) -> int:
    """Register all extended region and marker tools with the MCP instance"""
    tools = [
        # Enumeration
        (enumerate_project_markers, "Enumerate project markers and regions"),
        (enumerate_project_markers_extended, "Enumerate markers with color info"),
        (count_project_markers, "Count total markers and regions"),
        
        # Navigation
        (go_to_marker, "Navigate to a specific marker"),
        (go_to_region, "Navigate to start of a specific region"),
        (get_marker_and_region_names_from_time, "Get markers/regions at time"),
        (marker_region_index_from_time, "Get marker/region index from time"),
        
        # Modification
        (set_project_marker, "Add or update a project marker/region"),
        (set_project_marker_with_color, "Add/update marker with color"),
        (delete_project_marker, "Delete a project marker or region"),
        (delete_project_marker_by_index, "Delete marker/region by index"),
        
        # Tempo/Time Signature
        (find_tempo_time_sig_marker, "Find tempo marker at or before time"),
        (add_tempo_time_sig_marker, "Add tempo/time signature marker"),
        (delete_tempo_time_sig_marker, "Delete tempo/time signature marker"),
        
        # Region Rendering
        (get_region_render_matrix, "Get region render matrix settings"),
        (set_region_render_matrix, "Set region render matrix"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)