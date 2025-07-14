-- REAPER MCP Bridge (No Socket Version)
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

-- Simple JSON decoding (minimal implementation)
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
        -- Array
        local arr = {}
        local content = str:sub(2, -2)
        if content ~= "" then
            -- Simple split by comma (doesn't handle nested structures well)
            local i = 1
            for value in content:gmatch("[^,]+") do
                arr[i] = decode_json(value)
                i = i + 1
            end
        end
        return arr
    elseif str:match("^{.*}$") then
        -- Object
        local obj = {}
        local content = str:sub(2, -2)
        -- Simple pattern matching (doesn't handle nested structures well)
        for key, value in content:gmatch('"([^"]+)"%s*:%s*([^,}]+)') do
            obj[key] = decode_json(value:match("^%s*(.-)%s*$"))
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
                    
                    -- Check if function exists
                    if reaper[fname] then
                        -- Handle specific functions that need special treatment
                        if fname == "GetTrackName" then
                            if args[1] then
                                local retval, name = reaper.GetTrackName(args[1])
                                response.ok = true
                                response.ret = {retval, name}
                            else
                                response.error = "GetTrackName requires a track argument"
                            end
                            
                        elseif fname == "GetSetMediaTrackInfo_String" then
                            if args[1] and args[2] and args[3] ~= nil then
                                local retval, str = reaper.GetSetMediaTrackInfo_String(args[1], args[2], args[3], args[4] or false)
                                response.ok = true
                                response.ret = {retval, str}
                            else
                                response.error = "GetSetMediaTrackInfo_String requires at least 3 arguments"
                            end
                            
                        elseif fname == "GetProjectPath" then
                            local path, _ = reaper.GetProjectPath("")
                            response.ok = true
                            response.ret = path
                            
                        elseif fname == "GetProjectName" then
                            if args[1] then
                                local retval, name = reaper.GetProjectName(args[1])
                                response.ok = true
                                response.ret = {retval, name}
                            else
                                response.error = "GetProjectName requires a project argument"
                            end
                            
                        elseif fname == "MIDI_GetEvt" then
                            if args[1] and args[2] ~= nil then
                                local retval, selected, muted, ppqpos, msg = reaper.MIDI_GetEvt(args[1], args[2], args[3] or false, args[4] or false, args[5] or 0, args[6] or "")
                                response.ok = true
                                response.ret = {retval, selected, muted, ppqpos, msg}
                            else
                                response.error = "MIDI_GetEvt requires at least 2 arguments"
                            end
                            
                        elseif fname == "TakeFX_GetFXName" then
                            if args[1] and args[2] ~= nil then
                                local retval, name = reaper.TakeFX_GetFXName(args[1], args[2])
                                response.ok = true
                                response.ret = {retval, name}
                            else
                                response.error = "TakeFX_GetFXName requires at least 2 arguments"
                            end
                            
                        elseif fname == "TakeFX_GetPreset" then
                            if args[1] and args[2] ~= nil then
                                local retval, preset = reaper.TakeFX_GetPreset(args[1], args[2])
                                response.ok = true
                                response.ret = {retval, preset}
                            else
                                response.error = "TakeFX_GetPreset requires at least 2 arguments"
                            end
                            
                        elseif fname == "TakeFX_GetParamName" then
                            if args[1] and args[2] ~= nil and args[3] ~= nil then
                                local retval, name = reaper.TakeFX_GetParamName(args[1], args[2], args[3])
                                response.ok = true
                                response.ret = {retval, name}
                            else
                                response.error = "TakeFX_GetParamName requires at least 3 arguments"
                            end
                            
                        elseif fname == "TakeFX_GetParam" then
                            if args[1] and args[2] ~= nil and args[3] ~= nil then
                                local value, minval, maxval = reaper.TakeFX_GetParam(args[1], args[2], args[3])
                                response.ok = true
                                response.ret = {value, minval, maxval}
                            else
                                response.error = "TakeFX_GetParam requires at least 3 arguments"
                            end
                            
                        elseif fname == "TrackFX_GetParamName" then
                            if args[1] and args[2] ~= nil and args[3] ~= nil then
                                local retval, name = reaper.TrackFX_GetParamName(args[1], args[2], args[3])
                                response.ok = true
                                response.ret = {retval, name}
                            else
                                response.error = "TrackFX_GetParamName requires at least 3 arguments"
                            end
                            
                        elseif fname == "TrackFX_GetPreset" then
                            if args[1] and args[2] ~= nil then
                                local retval, preset = reaper.TrackFX_GetPreset(args[1], args[2])
                                response.ok = true
                                response.ret = {retval, preset}
                            else
                                response.error = "TrackFX_GetPreset requires at least 2 arguments"
                            end
                            
                        elseif fname == "TrackFX_GetPresetIndex" then
                            if args[1] and args[2] ~= nil then
                                local preset_index, num_presets = reaper.TrackFX_GetPresetIndex(args[1], args[2])
                                response.ok = true
                                response.ret = {preset_index, num_presets}
                            else
                                response.error = "TrackFX_GetPresetIndex requires at least 2 arguments"
                            end
                            
                        elseif fname == "TrackFX_GetIOSize" then
                            if args[1] and args[2] ~= nil then
                                local input_pins, output_pins = reaper.TrackFX_GetIOSize(args[1], args[2])
                                response.ok = true
                                response.ret = {input_pins, output_pins}
                            else
                                response.error = "TrackFX_GetIOSize requires at least 2 arguments"
                            end
                            
                        elseif fname == "TrackFX_FormatParamValue" then
                            if args[1] and args[2] ~= nil and args[3] ~= nil and args[4] ~= nil then
                                local retval, formatted = reaper.TrackFX_FormatParamValue(args[1], args[2], args[3], args[4], args[5] or "")
                                response.ok = true
                                response.ret = {retval, formatted}
                            else
                                response.error = "TrackFX_FormatParamValue requires at least 4 arguments"
                            end
                            
                        elseif fname == "TrackFX_FormatParamValueNormalized" then
                            if args[1] and args[2] ~= nil and args[3] ~= nil and args[4] ~= nil then
                                local retval, formatted = reaper.TrackFX_FormatParamValueNormalized(args[1], args[2], args[3], args[4], args[5] or "")
                                response.ok = true
                                response.ret = {retval, formatted}
                            else
                                response.error = "TrackFX_FormatParamValueNormalized requires at least 4 arguments"
                            end
                            
                        elseif fname == "GetProjExtState" then
                            if args[1] ~= nil and args[2] and args[3] then
                                local retval, value = reaper.GetProjExtState(args[1], args[2], args[3])
                                response.ok = true
                                response.ret = {retval, value}
                            else
                                response.error = "GetProjExtState requires at least 3 arguments"
                            end
                            
                        elseif fname == "EnumProjExtState" then
                            if args[1] ~= nil and args[2] and args[3] ~= nil then
                                local retval, key, value = reaper.EnumProjExtState(args[1], args[2], args[3])
                                response.ok = true
                                response.ret = {retval, key, value}
                            else
                                response.error = "EnumProjExtState requires at least 3 arguments"
                            end
                            
                        elseif fname == "GetTrackStateChunk" then
                            if args[1] then
                                local retval, chunk = reaper.GetTrackStateChunk(args[1], args[2] or "", args[3] or 65536, args[4] or false)
                                response.ok = true
                                response.ret = {retval, chunk}
                            else
                                response.error = "GetTrackStateChunk requires at least 1 argument"
                            end
                            
                        elseif fname == "GetItemStateChunk" then
                            if args[1] then
                                local retval, chunk = reaper.GetItemStateChunk(args[1], args[2] or "", args[3] or 65536, args[4] or false)
                                response.ok = true
                                response.ret = {retval, chunk}
                            else
                                response.error = "GetItemStateChunk requires at least 1 argument"
                            end
                            
                        elseif fname == "GetEnvelopeStateChunk" then
                            if args[1] then
                                local retval, chunk = reaper.GetEnvelopeStateChunk(args[1], args[2] or "", args[3] or 65536, args[4] or false)
                                response.ok = true
                                response.ret = {retval, chunk}
                            else
                                response.error = "GetEnvelopeStateChunk requires at least 1 argument"
                            end
                            
                        elseif fname == "GetTakeStretchMarker" then
                            if args[1] and args[2] ~= nil then
                                local idx, pos, srcpos = reaper.GetTakeStretchMarker(args[1], args[2])
                                response.ok = true
                                response.ret = {idx, pos, srcpos}
                            else
                                response.error = "GetTakeStretchMarker requires at least 2 arguments"
                            end
                            
                        elseif fname == "GetTakeMarker" then
                            if args[1] and args[2] ~= nil then
                                local position, name, color = reaper.GetTakeMarker(args[1], args[2])
                                response.ok = true
                                response.ret = {position, name, color}
                            else
                                response.error = "GetTakeMarker requires at least 2 arguments"
                            end
                            
                        elseif fname == "GetMediaSourceFileName" then
                            if args[1] then
                                local filename = reaper.GetMediaSourceFileName(args[1], args[2] or "")
                                response.ok = true
                                response.ret = filename
                            else
                                response.error = "GetMediaSourceFileName requires at least 1 argument"
                            end
                            
                        elseif fname == "GetTrackSendName" then
                            if args[1] and args[2] ~= nil then
                                local retval, name = reaper.GetTrackSendName(args[1], args[2], args[3] or "")
                                response.ok = true
                                response.ret = {retval, name}
                            else
                                response.error = "GetTrackSendName requires at least 2 arguments"
                            end
                            
                        elseif fname == "GetTrackReceiveName" then
                            if args[1] and args[2] ~= nil then
                                local retval, name = reaper.GetTrackReceiveName(args[1], args[2], args[3] or "")
                                response.ok = true
                                response.ret = {retval, name}
                            else
                                response.error = "GetTrackReceiveName requires at least 2 arguments"
                            end
                            
                        elseif fname == "GetTrackSendUIVolPan" then
                            if args[1] and args[2] ~= nil then
                                local volume, pan = reaper.GetTrackSendUIVolPan(args[1], args[2])
                                response.ok = true
                                response.ret = {volume, pan}
                            else
                                response.error = "GetTrackSendUIVolPan requires at least 2 arguments"
                            end
                            
                        elseif fname == "GetTrackReceiveUIVolPan" then
                            if args[1] and args[2] ~= nil then
                                local volume, pan = reaper.GetTrackReceiveUIVolPan(args[1], args[2])
                                response.ok = true
                                response.ret = {volume, pan}
                            else
                                response.error = "GetTrackReceiveUIVolPan requires at least 2 arguments"
                            end
                            
                        elseif fname == "GetTrackReceiveUIMute" then
                            if args[1] and args[2] ~= nil then
                                local retval, muted = reaper.GetTrackReceiveUIMute(args[1], args[2])
                                response.ok = true
                                response.ret = {retval, muted}
                            else
                                response.error = "GetTrackReceiveUIMute requires at least 2 arguments"
                            end
                            
                        elseif fname == "GetTrackUIVolPan" then
                            if args[1] then
                                local volume, pan = reaper.GetTrackUIVolPan(args[1])
                                response.ok = true
                                response.ret = {volume, pan}
                            else
                                response.error = "GetTrackUIVolPan requires at least 1 argument"
                            end
                            
                        elseif fname == "CalcMediaSrcLoudness" then
                            if args[1] then
                                local retval, lufs_integrated, lufs_range, truepeak = reaper.CalcMediaSrcLoudness(args[1])
                                response.ok = true
                                response.ret = {retval, lufs_integrated, lufs_range, truepeak}
                            else
                                response.error = "CalcMediaSrcLoudness requires at least 1 argument"
                            end
                            
                        elseif fname == "CalculateNormalization" then
                            if args[1] and args[2] ~= nil and args[3] ~= nil then
                                local retval, gain_mul, offset = reaper.CalculateNormalization(args[1], args[2], args[3], args[4] or 0.0, args[5] or 0.0, args[6] or true)
                                response.ok = true
                                response.ret = {retval, gain_mul, offset}
                            else
                                response.error = "CalculateNormalization requires at least 3 arguments"
                            end
                            
                        elseif fname == "GetPeakFileName" then
                            if args[1] then
                                local peakfilename = reaper.GetPeakFileName(args[1], args[2] or "", args[3] or 4096)
                                response.ok = true
                                response.ret = peakfilename
                            else
                                response.error = "GetPeakFileName requires at least 1 argument"
                            end
                            
                        else
                            -- Generic function call
                            local ok, result = pcall(reaper[fname], table.unpack(args))
                            if ok then
                                response.ok = true
                                response.ret = result
                            else
                                response.error = "Error calling " .. fname .. ": " .. tostring(result)
                            end
                        end
                    else
                        response.error = "Unknown function: " .. fname
                    end
                    
                    -- Write response
                    local response_json = encode_json(response)
                    reaper.ShowConsoleMsg("Sending response " .. i .. ": " .. response_json .. "\n")
                    write_file(numbered_response_file, response_json)
                end
                
                -- Clean up request file
                delete_file(numbered_request_file)
            end
        end
    end
end

-- Main loop
ensure_dir()
reaper.ShowConsoleMsg("REAPER MCP Bridge (File-based) started\n")
reaper.ShowConsoleMsg("Bridge directory: " .. bridge_dir .. "\n")

function main()
    process_request()
    reaper.defer(main)
end

main()