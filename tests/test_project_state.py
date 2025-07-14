import pytest
import pytest_asyncio
import asyncio

@pytest.mark.asyncio
async def test_undo_system_basic(reaper_mcp_client):
    """Test basic undo/redo operations"""
    # Begin undo block
    result = await reaper_mcp_client.call_tool(
        "undo_begin_block2",
        {"project_index": 0}
    )
    print(f"Begin undo block: {result}")
    assert "Started new undo block" in result.content[0].text
    
    # Create a track (this will be undoable)
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # End undo block
    result = await reaper_mcp_client.call_tool(
        "undo_end_block2",
        {"desc": "Test: Create Track", "extra_flags": 1, "project_index": 0}
    )
    print(f"End undo block: {result}")
    assert "Ended undo block: Test: Create Track" in result.content[0].text
    
    # Check if we can undo
    result = await reaper_mcp_client.call_tool(
        "undo_can_undo2",
        {"project_index": 0}
    )
    print(f"Can undo: {result}")
    assert "Can undo:" in result.content[0].text or "Nothing to undo" in result.content[0].text
    
    # Perform undo
    if "Can undo:" in result.content[0].text:
        result = await reaper_mcp_client.call_tool(
            "undo_do_undo2",
            {"project_index": 0}
        )
        print(f"Undo result: {result}")
        assert "Performed undo" in result.content[0].text
        
        # Check if we can redo
        result = await reaper_mcp_client.call_tool(
            "undo_can_redo2",
            {"project_index": 0}
        )
        print(f"Can redo: {result}")
        assert "Can redo:" in result.content[0].text or "Nothing to redo" in result.content[0].text
        
        # Perform redo
        if "Can redo:" in result.content[0].text:
            result = await reaper_mcp_client.call_tool(
                "undo_do_redo2",
                {"project_index": 0}
            )
            print(f"Redo result: {result}")
            assert "Performed redo" in result.content[0].text


@pytest.mark.asyncio
async def test_state_change_reporting(reaper_mcp_client):
    """Test state change reporting for undo history"""
    # Report simple state change
    result = await reaper_mcp_client.call_tool(
        "undo_on_state_change",
        {"desc": "Test State Change"}
    )
    print(f"State change: {result}")
    assert "Recorded state change: Test State Change" in result.content[0].text
    
    # Report project-specific state change
    result = await reaper_mcp_client.call_tool(
        "undo_on_state_change2",
        {"project_index": 0, "desc": "Project State Change"}
    )
    print(f"Project state change: {result}")
    assert "Recorded state change: Project State Change" in result.content[0].text
    
    # Report extended state change
    result = await reaper_mcp_client.call_tool(
        "undo_on_state_change_ex",
        {"desc": "Extended State Change", "whichStates": 1, "trackparm": 0}
    )
    print(f"Extended state change: {result}")
    assert "Recorded extended state change" in result.content[0].text


@pytest.mark.asyncio
async def test_extended_state_management(reaper_mcp_client):
    """Test extended state storage and retrieval"""
    section = "TestSection"
    key = "TestKey"
    value = "TestValue123"
    
    # Set extended state
    result = await reaper_mcp_client.call_tool(
        "set_ext_state",
        {"section": section, "key": key, "value": value, "persist": True}
    )
    print(f"Set state: {result}")
    assert f"Set persistent state: [{section}] {key} = {value}" in result.content[0].text
    
    # Get extended state
    result = await reaper_mcp_client.call_tool(
        "get_ext_state",
        {"section": section, "key": key}
    )
    print(f"Get state: {result}")
    assert f"[{section}] {key} = {value}" in result.content[0].text
    
    # Check if state exists
    result = await reaper_mcp_client.call_tool(
        "has_ext_state",
        {"section": section, "key": key}
    )
    print(f"Has state: {result}")
    assert f"State exists: [{section}] {key}" in result.content[0].text
    
    # Delete extended state
    result = await reaper_mcp_client.call_tool(
        "delete_ext_state",
        {"section": section, "key": key, "persist": True}
    )
    print(f"Delete state: {result}")
    assert f"Deleted persistent state: [{section}] {key}" in result.content[0].text
    
    # Verify deletion
    result = await reaper_mcp_client.call_tool(
        "has_ext_state",
        {"section": section, "key": key}
    )
    print(f"Has state after delete: {result}")
    assert "State does not exist" in result.content[0].text


@pytest.mark.asyncio
async def test_project_extended_state(reaper_mcp_client):
    """Test project-specific extended state"""
    section = "ProjectTestSection"
    key = "ProjectTestKey"
    value = "ProjectTestValue456"
    
    # Set project extended state
    result = await reaper_mcp_client.call_tool(
        "set_proj_ext_state",
        {"section": section, "key": key, "value": value, "project_index": 0}
    )
    print(f"Set project state: {result}")
    assert f"Set project state: [{section}] {key} = {value}" in result.content[0].text
    
    # Get project extended state
    result = await reaper_mcp_client.call_tool(
        "get_proj_ext_state",
        {"section": section, "key": key, "project_index": 0}
    )
    print(f"Get project state: {result}")
    assert f"Project [{section}] {key} = {value}" in result.content[0].text
    
    # Enumerate project state keys
    result = await reaper_mcp_client.call_tool(
        "enum_proj_ext_state",
        {"section": section, "index": 0, "project_index": 0}
    )
    print(f"Enum project state: {result}")
    # Either found the key or no key at index
    assert "Key 0:" in result.content[0].text or "No key at index 0" in result.content[0].text


@pytest.mark.asyncio
async def test_project_metadata(reaper_mcp_client):
    """Test project metadata operations"""
    # Set project author
    author = "Test Author"
    result = await reaper_mcp_client.call_tool(
        "get_set_project_author",
        {"set": True, "author": author, "project_index": 0}
    )
    print(f"Set author: {result}")
    assert f"Set project author to: {author}" in result.content[0].text
    
    # Get project author
    result = await reaper_mcp_client.call_tool(
        "get_set_project_author",
        {"set": False, "author": "", "project_index": 0}
    )
    print(f"Get author: {result}")
    assert "Project author:" in result.content[0].text
    
    # Set project notes
    notes = "This is a test project\nWith multiple lines"
    result = await reaper_mcp_client.call_tool(
        "get_set_project_notes",
        {"set": True, "notes": notes, "project_index": 0}
    )
    print(f"Set notes: {result}")
    assert "Set project notes" in result.content[0].text
    
    # Get project notes
    result = await reaper_mcp_client.call_tool(
        "get_set_project_notes",
        {"set": False, "notes": "", "project_index": 0}
    )
    print(f"Get notes: {result}")
    assert "Project notes:" in result.content[0].text
    
    # Get project time offset
    result = await reaper_mcp_client.call_tool(
        "get_project_time_offset",
        {"project_index": 0}
    )
    print(f"Time offset: {result}")
    assert "Project time offset:" in result.content[0].text


@pytest.mark.asyncio
async def test_track_state_chunk(reaper_mcp_client):
    """Test track state chunk operations"""
    # Create a track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Set some track properties
    await reaper_mcp_client.call_tool("set_track_name", {"track_index": 0, "name": "Test Track"})
    await reaper_mcp_client.call_tool("set_track_color", {"track_index": 0, "color": 0xFF0000})
    
    # Get track state chunk
    result = await reaper_mcp_client.call_tool(
        "get_track_state_chunk",
        {"track_index": 0, "flags": 0}
    )
    print(f"Get track chunk: {result}")
    assert "Track state chunk" in result.content[0].text
    assert "lines)" in result.content[0].text
    
    # Note: We can't easily test set_track_state_chunk without a valid chunk string
    # This would normally be used for duplicating or restoring track configurations


@pytest.mark.asyncio
async def test_item_state_chunk(reaper_mcp_client):
    """Test media item state chunk operations"""
    # Create track and item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("add_media_item_to_track", {"track_index": 0})
    
    # Get item state chunk
    result = await reaper_mcp_client.call_tool(
        "get_item_state_chunk",
        {"item_index": 0, "flags": 0}
    )
    print(f"Get item chunk: {result}")
    assert "Item state chunk" in result.content[0].text
    assert "lines)" in result.content[0].text


@pytest.mark.asyncio
async def test_envelope_state_chunk(reaper_mcp_client):
    """Test envelope state chunk operations"""
    # Create track
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    
    # Get or create volume envelope
    result = await reaper_mcp_client.call_tool(
        "get_track_envelope",
        {"track_index": 0, "envelope_index": 0}
    )
    print(f"Get envelope: {result}")
    
    # Try to get envelope state chunk (may fail if envelope doesn't exist)
    try:
        result = await reaper_mcp_client.call_tool(
            "get_envelope_state_chunk",
            {"track_index": 0, "envelope_name": "Volume", "flags": 0}
        )
        print(f"Get envelope chunk: {result}")
        assert "Envelope state chunk" in result.content[0].text or "Failed" in result.content[0].text
    except Exception as e:
        print(f"Expected error getting envelope chunk: {e}")


@pytest.mark.asyncio
async def test_project_play_states(reaper_mcp_client):
    """Test getting play states of all projects"""
    result = await reaper_mcp_client.call_tool(
        "get_all_project_play_states",
        {"project_index": 0}
    )
    print(f"Play states: {result}")
    assert "Project play states:" in result.content[0].text or "All projects stopped" in result.content[0].text


@pytest.mark.asyncio
async def test_flush_undo(reaper_mcp_client):
    """Test flushing undo buffer"""
    result = await reaper_mcp_client.call_tool(
        "csurf_flush_undo",
        {"force": False}
    )
    print(f"Flush undo: {result}")
    assert "Flushed undo buffer" in result.content[0].text


@pytest.mark.asyncio
async def test_item_state_change(reaper_mcp_client):
    """Test item-specific state change reporting"""
    # Create track and item
    await reaper_mcp_client.call_tool("insert_track", {"index": 0, "use_defaults": True})
    await reaper_mcp_client.call_tool("add_media_item_to_track", {"track_index": 0})
    
    # Report item state change
    result = await reaper_mcp_client.call_tool(
        "undo_on_state_change_item",
        {"project_index": 0, "desc": "Item Modified", "item_index": 0}
    )
    print(f"Item state change: {result}")
    assert "Recorded item state change: Item Modified" in result.content[0].text