"""
Test utilities for REAPER MCP tests

This module provides utilities to ensure tests work reliably regardless of
the initial REAPER project state.
"""

import re
import asyncio
from typing import Optional, Tuple


async def ensure_clean_project(reaper_mcp_client) -> None:
    """Ensure we have a clean project state by removing all tracks"""
    # Get current track count
    result = await reaper_mcp_client.call_tool("get_track_count", {})
    match = re.search(r'(\d+) tracks?', result.content[0].text)
    track_count = int(match.group(1)) if match else 0
    
    # Delete all tracks in reverse order to avoid index shifting
    for i in range(track_count - 1, -1, -1):
        try:
            await reaper_mcp_client.call_tool("delete_track", {"track_index": i})
        except:
            # Track might already be deleted or index invalid
            pass
    
    # Verify clean state
    result = await reaper_mcp_client.call_tool("get_track_count", {})
    match = re.search(r'(\d+) tracks?', result.content[0].text)
    final_count = int(match.group(1)) if match else 0
    
    if final_count > 0:
        # If tracks remain, it might be due to locked tracks or other issues
        # Log but don't fail
        print(f"Warning: {final_count} tracks remain after cleanup")


async def create_track_with_verification(reaper_mcp_client, index: int = 0) -> int:
    """
    Create a track and return its actual index after creation.
    This handles the case where track insertion might not place the track
    exactly where requested.
    """
    # Get initial track count
    result = await reaper_mcp_client.call_tool("get_track_count", {})
    match = re.search(r'(\d+) tracks?', result.content[0].text)
    initial_count = int(match.group(1)) if match else 0
    
    # Insert track
    result = await reaper_mcp_client.call_tool(
        "insert_track",
        {"index": index, "use_defaults": True}
    )
    
    if "success" not in result.content[0].text.lower() and "inserted" not in result.content[0].text.lower():
        raise Exception(f"Failed to create track: {result.content[0].text}")
    
    # Small delay to ensure REAPER has processed the track creation
    await asyncio.sleep(0.1)
    
    # Get new track count
    result = await reaper_mcp_client.call_tool("get_track_count", {})
    match = re.search(r'(\d+) tracks?', result.content[0].text)
    new_count = int(match.group(1)) if match else 0
    
    if new_count <= initial_count:
        raise Exception("Track count did not increase after insertion")
    
    # Find the newly created track
    # When inserting at index 0, the new track should be at index 0
    # When inserting at the end, it should be at new_count - 1
    if index == 0:
        actual_index = 0
    elif index >= initial_count:
        actual_index = new_count - 1
    else:
        actual_index = index
    
    # Verify the track exists
    result = await reaper_mcp_client.call_tool(
        "get_track",
        {"track_index": actual_index}
    )
    
    if "found track" not in result.content[0].text.lower():
        # Try to find the track by checking all indices
        for i in range(new_count):
            result = await reaper_mcp_client.call_tool(
                "get_track",
                {"track_index": i}
            )
            if "found track" in result.content[0].text.lower():
                actual_index = i
                break
        else:
            raise Exception("Could not find newly created track")
    
    return actual_index


async def create_media_item_with_verification(reaper_mcp_client, track_index: int) -> int:
    """
    Create a media item on a track and return its actual index.
    """
    # Get initial item count
    result = await reaper_mcp_client.call_tool("count_media_items", {})
    match = re.search(r'(\d+) media items', result.content[0].text)
    initial_count = int(match.group(1)) if match else 0
    
    # Add media item
    result = await reaper_mcp_client.call_tool(
        "add_media_item_to_track",
        {"track_index": track_index}
    )
    
    if "added" not in result.content[0].text.lower() and "success" not in result.content[0].text.lower():
        raise Exception(f"Failed to create media item: {result.content[0].text}")
    
    # Get new item count
    result = await reaper_mcp_client.call_tool("count_media_items", {})
    match = re.search(r'(\d+) media items', result.content[0].text)
    new_count = int(match.group(1)) if match else 0
    
    if new_count <= initial_count:
        raise Exception("Media item count did not increase")
    
    # The new item is typically the last one
    return new_count - 1


async def create_midi_item_with_verification(reaper_mcp_client, track_index: int, 
                                           position: float = 0.0, 
                                           length: float = 1.0) -> Tuple[int, int]:
    """
    Create a MIDI item on a track and return (item_index, take_index).
    """
    # Create the MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {
            "track_index": track_index,
            "position": position,
            "length": length
        }
    )
    
    # Extract item index from response
    match = re.search(r'index (\d+)', result.content[0].text)
    if match:
        item_index = int(match.group(1))
    else:
        # If not in response, assume it's the last item
        result = await reaper_mcp_client.call_tool("count_media_items", {})
        match = re.search(r'(\d+) media items', result.content[0].text)
        count = int(match.group(1)) if match else 0
        item_index = count - 1 if count > 0 else 0
    
    # MIDI items typically have take index 0
    return item_index, 0


async def add_fx_with_verification(reaper_mcp_client, track_index: int, 
                                  fx_name: str = "ReaEQ") -> int:
    """
    Add an FX to a track and return its index.
    Handles potential failures gracefully.
    """
    # First verify the track exists
    result = await reaper_mcp_client.call_tool(
        "get_track",
        {"track_index": track_index}
    )
    
    if "found track" not in result.content[0].text.lower():
        raise Exception(f"Track {track_index} not found")
    
    # Get initial FX count
    result = await reaper_mcp_client.call_tool(
        "track_fx_get_count",
        {"track_index": track_index}
    )
    match = re.search(r'has (\d+) FX', result.content[0].text)
    initial_count = int(match.group(1)) if match else 0
    
    # Add FX
    result = await reaper_mcp_client.call_tool(
        "track_fx_add_by_name",
        {"track_index": track_index, "fx_name": fx_name}
    )
    
    # Check if it was added
    if "added" in result.content[0].text.lower():
        # Extract FX index from response if available
        match = re.search(r'FX index (\d+)', result.content[0].text)
        if match:
            return int(match.group(1))
        else:
            return initial_count  # Assume it was added at the end
    else:
        # FX might not be available or other issue
        # Return -1 to indicate failure
        return -1


async def get_track_envelope_with_verification(reaper_mcp_client, track_index: int, 
                                              envelope_name: str) -> Optional[str]:
    """
    Get a track envelope, handling cases where it might not exist.
    Returns envelope info or None if not found.
    """
    try:
        result = await reaper_mcp_client.call_tool(
            "get_track_envelope_by_name",
            {"track_index": track_index, "envelope_name": envelope_name}
        )
        
        if "error" in result.content[0].text.lower() or "not found" in result.content[0].text.lower():
            return None
        
        return result.content[0].text
    except:
        return None


def extract_number_from_response(text: str, pattern: str = r'(\d+)') -> Optional[int]:
    """Extract a number from a response text using a regex pattern"""
    match = re.search(pattern, text)
    return int(match.group(1)) if match else None


def assert_response_contains(result, expected_text: str, case_sensitive: bool = False) -> None:
    """Assert that the response contains expected text"""
    response_text = result.content[0].text
    if not case_sensitive:
        response_text = response_text.lower()
        expected_text = expected_text.lower()
    
    assert expected_text in response_text, f"Expected '{expected_text}' in response, got: {result.content[0].text}"


def assert_response_success(result) -> None:
    """Assert that the response indicates success"""
    response_text = result.content[0].text.lower()
    success_indicators = ["success", "successfully", "completed", "added", "created", "inserted", "set", "updated"]
    
    # Check for error indicators first
    if "error" in response_text or "failed" in response_text:
        # Unless it's something like "no errors"
        if "no error" not in response_text and "0 error" not in response_text:
            raise AssertionError(f"Response indicates failure: {result.content[0].text}")
    
    # Check for at least one success indicator
    if not any(indicator in response_text for indicator in success_indicators):
        # Some responses just state facts without explicit success words
        # Check if it's not an error and contains expected patterns
        if not ("track" in response_text or "item" in response_text or 
                "fx" in response_text or "envelope" in response_text):
            raise AssertionError(f"Response does not indicate success: {result.content[0].text}")