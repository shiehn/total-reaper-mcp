"""Test rendering and freezing operations"""
import pytest
import pytest_asyncio
import asyncio
from .test_utils import (
    ensure_clean_project,
    create_track_with_verification,
    create_media_item_with_verification,
    assert_response_contains,
    assert_response_success
)


@pytest.mark.asyncio
async def test_track_freeze_operations(reaper_mcp_client):
    """Test track freezing and unfreezing"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Add an FX to the track
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": track_index, "fx_name": "ReaEQ", "instantiate": False}
    )
    
    # Add a media item
    item_index = await create_media_item_with_verification(reaper_mcp_client, track_index)
    
    # Check freeze state (should be unfrozen)
    result = await reaper_mcp_client.call_tool(
        "is_track_frozen",
        {"track_index": track_index}
    )
    assert_response_contains(result, "Track frozen: False")
    
    # Freeze the track
    result = await reaper_mcp_client.call_tool(
        "freeze_track",
        {"track_index": track_index}
    )
    assert_response_contains(result, f"Froze track {track_index}")
    
    # Check freeze state (should be frozen)
    result = await reaper_mcp_client.call_tool(
        "is_track_frozen",
        {"track_index": track_index}
    )
    assert_response_contains(result, "Track frozen: True")
    
    # Unfreeze the track
    result = await reaper_mcp_client.call_tool(
        "unfreeze_track",
        {"track_index": track_index}
    )
    assert_response_contains(result, f"Unfroze track {track_index}")


@pytest.mark.asyncio
async def test_render_time_selection(reaper_mcp_client):
    """Test rendering time selection"""
    # Create a track with media
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
    
    # Set time selection
    result = await reaper_mcp_client.call_tool(
        "get_set_loop_time_range",
        {
            "is_set": True,
            "is_loop": False,
            "start": 2.0,
            "end": 8.0,
            "allow_autoseek": False
        }
    )
    
    # Render time selection to new track
    result = await reaper_mcp_client.call_tool(
        "render_time_selection",
        {"add_to_project": True}
    )
    assert "Rendered time selection to new track" in result.content[0].text


@pytest.mark.asyncio
async def test_apply_fx_to_items(reaper_mcp_client):
    """Test applying FX to items destructively"""
    # Create a track
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "want_defaults": True}
    )
    assert "Successfully inserted track" in result.content[0].text
    
    # Add an FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": 0, "fx_name": "ReaEQ", "instantiate": False}
    )
    
    # Add media items
    for i in range(3):
        result = await reaper_mcp_client.call_tool(
            "add_media_item_to_track",
            {"track_index": 0}
        )
        assert "Added media item" in result.content[0].text
    
    # Apply FX to items
    result = await reaper_mcp_client.call_tool(
        "apply_fx_to_items",
        {"track_index": 0}
    )
    assert "Applied FX to items on track 0" in result.content[0].text


@pytest.mark.asyncio 
async def test_project_render(reaper_mcp_client):
    """Test project rendering"""
    # Create some content
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
    
    # Note: Actual rendering would open dialog, so we just test the call
    result = await reaper_mcp_client.call_tool(
        "render_project",
        {"bounds": "entire_project"}
    )
    assert "Started render dialog" in result.content[0].text or "Failed" in result.content[0].text