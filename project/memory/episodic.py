# EpisodicMemory: stores past events/tasks
import json
import os

EPISODIC_PATH = os.path.join(os.path.dirname(__file__), '../data/episodic.json')

class EpisodicMemory:
    def __init__(self):
        self.episodes = self._load_episodes()

    def _load_episodes(self):
        if os.path.exists(EPISODIC_PATH):
            with open(EPISODIC_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _save_episodes(self):
        with open(EPISODIC_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.episodes, f, ensure_ascii=False, indent=2)

    def add_episode(self, event):
        self.episodes.append(event)
        self._save_episodes()

    def retrieve_recent(self, n=5):
        return self.episodes[-n:]
