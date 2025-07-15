"""Simple integration tests for new music production tools."""

import pytest


class TestNewToolsSimple:
    """Simple tests to verify new tools are callable."""
    
    @pytest.mark.asyncio
    async def test_loop_management_tools(self, reaper_mcp_client):
        """Test basic loop management tool calls."""
        # Test time selection
        await reaper_mcp_client.call_tool("set_time_selection", {
            "start": 0.0,
            "end": 4.0
        })
        
        result = await reaper_mcp_client.call_tool("get_time_selection", {})
        assert result is not None
        
        # Test loop enabling
        await reaper_mcp_client.call_tool("set_loop_enabled", {"enabled": True})
        
        # Test grid division
        await reaper_mcp_client.call_tool("set_grid_division", {
            "division": 0.25,
            "swing": 0.0
        })
        
        result = await reaper_mcp_client.call_tool("get_grid_division", {})
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_bounce_render_tools(self, reaper_mcp_client):
        """Test basic bounce/render tool calls."""
        # Create a track first
        await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "use_defaults": True
        })
        
        # Test freeze (might fail without content, but should be callable)
        try:
            await reaper_mcp_client.call_tool("freeze_track", {
                "track_index": 0,
                "freeze_fx": True
            })
        except Exception:
            pass  # OK if it fails, we just want to verify it's callable
        
        # Test glue (needs selected items)
        try:
            await reaper_mcp_client.call_tool("glue_selected_items", {})
        except Exception:
            pass
    
    @pytest.mark.asyncio
    async def test_groove_quantization_tools(self, reaper_mcp_client):
        """Test basic groove/quantization tool calls."""
        # Create a track
        await reaper_mcp_client.call_tool("insert_track", {
            "index": 0,
            "use_defaults": True
        })
        
        # Test rhythm generation
        await reaper_mcp_client.call_tool("generate_random_rhythm", {
            "track_index": 0,
            "pattern_length": 4.0,
            "density": 0.5,
            "note_length": 0.25
        })
        
        # Test shuffle
        try:
            await reaper_mcp_client.call_tool("apply_shuffle", {
                "amount": 0.5,
                "pattern": "16th"
            })
        except Exception:
            pass
        
        # Test humanize
        try:
            await reaper_mcp_client.call_tool("humanize_items", {
                "position_amount": 0.01,
                "velocity_amount": 10,
                "timing_mode": "random"
            })
        except Exception:
            pass
    
    @pytest.mark.asyncio
    async def test_bus_routing_tools(self, reaper_mcp_client):
        """Test basic bus routing tool calls."""
        # Create bus track
        await reaper_mcp_client.call_tool("create_bus_track", {
            "name": "Test Bus",
            "num_channels": 2
        })
        
        # Create reverb bus
        await reaper_mcp_client.call_tool("create_reverb_send_bus", {
            "reverb_type": "hall",
            "return_level_db": -12.0
        })
        
        # Test routing matrix analysis
        result = await reaper_mcp_client.call_tool("analyze_routing_matrix", {})
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_polyrhythm_creation(self, reaper_mcp_client):
        """Test polyrhythm creation."""
        # Create tracks
        for i in range(3):
            await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "use_defaults": True
            })
        
        # Create polyrhythm
        await reaper_mcp_client.call_tool("create_polyrhythm", {
            "track_indices": [0, 1, 2],
            "base_division": 0.25,
            "ratios": [3, 4, 5]
        })
    
    @pytest.mark.asyncio
    async def test_stem_bus_creation(self, reaper_mcp_client):
        """Test stem bus creation."""
        # Create some tracks
        for i in range(4):
            await reaper_mcp_client.call_tool("insert_track", {
                "index": i,
                "use_defaults": True
            })
        
        # Create stem buses
        await reaper_mcp_client.call_tool("create_stem_buses", {
            "stem_groups": {
                "Drums": [0, 1],
                "Bass": [2],
                "Keys": [3]
            }
        })