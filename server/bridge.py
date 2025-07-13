"""
REAPER File Bridge - Shared communication module

This module provides the file-based bridge for communicating with REAPER.
It's shared across all tool modules to maintain a single connection point.
"""

import os
import json
import asyncio
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# Bridge directory configuration
BRIDGE_DIR = Path(os.environ.get(
    'REAPER_MCP_BRIDGE_DIR',
    os.path.expanduser('~/Library/Application Support/REAPER/Scripts/mcp_bridge_data')
))
BRIDGE_DIR.mkdir(parents=True, exist_ok=True)

class ReaperFileBridge:
    """File-based bridge for communicating with REAPER"""
    
    def __init__(self):
        self.bridge_dir = BRIDGE_DIR
        self.request_id = 0
        
    async def call_lua(self, func_name: str, args: Optional[List[Any]] = None) -> Dict[str, Any]:
        """Call a Lua function and wait for response"""
        self.request_id += 1
        request_file = self.bridge_dir / f"request_{self.request_id}.json"
        response_file = self.bridge_dir / f"response_{self.request_id}.json"
        
        # Write request
        request_data = {
            "id": self.request_id,
            "func": func_name,
            "args": args or []
        }
        
        try:
            with open(request_file, 'w') as f:
                json.dump(request_data, f)
            
            # Wait for response (with timeout)
            start_time = asyncio.get_event_loop().time()
            timeout = 5.0  # 5 second timeout
            
            while asyncio.get_event_loop().time() - start_time < timeout:
                if response_file.exists():
                    try:
                        with open(response_file, 'r') as f:
                            response = json.load(f)
                        # Clean up files
                        request_file.unlink(missing_ok=True)
                        response_file.unlink(missing_ok=True)
                        return response
                    except json.JSONDecodeError:
                        # File might be partially written, wait a bit
                        await asyncio.sleep(0.01)
                await asyncio.sleep(0.1)
            
            # Timeout
            request_file.unlink(missing_ok=True)
            logger.error("Timeout waiting for REAPER response")
            return {"ok": False, "error": "Timeout waiting for REAPER response"}
            
        except Exception as e:
            logger.error(f"Bridge error: {e}")
            return {"ok": False, "error": str(e)}

# Singleton instance
bridge = ReaperFileBridge()