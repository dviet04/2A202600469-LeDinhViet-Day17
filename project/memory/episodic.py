# EpisodicMemory: stores past events/tasks using Redis
import json
import os
import logging

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logging.warning("[Episodic] Redis not available, falling back to JSON")

EPISODIC_PATH = os.path.join(os.path.dirname(__file__), '../data/episodic.json')
REDIS_EPISODIC_KEY = "episodic:list"

class EpisodicMemory:
    def __init__(self, redis_host="localhost", redis_port=6379, redis_db=0):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.episodes = []
        
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
                logging.info("[Episodic] Connected to Redis")
            except Exception as e:
                logging.warning(f"[Episodic] Redis connection failed: {e}, falling back to JSON")
                self.use_redis = False
        
        # Load initial episodes
        self.episodes = self._load_episodes()

    def _load_episodes(self):
        """Load episodes from Redis or JSON"""
        if self.use_redis:
            try:
                # Get all episodes from Redis list
                episodes = []
                items = self.redis_client.lrange(REDIS_EPISODIC_KEY, 0, -1)
                for item in items:
                    try:
                        episodes.append(json.loads(item))
                    except:
                        pass
                if episodes:
                    return episodes
            except Exception as e:
                logging.error(f"[Episodic] Error loading from Redis: {e}")
        
        # Fallback to JSON
        if os.path.exists(EPISODIC_PATH):
            try:
                with open(EPISODIC_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save_episodes(self):
        """Save episodes to Redis and backup to JSON"""
        if self.use_redis:
            try:
                # Clear old list
                self.redis_client.delete(REDIS_EPISODIC_KEY)
                # Add all episodes as JSON strings
                for episode in self.episodes:
                    self.redis_client.rpush(REDIS_EPISODIC_KEY, json.dumps(episode, ensure_ascii=False))
                logging.info("[Episodic] Saved to Redis")
            except Exception as e:
                logging.error(f"[Episodic] Error saving to Redis: {e}")
        
        # Always backup to JSON
        try:
            with open(EPISODIC_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.episodes, f, ensure_ascii=False, indent=2)
            logging.debug("[Episodic] Backed up to JSON")
        except Exception as e:
            logging.error(f"[Episodic] Error backing up to JSON: {e}")

    def add_episode(self, event):
        """Add episode to memory"""
        self.episodes.append(event)
        
        # Save to Redis
        if self.use_redis:
            try:
                self.redis_client.rpush(REDIS_EPISODIC_KEY, json.dumps(event, ensure_ascii=False))
                logging.info(f"[Episodic] Added to Redis: {event.get('event', 'Unknown')}")
            except Exception as e:
                logging.error(f"[Episodic] Error adding to Redis: {e}")
        
        # Backup to JSON
        self._save_episodes()

    def retrieve_recent(self, n=5):
        """Get most recent n episodes"""
        return self.episodes[-n:] if self.episodes else []

