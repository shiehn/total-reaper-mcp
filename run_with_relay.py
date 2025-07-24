#!/usr/bin/env python3
"""
Run the MCP server connected to WebSocket relay
"""
import os
import asyncio
import logging
from server.app import register_all_tools
from server.websocket_client import MCPWebSocketClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Set environment
    os.environ["MCP_RELAY_URL"] = "ws://localhost:8765/mcp"
    os.environ["MCP_AUTH_TOKEN"] = "test_token_12345"
    
    # Register tools
    logger.info("Registering tools...")
    total = register_all_tools()
    logger.info(f"Registered {total} tools")
    
    # Bridge directory for file communication with REAPER
    bridge_dir = os.path.expanduser("~/Library/Application Support/REAPER/Scripts/mcp_bridge_data")
    
    # Tool handler
    async def handle_command(method: str, params: dict):
        logger.info(f"Executing: {method} with params: {params}")
        
        # Import the bridge
        from server.bridge import bridge
        
        try:
            # Different commands have different calling patterns
            # Let's handle the common cases
            
            if method == "CountTracks" or method == "get_track_count":
                # Call through the bridge
                result = await bridge.call_lua("CountTracks", [0])
                logger.info(f"Result: {result}")
                if result.get("ok"):
                    return {"success": True, "result": result.get("ret", 0)}
                else:
                    return {"error": result.get("error", "Unknown error")}
                    
            elif method == "InsertTrackAtIndex" or method == "insert_track":
                # Parse params
                index = params.get("index", -1)
                if isinstance(index, str):
                    index = int(index)
                result = await bridge.call_lua("InsertTrackAtIndex", [index, True])
                logger.info(f"Result: {result}")
                if result.get("ok"):
                    return {"success": True, "result": {"success": True, "track_index": index}}
                else:
                    return {"error": result.get("error", "Unknown error")}
                    
            elif method == "Main_OnCommand":
                # Main_OnCommand takes (command_id, flag)
                cmd = params.get("cmd") or params.get("command") or params.get("command_id")
                if isinstance(cmd, str):
                    cmd = int(cmd)
                flag = params.get("flag", 0)
                result = await bridge.call_lua("Main_OnCommand", [cmd, flag])
                logger.info(f"Result: {result}")
                if result.get("ok"):
                    return {"success": True, "result": {"success": True}}
                else:
                    return {"error": result.get("error", "Unknown error")}
                    
            elif method == "GetTrack":
                # GetTrack takes (project, trackidx)
                proj = params.get("proj") or params.get("project") or 0
                idx = params.get("index") or params.get("trackidx") or params.get("track_index")
                if isinstance(idx, str):
                    idx = int(idx)
                result = await bridge.call_lua("GetTrack", [proj, idx])
                logger.info(f"Result: {result}")
                if result.get("ok"):
                    return {"success": True, "result": result.get("ret", None)}
                else:
                    return {"error": result.get("error", "Unknown error")}
                    
            else:
                # For other methods, try to call directly
                # Build args from params
                args = []
                if "proj" in params:
                    args.append(params["proj"])
                if "project" in params:
                    args.append(params["project"])
                if "trackidx" in params:
                    args.append(params["trackidx"])
                if "track_index" in params:
                    args.append(params["track_index"])
                if "index" in params:
                    args.append(params["index"])
                    
                # Add remaining params
                for k, v in params.items():
                    if k not in ["proj", "project", "trackidx", "track_index", "index"]:
                        args.append(v)
                
                result = await bridge.call_lua(method, args)
                logger.info(f"Result: {result}")
                
                if result.get("ok"):
                    return {"success": True, "result": result.get("ret", result)}
                else:
                    return {"error": result.get("error", "Unknown error")}
                    
        except Exception as e:
            logger.error(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    # Create relay client
    relay_url = "ws://localhost:8765/mcp"
    auth_token = "test_token_12345"
    
    logger.info(f"Connecting to relay: {relay_url}")
    client = MCPWebSocketClient(relay_url, auth_token, handle_command)
    
    # Start connection
    await client.connect()
    
    logger.info("Connected to relay! Waiting for commands...")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        client.stop()

if __name__ == "__main__":
    asyncio.run(main())