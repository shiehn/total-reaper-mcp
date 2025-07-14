import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_track_info_string_operations(reaper_mcp_client):
    """Test getting and setting track string parameters"""
    # Create a track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 0, "name": "Test Track"})
    
    # Get track GUID
    result = await reaper_mcp_client.call_tool(
        "get_set_media_track_info_string",
        {"track_index": 0, "param_name": "GUID", "value": "", "set_value": False}
    )
    print(f"Track GUID: {result}")
    assert "Track GUID:" in result.content[0].text
    
    # Get track name via info string
    result = await reaper_mcp_client.call_tool(
        "get_set_media_track_info_string",
        {"track_index": 0, "param_name": "P_NAME", "value": "", "set_value": False}
    )
    print(f"Track name: {result}")
    assert "Track P_NAME:" in result.content[0].text
    assert "Test Track" in result.content[0].text
    
    # Set track name via info string
    result = await reaper_mcp_client.call_tool(
        "get_set_media_track_info_string",
        {"track_index": 0, "param_name": "P_NAME", "value": "Updated Track", "set_value": True}
    )
    print(f"Set name: {result}")
    assert "Set track P_NAME to: Updated Track" in result.content[0].text
    
    # Get track icon
    result = await reaper_mcp_client.call_tool(
        "get_set_media_track_info_string",
        {"track_index": 0, "param_name": "P_ICON", "value": "", "set_value": False}
    )
    print(f"Track icon: {result}")
    assert "Track P_ICON:" in result.content[0].text


@pytest.mark.asyncio
async def test_track_envelope_by_name(reaper_mcp_client):
    """Test getting track envelope by name"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Try to get volume envelope by name
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope_by_name",
        {"track_index": 0, "envelope_name": "Volume"}
    )
    print(f"Volume envelope: {result}")
    assert "envelope" in result.content[0].text.lower()
    
    # Try to get pan envelope
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope_by_name",
        {"track_index": 0, "envelope_name": "Pan"}
    )
    print(f"Pan envelope: {result}")
    assert "envelope" in result.content[0].text.lower()
    
    # Try non-existent envelope
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope_by_name",
        {"track_index": 0, "envelope_name": "NonExistent"}
    )
    print(f"Non-existent envelope: {result}")
    assert "No envelope" in result.content[0].text or "envelope" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_track_midi_lyrics(reaper_mcp_client):
    """Test getting track MIDI lyrics"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Get MIDI lyrics (likely none on empty track)
    result = await reaper_mcp_client.call_tool(
        "get_track_midi_lyrics",
        {"track_index": 0}
    )
    print(f"MIDI lyrics: {result}")
    assert "MIDI lyrics" in result.content[0].text or "no MIDI lyrics" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_track_list_operations(reaper_mcp_client):
    """Test track list window operations"""
    # Adjust track list windows
    result = await reaper_mcp_client.call_tool(
        "track_list_adjust_windows",
        {"resize_behavior": 0}  # normal
    )
    print(f"Adjust windows: {result}")
    assert "Adjusted track list windows" in result.content[0].text
    
    # Try different resize behaviors
    result = await reaper_mcp_client.call_tool(
        "track_list_adjust_windows",
        {"resize_behavior": 1}  # no resize
    )
    print(f"Adjust no resize: {result}")
    assert "no resize" in result.content[0].text
    
    # Update external surfaces
    result = await reaper_mcp_client.call_tool(
        "track_list_update_all_external_surfaces",
        {}
    )
    print(f"Update surfaces: {result}")
    assert "Updated all external control surfaces" in result.content[0].text


@pytest.mark.asyncio
async def test_bypass_fx_all_tracks(reaper_mcp_client):
    """Test bypassing FX on all tracks"""
    # Create tracks with FX
    for i in range(3):
        await reaper_mcp_client.call_tool("insert_track", {"index": i, "use_defaults": True})
        await reaper_mcp_client.call_tool("set_track_name", {"track_index": i, "name": f"Track {i+1}"})
        # Add FX
        await reaper_mcp_client.call_tool(
            "track_fx_add_by_name",
            {"track_index": i, "fx_name": "ReaEQ", "instantiate": -1}
        )
    
    # Bypass all FX
    result = await reaper_mcp_client.call_tool(
        "bypass_fx_all_tracks",
        {"bypass": True}
    )
    print(f"Bypass all: {result}")
    assert "Bypassed FX on all tracks" in result.content[0].text
    
    # Un-bypass all FX
    result = await reaper_mcp_client.call_tool(
        "bypass_fx_all_tracks",
        {"bypass": False}
    )
    print(f"Un-bypass all: {result}")
    assert "Un-bypassed FX on all tracks" in result.content[0].text


@pytest.mark.asyncio
async def test_control_surface_track_operations(reaper_mcp_client):
    """Test control surface track operations"""
    # Get number of tracks
    result = await reaper_mcp_client.call_tool(
        "csurf_num_tracks",
        {"include_master": True}
    )
    print(f"Track count: {result}")
    assert "Control surface track count:" in result.content[0].text
    
    # Create some tracks
    for i in range(3):
        await reaper_mcp_client.call_tool("insert_track", {"index": i, "use_defaults": True})
    
    # Get count without master
    result = await reaper_mcp_client.call_tool(
        "csurf_num_tracks",
        {"include_master": False}
    )
    print(f"Track count (no master): {result}")
    assert "excluding master" in result.content[0].text
    
    # Get track from ID
    result = await reaper_mcp_client.call_tool(
        "csurf_track_from_id",
        {"track_id": 1, "allow_master": True}
    )
    print(f"Track from ID: {result}")
    assert "Control surface track" in result.content[0].text
    
    # Get ID from track
    result = await reaper_mcp_client.call_tool(
        "csurf_track_to_id",
        {"track_index": 0, "allow_master": True}
    )
    print(f"ID from track: {result}")
    assert "control surface ID:" in result.content[0].text.lower()
    
    # Test with master track
    result = await reaper_mcp_client.call_tool(
        "csurf_track_to_id",
        {"track_index": -1, "allow_master": True}  # -1 for master
    )
    print(f"Master track ID: {result}")
    assert "control surface ID:" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_mixer_scroll_operations(reaper_mcp_client):
    """Test mixer scroll operations"""
    # Create many tracks to enable scrolling
    for i in range(10):
        await reaper_mcp_client.call_tool("insert_track", {"index": i, "use_defaults": True})
        await reaper_mcp_client.call_tool("set_track_name", {"track_index": i, "name": f"Track {i+1}"})
    
    # Get current scroll position
    result = await reaper_mcp_client.call_tool("get_mixer_scroll", {})
    print(f"Initial scroll: {result}")
    assert "Mixer scroll:" in result.content[0].text
    
    # Set scroll to track 5
    result = await reaper_mcp_client.call_tool(
        "set_mixer_scroll",
        {"track_index": 5}
    )
    print(f"Set scroll: {result}")
    assert "Set mixer scroll to track 5" in result.content[0].text
    
    # Verify scroll changed
    result = await reaper_mcp_client.call_tool("get_mixer_scroll", {})
    print(f"New scroll: {result}")
    assert "Mixer scroll:" in result.content[0].text
    
    # Set scroll to beginning
    result = await reaper_mcp_client.call_tool(
        "set_mixer_scroll",
        {"track_index": 0}
    )
    print(f"Reset scroll: {result}")


@pytest.mark.asyncio
async def test_track_management_workflow(reaper_mcp_client):
    """Test a complete track management workflow"""
    # Create project with various track types
    track_configs = [
        ("Drums", "drums.png"),
        ("Bass", "bass.png"),
        ("Guitar", "guitar.png"),
        ("Vocals", "mic.png"),
        ("Keys", "keys.png"),
    ]
    
    # Create and configure tracks
    for i, (name, icon) in enumerate(track_configs):
        await reaper_mcp_client.call_tool("insert_track", {"index": i, "use_defaults": True})
        
        # Set name
        await reaper_mcp_client.call_tool(
            "get_set_media_track_info_string",
            {"track_index": i, "param_name": "P_NAME", "value": name, "set_value": True}
        )
        
        # Set icon (if supported)
        await reaper_mcp_client.call_tool(
            "get_set_media_track_info_string",
            {"track_index": i, "param_name": "P_ICON", "value": icon, "set_value": True}
        )
        
        # Add some FX
        await reaper_mcp_client.call_tool(
            "track_fx_add_by_name",
            {"track_index": i, "fx_name": "ReaEQ", "instantiate": -1}
        )
    
    # Get control surface info
    result = await reaper_mcp_client.call_tool(
        "csurf_num_tracks",
        {"include_master": True}
    )
    print(f"Total tracks: {result}")
    
    # Test bypassing all FX
    await reaper_mcp_client.call_tool(
        "bypass_fx_all_tracks",
        {"bypass": True}
    )
    print("Bypassed all FX")
    
    # Update external surfaces
    await reaper_mcp_client.call_tool(
        "track_list_update_all_external_surfaces",
        {}
    )
    
    # Check some track info
    for i in range(len(track_configs)):
        result = await reaper_mcp_client.call_tool(
            "csurf_track_to_id",
            {"track_index": i, "allow_master": False}
        )
        print(f"Track {i} control surface ID: {result}")
    
    print("Track management workflow completed!")


@pytest.mark.asyncio
async def test_track_envelope_by_chunk_name(reaper_mcp_client):
    """Test getting track envelope by chunk name"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Try to get envelope by chunk name (from envelope_extended module)
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope_by_chunk_name",
        {"track_index": 0, "chunk_name": "VOLENV"}
    )
    print(f"Volume envelope by chunk: {result}")
    assert "envelope" in result.content[0].text.lower()
    
    # Try pan envelope
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope_by_chunk_name",
        {"track_index": 0, "chunk_name": "PANENV"}
    )
    print(f"Pan envelope by chunk: {result}")
    assert "envelope" in result.content[0].text.lower()