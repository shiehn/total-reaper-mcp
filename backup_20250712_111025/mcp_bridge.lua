-- REAPER MCP Bridge
-- This script runs inside REAPER and communicates with the MCP server

local socket = require('socket')
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