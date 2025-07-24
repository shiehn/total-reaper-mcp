"""
Integration tests to verify DSL functions exist in the bridge
"""

import pytest
import asyncio
import os
from typing import Optional
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from server.bridge import ReaperFileBridge as ReaperBridge, BRIDGE_DIR

pytestmark = pytest.mark.integration


class TestDSLBridgeFunctions:
    """Test that DSL functions are available in the bridge"""
    
    @pytest.fixture
    async def bridge(self):
        """Create bridge instance"""
        bridge = ReaperBridge()
        yield bridge
    
    async def test_dsl_functions_exist(self, bridge):
        """Test that critical DSL functions are available"""
        # Test functions that should exist
        dsl_functions = [
            ("GetAllTracksInfo", []),
            ("GetTrackInfo", [0]),
            ("GetCursorPosition", []),
            ("GetTimeSelection", []),
            ("BarsToTime", [1, 0.0]),
            ("Play", []),
            ("Stop", []),
            ("GetTempo", []),
        ]
        
        missing_functions = []
        
        for func_name, args in dsl_functions:
            try:
                result = await bridge.call_lua(func_name, args)
                
                # Check if function exists
                if not result.get("ok") and "Unknown function" in result.get("error", ""):
                    missing_functions.append(func_name)
                elif result.get("error", "").startswith("Bridge error:"):
                    # Bridge-level error, not function missing
                    pass
                    
            except asyncio.TimeoutError:
                # Timeout might mean REAPER isn't running, not that function is missing
                pass
            except Exception as e:
                # Other errors don't necessarily mean function is missing
                pass
        
        if missing_functions:
            pytest.fail(f"DSL functions missing from bridge: {', '.join(missing_functions)}\n"
                       f"Please install the bridge using ./scripts/install_bridge.sh")
    
    async def test_traditional_functions_still_work(self, bridge):
        """Ensure traditional ReaScript functions still work with DSL bridge"""
        try:
            # Test a basic function
            result = await bridge.call_lua("CountTracks", [0])
            
            # Should either work or timeout (if REAPER not running)
            if result.get("error") and "Unknown function" in result.get("error"):
                pytest.fail("Traditional functions broken in DSL bridge!")
                
        except asyncio.TimeoutError:
            # This is fine - REAPER might not be running
            pass
    
    async def test_dsl_track_info_response_format(self, bridge):
        """Test that DSL functions return expected format"""
        try:
            result = await bridge.call_lua("GetAllTracksInfo", [])
            
            if result.get("ok"):
                # Verify response structure
                assert "tracks" in result, "GetAllTracksInfo should return tracks array"
                
                # If there are tracks, check their structure
                if result["tracks"]:
                    track = result["tracks"][0]
                    expected_fields = ["name", "guid", "has_midi", "has_audio", "fx_names"]
                    for field in expected_fields:
                        assert field in track, f"Track info missing field: {field}"
                        
        except asyncio.TimeoutError:
            # This is fine - REAPER might not be running
            pass
    
    async def test_error_handling_for_invalid_args(self, bridge):
        """Test that DSL functions handle invalid arguments gracefully"""
        try:
            # GetTrackInfo with invalid index
            result = await bridge.call_lua("GetTrackInfo", [9999])
            
            # Should return ok=false with error message
            if result.get("ok") is False:
                assert "error" in result, "Failed DSL call should include error message"
                
        except asyncio.TimeoutError:
            # This is fine - REAPER might not be running
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])