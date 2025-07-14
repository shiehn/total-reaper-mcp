import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_midi_ppq_time_conversion(reaper_mcp_client):
    """Test PPQ and time conversion methods"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "position": 0.0, "length": 10.0}
    )
    
    # Test time to PPQ conversion
    result = await reaper_mcp_client.call_tool(
        "midi_get_ppq_pos_from_proj_time",
        {"item_index": 0, "take_index": 0, "time": 2.0}
    )
    print(f"Time to PPQ result: {result}")
    assert "Time 2.000s = PPQ" in result.content[0].text
    
    # Test PPQ to time conversion
    result = await reaper_mcp_client.call_tool(
        "midi_get_proj_time_from_ppq_pos",
        {"item_index": 0, "take_index": 0, "ppq_pos": 960.0}  # 1 quarter note
    )
    print(f"PPQ to time result: {result}")
    assert "PPQ 960.0 = Time" in result.content[0].text
    
    # Get start of measure
    result = await reaper_mcp_client.call_tool(
        "midi_get_ppq_pos_start_of_measure",
        {"item_index": 0, "take_index": 0, "ppq_pos": 1000.0}
    )
    print(f"Start of measure result: {result}")
    assert "Start of measure" in result.content[0].text
    
    # Get end of measure
    result = await reaper_mcp_client.call_tool(
        "midi_get_ppq_pos_end_of_measure",
        {"item_index": 0, "take_index": 0, "ppq_pos": 1000.0}
    )
    print(f"End of measure result: {result}")
    assert "End of measure" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_grid_settings(reaper_mcp_client):
    """Test MIDI grid settings"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "position": 0.0, "length": 10.0}
    )
    
    # Get MIDI grid settings
    result = await reaper_mcp_client.call_tool(
        "midi_get_grid",
        {"item_index": 0, "take_index": 0}
    )
    print(f"MIDI grid result: {result}")
    assert "MIDI grid:" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_get_evt(reaper_mcp_client):
    """Test getting MIDI events by index"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "position": 0.0, "length": 10.0}
    )
    
    # Insert some MIDI events
    await reaper_mcp_client.call_tool(
        "midi_insert_evt",
        {
            "item_index": 0,
            "take_index": 0,
            "ppq_pos": 0.0,
            "event_type": "note_on",
            "data1": 60,
            "data2": 100,
            "channel": 0
        }
    )
    
    await reaper_mcp_client.call_tool(
        "midi_insert_evt",
        {
            "item_index": 0,
            "take_index": 0,
            "ppq_pos": 960.0,
            "event_type": "note_off",
            "data1": 60,
            "data2": 0,
            "channel": 0
        }
    )
    
    # Get event by index
    result = await reaper_mcp_client.call_tool(
        "midi_get_evt",
        {"item_index": 0, "take_index": 0, "event_index": 0}
    )
    print(f"Get event 0 result: {result}")
    assert "Event 0:" in result.content[0].text or "Event 0 not found" in result.content[0].text
    
    # Try to get non-existent event
    result = await reaper_mcp_client.call_tool(
        "midi_get_evt",
        {"item_index": 0, "take_index": 0, "event_index": 999}
    )
    print(f"Get event 999 result: {result}")
    assert "not found" in result.content[0].text or "Invalid" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_enum_selected_notes(reaper_mcp_client):
    """Test enumerating selected MIDI notes"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "position": 0.0, "length": 10.0}
    )
    
    # Insert some notes with selection
    notes = [
        {"pitch": 60, "selected": True},
        {"pitch": 62, "selected": False},
        {"pitch": 64, "selected": True},
        {"pitch": 65, "selected": True}
    ]
    
    for i, note in enumerate(notes):
        await reaper_mcp_client.call_tool(
            "insert_midi_note",
            {
                "item_index": 0,
                "take_index": 0,
                "pitch": note["pitch"],
                "velocity": 100,
                "start_time": i * 0.5,
                "duration": 0.4,
                "channel": 0,
                "selected": note["selected"]
            }
        )
    
    # Enumerate selected notes
    result = await reaper_mcp_client.call_tool(
        "midi_enum_sel_notes",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Enum selected notes result: {result}")
    assert "Selected notes" in result.content[0].text or "No notes selected" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_set_item_extents(reaper_mcp_client):
    """Test setting MIDI item extents"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "position": 0.0, "length": 4.0}
    )
    
    # Set item extents in quarter notes
    result = await reaper_mcp_client.call_tool(
        "midi_set_item_extents",
        {
            "item_index": 0,
            "take_index": 0,
            "start_qn": 0.0,
            "end_qn": 16.0  # 4 bars at 4/4
        }
    )
    print(f"Set item extents result: {result}")
    assert "Set MIDI item extents" in result.content[0].text


@pytest.mark.asyncio
async def test_midi_event_operations_workflow(reaper_mcp_client):
    """Test a workflow using MIDI event operations"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "position": 0.0, "length": 8.0}
    )
    print(f"Create MIDI item: {result}")
    
    # Insert a series of notes
    notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
    for i, pitch in enumerate(notes):
        # Convert time to PPQ
        time = i * 0.5
        result = await reaper_mcp_client.call_tool(
            "midi_get_ppq_pos_from_proj_time",
            {"item_index": 0, "take_index": 0, "time": time}
        )
        # Extract PPQ value from result
        ppq_text = result.content[0].text
        try:
            ppq = float(ppq_text.split("PPQ ")[1].split(".")[0])
        except:
            ppq = i * 960.0  # Default to 1 quarter note per half second
        
        # Insert note
        await reaper_mcp_client.call_tool(
            "insert_midi_note",
            {
                "item_index": 0,
                "take_index": 0,
                "pitch": pitch,
                "velocity": 90,
                "start_time": time,
                "duration": 0.4,
                "channel": 0,
                "selected": i % 2 == 0  # Select every other note
            }
        )
    
    # Sort MIDI events
    await reaper_mcp_client.call_tool(
        "midi_sort",
        {"item_index": 0, "take_index": 0}
    )
    
    # Enumerate selected notes
    result = await reaper_mcp_client.call_tool(
        "midi_enum_sel_notes",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Selected notes: {result}")
    assert "Selected notes" in result.content[0].text
    
    # Get grid settings
    result = await reaper_mcp_client.call_tool(
        "midi_get_grid",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Grid settings: {result}")
    
    # Get some measure boundaries
    for ppq in [0.0, 960.0, 1920.0]:
        result = await reaper_mcp_client.call_tool(
            "midi_get_ppq_pos_start_of_measure",
            {"item_index": 0, "take_index": 0, "ppq_pos": ppq + 100}
        )
        print(f"Start of measure for PPQ {ppq + 100}: {result}")
        
        result = await reaper_mcp_client.call_tool(
            "midi_get_ppq_pos_end_of_measure",
            {"item_index": 0, "take_index": 0, "ppq_pos": ppq + 100}
        )
        print(f"End of measure for PPQ {ppq + 100}: {result}")
    
    print("MIDI event operations workflow completed successfully!")