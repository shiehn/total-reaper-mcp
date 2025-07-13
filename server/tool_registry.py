"""
Tool Registry Helper for Modern MCP Pattern

This module provides utilities to automatically register tools from modules,
reducing boilerplate code in the main server file.
"""

import inspect
import asyncio
from typing import Callable, Dict, List, Any, get_type_hints
from functools import wraps


class ToolRegistry:
    """Helper class to manage tool registration for MCP"""
    
    def __init__(self, mcp_instance):
        """Initialize with an MCP instance (FastMCP)"""
        self.mcp = mcp_instance
        self.registered_tools = {}
        
    def register_module_tools(self, module, prefix: str = ""):
        """
        Automatically register all async functions from a module as MCP tools.
        
        Args:
            module: The module containing tool functions
            prefix: Optional prefix for tool names
        """
        for name, obj in inspect.getmembers(module):
            # Skip private functions and non-async functions
            if name.startswith('_') or not inspect.iscoroutinefunction(obj):
                continue
                
            # Get function signature and docstring
            sig = inspect.signature(obj)
            doc = inspect.getdoc(obj) or f"Execute {name}"
            
            # Create tool name
            tool_name = f"{prefix}{name}" if prefix else name
            
            # Register the tool
            self.register_tool(tool_name, obj, doc)
            
    def register_tool(self, name: str, func: Callable, description: str = None):
        """
        Register a single tool with the MCP instance.
        
        Args:
            name: Tool name
            func: The async function to register
            description: Tool description (uses docstring if not provided)
        """
        if description is None:
            description = inspect.getdoc(func) or f"Execute {name}"
            # Take only the first line of the docstring
            description = description.split('\n')[0]
        
        # Create a wrapper that matches MCP's expected signature
        @wraps(func)
        async def tool_wrapper(**kwargs):
            # Filter out any MCP-specific parameters that the function doesn't expect
            sig = inspect.signature(func)
            filtered_kwargs = {}
            for param_name, param in sig.parameters.items():
                if param_name in kwargs:
                    filtered_kwargs[param_name] = kwargs[param_name]
                elif param.default is not param.empty:
                    # Use default value if not provided
                    pass
                else:
                    # Required parameter missing
                    raise ValueError(f"Missing required parameter: {param_name}")
            
            # Call the original function
            return await func(**filtered_kwargs)
        
        # Copy the original function's annotations
        tool_wrapper.__annotations__ = func.__annotations__.copy()
        
        # Register with MCP using the decorator
        decorated = self.mcp.tool()(tool_wrapper)
        
        # Store reference
        self.registered_tools[name] = {
            'function': func,
            'wrapper': decorated,
            'description': description
        }
        
        return decorated
    
    def register_tools_from_dict(self, tools_dict: Dict[str, Dict[str, Any]]):
        """
        Register tools from a dictionary specification.
        
        Args:
            tools_dict: Dictionary with tool specifications
                {
                    'tool_name': {
                        'function': async_function,
                        'description': 'Tool description',
                        'category': 'optional_category'
                    }
                }
        """
        for tool_name, tool_spec in tools_dict.items():
            func = tool_spec.get('function')
            desc = tool_spec.get('description')
            
            if func and inspect.iscoroutinefunction(func):
                self.register_tool(tool_name, func, desc)
    
    def get_registered_tools(self) -> List[str]:
        """Get list of all registered tool names"""
        return list(self.registered_tools.keys())
    
    def get_tool_info(self, name: str) -> Dict[str, Any]:
        """Get information about a registered tool"""
        return self.registered_tools.get(name, {})


def create_tool_wrapper(module_func: Callable) -> Callable:
    """
    Create a wrapper function that can be decorated with @mcp.tool()
    
    This is useful for creating inline tool registrations in the main server file.
    """
    @wraps(module_func)
    async def wrapper(**kwargs):
        # Get the function signature
        sig = inspect.signature(module_func)
        
        # Filter kwargs to match function parameters
        filtered_kwargs = {}
        for param_name in sig.parameters:
            if param_name in kwargs:
                filtered_kwargs[param_name] = kwargs[param_name]
        
        # Call the module function
        return await module_func(**filtered_kwargs)
    
    # Preserve function metadata
    wrapper.__name__ = module_func.__name__
    wrapper.__doc__ = module_func.__doc__
    wrapper.__annotations__ = module_func.__annotations__.copy()
    
    return wrapper


def batch_register_tools(mcp_instance, tool_modules: Dict[str, Any]):
    """
    Batch register tools from multiple modules.
    
    Args:
        mcp_instance: The FastMCP instance
        tool_modules: Dictionary mapping module names to modules
            {
                'tracks': tracks_module,
                'midi': midi_module,
                ...
            }
    
    Returns:
        ToolRegistry instance with all registered tools
    """
    registry = ToolRegistry(mcp_instance)
    
    for module_name, module in tool_modules.items():
        print(f"Registering tools from {module_name}...")
        registry.register_module_tools(module)
    
    return registry