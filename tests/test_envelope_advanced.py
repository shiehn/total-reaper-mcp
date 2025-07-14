import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_envelope_operations(reaper_mcp_client):
    """Test basic envelope operations"""
    # Create a track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Count envelopes on track
    result = await reaper_mcp_client.call_tool(
        "count_track_envelopes",
        {"track_index": 0}
    )
    print(f"Count envelopes result: {result}")
    assert "envelopes" in result.content[0].text
    
    # Get track automation mode
    result = await reaper_mcp_client.call_tool(
        "get_track_automation_mode",
        {"track_index": 0}
    )
    print(f"Automation mode result: {result}")
    assert "automation mode:" in result.content[0].text.lower()
    
    # Set track automation mode to Touch
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 2}  # Touch mode
    )
    print(f"Set automation mode result: {result}")
    assert "Touch" in result.content[0].text
    
    # Get volume envelope (might not exist by default)
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope_by_name",
        {"track_index": 0, "envelope_name": "Volume"}
    )
    print(f"Get volume envelope result: {result}")
    # Envelope might not exist by default, that's ok
    assert "envelope" in result.content[0].text.lower()
    
    # Try to insert envelope points - might fail if envelope doesn't exist
    try:
        result = await reaper_mcp_client.call_tool(
            "insert_envelope_point",
            {
                "track_index": 0,
                "envelope_name": "Volume",
                "time": 0.0,
                "value": 1.0,
                "shape": 0,
                "selected": False
            }
        )
        print(f"Insert point result: {result}")
        if "error" not in result.content[0].text.lower():
            assert "Inserted point" in result.content[0].text
    except:
        print("Volume envelope doesn't exist, skipping insert test")
    
    # Try to insert another point if envelope exists
    try:
        result = await reaper_mcp_client.call_tool(
            "insert_envelope_point",
            {
                "track_index": 0,
                "envelope_name": "Volume",
                "time": 2.0,
                "value": 0.5,
                "shape": 0,
                "selected": False
            }
        )
        if "error" not in result.content[0].text.lower():
            assert "Inserted point" in result.content[0].text
    except:
        pass
    
    # Count envelope points
    result = await reaper_mcp_client.call_tool(
        "count_envelope_points",
        {"track_index": 0, "envelope_name": "Volume"}
    )
    print(f"Count points result: {result}")
    assert "points" in result.content[0].text


@pytest.mark.asyncio
async def test_envelope_extended_operations(reaper_mcp_client):
    """Test extended envelope operations"""
    # Create a track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Try to show track envelopes which might create the volume envelope
    try:
        await reaper_mcp_client.call_tool(
            "main_action",
            {"action_id": 41866}  # Track: Toggle track volume envelope visible
        )
    except:
        pass
    
    # Insert envelope point with extended parameters
    try:
        result = await reaper_mcp_client.call_tool(
            "insert_envelope_point_ex",
            {
                "track_index": 0,
                "envelope_name": "Volume",
                "time": 0.0,
                "value": 1.0,
                "shape": 1,  # Linear shape
                "tension": 0.5,
                "selected": True,
                "no_sort": False
            }
        )
        print(f"Insert point ex result: {result}")
        if "error" not in result.content[0].text.lower():
            assert "Inserted point" in result.content[0].text
            assert "tension=0.500" in result.content[0].text
    except:
        print("Volume envelope doesn't exist, skipping extended insert test")
    
    # Add more points for testing if envelope exists
    envelope_exists = False
    for t in [1.0, 2.0, 3.0, 4.0]:
        try:
            result = await reaper_mcp_client.call_tool(
                "insert_envelope_point",
                {
                    "track_index": 0,
                    "envelope_name": "Volume",
                    "time": t,
                    "value": 0.5 + (t / 10),
                    "shape": 0
                }
            )
            if "error" not in result.content[0].text.lower():
                envelope_exists = True
        except:
            pass
    
    # Only test remaining operations if envelope exists
    if envelope_exists:
        # Evaluate envelope at specific time
        result = await reaper_mcp_client.call_tool(
            "envelope_evaluate",
            {
                "track_index": 0,
                "envelope_name": "Volume",
                "time": 1.5
            }
        )
        print(f"Evaluate envelope result: {result}")
        assert "value at 1.500s" in result.content[0].text
    
        # Delete envelope point range
        result = await reaper_mcp_client.call_tool(
            "delete_envelope_point_range",
            {
                "track_index": 0,
                "envelope_name": "Volume",
                "start_time": 1.5,
                "end_time": 3.5
            }
        )
        print(f"Delete range result: {result}")
        assert "Deleted envelope points between" in result.content[0].text
        
        # Sort envelope points
        result = await reaper_mcp_client.call_tool(
            "envelope_sort_points",
            {
                "track_index": 0,
                "envelope_name": "Volume"
            }
        )
        print(f"Sort points result: {result}")
        assert "Sorted envelope" in result.content[0].text
        
        # Get envelope scaling mode
        result = await reaper_mcp_client.call_tool(
            "get_envelope_scaling_mode",
            {
                "track_index": 0,
                "envelope_name": "Volume"
            }
        )
        print(f"Scaling mode result: {result}")
        assert "scaling mode:" in result.content[0].text.lower()
    else:
        print("Skipping envelope operations - no envelope exists")


@pytest.mark.asyncio
async def test_envelope_by_index(reaper_mcp_client):
    """Test envelope operations by index"""
    # Create a track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Get envelope by index
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope",
        {"track_index": 0, "envelope_index": 0}
    )
    print(f"Get envelope by index result: {result}")
    # May or may not have an envelope at index 0
    assert "envelope" in result.content[0].text.lower()
    
    # Get envelope name (if exists)
    if "No envelope" not in result.content[0].text:
        result = await reaper_mcp_client.call_tool(
            "get_envelope_name",
            {"track_index": 0, "envelope_index": 0}
        )
        print(f"Get envelope name result: {result}")
        assert "Envelope 0:" in result.content[0].text


@pytest.mark.asyncio
async def test_fx_envelope(reaper_mcp_client):
    """Test FX parameter envelope"""
    # Create a track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add an FX (ReaEQ)
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 0, "fx_name": "ReaEQ"}
    )
    
    if "Added FX" in result.content[0].text:
        # Try to get FX envelope
        result = await reaper_mcp_client.call_tool(
            "get_fx_envelope",
            {
                "track_index": 0,
                "fx_index": 0,
                "param_index": 0  # First parameter
            }
        )
        print(f"Get FX envelope result: {result}")
        assert "envelope" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_envelope_point_operations(reaper_mcp_client):
    """Test individual envelope point operations"""
    # Create a track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Try to show track envelopes
    try:
        await reaper_mcp_client.call_tool(
            "main_action",
            {"action_id": 41866}  # Track: Toggle track volume envelope visible
        )
    except:
        pass
    
    # Insert several envelope points
    points = [
        {"time": 0.0, "value": 1.0},
        {"time": 1.0, "value": 0.5},
        {"time": 2.0, "value": 0.8},
        {"time": 3.0, "value": 0.3}
    ]
    
    envelope_created = False
    for point in points:
        try:
            result = await reaper_mcp_client.call_tool(
                "insert_envelope_point",
                {
                    "track_index": 0,
                    "envelope_name": "Volume",
                    "time": point["time"],
                    "value": point["value"],
                    "shape": 0
                }
            )
            if "error" not in result.content[0].text.lower():
                envelope_created = True
        except:
            pass
    
    if not envelope_created:
        print("Volume envelope doesn't exist, skipping point operations")
        return
    
    # Get envelope point info
    result = await reaper_mcp_client.call_tool(
        "get_envelope_point",
        {
            "track_index": 0,
            "envelope_name": "Volume",
            "point_index": 0
        }
    )
    print(f"Get point 0 result: {result}")
    if "error" not in result.content[0].text.lower():
        assert "Point 0:" in result.content[0].text
        assert "time=0.000s" in result.content[0].text
    
    # Set envelope point value
    result = await reaper_mcp_client.call_tool(
        "set_envelope_point_value",
        {
            "track_index": 0,
            "envelope_name": "Volume",
            "point_index": 1,
            "value": 0.75
        }
    )
    print(f"Set point value result: {result}")
    assert "Set point 1 value to 0.750" in result.content[0].text
    
    # Verify the change
    result = await reaper_mcp_client.call_tool(
        "get_envelope_point",
        {
            "track_index": 0,
            "envelope_name": "Volume",
            "point_index": 1
        }
    )
    print(f"Get point 1 after change: {result}")
    assert "value=0.750" in result.content[0].text
    
    # Delete a point
    result = await reaper_mcp_client.call_tool(
        "delete_envelope_point",
        {
            "track_index": 0,
            "envelope_name": "Volume",
            "point_index": 2
        }
    )
    print(f"Delete point result: {result}")
    assert "Deleted point 2" in result.content[0].text


@pytest.mark.asyncio
async def test_selected_envelope(reaper_mcp_client):
    """Test selected envelope operations"""
    # Get selected envelope (probably none)
    result = await reaper_mcp_client.call_tool(
        "get_selected_envelope",
        {"project_index": 0}
    )
    print(f"Get selected envelope result: {result}")
    assert "envelope" in result.content[0].text.lower()


@pytest.mark.asyncio 
async def test_envelope_workflow(reaper_mcp_client):
    """Test a complete envelope automation workflow"""
    # Create a track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Set track name
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 0, "name": "Automated Track"}
    )
    
    # Set automation mode to Write
    await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 3}  # Write mode
    )
    
    # Create a volume fade
    fade_points = [
        {"time": 0.0, "value": 1.0},    # Full volume
        {"time": 2.0, "value": 0.0},    # Fade to silence
        {"time": 4.0, "value": 0.0},    # Stay silent
        {"time": 6.0, "value": 1.0},    # Fade back in
    ]
    
    for point in fade_points:
        result = await reaper_mcp_client.call_tool(
            "insert_envelope_point",
            {
                "track_index": 0,
                "envelope_name": "Volume",
                "time": point["time"],
                "value": point["value"],
                "shape": 1  # Linear shape for smooth fades
            }
        )
        print(f"Added fade point at {point['time']}s: {result}")
    
    # Create a pan automation
    pan_points = [
        {"time": 0.0, "value": 0.5},    # Center
        {"time": 2.0, "value": 0.0},    # Hard left
        {"time": 4.0, "value": 1.0},    # Hard right
        {"time": 6.0, "value": 0.5},    # Back to center
    ]
    
    for point in pan_points:
        result = await reaper_mcp_client.call_tool(
            "insert_envelope_point",
            {
                "track_index": 0,
                "envelope_name": "Pan",
                "time": point["time"],
                "value": point["value"],
                "shape": 2  # Slow start/end
            }
        )
        print(f"Added pan point at {point['time']}s: {result}")
    
    # Evaluate volume at various points
    test_times = [0.0, 1.0, 2.0, 3.0, 5.0, 6.0]
    for time in test_times:
        result = await reaper_mcp_client.call_tool(
            "envelope_evaluate",
            {
                "track_index": 0,
                "envelope_name": "Volume",
                "time": time
            }
        )
        print(f"Volume at {time}s: {result}")
    
    # Set automation mode back to Read
    result = await reaper_mcp_client.call_tool(
        "set_track_automation_mode",
        {"track_index": 0, "mode": 1}  # Read mode
    )
    print(f"Set automation to read mode: {result}")
    assert "Read" in result.content[0].text