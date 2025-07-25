"""
REAPER File Bridge - Shared communication module

This module provides the file-based bridge for communicating with REAPER.
It's shared across all tool modules to maintain a single connection point.
"""

import os
import json
import asyncio
import logging
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# Bridge directory configuration
BRIDGE_DIR = Path(os.environ.get(
    'REAPER_MCP_BRIDGE_DIR',
    os.path.expanduser('~/Library/Application Support/REAPER/Scripts/mcp_bridge_data')
))
BRIDGE_DIR.mkdir(parents=True, exist_ok=True)

# ReaScript logging configuration
REASCRIPT_LOGGING_ENABLED = os.environ.get('REASCRIPT_LOGGING', '').lower() in ('1', 'true', 'yes')
REASCRIPT_LOG_FILE = Path(os.environ.get(
    'REASCRIPT_LOG_FILE',
    '/tmp/reascript_calls.jsonl'
))

class ReaperFileBridge:
    """File-based bridge for communicating with REAPER"""
    
    def __init__(self):
        self.bridge_dir = BRIDGE_DIR
        self.request_id = 0
        self.call_tracking = []  # Track calls during operations
        self.tracking_enabled = False
        
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
        
        # Track call start time for performance logging
        call_start_time = time.time()
        
        # Log ReaScript call if enabled
        if REASCRIPT_LOGGING_ENABLED:
            log_entry = {
                "timestamp": call_start_time,
                "request_id": self.request_id,
                "type": "call",
                "function": func_name,
                "args": args or [],
                "dsl_tool": os.environ.get('CURRENT_DSL_TOOL', 'unknown')
            }
            try:
                with open(REASCRIPT_LOG_FILE, 'a') as f:
                    f.write(json.dumps(log_entry) + '\n')
            except Exception as e:
                logger.debug(f"Failed to log ReaScript call: {e}")
        
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
                        
                        # Track call if tracking is enabled
                        if self.tracking_enabled:
                            duration_ms = (time.time() - call_start_time) * 1000
                            self.call_tracking.append({
                                "timestamp": call_start_time,
                                "function": func_name,
                                "args": args or [],
                                "response": response,
                                "duration_ms": duration_ms,
                                "success": response.get("ok", False)
                            })
                        
                        # Log ReaScript response if enabled
                        if REASCRIPT_LOGGING_ENABLED:
                            duration_ms = (time.time() - call_start_time) * 1000
                            log_entry = {
                                "timestamp": time.time(),
                                "request_id": self.request_id,
                                "type": "response",
                                "function": func_name,
                                "response": response,
                                "duration_ms": duration_ms,
                                "success": response.get("ok", False),
                                "dsl_tool": os.environ.get('CURRENT_DSL_TOOL', 'unknown')
                            }
                            try:
                                with open(REASCRIPT_LOG_FILE, 'a') as f:
                                    f.write(json.dumps(log_entry) + '\n')
                            except Exception as e:
                                logger.debug(f"Failed to log ReaScript response: {e}")
                        
                        return response
                    except json.JSONDecodeError:
                        # File might be partially written, wait a bit
                        await asyncio.sleep(0.01)
                await asyncio.sleep(0.1)
            
            # Timeout
            request_file.unlink(missing_ok=True)
            logger.error("Timeout waiting for REAPER response")
            timeout_response = {"ok": False, "error": "Timeout waiting for REAPER response"}
            
            # Track timeout if tracking is enabled
            if self.tracking_enabled:
                duration_ms = (time.time() - call_start_time) * 1000
                self.call_tracking.append({
                    "timestamp": call_start_time,
                    "function": func_name,
                    "args": args or [],
                    "response": timeout_response,
                    "duration_ms": duration_ms,
                    "success": False,
                    "timeout": True
                })
            
            # Log timeout if enabled
            if REASCRIPT_LOGGING_ENABLED:
                duration_ms = (time.time() - call_start_time) * 1000
                log_entry = {
                    "timestamp": time.time(),
                    "request_id": self.request_id,
                    "type": "timeout",
                    "function": func_name,
                    "duration_ms": duration_ms,
                    "dsl_tool": os.environ.get('CURRENT_DSL_TOOL', 'unknown')
                }
                try:
                    with open(REASCRIPT_LOG_FILE, 'a') as f:
                        f.write(json.dumps(log_entry) + '\n')
                except Exception as e:
                    logger.debug(f"Failed to log ReaScript timeout: {e}")
            
            return timeout_response
            
        except Exception as e:
            logger.error(f"Bridge error: {e}")
            error_response = {"ok": False, "error": str(e)}
            
            # Track error if tracking is enabled
            if self.tracking_enabled:
                duration_ms = (time.time() - call_start_time) * 1000
                self.call_tracking.append({
                    "timestamp": call_start_time,
                    "function": func_name,
                    "args": args or [],
                    "response": error_response,
                    "duration_ms": duration_ms,
                    "success": False,
                    "error": str(e)
                })
            
            # Log error if enabled
            if REASCRIPT_LOGGING_ENABLED:
                duration_ms = (time.time() - call_start_time) * 1000
                log_entry = {
                    "timestamp": time.time(),
                    "request_id": self.request_id,
                    "type": "error",
                    "function": func_name,
                    "error": str(e),
                    "duration_ms": duration_ms,
                    "dsl_tool": os.environ.get('CURRENT_DSL_TOOL', 'unknown')
                }
                try:
                    with open(REASCRIPT_LOG_FILE, 'a') as f:
                        f.write(json.dumps(log_entry) + '\n')
                except Exception as e:
                    logger.debug(f"Failed to log ReaScript error: {e}")
            
            return error_response
    
    def start_tracking(self):
        """Start tracking ReaScript calls"""
        self.tracking_enabled = True
        self.call_tracking = []
    
    def stop_tracking(self):
        """Stop tracking and return collected calls"""
        self.tracking_enabled = False
        calls = self.call_tracking.copy()
        self.call_tracking = []
        return calls
    
    def get_tracked_calls(self):
        """Get tracked calls without clearing"""
        return self.call_tracking.copy()

# Singleton instance
bridge = ReaperFileBridge()