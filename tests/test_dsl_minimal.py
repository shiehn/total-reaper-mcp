"""
Minimal DSL integration tests that work with the existing bridge

These tests verify the DSL layer structure is correct, even if the
Lua bridge functions aren't installed yet.
"""

import pytest
import logging

logger = logging.getLogger(__name__)

async def call_dsl_tool(client, tool_name, params):
    """Helper to call DSL tools and return the text response"""
    result = await client.call_tool(tool_name, params)
    return result.content[0].text if result.content else ""

@pytest.mark.asyncio
class TestDSLStructure:
    """Test DSL tools are properly registered and callable"""
    
    async def test_dsl_tools_exist(self, reaper_mcp_client):
        """Test that DSL tools are registered when using DSL profile"""
        # Get list of available tools
        tools = await reaper_mcp_client.list_tools()
        tool_names = {t.name for t in tools.tools}
        
        # Check that DSL tools exist
        expected_dsl_tools = [
            "dsl_track_create",
            "dsl_track_volume", 
            "dsl_track_pan",
            "dsl_track_mute",
            "dsl_track_solo",
            "dsl_time_select",
            "dsl_loop_create",
            "dsl_midi_insert",
            "dsl_quantize",
            "dsl_play",
            "dsl_stop",
            "dsl_set_tempo",
            "dsl_list_tracks",
            "dsl_get_tempo_info",
            "dsl_reset_context"
        ]
        
        for tool in expected_dsl_tools:
            assert tool in tool_names, f"Missing DSL tool: {tool}"
    
    async def test_dsl_reset_context(self, reaper_mcp_client):
        """Test the context reset tool (doesn't require bridge functions)"""
        result = await call_dsl_tool(reaper_mcp_client, "dsl_reset_context", {})
        assert "Session context reset" in result
    
    async def test_dsl_play(self, reaper_mcp_client):
        """Test play command (uses DSL bridge function)"""
        result = await call_dsl_tool(reaper_mcp_client, "dsl_play", {})
        # Should either succeed, timeout, or need bridge installation
        assert any(msg in result for msg in [
            "Started playback",
            "Timeout",
            "not available in bridge",
            "DSL Lua functions need to be installed"
        ])
    
    async def test_dsl_stop(self, reaper_mcp_client):
        """Test stop command (uses DSL bridge function)"""  
        result = await call_dsl_tool(reaper_mcp_client, "dsl_stop", {})
        # Should either succeed, timeout, or need bridge installation
        assert any(msg in result for msg in [
            "Stopped playback",
            "Timeout", 
            "not available in bridge",
            "DSL Lua functions need to be installed"
        ])
    
    async def test_dsl_tool_descriptions(self, reaper_mcp_client):
        """Test that DSL tools have proper descriptions"""
        tools = await reaper_mcp_client.list_tools()
        
        dsl_tools = {t.name: t for t in tools.tools if t.name.startswith("dsl_")}
        
        # Check a few key tools have good descriptions
        volume_desc = dsl_tools["dsl_track_volume"].description.lower()
        assert "flexible" in volume_desc
        assert "track" in volume_desc and "volume" in volume_desc
        
        loop_desc = dsl_tools["dsl_loop_create"].description.lower()
        assert "loop" in loop_desc
        
        midi_desc = dsl_tools["dsl_midi_insert"].description.lower()
        assert "midi" in midi_desc
        assert "external" in midi_desc or "insert" in midi_desc

@pytest.mark.asyncio 
class TestDSLErrorHandling:
    """Test DSL error handling without requiring bridge functions"""
    
    async def test_missing_required_params(self, reaper_mcp_client):
        """Test handling of missing required parameters"""
        # Check that the tool has required parameters in its schema
        tools = await reaper_mcp_client.list_tools()
        volume_tool = next(t for t in tools.tools if t.name == "dsl_track_volume")
        
        # The tool should have an input schema with required fields
        assert volume_tool.inputSchema is not None
        
        # Try to call without params - MCP may or may not validate
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {})
        # Should get an error from our code if MCP doesn't validate
        assert "Error:" in result or "required" in result.lower()
    
    async def test_invalid_track_reference(self, reaper_mcp_client):
        """Test handling of invalid track reference"""
        # This will fail at the resolver level
        result = await call_dsl_tool(reaper_mcp_client, "dsl_track_volume", {
            "track": "NonExistentTrack_XYZ_123",
            "volume": "-6dB"
        })
        assert "Error:" in result or "Failed" in result
    
    async def test_invalid_time_format(self, reaper_mcp_client):
        """Test handling of invalid time format"""
        result = await call_dsl_tool(reaper_mcp_client, "dsl_time_select", {
            "time": "invalid time format xyz"
        })
        assert "Error:" in result or "Cannot parse time" in result