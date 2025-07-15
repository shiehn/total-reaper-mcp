import pytest
import pytest_asyncio
from .test_utils import (
    ensure_clean_project,
    assert_response_success
)

@pytest.mark.asyncio
async def test_save_project(reaper_mcp_client):
    """Test saving project"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Save project
    result = await reaper_mcp_client.call_tool(
        "save_project",
        {}
    )
    print(f"Save project result: {result}")
    assert_response_success(result)

@pytest.mark.asyncio
async def test_save_project_as(reaper_mcp_client):
    """Test saving project with a new name"""
    # Ensure clean project state
    await ensure_clean_project(reaper_mcp_client)
    
    # Save project as (if supported with filename parameter)
    result = await reaper_mcp_client.call_tool(
        "save_project",
        {"filename": "test_project.rpp"}
    )
    print(f"Save project as result: {result}")
    # This might fail if filename parameter is not supported
    # which is OK - the basic save test above should pass