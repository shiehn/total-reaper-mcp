"""Test MIDI generation capabilities"""
import pytest
import pytest_asyncio
from .test_utils import ensure_clean_project

@pytest.mark.asyncio
async def test_midi_scale_generation(reaper_mcp_client):
    """Test generating MIDI scales"""
    # Ensure clean project
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "position": 0.0,
            "length": 8.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Extract item index
    import re
    match = re.search(r'index (\d+)', result.content[0].text)
    item_index = int(match.group(1)) if match else 0
    
    # Generate C major scale
    result = await reaper_mcp_client.call_tool(
        "generate_midi_scale",
        {
            "item_index": item_index,
            "take_index": 0,
            "root_note": 60,  # Middle C
            "scale_type": "major",
            "octaves": 2,
            "note_length": 0.25
        }
    )
    assert "Generated major scale" in result.content[0].text
    assert "notes starting from C4" in result.content[0].text

@pytest.mark.asyncio
async def test_midi_chord_progression(reaper_mcp_client):
    """Test generating chord progressions"""
    # Ensure clean project
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Add a small delay to ensure track is created
    import asyncio
    await asyncio.sleep(0.1)
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "position": 0.0,
            "length": 8.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Extract item index
    import re
    match = re.search(r'index (\d+)', result.content[0].text)
    item_index = int(match.group(1)) if match else 0
    
    # Generate chord progression
    result = await reaper_mcp_client.call_tool(
        "generate_midi_chord_sequence",
        {
            "item_index": item_index,
            "take_index": 0,
            "chord_progression": ["Cmaj", "Am", "Fmaj", "G7"],
            "duration": 1.0
        }
    )
    assert "Generated chord progression" in result.content[0].text
    assert "Cmaj → Am → Fmaj → G7" in result.content[0].text

@pytest.mark.asyncio
async def test_midi_drum_pattern(reaper_mcp_client):
    """Test generating drum patterns"""
    # Ensure clean project
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track
    track_result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    print(f"Track creation result: {track_result.content[0].text}")
    
    # Check track count
    count_result = await reaper_mcp_client.call_tool(
        "count_tracks",
        {}
    )
    print(f"Track count: {count_result.content[0].text}")
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "position": 0.0,
            "length": 16.0,
            "quantize": False
        }
    )
    print(f"MIDI item creation result: {result.content[0].text}")
    assert "Created MIDI item" in result.content[0].text
    
    # Extract item index
    import re
    match = re.search(r'index (\d+)', result.content[0].text)
    item_index = int(match.group(1)) if match else 0
    
    # Generate basic rock pattern
    result = await reaper_mcp_client.call_tool(
        "generate_midi_drum_pattern",
        {
            "item_index": item_index,
            "take_index": 0,
            "pattern": "basic_rock",
            "bars": 4
        }
    )
    assert "Generated basic_rock drum pattern" in result.content[0].text
    assert "notes over 4 bars" in result.content[0].text

@pytest.mark.asyncio
async def test_midi_transformation(reaper_mcp_client):
    """Test MIDI transformation operations"""
    # Ensure clean project
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Add a small delay to ensure track is created
    import asyncio
    await asyncio.sleep(0.1)
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "position": 0.0,
            "length": 4.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Extract item index
    import re
    match = re.search(r'index (\d+)', result.content[0].text)
    item_index = int(match.group(1)) if match else 0
    
    # First generate some notes to transform
    await reaper_mcp_client.call_tool(
        "generate_midi_scale",
        {
            "item_index": item_index,
            "take_index": 0,
            "root_note": 60,
            "scale_type": "major",
            "octaves": 1,
            "note_length": 0.25
        }
    )
    
    # Test transposition
    result = await reaper_mcp_client.call_tool(
        "transpose_midi_notes",
        {
            "item_index": item_index,
            "take_index": 0,
            "semitones": 5,
            "selected_only": False
        }
    )
    assert "Transposed" in result.content[0].text
    assert "5 semitones up" in result.content[0].text
    
    # Test quantization
    result = await reaper_mcp_client.call_tool(
        "quantize_midi_notes",
        {
            "item_index": item_index,
            "take_index": 0,
            "grid": "1/16",
            "strength": 0.8
        }
    )
    assert "Quantized" in result.content[0].text
    assert "1/16 grid" in result.content[0].text
    assert "80% strength" in result.content[0].text
    
    # Test humanization
    result = await reaper_mcp_client.call_tool(
        "humanize_midi_timing",
        {
            "item_index": item_index,
            "take_index": 0,
            "timing_amount": 0.02,
            "velocity_amount": 0.15
        }
    )
    assert "Humanized" in result.content[0].text
    assert "timing: ±20ms" in result.content[0].text
    assert "velocity: ±15%" in result.content[0].text

@pytest.mark.asyncio
async def test_midi_analysis(reaper_mcp_client):
    """Test MIDI analysis functions"""
    # Ensure clean project
    await ensure_clean_project(reaper_mcp_client)
    
    # Create a track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0}
    )
    
    # Add a small delay to ensure track is created
    import asyncio
    await asyncio.sleep(0.1)
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": 0,
            "position": 0.0,
            "length": 4.0,
            "quantize": False
        }
    )
    assert "Created MIDI item" in result.content[0].text
    
    # Extract item index
    import re
    match = re.search(r'index (\d+)', result.content[0].text)
    item_index = int(match.group(1)) if match else 0
    
    # Generate some content to analyze
    chord_result = await reaper_mcp_client.call_tool(
        "generate_midi_chord_sequence",
        {
            "item_index": item_index,
            "take_index": 0,
            "chord_progression": ["Cmaj", "Fmaj", "G7", "Cmaj"],
            "duration": 1.0
        }
    )
    assert "Generated chord progression" in chord_result.content[0].text
    
    # Add a small delay to ensure MIDI notes are written
    await asyncio.sleep(0.1)
    
    # Analyze pattern
    result = await reaper_mcp_client.call_tool(
        "analyze_midi_pattern",
        {
            "item_index": item_index,
            "take_index": 0
        }
    )
    assert "MIDI pattern analysis" in result.content[0].text
    assert "Notes analyzed:" in result.content[0].text
    
    # Detect chord progressions
    result = await reaper_mcp_client.call_tool(
        "detect_midi_chord_progressions",
        {
            "item_index": item_index,
            "take_index": 0
        }
    )
    # Check that we got chord names back (should contain "major" or chord symbols)
    result_text = result.content[0].text.lower()
    assert "major" in result_text or "minor" in result_text or "→" in result_text
    
    # Get note distribution
    result = await reaper_mcp_client.call_tool(
        "get_midi_note_distribution",
        {
            "item_index": item_index,
            "take_index": 0
        }
    )
    assert "MIDI note distribution" in result.content[0].text
    assert "total notes" in result.content[0].text
    
    # Detect key signature
    result = await reaper_mcp_client.call_tool(
        "detect_midi_key_signature",
        {
            "item_index": item_index,
            "take_index": 0
        }
    )
    assert "Detected key:" in result.content[0].text
    assert "confidence:" in result.content[0].text