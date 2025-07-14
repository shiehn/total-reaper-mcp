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