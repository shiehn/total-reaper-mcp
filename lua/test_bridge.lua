-- Test script to debug bridge issues
local bridge_dir = reaper.GetResourcePath() .. '/Scripts/mcp_bridge_data/'

-- Simple JSON encoding
local function encode_json(v)
    if type(v) == "nil" then
        return "null"
    elseif type(v) == "boolean" then
        return tostring(v)
    elseif type(v) == "number" then
        return tostring(v)
    elseif type(v) == "string" then
        return string.format('"%s"', v:gsub('"', '\\"'))
    elseif type(v) == "userdata" then
        return string.format('{"__ptr":"%s"}', tostring(v))
    else
        return "null"
    end
end

-- Test GetMasterTrack
reaper.ShowConsoleMsg("Testing GetMasterTrack...\n")
local master = reaper.GetMasterTrack(0)
reaper.ShowConsoleMsg("Master track: " .. tostring(master) .. "\n")
reaper.ShowConsoleMsg("Type: " .. type(master) .. "\n")

-- Write test response
local response = {
    ok = true,
    ret = master
}

local response_json = encode_json(response)
reaper.ShowConsoleMsg("JSON would be: " .. response_json .. "\n")

-- Actually encode the response properly
local response_str = '{"ok":true,"ret":' .. encode_json(master) .. '}'
reaper.ShowConsoleMsg("Proper JSON: " .. response_str .. "\n")

-- Test file operations
local test_file = bridge_dir .. "test.txt"
local file = io.open(test_file, "w")
if file then
    file:write("Test successful!")
    file:close()
    reaper.ShowConsoleMsg("File write successful\n")
else
    reaper.ShowConsoleMsg("File write failed!\n")
end