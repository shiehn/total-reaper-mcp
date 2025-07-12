import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_track_send_creation(reaper_mcp_client):
    """Test creating sends between tracks"""
    # Create source and destination tracks
    for i in range(2):
        result = await reaper_mcp_client.call_tool(
            "insert_track",
            {"index": i, "use_defaults": True}
        )
        assert "success" in result.content[0].text.lower()
    
    # Name the tracks for clarity
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 0, "name": "Source Track"}
    )
    await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 1, "name": "Destination Track"}
    )
    
    # Create send from track 0 to track 1
    result = await reaper_mcp_client.call_tool(
        "create_track_send",
        {"source_track_index": 0, "dest_track_index": 1}
    )
    print(f"Create send result: {result}")
    assert "created send" in result.content[0].text.lower()
    assert "send index" in result.content[0].text.lower()
    
    # Check number of sends on source track
    result = await reaper_mcp_client.call_tool(
        "get_track_num_sends",
        {"track_index": 0}
    )
    print(f"Number of sends: {result}")
    assert "1 sends" in result.content[0].text or "1 send" in result.content[0].text

@pytest.mark.asyncio
async def test_track_send_volume(reaper_mcp_client):
    """Test setting and getting send volume"""
    # Create tracks and send
    for i in range(2):
        await reaper_mcp_client.call_tool(
            "insert_track",
            {"index": i, "use_defaults": True}
        )
    
    await reaper_mcp_client.call_tool(
        "create_track_send",
        {"source_track_index": 0, "dest_track_index": 1}
    )
    
    # Set send volume to 0.5
    result = await reaper_mcp_client.call_tool(
        "set_track_send_volume",
        {"track_index": 0, "send_index": 0, "volume": 0.5}
    )
    print(f"Set send volume result: {result}")
    assert "set send" in result.content[0].text.lower()
    assert "0.500" in result.content[0].text
    
    # Get send info
    result = await reaper_mcp_client.call_tool(
        "get_track_send_info",
        {"track_index": 0, "send_index": 0}
    )
    print(f"Get send info result: {result}")
    assert "volume=0.5" in result.content[0].text
    
    # Set to different volume
    await reaper_mcp_client.call_tool(
        "set_track_send_volume",
        {"track_index": 0, "send_index": 0, "volume": 0.75}
    )
    
    # Verify new volume
    result = await reaper_mcp_client.call_tool(
        "get_track_send_info",
        {"track_index": 0, "send_index": 0}
    )
    assert "volume=0.75" in result.content[0].text

@pytest.mark.asyncio
async def test_multiple_sends(reaper_mcp_client):
    """Test creating multiple sends from one track"""
    # Create one source and three destination tracks
    for i in range(4):
        await reaper_mcp_client.call_tool(
            "insert_track",
            {"index": i, "use_defaults": True}
        )
    
    # Create sends from track 0 to tracks 1, 2, and 3
    for dest in range(1, 4):
        result = await reaper_mcp_client.call_tool(
            "create_track_send",
            {"source_track_index": 0, "dest_track_index": dest}
        )
        print(f"Create send to track {dest}: {result}")
        assert "created send" in result.content[0].text.lower()
    
    # Check number of sends
    result = await reaper_mcp_client.call_tool(
        "get_track_num_sends",
        {"track_index": 0}
    )
    assert "3 sends" in result.content[0].text
    
    # Set different volumes for each send
    volumes = [0.3, 0.5, 0.7]
    for i, vol in enumerate(volumes):
        await reaper_mcp_client.call_tool(
            "set_track_send_volume",
            {"track_index": 0, "send_index": i, "volume": vol}
        )

@pytest.mark.asyncio
async def test_remove_send(reaper_mcp_client):
    """Test removing sends"""
    # Create tracks and multiple sends
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "insert_track",
            {"index": i, "use_defaults": True}
        )
    
    # Create two sends from track 0
    await reaper_mcp_client.call_tool(
        "create_track_send",
        {"source_track_index": 0, "dest_track_index": 1}
    )
    await reaper_mcp_client.call_tool(
        "create_track_send",
        {"source_track_index": 0, "dest_track_index": 2}
    )
    
    # Verify 2 sends
    result = await reaper_mcp_client.call_tool(
        "get_track_num_sends",
        {"track_index": 0}
    )
    assert "2 sends" in result.content[0].text
    
    # Remove first send (index 0)
    result = await reaper_mcp_client.call_tool(
        "remove_track_send",
        {"track_index": 0, "send_index": 0}
    )
    print(f"Remove send result: {result}")
    assert "removed send" in result.content[0].text.lower()
    
    # Verify 1 send remaining
    result = await reaper_mcp_client.call_tool(
        "get_track_num_sends",
        {"track_index": 0}
    )
    assert "1 sends" in result.content[0].text or "1 send" in result.content[0].text

@pytest.mark.asyncio
async def test_send_routing_chain(reaper_mcp_client):
    """Test creating a routing chain: Track 0 -> Track 1 -> Track 2"""
    # Create three tracks
    for i in range(3):
        await reaper_mcp_client.call_tool(
            "insert_track",
            {"index": i, "use_defaults": True}
        )
        await reaper_mcp_client.call_tool(
            "set_track_name",
            {"track_index": i, "name": f"Track {i}"}
        )
    
    # Create send chain
    result = await reaper_mcp_client.call_tool(
        "create_track_send",
        {"source_track_index": 0, "dest_track_index": 1}
    )
    assert "created send" in result.content[0].text.lower()
    
    result = await reaper_mcp_client.call_tool(
        "create_track_send",
        {"source_track_index": 1, "dest_track_index": 2}
    )
    assert "created send" in result.content[0].text.lower()
    
    # Verify sends
    for track in [0, 1]:
        result = await reaper_mcp_client.call_tool(
            "get_track_num_sends",
            {"track_index": track}
        )
        assert "1 sends" in result.content[0].text or "1 send" in result.content[0].text

@pytest.mark.asyncio
async def test_send_error_handling(reaper_mcp_client):
    """Test error handling for send operations"""
    # Try to create send with non-existent tracks
    result = await reaper_mcp_client.call_tool(
        "create_track_send",
        {"source_track_index": 999, "dest_track_index": 0}
    )
    assert "failed" in result.content[0].text.lower()
    
    # Create one track
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # Try to create send to non-existent destination
    result = await reaper_mcp_client.call_tool(
        "create_track_send",
        {"source_track_index": 0, "dest_track_index": 999}
    )
    assert "failed" in result.content[0].text.lower()
    
    # Try to get send info for non-existent send
    result = await reaper_mcp_client.call_tool(
        "get_track_send_info",
        {"track_index": 0, "send_index": 999}
    )
    assert "failed" in result.content[0].text.lower() or "error" in result.content[0].text.lower()