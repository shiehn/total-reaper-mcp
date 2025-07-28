"""
Routing & Sends Management Tools for REAPER MCP

This module contains tools for managing track sends, receives, hardware outputs,
and routing configurations.
"""

from typing import Optional, Tuple, Any
from ..bridge import bridge


# ============================================================================
# Track Send Management (12 tools)
# ============================================================================

async def get_track_num_sends(track_index: int, category: int = 0) -> str:
    """Get number of sends/receives/hardware outputs on track"""
    # Category: 0=sends, 1=receives, 2=hardware outputs
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get send count
    result = await bridge.call_lua("GetTrackNumSends", [track_handle, category])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        category_name = ["sends", "receives", "hardware outputs"][category]
        return f"Track has {count} {category_name}"
    else:
        raise Exception(f"Failed to get send count: {result.get('error', 'Unknown error')}")


async def create_track_send(src_track_index: int, dst_track_index: int) -> str:
    """Create a send from source track to destination track"""
    # Verify tracks exist first
    src_track_result = await bridge.call_lua("GetTrack", [0, src_track_index])
    if not src_track_result.get("ok") or not src_track_result.get("ret"):
        raise Exception(f"Failed to find source track at index {src_track_index}")
    
    dst_track_result = await bridge.call_lua("GetTrack", [0, dst_track_index])
    if not dst_track_result.get("ok") or not dst_track_result.get("ret"):
        raise Exception(f"Failed to find destination track at index {dst_track_index}")
    
    # Create send using track indices (CreateTrackSend handler will convert to track objects)
    result = await bridge.call_lua("CreateTrackSend", [src_track_index, dst_track_index])
    
    if result.get("ok"):
        send_idx = result.get("ret", -1)
        if send_idx >= 0:
            return f"Created send from track {src_track_index} to track {dst_track_index} (send index: {send_idx})"
        else:
            return "Failed to create send"
    else:
        raise Exception(f"Failed to create send: {result.get('error', 'Unknown error')}")


async def remove_track_send(track_index: int, category: int, send_index: int) -> str:
    """Remove a send/receive/hardware output from track"""
    # Category: 0=sends, 1=receives, 2=hardware outputs
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Remove send
    result = await bridge.call_lua("RemoveTrackSend", [track_handle, category, send_index])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            category_name = ["send", "receive", "hardware output"][category]
            return f"Removed {category_name} {send_index} from track {track_index}"
        else:
            return f"Failed to remove send/receive"
    else:
        raise Exception(f"Failed to remove send: {result.get('error', 'Unknown error')}")


async def get_track_send_name(track_index: int, send_index: int) -> str:
    """Get the name of a track send"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get send name
    result = await bridge.call_lua("GetTrackSendName", [track_handle, send_index, ""])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, name = ret[:2]
            if retval:
                return f"Send {send_index}: {name}"
        return f"Send {send_index}: (unnamed)"
    else:
        raise Exception(f"Failed to get send name: {result.get('error', 'Unknown error')}")


async def get_track_receive_name(track_index: int, receive_index: int) -> str:
    """Get the name of a track receive"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get receive name  
    result = await bridge.call_lua("GetTrackReceiveName", [track_handle, receive_index, ""])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, name = ret[:2]
            if retval:
                return f"Receive {receive_index}: {name}"
        return f"Receive {receive_index}: (unnamed)"
    else:
        raise Exception(f"Failed to get receive name: {result.get('error', 'Unknown error')}")


async def get_track_send_info_value(track_index: int, category: int, send_index: int, param_name: str) -> str:
    """Get send/receive/hardware output parameter value"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get send info
    result = await bridge.call_lua("GetTrackSendInfo_Value", [track_handle, category, send_index, param_name])
    
    if result.get("ok"):
        value = result.get("ret", 0.0)
        category_name = ["Send", "Receive", "Hardware output"][category]
        return f"{category_name} {send_index} {param_name}: {value}"
    else:
        raise Exception(f"Failed to get send info: {result.get('error', 'Unknown error')}")


async def set_track_send_info_value(track_index: int, category: int, send_index: int, 
                                   param_name: str, value: float) -> str:
    """Set send/receive/hardware output parameter value"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set send info
    result = await bridge.call_lua("SetTrackSendInfo_Value", [track_handle, category, send_index, param_name, value])
    
    if result.get("ok"):
        success = result.get("ret", False)
        if success:
            category_name = ["Send", "Receive", "Hardware output"][category]
            return f"Set {category_name} {send_index} {param_name} to {value}"
        else:
            return f"Failed to set send parameter"
    else:
        raise Exception(f"Failed to set send info: {result.get('error', 'Unknown error')}")


async def get_set_track_send_info_string(track_index: int, category: int, send_index: int,
                                        param_name: str, value: str = "", set_value: bool = False) -> str:
    """Get or set send/receive/hardware output string parameter"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get/set send string info
    result = await bridge.call_lua("GetSetTrackSendInfo_String", [
        track_handle, category, send_index, param_name, value, set_value
    ])
    
    if result.get("ok"):
        if set_value:
            category_name = ["Send", "Receive", "Hardware output"][category]
            return f"Set {category_name} {send_index} {param_name} to: {value}"
        else:
            info_value = result.get("ret", "")
            category_name = ["Send", "Receive", "Hardware output"][category]
            return f"{category_name} {send_index} {param_name}: {info_value if info_value else '(not set)'}"
    else:
        raise Exception(f"Failed to get/set send string info: {result.get('error', 'Unknown error')}")


async def get_track_send_ui_vol_pan(track_index: int, send_index: int) -> str:
    """Get track send volume and pan UI values"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get UI vol/pan
    result = await bridge.call_lua("GetTrackSendUIVolPan", [track_handle, send_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            volume, pan = ret[:2]
            return f"Send {send_index}: volume={volume:.3f}, pan={pan:.3f}"
        else:
            return f"Failed to get send UI values"
    else:
        raise Exception(f"Failed to get send UI vol/pan: {result.get('error', 'Unknown error')}")


async def set_track_send_ui_vol(track_index: int, send_index: int, volume: float) -> str:
    """Set track send UI volume"""
    # Verify track exists first
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set UI volume using track index (SetTrackSendUIVol handler will convert to track object)
    result = await bridge.call_lua("SetTrackSendUIVol", [track_index, send_index, volume, 0])
    
    if result.get("ok"):
        return f"Set send {send_index} UI volume to {volume:.3f}"
    else:
        raise Exception(f"Failed to set send UI volume: {result.get('error', 'Unknown error')}")


async def set_track_send_ui_pan(track_index: int, send_index: int, pan: float) -> str:
    """Set track send UI pan"""
    # Verify track exists first
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set UI pan using track index (SetTrackSendUIPan handler will convert to track object)
    result = await bridge.call_lua("SetTrackSendUIPan", [track_index, send_index, pan, 0])
    
    if result.get("ok"):
        return f"Set send {send_index} UI pan to {pan:.3f}"
    else:
        raise Exception(f"Failed to set send UI pan: {result.get('error', 'Unknown error')}")


async def toggle_track_send_ui_mute(track_index: int, send_index: int) -> str:
    """Toggle track send UI mute state"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Toggle mute
    result = await bridge.call_lua("ToggleTrackSendUIMute", [track_handle, send_index])
    
    if result.get("ok"):
        new_state = result.get("ret", False)
        state_str = "muted" if new_state else "unmuted"
        return f"Send {send_index} is now {state_str}"
    else:
        raise Exception(f"Failed to toggle send mute: {result.get('error', 'Unknown error')}")


# ============================================================================
# Track Receive Management (8 tools)
# ============================================================================

async def get_track_receive_ui_vol_pan(track_index: int, receive_index: int) -> str:
    """Get track receive volume and pan UI values"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get UI vol/pan
    result = await bridge.call_lua("GetTrackReceiveUIVolPan", [track_handle, receive_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            volume, pan = ret[:2]
            return f"Receive {receive_index}: volume={volume:.3f}, pan={pan:.3f}"
        else:
            return f"Failed to get receive UI values"
    else:
        raise Exception(f"Failed to get receive UI vol/pan: {result.get('error', 'Unknown error')}")


async def get_track_receive_ui_mute(track_index: int, receive_index: int) -> str:
    """Get track receive UI mute state"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get UI mute
    result = await bridge.call_lua("GetTrackReceiveUIMute", [track_handle, receive_index])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            retval, muted = ret[:2]
            if retval:
                state_str = "muted" if muted else "unmuted"
                return f"Receive {receive_index} is {state_str}"
        return f"Failed to get receive mute state"
    else:
        raise Exception(f"Failed to get receive UI mute: {result.get('error', 'Unknown error')}")


async def get_send_destination_track(src_track_index: int, send_index: int) -> str:
    """Get the destination track of a send"""
    # Get source track
    track_result = await bridge.call_lua("GetTrack", [0, src_track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {src_track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get destination track via P_DESTTRACK parameter
    result = await bridge.call_lua("GetTrackSendInfo_Value", [track_handle, 0, send_index, "P_DESTTRACK"])
    
    if result.get("ok"):
        dest_track = result.get("ret")
        if dest_track:
            # Get destination track name
            name_result = await bridge.call_lua("GetTrackName", [dest_track])
            if name_result.get("ok") and isinstance(name_result.get("ret"), list):
                _, track_name = name_result.get("ret")[:2]
                return f"Send {send_index} goes to: {track_name}"
            else:
                return f"Send {send_index} has destination track"
        else:
            return f"Send {send_index} has no destination"
    else:
        raise Exception(f"Failed to get send destination: {result.get('error', 'Unknown error')}")


async def get_receive_source_track(dst_track_index: int, receive_index: int) -> str:
    """Get the source track of a receive"""
    # Get destination track
    track_result = await bridge.call_lua("GetTrack", [0, dst_track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {dst_track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get source track via P_SRCTRACK parameter
    result = await bridge.call_lua("GetTrackSendInfo_Value", [track_handle, 1, receive_index, "P_SRCTRACK"])
    
    if result.get("ok"):
        src_track = result.get("ret")
        if src_track:
            # Get source track name
            name_result = await bridge.call_lua("GetTrackName", [src_track])
            if name_result.get("ok") and isinstance(name_result.get("ret"), list):
                _, track_name = name_result.get("ret")[:2]
                return f"Receive {receive_index} comes from: {track_name}"
            else:
                return f"Receive {receive_index} has source track"
        else:
            return f"Receive {receive_index} has no source"
    else:
        raise Exception(f"Failed to get receive source: {result.get('error', 'Unknown error')}")


async def set_send_enabled(track_index: int, send_index: int, enabled: bool) -> str:
    """Enable or disable a send"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set enabled state (I_SENDMODE: 0=mute, 1=normal, 3=mute automation)
    value = 1.0 if enabled else 0.0
    result = await bridge.call_lua("SetTrackSendInfo_Value", [track_handle, 0, send_index, "I_SENDMODE", value])
    
    if result.get("ok"):
        state_str = "enabled" if enabled else "disabled"
        return f"Send {send_index} {state_str}"
    else:
        raise Exception(f"Failed to set send enabled state: {result.get('error', 'Unknown error')}")


async def set_send_mode(track_index: int, send_index: int, mode: int) -> str:
    """Set send mode (0=post-fader, 1=pre-fader, 3=post-fx)"""
    # Verify track exists first
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    # Set send mode using track index (SetTrackSendInfo_Value handler will convert to track object)
    result = await bridge.call_lua("SetTrackSendInfo_Value", [track_index, 0, send_index, "I_SENDMODE", float(mode)])
    
    if result.get("ok"):
        mode_names = {0: "post-fader", 1: "pre-fader", 3: "post-fx"}
        mode_str = mode_names.get(mode, f"mode {mode}")
        return f"Set send {send_index} to {mode_str}"
    else:
        raise Exception(f"Failed to set send mode: {result.get('error', 'Unknown error')}")


async def get_send_envelope(track_index: int, send_index: int, envelope_index: int) -> str:
    """Get send envelope (0=volume, 1=pan, 2=mute)"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get send envelope
    result = await bridge.call_lua("BR_GetMediaTrackSendInfo_Envelope", [track_handle, 0, send_index, envelope_index])
    
    if result.get("ok"):
        envelope = result.get("ret")
        if envelope:
            env_names = {0: "volume", 1: "pan", 2: "mute"}
            env_name = env_names.get(envelope_index, f"envelope {envelope_index}")
            return f"Got send {send_index} {env_name} envelope"
        else:
            return f"Send {send_index} has no envelope at index {envelope_index}"
    else:
        # Try alternative method
        return f"Send envelope functionality requires SWS extension"


async def create_hardware_output_send(track_index: int, output_channel: int) -> str:
    """Create a hardware output send on track"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Create hardware output by setting channel
    # First, get current hardware output count
    count_result = await bridge.call_lua("GetTrackNumSends", [track_handle, 2])
    if not count_result.get("ok"):
        raise Exception("Failed to get hardware output count")
    
    hw_count = count_result.get("ret", 0)
    
    # Add new hardware output
    result = await bridge.call_lua("SetTrackSendInfo_Value", [
        track_handle, 2, hw_count, "I_DSTCHAN", float(output_channel)
    ])
    
    if result.get("ok"):
        return f"Created hardware output to channel {output_channel} on track {track_index}"
    else:
        raise Exception(f"Failed to create hardware output: {result.get('error', 'Unknown error')}")


# ============================================================================
# Hardware & MIDI Routing (6 tools)
# ============================================================================

async def get_num_audio_outputs() -> str:
    """Get number of audio outputs"""
    result = await bridge.call_lua("GetNumAudioOutputs", [])
    
    if result.get("ok"):
        count = result.get("ret", 0)
        return f"System has {count} audio outputs"
    else:
        raise Exception(f"Failed to get audio output count: {result.get('error', 'Unknown error')}")


async def get_output_channel_name(channel: int) -> str:
    """Get the name of an output channel"""
    result = await bridge.call_lua("GetOutputChannelName", [channel])
    
    if result.get("ok"):
        name = result.get("ret", "")
        if name:
            return f"Output channel {channel}: {name}"
        else:
            return f"Output channel {channel}: (unnamed)"
    else:
        raise Exception(f"Failed to get output channel name: {result.get('error', 'Unknown error')}")


async def send_midi_message_to_hardware(output: int, msg: str) -> str:
    """Send MIDI message to hardware output"""
    # Convert message string to proper format
    result = await bridge.call_lua("SendMIDIMessageToHardware", [output, msg])
    
    if result.get("ok"):
        return f"Sent MIDI message to output {output}"
    else:
        raise Exception(f"Failed to send MIDI message: {result.get('error', 'Unknown error')}")


async def get_track_ui_vol_pan(track_index: int) -> str:
    """Get track UI volume and pan values"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Get UI vol/pan
    result = await bridge.call_lua("GetTrackUIVolPan", [track_handle])
    
    if result.get("ok"):
        ret = result.get("ret", [])
        if isinstance(ret, list) and len(ret) >= 2:
            volume, pan = ret[:2]
            return f"Track UI: volume={volume:.3f}, pan={pan:.3f}"
        else:
            return f"Failed to get track UI values"
    else:
        raise Exception(f"Failed to get track UI vol/pan: {result.get('error', 'Unknown error')}")


async def set_track_ui_volume(track_index: int, volume: float, relative: bool = False) -> str:
    """Set track UI volume"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set UI volume
    gang = 1 if relative else 0
    result = await bridge.call_lua("SetTrackUIVolume", [track_handle, volume, gang, True])
    
    if result.get("ok"):
        mode = "relative" if relative else "absolute"
        return f"Set track UI volume to {volume:.3f} ({mode})"
    else:
        raise Exception(f"Failed to set track UI volume: {result.get('error', 'Unknown error')}")


async def set_track_ui_pan(track_index: int, pan: float, relative: bool = False) -> str:
    """Set track UI pan"""
    # Get track
    track_result = await bridge.call_lua("GetTrack", [0, track_index])
    if not track_result.get("ok") or not track_result.get("ret"):
        raise Exception(f"Failed to find track at index {track_index}")
    
    track_handle = track_result.get("ret")
    
    # Set UI pan
    gang = 1 if relative else 0
    result = await bridge.call_lua("SetTrackUIPan", [track_handle, pan, gang, True])
    
    if result.get("ok"):
        mode = "relative" if relative else "absolute"
        return f"Set track UI pan to {pan:.3f} ({mode})"
    else:
        raise Exception(f"Failed to set track UI pan: {result.get('error', 'Unknown error')}")


# ============================================================================
# Registration Function
# ============================================================================

def register_routing_sends_tools(mcp) -> int:
    """Register all routing & sends tools with the MCP instance"""
    tools = [
        # Track Send Management
        (get_track_num_sends, "Get number of sends/receives/hardware outputs on track"),
        (create_track_send, "Create a send from source track to destination track"),
        (remove_track_send, "Remove a send/receive/hardware output from track"),
        (get_track_send_name, "Get the name of a track send"),
        (get_track_receive_name, "Get the name of a track receive"),
        (get_track_send_info_value, "Get send/receive/hardware output parameter value"),
        (set_track_send_info_value, "Set send/receive/hardware output parameter value"),
        (get_set_track_send_info_string, "Get or set send/receive/hardware output string parameter"),
        (get_track_send_ui_vol_pan, "Get track send volume and pan UI values"),
        (set_track_send_ui_vol, "Set track send UI volume"),
        (set_track_send_ui_pan, "Set track send UI pan"),
        (toggle_track_send_ui_mute, "Toggle track send UI mute state"),
        
        # Track Receive Management
        (get_track_receive_ui_vol_pan, "Get track receive volume and pan UI values"),
        (get_track_receive_ui_mute, "Get track receive UI mute state"),
        (get_send_destination_track, "Get the destination track of a send"),
        (get_receive_source_track, "Get the source track of a receive"),
        (set_send_enabled, "Enable or disable a send"),
        (set_send_mode, "Set send mode (post-fader/pre-fader/post-fx)"),
        (get_send_envelope, "Get send envelope (volume/pan/mute)"),
        (create_hardware_output_send, "Create a hardware output send on track"),
        
        # Hardware & MIDI Routing
        (get_num_audio_outputs, "Get number of audio outputs"),
        (get_output_channel_name, "Get the name of an output channel"),
        (send_midi_message_to_hardware, "Send MIDI message to hardware output"),
        (get_track_ui_vol_pan, "Get track UI volume and pan values"),
        (set_track_ui_volume, "Set track UI volume"),
        (set_track_ui_pan, "Set track UI pan"),
    ]
    
    # Register each tool
    for func, desc in tools:
        decorated = mcp.tool()(func)
    
    return len(tools)