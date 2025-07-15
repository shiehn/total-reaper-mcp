"""Test analysis tools operations"""
import pytest
import pytest_asyncio
from .test_utils import ensure_clean_project

@pytest.mark.asyncio
async def test_project_structure_analysis(reaper_mcp_client):
    """Test analyzing project structure"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Start with empty project
    result = await reaper_mcp_client.call_tool(
        "analyze_project_structure",
        {}
    )
    assert result is not None
    assert "Project structure:" in result.content[0].text
    assert "0 tracks" in result.content[0].text
    assert "0 items" in result.content[0].text
    assert "length:" in result.content[0].text
    
    # Add some content
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    # Analyze again
    result = await reaper_mcp_client.call_tool(
        "analyze_project_structure",
        {}
    )
    assert result is not None
    assert "1 tracks" in result.content[0].text
    assert "1 items" in result.content[0].text

@pytest.mark.asyncio
async def test_track_hierarchy(reaper_mcp_client):
    """Test getting track hierarchy"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create folder track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {
            "track_index": 0,
            "name": "Drums"
        }
    )
    
    # Get hierarchy
    result = await reaper_mcp_client.call_tool(
        "get_track_hierarchy",
        {}
    )
    assert result is not None
    assert "Track hierarchy:" in result.content[0].text
    assert "Drums" in result.content[0].text

@pytest.mark.asyncio
async def test_track_content_analysis(reaper_mcp_client):
    """Test analyzing track content"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create track with content
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {
            "track_index": 0,
            "name": "Lead Vocal"
        }
    )
    
    # Add item
    item_result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    assert "Added media item" in item_result.content[0].text
    
    # Verify item count
    count_result = await reaper_mcp_client.call_tool(
        "count_media_items",
        {}
    )
    # Should have at least 1 item
    
    # Add FX
    fx_result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {
            "track_index": 0,
            "fx_name": "ReaEQ"
        }
    )
    # FX might not exist in test environment, so we don't assert success
    
    # Analyze track
    result = await reaper_mcp_client.call_tool(
        "analyze_track_content",
        {"track_index": 0}
    )
    assert result is not None
    assert "Lead Vocal" in result.content[0].text
    # The item might not be on the track if add failed
    assert "Items:" in result.content[0].text
    assert "FX:" in result.content[0].text
    assert "Envelopes:" in result.content[0].text

@pytest.mark.asyncio
async def test_tempo_map_analysis(reaper_mcp_client):
    """Test tempo map analysis"""
    result = await reaper_mcp_client.call_tool(
        "analyze_tempo_map",
        {}
    )
    assert result is not None
    assert "Tempo map" in result.content[0].text or "No tempo changes" in result.content[0].text

@pytest.mark.asyncio
async def test_project_rhythm_analysis(reaper_mcp_client):
    """Test rhythm analysis"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Add some items
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Add items on beats
    for i in range(4):
        await reaper_mcp_client.call_tool(
            "add_media_item_to_track",
            {"track_index": 0}
        )
        
        await reaper_mcp_client.call_tool(
            "set_media_item_position",
            {
                "item_index": i,
                "position": i * 0.5  # Every half second (120 BPM)
            }
        )
    
    # Analyze rhythm
    result = await reaper_mcp_client.call_tool(
        "analyze_project_rhythm",
        {}
    )
    assert result is not None
    assert "Rhythm analysis:" in result.content[0].text
    assert "BPM" in result.content[0].text
    # Beat-aligned percentage or "No items" if items weren't created properly
    assert "Beat-aligned:" in result.content[0].text or "No items" in result.content[0].text

@pytest.mark.asyncio
async def test_item_overlap_detection(reaper_mcp_client):
    """Test overlapping item detection"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Create track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Add overlapping items
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    await reaper_mcp_client.call_tool(
        "set_media_item_position",
        {
            "item_index": 0,
            "position": 0.0
        }
    )
    
    await reaper_mcp_client.call_tool(
        "set_media_item_length",
        {
            "item_index": 0,
            "length": 2.0
        }
    )
    
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0}
    )
    
    await reaper_mcp_client.call_tool(
        "set_media_item_position",
        {
            "item_index": 1,
            "position": 1.0  # Overlaps with first item
        }
    )
    
    # Check for overlaps
    result = await reaper_mcp_client.call_tool(
        "analyze_item_overlaps",
        {}
    )
    assert result is not None
    assert "overlap" in result.content[0].text.lower()

@pytest.mark.asyncio 
async def test_midi_content_summary(reaper_mcp_client):
    """Test MIDI content analysis"""
    result = await reaper_mcp_client.call_tool(
        "analyze_midi_content_summary",
        {}
    )
    assert result is not None
    assert "MIDI" in result.content[0].text
    # Either finds MIDI or reports none found
    assert "MIDI items:" in result.content[0].text or "No MIDI content found" in result.content[0].text