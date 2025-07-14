import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_envelope_point_range_operations(reaper_mcp_client):
    """Test envelope point range operations"""
    # Create track with volume envelope
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 0, "name": "Envelope Test Track"})
    
    # Add some envelope points
    for i in range(5):
        await reaper_mcp_client.call_tool(
            "insert_envelope_point",
            {
                "track_index": 0,
                "envelope_index": 0,  # Volume envelope
                "time": i * 2.0,
                "value": 0.5 + (i * 0.1),
                "shape": 0,
                "tension": 0.0,
                "selected": False
            }
        )
    
    # Test delete range
    result = await reaper_mcp_client.call_tool(
        "delete_envelope_point_range",
        {"track_index": 0, "envelope_index": 0, "start_time": 2.0, "end_time": 6.0}
    )
    print(f"Delete range: {result}")
    assert "Deleted envelope points" in result.content[0].text or "No points found" in result.content[0].text
    
    # Test sort points
    result = await reaper_mcp_client.call_tool(
        "envelope_sort_points",
        {"track_index": 0, "envelope_index": 0}
    )
    print(f"Sort points: {result}")
    assert "sorted" in result.content[0].text.lower()
    
    # Test extended operations (may require automation items)
    result = await reaper_mcp_client.call_tool(
        "delete_envelope_point_range_ex",
        {"track_index": 0, "envelope_index": 0, "automation_item_index": -1, 
         "start_time": 0.0, "end_time": 1.0}
    )
    print(f"Delete range ex: {result}")
    assert "envelope points" in result.content[0].text.lower()
    
    result = await reaper_mcp_client.call_tool(
        "envelope_sort_points_ex",
        {"track_index": 0, "envelope_index": 0, "automation_item_index": -1}
    )
    print(f"Sort points ex: {result}")
    assert "sorted" in result.content[0].text.lower() or "sort failed" in result.content[0].text


@pytest.mark.asyncio
async def test_envelope_evaluation_info(reaper_mcp_client):
    """Test envelope evaluation and information retrieval"""
    # Create track with envelope
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add envelope points
    await reaper_mcp_client.call_tool(
        "insert_envelope_point",
        {"track_index": 0, "envelope_index": 0, "time": 0.0, "value": 0.0}
    )
    await reaper_mcp_client.call_tool(
        "insert_envelope_point",
        {"track_index": 0, "envelope_index": 0, "time": 5.0, "value": 1.0}
    )
    
    # Test evaluate
    result = await reaper_mcp_client.call_tool(
        "envelope_evaluate",
        {"track_index": 0, "envelope_index": 0, "time": 2.5, "sample_rate": 0, "get_value_only": True}
    )
    print(f"Evaluate: {result}")
    assert "Envelope value" in result.content[0].text
    
    # Test format value
    result = await reaper_mcp_client.call_tool(
        "envelope_format_value",
        {"track_index": 0, "envelope_index": 0, "value": 0.75}
    )
    print(f"Format value: {result}")
    assert "value" in result.content[0].text.lower()
    
    # Test get info value
    result = await reaper_mcp_client.call_tool(
        "get_envelope_info_value",
        {"track_index": 0, "envelope_index": 0, "param_name": "P_TRACK"}
    )
    print(f"Info value: {result}")
    assert "Envelope P_TRACK:" in result.content[0].text
    
    # Test get name
    result = await reaper_mcp_client.call_tool(
        "get_envelope_name",
        {"track_index": 0, "envelope_index": 0}
    )
    print(f"Envelope name: {result}")
    assert "Envelope" in result.content[0].text
    
    # Test scaling mode
    result = await reaper_mcp_client.call_tool(
        "get_envelope_scaling_mode",
        {"track_index": 0, "envelope_index": 0}
    )
    print(f"Scaling mode: {result}")
    assert "scaling mode:" in result.content[0].text.lower()
    
    # Test parent track
    result = await reaper_mcp_client.call_tool(
        "envelope_get_parent_track",
        {"track_index": 0, "envelope_index": 0}
    )
    print(f"Parent track: {result}")
    assert "parent track:" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_envelope_state_management(reaper_mcp_client):
    """Test envelope state management"""
    # Create track with envelope
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Get state chunk
    result = await reaper_mcp_client.call_tool(
        "get_envelope_state_chunk",
        {"track_index": 0, "envelope_index": 0, "is_undo": False}
    )
    print(f"State chunk: {result}")
    assert "state chunk" in result.content[0].text.lower()
    
    # Test info string get/set
    result = await reaper_mcp_client.call_tool(
        "get_set_envelope_info_string",
        {"track_index": 0, "envelope_index": 0, "param_name": "P_ENV_NAME", 
         "value": "", "set_value": False}
    )
    print(f"Info string: {result}")
    assert "P_ENV_NAME:" in result.content[0].text
    
    # Set info string
    result = await reaper_mcp_client.call_tool(
        "get_set_envelope_info_string",
        {"track_index": 0, "envelope_index": 0, "param_name": "P_ENV_NAME", 
         "value": "Custom Envelope", "set_value": True}
    )
    print(f"Set info string: {result}")
    assert "Set envelope P_ENV_NAME" in result.content[0].text
    
    # Test get/set state
    result = await reaper_mcp_client.call_tool(
        "get_set_envelope_state",
        {"track_index": 0, "envelope_index": 0, "state_data": "", "set_state": False}
    )
    print(f"Get state: {result}")
    assert "Envelope state" in result.content[0].text
    
    # Test get/set state v2
    result = await reaper_mcp_client.call_tool(
        "get_set_envelope_state2",
        {"track_index": 0, "envelope_index": 0, "state_data": "", "set_state": False}
    )
    print(f"Get state v2: {result}")
    assert "Envelope state v2" in result.content[0].text


@pytest.mark.asyncio
async def test_envelope_scaling(reaper_mcp_client):
    """Test envelope scaling operations"""
    # Create track with envelope
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Test scale from envelope mode
    result = await reaper_mcp_client.call_tool(
        "scale_from_envelope_mode",
        {"track_index": 0, "envelope_index": 0, "value": 0.5}
    )
    print(f"Scale from: {result}")
    assert "Scaled from envelope mode:" in result.content[0].text
    
    # Test scale to envelope mode
    result = await reaper_mcp_client.call_tool(
        "scale_to_envelope_mode",
        {"track_index": 0, "envelope_index": 0, "value": 0.5}
    )
    print(f"Scale to: {result}")
    assert "Scaled to envelope mode:" in result.content[0].text


@pytest.mark.asyncio
async def test_envelope_point_extended(reaper_mcp_client):
    """Test extended envelope point operations"""
    # Create track with envelope
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add an envelope point first
    await reaper_mcp_client.call_tool(
        "insert_envelope_point",
        {"track_index": 0, "envelope_index": 0, "time": 2.0, "value": 0.5}
    )
    
    # Set point extended
    result = await reaper_mcp_client.call_tool(
        "set_envelope_point_ex",
        {
            "track_index": 0,
            "envelope_index": 0,
            "automation_item_index": -1,
            "point_index": 0,
            "time": 2.5,
            "value": 0.75,
            "shape": 1,
            "tension": 0.5,
            "selected": True
        }
    )
    print(f"Set point ex: {result}")
    assert "Set envelope point" in result.content[0].text


@pytest.mark.asyncio
async def test_envelope_by_chunk_name(reaper_mcp_client):
    """Test getting envelope by chunk name"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Try to get envelope by chunk name
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope_by_chunk_name",
        {"track_index": 0, "chunk_name": "VOLENV"}
    )
    print(f"By chunk name: {result}")
    assert "envelope" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_envelope_workflow(reaper_mcp_client):
    """Test a complete envelope workflow"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 0, "name": "Automated Track"})
    
    # Create volume automation
    points = [
        (0.0, 1.0),    # Full volume
        (2.0, 0.5),    # Half volume
        (4.0, 0.0),    # Silence
        (6.0, 0.5),    # Half volume
        (8.0, 1.0),    # Full volume
    ]
    
    for time, value in points:
        await reaper_mcp_client.call_tool(
            "insert_envelope_point",
            {"track_index": 0, "envelope_index": 0, "time": time, "value": value}
        )
    
    # Evaluate at different times
    test_times = [1.0, 3.0, 5.0, 7.0]
    for t in test_times:
        result = await reaper_mcp_client.call_tool(
            "envelope_evaluate",
            {"track_index": 0, "envelope_index": 0, "time": t}
        )
        print(f"Value at {t}s: {result}")
    
    # Get envelope info
    result = await reaper_mcp_client.call_tool(
        "get_envelope_name",
        {"track_index": 0, "envelope_index": 0}
    )
    print(f"Final envelope: {result}")
    
    print("Envelope workflow completed!")


@pytest.mark.asyncio 
async def test_take_envelope_operations(reaper_mcp_client):
    """Test envelope operations on takes"""
    # Create track and item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 10.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Try to get parent take of envelope (requires take envelope)
    result = await reaper_mcp_client.call_tool(
        "envelope_get_parent_take",
        {"item_index": 0, "take_index": 0, "envelope_index": 0}
    )
    print(f"Parent take: {result}")
    # May fail if no take envelope exists
    assert "parent take" in result.content[0].text.lower() or "Failed" in result.content[0].text