from agent.state import MemoryState
from memory.short_term import ShortTermMemory
from memory.profile import ProfileMemory
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory

# Router: fetch from all memory types and populate state

def retrieve_memory(state: MemoryState, user_id: str = "default_user") -> MemoryState:
    stm = ShortTermMemory()
    pfm = ProfileMemory()
    epm = EpisodicMemory()
    semm = SemanticMemory()

    state["user_profile"] = pfm.get_profile(user_id)
    state["episodes"] = epm.retrieve_recent(5)
    state["semantic_hits"] = semm.search(state["messages"][-1]["content"] if state["messages"] else "")
    return state
