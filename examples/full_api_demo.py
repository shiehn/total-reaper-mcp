#!/usr/bin/env python3
"""
Comprehensive demonstration of the REAPER MCP Server Full API
This shows how to use various ReaScript functions via MCP
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def demonstrate_full_api():
    """Demonstrate various API capabilities"""
    server_params = StdioServerParameters(
        command="python",
        args=["server/app_complete.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("🎵 REAPER MCP Full API Demo")
            print("=" * 50)
            
            # 1. Project Information
            print("\n📁 PROJECT INFO:")
            result = await session.call_tool("get_project_name", {"project_index": 0})
            print(f"  {result.content[0].text}")
            
            result = await session.call_tool("get_project_tempo", {})
            print(f"  {result.content[0].text}")
            
            # 2. Track Management
            print("\n🎚️ TRACK MANAGEMENT:")
            
            # Count existing tracks
            result = await session.call_tool("count_tracks", {"project_index": 0})
            print(f"  {result.content[0].text}")
            
            # Create a new track
            result = await session.call_tool("insert_track_at_index", {
                "index": 0,
                "use_defaults": True
            })
            print(f"  Created track: {result.content[0].text}")
            
            # Set track properties
            await session.call_tool("set_track_name", {
                "track_index": 0,
                "name": "AI Demo Track"
            })
            
            await session.call_tool("set_track_color", {
                "track_index": 0,
                "color": 0xFF0000  # Red
            })
            
            await session.call_tool("set_track_volume", {
                "track_index": 0,
                "volume_db": -6.0
            })
            
            await session.call_tool("set_track_pan", {
                "track_index": 0,
                "pan": -0.25  # Slightly left
            })
            
            print("  ✅ Track configured")
            
            # 3. MIDI Item Creation
            print("\n🎹 MIDI CREATION:")
            
            # Create MIDI item
            result = await session.call_tool("create_midi_item", {
                "track_index": 0,
                "start_time": 0.0,
                "end_time": 4.0,
                "qn": False
            })
            print(f"  Created MIDI item")
            
            # Get the take
            result = await session.call_tool("get_active_take", {"item_index": 0})
            take_ptr = result.content[0].text.split(": ")[-1]
            
            # Insert some notes (C major scale)
            notes = [
                {"pitch": 60, "start": 0.0, "duration": 0.5},    # C
                {"pitch": 62, "start": 0.5, "duration": 0.5},    # D
                {"pitch": 64, "start": 1.0, "duration": 0.5},    # E
                {"pitch": 65, "start": 1.5, "duration": 0.5},    # F
                {"pitch": 67, "start": 2.0, "duration": 0.5},    # G
                {"pitch": 69, "start": 2.5, "duration": 0.5},    # A
                {"pitch": 71, "start": 3.0, "duration": 0.5},    # B
                {"pitch": 72, "start": 3.5, "duration": 0.5},    # C
            ]
            
            print("  Inserting notes...")
            for note in notes:
                # Convert time to PPQ
                ppq_start = await session.call_tool("midi_get_ppq_pos_from_proj_time", {
                    "take_ptr": take_ptr,
                    "time": note["start"]
                })
                ppq_end = await session.call_tool("midi_get_ppq_pos_from_proj_time", {
                    "take_ptr": take_ptr,
                    "time": note["start"] + note["duration"]
                })
                
                # Insert note
                await session.call_tool("midi_insert_note", {
                    "take_ptr": take_ptr,
                    "selected": False,
                    "muted": False,
                    "start_ppq": float(ppq_start.content[0].text.split(": ")[-1]),
                    "end_ppq": float(ppq_end.content[0].text.split(": ")[-1]),
                    "channel": 0,
                    "pitch": note["pitch"],
                    "velocity": 100,
                    "no_sort": True
                })
            
            # Sort MIDI
            await session.call_tool("midi_sort", {"take_ptr": take_ptr})
            print("  ✅ MIDI notes inserted")
            
            # 4. Add FX
            print("\n🎛️ EFFECTS:")
            
            # Add reverb
            result = await session.call_tool("track_fx_add_by_name", {
                "track_index": 0,
                "fx_name": "ReaVerbate",
                "instantiate": False
            })
            print("  Added reverb effect")
            
            # 5. Markers
            print("\n📍 MARKERS:")
            
            # Add markers
            await session.call_tool("add_project_marker", {
                "project_index": 0,
                "is_region": False,
                "position": 0.0,
                "region_end": 0.0,
                "name": "Start",
                "index": -1
            })
            
            await session.call_tool("add_project_marker", {
                "project_index": 0,
                "is_region": False,
                "position": 4.0,
                "region_end": 0.0,
                "name": "End",
                "index": -1
            })
            print("  ✅ Markers added")
            
            # 6. Envelope automation
            print("\n📈 AUTOMATION:")
            
            # Get volume envelope
            result = await session.call_tool("get_track_envelope_by_name", {
                "track_index": 0,
                "envelope_name": "Volume"
            })
            
            if "envelope" in result.content[0].text:
                env_ptr = result.content[0].text.split(": ")[-1]
                
                # Add automation points
                await session.call_tool("insert_envelope_point", {
                    "envelope_ptr": env_ptr,
                    "time": 0.0,
                    "value": 1.0,
                    "shape": 0,
                    "tension": 0.0,
                    "selected": False,
                    "no_sort": False
                })
                
                await session.call_tool("insert_envelope_point", {
                    "envelope_ptr": env_ptr,
                    "time": 2.0,
                    "value": 0.5,
                    "shape": 0,
                    "tension": 0.0,
                    "selected": False,
                    "no_sort": False
                })
                
                await session.call_tool("insert_envelope_point", {
                    "envelope_ptr": env_ptr,
                    "time": 4.0,
                    "value": 1.0,
                    "shape": 0,
                    "tension": 0.0,
                    "selected": False,
                    "no_sort": False
                })
                
                print("  ✅ Volume automation added")
            
            # 7. Transport control
            print("\n▶️ TRANSPORT:")
            
            # Set cursor to start
            await session.call_tool("set_edit_cursor_position", {
                "time": 0.0,
                "move_view": True,
                "seek_play": False
            })
            
            # Update UI
            await session.call_tool("update_arrange", {})
            await session.call_tool("update_timeline", {})
            
            # Create undo point
            await session.call_tool("undo_begin_block", {})
            await session.call_tool("undo_end_block", {
                "description": "MCP API Demo",
                "flags": -1
            })
            
            print("  ✅ Ready to play!")
            
            # Play
            print("\n🎵 Starting playback...")
            await session.call_tool("play", {})
            
            # Wait a bit
            await asyncio.sleep(5)
            
            # Stop
            await session.call_tool("stop", {})
            print("  ✅ Playback complete")
            
            # 8. Save project
            print("\n💾 SAVING:")
            result = await session.call_tool("save_project", {
                "project_index": 0,
                "force_save_as": False
            })
            print(f"  {result.content[0].text}")
            
            print("\n✨ Demo complete!")
            print("Check REAPER to see the created track with MIDI notes and automation!")

if __name__ == "__main__":
    print("Starting REAPER MCP Full API Demo...")
    print("Make sure REAPER is running with mcp_bridge_complete.lua loaded!")
    print("")
    asyncio.run(demonstrate_full_api())