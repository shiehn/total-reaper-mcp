"""
Tool profiles for different use cases and LLM providers
"""

# Define tool profiles with their included categories
TOOL_PROFILES = {
    "groq-essential": {
        "name": "Groq Essential",
        "description": "Core REAPER functionality for Groq (max 128 tools)",
        "categories": [
            "Tracks",  # Track management
            "Transport",  # Play, stop, record
            "Media Items",  # Basic item operations
            "FX",  # Effects management
            "MIDI",  # MIDI operations
        ]
    },
    "groq-extended": {
        "name": "Groq Extended",
        "description": "Extended functionality that may exceed 128 tools",
        "categories": [
            "Tracks",  # Track management
            "Transport",  # Play, stop, record
            "Media Items",  # Basic item operations
            "FX",  # Effects management
            "MIDI",  # MIDI operations
            "Project",  # Project operations
            "Time Selection",  # Time selection
            "Markers",  # Markers and regions
        ]
    },
    "minimal": {
        "name": "Minimal",
        "description": "Bare minimum tools for testing",
        "categories": [
            "Tracks",
            "Transport",
            "Project",
        ]
    },
    "midi-production": {
        "name": "MIDI Production",
        "description": "Tools for MIDI-focused workflows",
        "categories": [
            "Tracks",
            "Transport", 
            "MIDI",
            "MIDI Editor & Piano Roll",
            "Advanced MIDI Analysis & Generation",
            "Advanced MIDI Generation",
            "Time Selection",
            "Tempo & Time Signature",
        ]
    },
    "mixing": {
        "name": "Mixing",
        "description": "Tools for mixing and mastering",
        "categories": [
            "Tracks",
            "FX",
            "Track FX Extended",
            "Routing & Sends",
            "Bus Routing & Mixing Workflows",
            "Automation & Envelopes",
            "Rendering & Freezing",
        ]
    },
    "full": {
        "name": "Full",
        "description": "All available tools (may cause issues with some LLMs)",
        "categories": None  # None means all categories
    },
    "dsl": {
        "name": "DSL/Macros",
        "description": "Natural language friendly DSL tools for common workflows",
        "categories": [
            "DSL"  # Just the DSL tools
        ]
    },
    "dsl-production": {
        "name": "DSL Production",
        "description": "DSL tools plus essential MIDI and track management",
        "categories": [
            "DSL",
            "Advanced MIDI Generation",  # For external MIDI generation
            "FX",  # For adding instruments
            "Rendering & Freezing"  # For bouncing
        ]
    }
}

def get_profile_categories(profile_name):
    """Get the list of categories for a given profile"""
    profile = TOOL_PROFILES.get(profile_name, TOOL_PROFILES["full"])
    return profile.get("categories", None)