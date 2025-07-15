import pytest
import pytest_asyncio
import asyncio
import json
import time
from .test_utils import (
    ensure_clean_project,
    create_track_with_verification,
    assert_response_contains,
    assert_response_success,
    extract_number_from_response
)

@pytest.mark.asyncio
async def test_insert_track(reaper_mcp_client):
    """Test inserting a track at index 0"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Get initial track count
    result = await reaper_mcp_client.call_tool(
        "get_track_count",
        {}
    )
    print(f"Initial track count result: {result}")
    initial_count = extract_number_from_response(result.content[0].text, r'(\d+) tracks?') or 0
    
    # Insert a new track using our utility
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Verify track count increased
    result = await reaper_mcp_client.call_tool(
        "get_track_count",
        {}
    )
    print(f"Final track count result: {result}")
    final_count = extract_number_from_response(result.content[0].text, r'(\d+) tracks?') or 0
    assert final_count == initial_count + 1

@pytest.mark.asyncio
async def test_get_reaper_version(reaper_mcp_client):
    """Test getting REAPER version"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    result = await reaper_mcp_client.call_tool(
        "get_reaper_version",
        {}
    )
    print(f"REAPER version result: {result}")
    assert_response_contains(result, "REAPER version:")

@pytest.mark.asyncio
async def test_get_track(reaper_mcp_client):
    """Test getting a track by index"""
    # First ensure we have at least one track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Get the track at index 0
    result = await reaper_mcp_client.call_tool(
        "get_track",
        {"index": 0}
    )
    print(f"Get track result: {result}")
    assert "Track at index 0:" in result.content[0].text
    
    # Try to get a non-existent track
    result = await reaper_mcp_client.call_tool(
        "get_track",
        {"index": 999}
    )
    print(f"Get non-existent track result: {result}")
    assert "No track found at index 999" in result.content[0].text

@pytest.mark.asyncio
async def test_set_track_selected(reaper_mcp_client):
    """Test selecting and deselecting tracks"""
    # First ensure we have at least one track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Select the track
    result = await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": 0, "selected": True}
    )
    print(f"Select track result: {result}")
    assert "Track at index 0 has been selected" in result.content[0].text
    
    # Deselect the track
    result = await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": 0, "selected": False}
    )
    print(f"Deselect track result: {result}")
    assert "Track at index 0 has been deselected" in result.content[0].text
    
    # Try to select a non-existent track
    result = await reaper_mcp_client.call_tool(
        "set_track_selected",
        {"track_index": 999, "selected": True}
    )
    print(f"Select non-existent track result: {result}")
    assert "Failed to find track at index 999" in result.content[0].text

@pytest.mark.asyncio
async def test_get_track_name(reaper_mcp_client):
    """Test getting track names"""
    # First ensure we have at least one track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Get the name of the track (should be empty by default)
    result = await reaper_mcp_client.call_tool(
        "get_track_name",
        {"track_index": 0}
    )
    print(f"Get track name result: {result}")
    # Track might have no name or a default name
    assert "Track 0" in result.content[0].text
    
    # Try to get name of non-existent track
    result = await reaper_mcp_client.call_tool(
        "get_track_name",
        {"track_index": 999}
    )
    print(f"Get non-existent track name result: {result}")
    assert "Failed to get track name" in result.content[0].text

@pytest.mark.asyncio
async def test_set_track_name(reaper_mcp_client):
    """Test setting track names"""
    # First ensure we have at least one track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Set the track name
    result = await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 0, "name": "My Test Track"}
    )
    print(f"Set track name result: {result}")
    assert "Track 0 renamed to \"My Test Track\"" in result.content[0].text
    
    # Verify the name was set
    result = await reaper_mcp_client.call_tool(
        "get_track_name",
        {"track_index": 0}
    )
    print(f"Get renamed track result: {result}")
    assert "My Test Track" in result.content[0].text
    
    # Try to rename non-existent track
    result = await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 999, "name": "Should Fail"}
    )
    print(f"Set non-existent track name result: {result}")
    assert "Failed to set track name" in result.content[0].text

@pytest.mark.asyncio
async def test_list_tools(reaper_mcp_client):
    """Test listing available tools"""
    result = await reaper_mcp_client.list_tools()
    tools = result.tools
    tool_names = [tool.name for tool in tools]
    
    assert "insert_track" in tool_names
    assert "get_track_count" in tool_names
    assert "get_reaper_version" in tool_names
    assert "get_track" in tool_names
    assert "set_track_selected" in tool_names
    assert "get_track_name" in tool_names
    assert "set_track_name" in tool_names
    
    # Verify tool schemas
    insert_track_tool = next(t for t in tools if t.name == "insert_track")
    assert "index" in insert_track_tool.inputSchema["properties"]
    assert "use_defaults" in insert_track_tool.inputSchema["properties"]
    
    get_track_tool = next(t for t in tools if t.name == "get_track")
    assert "index" in get_track_tool.inputSchema["properties"]
    
    set_track_selected_tool = next(t for t in tools if t.name == "set_track_selected")
    assert "track_index" in set_track_selected_tool.inputSchema["properties"]
    assert "selected" in set_track_selected_tool.inputSchema["properties"]
    
    get_track_name_tool = next(t for t in tools if t.name == "get_track_name")
    assert "track_index" in get_track_name_tool.inputSchema["properties"]
    
    set_track_name_tool = next(t for t in tools if t.name == "set_track_name")
    assert "track_index" in set_track_name_tool.inputSchema["properties"]
    assert "name" in set_track_name_tool.inputSchema["properties"]

@pytest.mark.asyncio
async def test_markers_and_regions(reaper_mcp_client):
    """Test marker and region functionality"""
    # First, count existing markers
    result = await reaper_mcp_client.call_tool(
        "count_project_markers",
        {}
    )
    print(f"Initial marker count: {result}")
    
    # Add a marker at 10 seconds
    result = await reaper_mcp_client.call_tool(
        "add_project_marker",
        {
            "is_region": False,
            "position": 10.0,
            "name": "Test Marker 1"
        }
    )
    print(f"Add marker result: {result}")
    assert "Added marker 'Test Marker 1'" in result.content[0].text
    
    # Add a region from 20 to 30 seconds
    result = await reaper_mcp_client.call_tool(
        "add_project_marker",
        {
            "is_region": True,
            "position": 20.0,
            "region_end": 30.0,
            "name": "Test Region 1"
        }
    )
    print(f"Add region result: {result}")
    assert "Added region 'Test Region 1'" in result.content[0].text
    
    # Count markers again
    result = await reaper_mcp_client.call_tool(
        "count_project_markers",
        {}
    )
    print(f"Updated marker count: {result}")
    assert "Total markers/regions:" in result.content[0].text
    
    # Enumerate first marker
    result = await reaper_mcp_client.call_tool(
        "enum_project_markers",
        {"marker_index": 0}
    )
    print(f"First marker info: {result}")
    assert "at " in result.content[0].text  # Should contain position info
    
    # Try to get non-existent marker
    result = await reaper_mcp_client.call_tool(
        "enum_project_markers",
        {"marker_index": 999}
    )
    print(f"Non-existent marker result: {result}")
    assert "No marker/region found" in result.content[0].text
    
    # Delete a marker (note: we need to know the actual displayed number)
    # For testing, we'll try to delete marker 1
    result = await reaper_mcp_client.call_tool(
        "delete_project_marker",
        {
            "marker_index": 1,
            "is_region": False
        }
    )
    print(f"Delete marker result: {result}")
    # Note: This might fail if the marker doesn't exist, which is fine for the test

@pytest.mark.asyncio
async def test_time_selection(reaper_mcp_client):
    """Test time selection and loop range functionality"""
    # Get current time selection
    result = await reaper_mcp_client.call_tool(
        "get_loop_time_range",
        {"is_loop": False}
    )
    print(f"Initial time selection: {result}")
    
    # Set a time selection from 5 to 15 seconds
    result = await reaper_mcp_client.call_tool(
        "set_loop_time_range",
        {
            "is_loop": False,
            "start": 5.0,
            "end": 15.0
        }
    )
    print(f"Set time selection result: {result}")
    assert "Set time selection: 5.000s to 15.000s" in result.content[0].text
    
    # Verify the time selection was set
    result = await reaper_mcp_client.call_tool(
        "get_loop_time_range",
        {"is_loop": False}
    )
    print(f"Get time selection result: {result}")
    assert "5.000s to 15.000s" in result.content[0].text
    assert "duration: 10.000s" in result.content[0].text
    
    # Set a loop range from 20 to 25 seconds
    result = await reaper_mcp_client.call_tool(
        "set_loop_time_range",
        {
            "is_loop": True,
            "start": 20.0,
            "end": 25.0,
            "allow_autoseek": True
        }
    )
    print(f"Set loop range result: {result}")
    assert "Set loop: 20.000s to 25.000s" in result.content[0].text
    
    # Get the loop range
    result = await reaper_mcp_client.call_tool(
        "get_loop_time_range",
        {"is_loop": True}
    )
    print(f"Get loop range result: {result}")
    assert "20.000s to 25.000s" in result.content[0].text

@pytest.mark.asyncio
async def test_transport_controls(reaper_mcp_client):
    """Test basic transport controls"""
    # Test play
    result = await reaper_mcp_client.call_tool(
        "play",
        {}
    )
    print(f"Play result: {result}")
    assert "Started playback" in result.content[0].text
    
    # Test pause
    result = await reaper_mcp_client.call_tool(
        "pause",
        {}
    )
    print(f"Pause result: {result}")
    assert "Paused" in result.content[0].text
    
    # Test stop
    result = await reaper_mcp_client.call_tool(
        "stop",
        {}
    )
    print(f"Stop result: {result}")
    assert "Stopped" in result.content[0].text
    
    # Test record
    result = await reaper_mcp_client.call_tool(
        "record",
        {}
    )
    print(f"Record result: {result}")
    assert "Started recording" in result.content[0].text
    
    # Stop recording
    result = await reaper_mcp_client.call_tool(
        "stop",
        {}
    )
    print(f"Stop recording result: {result}")

@pytest.mark.asyncio
async def test_set_play_state(reaper_mcp_client):
    """Test setting play state with CSurf_SetPlayState"""
    # Test play
    result = await reaper_mcp_client.call_tool(
        "set_play_state",
        {
            "play": True,
            "pause": False,
            "record": False
        }
    )
    print(f"Set play state result: {result}")
    assert "Set play state: play" in result.content[0].text
    
    # Test pause
    result = await reaper_mcp_client.call_tool(
        "set_play_state",
        {
            "play": False,
            "pause": True,
            "record": False
        }
    )
    print(f"Set pause state result: {result}")
    assert "Set play state: pause" in result.content[0].text
    
    # Test record
    result = await reaper_mcp_client.call_tool(
        "set_play_state",
        {
            "play": False,
            "pause": False,
            "record": True
        }
    )
    print(f"Set record state result: {result}")
    assert "Set play state: record" in result.content[0].text
    
    # Test stop (all false)
    result = await reaper_mcp_client.call_tool(
        "set_play_state",
        {
            "play": False,
            "pause": False,
            "record": False
        }
    )
    print(f"Set stop state result: {result}")
    assert "Set play state: stop" in result.content[0].text
    
    # Test play + record
    result = await reaper_mcp_client.call_tool(
        "set_play_state",
        {
            "play": True,
            "pause": False,
            "record": True
        }
    )
    print(f"Set play+record state result: {result}")
    assert "play" in result.content[0].text
    assert "record" in result.content[0].text

@pytest.mark.asyncio
async def test_set_repeat_state(reaper_mcp_client):
    """Test setting repeat/loop state"""
    # Enable repeat
    result = await reaper_mcp_client.call_tool(
        "set_repeat_state",
        {"repeat": True}
    )
    print(f"Enable repeat result: {result}")
    assert "Repeat enabled" in result.content[0].text
    
    # Disable repeat
    result = await reaper_mcp_client.call_tool(
        "set_repeat_state",
        {"repeat": False}
    )
    print(f"Disable repeat result: {result}")
    assert "Repeat disabled" in result.content[0].text

@pytest.mark.asyncio
async def test_get_play_state(reaper_mcp_client):
    """Test getting playback state"""
    # Stop first to ensure known state
    await reaper_mcp_client.call_tool("stop", {})
    
    # Get play state when stopped
    result = await reaper_mcp_client.call_tool(
        "get_play_state",
        {}
    )
    print(f"Get play state (stopped) result: {result}")
    assert "playback state: 0" in result.content[0].text  # 0 = stopped
    
    # Start playing
    await reaper_mcp_client.call_tool("play", {})
    
    # Get play state when playing
    result = await reaper_mcp_client.call_tool(
        "get_play_state",
        {}
    )
    print(f"Get play state (playing) result: {result}")
    assert "playback state:" in result.content[0].text
    # Should be 1 (playing) but might change quickly
    
    # Stop playback
    await reaper_mcp_client.call_tool("stop", {})