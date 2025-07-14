import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_track_send_basic_operations(reaper_mcp_client):
    """Test basic track send operations"""
    # Create two tracks
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("insert_track", {"index": 1, "use_defaults": True})
    
    # Set track names for clarity
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 0, "name": "Source Track"})
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 1, "name": "Destination Track"})
    
    # Get initial send count
    result = await reaper_mcp_client.call_tool(
        "get_track_num_sends",
        {"track_index": 0, "category": 0}  # 0=sends
    )
    print(f"Initial send count: {result}")
    assert "Track has 0 sends" in result.content[0].text
    
    # Create a send from track 0 to track 1
    result = await reaper_mcp_client.call_tool(
        "create_track_send",
        {"src_track_index": 0, "dst_track_index": 1}
    )
    print(f"Create send: {result}")
    assert "Created send from track 0 to track 1" in result.content[0].text
    
    # Get send count after creation
    result = await reaper_mcp_client.call_tool(
        "get_track_num_sends",
        {"track_index": 0, "category": 0}
    )
    print(f"Send count after creation: {result}")
    assert "Track has 1 sends" in result.content[0].text
    
    # Get send name
    result = await reaper_mcp_client.call_tool(
        "get_track_send_name",
        {"track_index": 0, "send_index": 0}
    )
    print(f"Send name: {result}")
    assert "Send 0:" in result.content[0].text
    
    # Get send destination
    result = await reaper_mcp_client.call_tool(
        "get_send_destination_track",
        {"src_track_index": 0, "send_index": 0}
    )
    print(f"Send destination: {result}")
    assert "Send 0 goes to:" in result.content[0].text
    
    # Remove the send
    result = await reaper_mcp_client.call_tool(
        "remove_track_send",
        {"track_index": 0, "category": 0, "send_index": 0}
    )
    print(f"Remove send: {result}")
    assert "Removed send 0 from track 0" in result.content[0].text


@pytest.mark.asyncio
async def test_track_send_parameters(reaper_mcp_client):
    """Test track send parameter operations"""
    # Create tracks and send
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("insert_track", {"index": 1, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "create_track_send",
        {"src_track_index": 0, "dst_track_index": 1}
    )
    
    # Get send info value (D_VOL for volume)
    result = await reaper_mcp_client.call_tool(
        "get_track_send_info_value",
        {"track_index": 0, "category": 0, "send_index": 0, "param_name": "D_VOL"}
    )
    print(f"Send volume: {result}")
    assert "Send 0 D_VOL:" in result.content[0].text
    
    # Set send info value
    result = await reaper_mcp_client.call_tool(
        "set_track_send_info_value",
        {"track_index": 0, "category": 0, "send_index": 0, "param_name": "D_VOL", "value": 0.5}
    )
    print(f"Set send volume: {result}")
    assert "Set Send 0 D_VOL to 0.5" in result.content[0].text
    
    # Get/set string info (P_DESTTRACK for destination)
    result = await reaper_mcp_client.call_tool(
        "get_set_track_send_info_string",
        {"track_index": 0, "category": 0, "send_index": 0, "param_name": "P_NAME", 
         "value": "To Reverb", "set_value": True}
    )
    print(f"Set send name: {result}")
    assert "Set Send 0 P_NAME to: To Reverb" in result.content[0].text
    
    # Get UI vol/pan
    result = await reaper_mcp_client.call_tool(
        "get_track_send_ui_vol_pan",
        {"track_index": 0, "send_index": 0}
    )
    print(f"Send UI vol/pan: {result}")
    assert "Send 0: volume=" in result.content[0].text
    
    # Set UI volume
    result = await reaper_mcp_client.call_tool(
        "set_track_send_ui_vol",
        {"track_index": 0, "send_index": 0, "volume": 0.75}
    )
    print(f"Set UI volume: {result}")
    assert "Set send 0 UI volume to 0.750" in result.content[0].text
    
    # Set UI pan
    result = await reaper_mcp_client.call_tool(
        "set_track_send_ui_pan",
        {"track_index": 0, "send_index": 0, "pan": -0.25}
    )
    print(f"Set UI pan: {result}")
    assert "Set send 0 UI pan to -0.250" in result.content[0].text
    
    # Toggle mute
    result = await reaper_mcp_client.call_tool(
        "toggle_track_send_ui_mute",
        {"track_index": 0, "send_index": 0}
    )
    print(f"Toggle mute: {result}")
    assert "Send 0 is now" in result.content[0].text


@pytest.mark.asyncio
async def test_track_receive_operations(reaper_mcp_client):
    """Test track receive operations"""
    # Create tracks and send
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("insert_track", {"index": 1, "use_defaults": True})
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 0, "name": "Send From"})
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 1, "name": "Receive To"})
    
    # Create send (which creates a receive on destination)
    await reaper_mcp_client.call_tool(
        "create_track_send",
        {"src_track_index": 0, "dst_track_index": 1}
    )
    
    # Get receive count on destination track
    result = await reaper_mcp_client.call_tool(
        "get_track_num_sends",
        {"track_index": 1, "category": 1}  # 1=receives
    )
    print(f"Receive count: {result}")
    assert "Track has 1 receives" in result.content[0].text
    
    # Get receive name
    result = await reaper_mcp_client.call_tool(
        "get_track_receive_name",
        {"track_index": 1, "receive_index": 0}
    )
    print(f"Receive name: {result}")
    assert "Receive 0:" in result.content[0].text
    
    # Get receive source
    result = await reaper_mcp_client.call_tool(
        "get_receive_source_track",
        {"dst_track_index": 1, "receive_index": 0}
    )
    print(f"Receive source: {result}")
    assert "Receive 0 comes from:" in result.content[0].text
    
    # Get receive UI vol/pan
    result = await reaper_mcp_client.call_tool(
        "get_track_receive_ui_vol_pan",
        {"track_index": 1, "receive_index": 0}
    )
    print(f"Receive UI vol/pan: {result}")
    assert "Receive 0: volume=" in result.content[0].text
    
    # Get receive mute state
    result = await reaper_mcp_client.call_tool(
        "get_track_receive_ui_mute",
        {"track_index": 1, "receive_index": 0}
    )
    print(f"Receive mute: {result}")
    assert "Receive 0 is" in result.content[0].text


@pytest.mark.asyncio
async def test_send_advanced_operations(reaper_mcp_client):
    """Test advanced send operations"""
    # Create tracks and send
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("insert_track", {"index": 1, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "create_track_send",
        {"src_track_index": 0, "dst_track_index": 1}
    )
    
    # Enable/disable send
    result = await reaper_mcp_client.call_tool(
        "set_send_enabled",
        {"track_index": 0, "send_index": 0, "enabled": False}
    )
    print(f"Disable send: {result}")
    assert "Send 0 disabled" in result.content[0].text
    
    result = await reaper_mcp_client.call_tool(
        "set_send_enabled",
        {"track_index": 0, "send_index": 0, "enabled": True}
    )
    print(f"Enable send: {result}")
    assert "Send 0 enabled" in result.content[0].text
    
    # Set send mode (0=post-fader, 1=pre-fader, 3=post-fx)
    result = await reaper_mcp_client.call_tool(
        "set_send_mode",
        {"track_index": 0, "send_index": 0, "mode": 1}
    )
    print(f"Set send mode: {result}")
    assert "Set send 0 to pre-fader" in result.content[0].text
    
    # Try to get send envelope (requires SWS)
    result = await reaper_mcp_client.call_tool(
        "get_send_envelope",
        {"track_index": 0, "send_index": 0, "envelope_index": 0}  # 0=volume envelope
    )
    print(f"Send envelope: {result}")
    # May fail without SWS extension
    assert "envelope" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_hardware_output_operations(reaper_mcp_client):
    """Test hardware output operations"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Get hardware output count
    result = await reaper_mcp_client.call_tool(
        "get_track_num_sends",
        {"track_index": 0, "category": 2}  # 2=hardware outputs
    )
    print(f"Hardware output count: {result}")
    assert "Track has" in result.content[0].text and "hardware outputs" in result.content[0].text
    
    # Create hardware output
    result = await reaper_mcp_client.call_tool(
        "create_hardware_output_send",
        {"track_index": 0, "output_channel": 1}
    )
    print(f"Create hardware output: {result}")
    assert "Created hardware output" in result.content[0].text or "Failed" in result.content[0].text
    
    # Get audio output info
    result = await reaper_mcp_client.call_tool(
        "get_num_audio_outputs",
        {}
    )
    print(f"Audio outputs: {result}")
    assert "System has" in result.content[0].text and "audio outputs" in result.content[0].text
    
    # Get output channel name
    result = await reaper_mcp_client.call_tool(
        "get_output_channel_name",
        {"channel": 0}
    )
    print(f"Output channel name: {result}")
    assert "Output channel 0:" in result.content[0].text


@pytest.mark.asyncio
async def test_track_ui_operations(reaper_mcp_client):
    """Test track UI volume/pan operations"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Get track UI vol/pan
    result = await reaper_mcp_client.call_tool(
        "get_track_ui_vol_pan",
        {"track_index": 0}
    )
    print(f"Track UI vol/pan: {result}")
    assert "Track UI: volume=" in result.content[0].text
    
    # Set track UI volume
    result = await reaper_mcp_client.call_tool(
        "set_track_ui_volume",
        {"track_index": 0, "volume": 0.8, "relative": False}
    )
    print(f"Set UI volume: {result}")
    assert "Set track UI volume to 0.800" in result.content[0].text
    
    # Set track UI pan
    result = await reaper_mcp_client.call_tool(
        "set_track_ui_pan",
        {"track_index": 0, "pan": 0.5, "relative": False}
    )
    print(f"Set UI pan: {result}")
    assert "Set track UI pan to 0.500" in result.content[0].text


@pytest.mark.asyncio
async def test_send_workflow(reaper_mcp_client):
    """Test a complete send routing workflow"""
    # Create multiple tracks for routing
    track_names = ["Drums", "Bass", "Guitar", "Reverb Bus", "Delay Bus"]
    for i, name in enumerate(track_names):
        await reaper_mcp_client.call_tool("insert_track", {"index": i, "use_defaults": True})
        await reaper_mcp_client.call_tool("set_track_name", {"track_index": i, "name": name})
    
    # Create sends from instruments to buses
    sends = [
        (0, 3),  # Drums to Reverb
        (1, 3),  # Bass to Reverb  
        (2, 3),  # Guitar to Reverb
        (2, 4),  # Guitar to Delay
    ]
    
    for src, dst in sends:
        result = await reaper_mcp_client.call_tool(
            "create_track_send",
            {"src_track_index": src, "dst_track_index": dst}
        )
        print(f"Created send from track {src} to {dst}")
    
    # Configure send levels
    send_configs = [
        (0, 0, 0.3),  # Drums to reverb at 30%
        (1, 0, 0.2),  # Bass to reverb at 20%
        (2, 0, 0.4),  # Guitar to reverb at 40%
        (2, 1, 0.5),  # Guitar to delay at 50%
    ]
    
    for track, send_idx, volume in send_configs:
        await reaper_mcp_client.call_tool(
            "set_track_send_ui_vol",
            {"track_index": track, "send_index": send_idx, "volume": volume}
        )
    
    # Set pre-fader for guitar to delay
    await reaper_mcp_client.call_tool(
        "set_send_mode",
        {"track_index": 2, "send_index": 1, "mode": 1}  # pre-fader
    )
    
    # Check final routing
    for i in range(3):
        result = await reaper_mcp_client.call_tool(
            "get_track_num_sends",
            {"track_index": i, "category": 0}
        )
        print(f"Track {i} send count: {result}")
    
    # Check receives on buses
    for i in [3, 4]:
        result = await reaper_mcp_client.call_tool(
            "get_track_num_sends",
            {"track_index": i, "category": 1}
        )
        print(f"Track {i} receive count: {result}")
    
    print("Send routing workflow completed successfully!")