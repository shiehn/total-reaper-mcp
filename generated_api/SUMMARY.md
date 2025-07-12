# ReaScript API Implementation Summary

Total methods generated: 94

## Track Management (17 methods)
- `count_tracks` - Count tracks in project
- `get_track` - Get track by index
- `get_master_track` - Get master track
- `get_track_name` - Get track name
- `set_track_name` - Set track name
- `insert_track_at_index` - Insert new track at index
- `delete_track` - Delete track
- `get_track_mute` - Get track mute state
- `set_track_mute` - Set track mute state
- `get_track_solo` - Get track solo state
- `set_track_solo` - Set track solo state
- `get_track_volume` - Get track volume
- `set_track_volume` - Set track volume
- `get_track_pan` - Get track pan
- `set_track_pan` - Set track pan
- `get_track_color` - Get track color
- `set_track_color` - Set track color

## Media Items (9 methods)
- `count_media_items` - Count media items in project
- `get_media_item` - Get media item by index
- `add_media_item_to_track` - Add new media item to track
- `delete_media_item` - Delete media item from track
- `get_media_item_position` - Get media item position
- `set_media_item_position` - Set media item position
- `get_media_item_length` - Get media item length
- `set_media_item_length` - Set media item length
- `create_midi_item` - Create new MIDI item

## Takes (5 methods)
- `count_takes` - Count takes in media item
- `get_take` - Get take from media item
- `get_active_take` - Get active take from media item
- `set_active_take` - Set active take for media item
- `add_take_to_item` - Add new take to media item

## MIDI (9 methods)
- `midi_insert_note` - Insert MIDI note
- `midi_delete_note` - Delete MIDI note
- `midi_count_events` - Count MIDI events in take
- `midi_get_note` - Get MIDI note info
- `midi_set_note` - Set MIDI note properties
- `midi_sort` - Sort MIDI events
- `midi_insert_cc` - Insert MIDI CC event
- `midi_get_ppq_pos_from_proj_time` - Convert project time to PPQ
- `midi_get_proj_time_from_ppq_pos` - Convert PPQ to project time

## Transport (10 methods)
- `play` - Start playback
- `stop` - Stop playback
- `pause` - Pause playback
- `record` - Start recording
- `get_play_state` - Get playback state
- `get_play_position` - Get play position
- `get_cursor_position` - Get edit cursor position
- `set_edit_cursor_position` - Set edit cursor position
- `go_to_marker` - Go to marker
- `go_to_region` - Go to region

## Project (5 methods)
- `get_project_name` - Get project name
- `get_project_path` - Get project path
- `save_project` - Save project
- `is_project_dirty` - Check if project has unsaved changes
- `mark_project_dirty` - Mark project as having unsaved changes

## Time and Tempo (4 methods)
- `get_project_tempo` - Get master tempo
- `set_project_tempo` - Set current tempo
- `time_to_beats` - Convert time to beats
- `beats_to_time` - Convert beats to time

## Markers and Regions (4 methods)
- `add_project_marker` - Add project marker
- `delete_project_marker` - Delete project marker
- `count_project_markers` - Count project markers
- `enum_project_markers` - Enumerate project markers

## FX (7 methods)
- `track_fx_get_count` - Get FX count on track
- `track_fx_add_by_name` - Add FX to track by name
- `track_fx_delete` - Delete FX from track
- `track_fx_get_enabled` - Get FX enabled state
- `track_fx_set_enabled` - Set FX enabled state
- `track_fx_get_param` - Get FX parameter value
- `track_fx_set_param` - Set FX parameter value

## Envelopes (6 methods)
- `get_track_envelope` - Get track envelope
- `get_track_envelope_by_name` - Get track envelope by name
- `count_envelope_points` - Count envelope points
- `get_envelope_point` - Get envelope point
- `insert_envelope_point` - Insert envelope point
- `delete_envelope_point` - Delete envelope point

## Undo (6 methods)
- `undo` - Perform undo
- `redo` - Perform redo
- `undo_begin_block` - Begin undo block
- `undo_end_block` - End undo block
- `undo_can_undo` - Check if undo available
- `undo_can_redo` - Check if redo available

## Actions (4 methods)
- `main_on_command` - Execute action
- `main_on_command_ex` - Execute action with project
- `get_action_name` - Get action name from command ID
- `lookup_command_id` - Lookup command ID by name

## UI (5 methods)
- `update_arrange` - Update arrange view
- `update_timeline` - Update timeline
- `track_list_update_all_external_surfaces` - Update external surfaces
- `refresh_toolbar` - Refresh toolbar
- `refresh_toolbar_ex` - Refresh toolbar with section

## Routing (3 methods)
- `create_track_send` - Create track send
- `remove_track_send` - Remove track send
- `get_track_num_sends` - Get number of sends

