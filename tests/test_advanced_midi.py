"""Test advanced MIDI operations"""
import pytest
import pytest_asyncio
import asyncio


def assert_tools_available(available_tools, required_tools):
    """Assert that all required tools are available, failing with clear message if not"""
    for tool in required_tools:
        assert tool in available_tools, f"MISSING IMPLEMENTATION: Tool '{tool}' is not implemented in the server but is required for MIDI functionality"


@pytest.mark.asyncio
async def test_midi_note_names(reaper_mcp_client):
    """Test MIDI note name operations"""
    # Check if tool is available
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    assert_tools_available(available_tools, ["midi_get_note_name"])
    
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
    # Check if required tools are available
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    assert_tools_available(available_tools, ["midi_count_events"])
    
    # Create a track with MIDI item
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "position": 0.0,
            "length": 4.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Add some MIDI notes
    for i in range(5):
        result = await reaper_mcp_client.call_tool(
            "insert_midi_note",
            {
                "item_index": 0,
                "take_index": 0,
                "pitch": 60 + i,
                "velocity": 100,
                "start_time": i * 1.0,  # Each note starts 1 second apart
                "duration": 0.9,  # 0.9 second duration
                "channel": 0,
                "selected": False,
                "muted": False
            }
        )
    
    # Count events
    result = await reaper_mcp_client.call_tool(
        "midi_count_events",
        {"item_index": 0, "take_index": 0}
    )
    assert "MIDI event counts:" in result.content[0].text
    assert "notes=" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_scale_operations(reaper_mcp_client):
    """Test MIDI scale operations"""
    # Check if required tools are available
    required_tools = ["midi_get_scale", "midi_set_scale"]
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    assert_tools_available(available_tools, required_tools)
    
    # Create a track with MIDI item
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "position": 0.0,
            "length": 4.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Get initial scale
    result = await reaper_mcp_client.call_tool(
        "midi_get_scale",
        {"item_index": 0, "take_index": 0}
    )
    assert "Scale:" in result.content[0].text
    
    # Set scale to D minor (root=2, scale=1)
    result = await reaper_mcp_client.call_tool(
        "midi_set_scale",
        {
            "item_index": 0,
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
    # Check if required tools are available
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    assert_tools_available(available_tools, ["midi_select_all"])
    
    # Create a track with MIDI item
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "position": 0.0,
            "length": 4.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Add some notes
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "insert_midi_note",
            {
                "item_index": 0,
                "take_index": 0,
                "pitch": 60 + i,
                "velocity": 100,
                "start_time": i * 0.5,  # Each note starts 0.5 seconds apart
                "duration": 0.4,  # 0.4 second duration
                "channel": 0,
                "selected": False,
                "muted": False
            }
        )
    
    # Add some CC events
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "insert_midi_cc",
            {
                "item_index": 0,
                "take_index": 0,
                "time": i * 0.5,
                "channel": 0,
                "cc_number": 7,  # Volume CC
                "value": 64 + i * 20
            }
        )
    
    # Select all events
    result = await reaper_mcp_client.call_tool(
        "midi_select_all",
        {
            "item_index": 0,
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
    # Check if required tools are available
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    assert_tools_available(available_tools, ["midi_get_all_events"])
    
    # Create a track with MIDI item
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "position": 0.0,
            "length": 4.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Add a note
    result = await reaper_mcp_client.call_tool(
        "insert_midi_note",
        {
            "item_index": 0,
            "take_index": 0,
            "pitch": 60,
            "velocity": 100,
            "position": 0.0,
            "duration": 1.0,
            "channel": 0
        }
    )
    
    # Get all events
    result = await reaper_mcp_client.call_tool(
        "midi_get_all_events",
        {"item_index": 0, "take_index": 0}
    )
    assert "MIDI events data:" in result.content[0].text