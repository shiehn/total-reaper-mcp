"""Test action management operations"""
import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_command_lookup(reaper_mcp_client):
    """Test command lookup operations"""
    # Look up a known command name
    result = await reaper_mcp_client.call_tool(
        "named_command_lookup",
        {"command_name": "_SWS_ABOUT"}
    )
    assert result is not None
    # Should either find it or not (depending on whether SWS is installed)
    assert "has ID:" in result.content[0].text or "not found" in result.content[0].text

@pytest.mark.asyncio
async def test_toggle_command_state(reaper_mcp_client):
    """Test getting toggle command state"""
    # Check state of "Toggle metronome" (command 40364)
    result = await reaper_mcp_client.call_tool(
        "get_toggle_command_state_ex",
        {
            "section_id": 0,  # Main section
            "command_id": 40364  # Toggle metronome
        }
    )
    assert result is not None
    assert "Toggle command" in result.content[0].text
    assert any(state in result.content[0].text for state in ["ON", "OFF", "Not found"])

@pytest.mark.asyncio
async def test_action_shortcuts(reaper_mcp_client):
    """Test action shortcut operations"""
    # Count shortcuts for "Play" command (1007)
    result = await reaper_mcp_client.call_tool(
        "count_action_shortcuts",
        {
            "section": 0,  # Main section
            "command_id": 1007  # Play
        }
    )
    assert result is not None
    assert "shortcuts" in result.content[0].text
    
    # Try to get first shortcut description (if any exist)
    result = await reaper_mcp_client.call_tool(
        "get_action_shortcut_desc",
        {
            "section": 0,
            "command_id": 1007,
            "shortcut_index": 0
        }
    )
    assert result is not None
    assert "Shortcut" in result.content[0].text or "No shortcut found" in result.content[0].text

@pytest.mark.asyncio 
async def test_toolbar_refresh(reaper_mcp_client):
    """Test toolbar refresh"""
    # Refresh toolbar for a command
    result = await reaper_mcp_client.call_tool(
        "refresh_toolbar",
        {"command_id": 0}  # 0 = refresh all
    )
    assert result is not None
    assert "Refreshed toolbar" in result.content[0].text

@pytest.mark.asyncio
async def test_section_lookup(reaper_mcp_client):
    """Test section ID lookup"""
    # Get section from a unique ID
    result = await reaper_mcp_client.call_tool(
        "section_from_unique_id",
        {"unique_id": 1007}  # Play command
    )
    assert result is not None
    assert "belongs to:" in result.content[0].text
    # Section -1 is valid and means it's not in a recognized section
    assert "Section -1" in result.content[0].text or "Main" in result.content[0].text