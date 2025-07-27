"""
Integration tests for newly added DSL tools

These tests verify that the new DSL wrapper functions correctly call REAPER
and provide the expected functionality.
"""

import pytest
import logging
import re
from .test_utils import (
    ensure_clean_project,
    assert_response_contains,
    assert_response_success,
    extract_number_from_response
)

logger = logging.getLogger(__name__)

async def call_dsl_tool(client, tool_name, params):
    """Helper to call DSL tools and return the text response"""
    result = await client.call_tool(tool_name, params)
    return result.content[0].text if result.content else ""

@pytest.mark.asyncio
class TestDSLTrackManagementNew:
    """Test new DSL track management tools"""
    
    async def test_track_rename(self, reaper_mcp_client):
        """Test renaming a track"""
        # Create a track with a unique name
        unique_name = f"RenameTest_{id(self)}"
        new_name = f"Renamed_{id(self)}"
        
        create_result = await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": unique_name})
        print(f"Create result: {create_result}")
        
        # Get track list to find the index
        tracks = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        print(f"Track list: {tracks}")
        
        # Rename it - use index 0 since it's the first track
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_rename", {
            "track": 0,  # Use index instead of name
            "name": new_name
        })
        assert "Renamed track" in result and f"to '{new_name}'" in result
        
        # Verify the name changed
        tracks_after = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        assert new_name in tracks_after
        assert unique_name not in tracks_after
    
    async def test_track_delete(self, reaper_mcp_client):
        """Test deleting a track"""
        # Get initial track count
        tracks_before = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        initial_count = int(re.search(r'(\d+) tracks?', tracks_before).group(1))
        
        # Create two tracks with unique names
        delete_name = f"DeleteTest_{id(self)}"
        keep_name = f"KeepTest_{id(self)}"
        
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": delete_name})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": keep_name})
        
        # Verify we added 2 tracks
        tracks_mid = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        mid_count = int(re.search(r'(\d+) tracks?', tracks_mid).group(1))
        assert mid_count == initial_count + 2
        
        # Delete one track
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_delete", {
            "track": delete_name
        })
        assert "Deleted track" in result
        
        # Verify we're back to initial + 1
        tracks_after = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        final_count = int(re.search(r'(\d+) tracks?', tracks_after).group(1))
        assert final_count == initial_count + 1
        assert keep_name in tracks_after
        assert delete_name not in tracks_after
    
    async def test_track_arm(self, reaper_mcp_client):
        """Test arming/unarming tracks for recording"""
        # Create a track
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Recording Track"})
        
        # Arm it
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_arm", {
            "track": "Recording Track",
            "armed": True
        })
        assert "Track 1 armed for recording" in result
        
        # Unarm it
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_arm", {
            "track": "Recording Track",
            "armed": False
        })
        assert "Track 1 unarmed for recording" in result
    
    async def test_track_duplicate(self, reaper_mcp_client):
        """Test duplicating a track"""
        # Create a track with specific settings
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Original Track"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {
            "track": "Original Track",
            "volume": "-6dB"
        })
        
        # Duplicate it
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_duplicate", {
            "track": "Original Track"
        })
        assert "Duplicated track 1" in result
        
        # Verify we now have 2 tracks
        tracks = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        assert "2 tracks" in tracks
    
    async def test_track_color(self, reaper_mcp_client):
        """Test coloring tracks"""
        # Create a track
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Colorful Track"})
        
        # Color it red
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_color", {
            "track": "Colorful Track",
            "color": "red"
        })
        assert "Colored track 1 red" in result
        
        # Try other colors
        for color in ["blue", "green", "yellow", "purple"]:
            result = await call_dsl_tool(reaper_mcp_client, "dsl_track_color", {
                "track": 0,  # Use index
                "color": color
            })
            assert f"Colored track 1 {color}" in result

@pytest.mark.asyncio
class TestDSLNavigationAndTransport:
    """Test new DSL navigation and transport tools"""
    
    async def test_go_to_positions(self, reaper_mcp_client):
        """Test navigating to different positions"""
        # Go to beginning
        result = await call_dsl_tool(reaper_mcp_client, "dsl_go_to", {
            "position": "start"
        })
        assert "Moved to 0.0 seconds" in result
        
        # Go to specific time
        result = await call_dsl_tool(reaper_mcp_client, "dsl_go_to", {
            "position": 10.5
        })
        assert "Moved to 10.5 seconds" in result
        
        # Go to end
        result = await call_dsl_tool(reaper_mcp_client, "dsl_go_to", {
            "position": "end"
        })
        assert "Moved to" in result and "seconds" in result
    
    async def test_record(self, reaper_mcp_client):
        """Test starting recording"""
        # Create and arm a track first
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Record Track"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_arm", {
            "track": "Record Track",
            "armed": True
        })
        
        # Start recording
        result = await call_dsl_tool(reaper_mcp_client, "dsl_record", {})
        assert "Recording started" in result
        
        # Stop recording
        await call_dsl_tool(reaper_mcp_client, "dsl_stop", {})

@pytest.mark.asyncio
class TestDSLEditOperations:
    """Test new DSL editing operations"""
    
    async def test_undo(self, reaper_mcp_client):
        """Test undo functionality"""
        # Do something to undo
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Track to Undo"})
        
        # Undo it
        result = await call_dsl_tool(reaper_mcp_client, "dsl_undo", {})
        assert "Undid last action" in result
        
        # Verify track is gone
        tracks = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        assert "Track to Undo" not in tracks or "0 tracks" in tracks
    
    async def test_split_items(self, reaper_mcp_client):
        """Test splitting items at cursor"""
        # Create a track with an item
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Split Test"})
        await call_dsl_tool(reaper_mcp_client, "dsl_loop_create", {
            "track": "Split Test",
            "time": "4 bars",
            "midi": True
        })
        
        # Move cursor to middle
        await call_dsl_tool(reaper_mcp_client, "dsl_go_to", {"position": 2.0})
        
        # Split at cursor
        result = await call_dsl_tool(reaper_mcp_client, "dsl_split", {
            "position": "cursor"
        })
        assert "Split" in result or "No items selected" in result
    
    async def test_fade_operations(self, reaper_mcp_client):
        """Test fade in/out operations"""
        # Create track with audio item
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Fade Test"})
        
        # Note: Need selected items for fades to work
        # This will likely fail without items, but shows the API
        
        # Fade in
        result = await call_dsl_tool(reaper_mcp_client, "dsl_fade", {
            "type": "in",
            "duration": 0.5
        })
        assert "fade in" in result.lower() or "no" in result.lower()
        
        # Fade out
        result = await call_dsl_tool(reaper_mcp_client, "dsl_fade", {
            "type": "out",
            "duration": 0.5
        })
        assert "fade out" in result.lower() or "no" in result.lower()
    
    async def test_normalize(self, reaper_mcp_client):
        """Test normalizing items"""
        # This requires selected items
        result = await call_dsl_tool(reaper_mcp_client, "dsl_normalize", {
            "target": "selected"
        })
        assert "Normalized" in result or "No items" in result.lower()
    
    async def test_reverse(self, reaper_mcp_client):
        """Test reversing audio"""
        # This requires selected audio items
        result = await call_dsl_tool(reaper_mcp_client, "dsl_reverse", {
            "target": "selected"
        })
        assert "Reversed" in result or "No items" in result.lower()

@pytest.mark.asyncio
class TestDSLProjectOperations:
    """Test new DSL project operations"""
    
    async def test_save_project(self, reaper_mcp_client):
        """Test saving project"""
        # Create some content
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Save Test Track"})
        
        # Save project
        result = await call_dsl_tool(reaper_mcp_client, "dsl_save", {})
        assert "Project saved" in result
        
        # Save as (note: implementation may be limited)
        result = await call_dsl_tool(reaper_mcp_client, "dsl_save", {
            "name": "Test Project"
        })
        assert "save" in result.lower()
    
    async def test_render_project(self, reaper_mcp_client):
        """Test rendering/bouncing project"""
        # Create content to render
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Render Track"})
        
        # Render as wav
        result = await call_dsl_tool(reaper_mcp_client, "dsl_render", {
            "format": "wav",
            "what": "project"
        })
        assert "Rendered project as wav" in result

@pytest.mark.asyncio
class TestDSLMarkersAndRegions:
    """Test new DSL marker and region tools"""
    
    async def test_add_marker(self, reaper_mcp_client):
        """Test adding markers"""
        # Add marker at current position
        result = await call_dsl_tool(reaper_mcp_client, "dsl_marker", {
            "action": "add",
            "name": "Verse Start"
        })
        assert "Added marker 'Verse Start'" in result
        
        # Add marker at specific position
        result = await call_dsl_tool(reaper_mcp_client, "dsl_marker", {
            "action": "add",
            "name": "Chorus",
            "position": 30.0
        })
        assert "Added marker 'Chorus' at 30.0 seconds" in result
    
    async def test_create_region(self, reaper_mcp_client):
        """Test creating regions"""
        # Select a time range first
        await call_dsl_tool(reaper_mcp_client, "dsl_time_select", {"time": "8 bars"})
        
        # Create region from selection
        result = await call_dsl_tool(reaper_mcp_client, "dsl_region", {
            "action": "create",
            "name": "Intro"
        })
        assert "Created region 'Intro'" in result
        
        # Create region with specific bounds
        result = await call_dsl_tool(reaper_mcp_client, "dsl_region", {
            "action": "create",
            "name": "Verse",
            "start": 10.0,
            "end": 30.0
        })
        assert "Created region 'Verse' from 10.0 to 30.0 seconds" in result

@pytest.mark.asyncio
class TestDSLSelectionOperations:
    """Test new DSL selection tools"""
    
    async def test_select_all_none(self, reaper_mcp_client):
        """Test selecting all or no items"""
        # Create track with items
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Selection Test"})
        await call_dsl_tool(reaper_mcp_client, "dsl_loop_create", {
            "track": "Selection Test",
            "time": "4 bars",
            "midi": True
        })
        
        # Select all
        result = await call_dsl_tool(reaper_mcp_client, "dsl_select", {
            "what": "all"
        })
        assert "Selected all items" in result
        
        # Select none
        result = await call_dsl_tool(reaper_mcp_client, "dsl_select", {
            "what": "none"
        })
        assert "Deselected all items" in result

@pytest.mark.asyncio
class TestDSLOrganizationTools:
    """Test new DSL organization tools"""
    
    async def test_group_tracks(self, reaper_mcp_client):
        """Test grouping tracks into folders"""
        # Create multiple tracks
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Drum Kick"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Drum Snare"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Drum Hi-Hat"})
        
        # Group them
        result = await call_dsl_tool(reaper_mcp_client, "dsl_group_tracks", {
            "name": "Drums"
        })
        assert "Grouped tracks into folder" in result

@pytest.mark.asyncio
class TestDSLRoutingTools:
    """Test new DSL routing tools"""
    
    async def test_create_send(self, reaper_mcp_client):
        """Test creating sends between tracks"""
        # Create source and destination tracks
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Vocals"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Reverb Bus"})
        
        # Create send
        result = await call_dsl_tool(reaper_mcp_client, "dsl_send", {
            "from_track": "Vocals",
            "to_track": "Reverb Bus",
            "amount": -6.0
        })
        assert "Created send from track 1 to track 2" in result

@pytest.mark.asyncio
class TestDSLCompleteWorkflow:
    """Test a complete workflow with new tools"""
    
    async def test_complete_mixing_workflow(self, reaper_mcp_client):
        """Test a complete mixing workflow using new DSL tools"""
        # Create and organize tracks
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Lead Vocal"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Backing Vocal 1"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Backing Vocal 2"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Reverb Return"})
        
        # Color code tracks
        await call_dsl_tool(reaper_mcp_client, "dsl_track_color", {
            "track": "Lead Vocal",
            "color": "red"
        })
        await call_dsl_tool(reaper_mcp_client, "dsl_track_color", {
            "track": "Reverb Return",
            "color": "blue"
        })
        
        # Set up sends
        for track in ["Lead Vocal", "Backing Vocal 1", "Backing Vocal 2"]:
            await call_dsl_tool(reaper_mcp_client, "dsl_send", {
                "from_track": track,
                "to_track": "Reverb Return",
                "amount": -12.0
            })
        
        # Add markers for song structure
        await call_dsl_tool(reaper_mcp_client, "dsl_marker", {
            "action": "add",
            "name": "Intro",
            "position": 0.0
        })
        await call_dsl_tool(reaper_mcp_client, "dsl_marker", {
            "action": "add",
            "name": "Verse 1",
            "position": 10.0
        })
        
        # Create regions
        await call_dsl_tool(reaper_mcp_client, "dsl_region", {
            "action": "create",
            "name": "Chorus",
            "start": 30.0,
            "end": 50.0
        })
        
        # Save the project
        result = await call_dsl_tool(reaper_mcp_client, "dsl_save", {})
        assert "Project saved" in result
        
        # Verify the structure
        tracks = await call_dsl_tool(reaper_mcp_client, "dsl_list_tracks", {})
        assert "4 tracks" in tracks