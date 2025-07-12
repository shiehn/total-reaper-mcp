# Hybrid Lua–Python REAPER MCP Server  
**Detailed Development Guide**

---

## 0. Prerequisites

| Requirement | Purpose | Extra Setup |
|-------------|---------|-------------|
| REAPER 6.83 or newer | Bundles embedded Lua 5.4 and full ReaScript API | None |
| macOS 10.15 (Catalina) – 14.x | Supported by PyInstaller universal‑2 builds | None |
| No external Python / Lua | The bridge runs on REAPER’s Lua; Python is bundled in your EXE | – |

---

## 1. Repository Layout

```text
reaper-mcp/
├─ lua/
│  └─ mcp_bridge.lua            # 40‑line reflection stub
├─ server/
│  ├─ app.py                    # FastAPI entry‑point
│  ├─ handles.py                # ID↔pointer helpers
│  ├─ client.py                 # Optional Python wrapper
│  └─ pyproject.toml            # Poetry / Hatch
├─ scripts/
│  └─ install.sh                # One‑liner installer
├─ .github/workflows/
│  └─ build-mac.yml             # CI: universal build + release
└─ README.md
```

---

## 2. Lua Reflection Stub (`lua/mcp_bridge.lua`)

```lua
local json   = require('dkjson')            -- bundled
local socket = require('socket').udp()
socket:setpeername('127.0.0.1', 9000)

local handles, next_id = {}, 1

local function pack(v)
  if type(v) == 'userdata' then
    local id = next_id; next_id = id + 1
    handles[id] = v
    return { __ptr = id }
  end
  return v
end

function mcp_bridge(call, ...)
  local ok, ret = pcall(_G[call], ...)
  if ok then ret = pack(ret) end
  socket:send(json.encode{ ok = ok, ret = ret })
  return ret
end

function mcp_lookup(id) return handles[id] end
```

*Runs on every REAPER install with zero extra dependencies.*

---

## 3. Python Server (`server/app.py`)

```python
import json, socket
from fastapi import FastAPI

UDP = ('127.0.0.1', 9000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
app = FastAPI()

def call_lua(fname, args):
    sock.send(json.dumps({'call': fname, 'args': args}).encode())
    data, _ = sock.recvfrom(65536)
    return json.loads(data)

@app.post('/call')
async def call(body: dict):
    return call_lua(body['call'], body.get('args', []))

def main():
    import uvicorn
    uvicorn.run('server.app:app', port=8765, reload=False)
```

`pyproject.toml` (Poetry example):

```toml
[project]
name = "reaper_mcp_server"
version = "0.1.0"
dependencies = ["fastapi", "uvicorn[standard]"]
[tool.poetry.scripts]
mcp-server = "server.app:main"
```

---

## 4. Local Development & Tests

```bash
# launch REAPER manually and run mcp_bridge.lua
poetry install
poetry run mcp-server &

curl -X POST http://127.0.0.1:8765/call      -d '{"call":"InsertTrackAtIndex","args":[0,true]}'
pytest
```

---

## 5. Freeze to Universal macOS EXE

```bash
# On Intel builder
pyinstaller -F -n mcp_server_x86 server/app.py --target-arch x86_64
# On Apple‑Silicon builder
pyinstaller -F -n mcp_server_arm server/app.py --target-arch arm64
# Merge
lipo -create dist/mcp_server_x86 dist/mcp_server_arm      -output dist/mcp_server_universal
tar -czf mcp_server-mac.tar.gz -C dist mcp_server_universal
```

---

## 6. GitHub Actions CI (`.github/workflows/build-mac.yml`)

```yaml
name: build-mac
on: [push, workflow_dispatch]
jobs:
  build:
    strategy:
      matrix: arch: [x86_64, arm64]
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - run: brew install python@3.11 pyinstaller
      - run: ./scripts/build_${{ matrix.arch }}.sh
  merge:
    needs: build
    runs-on: macos-latest
    steps:
      - uses: actions/download-artifact@v4
      - run: lipo -create dist/*_x86 dist/*_arm -output mcp_server_universal
      - run: gh release upload ...
```

---

## 7. One‑Liner Installer (`scripts/install.sh`)

```bash
#!/usr/bin/env bash
set -e
SCRIPTS="$HOME/Library/Application Support/REAPER/Scripts"
curl -fsSL https://raw.githubusercontent.com/your-org/reaper-mcp/main/lua/mcp_bridge.lua      -o "$SCRIPTS/mcp_bridge.lua"
xattr -rd com.apple.quarantine "$SCRIPTS/mcp_bridge.lua"

APPDIR="$HOME/Applications/MCP-Server"
mkdir -p "$APPDIR"
LATEST=$(curl -s https://api.github.com/repos/your-org/reaper-mcp/releases/latest |          grep mac | cut -d '"' -f4)
curl -L "$LATEST" | tar -xz -C "$APPDIR"
xattr -rd com.apple.quarantine "$APPDIR/mcp_server"

open -a "$APPDIR/mcp_server"
echo 'Open REAPER ➜ Actions ➜ Run "mcp_bridge.lua" (add to startup).'
```

---

## 8. Optional Enhancements

* **ReaPack feed** for auto‑updating the Lua stub.  
* **launchd plist** to auto‑start the server on login.  
* **Startup Action** so REAPER runs the stub automatically.

---

## 9. Common macOS Questions

| Question | Answer |
|----------|--------|
| Do I need to enable Python in REAPER? | No—the Python process is external. |
| Will Gatekeeper complain? | The installer clears the quarantine bit, so no warning dialog. |
| Intel vs Apple Silicon? | Universal‑2 EXE runs natively on both CPUs. |

---

## 10. Claude Code Workflow

```bash
claude-code py .
# edit files, run pytest, build scripts
./scripts/build_arm.sh
```

Claude Code can modify any file in the repo; commit and push to trigger CI.

---

## 11. Milestone Checklist

| Milestone | Deliverable |
|-----------|-------------|
| M0 | Lua stub responds with API version. |
| M1 | `/call` inserts a track (CRUD proven). |
| M2 | Universal PyInstaller build produced by CI. |
| M3 | `install.sh` completes on fresh macOS VM in <30 s. |
| M4 | ReaPack auto‑updates verified. |
| M5 | launchd + Startup Action for hands‑free load. |

---

*Project complete once M3 is reached—users get full‑CRUD MCP server with a single command.*
