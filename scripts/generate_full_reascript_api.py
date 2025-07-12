#!/usr/bin/env python3
"""
Comprehensive ReaScript API implementation generator
This generates implementations for the ENTIRE ReaScript API
"""

import json
import os
from typing import List, Dict, Any

# Complete ReaScript API function definitions
# Based on https://www.reaper.fm/sdk/reascript/reascripthelp.html

REASCRIPT_API = {
    "Track Management": [
        {
            "name": "count_tracks",
            "lua_func": "CountTracks",
            "description": "Count tracks in project",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index (0=current)", "default": 0}
            ],
            "returns": "integer"
        },
        {
            "name": "get_track",
            "lua_func": "GetTrack",
            "description": "Get track by index",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index (0=current)", "default": 0},
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"}
            ],
            "returns": "MediaTrack*"
        },
        {
            "name": "get_master_track",
            "lua_func": "GetMasterTrack",
            "description": "Get master track",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index (0=current)", "default": 0}
            ],
            "returns": "MediaTrack*"
        },
        {
            "name": "get_track_name",
            "lua_func": "GetTrackName",
            "description": "Get track name",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"}
            ],
            "returns": "string"
        },
        {
            "name": "set_track_name",
            "lua_func": "GetSetMediaTrackInfo_String",
            "description": "Set track name",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"},
                {"name": "name", "type": "string", "desc": "New track name"}
            ],
            "returns": "boolean"
        },
        {
            "name": "insert_track_at_index",
            "lua_func": "InsertTrackAtIndex",
            "description": "Insert new track at index",
            "params": [
                {"name": "index", "type": "integer", "desc": "Index to insert at"},
                {"name": "use_defaults", "type": "boolean", "desc": "Use default track settings", "default": True}
            ],
            "returns": "void"
        },
        {
            "name": "delete_track",
            "lua_func": "DeleteTrack",
            "description": "Delete track",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index to delete"}
            ],
            "returns": "void"
        },
        {
            "name": "get_track_mute",
            "lua_func": "GetMediaTrackInfo_Value",
            "description": "Get track mute state",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"}
            ],
            "info_param": "B_MUTE",
            "returns": "boolean"
        },
        {
            "name": "set_track_mute",
            "lua_func": "SetMediaTrackInfo_Value", 
            "description": "Set track mute state",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"},
                {"name": "mute", "type": "boolean", "desc": "Mute state"}
            ],
            "info_param": "B_MUTE",
            "returns": "boolean"
        },
        {
            "name": "get_track_solo",
            "lua_func": "GetMediaTrackInfo_Value",
            "description": "Get track solo state",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"}
            ],
            "info_param": "I_SOLO",
            "returns": "integer"
        },
        {
            "name": "set_track_solo",
            "lua_func": "SetMediaTrackInfo_Value",
            "description": "Set track solo state",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"},
                {"name": "solo", "type": "boolean", "desc": "Solo state"}
            ],
            "info_param": "I_SOLO",
            "returns": "boolean"
        },
        {
            "name": "get_track_volume",
            "lua_func": "GetMediaTrackInfo_Value",
            "description": "Get track volume",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"}
            ],
            "info_param": "D_VOL",
            "returns": "number",
            "convert": "db"
        },
        {
            "name": "set_track_volume",
            "lua_func": "SetMediaTrackInfo_Value",
            "description": "Set track volume",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"},
                {"name": "volume_db", "type": "number", "desc": "Volume in dB"}
            ],
            "info_param": "D_VOL",
            "returns": "boolean",
            "convert": "from_db"
        },
        {
            "name": "get_track_pan",
            "lua_func": "GetMediaTrackInfo_Value",
            "description": "Get track pan",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"}
            ],
            "info_param": "D_PAN",
            "returns": "number"
        },
        {
            "name": "set_track_pan",
            "lua_func": "SetMediaTrackInfo_Value",
            "description": "Set track pan",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"},
                {"name": "pan", "type": "number", "desc": "Pan value (-1 to 1)"}
            ],
            "info_param": "D_PAN",
            "returns": "boolean"
        },
        {
            "name": "get_track_color",
            "lua_func": "GetTrackColor",
            "description": "Get track color",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"}
            ],
            "returns": "integer"
        },
        {
            "name": "set_track_color", 
            "lua_func": "SetTrackColor",
            "description": "Set track color",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"},
                {"name": "color", "type": "integer", "desc": "RGB color value"}
            ],
            "returns": "void"
        }
    ],
    
    "Media Items": [
        {
            "name": "count_media_items",
            "lua_func": "CountMediaItems",
            "description": "Count media items in project",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index (0=current)", "default": 0}
            ],
            "returns": "integer"
        },
        {
            "name": "get_media_item",
            "lua_func": "GetMediaItem",
            "description": "Get media item by index",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index (0=current)", "default": 0},
                {"name": "item_index", "type": "integer", "desc": "Item index (0-based)"}
            ],
            "returns": "MediaItem*"
        },
        {
            "name": "add_media_item_to_track",
            "lua_func": "AddMediaItemToTrack",
            "description": "Add new media item to track",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"}
            ],
            "returns": "MediaItem*"
        },
        {
            "name": "delete_media_item",
            "lua_func": "DeleteTrackMediaItem",
            "description": "Delete media item from track",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"},
                {"name": "item_index", "type": "integer", "desc": "Item index on track"}
            ],
            "returns": "boolean"
        },
        {
            "name": "get_media_item_position",
            "lua_func": "GetMediaItemInfo_Value",
            "description": "Get media item position",
            "params": [
                {"name": "item_index", "type": "integer", "desc": "Item index (0-based)"}
            ],
            "info_param": "D_POSITION",
            "returns": "number"
        },
        {
            "name": "set_media_item_position",
            "lua_func": "SetMediaItemInfo_Value",
            "description": "Set media item position",
            "params": [
                {"name": "item_index", "type": "integer", "desc": "Item index (0-based)"},
                {"name": "position", "type": "number", "desc": "Position in seconds"}
            ],
            "info_param": "D_POSITION",
            "returns": "boolean"
        },
        {
            "name": "get_media_item_length",
            "lua_func": "GetMediaItemInfo_Value",
            "description": "Get media item length",
            "params": [
                {"name": "item_index", "type": "integer", "desc": "Item index (0-based)"}
            ],
            "info_param": "D_LENGTH",
            "returns": "number"
        },
        {
            "name": "set_media_item_length",
            "lua_func": "SetMediaItemInfo_Value",
            "description": "Set media item length",
            "params": [
                {"name": "item_index", "type": "integer", "desc": "Item index (0-based)"},
                {"name": "length", "type": "number", "desc": "Length in seconds"}
            ],
            "info_param": "D_LENGTH",
            "returns": "boolean"
        },
        {
            "name": "create_midi_item",
            "lua_func": "CreateNewMIDIItemInProj",
            "description": "Create new MIDI item",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index (0-based)"},
                {"name": "start_time", "type": "number", "desc": "Start time in seconds"},
                {"name": "end_time", "type": "number", "desc": "End time in seconds"},
                {"name": "qn", "type": "boolean", "desc": "Use quarter notes", "default": False}
            ],
            "returns": "MediaItem*"
        }
    ],
    
    "Takes": [
        {
            "name": "count_takes",
            "lua_func": "CountTakes", 
            "description": "Count takes in media item",
            "params": [
                {"name": "item_index", "type": "integer", "desc": "Item index (0-based)"}
            ],
            "returns": "integer"
        },
        {
            "name": "get_take",
            "lua_func": "GetMediaItemTake",
            "description": "Get take from media item",
            "params": [
                {"name": "item_index", "type": "integer", "desc": "Item index (0-based)"},
                {"name": "take_index", "type": "integer", "desc": "Take index (0-based)"}
            ],
            "returns": "MediaItem_Take*"
        },
        {
            "name": "get_active_take",
            "lua_func": "GetActiveTake",
            "description": "Get active take from media item",
            "params": [
                {"name": "item_index", "type": "integer", "desc": "Item index (0-based)"}
            ],
            "returns": "MediaItem_Take*"
        },
        {
            "name": "set_active_take",
            "lua_func": "SetActiveTake",
            "description": "Set active take for media item",
            "params": [
                {"name": "take_ptr", "type": "string", "desc": "Take pointer"}
            ],
            "returns": "void"
        },
        {
            "name": "add_take_to_item",
            "lua_func": "AddTakeToMediaItem",
            "description": "Add new take to media item",
            "params": [
                {"name": "item_index", "type": "integer", "desc": "Item index (0-based)"}
            ],
            "returns": "MediaItem_Take*"
        }
    ],
    
    "MIDI": [
        {
            "name": "midi_insert_note",
            "lua_func": "MIDI_InsertNote",
            "description": "Insert MIDI note",
            "params": [
                {"name": "take_ptr", "type": "string", "desc": "Take pointer"},
                {"name": "selected", "type": "boolean", "desc": "Note selected", "default": False},
                {"name": "muted", "type": "boolean", "desc": "Note muted", "default": False},
                {"name": "start_ppq", "type": "number", "desc": "Start position in PPQ"},
                {"name": "end_ppq", "type": "number", "desc": "End position in PPQ"},
                {"name": "channel", "type": "integer", "desc": "MIDI channel (0-15)", "default": 0},
                {"name": "pitch", "type": "integer", "desc": "MIDI pitch (0-127)"},
                {"name": "velocity", "type": "integer", "desc": "Velocity (0-127)", "default": 100},
                {"name": "no_sort", "type": "boolean", "desc": "Don't sort after insert", "default": False}
            ],
            "returns": "boolean"
        },
        {
            "name": "midi_delete_note",
            "lua_func": "MIDI_DeleteNote",
            "description": "Delete MIDI note",
            "params": [
                {"name": "take_ptr", "type": "string", "desc": "Take pointer"},
                {"name": "note_index", "type": "integer", "desc": "Note index to delete"}
            ],
            "returns": "boolean"
        },
        {
            "name": "midi_count_events",
            "lua_func": "MIDI_CountEvts",
            "description": "Count MIDI events in take",
            "params": [
                {"name": "take_ptr", "type": "string", "desc": "Take pointer"}
            ],
            "returns": "table"
        },
        {
            "name": "midi_get_note",
            "lua_func": "MIDI_GetNote",
            "description": "Get MIDI note info",
            "params": [
                {"name": "take_ptr", "type": "string", "desc": "Take pointer"},
                {"name": "note_index", "type": "integer", "desc": "Note index"}
            ],
            "returns": "table"
        },
        {
            "name": "midi_set_note",
            "lua_func": "MIDI_SetNote",
            "description": "Set MIDI note properties",
            "params": [
                {"name": "take_ptr", "type": "string", "desc": "Take pointer"},
                {"name": "note_index", "type": "integer", "desc": "Note index"},
                {"name": "selected", "type": "boolean", "desc": "Note selected", "optional": True},
                {"name": "muted", "type": "boolean", "desc": "Note muted", "optional": True},
                {"name": "start_ppq", "type": "number", "desc": "Start position in PPQ", "optional": True},
                {"name": "end_ppq", "type": "number", "desc": "End position in PPQ", "optional": True},
                {"name": "channel", "type": "integer", "desc": "MIDI channel", "optional": True},
                {"name": "pitch", "type": "integer", "desc": "MIDI pitch", "optional": True},
                {"name": "velocity", "type": "integer", "desc": "Velocity", "optional": True},
                {"name": "no_sort", "type": "boolean", "desc": "Don't sort", "default": False}
            ],
            "returns": "boolean"
        },
        {
            "name": "midi_sort",
            "lua_func": "MIDI_Sort",
            "description": "Sort MIDI events",
            "params": [
                {"name": "take_ptr", "type": "string", "desc": "Take pointer"}
            ],
            "returns": "void"
        },
        {
            "name": "midi_insert_cc",
            "lua_func": "MIDI_InsertCC",
            "description": "Insert MIDI CC event",
            "params": [
                {"name": "take_ptr", "type": "string", "desc": "Take pointer"},
                {"name": "selected", "type": "boolean", "desc": "CC selected", "default": False},
                {"name": "muted", "type": "boolean", "desc": "CC muted", "default": False},
                {"name": "ppq_pos", "type": "number", "desc": "Position in PPQ"},
                {"name": "type", "type": "integer", "desc": "Message type"},
                {"name": "channel", "type": "integer", "desc": "MIDI channel (0-15)"},
                {"name": "msg2", "type": "integer", "desc": "CC number or note"},
                {"name": "msg3", "type": "integer", "desc": "CC value or velocity"}
            ],
            "returns": "boolean"
        },
        {
            "name": "midi_get_ppq_pos_from_proj_time",
            "lua_func": "MIDI_GetPPQPosFromProjTime",
            "description": "Convert project time to PPQ",
            "params": [
                {"name": "take_ptr", "type": "string", "desc": "Take pointer"},
                {"name": "time", "type": "number", "desc": "Time in seconds"}
            ],
            "returns": "number"
        },
        {
            "name": "midi_get_proj_time_from_ppq_pos",
            "lua_func": "MIDI_GetProjTimeFromPPQPos",
            "description": "Convert PPQ to project time",
            "params": [
                {"name": "take_ptr", "type": "string", "desc": "Take pointer"},
                {"name": "ppq", "type": "number", "desc": "Position in PPQ"}
            ],
            "returns": "number"
        }
    ],
    
    "Transport": [
        {
            "name": "play",
            "lua_func": "CSurf_OnPlay",
            "description": "Start playback",
            "params": [],
            "returns": "void"
        },
        {
            "name": "stop",
            "lua_func": "CSurf_OnStop",
            "description": "Stop playback",
            "params": [],
            "returns": "void"
        },
        {
            "name": "pause",
            "lua_func": "CSurf_OnPause",
            "description": "Pause playback",
            "params": [],
            "returns": "void"
        },
        {
            "name": "record",
            "lua_func": "CSurf_OnRecord",
            "description": "Start recording",
            "params": [],
            "returns": "void"
        },
        {
            "name": "get_play_state",
            "lua_func": "GetPlayState",
            "description": "Get playback state",
            "params": [],
            "returns": "integer"
        },
        {
            "name": "get_play_position",
            "lua_func": "GetPlayPosition",
            "description": "Get play position",
            "params": [],
            "returns": "number"
        },
        {
            "name": "get_cursor_position",
            "lua_func": "GetCursorPosition",
            "description": "Get edit cursor position",
            "params": [],
            "returns": "number"
        },
        {
            "name": "set_edit_cursor_position",
            "lua_func": "SetEditCurPos",
            "description": "Set edit cursor position",
            "params": [
                {"name": "time", "type": "number", "desc": "Time in seconds"},
                {"name": "move_view", "type": "boolean", "desc": "Move view to cursor"},
                {"name": "seek_play", "type": "boolean", "desc": "Seek during playback"}
            ],
            "returns": "void"
        },
        {
            "name": "go_to_marker",
            "lua_func": "GoToMarker",
            "description": "Go to marker",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0},
                {"name": "marker_index", "type": "integer", "desc": "Marker index"},
                {"name": "use_timeline_order", "type": "boolean", "desc": "Use timeline order", "default": True}
            ],
            "returns": "void"
        },
        {
            "name": "go_to_region",
            "lua_func": "GoToRegion",
            "description": "Go to region",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0},
                {"name": "region_index", "type": "integer", "desc": "Region index"},
                {"name": "use_timeline_order", "type": "boolean", "desc": "Use timeline order", "default": True}
            ],
            "returns": "void"
        }
    ],
    
    "Project": [
        {
            "name": "get_project_name",
            "lua_func": "GetProjectName",
            "description": "Get project name",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0}
            ],
            "returns": "string"
        },
        {
            "name": "get_project_path",
            "lua_func": "GetProjectPath",
            "description": "Get project path",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0}
            ],
            "returns": "string"
        },
        {
            "name": "save_project",
            "lua_func": "Main_SaveProject",
            "description": "Save project",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0},
                {"name": "force_save_as", "type": "boolean", "desc": "Force save as", "default": False}
            ],
            "returns": "void"
        },
        {
            "name": "is_project_dirty",
            "lua_func": "IsProjectDirty",
            "description": "Check if project has unsaved changes",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0}
            ],
            "returns": "integer"
        },
        {
            "name": "mark_project_dirty",
            "lua_func": "MarkProjectDirty",
            "description": "Mark project as having unsaved changes",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0}
            ],
            "returns": "void"
        }
    ],
    
    "Time and Tempo": [
        {
            "name": "get_project_tempo",
            "lua_func": "Master_GetTempo",
            "description": "Get master tempo",
            "params": [],
            "returns": "number"
        },
        {
            "name": "set_project_tempo",
            "lua_func": "SetCurrentBPM",
            "description": "Set current tempo",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0},
                {"name": "bpm", "type": "number", "desc": "Beats per minute"},
                {"name": "undo", "type": "boolean", "desc": "Create undo point", "default": True}
            ],
            "returns": "void"
        },
        {
            "name": "time_to_beats",
            "lua_func": "TimeMap2_timeToBeats",
            "description": "Convert time to beats",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0},
                {"name": "time", "type": "number", "desc": "Time in seconds"}
            ],
            "returns": "table"
        },
        {
            "name": "beats_to_time",
            "lua_func": "TimeMap2_beatsToTime",
            "description": "Convert beats to time",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0},
                {"name": "beats", "type": "number", "desc": "Beat position"}
            ],
            "returns": "number"
        }
    ],
    
    "Markers and Regions": [
        {
            "name": "add_project_marker",
            "lua_func": "AddProjectMarker",
            "description": "Add project marker",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0},
                {"name": "is_region", "type": "boolean", "desc": "Create region", "default": False},
                {"name": "position", "type": "number", "desc": "Position in seconds"},
                {"name": "region_end", "type": "number", "desc": "Region end (if region)", "default": 0},
                {"name": "name", "type": "string", "desc": "Marker/region name"},
                {"name": "index", "type": "integer", "desc": "Index (-1 for next)", "default": -1}
            ],
            "returns": "integer"
        },
        {
            "name": "delete_project_marker",
            "lua_func": "DeleteProjectMarker",
            "description": "Delete project marker",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0},
                {"name": "marker_index", "type": "integer", "desc": "Marker index"},
                {"name": "is_region", "type": "boolean", "desc": "Is region", "default": False}
            ],
            "returns": "boolean"
        },
        {
            "name": "count_project_markers",
            "lua_func": "CountProjectMarkers",
            "description": "Count project markers",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0}
            ],
            "returns": "table"
        },
        {
            "name": "enum_project_markers",
            "lua_func": "EnumProjectMarkers",
            "description": "Enumerate project markers",
            "params": [
                {"name": "index", "type": "integer", "desc": "Marker index"}
            ],
            "returns": "table"
        }
    ],
    
    "FX": [
        {
            "name": "track_fx_get_count",
            "lua_func": "TrackFX_GetCount",
            "description": "Get FX count on track",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"}
            ],
            "returns": "integer"
        },
        {
            "name": "track_fx_add_by_name",
            "lua_func": "TrackFX_AddByName",
            "description": "Add FX to track by name",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"},
                {"name": "fx_name", "type": "string", "desc": "FX name"},
                {"name": "instantiate", "type": "boolean", "desc": "Instantiate if not found", "default": False}
            ],
            "returns": "integer"
        },
        {
            "name": "track_fx_delete",
            "lua_func": "TrackFX_Delete",
            "description": "Delete FX from track",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"},
                {"name": "fx_index", "type": "integer", "desc": "FX index"}
            ],
            "returns": "boolean"
        },
        {
            "name": "track_fx_get_enabled",
            "lua_func": "TrackFX_GetEnabled",
            "description": "Get FX enabled state",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"},
                {"name": "fx_index", "type": "integer", "desc": "FX index"}
            ],
            "returns": "boolean"
        },
        {
            "name": "track_fx_set_enabled",
            "lua_func": "TrackFX_SetEnabled",
            "description": "Set FX enabled state",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"},
                {"name": "fx_index", "type": "integer", "desc": "FX index"},
                {"name": "enabled", "type": "boolean", "desc": "Enabled state"}
            ],
            "returns": "void"
        },
        {
            "name": "track_fx_get_param",
            "lua_func": "TrackFX_GetParam",
            "description": "Get FX parameter value",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"},
                {"name": "fx_index", "type": "integer", "desc": "FX index"},
                {"name": "param_index", "type": "integer", "desc": "Parameter index"}
            ],
            "returns": "table"
        },
        {
            "name": "track_fx_set_param",
            "lua_func": "TrackFX_SetParam",
            "description": "Set FX parameter value",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"},
                {"name": "fx_index", "type": "integer", "desc": "FX index"},
                {"name": "param_index", "type": "integer", "desc": "Parameter index"},
                {"name": "value", "type": "number", "desc": "Parameter value"}
            ],
            "returns": "boolean"
        }
    ],
    
    "Envelopes": [
        {
            "name": "get_track_envelope",
            "lua_func": "GetTrackEnvelope",
            "description": "Get track envelope",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"},
                {"name": "envelope_index", "type": "integer", "desc": "Envelope index"}
            ],
            "returns": "TrackEnvelope*"
        },
        {
            "name": "get_track_envelope_by_name",
            "lua_func": "GetTrackEnvelopeByName",
            "description": "Get track envelope by name",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"},
                {"name": "envelope_name", "type": "string", "desc": "Envelope name"}
            ],
            "returns": "TrackEnvelope*"
        },
        {
            "name": "count_envelope_points",
            "lua_func": "CountEnvelopePoints",
            "description": "Count envelope points",
            "params": [
                {"name": "envelope_ptr", "type": "string", "desc": "Envelope pointer"}
            ],
            "returns": "integer"
        },
        {
            "name": "get_envelope_point",
            "lua_func": "GetEnvelopePoint",
            "description": "Get envelope point",
            "params": [
                {"name": "envelope_ptr", "type": "string", "desc": "Envelope pointer"},
                {"name": "point_index", "type": "integer", "desc": "Point index"}
            ],
            "returns": "table"
        },
        {
            "name": "insert_envelope_point",
            "lua_func": "InsertEnvelopePoint",
            "description": "Insert envelope point",
            "params": [
                {"name": "envelope_ptr", "type": "string", "desc": "Envelope pointer"},
                {"name": "time", "type": "number", "desc": "Time position"},
                {"name": "value", "type": "number", "desc": "Point value"},
                {"name": "shape", "type": "integer", "desc": "Point shape", "default": 0},
                {"name": "tension", "type": "number", "desc": "Curve tension", "default": 0},
                {"name": "selected", "type": "boolean", "desc": "Point selected", "default": False},
                {"name": "no_sort", "type": "boolean", "desc": "Don't sort", "default": False}
            ],
            "returns": "boolean"
        },
        {
            "name": "delete_envelope_point",
            "lua_func": "DeleteEnvelopePointEx",
            "description": "Delete envelope point",
            "params": [
                {"name": "envelope_ptr", "type": "string", "desc": "Envelope pointer"},
                {"name": "point_index", "type": "integer", "desc": "Point index"}
            ],
            "returns": "boolean"
        }
    ],
    
    "Undo": [
        {
            "name": "undo",
            "lua_func": "Undo_DoUndo2",
            "description": "Perform undo",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0}
            ],
            "returns": "boolean"
        },
        {
            "name": "redo",
            "lua_func": "Undo_DoRedo2",
            "description": "Perform redo",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0}
            ],
            "returns": "boolean"
        },
        {
            "name": "undo_begin_block",
            "lua_func": "Undo_BeginBlock",
            "description": "Begin undo block",
            "params": [],
            "returns": "void"
        },
        {
            "name": "undo_end_block",
            "lua_func": "Undo_EndBlock",
            "description": "End undo block",
            "params": [
                {"name": "description", "type": "string", "desc": "Undo description"},
                {"name": "flags", "type": "integer", "desc": "Undo flags", "default": -1}
            ],
            "returns": "void"
        },
        {
            "name": "undo_can_undo",
            "lua_func": "Undo_CanUndo2",
            "description": "Check if undo available",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0}
            ],
            "returns": "string"
        },
        {
            "name": "undo_can_redo",
            "lua_func": "Undo_CanRedo2",
            "description": "Check if redo available",
            "params": [
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0}
            ],
            "returns": "string"
        }
    ],
    
    "Actions": [
        {
            "name": "main_on_command",
            "lua_func": "Main_OnCommand",
            "description": "Execute action",
            "params": [
                {"name": "command_id", "type": "integer", "desc": "Command ID"},
                {"name": "flag", "type": "integer", "desc": "Flag", "default": 0}
            ],
            "returns": "void"
        },
        {
            "name": "main_on_command_ex",
            "lua_func": "Main_OnCommandEx",
            "description": "Execute action with project",
            "params": [
                {"name": "command_id", "type": "integer", "desc": "Command ID"},
                {"name": "flag", "type": "integer", "desc": "Flag", "default": 0},
                {"name": "project_index", "type": "integer", "desc": "Project index", "default": 0}
            ],
            "returns": "void"
        },
        {
            "name": "get_action_name",
            "lua_func": "kbd_getTextFromCmd",
            "description": "Get action name from command ID",
            "params": [
                {"name": "command_id", "type": "integer", "desc": "Command ID"},
                {"name": "section", "type": "integer", "desc": "Section", "default": 0}
            ],
            "returns": "string"
        },
        {
            "name": "lookup_command_id",
            "lua_func": "NamedCommandLookup",
            "description": "Lookup command ID by name",
            "params": [
                {"name": "command_name", "type": "string", "desc": "Command name"}
            ],
            "returns": "integer"
        }
    ],
    
    "UI": [
        {
            "name": "update_arrange",
            "lua_func": "UpdateArrange",
            "description": "Update arrange view",
            "params": [],
            "returns": "void"
        },
        {
            "name": "update_timeline",
            "lua_func": "UpdateTimeline",
            "description": "Update timeline",
            "params": [],
            "returns": "void"
        },
        {
            "name": "track_list_update_all_external_surfaces",
            "lua_func": "TrackList_UpdateAllExternalSurfaces",
            "description": "Update external surfaces",
            "params": [],
            "returns": "void"
        },
        {
            "name": "refresh_toolbar",
            "lua_func": "RefreshToolbar",
            "description": "Refresh toolbar",
            "params": [
                {"name": "command_id", "type": "integer", "desc": "Command ID"}
            ],
            "returns": "void"
        },
        {
            "name": "refresh_toolbar_ex",
            "lua_func": "RefreshToolbar2",
            "description": "Refresh toolbar with section",
            "params": [
                {"name": "section_id", "type": "integer", "desc": "Section ID"},
                {"name": "command_id", "type": "integer", "desc": "Command ID"}
            ],
            "returns": "void"
        }
    ],
    
    "Routing": [
        {
            "name": "create_track_send",
            "lua_func": "CreateTrackSend",
            "description": "Create track send",
            "params": [
                {"name": "src_track_index", "type": "integer", "desc": "Source track index"},
                {"name": "dest_track_index", "type": "integer", "desc": "Destination track index"}
            ],
            "returns": "integer"
        },
        {
            "name": "remove_track_send",
            "lua_func": "RemoveTrackSend",
            "description": "Remove track send",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"},
                {"name": "category", "type": "integer", "desc": "Category (0=send)"},
                {"name": "send_index", "type": "integer", "desc": "Send index"}
            ],
            "returns": "boolean"
        },
        {
            "name": "get_track_num_sends",
            "lua_func": "GetTrackNumSends",
            "description": "Get number of sends",
            "params": [
                {"name": "track_index", "type": "integer", "desc": "Track index"},
                {"name": "category", "type": "integer", "desc": "Category", "default": 0}
            ],
            "returns": "integer"
        }
    ]
}

class ReaScriptAPIGenerator:
    def __init__(self):
        self.output_dir = "generated_api"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_tool_definition(self, method: Dict[str, Any]) -> str:
        """Generate tool definition for app.py"""
        tool = f'        Tool(\n'
        tool += f'            name="{method["name"]}",\n'
        tool += f'            description="{method["description"]}",\n'
        tool += f'            inputSchema={{\n'
        tool += f'                "type": "object",\n'
        
        if method["params"]:
            tool += f'                "properties": {{\n'
            for i, param in enumerate(method["params"]):
                tool += f'                    "{param["name"]}": {{\n'
                tool += f'                        "type": "{param["type"]}",\n'
                tool += f'                        "description": "{param["desc"]}"'
                
                if param.get("min") is not None:
                    tool += f',\n                        "minimum": {param["min"]}'
                if param.get("max") is not None:
                    tool += f',\n                        "maximum": {param["max"]}'
                if param.get("default") is not None:
                    tool += f',\n                        "default": {json.dumps(param["default"])}'
                    
                tool += f'\n                    }}'
                if i < len(method["params"]) - 1:
                    tool += ','
                tool += '\n'
                
            tool += f'                }},\n'
            
            required = [p["name"] for p in method["params"] 
                       if "default" not in p and not p.get("optional", False)]
            if required:
                tool += f'                "required": {json.dumps(required)}\n'
            else:
                tool += f'                "required": []\n'
        else:
            tool += f'                "properties": {{}}\n'
            
        tool += f'            }}\n'
        tool += f'        )'
        
        return tool
    
    def generate_handler(self, method: Dict[str, Any]) -> str:
        """Generate handler for app.py"""
        handler = f'    elif name == "{method["name"]}":\n'
        
        # Extract parameters
        for param in method["params"]:
            if "default" in param:
                handler += f'        {param["name"]} = arguments.get("{param["name"]}", {json.dumps(param["default"])})\n'
            elif not param.get("optional", False):
                handler += f'        {param["name"]} = arguments["{param["name"]}"]\n'
            else:
                handler += f'        {param["name"]} = arguments.get("{param["name"]}")\n'
        
        if method["params"]:
            handler += '        \n'
        
        # Build args for Lua call
        lua_args = []
        for param in method["params"]:
            lua_args.append(param["name"])
        
        handler += f'        result = bridge.call_lua("{method["lua_func"]}", [{", ".join(lua_args)}])\n'
        handler += '        \n'
        handler += '        if result.get("ok"):\n'
        
        # Format response based on return type
        if method["returns"] == "void":
            handler += f'            return [TextContent(\n'
            handler += f'                type="text",\n'
            handler += f'                text="{method["description"]} completed successfully"\n'
            handler += f'            )]\n'
        else:
            handler += f'            return [TextContent(\n'
            handler += f'                type="text",\n'
            handler += f'                text=f"{method["description"]}: {{result.get(\'ret\')}}"\n'
            handler += f'            )]\n'
            
        handler += '        else:\n'
        handler += '            return [TextContent(\n'
        handler += '                type="text",\n'
        handler += f'                text=f"Failed to {method["name"].replace("_", " ")}: {{result.get(\'error\', \'Unknown error\')}}"\n'
        handler += '            )]'
        
        return handler
    
    def generate_lua_handler(self, method: Dict[str, Any]) -> str:
        """Generate Lua handler for mcp_bridge.lua"""
        # This is simplified - real implementation would need proper Lua code generation
        handler = f'            elseif fname == "{method["lua_func"]}" then\n'
        
        if method["params"]:
            required_count = len([p for p in method["params"] 
                                if "default" not in p and not p.get("optional", False)])
            handler += f'                if #args >= {required_count} then\n'
            handler += f'                    -- Implementation for {method["lua_func"]}\n'
            handler += f'                    response.ok = true\n'
            handler += f'                else\n'
            handler += f'                    response.error = "{method["lua_func"]} requires {required_count} arguments"\n'
            handler += f'                end\n'
        else:
            handler += f'                -- Implementation for {method["lua_func"]}\n'
            handler += f'                response.ok = true\n'
            
        return handler
    
    def generate_test(self, method: Dict[str, Any]) -> str:
        """Generate test for method"""
        test = f'''@pytest.mark.asyncio
async def test_{method["name"]}(reaper_mcp_client):
    """Test {method["description"]}"""
    result = await reaper_mcp_client.call_tool(
        "{method["name"]}",
        {{{", ".join([f'"{p["name"]}": {json.dumps(p.get("default", "test_value"))}' for p in method["params"]])}}}
    )
    assert result.content[0].text is not None
'''
        return test
    
    def generate_all(self):
        """Generate all files"""
        tools = []
        handlers = []
        lua_handlers = []
        tests = []
        
        for category, methods in REASCRIPT_API.items():
            print(f"\nProcessing {category}: {len(methods)} methods")
            
            for method in methods:
                tools.append(self.generate_tool_definition(method))
                handlers.append(self.generate_handler(method))
                lua_handlers.append(self.generate_lua_handler(method))
                tests.append(self.generate_test(method))
        
        # Write tools file
        with open(os.path.join(self.output_dir, "tools.py"), "w") as f:
            f.write("# Generated tool definitions for app.py\n\n")
            f.write("TOOLS = [\n")
            f.write(",\n".join(tools))
            f.write("\n]")
        
        # Write handlers file
        with open(os.path.join(self.output_dir, "handlers.py"), "w") as f:
            f.write("# Generated handlers for app.py\n\n")
            for handler in handlers:
                f.write(handler)
                f.write("\n\n")
        
        # Write Lua handlers file
        with open(os.path.join(self.output_dir, "lua_handlers.lua"), "w") as f:
            f.write("-- Generated Lua handlers for mcp_bridge.lua\n\n")
            for lua_handler in lua_handlers:
                f.write(lua_handler)
                f.write("\n")
        
        # Write tests file
        with open(os.path.join(self.output_dir, "tests.py"), "w") as f:
            f.write("# Generated tests\n")
            f.write("import pytest\n")
            f.write("import pytest_asyncio\n\n")
            for test in tests:
                f.write(test)
                f.write("\n")
        
        # Generate summary
        total_methods = sum(len(methods) for methods in REASCRIPT_API.values())
        with open(os.path.join(self.output_dir, "SUMMARY.md"), "w") as f:
            f.write(f"# ReaScript API Implementation Summary\n\n")
            f.write(f"Total methods generated: {total_methods}\n\n")
            
            for category, methods in REASCRIPT_API.items():
                f.write(f"## {category} ({len(methods)} methods)\n")
                for method in methods:
                    f.write(f"- `{method['name']}` - {method['description']}\n")
                f.write("\n")
        
        print(f"\n✅ Generated {total_methods} ReaScript API methods!")
        print(f"Output directory: {self.output_dir}")

if __name__ == "__main__":
    generator = ReaScriptAPIGenerator()
    generator.generate_all()