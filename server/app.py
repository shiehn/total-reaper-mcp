#!/usr/bin/env python3
"""
REAPER MCP Server - Modern Pattern with Full API

This is the main server using the modern @mcp.tool() decorator pattern
with all 228 tools migrated from the legacy monolithic implementation.
"""

import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MCP imports
from mcp.server.fastmcp import FastMCP

# Import bridge
from .bridge import bridge, BRIDGE_DIR

# Initialize MCP server
mcp = FastMCP("reaper-mcp")

# Import and register all tool modules
from .tools.tracks import register_track_tools
from .tools.core_api import register_core_api_tools
from .tools.media_items import register_media_items_tools
from .tools.midi import register_midi_tools
from .tools.fx import register_fx_tools
from .tools.project import register_project_tools
from .tools.transport import register_transport_tools
from .tools.time_selection import register_time_selection_tools
from .tools.markers import register_markers_tools
from .tools.automation import register_automation_tools
from .tools.rendering import register_rendering_tools
from .tools.gui import register_gui_tools
from .tools.fx_take import register_fx_take_tools
from .tools.fx_track_extended import register_fx_track_extended_tools
from .tools.project_state import register_project_state_tools
from .tools.media_items_extended import register_media_items_extended_tools
from .tools.routing_sends import register_routing_sends_tools
from .tools.audio_accessor import register_audio_accessor_tools
from .tools.midi_editor import register_midi_editor_tools
from .tools.color_management import register_color_management_tools
from .tools.tempo_time_signature import register_tempo_time_signature_tools
from .tools.recording import register_recording_tools
from .tools.envelope_extended import register_envelope_extended_tools
from .tools.time_tempo_extended import register_time_tempo_extended_tools
from .tools.track_management_extended import register_track_management_extended_tools
from .tools.action_management import register_action_management_tools
from .tools.file_io import register_file_io_tools
from .tools.layouts import register_layouts_tools
from .tools.take_management import register_take_management_tools
from .tools.regions_markers_extended import register_regions_markers_extended_tools
from .tools.analysis_tools import register_analysis_tools
from .tools.video_media import register_video_media_tools
from .tools.peaks_waveform import register_peaks_waveform_tools
from .tools.script_extensions import register_script_extensions_tools
from .tools.project_tabs import register_project_tabs_tools
from .tools.midi_advanced import register_midi_advanced_tools
from .tools.loop_management import register_loop_management_tools
from .tools.bounce_render import register_bounce_render_tools
from .tools.groove_quantization import register_groove_quantization_tools
from .tools.bus_routing import register_bus_routing_tools
from .tools.tempo_time_management import register_tempo_time_tools
from .tools.advanced_midi_generation import register_advanced_midi_tools

# Register all tools
def register_all_tools():
    """Register all tool categories"""
    logger.info("Registering all MCP tools...")
    
    # Track the total number of tools registered
    total_tools = 0
    
    # Register each category
    categories = [
        ("Track Management", register_track_tools),
        ("Core API & Utilities", register_core_api_tools),
        ("Media Items & Takes", register_media_items_tools),
        ("MIDI Operations", register_midi_tools),
        ("FX & Processing", register_fx_tools),
        ("Project Management", register_project_tools),
        ("Transport & Playback", register_transport_tools),
        ("Time Selection & Navigation", register_time_selection_tools),
        ("Markers & Regions", register_markers_tools),
        ("Automation & Envelopes", register_automation_tools),
        ("Rendering & Freezing", register_rendering_tools),
        ("GUI & Interface", register_gui_tools),
        ("Take FX", register_fx_take_tools),
        ("Track FX Extended", register_fx_track_extended_tools),
        ("Project State Management", register_project_state_tools),
        ("Media Items Extended", register_media_items_extended_tools),
        ("Routing & Sends", register_routing_sends_tools),
        ("Audio Accessor & Analysis", register_audio_accessor_tools),
        ("MIDI Editor & Piano Roll", register_midi_editor_tools),
        ("Color Management", register_color_management_tools),
        ("Tempo & Time Signature", register_tempo_time_signature_tools),
        ("Recording Operations", register_recording_tools),
        ("Envelope Extended", register_envelope_extended_tools),
        ("Time/Tempo Extended", register_time_tempo_extended_tools),
        ("Track Management Extended", register_track_management_extended_tools),
        ("Action Management", register_action_management_tools),
        ("File I/O & Project Management", register_file_io_tools),
        ("Layouts & Screensets", register_layouts_tools),
        ("Take Management Extended", register_take_management_tools),
        ("Regions & Markers Extended", register_regions_markers_extended_tools),
        ("Analysis Tools", register_analysis_tools),
        ("Video & Visual Media", register_video_media_tools),
        ("Peak & Waveform Display", register_peaks_waveform_tools),
        ("Script Extension Management", register_script_extensions_tools),
        ("Project Tab Management", register_project_tabs_tools),
        ("Advanced MIDI Analysis & Generation", register_midi_advanced_tools),
        ("Loop & Time Selection Management", register_loop_management_tools),
        ("Bounce & Render Operations", register_bounce_render_tools),
        ("Groove & Quantization Tools", register_groove_quantization_tools),
        ("Bus Routing & Mixing Workflows", register_bus_routing_tools),
        ("Tempo & Time Management", register_tempo_time_tools),
        ("Advanced MIDI Generation", register_advanced_midi_tools),
    ]
    
    for category_name, register_func in categories:
        try:
            count = register_func(mcp)
            total_tools += count
            logger.info(f"✓ {category_name}: {count} tools")
        except Exception as e:
            logger.error(f"✗ Failed to register {category_name}: {e}")
    
    logger.info(f"Total tools registered: {total_tools}")
    return total_tools

def main():
    """Run the MCP server"""
    logger.info("=" * 60)
    logger.info("REAPER MCP Server - Modern Pattern")
    logger.info("=" * 60)
    logger.info(f"Bridge directory: {BRIDGE_DIR}")
    logger.info("Make sure mcp_bridge_file_v2.lua is running in REAPER!")
    logger.info("")
    
    # Register all tools
    total = register_all_tools()
    
    if total == 0:
        logger.error("No tools registered! Exiting.")
        sys.exit(1)
    
    logger.info("")
    logger.info("Server ready. Waiting for connections...")
    logger.info("=" * 60)
    
    # Run the server
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()