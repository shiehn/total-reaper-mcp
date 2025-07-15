"""Test video and visual media operations"""
import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_video_item_detection(reaper_mcp_client):
    """Test detecting if item contains video"""
    # Create a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Add an item
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    # Check if item has video (should be false for empty item)
    result = await reaper_mcp_client.call_tool(
        "is_item_video",
        {"item_index": 0}
    )
    assert result is not None
    assert "video" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_video_processor_operations(reaper_mcp_client):
    """Test video processor management"""
    # Create a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Get initial video processor count
    result = await reaper_mcp_client.call_tool(
        "get_video_processor_count",
        {"track_index": 0}
    )
    assert result is not None
    assert "0 video processor" in result.content[0].text
    
    # Try to add a video processor (may not exist in test environment)
    result = await reaper_mcp_client.call_tool(
        "add_video_processor",
        {
            "track_index": 0,
            "processor_name": "Video processor: Chroma-key"
        }
    )
    assert result is not None
    # Either added or not found
    assert "video processor" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_video_fade_settings(reaper_mcp_client):
    """Test setting video fades on items"""
    # Create a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Add an item
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    # Set video fades
    result = await reaper_mcp_client.call_tool(
        "set_item_video_fade",
        {
            "item_index": 0,
            "fade_in": 0.5,
            "fade_out": 1.0
        }
    )
    assert result is not None
    assert "0.50s" in result.content[0].text
    assert "1.00s" in result.content[0].text

@pytest.mark.asyncio
async def test_project_video_settings(reaper_mcp_client):
    """Test getting project video settings"""
    result = await reaper_mcp_client.call_tool(
        "get_project_video_settings",
        {}
    )
    assert result is not None
    assert "Video settings:" in result.content[0].text
    # Should show resolution and fps
    assert "x" in result.content[0].text  # Resolution format
    assert "fps" in result.content[0].text

@pytest.mark.asyncio
async def test_video_window_operations(reaper_mcp_client):
    """Test video window management"""
    # Set video window position
    result = await reaper_mcp_client.call_tool(
        "set_video_window_position",
        {
            "x": 100,
            "y": 100,
            "width": 800,
            "height": 600
        }
    )
    assert result is not None
    assert "800x600" in result.content[0].text
    assert "(100, 100)" in result.content[0].text
    
    # Toggle video window
    result = await reaper_mcp_client.call_tool(
        "toggle_video_window",
        {}
    )
    assert result is not None
    assert "Toggled video window" in result.content[0].text

@pytest.mark.asyncio
async def test_video_fx_on_takes(reaper_mcp_client):
    """Test video FX operations on takes"""
    # Create a track with an item
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    # Get initial video FX count
    result = await reaper_mcp_client.call_tool(
        "get_take_video_fx_count",
        {
            "item_index": 0,
            "take_index": 0
        }
    )
    assert result is not None
    assert "0 video FX" in result.content[0].text
    
    # Try to add video FX
    result = await reaper_mcp_client.call_tool(
        "add_take_video_fx",
        {
            "item_index": 0,
            "take_index": 0,
            "fx_name": "Video processor: Opacity"
        }
    )
    assert result is not None
    assert "video fx" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_video_colorspace(reaper_mcp_client):
    """Test video colorspace settings"""
    result = await reaper_mcp_client.call_tool(
        "set_video_colorspace",
        {"colorspace": "Rec709"}
    )
    assert result is not None
    assert "Rec709" in result.content[0].text
    
    # Test invalid colorspace
    result = await reaper_mcp_client.call_tool(
        "set_video_colorspace",
        {"colorspace": "InvalidSpace"}
    )
    assert result is not None
    assert "Invalid colorspace" in result.content[0].text

@pytest.mark.asyncio
async def test_video_content_analysis(reaper_mcp_client):
    """Test analyzing video content in project"""
    result = await reaper_mcp_client.call_tool(
        "analyze_video_content",
        {}
    )
    assert result is not None
    assert "video" in result.content[0].text.lower()
    # Either finds video or reports none
    assert "Video items:" in result.content[0].text or "No video content" in result.content[0].text

@pytest.mark.asyncio
async def test_video_item_properties(reaper_mcp_client):
    """Test getting video item properties"""
    # Create a track with an item
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    # Get video properties
    result = await reaper_mcp_client.call_tool(
        "get_video_item_properties",
        {"item_index": 0}
    )
    assert result is not None
    # Should show position and length or indicate no video
    assert "Position:" in result.content[0].text or "does not contain video" in result.content[0].text

@pytest.mark.asyncio
async def test_render_video_frame(reaper_mcp_client):
    """Test video frame rendering setup"""
    result = await reaper_mcp_client.call_tool(
        "render_video_frame",
        {
            "time_position": 5.0,
            "output_path": "/tmp/frame.png"
        }
    )
    assert result is not None
    assert "Frame rendering" in result.content[0].text
    assert "5.000s" in result.content[0].text
    assert "/tmp/frame.png" in result.content[0].text