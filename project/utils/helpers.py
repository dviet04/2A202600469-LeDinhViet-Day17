# Helper functions for profile/episode extraction
import openai
from utils.config import OPENAI_API_KEY

def detect_profile_update(text):
    # Chỉ dùng LLM để extract profile info (trả về tất cả fields)
    try:
        import json
        import logging
        
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        prompt = (
            "Extract ALL personal information from this text as JSON. "
            "Return ONLY the JSON object, no explanation. "
            "Include any of these keys if present: name, occupation, age, allergy, food, color, hobby, location, etc. "
            "Example: 'I am John, developer, allergic to peanuts' -> {\"name\":\"John\",\"occupation\":\"developer\",\"allergy\":\"peanuts\"}. "
            "If NO info found, return {} "
            f"Text: {text}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.0
        )
        content = response.choices[0].message.content.strip()
        
        # Strip markdown code block if present (```json ... ```)
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        data = json.loads(content)
        if isinstance(data, dict) and len(data) > 0:
            logging.info(f"[Profile] Detected: {data}")
            return data
        else:
            logging.debug(f"[Profile] No data detected from: {text[:50]}")
    except Exception as e:
        logging.error(f"[Profile] Error: {e}")
    return None
def extract_episode(text, session_id=None):
    # Chỉ dùng LLM để extract trải nghiệm/hành động thực tế
    try:
        import json
        import logging
        
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        prompt = (
            "Extract the MAIN action or event from this message. "
            "SKIP: greetings (hello, hi), thanks (thanks, cảm ơn, appreciate), questions without action. "
            "EXTRACT: real events, actions, tasks, problems, achievements, learning moments. "
            "Return ONLY JSON with key 'event' and value as brief description. "
            "Example: 'I completed Task A' -> {\"event\":\"completed Task A\"}. "
            "Example: 'Thanks for help' -> {}. "
            "If no meaningful event, return {}. "
            f"Text: {text}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80,
            temperature=0.0
        )
        content = response.choices[0].message.content.strip()
        
        # Strip markdown code block if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        data = json.loads(content)
        if isinstance(data, dict) and "event" in data and data["event"]:
            event = data["event"].strip()
            if len(event) > 3:  # At least 3 characters (was 5)
                data["session_id"] = session_id
                logging.info(f"[Episode] Detected: {event}")
                return data
            else:
                logging.debug(f"[Episode] Event too short: {event}")
        else:
            logging.debug(f"[Episode] No event detected from: {text[:50]}")
    except Exception as e:
        logging.error(f"[Episode] Error: {e}")
    return None
