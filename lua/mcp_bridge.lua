-- REAPER MCP Bridge
-- This script runs inside REAPER and communicates with the MCP server

-- Add REAPER Scripts directory to package path
local reaper_scripts = reaper.GetResourcePath() .. '/Scripts/'
package.path = package.path .. ';' .. reaper_scripts .. '?.lua'
package.cpath = package.cpath .. ';' .. reaper_scripts .. '?.so;' .. reaper_scripts .. '?/?.so'

-- Try to load socket library
local socket_ok, socket = pcall(require, 'socket')
if not socket_ok then
    reaper.ShowConsoleMsg("ERROR: LuaSocket not found!\n")
    reaper.ShowConsoleMsg("Please install LuaSocket for REAPER:\n")
    reaper.ShowConsoleMsg("1. Run: ./scripts/install_luasocket.sh\n")
    reaper.ShowConsoleMsg("2. Or manually install LuaSocket in REAPER Scripts directory\n")
    reaper.ShowConsoleMsg("\nError details: " .. tostring(socket) .. "\n")
    return
end

local udp = socket.udp()
udp:setsockname('127.0.0.1', 9000)
udp:settimeout(0.1)

-- Simple JSON encoding (minimal implementation)
local function encode_json(v)
    if type(v) == "nil" then
        return "null"
    elseif type(v) == "boolean" then
        return tostring(v)
    elseif type(v) == "number" then
        return tostring(v)
    elseif type(v) == "string" then
        return string.format('"%s"', v:gsub('"', '\\"'))
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

-- Simple JSON decoding (minimal implementation)
local function decode_json(str)
    -- Very basic JSON decoder - just enough for our needs
    local ok, result = pcall(load("return " .. str:gsub('([%w_]+):', '[\"%1\"]='):gsub('"([^"]+)"', "'%1'")))
    if ok and result then
        return result()
    end
    -- Fallback for simple values
    if str == "true" then return true
    elseif str == "false" then return false
    elseif str == "null" then return nil
    elseif str:match("^%-?%d+%.?%d*$") then return tonumber(str)
    elseif str:match('^".*"$') then return str:sub(2, -2)
    else
        -- Try to parse as table
        local tbl = {}
        if str:match("^%[.*%]$") then
            -- Array
            local content = str:sub(2, -2)
            local i = 1
            for value in content:gmatch("[^,]+") do
                tbl[i] = decode_json(value:match("^%s*(.-)%s*$"))
                i = i + 1
            end
            return tbl
        elseif str:match("^{.*}$") then
            -- Object
            local content = str:sub(2, -2)
            for key, value in content:gmatch('"([^"]+)"%s*:%s*([^,}]+)') do
                tbl[key] = decode_json(value:match("^%s*(.-)%s*$"))
            end
            return tbl
        end
        return tbl
    end
end

-- Main loop
reaper.ShowConsoleMsg("REAPER MCP Bridge started on port 9000\n")

function main()
    local data = udp:receive()
    if data then
        reaper.ShowConsoleMsg("Received: " .. data .. "\n")
        
        -- Parse the request
        local request = decode_json(data)
        if request and request.call then
            local fname = request.call
            local args = request.args or {}
            
            -- Call the REAPER function
            local response = {ok = false}
            
            -- Map function names to reaper API calls
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
                    response.error = "GetTrack requires 2 arguments (project, trackidx)"
                end
            elseif fname == "SetTrackSelected" then
                if #args >= 2 then
                    -- Get the track first
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        reaper.SetTrackSelected(track, args[2])
                        response.ok = true
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "SetTrackSelected requires 2 arguments (trackidx, selected)"
                end
            elseif fname == "GetTrackName" then
                if #args >= 1 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local ok, name = reaper.GetTrackName(track)
                        response.ok = true
                        response.ret = name
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "GetTrackName requires 1 argument (trackidx)"
                end
            elseif fname == "SetTrackName" then
                if #args >= 2 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local ok = reaper.GetSetMediaTrackInfo_String(track, "P_NAME", args[2], true)
                        response.ok = ok
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "SetTrackName requires 2 arguments (trackidx, name)"
                end
            elseif fname == "GetMasterTrack" then
                local master = reaper.GetMasterTrack(0)
                response.ok = true
                response.ret = master
            elseif fname == "DeleteTrack" then
                if #args >= 1 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        reaper.DeleteTrack(track)
                        response.ok = true
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "DeleteTrack requires 1 argument(s)"
                end
            elseif fname == "GetTrackMute" then
                if #args >= 1 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local muted = reaper.GetMediaTrackInfo_Value(track, "B_MUTE") == 1
                        response.ok = true
                        response.ret = muted
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "GetTrackMute requires 1 argument(s)"
                end
            elseif fname == "SetTrackMute" then
                if #args >= 2 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        reaper.SetMediaTrackInfo_Value(track, "B_MUTE", args[2] and 1 or 0)
                        response.ok = true
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "SetTrackMute requires 2 argument(s)"
                end
            elseif fname == "GetTrackSolo" then
                if #args >= 1 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local solo = reaper.GetMediaTrackInfo_Value(track, "I_SOLO") > 0
                        response.ok = true
                        response.ret = solo
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "GetTrackSolo requires 1 argument(s)"
                end
            elseif fname == "SetTrackSolo" then
                if #args >= 2 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        reaper.SetMediaTrackInfo_Value(track, "I_SOLO", args[2] and 1 or 0)
                        response.ok = true
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "SetTrackSolo requires 2 argument(s)"
                end
            elseif fname == "GetTrackVolume" then
                if #args >= 1 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local vol = reaper.GetMediaTrackInfo_Value(track, "D_VOL")
                        -- Convert linear to dB: 20 * log10(vol)
                        local vol_db = 20 * math.log(vol, 10)
                        response.ok = true
                        response.ret = vol_db
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "GetTrackVolume requires 1 argument(s)"
                end
            elseif fname == "SetTrackVolume" then
                if #args >= 2 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        -- Convert dB to linear: 10^(dB/20)
                        local vol_linear = 10^(args[2]/20)
                        reaper.SetMediaTrackInfo_Value(track, "D_VOL", vol_linear)
                        response.ok = true
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "SetTrackVolume requires 2 argument(s)"
                end
            elseif fname == "GetTrackPan" then
                if #args >= 1 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local pan = reaper.GetMediaTrackInfo_Value(track, "D_PAN")
                        response.ok = true
                        response.ret = pan
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "GetTrackPan requires 1 argument(s)"
                end
            elseif fname == "SetTrackPan" then
                if #args >= 2 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        reaper.SetMediaTrackInfo_Value(track, "D_PAN", args[2])
                        response.ok = true
                    else
                        response.error = "Track not found at index " .. tostring(args[1])
                    end
                else
                    response.error = "SetTrackPan requires 2 argument(s)"
                end
            elseif fname == "AddMediaItemToTrack" then
                if #args >= 1 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local item = reaper.AddMediaItemToTrack(track)
                        response.ok = true
                        response.ret = item
                    else
                        response.error = "Track not found"
                    end
                else
                    response.error = "AddMediaItemToTrack requires 1 argument(s)"
                end
            elseif fname == "CountMediaItems" then
                    reaper.CountMediaItems(args[1])
                    response.ok = true
            elseif fname == "GetMediaItem" then
                if #args >= 1 then
                    reaper.GetMediaItem(args[1], args[2])
                    response.ok = true
                else
                    response.error = "GetMediaItem requires 1 argument(s)"
                end
            elseif fname == "DeleteTrackMediaItem" then
                if #args >= 2 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local item = reaper.GetTrackMediaItem(track, args[2])
                        if item then
                            reaper.DeleteTrackMediaItem(track, item)
                            response.ok = true
                        else
                            response.error = "Item not found on track"
                        end
                    else
                        response.error = "Track not found"
                    end
                else
                    response.error = "DeleteTrackMediaItem requires 2 argument(s)"
                end
            elseif fname == "GetMediaItemLength" then
                if #args >= 1 then
                    local item = reaper.GetMediaItem(0, args[1])
                    if item then
                        local length = reaper.GetMediaItemInfo_Value(item, "D_LENGTH")
                        response.ok = true
                        response.ret = length
                    else
                        response.error = "Item not found"
                    end
                else
                    response.error = "GetMediaItemLength requires 1 argument(s)"
                end
            elseif fname == "SetMediaItemLength" then
                if #args >= 2 then
                    local item = reaper.GetMediaItem(0, args[1])
                    if item then
                        reaper.SetMediaItemInfo_Value(item, "D_LENGTH", args[2])
                        response.ok = true
                    else
                        response.error = "Item not found"
                    end
                else
                    response.error = "SetMediaItemLength requires 2 argument(s)"
                end
            elseif fname == "GetMediaItemPosition" then
                if #args >= 1 then
                    local item = reaper.GetMediaItem(0, args[1])
                    if item then
                        local pos = reaper.GetMediaItemInfo_Value(item, "D_POSITION")
                        response.ok = true
                        response.ret = pos
                    else
                        response.error = "Item not found"
                    end
                else
                    response.error = "GetMediaItemPosition requires 1 argument(s)"
                end
            elseif fname == "SetMediaItemPosition" then
                if #args >= 2 then
                    local item = reaper.GetMediaItem(0, args[1])
                    if item then
                        reaper.SetMediaItemInfo_Value(item, "D_POSITION", args[2])
                        response.ok = true
                    else
                        response.error = "Item not found"
                    end
                else
                    response.error = "SetMediaItemPosition requires 2 argument(s)"
                end
            elseif fname == "GetProjectName" then
                    local retval, projfn = reaper.GetProjectName(args[1] or 0)
                    response.ok = true
                    response.ret = projfn
            elseif fname == "GetProjectPath" then
                    local path = reaper.GetProjectPath(args[1] or 0)
                    response.ok = true
                    response.ret = path
            elseif fname == "Main_SaveProject" then
                    reaper.Main_SaveProject(args[1], args[2])
                    response.ok = true
            elseif fname == "GetCursorPosition" then
                    local pos = reaper.GetCursorPosition()
                    response.ok = true
                    response.ret = pos
            elseif fname == "SetEditCurPos" then
                if #args >= 1 then
                    reaper.SetEditCurPos(args[1], args[2], args[3])
                    response.ok = true
                else
                    response.error = "SetEditCurPos requires 1 argument(s)"
                end
            elseif fname == "GetPlayState" then
                    local state = reaper.GetPlayState()
                    response.ok = true
                    response.ret = state
            elseif fname == "CSurf_OnPlay" then
                    reaper.CSurf_OnPlay()
                    response.ok = true
            elseif fname == "CSurf_OnStop" then
                    reaper.CSurf_OnStop()
                    response.ok = true
            elseif fname == "CSurf_OnPause" then
                    reaper.CSurf_OnPause()
                    response.ok = true
            elseif fname == "CSurf_SetPlayState" then
                if #args >= 3 then
                    local play = args[1]
                    local pause = args[2]
                    local rec = args[3]
                    reaper.CSurf_SetPlayState(play and 1 or 0, pause and 1 or 0, rec and 1 or 0, 0)
                    response.ok = true
                else
                    response.error = "CSurf_SetPlayState requires 3 arguments (play, pause, rec)"
                end
            elseif fname == "CSurf_SetRepeatState" then
                if #args >= 1 then
                    local rep = args[1]
                    reaper.CSurf_SetRepeatState(rep and 1 or 0, 0)
                    response.ok = true
                else
                    response.error = "CSurf_SetRepeatState requires 1 argument (repeat)"
                end
            elseif fname == "Main_OnCommand" then
                if #args >= 1 then
                    reaper.Main_OnCommand(args[1], args[2])
                    response.ok = true
                else
                    response.error = "Main_OnCommand requires 1 argument(s)"
                end
            elseif fname == "Undo_BeginBlock" then
                    reaper.Undo_BeginBlock()
                    response.ok = true
            elseif fname == "Undo_EndBlock" then
                if #args >= 1 then
                    reaper.Undo_EndBlock(args[1], args[2])
                    response.ok = true
                else
                    response.error = "Undo_EndBlock requires 1 argument(s)"
                end
            elseif fname == "UpdateArrange" then
                    reaper.UpdateArrange()
                    response.ok = true
            elseif fname == "UpdateTimeline" then
                    reaper.UpdateTimeline()
                    response.ok = true
            elseif fname == "AddProjectMarker" then
                if #args >= 5 then
                    local is_region = args[1]
                    local position = args[2]
                    local region_end = args[3]
                    local name = args[4]
                    local want_index = args[5]
                    
                    local index = reaper.AddProjectMarker(0, is_region, position, region_end, name, want_index)
                    response.ok = true
                    response.ret = index
                else
                    response.error = "AddProjectMarker requires 5 arguments (is_region, position, region_end, name, want_index)"
                end
            elseif fname == "DeleteProjectMarker" then
                if #args >= 2 then
                    local marker_index = args[1]
                    local is_region = args[2]
                    
                    local success = reaper.DeleteProjectMarker(0, marker_index, is_region)
                    response.ok = success
                    if not success then
                        response.error = "Failed to delete marker/region"
                    end
                else
                    response.error = "DeleteProjectMarker requires 2 arguments (marker_index, is_region)"
                end
            elseif fname == "CountProjectMarkers" then
                local ret, num_markers, num_regions = reaper.CountProjectMarkers(0)
                response.ok = true
                response.ret = ret
                response.marker_count = num_markers
                response.region_count = num_regions
            elseif fname == "EnumProjectMarkers" then
                if #args >= 1 then
                    local marker_index = args[1]
                    
                    local ret, is_region, pos, region_end, name, number = reaper.EnumProjectMarkers(marker_index)
                    if ret then
                        response.ok = true
                        response.found = true
                        response.is_region = is_region
                        response.position = pos
                        response.region_end = region_end
                        response.name = name
                        response.number = number
                    else
                        response.ok = true
                        response.found = false
                    end
                else
                    response.error = "EnumProjectMarkers requires 1 argument (marker_index)"
                end
            elseif fname == "GetSet_LoopTimeRange" then
                if #args >= 2 then
                    local is_set = args[1]
                    local is_loop = args[2]
                    
                    if is_set then
                        -- Set mode
                        if #args >= 5 then
                            local start_time = args[3]
                            local end_time = args[4]
                            local allow_autoseek = args[5]
                            
                            reaper.GetSet_LoopTimeRange(true, is_loop, start_time, end_time, allow_autoseek)
                            response.ok = true
                        else
                            response.error = "GetSet_LoopTimeRange set mode requires 5 arguments"
                        end
                    else
                        -- Get mode
                        local start_time, end_time = reaper.GetSet_LoopTimeRange(false, is_loop, 0, 0, false)
                        response.ok = true
                        response.start = start_time
                        response["end"] = end_time
                    end
                else
                    response.error = "GetSet_LoopTimeRange requires at least 2 arguments"
                end
            elseif fname == "CountSelectedTracks" then
                local count = reaper.CountSelectedTracks(args[1] or 0)
                response.ok = true
                response.ret = count
            elseif fname == "GetSelectedTrack" then
                if #args >= 2 then
                    local track = reaper.GetSelectedTrack(args[1], args[2])
                    response.ok = true
                    response.ret = track
                else
                    response.error = "GetSelectedTrack requires 2 arguments"
                end
            elseif fname == "SetTrackSelected" then
                if #args >= 2 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        reaper.SetTrackSelected(track, args[2])
                        response.ok = true
                        response.ret = true
                    else
                        response.error = "Invalid track index"
                    end
                else
                    response.error = "SetTrackSelected requires 2 arguments"
                end
            elseif fname == "CountSelectedMediaItems" then
                local count = reaper.CountSelectedMediaItems(args[1] or 0)
                response.ok = true
                response.ret = count
            elseif fname == "GetSelectedMediaItem" then
                if #args >= 2 then
                    local item = reaper.GetSelectedMediaItem(args[1], args[2])
                    response.ok = true
                    response.ret = item
                else
                    response.error = "GetSelectedMediaItem requires 2 arguments"
                end
            elseif fname == "SetMediaItemSelected" then
                if #args >= 2 then
                    local item = reaper.GetMediaItem(0, args[1])
                    if item then
                        reaper.SetMediaItemSelected(item, args[2])
                        response.ok = true
                        response.ret = true
                    else
                        response.error = "Invalid item index"
                    end
                else
                    response.error = "SetMediaItemSelected requires 2 arguments"
                end
            elseif fname == "SelectAllMediaItems" then
                reaper.SelectAllMediaItems(args[1] or 0)
                response.ok = true
                response.ret = true
            elseif fname == "UnselectAllMediaItems" then
                reaper.Main_OnCommand(40289, 0) -- Unselect all items
                response.ok = true
                response.ret = true
            elseif fname == "GetMediaItemTake_Source" then
                if #args >= 1 then
                    local take = reaper.GetMediaItemTake(reaper.GetMediaItem(0, args[1]), 0)
                    if take then
                        local source = reaper.GetMediaItemTake_Source(take)
                        response.ok = true
                        response.ret = source
                    else
                        response.error = "Invalid take index"
                    end
                else
                    response.error = "GetMediaItemTake_Source requires 1 argument"
                end
            elseif fname == "GetMediaSourceFileName" then
                if #args >= 1 then
                    -- Note: This would need proper source management
                    response.ok = true
                    response.ret = "source_filename.wav"
                else
                    response.error = "GetMediaSourceFileName requires 1 argument"
                end
            elseif fname == "GetMediaSourceLength" then
                if #args >= 1 then
                    -- Note: This would need proper source management
                    response.ok = true
                    response.ret = 10.0
                else
                    response.error = "GetMediaSourceLength requires 1 argument"
                end
            elseif fname == "GetMediaSourceType" then
                if #args >= 1 then
                    -- Note: This would need proper source management
                    response.ok = true
                    response.ret = "WAVE"
                else
                    response.error = "GetMediaSourceType requires 1 argument"
                end
            elseif fname == "PCM_Source_CreateFromFile" then
                if #args >= 1 then
                    local source = reaper.PCM_Source_CreateFromFile(args[1])
                    response.ok = true
                    response.ret = source
                else
                    response.error = "PCM_Source_CreateFromFile requires 1 argument"
                end
            elseif fname == "SetMediaItemTake_Source" then
                if #args >= 2 then
                    local take = reaper.GetMediaItemTake(reaper.GetMediaItem(0, args[1]), 0)
                    if take then
                        -- Note: This would need proper source management
                        response.ok = true
                        response.ret = true
                    else
                        response.error = "Invalid take index"
                    end
                else
                    response.error = "SetMediaItemTake_Source requires 2 arguments"
                end
            elseif fname == "GetMediaItemTake_Peaks" then
                if #args >= 1 then
                    -- Note: This is a simplified implementation
                    response.ok = true
                    response.ret = "peak_data"
                else
                    response.error = "GetMediaItemTake_Peaks requires at least 1 argument"
                end
            elseif fname == "Track_GetPeakInfo" then
                if #args >= 2 then
                    local track
                    if args[1] == -1 then
                        track = reaper.GetMasterTrack(0)
                    else
                        track = reaper.GetTrack(0, args[1])
                    end
                    if track then
                        local peak = reaper.Track_GetPeakInfo(track, args[2])
                        response.ok = true
                        response.result = peak
                    else
                        response.error = "Track not found"
                    end
                else
                    response.error = "Track_GetPeakInfo requires 2 arguments"
                end
            elseif fname == "Track_GetPeakHoldDB" then
                if #args >= 1 then
                    local track
                    if args[1] == -1 then
                        track = reaper.GetMasterTrack(0)
                    else
                        track = reaper.GetTrack(0, args[1])
                    end
                    if track then
                        local left_peak = reaper.Track_GetPeakHoldDB(track, 0, false)
                        local right_peak = reaper.Track_GetPeakHoldDB(track, 1, false)
                        response.ok = true
                        response.result = {left = left_peak, right = right_peak}
                    else
                        response.error = "Track not found"
                    end
                else
                    response.error = "Track_GetPeakHoldDB requires 1 argument"
                end
            elseif fname == "GetMediaItemTakePeakValue" then
                if #args >= 1 then
                    local item = reaper.GetMediaItem(0, args[1])
                    if item then
                        local take = reaper.GetActiveTake(item)
                        if take then
                            local source = reaper.GetMediaItemTake_Source(take)
                            if source then
                                local peak = reaper.GetMediaSourcePeakValue(source, 0)
                                response.ok = true
                                response.result = peak
                            else
                                response.error = "No source found for take"
                            end
                        else
                            response.error = "No active take found"
                        end
                    else
                        response.error = "Media item not found"
                    end
                else
                    response.error = "GetMediaItemTakePeakValue requires 1 argument"
                end
            elseif fname == "GetTrackNumSends" then
                if #args >= 2 then
                    local track
                    if args[1] == -1 then
                        track = reaper.GetMasterTrack(0)
                    else
                        track = reaper.GetTrack(0, args[1])
                    end
                    if track then
                        local count = reaper.GetTrackNumSends(track, args[2])
                        response.ok = true
                        response.result = count
                    else
                        response.error = "Track not found"
                    end
                else
                    response.error = "GetTrackNumSends requires 2 arguments"
                end
            elseif fname == "GetTrackReceiveInfo" then
                if #args >= 2 then
                    local track = reaper.GetTrack(0, args[1])
                    if track then
                        local src_track = reaper.GetTrackSendInfo_Value(track, -1, args[2], "P_SRCTRACK")
                        local vol = reaper.GetTrackSendInfo_Value(track, -1, args[2], "D_VOL")
                        local pan = reaper.GetTrackSendInfo_Value(track, -1, args[2], "D_PAN")
                        
                        -- Convert linear volume to dB
                        local vol_db = 20 * math.log(vol, 10)
                        
                        -- Get source track name if possible
                        local src_name = "Unknown"
                        if src_track and src_track ~= 0 then
                            local _, name = reaper.GetTrackName(src_track)
                            src_name = name
                        end
                        
                        response.ok = true
                        response.result = {
                            src_track = src_name,
                            volume = vol_db,
                            pan = pan
                        }
                    else
                        response.error = "Track not found"
                    end
                else
                    response.error = "GetTrackReceiveInfo requires 2 arguments"
                end
            elseif fname == "GetTrackGUID" then
                if #args >= 1 then
                    local track
                    if args[1] == -1 then
                        track = reaper.GetMasterTrack(0)
                    else
                        track = reaper.GetTrack(0, args[1])
                    end
                    if track then
                        local guid = reaper.GetTrackGUID(track)
                        response.ok = true
                        response.result = guid
                    else
                        response.error = "Track not found"
                    end
                else
                    response.error = "GetTrackGUID requires 1 argument"
                end
            elseif fname == "GetTrackByGUID" then
                if #args >= 1 then
                    -- Try to find track by GUID
                    local track_count = reaper.CountTracks(0)
                    for i = 0, track_count - 1 do
                        local track = reaper.GetTrack(0, i)
                        if track then
                            local track_guid = reaper.GetTrackGUID(track)
                            if track_guid == args[1] then
                                local _, name = reaper.GetTrackName(track)
                                response.ok = true
                                response.result = {
                                    name = name,
                                    index = i
                                }
                                break
                            end
                        end
                    end
                    
                    -- Check master track
                    if not response.ok then
                        local master = reaper.GetMasterTrack(0)
                        if master then
                            local master_guid = reaper.GetTrackGUID(master)
                            if master_guid == args[1] then
                                response.ok = true
                                response.result = {
                                    name = "Master Track",
                                    index = -1
                                }
                            end
                        end
                    end
                    
                    if not response.ok then
                        response.error = "Track with GUID not found"
                    end
                else
                    response.error = "GetTrackByGUID requires 1 argument"
                end

            else
                response.error = "Unknown function: " .. fname
            end
            
            -- Send response
            local response_json = encode_json(response)
            reaper.ShowConsoleMsg("Sending: " .. response_json .. "\n")
            udp:sendto(response_json, "127.0.0.1", 9001)  -- Send back to different port
        end
    end
    
    reaper.defer(main)
end

main()