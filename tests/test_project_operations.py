import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_project_info(reaper_mcp_client):
    """Test project information retrieval"""
    # Get project name
    result = await reaper_mcp_client.call_tool(
        "get_project_name",
        {}
    )
    print(f"Get project name result: {result}")
    assert "project" in result.content[0].text.lower()
    
    # Get project path
    result = await reaper_mcp_client.call_tool(
        "get_project_path",
        {}
    )
    print(f"Get project path result: {result}")
    assert "path" in result.content[0].text.lower() or "/" in result.content[0].text

@pytest.mark.asyncio
async def test_cursor_operations(reaper_mcp_client):
    """Test edit cursor operations"""
    # Set edit cursor position
    result = await reaper_mcp_client.call_tool(
        "set_edit_cursor_position",
        {"time": 10.0}
    )
    print(f"Set cursor position result: {result}")
    assert "success" in result.content[0].text.lower() or "10.0" in result.content[0].text
    
    # Get cursor position
    result = await reaper_mcp_client.call_tool(
        "get_cursor_position",
        {}
    )
    print(f"Get cursor position result: {result}")
    assert "10.0" in result.content[0].text

@pytest.mark.asyncio
async def test_undo_operations(reaper_mcp_client):
    """Test undo block operations"""
    # Begin undo block
    result = await reaper_mcp_client.call_tool(
        "undo_begin_block",
        {}
    )
    print(f"Begin undo block result: {result}")
    assert "success" in result.content[0].text.lower() or "started" in result.content[0].text.lower()
    
    # Create a track (as an undoable action)
    await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": 0, "use_defaults": True}
    )
    
    # End undo block
    result = await reaper_mcp_client.call_tool(
        "undo_end_block",
        {"description": "Test Undo Block"}
    )
    print(f"End undo block result: {result}")
    assert "success" in result.content[0].text.lower() or "ended" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_update_operations(reaper_mcp_client):
    """Test arrange and timeline update operations"""
    # Update arrange
    result = await reaper_mcp_client.call_tool(
        "update_arrange",
        {}
    )
    print(f"Update arrange result: {result}")
    assert "success" in result.content[0].text.lower() or "updated" in result.content[0].text.lower()
    
    # Update timeline
    result = await reaper_mcp_client.call_tool(
        "update_timeline",
        {}
    )
    print(f"Update timeline result: {result}")
    assert "success" in result.content[0].text.lower() or "updated" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_execute_action(reaper_mcp_client):
    """Test executing REAPER actions"""
    # Execute action (40001 = insert new track)
    result = await reaper_mcp_client.call_tool(
        "execute_action",
        {"command_id": 40001}
    )
    print(f"Execute action result: {result}")
    assert "success" in result.content[0].text.lower() or "executed" in result.content[0].text.lower()