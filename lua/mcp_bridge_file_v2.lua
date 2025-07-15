-- REAPER MCP Bridge (File-based, Full API)
-- This script runs inside REAPER and communicates with the MCP server using files

local bridge_dir = reaper.GetResourcePath() .. '/Scripts/mcp_bridge_data/'

-- Create bridge directory if it doesn't exist
local function ensure_dir()
    reaper.RecursiveCreateDirectory(bridge_dir, 0)
end

-- Simple JSON encoding (minimal implementation)
local function encode_json(v)
    if type(v) == "nil" then
        return "null"
    elseif type(v) == "boolean" then
        return tostring(v)
    elseif type(v) == "number" then
        return tostring(v)
    elseif type(v) == "string" then
        return string.format('"%s"', v:gsub('"', '\\"'):gsub('\n', '\\n'):gsub('\r', '\\r'))
    elseif type(v) == "table" then
        local parts = {}
        local is_array = #v > 0
        if is_array then
            for i, item in ipairs(v) do
                table.insert(parts, encode_json(item))
            end
            return "[" .. table.concat(parts, ",") .. "]"
        else
            for k, item in pairs(v) do
                table.insert(parts, string.format('"%s":%s', k, encode_json(item)))
            end
            return "{" .. table.concat(parts, ",") .. "}"
        end
    elseif type(v) == "userdata" then
        -- Handle userdata (pointers) by converting to a handle ID
        return encode_json({__ptr = tostring(v)})
    else
        return "null"
    end
end

-- Better JSON decoding that handles arrays properly
local function decode_json(str)
    if not str or str == "" then return nil end
    
    -- Remove whitespace
    str = str:gsub("^%s*(.-)%s*$", "%1")
    
    -- Very basic JSON decoder
    if str == "null" then return nil
    elseif str == "true" then return true
    elseif str == "false" then return false
    elseif str:match("^%-?%d+%.?%d*$") then return tonumber(str)
    elseif str:match('^"(.*)"$') then 
        -- Unescape string
        local s = str:match('^"(.*)"$')
        s = s:gsub('\\n', '\n'):gsub('\\r', '\r'):gsub('\\"', '"')
        return s
    elseif str:match("^%[.*%]$") then
        -- Array - improved parsing
        local arr = {}
        local content = str:sub(2, -2)
        if content ~= "" then
            -- Handle nested structures better
            local i = 1
            local pos = 1
            local depth = 0
            local start = 1
            
            while pos <= #content do
                local char = content:sub(pos, pos)
                if char == '[' or char == '{' then
                    depth = depth + 1
                elseif char == ']' or char == '}' then
                    depth = depth - 1
                elseif char == ',' and depth == 0 then
                    -- Found a top-level comma
                    local value = content:sub(start, pos - 1)
                    arr[i] = decode_json(value:match("^%s*(.-)%s*$"))
                    i = i + 1
                    start = pos + 1
                end
                pos = pos + 1
            end
            
            -- Don't forget the last element
            if start <= #content then
                local value = content:sub(start)
                arr[i] = decode_json(value:match("^%s*(.-)%s*$"))
            end
        end
        return arr
    elseif str:match("^{.*}$") then
        -- Object - improved parsing
        local obj = {}
        local content = str:sub(2, -2)
        
        -- Better object parsing that handles nested values
        local pos = 1
        while pos <= #content do
            -- Find key
            local key_start = content:find('"', pos)
            if not key_start then break end
            local key_end = content:find('"', key_start + 1)
            if not key_end then break end
            local key = content:sub(key_start + 1, key_end - 1)
            
            -- Find colon
            local colon = content:find(':', key_end + 1)
            if not colon then break end
            
            -- Find value (handle nested structures)
            local value_start = colon + 1
            while value_start <= #content and content:sub(value_start, value_start):match("%s") do
                value_start = value_start + 1
            end
            
            local value_end = value_start
            local depth = 0
            local in_string = false
            local escape = false
            
            while value_end <= #content do
                local char = content:sub(value_end, value_end)
                
                if escape then
                    escape = false
                elseif char == '\\' then
                    escape = true
                elseif char == '"' and not escape then
                    in_string = not in_string
                elseif not in_string then
                    if char == '[' or char == '{' then
                        depth = depth + 1
                    elseif char == ']' or char == '}' then
                        depth = depth - 1
                    elseif (char == ',' or char == '}') and depth == 0 then
                        break
                    end
                end
                
                value_end = value_end + 1
            end
            
            local value = content:sub(value_start, value_end - 1)
            obj[key] = decode_json(value:match("^%s*(.-)%s*$"))
            
            pos = value_end + 1
        end
        
        return obj
    end
    return nil
end

-- Read file contents
local function read_file(filepath)
    local file = io.open(filepath, "r")
    if not file then return nil end
    local content = file:read("*all")
    file:close()
    return content
end

-- Write file contents
local function write_file(filepath, content)
    local file = io.open(filepath, "w")
    if not file then return false end
    file:write(content)
    file:close()
    return true
end

-- Check if file exists
local function file_exists(filepath)
    local file = io.open(filepath, "r")
    if file then
        file:close()
        return true
    end
    return false
end

-- Delete file
local function delete_file(filepath)
    os.remove(filepath)
end

-- Main processing function
local function process_request()
    -- Look for any request files with numbered pattern
    for i = 1, 1000 do
        local numbered_request_file = bridge_dir .. 'request_' .. i .. '.json'
        local numbered_response_file = bridge_dir .. 'response_' .. i .. '.json'
        
        if file_exists(numbered_request_file) then
            -- Wrap in pcall to catch any errors
            local ok, err = pcall(function()
                -- Read and process request
                local request_data = read_file(numbered_request_file)
                if request_data then
                    reaper.ShowConsoleMsg("Processing request " .. i .. ": " .. request_data .. "\n")
                    
                    -- Parse the request
                    local request = decode_json(request_data)
                    if request and request.func then
                        local fname = request.func
                        local args = request.args or {}
                    
                    -- Call the REAPER function
                    local response = {ok = false}
                    
                    -- Handle all API functions
                    if fname == "InsertTrackAtIndex" then
                        if #args >= 2 then
                            reaper.InsertTrackAtIndex(args[1], args[2])
                            response.ok = true
                        else
                            response.error = "InsertTrackAtIndex requires 2 arguments"
                        end
                    
                    elseif fname == "CountTracks" then
                        local count = reaper.CountTracks(args[1] or 0)
                        response.ok = true
                        response.ret = count
                    
                    elseif fname == "GetAppVersion" then
                        local version = reaper.GetAppVersion()
                        response.ok = true
                        response.ret = version
                    
                    elseif fname == "GetTrack" then
                        if #args >= 2 then
                            local track = reaper.GetTrack(args[1], args[2])
                            response.ok = true
                            response.ret = track
                        else
                            response.error = "GetTrack requires 2 arguments"
                        end
                    
                    elseif fname == "SetTrackSelected" then
                        if #args >= 2 then
                            local track = reaper.GetTrack(0, args[1])
                            if track then
                                reaper.SetTrackSelected(track, args[2])
                                response.ok = true
                            else
                                response.error = "Track not found"
                            end
                        else
                            response.error = "SetTrackSelected requires 2 arguments"
                        end
                    
                    elseif fname == "GetTrackName" then
                        if #args >= 1 then
                            local track = args[1]
                            -- Handle track index or pointer object
                            if type(args[1]) == "number" then
                                -- It's a track index
                                if args[1] == -1 then
                                    -- Special case for master track
                                    track = reaper.GetMasterTrack(0)
                                else
                                    track = reaper.GetTrack(0, args[1])
                                end
                                if not track then
                                    response.error = "Track not found at index " .. tostring(args[1])
                                    response.ok = false
                                end
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer object - we can't use it
                                response.error = "Cannot use track pointer from previous call - use track index instead"
                                response.ok = false
                                track = nil
                            elseif type(args[1]) == "userdata" then
                                -- It's already a track object
                                track = args[1]
                            end
                            
                            if track then
                                local retval, name = reaper.GetTrackName(track)
                                response.ok = true
                                response.ret = name
                            end
                        else
                            response.error = "GetTrackName requires 1 argument"
                        end
                    
                    elseif fname == "SetTrackName" then
                        if #args >= 2 then
                            local track = reaper.GetTrack(0, args[1])
                            if track then
                                reaper.GetSetMediaTrackInfo_String(track, "P_NAME", args[2], true)
                                response.ok = true
                            else
                                response.error = "Track not found"
                            end
                        else
                            response.error = "SetTrackName requires 2 arguments"
                        end
                    
                    elseif fname == "GetMasterTrack" then
                        local track = reaper.GetMasterTrack(args[1] or 0)
                        response.ok = true
                        response.ret = track
                    
                    elseif fname == "DeleteTrack" then
                        if args[1] then
                            -- Check if it's a track index or a pointer object
                            local track = nil
                            if type(args[1]) == "number" then
                                -- It's a track index
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer object - we can't use it directly
                                -- For now, return an error
                                response.error = "Cannot use track pointer from previous call - use DeleteTrackByIndex instead"
                                response.ok = false
                            else
                                track = args[1]  -- Assume it's already a track
                            end
                            
                            if track then
                                reaper.DeleteTrack(track)
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "DeleteTrack requires track pointer or index"
                        end
                    
                    elseif fname == "DeleteTrackByIndex" then
                        if args[1] then
                            local track = reaper.GetTrack(0, args[1])
                            if track then
                                reaper.DeleteTrack(track)
                                response.ok = true
                            else
                                response.error = "Track not found at index " .. tostring(args[1])
                                response.ok = false
                            end
                        else
                            response.error = "DeleteTrackByIndex requires track index"
                        end
                    
                    elseif fname == "GetMediaTrackInfo_Value" then
                        if #args >= 2 then
                            local track = args[1]
                            -- Handle track index or pointer object
                            if type(args[1]) == "number" then
                                -- It's a track index
                                if args[1] == -1 then
                                    -- Special case for master track
                                    track = reaper.GetMasterTrack(0)
                                else
                                    track = reaper.GetTrack(0, args[1])
                                end
                                if not track then
                                    response.error = "Track not found at index " .. tostring(args[1])
                                    response.ok = false
                                end
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer object - we can't use it
                                response.error = "Cannot use track pointer from previous call - use track index instead"
                                response.ok = false
                                track = nil
                            end
                            
                            if track then
                                local value = reaper.GetMediaTrackInfo_Value(track, args[2])
                                response.ok = true
                                response.ret = value
                            end
                        else
                            response.error = "GetMediaTrackInfo_Value requires 2 arguments"
                        end
                    
                    elseif fname == "SetMediaTrackInfo_Value" then
                        if #args >= 3 then
                            local track = args[1]
                            -- Handle track index or pointer object
                            if type(args[1]) == "number" then
                                -- It's a track index
                                if args[1] == -1 then
                                    -- Special case for master track
                                    track = reaper.GetMasterTrack(0)
                                else
                                    track = reaper.GetTrack(0, args[1])
                                end
                                if not track then
                                    response.error = "Track not found at index " .. tostring(args[1])
                                    response.ok = false
                                end
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer object - we can't use it
                                response.error = "Cannot use track pointer from previous call - use track index instead"
                                response.ok = false
                                track = nil
                            end
                            
                            if track then
                                reaper.SetMediaTrackInfo_Value(track, args[2], args[3])
                                response.ok = true
                            end
                        else
                            response.error = "SetMediaTrackInfo_Value requires 3 arguments"
                        end
                    
                    elseif fname == "GetSetMediaTrackInfo_String" then
                        if #args >= 4 then
                            local track = args[1]
                            local param = args[2]
                            local newvalue = args[3]
                            local setnewvalue = args[4]
                            
                            -- Handle track index or pointer object
                            if type(args[1]) == "number" then
                                -- It's a track index
                                if args[1] == -1 then
                                    -- Special case for master track
                                    track = reaper.GetMasterTrack(0)
                                else
                                    track = reaper.GetTrack(0, args[1])
                                end
                                if not track then
                                    response.error = "Track not found at index " .. tostring(args[1])
                                    response.ok = false
                                end
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer object - we can't use it
                                response.error = "Cannot use track pointer from previous call - use track index instead"
                                response.ok = false
                                track = nil
                            elseif type(args[1]) == "userdata" then
                                -- It's already a track object
                                track = args[1]
                            end
                            
                            if track then
                                local ok, strval = reaper.GetSetMediaTrackInfo_String(track, param, newvalue, setnewvalue)
                                response.ok = ok
                                response.ret = strval
                            end
                        else
                            response.error = "GetSetMediaTrackInfo_String requires 4 arguments"
                        end
                    
                    elseif fname == "AddMediaItemToTrack" then
                        if args[1] then
                            local track = nil
                            -- Check if it's a track index (number) or a track object
                            if type(args[1]) == "number" then
                                -- It's a track index, get the track
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "userdata" then
                                -- It's already a track object
                                track = args[1]
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer reference from a previous call - we can't use it
                                response.error = "Cannot use track pointer from previous call - bridge limitation"
                                response.ok = false
                            end
                            
                            if track then
                                local item = reaper.AddMediaItemToTrack(track)
                                response.ok = true
                                response.ret = item
                            else
                                response.error = "Invalid track parameter - provide track index or valid track object"
                                response.ok = false
                            end
                        else
                            response.error = "AddMediaItemToTrack requires track index or track object"
                        end
                    
                    elseif fname == "CountMediaItems" then
                        local count = reaper.CountMediaItems(args[1] or 0)
                        response.ok = true
                        response.ret = count
                    
                    elseif fname == "AddTakeToMediaItem" then
                        if args[1] then
                            local item = nil
                            -- Handle item index or pointer
                            if type(args[1]) == "number" then
                                -- It's an item index
                                item = reaper.GetMediaItem(0, args[1])
                            elseif type(args[1]) == "userdata" then
                                -- It's already an item object
                                item = args[1]
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer reference from a previous call - we can't use it
                                response.error = "Cannot use item pointer from previous call - use item index instead"
                                response.ok = false
                            end
                            
                            if item then
                                local take = reaper.AddTakeToMediaItem(item)
                                response.ok = true
                                response.ret = take
                            else
                                response.error = "Invalid item parameter"
                                response.ok = false
                            end
                        else
                            response.error = "AddTakeToMediaItem requires item index or item object"
                        end
                    
                    elseif fname == "GetMediaItem" then
                        if #args >= 2 then
                            local item = reaper.GetMediaItem(args[1], args[2])
                            response.ok = true
                            response.ret = item
                        else
                            response.error = "GetMediaItem requires 2 arguments"
                        end
                    
                    elseif fname == "GetMediaItemTake" then
                        if #args >= 2 then
                            local item = nil
                            -- Handle item index or pointer
                            if type(args[1]) == "number" then
                                -- It's an item index
                                item = reaper.GetMediaItem(0, args[1])
                            elseif type(args[1]) == "userdata" then
                                -- It's already an item object
                                item = args[1]
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer reference
                                response.error = "Cannot use item pointer from previous call"
                                response.ok = false
                            end
                            
                            if item then
                                local take = reaper.GetMediaItemTake(item, args[2])
                                response.ok = true
                                response.ret = take
                            else
                                response.error = "Invalid item parameter"
                                response.ok = false
                            end
                        else
                            response.error = "GetMediaItemTake requires 2 arguments"
                        end
                    
                    elseif fname == "CountTakes" then
                        if #args >= 1 then
                            local item = nil
                            -- Handle item index or pointer
                            if type(args[1]) == "number" then
                                -- It's an item index
                                item = reaper.GetMediaItem(0, args[1])
                            elseif type(args[1]) == "userdata" then
                                -- It's already an item object
                                item = args[1]
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer reference
                                response.error = "Cannot use item pointer from previous call"
                                response.ok = false
                            end
                            
                            if item then
                                local count = reaper.CountTakes(item)
                                response.ok = true
                                response.ret = count
                            else
                                response.error = "Invalid item parameter"
                                response.ok = false
                            end
                        else
                            response.error = "CountTakes requires 1 argument"
                        end
                    
                    elseif fname == "GetTrackMediaItem" then
                        if #args >= 2 then
                            local item = reaper.GetTrackMediaItem(args[1], args[2])
                            response.ok = true
                            response.ret = item
                        else
                            response.error = "GetTrackMediaItem requires 2 arguments"
                        end
                    
                    elseif fname == "DeleteTrackMediaItem" then
                        if #args >= 2 then
                            local result = reaper.DeleteTrackMediaItem(args[1], args[2])
                            response.ok = result
                        else
                            response.error = "DeleteTrackMediaItem requires 2 arguments"
                        end
                    
                    elseif fname == "GetMediaItemInfo_Value" then
                        if #args >= 2 then
                            local value = reaper.GetMediaItemInfo_Value(args[1], args[2])
                            response.ok = true
                            response.ret = value
                        else
                            response.error = "GetMediaItemInfo_Value requires 2 arguments"
                        end
                    
                    elseif fname == "SetMediaItemLength" then
                        if #args >= 3 then
                            local item = args[1]
                            -- Handle item index or pointer
                            if type(args[1]) == "number" then
                                -- It's an item index
                                item = reaper.GetMediaItem(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer reference from a previous call - we can't use it
                                response.error = "Cannot use item pointer from previous call - use item index instead"
                                response.ok = false
                                item = nil
                            end
                            
                            if item then
                                reaper.SetMediaItemLength(item, args[2], args[3])
                                response.ok = true
                            else
                                response.error = "Invalid item parameter"
                                response.ok = false
                            end
                        else
                            response.error = "SetMediaItemLength requires 3 arguments"
                        end
                    
                    elseif fname == "SetMediaItemPosition" then
                        if #args >= 3 then
                            local item = args[1]
                            -- Handle item index or pointer
                            if type(args[1]) == "number" then
                                -- It's an item index
                                item = reaper.GetMediaItem(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer reference from a previous call - we can't use it
                                response.error = "Cannot use item pointer from previous call - use item index instead"
                                response.ok = false
                                item = nil
                            end
                            
                            if item then
                                reaper.SetMediaItemPosition(item, args[2], args[3])
                                response.ok = true
                            else
                                response.error = "Invalid item parameter"
                                response.ok = false
                            end
                        else
                            response.error = "SetMediaItemPosition requires 3 arguments"
                        end
                    
                    elseif fname == "GetProjectName" then
                        local retval, name = reaper.GetProjectName(args[1] or 0, "", 512)
                        response.ok = true
                        response.ret = {name}
                    
                    elseif fname == "GetProjectPath" then
                        local path = reaper.GetProjectPath("", 2048)
                        response.ok = true
                        response.ret = path
                    
                    elseif fname == "Main_SaveProject" then
                        reaper.Main_SaveProject(args[1] or 0, args[2] or false)
                        response.ok = true
                    
                    elseif fname == "GetCursorPosition" then
                        local pos = reaper.GetCursorPosition()
                        response.ok = true
                        response.ret = pos
                    
                    elseif fname == "SetEditCurPos" then
                        if #args >= 1 then
                            reaper.SetEditCurPos(args[1], args[2] or true, args[3] or false)
                            response.ok = true
                        else
                            response.error = "SetEditCurPos requires at least 1 argument"
                        end
                    
                    elseif fname == "GetPlayState" then
                        local state = reaper.GetPlayState()
                        response.ok = true
                        response.ret = state
                    
                    elseif fname == "Main_OnCommand" then
                        if #args >= 2 then
                            reaper.Main_OnCommand(args[1], args[2])
                            response.ok = true
                        else
                            response.error = "Main_OnCommand requires 2 arguments"
                        end
                    
                    elseif fname == "SetPlayState" then
                        if #args >= 3 then
                            local play = args[1] and 1 or 0
                            local pause = args[2] and 2 or 0
                            local rec = args[3] and 4 or 0
                            -- Use Main_OnCommand instead of CSurf_SetPlayState
                            -- Play = 1007, Pause = 1008, Stop = 1016, Record = 1013
                            if rec > 0 then
                                reaper.Main_OnCommand(1013, 0)  -- Record
                            elseif play > 0 then
                                reaper.Main_OnCommand(1007, 0)  -- Play
                            elseif pause > 0 then
                                reaper.Main_OnCommand(1008, 0)  -- Pause
                            else
                                reaper.Main_OnCommand(1016, 0)  -- Stop
                            end
                            response.ok = true
                        else
                            response.error = "SetPlayState requires 3 arguments"
                        end
                    
                    elseif fname == "GetSetRepeat" then
                        if #args >= 1 then
                            local prev = reaper.GetSetRepeat(args[1])
                            response.ok = true
                            response.ret = prev
                        else
                            response.error = "GetSetRepeat requires 1 argument"
                        end
                    
                    elseif fname == "Undo_BeginBlock" then
                        reaper.Undo_BeginBlock()
                        response.ok = true
                    
                    elseif fname == "Undo_EndBlock" then
                        if #args >= 1 then
                            reaper.Undo_EndBlock(args[1], args[2] or -1)
                            response.ok = true
                        else
                            response.error = "Undo_EndBlock requires at least 1 argument"
                        end
                    
                    elseif fname == "UpdateArrange" then
                        reaper.UpdateArrange()
                        response.ok = true
                    
                    elseif fname == "UpdateTimeline" then
                        reaper.UpdateTimeline()
                        response.ok = true
                    
                    elseif fname == "AddProjectMarker" then
                        if #args >= 5 then
                            local index = reaper.AddProjectMarker(args[1], args[2], args[3], args[4], args[5], args[6] or -1)
                            response.ok = true
                            response.ret = index
                        else
                            response.error = "AddProjectMarker requires at least 5 arguments"
                        end
                    
                    elseif fname == "DeleteProjectMarker" then
                        if #args >= 3 then
                            local result = reaper.DeleteProjectMarker(args[1], args[2], args[3])
                            response.ok = result
                        else
                            response.error = "DeleteProjectMarker requires 3 arguments"
                        end
                    
                    elseif fname == "CountProjectMarkers" then
                        local ret, num_markers, num_regions = reaper.CountProjectMarkers(args[1] or 0)
                        response.ok = true
                        response.ret = {num_markers, num_regions}
                    
                    elseif fname == "EnumProjectMarkers" then
                        if #args >= 1 then
                            local ret, is_region, pos, region_end, name, idx = reaper.EnumProjectMarkers(args[1])
                            if ret then
                                response.ok = true
                                response.ret = {ret, is_region, pos, region_end, name, idx}
                            else
                                response.ok = true
                                response.ret = {}
                            end
                        else
                            response.error = "EnumProjectMarkers requires 1 argument"
                        end
                    
                    elseif fname == "GetSet_LoopTimeRange" then
                        if #args >= 2 then
                            if args[1] then  -- Set mode
                                if #args >= 5 then
                                    reaper.GetSet_LoopTimeRange(true, args[2], args[3], args[4], args[5])
                                    response.ok = true
                                else
                                    response.error = "GetSet_LoopTimeRange set mode requires 5 arguments"
                                end
                            else  -- Get mode
                                local start_time, end_time = reaper.GetSet_LoopTimeRange(false, args[2], 0, 0, false)
                                response.ok = true
                                response.ret = {start_time, end_time}
                            end
                        else
                            response.error = "GetSet_LoopTimeRange requires at least 2 arguments"
                        end
                    
                    elseif fname == "MIDI_CountEvts" then
                        if #args >= 1 then
                            local take = args[1]
                            -- Handle take object or pointer
                            if type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer reference - we can't use it
                                response.error = "Cannot use take pointer from previous call"
                                response.ok = false
                            else
                                local retval, notes, cc, text = reaper.MIDI_CountEvts(take)
                                response.ok = true
                                response.retval = retval
                                response.notes = notes
                                response.cc = cc
                                response.text = text
                            end
                        else
                            response.error = "MIDI_CountEvts requires 1 argument (take)"
                        end
                    
                    elseif fname == "GetItemTakeAndCountMIDI" then
                        -- Combined function to get item, take and count MIDI events
                        if #args >= 2 then
                            local item_index = args[1]
                            local take_index = args[2]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Failed to find media item at index " .. tostring(item_index)
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Failed to find take at index " .. tostring(take_index)
                                    response.ok = false
                                else
                                    -- Count MIDI events
                                    local retval, notes, cc, text = reaper.MIDI_CountEvts(take)
                                    response.ok = true
                                    response.retval = retval
                                    response.notes = notes
                                    response.cc = cc
                                    response.text = text
                                end
                            end
                        else
                            response.error = "GetItemTakeAndCountMIDI requires 2 arguments (item_index, take_index)"
                        end
                    
                    elseif fname == "InsertMIDINoteToItemTake" then
                        -- Combined function to insert MIDI note
                        if #args >= 11 then
                            local item_index = args[1]
                            local take_index = args[2]
                            local pitch = args[3]
                            local velocity = args[4]
                            local start_time = args[5]
                            local duration = args[6]
                            local channel = args[7]
                            local selected = args[8]
                            local muted = args[9]
                            -- args[10] reserved for future use
                            -- args[11] reserved for future use
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Failed to find media item at index " .. tostring(item_index)
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Failed to find take at index " .. tostring(take_index)
                                    response.ok = false
                                else
                                    -- Convert time to PPQ
                                    local ppq_start = reaper.MIDI_GetPPQPosFromProjTime(take, start_time)
                                    local ppq_end = reaper.MIDI_GetPPQPosFromProjTime(take, start_time + duration)
                                    
                                    -- Insert note
                                    local result = reaper.MIDI_InsertNote(take, selected, muted, ppq_start, ppq_end, channel, pitch, velocity, true)
                                    response.ok = result
                                    if not result then
                                        response.error = "Failed to insert MIDI note"
                                    end
                                end
                            end
                        else
                            response.error = "InsertMIDINoteToItemTake requires 11 arguments"
                        end
                    
                    elseif fname == "GetMIDIScaleFromItemTake" then
                        -- Combined function to get MIDI scale
                        if #args >= 2 then
                            local item_index = args[1]
                            local take_index = args[2]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Failed to find media item at index " .. tostring(item_index)
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Failed to find take at index " .. tostring(take_index)
                                    response.ok = false
                                else
                                    -- Get scale
                                    local root, scale, name = reaper.MIDI_GetScale(take)
                                    response.ok = true
                                    response.root = root
                                    response.scale = scale
                                    response.name = name or ""
                                end
                            end
                        else
                            response.error = "GetMIDIScaleFromItemTake requires 2 arguments (item_index, take_index)"
                        end
                    
                    elseif fname == "SetMIDIScaleToItemTake" then
                        -- Combined function to set MIDI scale
                        if #args >= 5 then
                            local item_index = args[1]
                            local take_index = args[2]
                            local root = args[3]
                            local scale = args[4]
                            local name = args[5] or ""
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Failed to find media item at index " .. tostring(item_index)
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Failed to find take at index " .. tostring(take_index)
                                    response.ok = false
                                else
                                    -- Set scale
                                    local result = reaper.MIDI_SetScale(take, root, scale, name)
                                    response.ok = result
                                    if not result then
                                        response.error = "Failed to set MIDI scale"
                                    end
                                end
                            end
                        else
                            response.error = "SetMIDIScaleToItemTake requires 5 arguments"
                        end
                    
                    elseif fname == "SelectAllMIDIInItemTake" then
                        -- Combined function to select all MIDI events
                        if #args >= 2 then
                            local item_index = args[1]
                            local take_index = args[2]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Failed to find media item at index " .. tostring(item_index)
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Failed to find take at index " .. tostring(take_index)
                                    response.ok = false
                                else
                                    -- Select all MIDI events
                                    reaper.MIDI_SelectAll(take, true)
                                    response.ok = true
                                end
                            end
                        else
                            response.error = "SelectAllMIDIInItemTake requires 2 arguments"
                        end
                    
                    elseif fname == "GetAllMIDIEventsFromItemTake" then
                        -- Combined function to get all MIDI events
                        if #args >= 2 then
                            local item_index = args[1]
                            local take_index = args[2]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Failed to find media item at index " .. tostring(item_index)
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Failed to find take at index " .. tostring(take_index)
                                    response.ok = false
                                else
                                    -- Get all events
                                    local retval, events = reaper.MIDI_GetAllEvts(take, "")
                                    response.ok = retval
                                    response.ret = events
                                    if not retval then
                                        response.error = "Failed to get MIDI events"
                                    end
                                end
                            end
                        else
                            response.error = "GetAllMIDIEventsFromItemTake requires 2 arguments"
                        end
                    
                    elseif fname == "TrackFX_AddByName" then
                        -- Add FX to track by name
                        if #args >= 3 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                local fx_index = reaper.TrackFX_AddByName(track, args[2], args[3] or false, args[4] or -1)
                                response.ok = true
                                response.ret = fx_index
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_AddByName requires at least 3 arguments"
                        end
                    
                    elseif fname == "TrackFX_GetCount" then
                        -- Get FX count for track
                        if #args >= 1 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                local count = reaper.TrackFX_GetCount(track)
                                response.ok = true
                                response.ret = count
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_GetCount requires 1 argument"
                        end
                    
                    elseif fname == "GetTrackEnvelopeByName" then
                        -- Get envelope by name
                        if #args >= 2 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                local envelope = reaper.GetTrackEnvelopeByName(track, args[2])
                                response.ok = true
                                response.ret = envelope
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "GetTrackEnvelopeByName requires 2 arguments"
                        end
                    
                    elseif fname == "GetTrackAutomationMode" then
                        -- Get track automation mode
                        if #args >= 1 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                local mode = reaper.GetTrackAutomationMode(track)
                                response.ok = true
                                response.ret = mode
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "GetTrackAutomationMode requires 1 argument"
                        end
                    
                    elseif fname == "SetTrackAutomationMode" then
                        -- Set track automation mode
                        if #args >= 2 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                reaper.SetTrackAutomationMode(track, args[2])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "SetTrackAutomationMode requires 2 arguments"
                        end
                    
                    elseif fname == "TrackFX_Delete" then
                        -- Delete FX from track
                        if #args >= 2 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                reaper.TrackFX_Delete(track, args[2])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_Delete requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_GetEnabled" then
                        -- Get FX enabled state
                        if #args >= 2 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                response.ret = reaper.TrackFX_GetEnabled(track, args[2])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_GetEnabled requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_SetEnabled" then
                        -- Set FX enabled state
                        if #args >= 3 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                reaper.TrackFX_SetEnabled(track, args[2], args[3])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_SetEnabled requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_GetFXName" then
                        -- Get FX name
                        if #args >= 4 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                local retval, name = reaper.TrackFX_GetFXName(track, args[2], "", args[4] or 256)
                                if retval then
                                    response.ret = name
                                    response.ok = true
                                else
                                    response.error = "Failed to get FX name"
                                    response.ok = false
                                end
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_GetFXName requires at least 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_GetNumParams" then
                        -- Get FX parameter count
                        if #args >= 2 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                response.ret = reaper.TrackFX_GetNumParams(track, args[2])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_GetNumParams requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_GetParam" then
                        -- Get FX parameter value
                        if #args >= 3 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                local retval, minval, maxval = reaper.TrackFX_GetParam(track, args[2], args[3])
                                response.value = retval
                                response.min = minval
                                response.max = maxval
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_GetParam requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_SetParam" then
                        -- Set FX parameter value
                        if #args >= 4 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                response.ret = reaper.TrackFX_SetParam(track, args[2], args[3], args[4])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_SetParam requires 4 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_GetParamName" then
                        -- Get FX parameter name
                        if #args >= 4 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                local retval, name = reaper.TrackFX_GetParamName(track, args[2], args[3], "", args[4] or 256)
                                if retval then
                                    response.ret = name
                                    response.ok = true
                                else
                                    response.error = "Failed to get parameter name"
                                    response.ok = false
                                end
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_GetParamName requires at least 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_GetPreset" then
                        -- Get FX preset name
                        if #args >= 3 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                local retval, name = reaper.TrackFX_GetPreset(track, args[2], "", args[3] or 256)
                                if retval then
                                    response.ret = name
                                    response.ok = true
                                else
                                    response.error = "Failed to get preset name"
                                    response.ok = false
                                end
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_GetPreset requires at least 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_SetPreset" then
                        -- Set FX preset
                        if #args >= 3 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                response.ret = reaper.TrackFX_SetPreset(track, args[2], args[3])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_SetPreset requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_Show" then
                        -- Show/hide FX window
                        if #args >= 3 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                reaper.TrackFX_Show(track, args[2], args[3])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_Show requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_GetOpen" then
                        -- Get FX window open state
                        if #args >= 2 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                response.ret = reaper.TrackFX_GetOpen(track, args[2])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_GetOpen requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_SetOpen" then
                        -- Set FX window open state
                        if #args >= 3 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                reaper.TrackFX_SetOpen(track, args[2], args[3])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_SetOpen requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_GetChainVisible" then
                        -- Get FX chain visibility
                        if #args >= 1 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                response.ret = reaper.TrackFX_GetChainVisible(track)
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_GetChainVisible requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_CopyToTrack" then
                        -- Copy/move FX between tracks
                        if #args >= 5 then
                            local src_track = nil
                            local dest_track = nil
                            
                            if type(args[1]) == "number" then
                                src_track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use source track pointer from previous call"
                                response.ok = false
                            else
                                src_track = args[1]
                            end
                            
                            if type(args[3]) == "number" then
                                dest_track = reaper.GetTrack(0, args[3])
                            elseif type(args[3]) == "table" and args[3].__ptr then
                                response.error = "Cannot use destination track pointer from previous call"
                                response.ok = false
                            else
                                dest_track = args[3]
                            end
                            
                            if src_track and dest_track then
                                reaper.TrackFX_CopyToTrack(src_track, args[2], dest_track, args[4], args[5])
                                response.ok = true
                            else
                                if not src_track then
                                    response.error = "Source track not found"
                                else
                                    response.error = "Destination track not found"
                                end
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_CopyToTrack requires 5 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_GetOffline" then
                        -- Get FX offline state
                        if #args >= 2 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                response.ret = reaper.TrackFX_GetOffline(track, args[2])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_GetOffline requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TrackFX_SetOffline" then
                        -- Set FX offline state
                        if #args >= 3 then
                            local track = nil
                            if type(args[1]) == "number" then
                                track = reaper.GetTrack(0, args[1])
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                track = args[1]
                            end
                            
                            if track then
                                reaper.TrackFX_SetOffline(track, args[2], args[3])
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "TrackFX_SetOffline requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetGlobalAutomationOverride" then
                        -- Get global automation override
                        local mode = reaper.GetGlobalAutomationOverride()
                        response.ok = true
                        response.ret = mode
                    
                    elseif fname == "SetGlobalAutomationOverride" then
                        -- Set global automation override
                        if #args >= 1 then
                            reaper.SetGlobalAutomationOverride(args[1])
                            response.ok = true
                        else
                            response.error = "SetGlobalAutomationOverride requires 1 argument"
                            response.ok = false
                        end
                    
                    else
                        -- Try generic function call
                        if reaper[fname] then
                            local ok, result = pcall(reaper[fname], table.unpack(args))
                            if ok then
                                response.ok = true
                                response.ret = result
                            else
                                response.error = "Error calling " .. fname .. ": " .. tostring(result)
                            end
                        else
                            response.error = "Unknown function: " .. fname
                        end
                    end
                    
                    -- Write response
                    local response_json = encode_json(response)
                    reaper.ShowConsoleMsg("Sending response " .. i .. ": " .. response_json .. "\n")
                    write_file(numbered_response_file, response_json)
                end
            end
            end)
            
            if not ok then
                -- Error occurred, write error response
                reaper.ShowConsoleMsg("ERROR processing request " .. i .. ": " .. tostring(err) .. "\n")
                local error_response = {ok = false, error = "Bridge error: " .. tostring(err)}
                write_file(numbered_response_file, encode_json(error_response))
            end
            
            -- Always clean up request file
            delete_file(numbered_request_file)
        end
    end
end

-- Main loop
ensure_dir()
reaper.ShowConsoleMsg("REAPER MCP Bridge (File-based, Full API) started\n")
reaper.ShowConsoleMsg("Bridge directory: " .. bridge_dir .. "\n")

function main()
    process_request()
    reaper.defer(main)
end

main()