"""
Smart resolvers for natural language references to REAPER entities

These resolvers handle flexible references to tracks, items, time ranges, etc.
They support fuzzy matching, content analysis, and context awareness.
"""

import re
import json
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)

@dataclass
class TrackRef:
    """Reference to a resolved track"""
    index: int
    guid: str
    name: str
    role: Optional[str] = None
    has_midi: bool = False
    has_audio: bool = False
    fx_names: List[str] = None
    confidence: float = 0.0
    
    def to_dict(self):
        return {
            "index": self.index,
            "guid": self.guid,
            "name": self.name,
            "role": self.role,
            "confidence": self.confidence
        }

@dataclass
class TimeRef:
    """Reference to a resolved time range"""
    start: float
    end: float
    bars: Optional[int] = None
    
    def to_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "bars": self.bars
        }

@dataclass
class ItemRef:
    """Reference to a resolved item"""
    index: int
    track_index: int
    position: float
    length: float
    name: Optional[str] = None
    is_midi: bool = False
    confidence: float = 0.0
    
    def to_dict(self):
        return {
            "index": self.index,
            "track_index": self.track_index,
            "position": self.position,
            "length": self.length,
            "name": self.name,
            "is_midi": self.is_midi
        }

class SessionContext:
    """Maintains context about recent operations"""
    def __init__(self):
        self.last_track: Optional[TrackRef] = None
        self.last_time: Optional[TimeRef] = None
        self.last_items: List[ItemRef] = []
        self.track_references: Dict[str, int] = {}  # name -> count
        
    def update_track(self, track: TrackRef):
        self.last_track = track
        if track.name:
            self.track_references[track.name] = self.track_references.get(track.name, 0) + 1
    
    def update_time(self, time: TimeRef):
        self.last_time = time
        
    def update_items(self, items: List[ItemRef]):
        self.last_items = items

# Global session context
_context = SessionContext()

class ResolverError(Exception):
    """Base exception for resolver errors"""
    def __init__(self, message: str, candidates: List[Any] = None):
        super().__init__(message)
        self.candidates = candidates or []

class DisambiguationNeeded(ResolverError):
    """Multiple matches found, need user clarification"""
    pass

def fuzzy_match_score(s1: str, s2: str) -> float:
    """Calculate fuzzy match score between two strings"""
    if not s1 or not s2:
        return 0.0
    
    # Exact match (case insensitive)
    if s1.lower() == s2.lower():
        return 1.0
    
    # Check if one contains the other
    s1_lower, s2_lower = s1.lower(), s2.lower()
    if s1_lower in s2_lower or s2_lower in s1_lower:
        return 0.8
    
    # Use sequence matcher for similarity
    return SequenceMatcher(None, s1_lower, s2_lower).ratio()

def parse_role_from_name(name: str) -> Optional[str]:
    """Extract role from track name"""
    name_lower = name.lower()
    
    # Common role patterns
    role_patterns = {
        'bass': ['bass', 'sub', 'low'],
        'drums': ['drum', 'kit', 'beat', 'perc', 'kick', 'snare', 'hat'],
        'keys': ['key', 'piano', 'synth', 'pad', 'organ'],
        'guitar': ['guitar', 'gtr'],
        'vocals': ['vocal', 'vox', 'voice'],
        'lead': ['lead', 'melody'],
        'strings': ['string', 'violin', 'cello'],
        'brass': ['brass', 'horn', 'trumpet', 'sax']
    }
    
    for role, patterns in role_patterns.items():
        for pattern in patterns:
            if pattern in name_lower:
                return role
    
    return None

async def resolve_track(bridge, selector: Union[str, int, Dict[str, Any]]) -> TrackRef:
    """
    Resolve a flexible track reference to a specific track
    
    Selector can be:
    - int: track index (0-based)
    - str: track name or role (fuzzy matched)
    - dict: complex selector with multiple criteria
      - index: exact track index
      - name: track name (fuzzy matched)
      - role: track role (bass, drums, etc)
      - has_fx: track must have this effect
      - has_midi: track must have MIDI items
      - last: use last referenced track
    """
    from ..bridge import bridge as reaper_bridge
    
    # Handle simple cases
    if isinstance(selector, int):
        return await _get_track_by_index(bridge, selector)
    
    if isinstance(selector, str):
        # Check for special keywords
        if selector.lower() in ['last', 'that', 'previous']:
            if _context.last_track:
                return _context.last_track
            raise ResolverError("No previous track reference found")
        
        # Try as name/role
        selector = {"name": selector}
    
    # Build candidate list
    track_count = await _get_track_count(bridge)
    candidates = []
    
    for i in range(track_count):
        track_info = await _get_track_info(bridge, i)
        if not track_info:
            continue
            
        score = _score_track(track_info, selector)
        if score > 0:
            candidates.append((track_info, score))
    
    if not candidates:
        raise ResolverError(f"No tracks found matching criteria: {selector}")
    
    # Sort by score
    candidates.sort(key=lambda x: x[1], reverse=True)
    
    # Check if we need disambiguation
    if len(candidates) > 1 and candidates[0][1] < 0.8:
        # Multiple matches with low confidence
        raise DisambiguationNeeded(
            "Multiple tracks found, please be more specific",
            [c[0] for c in candidates[:3]]  # Top 3 candidates
        )
    
    # Use best match
    best_track = candidates[0][0]
    _context.update_track(best_track)
    return best_track

def _score_track(track: TrackRef, selector: Dict[str, Any]) -> float:
    """Score how well a track matches the selector"""
    scores = []
    
    # Exact index match
    if 'index' in selector and track.index == selector['index']:
        return 1.0
    
    # Name matching
    if 'name' in selector:
        name_score = fuzzy_match_score(selector['name'], track.name)
        scores.append(name_score)
        
        # Also check against role
        if track.role:
            role_score = fuzzy_match_score(selector['name'], track.role)
            scores.append(role_score * 0.8)  # Slightly lower weight for role match
    
    # Role matching
    if 'role' in selector and track.role:
        scores.append(fuzzy_match_score(selector['role'], track.role))
    
    # FX matching
    if 'has_fx' in selector and track.fx_names:
        fx_matches = any(
            fuzzy_match_score(selector['has_fx'], fx) > 0.7 
            for fx in track.fx_names
        )
        scores.append(1.0 if fx_matches else 0.0)
    
    # Content matching
    if 'has_midi' in selector:
        scores.append(1.0 if track.has_midi == selector['has_midi'] else 0.0)
    
    if 'has_audio' in selector:
        scores.append(1.0 if track.has_audio == selector['has_audio'] else 0.0)
    
    # Context boost
    if _context.last_track and track.guid == _context.last_track.guid:
        scores.append(0.3)  # Small boost for recently used
    
    return max(scores) if scores else 0.0

async def _get_track_count(bridge) -> int:
    """Get the number of tracks in the project"""
    # Use GetAllTracksInfo which we know works
    result = await bridge.call_lua("GetAllTracksInfo", [])
    if result.get("ok"):
        tracks = result.get("tracks", [])
        return len(tracks)
    return 0

async def _get_track_by_index(bridge, index: int) -> TrackRef:
    """Get track info by index"""
    track_info = await _get_track_info(bridge, index)
    if track_info:
        return track_info
    raise ResolverError(f"Track at index {index} not found")

async def _get_track_info(bridge, index: int) -> Optional[TrackRef]:
    """Get detailed track information"""
    result = await bridge.call_lua("GetTrackInfo", [index])
    if not result.get("ok"):
        return None
    
    info = result.get("info", {})
    
    track = TrackRef(
        index=index,
        guid=info.get("guid", ""),
        name=info.get("name", f"Track {index + 1}"),
        has_midi=info.get("has_midi", False),
        has_audio=info.get("has_audio", False),
        fx_names=info.get("fx_names", []),
        confidence=1.0
    )
    
    # Try to infer role from name
    track.role = parse_role_from_name(track.name)
    
    return track

async def resolve_time(bridge, selector: Union[str, float, Dict[str, Any]]) -> TimeRef:
    """
    Resolve a flexible time reference
    
    Selector can be:
    - float: time in seconds
    - str: "8 bars", "cursor", "selection", "loop"
    - dict: {bars: 8, from: "cursor"}, {start: 0, end: 10}
    """
    if isinstance(selector, (int, float)):
        # Assume it's a duration from cursor
        cursor_pos = await _get_cursor_position(bridge)
        return TimeRef(start=cursor_pos, end=cursor_pos + float(selector))
    
    if isinstance(selector, str):
        return await _parse_time_string(bridge, selector)
    
    if isinstance(selector, dict):
        return await _parse_time_dict(bridge, selector)
    
    raise ResolverError(f"Invalid time selector: {selector}")

async def _parse_time_string(bridge, time_str: str) -> TimeRef:
    """Parse time string like '8 bars', 'selection', etc"""
    time_str = time_str.lower().strip()
    
    # Special keywords
    if time_str in ['selection', 'selected']:
        return await _get_time_selection(bridge)
    
    if time_str in ['loop', 'loop_region']:
        return await _get_loop_region(bridge)
    
    if time_str == 'cursor':
        pos = await _get_cursor_position(bridge)
        return TimeRef(start=pos, end=pos)
    
    # Parse bars/beats
    bars_match = re.match(r'(\d+)\s*bars?', time_str)
    if bars_match:
        bars = int(bars_match.group(1))
        cursor = await _get_cursor_position(bridge)
        duration = await _bars_to_time(bridge, bars, cursor)
        return TimeRef(start=cursor, end=cursor + duration, bars=bars)
    
    # Parse time format (MM:SS or HH:MM:SS)
    time_match = re.match(r'(\d+):(\d+)(?::(\d+))?', time_str)
    if time_match:
        mins = int(time_match.group(1))
        secs = int(time_match.group(2))
        hours = int(time_match.group(3) or 0)
        total_secs = hours * 3600 + mins * 60 + secs
        return TimeRef(start=0, end=total_secs)
    
    raise ResolverError(f"Cannot parse time: {time_str}")

async def _parse_time_dict(bridge, selector: Dict[str, Any]) -> TimeRef:
    """Parse time dictionary selector"""
    if 'start' in selector and 'end' in selector:
        return TimeRef(start=float(selector['start']), end=float(selector['end']))
    
    if 'bars' in selector:
        bars = selector['bars']
        from_pos = 0.0
        
        if 'from' in selector:
            if selector['from'] == 'cursor':
                from_pos = await _get_cursor_position(bridge)
            elif isinstance(selector['from'], (int, float)):
                from_pos = float(selector['from'])
        
        duration = await _bars_to_time(bridge, bars, from_pos)
        return TimeRef(start=from_pos, end=from_pos + duration, bars=bars)
    
    if 'region' in selector:
        return await _get_region_time(bridge, selector['region'])
    
    if 'marker' in selector:
        marker_pos = await _get_marker_position(bridge, selector['marker'])
        return TimeRef(start=marker_pos, end=marker_pos)
    
    raise ResolverError(f"Invalid time selector: {selector}")

async def _get_cursor_position(bridge) -> float:
    """Get current edit cursor position"""
    result = await bridge.call_lua("GetCursorPosition", [])
    if result.get("ok"):
        return result.get("ret", 0.0)
    return 0.0

async def _get_time_selection(bridge) -> TimeRef:
    """Get current time selection"""
    result = await bridge.call_lua("GetTimeSelection", [])
    if result.get("ok"):
        start = result.get("start", 0.0)
        end = result.get("end", 0.0)
        if start == end:
            raise ResolverError("No time selection active")
        return TimeRef(start=start, end=end)
    raise ResolverError("Failed to get time selection")

async def _get_loop_region(bridge) -> TimeRef:
    """Get current loop region"""
    result = await bridge.call_lua("GetLoopTimeRange", [])
    if result.get("ok"):
        start = result.get("start", 0.0)
        end = result.get("end", 0.0)
        if start == end:
            raise ResolverError("No loop region set")
        return TimeRef(start=start, end=end)
    raise ResolverError("Failed to get loop region")

async def _bars_to_time(bridge, bars: int, start_pos: float = 0.0) -> float:
    """Convert bars to time duration"""
    result = await bridge.call_lua("BarsToTime", [bars, start_pos])
    if result.get("ok"):
        return result.get("ret", 0.0)
    # Fallback: assume 120 BPM, 4/4
    return bars * 4 * 60 / 120

async def _get_region_time(bridge, region_name: str) -> TimeRef:
    """Get time range for a named region"""
    result = await bridge.call_lua("FindRegion", [region_name])
    if result.get("ok") and result.get("found"):
        return TimeRef(
            start=result.get("start", 0.0),
            end=result.get("end", 0.0)
        )
    raise ResolverError(f"Region not found: {region_name}")

async def _get_marker_position(bridge, marker_name: str) -> float:
    """Get position of a named marker"""
    result = await bridge.call_lua("FindMarker", [marker_name])
    if result.get("ok") and result.get("found"):
        return result.get("position", 0.0)
    raise ResolverError(f"Marker not found: {marker_name}")

async def resolve_items(bridge, selector: Union[str, Dict[str, Any]]) -> List[ItemRef]:
    """
    Resolve item references
    
    Selector can be:
    - str: "selected", "all", "last"
    - dict: {track: track_selector, time: time_selector}
    """
    if isinstance(selector, str):
        if selector == "selected":
            return await _get_selected_items(bridge)
        elif selector == "all":
            return await _get_all_items(bridge)
        elif selector == "last":
            if _context.last_items:
                return _context.last_items
            raise ResolverError("No previous item reference")
    
    if isinstance(selector, dict):
        items = []
        
        # Filter by track
        if 'track' in selector:
            track = await resolve_track(bridge, selector['track'])
            items = await _get_track_items(bridge, track.index)
        else:
            items = await _get_all_items(bridge)
        
        # Filter by time
        if 'time' in selector:
            time_ref = await resolve_time(bridge, selector['time'])
            items = [i for i in items if _item_in_time_range(i, time_ref)]
        
        return items
    
    raise ResolverError(f"Invalid item selector: {selector}")

def _item_in_time_range(item: ItemRef, time_ref: TimeRef) -> bool:
    """Check if item overlaps with time range"""
    item_end = item.position + item.length
    return not (item_end <= time_ref.start or item.position >= time_ref.end)

async def _get_selected_items(bridge) -> List[ItemRef]:
    """Get all selected items"""
    result = await bridge.call_lua("GetSelectedItems", [])
    if result.get("ok"):
        items = []
        for item_data in result.get("items", []):
            items.append(_parse_item_data(item_data))
        return items
    return []

async def _get_all_items(bridge) -> List[ItemRef]:
    """Get all items in project"""
    result = await bridge.call_lua("GetAllItems", [])
    if result.get("ok"):
        items = []
        for item_data in result.get("items", []):
            items.append(_parse_item_data(item_data))
        return items
    return []

async def _get_track_items(bridge, track_index: int) -> List[ItemRef]:
    """Get all items on a specific track"""
    result = await bridge.call_lua("GetTrackItems", [track_index])
    if result.get("ok"):
        items = []
        for item_data in result.get("items", []):
            items.append(_parse_item_data(item_data))
        return items
    return []

def _parse_item_data(data: Dict[str, Any]) -> ItemRef:
    """Parse item data from Lua response"""
    return ItemRef(
        index=data.get("index", 0),
        track_index=data.get("track_index", 0),
        position=data.get("position", 0.0),
        length=data.get("length", 0.0),
        name=data.get("name"),
        is_midi=data.get("is_midi", False),
        confidence=1.0
    )

# Public API
def get_context() -> SessionContext:
    """Get the current session context"""
    return _context

def reset_context():
    """Reset session context"""
    global _context
    _context = SessionContext()