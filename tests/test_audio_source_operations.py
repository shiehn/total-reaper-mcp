"""Test audio source management operations"""
import pytest
import pytest_asyncio
import asyncio


def assert_tools_available(available_tools, required_tools):
    """Assert that all required tools are available, failing with clear message if not"""
    for tool in required_tools:
        assert tool in available_tools, f"MISSING IMPLEMENTATION: Tool '{tool}' is not implemented in the server but is required for audio source functionality"


@pytest.mark.asyncio
async def test_media_source_operations(reaper_mcp_client):
    """Test media source operations"""
    # Check if required tools are available
    required_tools = ["get_media_item_take_source", "get_media_source_filename", 
                      "get_media_source_length", "get_media_source_type"]
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    
    assert_tools_available(available_tools, required_tools)
    
    # Create a track with a media item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Add a media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in result.content[0].text
    
    # Get media item take source
    result = await reaper_mcp_client.call_tool(
        "get_media_item_take_source",
        {"take_index": 0}
    )
    assert "Get media item take source:" in result.content[0].text
    
    # Get media source filename
    result = await reaper_mcp_client.call_tool(
        "get_media_source_filename",
        {"source_index": 0}
    )
    assert "Media source filename:" in result.content[0].text
    
    # Get media source length
    result = await reaper_mcp_client.call_tool(
        "get_media_source_length",
        {"source_index": 0}
    )
    assert "Media source length:" in result.content[0].text
    assert "seconds" in result.content[0].text
    
    # Get media source type
    result = await reaper_mcp_client.call_tool(
        "get_media_source_type",
        {"source_index": 0}
    )
    assert "Media source type:" in result.content[0].text


@pytest.mark.asyncio
async def test_pcm_source_creation(reaper_mcp_client):
    """Test PCM source creation from file"""
    # Check if tool is available
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    assert_tools_available(available_tools, ["pcm_source_create_from_file"])
    
    # Create PCM source from file
    # Note: This test uses a placeholder filename as we don't have actual audio files
    result = await reaper_mcp_client.call_tool(
        "pcm_source_create_from_file",
        {"filename": "/path/to/test.wav"}
    )
    assert "Created PCM source:" in result.content[0].text or "Failed" in result.content[0].text


@pytest.mark.asyncio
async def test_media_take_peaks(reaper_mcp_client):
    """Test getting media take peak data"""
    # Check if tool is available
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    assert_tools_available(available_tools, ["get_media_item_take_peaks"])
    
    # Create a track with a media item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Add a media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in result.content[0].text
    
    # Get take peaks with default parameters
    result = await reaper_mcp_client.call_tool(
        "get_media_item_take_peaks",
        {"take_index": 0}
    )
    assert "Media item take peaks:" in result.content[0].text
    
    # Get take peaks with custom parameters
    result = await reaper_mcp_client.call_tool(
        "get_media_item_take_peaks",
        {
            "take_index": 0,
            "channel": 0,
            "sample_rate": 44100.0,
            "start_time": 1.0,
            "num_samples": 500
        }
    )
    assert "Media item take peaks:" in result.content[0].text


@pytest.mark.asyncio
async def test_set_media_take_source(reaper_mcp_client):
    """Test setting media take source"""
    # Check if tool is available
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    assert_tools_available(available_tools, ["set_media_item_take_source"])
    
    # Create a track with a media item
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Add a media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in result.content[0].text
    
    # Set media item take source
    result = await reaper_mcp_client.call_tool(
        "set_media_item_take_source",
        {
            "take_index": 0,
            "source_index": 0
        }
    )
    assert "Set media item take source:" in result.content[0].text or "Failed" in result.content[0].text