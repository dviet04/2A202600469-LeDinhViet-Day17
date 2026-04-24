from agent.state import MemoryState
from utils.tokenizer import count_tokens

def build_prompt(state: MemoryState) -> str:
    budget = state.get("memory_budget", 1024)
    prompt_sections = []
    # User Profile
    profile = state.get("user_profile", {})
    profile_str = "\n".join([f"{k}: {v}" for k, v in profile.items()])
    prompt_sections.append(f"[USER PROFILE]\n{profile_str}")
    # Episodic Memory
    episodes = state.get("episodes", [])
    episodes_str = "\n".join([str(ep) for ep in episodes])
    prompt_sections.append(f"[EPISODIC MEMORY]\n{episodes_str}")
    # Semantic Memory
    semantic_hits = state.get("semantic_hits", [])
    semantic_str = "\n".join(semantic_hits)
    prompt_sections.append(f"[SEMANTIC MEMORY]\n{semantic_str}")
    # Recent Conversation
    messages = state.get("messages", [])
    conv_str = "\n".join([f"{m['role']}: {m['content']}" for m in messages[-5:]])
    prompt_sections.append(f"[RECENT CONVERSATION]\n{conv_str}")
    # Current Question
    if messages:
        prompt_sections.append(f"[CURRENT QUESTION]\n{messages[-1]['content']}")
    # Trim to budget
    prompt = "\n\n".join(prompt_sections)
    while count_tokens(prompt) > budget and len(messages) > 1:
        messages.pop(0)
        conv_str = "\n".join([f"{m['role']}: {m['content']}" for m in messages[-5:]])
        prompt_sections[3] = f"[RECENT CONVERSATION]\n{conv_str}"
        prompt = "\n\n".join(prompt_sections)
    return prompt
