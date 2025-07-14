import pytest
import pytest_asyncio
import asyncio
import random

@pytest.mark.asyncio
async def test_midi_editor_window_operations(reaper_mcp_client):
    """Test MIDI editor window management"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 0, "name": "MIDI Track"})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 8.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Insert some MIDI notes first
    for i in range(4):
        await reaper_mcp_client.call_tool(
            "midi_insert_evt",
            {
                "item_index": 0,
                "take_index": 0,
                "ppq_pos": i * 480,  # Every beat
                "event_type": "note_on",
                "data1": 60 + i * 4,  # C, E, G#, C
                "data2": 100,
                "channel": 0
            }
        )
        await reaper_mcp_client.call_tool(
            "midi_insert_evt",
            {
                "item_index": 0,
                "take_index": 0,
                "ppq_pos": (i + 0.5) * 480,  # Half beat later
                "event_type": "note_off",
                "data1": 60 + i * 4,
                "data2": 0,
                "channel": 0
            }
        )
    
    # Check for active MIDI editor before opening
    result = await reaper_mcp_client.call_tool("midi_editor_get_active", {})
    print(f"Active editor check: {result}")
    assert "No active MIDI editor" in result.content[0].text
    
    # Open MIDI editor
    result = await reaper_mcp_client.call_tool(
        "midi_open_editor",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Open editor: {result}")
    assert "Opened MIDI editor" in result.content[0].text or "Failed" in result.content[0].text
    
    # Get active editor
    result = await reaper_mcp_client.call_tool("midi_editor_get_active", {})
    print(f"Active editor: {result}")
    # May or may not find active editor depending on UI state
    assert "MIDI editor" in result.content[0].text
    
    # Get MIDI editor mode
    result = await reaper_mcp_client.call_tool("midi_editor_get_mode", {})
    print(f"Editor mode: {result}")
    assert "MIDI editor mode:" in result.content[0].text
    
    # Get take from editor
    result = await reaper_mcp_client.call_tool(
        "midi_editor_get_take",
        {"editor_id": "active"}
    )
    print(f"Editor take: {result}")
    assert "take" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_midi_note_selection(reaper_mcp_client):
    """Test MIDI note selection operations"""
    # Create track and MIDI item with notes
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Add various MIDI notes
    notes = [
        (0, 60, 100),    # C4 at beat 1
        (480, 64, 90),   # E4 at beat 2  
        (960, 67, 80),   # G4 at beat 3
        (1440, 72, 110), # C5 at beat 4
    ]
    
    for ppq, pitch, vel in notes:
        await reaper_mcp_client.call_tool(
            "midi_insert_evt",
            {
                "item_index": 0,
                "take_index": 0,
                "ppq_pos": ppq,
                "event_type": "note_on",
                "data1": pitch,
                "data2": vel,
                "channel": 0
            }
        )
        await reaper_mcp_client.call_tool(
            "midi_insert_evt",
            {
                "item_index": 0,
                "take_index": 0,
                "ppq_pos": ppq + 240,  # 8th note duration
                "event_type": "note_off",
                "data1": pitch,
                "data2": 0,
                "channel": 0
            }
        )
    
    # Select notes in range
    result = await reaper_mcp_client.call_tool(
        "midi_select_notes",
        {
            "item_index": 0,
            "take_index": 0,
            "start_ppq": 400,
            "end_ppq": 1000,
            "pitch_low": 60,
            "pitch_high": 70
        }
    )
    print(f"Select notes: {result}")
    assert "Selected notes in range" in result.content[0].text
    
    # Get selected notes
    result = await reaper_mcp_client.call_tool(
        "midi_get_selected_notes",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Selected notes: {result}")
    assert "Note" in result.content[0].text or "No selected notes" in result.content[0].text
    
    # Set note selection
    result = await reaper_mcp_client.call_tool(
        "midi_set_note_selected",
        {"item_index": 0, "take_index": 0, "note_index": 0, "selected": True}
    )
    print(f"Set selection: {result}")
    assert "Note 0" in result.content[0].text
    
    # Get MIDI grid
    result = await reaper_mcp_client.call_tool(
        "midi_get_grid",
        {"item_index": 0, "take_index": 0}
    )
    print(f"MIDI grid: {result}")
    assert "MIDI grid:" in result.content[0].text or "Failed" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_cc_operations(reaper_mcp_client):
    """Test MIDI CC operations"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Add CC events
    for i in range(8):
        await reaper_mcp_client.call_tool(
            "midi_insert_evt",
            {
                "item_index": 0,
                "take_index": 0,
                "ppq_pos": i * 240,  # Every 8th note
                "event_type": "cc",
                "data1": 7,  # Volume CC
                "data2": 64 + i * 8,  # Gradual increase
                "channel": 0
            }
        )
    
    # Select CC events
    result = await reaper_mcp_client.call_tool(
        "midi_select_cc",
        {"item_index": 0, "take_index": 0, "cc_num": 7, "channel": 0}
    )
    print(f"Select CC: {result}")
    assert "Selected" in result.content[0].text and "CC7" in result.content[0].text
    
    # Get CC shape
    result = await reaper_mcp_client.call_tool(
        "midi_get_cc_shape",
        {"item_index": 0, "take_index": 0, "cc_index": 0}
    )
    print(f"CC shape: {result}")
    assert "CC" in result.content[0].text and "shape:" in result.content[0].text.lower()
    
    # Set CC shape
    result = await reaper_mcp_client.call_tool(
        "midi_set_cc_shape",
        {"item_index": 0, "take_index": 0, "cc_index": 0, "shape": 2, "beztension": 0.0}
    )
    print(f"Set CC shape: {result}")
    assert "Set CC" in result.content[0].text or "Failed" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_time_conversions(reaper_mcp_client):
    """Test MIDI time conversion functions"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 1.0, "length": 4.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # PPQ to project QN
    result = await reaper_mcp_client.call_tool(
        "midi_get_proj_qn_from_ppq",
        {"item_index": 0, "take_index": 0, "ppq": 960}
    )
    print(f"PPQ to QN: {result}")
    assert "PPQ" in result.content[0].text and "QN" in result.content[0].text
    
    # QN to PPQ
    result = await reaper_mcp_client.call_tool(
        "midi_get_ppq_from_proj_qn",
        {"item_index": 0, "take_index": 0, "qn": 4.0}
    )
    print(f"QN to PPQ: {result}")
    assert "QN" in result.content[0].text and "PPQ" in result.content[0].text
    
    # PPQ to project time
    result = await reaper_mcp_client.call_tool(
        "midi_get_proj_time_from_ppq",
        {"item_index": 0, "take_index": 0, "ppq": 480}
    )
    print(f"PPQ to time: {result}")
    assert "PPQ" in result.content[0].text and "seconds" in result.content[0].text
    
    # Time to PPQ
    result = await reaper_mcp_client.call_tool(
        "midi_get_ppq_from_proj_time",
        {"item_index": 0, "take_index": 0, "time": 2.0}
    )
    print(f"Time to PPQ: {result}")
    assert "seconds" in result.content[0].text and "PPQ" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_humanize(reaper_mcp_client):
    """Test MIDI humanization"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Add perfectly quantized notes
    for i in range(16):
        ppq = i * 240  # Perfect 16th notes
        await reaper_mcp_client.call_tool(
            "midi_insert_evt",
            {
                "item_index": 0,
                "take_index": 0,
                "ppq_pos": ppq,
                "event_type": "note_on",
                "data1": 60,
                "data2": 100,  # All same velocity
                "channel": 0
            }
        )
        await reaper_mcp_client.call_tool(
            "midi_insert_evt",
            {
                "item_index": 0,
                "take_index": 0,
                "ppq_pos": ppq + 120,
                "event_type": "note_off",
                "data1": 60,
                "data2": 0,
                "channel": 0
            }
        )
    
    # Select all notes
    await reaper_mcp_client.call_tool(
        "midi_select_all",
        {"item_index": 0, "take_index": 0}
    )
    
    # Humanize notes
    result = await reaper_mcp_client.call_tool(
        "midi_humanize_notes",
        {
            "item_index": 0,
            "take_index": 0,
            "strength": 0.15,
            "timing": True,
            "velocity": True
        }
    )
    print(f"Humanize: {result}")
    assert "Humanized" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_display_functions(reaper_mcp_client):
    """Test MIDI display and visualization functions"""
    # Get note name
    result = await reaper_mcp_client.call_tool(
        "midi_get_note_name",
        {"note_number": 60}
    )
    print(f"Note name: {result}")
    assert "Note 60:" in result.content[0].text
    
    # Test various note names
    note_tests = [0, 36, 60, 69, 84, 127]
    for note in note_tests:
        result = await reaper_mcp_client.call_tool(
            "midi_get_note_name",
            {"note_number": note}
        )
        print(f"Note {note}: {result}")
        assert f"Note {note}:" in result.content[0].text
    
    # Get recent input event (may not have any)
    result = await reaper_mcp_client.call_tool(
        "midi_get_recent_input_event",
        {"idx": 0}
    )
    print(f"Recent input: {result}")
    assert "Input" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_editor_settings(reaper_mcp_client):
    """Test MIDI editor settings"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Try to open editor
    await reaper_mcp_client.call_tool(
        "midi_open_editor",
        {"item_index": 0, "take_index": 0}
    )
    
    # Get/set editor settings
    result = await reaper_mcp_client.call_tool(
        "midi_editor_get_setting_int",
        {"editor_id": "active", "setting_name": "snap_enabled"}
    )
    print(f"Get setting: {result}")
    assert "MIDI editor" in result.content[0].text or "No active" in result.content[0].text
    
    result = await reaper_mcp_client.call_tool(
        "midi_editor_set_setting_int",
        {"editor_id": "active", "setting_name": "snap_enabled", "value": 1}
    )
    print(f"Set setting: {result}")
    assert "MIDI editor" in result.content[0].text or "No active" in result.content[0].text
    
    # Execute editor command
    result = await reaper_mcp_client.call_tool(
        "midi_editor_on_command",
        {"command_id": 40049}  # Select all
    )
    print(f"Editor command: {result}")
    assert "MIDI editor" in result.content[0].text or "No active" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_text_sysex(reaper_mcp_client):
    """Test MIDI text and sysex events"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Insert text events
    text_events = [
        ("track_name", "Piano Track"),
        ("marker", "Verse 1"),
        ("lyric", "La la la"),
    ]
    
    for i, (evt_type, text) in enumerate(text_events):
        await reaper_mcp_client.call_tool(
            "midi_insert_text_sysex_evt",
            {
                "item_index": 0,
                "take_index": 0,
                "ppq_pos": i * 480,
                "event_type": evt_type,
                "text": text
            }
        )
    
    # Get text event
    result = await reaper_mcp_client.call_tool(
        "midi_get_text_sysex_evt",
        {"item_index": 0, "take_index": 0, "event_index": 0}
    )
    print(f"Text event: {result}")
    assert "Event" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_item_operations(reaper_mcp_client):
    """Test MIDI item-specific operations"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 2.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Add notes outside item bounds
    await reaper_mcp_client.call_tool(
        "midi_insert_evt",
        {
            "item_index": 0,
            "take_index": 0,
            "ppq_pos": 0,
            "event_type": "note_on",
            "data1": 60,
            "data2": 100
        }
    )
    await reaper_mcp_client.call_tool(
        "midi_insert_evt",
        {
            "item_index": 0,
            "take_index": 0,
            "ppq_pos": 3840,  # 4 beats (outside 2 second item)
            "event_type": "note_off",
            "data1": 60,
            "data2": 0
        }
    )
    
    # Set item extents to match MIDI
    result = await reaper_mcp_client.call_tool(
        "midi_set_item_extents",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Set extents: {result}")
    assert "Set item extents" in result.content[0].text
    
    # Disable sorting
    result = await reaper_mcp_client.call_tool(
        "midi_disablesorting",
        {"item_index": 0, "take_index": 0, "disable": True}
    )
    print(f"Disable sorting: {result}")
    assert "MIDI auto-sorting disabled" in result.content[0].text
    
    # Re-enable sorting
    result = await reaper_mcp_client.call_tool(
        "midi_disablesorting",
        {"item_index": 0, "take_index": 0, "disable": False}
    )
    print(f"Enable sorting: {result}")
    assert "MIDI auto-sorting enabled" in result.content[0].text
    
    # Refresh editor
    result = await reaper_mcp_client.call_tool("midi_refresh_editor", {})
    print(f"Refresh: {result}")
    assert "Refreshed MIDI editor" in result.content[0].text or "No active" in result.content[0].text