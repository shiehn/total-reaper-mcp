"""
WebSocket client for connecting MCP server to the relay service
"""

import asyncio
import json
import logging
import os
from typing import Optional, Dict, Any, Callable
from datetime import datetime

import websockets
from websockets.client import WebSocketClientProtocol

logger = logging.getLogger(__name__)

class MCPWebSocketClient:
    """WebSocket client that connects MCP server to the relay"""
    
    def __init__(self, relay_url: str, auth_token: str, command_handler: Callable):
        self.relay_url = relay_url
        self.auth_token = auth_token
        self.command_handler = command_handler
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.connected = False
        self.reconnect_delay = 5.0
        self.max_reconnect_delay = 60.0
        self.ping_interval = 30.0
        self._running = False
        self.connection_attempts = 0
        self.last_connected = None
        self.health_check_interval = 60.0  # Check REAPER health every minute
        self._health_task = None
        
    async def connect(self):
        """Connect to the relay server"""
        self._running = True
        current_delay = self.reconnect_delay
        
        while self._running:
            try:
                self.connection_attempts += 1
                logger.info(f"Connecting to relay: {self.relay_url} (attempt #{self.connection_attempts})")
                
                async with websockets.connect(
                    self.relay_url,
                    ping_interval=20,  # Send WebSocket pings every 20s
                    ping_timeout=10    # Wait 10s for pong
                ) as websocket:
                    self.websocket = websocket
                    
                    # Authenticate
                    await self._authenticate()
                    
                    # Reset reconnect delay on successful connection
                    current_delay = self.reconnect_delay
                    self.connection_attempts = 0
                    self.last_connected = datetime.now()
                    
                    # Start monitoring tasks
                    ping_task = asyncio.create_task(self._ping_loop())
                    health_task = asyncio.create_task(self._health_check_loop())
                    
                    try:
                        # Handle messages
                        await self._handle_messages()
                    finally:
                        ping_task.cancel()
                        health_task.cancel()
                        await asyncio.gather(ping_task, health_task, return_exceptions=True)
                        
            except websockets.exceptions.InvalidStatusCode as e:
                logger.error(f"Connection rejected: {e}")
                if e.status_code == 401:
                    logger.error("Authentication failed - check your token")
                    break
            except Exception as e:
                logger.error(f"Connection error: {e}")
                
            if self._running:
                logger.info(f"Reconnecting in {current_delay} seconds...")
                await asyncio.sleep(current_delay)
                # Exponential backoff
                current_delay = min(current_delay * 2, self.max_reconnect_delay)
                
        self.connected = False
        logger.info("WebSocket client stopped")
        
    async def _authenticate(self):
        """Authenticate with the relay server"""
        logger.info("Authenticating...")
        await self.websocket.send(json.dumps({
            "type": "auth",
            "token": self.auth_token
        }))
        
        # Wait for auth response
        response = await self.websocket.recv()
        data = json.loads(response)
        
        if data.get("type") == "auth_success":
            self.connected = True
            logger.info(f"Authenticated successfully as user {data.get('user_id')}")
        else:
            raise Exception(f"Authentication failed: {data.get('error')}")
            
    async def _handle_messages(self):
        """Handle incoming messages from relay"""
        async for message in self.websocket:
            try:
                data = json.loads(message)
                message_type = data.get("type")
                
                if message_type == "command":
                    # Handle command from relay
                    asyncio.create_task(self._handle_command(data))
                elif message_type == "pong":
                    # Pong response to our ping
                    pass
                else:
                    logger.warning(f"Unknown message type: {message_type}")
                    
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON: {message}")
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                
    async def _handle_command(self, command_data: Dict[str, Any]):
        """Handle command from relay"""
        request_id = command_data.get("request_id")
        method = command_data.get("method")
        params = command_data.get("params", {})
        
        logger.info(f"Executing command: {method}")
        
        try:
            # Execute command through MCP
            result = await self.command_handler(method, params)
            
            # Send success response
            await self.send_response(request_id, result=result)
            
        except Exception as e:
            logger.error(f"Command error: {e}")
            # Send error response
            await self.send_response(request_id, error=str(e))
            
    async def send_response(self, request_id: str, result: Any = None, error: str = None):
        """Send response back to relay"""
        response = {
            "type": "response",
            "request_id": request_id
        }
        
        if error:
            response["error"] = error
        else:
            response["result"] = result
            
        if self.websocket and self.connected:
            await self.websocket.send(json.dumps(response))
            
    async def send_event(self, event_type: str, data: Dict[str, Any]):
        """Send event to relay"""
        if self.websocket and self.connected:
            await self.websocket.send(json.dumps({
                "type": "event",
                "event_type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }))
            
    async def _ping_loop(self):
        """Send periodic pings to keep connection alive"""
        while self.connected:
            try:
                await asyncio.sleep(self.ping_interval)
                if self.websocket and self.connected:
                    await self.websocket.send(json.dumps({"type": "ping"}))
            except Exception as e:
                logger.error(f"Ping error: {e}")
                break
                
    async def disconnect(self):
        """Disconnect from relay"""
        self._running = False
        if self.websocket:
            await self.websocket.close()
            
    def is_connected(self) -> bool:
        """Check if connected to relay"""
        return self.connected
        
    async def _health_check_loop(self):
        """Periodically check REAPER health"""
        while self.connected:
            try:
                await asyncio.sleep(self.health_check_interval)
                
                # Send health status event
                health_info = {
                    "connected": self.connected,
                    "last_connected": self.last_connected.isoformat() if self.last_connected else None,
                    "connection_attempts": self.connection_attempts
                }
                
                # Try a simple REAPER command to verify bridge is working
                try:
                    # This will test the bridge connection
                    result = await self.command_handler("CountTracks", {})
                    health_info["reaper_connected"] = True
                    health_info["reaper_test_result"] = result
                except Exception as e:
                    health_info["reaper_connected"] = False
                    health_info["reaper_error"] = str(e)
                    logger.warning(f"REAPER health check failed: {e}")
                
                # Send health event to relay
                await self.send_event("health_status", health_info)
                
            except Exception as e:
                logger.error(f"Health check error: {e}")
                break


# Integration with MCP server
async def create_relay_client(mcp_server_instance) -> MCPWebSocketClient:
    """Create and configure relay client for MCP server"""
    
    # Get configuration from environment
    relay_url = os.environ.get("MCP_RELAY_URL", "ws://localhost:8765/mcp")
    auth_token = os.environ.get("MCP_AUTH_TOKEN", "")
    
    if not auth_token:
        logger.warning("No MCP_AUTH_TOKEN set - relay connection disabled")
        return None
        
    # Create command handler that bridges to MCP
    async def handle_command(method: str, params: Dict[str, Any]) -> Any:
        # This will call the appropriate MCP tool
        tool_func = mcp_server_instance.get_tool(method)
        if not tool_func:
            raise Exception(f"Unknown method: {method}")
            
        # Execute the tool
        result = await tool_func(**params)
        return result
        
    # Create client
    client = MCPWebSocketClient(relay_url, auth_token, handle_command)
    
    # Start connection in background
    asyncio.create_task(client.connect())
    
    return client