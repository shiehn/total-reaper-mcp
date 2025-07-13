# Generated tool definitions for app.py

TOOLS = [
        Tool(
            name="count_tracks",
            description="Count tracks in project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_track",
            description="Get track by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    },
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="get_master_track",
            description="Get master track",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_track_name",
            description="Get track name",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_name",
            description="Set track name",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "name": {
                        "type": "string",
                        "description": "New track name"
                    }
                },
                "required": ["track_index", "name"]
            }
        ),
        Tool(
            name="insert_track_at_index",
            description="Insert new track at index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "Index to insert at"
                    },
                    "use_defaults": {
                        "type": "boolean",
                        "description": "Use default track settings",
                        "default": true
                    }
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="delete_track",
            description="Delete track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index to delete"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="get_track_mute",
            description="Get track mute state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_mute",
            description="Set track mute state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "mute": {
                        "type": "boolean",
                        "description": "Mute state"
                    }
                },
                "required": ["track_index", "mute"]
            }
        ),
        Tool(
            name="get_track_solo",
            description="Get track solo state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_solo",
            description="Set track solo state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "solo": {
                        "type": "boolean",
                        "description": "Solo state"
                    }
                },
                "required": ["track_index", "solo"]
            }
        ),
        Tool(
            name="get_track_volume",
            description="Get track volume",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_volume",
            description="Set track volume",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "volume_db": {
                        "type": "number",
                        "description": "Volume in dB"
                    }
                },
                "required": ["track_index", "volume_db"]
            }
        ),
        Tool(
            name="get_track_pan",
            description="Get track pan",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_pan",
            description="Set track pan",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "pan": {
                        "type": "number",
                        "description": "Pan value (-1 to 1)"
                    }
                },
                "required": ["track_index", "pan"]
            }
        ),
        Tool(
            name="get_track_color",
            description="Get track color",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_color",
            description="Set track color",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "color": {
                        "type": "integer",
                        "description": "RGB color value"
                    }
                },
                "required": ["track_index", "color"]
            }
        ),
        Tool(
            name="count_media_items",
            description="Count media items in project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_media_item",
            description="Get media item by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    },
                    "item_index": {
                        "type": "integer",
                        "description": "Item index (0-based)"
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="add_media_item_to_track",
            description="Add new media item to track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="delete_media_item",
            description="Delete media item from track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "item_index": {
                        "type": "integer",
                        "description": "Item index on track"
                    }
                },
                "required": ["track_index", "item_index"]
            }
        ),
        Tool(
            name="get_media_item_position",
            description="Get media item position",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index (0-based)"
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="set_media_item_position",
            description="Set media item position",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index (0-based)"
                    },
                    "position": {
                        "type": "number",
                        "description": "Position in seconds"
                    }
                },
                "required": ["item_index", "position"]
            }
        ),
        Tool(
            name="get_media_item_length",
            description="Get media item length",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index (0-based)"
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="set_media_item_length",
            description="Set media item length",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index (0-based)"
                    },
                    "length": {
                        "type": "number",
                        "description": "Length in seconds"
                    }
                },
                "required": ["item_index", "length"]
            }
        ),
        Tool(
            name="create_midi_item",
            description="Create new MIDI item",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index (0-based)"
                    },
                    "start_time": {
                        "type": "number",
                        "description": "Start time in seconds"
                    },
                    "end_time": {
                        "type": "number",
                        "description": "End time in seconds"
                    },
                    "qn": {
                        "type": "boolean",
                        "description": "Use quarter notes",
                        "default": false
                    }
                },
                "required": ["track_index", "start_time", "end_time"]
            }
        ),
        Tool(
            name="count_takes",
            description="Count takes in media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index (0-based)"
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="get_take",
            description="Get take from media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index (0-based)"
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "Take index (0-based)"
                    }
                },
                "required": ["item_index", "take_index"]
            }
        ),
        Tool(
            name="get_active_take",
            description="Get active take from media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index (0-based)"
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="set_active_take",
            description="Set active take for media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_ptr": {
                        "type": "string",
                        "description": "Take pointer"
                    }
                },
                "required": ["take_ptr"]
            }
        ),
        Tool(
            name="add_take_to_item",
            description="Add new take to media item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Item index (0-based)"
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="midi_insert_note",
            description="Insert MIDI note",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_ptr": {
                        "type": "string",
                        "description": "Take pointer"
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Note selected",
                        "default": false
                    },
                    "muted": {
                        "type": "boolean",
                        "description": "Note muted",
                        "default": false
                    },
                    "start_ppq": {
                        "type": "number",
                        "description": "Start position in PPQ"
                    },
                    "end_ppq": {
                        "type": "number",
                        "description": "End position in PPQ"
                    },
                    "channel": {
                        "type": "integer",
                        "description": "MIDI channel (0-15)",
                        "default": 0
                    },
                    "pitch": {
                        "type": "integer",
                        "description": "MIDI pitch (0-127)"
                    },
                    "velocity": {
                        "type": "integer",
                        "description": "Velocity (0-127)",
                        "default": 100
                    },
                    "no_sort": {
                        "type": "boolean",
                        "description": "Don't sort after insert",
                        "default": false
                    }
                },
                "required": ["take_ptr", "start_ppq", "end_ppq", "pitch"]
            }
        ),
        Tool(
            name="midi_delete_note",
            description="Delete MIDI note",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_ptr": {
                        "type": "string",
                        "description": "Take pointer"
                    },
                    "note_index": {
                        "type": "integer",
                        "description": "Note index to delete"
                    }
                },
                "required": ["take_ptr", "note_index"]
            }
        ),
        Tool(
            name="midi_count_events",
            description="Count MIDI events in take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_ptr": {
                        "type": "string",
                        "description": "Take pointer"
                    }
                },
                "required": ["take_ptr"]
            }
        ),
        Tool(
            name="midi_get_note",
            description="Get MIDI note info",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_ptr": {
                        "type": "string",
                        "description": "Take pointer"
                    },
                    "note_index": {
                        "type": "integer",
                        "description": "Note index"
                    }
                },
                "required": ["take_ptr", "note_index"]
            }
        ),
        Tool(
            name="midi_set_note",
            description="Set MIDI note properties",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_ptr": {
                        "type": "string",
                        "description": "Take pointer"
                    },
                    "note_index": {
                        "type": "integer",
                        "description": "Note index"
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Note selected"
                    },
                    "muted": {
                        "type": "boolean",
                        "description": "Note muted"
                    },
                    "start_ppq": {
                        "type": "number",
                        "description": "Start position in PPQ"
                    },
                    "end_ppq": {
                        "type": "number",
                        "description": "End position in PPQ"
                    },
                    "channel": {
                        "type": "integer",
                        "description": "MIDI channel"
                    },
                    "pitch": {
                        "type": "integer",
                        "description": "MIDI pitch"
                    },
                    "velocity": {
                        "type": "integer",
                        "description": "Velocity"
                    },
                    "no_sort": {
                        "type": "boolean",
                        "description": "Don't sort",
                        "default": false
                    }
                },
                "required": ["take_ptr", "note_index"]
            }
        ),
        Tool(
            name="midi_sort",
            description="Sort MIDI events",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_ptr": {
                        "type": "string",
                        "description": "Take pointer"
                    }
                },
                "required": ["take_ptr"]
            }
        ),
        Tool(
            name="midi_insert_cc",
            description="Insert MIDI CC event",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_ptr": {
                        "type": "string",
                        "description": "Take pointer"
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "CC selected",
                        "default": false
                    },
                    "muted": {
                        "type": "boolean",
                        "description": "CC muted",
                        "default": false
                    },
                    "ppq_pos": {
                        "type": "number",
                        "description": "Position in PPQ"
                    },
                    "type": {
                        "type": "integer",
                        "description": "Message type"
                    },
                    "channel": {
                        "type": "integer",
                        "description": "MIDI channel (0-15)"
                    },
                    "msg2": {
                        "type": "integer",
                        "description": "CC number or note"
                    },
                    "msg3": {
                        "type": "integer",
                        "description": "CC value or velocity"
                    }
                },
                "required": ["take_ptr", "ppq_pos", "type", "channel", "msg2", "msg3"]
            }
        ),
        Tool(
            name="midi_get_ppq_pos_from_proj_time",
            description="Convert project time to PPQ",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_ptr": {
                        "type": "string",
                        "description": "Take pointer"
                    },
                    "time": {
                        "type": "number",
                        "description": "Time in seconds"
                    }
                },
                "required": ["take_ptr", "time"]
            }
        ),
        Tool(
            name="midi_get_proj_time_from_ppq_pos",
            description="Convert PPQ to project time",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_ptr": {
                        "type": "string",
                        "description": "Take pointer"
                    },
                    "ppq": {
                        "type": "number",
                        "description": "Position in PPQ"
                    }
                },
                "required": ["take_ptr", "ppq"]
            }
        ),
        Tool(
            name="play",
            description="Start playback",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="stop",
            description="Stop playback",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="pause",
            description="Pause playback",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="record",
            description="Start recording",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_play_state",
            description="Get playback state",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_play_position",
            description="Get play position",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_cursor_position",
            description="Get edit cursor position",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_edit_cursor_position",
            description="Set edit cursor position",
            inputSchema={
                "type": "object",
                "properties": {
                    "time": {
                        "type": "number",
                        "description": "Time in seconds"
                    },
                    "move_view": {
                        "type": "boolean",
                        "description": "Move view to cursor"
                    },
                    "seek_play": {
                        "type": "boolean",
                        "description": "Seek during playback"
                    }
                },
                "required": ["time", "move_view", "seek_play"]
            }
        ),
        Tool(
            name="go_to_marker",
            description="Go to marker",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    },
                    "marker_index": {
                        "type": "integer",
                        "description": "Marker index"
                    },
                    "use_timeline_order": {
                        "type": "boolean",
                        "description": "Use timeline order",
                        "default": true
                    }
                },
                "required": ["marker_index"]
            }
        ),
        Tool(
            name="go_to_region",
            description="Go to region",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    },
                    "region_index": {
                        "type": "integer",
                        "description": "Region index"
                    },
                    "use_timeline_order": {
                        "type": "boolean",
                        "description": "Use timeline order",
                        "default": true
                    }
                },
                "required": ["region_index"]
            }
        ),
        Tool(
            name="get_project_name",
            description="Get project name",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_project_path",
            description="Get project path",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="save_project",
            description="Save project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    },
                    "force_save_as": {
                        "type": "boolean",
                        "description": "Force save as",
                        "default": false
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="is_project_dirty",
            description="Check if project has unsaved changes",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="mark_project_dirty",
            description="Mark project as having unsaved changes",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_project_tempo",
            description="Get master tempo",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="set_project_tempo",
            description="Set current tempo",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    },
                    "bpm": {
                        "type": "number",
                        "description": "Beats per minute"
                    },
                    "undo": {
                        "type": "boolean",
                        "description": "Create undo point",
                        "default": true
                    }
                },
                "required": ["bpm"]
            }
        ),
        Tool(
            name="time_to_beats",
            description="Convert time to beats",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    },
                    "time": {
                        "type": "number",
                        "description": "Time in seconds"
                    }
                },
                "required": ["time"]
            }
        ),
        Tool(
            name="beats_to_time",
            description="Convert beats to time",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    },
                    "beats": {
                        "type": "number",
                        "description": "Beat position"
                    }
                },
                "required": ["beats"]
            }
        ),
        Tool(
            name="add_project_marker",
            description="Add project marker",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    },
                    "is_region": {
                        "type": "boolean",
                        "description": "Create region",
                        "default": false
                    },
                    "position": {
                        "type": "number",
                        "description": "Position in seconds"
                    },
                    "region_end": {
                        "type": "number",
                        "description": "Region end (if region)",
                        "default": 0
                    },
                    "name": {
                        "type": "string",
                        "description": "Marker/region name"
                    },
                    "index": {
                        "type": "integer",
                        "description": "Index (-1 for next)",
                        "default": -1
                    }
                },
                "required": ["position", "name"]
            }
        ),
        Tool(
            name="delete_project_marker",
            description="Delete project marker",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    },
                    "marker_index": {
                        "type": "integer",
                        "description": "Marker index"
                    },
                    "is_region": {
                        "type": "boolean",
                        "description": "Is region",
                        "default": false
                    }
                },
                "required": ["marker_index"]
            }
        ),
        Tool(
            name="count_project_markers",
            description="Count project markers",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="enum_project_markers",
            description="Enumerate project markers",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "Marker index"
                    }
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="track_fx_get_count",
            description="Get FX count on track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="track_fx_add_by_name",
            description="Add FX to track by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "fx_name": {
                        "type": "string",
                        "description": "FX name"
                    },
                    "instantiate": {
                        "type": "boolean",
                        "description": "Instantiate if not found",
                        "default": false
                    }
                },
                "required": ["track_index", "fx_name"]
            }
        ),
        Tool(
            name="track_fx_delete",
            description="Delete FX from track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "fx_index": {
                        "type": "integer",
                        "description": "FX index"
                    }
                },
                "required": ["track_index", "fx_index"]
            }
        ),
        Tool(
            name="track_fx_get_enabled",
            description="Get FX enabled state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "fx_index": {
                        "type": "integer",
                        "description": "FX index"
                    }
                },
                "required": ["track_index", "fx_index"]
            }
        ),
        Tool(
            name="track_fx_set_enabled",
            description="Set FX enabled state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "fx_index": {
                        "type": "integer",
                        "description": "FX index"
                    },
                    "enabled": {
                        "type": "boolean",
                        "description": "Enabled state"
                    }
                },
                "required": ["track_index", "fx_index", "enabled"]
            }
        ),
        Tool(
            name="track_fx_get_param",
            description="Get FX parameter value",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "fx_index": {
                        "type": "integer",
                        "description": "FX index"
                    },
                    "param_index": {
                        "type": "integer",
                        "description": "Parameter index"
                    }
                },
                "required": ["track_index", "fx_index", "param_index"]
            }
        ),
        Tool(
            name="track_fx_set_param",
            description="Set FX parameter value",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "fx_index": {
                        "type": "integer",
                        "description": "FX index"
                    },
                    "param_index": {
                        "type": "integer",
                        "description": "Parameter index"
                    },
                    "value": {
                        "type": "number",
                        "description": "Parameter value"
                    }
                },
                "required": ["track_index", "fx_index", "param_index", "value"]
            }
        ),
        Tool(
            name="get_track_envelope",
            description="Get track envelope",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "envelope_index": {
                        "type": "integer",
                        "description": "Envelope index"
                    }
                },
                "required": ["track_index", "envelope_index"]
            }
        ),
        Tool(
            name="get_track_envelope_by_name",
            description="Get track envelope by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "envelope_name": {
                        "type": "string",
                        "description": "Envelope name"
                    }
                },
                "required": ["track_index", "envelope_name"]
            }
        ),
        Tool(
            name="count_envelope_points",
            description="Count envelope points",
            inputSchema={
                "type": "object",
                "properties": {
                    "envelope_ptr": {
                        "type": "string",
                        "description": "Envelope pointer"
                    }
                },
                "required": ["envelope_ptr"]
            }
        ),
        Tool(
            name="get_envelope_point",
            description="Get envelope point",
            inputSchema={
                "type": "object",
                "properties": {
                    "envelope_ptr": {
                        "type": "string",
                        "description": "Envelope pointer"
                    },
                    "point_index": {
                        "type": "integer",
                        "description": "Point index"
                    }
                },
                "required": ["envelope_ptr", "point_index"]
            }
        ),
        Tool(
            name="insert_envelope_point",
            description="Insert envelope point",
            inputSchema={
                "type": "object",
                "properties": {
                    "envelope_ptr": {
                        "type": "string",
                        "description": "Envelope pointer"
                    },
                    "time": {
                        "type": "number",
                        "description": "Time position"
                    },
                    "value": {
                        "type": "number",
                        "description": "Point value"
                    },
                    "shape": {
                        "type": "integer",
                        "description": "Point shape",
                        "default": 0
                    },
                    "tension": {
                        "type": "number",
                        "description": "Curve tension",
                        "default": 0
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Point selected",
                        "default": false
                    },
                    "no_sort": {
                        "type": "boolean",
                        "description": "Don't sort",
                        "default": false
                    }
                },
                "required": ["envelope_ptr", "time", "value"]
            }
        ),
        Tool(
            name="delete_envelope_point",
            description="Delete envelope point",
            inputSchema={
                "type": "object",
                "properties": {
                    "envelope_ptr": {
                        "type": "string",
                        "description": "Envelope pointer"
                    },
                    "point_index": {
                        "type": "integer",
                        "description": "Point index"
                    }
                },
                "required": ["envelope_ptr", "point_index"]
            }
        ),
        Tool(
            name="undo",
            description="Perform undo",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="redo",
            description="Perform redo",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="undo_begin_block",
            description="Begin undo block",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="undo_end_block",
            description="End undo block",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Undo description"
                    },
                    "flags": {
                        "type": "integer",
                        "description": "Undo flags",
                        "default": -1
                    }
                },
                "required": ["description"]
            }
        ),
        Tool(
            name="undo_can_undo",
            description="Check if undo available",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="undo_can_redo",
            description="Check if redo available",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="main_on_command",
            description="Execute action",
            inputSchema={
                "type": "object",
                "properties": {
                    "command_id": {
                        "type": "integer",
                        "description": "Command ID"
                    },
                    "flag": {
                        "type": "integer",
                        "description": "Flag",
                        "default": 0
                    }
                },
                "required": ["command_id"]
            }
        ),
        Tool(
            name="main_on_command_ex",
            description="Execute action with project",
            inputSchema={
                "type": "object",
                "properties": {
                    "command_id": {
                        "type": "integer",
                        "description": "Command ID"
                    },
                    "flag": {
                        "type": "integer",
                        "description": "Flag",
                        "default": 0
                    },
                    "project_index": {
                        "type": "integer",
                        "description": "Project index",
                        "default": 0
                    }
                },
                "required": ["command_id"]
            }
        ),
        Tool(
            name="get_action_name",
            description="Get action name from command ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "command_id": {
                        "type": "integer",
                        "description": "Command ID"
                    },
                    "section": {
                        "type": "integer",
                        "description": "Section",
                        "default": 0
                    }
                },
                "required": ["command_id"]
            }
        ),
        Tool(
            name="lookup_command_id",
            description="Lookup command ID by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "command_name": {
                        "type": "string",
                        "description": "Command name"
                    }
                },
                "required": ["command_name"]
            }
        ),
        Tool(
            name="update_arrange",
            description="Update arrange view",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="update_timeline",
            description="Update timeline",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="track_list_update_all_external_surfaces",
            description="Update external surfaces",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="refresh_toolbar",
            description="Refresh toolbar",
            inputSchema={
                "type": "object",
                "properties": {
                    "command_id": {
                        "type": "integer",
                        "description": "Command ID"
                    }
                },
                "required": ["command_id"]
            }
        ),
        Tool(
            name="refresh_toolbar_ex",
            description="Refresh toolbar with section",
            inputSchema={
                "type": "object",
                "properties": {
                    "section_id": {
                        "type": "integer",
                        "description": "Section ID"
                    },
                    "command_id": {
                        "type": "integer",
                        "description": "Command ID"
                    }
                },
                "required": ["section_id", "command_id"]
            }
        ),
        Tool(
            name="create_track_send",
            description="Create track send",
            inputSchema={
                "type": "object",
                "properties": {
                    "src_track_index": {
                        "type": "integer",
                        "description": "Source track index"
                    },
                    "dest_track_index": {
                        "type": "integer",
                        "description": "Destination track index"
                    }
                },
                "required": ["src_track_index", "dest_track_index"]
            }
        ),
        Tool(
            name="remove_track_send",
            description="Remove track send",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "category": {
                        "type": "integer",
                        "description": "Category (0=send)"
                    },
                    "send_index": {
                        "type": "integer",
                        "description": "Send index"
                    }
                },
                "required": ["track_index", "category", "send_index"]
            }
        ),
        Tool(
            name="get_track_num_sends",
            description="Get number of sends",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "category": {
                        "type": "integer",
                        "description": "Category",
                        "default": 0
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="count_selected_tracks",
            description="Count selected tracks in project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_selected_track",
            description="Get selected track by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    },
                    "selected_track_index": {
                        "type": "integer",
                        "description": "Selected track index (0-based)"
                    }
                },
                "required": ["selected_track_index"]
            }
        ),
        Tool(
            name="set_track_selected",
            description="Set track selection state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Selection state"
                    }
                },
                "required": ["track_index", "selected"]
            }
        ),
        Tool(
            name="count_selected_media_items",
            description="Count selected media items in project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_selected_media_item",
            description="Get selected media item by index",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    },
                    "selected_item_index": {
                        "type": "integer",
                        "description": "Selected item index (0-based)"
                    }
                },
                "required": ["selected_item_index"]
            }
        ),
        Tool(
            name="set_media_item_selected",
            description="Set media item selection state",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index"
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Selection state"
                    }
                },
                "required": ["item_index", "selected"]
            }
        ),
        Tool(
            name="select_all_media_items",
            description="Select all media items in project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="unselect_all_media_items",
            description="Unselect all media items in project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_media_item_take_source",
            description="Get media source from take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    }
                },
                "required": ["take_index"]
            }
        ),
        Tool(
            name="get_media_source_filename",
            description="Get filename of media source",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_index": {
                        "type": "integer",
                        "description": "Source index"
                    }
                },
                "required": ["source_index"]
            }
        ),
        Tool(
            name="get_media_source_length",
            description="Get length of media source in seconds",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_index": {
                        "type": "integer",
                        "description": "Source index"
                    }
                },
                "required": ["source_index"]
            }
        ),
        Tool(
            name="get_media_source_type",
            description="Get type of media source",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_index": {
                        "type": "integer",
                        "description": "Source index"
                    }
                },
                "required": ["source_index"]
            }
        ),
        Tool(
            name="pcm_source_create_from_file",
            description="Create PCM source from file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "File path"
                    }
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="set_media_item_take_source",
            description="Set media source for take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "source_index": {
                        "type": "integer",
                        "description": "Source index"
                    }
                },
                "required": ["take_index", "source_index"]
            }
        ),
        Tool(
            name="get_media_item_take_peaks",
            description="Get peak data for take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "channel": {
                        "type": "integer",
                        "description": "Channel (0-based)",
                        "default": 0
                    },
                    "sample_rate": {
                        "type": "number",
                        "description": "Sample rate",
                        "default": 1000.0
                    },
                    "start_time": {
                        "type": "number",
                        "description": "Start time",
                        "default": 0.0
                    },
                    "num_samples": {
                        "type": "integer",
                        "description": "Number of samples",
                        "default": 1000
                    }
                },
                "required": ["take_index"]
            }
        ),
        Tool(
            name="get_track_depth",
            description="Get track folder depth",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_folder_state",
            description="Set track folder state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "folder_state": {
                        "type": "integer",
                        "description": "Folder state: 0=normal, 1=folder parent, <0=last in folder"
                    }
                },
                "required": ["track_index", "folder_state"]
            }
        ),
        Tool(
            name="get_track_folder_compact_state",
            description="Get track folder compact state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_folder_compact_state",
            description="Set track folder compact state",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "compact_state": {
                        "type": "integer",
                        "description": "Compact state: 0=open, 1=small, 2=tiny"
                    }
                },
                "required": ["track_index", "compact_state"]
            }
        ),
        Tool(
            name="get_parent_track",
            description="Get parent track of a track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_height",
            description="Set track height in TCP",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Height in pixels"
                    },
                    "lock_height": {
                        "type": "boolean",
                        "description": "Lock height",
                        "default": false
                    }
                },
                "required": ["track_index", "height"]
            }
        ),
        Tool(
            name="main_render_project",
            description="Render project to file",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    },
                    "render_tail_ms": {
                        "type": "integer",
                        "description": "Render tail in milliseconds",
                        "default": 1000
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="freeze_track",
            description="Freeze track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="unfreeze_track",
            description="Unfreeze track",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="is_track_frozen",
            description="Check if track is frozen",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="render_time_selection",
            description="Render time selection to new track",
            inputSchema={
                "type": "object",
                "properties": {
                    "add_to_project": {
                        "type": "boolean",
                        "description": "Add rendered file to project",
                        "default": true
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="apply_fx_to_items",
            description="Apply track FX to items (destructive)",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="midi_get_all_events",
            description="Get all MIDI events from take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    }
                },
                "required": ["take_index"]
            }
        ),
        Tool(
            name="midi_set_all_events",
            description="Set all MIDI events in take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "events_data": {
                        "type": "string",
                        "description": "MIDI events data"
                    }
                },
                "required": ["take_index", "events_data"]
            }
        ),
        Tool(
            name="midi_get_note_name",
            description="Get MIDI note name",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_number": {
                        "type": "integer",
                        "description": "MIDI note number (0-127)"
                    }
                },
                "required": ["note_number"]
            }
        ),
        Tool(
            name="midi_get_scale",
            description="Get MIDI scale info for take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    }
                },
                "required": ["take_index"]
            }
        ),
        Tool(
            name="midi_set_scale",
            description="Set MIDI scale for take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "root": {
                        "type": "integer",
                        "description": "Root note (0=C)"
                    },
                    "scale": {
                        "type": "integer",
                        "description": "Scale type (0=major, 1=minor, etc.)"
                    },
                    "channel": {
                        "type": "integer",
                        "description": "MIDI channel",
                        "default": 0
                    }
                },
                "required": ["take_index", "root", "scale"]
            }
        ),
        Tool(
            name="midi_get_text_sysex_event",
            description="Get text/sysex event from take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "event_index": {
                        "type": "integer",
                        "description": "Event index"
                    }
                },
                "required": ["take_index", "event_index"]
            }
        ),
        Tool(
            name="midi_set_text_sysex_event",
            description="Set text/sysex event in take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "event_index": {
                        "type": "integer",
                        "description": "Event index (-1 for new)"
                    },
                    "selected": {
                        "type": "boolean",
                        "description": "Is selected"
                    },
                    "muted": {
                        "type": "boolean",
                        "description": "Is muted"
                    },
                    "ppq_pos": {
                        "type": "number",
                        "description": "Position in PPQ"
                    },
                    "type": {
                        "type": "integer",
                        "description": "Event type"
                    },
                    "message": {
                        "type": "string",
                        "description": "Event message"
                    }
                },
                "required": ["take_index", "event_index", "selected", "muted", "ppq_pos", "type", "message"]
            }
        ),
        Tool(
            name="midi_count_events",
            description="Count MIDI events in take",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    }
                },
                "required": ["take_index"]
            }
        ),
        Tool(
            name="midi_enum_sel_notes",
            description="Enumerate selected MIDI notes",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "note_index": {
                        "type": "integer",
                        "description": "Selected note index"
                    }
                },
                "required": ["take_index", "note_index"]
            }
        ),
        Tool(
            name="midi_select_all",
            description="Select all MIDI events",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "select_notes": {
                        "type": "boolean",
                        "description": "Select notes",
                        "default": true
                    },
                    "select_cc": {
                        "type": "boolean",
                        "description": "Select CC",
                        "default": true
                    },
                    "select_text": {
                        "type": "boolean",
                        "description": "Select text/sysex",
                        "default": true
                    }
                },
                "required": ["take_index"]
            }
        ),
        Tool(
            name="get_resource_path",
            description="Get REAPER resource path",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_exe_path",
            description="Get REAPER executable path",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="recursive_create_directory",
            description="Recursively create directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to create"
                    },
                    "mode": {
                        "type": "integer",
                        "description": "Directory permissions mode",
                        "default": 0
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="get_project_path",
            description="Get project directory path",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_project_state_change_count",
            description="Get project state change count",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_track_state_chunk",
            description="Get track state chunk",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "is_undo": {
                        "type": "boolean",
                        "description": "Is for undo",
                        "default": false
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="set_track_state_chunk",
            description="Set track state chunk",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "state_chunk": {
                        "type": "string",
                        "description": "State chunk string"
                    },
                    "is_undo": {
                        "type": "boolean",
                        "description": "Is for undo",
                        "default": false
                    }
                },
                "required": ["track_index", "state_chunk"]
            }
        ),
        Tool(
            name="browse_for_file",
            description="Open file browser dialog",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Dialog title"
                    },
                    "extension": {
                        "type": "string",
                        "description": "File extension filter"
                    }
                },
                "required": ["title", "extension"]
            }
        ),
        Tool(
            name="show_console_msg",
            description="Show message in REAPER console",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to display"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="clear_console",
            description="Clear REAPER console",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="show_message_box",
            description="Show message box dialog",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to display"
                    },
                    "title": {
                        "type": "string",
                        "description": "Dialog title"
                    },
                    "type": {
                        "type": "integer",
                        "description": "Message box type (0=OK, 1=OK/Cancel, etc.)",
                        "default": 0
                    }
                },
                "required": ["message", "title"]
            }
        ),
        Tool(
            name="get_main_hwnd",
            description="Get main window handle",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="dock_window_add",
            description="Add dock window",
            inputSchema={
                "type": "object",
                "properties": {
                    "hwnd": {
                        "type": "string",
                        "description": "Window handle"
                    },
                    "name": {
                        "type": "string",
                        "description": "Dock name"
                    },
                    "pos": {
                        "type": "integer",
                        "description": "Dock position"
                    },
                    "allow_show": {
                        "type": "boolean",
                        "description": "Allow show",
                        "default": true
                    }
                },
                "required": ["hwnd", "name", "pos"]
            }
        ),
        Tool(
            name="get_mouse_position",
            description="Get current mouse position",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_cursor_context",
            description="Get cursor context",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_media_item_info_value",
            description="Get media item property value",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index"
                    },
                    "param_name": {
                        "type": "string",
                        "description": "Parameter name (D_POSITION, D_LENGTH, etc.)"
                    }
                },
                "required": ["item_index", "param_name"]
            }
        ),
        Tool(
            name="set_media_item_info_value",
            description="Set media item property value",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index"
                    },
                    "param_name": {
                        "type": "string",
                        "description": "Parameter name (D_POSITION, D_LENGTH, etc.)"
                    },
                    "value": {
                        "type": "number",
                        "description": "New value"
                    }
                },
                "required": ["item_index", "param_name", "value"]
            }
        ),
        Tool(
            name="get_take_name",
            description="Get take name",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    }
                },
                "required": ["take_index"]
            }
        ),
        Tool(
            name="set_take_name",
            description="Set take name",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "name": {
                        "type": "string",
                        "description": "New take name"
                    }
                },
                "required": ["take_index", "name"]
            }
        ),
        Tool(
            name="get_media_item_take_info_value",
            description="Get take property value",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "param_name": {
                        "type": "string",
                        "description": "Parameter name (D_STARTOFFS, D_VOL, etc.)"
                    }
                },
                "required": ["take_index", "param_name"]
            }
        ),
        Tool(
            name="set_media_item_take_info_value",
            description="Set take property value",
            inputSchema={
                "type": "object",
                "properties": {
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "param_name": {
                        "type": "string",
                        "description": "Parameter name (D_STARTOFFS, D_VOL, etc.)"
                    },
                    "value": {
                        "type": "number",
                        "description": "New value"
                    }
                },
                "required": ["take_index", "param_name", "value"]
            }
        ),
        Tool(
            name="get_item_state_chunk",
            description="Get item state chunk",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index"
                    },
                    "is_undo": {
                        "type": "boolean",
                        "description": "Is for undo",
                        "default": false
                    }
                },
                "required": ["item_index"]
            }
        ),
        Tool(
            name="set_item_state_chunk",
            description="Set item state chunk",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index"
                    },
                    "state_chunk": {
                        "type": "string",
                        "description": "State chunk string"
                    },
                    "is_undo": {
                        "type": "boolean",
                        "description": "Is for undo",
                        "default": false
                    }
                },
                "required": ["item_index", "state_chunk"]
            }
        ),
        Tool(
            name="split_media_item",
            description="Split media item at position",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_index": {
                        "type": "integer",
                        "description": "Media item index"
                    },
                    "position": {
                        "type": "number",
                        "description": "Split position in seconds"
                    }
                },
                "required": ["item_index", "position"]
            }
        ),
        Tool(
            name="count_track_envelopes",
            description="Count track envelopes",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    }
                },
                "required": ["track_index"]
            }
        ),
        Tool(
            name="get_track_envelope_by_name",
            description="Get track envelope by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_index": {
                        "type": "integer",
                        "description": "Track index"
                    },
                    "envelope_name": {
                        "type": "string",
                        "description": "Envelope name"
                    }
                },
                "required": ["track_index", "envelope_name"]
            }
        ),
        Tool(
            name="get_envelope_scaling_mode",
            description="Get envelope scaling mode",
            inputSchema={
                "type": "object",
                "properties": {
                    "envelope_index": {
                        "type": "integer",
                        "description": "Envelope index"
                    }
                },
                "required": ["envelope_index"]
            }
        ),
        Tool(
            name="set_envelope_scaling_mode",
            description="Set envelope scaling mode",
            inputSchema={
                "type": "object",
                "properties": {
                    "envelope_index": {
                        "type": "integer",
                        "description": "Envelope index"
                    },
                    "scaling_mode": {
                        "type": "integer",
                        "description": "Scaling mode"
                    }
                },
                "required": ["envelope_index", "scaling_mode"]
            }
        ),
        Tool(
            name="envelope_sort_points",
            description="Sort envelope points by time",
            inputSchema={
                "type": "object",
                "properties": {
                    "envelope_index": {
                        "type": "integer",
                        "description": "Envelope index"
                    }
                },
                "required": ["envelope_index"]
            }
        ),
        Tool(
            name="envelope_sort_points_ex",
            description="Sort envelope points with automation items",
            inputSchema={
                "type": "object",
                "properties": {
                    "envelope_index": {
                        "type": "integer",
                        "description": "Envelope index"
                    },
                    "automation_item_index": {
                        "type": "integer",
                        "description": "Automation item index (-1 for all)",
                        "default": -1
                    }
                },
                "required": ["envelope_index"]
            }
        ),
        Tool(
            name="delete_envelope_point_range",
            description="Delete envelope points in time range",
            inputSchema={
                "type": "object",
                "properties": {
                    "envelope_index": {
                        "type": "integer",
                        "description": "Envelope index"
                    },
                    "start_time": {
                        "type": "number",
                        "description": "Start time"
                    },
                    "end_time": {
                        "type": "number",
                        "description": "End time"
                    }
                },
                "required": ["envelope_index", "start_time", "end_time"]
            }
        ),
        Tool(
            name="scale_from_envelope",
            description="Scale media item from envelope",
            inputSchema={
                "type": "object",
                "properties": {
                    "envelope_index": {
                        "type": "integer",
                        "description": "Envelope index"
                    },
                    "take_index": {
                        "type": "integer",
                        "description": "Take index"
                    },
                    "start_time": {
                        "type": "number",
                        "description": "Start time",
                        "default": 0.0
                    },
                    "end_time": {
                        "type": "number",
                        "description": "End time (-1 for item end)",
                        "default": -1.0
                    }
                },
                "required": ["envelope_index", "take_index"]
            }
        ),
        Tool(
            name="get_project_time_signature2",
            description="Get time signature at position",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    },
                    "position": {
                        "type": "number",
                        "description": "Position in seconds"
                    }
                },
                "required": ["position"]
            }
        ),
        Tool(
            name="set_project_grid",
            description="Set project grid settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    },
                    "division": {
                        "type": "number",
                        "description": "Grid division"
                    },
                    "swing_mode": {
                        "type": "integer",
                        "description": "Swing mode",
                        "default": 0
                    },
                    "swing_amount": {
                        "type": "number",
                        "description": "Swing amount",
                        "default": 0.0
                    }
                },
                "required": ["division"]
            }
        ),
        Tool(
            name="get_set_project_info",
            description="Get or set project info",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    },
                    "param_name": {
                        "type": "string",
                        "description": "Parameter name"
                    },
                    "is_set": {
                        "type": "boolean",
                        "description": "Set mode (true) or get mode (false)",
                        "default": false
                    },
                    "value": {
                        "type": "number",
                        "description": "Value to set (only for set mode)",
                        "default": 0.0
                    }
                },
                "required": ["param_name"]
            }
        ),
        Tool(
            name="get_project_time_offset",
            description="Get project time offset",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    },
                    "rounding": {
                        "type": "boolean",
                        "description": "Apply rounding",
                        "default": false
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="count_project_markers",
            description="Count all markers and regions",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_last_marker_and_cur_region",
            description="Get last marker and current region",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_index": {
                        "type": "integer",
                        "description": "Project index (0=current)",
                        "default": 0
                    },
                    "position": {
                        "type": "number",
                        "description": "Position in seconds"
                    }
                },
                "required": ["position"]
            }
        )
]