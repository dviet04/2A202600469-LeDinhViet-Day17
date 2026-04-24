from typing import TypedDict, List, Dict

class MemoryState(TypedDict):
    messages: List[Dict]
    user_profile: Dict
    episodes: List[Dict]
    semantic_hits: List[str]
    memory_budget: int
