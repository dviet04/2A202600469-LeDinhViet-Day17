# ProfileMemory: manages user profile facts using Redis
import json
import os
import logging

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logging.warning("[Profile] Redis not available, falling back to JSON")

PROFILE_PATH = os.path.join(os.path.dirname(__file__), '../data/profile.json')

class ProfileMemory:
    def __init__(self, redis_host="localhost", redis_port=6379, redis_db=0):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.profile = {}
        
        # Try to connect to Redis
        self.redis_client = None
        self.use_redis = False
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    decode_responses=True
                )
                # Test connection
                self.redis_client.ping()
                self.use_redis = True
                logging.info("[Profile] Connected to Redis")
            except Exception as e:
                logging.warning(f"[Profile] Redis connection failed: {e}, falling back to JSON")
                self.use_redis = False
        
        # Load initial profile
        self.profile = self._load_profile()

    def _load_profile(self):
        """Load profile from Redis or JSON"""
        if self.use_redis:
            try:
                # Get all profile keys from Redis
                profile_dict = {}
                # Scan for profile keys
                for key in self.redis_client.keys("profile:*"):
                    user_id = key.split(":", 1)[1]
                    user_data = self.redis_client.hgetall(key)
                    if user_data:
                        profile_dict[user_id] = user_data
                return profile_dict
            except Exception as e:
                logging.error(f"[Profile] Error loading from Redis: {e}")
        
        # Fallback to JSON
        if os.path.exists(PROFILE_PATH):
            try:
                with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_profile(self):
        """Save profile to Redis and backup to JSON"""
        if self.use_redis:
            try:
                for user_id, user_data in self.profile.items():
                    key = f"profile:{user_id}"
                    # Clear old data
                    self.redis_client.delete(key)
                    # Set new data
                    if user_data:
                        self.redis_client.hset(key, mapping=user_data)
                logging.info("[Profile] Saved to Redis")
            except Exception as e:
                logging.error(f"[Profile] Error saving to Redis: {e}")
        
        # Always backup to JSON
        try:
            with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.profile, f, ensure_ascii=False, indent=2)
            logging.debug("[Profile] Backed up to JSON")
        except Exception as e:
            logging.error(f"[Profile] Error backing up to JSON: {e}")

    def get_profile(self, user_id="default_user"):
        """Get profile for user"""
        if self.use_redis:
            try:
                key = f"profile:{user_id}"
                user_data = self.redis_client.hgetall(key)
                if user_data:
                    return user_data
            except Exception as e:
                logging.error(f"[Profile] Error reading from Redis: {e}")
        
        # Fallback to in-memory
        return self.profile.get(user_id, {})

    def update_profile(self, key, value, user_id="default_user"):
        """Update profile field"""
        if user_id not in self.profile:
            self.profile[user_id] = {}
        
        # Update in-memory
        self.profile[user_id][key] = value
        
        # Update Redis
        if self.use_redis:
            try:
                redis_key = f"profile:{user_id}"
                self.redis_client.hset(redis_key, key, value)
                logging.info(f"[Profile] Updated Redis: {user_id}.{key}={value}")
            except Exception as e:
                logging.error(f"[Profile] Error updating Redis: {e}")
        
        # Backup to JSON
        self._save_profile()

