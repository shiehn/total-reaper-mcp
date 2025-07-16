# REAPER MCP Implementation Master List

This is the consolidated master list tracking all ReaScript API methods implemented in the REAPER MCP Server.

## Implementation Statistics
- **Total Implemented**: 756 tools (includes both ReaScript methods and high-level music production tools)
- **ReaScript API Methods**: 375+ core methods
- **Music Production Tools**: 45 new high-level tools
- **Test Coverage**: ~97%
- **Categories**: 44 (40 ReaScript + 4 new music production categories)
- **Test Files**: 47 (includes new integration tests)
- **ReaScript API Version**: REAPER 6.83+ (embedded Lua 5.4)

## Implementation Status by Category

### ✅ Track Management (22 methods)
- [x] `InsertTrackAtIndex` - Insert a new track at specified index
- [x] `CountTracks` - Get the number of tracks in current project
- [x] `GetTrack` - Get track by index from the current project
- [x] `GetMasterTrack` - Get the master track
- [x] `DeleteTrack` - Delete a track by index
- [x] `SetTrackSelected` - Select or deselect a track
- [x] `GetTrackName` - Get the name of a track
- [x] `SetTrackName` - Set the name of a track
- [x] `GetAppVersion` - Get REAPER version string
- [x] `GetTrackMute` - Get track mute state
- [x] `SetTrackMute` - Set track mute state
- [x] `GetTrackSolo` - Get track solo state
- [x] `SetTrackSolo` - Set track solo state
- [x] `GetTrackVolume` - Get track volume in dB
- [x] `SetTrackVolume` - Set track volume in dB
- [x] `GetTrackPan` - Get track pan position
- [x] `SetTrackPan` - Set track pan position
- [x] `GetLastTouchedTrack` - Get the last touched track
- [x] `GetTrackMIDINoteName` - Get MIDI note name for a track and pitch
- [x] `AnyTrackSolo` - Check if any track is soloed
- [x] `GetMixerScroll` - Get the leftmost track visible in the mixer
- [x] `SetMixerScroll` - Set the leftmost track visible in the mixer

### ✅ Selection Operations (8 methods)
- [x] `CountSelectedTracks` - Count selected tracks
- [x] `GetSelectedTrack` - Get selected track by index
- [x] `SetTrackSelected` - Set track selection state
- [x] `CountSelectedMediaItems` - Count selected media items
- [x] `GetSelectedMediaItem` - Get selected media item by index
- [x] `SetMediaItemSelected` - Set media item selection state
- [x] `SelectAllMediaItems` - Select all media items
- [x] `UnselectAllMediaItems` - Unselect all media items

### ✅ Audio Source Management (7 methods)
- [x] `GetMediaItemTakeSource` - Get media source from take
- [x] `GetMediaSourceFilename` - Get source filename
- [x] `GetMediaSourceLength` - Get source length
- [x] `GetMediaSourceType` - Get source type
- [x] `PCM_Source_CreateFromFile` - Create PCM source from file
- [x] `SetMediaItemTakeSource` - Set take source
- [x] `GetMediaItemTakePeaks` - Get peak data

### ✅ Track Grouping/Folders (6 methods)
- [x] `GetTrackDepth` - Get track folder depth
- [x] `SetTrackFolderState` - Set track folder state
- [x] `GetTrackFolderCompactState` - Get folder compact state
- [x] `SetTrackFolderCompactState` - Set folder compact state
- [x] `GetParentTrack` - Get parent track
- [x] `SetTrackHeight` - Set track height

### ✅ Media Items (9 methods)
- [x] `AddMediaItemToTrack` - Add a new media item to a track
- [x] `CountMediaItems` - Count total media items in project
- [x] `GetMediaItem` - Get media item by index
- [x] `DeleteTrackMediaItem` - Delete a media item from track
- [x] `GetMediaItemLength` - Get media item length
- [x] `SetMediaItemLength` - Set media item length
- [x] `GetMediaItemPosition` - Get media item position
- [x] `SetMediaItemPosition` - Set media item position
- [x] `CountTrackMediaItems` - Count items on track

### ✅ MIDI Operations (19 methods)
**Basic MIDI (9 methods):**
- [x] `MIDI_InsertNote` - Insert MIDI note
- [x] `MIDI_DeleteNote` - Delete MIDI note
- [x] `MIDI_SetNote` - Modify MIDI note
- [x] `MIDI_GetNote` - Get MIDI note details
- [x] `MIDI_CountEvts` - Count MIDI events
- [x] `MIDI_InsertCC` - Insert control change
- [x] `MIDI_DeleteCC` - Delete control change
- [x] `MIDI_SetCC` - Modify control change
- [x] `MIDI_GetCC` - Get control change details

**Advanced MIDI (10 methods):**
- [x] `MIDI_GetAllEvts` - Get all MIDI events
- [x] `MIDI_SetAllEvts` - Set all MIDI events
- [x] `MIDI_GetNoteName` - Get note name
- [x] `MIDI_GetScale` - Get scale settings
- [x] `MIDI_SetScale` - Set scale settings
- [x] `MIDI_GetTextSysexEvt` - Get text/sysex event
- [x] `MIDI_SetTextSysexEvt` - Set text/sysex event
- [x] `MIDI_CountEvents` - Count all event types
- [x] `MIDI_EnumSelNotes` - Enumerate selected notes
- [x] `MIDI_SelectAll` - Select all MIDI

### ✅ Rendering/Freezing (6 methods)
- [x] `Main_RenderProject` - Render project
- [x] `FreezeTrack` - Freeze track
- [x] `UnfreezeTrack` - Unfreeze track
- [x] `IsTrackFrozen` - Check if track frozen
- [x] `RenderTimeSelection` - Render time selection
- [x] `ApplyFXToItems` - Apply FX to items

### ✅ Effects/FX (7 methods)
- [x] `TrackFX_AddByName` - Add FX by name
- [x] `TrackFX_Delete` - Delete FX
- [x] `TrackFX_GetCount` - Count FX on track
- [x] `TrackFX_GetFXName` - Get FX name
- [x] `TrackFX_GetParam` - Get parameter value
- [x] `TrackFX_SetParam` - Set parameter value
- [x] `TrackFX_GetEnabled` - Get enabled state

### ✅ Transport & Playback (10 methods)
- [x] `GetCursorPosition` - Get edit cursor position
- [x] `SetEditCurPos` - Set edit cursor position
- [x] `GetPlayState` - Get current playback state
- [x] `CSurf_OnPlay` - Start playback
- [x] `CSurf_OnStop` - Stop playback
- [x] `CSurf_OnPause` - Pause playback
- [x] `CSurf_SetPlayState` - Set play/pause/record state
- [x] `CSurf_SetRepeatState` - Set repeat/loop state
- [x] `Main_OnCommand` - Execute REAPER action
- [x] `GoToMarker` - Navigate to marker

### ✅ Project Management (11 methods)
- [x] `GetProjectName` - Get project name
- [x] `GetProjectPath` - Get project path
- [x] `Main_SaveProject` - Save project
- [x] `IsProjectDirty` - Check if project has unsaved changes
- [x] `GetProjectStateChangeCount` - Get state change count
- [x] `GetResourcePath` - Get REAPER resource path
- [x] `GetExePath` - Get REAPER executable path
- [x] `RecursiveCreateDirectory` - Create directory recursively
- [x] `MarkProjectDirty` - Mark the project as having unsaved changes
- [x] `GetProjectLength` - Get the length of the project
- [x] `IsInRealTimeAudio` - Check if currently in real-time audio thread

### ✅ Envelopes (6 methods)
- [x] `GetTrackEnvelope` - Get track envelope
- [x] `InsertEnvelopePoint` - Insert envelope point
- [x] `DeleteEnvelopePoint` - Delete envelope point
- [x] `GetEnvelopePoint` - Get envelope point details
- [x] `SetEnvelopePoint` - Set envelope point
- [x] `CountEnvelopePoints` - Count envelope points

### ✅ Automation (6 methods)
- [x] `GetTrackAutomationMode` - Get automation mode
- [x] `SetTrackAutomationMode` - Set automation mode
- [x] `GetGlobalAutomationMode` - Get global automation
- [x] `SetGlobalAutomationMode` - Set global automation
- [x] `GetSetAutomationItemInfo` - Get/set automation item info
- [x] `CountAutomationItems` - Count automation items

### ✅ Time and Tempo (8 methods)
- [x] `GetProjectBPM` - Get project BPM
- [x] `SetProjectBPM` - Set project BPM
- [x] `TimeMap_GetTimeSigAtTime` - Get time signature
- [x] `TimeMap_QNToTime` - Convert quarter notes to time
- [x] `TimeMap2_QNToTime` - Convert quarter notes to time using TimeMap2
- [x] `TimeMap2_timeToQN` - Convert time to quarter notes using TimeMap2
- [x] `TimeMap_GetMeasureInfo` - Get measure information at time position
- [x] `GetTempoTimeSigMarker` - Get tempo/time signature marker by index

### ✅ Markers and Regions (4 methods)
- [x] `AddProjectMarker` - Add marker/region
- [x] `DeleteProjectMarker` - Delete marker/region
- [x] `CountProjectMarkers` - Count markers/regions
- [x] `EnumProjectMarkers` - Enumerate markers/regions

### ✅ Track Routing (3 methods)
- [x] `CreateTrackSend` - Create track send
- [x] `RemoveTrackSend` - Remove track send
- [x] `GetTrackNumSends` - Get send count

### ✅ GUI/Console Operations (7 methods)
- [x] `ShowConsoleMsg` - Show console message
- [x] `ClearConsole` - Clear console
- [x] `ShowMessageBox` - Show message box
- [x] `GetMainHwnd` - Get main window handle
- [x] `DockWindowAdd` - Dock window
- [x] `GetMousePosition` - Get mouse position
- [x] `GetCursorContext` - Get cursor context

### ✅ Takes (8 methods)
- [x] `AddTakeToMediaItem` - Add take to item
- [x] `CountTakes` - Count takes
- [x] `GetActiveTake` - Get active take
- [x] `SetActiveTake` - Set active take
- [x] `GetTake` - Get take by index
- [x] `GetTakeName` - Get take name
- [x] `SetTakeName` - Set take name
- [x] `DeleteTakeFromItem` - Delete take

### ✅ Time Selection/Loop (2 methods)
- [x] `GetSet_LoopTimeRange` - Get/set loop range
- [x] `GetSet_ArrangeView` - Get/set arrange view

### ✅ Loop & Time Selection Management (16 high-level tools) - NEW
- [x] `get_time_selection` - Get current time selection (loop) in project
- [x] `set_time_selection` - Set time selection (loop) in project
- [x] `clear_time_selection` - Clear time selection
- [x] `get_loop_points` - Get loop point positions and status
- [x] `set_loop_enabled` - Enable or disable looping
- [x] `set_loop_points` - Set loop points and optionally enable looping
- [x] `duplicate_time_selection` - Duplicate contents of time selection
- [x] `shift_time_selection` - Shift time selection by offset
- [x] `create_loop_from_items` - Create time selection from selected items
- [x] `split_items_at_loop_points` - Split all items at loop boundaries
- [x] `get_grid_division` - Get current grid division setting
- [x] `set_grid_division` - Set grid division for quantization
- [x] `quantize_time_selection` - Quantize items in time selection to grid
- [x] `crop_to_time_selection` - Crop project to time selection
- [x] `insert_time_at_loop_start` - Insert empty time at loop start
- [x] `remove_time_selection` - Remove contents of time selection with ripple edit

### ✅ Bounce & Render Operations (11 high-level tools) - NEW
- [x] `bounce_track_in_place` - Bounce track in place, replacing with rendered audio
- [x] `bounce_tracks_to_stems` - Bounce multiple tracks to individual stem files
- [x] `freeze_track` - Freeze track to reduce CPU usage (enhanced)
- [x] `unfreeze_track` - Unfreeze previously frozen track (enhanced)
- [x] `render_selected_items_to_new_track` - Render selected items to new track
- [x] `glue_selected_items` - Glue selected items together
- [x] `apply_track_fx_to_items` - Apply track FX to items as render
- [x] `create_submix_from_tracks` - Create submix bus from selected tracks
- [x] `render_project_to_file` - Render entire project to file
- [x] `render_time_selection` - Render only time selection to file (enhanced)
- [x] `consolidate_track` - Consolidate all items on track into single item

### ✅ Groove & Quantization Tools (9 high-level tools) - NEW
- [x] `quantize_items_to_grid` - Quantize selected items with swing and strength
- [x] `humanize_items` - Add human timing and velocity variations
- [x] `create_groove_template` - Create groove template from selected items
- [x] `apply_groove_to_items` - Apply groove template to selected items
- [x] `generate_random_rhythm` - Generate random rhythm pattern on track
- [x] `apply_shuffle` - Apply shuffle/swing to selected items
- [x] `create_polyrhythm` - Create polyrhythmic patterns across tracks
- [x] `stretch_items_to_tempo` - Stretch selected items to match target tempo
- [x] `detect_tempo_from_selection` - Detect tempo from selected audio items

### ✅ Bus Routing & Mixing Workflows (9 high-level tools) - NEW
- [x] `create_bus_track` - Create bus track for routing multiple tracks
- [x] `route_tracks_to_bus` - Route multiple tracks to bus track
- [x] `create_parallel_compression_bus` - Create parallel compression setup
- [x] `create_reverb_send_bus` - Create reverb send bus with plugin
- [x] `create_stem_buses` - Create stem buses for track groups
- [x] `create_sidechain_routing` - Create sidechain routing between tracks
- [x] `setup_monitor_mix` - Setup monitor mix for performers
- [x] `create_headphone_cue_mixes` - Create multiple headphone cue mixes
- [x] `analyze_routing_matrix` - Analyze and return current routing matrix

### ✅ Undo System (2 methods)
- [x] `Undo_BeginBlock` - Begin undo block
- [x] `Undo_EndBlock` - End undo block

### ✅ UI Updates (2 methods)
- [x] `UpdateArrange` - Update arrange view
- [x] `UpdateTimeline` - Update timeline

### ✅ Track State (2 methods)
- [x] `GetTrackStateChunk` - Get track state
- [x] `SetTrackStateChunk` - Set track state

### ✅ Miscellaneous (3 methods)
- [x] `GetSelectedItems` - Get selected items
- [x] `BrowseForFile` - Browse for file
- [x] `GetProjectSettings` - Get project settings

### ✅ Audio/Peak Analysis (3 methods)
- [x] `GetTrackPeak` - Get current track peak level
- [x] `GetTrackPeakInfo` - Get detailed peak information
- [x] `GetMediaItemPeak` - Get media item peak value

### ✅ Advanced Track Operations (4 methods)
- [x] `GetTrackReceiveCount` - Count track receives
- [x] `GetTrackReceiveInfo` - Get track receive information
- [x] `GetTrackGUID` - Get track GUID
- [x] `GetTrackFromGUID` - Get track from GUID

### ✅ Advanced Item/Take Operations (5 methods)
- [x] `SplitMediaItem` - Split item at position
- [x] `GlueMediaItems` - Glue items together
- [x] `GetMediaItemTrack` - Get parent track of item
- [x] `DuplicateMediaItem` - Duplicate a media item
- [x] `SetMediaItemColor` - Set item color

### ✅ Recording Operations (6 methods)
- [x] `GetTrackRecordMode` - Get track record mode
- [x] `SetTrackRecordMode` - Set track record mode
- [x] `GetTrackRecordInput` - Get track record input
- [x] `SetTrackRecordInput` - Set track record input
- [x] `GetTrackRecordArm` - Get track record arm state
- [x] `SetTrackRecordArm` - Set track record arm state

### ✅ MIDI Hardware (4 methods)
- [x] `GetNumMIDIInputs` - Count MIDI inputs
- [x] `GetNumMIDIOutputs` - Count MIDI outputs
- [x] `GetMIDIInputName` - Get MIDI input name
- [x] `GetMIDIOutputName` - Get MIDI output name

### ✅ Color Management (3 methods)
- [x] `GetTrackColor` - Get track color
- [x] `SetTrackColor` - Set track color
- [x] `GetMediaItemColor` - Get item color
- Note: `SetMediaItemColor` already implemented in Advanced Item/Take Operations

### ✅ Advanced Project Operations (5 methods)
- [x] `Main_openProject` - Open project file
- [x] `EnumProjects` - Enumerate open projects
- [x] `SelectProjectInstance` - Switch to project
- [x] `GetCurrentProjectIndex` - Get current project index
- [x] `CloseProject` - Close current project

### ✅ Bounce/Render Operations (4 methods)
- [x] `RenderProject` - Render project to disk
- [x] `BounceTracks` - Bounce selected tracks
- [x] `GetRenderSettings` - Get render settings
- [x] `SetRenderSettings` - Set render settings

### ✅ Video Operations (4 methods)
- [x] `CheckVideoSupport` - Check if video is available
- [x] `GetVideoSettings` - Get video processor settings
- [x] `SetVideoSettings` - Set video processor settings
- [x] `AddVideoToTrack` - Add video file to track

### ✅ Core API Functions (3 methods)
- [x] `APIExists` - Check if a ReaScript API function exists
- [x] `GetLastColorThemeFile` - Get the last color theme file
- [x] `GetToggleCommandState` - Get the state of a toggle command

### ✅ Audio Accessor & Analysis (26 methods)
**Audio Accessor Management (8 methods):**
- [x] `CreateTrackAudioAccessor` - Create an audio accessor for a track
- [x] `CreateTakeAudioAccessor` - Create an audio accessor for a take
- [x] `DestroyAudioAccessor` - Destroy an audio accessor
- [x] `AudioAccessorUpdate` - Update audio accessor after changes
- [x] `AudioAccessorStateChanged` - Check if audio accessor state has changed
- [x] `AudioAccessorValidateState` - Validate audio accessor state
- [x] `GetAudioAccessorStartTime` - Get audio accessor start time
- [x] `GetAudioAccessorEndTime` - Get audio accessor end time

**Audio Analysis & Loudness (8 methods):**
- [x] `CalcMediaSrcLoudness` - Calculate loudness of media source
- [x] `CalculateNormalization` - Calculate normalization values for a take
- [x] `GetAudioDeviceInfo` - Get audio device information
- [x] `GetOutputLatency` - Get audio output latency
- [x] `GetNumAudioInputs` - Get number of audio inputs
- [x] `GetInputActivityLevel` - Get input channel activity level
- [x] `Audio_IsRunning` - Check if audio engine is running
- [x] `Audio_IsPreBuffer` - Check if audio is pre-buffering

**Peak Analysis (10 methods):**
- [x] `CalculatePeaks` - Calculate peaks for audio file
- [x] `PCM_Source_BuildPeaks` - Build peaks for PCM source
- [x] `GetPeakFileName` - Get the peak file name for a source file
- [x] `ClearPeakCache` - Clear the peak cache
- [x] `Track_GetPeakInfo` - Get detailed track peak information
- [x] `Track_GetPeakHoldDB` - Get track peak hold in dB
- [x] `GetPeaksBitmap` - Get peaks as bitmap data
- [x] `HiresPeaksFromSource` - Generate high-resolution peaks from source
- [x] `CalculatePeaksFloatSrcPtr` - Calculate peaks from float source data
- [x] `GetAudioAccessorSamples` - Get audio samples from accessor

### ✅ MIDI Editor & Piano Roll (26 methods)
**MIDI Editor Window Management (8 methods):**
- [x] `MIDI_Editor_Open` - Open MIDI editor for a take
- [x] `MIDIEditor_GetActive` - Get the active MIDI editor window
- [x] `MIDIEditor_GetTake` - Get the take from a MIDI editor
- [x] `MIDIEditor_GetSetting_int` - Get integer setting from MIDI editor
- [x] `MIDIEditor_SetSetting_int` - Set integer setting in MIDI editor
- [x] `MIDIEditor_GetMode` - Get MIDI editor mode
- [x] `MIDIEditor_OnCommand` - Execute MIDI editor command
- [x] `MIDI_RefreshEditor` - Refresh MIDI editor display

**MIDI Note Selection & Editing (10 methods):**
- [x] `MIDI_SelectNotes` - Select notes in range
- [x] `MIDI_GetSelectedNotes` - Get selected notes
- [x] `MIDI_SetNoteSelected` - Set note selection state
- [x] `MIDI_GetGrid` - Get MIDI grid settings
- [x] `MIDI_SelectCC` - Select CC events
- [x] `MIDI_GetCCShape` - Get CC shape
- [x] `MIDI_SetCCShape` - Set CC shape
- [x] `MIDI_HumanizeNotes` - Humanize MIDI notes
- [x] `MIDI_DisableSort` - Disable/enable MIDI auto-sorting
- [x] `MIDI_SetItemExtents` - Set item extents to match MIDI

**MIDI Time Conversion (4 methods):**
- [x] `MIDI_GetProjQNFromPPQPos` - Convert PPQ to project QN
- [x] `MIDI_GetPPQPosFromProjQN` - Convert project QN to PPQ
- [x] `MIDI_GetProjTimeFromPPQPos` - Convert PPQ to project time
- [x] `MIDI_GetPPQPosFromProjTime` - Convert project time to PPQ

**MIDI Display & Other (4 methods):**
- [x] `MIDI_GetNoteName` - Get MIDI note name
- [x] `MIDI_GetRecentInputEvent` - Get recent MIDI input event
- [x] `MIDI_InsertTextSysexEvt` - Insert text/sysex event
- [x] `MIDI_GetTextSysexEvt` - Get text/sysex event

### ✅ Routing & Sends (24 methods)
**Basic Send Operations (8 methods):**
- [x] `CreateTrackSend` - Create a send from one track to another
- [x] `RemoveTrackSend` - Remove a track send
- [x] `GetTrackNumSends` - Get number of sends/receives/hardware outputs
- [x] `GetTrackSendName` - Get send name
- [x] `GetSendDestinationTrack` - Get send destination track
- [x] `GetTrackReceiveName` - Get receive name
- [x] `GetReceiveSourceTrack` - Get receive source track
- [x] `CreateHardwareOutputSend` - Create hardware output send

**Send Parameter Management (8 methods):**
- [x] `GetTrackSendInfo_Value` - Get send parameter value
- [x] `SetTrackSendInfo_Value` - Set send parameter value
- [x] `GetSetTrackSendInfo_String` - Get/set send string parameter
- [x] `GetTrackSendUIVolPan` - Get send UI volume and pan
- [x] `SetTrackSendUIVol` - Set send UI volume
- [x] `SetTrackSendUIPan` - Set send UI pan
- [x] `ToggleTrackSendUIMute` - Toggle send mute
- [x] `GetTrackReceiveUIMute` - Get receive mute state

**Advanced Send Operations (4 methods):**
- [x] `SetSendEnabled` - Enable/disable send
- [x] `SetSendMode` - Set send mode (pre/post-fader)
- [x] `GetSendEnvelope` - Get send envelope
- [x] `GetTrackReceiveUIVolPan` - Get receive UI volume and pan

**Audio Output Management (4 methods):**
- [x] `GetNumAudioOutputs` - Get number of audio outputs
- [x] `GetOutputChannelName` - Get output channel name
- [x] `GetTrackUIVolPan` - Get track UI volume and pan
- [x] `SetTrackUIVolume` - Set track UI volume

### ✅ Take FX (19 methods)
**Basic Take FX Operations (8 methods):**
- [x] `TakeFX_GetCount` - Get take FX count
- [x] `TakeFX_AddByName` - Add FX to take by name
- [x] `TakeFX_Delete` - Delete take FX
- [x] `TakeFX_GetFXName` - Get take FX name
- [x] `TakeFX_GetEnabled` - Get take FX enabled state
- [x] `TakeFX_SetEnabled` - Set take FX enabled state
- [x] `TakeFX_GetPreset` - Get current take FX preset
- [x] `TakeFX_SetPreset` - Set take FX preset

**Take FX Parameters (7 methods):**
- [x] `TakeFX_GetNumParams` - Get number of parameters
- [x] `TakeFX_GetParamName` - Get parameter name
- [x] `TakeFX_GetParam` - Get parameter value
- [x] `TakeFX_SetParam` - Set parameter value
- [x] `TakeFX_GetParamNormalized` - Get normalized parameter value
- [x] `TakeFX_SetParamNormalized` - Set normalized parameter value
- [x] `TakeFX_GetFormattedParamValue` - Get formatted parameter value

**Take FX Copy Operations (4 methods):**
- [x] `TakeFX_CopyToTrack` - Copy take FX to track
- [x] `TakeFX_CopyToTake` - Copy take FX to another take
- [x] `TakeFX_GetFXGUID` - Get take FX GUID
- [x] `TakeFX_GetByIndex` - Get take FX by index

### ✅ Extended Audio Functions (2 methods)
- [x] `GetMediaSourceSampleRate` - Get the sample rate of a media source
- [x] `GetMediaSourceNumChannels` - Get the number of channels in a media source

### ✅ Extended Track Functions (2 methods)
- [x] `IsTrackVisible` - Check if a track is visible in TCP or MCP
- [x] `SetOnlyTrackSelected` - Set only one track selected, deselecting all others

### ✅ Utility Functions (2 methods)
- [x] `DB2SLIDER` - Convert dB value to slider value
- [x] `SLIDER2DB` - Convert slider value to dB value

### ✅ Envelope Extended (19 methods)
**Point Range Operations (4 methods):**
- [x] `DeleteEnvelopePointRange` - Delete envelope points in time range
- [x] `Envelope_SortPoints` - Sort envelope points by time
- [x] `DeleteEnvelopePointRangeEx` - Delete points in automation item
- [x] `Envelope_SortPointsEx` - Sort points in automation item

**Evaluation & Information (8 methods):**
- [x] `Envelope_Evaluate` - Evaluate envelope value at time
- [x] `Envelope_FormatValue` - Format envelope value for display
- [x] `GetEnvelopeInfo_Value` - Get envelope info parameter
- [x] `GetEnvelopeName` - Get envelope name
- [x] `GetEnvelopeScalingMode` - Get envelope scaling mode
- [x] `GetTrackEnvelopeByChunkName` - Get envelope by chunk name
- [x] `Envelope_GetParentTrack` - Get envelope's parent track
- [x] `Envelope_GetParentTake` - Get envelope's parent take

**State Management (4 methods):**
- [x] `GetEnvelopeStateChunk` - Get envelope state chunk
- [x] `GetSetEnvelopeInfo_String` - Get/set envelope string info
- [x] `GetSetEnvelopeState` - Get/set envelope state
- [x] `GetSetEnvelopeState2` - Get/set envelope state v2

**Scaling & Extended (3 methods):**
- [x] `ScaleFromEnvelopeMode` - Scale from envelope mode
- [x] `ScaleToEnvelopeMode` - Scale to envelope mode
- [x] `SetEnvelopePointEx` - Set envelope point extended

### ✅ Time/Tempo Extended (23 methods)
**Tempo/Time Signature Markers (6 methods):**
- [x] `AddTempoTimeSigMarker` - Add tempo/time signature marker
- [x] `CountTempoTimeSigMarkers` - Count tempo/time signature markers
- [x] `DeleteTempoTimeSigMarker` - Delete tempo/time signature marker
- [x] `EditTempoTimeSigMarker` - Edit tempo/time signature marker
- [x] `FindTempoTimeSigMarker` - Find tempo/time signature marker
- [x] `SetTempoTimeSigMarker` - Set tempo/time signature marker

**TimeMap2 Functions (6 methods):**
- [x] `TimeMap2_beatsToTime` - Convert beats to time
- [x] `TimeMap2_GetDividedBpmAtTime` - Get divided BPM at time
- [x] `TimeMap2_GetNextChangeTime` - Get next tempo change time
- [x] `TimeMap2_QNToTime` - Convert quarter notes to time
- [x] `TimeMap2_timeToBeats` - Convert time to beats
- [x] `TimeMap2_timeToQN` - Convert time to quarter notes

**TimeMap Functions (11 methods):**
- [x] `TimeMap_GetTimeSigAtTime` - Get time signature at time
- [x] `TimeMap_QNToTime` - Convert quarter notes to time
- [x] `TimeMap_QNToTime_abs` - Convert quarter notes to absolute time
- [x] `TimeMap_timeToQN` - Convert time to quarter notes
- [x] `TimeMap_timeToQN_abs` - Convert time to absolute quarter notes
- [x] `TimeMap_QNToMeasures` - Convert quarter notes to measures
- [x] `TimeMap_GetMeasureInfo` - Get measure info at time
- [x] `TimeMap_GetDividedBpmAtTime` - Get divided BPM at time
- [x] `TimeMap_curFrameRate` - Get current frame rate
- [x] `TimeMap_GetMetronomePattern` - Get metronome pattern
- [x] `GetTempoMatchPlayRate` - Get tempo match play rate

**Clear Functions (2 methods):**
- [x] `ClearAllRecArmed` - Clear all record armed tracks
- [x] `ClearPeakCache` - Clear peak cache

### ✅ Track Management Extended (11 methods)
**Track Information Extended (6 methods):**
- [x] `GetSetMediaTrackInfo_String` - Get/set track string parameter
- [x] `GetTrackEnvelopeByName` - Get track envelope by name
- [x] `GetTrackMIDILyrics` - Get track MIDI lyrics
- [x] `TrackList_AdjustWindows` - Adjust track list windows
- [x] `TrackList_UpdateAllExternalSurfaces` - Update external surfaces
- [x] `BypassFxAllTracks` - Bypass FX on all tracks

**Control Surface Track Operations (5 methods):**
- [x] `CSurf_NumTracks` - Get number of tracks for control surface
- [x] `CSurf_TrackFromID` - Get track from control surface ID
- [x] `CSurf_TrackToID` - Get control surface ID from track
- [x] `GetMixerScroll` - Get mixer scroll position
- [x] `SetMixerScroll` - Set mixer scroll position

## 🔮 Not Yet Implemented API Methods

Based on the ReaScript API documentation (https://www.reaper.fm/sdk/reascript/reascripthelp.html), here are additional methods that could be implemented.

### Summary of Missing Functions
- **Core API Functions**: ~10 functions (APIExists, APITest, etc.)
- **Audio Functions**: ~18 functions (Audio_Init, AudioAccessor functions, etc.)
- **Track Management Extended**: ~14 functions (control surface, extended info functions)
- **Media Item Extended**: ~11 functions (extended info, state management)
- **MIDI Extended**: ~17 functions (PPQ/time conversion, event management)
- **FX Extended**: ~85+ functions (comprehensive FX parameter control for tracks and takes)
- **Envelope Extended**: ~22 functions (advanced envelope manipulation)
- **Time/Tempo Extended**: ~28 functions (TimeMap functions, tempo markers)
- **Control Surface Functions**: ~48 functions (CSurf_* functions)
- **File I/O and Preferences**: ~400+ functions (including SWS extensions)
- **String/Utility Functions**: ~20 functions (string formatting, GUID operations)
- **Low-Level/Advanced Functions**: ~12 functions (plugin API, object state)

**Total Unimplemented**: ~664+ functions (including SWS extensions)

Note: Many functions marked as "partial impl exists" have basic implementations but may need extended functionality to match the full ReaScript API.

### Core API Functions
- [ ] `APITest` - Test API functionality
- [ ] `GetAppVersion` - Get REAPER version string (partial impl exists)
- [ ] `GetLastTouchedFX` - Get last touched FX
- [ ] `GetMasterMuteSoloFlags` - Get master mute/solo flags
- [ ] `PreventUIRefresh` - Prevent UI refresh temporarily
- [ ] `ReaScriptError` - Generate ReaScript error

### Audio Functions
- [ ] `Audio_Init` - Initialize audio system
- [ ] `Audio_IsPreBuffer` - Check if audio is pre-buffering
- [ ] `Audio_IsRunning` - Check if audio is running  
- [ ] `Audio_Quit` - Quit audio system
- [ ] `AudioAccessorStateChanged` - Check if audio accessor state changed
- [ ] `AudioAccessorUpdate` - Update audio accessor
- [ ] `AudioAccessorValidateState` - Validate audio accessor state
- [ ] `CalcMediaSrcLoudness` - Calculate media source loudness
- [ ] `CalculateNormalization` - Calculate normalization values
- [ ] `CreateTakeAudioAccessor` - Create take audio accessor (partial impl exists)
- [ ] `CreateTrackAudioAccessor` - Create track audio accessor (partial impl exists)
- [ ] `DestroyAudioAccessor` - Destroy audio accessor
- [ ] `GetAudioAccessorEndTime` - Get audio accessor end time
- [ ] `GetAudioAccessorHash` - Get audio accessor hash
- [ ] `GetAudioAccessorSamples` - Get audio accessor samples
- [ ] `GetAudioAccessorStartTime` - Get audio accessor start time

### Track Management Extended (Remaining)
- [ ] `GetTrackAutomationMode` - Get track automation mode (partial impl exists)

### Media Item Extended
- [ ] `GetMediaItemInfo_Value` - Get media item info value
- [ ] `GetMediaItemTake_Item` - Get item from take
- [ ] `GetMediaItemTake_Peaks` - Get take peak data
- [ ] `GetMediaItemTake_Source` - Get take source (partial impl exists)
- [ ] `GetMediaItemTake_Track` - Get track from take
- [ ] `GetSetItemState` - Get/set item state
- [ ] `GetSetItemState2` - Get/set item state v2
- [ ] `GetSetMediaItemInfo_String` - Get/set item info string
- [ ] `GetSetMediaItemTakeInfo_String` - Get/set take info string
- [ ] `SetMediaItemInfo_Value` - Set media item info value
- [ ] `SetMediaItemTake_Source` - Set take source (partial impl exists)

### MIDI Extended
- [ ] `MIDI_DisableSort` - Disable MIDI sorting
- [ ] `MIDI_GetEvt` - Get MIDI event
- [ ] `MIDI_GetGrid` - Get MIDI grid settings
- [ ] `MIDI_GetHash` - Get MIDI hash
- [ ] `MIDI_GetPPQPos_EndOfMeasure` - Get PPQ position end of measure
- [ ] `MIDI_GetPPQPos_StartOfMeasure` - Get PPQ position start of measure
- [ ] `MIDI_GetPPQPosFromProjQN` - Get PPQ position from project QN
- [ ] `MIDI_GetPPQPosFromProjTime` - Get PPQ position from project time
- [ ] `MIDI_GetProjQNFromPPQPos` - Get project QN from PPQ position
- [ ] `MIDI_GetProjTimeFromPPQPos` - Get project time from PPQ position
- [ ] `MIDI_GetRecentInputEvent` - Get recent MIDI input event
- [ ] `MIDI_GetTrackHash` - Get track MIDI hash
- [ ] `MIDI_InsertEvt` - Insert MIDI event
- [ ] `MIDI_InsertTextSysexEvt` - Insert text/sysex event
- [ ] `MIDI_SetEvt` - Set MIDI event
- [ ] `MIDI_SetItemExtents` - Set MIDI item extents
- [ ] `MIDI_Sort` - Sort MIDI events

### FX Extended
- [ ] `FxGetPresetName` - Get FX preset name
- [ ] `GetFocusedFX` - Get focused FX
- [ ] `GetFocusedFX2` - Get focused FX v2
- [ ] `GetLastTouchedFX` - Get last touched FX
- [ ] `TakeFX_AddByName` - Add take FX by name
- [ ] `TakeFX_CopyToTake` - Copy FX to take
- [ ] `TakeFX_CopyToTrack` - Copy FX to track
- [ ] `TakeFX_Delete` - Delete take FX
- [ ] `TakeFX_EndParamEdit` - End take FX param edit
- [ ] `TakeFX_FormatParamValue` - Format take FX param value
- [ ] `TakeFX_FormatParamValueNormalized` - Format normalized param value
- [ ] `TakeFX_GetChainVisible` - Get take FX chain visibility
- [ ] `TakeFX_GetCount` - Get take FX count
- [ ] `TakeFX_GetEnabled` - Get take FX enabled state
- [ ] `TakeFX_GetEnvelope` - Get take FX envelope
- [ ] `TakeFX_GetFXGUID` - Get take FX GUID
- [ ] `TakeFX_GetFXName` - Get take FX name
- [ ] `TakeFX_GetIOSize` - Get take FX IO size
- [ ] `TakeFX_GetNamedConfigParm` - Get take FX named config param
- [ ] `TakeFX_GetNumParams` - Get take FX parameter count
- [ ] `TakeFX_GetOffline` - Get take FX offline state
- [ ] `TakeFX_GetOpen` - Get take FX open state
- [ ] `TakeFX_GetParam` - Get take FX parameter
- [ ] `TakeFX_GetParameterStepSizes` - Get take FX parameter step sizes
- [ ] `TakeFX_GetParamEx` - Get take FX parameter extended
- [ ] `TakeFX_GetParamFromIdent` - Get take FX param from identifier
- [ ] `TakeFX_GetParamIdent` - Get take FX param identifier
- [ ] `TakeFX_GetParamName` - Get take FX param name
- [ ] `TakeFX_GetParamNormalized` - Get take FX normalized param
- [ ] `TakeFX_GetPinMappings` - Get take FX pin mappings
- [ ] `TakeFX_GetPreset` - Get take FX preset
- [ ] `TakeFX_GetPresetIndex` - Get take FX preset index
- [ ] `TakeFX_GetUserPresetFilename` - Get take FX user preset filename
- [ ] `TakeFX_NavigatePresets` - Navigate take FX presets
- [ ] `TakeFX_SetEnabled` - Set take FX enabled
- [ ] `TakeFX_SetNamedConfigParm` - Set take FX named config param
- [ ] `TakeFX_SetOffline` - Set take FX offline
- [ ] `TakeFX_SetOpen` - Set take FX open
- [ ] `TakeFX_SetParam` - Set take FX parameter
- [ ] `TakeFX_SetParamNormalized` - Set take FX normalized param
- [ ] `TakeFX_SetPinMappings` - Set take FX pin mappings
- [ ] `TakeFX_SetPreset` - Set take FX preset
- [ ] `TakeFX_SetPresetByIndex` - Set take FX preset by index
- [ ] `TakeFX_Show` - Show take FX window
- [ ] `TrackFX_CopyToTake` - Copy track FX to take
- [ ] `TrackFX_CopyToTrack` - Copy track FX to track
- [ ] `TrackFX_EndParamEdit` - End track FX param edit
- [ ] `TrackFX_FormatParamValue` - Format track FX param value
- [ ] `TrackFX_FormatParamValueNormalized` - Format normalized param value
- [ ] `TrackFX_GetByName` - Get track FX by name
- [ ] `TrackFX_GetChainVisible` - Get track FX chain visibility
- [ ] `TrackFX_GetEQ` - Get track EQ
- [ ] `TrackFX_GetEQBandEnabled` - Get EQ band enabled
- [ ] `TrackFX_GetEQParam` - Get EQ parameter
- [ ] `TrackFX_GetFloatingWindow` - Get floating FX window
- [ ] `TrackFX_GetFXGUID` - Get track FX GUID
- [ ] `TrackFX_GetIOSize` - Get track FX IO size
- [ ] `TrackFX_GetNamedConfigParm` - Get track FX named config param
- [ ] `TrackFX_GetNumParams` - Get track FX parameter count
- [ ] `TrackFX_GetOffline` - Get track FX offline state
- [ ] `TrackFX_GetOpen` - Get track FX open state
- [ ] `TrackFX_GetParameterStepSizes` - Get track FX parameter step sizes
- [ ] `TrackFX_GetParamEx` - Get track FX parameter extended
- [ ] `TrackFX_GetParamFromIdent` - Get track FX param from identifier
- [ ] `TrackFX_GetParamIdent` - Get track FX param identifier
- [ ] `TrackFX_GetParamName` - Get track FX param name
- [ ] `TrackFX_GetParamNormalized` - Get track FX normalized param
- [ ] `TrackFX_GetPinMappings` - Get track FX pin mappings
- [ ] `TrackFX_GetPreset` - Get track FX preset
- [ ] `TrackFX_GetPresetIndex` - Get track FX preset index
- [ ] `TrackFX_GetRecChainVisible` - Get record FX chain visibility
- [ ] `TrackFX_GetRecCount` - Get record FX count
- [ ] `TrackFX_GetUserPresetFilename` - Get track FX user preset filename
- [ ] `TrackFX_NavigatePresets` - Navigate track FX presets
- [ ] `TrackFX_SetEQBandEnabled` - Set EQ band enabled
- [ ] `TrackFX_SetEQParam` - Set EQ parameter
- [ ] `TrackFX_SetEnabled` - Set track FX enabled (partial impl exists)
- [ ] `TrackFX_SetNamedConfigParm` - Set track FX named config param
- [ ] `TrackFX_SetOffline` - Set track FX offline
- [ ] `TrackFX_SetOpen` - Set track FX open
- [ ] `TrackFX_SetParamNormalized` - Set track FX normalized param
- [ ] `TrackFX_SetPinMappings` - Set track FX pin mappings
- [ ] `TrackFX_SetPreset` - Set track FX preset
- [ ] `TrackFX_SetPresetByIndex` - Set track FX preset by index
- [ ] `TrackFX_Show` - Show track FX window


### Control Surface Functions
- [ ] `CSurf_FlushUndo` - Flush undo (partial impl exists)
- [ ] `CSurf_GetTouchState` - Get touch state
- [ ] `CSurf_GoEnd` - Go to end
- [ ] `CSurf_GoStart` - Go to start
- [ ] `CSurf_OnArrow` - Handle arrow key
- [ ] `CSurf_OnFwd` - Handle forward
- [ ] `CSurf_OnFXChange` - Handle FX change
- [ ] `CSurf_OnInputMonitorChange` - Handle input monitor change
- [ ] `CSurf_OnInputMonitorChangeEx` - Handle input monitor change extended
- [ ] `CSurf_OnMuteChange` - Handle mute change
- [ ] `CSurf_OnMuteChangeEx` - Handle mute change extended
- [ ] `CSurf_OnPanChange` - Handle pan change
- [ ] `CSurf_OnPanChangeEx` - Handle pan change extended
- [ ] `CSurf_OnPlayRateChange` - Handle play rate change
- [ ] `CSurf_OnRecArmChange` - Handle record arm change
- [ ] `CSurf_OnRecArmChangeEx` - Handle record arm change extended
- [ ] `CSurf_OnRecvPanChange` - Handle receive pan change
- [ ] `CSurf_OnRecvVolumeChange` - Handle receive volume change
- [ ] `CSurf_OnRew` - Handle rewind
- [ ] `CSurf_OnRewFwd` - Handle rewind/forward
- [ ] `CSurf_OnScroll` - Handle scroll
- [ ] `CSurf_OnSelectedChange` - Handle selection change
- [ ] `CSurf_OnSendPanChange` - Handle send pan change
- [ ] `CSurf_OnSendVolumeChange` - Handle send volume change
- [ ] `CSurf_OnSoloChange` - Handle solo change
- [ ] `CSurf_OnSoloChangeEx` - Handle solo change extended
- [ ] `CSurf_OnTempoChange` - Handle tempo change
- [ ] `CSurf_OnTrackSelection` - Handle track selection
- [ ] `CSurf_OnVolumeChange` - Handle volume change
- [ ] `CSurf_OnVolumeChangeEx` - Handle volume change extended
- [ ] `CSurf_OnWidthChange` - Handle width change
- [ ] `CSurf_OnWidthChangeEx` - Handle width change extended
- [ ] `CSurf_OnZoom` - Handle zoom
- [ ] `CSurf_ResetAllCachedVolPanStates` - Reset cached vol/pan states
- [ ] `CSurf_ScrubAmt` - Scrub amount
- [ ] `CSurf_SetAutoMode` - Set automation mode
- [ ] `CSurf_SetPlayState` - Set play state (partial impl exists)
- [ ] `CSurf_SetRepeatState` - Set repeat state (partial impl exists)
- [ ] `CSurf_SetSurfaceMute` - Set surface mute
- [ ] `CSurf_SetSurfacePan` - Set surface pan
- [ ] `CSurf_SetSurfaceRecArm` - Set surface record arm
- [ ] `CSurf_SetSurfaceSelected` - Set surface selected
- [ ] `CSurf_SetSurfaceSolo` - Set surface solo
- [ ] `CSurf_SetSurfaceVolume` - Set surface volume
- [ ] `CSurf_SetTrackListChange` - Set track list change

### File I/O and Preferences
- [ ] `BR_EnvAlloc` - Allocate envelope (SWS extension)
- [ ] `BR_EnvCountPoints` - Count envelope points (SWS extension)
- [ ] `BR_EnvDeletePoint` - Delete envelope point (SWS extension)
- [ ] `BR_EnvFind` - Find envelope (SWS extension)
- [ ] `BR_EnvFindNext` - Find next envelope (SWS extension)
- [ ] `BR_EnvFindPrevious` - Find previous envelope (SWS extension)
- [ ] `BR_EnvFree` - Free envelope (SWS extension)
- [ ] `BR_EnvGetParentTake` - Get envelope parent take (SWS extension)
- [ ] `BR_EnvGetParentTrack` - Get envelope parent track (SWS extension)
- [ ] `BR_EnvGetPoint` - Get envelope point (SWS extension)
- [ ] `BR_EnvGetProperties` - Get envelope properties (SWS extension)
- [ ] `BR_EnvSetPoint` - Set envelope point (SWS extension)
- [ ] `BR_EnvSetProperties` - Set envelope properties (SWS extension)
- [ ] `BR_EnvSortPoints` - Sort envelope points (SWS extension)
- [ ] `BR_EnvValueAtPos` - Get envelope value at position (SWS extension)
- [ ] `BR_GetMediaItemByGUID` - Get media item by GUID (SWS extension)
- [ ] `BR_GetMediaItemGUID` - Get media item GUID (SWS extension)
- [ ] `BR_GetMediaItemImageResource` - Get media item image resource (SWS extension)
- [ ] `BR_GetMediaItemTakeGUID` - Get media item take GUID (SWS extension)
- [ ] `BR_GetMediaSourceProperties` - Get media source properties (SWS extension)
- [ ] `BR_GetMediaTrackByGUID` - Get media track by GUID (SWS extension)
- [ ] `BR_GetMediaTrackGUID` - Get media track GUID (SWS extension)
- [ ] `BR_GetMediaTrackLayouts` - Get media track layouts (SWS extension)
- [ ] `BR_GetMediaTrackSendInfo_Envelope` - Get track send envelope (SWS extension)
- [ ] `BR_GetMediaTrackSendInfo_Track` - Get track send info (SWS extension)
- [ ] `BR_GetMidiNoteName` - Get MIDI note name (SWS extension)
- [ ] `BR_GetMidiNoteNameEx` - Get MIDI note name extended (SWS extension)
- [ ] `BR_GetMidiSourceLenPPQ` - Get MIDI source length in PPQ (SWS extension)
- [ ] `BR_GetMidiTakeByGUID` - Get MIDI take by GUID (SWS extension)
- [ ] `BR_GetMidiTakePoolGUID` - Get MIDI take pool GUID (SWS extension)
- [ ] `BR_GetMidiTakeTempoInfo` - Get MIDI take tempo info (SWS extension)
- [ ] `BR_GetMouseCursorContext` - Get mouse cursor context (SWS extension)
- [ ] `BR_GetMouseCursorContext_Envelope` - Get mouse cursor envelope (SWS extension)
- [ ] `BR_GetMouseCursorContext_Item` - Get mouse cursor item (SWS extension)
- [ ] `BR_GetMouseCursorContext_MIDI` - Get mouse cursor MIDI (SWS extension)
- [ ] `BR_GetMouseCursorContext_Position` - Get mouse cursor position (SWS extension)
- [ ] `BR_GetMouseCursorContext_StretchMarker` - Get mouse cursor stretch marker (SWS extension)
- [ ] `BR_GetMouseCursorContext_Take` - Get mouse cursor take (SWS extension)
- [ ] `BR_GetMouseCursorContext_Track` - Get mouse cursor track (SWS extension)
- [ ] `BR_GetNextGridDivision` - Get next grid division (SWS extension)
- [ ] `BR_GetPrevGridDivision` - Get previous grid division (SWS extension)
- [ ] `BR_GetSetTrackSendInfo` - Get/set track send info (SWS extension)
- [ ] `BR_GetTakeFXCount` - Get take FX count (SWS extension)
- [ ] `BR_IsTakeMidi` - Check if take is MIDI (SWS extension)
- [ ] `BR_ItemAtMouseCursor` - Get item at mouse cursor (SWS extension)
- [ ] `BR_MIDI_CCLaneRemove` - Remove MIDI CC lane (SWS extension)
- [ ] `BR_MIDI_CCLaneReplace` - Replace MIDI CC lane (SWS extension)
- [ ] `BR_PositionAtMouseCursor` - Get position at mouse cursor (SWS extension)
- [ ] `BR_SetArrangeView` - Set arrange view (SWS extension)
- [ ] `BR_SetItemEdges` - Set item edges (SWS extension)
- [ ] `BR_SetMediaItemImageResource` - Set media item image resource (SWS extension)
- [ ] `BR_SetMediaSourceProperties` - Set media source properties (SWS extension)
- [ ] `BR_SetMediaTrackLayouts` - Set media track layouts (SWS extension)
- [ ] `BR_SetMidiTakeTempoInfo` - Set MIDI take tempo info (SWS extension)
- [ ] `BR_SetTakeSourceFromFile` - Set take source from file (SWS extension)
- [ ] `BR_SetTakeSourceFromFile2` - Set take source from file v2 (SWS extension)
- [ ] `BR_TakeAtMouseCursor` - Get take at mouse cursor (SWS extension)
- [ ] `BR_TrackAtMouseCursor` - Get track at mouse cursor (SWS extension)
- [ ] `BR_TrackFX_GetFXModuleName` - Get track FX module name (SWS extension)
- [ ] `BR_Win32_CB_FindString` - Win32 combo box find string (SWS extension)
- [ ] `BR_Win32_CB_FindStringExact` - Win32 combo box find exact string (SWS extension)
- [ ] `BR_Win32_ClientToScreen` - Win32 client to screen (SWS extension)
- [ ] `BR_Win32_DrawText` - Win32 draw text (SWS extension)
- [ ] `BR_Win32_GET_INI_STRING` - Win32 get INI string (SWS extension)
- [ ] `BR_Win32_GetConstant` - Win32 get constant (SWS extension)
- [ ] `BR_Win32_GetCursorPos` - Win32 get cursor position (SWS extension)
- [ ] `BR_Win32_GetFocus` - Win32 get focus (SWS extension)
- [ ] `BR_Win32_GetForegroundWindow` - Win32 get foreground window (SWS extension)
- [ ] `BR_Win32_GetMainHwnd` - Win32 get main window (SWS extension)
- [ ] `BR_Win32_GetMixerHwnd` - Win32 get mixer window (SWS extension)
- [ ] `BR_Win32_GetMonitorRectFromPoint` - Win32 get monitor rect (SWS extension)
- [ ] `BR_Win32_GetParent` - Win32 get parent (SWS extension)
- [ ] `BR_Win32_GetPrivateProfileString` - Win32 get profile string (SWS extension)
- [ ] `BR_Win32_GetSystemMetrics` - Win32 get system metrics (SWS extension)
- [ ] `BR_Win32_GetWindow` - Win32 get window (SWS extension)
- [ ] `BR_Win32_GetWindowLong` - Win32 get window long (SWS extension)
- [ ] `BR_Win32_GetWindowLongPtr` - Win32 get window long pointer (SWS extension)
- [ ] `BR_Win32_GetWindowRect` - Win32 get window rect (SWS extension)
- [ ] `BR_Win32_GetWindowText` - Win32 get window text (SWS extension)
- [ ] `BR_Win32_HwndToString` - Win32 HWND to string (SWS extension)
- [ ] `BR_Win32_IsWindow` - Win32 is window (SWS extension)
- [ ] `BR_Win32_IsWindowVisible` - Win32 is window visible (SWS extension)
- [ ] `BR_Win32_LPARAM` - Win32 LPARAM (SWS extension)
- [ ] `BR_Win32_MIDIEditor_GetActive` - Win32 get active MIDI editor (SWS extension)
- [ ] `BR_Win32_ScreenToClient` - Win32 screen to client (SWS extension)
- [ ] `BR_Win32_SendMessage` - Win32 send message (SWS extension)
- [ ] `BR_Win32_SetFocus` - Win32 set focus (SWS extension)
- [ ] `BR_Win32_SetForegroundWindow` - Win32 set foreground window (SWS extension)
- [ ] `BR_Win32_SetWindowLong` - Win32 set window long (SWS extension)
- [ ] `BR_Win32_SetWindowLongPtr` - Win32 set window long pointer (SWS extension)
- [ ] `BR_Win32_SetWindowPos` - Win32 set window position (SWS extension)
- [ ] `BR_Win32_ShellExecute` - Win32 shell execute (SWS extension)
- [ ] `BR_Win32_ShowWindow` - Win32 show window (SWS extension)
- [ ] `BR_Win32_StringToHwnd` - Win32 string to HWND (SWS extension)
- [ ] `BR_Win32_WindowFromPoint` - Win32 window from point (SWS extension)
- [ ] `BR_Win32_WritePrivateProfileString` - Win32 write profile string (SWS extension)
- [ ] `ClearConsole` - Clear console (partial impl exists)
- [ ] `DeleteExtState` - Delete extended state
- [ ] `Dock_UpdateDockID` - Update dock ID
- [ ] `DockGetPosition` - Get dock position
- [ ] `DockIsChildOfDock` - Check if child of dock
- [ ] `DockWindowActivate` - Activate dock window
- [ ] `DockWindowAdd` - Add dock window (partial impl exists)
- [ ] `DockWindowAddEx` - Add dock window extended
- [ ] `DockWindowRefresh` - Refresh dock window
- [ ] `DockWindowRefreshForHWND` - Refresh dock window for HWND
- [ ] `DockWindowRemove` - Remove dock window
- [ ] `EnsureNotCompletelyOffscreen` - Ensure window not offscreen
- [ ] `EnumerateFiles` - Enumerate files
- [ ] `EnumerateSubdirectories` - Enumerate subdirectories
- [ ] `ExecProcess` - Execute process
- [ ] `file_exists` - Check if file exists
- [ ] `format_timestr` - Format time string
- [ ] `format_timestr_len` - Format time string with length
- [ ] `format_timestr_pos` - Format time string position
- [ ] `genGuid` - Generate GUID
- [ ] `get_config_var_string` - Get config variable string
- [ ] `get_ini_file` - Get INI file
- [ ] `get_midi_config_var` - Get MIDI config variable
- [ ] `GetActionShortcutDesc` - Get action shortcut description
- [ ] `GetActiveTake` - Get active take (partial impl exists)
- [ ] `GetAllProjectPlayStates` - Get all project play states
- [ ] `GetAppVersion` - Get app version (partial impl exists)
- [ ] `GetArmedCommand` - Get armed command
- [ ] `GetAudioAccessorHash` - Get audio accessor hash
- [ ] `GetColorTheme` - Get color theme
- [ ] `GetColorThemeStruct` - Get color theme struct
- [ ] `GetConfigWantsDock` - Get config wants dock
- [ ] `GetCurrentProjectInLoadSave` - Get current project in load/save
- [ ] `GetCursorContext` - Get cursor context (partial impl exists)
- [ ] `GetCursorContext2` - Get cursor context v2
- [ ] `GetCursorPosition` - Get cursor position (partial impl exists)
- [ ] `GetCursorPositionEx` - Get cursor position extended
- [ ] `GetDisplayedMediaItemColor` - Get displayed media item color
- [ ] `GetDisplayedMediaItemColor2` - Get displayed media item color v2
- [ ] `GetEnvelopeInfo_Value` - Get envelope info value
- [ ] `GetEnvelopeName` - Get envelope name
- [ ] `GetEnvelopeScalingMode` - Get envelope scaling mode
- [ ] `GetEnvelopeStateChunk` - Get envelope state chunk
- [ ] `GetExePath` - Get executable path (partial impl exists)
- [ ] `GetExtState` - Get extended state
- [ ] `GetFocusedFX` - Get focused FX
- [ ] `GetFocusedFX2` - Get focused FX v2
- [ ] `GetFreeDiskSpaceForRecordPath` - Get free disk space
- [ ] `GetFXEnvelope` - Get FX envelope
- [ ] `GetGlobalAutomationOverride` - Get global automation override
- [ ] `GetHZoomLevel` - Get horizontal zoom level
- [ ] `GetIconThemePointer` - Get icon theme pointer
- [ ] `GetIconThemePointerForDPI` - Get icon theme pointer for DPI
- [ ] `GetIconThemeStruct` - Get icon theme struct
- [ ] `GetInputActivityLevel` - Get input activity level
- [ ] `GetInputChannelName` - Get input channel name
- [ ] `GetInputOutputLatency` - Get input/output latency
- [ ] `GetItemEditingTime2` - Get item editing time v2
- [ ] `GetItemFromPoint` - Get item from point
- [ ] `GetItemProjectContext` - Get item project context
- [ ] `GetItemStateChunk` - Get item state chunk
- [ ] `GetLastMarkerAndCurRegion` - Get last marker and current region
- [ ] `GetLastTouchedFX` - Get last touched FX
- [ ] `GetMainHwnd` - Get main window handle (partial impl exists)
- [ ] `GetMasterMuteSoloFlags` - Get master mute/solo flags
- [ ] `GetMasterTrack` - Get master track (partial impl exists)
- [ ] `GetMasterTrackVisibility` - Get master track visibility
- [ ] `GetMaxMidiInputs` - Get max MIDI inputs
- [ ] `GetMaxMidiOutputs` - Get max MIDI outputs
- [ ] `GetMediaFileMetadata` - Get media file metadata
- [ ] `GetMediaItem` - Get media item (partial impl exists)
- [ ] `GetMediaItem_Track` - Get media item track (partial impl exists)
- [ ] `GetMediaItemInfo_Value` - Get media item info value
- [ ] `GetMediaItemNumTakes` - Get media item take count
- [ ] `GetMediaItemTake` - Get media item take
- [ ] `GetMediaItemTake_Item` - Get item from take
- [ ] `GetMediaItemTake_Peaks` - Get take peaks
- [ ] `GetMediaItemTake_Source` - Get take source (partial impl exists)
- [ ] `GetMediaItemTake_Track` - Get track from take
- [ ] `GetMediaItemTakeByGUID` - Get take by GUID
- [ ] `GetMediaItemTakeInfo_Value` - Get take info value
- [ ] `GetMediaItemTrack` - Get media item track (partial impl exists)
- [ ] `GetMediaSourceFileName` - Get media source filename (partial impl exists)
- [ ] `GetMediaSourceLength` - Get media source length (partial impl exists)
- [ ] `GetMediaSourceParent` - Get media source parent
- [ ] `GetMediaSourceType` - Get media source type (partial impl exists)
- [ ] `GetMediaTrackInfo_Value` - Get media track info value
- [ ] `GetMIDIInputName` - Get MIDI input name (partial impl exists)
- [ ] `GetMIDIOutputName` - Get MIDI output name (partial impl exists)
- [ ] `GetMouseModifier` - Get mouse modifier
- [ ] `GetMousePosition` - Get mouse position (partial impl exists)
- [ ] `GetNumAudioInputs` - Get number of audio inputs
- [ ] `GetNumAudioOutputs` - Get number of audio outputs
- [ ] `GetNumMIDIInputs` - Get number of MIDI inputs (partial impl exists)
- [ ] `GetNumMIDIOutputs` - Get number of MIDI outputs (partial impl exists)
- [ ] `GetNumTakeMarkers` - Get number of take markers
- [ ] `GetNumTracks` - Get number of tracks
- [ ] `GetOS` - Get operating system
- [ ] `GetOutputChannelName` - Get output channel name
- [ ] `GetOutputLatency` - Get output latency
- [ ] `GetParentTrack` - Get parent track (partial impl exists)
- [ ] `GetPeakFileName` - Get peak filename
- [ ] `GetPeakFileNameEx` - Get peak filename extended
- [ ] `GetPeakFileNameEx2` - Get peak filename extended v2
- [ ] `GetPeaksBitmap` - Get peaks bitmap
- [ ] `GetPlayPosition` - Get play position
- [ ] `GetPlayPosition2` - Get play position v2
- [ ] `GetPlayPosition2Ex` - Get play position v2 extended
- [ ] `GetPlayPositionEx` - Get play position extended
- [ ] `GetPlayState` - Get play state (partial impl exists)
- [ ] `GetPlayStateEx` - Get play state extended
- [ ] `GetProjectBPM` - Get project BPM (partial impl exists)
- [ ] `GetProjectFileCount` - Get project file count
- [ ] `GetProjectItem` - Get project item
- [ ] `GetProjectName` - Get project name (partial impl exists)
- [ ] `GetProjectPath` - Get project path (partial impl exists)
- [ ] `GetProjectPathEx` - Get project path extended
- [ ] `GetProjectStateChangeCount` - Get project state change count (partial impl exists)
- [ ] `GetProjectTimeOffset` - Get project time offset
- [ ] `GetProjectTimeSignature` - Get project time signature
- [ ] `GetProjectTimeSignature2` - Get project time signature v2
- [ ] `GetProjExtState` - Get project extended state
- [ ] `GetReaperPrefs` - Get REAPER preferences
- [ ] `GetResourcePath` - Get resource path (partial impl exists)
- [ ] `GetSelectedEnvelope` - Get selected envelope
- [ ] `GetSelectedMediaItem` - Get selected media item (partial impl exists)
- [ ] `GetSelectedTrack` - Get selected track (partial impl exists)
- [ ] `GetSelectedTrack2` - Get selected track v2
- [ ] `GetSelectedTrackEnvelope` - Get selected track envelope
- [ ] `GetSet_ArrangeView2` - Get/set arrange view v2
- [ ] `GetSet_LoopTimeRange` - Get/set loop time range (partial impl exists)
- [ ] `GetSet_LoopTimeRange2` - Get/set loop time range v2
- [ ] `GetSetAutomationItemInfo` - Get/set automation item info (partial impl exists)
- [ ] `GetSetAutomationItemInfo_String` - Get/set automation item info string
- [ ] `GetSetEnvelopeInfo_String` - Get/set envelope info string
- [ ] `GetSetEnvelopeState` - Get/set envelope state
- [ ] `GetSetEnvelopeState2` - Get/set envelope state v2
- [ ] `GetSetItemState` - Get/set item state
- [ ] `GetSetItemState2` - Get/set item state v2
- [ ] `GetSetMediaItemInfo_String` - Get/set media item info string
- [ ] `GetSetMediaItemTakeInfo_String` - Get/set take info string
- [ ] `GetSetMediaTrackInfo_String` - Get/set track info string
- [ ] `GetSetObjectState` - Get/set object state
- [ ] `GetSetObjectState2` - Get/set object state v2
- [ ] `GetSetProjectAuthor` - Get/set project author
- [ ] `GetSetProjectGrid` - Get/set project grid
- [ ] `GetSetProjectInfo` - Get/set project info
- [ ] `GetSetProjectInfo_String` - Get/set project info string
- [ ] `GetSetProjectNotes` - Get/set project notes
- [ ] `GetSetRepeat` - Get/set repeat
- [ ] `GetSetRepeatEx` - Get/set repeat extended
- [ ] `GetSetTrackGroupMembership` - Get/set track group membership
- [ ] `GetSetTrackGroupMembershipHigh` - Get/set track group membership high
- [ ] `GetSetTrackMIDISupportFile` - Get/set track MIDI support file
- [ ] `GetSetTrackSendInfo` - Get/set track send info
- [ ] `GetSetTrackSendInfo_String` - Get/set track send info string
- [ ] `GetSetTrackState` - Get/set track state
- [ ] `GetSetTrackState2` - Get/set track state v2
- [ ] `GetSubProjectFromSource` - Get sub-project from source
- [ ] `GetTake` - Get take (partial impl exists)
- [ ] `GetTakeEnvelope` - Get take envelope
- [ ] `GetTakeEnvelopeByName` - Get take envelope by name
- [ ] `GetTakeMarker` - Get take marker
- [ ] `GetTakeName` - Get take name (partial impl exists)
- [ ] `GetTakeNumStretchMarkers` - Get take stretch marker count
- [ ] `GetTakeStretchMarker` - Get take stretch marker
- [ ] `GetTakeStretchMarkerSlope` - Get take stretch marker slope
- [ ] `GetTCPFXParm` - Get TCP FX parameter
- [ ] `GetTempoMatchPlayRate` - Get tempo match play rate
- [ ] `GetThemeColor` - Get theme color
- [ ] `GetThingFromPoint` - Get thing from point
- [ ] `GetToggleCommandState2` - Get toggle command state v2
- [ ] `GetToggleCommandStateEx` - Get toggle command state extended
- [ ] `GetToggleCommandStateThroughHooks` - Get toggle command state through hooks
- [ ] `GetTooltipWindow` - Get tooltip window
- [ ] `GetTrack` - Get track (partial impl exists)
- [ ] `GetTrackAutomationMode` - Get track automation mode (partial impl exists)
- [ ] `GetTrackColor` - Get track color (partial impl exists)
- [ ] `GetTrackDepth` - Get track depth (partial impl exists)
- [ ] `GetTrackEnvelope` - Get track envelope (partial impl exists)
- [ ] `GetTrackEnvelopeByChunkName` - Get track envelope by chunk name
- [ ] `GetTrackEnvelopeByName` - Get track envelope by name
- [ ] `GetTrackFromPoint` - Get track from point
- [ ] `GetTrackFromUID` - Get track from UID
- [ ] `GetTrackGUID` - Get track GUID (partial impl exists)
- [ ] `GetTrackInfo` - Get track info
- [ ] `GetTrackMediaItem` - Get track media item
- [ ] `GetTrackMIDILyrics` - Get track MIDI lyrics
- [ ] `GetTrackMIDINoteNameEx` - Get track MIDI note name extended
- [ ] `GetTrackMIDINoteRange` - Get track MIDI note range
- [ ] `GetTrackName` - Get track name (partial impl exists)
- [ ] `GetTrackNumMediaItems` - Get track media item count
- [ ] `GetTrackNumSends` - Get track send count (partial impl exists)
- [ ] `GetTrackReceiveName` - Get track receive name
- [ ] `GetTrackReceiveUIMute` - Get track receive UI mute
- [ ] `GetTrackReceiveUIVolPan` - Get track receive UI vol/pan
- [ ] `GetTrackSendInfo_Value` - Get track send info value
- [ ] `GetTrackSendName` - Get track send name
- [ ] `GetTrackSendUIMute` - Get track send UI mute
- [ ] `GetTrackSendUIVolPan` - Get track send UI vol/pan
- [ ] `GetTrackState` - Get track state
- [ ] `GetTrackStateChunk` - Get track state chunk (partial impl exists)
- [ ] `GetTrackUID` - Get track UID
- [ ] `GetTrackUIVolPan` - Get track UI vol/pan
- [ ] `GetUnderrunTime` - Get underrun time
- [ ] `GetUserFileNameForRead` - Get user filename for read
- [ ] `GetUserInputs` - Get user inputs
- [ ] `GoToMarker` - Go to marker (partial impl exists)
- [ ] `GoToRegion` - Go to region
- [ ] `GR_SelectColor` - Select color
- [ ] `GSC_mainwnd` - Get main window
- [ ] `guidToString` - GUID to string
- [ ] `HasExtState` - Has extended state
- [ ] `HasTrackMIDIPrograms` - Has track MIDI programs
- [ ] `HasTrackMIDIProgramsEx` - Has track MIDI programs extended
- [ ] `Help_Set` - Set help
- [ ] `HiresPeaksFromSource` - Hires peaks from source
- [ ] `InsertAutomationItem` - Insert automation item
- [ ] `InsertEnvelopePoint` - Insert envelope point (partial impl exists)
- [ ] `InsertEnvelopePointEx` - Insert envelope point extended
- [ ] `InsertMedia` - Insert media
- [ ] `InsertMediaSection` - Insert media section
- [ ] `InsertTrackAtIndex` - Insert track at index (partial impl exists)
- [ ] `IsItemTakeActiveForPlayback` - Is item take active for playback
- [ ] `IsMediaExtension` - Is media extension
- [ ] `IsMediaItemSelected` - Is media item selected
- [ ] `IsProjectDirty` - Is project dirty (partial impl exists)
- [ ] `IsREAPER` - Is REAPER
- [ ] `IsTrackSelected` - Is track selected
- [ ] `IsTrackVisible` - Is track visible
- [ ] `joystick_create` - Create joystick
- [ ] `joystick_destroy` - Destroy joystick
- [ ] `joystick_enum` - Enumerate joysticks
- [ ] `joystick_getaxis` - Get joystick axis
- [ ] `joystick_getbuttonmask` - Get joystick button mask
- [ ] `joystick_getinfo` - Get joystick info
- [ ] `joystick_getpov` - Get joystick POV
- [ ] `joystick_update` - Update joystick
- [ ] `LICE_ClipLine` - LICE clip line
- [ ] `Loop_OnArrow` - Loop on arrow
- [ ] `Main_OnCommand` - Main on command (partial impl exists)
- [ ] `Main_OnCommandEx` - Main on command extended
- [ ] `Main_openProject` - Open project (partial impl exists)
- [ ] `Main_SaveProject` - Save project (partial impl exists)
- [ ] `Main_SaveProjectEx` - Save project extended
- [ ] `Main_UpdateLoopInfo` - Update loop info
- [ ] `MarkTrackItemsDirty` - Mark track items dirty
- [ ] `Master_GetPlayRate` - Get master play rate
- [ ] `Master_GetPlayRateAtTime` - Get master play rate at time
- [ ] `Master_GetTempo` - Get master tempo
- [ ] `Master_NormalizePlayRate` - Normalize master play rate
- [ ] `Master_NormalizeTempo` - Normalize master tempo
- [ ] `MB` - Message box
- [ ] `MediaItemDescendsFromTrack` - Media item descends from track
- [ ] `MIDI_CountEvts` - Count MIDI events (partial impl exists)
- [ ] `MIDI_DeleteCC` - Delete MIDI CC (partial impl exists)
- [ ] `MIDI_DeleteEvt` - Delete MIDI event
- [ ] `MIDI_DeleteNote` - Delete MIDI note (partial impl exists)
- [ ] `MIDI_DeleteTextSysexEvt` - Delete text/sysex event
- [ ] `MIDI_DisableSort` - Disable MIDI sort
- [ ] `MIDI_EnumSelCC` - Enumerate selected CC
- [ ] `MIDI_EnumSelEvts` - Enumerate selected events
- [ ] `MIDI_EnumSelNotes` - Enumerate selected notes (partial impl exists)
- [ ] `MIDI_EnumSelTextSysexEvts` - Enumerate selected text/sysex
- [ ] `MIDI_eventlist_Create` - Create MIDI event list
- [ ] `MIDI_eventlist_Destroy` - Destroy MIDI event list
- [ ] `MIDI_GetAllEvts` - Get all MIDI events (partial impl exists)
- [ ] `MIDI_GetCC` - Get MIDI CC (partial impl exists)
- [ ] `MIDI_GetCCShape` - Get MIDI CC shape
- [ ] `MIDI_GetEvt` - Get MIDI event
- [ ] `MIDI_GetGrid` - Get MIDI grid
- [ ] `MIDI_GetHash` - Get MIDI hash
- [ ] `MIDI_GetNote` - Get MIDI note (partial impl exists)
- [ ] `MIDI_GetPPQPos_EndOfMeasure` - Get PPQ position end of measure
- [ ] `MIDI_GetPPQPos_StartOfMeasure` - Get PPQ position start of measure
- [ ] `MIDI_GetPPQPosFromProjQN` - Get PPQ position from project QN
- [ ] `MIDI_GetPPQPosFromProjTime` - Get PPQ position from project time
- [ ] `MIDI_GetProjQNFromPPQPos` - Get project QN from PPQ position
- [ ] `MIDI_GetProjTimeFromPPQPos` - Get project time from PPQ position
- [ ] `MIDI_GetRecentInputEvent` - Get recent MIDI input event
- [ ] `MIDI_GetScale` - Get MIDI scale (partial impl exists)
- [ ] `MIDI_GetTextSysexEvt` - Get text/sysex event (partial impl exists)
- [ ] `MIDI_GetTrackHash` - Get track MIDI hash
- [ ] `MIDI_InsertCC` - Insert MIDI CC (partial impl exists)
- [ ] `MIDI_InsertEvt` - Insert MIDI event
- [ ] `MIDI_InsertNote` - Insert MIDI note (partial impl exists)
- [ ] `MIDI_InsertTextSysexEvt` - Insert text/sysex event
- [ ] `MIDI_RefreshEventList` - Refresh MIDI event list
- [ ] `MIDI_SelectAll` - Select all MIDI (partial impl exists)
- [ ] `MIDI_SetAllEvts` - Set all MIDI events (partial impl exists)
- [ ] `MIDI_SetCC` - Set MIDI CC (partial impl exists)
- [ ] `MIDI_SetCCShape` - Set MIDI CC shape
- [ ] `MIDI_SetEvt` - Set MIDI event
- [ ] `MIDI_SetItemExtents` - Set MIDI item extents
- [ ] `MIDI_SetNote` - Set MIDI note (partial impl exists)
- [ ] `MIDI_SetTextSysexEvt` - Set text/sysex event (partial impl exists)
- [ ] `MIDI_Sort` - Sort MIDI
- [ ] `MIDIEditor_EnumTakes` - Enumerate MIDI editor takes
- [ ] `MIDIEditor_GetActive` - Get active MIDI editor
- [ ] `MIDIEditor_GetMode` - Get MIDI editor mode
- [ ] `MIDIEditor_GetSetting_int` - Get MIDI editor setting int
- [ ] `MIDIEditor_GetSetting_str` - Get MIDI editor setting string
- [ ] `MIDIEditor_GetTake` - Get MIDI editor take
- [ ] `MIDIEditor_LastFocused_OnCommand` - Last focused MIDI editor command
- [ ] `MIDIEditor_OnCommand` - MIDI editor command
- [ ] `MIDIEditor_SetSetting_int` - Set MIDI editor setting int
- [ ] `mkpanstr` - Make pan string
- [ ] `mkvolpanstr` - Make volume/pan string
- [ ] `mkvolstr` - Make volume string
- [ ] `MoveEditCursor` - Move edit cursor
- [ ] `MoveMediaItemToTrack` - Move media item to track
- [ ] `MuteAllTracks` - Mute all tracks
- [ ] `my_getViewport` - Get viewport
- [ ] `NamedCommandLookup` - Named command lookup
- [ ] `OnPauseButton` - On pause button
- [ ] `OnPauseButtonEx` - On pause button extended
- [ ] `OnPlayButton` - On play button
- [ ] `OnPlayButtonEx` - On play button extended
- [ ] `OnStopButton` - On stop button
- [ ] `OnStopButtonEx` - On stop button extended
- [ ] `OpenColorThemeFile` - Open color theme file
- [ ] `OpenMediaExplorer` - Open media explorer
- [ ] `OscLocalMessageToHost` - OSC local message to host
- [ ] `parse_timestr` - Parse time string
- [ ] `parse_timestr_len` - Parse time string with length
- [ ] `parse_timestr_pos` - Parse time string position
- [ ] `parsepanstr` - Parse pan string
- [ ] `PCM_Sink_Create` - Create PCM sink
- [ ] `PCM_Sink_CreateEx` - Create PCM sink extended
- [ ] `PCM_Sink_CreateMIDIFile` - Create MIDI file sink
- [ ] `PCM_Sink_CreateMIDIFileEx` - Create MIDI file sink extended
- [ ] `PCM_Sink_Enum` - Enumerate PCM sinks
- [ ] `PCM_Sink_GetExtension` - Get PCM sink extension
- [ ] `PCM_Sink_ShowConfig` - Show PCM sink config
- [ ] `PCM_Source_BuildPeaks` - Build PCM source peaks
- [ ] `PCM_Source_CreateFromFile` - Create PCM source from file (partial impl exists)
- [ ] `PCM_Source_CreateFromFileEx` - Create PCM source from file extended
- [ ] `PCM_Source_CreateFromType` - Create PCM source from type
- [ ] `PCM_Source_Destroy` - Destroy PCM source
- [ ] `PCM_Source_GetPeaks` - Get PCM source peaks
- [ ] `PCM_Source_GetSectionInfo` - Get PCM source section info
- [ ] `PeakBuild_Create` - Create peak build
- [ ] `PeakBuild_CreateEx` - Create peak build extended
- [ ] `PeakGet_Create` - Create peak get
- [ ] `PeakGet_CreateEx` - Create peak get extended
- [ ] `PitchShiftSubModeMenu` - Pitch shift sub-mode menu
- [ ] `PlayPreview` - Play preview
- [ ] `PlayPreviewEx` - Play preview extended
- [ ] `PlayTrackPreview` - Play track preview
- [ ] `PlayTrackPreview2` - Play track preview v2
- [ ] `PlayTrackPreview2Ex` - Play track preview v2 extended
- [ ] `PlayTrackPreviewEx` - Play track preview extended
- [ ] `plugin_getapi` - Get plugin API
- [ ] `plugin_getFilterList` - Get plugin filter list
- [ ] `plugin_getImportableProjectFilterList` - Get importable project filter list
- [ ] `plugin_register` - Register plugin
- [ ] `PluginWantsAlwaysRunFx` - Plugin wants always run FX
- [ ] `PreventUIRefresh` - Prevent UI refresh
- [ ] `PromptForAction` - Prompt for action
- [ ] `ReaImGui_Attach` - ReaImGui attach
- [ ] `ReaImGui_CreateContext` - ReaImGui create context
- [ ] `ReaImGui_Detach` - ReaImGui detach
- [ ] `ReaImGui_GetContext` - ReaImGui get context
- [ ] `ReaImGui_GetVersion` - ReaImGui get version
- [ ] `ReaMote_GetLatency` - ReaMote get latency
- [ ] `ReaMote_OnCommand` - ReaMote on command
- [ ] `ReaperGetPitchShiftAPI` - Get pitch shift API
- [ ] `ReaScriptError` - ReaScript error
- [ ] `RecursiveCreateDirectory` - Recursively create directory (partial impl exists)
- [ ] `reduce_open_files` - Reduce open files
- [ ] `RefreshToolbar` - Refresh toolbar
- [ ] `RefreshToolbar2` - Refresh toolbar v2
- [ ] `relative_fn` - Relative filename
- [ ] `RemoveTrackSend` - Remove track send (partial impl exists)
- [ ] `RenderFileSection` - Render file section
- [ ] `ReorderSelectedTracks` - Reorder selected tracks
- [ ] `Resample_EnumModes` - Enumerate resample modes
- [ ] `Resampler_Create` - Create resampler
- [ ] `resolve_fn` - Resolve filename
- [ ] `resolve_fn2` - Resolve filename v2
- [ ] `ReverseNamedCommandLookup` - Reverse named command lookup
- [ ] `ScaleFromEnvelopeMode` - Scale from envelope mode
- [ ] `ScaleToEnvelopeMode` - Scale to envelope mode
- [ ] `screenset_register` - Register screenset
- [ ] `screenset_registerNew` - Register new screenset
- [ ] `screenset_unregister` - Unregister screenset
- [ ] `screenset_unregisterByParam` - Unregister screenset by param
- [ ] `screenset_update` - Update screenset
- [ ] `screenset_updateNew` - Update new screenset
- [ ] `screenset_updateStringID` - Update screenset string ID
- [ ] `SelectAllMediaItems` - Select all media items (partial impl exists)
- [ ] `SelectProjectInstance` - Select project instance (partial impl exists)
- [ ] `SendMIDIMessageToHardware` - Send MIDI message to hardware
- [ ] `SendUnifiedNotification` - Send unified notification
- [ ] `SetActiveTake` - Set active take (partial impl exists)
- [ ] `SetAutomationMode` - Set automation mode
- [ ] `SetCurrentBPM` - Set current BPM
- [ ] `SetCursorContext` - Set cursor context
- [ ] `SetEditCurPos` - Set edit cursor position (partial impl exists)
- [ ] `SetEditCurPos2` - Set edit cursor position v2
- [ ] `SetEnvelopePoint` - Set envelope point (partial impl exists)
- [ ] `SetEnvelopePointEx` - Set envelope point extended
- [ ] `SetEnvelopeStateChunk` - Set envelope state chunk
- [ ] `SetExtState` - Set extended state
- [ ] `SetGlobalAutomationOverride` - Set global automation override
- [ ] `SetItemStateChunk` - Set item state chunk
- [ ] `SetMasterTrackVisibility` - Set master track visibility
- [ ] `SetMediaItemInfo_Value` - Set media item info value
- [ ] `SetMediaItemLength` - Set media item length (partial impl exists)
- [ ] `SetMediaItemPosition` - Set media item position (partial impl exists)
- [ ] `SetMediaItemSelected` - Set media item selected (partial impl exists)
- [ ] `SetMediaItemTake_Source` - Set take source (partial impl exists)
- [ ] `SetMediaItemTakeInfo_Value` - Set take info value
- [ ] `SetMediaTrackInfo_Value` - Set media track info value
- [ ] `SetMIDIEditorGrid` - Set MIDI editor grid
- [ ] `SetMouseModifier` - Set mouse modifier
- [ ] `SetOnlyTrackSelected` - Set only track selected
- [ ] `SetProjectBPM` - Set project BPM (partial impl exists)
- [ ] `SetProjectGrid` - Set project grid
- [ ] `SetProjectMarker` - Set project marker
- [ ] `SetProjectMarker2` - Set project marker v2
- [ ] `SetProjectMarker3` - Set project marker v3
- [ ] `SetProjectMarker4` - Set project marker v4
- [ ] `SetProjectMarkerByIndex` - Set project marker by index
- [ ] `SetProjectMarkerByIndex2` - Set project marker by index v2
- [ ] `SetProjExtState` - Set project extended state
- [ ] `SetRegionRenderMatrix` - Set region render matrix
- [ ] `SetRenderLastError` - Set render last error
- [ ] `SetTakeMarker` - Set take marker
- [ ] `SetTakeName` - Set take name (partial impl exists)
- [ ] `SetTakeStretchMarker` - Set take stretch marker
- [ ] `SetTakeStretchMarkerSlope` - Set take stretch marker slope
- [ ] `SetTempoTimeSigMarker` - Set tempo/time signature marker
- [ ] `SetThemeColor` - Set theme color
- [ ] `SetToggleCommandState` - Set toggle command state
- [ ] `SetTrackAutomationMode` - Set track automation mode (partial impl exists)
- [ ] `SetTrackColor` - Set track color (partial impl exists)
- [ ] `SetTrackFolderCompactState` - Set track folder compact state (partial impl exists)
- [ ] `SetTrackFolderState` - Set track folder state (partial impl exists)
- [ ] `SetTrackMIDILyrics` - Set track MIDI lyrics
- [ ] `SetTrackMIDINoteName` - Set track MIDI note name
- [ ] `SetTrackMIDINoteNameEx` - Set track MIDI note name extended
- [ ] `SetTrackMute` - Set track mute (partial impl exists)
- [ ] `SetTrackName` - Set track name (partial impl exists)
- [ ] `SetTrackPan` - Set track pan (partial impl exists)
- [ ] `SetTrackRecordArm` - Set track record arm (partial impl exists)
- [ ] `SetTrackRecordInput` - Set track record input (partial impl exists)
- [ ] `SetTrackRecordMode` - Set track record mode (partial impl exists)
- [ ] `SetTrackSelected` - Set track selected (partial impl exists)
- [ ] `SetTrackSendInfo_Value` - Set track send info value
- [ ] `SetTrackSendUIPan` - Set track send UI pan
- [ ] `SetTrackSendUIVol` - Set track send UI volume
- [ ] `SetTrackSolo` - Set track solo (partial impl exists)
- [ ] `SetTrackStateChunk` - Set track state chunk (partial impl exists)
- [ ] `SetTrackUIInputMonitor` - Set track UI input monitor
- [ ] `SetTrackUIMute` - Set track UI mute
- [ ] `SetTrackUIPan` - Set track UI pan
- [ ] `SetTrackUIPolarity` - Set track UI polarity
- [ ] `SetTrackUIRecArm` - Set track UI record arm
- [ ] `SetTrackUISolo` - Set track UI solo
- [ ] `SetTrackUIVolume` - Set track UI volume
- [ ] `SetTrackUIWidth` - Set track UI width
- [ ] `SetTrackVolume` - Set track volume (partial impl exists)
- [ ] `ShowActionList` - Show action list
- [ ] `ShowConsoleMsg` - Show console message (partial impl exists)
- [ ] `ShowMessageBox` - Show message box (partial impl exists)
- [ ] `ShowPopupMenu` - Show popup menu
- [ ] `SLIDER2DB` - Slider to dB
- [ ] `SnapToGrid` - Snap to grid
- [ ] `SoloAllTracks` - Solo all tracks
- [ ] `Splash_GetWnd` - Get splash window
- [ ] `SplitMediaItem` - Split media item (partial impl exists)
- [ ] `StopPreview` - Stop preview
- [ ] `StopTrackPreview` - Stop track preview
- [ ] `stringToGuid` - String to GUID
- [ ] `StuffMIDIMessage` - Stuff MIDI message
- [ ] `TakeFX_AddByName` - Add take FX by name
- [ ] `TakeFX_CopyToTake` - Copy FX to take
- [ ] `TakeFX_CopyToTrack` - Copy FX to track
- [ ] `TakeFX_Delete` - Delete take FX
- [ ] `TakeFX_EndParamEdit` - End take FX param edit
- [ ] `TakeFX_FormatParamValue` - Format take FX param value
- [ ] `TakeFX_FormatParamValueNormalized` - Format normalized param value
- [ ] `TakeFX_GetChainVisible` - Get take FX chain visibility
- [ ] `TakeFX_GetCount` - Get take FX count
- [ ] `TakeFX_GetEnabled` - Get take FX enabled state
- [ ] `TakeFX_GetEnvelope` - Get take FX envelope
- [ ] `TakeFX_GetFXGUID` - Get take FX GUID
- [ ] `TakeFX_GetFXName` - Get take FX name
- [ ] `TakeFX_GetIOSize` - Get take FX IO size
- [ ] `TakeFX_GetNamedConfigParm` - Get take FX named config param
- [ ] `TakeFX_GetNumParams` - Get take FX parameter count
- [ ] `TakeFX_GetOffline` - Get take FX offline state
- [ ] `TakeFX_GetOpen` - Get take FX open state
- [ ] `TakeFX_GetParam` - Get take FX parameter
- [ ] `TakeFX_GetParameterStepSizes` - Get take FX parameter step sizes
- [ ] `TakeFX_GetParamEx` - Get take FX parameter extended
- [ ] `TakeFX_GetParamFromIdent` - Get take FX param from identifier
- [ ] `TakeFX_GetParamIdent` - Get take FX param identifier
- [ ] `TakeFX_GetParamName` - Get take FX param name
- [ ] `TakeFX_GetParamNormalized` - Get take FX normalized param
- [ ] `TakeFX_GetPinMappings` - Get take FX pin mappings
- [ ] `TakeFX_GetPreset` - Get take FX preset
- [ ] `TakeFX_GetPresetIndex` - Get take FX preset index
- [ ] `TakeFX_GetUserPresetFilename` - Get take FX user preset filename
- [ ] `TakeFX_NavigatePresets` - Navigate take FX presets
- [ ] `TakeFX_SetEnabled` - Set take FX enabled
- [ ] `TakeFX_SetNamedConfigParm` - Set take FX named config param
- [ ] `TakeFX_SetOffline` - Set take FX offline
- [ ] `TakeFX_SetOpen` - Set take FX open
- [ ] `TakeFX_SetParam` - Set take FX parameter
- [ ] `TakeFX_SetParamNormalized` - Set take FX normalized param
- [ ] `TakeFX_SetPinMappings` - Set take FX pin mappings
- [ ] `TakeFX_SetPreset` - Set take FX preset
- [ ] `TakeFX_SetPresetByIndex` - Set take FX preset by index
- [ ] `TakeFX_Show` - Show take FX window
- [ ] `TakeIsMIDI` - Take is MIDI
- [ ] `ThemeLayout_GetLayout` - Get theme layout
- [ ] `ThemeLayout_GetParameter` - Get theme layout parameter
- [ ] `ThemeLayout_RefreshAll` - Refresh all theme layouts
- [ ] `ThemeLayout_SetLayout` - Set theme layout
- [ ] `ThemeLayout_SetParameter` - Set theme layout parameter
- [ ] `time_precise` - Precise time
- [ ] `TimeMap2_beatsToTime` - Convert beats to time
- [ ] `TimeMap2_GetDividedBpmAtTime` - Get divided BPM at time
- [ ] `TimeMap2_GetNextChangeTime` - Get next tempo change time
- [ ] `TimeMap2_timeToBeats` - Convert time to beats
- [ ] `TimeMap_curFrameRate` - Get current frame rate
- [ ] `TimeMap_GetDividedBpmAtTime` - Get divided BPM at time
- [ ] `TimeMap_GetMetronomePattern` - Get metronome pattern
- [ ] `TimeMap_GetTimeSigAtTime` - Get time signature at time (partial impl exists)
- [ ] `TimeMap_QNToMeasures` - Convert QN to measures
- [ ] `TimeMap_QNToTime` - Convert QN to time (partial impl exists)
- [ ] `TimeMap_QNToTime_abs` - Convert QN to absolute time
- [ ] `TimeMap_timeToQN` - Convert time to QN
- [ ] `TimeMap_timeToQN_abs` - Convert time to absolute QN
- [ ] `ToggleTrackSendUIMute` - Toggle track send UI mute
- [ ] `Track_GetPeakInfo` - Get track peak info (partial impl exists)
- [ ] `Track_GetPeakHoldDB` - Get track peak hold dB
- [ ] `TrackCtl_SetToolTip` - Set track control tooltip
- [ ] `TrackFX_AddByName` - Add track FX by name (partial impl exists)
- [ ] `TrackFX_CopyToTake` - Copy track FX to take
- [ ] `TrackFX_CopyToTrack` - Copy track FX to track
- [ ] `TrackFX_Delete` - Delete track FX (partial impl exists)
- [ ] `TrackFX_EndParamEdit` - End track FX param edit
- [ ] `TrackFX_FormatParamValue` - Format track FX param value
- [ ] `TrackFX_FormatParamValueNormalized` - Format normalized param value
- [ ] `TrackFX_GetByName` - Get track FX by name
- [ ] `TrackFX_GetChainVisible` - Get track FX chain visibility
- [ ] `TrackFX_GetCount` - Get track FX count (partial impl exists)
- [ ] `TrackFX_GetEnabled` - Get track FX enabled (partial impl exists)
- [ ] `TrackFX_GetEQ` - Get track EQ
- [ ] `TrackFX_GetEQBandEnabled` - Get EQ band enabled
- [ ] `TrackFX_GetEQParam` - Get EQ parameter
- [ ] `TrackFX_GetFloatingWindow` - Get floating FX window
- [ ] `TrackFX_GetFXGUID` - Get track FX GUID
- [ ] `TrackFX_GetFXName` - Get track FX name (partial impl exists)
- [ ] `TrackFX_GetIOSize` - Get track FX IO size
- [ ] `TrackFX_GetNamedConfigParm` - Get track FX named config param
- [ ] `TrackFX_GetNumParams` - Get track FX parameter count
- [ ] `TrackFX_GetOffline` - Get track FX offline state
- [ ] `TrackFX_GetOpen` - Get track FX open state
- [ ] `TrackFX_GetParam` - Get track FX parameter (partial impl exists)
- [ ] `TrackFX_GetParameterStepSizes` - Get track FX parameter step sizes
- [ ] `TrackFX_GetParamEx` - Get track FX parameter extended
- [ ] `TrackFX_GetParamFromIdent` - Get track FX param from identifier
- [ ] `TrackFX_GetParamIdent` - Get track FX param identifier
- [ ] `TrackFX_GetParamName` - Get track FX param name
- [ ] `TrackFX_GetParamNormalized` - Get track FX normalized param
- [ ] `TrackFX_GetPinMappings` - Get track FX pin mappings
- [ ] `TrackFX_GetPreset` - Get track FX preset
- [ ] `TrackFX_GetPresetIndex` - Get track FX preset index
- [ ] `TrackFX_GetRecChainVisible` - Get record FX chain visibility
- [ ] `TrackFX_GetRecCount` - Get record FX count
- [ ] `TrackFX_GetUserPresetFilename` - Get track FX user preset filename
- [ ] `TrackFX_NavigatePresets` - Navigate track FX presets
- [ ] `TrackFX_SetEQBandEnabled` - Set EQ band enabled
- [ ] `TrackFX_SetEQParam` - Set EQ parameter
- [ ] `TrackFX_SetEnabled` - Set track FX enabled
- [ ] `TrackFX_SetNamedConfigParm` - Set track FX named config param
- [ ] `TrackFX_SetOffline` - Set track FX offline
- [ ] `TrackFX_SetOpen` - Set track FX open
- [ ] `TrackFX_SetParam` - Set track FX parameter (partial impl exists)
- [ ] `TrackFX_SetParamNormalized` - Set track FX normalized param
- [ ] `TrackFX_SetPinMappings` - Set track FX pin mappings
- [ ] `TrackFX_SetPreset` - Set track FX preset
- [ ] `TrackFX_SetPresetByIndex` - Set track FX preset by index
- [ ] `TrackFX_Show` - Show track FX window
- [ ] `TrackList_AdjustWindows` - Adjust track list windows
- [ ] `TrackList_UpdateAllExternalSurfaces` - Update external surfaces
- [ ] `Undo_BeginBlock` - Begin undo block (partial impl exists)
- [ ] `Undo_BeginBlock2` - Begin undo block v2
- [ ] `Undo_CanRedo2` - Can redo v2
- [ ] `Undo_CanUndo2` - Can undo v2
- [ ] `Undo_DoRedo2` - Do redo v2
- [ ] `Undo_DoUndo2` - Do undo v2
- [ ] `Undo_EndBlock` - End undo block (partial impl exists)
- [ ] `Undo_EndBlock2` - End undo block v2
- [ ] `Undo_OnStateChange` - On state change
- [ ] `Undo_OnStateChange2` - On state change v2
- [ ] `Undo_OnStateChange_Item` - On state change item
- [ ] `Undo_OnStateChangeEx` - On state change extended
- [ ] `Undo_OnStateChangeEx2` - On state change extended v2
- [ ] `UnfreezeTrack` - Unfreeze track (partial impl exists)
- [ ] `UnmuteAllTracks` - Unmute all tracks
- [ ] `UnsoloAllTracks` - Unsolo all tracks
- [ ] `UpdateArrange` - Update arrange (partial impl exists)
- [ ] `UpdateItemInProject` - Update item in project
- [ ] `UpdateTimeline` - Update timeline (partial impl exists)
- [ ] `ValidatePtr` - Validate pointer
- [ ] `ValidatePtr2` - Validate pointer v2
- [ ] `ViewPrefs` - View preferences
- [ ] `WDL_VirtualWnd_ScaledBlitBG` - Virtual window scaled blit
- [ ] `WDL_VirtualIconButton_GetIcon` - Get virtual icon button icon

### String/Utility Functions
- [ ] `WDL_FastString` - Fast string operations
- [ ] `WDL_String` - String operations
- [ ] `format_timestr` - Format time string
- [ ] `format_timestr_len` - Format time string with length
- [ ] `format_timestr_pos` - Format time string position
- [ ] `parse_timestr` - Parse time string
- [ ] `parse_timestr_len` - Parse time string with length
- [ ] `parse_timestr_pos` - Parse time string position
- [ ] `mkpanstr` - Make pan string
- [ ] `mkvolpanstr` - Make volume/pan string
- [ ] `mkvolstr` - Make volume string
- [ ] `parsepanstr` - Parse pan string
- [ ] `guidToString` - GUID to string
- [ ] `stringToGuid` - String to GUID
- [ ] `genGuid` - Generate GUID
- [ ] `relative_fn` - Relative filename
- [ ] `resolve_fn` - Resolve filename
- [ ] `resolve_fn2` - Resolve filename v2

### Low-Level/Advanced Functions
- [ ] `get_config_var_string` - Get config variable string
- [ ] `get_ini_file` - Get INI file
- [ ] `get_midi_config_var` - Get MIDI config variable
- [ ] `GetSetObjectState` - Get/set object state
- [ ] `GetSetObjectState2` - Get/set object state v2
- [ ] `ValidatePtr` - Validate pointer
- [ ] `ValidatePtr2` - Validate pointer v2
- [ ] `plugin_getapi` - Get plugin API
- [ ] `plugin_getFilterList` - Get plugin filter list
- [ ] `plugin_getImportableProjectFilterList` - Get importable project filter list
- [ ] `plugin_register` - Register plugin

### SWS Extension Functions (BR_*)
The BR_* functions are part of the SWS extension and represent additional functionality not in core REAPER. These are listed above in the relevant categories.

## Method Naming Convention
- **MCP Tool Name**: snake_case (e.g., `get_track_count`)
- **Lua Function Name**: PascalCase matching REAPER API (e.g., `CountTracks`)
- **Parameters**: Typically include project (0 for current) and indices

## Test Coverage Summary
All 228 implemented methods have comprehensive test coverage across 32 test files:
- test_track_methods.py
- test_track_volume_pan.py
- test_selection_operations.py
- test_audio_source_operations.py
- test_track_folders.py
- test_media_items.py
- test_midi_operations.py
- test_advanced_midi.py
- test_rendering_freezing.py
- test_fx_operations.py
- test_project_operations.py
- test_save_project.py
- test_envelope_operations.py
- test_automation_operations.py
- test_tempo_time_signature.py
- test_track_routing.py
- test_file_operations.py
- test_gui_operations.py
- test_take_operations.py
- test_project_settings.py
- test_selected_items.py
- test_peak_analysis.py
- test_advanced_track_operations.py
- test_advanced_item_operations.py
- test_recording_operations.py
- test_midi_hardware.py
- test_color_management.py
- test_advanced_project_operations.py
- test_bounce_render_operations.py
- test_video_operations.py
- test_core_api_functions.py
- test_time_tempo_extended.py
- test_audio_accessor.py
- test_midi_editor.py
- test_routing_sends.py
- test_take_fx.py
- test_recording.py

## Adding New Methods
1. Create or update tool module in `server/tools/` directory
2. Add registration function to module (e.g., `register_audio_accessor_tools`)
3. Import and register in `server/app.py`
4. Add Lua mapping in `lua/mcp_bridge.lua` if needed
5. Add tests in appropriate test file
6. Update this master list
7. Commit with descriptive message

## Notes
- Track indices are 0-based
- Project parameter is typically 0 for current project
- Volume is converted between dB (Python) and linear (Lua) representations
- Error handling includes existence checks where applicable
- Latest update: Added 94 new methods across 5 categories (Audio Accessor, MIDI Editor, Routing/Sends, Take FX)
- All implementations follow modern modular pattern with separate tool files