# Generated handlers for app.py

    elif name == "count_tracks":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("CountTracks", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count tracks in project: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count tracks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track":
        project_index = arguments.get("project_index", 0)
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetTrack", [project_index, track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track by index: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_master_track":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("GetMasterTrack", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get master track: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get master track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_name":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetTrackName", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track name: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_name":
        track_index = arguments["track_index"]
        name = arguments["name"]
        
        result = bridge.call_lua("GetSetMediaTrackInfo_String", [track_index, name])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track name: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "insert_track_at_index":
        index = arguments["index"]
        use_defaults = arguments.get("use_defaults", true)
        
        result = bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Insert new track at index completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to insert track at index: {result.get('error', 'Unknown error')}"
            )]

    elif name == "delete_track":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("DeleteTrack", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Delete track completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_mute":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetMediaTrackInfo_Value", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track mute state: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track mute: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_mute":
        track_index = arguments["track_index"]
        mute = arguments["mute"]
        
        result = bridge.call_lua("SetMediaTrackInfo_Value", [track_index, mute])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track mute state: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track mute: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_solo":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetMediaTrackInfo_Value", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track solo state: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track solo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_solo":
        track_index = arguments["track_index"]
        solo = arguments["solo"]
        
        result = bridge.call_lua("SetMediaTrackInfo_Value", [track_index, solo])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track solo state: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track solo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_volume":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetMediaTrackInfo_Value", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track volume: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track volume: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_volume":
        track_index = arguments["track_index"]
        volume_db = arguments["volume_db"]
        
        result = bridge.call_lua("SetMediaTrackInfo_Value", [track_index, volume_db])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track volume: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track volume: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_pan":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetMediaTrackInfo_Value", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track pan: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track pan: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_pan":
        track_index = arguments["track_index"]
        pan = arguments["pan"]
        
        result = bridge.call_lua("SetMediaTrackInfo_Value", [track_index, pan])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track pan: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track pan: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_color":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetTrackColor", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track color: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track color: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_color":
        track_index = arguments["track_index"]
        color = arguments["color"]
        
        result = bridge.call_lua("SetTrackColor", [track_index, color])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Set track color completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track color: {result.get('error', 'Unknown error')}"
            )]

    elif name == "count_media_items":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("CountMediaItems", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count media items in project: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count media items: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item":
        project_index = arguments.get("project_index", 0)
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("GetMediaItem", [project_index, item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item by index: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item: {result.get('error', 'Unknown error')}"
            )]

    elif name == "add_media_item_to_track":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("AddMediaItemToTrack", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Add new media item to track: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add media item to track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "delete_media_item":
        track_index = arguments["track_index"]
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("DeleteTrackMediaItem", [track_index, item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Delete media item from track: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete media item: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_position":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("GetMediaItemInfo_Value", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item position: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_position":
        item_index = arguments["item_index"]
        position = arguments["position"]
        
        result = bridge.call_lua("SetMediaItemInfo_Value", [item_index, position])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item position: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_length":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("GetMediaItemInfo_Value", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item length: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_length":
        item_index = arguments["item_index"]
        length = arguments["length"]
        
        result = bridge.call_lua("SetMediaItemInfo_Value", [item_index, length])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item length: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "create_midi_item":
        track_index = arguments["track_index"]
        start_time = arguments["start_time"]
        end_time = arguments["end_time"]
        qn = arguments.get("qn", false)
        
        result = bridge.call_lua("CreateNewMIDIItemInProj", [track_index, start_time, end_time, qn])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Create new MIDI item: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create midi item: {result.get('error', 'Unknown error')}"
            )]

    elif name == "count_takes":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("CountTakes", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count takes in media item: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count takes: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_take":
        item_index = arguments["item_index"]
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake", [item_index, take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get take from media item: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get take: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_active_take":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("GetActiveTake", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get active take from media item: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get active take: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_active_take":
        take_ptr = arguments["take_ptr"]
        
        result = bridge.call_lua("SetActiveTake", [take_ptr])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Set active take for media item completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set active take: {result.get('error', 'Unknown error')}"
            )]

    elif name == "add_take_to_item":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("AddTakeToMediaItem", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Add new take to media item: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add take to item: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_insert_note":
        take_ptr = arguments["take_ptr"]
        selected = arguments.get("selected", false)
        muted = arguments.get("muted", false)
        start_ppq = arguments["start_ppq"]
        end_ppq = arguments["end_ppq"]
        channel = arguments.get("channel", 0)
        pitch = arguments["pitch"]
        velocity = arguments.get("velocity", 100)
        no_sort = arguments.get("no_sort", false)
        
        result = bridge.call_lua("MIDI_InsertNote", [take_ptr, selected, muted, start_ppq, end_ppq, channel, pitch, velocity, no_sort])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Insert MIDI note: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi insert note: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_delete_note":
        take_ptr = arguments["take_ptr"]
        note_index = arguments["note_index"]
        
        result = bridge.call_lua("MIDI_DeleteNote", [take_ptr, note_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Delete MIDI note: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi delete note: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_count_events":
        take_ptr = arguments["take_ptr"]
        
        result = bridge.call_lua("MIDI_CountEvts", [take_ptr])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count MIDI events in take: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi count events: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_get_note":
        take_ptr = arguments["take_ptr"]
        note_index = arguments["note_index"]
        
        result = bridge.call_lua("MIDI_GetNote", [take_ptr, note_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get MIDI note info: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi get note: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_set_note":
        take_ptr = arguments["take_ptr"]
        note_index = arguments["note_index"]
        selected = arguments.get("selected")
        muted = arguments.get("muted")
        start_ppq = arguments.get("start_ppq")
        end_ppq = arguments.get("end_ppq")
        channel = arguments.get("channel")
        pitch = arguments.get("pitch")
        velocity = arguments.get("velocity")
        no_sort = arguments.get("no_sort", false)
        
        result = bridge.call_lua("MIDI_SetNote", [take_ptr, note_index, selected, muted, start_ppq, end_ppq, channel, pitch, velocity, no_sort])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set MIDI note properties: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi set note: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_sort":
        take_ptr = arguments["take_ptr"]
        
        result = bridge.call_lua("MIDI_Sort", [take_ptr])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Sort MIDI events completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi sort: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_insert_cc":
        take_ptr = arguments["take_ptr"]
        selected = arguments.get("selected", false)
        muted = arguments.get("muted", false)
        ppq_pos = arguments["ppq_pos"]
        type = arguments["type"]
        channel = arguments["channel"]
        msg2 = arguments["msg2"]
        msg3 = arguments["msg3"]
        
        result = bridge.call_lua("MIDI_InsertCC", [take_ptr, selected, muted, ppq_pos, type, channel, msg2, msg3])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Insert MIDI CC event: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi insert cc: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_get_ppq_pos_from_proj_time":
        take_ptr = arguments["take_ptr"]
        time = arguments["time"]
        
        result = bridge.call_lua("MIDI_GetPPQPosFromProjTime", [take_ptr, time])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Convert project time to PPQ: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi get ppq pos from proj time: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_get_proj_time_from_ppq_pos":
        take_ptr = arguments["take_ptr"]
        ppq = arguments["ppq"]
        
        result = bridge.call_lua("MIDI_GetProjTimeFromPPQPos", [take_ptr, ppq])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Convert PPQ to project time: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi get proj time from ppq pos: {result.get('error', 'Unknown error')}"
            )]

    elif name == "play":
        result = bridge.call_lua("CSurf_OnPlay", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Start playback completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to play: {result.get('error', 'Unknown error')}"
            )]

    elif name == "stop":
        result = bridge.call_lua("CSurf_OnStop", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Stop playback completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to stop: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pause":
        result = bridge.call_lua("CSurf_OnPause", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Pause playback completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to pause: {result.get('error', 'Unknown error')}"
            )]

    elif name == "record":
        result = bridge.call_lua("CSurf_OnRecord", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Start recording completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to record: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_play_state":
        result = bridge.call_lua("GetPlayState", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get playback state: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get play state: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_play_position":
        result = bridge.call_lua("GetPlayPosition", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get play position: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get play position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_cursor_position":
        result = bridge.call_lua("GetCursorPosition", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get edit cursor position: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get cursor position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_edit_cursor_position":
        time = arguments["time"]
        move_view = arguments["move_view"]
        seek_play = arguments["seek_play"]
        
        result = bridge.call_lua("SetEditCurPos", [time, move_view, seek_play])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Set edit cursor position completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set edit cursor position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "go_to_marker":
        project_index = arguments.get("project_index", 0)
        marker_index = arguments["marker_index"]
        use_timeline_order = arguments.get("use_timeline_order", true)
        
        result = bridge.call_lua("GoToMarker", [project_index, marker_index, use_timeline_order])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Go to marker completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to go to marker: {result.get('error', 'Unknown error')}"
            )]

    elif name == "go_to_region":
        project_index = arguments.get("project_index", 0)
        region_index = arguments["region_index"]
        use_timeline_order = arguments.get("use_timeline_order", true)
        
        result = bridge.call_lua("GoToRegion", [project_index, region_index, use_timeline_order])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Go to region completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to go to region: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_project_name":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("GetProjectName", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get project name: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_project_path":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("GetProjectPath", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get project path: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project path: {result.get('error', 'Unknown error')}"
            )]

    elif name == "save_project":
        project_index = arguments.get("project_index", 0)
        force_save_as = arguments.get("force_save_as", false)
        
        result = bridge.call_lua("Main_SaveProject", [project_index, force_save_as])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Save project completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to save project: {result.get('error', 'Unknown error')}"
            )]

    elif name == "is_project_dirty":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("IsProjectDirty", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Check if project has unsaved changes: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to is project dirty: {result.get('error', 'Unknown error')}"
            )]

    elif name == "mark_project_dirty":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("MarkProjectDirty", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Mark project as having unsaved changes completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to mark project dirty: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_project_tempo":
        result = bridge.call_lua("Master_GetTempo", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get master tempo: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project tempo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_project_tempo":
        project_index = arguments.get("project_index", 0)
        bpm = arguments["bpm"]
        undo = arguments.get("undo", true)
        
        result = bridge.call_lua("SetCurrentBPM", [project_index, bpm, undo])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Set current tempo completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set project tempo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "time_to_beats":
        project_index = arguments.get("project_index", 0)
        time = arguments["time"]
        
        result = bridge.call_lua("TimeMap2_timeToBeats", [project_index, time])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Convert time to beats: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to time to beats: {result.get('error', 'Unknown error')}"
            )]

    elif name == "beats_to_time":
        project_index = arguments.get("project_index", 0)
        beats = arguments["beats"]
        
        result = bridge.call_lua("TimeMap2_beatsToTime", [project_index, beats])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Convert beats to time: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to beats to time: {result.get('error', 'Unknown error')}"
            )]

    elif name == "add_project_marker":
        project_index = arguments.get("project_index", 0)
        is_region = arguments.get("is_region", false)
        position = arguments["position"]
        region_end = arguments.get("region_end", 0)
        name = arguments["name"]
        index = arguments.get("index", -1)
        
        result = bridge.call_lua("AddProjectMarker", [project_index, is_region, position, region_end, name, index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Add project marker: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add project marker: {result.get('error', 'Unknown error')}"
            )]

    elif name == "delete_project_marker":
        project_index = arguments.get("project_index", 0)
        marker_index = arguments["marker_index"]
        is_region = arguments.get("is_region", false)
        
        result = bridge.call_lua("DeleteProjectMarker", [project_index, marker_index, is_region])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Delete project marker: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete project marker: {result.get('error', 'Unknown error')}"
            )]

    elif name == "count_project_markers":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("CountProjectMarkers", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count project markers: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count project markers: {result.get('error', 'Unknown error')}"
            )]

    elif name == "enum_project_markers":
        index = arguments["index"]
        
        result = bridge.call_lua("EnumProjectMarkers", [index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Enumerate project markers: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to enum project markers: {result.get('error', 'Unknown error')}"
            )]

    elif name == "track_fx_get_count":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("TrackFX_GetCount", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get FX count on track: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx get count: {result.get('error', 'Unknown error')}"
            )]

    elif name == "track_fx_add_by_name":
        track_index = arguments["track_index"]
        fx_name = arguments["fx_name"]
        instantiate = arguments.get("instantiate", false)
        
        result = bridge.call_lua("TrackFX_AddByName", [track_index, fx_name, instantiate])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Add FX to track by name: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx add by name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "track_fx_delete":
        track_index = arguments["track_index"]
        fx_index = arguments["fx_index"]
        
        result = bridge.call_lua("TrackFX_Delete", [track_index, fx_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Delete FX from track: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx delete: {result.get('error', 'Unknown error')}"
            )]

    elif name == "track_fx_get_enabled":
        track_index = arguments["track_index"]
        fx_index = arguments["fx_index"]
        
        result = bridge.call_lua("TrackFX_GetEnabled", [track_index, fx_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get FX enabled state: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx get enabled: {result.get('error', 'Unknown error')}"
            )]

    elif name == "track_fx_set_enabled":
        track_index = arguments["track_index"]
        fx_index = arguments["fx_index"]
        enabled = arguments["enabled"]
        
        result = bridge.call_lua("TrackFX_SetEnabled", [track_index, fx_index, enabled])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Set FX enabled state completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx set enabled: {result.get('error', 'Unknown error')}"
            )]

    elif name == "track_fx_get_param":
        track_index = arguments["track_index"]
        fx_index = arguments["fx_index"]
        param_index = arguments["param_index"]
        
        result = bridge.call_lua("TrackFX_GetParam", [track_index, fx_index, param_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get FX parameter value: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx get param: {result.get('error', 'Unknown error')}"
            )]

    elif name == "track_fx_set_param":
        track_index = arguments["track_index"]
        fx_index = arguments["fx_index"]
        param_index = arguments["param_index"]
        value = arguments["value"]
        
        result = bridge.call_lua("TrackFX_SetParam", [track_index, fx_index, param_index, value])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set FX parameter value: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx set param: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_envelope":
        track_index = arguments["track_index"]
        envelope_index = arguments["envelope_index"]
        
        result = bridge.call_lua("GetTrackEnvelope", [track_index, envelope_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track envelope: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track envelope: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_envelope_by_name":
        track_index = arguments["track_index"]
        envelope_name = arguments["envelope_name"]
        
        result = bridge.call_lua("GetTrackEnvelopeByName", [track_index, envelope_name])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track envelope by name: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track envelope by name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "count_envelope_points":
        envelope_ptr = arguments["envelope_ptr"]
        
        result = bridge.call_lua("CountEnvelopePoints", [envelope_ptr])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count envelope points: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count envelope points: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_envelope_point":
        envelope_ptr = arguments["envelope_ptr"]
        point_index = arguments["point_index"]
        
        result = bridge.call_lua("GetEnvelopePoint", [envelope_ptr, point_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get envelope point: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get envelope point: {result.get('error', 'Unknown error')}"
            )]

    elif name == "insert_envelope_point":
        envelope_ptr = arguments["envelope_ptr"]
        time = arguments["time"]
        value = arguments["value"]
        shape = arguments.get("shape", 0)
        tension = arguments.get("tension", 0)
        selected = arguments.get("selected", false)
        no_sort = arguments.get("no_sort", false)
        
        result = bridge.call_lua("InsertEnvelopePoint", [envelope_ptr, time, value, shape, tension, selected, no_sort])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Insert envelope point: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to insert envelope point: {result.get('error', 'Unknown error')}"
            )]

    elif name == "delete_envelope_point":
        envelope_ptr = arguments["envelope_ptr"]
        point_index = arguments["point_index"]
        
        result = bridge.call_lua("DeleteEnvelopePointEx", [envelope_ptr, point_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Delete envelope point: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete envelope point: {result.get('error', 'Unknown error')}"
            )]

    elif name == "undo":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("Undo_DoUndo2", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Perform undo: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "redo":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("Undo_DoRedo2", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Perform redo: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to redo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "undo_begin_block":
        result = bridge.call_lua("Undo_BeginBlock", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Begin undo block completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo begin block: {result.get('error', 'Unknown error')}"
            )]

    elif name == "undo_end_block":
        description = arguments["description"]
        flags = arguments.get("flags", -1)
        
        result = bridge.call_lua("Undo_EndBlock", [description, flags])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="End undo block completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo end block: {result.get('error', 'Unknown error')}"
            )]

    elif name == "undo_can_undo":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("Undo_CanUndo2", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Check if undo available: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo can undo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "undo_can_redo":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("Undo_CanRedo2", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Check if redo available: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo can redo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "main_on_command":
        command_id = arguments["command_id"]
        flag = arguments.get("flag", 0)
        
        result = bridge.call_lua("Main_OnCommand", [command_id, flag])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Execute action completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to main on command: {result.get('error', 'Unknown error')}"
            )]

    elif name == "main_on_command_ex":
        command_id = arguments["command_id"]
        flag = arguments.get("flag", 0)
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("Main_OnCommandEx", [command_id, flag, project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Execute action with project completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to main on command ex: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_action_name":
        command_id = arguments["command_id"]
        section = arguments.get("section", 0)
        
        result = bridge.call_lua("kbd_getTextFromCmd", [command_id, section])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get action name from command ID: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get action name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "lookup_command_id":
        command_name = arguments["command_name"]
        
        result = bridge.call_lua("NamedCommandLookup", [command_name])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Lookup command ID by name: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to lookup command id: {result.get('error', 'Unknown error')}"
            )]

    elif name == "update_arrange":
        result = bridge.call_lua("UpdateArrange", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Update arrange view completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to update arrange: {result.get('error', 'Unknown error')}"
            )]

    elif name == "update_timeline":
        result = bridge.call_lua("UpdateTimeline", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Update timeline completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to update timeline: {result.get('error', 'Unknown error')}"
            )]

    elif name == "track_list_update_all_external_surfaces":
        result = bridge.call_lua("TrackList_UpdateAllExternalSurfaces", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Update external surfaces completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track list update all external surfaces: {result.get('error', 'Unknown error')}"
            )]

    elif name == "refresh_toolbar":
        command_id = arguments["command_id"]
        
        result = bridge.call_lua("RefreshToolbar", [command_id])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Refresh toolbar completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to refresh toolbar: {result.get('error', 'Unknown error')}"
            )]

    elif name == "refresh_toolbar_ex":
        section_id = arguments["section_id"]
        command_id = arguments["command_id"]
        
        result = bridge.call_lua("RefreshToolbar2", [section_id, command_id])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Refresh toolbar with section completed successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to refresh toolbar ex: {result.get('error', 'Unknown error')}"
            )]

    elif name == "create_track_send":
        src_track_index = arguments["src_track_index"]
        dest_track_index = arguments["dest_track_index"]
        
        result = bridge.call_lua("CreateTrackSend", [src_track_index, dest_track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Create track send: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create track send: {result.get('error', 'Unknown error')}"
            )]

    elif name == "remove_track_send":
        track_index = arguments["track_index"]
        category = arguments["category"]
        send_index = arguments["send_index"]
        
        result = bridge.call_lua("RemoveTrackSend", [track_index, category, send_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Remove track send: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to remove track send: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_num_sends":
        track_index = arguments["track_index"]
        category = arguments.get("category", 0)
        
        result = bridge.call_lua("GetTrackNumSends", [track_index, category])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get number of sends: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track num sends: {result.get('error', 'Unknown error')}"
            )]

