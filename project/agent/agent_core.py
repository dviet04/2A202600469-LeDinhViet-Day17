
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
import time
import threading

# Config logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

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

        # 5. Update profile if new fact detected (background)
        def save_profile_bg(profile_dict):
            try:
                for key, value in profile_dict.items():
                    self.pfm.update_profile(key, value)
                    logging.info(f"[BG Thread] Profile updated: {key} = {value}")
            except Exception as e:
                logging.error(f"[BG Thread] Error saving profile: {e}")

        profile_update = detect_profile_update(input_text)
        profile_thread = None
        if profile_update:
            profile_thread = threading.Thread(target=save_profile_bg, args=(profile_update,), daemon=False)
            profile_thread.start()

        # 6. Save episodic memory if event detected (background)
        def save_episode_bg(episode):
            try:
                self.epm.add_episode(episode)
                logging.info(f"[BG Thread] Episode saved: {episode}")
            except Exception as e:
                logging.error(f"[BG Thread] Error saving episode: {e}")

        import uuid
        current_session_id = str(uuid.uuid4())
        episode = extract_episode(input_text, session_id=current_session_id)
        episode_thread = None
        if episode:
            episode_thread = threading.Thread(target=save_episode_bg, args=(episode,), daemon=False)
            episode_thread.start()

        # Add agent response to short-term memory
        self.stm.add_message({"role": "agent", "content": response})
        self.state["messages"] = self.stm.get_messages()

        # WAIT for background threads to complete BEFORE returning
        # This ensures file is written before we return
        if profile_thread:
            profile_thread.join(timeout=2)
            logging.info("[Main] Profile thread completed")
        if episode_thread:
            episode_thread.join(timeout=2)
            logging.info("[Main] Episode thread completed")
        
        # AFTER threads complete, reload instances to get fresh data from files
        # This ensures next turn sees the updated memory from this turn
        self.pfm = ProfileMemory()  # Reload from file
        self.epm = EpisodicMemory()  # Reload from file
        self.state["user_profile"] = self.pfm.get_profile(self.user_id)
        self.state["episodes"] = self.epm.retrieve_recent(5)
        logging.info(f"[Main] State reloaded: profile={self.state['user_profile']}, episodes={len(self.state['episodes'])}")

        return response
