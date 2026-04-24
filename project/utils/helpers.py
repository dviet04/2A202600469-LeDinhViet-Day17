# Helper functions for profile/episode extraction
import re

def detect_profile_update(text):
    # Simple pattern: "I am allergic to X" or "Tôi dị ứng X"
    match = re.search(r"allergic to ([\w\s]+)", text, re.IGNORECASE)
    if match:
        return ("allergy", match.group(1).strip())
    match = re.search(r"dị ứng ([\w\s]+)", text, re.IGNORECASE)
    if match:
        return ("allergy", match.group(1).strip())
    return None

def extract_episode(text):
    # If text contains "I completed" or "Tôi đã hoàn thành"
    if "completed" in text or "hoàn thành" in text:
        return {"event": text}
    return None
