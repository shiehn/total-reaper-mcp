"""Synchronous bridge wrapper for tools that need sync API calls."""

import asyncio
from typing import Dict, Any
from ..bridge import bridge


class ReaperBridge:
    """Synchronous wrapper for the async bridge."""
    
    @staticmethod
    def send_request(request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a synchronous request to REAPER.
        
        Args:
            request: Dict containing action and parameters
            
        Returns:
            Response dict from REAPER
        """
        # Extract the action and parameters
        action = request.get("action")
        
        # Build args list based on the request
        args = []
        
        # Map common request patterns to Lua function parameters
        if "proj" in request:
            args.append(request["proj"])
        if "project" in request:
            args.append(request["project"])
        if "trackidx" in request:
            args.append(request["trackidx"])
        if "track" in request:
            args.append(request["track"])
        if "item" in request:
            args.append(request["item"])
        if "take" in request:
            args.append(request["take"])
        if "idx" in request:
            args.append(request["idx"])
        if "index" in request:
            args.append(request["index"])
        if "selitem" in request:
            args.append(request["selitem"])
        if "parmname" in request:
            args.append(request["parmname"])
        if "newvalue" in request:
            args.append(request["newvalue"])
        if "value" in request:
            args.append(request["value"])
        if "str" in request:
            args.append(request["str"])
        if "setnewvalue" in request:
            args.append(request["setnewvalue"])
        if "stringNeedBig" in request:
            args.append(request["stringNeedBig"])
        if "command" in request:
            args.append(request["command"])
        if "val" in request:
            args.append(request["val"])
        if "is_set" in request:
            args.append(request["is_set"])
        if "desc" in request:
            args.append(request["desc"])
        
        # Special handling for certain actions
        if action == "GetSet_LoopTimeRange":
            args = [
                request.get("isSet", False),
                request.get("isLoop", True),
                request.get("startOut", 0.0),
                request.get("endOut", 0.0),
                request.get("allowautoseek", False)
            ]
        elif action == "CreateNewMIDIItemInProj":
            args = [
                request.get("track"),
                request.get("starttime"),
                request.get("endtime"),
                request.get("qnInOptional", False)
            ]
        elif action == "GetSetProjectGrid":
            args = [
                request.get("project", 0),
                request.get("set", False),
                request.get("division", 0.25),
                request.get("swingmode", 0),
                request.get("swingamt", 0)
            ]
        
        # Run the async call synchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(bridge.call_lua(action, args))
            
            # Transform the result to match expected format
            response = {"result": True}
            
            # Map common return patterns
            if isinstance(result, dict):
                response.update(result)
                
                # Special handling for GetSet_LoopTimeRange
                if action == "GetSet_LoopTimeRange" and "ret" in result:
                    ret = result.get("ret", [0.0, 0.0])
                    if len(ret) >= 2:
                        response["startOut"] = ret[0]
                        response["endOut"] = ret[1]
                
                # Map 'ok' to 'result' if needed
                if "ok" in result and "result" not in result:
                    response["result"] = result["ok"]
                    
            elif isinstance(result, (int, float, str, bool)):
                # Single value returns
                if "track" in action.lower():
                    response["track"] = result
                elif "item" in action.lower():
                    response["item"] = result
                elif "count" in action.lower():
                    response["count"] = result
                else:
                    response["value"] = result
            
            return response
            
        except Exception as e:
            return {"result": False, "error": str(e)}
        finally:
            loop.close()