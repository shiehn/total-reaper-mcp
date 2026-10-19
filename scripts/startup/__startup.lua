-- Auto-start the total-reaper-mcp bridge on every REAPER launch, so the
-- MCP tools work immediately after a restart with no manual "run the action"
-- step. Wrapped in pcall so a bridge error never blocks REAPER startup.
local ok, err = pcall(function()
    dofile(reaper.GetResourcePath() .. '/Scripts/mcp_bridge_file_v2.lua')
end)
if not ok then
    reaper.ShowConsoleMsg('MCP bridge auto-start failed: ' .. tostring(err) .. '\n')
end
