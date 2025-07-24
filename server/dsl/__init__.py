"""
DSL/Macro layer for natural language REAPER control
"""

from .tools import register_dsl_tools
from .resolvers import ResolverError, DisambiguationNeeded, get_context, reset_context
from .wrappers import OperationResult

__all__ = [
    'register_dsl_tools',
    'ResolverError',
    'DisambiguationNeeded',
    'OperationResult',
    'get_context',
    'reset_context'
]