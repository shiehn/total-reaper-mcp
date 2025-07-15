"""Test cases for bounce and render operations"""

import pytest
import pytest_asyncio
from .test_utils import (
    ensure_clean_project,
    assert_response_contains,
    assert_response_success
)


@pytest.mark.asyncio
async def test_get_render_settings(reaper_mcp_client):
    """Test getting render settings"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    result = await reaper_mcp_client.call_tool(
        "get_render_settings",
        {}
    )
    assert_response_contains(result, "Render settings:")
    assert_response_contains(result, "Sample rate:")
    assert_response_contains(result, "Channels:")
    assert_response_contains(result, "Format:")
    
@pytest.mark.asyncio
async def test_set_render_settings(reaper_mcp_client):
    """Test setting render settings"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Set sample rate
    result = await reaper_mcp_client.call_tool(
        "set_render_settings",
        {"sample_rate": 48000}
    )
    assert_response_success(result)
    assert_response_contains(result, "Sample rate: 48000 Hz")
    
    # Set multiple settings
    result = await reaper_mcp_client.call_tool(
        "set_render_settings",
        {
            "sample_rate": 44100,
            "channels": 2,
            "format": "WAV"
        }
    )
    assert_response_success(result)
    assert_response_contains(result, "Sample rate: 44100 Hz")
    assert_response_contains(result, "Channels: 2")
    assert_response_contains(result, "Format: WAV")
    
    def test_render_project_bounds(self, mock_project):
        """Test render project with different bounds"""
        # Note: These will open render dialogs in REAPER
        # We can't fully test the render process without user interaction
        
        # Test entire project render
        result = call_tool("render_project", {"bounds": "entire_project"})
        assert result["success"]
        assert "entire project" in result["result"]
        
        # Test time selection render
        result = call_tool("render_project", {"bounds": "time_selection"})
        assert result["success"]
        assert "time selection" in result["result"]
        
        # Test selected items render
        result = call_tool("render_project", {"bounds": "selected_items"})
        assert result["success"]
        assert "selected items" in result["result"]
    
    def test_render_project_default(self, mock_project):
        """Test render project with default bounds"""
        result = call_tool("render_project", {})
        assert result["success"]
        assert "entire project" in result["result"]
    
    def test_bounce_tracks(self, mock_project):
        """Test bouncing tracks"""
        # Create and select a track
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        result = call_tool("set_track_selected", {"track_index": 0, "selected": True})
        assert result["success"]
        
        # Bounce the track
        result = call_tool("bounce_tracks", {"add_to_project": True})
        assert result["success"]
        assert "Bounced selected tracks" in result["result"]
        assert "to new track" in result["result"]
    
    def test_bounce_tracks_default(self, mock_project):
        """Test bounce tracks with default settings"""
        # Create and select a track
        result = call_tool("insert_track", {"index": 0})
        assert result["success"]
        
        result = call_tool("set_track_selected", {"track_index": 0, "selected": True})
        assert result["success"]
        
        # Bounce with defaults
        result = call_tool("bounce_tracks", {})
        assert result["success"]
        assert "Bounced selected tracks" in result["result"]
    
    def test_render_settings_options(self, mock_project):
        """Test various render setting options"""
        # Test different sample rates
        for srate in [44100, 48000, 96000]:
            result = call_tool("set_render_settings", {"sample_rate": srate})
            assert result["success"]
            assert f"Sample rate: {srate} Hz" in result["result"]
        
        # Test different channel configurations
        for channels in [1, 2, 6]:
            result = call_tool("set_render_settings", {"channels": channels})
            assert result["success"]
            assert f"Channels: {channels}" in result["result"]
        
        # Test different formats
        for fmt in ["WAV", "MP3", "FLAC"]:
            result = call_tool("set_render_settings", {"format": fmt})
            assert result["success"]
            assert f"Format: {fmt}" in result["result"]
    
    def test_empty_render_settings(self, mock_project):
        """Test setting render settings with no parameters"""
        result = call_tool("set_render_settings", {})
        assert result["success"]
        assert "No render settings specified" in result["result"]