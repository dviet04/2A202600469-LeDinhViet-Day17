
from agent.state import MemoryState
from agent.router import retrieve_memory
from agent.prompt_builder import build_prompt
from memory.short_term import ShortTermMemory
from memory.profile import ProfileMemory
from memory.episodic import EpisodicMemory
from utils.helpers import detect_profile_update, extract_episode

from utils.config import OPENAI_API_KEY
import openai
import logging

def call_openai_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return "[ERROR] LLM call failed."

class MultiMemoryAgent:
    def __init__(self):
        self.stm = ShortTermMemory()
        self.pfm = ProfileMemory()
        self.epm = EpisodicMemory()
        self.state = MemoryState(
            messages=[],
            user_profile={},
            episodes=[],
            semantic_hits=[],
            memory_budget=1024
        )
        self.user_id = "default_user"

    def run(self, input_text: str) -> str:
        # 1. Update short-term memory
        self.stm.add_message({"role": "user", "content": input_text})
        self.state["messages"] = self.stm.get_messages()
        # 2. Retrieve memory
        self.state = retrieve_memory(self.state, self.user_id)
        # 3. Build prompt
        prompt = build_prompt(self.state)
        # 4. Call OpenAI LLM
        response = call_openai_llm(prompt)
        # 5. Update profile if new fact detected
        profile_update = detect_profile_update(input_text)
        if profile_update:
            key, value = profile_update
            self.pfm.update_profile(key, value)
            self.state["user_profile"] = self.pfm.get_profile(self.user_id)
        # 6. Save episodic memory if event detected
        episode = extract_episode(input_text)
        if episode:
            self.epm.add_episode(episode)
            self.state["episodes"] = self.epm.retrieve_recent(5)
        # Add agent response to short-term memory
        self.stm.add_message({"role": "agent", "content": response})
        self.state["messages"] = self.stm.get_messages()
        return response
