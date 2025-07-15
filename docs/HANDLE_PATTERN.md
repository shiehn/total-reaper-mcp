# REAPER MCP Handle/Index Pattern Documentation

## The Problem
REAPER's native API uses pointers/handles for tracks, items, takes, etc. However, passing pointers between Python and Lua is problematic due to serialization.

## The Solution Pattern

### Python Side (MCP Tools)
- **ALWAYS pass indices** (track_index, item_index, take_index)
- **NEVER retrieve handles** in Python code
- Let the Lua bridge handle all conversions

### Lua Bridge Side
- **Accept indices from Python**
- **Convert indices to handles** using GetTrack, GetMediaItem, etc.
- **Pass handles to REAPER API**
- **Return success/data to Python**

## Examples

### CORRECT Pattern:
```python
# Python side - pass index
async def set_track_selected(track_index: int, selected: bool):
    result = await bridge.call_lua("SetTrackSelected", [track_index, selected])
```

```lua
-- Lua side - convert index to handle
elseif fname == "SetTrackSelected" then
    local track = reaper.GetTrack(0, args[1])  -- Convert index to handle
    if track then
        reaper.SetTrackSelected(track, args[2])  -- Use handle with API
        response.ok = true
    end
```

### INCORRECT Pattern:
```python
# Python side - DON'T DO THIS
async def set_track_selected(track_index: int, selected: bool):
    # Wrong: Getting handle in Python
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    track = track_result.get("ret")
    result = await bridge.call_lua("SetTrackSelected", [track, selected])
```

## Common Functions Following This Pattern

### Track Operations
- SetTrackSelected(track_index, selected)
- SetMediaTrackInfo_Value(track_index, param, value)
- GetMediaTrackInfo_Value(track_index, param)
- TrackFX_*(track_index, ...)

### Item Operations
- SetMediaItemInfo_Value(item_index, param, value)
- GetMediaItemInfo_Value(item_index, param)
- GetMediaItemTake(item_index, take_index)

### Take Operations
- SetMediaItemTakeInfo_Value(take_index, param, value)
- GetMediaItemTakeInfo_Value(take_index, param)
- TakeFX_*(take_index, ...)

## Special Cases

### Envelope Operations
Due to MCP framework issues, envelope operations currently have problems with parameter transformation.

### Cross-references
When a function returns a track/item/take that needs to be used elsewhere, return its index, not its handle.

## Testing Pattern
Tests should use indices consistently and let the bridge handle conversions.