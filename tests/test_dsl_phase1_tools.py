"""
Integration tests for Phase 1 DSL tools (FX, Routing, Automation, Markers)

These tests verify the new compound command handling tools work correctly
with actual REAPER functionality.
"""

import pytest
import logging
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
class TestDSLEffectsTools:
    """Test FX management DSL tools"""
    
    async def test_add_effect_basic(self, reaper_mcp_client):
        """Test adding basic effects to tracks"""
        # Create a test track
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {
            "name": "Test Track"
        })
        assert "Created track 'Test Track'" in result
        
        # Add reverb
        result = await call_dsl_tool(reaper_mcp_client, "dsl_add_effect", {
            "track": "Test Track",
            "effect": "reverb"
        })
        assert "Added reverb to track" in result
        
        # Add compression
        result = await call_dsl_tool(reaper_mcp_client, "dsl_add_effect", {
            "track": 0,
            "effect": "compression"
        })
        assert "Added compression to track 1" in result
        
        # Add EQ with preset
        result = await call_dsl_tool(reaper_mcp_client, "dsl_add_effect", {
            "track": "Test Track",
            "effect": "eq",
            "preset": "Vocal Brighten"
        })
        assert "Added eq to track" in result
        assert "with preset 'Vocal Brighten'" in result
    
    @pytest.mark.asyncio
    async def test_adjust_effect(self, reaper_mcp_client):
        """Test adjusting effect parameters"""
        # Create track and add effect
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "FX Test"})
        await call_dsl_tool(reaper_mcp_client, "dsl_add_effect", {
            "track": "FX Test",
            "effect": "reverb"
        })
        
        # Adjust with numeric value
        result = await call_dsl_tool(reaper_mcp_client, "dsl_adjust_effect", {
            "track": "FX Test",
            "effect": "reverb",
            "setting": "mix",
            "value": 0.5
        })
        assert "Adjusted reverb mix to 0.5" in result
        
        # Adjust with descriptive value
        result = await call_dsl_tool(reaper_mcp_client, "dsl_adjust_effect", {
            "track": "FX Test",
            "effect": "reverb",
            "setting": "amount",
            "value": "wet"
        })
        assert "Adjusted reverb amount to 0.7" in result
    
    @pytest.mark.asyncio
    async def test_effect_bypass(self, reaper_mcp_client):
        """Test bypassing and enabling effects"""
        # Create track and add effect
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Bypass Test"})
        
        # Add effect and check result
        add_result = await call_dsl_tool(reaper_mcp_client, "dsl_add_effect", {
            "track": "Bypass Test",
            "effect": "delay"
        })
        logger.info(f"Add effect result: {add_result}")
        assert "Added delay" in add_result
        
        # Bypass effect
        result = await call_dsl_tool(reaper_mcp_client, "dsl_effect_bypass", {
            "track": "Bypass Test",
            "effect": "delay",
            "bypass": True
        })
        logger.info(f"Bypass result: {result}")
        assert "Bypassed delay on track" in result
        
        # Enable effect
        result = await call_dsl_tool(reaper_mcp_client, "dsl_effect_bypass", {
            "track": "Bypass Test",
            "effect": "delay",
            "bypass": False
        })
        assert "Enabled delay on track" in result


class TestDSLRoutingTools:
    """Test routing and bus DSL tools"""
    
    @pytest.mark.asyncio
    async def test_create_send(self, reaper_mcp_client):
        """Test creating sends between tracks"""
        # Create source and destination tracks
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Vocals"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Reverb Bus"})
        
        # Create send at 30%
        result = await call_dsl_tool(reaper_mcp_client, "dsl_create_send", {
            "from_track": "Vocals",
            "to_track": "Reverb Bus",
            "amount": 0.3
        })
        assert "Created post-fader send" in result
        assert "at 30%" in result
        
        # Create pre-fader send
        result = await call_dsl_tool(reaper_mcp_client, "dsl_create_send", {
            "from_track": 0,
            "to_track": 1,
            "amount": 0.5,
            "pre_fader": True
        })
        assert "Created pre-fader send" in result
        assert "at 50%" in result
    
    @pytest.mark.asyncio
    async def test_create_bus_simple(self, reaper_mcp_client):
        """Test creating a simple bus"""
        # Create some tracks
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Kick"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Snare"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Hi-Hat"})
        
        # Create drum bus
        result = await call_dsl_tool(reaper_mcp_client, "dsl_create_bus", {
            "name": "Drum Bus",
            "source_tracks": ["Kick", "Snare", "Hi-Hat"]
        })
        assert "Created Drum Bus" in result
        assert "routed 3 tracks" in result
        assert "Kick" in result
        assert "Snare" in result
    
    @pytest.mark.asyncio
    async def test_create_bus_with_pattern(self, reaper_mcp_client):
        """Test creating bus with pattern matching"""
        # Create drum tracks
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Drum - Kick"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Drum - Snare"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Guitar Lead"})
        
        # Create bus for all drums
        result = await call_dsl_tool(reaper_mcp_client, "dsl_create_bus", {
            "name": "All Drums",
            "source_tracks": "all drums",
            "add_effect": "compression"
        })
        assert "Created All Drums bus with compression" in result
        assert "routed 2 tracks" in result
        assert "Drum - Kick" in result
        assert "Drum - Snare" in result
        assert "Guitar Lead" not in result


class TestDSLAutomationTools:
    """Test automation DSL tools"""
    
    @pytest.mark.asyncio
    async def test_automate_fade(self, reaper_mcp_client):
        """Test creating fade automation"""
        # Create track
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Fade Test"})
        
        # Create fade in
        result = await call_dsl_tool(reaper_mcp_client, "dsl_automate", {
            "track": "Fade Test",
            "parameter": "volume",
            "automation_type": "fade_in",
            "details": "4 bars"
        })
        assert "Created fade in" in result
        assert "on volume for track" in result
        
        # Create fade out
        result = await call_dsl_tool(reaper_mcp_client, "dsl_automate", {
            "track": 0,
            "parameter": "volume",
            "automation_type": "fade_out"
        })
        assert "Created fade out" in result
    
    @pytest.mark.asyncio
    async def test_automate_pan_sweep(self, reaper_mcp_client):
        """Test creating pan automation"""
        # Create track
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Synth"})
        
        # Create pan sweep
        result = await call_dsl_tool(reaper_mcp_client, "dsl_automate", {
            "track": "Synth",
            "parameter": "pan",
            "automation_type": "pan_sweep",
            "details": "8 bars"
        })
        assert "Created pan sweep" in result
        assert "on pan for track" in result
    
    @pytest.mark.asyncio
    async def test_automate_section(self, reaper_mcp_client):
        """Test section-based automation"""
        result = await call_dsl_tool(reaper_mcp_client, "dsl_automate_section", {
            "section": "chorus",
            "changes": {
                "volume": "+3dB",
                "reverb": "increase",
                "energy": "high"
            }
        })
        assert "Automation for section 'chorus'" in result
        assert "volume: +3dB" in result


class TestDSLMarkerTool:
    """Test marker/region DSL tool"""
    
    @pytest.mark.asyncio
    async def test_add_marker(self, reaper_mcp_client):
        """Test adding markers"""
        # Add marker at current position
        result = await call_dsl_tool(reaper_mcp_client, "dsl_marker", {
            "action": "add",
            "name": "Intro Start"
        })
        assert "Added marker 'Intro Start'" in result
        
        # Add marker at specific time
        result = await call_dsl_tool(reaper_mcp_client, "dsl_marker", {
            "action": "add",
            "position": 10.5,
            "name": "Verse 1"
        })
        assert "Added marker 'Verse 1' at 10.5 seconds" in result
        
        # Add marker at bar position
        result = await call_dsl_tool(reaper_mcp_client, "dsl_marker", {
            "action": "add",
            "position": "16 bars",
            "name": "Chorus"
        })
        assert "Added marker 'Chorus'" in result
    
    @pytest.mark.asyncio
    async def test_create_region(self, reaper_mcp_client):
        """Test creating regions"""
        result = await call_dsl_tool(reaper_mcp_client, "dsl_marker", {
            "action": "create_region",
            "position": "0-8",
            "name": "Intro"
        })
        assert "Created region 'Intro' from 0 to 8 seconds" in result
    
    @pytest.mark.asyncio
    async def test_go_to_marker(self, reaper_mcp_client):
        """Test navigating to markers"""
        # Create a marker first
        await call_dsl_tool(reaper_mcp_client, "dsl_marker", {
            "action": "add",
            "position": 20.0,
            "name": "Bridge"
        })
        
        # Navigate to it
        result = await call_dsl_tool(reaper_mcp_client, "dsl_marker", {
            "action": "go_to",
            "name": "Bridge"
        })
        assert "Moved to marker 'Bridge'" in result


class TestCompoundCommands:
    """Test compound command scenarios"""
    
    @pytest.mark.asyncio
    async def test_add_reverb_and_compress(self, reaper_mcp_client):
        """Test 'add reverb to vocals and compress them'"""
        # Create vocal track
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Lead Vocal"})
        
        # Add reverb
        result1 = await call_dsl_tool(reaper_mcp_client, "dsl_add_effect", {
            "track": "Lead Vocal",
            "effect": "reverb"
        })
        assert "Added reverb" in result1
        
        # Add compression
        result2 = await call_dsl_tool(reaper_mcp_client, "dsl_add_effect", {
            "track": "Lead Vocal",
            "effect": "compression",
            "preset": "gentle"
        })
        assert "Added compression" in result2
    
    @pytest.mark.asyncio
    async def test_create_drum_bus_workflow(self, reaper_mcp_client):
        """Test 'create drum bus, route all drums, and add compression'"""
        # Create drum tracks
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Kick Drum"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Snare Drum"})
        await call_dsl_tool(reaper_mcp_client, "dsl_track_create", {"name": "Hi-Hat"})
        
        # Create bus with compression in one call
        result = await call_dsl_tool(reaper_mcp_client, "dsl_create_bus", {
            "name": "Drum Bus",
            "source_tracks": "all drums",
            "add_effect": "compression"
        })
        
        assert "Created Drum Bus with compression" in result
        assert "routed 3 tracks" in result