-- Script to reload the MCP bridge in REAPER
-- This can be run from REAPER's action list to reload the bridge

-- First, show a message
reaper.ShowConsoleMsg("Reloading MCP Bridge...\n")

-- Path to the bridge script
local bridge_path = reaper.GetResourcePath() .. "/Scripts/mcp_bridge_file_v2.lua"

-- Check if file exists
local file = io.open(bridge_path, "r")
if not file then
    reaper.ShowConsoleMsg("Error: Bridge file not found at " .. bridge_path .. "\n")
    return
end
file:close()

-- Load and run the bridge
local ok, err = pcall(dofile, bridge_path)
if ok then
    reaper.ShowConsoleMsg("MCP Bridge reloaded successfully!\n")
    reaper.ShowConsoleMsg("The bridge should now include DSL functions.\n")
else
    reaper.ShowConsoleMsg("Error loading bridge: " .. tostring(err) .. "\n")
end