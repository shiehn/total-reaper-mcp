#!/usr/bin/env python3
"""
Integration tests for Core API, Audio, Track Extended, and Utility functions
Tests the MCP tools with the REAPER Lua bridge
"""

import pytest
import pytest_asyncio
import asyncio
import os
from pathlib import Path

@pytest.mark.asyncio
async def test_api_exists(reaper_mcp_client):
    """Test checking if API functions exist"""
    # Test with a function that should exist
    result = await reaper_mcp_client.call_tool(
        "api_exists",
        {"function_name": "CountTracks"}
    )
    assert result is not None
    assert "exists" in result.content[0].text.lower()
    assert "counttracks" in result.content[0].text.lower()
    
    # Test with a function that should not exist
    result = await reaper_mcp_client.call_tool(
        "api_exists",
        {"function_name": "NonExistentFunction123"}
    )
    assert result is not None
    assert "does not exist" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_get_last_color_theme_file(reaper_mcp_client):
    """Test getting the last color theme file"""
    result = await reaper_mcp_client.call_tool(
        "get_last_color_theme_file",
        {}
    )
    assert result is not None
    # Result might be empty if no theme loaded, but should not fail
    print(f"Last color theme: {result.content[0].text}")

@pytest.mark.asyncio
async def test_get_toggle_command_state(reaper_mcp_client):
    """Test getting toggle command state"""
    # Test with a known command ID (40041 = Toggle auto-crossfade on split)
    result = await reaper_mcp_client.call_tool(
        "get_toggle_command_state",
        {"command_id": 40041}
    )
    assert result is not None
    assert "toggle state" in result.content[0].text.lower()
    assert any(state in result.content[0].text.lower() for state in ["on", "off", "not found"])

@pytest.mark.asyncio
async def test_media_source_properties(reaper_mcp_client):
    """Test getting media source sample rate and channels"""
    # First create a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Add a media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    # For this test, we'll need an audio file. Let's check if we can create a source from a test file
    # First, let's see if we have any audio files in the test directory
    test_audio_files = [
        "/System/Library/Sounds/Glass.aiff",  # macOS system sound
        "/System/Library/Sounds/Ping.aiff",   # macOS system sound
        "/usr/share/sounds/alsa/Noise.wav",   # Linux
        "C:\\Windows\\Media\\Windows Ding.wav" # Windows
    ]
    
    audio_file = None
    for file in test_audio_files:
        if os.path.exists(file):
            audio_file = file
            break
    
    if not audio_file:
        pytest.skip("No test audio file available")
    
    # Add audio source to the item
    result = await reaper_mcp_client.call_tool(
        "pcm_source_create_from_file",
        {
            "filename": audio_file,
            "item_index": 0,
            "take_index": 0
        }
    )
    
    # Test sample rate
    result = await reaper_mcp_client.call_tool(
        "get_media_source_sample_rate",
        {
            "item_index": 0,
            "take_index": 0
        }
    )
    assert result is not None
    assert "sample rate" in result.content[0].text.lower()
    assert "hz" in result.content[0].text.lower()
    
    # Test number of channels
    result = await reaper_mcp_client.call_tool(
        "get_media_source_num_channels",
        {
            "item_index": 0,
            "take_index": 0
        }
    )
    assert result is not None
    assert "channels" in result.content[0].text.lower()
    assert any(ch in result.content[0].text.lower() for ch in ["mono", "stereo", "channels"])

@pytest.mark.asyncio
async def test_track_visibility(reaper_mcp_client):
    """Test checking track visibility"""
    # Insert a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Check TCP visibility
    result = await reaper_mcp_client.call_tool(
        "is_track_visible",
        {
            "track_index": 0,
            "mixer": False
        }
    )
    assert result is not None
    assert "track control panel" in result.content[0].text.lower()
    assert "visible" in result.content[0].text.lower()
    
    # Check mixer visibility
    result = await reaper_mcp_client.call_tool(
        "is_track_visible",
        {
            "track_index": 0,
            "mixer": True
        }
    )
    assert result is not None
    assert "mixer" in result.content[0].text.lower()
    assert "visible" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_set_only_track_selected(reaper_mcp_client):
    """Test setting only one track selected"""
    # Insert multiple tracks
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "insert_track",
            {"index": i}
        )
    
    # Select all tracks first
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "set_track_selected",
            {
                "track_index": i,
                "selected": True
            }
        )
    
    # Check that multiple tracks are selected
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert "3" in result.content[0].text
    
    # Set only track 1 selected
    result = await reaper_mcp_client.call_tool(
        "set_only_track_selected",
        {"track_index": 1}
    )
    assert "only selected track" in result.content[0].text.lower()
    
    # Verify only one track is selected
    result = await reaper_mcp_client.call_tool(
        "count_selected_tracks",
        {}
    )
    assert "1" in result.content[0].text
    
    # Verify it's track 1
    result = await reaper_mcp_client.call_tool(
        "get_selected_track",
        {"index": 0}
    )
    assert "index 1" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_db_slider_conversion(reaper_mcp_client):
    """Test dB to slider and slider to dB conversion"""
    # Test dB to slider
    test_values = [0, -6, -12, -20, -40]
    
    for db in test_values:
        result = await reaper_mcp_client.call_tool(
            "db_to_slider",
            {"db": db}
        )
        assert result is not None
        assert f"{db} dB" in result.content[0].text
        assert "slider value" in result.content[0].text
        print(f"DB to slider: {result.content[0].text}")
    
    # Test slider to dB
    test_sliders = [0.0, 0.25, 0.5, 0.75, 1.0]
    
    for slider in test_sliders:
        result = await reaper_mcp_client.call_tool(
            "slider_to_db",
            {"slider": slider}
        )
        assert result is not None
        assert f"{slider}" in result.content[0].text
        assert "dB" in result.content[0].text
        print(f"Slider to dB: {result.content[0].text}")
    
    # Test round-trip conversion
    original_db = -6.0
    
    # Convert to slider
    result = await reaper_mcp_client.call_tool(
        "db_to_slider",
        {"db": original_db}
    )
    # Extract slider value from result
    slider_val = float(result.content[0].text.split("=")[1].split("(")[0].strip())
    
    # Convert back to dB
    result = await reaper_mcp_client.call_tool(
        "slider_to_db",
        {"slider": slider_val}
    )
    # Extract dB value
    converted_db = float(result.content[0].text.split("=")[1].split("dB")[0].strip())
    
    # Should be close to original (within 0.01 dB)
    assert abs(original_db - converted_db) < 0.01
    print(f"Round-trip conversion: {original_db} dB -> {slider_val} -> {converted_db} dB")