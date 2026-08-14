# Local hardening patches (2026-07-24)

Fixes for a sticky desync + modal-dialog hang hit while driving REAPER heavily
via the file bridge. The two code changes below are general and are proposed
upstream; the REAPER-config bits are local setup notes.

## Code (in this repo — proposed upstream)

**`lua/mcp_bridge.lua` — poll the requests that exist, not a fixed 1..1000 range**
- `process_request()` looped `for i = 1, 1000`, calling `file_exists()` on every
  id each defer tick. Two costs: a thousand stats per tick on an otherwise idle
  bridge, and — the one that actually bites — **any id outside that window was
  ignored in complete silence**. A client writing `request_7000.json` got no
  reply, no error and no console line; the files just accumulated. Nothing
  documents the range, so from the client's side the bridge simply stops
  answering.
- `pending_request_ids()` now enumerates the bridge directory with
  `reaper.EnumerateFiles`, matches `request_(%d+)%.json` and sorts by id.

**`server/bridge.py` — desync-proof file IPC**
- Purge stale `request_*`/`response_*` files on `ReaperFileBridge.__init__` and
  clear the same-id pair before each request + on timeout. A `response_N.json`
  left over from a timed-out call (or a previous server run, since `request_id`
  is in-memory and resets to 0 on restart) was otherwise read as the answer to a
  brand-new same-id request → the sticky `Failed to get tracks info` /
  `Timeout waiting for REAPER response` that never recovered until REAPER's
  bridge action was re-run.
- Timeout is now `REAPER_MCP_TIMEOUT` env (default **15 s**, was a hard 5 s) so
  bulk operations (hundreds of `MIDI_InsertNote`s) don't spuriously time out
  while the bridge is still busy — a spurious timeout is what left the stale
  response behind in the first place.

**`server/dsl/tools.py` — dialog-safe `dsl_save`**
- `dsl_save` used `Main_SaveProject(0, force_save_as)`, which pops a modal
  **Save As** dialog for a never-saved project (or any save-as). A modal dialog
  blocks the single-threaded Lua bridge and hangs every subsequent MCP call
  until dismissed. Now it writes a concrete `.rpp` via `Main_SaveProjectEx`
  (named → `~/Music/REAPER Projects/<name>.rpp`, unnamed → reuse the current
  project file or `Untitled.rpp`) — never a dialog. Dir override:
  `REAPER_MCP_PROJECT_DIR`.

## REAPER-side setup (local — lives in the REAPER resource dir, not this repo)

- **Auto-start:** `<REAPER resource>/Scripts/__startup.lua` `dofile`s the bridge
  on every launch (wrapped in `pcall`), so the MCP tools work right after a
  REAPER restart with no manual "run the action" step:
  ```lua
  local ok, err = pcall(function()
      dofile(reaper.GetResourcePath() .. '/Scripts/mcp_bridge_file_v2.lua')
  end)
  if not ok then reaper.ShowConsoleMsg('MCP bridge auto-start failed: ' .. tostring(err) .. '\n') end
  ```
- **Single-instance guard:** a `if _G.__MCP_BRIDGE_RUNNING then return end` /
  `_G.__MCP_BRIDGE_RUNNING = true` guard at the top of the running bridge script
  prevents a duplicate `reaper.defer` poll loop if it's started twice
  (e.g. `__startup` + a manual re-run) racing on the same request files.

## Hard-won rule

**Never interleave direct file-IPC writes to the bridge dir with MCP tool calls.**
Two writers reaching the same numeric id (the server's counter climbs into the
hundreds over a session; manual pings often use 700+) cross-read each other's
responses → the desync above. Use MCP-only or direct-IPC-only for a whole task.
