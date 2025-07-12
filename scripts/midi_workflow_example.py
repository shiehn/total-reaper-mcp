#!/usr/bin/env python3
"""
Example of how the MIDI workflow would work with the MCP server
once the necessary methods are implemented.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def create_midi_from_ai(midi_data):
    """
    Example workflow for creating a MIDI track from AI-generated data.
    
    Args:
        midi_data: List of dicts with MIDI note information
                  [{"pitch": 60, "velocity": 100, "start": 0.0, "duration": 0.5}, ...]
    """
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "server.app"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Step 1: Create a new track
            print("Creating new track...")
            result = await session.call_tool(
                "insert_track",
                {"index": 0, "use_defaults": True}
            )
            print(f"✓ {result.content[0].text}")
            
            # Step 2: Name the track
            result = await session.call_tool(
                "set_track_name",
                {"track_index": 0, "name": "AI Generated MIDI"}
            )
            print(f"✓ {result.content[0].text}")
            
            # Step 3: Create a MIDI item (NEEDS IMPLEMENTATION)
            # This would create a new MIDI item with an empty take
            print("Creating MIDI item...")
            result = await session.call_tool(
                "create_midi_item",  # Not yet implemented
                {
                    "track_index": 0,
                    "start_time": 0.0,
                    "end_time": 10.0  # 10 second item
                }
            )
            
            # Step 4: Get the MIDI take (NEEDS IMPLEMENTATION)
            result = await session.call_tool(
                "get_media_item_take",  # Not yet implemented
                {"item_index": 0, "take_index": 0}
            )
            
            # Step 5: Insert MIDI notes (NEEDS IMPLEMENTATION)
            print("Inserting MIDI notes...")
            for note in midi_data:
                # Convert time to PPQ (Pulses Per Quarter note)
                # Assuming 960 PPQ and 120 BPM
                ppq_per_second = 960 * 2  # 960 PPQ * (120 BPM / 60 sec)
                start_ppq = int(note["start"] * ppq_per_second)
                end_ppq = int((note["start"] + note["duration"]) * ppq_per_second)
                
                result = await session.call_tool(
                    "insert_midi_note",  # Not yet implemented
                    {
                        "take_index": 0,
                        "selected": False,
                        "muted": False,
                        "start_ppq": start_ppq,
                        "end_ppq": end_ppq,
                        "channel": 0,
                        "pitch": note["pitch"],
                        "velocity": note["velocity"]
                    }
                )
            
            # Step 6: Sort MIDI events (NEEDS IMPLEMENTATION)
            result = await session.call_tool(
                "midi_sort",  # Not yet implemented
                {"take_index": 0}
            )
            
            # Step 7: Update the arrange view
            result = await session.call_tool(
                "update_arrange",  # Ready to implement
                {}
            )
            
            # Step 8: Set cursor to beginning
            result = await session.call_tool(
                "set_cursor_position",  # Ready to implement
                {"time": 0.0, "move_view": True, "seek_play": False}
            )
            
            # Step 9: Start playback
            print("Starting playback...")
            result = await session.call_tool(
                "play",  # Ready to implement
                {}
            )
            print(f"✓ {result.content[0].text}")

# Example usage
if __name__ == "__main__":
    # Example AI-generated MIDI data (C major scale)
    ai_generated_midi = [
        {"pitch": 60, "velocity": 100, "start": 0.0, "duration": 0.5},  # C
        {"pitch": 62, "velocity": 90, "start": 0.5, "duration": 0.5},   # D
        {"pitch": 64, "velocity": 90, "start": 1.0, "duration": 0.5},   # E
        {"pitch": 65, "velocity": 90, "start": 1.5, "duration": 0.5},   # F
        {"pitch": 67, "velocity": 90, "start": 2.0, "duration": 0.5},   # G
        {"pitch": 69, "velocity": 90, "start": 2.5, "duration": 0.5},   # A
        {"pitch": 71, "velocity": 90, "start": 3.0, "duration": 0.5},   # B
        {"pitch": 72, "velocity": 100, "start": 3.5, "duration": 1.0},  # C
    ]
    
    asyncio.run(create_midi_from_ai(ai_generated_midi))