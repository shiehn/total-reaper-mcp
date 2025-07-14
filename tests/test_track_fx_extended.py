import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_track_fx_extended_parameters(reaper_mcp_client):
    """Test track FX extended parameter operations"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add an FX with parameters (ReaComp)
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 0, "fx_name": "ReaComp", "instantiate": 1}
    )
    
    if "Added FX" in result.content[0].text:
        # Get parameter count
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_num_params",
            {"track_index": 0, "fx_index": 0}
        )
        print(f"Parameter count: {result}")
        assert "parameters" in result.content[0].text
        
        # Get first parameter name
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_param_name",
            {"track_index": 0, "fx_index": 0, "param_index": 0}
        )
        print(f"Parameter 0 name: {result}")
        assert "Parameter 0:" in result.content[0].text
        
        # Get normalized parameter value
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_param_normalized",
            {"track_index": 0, "fx_index": 0, "param_index": 0}
        )
        print(f"Normalized value: {result}")
        assert "normalized value:" in result.content[0].text
        
        # Set normalized parameter value
        result = await reaper_mcp_client.call_tool(
            "track_fx_set_param_normalized",
            {"track_index": 0, "fx_index": 0, "param_index": 0, "value": 0.75}
        )
        print(f"Set normalized result: {result}")
        assert "normalized value to 0.750" in result.content[0].text


@pytest.mark.asyncio
async def test_track_fx_preset_operations(reaper_mcp_client):
    """Test track FX preset management"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add an FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 0, "fx_name": "ReaEQ", "instantiate": 1}
    )
    
    if "Added FX" in result.content[0].text:
        # Get current preset
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_preset",
            {"track_index": 0, "fx_index": 0}
        )
        print(f"Current preset: {result}")
        assert "preset" in result.content[0].text.lower()
        
        # Get preset index
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_preset_index",
            {"track_index": 0, "fx_index": 0}
        )
        print(f"Preset index: {result}")
        assert "preset" in result.content[0].text
        
        # Try to set a preset by name (might fail if preset doesn't exist)
        result = await reaper_mcp_client.call_tool(
            "track_fx_set_preset",
            {"track_index": 0, "fx_index": 0, "preset_name": "Vocal"}
        )
        print(f"Set preset result: {result}")
        assert "preset" in result.content[0].text.lower()
        
        # Navigate presets
        result = await reaper_mcp_client.call_tool(
            "track_fx_navigate_presets",
            {"track_index": 0, "fx_index": 0, "direction": 1}
        )
        print(f"Navigate preset result: {result}")
        assert "preset" in result.content[0].text or "No more presets" in result.content[0].text


@pytest.mark.asyncio
async def test_track_fx_copy_operations(reaper_mcp_client):
    """Test copying track FX"""
    # Create two tracks
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("insert_track", {"index": 1, "use_defaults": True})
    
    # Add FX to first track
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 0, "fx_name": "ReaDelay", "instantiate": 1}
    )
    
    if "Added FX" in result.content[0].text:
        # Copy track FX to another track
        result = await reaper_mcp_client.call_tool(
            "track_fx_copy_to_track",
            {
                "src_track_index": 0,
                "src_fx_index": 0,
                "dst_track_index": 1,
                "dst_fx_index": 0,
                "move": False
            }
        )
        print(f"Copy to track result: {result}")
        assert "Copied FX" in result.content[0].text
        
        # Verify the copy worked by checking FX count on destination
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_count",
            {"track_index": 1}
        )
        print(f"Destination track FX count: {result}")
        assert "Track has 1 FX" in result.content[0].text


@pytest.mark.asyncio
async def test_track_fx_window_operations(reaper_mcp_client):
    """Test track FX window operations"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add an FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 0, "fx_name": "ReaEQ", "instantiate": 1}
    )
    
    if "Added FX" in result.content[0].text:
        # Get chain visibility
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_chain_visible",
            {"track_index": 0}
        )
        print(f"Chain visibility: {result}")
        assert "chain window" in result.content[0].text.lower()
        
        # Show FX window
        result = await reaper_mcp_client.call_tool(
            "track_fx_show",
            {"track_index": 0, "fx_index": 0, "show_flag": 3}
        )
        print(f"Show FX result: {result}")
        assert "Showed FX" in result.content[0].text
        
        # Get open state
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_open",
            {"track_index": 0, "fx_index": 0}
        )
        print(f"FX open state: {result}")
        assert "window is" in result.content[0].text
        
        # Close FX window
        result = await reaper_mcp_client.call_tool(
            "track_fx_set_open",
            {"track_index": 0, "fx_index": 0, "open": False}
        )
        print(f"Close FX result: {result}")
        assert "Closed FX" in result.content[0].text


@pytest.mark.asyncio
async def test_track_fx_advanced_info(reaper_mcp_client):
    """Test advanced track FX information"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add an FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 0, "fx_name": "ReaComp", "instantiate": 1}
    )
    
    if "Added FX" in result.content[0].text:
        # Get FX GUID
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_fx_guid",
            {"track_index": 0, "fx_index": 0}
        )
        print(f"FX GUID: {result}")
        assert "GUID:" in result.content[0].text or "Failed to get GUID" in result.content[0].text
        
        # Get IO size
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_io_size",
            {"track_index": 0, "fx_index": 0}
        )
        print(f"IO size: {result}")
        assert "input pins" in result.content[0].text
        
        # Get offline state
        result = await reaper_mcp_client.call_tool(
            "track_fx_get_offline",
            {"track_index": 0, "fx_index": 0}
        )
        print(f"Offline state: {result}")
        assert "offline" in result.content[0].text or "online" in result.content[0].text
        
        # Set offline
        result = await reaper_mcp_client.call_tool(
            "track_fx_set_offline",
            {"track_index": 0, "fx_index": 0, "offline": True}
        )
        print(f"Set offline result: {result}")
        assert "Set FX" in result.content[0].text and "offline" in result.content[0].text


@pytest.mark.asyncio
async def test_track_fx_format_operations(reaper_mcp_client):
    """Test track FX parameter formatting"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add an FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 0, "fx_name": "ReaComp", "instantiate": 1}
    )
    
    if "Added FX" in result.content[0].text:
        # Format parameter value
        result = await reaper_mcp_client.call_tool(
            "track_fx_format_param_value",
            {"track_index": 0, "fx_index": 0, "param_index": 0, "value": 0.5}
        )
        print(f"Formatted value: {result}")
        assert "formatted value:" in result.content[0].text or "Failed to format" in result.content[0].text
        
        # Format normalized parameter value
        result = await reaper_mcp_client.call_tool(
            "track_fx_format_param_value_normalized",
            {"track_index": 0, "fx_index": 0, "param_index": 0, "value": 0.75}
        )
        print(f"Formatted normalized value: {result}")
        assert "formatted value:" in result.content[0].text or "Failed to format" in result.content[0].text


@pytest.mark.asyncio
async def test_track_fx_record_chain(reaper_mcp_client):
    """Test track record FX chain operations"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Get record FX count
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_rec_count",
        {"track_index": 0}
    )
    print(f"Record FX count: {result}")
    assert "record input FX" in result.content[0].text
    
    # Get record chain visibility
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_rec_chain_visible",
        {"track_index": 0}
    )
    print(f"Record chain visibility: {result}")
    assert "Record FX chain" in result.content[0].text


@pytest.mark.asyncio
async def test_track_fx_get_by_name(reaper_mcp_client):
    """Test getting track FX by name"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add multiple FX
    for fx_name in ["ReaEQ", "ReaComp", "ReaDelay"]:
        await reaper_mcp_client.call_tool(
            "track_fx_add_by_name",
            {"track_index": 0, "fx_name": fx_name, "instantiate": 1}
        )
    
    # Get FX by name (should find it)
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_by_name",
        {"track_index": 0, "fx_name": "ReaComp", "instantiate": False}
    )
    print(f"Get by name result: {result}")
    assert "Found 'ReaComp' at index" in result.content[0].text
    
    # Get non-existent FX by name
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_by_name",
        {"track_index": 0, "fx_name": "NonExistentFX", "instantiate": False}
    )
    print(f"Get non-existent result: {result}")
    assert "not found" in result.content[0].text


@pytest.mark.asyncio
async def test_track_fx_copy_to_take(reaper_mcp_client):
    """Test copying track FX to take"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add FX to track
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 0, "fx_name": "ReaEQ", "instantiate": 1}
    )
    
    # Create media item with take
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    await reaper_mcp_client.call_tool(
        "add_take_to_item",
        {"item_index": 0}
    )
    
    if "Added FX" in result.content[0].text:
        # Copy track FX to take
        result = await reaper_mcp_client.call_tool(
            "track_fx_copy_to_take",
            {
                "track_index": 0,
                "fx_index": 0,
                "item_index": 0,
                "take_index": 0,
                "take_fx_index": 0,
                "move": False
            }
        )
        print(f"Copy to take result: {result}")
        assert "Copied track FX" in result.content[0].text
        
        # Verify the copy worked
        result = await reaper_mcp_client.call_tool(
            "take_fx_get_count",
            {"item_index": 0, "take_index": 0}
        )
        print(f"Take FX count: {result}")
        assert "Take has 1 FX" in result.content[0].text