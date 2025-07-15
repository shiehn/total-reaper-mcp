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
                            local track_index = args[1]
                            local item_index = args[2]
                            
                            -- Get track by index
                            local track
                            if track_index == -1 then
                                track = reaper.GetMasterTrack(0)
                            else
                                track = reaper.GetTrack(0, track_index)
                            end
                            
                            if not track then
                                response.error = "Track not found at index " .. tostring(track_index)
                                response.ok = false
                            else
                                -- Get item on track
                                local item = reaper.GetTrackMediaItem(track, item_index)
                                if not item then
                                    response.error = "Media item not found at index " .. tostring(item_index) .. " on track"
                                    response.ok = false
                                else
                                    -- Delete the item
                                    local result = reaper.DeleteTrackMediaItem(track, item)
                                    response.ok = result
                                end
                            end
                        else
                            response.error = "DeleteTrackMediaItem requires 2 arguments"
                        end
                    
                    elseif fname == "GetMediaItemInfo_Value" then
                        if #args >= 2 then
                            local item = args[1]
                            -- Handle item index or pointer
                            if type(args[1]) == "number" then
                                -- It's an item index
                                item = reaper.GetMediaItem(0, args[1])
                                if not item then
                                    response.error = "Item not found at index " .. tostring(args[1])
                                    response.ok = false
                                end
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                -- It's a pointer reference from a previous call - we can't use it
                                response.error = "Cannot use item pointer from previous call - use item index instead"
                                response.ok = false
                                item = nil
                            elseif type(args[1]) == "userdata" then
                                -- It's already an item object
                                item = args[1]
                            end
                            
                            if item then
                                local value = reaper.GetMediaItemInfo_Value(item, args[2])
                                response.ok = true
                                response.ret = value
                            end
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
                    
                    elseif fname == "SetMediaItemSelected" then
                        if #args >= 2 then
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
                                reaper.SetMediaItemSelected(item, args[2])
                                response.ok = true
                            else
                                response.error = "Invalid item parameter"
                                response.ok = false
                            end
                        else
                            response.error = "SetMediaItemSelected requires 2 arguments"
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
                    
                    elseif fname == "SortMIDIInItemTake" then
                        -- Combined function to sort MIDI
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
                                    -- Sort MIDI
                                    reaper.MIDI_Sort(take)
                                    response.ok = true
                                end
                            end
                        else
                            response.error = "SortMIDIInItemTake requires 2 arguments (item_index, take_index)"
                        end
                    
                    elseif fname == "InsertMIDICCToItemTake" then
                        -- Combined function to insert MIDI CC
                        if #args >= 7 then
                            local item_index = args[1]
                            local take_index = args[2]
                            local time = args[3]
                            local channel = args[4]
                            local cc_number = args[5]
                            local value = args[6]
                            local selected = args[7]
                            
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
                                    local ppq_pos = reaper.MIDI_GetPPQPosFromProjTime(take, time)
                                    
                                    -- Insert CC event
                                    local inserted = reaper.MIDI_InsertCC(take, selected, false, ppq_pos, 0xB0, channel, cc_number, value)
                                    if inserted then
                                        response.ok = true
                                    else
                                        response.ok = false
                                        response.error = "Failed to insert MIDI CC"
                                    end
                                end
                            end
                        else
                            response.error = "InsertMIDICCToItemTake requires 7 arguments"
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
                            local track_index = args[1]
                            
                            -- Handle case where args[1] might be a table with a numeric value
                            if type(track_index) == "table" then
                                -- Try multiple ways to extract numeric value from table
                                -- Check for direct numeric index
                                if track_index[1] and type(track_index[1]) == "number" then
                                    track_index = track_index[1]
                                -- Check for 'value' key
                                elseif track_index.value and type(track_index.value) == "number" then
                                    track_index = track_index.value
                                -- Check for 'track_index' key
                                elseif track_index.track_index and type(track_index.track_index) == "number" then
                                    track_index = track_index.track_index
                                else
                                    -- Try to find any numeric value in table
                                    for k, v in pairs(track_index) do
                                        if type(v) == "number" then
                                            track_index = v
                                            break
                                        end
                                    end
                                end
                            end
                            
                            if type(track_index) == "number" then
                                if track_index == -1 then
                                    -- Master track
                                    track = reaper.GetMasterTrack(0)
                                else
                                    track = reaper.GetTrack(0, track_index)
                                end
                            elseif type(args[1]) == "table" and args[1].__ptr then
                                response.error = "Cannot use track pointer from previous call"
                                response.ok = false
                            else
                                response.error = "Invalid track index type: " .. type(args[1]) .. " (could not extract number from table)"
                                response.ok = false
                            end
                            
                            if track then
                                local envelope = reaper.GetTrackEnvelopeByName(track, args[2])
                                response.ok = true
                                response.ret = envelope
                            elseif response.ok ~= false then
                                -- Only set error if not already set
                                local track_count = reaper.CountTracks(0)
                                response.error = "Track not found at index " .. tostring(track_index) .. " (project has " .. track_count .. " tracks)"
                                response.ok = false
                            end
                        else
                            response.error = "GetTrackEnvelopeByName requires 2 arguments"
                        end
                    
                    elseif fname == "GetTrackAutomationMode" then
                        -- Get track automation mode
                        if #args >= 1 then
                            local track = nil
                            local track_index = args[1]
                            
                            -- Handle case where args[1] might be a table with a numeric value
                            if type(track_index) == "table" then
                                -- Try multiple ways to extract numeric value from table
                                if track_index[1] and type(track_index[1]) == "number" then
                                    track_index = track_index[1]
                                elseif track_index.value and type(track_index.value) == "number" then
                                    track_index = track_index.value
                                elseif track_index.track_index and type(track_index.track_index) == "number" then
                                    track_index = track_index.track_index
                                else
                                    -- Try to find any numeric value in table
                                    for k, v in pairs(track_index) do
                                        if type(v) == "number" then
                                            track_index = v
                                            break
                                        end
                                    end
                                end
                            end
                            
                            if type(track_index) == "number" then
                                track = reaper.GetTrack(0, track_index)
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
                            local track_index = args[1]
                            
                            -- Handle case where args[1] might be a table with a numeric value
                            if type(track_index) == "table" then
                                -- Try multiple ways to extract numeric value from table
                                if track_index[1] and type(track_index[1]) == "number" then
                                    track_index = track_index[1]
                                elseif track_index.value and type(track_index.value) == "number" then
                                    track_index = track_index.value
                                elseif track_index.track_index and type(track_index.track_index) == "number" then
                                    track_index = track_index.track_index
                                else
                                    -- Try to find any numeric value in table
                                    for k, v in pairs(track_index) do
                                        if type(v) == "number" then
                                            track_index = v
                                            break
                                        end
                                    end
                                end
                            end
                            
                            if type(track_index) == "number" then
                                track = reaper.GetTrack(0, track_index)
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
                    
                    elseif fname == "GetMainHwnd" then
                        -- Get main window handle
                        local hwnd = reaper.GetMainHwnd()
                        response.ok = true
                        response.ret = hwnd
                    
                    elseif fname == "GetMousePosition" then
                        -- Get current mouse position
                        local x, y = reaper.GetMousePosition()
                        response.ok = true
                        response.ret = {x, y}
                    
                    elseif fname == "GetCursorContext" then
                        -- Get cursor context
                        local context = reaper.GetCursorContext()
                        response.ok = true
                        response.ret = context
                    
                    elseif fname == "ShowMessageBox" then
                        -- Show message box
                        if #args >= 3 then
                            local result = reaper.ShowMessageBox(args[1], args[2], args[3])
                            response.ok = true
                            response.ret = result
                        else
                            response.error = "ShowMessageBox requires 3 arguments (message, title, type)"
                            response.ok = false
                        end
                    
                    elseif fname == "ShowConsoleMsg" then
                        -- Show console message
                        if #args >= 1 then
                            reaper.ShowConsoleMsg(args[1])
                            response.ok = true
                        else
                            response.error = "ShowConsoleMsg requires 1 argument (message)"
                            response.ok = false
                        end
                    
                    elseif fname == "ClearConsole" then
                        -- Clear console
                        reaper.ClearConsole()
                        response.ok = true
                    
                    elseif fname == "PCM_Source_CreateFromFile" then
                        -- Create PCM source from file
                        if #args >= 1 then
                            local source = reaper.PCM_Source_CreateFromFile(args[1])
                            response.ok = true
                            response.ret = source
                        else
                            response.error = "PCM_Source_CreateFromFile requires 1 argument (filename)"
                            response.ok = false
                        end
                    
                    elseif fname == "SetMediaItemTake_Source" then
                        -- Set media source on take
                        if #args >= 2 then
                            local retval = reaper.SetMediaItemTake_Source(args[1], args[2])
                            response.ok = true
                            response.ret = retval
                        else
                            response.error = "SetMediaItemTake_Source requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetMediaItemTake_Source" then
                        -- Get media source from take
                        if #args >= 1 then
                            local source = reaper.GetMediaItemTake_Source(args[1])
                            response.ok = true
                            response.ret = source
                        else
                            response.error = "GetMediaItemTake_Source requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetMediaSourceSampleRate" then
                        -- Get sample rate from media source
                        if #args >= 1 then
                            local samplerate = reaper.GetMediaSourceSampleRate(args[1])
                            response.ok = true
                            response.ret = samplerate
                        else
                            response.error = "GetMediaSourceSampleRate requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetMediaSourceNumChannels" then
                        -- Get channel count from media source
                        if #args >= 1 then
                            local channels = reaper.GetMediaSourceNumChannels(args[1])
                            response.ok = true
                            response.ret = channels
                        else
                            response.error = "GetMediaSourceNumChannels requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "DB2SLIDER" then
                        -- Convert dB to slider value
                        if #args >= 1 then
                            local slider = reaper.DB2SLIDER(args[1])
                            response.ok = true
                            response.ret = slider
                        else
                            response.error = "DB2SLIDER requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "SLIDER2DB" then
                        -- Convert slider value to dB
                        if #args >= 1 then
                            local db = reaper.SLIDER2DB(args[1])
                            response.ok = true
                            response.ret = db
                        else
                            response.error = "SLIDER2DB requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "AddTakeToMediaItem" then
                        -- Add take to media item
                        if #args >= 1 then
                            local take = reaper.AddTakeToMediaItem(args[1])
                            response.ok = true
                            response.ret = take
                        else
                            response.error = "AddTakeToMediaItem requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "CountTakes" then
                        -- Count takes in media item
                        if #args >= 1 then
                            local count = reaper.CountTakes(args[1])
                            response.ok = true
                            response.ret = count
                        else
                            response.error = "CountTakes requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetTake" then
                        -- Get take from item by indices
                        if #args >= 2 then
                            local item = reaper.GetMediaItem(0, args[1])
                            if item then
                                local take = reaper.GetMediaItemTake(item, args[2])
                                response.ok = true
                                response.ret = take
                            else
                                response.error = "Item not found"
                                response.ok = false
                            end
                        else
                            response.error = "GetTake requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "IsTrackVisible" then
                        -- Check if track is visible in TCP/MCP
                        if #args >= 2 then
                            local visible = reaper.IsTrackVisible(args[1], args[2])
                            response.ok = true
                            response.ret = visible
                        else
                            response.error = "IsTrackVisible requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "SetOnlyTrackSelected" then
                        -- Set only one track selected
                        if #args >= 1 then
                            local track = args[1]
                            -- Handle track index
                            if type(track) == "number" then
                                track = reaper.GetTrack(0, track)
                            end
                            if track then
                                reaper.SetOnlyTrackSelected(track)
                                response.ok = true
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "SetOnlyTrackSelected requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "NamedCommandLookup" then
                        -- Look up named command
                        if #args >= 1 then
                            local cmd_id = reaper.NamedCommandLookup(args[1])
                            response.ok = true
                            response.ret = cmd_id
                        else
                            response.error = "NamedCommandLookup requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "ReverseNamedCommandLookup" then
                        -- Reverse command lookup
                        if #args >= 2 then
                            local name = reaper.ReverseNamedCommandLookup(args[1], args[2])
                            response.ok = true
                            response.ret = name or ""
                        else
                            response.error = "ReverseNamedCommandLookup requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetToggleCommandStateEx" then
                        -- Get toggle command state for section
                        if #args >= 2 then
                            local state = reaper.GetToggleCommandStateEx(args[1], args[2])
                            response.ok = true
                            response.ret = state
                        else
                            response.error = "GetToggleCommandStateEx requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "RefreshToolbar" then
                        -- Refresh toolbar
                        if #args >= 1 then
                            reaper.RefreshToolbar(args[1])
                            response.ok = true
                        else
                            response.error = "RefreshToolbar requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "EnumerateFiles" then
                        -- Enumerate files
                        if #args >= 2 then
                            local file = reaper.EnumerateFiles(args[1], args[2])
                            response.ok = true
                            response.ret = file or ""
                        else
                            response.error = "EnumerateFiles requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "EnumerateSubdirectories" then
                        -- Enumerate subdirectories
                        if #args >= 2 then
                            local dir = reaper.EnumerateSubdirectories(args[1], args[2])
                            response.ok = true
                            response.ret = dir or ""
                        else
                            response.error = "EnumerateSubdirectories requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetProjectPath" then
                        -- Get project path
                        if #args >= 1 then
                            local path = reaper.GetProjectPath(args[1])
                            response.ok = true
                            response.ret = path or ""
                        else
                            response.error = "GetProjectPath requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetProjectName" then
                        -- Get project name
                        if #args >= 1 then
                            local name = reaper.GetProjectName(args[1])
                            response.ok = true
                            response.ret = name or ""
                        else
                            response.error = "GetProjectName requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "IsProjectDirty" then
                        -- Check if project is dirty
                        if #args >= 1 then
                            local dirty = reaper.IsProjectDirty(args[1])
                            response.ok = true
                            response.ret = dirty
                        else
                            response.error = "IsProjectDirty requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetResourcePath" then
                        -- Get resource path
                        local path = reaper.GetResourcePath()
                        response.ok = true
                        response.ret = path
                    
                    elseif fname == "GetExePath" then
                        -- Get exe path
                        local path = reaper.GetExePath()
                        response.ok = true
                        response.ret = path
                    
                    elseif fname == "GetExtState" then
                        -- Get extended state
                        if #args >= 2 then
                            local value = reaper.GetExtState(args[1], args[2])
                            response.ok = true
                            response.ret = value or ""
                        else
                            response.error = "GetExtState requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "SetExtState" then
                        -- Set extended state
                        if #args >= 4 then
                            reaper.SetExtState(args[1], args[2], args[3], args[4])
                            response.ok = true
                        else
                            response.error = "SetExtState requires 4 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "HasExtState" then
                        -- Check if extended state exists
                        if #args >= 2 then
                            local exists = reaper.HasExtState(args[1], args[2])
                            response.ok = true
                            response.ret = exists
                        else
                            response.error = "HasExtState requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "DeleteExtState" then
                        -- Delete extended state
                        if #args >= 3 then
                            reaper.DeleteExtState(args[1], args[2], args[3])
                            response.ok = true
                        else
                            response.error = "DeleteExtState requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "DockWindowActivate" then
                        -- Activate docker window
                        if #args >= 1 then
                            reaper.DockWindowActivate(args[1])
                            response.ok = true
                        else
                            response.error = "DockWindowActivate requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "DockWindowAddEx" then
                        -- Add window to docker
                        if #args >= 4 then
                            reaper.DockWindowAddEx(args[1], args[2], args[3], args[4])
                            response.ok = true
                        else
                            response.error = "DockWindowAddEx requires 4 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "DockWindowRefresh" then
                        -- Refresh docker windows
                        reaper.DockWindowRefresh()
                        response.ok = true
                    
                    elseif fname == "DockWindowRefreshByName" then
                        -- Refresh docker window by name
                        if #args >= 1 then
                            reaper.DockWindowRefreshByName(args[1])
                            response.ok = true
                        else
                            response.error = "DockWindowRefreshByName requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "DockGetPosition" then
                        -- Get docker position
                        if #args >= 1 then
                            local pos = reaper.DockGetPosition(args[1])
                            response.ok = true
                            response.ret = pos
                        else
                            response.error = "DockGetPosition requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "DeleteTakeFromMediaItem" then
                        -- Delete take from item
                        if #args >= 1 then
                            local result = reaper.DeleteTakeFromMediaItem(args[1])
                            response.ok = result
                        else
                            response.error = "DeleteTakeFromMediaItem requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetNumTakeMarkers" then
                        -- Get number of take markers
                        if #args >= 1 then
                            local count = reaper.GetNumTakeMarkers(args[1])
                            response.ok = true
                            response.ret = count
                        else
                            response.error = "GetNumTakeMarkers requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetTakeMarker" then
                        -- Get take marker info
                        if #args >= 2 then
                            local position, name, color = reaper.GetTakeMarker(args[1], args[2])
                            response.ok = true
                            response.position = position
                            response.name = name or ""
                            response.color = color or 0
                        else
                            response.error = "GetTakeMarker requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "SetTakeMarker" then
                        -- Set/add take marker
                        if #args >= 5 then
                            local idx = reaper.SetTakeMarker(args[1], args[2], args[3], args[4], args[5])
                            response.ok = true
                            response.ret = idx
                        else
                            response.error = "SetTakeMarker requires 5 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "DeleteTakeMarker" then
                        -- Delete take marker
                        if #args >= 2 then
                            local result = reaper.DeleteTakeMarker(args[1], args[2])
                            response.ok = result
                        else
                            response.error = "DeleteTakeMarker requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "CountTakeEnvelopes" then
                        -- Count take envelopes
                        if #args >= 1 then
                            local count = reaper.CountTakeEnvelopes(args[1])
                            response.ok = true
                            response.ret = count
                        else
                            response.error = "CountTakeEnvelopes requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetTakeEnvelopeByName" then
                        -- Get take envelope by name
                        if #args >= 2 then
                            local env = reaper.GetTakeEnvelopeByName(args[1], args[2])
                            response.ok = true
                            response.ret = env
                        else
                            response.error = "GetTakeEnvelopeByName requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "EnumProjectMarkers" then
                        -- Enumerate project markers
                        if #args >= 1 then
                            local retval, isrgn, pos, rgnend, name, markrgnindexnumber = reaper.EnumProjectMarkers(args[1])
                            response.ok = retval > 0
                            response.isrgn = isrgn
                            response.pos = pos
                            response.rgnend = rgnend
                            response.name = name or ""
                            response.markrgnindexnumber = markrgnindexnumber
                        else
                            response.error = "EnumProjectMarkers requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "EnumProjectMarkers3" then
                        -- Enumerate project markers with color
                        if #args >= 2 then
                            local retval, isrgn, pos, rgnend, name, markrgnindexnumber, color = reaper.EnumProjectMarkers3(args[1], args[2])
                            response.ok = retval > 0
                            response.isrgn = isrgn
                            response.pos = pos
                            response.rgnend = rgnend
                            response.name = name or ""
                            response.markrgnindexnumber = markrgnindexnumber
                            response.color = color
                        else
                            response.error = "EnumProjectMarkers3 requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "CountProjectMarkers" then
                        -- Count project markers
                        if #args >= 1 then
                            local num_markers, num_regions = reaper.CountProjectMarkers(args[1])
                            response.ok = true
                            response.num_markers = num_markers
                            response.num_regions = num_regions
                        else
                            response.error = "CountProjectMarkers requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "SetProjectMarker" then
                        -- Set project marker
                        if #args >= 5 then
                            local result = reaper.SetProjectMarker(args[1], args[2], args[3], args[4], args[5])
                            response.ok = result
                        else
                            response.error = "SetProjectMarker requires 5 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "SetProjectMarker3" then
                        -- Set project marker with color
                        if #args >= 7 then
                            local result = reaper.SetProjectMarker3(args[1], args[2], args[3], args[4], args[5], args[6], args[7])
                            response.ok = result
                        else
                            response.error = "SetProjectMarker3 requires 7 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "DeleteProjectMarker" then
                        -- Delete project marker
                        if #args >= 3 then
                            local result = reaper.DeleteProjectMarker(args[1], args[2], args[3])
                            response.ok = true
                            response.ret = result
                        else
                            response.error = "DeleteProjectMarker requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GoToMarker" then
                        -- Go to marker
                        if #args >= 3 then
                            reaper.GoToMarker(args[1], args[2], args[3])
                            response.ok = true
                        else
                            response.error = "GoToMarker requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "CountTrackEnvelopes" then
                        -- Count track envelopes
                        if #args >= 1 then
                            local count = reaper.CountTrackEnvelopes(args[1])
                            response.ok = true
                            response.ret = count
                        else
                            response.error = "CountTrackEnvelopes requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetTrackName" then
                        -- Get track name
                        if #args >= 1 then
                            local track = reaper.GetTrack(0, args[1])
                            if track then
                                local retval, name = reaper.GetTrackName(track)
                                response.ok = retval
                                response.ret = name or ""
                            else
                                response.error = "Track not found"
                                response.ok = false
                            end
                        else
                            response.error = "GetTrackName requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetMediaItem_Track" then
                        -- Get item's track
                        if #args >= 1 then
                            local track = reaper.GetMediaItem_Track(args[1])
                            response.ok = true
                            response.ret = track
                        else
                            response.error = "GetMediaItem_Track requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "TakeIsMIDI" then
                        -- Check if take is MIDI
                        if #args >= 1 then
                            local ismidi = reaper.TakeIsMIDI(args[1])
                            response.ok = true
                            response.ret = ismidi
                        else
                            response.error = "TakeIsMIDI requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "MIDI_GetNote" then
                        -- Get MIDI note
                        if #args >= 2 then
                            local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(args[1], args[2])
                            response.ok = retval
                            response.selected = selected
                            response.muted = muted
                            response.startppqpos = startppqpos
                            response.endppqpos = endppqpos
                            response.chan = chan
                            response.pitch = pitch
                            response.vel = vel
                        else
                            response.error = "MIDI_GetNote requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "TransposeMIDINotes" then
                        -- Transpose MIDI notes by item/take indices
                        if #args >= 4 then
                            local item_index = args[1]
                            local take_index = args[2]
                            local semitones = args[3]
                            local selected_only = args[4]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Item not found"
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Take not found"
                                    response.ok = false
                                else
                                    -- Check if MIDI
                                    if not reaper.TakeIsMIDI(take) then
                                        response.error = "Take is not MIDI"
                                        response.ok = false
                                    else
                                        -- Count notes
                                        local retval, notes = reaper.MIDI_CountEvts(take)
                                        local transposed = 0
                                        
                                        -- Transpose each note
                                        for i = 0, notes - 1 do
                                            local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
                                            
                                            if retval and (not selected_only or selected) then
                                                local new_pitch = math.max(0, math.min(127, pitch + semitones))
                                                reaper.MIDI_SetNote(take, i, selected, muted, startppqpos, endppqpos, chan, new_pitch, vel, false)
                                                transposed = transposed + 1
                                            end
                                        end
                                        
                                        -- Sort notes
                                        reaper.MIDI_Sort(take)
                                        
                                        response.ok = true
                                        response.transposed = transposed
                                        response.notes = notes
                                    end
                                end
                            end
                        else
                            response.error = "TransposeMIDINotes requires 4 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "QuantizeMIDINotes" then
                        -- Quantize MIDI notes by item/take indices
                        if #args >= 4 then
                            local item_index = args[1]
                            local take_index = args[2]
                            local grid_size = args[3]  -- In PPQ
                            local strength = args[4]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Item not found"
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Take not found"
                                    response.ok = false
                                else
                                    -- Check if MIDI
                                    if not reaper.TakeIsMIDI(take) then
                                        response.error = "Take is not MIDI"
                                        response.ok = false
                                    else
                                        -- Count notes
                                        local retval, notes = reaper.MIDI_CountEvts(take)
                                        local quantized = 0
                                        
                                        -- Quantize each note
                                        for i = 0, notes - 1 do
                                            local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
                                            
                                            if retval then
                                                -- Calculate quantized position
                                                local nearest_grid = math.floor(startppqpos / grid_size + 0.5) * grid_size
                                                -- Apply strength
                                                local new_pos = startppqpos + (nearest_grid - startppqpos) * strength
                                                -- Calculate new end position (maintain length)
                                                local length = endppqpos - startppqpos
                                                local new_end = new_pos + length
                                                
                                                reaper.MIDI_SetNote(take, i, selected, muted, new_pos, new_end, chan, pitch, vel, false)
                                                quantized = quantized + 1
                                            end
                                        end
                                        
                                        -- Sort notes
                                        reaper.MIDI_Sort(take)
                                        
                                        response.ok = true
                                        response.quantized = quantized
                                        response.notes = notes
                                    end
                                end
                            end
                        else
                            response.error = "QuantizeMIDINotes requires 4 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "HumanizeMIDITiming" then
                        -- Humanize MIDI notes by item/take indices
                        if #args >= 4 then
                            local item_index = args[1]
                            local take_index = args[2]
                            local timing_amount = args[3]  -- In seconds
                            local velocity_amount = args[4]  -- 0-1 range
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Item not found"
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Take not found"
                                    response.ok = false
                                else
                                    -- Check if MIDI
                                    if not reaper.TakeIsMIDI(take) then
                                        response.error = "Take is not MIDI"
                                        response.ok = false
                                    else
                                        -- Count notes
                                        local retval, notes = reaper.MIDI_CountEvts(take)
                                        local humanized = 0
                                        
                                        local ppq_per_quarter = 960
                                        local max_timing_shift = timing_amount * ppq_per_quarter
                                        
                                        -- Humanize each note
                                        for i = 0, notes - 1 do
                                            local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
                                            
                                            if retval then
                                                -- Randomize timing
                                                local timing_shift = (math.random() * 2 - 1) * max_timing_shift
                                                local new_start = math.max(0, startppqpos + timing_shift)
                                                local new_end = endppqpos + timing_shift
                                                
                                                -- Randomize velocity
                                                local vel_shift = (math.random() * 2 - 1) * velocity_amount * 127
                                                local new_vel = math.max(1, math.min(127, math.floor(vel + vel_shift)))
                                                
                                                reaper.MIDI_SetNote(take, i, selected, muted, new_start, new_end, chan, pitch, new_vel, false)
                                                humanized = humanized + 1
                                            end
                                        end
                                        
                                        -- Sort notes
                                        reaper.MIDI_Sort(take)
                                        
                                        response.ok = true
                                        response.humanized = humanized
                                        response.notes = notes
                                    end
                                end
                            end
                        else
                            response.error = "HumanizeMIDITiming requires 4 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "AnalyzeMIDIPattern" then
                        -- Analyze MIDI pattern by item/take indices
                        if #args >= 2 then
                            local item_index = args[1]
                            local take_index = args[2]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Item not found"
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Take not found"
                                    response.ok = false
                                else
                                    -- Check if MIDI
                                    if not reaper.TakeIsMIDI(take) then
                                        response.error = "Take is not MIDI"
                                        response.ok = false
                                    else
                                        -- Count notes
                                        local retval, notes = reaper.MIDI_CountEvts(take)
                                        
                                        -- Analyze first few notes for patterns
                                        local pitches = {}
                                        local velocities = {}
                                        local max_notes = math.min(notes, 50)
                                        
                                        for i = 0, max_notes - 1 do
                                            local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
                                            if retval then
                                                table.insert(pitches, pitch)
                                                table.insert(velocities, vel)
                                            end
                                        end
                                        
                                        if #pitches == 0 then
                                            response.ok = true
                                            response.analysis = "No notes to analyze"
                                        else
                                            -- Basic pattern analysis
                                            local min_pitch = math.min(table.unpack(pitches))
                                            local max_pitch = math.max(table.unpack(pitches))
                                            local pitch_range = max_pitch - min_pitch
                                            
                                            local total_vel = 0
                                            for _, v in ipairs(velocities) do
                                                total_vel = total_vel + v
                                            end
                                            local avg_velocity = total_vel / #velocities
                                            
                                            -- Detect intervals
                                            local ascending = true
                                            local descending = true
                                            for i = 2, #pitches do
                                                if pitches[i] <= pitches[i-1] then
                                                    ascending = false
                                                end
                                                if pitches[i] >= pitches[i-1] then
                                                    descending = false
                                                end
                                            end
                                            
                                            local pattern_type = "mixed"
                                            if ascending then pattern_type = "ascending"
                                            elseif descending then pattern_type = "descending"
                                            end
                                            
                                            response.ok = true
                                            response.notes_analyzed = #pitches
                                            response.pitch_range = pitch_range
                                            response.pattern_type = pattern_type
                                            response.avg_velocity = avg_velocity
                                        end
                                    end
                                end
                            end
                        else
                            response.error = "AnalyzeMIDIPattern requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GenerateMIDIChordSequence" then
                        -- Generate MIDI chord sequence by item/take indices
                        if #args >= 4 then
                            local item_index = args[1]
                            local take_index = args[2]
                            local chord_progression = args[3]  -- Table of chord names
                            local duration = args[4]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Item not found"
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Take not found"
                                    response.ok = false
                                else
                                    -- Check if MIDI
                                    if not reaper.TakeIsMIDI(take) then
                                        response.error = "Take is not MIDI"
                                        response.ok = false
                                    else
                                        -- Chord definitions (simplified)
                                        local chord_types = {
                                            maj = {0, 4, 7},
                                            min = {0, 3, 7},
                                            ["7"] = {0, 4, 7, 10},
                                            maj7 = {0, 4, 7, 11},
                                            min7 = {0, 3, 7, 10},
                                            dim = {0, 3, 6},
                                            aug = {0, 4, 8}
                                        }
                                        
                                        -- Note name to MIDI mapping
                                        local note_map = {C = 0, D = 2, E = 4, F = 5, G = 7, A = 9, B = 11}
                                        
                                        local ppq_per_quarter = 960
                                        local current_pos = 0
                                        local chords_added = 0
                                        
                                        for _, chord_name in ipairs(chord_progression) do
                                            -- Parse chord (e.g., "Cmaj", "Am7")
                                            local root_note = nil
                                            local chord_type = nil
                                            
                                            -- Find root note
                                            for note, value in pairs(note_map) do
                                                if string.sub(chord_name, 1, #note) == note then
                                                    root_note = value + 60  -- Middle octave
                                                    local rest = string.sub(chord_name, #note + 1)
                                                    
                                                    -- Handle sharps/flats
                                                    if string.sub(rest, 1, 1) == "#" then
                                                        root_note = root_note + 1
                                                        rest = string.sub(rest, 2)
                                                    elseif string.sub(rest, 1, 1) == "b" then
                                                        root_note = root_note - 1
                                                        rest = string.sub(rest, 2)
                                                    end
                                                    
                                                    -- Find chord type
                                                    chord_type = chord_types[rest] or chord_types.maj
                                                    break
                                                end
                                            end
                                            
                                            if root_note then
                                                -- Insert chord notes
                                                for _, interval in ipairs(chord_type) do
                                                    local pitch = root_note + interval
                                                    reaper.MIDI_InsertNote(take, false, false, current_pos, 
                                                                          current_pos + (duration * ppq_per_quarter),
                                                                          0, pitch, 80, false)
                                                end
                                                chords_added = chords_added + 1
                                                current_pos = current_pos + (duration * ppq_per_quarter)
                                            end
                                        end
                                        
                                        -- Sort notes
                                        reaper.MIDI_Sort(take)
                                        
                                        response.ok = true
                                        response.chords_added = chords_added
                                        response.progression = table.concat(chord_progression, " → ")
                                    end
                                end
                            end
                        else
                            response.error = "GenerateMIDIChordSequence requires 4 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "DetectMIDIChordProgressions" then
                        -- Detect chord progressions by item/take indices
                        if #args >= 2 then
                            local item_index = args[1]
                            local take_index = args[2]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Item not found"
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Take not found"
                                    response.ok = false
                                else
                                    -- Check if MIDI
                                    if not reaper.TakeIsMIDI(take) then
                                        response.error = "Take is not MIDI"
                                        response.ok = false
                                    else
                                        -- Get all notes
                                        local retval, notes = reaper.MIDI_CountEvts(take)
                                        
                                        -- Group notes by time to find chords
                                        local time_groups = {}
                                        
                                        for i = 0, notes - 1 do
                                            local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
                                            if retval then
                                                -- Quantize time to group simultaneous notes
                                                local time_key = math.floor(startppqpos / 240) * 240  -- Quarter note quantization
                                                
                                                if not time_groups[time_key] then
                                                    time_groups[time_key] = {}
                                                end
                                                table.insert(time_groups[time_key], pitch)
                                            end
                                        end
                                        
                                        -- Analyze chords
                                        local chords = {}
                                        local sorted_times = {}
                                        for time, _ in pairs(time_groups) do
                                            table.insert(sorted_times, time)
                                        end
                                        table.sort(sorted_times)
                                        
                                        local count = 0
                                        for _, time in ipairs(sorted_times) do
                                            if count >= 10 then break end  -- First 10 chords
                                            
                                            local pitches = time_groups[time]
                                            if #pitches >= 3 then  -- At least 3 notes for a chord
                                                -- Sort pitches
                                                table.sort(pitches)
                                                
                                                -- Basic chord detection
                                                local root = pitches[1] % 12
                                                local note_names = {"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"}
                                                local chord_name = note_names[root + 1]
                                                
                                                -- Check for major/minor (simplified)
                                                if #pitches >= 3 then
                                                    local third = (pitches[2] - pitches[1]) % 12
                                                    if third == 4 then
                                                        chord_name = chord_name .. " major"
                                                    elseif third == 3 then
                                                        chord_name = chord_name .. " minor"
                                                    end
                                                end
                                                
                                                table.insert(chords, chord_name)
                                                count = count + 1
                                            end
                                        end
                                        
                                        if #chords > 0 then
                                            response.ok = true
                                            response.progression = table.concat(chords, " → ")
                                        else
                                            response.ok = true
                                            response.progression = "No clear chord progression detected"
                                        end
                                    end
                                end
                            end
                        else
                            response.error = "DetectMIDIChordProgressions requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetMIDINoteDistribution" then
                        -- Get MIDI note distribution by item/take indices
                        if #args >= 2 then
                            local item_index = args[1]
                            local take_index = args[2]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Item not found"
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Take not found"
                                    response.ok = false
                                else
                                    -- Check if MIDI
                                    if not reaper.TakeIsMIDI(take) then
                                        response.error = "Take is not MIDI"
                                        response.ok = false
                                    else
                                        -- Get all notes
                                        local retval, notes = reaper.MIDI_CountEvts(take)
                                        
                                        -- Count note occurrences
                                        local pitch_counts = {}
                                        local total_velocity = 0
                                        
                                        for i = 0, notes - 1 do
                                            local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
                                            if retval then
                                                pitch_counts[pitch] = (pitch_counts[pitch] or 0) + 1
                                                total_velocity = total_velocity + vel
                                            end
                                        end
                                        
                                        -- Build distribution info
                                        local distribution = {}
                                        for pitch, count in pairs(pitch_counts) do
                                            table.insert(distribution, {pitch=pitch, count=count})
                                        end
                                        
                                        -- Sort by count
                                        table.sort(distribution, function(a, b) return a.count > b.count end)
                                        
                                        response.ok = true
                                        response.notes_total = notes
                                        response.distribution = distribution
                                        response.avg_velocity = notes > 0 and (total_velocity / notes) or 0
                                    end
                                end
                            end
                        else
                            response.error = "GetMIDINoteDistribution requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "DetectMIDIKeySignature" then
                        -- Detect key signature by item/take indices
                        if #args >= 2 then
                            local item_index = args[1]
                            local take_index = args[2]
                            
                            -- Get item
                            local item = reaper.GetMediaItem(0, item_index)
                            if not item then
                                response.error = "Item not found"
                                response.ok = false
                            else
                                -- Get take
                                local take = reaper.GetMediaItemTake(item, take_index)
                                if not take then
                                    response.error = "Take not found"
                                    response.ok = false
                                else
                                    -- Check if MIDI
                                    if not reaper.TakeIsMIDI(take) then
                                        response.error = "Take is not MIDI"
                                        response.ok = false
                                    else
                                        -- Get all notes
                                        local retval, notes = reaper.MIDI_CountEvts(take)
                                        
                                        -- Count pitch classes
                                        local pitch_classes = {}
                                        for i = 0, 11 do
                                            pitch_classes[i] = 0
                                        end
                                        
                                        for i = 0, notes - 1 do
                                            local retval, selected, muted, startppqpos, endppqpos, chan, pitch, vel = reaper.MIDI_GetNote(take, i)
                                            if retval then
                                                local pitch_class = pitch % 12
                                                pitch_classes[pitch_class] = pitch_classes[pitch_class] + 1
                                            end
                                        end
                                        
                                        -- Key profiles (simplified)
                                        local major_profile = {6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88}
                                        local minor_profile = {6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17}
                                        
                                        local note_names = {"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"}
                                        
                                        -- Calculate correlation with each key
                                        local best_major_key = nil
                                        local best_major_score = -1
                                        local best_minor_key = nil
                                        local best_minor_score = -1
                                        
                                        for root = 0, 11 do
                                            -- Calculate major correlation
                                            local major_score = 0
                                            local minor_score = 0
                                            
                                            for i = 0, 11 do
                                                local shifted_idx = (i + root) % 12
                                                major_score = major_score + pitch_classes[shifted_idx] * major_profile[i + 1]
                                                minor_score = minor_score + pitch_classes[shifted_idx] * minor_profile[i + 1]
                                            end
                                            
                                            if major_score > best_major_score then
                                                best_major_score = major_score
                                                best_major_key = root
                                            end
                                            
                                            if minor_score > best_minor_score then
                                                best_minor_score = minor_score
                                                best_minor_key = root
                                            end
                                        end
                                        
                                        -- Determine major or minor
                                        local key, confidence
                                        if best_major_score > best_minor_score then
                                            key = note_names[best_major_key + 1] .. " major"
                                            confidence = (best_major_score / (best_major_score + best_minor_score)) * 100
                                        else
                                            key = note_names[best_minor_key + 1] .. " minor"
                                            confidence = (best_minor_score / (best_major_score + best_minor_score)) * 100
                                        end
                                        
                                        response.ok = true
                                        response.key = key
                                        response.confidence = confidence
                                        response.notes_analyzed = notes
                                    end
                                end
                            end
                        else
                            response.error = "DetectMIDIKeySignature requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "Master_GetTempo" then
                        -- Get master tempo
                        local tempo = reaper.Master_GetTempo()
                        response.ok = true
                        response.ret = tempo
                    
                    elseif fname == "CountTempoTimeSigMarkers" then
                        -- Count tempo/time sig markers
                        if #args >= 1 then
                            local count = reaper.CountTempoTimeSigMarkers(args[1])
                            response.ok = true
                            response.ret = count
                        else
                            response.error = "CountTempoTimeSigMarkers requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "PCM_Source_GetSectionInfo" then
                        -- Get PCM source section info
                        if #args >= 2 then
                            local source = args[1]
                            local offset = args[2]
                            -- Note: This is a simplified version - real API has more params
                            -- For video detection, we'll check file extension
                            local filename_result = reaper.GetMediaSourceFileName(source, "")
                            local has_video = false
                            if filename_result and filename_result ~= "" then
                                local ext = filename_result:match("%.([^%.]+)$")
                                if ext then
                                    ext = ext:lower()
                                    has_video = (ext == "mp4" or ext == "mov" or ext == "avi" or 
                                               ext == "mkv" or ext == "webm" or ext == "wmv")
                                end
                            end
                            response.ok = true
                            response.has_video = has_video
                            response.ret = true
                        else
                            response.error = "PCM_Source_GetSectionInfo requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetMediaSourceFileName" then
                        -- Get media source filename
                        if #args >= 2 then
                            local filename = reaper.GetMediaSourceFileName(args[1], args[2])
                            response.ok = true
                            response.ret = filename
                        else
                            response.error = "GetMediaSourceFileName requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetProjectInfo" then
                        -- Get project info (simplified)
                        if #args >= 2 then
                            local proj = args[1]
                            local param = args[2]
                            if param == "PROJECT_FRAMERATE" then
                                -- Get project frame rate (default 30)
                                local fps = 30.0  -- Default
                                response.ok = true
                                response.ret = fps
                            else
                                response.error = "Unknown project info parameter: " .. param
                                response.ok = false
                            end
                        else
                            response.error = "GetProjectInfo requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "SetEditCurPos" then
                        -- Set edit cursor position
                        if #args >= 3 then
                            reaper.SetEditCurPos(args[1], args[2], args[3])
                            response.ok = true
                            response.ret = true
                        else
                            response.error = "SetEditCurPos requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "PCM_Source_BuildPeaks" then
                        -- Build peaks for PCM source
                        if #args >= 2 then
                            local ret = reaper.PCM_Source_BuildPeaks(args[1], args[2])
                            response.ok = true
                            response.ret = ret
                        else
                            response.error = "PCM_Source_BuildPeaks requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "UpdateItemInProject" then
                        -- Update item in project
                        if #args >= 1 then
                            reaper.UpdateItemInProject(args[1])
                            response.ok = true
                            response.ret = true
                        else
                            response.error = "UpdateItemInProject requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetSet_ArrangeView2" then
                        -- Get/set arrange view
                        if #args >= 4 then
                            local screen_x_start, screen_x_end = reaper.GetSet_ArrangeView2(args[1], args[2], args[3], args[4])
                            response.ok = true
                            response.start_time = screen_x_start
                            response.end_time = screen_x_end
                            response.ret = true
                        else
                            response.error = "GetSet_ArrangeView2 requires 4 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetMediaItemTakeInfo_Value" then
                        -- Get take info value
                        if #args >= 2 then
                            local value = reaper.GetMediaItemTakeInfo_Value(args[1], args[2])
                            response.ok = true
                            response.ret = value
                        else
                            response.error = "GetMediaItemTakeInfo_Value requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "DeleteExtState" then
                        -- Delete extended state
                        if #args >= 3 then
                            reaper.DeleteExtState(args[1], args[2], args[3])
                            response.ok = true
                            response.ret = true
                        else
                            response.error = "DeleteExtState requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetResourcePath" then
                        -- Get REAPER resource path
                        local path = reaper.GetResourcePath()
                        response.ok = true
                        response.ret = path
                    
                    elseif fname == "ShowConsoleMsg" then
                        -- Show console message
                        if #args >= 1 then
                            reaper.ShowConsoleMsg(args[1])
                            response.ok = true
                            response.ret = true
                        else
                            response.error = "ShowConsoleMsg requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "ValidatePtr" then
                        -- Validate pointer
                        if #args >= 2 then
                            local ptr = reaper.ValidatePtr(args[1], args[2])
                            response.ok = true
                            response.ret = ptr
                        else
                            response.error = "ValidatePtr requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetCurrentProjectInLoadSave" then
                        -- Get current project
                        local proj = reaper.GetCurrentProjectInLoadSave()
                        response.ok = true
                        response.ret = proj
                    
                    elseif fname == "Main_openProject" then
                        -- Open project
                        if #args >= 1 then
                            reaper.Main_openProject(args[1])
                            response.ok = true
                            response.ret = true
                        else
                            response.error = "Main_openProject requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetProjectName" then
                        -- Get project name
                        if #args >= 2 then
                            local name = reaper.GetProjectName(args[1], args[2])
                            response.ok = true
                            response.ret = name
                        else
                            response.error = "GetProjectName requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "IsProjectDirty" then
                        -- Check if project is dirty
                        if #args >= 1 then
                            local dirty = reaper.IsProjectDirty(args[1])
                            response.ok = true
                            response.ret = dirty
                        else
                            response.error = "IsProjectDirty requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetProjectNotes" then
                        -- Get project notes
                        if #args >= 1 then
                            local notes = reaper.GetProjectNotes(args[1])
                            response.ok = true
                            response.ret = notes
                        else
                            response.error = "GetProjectNotes requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "SetProjectNotes" then
                        -- Set project notes
                        if #args >= 2 then
                            reaper.SetProjectNotes(args[1], args[2])
                            response.ok = true
                            response.ret = true
                        else
                            response.error = "SetProjectNotes requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "MIDI_SetNote" then
                        -- Set MIDI note properties
                        if #args >= 9 then
                            local retval = reaper.MIDI_SetNote(args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9])
                            response.ok = retval
                            response.ret = retval
                        else
                            response.error = "MIDI_SetNote requires 9 arguments"
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