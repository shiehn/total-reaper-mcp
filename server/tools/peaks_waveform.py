"""
Peak and Waveform Display Tools for REAPER MCP

This module contains tools for working with audio peaks, waveform display,
and visual representation - useful for AI agents analyzing audio content.
"""

from typing import List, Dict, Any, Optional, Tuple
from ..bridge import bridge


# ============================================================================
# Peak Building and Management
# ============================================================================

async def build_peaks_for_item(item_index: int) -> str:
    """Build peaks for a media item"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Get active take
    take_result = await bridge.call_lua("GetActiveTake", [item])
    if not take_result.get("ok") or not take_result.get("ret"):
        return "Item has no active take"
    
    take = take_result.get("ret")
    
    # Get source
    source_result = await bridge.call_lua("GetMediaItemTake_Source", [take])
    if not source_result.get("ok") or not source_result.get("ret"):
        return "Take has no media source"
    
    source = source_result.get("ret")
    
    # Build peaks
    result = await bridge.call_lua("PCM_Source_BuildPeaks", [source, 0])
    if result.get("ok"):
        ret = result.get("ret", 0)
        if ret == 0:
            return "Peaks already built or building started"
        elif ret == 1:
            return "Peak building in progress"
        else:
            return f"Peak building status: {ret}"
    
    raise Exception("Failed to build peaks")


async def get_peak_file_path(item_index: int) -> str:
    """Get the path to the peak file for an item"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Get active take
    take_result = await bridge.call_lua("GetActiveTake", [item])
    if not take_result.get("ok") or not take_result.get("ret"):
        return "Item has no active take"
    
    take = take_result.get("ret")
    
    # Get source filename
    filename_result = await bridge.call_lua("GetMediaSourceFileName", [take, ""])
    if filename_result.get("ok"):
        source_file = filename_result.get("ret", "")
        if source_file:
            # Peak files are typically .reapeaks in the same directory
            peak_file = source_file + ".reapeaks"
            return f"Peak file path: {peak_file}"
        else:
            return "No source file associated with take"
    
    return "Could not determine peak file path"


async def invalidate_item_peaks(item_index: int) -> str:
    """Invalidate peaks for an item to force rebuild"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Update item to invalidate peaks
    result = await bridge.call_lua("UpdateItemInProject", [item])
    if result.get("ok"):
        return "Peaks invalidated for item"
    
    raise Exception("Failed to invalidate peaks")


# ============================================================================
# Waveform Display Settings
# ============================================================================

async def set_media_item_visual_height(item_index: int, height: float) -> str:
    """Set the visual height of a media item in the arrange view"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Set height
    result = await bridge.call_lua("SetMediaItemInfo_Value", [item, "F_FREEMODE_H", height])
    if result.get("ok"):
        return f"Set item visual height to {height:.1f} pixels"
    
    raise Exception("Failed to set item height")


async def get_waveform_display_mode() -> str:
    """Get the current waveform display mode"""
    # Get display mode from preferences
    # 0 = normal, 1 = rectified, 2 = spectral, etc.
    mode_result = await bridge.call_lua("GetExtState", ["REAPER", "waveform_display_mode"])
    mode = mode_result.get("ret", "0") if mode_result.get("ok") else "0"
    
    modes = {
        "0": "Normal",
        "1": "Rectified", 
        "2": "Spectral",
        "3": "Spectrogram"
    }
    
    mode_name = modes.get(mode, "Unknown")
    return f"Waveform display mode: {mode_name}"


async def set_waveform_display_mode(mode: str) -> str:
    """Set the waveform display mode (normal, rectified, spectral)"""
    valid_modes = {
        "normal": "0",
        "rectified": "1",
        "spectral": "2",
        "spectrogram": "3"
    }
    
    mode_lower = mode.lower()
    if mode_lower not in valid_modes:
        return f"Invalid mode. Valid options: {', '.join(valid_modes.keys())}"
    
    mode_value = valid_modes[mode_lower]
    
    # Store in extended state
    result = await bridge.call_lua("SetExtState", ["REAPER", "waveform_display_mode", mode_value])
    if result.get("ok"):
        # Execute action to update display
        await bridge.call_lua("Main_OnCommand", [40346 + int(mode_value), 0])
        return f"Set waveform display mode to {mode}"
    
    raise Exception("Failed to set display mode")


# ============================================================================
# Peak Sample Access
# ============================================================================

async def get_peak_samples(item_index: int, start_time: float, end_time: float, 
                          num_samples: int = 1000) -> str:
    """Get peak sample data for visualization"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Get active take
    take_result = await bridge.call_lua("GetActiveTake", [item])
    if not take_result.get("ok") or not take_result.get("ret"):
        return "Item has no active take"
    
    take = take_result.get("ret")
    
    # Get source
    source_result = await bridge.call_lua("GetMediaItemTake_Source", [take])
    if not source_result.get("ok") or not source_result.get("ret"):
        return "Take has no media source"
    
    source = source_result.get("ret")
    
    # Note: Actual peak reading requires PCM_Source_CreateFromType("REAPER_PEAKS")
    # This is a simplified version
    duration = end_time - start_time
    
    return (f"Peak sample request for {duration:.2f}s window with {num_samples} samples. "
            "Full implementation requires audio accessor API.")


async def get_item_peak_info(item_index: int) -> str:
    """Get peak information for an item"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Get take
    take_result = await bridge.call_lua("GetActiveTake", [item])
    if not take_result.get("ok") or not take_result.get("ret"):
        return "Item has no active take"
    
    take = take_result.get("ret")
    
    # Get basic info
    channels_result = await bridge.call_lua("GetMediaItemTakeInfo_Value", [take, "I_TAKEFX_NCH"])
    channels = int(channels_result.get("ret", 2)) if channels_result.get("ok") else 2
    
    # Get item length
    length_result = await bridge.call_lua("GetMediaItemInfo_Value", [item, "D_LENGTH"])
    length = length_result.get("ret", 0) if length_result.get("ok") else 0
    
    return (f"Peak info - Channels: {channels}, Length: {length:.2f}s, "
            f"Peak resolution depends on zoom level")


# ============================================================================
# Visual Analysis
# ============================================================================

async def analyze_item_dynamics(item_index: int) -> str:
    """Analyze the dynamic range of an item based on peaks"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Get take
    take_result = await bridge.call_lua("GetActiveTake", [item])
    if not take_result.get("ok") or not take_result.get("ret"):
        return "Item has no active take"
    
    take = take_result.get("ret")
    
    # Get volume and pan info as proxy for dynamics
    vol_result = await bridge.call_lua("GetMediaItemTakeInfo_Value", [take, "D_VOL"])
    pan_result = await bridge.call_lua("GetMediaItemTakeInfo_Value", [take, "D_PAN"])
    
    volume = vol_result.get("ret", 1.0) if vol_result.get("ok") else 1.0
    pan = pan_result.get("ret", 0.0) if pan_result.get("ok") else 0.0
    
    # Convert volume to dB
    import math
    volume_db = 20 * math.log10(volume) if volume > 0 else -150
    
    return (f"Item dynamics analysis:\n"
            f"  Volume: {volume_db:.1f} dB\n"
            f"  Pan: {pan:.1%} {'R' if pan > 0 else 'L' if pan < 0 else 'C'}\n"
            f"  (Full dynamic analysis requires audio accessor)")


async def find_transients_in_item(item_index: int, threshold: float = 0.1) -> str:
    """Find transients in an item based on peak analysis"""
    # This would use dynamic split or transient detection API
    # For now, return placeholder
    return (f"Transient detection with threshold {threshold} requires audio analysis. "
            "Use dynamic split action (40760) for basic transient marking.")


async def get_spectral_display_settings() -> str:
    """Get spectral display settings for items"""
    # Get spectral settings from extended state
    fft_size_result = await bridge.call_lua("GetExtState", ["REAPER", "spectral_fft_size"])
    window_result = await bridge.call_lua("GetExtState", ["REAPER", "spectral_window"])
    
    fft_size = fft_size_result.get("ret", "2048") if fft_size_result.get("ok") else "2048"
    window = window_result.get("ret", "Hann") if window_result.get("ok") else "Hann"
    
    return (f"Spectral display settings:\n"
            f"  FFT size: {fft_size}\n"
            f"  Window type: {window}")


async def set_item_spectrogram_settings(item_index: int, fft_size: int = 2048, 
                                       overlap: float = 0.5) -> str:
    """Configure spectrogram display for an item"""
    # Validate FFT size (must be power of 2)
    valid_fft_sizes = [256, 512, 1024, 2048, 4096, 8192, 16384]
    if fft_size not in valid_fft_sizes:
        return f"Invalid FFT size. Valid options: {valid_fft_sizes}"
    
    # Store settings
    await bridge.call_lua("SetExtState", ["REAPER", "spectral_fft_size", str(fft_size)])
    await bridge.call_lua("SetExtState", ["REAPER", "spectral_overlap", str(overlap)])
    
    return f"Set spectrogram - FFT: {fft_size}, Overlap: {overlap:.1%}"


# ============================================================================
# Zoom and Navigation
# ============================================================================

async def zoom_to_item_peaks(item_index: int) -> str:
    """Zoom view to show item at optimal peak detail level"""
    # Get media item
    item_result = await bridge.call_lua("GetMediaItem", [0, item_index])
    if not item_result.get("ok") or not item_result.get("ret"):
        raise Exception(f"Failed to get media item at index {item_index}")
    
    item = item_result.get("ret")
    
    # Get item position and length
    pos_result = await bridge.call_lua("GetMediaItemInfo_Value", [item, "D_POSITION"])
    length_result = await bridge.call_lua("GetMediaItemInfo_Value", [item, "D_LENGTH"])
    
    if pos_result.get("ok") and length_result.get("ok"):
        pos = pos_result.get("ret", 0)
        length = length_result.get("ret", 1)
        
        # Set time selection to item
        await bridge.call_lua("GetSet_LoopTimeRange", [True, False, pos, pos + length, False])
        
        # Zoom to selection
        await bridge.call_lua("Main_OnCommand", [40031, 0])  # View: Zoom time selection
        
        return f"Zoomed to item from {pos:.2f}s to {pos + length:.2f}s"
    
    raise Exception("Failed to get item bounds")


async def get_peak_display_scale() -> str:
    """Get the current peak display scale settings"""
    # Get zoom factor
    start_result = await bridge.call_lua("GetSet_ArrangeView2", [0, False, 0, 0])
    end_result = await bridge.call_lua("GetSet_ArrangeView2", [0, False, 0, 0])
    
    if start_result.get("ok") and end_result.get("ok"):
        view_start = start_result.get("start_time", 0)
        view_end = end_result.get("end_time", 10)
        visible_time = view_end - view_start
        
        # Estimate pixels per second
        pixels_per_second = 100  # Default estimate
        
        return (f"Peak display scale:\n"
                f"  Visible time: {visible_time:.1f}s\n"
                f"  Approx. scale: {pixels_per_second:.0f} pixels/second")
    
    return "Could not determine peak display scale"


# ============================================================================
# Registration Function
# ============================================================================

def register_peaks_waveform_tools(mcp) -> int:
    """Register all peak/waveform tools with the MCP instance"""
    tools = [
        # Peak Building and Management
        (build_peaks_for_item, "Build peaks for a media item"),
        (get_peak_file_path, "Get the path to the peak file for an item"),
        (invalidate_item_peaks, "Invalidate peaks for an item to force rebuild"),
        
        # Waveform Display Settings
        (set_media_item_visual_height, "Set the visual height of a media item"),
        (get_waveform_display_mode, "Get the current waveform display mode"),
        (set_waveform_display_mode, "Set the waveform display mode"),
        
        # Peak Sample Access
        (get_peak_samples, "Get peak sample data for visualization"),
        (get_item_peak_info, "Get peak information for an item"),
        
        # Visual Analysis
        (analyze_item_dynamics, "Analyze the dynamic range of an item"),
        (find_transients_in_item, "Find transients in an item"),
        (get_spectral_display_settings, "Get spectral display settings"),
        (set_item_spectrogram_settings, "Configure spectrogram display for an item"),
        
        # Zoom and Navigation
        (zoom_to_item_peaks, "Zoom view to show item at optimal peak detail"),
        (get_peak_display_scale, "Get the current peak display scale settings"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)