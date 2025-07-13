"""Test GUI and console operations"""
import pytest
import pytest_asyncio
import asyncio


@pytest.mark.asyncio
async def test_console_operations(reaper_mcp_client):
    """Test console message operations"""
    # Clear console first
    result = await reaper_mcp_client.call_tool(
        "clear_console",
        {}
    )
    assert "Cleared console" in result.content[0].text
    
    # Show console message
    result = await reaper_mcp_client.call_tool(
        "show_console_msg",
        {"message": "Test message from MCP\n"}
    )
    assert "Displayed message in console" in result.content[0].text
    
    # Show multiple messages
    for i in range(3):
        result = await reaper_mcp_client.call_tool(
            "show_console_msg",
            {"message": f"Line {i+1}\n"}
        )
        assert "Displayed message in console" in result.content[0].text


@pytest.mark.asyncio
async def test_window_operations(reaper_mcp_client):
    """Test window-related operations"""
    # Get main window handle
    result = await reaper_mcp_client.call_tool(
        "get_main_hwnd",
        {}
    )
    assert "Main window handle:" in result.content[0].text
    
    # Get mouse position
    result = await reaper_mcp_client.call_tool(
        "get_mouse_position",
        {}
    )
    assert "Mouse position:" in result.content[0].text
    assert "x=" in result.content[0].text
    assert "y=" in result.content[0].text
    
    # Get cursor context
    result = await reaper_mcp_client.call_tool(
        "get_cursor_context",
        {}
    )
    assert "Cursor context:" in result.content[0].text


@pytest.mark.asyncio
async def test_message_box(reaper_mcp_client):
    """Test message box operations"""
    # Note: In automation context, message boxes may not actually display
    result = await reaper_mcp_client.call_tool(
        "show_message_box",
        {
            "message": "Test message",
            "title": "MCP Test",
            "type": 0  # OK button only
        }
    )
    assert "Message box result:" in result.content[0].text


@pytest.mark.asyncio
async def test_dock_window(reaper_mcp_client):
    """Test dock window operations"""
    # Note: This requires actual window handle, so will return placeholder
    result = await reaper_mcp_client.call_tool(
        "dock_window_add",
        {
            "hwnd": "test_hwnd",
            "name": "Test Dock",
            "pos": 0,
            "allow_show": True
        }
    )
    assert "dock window" in result.content[0].text.lower() or "dock_window_not_available" in result.content[0].text