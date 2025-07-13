"""
REAPER MCP Tools Package

This package contains all the tool implementations organized by category.
Each module contains related tools using the modern @mcp.tool() decorator pattern.
"""

# Import all tools to make them available when the package is imported
from .tracks import *
from .midi import *
from .fx import *
from .project import *
from .media_items import *
from .automation import *
from .markers_regions import *
from .time_selection import *
from .transport import *
from .core_api import *

__all__ = [
    # Modules will export their tool names here
]