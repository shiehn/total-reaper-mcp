"""Debug test for new tools."""

import pytest


class TestDebugNewTools:
    """Debug tests to understand the result format."""
    
    @pytest.mark.asyncio
    async def test_result_format(self, reaper_mcp_client):
        """Test to understand result format."""
        # Test a simple call
        result = await reaper_mcp_client.call_tool("get_time_selection", {})
        
        print(f"Result type: {type(result)}")
        print(f"Result value: {result}")
        print(f"Result dir: {dir(result)}")
        
        # Try different access methods
        try:
            print(f"Direct access: start = {result['start']}")
        except Exception as e:
            print(f"Direct access failed: {e}")
        
        try:
            print(f"Get method: start = {result.get('start')}")
        except Exception as e:
            print(f"Get method failed: {e}")
        
        try:
            print(f"Content attr: {result.content}")
        except Exception as e:
            print(f"Content attr failed: {e}")
        
        # Check if it's a dict-like object
        if hasattr(result, 'items'):
            print("Result items:")
            for k, v in result.items():
                print(f"  {k}: {v}")