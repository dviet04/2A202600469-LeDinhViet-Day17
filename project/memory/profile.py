# ProfileMemory: manages user profile facts
import json
import os

PROFILE_PATH = os.path.join(os.path.dirname(__file__), '../data/profile.json')

class ProfileMemory:
    def __init__(self):
        self.profile = self._load_profile()

    def _load_profile(self):
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_profile(self):
        with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)

    def get_profile(self, user_id):
        return self.profile.get(user_id, {})

    def update_profile(self, key, value, user_id="default_user"):
        if user_id not in self.profile:
            self.profile[user_id] = {}
        # Overwrite conflict: new value replaces old
        self.profile[user_id][key] = value
        self._save_profile()
