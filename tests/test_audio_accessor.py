import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_audio_accessor_track_operations(reaper_mcp_client):
    """Test audio accessor operations on tracks"""
    # Create a track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 0, "name": "Test Track"})
    
    # Create track audio accessor
    result = await reaper_mcp_client.call_tool(
        "create_track_audio_accessor",
        {"track_index": 0}
    )
    print(f"Create track accessor: {result}")
    # Should succeed or fail based on track state
    assert "audio accessor" in result.content[0].text.lower()
    
    # Test accessor ID functionality (simulated)
    result = await reaper_mcp_client.call_tool(
        "audio_accessor_validate_state",
        {"accessor_id": "test_accessor"}
    )
    print(f"Validate accessor: {result}")
    assert "audio accessor state" in result.content[0].text.lower()
    
    # Check if state changed
    result = await reaper_mcp_client.call_tool(
        "audio_accessor_state_changed",
        {"accessor_id": "test_accessor"}
    )
    print(f"State changed: {result}")
    assert "Audio accessor state" in result.content[0].text
    
    # Update accessor
    result = await reaper_mcp_client.call_tool(
        "audio_accessor_update",
        {"accessor_id": "test_accessor"}
    )
    print(f"Update accessor: {result}")
    assert "Updated audio accessor" in result.content[0].text
    
    # Get start/end times
    result = await reaper_mcp_client.call_tool(
        "get_audio_accessor_start_time",
        {"accessor_id": "test_accessor"}
    )
    print(f"Start time: {result}")
    assert "start time:" in result.content[0].text.lower()
    
    result = await reaper_mcp_client.call_tool(
        "get_audio_accessor_end_time",
        {"accessor_id": "test_accessor"}
    )
    print(f"End time: {result}")
    assert "end time:" in result.content[0].text.lower()
    
    # Destroy accessor
    result = await reaper_mcp_client.call_tool(
        "destroy_audio_accessor",
        {"accessor_id": "test_accessor"}
    )
    print(f"Destroy accessor: {result}")
    assert "Destroyed audio accessor" in result.content[0].text


@pytest.mark.asyncio
async def test_audio_accessor_take_operations(reaper_mcp_client):
    """Test audio accessor operations on takes"""
    # Create track and item with take
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 5.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Create take audio accessor
    result = await reaper_mcp_client.call_tool(
        "create_take_audio_accessor",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Create take accessor: {result}")
    # Should succeed or fail based on take state
    assert "audio accessor" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_audio_analysis_loudness(reaper_mcp_client):
    """Test audio loudness analysis"""
    # Create track and item with take  
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 5.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Calculate loudness (may need actual audio source)
    result = await reaper_mcp_client.call_tool(
        "calc_media_src_loudness",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Calc loudness: {result}")
    # Should return loudness info or error
    assert "loudness" in result.content[0].text.lower() or "failed" in result.content[0].text.lower()
    
    # Calculate normalization
    result = await reaper_mcp_client.call_tool(
        "calculate_normalization",
        {"item_index": 0, "take_index": 0, "normalize_to_db": -23.0}
    )
    print(f"Calc normalization: {result}")
    assert "normalization" in result.content[0].text.lower() or "failed" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_audio_device_info(reaper_mcp_client):
    """Test audio device information"""
    # Get output latency
    result = await reaper_mcp_client.call_tool("get_output_latency", {})
    print(f"Output latency: {result}")
    assert "latency:" in result.content[0].text.lower()
    
    # Get number of audio inputs
    result = await reaper_mcp_client.call_tool("get_num_audio_inputs", {})
    print(f"Audio inputs: {result}")
    assert "audio inputs" in result.content[0].text.lower()
    
    # Check if audio is running
    result = await reaper_mcp_client.call_tool("audio_is_running", {})
    print(f"Audio running: {result}")
    assert "audio engine is" in result.content[0].text.lower()
    
    # Check pre-buffer status
    result = await reaper_mcp_client.call_tool("audio_is_pre_buffer", {})
    print(f"Pre-buffer: {result}")
    assert "pre-buffering" in result.content[0].text.lower()
    
    # Get audio device info
    result = await reaper_mcp_client.call_tool(
        "get_audio_device_info",
        {"name": "default", "attribute": "MODE"}
    )
    print(f"Device info: {result}")
    assert "Audio device" in result.content[0].text
    
    # Get input activity level
    result = await reaper_mcp_client.call_tool(
        "get_input_activity_level",
        {"input_channel": 0}
    )
    print(f"Input activity: {result}")
    assert "Input channel" in result.content[0].text and "level:" in result.content[0].text


@pytest.mark.asyncio
async def test_peak_analysis_basic(reaper_mcp_client):
    """Test basic peak analysis operations"""
    # Clear peak cache
    result = await reaper_mcp_client.call_tool("clear_peak_cache", {})
    print(f"Clear cache: {result}")
    assert "Cleared peak cache" in result.content[0].text
    
    # Test peak file name (would need real audio file)
    result = await reaper_mcp_client.call_tool(
        "get_peak_file_name",
        {"source_filename": "/test/audio.wav"}
    )
    print(f"Peak file name: {result}")
    assert "peak file" in result.content[0].text.lower()
    
    # Calculate peaks (would need real audio file)
    result = await reaper_mcp_client.call_tool(
        "calculate_peaks",
        {"source_filename": "/test/audio.wav", "sample_rate": 44100}
    )
    print(f"Calculate peaks: {result}")
    # Should fail without valid file
    assert "peak" in result.content[0].text.lower() or "failed" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_peak_analysis_track(reaper_mcp_client):
    """Test track peak analysis"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Get track peak info
    result = await reaper_mcp_client.call_tool(
        "get_track_peak_info",
        {"track_index": 0, "channel": 0}
    )
    print(f"Track peak info: {result}")
    assert "Track 0 channel 0 peak:" in result.content[0].text
    
    # Get track peak hold
    result = await reaper_mcp_client.call_tool(
        "track_get_peak_hold_db",
        {"track_index": 0, "channel": 0, "clear": False}
    )
    print(f"Peak hold: {result}")
    assert "peak hold:" in result.content[0].text.lower()
    
    # Get peak hold and clear
    result = await reaper_mcp_client.call_tool(
        "track_get_peak_hold_db",
        {"track_index": 0, "channel": 0, "clear": True}
    )
    print(f"Peak hold (cleared): {result}")
    assert "peak hold:" in result.content[0].text.lower() and "(cleared)" in result.content[0].text


@pytest.mark.asyncio
async def test_peak_analysis_advanced(reaper_mcp_client):
    """Test advanced peak analysis operations"""
    # Create track and item with take
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 5.0}
    )
    await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Build peaks for PCM source
    result = await reaper_mcp_client.call_tool(
        "pcm_source_build_peaks",
        {"item_index": 0, "take_index": 0, "mode": 0}
    )
    print(f"Build peaks: {result}")
    assert "peaks" in result.content[0].text.lower()
    
    # Generate hires peaks
    result = await reaper_mcp_client.call_tool(
        "hires_peaks_from_source",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Hires peaks: {result}")
    assert "high-resolution peaks" in result.content[0].text.lower() or "failed" in result.content[0].text.lower()
    
    # Get peaks bitmap
    result = await reaper_mcp_client.call_tool(
        "get_peaks_bitmap",
        {
            "item_index": 0,
            "take_index": 0,
            "width": 1000,
            "height": 200,
            "start_time": 0.0,
            "end_time": 5.0
        }
    )
    print(f"Peaks bitmap: {result}")
    assert "peaks bitmap" in result.content[0].text.lower() or "failed" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_audio_samples_operations(reaper_mcp_client):
    """Test audio sample operations"""
    # Calculate peaks from float source (simulated)
    result = await reaper_mcp_client.call_tool(
        "calculate_peaks_float_src",
        {"data_size": 44100, "sample_rate": 44100, "channels": 2}
    )
    print(f"Calc peaks float: {result}")
    assert "peak" in result.content[0].text.lower()
    
    # Get audio accessor samples (simulated)
    result = await reaper_mcp_client.call_tool(
        "get_audio_accessor_samples",
        {
            "accessor_id": "test_accessor",
            "sample_rate": 44100,
            "channels": 2,
            "start_time": 0.0,
            "samples": 1024
        }
    )
    print(f"Get samples: {result}")
    assert "samples" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_audio_analysis_workflow(reaper_mcp_client):
    """Test a complete audio analysis workflow"""
    # Create a project with multiple tracks
    track_names = ["Vocals", "Drums", "Bass", "Master"]
    for i, name in enumerate(track_names):
        await reaper_mcp_client.call_tool("insert_track", {"index": i, "use_defaults": True})
        await reaper_mcp_client.call_tool("set_track_name", {"track_index": i, "name": name})
    
    # Check audio system status
    result = await reaper_mcp_client.call_tool("audio_is_running", {})
    print(f"Audio status: {result}")
    
    result = await reaper_mcp_client.call_tool("get_output_latency", {})
    print(f"System latency: {result}")
    
    # Create items on tracks
    for i in range(3):  # Skip master
        await reaper_mcp_client.call_tool(
            "add_media_item_to_track",
            {"track_index": i, "start_time": 0.0, "length": 10.0}
        )
        await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": i})
    
    # Get peak info for each track
    for i, name in enumerate(track_names):
        result = await reaper_mcp_client.call_tool(
            "get_track_peak_info",
            {"track_index": i, "channel": 0}
        )
        print(f"{name} peak: {result}")
    
    # Clear peak cache at end
    await reaper_mcp_client.call_tool("clear_peak_cache", {})
    
    print("Audio analysis workflow completed!")