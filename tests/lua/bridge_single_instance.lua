-- Two runs of the bridge in separate environments sharing one ExtState, like two ReaScript
-- instances in one REAPER process.
local ext, clock, log = {}, 100.0, {}
local function make_reaper()
  local r = {
    GetExtState = function(s, k) return ext[s .. "/" .. k] or "" end,
    SetExtState = function(s, k, v) ext[s .. "/" .. k] = v end,
    time_precise = function() return clock end,
    ShowConsoleMsg = function(m) log[#log + 1] = m end,
    GetResourcePath = function() return "/tmp/fake-reaper" end,
    defer = function() end,            -- one iteration is enough
    RecursiveCreateDirectory = function() return 1 end,
    EnumerateFiles = function() return nil end,
  }
  return setmetatable(r, { __index = function() return function() end end })
end
local function run()
  local env = setmetatable({ reaper = make_reaper() }, { __index = _G })
  local chunk = assert(loadfile("lua/mcp_bridge.lua", "t", env))
  chunk()
end
run()                                  -- first start: must start and beat
local started1 = #log
clock = clock + 0.5; run()             -- second start 0.5 s later: must refuse
local refused = log[#log]:find("already running") ~= nil
clock = clock + 10; run()              -- after 10 s without beats (bridge died): must start again
local restarted = log[#log]:find("already running") == nil
print("first started:", started1 > 0 and not log[1]:find("already"))
print("duplicate refused:", refused)
print("restart after silence:", restarted)
