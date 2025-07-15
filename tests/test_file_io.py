"""Test file I/O and project management operations"""
import pytest
import pytest_asyncio
import os

@pytest.mark.asyncio
async def test_reaper_paths(reaper_mcp_client):
    """Test getting REAPER paths"""
    # Get resource path
    result = await reaper_mcp_client.call_tool(
        "get_resource_path",
        {}
    )
    assert result is not None
    assert "REAPER resource path:" in result.content[0].text
    assert "/" in result.content[0].text or "\\" in result.content[0].text
    
    # Get executable directory
    result = await reaper_mcp_client.call_tool(
        "get_exe_dir",
        {}
    )
    assert result is not None
    assert "REAPER executable directory:" in result.content[0].text

@pytest.mark.asyncio
async def test_project_info(reaper_mcp_client):
    """Test project information operations"""
    # Get project path
    result = await reaper_mcp_client.call_tool(
        "get_project_path",
        {"project_index": 0}
    )
    assert result is not None
    assert "Project" in result.content[0].text
    
    # Get project name
    result = await reaper_mcp_client.call_tool(
        "get_project_name",
        {"project_index": 0}
    )
    assert result is not None
    assert "project" in result.content[0].text.lower()
    
    # Check if project is dirty
    result = await reaper_mcp_client.call_tool(
        "is_project_dirty",
        {"project_index": 0}
    )
    assert result is not None
    assert "changes" in result.content[0].text

@pytest.mark.asyncio
async def test_file_operations(reaper_mcp_client):
    """Test file and directory operations"""
    # Check if a known file exists
    test_files = [
        "/System/Library/Sounds/Glass.aiff",  # macOS
        "C:\\Windows\\Media\\Windows Ding.wav",  # Windows
        "/usr/share/sounds/alsa/Noise.wav"  # Linux
    ]
    
    for test_file in test_files:
        result = await reaper_mcp_client.call_tool(
            "file_exists",
            {"filename": test_file}
        )
        assert result is not None
        assert "exists" in result.content[0].text or "does not exist" in result.content[0].text
        
        # If we find one that exists, we're good
        if "exists" in result.content[0].text and "does not exist" not in result.content[0].text:
            break

@pytest.mark.asyncio
async def test_extended_state(reaper_mcp_client):
    """Test extended state operations"""
    section = "MCP_Test"
    key = "test_value"
    value = "Hello from MCP!"
    
    # Set extended state
    result = await reaper_mcp_client.call_tool(
        "set_ext_state",
        {
            "section": section,
            "key": key,
            "value": value,
            "persist": False
        }
    )
    assert result is not None
    assert "Set ExtState" in result.content[0].text
    
    # Check if it exists
    result = await reaper_mcp_client.call_tool(
        "has_ext_state",
        {
            "section": section,
            "key": key
        }
    )
    assert result is not None
    assert "exists" in result.content[0].text
    
    # Get the value
    result = await reaper_mcp_client.call_tool(
        "get_ext_state",
        {
            "section": section,
            "key": key
        }
    )
    assert result is not None
    assert value in result.content[0].text or "ExtState" in result.content[0].text
    
    # Delete it
    result = await reaper_mcp_client.call_tool(
        "delete_ext_state",
        {
            "section": section,
            "key": key,
            "persist": False
        }
    )
    assert result is not None
    assert "Deleted ExtState" in result.content[0].text

@pytest.mark.asyncio
async def test_project_notes(reaper_mcp_client):
    """Test project notes operations"""
    # Get current project notes
    result = await reaper_mcp_client.call_tool(
        "get_set_project_notes",
        {
            "project_index": 0,
            "set_notes": False,
            "notes": ""
        }
    )
    assert result is not None
    assert "notes" in result.content[0].text.lower()
    
    # Set project notes
    test_notes = "Test notes from MCP"
    result = await reaper_mcp_client.call_tool(
        "get_set_project_notes",
        {
            "project_index": 0,
            "set_notes": True,
            "notes": test_notes
        }
    )
    assert result is not None
    assert "notes updated" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_enumerate_files(reaper_mcp_client):
    """Test file enumeration"""
    # Get resource path first
    result = await reaper_mcp_client.call_tool(
        "get_resource_path",
        {}
    )
    resource_path = result.content[0].text.split(": ", 1)[1]
    
    # Try to enumerate files in the resource path
    for i in range(3):  # Check first 3 files
        result = await reaper_mcp_client.call_tool(
            "enumerate_files",
            {
                "path": resource_path,
                "file_index": i
            }
        )
        assert result is not None
        # Either we get a file or "No file at index"
        assert "File " in result.content[0].text or "No file at index" in result.content[0].text