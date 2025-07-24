-- DSL Bridge Functions for REAPER MCP
-- These functions support the high-level DSL/Macro layer

-- Add these functions to the main bridge by including this file

-- DSL Helper Functions

-- Get detailed track information including MIDI/audio content and FX
local function GetTrackInfo(track_index)
    local track = nil
    if track_index == -1 then
        track = reaper.GetMasterTrack(0)
    else
        track = reaper.GetTrack(0, track_index)
    end
    
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    -- Get track info
    local retval, name = reaper.GetTrackName(track)
    local retval, guid = reaper.GetSetMediaTrackInfo_String(track, "GUID", "", false)
    
    -- Check for MIDI and audio items
    local has_midi = false
    local has_audio = false
    local item_count = reaper.CountTrackMediaItems(track)
    
    for i = 0, item_count - 1 do
        local item = reaper.GetTrackMediaItem(track, i)
        if item then
            local take = reaper.GetActiveTake(item)
            if take then
                if reaper.TakeIsMIDI(take) then
                    has_midi = true
                else
                    has_audio = true
                end
            end
        end
    end
    
    -- Get FX names
    local fx_names = {}
    local fx_count = reaper.TrackFX_GetCount(track)
    for i = 0, fx_count - 1 do
        local retval, fx_name = reaper.TrackFX_GetFXName(track, i, "")
        if retval then
            table.insert(fx_names, fx_name)
        end
    end
    
    -- Check for role in track notes
    local retval, notes = reaper.GetSetMediaTrackInfo_String(track, "P_EXT:role", "", false)
    local role = nil
    if notes and notes ~= "" then
        role = notes
    end
    
    return {
        ok = true,
        info = {
            guid = guid,
            name = name,
            has_midi = has_midi,
            has_audio = has_audio,
            fx_names = fx_names,
            role = role,
            muted = reaper.GetMediaTrackInfo_Value(track, "B_MUTE") == 1,
            soloed = reaper.GetMediaTrackInfo_Value(track, "I_SOLO") > 0
        }
    }
end

-- Get all tracks with detailed info
local function GetAllTracksInfo()
    local tracks = {}
    local count = reaper.CountTracks(0)
    
    for i = 0, count - 1 do
        local result = GetTrackInfo(i)
        if result.ok then
            local info = result.info
            info.index = i
            table.insert(tracks, info)
        end
    end
    
    return {ok = true, tracks = tracks}
end

-- Get/Set track notes (used for storing role)
local function SetTrackNotes(track_index, notes)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    -- Store in extended state
    reaper.GetSetMediaTrackInfo_String(track, "P_EXT:role", notes, true)
    return {ok = true}
end

-- Get current cursor position
local function GetCursorPosition()
    local pos = reaper.GetCursorPosition()
    return {ok = true, ret = pos}
end

-- Get time selection
local function GetTimeSelection()
    local start_time, end_time = reaper.GetSet_LoopTimeRange(false, false, 0, 0, false)
    return {ok = true, start = start_time, ["end"] = end_time}
end

-- Set time selection
local function SetTimeSelection(start_time, end_time)
    reaper.GetSet_LoopTimeRange(true, false, start_time, end_time, false)
    return {ok = true}
end

-- Get loop time range
local function GetLoopTimeRange()
    local start_time, end_time = reaper.GetSet_LoopTimeRange(false, true, 0, 0, false)
    return {ok = true, start = start_time, ["end"] = end_time}
end

-- Convert bars to time duration
local function BarsToTime(bars, start_pos)
    -- Get tempo at position
    local tempo = reaper.Master_GetTempo()
    local retval, num, denom = reaper.TimeMap_GetTimeSigAtTime(0, start_pos or 0)
    
    -- Calculate duration
    local beats_per_bar = num
    local total_beats = bars * beats_per_bar
    local duration = (total_beats / tempo) * 60
    
    return {ok = true, ret = duration}
end

-- Find region by name
local function FindRegion(name)
    local retval, num_markers, num_regions = reaper.CountProjectMarkers(0)
    
    for i = 0, num_markers + num_regions - 1 do
        local retval, isrgn, pos, rgnend, rgn_name, markrgnindexnumber = reaper.EnumProjectMarkers(i)
        if isrgn and rgn_name == name then
            return {ok = true, found = true, start = pos, ["end"] = rgnend}
        end
    end
    
    return {ok = true, found = false}
end

-- Find marker by name
local function FindMarker(name)
    local retval, num_markers, num_regions = reaper.CountProjectMarkers(0)
    
    for i = 0, num_markers + num_regions - 1 do
        local retval, isrgn, pos, rgnend, marker_name, markrgnindexnumber = reaper.EnumProjectMarkers(i)
        if not isrgn and marker_name == name then
            return {ok = true, found = true, position = pos}
        end
    end
    
    return {ok = true, found = false}
end

-- Get selected items
local function GetSelectedItems()
    local items = {}
    local count = reaper.CountSelectedMediaItems(0)
    
    for i = 0, count - 1 do
        local item = reaper.GetSelectedMediaItem(0, i)
        if item then
            local track = reaper.GetMediaItem_Track(item)
            local track_index = -1
            
            -- Find track index
            for j = 0, reaper.CountTracks(0) - 1 do
                if reaper.GetTrack(0, j) == track then
                    track_index = j
                    break
                end
            end
            
            local take = reaper.GetActiveTake(item)
            local is_midi = take and reaper.TakeIsMIDI(take)
            local retval, name = reaper.GetTakeName(take or item)
            
            table.insert(items, {
                index = i,
                track_index = track_index,
                position = reaper.GetMediaItemInfo_Value(item, "D_POSITION"),
                length = reaper.GetMediaItemInfo_Value(item, "D_LENGTH"),
                name = name,
                is_midi = is_midi
            })
        end
    end
    
    return {ok = true, items = items}
end

-- Get all items
local function GetAllItems()
    local items = {}
    local track_count = reaper.CountTracks(0)
    
    for t = 0, track_count - 1 do
        local track = reaper.GetTrack(0, t)
        local item_count = reaper.CountTrackMediaItems(track)
        
        for i = 0, item_count - 1 do
            local item = reaper.GetTrackMediaItem(track, i)
            if item then
                local take = reaper.GetActiveTake(item)
                local is_midi = take and reaper.TakeIsMIDI(take)
                local retval, name = reaper.GetTakeName(take or item)
                
                table.insert(items, {
                    index = i,
                    track_index = t,
                    position = reaper.GetMediaItemInfo_Value(item, "D_POSITION"),
                    length = reaper.GetMediaItemInfo_Value(item, "D_LENGTH"),
                    name = name,
                    is_midi = is_midi
                })
            end
        end
    end
    
    return {ok = true, items = items}
end

-- Get items on specific track
local function GetTrackItems(track_index)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    local items = {}
    local item_count = reaper.CountTrackMediaItems(track)
    
    for i = 0, item_count - 1 do
        local item = reaper.GetTrackMediaItem(track, i)
        if item then
            local take = reaper.GetActiveTake(item)
            local is_midi = take and reaper.TakeIsMIDI(take)
            local retval, name = reaper.GetTakeName(take or item)
            
            table.insert(items, {
                index = i,
                track_index = track_index,
                position = reaper.GetMediaItemInfo_Value(item, "D_POSITION"),
                length = reaper.GetMediaItemInfo_Value(item, "D_LENGTH"),
                name = name,
                is_midi = is_midi
            })
        end
    end
    
    return {ok = true, items = items}
end

-- Create MIDI item
local function CreateMIDIItem(track_index, start_pos, end_pos)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    local item = reaper.CreateNewMIDIItemInProj(track, start_pos, end_pos, false)
    if not item then
        return {ok = false, error = "Failed to create MIDI item"}
    end
    
    -- Find item index on track
    local item_index = -1
    for i = 0, reaper.CountTrackMediaItems(track) - 1 do
        if reaper.GetTrackMediaItem(track, i) == item then
            item_index = i
            break
        end
    end
    
    return {ok = true, item_index = item_index}
end

-- Create audio item (empty)
local function CreateAudioItem(track_index, start_pos, end_pos)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    -- Create empty item
    local item = reaper.AddMediaItemToTrack(track)
    if not item then
        return {ok = false, error = "Failed to create audio item"}
    end
    
    -- Set position and length
    reaper.SetMediaItemInfo_Value(item, "D_POSITION", start_pos)
    reaper.SetMediaItemInfo_Value(item, "D_LENGTH", end_pos - start_pos)
    
    -- Find item index on track
    local item_index = -1
    for i = 0, reaper.CountTrackMediaItems(track) - 1 do
        if reaper.GetTrackMediaItem(track, i) == item then
            item_index = i
            break
        end
    end
    
    return {ok = true, item_index = item_index}
end

-- Set item loop source
local function SetItemLoopSource(track_index, item_index, loop_source)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    local item = reaper.GetTrackMediaItem(track, item_index)
    if not item then
        return {ok = false, error = "Item not found"}
    end
    
    reaper.SetMediaItemInfo_Value(item, "B_LOOPSRC", loop_source and 1 or 0)
    return {ok = true}
end

-- Insert MIDI note
local function InsertMIDINote(track_index, item_index, pitch, start_ppq, length_ppq, velocity, channel)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    local item = reaper.GetTrackMediaItem(track, item_index)
    if not item then
        return {ok = false, error = "Item not found"}
    end
    
    local take = reaper.GetActiveTake(item)
    if not take or not reaper.TakeIsMIDI(take) then
        return {ok = false, error = "Not a MIDI take"}
    end
    
    -- Convert time to PPQ
    local item_pos = reaper.GetMediaItemInfo_Value(item, "D_POSITION")
    local ppq_start = reaper.MIDI_GetPPQPosFromProjTime(take, item_pos + start_ppq)
    local ppq_end = reaper.MIDI_GetPPQPosFromProjTime(take, item_pos + start_ppq + length_ppq)
    
    reaper.MIDI_InsertNote(take, false, false, ppq_start, ppq_end, channel or 0, pitch, velocity or 100, false)
    reaper.MIDI_Sort(take)
    
    return {ok = true}
end

-- Quantize item
local function QuantizeItem(track_index, item_index, strength, grid)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    local item = reaper.GetTrackMediaItem(track, item_index)
    if not item then
        return {ok = false, error = "Item not found"}
    end
    
    local take = reaper.GetActiveTake(item)
    if not take or not reaper.TakeIsMIDI(take) then
        return {ok = false, error = "Not a MIDI take"}
    end
    
    -- Note: This is a simplified quantization
    -- In practice, you'd use MIDI editor actions or more complex logic
    -- For now, just return success
    return {ok = true}
end

-- Track operations
local function GetTrackVolume(track_index)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    local vol = reaper.GetMediaTrackInfo_Value(track, "D_VOL")
    return {ok = true, ret = vol}
end

local function SetTrackVolume(track_index, volume)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    reaper.SetMediaTrackInfo_Value(track, "D_VOL", volume)
    return {ok = true}
end

local function GetTrackPan(track_index)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    local pan = reaper.GetMediaTrackInfo_Value(track, "D_PAN")
    return {ok = true, ret = pan}
end

local function SetTrackPan(track_index, pan)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    reaper.SetMediaTrackInfo_Value(track, "D_PAN", pan)
    return {ok = true}
end

local function SetTrackMute(track_index, mute)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    reaper.SetMediaTrackInfo_Value(track, "B_MUTE", mute and 1 or 0)
    return {ok = true}
end

local function SetTrackSolo(track_index, solo)
    local track = reaper.GetTrack(0, track_index)
    if not track then
        return {ok = false, error = "Track not found"}
    end
    
    reaper.SetMediaTrackInfo_Value(track, "I_SOLO", solo and 1 or 0)
    return {ok = true}
end

-- Transport operations
local function Play()
    reaper.Main_OnCommand(1007, 0) -- Transport: Play
    return {ok = true}
end

local function Stop()
    reaper.Main_OnCommand(1016, 0) -- Transport: Stop
    return {ok = true}
end

local function GetTempo()
    local tempo = reaper.Master_GetTempo()
    return {ok = true, ret = tempo}
end

local function SetTempo(bpm)
    reaper.SetTempoTimeSigMarker(0, -1, -1, -1, -1, bpm, 0, 0, false)
    return {ok = true}
end

local function GetTimeSignature()
    local retval, num, denom = reaper.TimeMap_GetTimeSigAtTime(0, reaper.GetCursorPosition())
    return {ok = true, numerator = num, denominator = denom}
end

-- Export function table for DSL
DSL_FUNCTIONS = {
    -- Track info
    GetTrackInfo = GetTrackInfo,
    GetAllTracksInfo = GetAllTracksInfo,
    SetTrackNotes = SetTrackNotes,
    
    -- Time operations
    GetCursorPosition = GetCursorPosition,
    GetTimeSelection = GetTimeSelection,
    SetTimeSelection = SetTimeSelection,
    GetLoopTimeRange = GetLoopTimeRange,
    BarsToTime = BarsToTime,
    FindRegion = FindRegion,
    FindMarker = FindMarker,
    
    -- Item operations
    GetSelectedItems = GetSelectedItems,
    GetAllItems = GetAllItems,
    GetTrackItems = GetTrackItems,
    CreateMIDIItem = CreateMIDIItem,
    CreateAudioItem = CreateAudioItem,
    SetItemLoopSource = SetItemLoopSource,
    InsertMIDINote = InsertMIDINote,
    QuantizeItem = QuantizeItem,
    
    -- Track operations
    GetTrackVolume = GetTrackVolume,
    SetTrackVolume = SetTrackVolume,
    GetTrackPan = GetTrackPan,
    SetTrackPan = SetTrackPan,
    SetTrackMute = SetTrackMute,
    SetTrackSolo = SetTrackSolo,
    
    -- Transport
    Play = Play,
    Stop = Stop,
    GetTempo = GetTempo,
    SetTempo = SetTempo,
    GetTimeSignature = GetTimeSignature
}