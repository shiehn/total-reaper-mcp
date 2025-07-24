#!/usr/bin/env python3
"""
Connect MCP server to WebSocket relay
"""

import asyncio
import json
import os
import websockets
import subprocess
import sys

async def handle_command(command_data):
    """Handle command from relay"""
    print(f"Received command: {command_data.get('method')}")
    
    # Execute via Reaper bridge
    method = command_data.get('method', '')
    params = command_data.get('params', {})
    
    # Simple example responses
    if method == "get_track_count":
        return {"count": 5}
    elif method == "get_master_track_info":
        return {"name": "Master", "volume": 0.7}
    elif method == "insert_track":
        return {"success": True, "track_index": params.get('index', 0)}
    else:
        return {"result": f"Executed {method}"}

async def run_relay_client():
    """Run the WebSocket relay client"""
    relay_url = os.environ.get("MCP_RELAY_URL", "ws://localhost:8765/mcp")
    auth_token = os.environ.get("MCP_AUTH_TOKEN", "test_token_12345")
    
    print(f"Connecting to relay: {relay_url}")
    print(f"Using token: {auth_token[:20]}...")
    
    async with websockets.connect(relay_url) as ws:
        # Authenticate
        await ws.send(json.dumps({
            "type": "auth",
            "token": auth_token
        }))
        
        # Get auth response
        response = await ws.recv()
        auth_data = json.loads(response)
        print(f"Auth response: {auth_data}")
        
        if auth_data.get("type") != "auth_success":
            print("Authentication failed!")
            return
        
        print("Connected to relay successfully!")
        
        # Send periodic pings and handle commands
        ping_task = None
        try:
            async def send_pings():
                while True:
                    await asyncio.sleep(30)
                    await ws.send(json.dumps({"type": "ping"}))
                    print("Sent ping")
            
            ping_task = asyncio.create_task(send_pings())
            
            # Handle messages
            async for message in ws:
                data = json.loads(message)
                msg_type = data.get("type")
                
                if msg_type == "command":
                    print(f"Command: {data.get('method')}")
                    request_id = data.get("request_id")
                    
                    try:
                        # Handle the command
                        result = await handle_command(data)
                        
                        # Send response
                        response = {
                            "type": "response",
                            "request_id": request_id,
                            "result": result
                        }
                    except Exception as e:
                        response = {
                            "type": "response",
                            "request_id": request_id,
                            "error": str(e)
                        }
                    
                    await ws.send(json.dumps(response))
                    print(f"Sent response for {data.get('method')}")
                    
                elif msg_type == "ping":
                    await ws.send(json.dumps({"type": "pong"}))
                    
        finally:
            if ping_task:
                ping_task.cancel()

if __name__ == "__main__":
    print("MCP WebSocket Relay Client")
    print("="*50)
    
    try:
        asyncio.run(run_relay_client())
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()