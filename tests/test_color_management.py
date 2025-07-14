import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_color_utilities(reaper_mcp_client):
    """Test color utility functions"""
    # Test RGB to native conversion
    result = await reaper_mcp_client.call_tool(
        "color_to_native",
        {"r": 255, "g": 128, "b": 64}
    )
    print(f"RGB to native: {result}")
    assert "Native color" in result.content[0].text
    
    # Extract native color value from result
    import re
    match = re.search(r"Native color (\d+)", result.content[0].text)
    assert match
    native_color = int(match.group(1))
    
    # Test native to RGB conversion
    result = await reaper_mcp_client.call_tool(
        "color_from_native",
        {"native_color": native_color}
    )
    print(f"Native to RGB: {result}")
    assert "RGB" in result.content[0].text
    
    # Test gradient color
    result = await reaper_mcp_client.call_tool(
        "gradient_color",
        {"start_color": 0xFF0000, "end_color": 0x0000FF, "position": 0.5}
    )
    print(f"Gradient color: {result}")
    assert "Gradient color" in result.content[0].text
    
    # Test theme color
    result = await reaper_mcp_client.call_tool(
        "get_theme_color",
        {"theme_color_name": "col_main_bg", "shade": 0}
    )
    print(f"Theme color: {result}")
    assert "Theme color" in result.content[0].text


@pytest.mark.asyncio
async def test_track_color_operations(reaper_mcp_client):
    """Test track color management"""
    # Create tracks
    for i in range(3):
        await reaper_mcp_client.call_tool("insert_track", {"index": i, "use_defaults": True})
        await reaper_mcp_client.call_tool("set_track_name", {"track_index": i, "name": f"Track {i+1}"})
    
    # Get initial track color
    result = await reaper_mcp_client.call_tool(
        "get_track_color",
        {"track_index": 0}
    )
    print(f"Initial track color: {result}")
    assert "Track 0" in result.content[0].text
    
    # Set track color
    result = await reaper_mcp_client.call_tool(
        "set_track_color",
        {"track_index": 0, "color": 0xFF0000}
    )
    print(f"Set track color: {result}")
    assert "Set track 0 color" in result.content[0].text
    
    # Set track color using RGB
    result = await reaper_mcp_client.call_tool(
        "set_track_color_rgb",
        {"track_index": 1, "r": 0, "g": 255, "b": 0}
    )
    print(f"Set track color RGB: {result}")
    assert "Set track 1 color" in result.content[0].text
    
    # Get track color after setting
    result = await reaper_mcp_client.call_tool(
        "get_track_color",
        {"track_index": 0}
    )
    print(f"Track color after set: {result}")
    assert "RGB" in result.content[0].text
    
    # Remove track color
    result = await reaper_mcp_client.call_tool(
        "set_track_color",
        {"track_index": 0, "color": 0}
    )
    print(f"Remove track color: {result}")
    assert "Removed custom color" in result.content[0].text


@pytest.mark.asyncio
async def test_track_color_gradient(reaper_mcp_client):
    """Test gradient coloring of tracks"""
    # Create multiple tracks
    for i in range(5):
        await reaper_mcp_client.call_tool("insert_track", {"index": i, "use_defaults": True})
        await reaper_mcp_client.call_tool("set_track_name", {"track_index": i, "name": f"Gradient {i+1}"})
    
    # Apply gradient coloring
    result = await reaper_mcp_client.call_tool(
        "color_tracks_gradient",
        {
            "start_track": 0,
            "end_track": 4,
            "start_color": 0xFF0000,  # Red
            "end_color": 0x0000FF     # Blue
        }
    )
    print(f"Gradient coloring: {result}")
    assert "Applied gradient coloring" in result.content[0].text
    
    # Check middle track has intermediate color
    result = await reaper_mcp_client.call_tool(
        "get_track_color",
        {"track_index": 2}
    )
    print(f"Middle track color: {result}")
    assert "Track 2 color:" in result.content[0].text


@pytest.mark.asyncio
async def test_selected_tracks_coloring(reaper_mcp_client):
    """Test coloring selected tracks"""
    # Create tracks
    for i in range(3):
        await reaper_mcp_client.call_tool("insert_track", {"index": i, "use_defaults": True})
    
    # Select tracks
    await reaper_mcp_client.call_tool("set_track_selected", {"track_index": 0, "selected": True})
    await reaper_mcp_client.call_tool("set_track_selected", {"track_index": 2, "selected": True})
    
    # Color selected tracks
    result = await reaper_mcp_client.call_tool(
        "color_selected_tracks",
        {"color": 0x00FF00}
    )
    print(f"Color selected: {result}")
    assert "Set color for" in result.content[0].text and "selected tracks" in result.content[0].text
    
    # Get track state color
    result = await reaper_mcp_client.call_tool(
        "get_track_state_color",
        {"track_index": 0, "auto_mode": True}
    )
    print(f"Track state color: {result}")
    assert "Track 0 color:" in result.content[0].text


@pytest.mark.asyncio
async def test_item_color_operations(reaper_mcp_client):
    """Test item color management"""
    # Create track and items
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "add_media_item_to_track",
            {"track_index": 0, "start_time": i * 2.0, "length": 1.5}
        )
    
    # Get initial item color
    result = await reaper_mcp_client.call_tool(
        "get_item_color",
        {"item_index": 0}
    )
    print(f"Initial item color: {result}")
    assert "Item 0" in result.content[0].text
    
    # Set item color
    result = await reaper_mcp_client.call_tool(
        "set_item_color",
        {"item_index": 0, "color": 0xFF00FF}
    )
    print(f"Set item color: {result}")
    assert "Set item 0 color" in result.content[0].text
    
    # Set item color using RGB
    result = await reaper_mcp_client.call_tool(
        "set_item_color_rgb",
        {"item_index": 1, "r": 255, "g": 255, "b": 0}
    )
    print(f"Set item color RGB: {result}")
    assert "Set item 1 color" in result.content[0].text
    
    # Get item color after setting
    result = await reaper_mcp_client.call_tool(
        "get_item_color",
        {"item_index": 0}
    )
    print(f"Item color after set: {result}")
    assert "RGB" in result.content[0].text


@pytest.mark.asyncio
async def test_selected_items_coloring(reaper_mcp_client):
    """Test coloring selected items"""
    # Create track and items
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    for i in range(4):
        await reaper_mcp_client.call_tool(
            "add_media_item_to_track",
            {"track_index": 0, "start_time": i * 1.0, "length": 0.8}
        )
    
    # Select items
    await reaper_mcp_client.call_tool("set_media_item_selected", {"item_index": 0, "selected": True})
    await reaper_mcp_client.call_tool("set_media_item_selected", {"item_index": 2, "selected": True})
    await reaper_mcp_client.call_tool("set_media_item_selected", {"item_index": 3, "selected": True})
    
    # Color selected items
    result = await reaper_mcp_client.call_tool(
        "color_selected_items",
        {"color": 0x00FFFF}
    )
    print(f"Color selected items: {result}")
    assert "Set color for" in result.content[0].text and "selected items" in result.content[0].text


@pytest.mark.asyncio
async def test_take_color_operations(reaper_mcp_client):
    """Test take color management"""
    # Create track and item with takes
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": 0, "start_time": 0.0, "length": 4.0}
    )
    
    # Add multiple takes
    for i in range(3):
        await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": 0})
    
    # Get take color
    result = await reaper_mcp_client.call_tool(
        "get_take_color",
        {"item_index": 0, "take_index": 0}
    )
    print(f"Initial take color: {result}")
    assert "Take 0" in result.content[0].text
    
    # Set take color
    result = await reaper_mcp_client.call_tool(
        "set_take_color",
        {"item_index": 0, "take_index": 0, "color": 0xFF8800}
    )
    print(f"Set take color: {result}")
    assert "Set take 0 color" in result.content[0].text


@pytest.mark.asyncio
async def test_color_items_by_type(reaper_mcp_client):
    """Test coloring items by source type"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Add audio items
    for i in range(2):
        await reaper_mcp_client.call_tool(
            "add_media_item_to_track",
            {"track_index": 0, "start_time": i * 2.0, "length": 1.5}
        )
        await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": i})
    
    # Add MIDI items
    for i in range(2):
        item_idx = i + 2
        await reaper_mcp_client.call_tool(
            "add_media_item_to_track",
            {"track_index": 0, "start_time": (i + 2) * 2.0, "length": 1.5}
        )
        await reaper_mcp_client.call_tool("add_take_to_item", {"item_index": item_idx})
        # Add MIDI note to make it a MIDI item
        await reaper_mcp_client.call_tool(
            "midi_insert_evt",
            {
                "item_index": item_idx,
                "take_index": 0,
                "ppq_pos": 0,
                "event_type": "note_on",
                "data1": 60,
                "data2": 100
            }
        )
    
    # Color items by source type
    result = await reaper_mcp_client.call_tool(
        "color_items_by_source_type",
        {"track_index": 0, "audio_color": 0x0000FF, "midi_color": 0xFF0000}
    )
    print(f"Color by type: {result}")
    assert "audio items" in result.content[0].text and "MIDI items" in result.content[0].text


@pytest.mark.asyncio
async def test_inherit_track_color(reaper_mcp_client):
    """Test inheriting track color to items"""
    # Create track with color
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("set_track_color", {"track_index": 0, "color": 0x00FF00})
    
    # Add items
    for i in range(4):
        await reaper_mcp_client.call_tool(
            "add_media_item_to_track",
            {"track_index": 0, "start_time": i * 1.0, "length": 0.8}
        )
    
    # Inherit track color to items
    result = await reaper_mcp_client.call_tool(
        "inherit_track_color_to_items",
        {"track_index": 0}
    )
    print(f"Inherit color: {result}")
    assert "Applied track color to" in result.content[0].text


@pytest.mark.asyncio
async def test_marker_region_colors(reaper_mcp_client):
    """Test marker and region color management"""
    # Add markers and regions
    await reaper_mcp_client.call_tool(
        "add_project_marker",
        {"position": 2.0, "name": "Marker 1", "color": 0}
    )
    await reaper_mcp_client.call_tool(
        "add_project_marker",
        {"position": 4.0, "name": "Marker 2", "color": 0}
    )
    await reaper_mcp_client.call_tool(
        "add_project_marker",
        {"position": 6.0, "name": "Region 1", "color": 0, "is_region": True, "region_end": 8.0}
    )
    await reaper_mcp_client.call_tool(
        "add_project_marker",
        {"position": 10.0, "name": "Region 2", "color": 0, "is_region": True, "region_end": 12.0}
    )
    
    # Get marker color
    result = await reaper_mcp_client.call_tool(
        "get_marker_region_color",
        {"index": 0}
    )
    print(f"Initial marker color: {result}")
    assert "has no custom color" in result.content[0].text or "color:" in result.content[0].text
    
    # Set marker color
    result = await reaper_mcp_client.call_tool(
        "set_marker_region_color",
        {"index": 0, "color": 0xFF0000}
    )
    print(f"Set marker color: {result}")
    assert "Set marker" in result.content[0].text or "Set region" in result.content[0].text
    
    # Color all markers
    result = await reaper_mcp_client.call_tool(
        "color_all_markers",
        {"color": 0x00FF00}
    )
    print(f"Color all markers: {result}")
    assert "Set color for" in result.content[0].text and "markers" in result.content[0].text
    
    # Color all regions
    result = await reaper_mcp_client.call_tool(
        "color_all_regions",
        {"color": 0x0000FF}
    )
    print(f"Color all regions: {result}")
    assert "Set color for" in result.content[0].text and "regions" in result.content[0].text


@pytest.mark.asyncio
async def test_color_regions_by_pattern(reaper_mcp_client):
    """Test coloring regions by name pattern"""
    # Add regions with different names
    regions = [
        ("Verse 1", 0.0, 4.0),
        ("Chorus", 4.0, 8.0),
        ("Verse 2", 8.0, 12.0),
        ("Bridge", 12.0, 16.0),
        ("Chorus", 16.0, 20.0)
    ]
    
    for name, start, end in regions:
        await reaper_mcp_client.call_tool(
            "add_project_marker",
            {"position": start, "name": name, "color": 0, "is_region": True, "region_end": end}
        )
    
    # Color regions matching pattern
    result = await reaper_mcp_client.call_tool(
        "color_regions_by_name_pattern",
        {"pattern": "Verse", "color": 0xFF00FF}
    )
    print(f"Color by pattern: {result}")
    assert "Set color for" in result.content[0].text and "regions matching pattern" in result.content[0].text
    
    # Auto-generate region colors
    result = await reaper_mcp_client.call_tool(
        "generate_region_colors_by_index",
        {}
    )
    print(f"Auto-color regions: {result}")
    assert "Auto-colored" in result.content[0].text and "regions" in result.content[0].text


@pytest.mark.asyncio
async def test_color_workflow(reaper_mcp_client):
    """Test a complete color management workflow"""
    # Create a project with tracks, items, and regions
    track_names = ["Drums", "Bass", "Guitar", "Vocals", "Effects"]
    track_colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF]
    
    # Create and color tracks
    for i, (name, color) in enumerate(zip(track_names, track_colors)):
        await reaper_mcp_client.call_tool("insert_track", {"index": i, "use_defaults": True})
        await reaper_mcp_client.call_tool("set_track_name", {"track_index": i, "name": name})
        await reaper_mcp_client.call_tool("set_track_color", {"track_index": i, "color": color})
    
    # Add items to each track
    for track_idx in range(len(track_names)):
        for item_idx in range(3):
            await reaper_mcp_client.call_tool(
                "add_media_item_to_track",
                {"track_index": track_idx, "start_time": item_idx * 2.0, "length": 1.8}
            )
    
    # Inherit track colors to items
    for track_idx in range(len(track_names)):
        await reaper_mcp_client.call_tool(
            "inherit_track_color_to_items",
            {"track_index": track_idx}
        )
    
    # Add colored regions for song structure
    structure = [
        ("Intro", 0.0, 2.0, 0x808080),
        ("Verse 1", 2.0, 6.0, 0x0080FF),
        ("Chorus", 6.0, 10.0, 0xFF8000),
        ("Verse 2", 10.0, 14.0, 0x0080FF),
        ("Chorus", 14.0, 18.0, 0xFF8000),
        ("Outro", 18.0, 20.0, 0x808080)
    ]
    
    for name, start, end, color in structure:
        await reaper_mcp_client.call_tool(
            "add_project_marker",
            {"position": start, "name": name, "color": color, "is_region": True, "region_end": end}
        )
    
    print("Color workflow completed successfully!")