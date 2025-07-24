-- Add this code before the line "else" at around line 3294
-- This integrates the DSL functions into the main bridge

                    -- DSL Bridge Functions
                    elseif fname == "GetTrackInfo" then
                        if #args >= 1 then
                            local result = GetTrackInfo(args[1])
                            response.ok = result.ok
                            if result.ok then
                                response.info = result.info
                            else
                                response.error = result.error
                            end
                        else
                            response.error = "GetTrackInfo requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetAllTracksInfo" then
                        local result = GetAllTracksInfo()
                        response.ok = result.ok
                        response.tracks = result.tracks
                    
                    elseif fname == "SetTrackNotes" then
                        if #args >= 2 then
                            local result = SetTrackNotes(args[1], args[2])
                            response.ok = result.ok
                            if not result.ok then
                                response.error = result.error
                            end
                        else
                            response.error = "SetTrackNotes requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetCursorPosition" then
                        local result = GetCursorPosition()
                        response.ok = result.ok
                        response.ret = result.ret
                    
                    elseif fname == "GetTimeSelection" then
                        local result = GetTimeSelection()
                        response.ok = result.ok
                        response.start = result.start
                        response["end"] = result["end"]
                    
                    elseif fname == "SetTimeSelection" then
                        if #args >= 2 then
                            local result = SetTimeSelection(args[1], args[2])
                            response.ok = result.ok
                        else
                            response.error = "SetTimeSelection requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetLoopTimeRange" then
                        local result = GetLoopTimeRange()
                        response.ok = result.ok
                        response.start = result.start
                        response["end"] = result["end"]
                    
                    elseif fname == "BarsToTime" then
                        if #args >= 2 then
                            local result = BarsToTime(args[1], args[2])
                            response.ok = result.ok
                            response.ret = result.ret
                        else
                            response.error = "BarsToTime requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "FindRegion" then
                        if #args >= 1 then
                            local result = FindRegion(args[1])
                            response.ok = result.ok
                            response.found = result.found
                            if result.found then
                                response.start = result.start
                                response["end"] = result["end"]
                            end
                        else
                            response.error = "FindRegion requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "FindMarker" then
                        if #args >= 1 then
                            local result = FindMarker(args[1])
                            response.ok = result.ok
                            response.found = result.found
                            if result.found then
                                response.position = result.position
                            end
                        else
                            response.error = "FindMarker requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetSelectedItems" then
                        local result = GetSelectedItems()
                        response.ok = result.ok
                        response.items = result.items
                    
                    elseif fname == "GetAllItems" then
                        local result = GetAllItems()
                        response.ok = result.ok
                        response.items = result.items
                    
                    elseif fname == "GetTrackItems" then
                        if #args >= 1 then
                            local result = GetTrackItems(args[1])
                            response.ok = result.ok
                            if result.ok then
                                response.items = result.items
                            else
                                response.error = result.error
                            end
                        else
                            response.error = "GetTrackItems requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "CreateMIDIItem" then
                        if #args >= 3 then
                            local result = CreateMIDIItem(args[1], args[2], args[3])
                            response.ok = result.ok
                            if result.ok then
                                response.item_index = result.item_index
                            else
                                response.error = result.error
                            end
                        else
                            response.error = "CreateMIDIItem requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "CreateAudioItem" then
                        if #args >= 3 then
                            local result = CreateAudioItem(args[1], args[2], args[3])
                            response.ok = result.ok
                            if result.ok then
                                response.item_index = result.item_index
                            else
                                response.error = result.error
                            end
                        else
                            response.error = "CreateAudioItem requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "SetItemLoopSource" then
                        if #args >= 3 then
                            local result = SetItemLoopSource(args[1], args[2], args[3])
                            response.ok = result.ok
                            if not result.ok then
                                response.error = result.error
                            end
                        else
                            response.error = "SetItemLoopSource requires 3 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "InsertMIDINote" then
                        if #args >= 5 then
                            local result = InsertMIDINote(args[1], args[2], args[3], args[4], args[5], args[6], args[7])
                            response.ok = result.ok
                            if not result.ok then
                                response.error = result.error
                            end
                        else
                            response.error = "InsertMIDINote requires at least 5 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "QuantizeItem" then
                        if #args >= 4 then
                            local result = QuantizeItem(args[1], args[2], args[3], args[4])
                            response.ok = result.ok
                            if not result.ok then
                                response.error = result.error
                            end
                        else
                            response.error = "QuantizeItem requires 4 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetTrackVolume" then
                        if #args >= 1 then
                            local result = GetTrackVolume(args[1])
                            response.ok = result.ok
                            if result.ok then
                                response.ret = result.ret
                            else
                                response.error = result.error
                            end
                        else
                            response.error = "GetTrackVolume requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "SetTrackVolume" then
                        if #args >= 2 then
                            local result = SetTrackVolume(args[1], args[2])
                            response.ok = result.ok
                            if not result.ok then
                                response.error = result.error
                            end
                        else
                            response.error = "SetTrackVolume requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "GetTrackPan" then
                        if #args >= 1 then
                            local result = GetTrackPan(args[1])
                            response.ok = result.ok
                            if result.ok then
                                response.ret = result.ret
                            else
                                response.error = result.error
                            end
                        else
                            response.error = "GetTrackPan requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "SetTrackPan" then
                        if #args >= 2 then
                            local result = SetTrackPan(args[1], args[2])
                            response.ok = result.ok
                            if not result.ok then
                                response.error = result.error
                            end
                        else
                            response.error = "SetTrackPan requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "SetTrackMute" then
                        if #args >= 2 then
                            local result = SetTrackMute(args[1], args[2])
                            response.ok = result.ok
                            if not result.ok then
                                response.error = result.error
                            end
                        else
                            response.error = "SetTrackMute requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "SetTrackSolo" then
                        if #args >= 2 then
                            local result = SetTrackSolo(args[1], args[2])
                            response.ok = result.ok
                            if not result.ok then
                                response.error = result.error
                            end
                        else
                            response.error = "SetTrackSolo requires 2 arguments"
                            response.ok = false
                        end
                    
                    elseif fname == "Play" then
                        local result = Play()
                        response.ok = result.ok
                    
                    elseif fname == "Stop" then
                        local result = Stop()
                        response.ok = result.ok
                    
                    elseif fname == "GetTempo" then
                        local result = GetTempo()
                        response.ok = result.ok
                        response.ret = result.ret
                    
                    elseif fname == "SetTempo" then
                        if #args >= 1 then
                            local result = SetTempo(args[1])
                            response.ok = result.ok
                        else
                            response.error = "SetTempo requires 1 argument"
                            response.ok = false
                        end
                    
                    elseif fname == "GetTimeSignature" then
                        local result = GetTimeSignature()
                        response.ok = result.ok
                        response.numerator = result.numerator
                        response.denominator = result.denominator
                    
                    -- Continue with the existing else clause...