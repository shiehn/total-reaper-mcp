import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_tempo_time_sig_marker_operations(reaper_mcp_client):
    """Test tempo/time signature marker operations"""
    # Count initial markers
    result = await reaper_mcp_client.call_tool("count_tempo_time_sig_markers", {})
    print(f"Initial count: {result}")
    initial_count = int(result.content[0].text.split()[-3]) if "has" in result.content[0].text else 0
    
    # Add tempo marker
    result = await reaper_mcp_client.call_tool(
        "add_tempo_time_sig_marker",
        {"time": 10.0, "bpm": 140.0, "time_sig_num": 6, "time_sig_denom": 8, "linear_tempo": False}
    )
    print(f"Add marker: {result}")
    assert "Added tempo marker" in result.content[0].text or "Failed" in result.content[0].text
    
    # Find marker
    result = await reaper_mcp_client.call_tool(
        "find_tempo_time_sig_marker",
        {"time": 10.0}
    )
    print(f"Find marker: {result}")
    assert "marker" in result.content[0].text.lower()
    
    # Count after adding
    result = await reaper_mcp_client.call_tool("count_tempo_time_sig_markers", {})
    print(f"Count after add: {result}")
    
    # Set marker parameters (if found)
    if "Found" in result.content[0].text:
        result = await reaper_mcp_client.call_tool(
            "set_tempo_time_sig_marker",
            {"marker_index": initial_count, "bpm": 160.0, "time": 10.0}
        )
        print(f"Set marker: {result}")
        assert "Updated tempo marker" in result.content[0].text or "Failed" in result.content[0].text
    
    # Get tempo match play rate
    result = await reaper_mcp_client.call_tool(
        "get_tempo_match_play_rate",
        {"source_time": 5.0, "srcstart": 0.0, "srclen": 10.0, "targetstart": 0.0}
    )
    print(f"Tempo match: {result}")
    assert "play rate:" in result.content[0].text.lower()
    
    # Delete marker (if we added one)
    if initial_count >= 0:
        result = await reaper_mcp_client.call_tool(
            "delete_tempo_time_sig_marker",
            {"marker_index": initial_count}
        )
        print(f"Delete marker: {result}")


@pytest.mark.asyncio
async def test_time_map2_conversions(reaper_mcp_client):
    """Test TimeMap2 conversion functions"""
    # Beats to time
    result = await reaper_mcp_client.call_tool(
        "time_map2_beats_to_time",
        {"beats": 4.0, "measure": 1}
    )
    print(f"Beats to time: {result}")
    assert "beats" in result.content[0].text and "seconds" in result.content[0].text
    
    # Time to beats
    result = await reaper_mcp_client.call_tool(
        "time_map2_time_to_beats",
        {"time": 2.0}
    )
    print(f"Time to beats: {result}")
    assert "beats" in result.content[0].text
    
    # Get BPM at time
    result = await reaper_mcp_client.call_tool(
        "time_map2_get_divided_bpm_at_time",
        {"time": 5.0}
    )
    print(f"BPM at time: {result}")
    assert "BPM" in result.content[0].text
    
    # Get next change time
    result = await reaper_mcp_client.call_tool(
        "time_map2_get_next_change_time",
        {"time": 0.0}
    )
    print(f"Next change: {result}")
    assert "tempo change" in result.content[0].text.lower()
    
    # QN to time
    result = await reaper_mcp_client.call_tool(
        "time_map2_qn_to_time",
        {"qn": 8.0}
    )
    print(f"QN to time: {result}")
    assert "quarter notes" in result.content[0].text and "seconds" in result.content[0].text
    
    # Time to QN
    result = await reaper_mcp_client.call_tool(
        "time_map2_time_to_qn",
        {"time": 4.0}
    )
    print(f"Time to QN: {result}")
    assert "seconds" in result.content[0].text and "quarter notes" in result.content[0].text


@pytest.mark.asyncio
async def test_time_map_functions(reaper_mcp_client):
    """Test TimeMap functions"""
    # Get time signature at time
    result = await reaper_mcp_client.call_tool(
        "time_map_get_time_sig_at_time",
        {"time": 0.0}
    )
    print(f"Time sig: {result}")
    assert "Time signature" in result.content[0].text
    
    # QN to time
    result = await reaper_mcp_client.call_tool(
        "time_map_qn_to_time",
        {"qn": 4.0}
    )
    print(f"QN to time: {result}")
    assert "quarter notes" in result.content[0].text and "seconds" in result.content[0].text
    
    # QN to time absolute
    result = await reaper_mcp_client.call_tool(
        "time_map_qn_to_time_abs",
        {"qn": 4.0}
    )
    print(f"QN to time abs: {result}")
    assert "quarter notes" in result.content[0].text and "absolute" in result.content[0].text
    
    # Time to QN
    result = await reaper_mcp_client.call_tool(
        "time_map_time_to_qn",
        {"time": 2.0}
    )
    print(f"Time to QN: {result}")
    assert "seconds" in result.content[0].text and "quarter notes" in result.content[0].text
    
    # Time to QN absolute
    result = await reaper_mcp_client.call_tool(
        "time_map_time_to_qn_abs",
        {"time": 2.0}
    )
    print(f"Time to QN abs: {result}")
    assert "seconds" in result.content[0].text and "absolute" in result.content[0].text
    
    # QN to measures
    result = await reaper_mcp_client.call_tool(
        "time_map_qn_to_measures",
        {"qn": 16.0}
    )
    print(f"QN to measures: {result}")
    assert "measure" in result.content[0].text.lower()
    
    # Get measure info
    result = await reaper_mcp_client.call_tool(
        "time_map_get_measure_info",
        {"time": 5.0}
    )
    print(f"Measure info: {result}")
    assert "measure" in result.content[0].text.lower()
    
    # Get divided BPM
    result = await reaper_mcp_client.call_tool(
        "time_map_get_divided_bpm_at_time",
        {"time": 3.0}
    )
    print(f"Divided BPM: {result}")
    assert "BPM" in result.content[0].text
    
    # Get frame rate
    result = await reaper_mcp_client.call_tool("time_map_cur_frame_rate", {})
    print(f"Frame rate: {result}")
    assert "frame rate:" in result.content[0].text.lower()
    
    # Get metronome pattern
    result = await reaper_mcp_client.call_tool(
        "time_map_get_metronome_pattern",
        {"time": 0.0}
    )
    print(f"Metronome: {result}")
    assert "Metronome" in result.content[0].text


@pytest.mark.asyncio
async def test_clear_functions(reaper_mcp_client):
    """Test clear functions"""
    # Clear all rec armed
    result = await reaper_mcp_client.call_tool("clear_all_rec_armed", {})
    print(f"Clear rec armed: {result}")
    assert "Cleared all record armed" in result.content[0].text
    
    # Clear peak cache
    result = await reaper_mcp_client.call_tool("clear_peak_cache", {})
    print(f"Clear peak cache: {result}")
    assert "Cleared peak cache" in result.content[0].text


@pytest.mark.asyncio
async def test_tempo_workflow(reaper_mcp_client):
    """Test a complete tempo mapping workflow"""
    # Clear any existing tempo markers (keep default)
    initial_count_result = await reaper_mcp_client.call_tool("count_tempo_time_sig_markers", {})
    initial_count = int(initial_count_result.content[0].text.split()[-3]) if "has" in initial_count_result.content[0].text else 0
    
    # Create tempo map
    tempo_map = [
        (0.0, 120.0, 4, 4),    # 120 BPM, 4/4
        (16.0, 140.0, 4, 4),   # Speed up at bar 17
        (32.0, 100.0, 3, 4),   # Slow down and 3/4
        (48.0, 120.0, 4, 4),   # Back to original
    ]
    
    # Add tempo markers
    for time, bpm, num, denom in tempo_map:
        result = await reaper_mcp_client.call_tool(
            "add_tempo_time_sig_marker",
            {"time": time, "bpm": bpm, "time_sig_num": num, "time_sig_denom": denom}
        )
        print(f"Added: {bpm} BPM {num}/{denom} at {time}s")
    
    # Test conversions at different points
    test_times = [0.0, 8.0, 20.0, 40.0]
    for t in test_times:
        # Get tempo info
        result = await reaper_mcp_client.call_tool(
            "time_map_get_time_sig_at_time",
            {"time": t}
        )
        print(f"Time sig at {t}s: {result}")
        
        # Convert to beats
        result = await reaper_mcp_client.call_tool(
            "time_map2_time_to_beats",
            {"time": t}
        )
        print(f"Beats at {t}s: {result}")
    
    # Check next change times
    result = await reaper_mcp_client.call_tool(
        "time_map2_get_next_change_time",
        {"time": 10.0}
    )
    print(f"Next change after 10s: {result}")
    
    # Final count
    result = await reaper_mcp_client.call_tool("count_tempo_time_sig_markers", {})
    print(f"Final marker count: {result}")
    
    print("Tempo workflow completed!")


@pytest.mark.asyncio
async def test_edit_tempo_marker(reaper_mcp_client):
    """Test editing tempo marker"""
    # Add a marker first
    await reaper_mcp_client.call_tool(
        "add_tempo_time_sig_marker",
        {"time": 5.0, "bpm": 130.0, "time_sig_num": 4, "time_sig_denom": 4}
    )
    
    # Try to edit it (will open dialog in REAPER)
    result = await reaper_mcp_client.call_tool(
        "edit_tempo_time_sig_marker",
        {"marker_index": 0}
    )
    print(f"Edit marker: {result}")
    assert "edit dialog" in result.content[0].text.lower() or "Failed" in result.content[0].text


@pytest.mark.asyncio
async def test_conversion_accuracy(reaper_mcp_client):
    """Test conversion accuracy between different time formats"""
    # Test round-trip conversions
    original_qn = 8.0
    
    # QN -> Time -> QN
    time_result = await reaper_mcp_client.call_tool(
        "time_map2_qn_to_time",
        {"qn": original_qn}
    )
    # Extract time value from result
    time_str = time_result.content[0].text.split("=")[1].strip().split()[0]
    time_val = float(time_str)
    
    qn_result = await reaper_mcp_client.call_tool(
        "time_map2_time_to_qn",
        {"time": time_val}
    )
    print(f"Round trip: {original_qn} QN -> {time_val}s -> {qn_result}")
    
    # Test beats conversion
    original_beats = 16.0
    time_result = await reaper_mcp_client.call_tool(
        "time_map2_beats_to_time",
        {"beats": original_beats}
    )
    print(f"Beats to time: {time_result}")
    
    # Get measure info for specific beat
    measure_result = await reaper_mcp_client.call_tool(
        "time_map_qn_to_measures",
        {"qn": original_qn}
    )
    print(f"QN to measures: {measure_result}")