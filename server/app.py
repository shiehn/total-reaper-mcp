#!/usr/bin/env python3
"""
REAPER MCP Server with Tool Profile Support

This version allows limiting tools based on profiles for different LLM providers.
"""

import os
import sys
import logging
import asyncio
import argparse
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

# Import WebSocket client for relay
from .websocket_client import create_relay_client

# Import tool profiles
from .tool_profiles import TOOL_PROFILES, get_profile_categories

# Initialize MCP server
mcp = FastMCP("reaper-mcp")

# Global reference to WebSocket client
relay_client = None

# Import all tool modules (we'll selectively register based on profile)
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
from .dsl.tools import register_dsl_tools
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

# Import DSL health check
from .dsl.health_check import verify_dsl_installation

# Category mapping
CATEGORY_REGISTRY = {
    "DSL": register_dsl_tools,
    "Core API": register_core_api_tools,
    "Tracks": register_track_tools,
    "Media Items": register_media_items_tools,
    "MIDI": register_midi_tools,
    "FX": register_fx_tools,
    "Project": register_project_tools,
    "Transport": register_transport_tools,
    "Time Selection": register_time_selection_tools,
    "Markers": register_markers_tools,
    "Automation & Envelopes": register_automation_tools,
    "Rendering & Freezing": register_rendering_tools,
    "GUI & Interface": register_gui_tools,
    "Take FX": register_fx_take_tools,
    "Track FX Extended": register_fx_track_extended_tools,
    "Project State Management": register_project_state_tools,
    "Media Items Extended": register_media_items_extended_tools,
    "Routing & Sends": register_routing_sends_tools,
    "Audio Accessor & Analysis": register_audio_accessor_tools,
    "MIDI Editor & Piano Roll": register_midi_editor_tools,
    "Color Management": register_color_management_tools,
    "Tempo & Time Signature": register_tempo_time_signature_tools,
    "Recording Operations": register_recording_tools,
    "Envelope Extended": register_envelope_extended_tools,
    "Time/Tempo Extended": register_time_tempo_extended_tools,
    "Track Management Extended": register_track_management_extended_tools,
    "Action Management": register_action_management_tools,
    "File I/O & Project Management": register_file_io_tools,
    "Layouts & Screensets": register_layouts_tools,
    "Take Management Extended": register_take_management_tools,
    "Regions & Markers Extended": register_regions_markers_extended_tools,
    "Analysis Tools": register_analysis_tools,
    "Video & Visual Media": register_video_media_tools,
    "Peak & Waveform Display": register_peaks_waveform_tools,
    "Script Extension Management": register_script_extensions_tools,
    "Project Tab Management": register_project_tabs_tools,
    "Advanced MIDI Analysis & Generation": register_midi_advanced_tools,
    "Loop & Time Selection Management": register_loop_management_tools,
    "Bounce & Render Operations": register_bounce_render_tools,
    "Groove & Quantization Tools": register_groove_quantization_tools,
    "Bus Routing & Mixing Workflows": register_bus_routing_tools,
    "Tempo & Time Management": register_tempo_time_tools,
    "Advanced MIDI Generation": register_advanced_midi_tools,
}

def register_tools_by_profile(profile_name):
    """Register tools based on the selected profile"""
    allowed_categories = get_profile_categories(profile_name)
    
    if allowed_categories is None:
        # Full profile - register everything
        logger.info(f"Using profile: {TOOL_PROFILES['full']['name']}")
        return register_all_tools()
    
    profile = TOOL_PROFILES.get(profile_name, TOOL_PROFILES["groq-essential"])
    logger.info(f"Using profile: {profile['name']} - {profile['description']}")
    logger.info(f"Categories to register: {', '.join(allowed_categories)}")
    
    total_tools = 0
    
    for category_name, register_func in CATEGORY_REGISTRY.items():
        # Check if this category is in our allowed list
        if category_name in allowed_categories:
            try:
                count = register_func(mcp)
                total_tools += count
                logger.info(f"✓ {category_name}: {count} tools")
            except Exception as e:
                logger.error(f"✗ Failed to register {category_name}: {e}")
        else:
            logger.debug(f"⊘ Skipping {category_name} (not in profile)")
    
    return total_tools

def register_all_tools():
    """Register all available tools (original behavior)"""
    total_tools = 0
    
    for category_name, register_func in CATEGORY_REGISTRY.items():
        try:
            count = register_func(mcp)
            total_tools += count
            logger.info(f"✓ {category_name}: {count} tools")
        except Exception as e:
            logger.error(f"✗ Failed to register {category_name}: {e}")
    
    return total_tools

async def main_async(args):
    """Run the MCP server with WebSocket relay support"""
    logger.info("=" * 60)
    logger.info("REAPER MCP Server - Modern Pattern")
    logger.info("=" * 60)
    logger.info(f"Bridge directory: {BRIDGE_DIR}")
    logger.info("Make sure mcp_bridge_file_v2.lua is running in REAPER!")
    logger.info("")
    
    # Register tools based on profile
    total = register_tools_by_profile(args.profile)
    
    if total == 0:
        logger.error("No tools registered! Exiting.")
        sys.exit(1)
    
    logger.info(f"Total tools registered: {total}")
    
    # Verify DSL functions if using a DSL profile
    profile = TOOL_PROFILES.get(args.profile)
    if profile:
        categories = profile.get("categories", [])
        await verify_dsl_installation(bridge, args.profile, categories)
    
    # Create and connect WebSocket client if relay URL is provided
    relay_url = os.environ.get("MCP_RELAY_URL")
    auth_token = os.environ.get("MCP_AUTH_TOKEN")
    
    if relay_url and auth_token:
        logger.info(f"Connecting to MCP relay at {relay_url}")
        global relay_client
        relay_client = await create_relay_client(relay_url, auth_token, mcp)
        
        if relay_client:
            logger.info("Connected to MCP relay successfully")
        else:
            logger.error("Failed to connect to MCP relay")
    
    logger.info("")
    logger.info("Server ready. Waiting for connections...")
    logger.info("=" * 60)
    
    # Run the server
    mcp.run(transport="stdio")

def main():
    """Entry point with argument parsing"""
    parser = argparse.ArgumentParser(description="REAPER MCP Server with Tool Profiles")
    parser.add_argument(
        "--profile",
        choices=list(TOOL_PROFILES.keys()),
        default="dsl-production",
        help="Tool profile to use (default: dsl-production)"
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="List available profiles and exit"
    )
    
    args = parser.parse_args()
    
    # Handle --list-profiles
    if args.list_profiles:
        print("\nAvailable Tool Profiles:")
        print("-" * 60)
        for name, profile in TOOL_PROFILES.items():
            print(f"\n{name}:")
            print(f"  Name: {profile['name']}")
            print(f"  Description: {profile['description']}")
            if profile['categories']:
                print(f"  Categories: {len(profile['categories'])}")
                for cat in profile['categories']:
                    print(f"    - {cat}")
        sys.exit(0)
    
    # Check if we should run in relay mode
    if os.environ.get("MCP_RELAY_URL"):
        # Run with asyncio for WebSocket support
        try:
            asyncio.run(main_async(args))
        except KeyboardInterrupt:
            logger.info("Shutting down...")
    else:
        # Run in standard stdio mode
        logger.info("=" * 60)
        logger.info("REAPER MCP Server - Modern Pattern")
        logger.info("=" * 60)
        logger.info(f"Bridge directory: {BRIDGE_DIR}")
        logger.info("Make sure mcp_bridge_file_v2.lua is running in REAPER!")
        logger.info("")
        
        # Register tools based on profile
        total = register_tools_by_profile(args.profile)
        
        if total == 0:
            logger.error("No tools registered! Exiting.")
            sys.exit(1)
        
        logger.info(f"Total tools registered: {total}")
        logger.info("")
        logger.info("Server ready. Waiting for connections...")
        logger.info("=" * 60)
        
        # Run the server
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()