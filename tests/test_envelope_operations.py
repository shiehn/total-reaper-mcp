import pytest
import pytest_asyncio
from .test_utils import (
    ensure_clean_project,
    create_track_with_verification,
    get_track_envelope_with_verification,
    assert_response_contains,
    assert_response_success,
    extract_number_from_response
)

def assert_tools_available(available_tools, required_tools):
    """Assert that all required tools are available, failing with clear message if not"""
    for tool in required_tools:
        assert tool in available_tools, f"MISSING IMPLEMENTATION: Tool '{tool}' is not implemented in the server but is required for envelope functionality"

@pytest.mark.asyncio
async def test_envelope_basic_operations(reaper_mcp_client):
    """Test basic envelope operations"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Get volume envelope
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope_by_name",
        {"track_index": track_index, "envelope_name": "Volume"}
    )
    print(f"Get volume envelope result: {result}")
    assert_response_contains(result, "Found envelope")
    assert_response_contains(result, "Volume")
    
    # Count initial points (should be 0 or minimal)
    result = await reaper_mcp_client.call_tool(
        "count_envelope_points",
        {"track_index": track_index, "envelope_name": "Volume"}
    )
    print(f"Count points result: {result}")
    initial_count = extract_number_from_response(result.content[0].text, r'has (\d+) points') or 0
    
    # Insert a point at 0s with full volume
    result = await reaper_mcp_client.call_tool(
        "insert_envelope_point",
        {
            "track_index": track_index,
            "envelope_name": "Volume",
            "time": 0.0,
            "value": 1.0,
            "shape": 0
        }
    )
    print(f"Insert point result: {result}")
    assert_response_contains(result, "Inserted point at")
    
    # Insert another point at 2s with half volume
    result = await reaper_mcp_client.call_tool(
        "insert_envelope_point",
        {
            "track_index": track_index,
            "envelope_name": "Volume",
            "time": 2.0,
            "value": 0.5,
            "shape": 0
        }
    )
    assert_response_contains(result, "Inserted point at")
    
    # Count points again
    result = await reaper_mcp_client.call_tool(
        "count_envelope_points",
        {"track_index": track_index, "envelope_name": "Volume"}
    )
    new_count = extract_number_from_response(result.content[0].text, r'has (\d+) points') or 0
    assert new_count >= initial_count + 2

@pytest.mark.asyncio
async def test_envelope_point_manipulation(reaper_mcp_client):
    """Test getting and setting envelope points"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create track and get its actual index
    track_index = await create_track_with_verification(reaper_mcp_client)
    
    # Insert a point
    await reaper_mcp_client.call_tool(
        "insert_envelope_point",
        {
            "track_index": track_index,
            "envelope_name": "Volume",
            "time": 1.0,
            "value": 0.8,
            "shape": 0
        }
    )
    
    # Get point info
    result = await reaper_mcp_client.call_tool(
        "get_envelope_point",
        {
            "track_index": track_index,
            "envelope_name": "Volume",
            "point_index": 0
        }
    )
    print(f"Get point info result: {result}")
    assert "time=" in result.content[0].text and "value=" in result.content[0].text
    
    # Set point value
    result = await reaper_mcp_client.call_tool(
        "set_envelope_point_value",
        {
            "track_index": 0,
            "envelope_name": "Volume",
            "point_index": 0,
            "value": 0.6
        }
    )
    print(f"Set point value result: {result}")
    assert "updated point" in result.content[0].text.lower()
    
    # Verify the value was changed
    result = await reaper_mcp_client.call_tool(
        "get_envelope_point",
        {
            "track_index": 0,
            "envelope_name": "Volume",
            "point_index": 0
        }
    )
    assert "value=0.6" in result.content[0].text

@pytest.mark.asyncio
async def test_envelope_pan_automation(reaper_mcp_client):
    """Test pan envelope automation"""
    # Create track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Create pan automation - pan from left to right
    times_and_values = [
        (0.0, -1.0),  # Hard left
        (1.0, 0.0),   # Center
        (2.0, 1.0),   # Hard right
        (3.0, 0.0)    # Back to center
    ]
    
    for time, value in times_and_values:
        result = await reaper_mcp_client.call_tool(
            "insert_envelope_point",
            {
                "track_index": 0,
                "envelope_name": "Pan",
                "time": time,
                "value": value,
                "shape": 0
            }
        )
        print(f"Insert pan point at {time}s: {result}")
        assert "Inserted point at" in result.content[0].text
    
    # Count pan envelope points
    result = await reaper_mcp_client.call_tool(
        "count_envelope_points",
        {"track_index": 0, "envelope_name": "Pan"}
    )
    assert "4" in result.content[0].text

@pytest.mark.asyncio
async def test_envelope_delete_points(reaper_mcp_client):
    """Test deleting envelope points"""
    # Create track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Insert multiple points
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "insert_envelope_point",
            {
                "track_index": 0,
                "envelope_name": "Volume",
                "time": float(i),
                "value": 1.0 - (i * 0.3),
                "shape": 0
            }
        )
    
    # Count points
    result = await reaper_mcp_client.call_tool(
        "count_envelope_points",
        {"track_index": 0, "envelope_name": "Volume"}
    )
    count_before = int(''.join(filter(str.isdigit, result.content[0].text)) or "0")
    
    # Delete middle point (index 1)
    result = await reaper_mcp_client.call_tool(
        "delete_envelope_point",
        {
            "track_index": 0,
            "envelope_name": "Volume",
            "point_index": 1
        }
    )
    print(f"Delete point result: {result}")
    assert "deleted point" in result.content[0].text.lower()
    
    # Count again
    result = await reaper_mcp_client.call_tool(
        "count_envelope_points",
        {"track_index": 0, "envelope_name": "Volume"}
    )
    count_after = int(''.join(filter(str.isdigit, result.content[0].text)) or "0")
    assert count_after == count_before - 1

@pytest.mark.asyncio
async def test_envelope_shapes(reaper_mcp_client):
    """Test different envelope point shapes"""
    # Create track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Test different shapes
    shapes = [
        (0, "linear"),
        (1, "square"),
        (2, "slow start/end"),
        (3, "fast start"),
        (4, "fast end"),
        (5, "bezier")
    ]
    
    for i, (shape_id, shape_name) in enumerate(shapes):
        result = await reaper_mcp_client.call_tool(
            "insert_envelope_point",
            {
                "track_index": 0,
                "envelope_name": "Volume",
                "time": float(i),
                "value": 0.8,
                "shape": shape_id
            }
        )
        print(f"Insert {shape_name} point: {result}")
        assert "Inserted point at" in result.content[0].text

@pytest.mark.asyncio
async def test_envelope_error_handling(reaper_mcp_client):
    """Test error handling for envelope operations"""
    # Try to get envelope on non-existent track
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope_by_name",
        {"track_index": 999, "envelope_name": "Volume"}
    )
    assert "failed" in result.content[0].text.lower()
    
    # Create track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Try to get non-existent envelope
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope_by_name",
        {"track_index": 0, "envelope_name": "NonExistentEnvelope"}
    )
    assert "not found" in result.content[0].text.lower()
    
    # Try to get non-existent point
    result = await reaper_mcp_client.call_tool(
        "get_envelope_point",
        {
            "track_index": 0,
            "envelope_name": "Volume",
            "point_index": 999
        }
    )
    assert "not found" in result.content[0].text.lower() or "failed" in result.content[0].text.lower()