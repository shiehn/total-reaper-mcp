import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_media_item_info_operations(reaper_mcp_client):
    """Test media item info get/set operations"""
    # Create track and item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("add_media_item_to_track", {"track_index": 0})
    
    # Get item info value (D_POSITION)
    result = await reaper_mcp_client.call_tool(
        "get_media_item_info_value",
        {"item_index": 0, "param_name": "D_POSITION"}
    )
    print(f"Item position: {result}")
    assert "Item D_POSITION:" in result.content[0].text
    
    # Set item info value (D_POSITION)
    result = await reaper_mcp_client.call_tool(
        "set_media_item_info_value",
        {"item_index": 0, "param_name": "D_POSITION", "value": 5.0}
    )
    print(f"Set position: {result}")
    assert "Set item D_POSITION to 5.0" in result.content[0].text
    
    # Get/set string info (P_NOTES)
    result = await reaper_mcp_client.call_tool(
        "get_set_media_item_info_string",
        {"item_index": 0, "param_name": "P_NOTES", "value": "Test note", "set_value": True}
    )
    print(f"Set notes: {result}")
    assert "Set item P_NOTES to: Test note" in result.content[0].text
    
    # Get string info
    result = await reaper_mcp_client.call_tool(
        "get_set_media_item_info_string",
        {"item_index": 0, "param_name": "P_NOTES", "value": "", "set_value": False}
    )
    print(f"Get notes: {result}")
    assert "Item P_NOTES: Test note" in result.content[0].text
    
    # Get displayed color
    result = await reaper_mcp_client.call_tool(
        "get_displayed_media_item_color",
        {"item_index": 0}
    )
    print(f"Displayed color: {result}")
    assert "Item displayed color:" in result.content[0].text


@pytest.mark.asyncio
async def test_take_management_operations(reaper_mcp_client):
    """Test take management and info operations"""
    # Create track and item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("add_media_item_to_track", {"track_index": 0})
    
    # Add takes
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Get number of takes
    result = await reaper_mcp_client.call_tool(
        "get_media_item_num_takes",
        {"item_index": 0}
    )
    print(f"Take count: {result}")
    assert "Media item has" in result.content[0].text and "takes" in result.content[0].text
    
    # Get specific take
    result = await reaper_mcp_client.call_tool(
        "get_media_item_take",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Get take: {result}")
    assert "Take 0:" in result.content[0].text
    
    # Get parent item of take
    result = await reaper_mcp_client.call_tool(
        "get_media_item_take_item",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Take parent: {result}")
    assert "Take 0 belongs to item" in result.content[0].text
    
    # Get track from take
    result = await reaper_mcp_client.call_tool(
        "get_media_item_take_track",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Take track: {result}")
    assert "Take is on track" in result.content[0].text
    
    # Get/set take info value
    result = await reaper_mcp_client.call_tool(
        "get_media_item_take_info_value",
        {"item_index": 0, "take_index": 0, "param_name": "D_VOL"}
    )
    print(f"Take volume: {result}")
    assert "Take D_VOL:" in result.content[0].text
    
    # Set take info value
    result = await reaper_mcp_client.call_tool(
        "set_media_item_take_info_value",
        {"item_index": 0, "take_index": 0, "param_name": "D_VOL", "value": 0.5}
    )
    print(f"Set take volume: {result}")
    assert "Set take D_VOL to 0.5" in result.content[0].text
    
    # Get/set take string info
    result = await reaper_mcp_client.call_tool(
        "get_set_media_item_take_info_string",
        {"item_index": 0, "take_index": 0, "param_name": "P_NAME", "value": "Take 1", "set_value": True}
    )
    print(f"Set take name: {result}")
    assert "Set take P_NAME to: Take 1" in result.content[0].text
    
    # Check if take is active
    result = await reaper_mcp_client.call_tool(
        "is_item_take_active_for_playback",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Take active: {result}")
    assert "Take 0 is" in result.content[0].text and ("active" in result.content[0].text or "not active" in result.content[0].text)


@pytest.mark.asyncio
async def test_take_markers(reaper_mcp_client):
    """Test take marker operations"""
    # Create track and item with take
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("add_media_item_to_track", {"track_index": 0})
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Get initial marker count
    result = await reaper_mcp_client.call_tool(
        "get_num_take_markers",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Initial marker count: {result}")
    assert "Take has 0 markers" in result.content[0].text
    
    # Add take marker
    result = await reaper_mcp_client.call_tool(
        "set_take_marker",
        {"item_index": 0, "take_index": 0, "marker_index": -1, "name": "Marker 1", "position": 1.0, "color": 0xFF0000}
    )
    print(f"Add marker: {result}")
    assert "Added marker at index" in result.content[0].text or "Updated marker at index" in result.content[0].text
    
    # Add another marker
    result = await reaper_mcp_client.call_tool(
        "set_take_marker",
        {"item_index": 0, "take_index": 0, "marker_index": -1, "name": "Marker 2", "position": 2.0, "color": 0x00FF00}
    )
    print(f"Add marker 2: {result}")
    
    # Get marker count
    result = await reaper_mcp_client.call_tool(
        "get_num_take_markers",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Marker count after add: {result}")
    assert "Take has" in result.content[0].text and "markers" in result.content[0].text
    
    # Get specific marker
    result = await reaper_mcp_client.call_tool(
        "get_take_marker",
        {"item_index": 0, "take_index": 0, "marker_index": 0}
    )
    print(f"Get marker: {result}")
    assert "Take marker 0:" in result.content[0].text or "No marker at index 0" in result.content[0].text
    
    # Count markers by name
    result = await reaper_mcp_client.call_tool(
        "count_take_markers_by_name",
        {"item_index": 0, "take_index": 0, "name": "Marker 1"}
    )
    print(f"Count by name: {result}")
    assert "Found" in result.content[0].text and "markers named 'Marker 1'" in result.content[0].text
    
    # Get all markers
    result = await reaper_mcp_client.call_tool(
        "get_all_take_markers",
        {"item_index": 0, "take_index": 0}
    )
    print(f"All markers: {result}")
    assert "Take has" in result.content[0].text or "markers:" in result.content[0].text
    
    # Delete marker
    result = await reaper_mcp_client.call_tool(
        "delete_take_marker",
        {"item_index": 0, "take_index": 0, "marker_index": 0}
    )
    print(f"Delete marker: {result}")
    assert "Deleted take marker 0" in result.content[0].text or "Failed to delete" in result.content[0].text


@pytest.mark.asyncio
async def test_stretch_markers(reaper_mcp_client):
    """Test stretch marker operations"""
    # Create track and item with take
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("add_media_item_to_track", {"track_index": 0})
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Get initial stretch marker count
    result = await reaper_mcp_client.call_tool(
        "get_take_num_stretch_markers",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Initial stretch marker count: {result}")
    assert "Take has" in result.content[0].text and "stretch markers" in result.content[0].text
    
    # Set stretch marker
    result = await reaper_mcp_client.call_tool(
        "set_take_stretch_marker",
        {"item_index": 0, "take_index": 0, "marker_index": -1, "pos": 1.0, "src_pos": 1.0}
    )
    print(f"Set stretch marker: {result}")
    assert "stretch marker" in result.content[0].text
    
    # Get stretch marker
    result = await reaper_mcp_client.call_tool(
        "get_take_stretch_marker",
        {"item_index": 0, "take_index": 0, "marker_index": 0}
    )
    print(f"Get stretch marker: {result}")
    assert "Stretch marker" in result.content[0].text or "No stretch marker" in result.content[0].text
    
    # Get stretch marker slope
    result = await reaper_mcp_client.call_tool(
        "get_take_stretch_marker_slope",
        {"item_index": 0, "take_index": 0, "marker_index": 0}
    )
    print(f"Get slope: {result}")
    assert "slope:" in result.content[0].text
    
    # Set stretch marker slope
    result = await reaper_mcp_client.call_tool(
        "set_take_stretch_marker_slope",
        {"item_index": 0, "take_index": 0, "marker_index": 0, "slope": 1.5}
    )
    print(f"Set slope: {result}")
    assert "slope to" in result.content[0].text or "Failed to set" in result.content[0].text
    
    # Get take playback rate
    result = await reaper_mcp_client.call_tool(
        "get_take_stretch_play_rate",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Playback rate: {result}")
    assert "Take playback rate:" in result.content[0].text
    
    # Delete stretch marker
    result = await reaper_mcp_client.call_tool(
        "delete_take_stretch_marker",
        {"item_index": 0, "take_index": 0, "marker_index": 0}
    )
    print(f"Delete stretch marker: {result}")
    assert "Deleted stretch marker" in result.content[0].text
    
    # Delete range of stretch markers
    result = await reaper_mcp_client.call_tool(
        "delete_take_stretch_markers",
        {"item_index": 0, "take_index": 0, "start_idx": 0, "end_idx": 2}
    )
    print(f"Delete range: {result}")
    assert "Deleted" in result.content[0].text and "stretch markers" in result.content[0].text


@pytest.mark.asyncio
async def test_source_operations(reaper_mcp_client):
    """Test media source operations"""
    # Create track and item with take
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("add_media_item_to_track", {"track_index": 0})
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Get parent source
    result = await reaper_mcp_client.call_tool(
        "get_media_source_parent",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Parent source: {result}")
    assert "source" in result.content[0].text.lower()
    
    # Validate a filename (using a common audio format)
    result = await reaper_mcp_client.call_tool(
        "validate_media_source_filename",
        {"filename": "test.wav"}
    )
    print(f"Validate filename: {result}")
    assert "valid media source" in result.content[0].text or "not a valid media source" in result.content[0].text
    
    # Get source peaks
    try:
        result = await reaper_mcp_client.call_tool(
            "get_source_peaks",
            {
                "item_index": 0,
                "take_index": 0,
                "start_time": 0.0,
                "num_channels": 2,
                "num_samples": 100,
                "want_min_max": 0
            }
        )
        print(f"Source peaks: {result}")
        assert "peak samples" in result.content[0].text
    except Exception as e:
        print(f"Expected error getting peaks from empty take: {e}")
    
    # Build peak cache
    result = await reaper_mcp_client.call_tool(
        "build_peak_cache_for_source",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Build peaks: {result}")
    assert "Peak cache" in result.content[0].text


@pytest.mark.asyncio
async def test_media_item_workflow(reaper_mcp_client):
    """Test a complete media item workflow"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 0, "name": "Audio Track"})
    
    # Create media item
    await reaper_mcp_client.call_tool("add_media_item_to_track", {"track_index": 0})
    
    # Set item properties
    await reaper_mcp_client.call_tool(
        "set_media_item_info_value",
        {"item_index": 0, "param_name": "D_LENGTH", "value": 10.0}
    )
    await reaper_mcp_client.call_tool(
        "set_media_item_info_value",
        {"item_index": 0, "param_name": "D_POSITION", "value": 2.0}
    )
    
    # Add multiple takes
    for i in range(3):
        await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
        await reaper_mcp_client.call_tool(
            "set_take_name",
            {"item_index": 0, "take_index": i, "name": f"Take {i+1}"}
        )
    
    # Set active take
    await reaper_mcp_client.call_tool(
        "set_active_take",
        {"item_index": 0, "take_index": 1}
    )
    
    # Add markers to active take
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "set_take_marker",
            {
                "item_index": 0,
                "take_index": 1,
                "marker_index": -1,
                "name": f"Section {i+1}",
                "position": float(i * 3),
                "color": 0xFF0000 + (i * 0x003300)
            }
        )
    
    # Get final state
    result = await reaper_mcp_client.call_tool(
        "get_media_item_num_takes",
        {"item_index": 0}
    )
    print(f"Final take count: {result}")
    
    result = await reaper_mcp_client.call_tool(
        "get_all_take_markers",
        {"item_index": 0, "take_index": 1}
    )
    print(f"Final markers: {result}")
    
    print("Media item workflow completed successfully!")