# Generated handlers for app.py

    elif name == "count_tracks":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("CountTracks", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count tracks in project: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count tracks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_master_track":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("GetMasterTrack", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get master track: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get master track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_name":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetTrackName", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track name: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to insert track at index: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "delete_track":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("DeleteTrack", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Delete track completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_mute":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetMediaTrackInfo_Value", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track mute state: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track mute: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track mute: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_solo":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetMediaTrackInfo_Value", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track solo state: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track solo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track solo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_volume":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetMediaTrackInfo_Value", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track volume: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track volume: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track volume: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_pan":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetMediaTrackInfo_Value", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track pan: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track pan: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track pan: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_color":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetTrackColor", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get track color: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track color: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track color: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "count_media_items":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("CountMediaItems", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count media items in project: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count media items: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "add_media_item_to_track":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("AddMediaItemToTrack", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Add new media item to track: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add media item to track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete media item: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_position":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("GetMediaItemInfo_Value", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item position: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_length":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("GetMediaItemInfo_Value", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item length: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create midi item: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "count_takes":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("CountTakes", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count takes in media item: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count takes: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get take: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_active_take":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("GetActiveTake", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get active take from media item: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get active take: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_active_take":
        take_ptr = arguments["take_ptr"]
        
        result = bridge.call_lua("SetActiveTake", [take_ptr])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Set active take for media item completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set active take: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "add_take_to_item":
        item_index = arguments["item_index"]
        
        result = bridge.call_lua("AddTakeToMediaItem", [item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Add new take to media item: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add take to item: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi insert note: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi delete note: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_count_events":
        take_ptr = arguments["take_ptr"]
        
        result = bridge.call_lua("MIDI_CountEvts", [take_ptr])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count MIDI events in take: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi count events: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi get note: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi set note: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_sort":
        take_ptr = arguments["take_ptr"]
        
        result = bridge.call_lua("MIDI_Sort", [take_ptr])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Sort MIDI events completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi sort: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi insert cc: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi get ppq pos from proj time: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to midi get proj time from ppq pos: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "play":
        result = bridge.call_lua("CSurf_OnPlay", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Start playback completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to play: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "stop":
        result = bridge.call_lua("CSurf_OnStop", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Stop playback completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to stop: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pause":
        result = bridge.call_lua("CSurf_OnPause", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Pause playback completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to pause: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "record":
        result = bridge.call_lua("CSurf_OnRecord", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Start recording completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to record: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_play_state":
        result = bridge.call_lua("GetPlayState", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get playback state: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get play state: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_play_position":
        result = bridge.call_lua("GetPlayPosition", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get play position: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get play position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_cursor_position":
        result = bridge.call_lua("GetCursorPosition", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get edit cursor position: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get cursor position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set edit cursor position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to go to marker: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to go to region: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_project_name":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("GetProjectName", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get project name: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_project_path":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("GetProjectPath", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get project path: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project path: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to save project: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "is_project_dirty":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("IsProjectDirty", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Check if project has unsaved changes: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to is project dirty: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "mark_project_dirty":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("MarkProjectDirty", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Mark project as having unsaved changes completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to mark project dirty: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_project_tempo":
        result = bridge.call_lua("Master_GetTempo", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get master tempo: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project tempo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set project tempo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to time to beats: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to beats to time: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add project marker: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete project marker: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "count_project_markers":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("CountProjectMarkers", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count project markers: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count project markers: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "enum_project_markers":
        index = arguments["index"]
        
        result = bridge.call_lua("EnumProjectMarkers", [index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Enumerate project markers: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to enum project markers: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "track_fx_get_count":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("TrackFX_GetCount", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get FX count on track: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx get count: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx add by name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx delete: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx get enabled: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx set enabled: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx get param: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track fx set param: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track envelope: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track envelope by name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "count_envelope_points":
        envelope_ptr = arguments["envelope_ptr"]
        
        result = bridge.call_lua("CountEnvelopePoints", [envelope_ptr])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count envelope points: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count envelope points: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get envelope point: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to insert envelope point: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to delete envelope point: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "undo":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("Undo_DoUndo2", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Perform undo: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "redo":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("Undo_DoRedo2", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Perform redo: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to redo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "undo_begin_block":
        result = bridge.call_lua("Undo_BeginBlock", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Begin undo block completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo begin block: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo end block: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "undo_can_undo":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("Undo_CanUndo2", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Check if undo available: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo can undo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "undo_can_redo":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("Undo_CanRedo2", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Check if redo available: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to undo can redo: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to main on command: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to main on command ex: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get action name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "lookup_command_id":
        command_name = arguments["command_name"]
        
        result = bridge.call_lua("NamedCommandLookup", [command_name])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Lookup command ID by name: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to lookup command id: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "update_arrange":
        result = bridge.call_lua("UpdateArrange", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Update arrange view completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to update arrange: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "update_timeline":
        result = bridge.call_lua("UpdateTimeline", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Update timeline completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to update timeline: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "track_list_update_all_external_surfaces":
        result = bridge.call_lua("TrackList_UpdateAllExternalSurfaces", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Update external surfaces completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to track list update all external surfaces: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "refresh_toolbar":
        command_id = arguments["command_id"]
        
        result = bridge.call_lua("RefreshToolbar", [command_id])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text="Refresh toolbar completed successfully"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to refresh toolbar: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to refresh toolbar ex: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create track send: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to remove track send: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
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

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track num sends: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "count_selected_tracks":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("CountSelectedTracks", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count selected tracks: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count selected tracks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_selected_track":
        project_index = arguments.get("project_index", 0)
        selected_track_index = arguments["selected_track_index"]
        
        result = bridge.call_lua("GetSelectedTrack", [project_index, selected_track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get selected track: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get selected track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_selected":
        track_index = arguments["track_index"]
        selected = arguments["selected"]
        
        result = bridge.call_lua("SetTrackSelected", [track_index, selected])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track selected: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track selected: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "count_selected_media_items":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("CountSelectedMediaItems", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Count selected media items: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count selected media items: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_selected_media_item":
        project_index = arguments.get("project_index", 0)
        selected_item_index = arguments["selected_item_index"]
        
        result = bridge.call_lua("GetSelectedMediaItem", [project_index, selected_item_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get selected media item: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get selected media item: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_selected":
        item_index = arguments["item_index"]
        selected = arguments["selected"]
        
        result = bridge.call_lua("SetMediaItemSelected", [item_index, selected])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item selected: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item selected: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "select_all_media_items":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("SelectAllMediaItems", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Select all media items: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to select all media items: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "unselect_all_media_items":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("UnselectAllMediaItems", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Unselect all media items: {result.get('ret')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to unselect all media items: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_source":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetMediaItemTake_Source", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Get media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_filename":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceFileName", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source filename: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source filename: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_length":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceLength", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source length: {result.get('ret')} seconds"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source length: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_source_type":
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("GetMediaSourceType", [source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media source type: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media source type: {result.get('error', 'Unknown error')}"
            )]

    elif name == "pcm_source_create_from_file":
        filename = arguments["filename"]
        
        result = bridge.call_lua("PCM_Source_CreateFromFile", [filename])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created PCM source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create PCM source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_source":
        take_index = arguments["take_index"]
        source_index = arguments["source_index"]
        
        result = bridge.call_lua("SetMediaItemTake_Source", [take_index, source_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set media item take source: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set media item take source: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_peaks":
        take_index = arguments["take_index"]
        channel = arguments.get("channel", 0)
        sample_rate = arguments.get("sample_rate", 1000.0)
        start_time = arguments.get("start_time", 0.0)
        num_samples = arguments.get("num_samples", 1000)
        
        result = bridge.call_lua("GetMediaItemTake_Peaks", [take_index, channel, sample_rate, start_time, num_samples])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Media item take peaks: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get media item take peaks: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_depth":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetTrackDepth", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track depth: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track depth: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_folder_state":
        track_index = arguments["track_index"]
        folder_state = arguments["folder_state"]
        
        result = bridge.call_lua("SetMediaTrackInfo_Value", [track_index, "I_FOLDERDEPTH", folder_state])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track folder state: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track folder state: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_folder_compact_state":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetMediaTrackInfo_Value", [track_index, "I_FOLDERCOMPACT"])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Track folder compact state: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track folder compact state: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_folder_compact_state":
        track_index = arguments["track_index"]
        compact_state = arguments["compact_state"]
        
        result = bridge.call_lua("SetMediaTrackInfo_Value", [track_index, "I_FOLDERCOMPACT", compact_state])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track folder compact state: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track folder compact state: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_parent_track":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetParentTrack", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Parent track: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get parent track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_height":
        track_index = arguments["track_index"]
        height = arguments["height"]
        lock_height = arguments.get("lock_height", False)
        
        result = bridge.call_lua("SetTrackHeight", [track_index, height, lock_height])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track height: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track height: {result.get('error', 'Unknown error')}"
            )]    elif name == "main_render_project":
        project_index = arguments.get("project_index", 0)
        render_tail_ms = arguments.get("render_tail_ms", 1000)
        
        result = bridge.call_lua("Main_OnCommand", [41824, 0])  # Render project to disk
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Rendering project..."
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to render project: {result.get('error', 'Unknown error')}"
            )]

    elif name == "freeze_track":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("FreezeTrack", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Froze track at index {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to freeze track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "unfreeze_track":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("UnfreezeTrack", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Unfroze track at index {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to unfreeze track: {result.get('error', 'Unknown error')}"
            )]

    elif name == "is_track_frozen":
        track_index = arguments["track_index"]
        
        result = bridge.call_lua("GetMediaTrackInfo_Value", [track_index, "I_FREEMODE"])
        
        if result.get("ok"):
            frozen = result.get('ret', 0) > 0
            return [TextContent(
                type="text",
                text=f"Track frozen: {frozen}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to check freeze state: {result.get('error', 'Unknown error')}"
            )]

    elif name == "render_time_selection":
        add_to_project = arguments.get("add_to_project", True)
        
        # Action: Render time selection to new track
        result = bridge.call_lua("Main_OnCommand", [40635, 0])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Rendered time selection to new track"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to render time selection: {result.get('error', 'Unknown error')}"
            )]

    elif name == "apply_fx_to_items":
        track_index = arguments["track_index"]
        
        # Action: Apply track FX to items (destructive)
        result = bridge.call_lua("ApplyFXToItems", [track_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Applied FX to items on track {track_index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to apply FX to items: {result.get('error', 'Unknown error')}"
            )]    elif name == "midi_get_all_events":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("MIDI_GetAllEvts", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"MIDI events data: {result.get('ret', '')[:100]}..."  # Truncate for display
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get MIDI events: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_set_all_events":
        take_index = arguments["take_index"]
        events_data = arguments["events_data"]
        
        result = bridge.call_lua("MIDI_SetAllEvts", [take_index, events_data])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set MIDI events: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set MIDI events: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_get_note_name":
        note_number = arguments["note_number"]
        
        result = bridge.call_lua("GetNoteName", [note_number])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Note name: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get note name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_get_scale":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("MIDI_GetScale", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"MIDI scale: root={result.get('root')}, scale={result.get('scale')}, name={result.get('name')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get MIDI scale: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_set_scale":
        take_index = arguments["take_index"]
        root = arguments["root"]
        scale = arguments["scale"]
        channel = arguments.get("channel", 0)
        
        result = bridge.call_lua("MIDI_SetScale", [take_index, root, scale, channel])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set MIDI scale: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set MIDI scale: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_get_text_sysex_event":
        take_index = arguments["take_index"]
        event_index = arguments["event_index"]
        
        result = bridge.call_lua("MIDI_GetTextSysexEvt", [take_index, event_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Text/Sysex event: type={result.get('type')}, message={result.get('message')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get text/sysex event: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_set_text_sysex_event":
        take_index = arguments["take_index"]
        event_index = arguments["event_index"]
        selected = arguments["selected"]
        muted = arguments["muted"]
        ppq_pos = arguments["ppq_pos"]
        event_type = arguments["type"]
        message = arguments["message"]
        
        result = bridge.call_lua("MIDI_SetTextSysexEvt", [take_index, event_index, selected, muted, ppq_pos, event_type, message])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set text/sysex event: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set text/sysex event: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_count_events":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("MIDI_CountEvts", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"MIDI event counts: notes={result.get('notes')}, cc={result.get('cc')}, text/sysex={result.get('text')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to count MIDI events: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_enum_sel_notes":
        take_index = arguments["take_index"]
        note_index = arguments["note_index"]
        
        result = bridge.call_lua("MIDI_EnumSelNotes", [take_index, note_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Selected note index: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to enumerate selected notes: {result.get('error', 'Unknown error')}"
            )]

    elif name == "midi_select_all":
        take_index = arguments["take_index"]
        select_notes = arguments.get("select_notes", True)
        select_cc = arguments.get("select_cc", True)
        select_text = arguments.get("select_text", True)
        
        result = bridge.call_lua("MIDI_SelectAll", [take_index, select_notes, select_cc, select_text])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Selected all MIDI events"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to select all MIDI events: {result.get('error', 'Unknown error')}"
            )]    elif name == "get_resource_path":
        result = bridge.call_lua("GetResourcePath", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Resource path: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get resource path: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_exe_path":
        result = bridge.call_lua("GetExePath", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Executable path: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get executable path: {result.get('error', 'Unknown error')}"
            )]

    elif name == "recursive_create_directory":
        path = arguments["path"]
        mode = arguments.get("mode", 0)
        
        result = bridge.call_lua("RecursiveCreateDirectory", [path, mode])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Created directory: {path}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to create directory: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_project_path":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("GetProjectPath", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Project path: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project path: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_project_state_change_count":
        project_index = arguments.get("project_index", 0)
        
        result = bridge.call_lua("GetProjectStateChangeCount", [project_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Project state change count: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get project state change count: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_track_state_chunk":
        track_index = arguments["track_index"]
        is_undo = arguments.get("is_undo", False)
        
        result = bridge.call_lua("GetTrackStateChunk", [track_index, is_undo])
        
        if result.get("ok"):
            chunk = result.get('ret', '')
            # Truncate long chunks for display
            display_chunk = chunk[:200] + "..." if len(chunk) > 200 else chunk
            return [TextContent(
                type="text",
                text=f"Track state chunk: {display_chunk}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get track state chunk: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_track_state_chunk":
        track_index = arguments["track_index"]
        state_chunk = arguments["state_chunk"]
        is_undo = arguments.get("is_undo", False)
        
        result = bridge.call_lua("SetTrackStateChunk", [track_index, state_chunk, is_undo])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set track state chunk successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set track state chunk: {result.get('error', 'Unknown error')}"
            )]

    elif name == "browse_for_file":
        title = arguments["title"]
        extension = arguments["extension"]
        
        result = bridge.call_lua("BrowseForFile", [title, extension])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Selected file: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to browse for file: {result.get('error', 'Unknown error')}"
            )]    elif name == "show_console_msg":
        message = arguments["message"]
        
        result = bridge.call_lua("ShowConsoleMsg", [message])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Displayed message in console"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to show console message: {result.get('error', 'Unknown error')}"
            )]

    elif name == "clear_console":
        result = bridge.call_lua("ClearConsole", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Cleared console"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to clear console: {result.get('error', 'Unknown error')}"
            )]

    elif name == "show_message_box":
        message = arguments["message"]
        title = arguments["title"]
        msg_type = arguments.get("type", 0)
        
        result = bridge.call_lua("MB", [message, title, msg_type])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Message box result: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to show message box: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_main_hwnd":
        result = bridge.call_lua("GetMainHwnd", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Main window handle: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get main window handle: {result.get('error', 'Unknown error')}"
            )]

    elif name == "dock_window_add":
        hwnd = arguments["hwnd"]
        dock_name = arguments["name"]
        pos = arguments["pos"]
        allow_show = arguments.get("allow_show", True)
        
        result = bridge.call_lua("DockWindowAdd", [hwnd, dock_name, pos, allow_show])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Added dock window"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to add dock window: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_mouse_position":
        result = bridge.call_lua("GetMousePosition", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Mouse position: x={result.get('x')}, y={result.get('y')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get mouse position: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_cursor_context":
        result = bridge.call_lua("GetCursorContext", [])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Cursor context: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get cursor context: {result.get('error', 'Unknown error')}"
            )]    elif name == "get_media_item_info_value":
        item_index = arguments["item_index"]
        param_name = arguments["param_name"]
        
        result = bridge.call_lua("GetMediaItemInfo_Value", [item_index, param_name])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Item {param_name}: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get item info: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_info_value":
        item_index = arguments["item_index"]
        param_name = arguments["param_name"]
        value = arguments["value"]
        
        result = bridge.call_lua("SetMediaItemInfo_Value", [item_index, param_name, value])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set item {param_name} to {value}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set item info: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_take_name":
        take_index = arguments["take_index"]
        
        result = bridge.call_lua("GetTakeName", [take_index])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Take name: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get take name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_take_name":
        take_index = arguments["take_index"]
        name = arguments["name"]
        
        result = bridge.call_lua("GetSetMediaItemTakeInfo_String", [take_index, "P_NAME", name, True])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set take name to: {name}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set take name: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_media_item_take_info_value":
        take_index = arguments["take_index"]
        param_name = arguments["param_name"]
        
        result = bridge.call_lua("GetMediaItemTakeInfo_Value", [take_index, param_name])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Take {param_name}: {result.get('ret')}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get take info: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_media_item_take_info_value":
        take_index = arguments["take_index"]
        param_name = arguments["param_name"]
        value = arguments["value"]
        
        result = bridge.call_lua("SetMediaItemTakeInfo_Value", [take_index, param_name, value])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set take {param_name} to {value}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set take info: {result.get('error', 'Unknown error')}"
            )]

    elif name == "get_item_state_chunk":
        item_index = arguments["item_index"]
        is_undo = arguments.get("is_undo", False)
        
        result = bridge.call_lua("GetItemStateChunk", [item_index, is_undo])
        
        if result.get("ok"):
            chunk = result.get('ret', '')
            display_chunk = chunk[:200] + "..." if len(chunk) > 200 else chunk
            return [TextContent(
                type="text",
                text=f"Item state chunk: {display_chunk}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to get item state chunk: {result.get('error', 'Unknown error')}"
            )]

    elif name == "set_item_state_chunk":
        item_index = arguments["item_index"]
        state_chunk = arguments["state_chunk"]
        is_undo = arguments.get("is_undo", False)
        
        result = bridge.call_lua("SetItemStateChunk", [item_index, state_chunk, is_undo])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Set item state chunk successfully"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to set item state chunk: {result.get('error', 'Unknown error')}"
            )]

    elif name == "split_media_item":
        item_index = arguments["item_index"]
        position = arguments["position"]
        
        result = bridge.call_lua("SplitMediaItem", [item_index, position])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Split item at position {position}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to split item: {result.get('error', 'Unknown error')}"
            )]