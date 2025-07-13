"""
REAPER MCP Tools Package

This package contains all the tool implementations organized by category.
Each module contains related tools using the modern @mcp.tool() decorator pattern.
"""

# Tool modules - each module contains functions and a register function
# The register function is called by the main server to register all tools
# with the MCP instance using the @mcp.tool() decorator