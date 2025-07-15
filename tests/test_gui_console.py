"""Test GUI and console operations"""
import pytest
import pytest_asyncio
import asyncio

def assert_tools_available(available_tools, required_tools):
    """Assert that all required tools are available, failing with clear message if not"""
    for tool in required_tools:
        assert tool in available_tools, f"MISSING IMPLEMENTATION: Tool '{tool}' is not implemented in the server but is required for GUI/console functionality"


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
    assert "Showed message" in result.content[0].text
    
    # Show multiple messages
    for i in range(3):
        result = await reaper_mcp_client.call_tool(
            "show_console_msg",
            {"message": f"Line {i+1}\n"}
        )
        assert "Showed message" in result.content[0].text


@pytest.mark.asyncio
async def test_window_operations(reaper_mcp_client):
    """Test window-related operations"""
    # Check if required tools are available
    required_tools = ["get_main_hwnd", "get_mouse_position", "get_cursor_context"]
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    
    assert_tools_available(available_tools, required_tools)
    
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
    # Check if tool is available
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    assert_tools_available(available_tools, ["show_message_box"])
    
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
    # Check if tool is available
    available_tools = getattr(reaper_mcp_client, '_available_tools', set())
    assert_tools_available(available_tools, ["dock_window_add"])
    
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