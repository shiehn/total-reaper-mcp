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
        )
]