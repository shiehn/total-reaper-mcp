import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_create_midi_item(reaper_mcp_client):
    """Test creating a MIDI item"""
    # Create a track first
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    assert "success" in result.content[0].text.lower()
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    print(f"Create MIDI item result: {result}")
    assert "created midi item" in result.content[0].text.lower()
    
    # Verify item was created
    result = await reaper_mcp_client.call_tool(
        "count_media_items",
        {}
    )
    assert "1" in result.content[0].text

@pytest.mark.asyncio
async def test_midi_note_operations(reaper_mcp_client):
    """Test inserting MIDI notes"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "start_time": 0.0, "length": 8.0}
    )
    
    # Insert a C4 note
    result = await reaper_mcp_client.call_tool(
        "insert_midi_note",
        {
            "item_index": 0,
            "take_index": 0,
            "pitch": 60,  # C4
            "velocity": 100,
            "start_time": 0.0,
            "duration": 1.0,
            "channel": 0
        }
    )
    print(f"Insert MIDI note result: {result}")
    assert "inserted midi note" in result.content[0].text.lower()
    assert "pitch=60" in result.content[0].text
    
    # Insert another note (E4)
    result = await reaper_mcp_client.call_tool(
        "insert_midi_note",
        {
            "item_index": 0,
            "take_index": 0,
            "pitch": 64,  # E4
            "velocity": 80,
            "start_time": 1.0,
            "duration": 1.0,
            "channel": 0
        }
    )
    assert "inserted midi note" in result.content[0].text.lower()
    
    # Sort MIDI events
    result = await reaper_mcp_client.call_tool(
        "midi_sort",
        {"item_index": 0, "take_index": 0}
    )
    print(f"MIDI sort result: {result}")
    assert "sorted successfully" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_midi_cc_operations(reaper_mcp_client):
    """Test inserting MIDI CC events"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    
    # Insert volume CC (CC7)
    result = await reaper_mcp_client.call_tool(
        "insert_midi_cc",
        {
            "item_index": 0,
            "take_index": 0,
            "time": 0.0,
            "channel": 0,
            "cc_number": 7,  # Volume
            "value": 100
        }
    )
    print(f"Insert MIDI CC result: {result}")
    assert "inserted midi cc" in result.content[0].text.lower()
    assert "cc7" in result.content[0].text.lower()
    
    # Insert pan CC (CC10)
    result = await reaper_mcp_client.call_tool(
        "insert_midi_cc",
        {
            "item_index": 0,
            "take_index": 0,
            "time": 2.0,
            "channel": 0,
            "cc_number": 10,  # Pan
            "value": 64  # Center
        }
    )
    assert "inserted midi cc" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_take_operations(reaper_mcp_client):
    """Test take management operations"""
    # Create track and MIDI item
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    
    # Count takes (should be 1)
    result = await reaper_mcp_client.call_tool(
        "count_takes",
        {"item_index": 0}
    )
    print(f"Count takes result: {result}")
    assert "1 takes" in result.content[0].text or "1 take" in result.content[0].text
    
    # Get active take (should be 0)
    result = await reaper_mcp_client.call_tool(
        "get_active_take",
        {"item_index": 0}
    )
    print(f"Get active take result: {result}")
    assert "active take" in result.content[0].text.lower()
    
    # Note: To test multiple takes, we would need to implement add_take_to_item
    # For now, we can only test with the single take created with the MIDI item

@pytest.mark.asyncio
async def test_midi_workflow(reaper_mcp_client):
    """Test a complete MIDI workflow"""
    # Create track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Set track name
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 0, "name": "MIDI Piano"}
    )
    
    # Create MIDI item
    await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    
    # Insert a C major chord (C-E-G)
    notes = [
        {"pitch": 60, "name": "C"},  # C4
        {"pitch": 64, "name": "E"},  # E4
        {"pitch": 67, "name": "G"}   # G4
    ]
    
    for note in notes:
        result = await reaper_mcp_client.call_tool(
            "insert_midi_note",
            {
                "item_index": 0,
                "take_index": 0,
                "pitch": note["pitch"],
                "velocity": 90,
                "start_time": 0.0,
                "duration": 2.0,
                "channel": 0
            }
        )
        print(f"Inserted {note['name']} note: {result}")
        assert "inserted midi note" in result.content[0].text.lower()
    
    # Add expression CC
    result = await reaper_mcp_client.call_tool(
        "insert_midi_cc",
        {
            "item_index": 0,
            "take_index": 0,
            "time": 0.0,
            "channel": 0,
            "cc_number": 11,  # Expression
            "value": 127
        }
    )
    assert "inserted midi cc" in result.content[0].text.lower()
    
    # Sort MIDI events
    result = await reaper_mcp_client.call_tool(
        "midi_sort",
        {"item_index": 0, "take_index": 0}
    )
    assert "sorted successfully" in result.content[0].text.lower()
    
    print("MIDI workflow completed successfully!")

@pytest.mark.asyncio
async def test_midi_error_handling(reaper_mcp_client):
    """Test error handling for MIDI operations"""
    # Try to create MIDI item on non-existent track
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 999, "start_time": 0.0, "length": 4.0}
    )
    assert "failed" in result.content[0].text.lower()
    
    # Try to insert note in non-existent item
    result = await reaper_mcp_client.call_tool(
        "insert_midi_note",
        {
            "item_index": 999,
            "take_index": 0,
            "pitch": 60,
            "velocity": 100,
            "start_time": 0.0,
            "duration": 1.0
        }
    )
    assert "failed" in result.content[0].text.lower()
    
    # Try to insert invalid MIDI pitch
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    
    # This should fail at the schema validation level
    try:
        result = await reaper_mcp_client.call_tool(
            "insert_midi_note",
            {
                "item_index": 0,
                "take_index": 0,
                "pitch": 200,  # Invalid pitch > 127
                "velocity": 100,
                "start_time": 0.0,
                "duration": 1.0
            }
        )
        # If we get here, check for error message
        assert "error" in result.content[0].text.lower() or "invalid" in result.content[0].text.lower()
    except Exception as e:
        # Schema validation might raise an exception
        print(f"Expected validation error: {e}")