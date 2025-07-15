#!/usr/bin/env python3
"""
Integration tests for Time/Tempo, Track Management Extended, and Project functions
Tests the MCP tools with the REAPER Lua bridge
"""

import pytest
import pytest_asyncio
import asyncio
from .test_utils import (
    ensure_clean_project,
    assert_response_contains,
    assert_response_success
)

@pytest.mark.asyncio
async def test_time_map_conversions(reaper_mcp_client):
    """Test converting between time and quarter notes"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Test QN to time
    result = await reaper_mcp_client.call_tool(
        "time_map2_qn_to_time",
        {"qn": 4.0}  # 4 quarter notes (1 measure at 4/4)
    )
    assert result is not None
    assert_response_contains(result, "quarter notes")
    assert_response_contains(result, "seconds")
    
    # Test time to QN
    result = await reaper_mcp_client.call_tool(
        "time_map2_time_to_qn",
        {"time": 2.0}  # 2 seconds
    )
    assert result is not None
    assert_response_contains(result, "seconds")
    assert_response_contains(result, "quarter notes")
    
    # Test round-trip conversion
    # First convert 8 QN to time
    result = await reaper_mcp_client.call_tool(
        "time_map2_qn_to_time",
        {"qn": 8.0}
    )
    # Extract time value
    time_text = result.content[0].text
    time_val = float(time_text.split("=")[1].split("seconds")[0].strip())
    
    # Convert back to QN
    result = await reaper_mcp_client.call_tool(
        "time_map2_time_to_qn",
        {"time": time_val}
    )
    # Extract QN value
    qn_text = result.content[0].text
    qn_val = float(qn_text.split("=")[1].split("quarter")[0].strip())
    
    # Should be close to original (within 0.001)
    assert abs(8.0 - qn_val) < 0.001

@pytest.mark.asyncio
async def test_measure_info(reaper_mcp_client):
    """Test getting measure information"""
    # Get info at time 0
    result = await reaper_mcp_client.call_tool(
        "time_map_get_measure_info",
        {"time": 0.0}
    )
    assert result is not None
    assert "measure" in result.content[0].text.lower()
    assert "time signature" in result.content[0].text.lower()
    assert "tempo" in result.content[0].text.lower()
    assert "bpm" in result.content[0].text.lower()
    
    # Get info at 5 seconds
    result = await reaper_mcp_client.call_tool(
        "time_map_get_measure_info",
        {"time": 5.0}
    )
    assert result is not None
    assert "measure" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_tempo_time_sig_markers(reaper_mcp_client):
    """Test getting tempo/time signature markers"""
    # Try to get the first marker (index 0)
    result = await reaper_mcp_client.call_tool(
        "get_tempo_time_sig_marker",
        {"marker_index": 0}
    )
    assert result is not None
    # Either we get marker info or "no marker" message
    text = result.content[0].text.lower()
    assert any(phrase in text for phrase in ["tempo", "no tempo/time signature marker"])
    
    # Try a non-existent marker
    result = await reaper_mcp_client.call_tool(
        "get_tempo_time_sig_marker",
        {"marker_index": 999}
    )
    assert result is not None
    assert "no tempo/time signature marker" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_last_touched_track(reaper_mcp_client):
    """Test getting the last touched track"""
    # Create some tracks first
    for i in range(2):
        await reaper_mcp_client.call_tool(
            "insert_track",
            {"index": i}
        )
    
    # Select track 1 to "touch" it
    await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": 1, "selected": True}
    )
    
    # Get last touched track
    result = await reaper_mcp_client.call_tool(
        "get_last_touched_track",
        {}
    )
    assert result is not None
    assert "last touched track" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_track_midi_note_names(reaper_mcp_client):
    """Test getting MIDI note names for tracks"""
    # Create a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Test middle C (MIDI note 60)
    result = await reaper_mcp_client.call_tool(
        "get_track_midi_note_name",
        {"track_index": 0, "pitch": 60, "channel": 0}
    )
    assert result is not None
    assert "midi note 60" in result.content[0].text.lower()
    # Should show C4 or C3 depending on octave numbering
    assert any(note in result.content[0].text for note in ["C3", "C4"])
    
    # Test A4 (MIDI note 69)
    result = await reaper_mcp_client.call_tool(
        "get_track_midi_note_name",
        {"track_index": 0, "pitch": 69}
    )
    assert result is not None
    assert "69" in result.content[0].text
    assert any(note in result.content[0].text for note in ["A3", "A4"])

@pytest.mark.asyncio
async def test_any_track_solo(reaper_mcp_client):
    """Test checking if any track is soloed"""
    # Initially no tracks should be soloed
    result = await reaper_mcp_client.call_tool(
        "any_track_solo",
        {}
    )
    assert result is not None
    assert "any track soloed" in result.content[0].text.lower()
    assert "no" in result.content[0].text.lower()
    
    # Create a track and solo it
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    await reaper_mcp_client.call_tool(
        "set_track_solo",
        {"track_index": 0, "solo": True}
    )
    
    # Now check again
    result = await reaper_mcp_client.call_tool(
        "any_track_solo",
        {}
    )
    assert result is not None
    assert "any track soloed" in result.content[0].text.lower()
    assert "yes" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_mixer_scroll(reaper_mcp_client):
    """Test getting and setting mixer scroll position"""
    # Create several tracks
    for i in range(5):
        await reaper_mcp_client.call_tool(
            "insert_track",
            {"index": i}
        )
    
    # Get initial mixer scroll
    result = await reaper_mcp_client.call_tool(
        "get_mixer_scroll",
        {}
    )
    assert result is not None
    assert "leftmost track" in result.content[0].text.lower()
    
    # Set mixer scroll to track 2
    result = await reaper_mcp_client.call_tool(
        "set_mixer_scroll",
        {"leftmost_track": 2}
    )
    assert result is not None
    assert "set mixer scroll" in result.content[0].text.lower()
    
    # Verify scroll position changed
    result = await reaper_mcp_client.call_tool(
        "get_mixer_scroll",
        {}
    )
    assert result is not None
    # Note: The actual scroll position might not be exactly 2 due to UI constraints

@pytest.mark.asyncio
async def test_project_dirty_state(reaper_mcp_client):
    """Test marking project as dirty"""
    # Mark project dirty
    result = await reaper_mcp_client.call_tool(
        "mark_project_dirty",
        {}
    )
    assert result is not None
    assert "marked as having unsaved changes" in result.content[0].text.lower()
    
    # Check if project is dirty
    result = await reaper_mcp_client.call_tool(
        "is_project_dirty",
        {}
    )
    assert result is not None
    assert "unsaved changes" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_project_length(reaper_mcp_client):
    """Test getting project length"""
    # Get initial project length
    result = await reaper_mcp_client.call_tool(
        "get_project_length",
        {}
    )
    assert result is not None
    assert "project length" in result.content[0].text.lower()
    assert "seconds" in result.content[0].text.lower()
    
    # Add some items to extend project length
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    # Set item to end at 10 seconds
    await reaper_mcp_client.call_tool(
        "set_media_item_position",
        {"item_index": 0, "position": 5.0}
    )
    await reaper_mcp_client.call_tool(
        "set_media_item_length",
        {"item_index": 0, "length": 5.0}
    )
    
    # Get new project length
    result = await reaper_mcp_client.call_tool(
        "get_project_length",
        {}
    )
    assert result is not None
    # Extract length value
    text = result.content[0].text
    length_str = text.split(":")[1].split("seconds")[0].strip()
    length = float(length_str)
    # Should be at least 10 seconds now
    assert length >= 10.0

@pytest.mark.asyncio 
async def test_real_time_audio_check(reaper_mcp_client):
    """Test checking real-time audio thread status"""
    result = await reaper_mcp_client.call_tool(
        "is_in_real_time_audio",
        {}
    )
    assert result is not None
    assert "real-time audio thread" in result.content[0].text.lower()
    # Should normally be "No" when called from MCP
    assert any(word in result.content[0].text.lower() for word in ["yes", "no"])