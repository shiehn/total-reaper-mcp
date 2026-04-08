"""
Capability gate meta-tools.

Always registered regardless of profile. Allow Claude to discover and
dynamically load tool categories mid-session without a server restart.

Usage flow:
  1. User asks for something the current profile can't do.
  2. Claude calls list_capabilities() to see what's available.
  3. Claude calls enable_capability("Category Name") to load it.
  4. FastMCP sends tools/list_changed notification.
  5. Claude re-fetches tool list and proceeds with the real task.
"""

import logging

logger = logging.getLogger(__name__)

# One-line descriptions shown in list_capabilities() output.
CATEGORY_DESCRIPTIONS = {
    "DSL":                                "Natural language macro tools (track, MIDI, FX, transport)",
    "Core API":                           "Low-level REAPER API passthrough",
    "Tracks":                             "Track create, delete, rename, volume, pan, mute, solo",
    "Media Items":                        "Item create, move, resize, split, glue",
    "MIDI":                               "Insert/edit MIDI notes and CC events",
    "FX":                                 "Add/remove VST effects, get/set presets and parameters",
    "Project":                            "Save, load, project info",
    "Transport":                          "Play, stop, record, cursor position, BPM",
    "Time Selection":                     "Get/set loop and time selection boundaries",
    "Markers":                            "Add/delete markers and regions",
    "Automation & Envelopes":             "Read/write automation envelopes",
    "Rendering & Freezing":               "Bounce, freeze, render to file",
    "GUI & Interface":                    "Show/hide REAPER windows and panels",
    "Take FX":                            "FX on individual takes",
    "Track FX Extended":                  "Get/set FX presets by name or index, navigate presets, param control",
    "Project State Management":           "Get/set arbitrary project state chunks",
    "Media Items Extended":               "Extended item operations (color, notes, properties)",
    "Routing & Sends":                    "Create and configure track sends and receives",
    "Audio Accessor & Analysis":          "Read raw audio sample data for analysis",
    "MIDI Editor & Piano Roll":           "Piano roll note selection, CC editing, quantise",
    "Color Management":                   "Track and item color get/set",
    "Tempo & Time Signature":             "Insert and query tempo/time-sig markers",
    "Recording Operations":               "Arm tracks, set input, monitor mode",
    "Envelope Extended":                  "Advanced envelope point and shape control",
    "Time/Tempo Extended":                "Extended timeline and tempo utilities",
    "Track Management Extended":          "Folder tracks, track grouping, TCP/MCP layout",
    "Action Management":                  "Run REAPER actions by ID or name",
    "File I/O & Project Management":      "File paths, recent projects, project notes",
    "Layouts & Screensets":               "Save/recall screensets and layouts",
    "Take Management Extended":           "Multi-take operations, active take switching",
    "Regions & Markers Extended":         "Bulk region/marker operations",
    "Analysis Tools":                     "Peak analysis, loudness, spectral tools",
    "Video & Visual Media":               "Video item properties and display",
    "Peak & Waveform Display":            "Waveform peak cache and display control",
    "Script Extension Management":        "ReaScript/extension state storage",
    "Project Tab Management":             "Multi-project tab open/close/switch",
    "Advanced MIDI Analysis & Generation":"Advanced MIDI pattern analysis and generation",
    "Loop & Time Selection Management":   "Loop points, duplicate time selection",
    "Bounce & Render Operations":         "Track bounce, stem render, offline FX apply",
    "Groove & Quantization Tools":        "Groove templates, humanise, swing",
    "Bus Routing & Mixing Workflows":     "Create submix buses, parallel compression, reverb sends",
    "Tempo & Time Management":            "Combined tempo/time utilities",
    "Advanced MIDI Generation":           "Generate chord progressions and scale runs",
}


def register_capability_tools(mcp, category_registry: dict, loaded_categories: set):
    """
    Register list_capabilities and enable_capability into the running MCP instance.

    Args:
        mcp:                The FastMCP instance.
        category_registry:  The CATEGORY_REGISTRY dict from app.py (name → register_func).
        loaded_categories:  The mutable set tracking which categories are active.
                            Mutations here are visible in app.py because sets are passed by reference.
    """

    @mcp.tool()
    async def list_capabilities() -> str:
        """
        List all tool categories that exist in this server but are not yet loaded in this session.
        Call this whenever you cannot find the right tool for what the user needs — there may be
        an unloaded category that provides it.
        """
        unloaded = []
        for name in category_registry:
            if name not in loaded_categories:
                desc = CATEGORY_DESCRIPTIONS.get(name, "")
                unloaded.append(f"  {name}" + (f" — {desc}" if desc else ""))

        if not unloaded:
            return "All available categories are already loaded in this session."

        lines = ["These categories are available but not loaded:", ""] + unloaded + [
            "",
            "Call enable_capability(category) to load any of them.",
        ]
        return "\n".join(lines)

    @mcp.tool()
    async def enable_capability(category: str) -> str:
        """
        Dynamically load a tool category into this session.
        After calling this the new tools are immediately available — no server restart needed.
        Use list_capabilities() first to see what category names are available.

        Args:
            category: Exact category name as returned by list_capabilities()
        """
        if category in loaded_categories:
            return f"'{category}' is already loaded in this session."

        register_func = category_registry.get(category)
        if register_func is None:
            close = [c for c in category_registry if category.lower() in c.lower()]
            hint = f" Did you mean one of: {', '.join(close)}?" if close else ""
            return f"Unknown category '{category}'.{hint} Call list_capabilities() to see valid names."

        try:
            count = register_func(mcp)
            loaded_categories.add(category)
            logger.info(f"Dynamically loaded category '{category}': {count} tools")
            return (
                f"Loaded '{category}': {count} tools are now available.\n"
                f"The tool list has been updated — you can use the new tools immediately."
            )
        except Exception as e:
            logger.error(f"Failed to load category '{category}': {e}")
            return f"Failed to load '{category}': {e}"

    return 2  # two tools registered
