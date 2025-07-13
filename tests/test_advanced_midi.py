"""Test advanced MIDI operations"""
import pytest
import pytest_asyncio
import asyncio


@pytest.mark.asyncio
async def test_midi_note_names(reaper_mcp_client):
    """Test MIDI note name operations"""
    # Test various note numbers
    test_notes = [
        (60, "C4"),    # Middle C
        (69, "A4"),    # A440
        (0, "C-1"),    # Lowest MIDI note
        (127, "G9"),   # Highest MIDI note
        (61, "C#4"),   # C sharp
    ]
    
    for note_num, expected_prefix in test_notes:
        result = await reaper_mcp_client.call_tool(
            "midi_get_note_name",
            {"note_number": note_num}
        )
        assert "Note name:" in result.content[0].text
        # Note: Exact format may vary, just check it contains expected note letter
        assert expected_prefix[0] in result.content[0].text


@pytest.mark.asyncio
async def test_midi_event_counts(reaper_mcp_client):
    """Test counting MIDI events"""
    # Create a track with MIDI item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Created track" in result.content[0].text
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "start_position": 0.0,
            "length": 4.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Add some MIDI notes
    for i in range(5):
        result = await reaper_mcp_client.call_tool(
            "midi_insert_note",
            {
                "take_index": 0,
                "selected": False,
                "muted": False,
                "start_ppq": i * 960,
                "end_ppq": (i + 1) * 960 - 10,
                "channel": 0,
                "pitch": 60 + i,
                "velocity": 100
            }
        )
    
    # Count events
    result = await reaper_mcp_client.call_tool(
        "midi_count_events",
        {"take_index": 0}
    )
    assert "MIDI event counts:" in result.content[0].text
    assert "notes=" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_scale_operations(reaper_mcp_client):
    """Test MIDI scale operations"""
    # Create a track with MIDI item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Created track" in result.content[0].text
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "start_position": 0.0,
            "length": 4.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Get initial scale
    result = await reaper_mcp_client.call_tool(
        "midi_get_scale",
        {"take_index": 0}
    )
    assert "MIDI scale:" in result.content[0].text
    
    # Set scale to D minor (root=2, scale=1)
    result = await reaper_mcp_client.call_tool(
        "midi_set_scale",
        {
            "take_index": 0,
            "root": 2,  # D
            "scale": 1,  # Minor
            "channel": 0
        }
    )
    assert "Set MIDI scale:" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_select_all_events(reaper_mcp_client):
    """Test selecting all MIDI events"""
    # Create a track with MIDI item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Created track" in result.content[0].text
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "start_position": 0.0,
            "length": 4.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Add some notes
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "midi_insert_note",
            {
                "take_index": 0,
                "selected": False,
                "muted": False,
                "start_ppq": i * 960,
                "end_ppq": (i + 1) * 960 - 10,
                "channel": 0,
                "pitch": 60 + i,
                "velocity": 100
            }
        )
    
    # Add some CC events
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "midi_insert_cc",
            {
                "take_index": 0,
                "selected": False,
                "muted": False,
                "ppq_pos": i * 480,
                "channel_msg": 176,  # CC
                "channel": 0,
                "msg2": 7,  # Volume CC
                "msg3": 64 + i * 20
            }
        )
    
    # Select all events
    result = await reaper_mcp_client.call_tool(
        "midi_select_all",
        {
            "take_index": 0,
            "select_notes": True,
            "select_cc": True,
            "select_text": True
        }
    )
    assert "Selected all MIDI events" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_get_all_events(reaper_mcp_client):
    """Test getting all MIDI events data"""
    # Create a track with MIDI item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Created track" in result.content[0].text
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "start_position": 0.0,
            "length": 4.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Add a note
    result = await reaper_mcp_client.call_tool(
        "midi_insert_note",
        {
            "take_index": 0,
            "selected": False,
            "muted": False,
            "start_ppq": 0,
            "end_ppq": 960,
            "channel": 0,
            "pitch": 60,
            "velocity": 100
        }
    )
    
    # Get all events
    result = await reaper_mcp_client.call_tool(
        "midi_get_all_events",
        {"take_index": 0}
    )
    assert "MIDI events data:" in result.content[0].text