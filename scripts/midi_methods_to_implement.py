#!/usr/bin/env python3
"""
MIDI-specific methods needed for AI MIDI workflow
These can be added to batch_implementation_v2.py
"""

midi_methods = [
    {
        "name": "create_midi_item",
        "description": "Create a new MIDI item with an empty take",
        "params": [
            {"name": "track_index", "type": "integer", "desc": "The track index (0-based)", "min": 0},
            {"name": "start_time", "type": "number", "desc": "Start time in seconds"},
            {"name": "length", "type": "number", "desc": "Length in seconds"}
        ],
        "lua_func": "CreateNewMIDIItemInProj",
        "lua_implementation": '''
            local track = reaper.GetTrack(0, args[1])
            if track then
                local item = reaper.CreateNewMIDIItemInProj(track, args[2], args[2] + args[3])
                response.ok = true
                response.ret = item
            else
                response.error = "Track not found at index " .. tostring(args[1])
            end
        '''
    },
    {
        "name": "get_media_item_take",
        "description": "Get a take from a media item",
        "params": [
            {"name": "item_index", "type": "integer", "desc": "The media item index (0-based)", "min": 0},
            {"name": "take_index", "type": "integer", "desc": "The take index (0-based)", "min": 0}
        ],
        "lua_func": "GetMediaItemTake",
        "lua_implementation": '''
            local item = reaper.GetMediaItem(0, args[1])
            if item then
                local take = reaper.GetMediaItemTake(item, args[2])
                response.ok = true
                response.ret = take
            else
                response.error = "Media item not found at index " .. tostring(args[1])
            end
        '''
    },
    {
        "name": "insert_midi_note",
        "description": "Insert a MIDI note into a take",
        "params": [
            {"name": "item_index", "type": "integer", "desc": "The media item index", "min": 0},
            {"name": "take_index", "type": "integer", "desc": "The take index", "min": 0},
            {"name": "pitch", "type": "integer", "desc": "MIDI pitch (0-127)", "min": 0, "max": 127},
            {"name": "velocity", "type": "integer", "desc": "MIDI velocity (0-127)", "min": 0, "max": 127},
            {"name": "start_time", "type": "number", "desc": "Start time in seconds"},
            {"name": "duration", "type": "number", "desc": "Duration in seconds"},
            {"name": "channel", "type": "integer", "desc": "MIDI channel (0-15)", "min": 0, "max": 15, "default": 0},
            {"name": "selected", "type": "boolean", "desc": "Is note selected", "default": False},
            {"name": "muted", "type": "boolean", "desc": "Is note muted", "default": False}
        ],
        "lua_func": "MIDI_InsertNote",
        "lua_implementation": '''
            local item = reaper.GetMediaItem(0, args[1])
            if item then
                local take = reaper.GetMediaItemTake(item, args[2])
                if take then
                    -- Convert time to PPQ
                    local ppq_start = reaper.MIDI_GetPPQPosFromProjTime(take, args[5])
                    local ppq_end = reaper.MIDI_GetPPQPosFromProjTime(take, args[5] + args[6])
                    
                    local result = reaper.MIDI_InsertNote(
                        take,
                        args[8] or false,  -- selected
                        args[9] or false,  -- muted
                        ppq_start,
                        ppq_end,
                        args[7] or 0,      -- channel
                        args[3],           -- pitch
                        args[4],           -- velocity
                        true               -- noSort (we'll sort later)
                    )
                    response.ok = result
                else
                    response.error = "Take not found at index " .. tostring(args[2])
                end
            else
                response.error = "Media item not found at index " .. tostring(args[1])
            end
        '''
    },
    {
        "name": "midi_sort",
        "description": "Sort MIDI events in a take after insertion",
        "params": [
            {"name": "item_index", "type": "integer", "desc": "The media item index", "min": 0},
            {"name": "take_index", "type": "integer", "desc": "The take index", "min": 0}
        ],
        "lua_func": "MIDI_Sort",
        "lua_implementation": '''
            local item = reaper.GetMediaItem(0, args[1])
            if item then
                local take = reaper.GetMediaItemTake(item, args[2])
                if take then
                    reaper.MIDI_Sort(take)
                    response.ok = true
                else
                    response.error = "Take not found at index " .. tostring(args[2])
                end
            else
                response.error = "Media item not found at index " .. tostring(args[1])
            end
        '''
    },
    {
        "name": "set_item_position",
        "description": "Set media item position",
        "params": [
            {"name": "item_index", "type": "integer", "desc": "The media item index", "min": 0},
            {"name": "position", "type": "number", "desc": "Position in seconds"}
        ],
        "lua_func": "SetMediaItemPosition",
        "lua_implementation": '''
            local item = reaper.GetMediaItem(0, args[1])
            if item then
                reaper.SetMediaItemPosition(item, args[2], true)
                response.ok = true
            else
                response.error = "Media item not found at index " .. tostring(args[1])
            end
        '''
    },
    {
        "name": "set_item_length",
        "description": "Set media item length",
        "params": [
            {"name": "item_index", "type": "integer", "desc": "The media item index", "min": 0},
            {"name": "length", "type": "number", "desc": "Length in seconds"}
        ],
        "lua_func": "SetMediaItemLength",
        "lua_implementation": '''
            local item = reaper.GetMediaItem(0, args[1])
            if item then
                reaper.SetMediaItemLength(item, args[2], true)
                response.ok = true
            else
                response.error = "Media item not found at index " .. tostring(args[1])
            end
        '''
    },
    {
        "name": "get_tempo_at_time",
        "description": "Get project tempo at a specific time",
        "params": [
            {"name": "time", "type": "number", "desc": "Time in seconds"}
        ],
        "lua_func": "TimeMap_GetDividedBpmAtTime",
        "lua_implementation": '''
            local tempo = reaper.TimeMap_GetDividedBpmAtTime(args[1])
            response.ok = true
            response.ret = tempo
        '''
    },
    {
        "name": "insert_midi_cc",
        "description": "Insert MIDI Control Change event",
        "params": [
            {"name": "item_index", "type": "integer", "desc": "The media item index", "min": 0},
            {"name": "take_index", "type": "integer", "desc": "The take index", "min": 0},
            {"name": "time", "type": "number", "desc": "Time in seconds"},
            {"name": "channel", "type": "integer", "desc": "MIDI channel (0-15)", "min": 0, "max": 15},
            {"name": "cc_number", "type": "integer", "desc": "CC number (0-127)", "min": 0, "max": 127},
            {"name": "value", "type": "integer", "desc": "CC value (0-127)", "min": 0, "max": 127},
            {"name": "selected", "type": "boolean", "desc": "Is CC selected", "default": False},
            {"name": "muted", "type": "boolean", "desc": "Is CC muted", "default": False}
        ],
        "lua_func": "MIDI_InsertCC",
        "lua_implementation": '''
            local item = reaper.GetMediaItem(0, args[1])
            if item then
                local take = reaper.GetMediaItemTake(item, args[2])
                if take then
                    local ppq_pos = reaper.MIDI_GetPPQPosFromProjTime(take, args[3])
                    local result = reaper.MIDI_InsertCC(
                        take,
                        args[7] or false,  -- selected
                        args[8] or false,  -- muted
                        ppq_pos,
                        176 + args[4],     -- 0xB0 + channel for CC
                        args[5],           -- CC number
                        args[6]            -- value
                    )
                    response.ok = result
                else
                    response.error = "Take not found at index " .. tostring(args[2])
                end
            else
                response.error = "Media item not found at index " .. tostring(args[1])
            end
        '''
    }
]

# Example of how these would be used in a complete workflow
example_workflow = """
# Complete AI MIDI Workflow Example:

1. Create a track
   await session.call_tool("insert_track", {"index": 0, "use_defaults": True})

2. Create a MIDI item
   await session.call_tool("create_midi_item", {
       "track_index": 0,
       "start_time": 0.0,
       "length": 8.0
   })

3. Insert MIDI notes
   for note in ai_generated_notes:
       await session.call_tool("insert_midi_note", {
           "item_index": 0,
           "take_index": 0,
           "pitch": note["pitch"],
           "velocity": note["velocity"],
           "start_time": note["start"],
           "duration": note["duration"],
           "channel": 0
       })

4. Sort MIDI events
   await session.call_tool("midi_sort", {"item_index": 0, "take_index": 0})

5. Start playback
   await session.call_tool("play", {})
"""

print("MIDI methods defined for AI workflow implementation")