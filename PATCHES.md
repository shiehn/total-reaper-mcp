# Local hardening patches (2026-07-24)

Fixes for a sticky desync + modal-dialog hang hit while driving REAPER heavily
via the file bridge. The two code changes below are general and are proposed
upstream; the REAPER-config bits are local setup notes.

## Code (in this repo — proposed upstream)

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

**`lua/mcp_bridge.lua` + `scripts/install_bridge.sh` — auto-start, one loop only**
- `install_bridge.sh` also installs `scripts/startup/__startup.lua` into
  `<REAPER resource>/Scripts/` (never over an existing one; if one exists without
  the bridge, it prints the line to add). REAPER runs it on every launch, so the
  MCP tools work right after a restart with no manual "run the action" step.
- Single instance: auto-start plus a manual run of the action would start two
  `reaper.defer` loops racing on the same request files. A `_G` flag cannot
  prevent it, because each ReaScript run has its own Lua state. The running loop
  stamps a heartbeat into the process-wide ExtState (`mcp_bridge/heartbeat`);
  a new start backs off while it is under 2 s old, and starts normally once a
  stopped bridge has gone quiet. Test: `lua tests/lua/bridge_single_instance.lua`.

**Install from a fresh clone**
- `.venv`/`.venv-new` are no longer tracked: their symlinks pointed at another
  machine's Python, so `python -m venv .venv` on a clone left no interpreter.
- `mcp<2` pinned: 2.x renamed FastMCP and `server.app` failed on import.

## Hard-won rule

**Never interleave direct file-IPC writes to the bridge dir with MCP tool calls.**
Two writers reaching the same numeric id (the server's counter climbs into the
hundreds over a session; manual pings often use 700+) cross-read each other's
responses → the desync above. Use MCP-only or direct-IPC-only for a whole task.
