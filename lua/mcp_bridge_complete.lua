-- REAPER MCP Bridge - Complete ReaScript API
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
        return string.format('"%s"', v:gsub('"', '\"'))
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
    local ok, result = pcall(load("return " .. str:gsub('([%w_]+):', '["%1"]='):gsub('"([^"]+)"', "'%1'")))
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
reaper.ShowConsoleMsg("REAPER MCP Bridge (Full API) started on port 9000
")

function main()
    local data = udp:receive()
    if data then
        reaper.ShowConsoleMsg("Received: " .. data .. "
")
        
        -- Parse the request
        local request = decode_json(data)
        if request and request.call then
            local fname = request.call
            local args = request.args or {}
            
            -- Call the REAPER function
            local response = {ok = false}
            
            -- Generic handler for most ReaScript functions
            local fn = reaper[fname]
            if fn then
                -- Try to call the function
                local ok, ret = pcall(fn, table.unpack(args))
                if ok then
                    response.ok = true
                    response.ret = ret
                else
                    response.error = "Error calling " .. fname .. ": " .. tostring(ret)
                end
            else
                response.error = "Unknown function: " .. fname
            end
            
            -- Send response
            local response_json = encode_json(response)
            reaper.ShowConsoleMsg("Sending: " .. response_json .. "
")
            udp:sendto(response_json, "127.0.0.1", 9001)  -- Send back to different port
        end
    end
    
    reaper.defer(main)
end

main()
