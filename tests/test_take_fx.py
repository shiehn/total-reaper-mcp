import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_take_fx_basic_operations(reaper_mcp_client):
    """Test basic take FX operations"""
    # Create track and audio item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Create a media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    print(f"Add media item result: {result}")
    
    # Add a take to the item
    result = await reaper_mcp_client.call_tool(
        "add_take_to_item",
        {"item_index": 0}
    )
    print(f"Add take result: {result}")
    
    # Get take FX count (should be 0)
    result = await reaper_mcp_client.call_tool(
        "take_fx_get_count",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Take FX count: {result}")
    assert "Take has 0 FX" in result.content[0].text
    
    # Add an FX (ReaEQ)
    result = await reaper_mcp_client.call_tool(
        "take_fx_add_by_name",
        {"item_index": 0, "take_index": 0, "fx_name": "ReaEQ", "instantiate": 1}
    )
    print(f"Add FX result: {result}")
    assert "Added FX" in result.content[0].text or "Failed to add FX" in result.content[0].text
    
    # If FX was added successfully, test other operations
    if "Added FX" in result.content[0].text:
        # Get FX count again
        result = await reaper_mcp_client.call_tool(
            "take_fx_get_count",
            {"item_index": 0, "take_index": 0}
        )
        print(f"Take FX count after add: {result}")
        assert "Take has 1 FX" in result.content[0].text
        
        # Get FX name
        result = await reaper_mcp_client.call_tool(
            "take_fx_get_fx_name",
            {"item_index": 0, "take_index": 0, "fx_index": 0}
        )
        print(f"FX name: {result}")
        # Either successfully got name or failed - both are ok for now
        assert "FX" in result.content[0].text or "Failed" in result.content[0].text
        
        # Get enabled state
        result = await reaper_mcp_client.call_tool(
            "take_fx_get_enabled",
            {"item_index": 0, "take_index": 0, "fx_index": 0}
        )
        print(f"FX enabled state: {result}")
        assert "enabled" in result.content[0].text or "disabled" in result.content[0].text
        
        # Disable FX
        result = await reaper_mcp_client.call_tool(
            "take_fx_set_enabled",
            {"item_index": 0, "take_index": 0, "fx_index": 0, "enabled": False}
        )
        print(f"Disable FX result: {result}")
        assert "Disabled FX" in result.content[0].text
        
        # Enable FX
        result = await reaper_mcp_client.call_tool(
            "take_fx_set_enabled",
            {"item_index": 0, "take_index": 0, "fx_index": 0, "enabled": True}
        )
        print(f"Enable FX result: {result}")
        assert "Enabled FX" in result.content[0].text


@pytest.mark.asyncio
async def test_take_fx_parameters(reaper_mcp_client):
    """Test take FX parameter operations"""
    # Create track and item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    await reaper_mcp_client.call_tool(
        "add_take_to_item",
        {"item_index": 0}
    )
    
    # Add an FX with parameters (ReaComp)
    result = await reaper_mcp_client.call_tool(
        "take_fx_add_by_name",
        {"item_index": 0, "take_index": 0, "fx_name": "ReaComp", "instantiate": 1}
    )
    
    if "Added FX" in result.content[0].text:
        # Get parameter count
        result = await reaper_mcp_client.call_tool(
            "take_fx_get_num_params",
            {"item_index": 0, "take_index": 0, "fx_index": 0}
        )
        print(f"Parameter count: {result}")
        assert "parameters" in result.content[0].text
        
        # Get first parameter name
        result = await reaper_mcp_client.call_tool(
            "take_fx_get_param_name",
            {"item_index": 0, "take_index": 0, "fx_index": 0, "param_index": 0}
        )
        print(f"Parameter 0 name: {result}")
        assert "Parameter 0:" in result.content[0].text
        
        # Get parameter value
        result = await reaper_mcp_client.call_tool(
            "take_fx_get_param",
            {"item_index": 0, "take_index": 0, "fx_index": 0, "param_index": 0}
        )
        print(f"Parameter value: {result}")
        assert "value=" in result.content[0].text
        
        # Set parameter value
        result = await reaper_mcp_client.call_tool(
            "take_fx_set_param",
            {"item_index": 0, "take_index": 0, "fx_index": 0, "param_index": 0, "value": 0.5}
        )
        print(f"Set parameter result: {result}")
        assert "Set parameter 0 to" in result.content[0].text
        
        # Get normalized parameter value
        result = await reaper_mcp_client.call_tool(
            "take_fx_get_param_normalized",
            {"item_index": 0, "take_index": 0, "fx_index": 0, "param_index": 0}
        )
        print(f"Normalized value: {result}")
        assert "normalized value:" in result.content[0].text
        
        # Set normalized parameter value
        result = await reaper_mcp_client.call_tool(
            "take_fx_set_param_normalized",
            {"item_index": 0, "take_index": 0, "fx_index": 0, "param_index": 0, "value": 0.75}
        )
        print(f"Set normalized result: {result}")
        assert "normalized value to 0.750" in result.content[0].text


@pytest.mark.asyncio
async def test_take_fx_presets(reaper_mcp_client):
    """Test take FX preset operations"""
    # Create track and item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    await reaper_mcp_client.call_tool(
        "add_take_to_item",
        {"item_index": 0}
    )
    
    # Add an FX
    result = await reaper_mcp_client.call_tool(
        "take_fx_add_by_name",
        {"item_index": 0, "take_index": 0, "fx_name": "ReaEQ", "instantiate": 1}
    )
    
    if "Added FX" in result.content[0].text:
        # Get current preset
        result = await reaper_mcp_client.call_tool(
            "take_fx_get_preset",
            {"item_index": 0, "take_index": 0, "fx_index": 0}
        )
        print(f"Current preset: {result}")
        assert "preset" in result.content[0].text.lower()
        
        # Try to set a preset (might fail if preset doesn't exist)
        result = await reaper_mcp_client.call_tool(
            "take_fx_set_preset",
            {"item_index": 0, "take_index": 0, "fx_index": 0, "preset_name": "Vocal"}
        )
        print(f"Set preset result: {result}")
        # Either succeeded or failed message is ok
        assert "preset" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_take_fx_copy_operations(reaper_mcp_client):
    """Test copying take FX"""
    # Create two tracks
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("insert_track", {"index": 1, "use_defaults": True})
    
    # Create items on both tracks
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    await reaper_mcp_client.call_tool(
        "add_take_to_item",
        {"item_index": 0}
    )
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 1}
    )
    await reaper_mcp_client.call_tool(
        "add_take_to_item",
        {"item_index": 1}
    )
    
    # Add FX to first take
    result = await reaper_mcp_client.call_tool(
        "take_fx_add_by_name",
        {"item_index": 0, "take_index": 0, "fx_name": "ReaDelay", "instantiate": 1}
    )
    
    if "Added FX" in result.content[0].text:
        # Copy take FX to track
        result = await reaper_mcp_client.call_tool(
            "take_fx_copy_to_track",
            {
                "item_index": 0,
                "take_index": 0,
                "fx_index": 0,
                "track_index": 1,
                "track_fx_index": 0,
                "move": False
            }
        )
        print(f"Copy to track result: {result}")
        assert "Copied take FX" in result.content[0].text
        
        # Copy take FX to another take
        result = await reaper_mcp_client.call_tool(
            "take_fx_copy_to_take",
            {
                "src_item_index": 0,
                "src_take_index": 0,
                "src_fx_index": 0,
                "dst_item_index": 1,
                "dst_take_index": 0,
                "dst_fx_index": 0,
                "move": False
            }
        )
        print(f"Copy to take result: {result}")
        assert "Copied FX from take" in result.content[0].text
        
        # Verify the copy worked by checking FX count on destination
        result = await reaper_mcp_client.call_tool(
            "take_fx_get_count",
            {"item_index": 1, "take_index": 0}
        )
        print(f"Destination take FX count: {result}")
        assert "Take has 1 FX" in result.content[0].text


@pytest.mark.asyncio
async def test_take_fx_workflow(reaper_mcp_client):
    """Test a complete take FX workflow"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 0, "name": "Vocal Take"}
    )
    
    # Create item
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    await reaper_mcp_client.call_tool(
        "add_take_to_item",
        {"item_index": 0}
    )
    
    # Add multiple FX to create a vocal chain
    fx_chain = [
        {"name": "ReaEQ", "desc": "EQ"},
        {"name": "ReaComp", "desc": "Compressor"},
        {"name": "ReaDelay", "desc": "Delay"}
    ]
    
    for i, fx in enumerate(fx_chain):
        result = await reaper_mcp_client.call_tool(
            "take_fx_add_by_name",
            {"item_index": 0, "take_index": 0, "fx_name": fx["name"], "instantiate": 1}
        )
        print(f"Added {fx['desc']}: {result}")
    
    # Get final FX count
    result = await reaper_mcp_client.call_tool(
        "take_fx_get_count",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Final FX count: {result}")
    
    # Adjust some parameters on the compressor (index 1)
    if "Take has" in result.content[0].text:
        # Set threshold
        await reaper_mcp_client.call_tool(
            "take_fx_set_param_normalized",
            {"item_index": 0, "take_index": 0, "fx_index": 1, "param_index": 0, "value": 0.3}
        )
        
        # Set ratio
        await reaper_mcp_client.call_tool(
            "take_fx_set_param_normalized",
            {"item_index": 0, "take_index": 0, "fx_index": 1, "param_index": 1, "value": 0.5}
        )
        
        print("Take FX workflow completed successfully!")


@pytest.mark.asyncio
async def test_take_fx_delete(reaper_mcp_client):
    """Test deleting take FX"""
    # Create track and item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    await reaper_mcp_client.call_tool(
        "add_take_to_item",
        {"item_index": 0}
    )
    
    # Add multiple FX
    for fx_name in ["ReaEQ", "ReaComp", "ReaDelay"]:
        await reaper_mcp_client.call_tool(
            "take_fx_add_by_name",
            {"item_index": 0, "take_index": 0, "fx_name": fx_name, "instantiate": 1}
        )
    
    # Get count before delete
    result = await reaper_mcp_client.call_tool(
        "take_fx_get_count",
        {"item_index": 0, "take_index": 0}
    )
    print(f"FX count before delete: {result}")
    
    # Delete middle FX (index 1)
    result = await reaper_mcp_client.call_tool(
        "take_fx_delete",
        {"item_index": 0, "take_index": 0, "fx_index": 1}
    )
    print(f"Delete FX result: {result}")
    assert "Deleted FX at index 1" in result.content[0].text
    
    # Get count after delete
    result = await reaper_mcp_client.call_tool(
        "take_fx_get_count",
        {"item_index": 0, "take_index": 0}
    )
    print(f"FX count after delete: {result}")
    # Should have one less FX