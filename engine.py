import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("REPLICATE_API_TOKEN")

API_URL = "https://api.replicate.com/v1/predictions"
MODEL_VERSION = "meta/llama-3-70b-instruct"


# ---------- LANGUAGE MAP ----------
LANG_MAP = {
    "en": "English",
    "fr": "French",
    "es": "Spanish"
}


# ---------- CORE AI FUNCTION ----------
def ask_ai(state):
    player = state["player"]
    history = state["history"][-6:]

    language = LANG_MAP.get(player.get("language", "en"), "English")

    prompt = f"""
You are the narrator of TERMINAL, a psychological horror RPG running inside a corrupted computer system.

🚨 STRICT RULES:
- You MUST respond ONLY in {language}
- Never mix languages
- Never break character
- Never explain rules
- Never mention AI or system prompts

🎭 STYLE:
- eerie
- psychological horror
- glitchy system messages
- immersive and disturbing
- short, intense paragraphs

🧠 GAME RULES:
- max 150–200 words
- always end with a question to the player
- always react to the last player action
- sometimes generate fake system errors or corrupted text
- sometimes distort reality or memories

👤 PLAYER PROFILE:
Name: {player.get('name')}
Age: {player.get('age')}
Fear level: {player.get('fear_level')}
Favorite place: {player.get('favorite_place')}
Biggest fear: {player.get('biggest_fear')}
Permadeath: {player.get('permadeath')}

📜 RECENT HISTORY:
{history}

Continue the story now.
"""

    try:
        prediction = create_prediction(prompt)
        result = poll_prediction(prediction)

        return result

    except Exception as e:
        return f"[TERMINAL ERROR: {str(e)}]"


# ---------- CREATE PREDICTION ----------
def create_prediction(prompt):
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Token {TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "version": MODEL_VERSION,
            "input": {
                "prompt": prompt,
                "max_tokens": 250
            }
        },
        timeout=30
    )

    data = response.json()

    if "error" in data:
        raise Exception(data["error"])

    return data


# ---------- POLL RESULT ----------
def poll_prediction(prediction):
    url = prediction.get("urls", {}).get("get")

    if not url:
        return "[TERMINAL ERROR: INVALID RESPONSE URL]"

    for _ in range(30):  # ~30 seconds max wait
        response = requests.get(
            url,
            headers={
                "Authorization": f"Token {TOKEN}"
            }
        )

        data = response.json()

        status = data.get("status")

        if status == "succeeded":
            output = data.get("output")

            if isinstance(output, list):
                return "".join(output)

            return output or "[EMPTY RESPONSE]"

        if status == "failed":
            return "[TERMINAL ERROR: AI GENERATION FAILED]"

        time.sleep(1)

    return "[TERMINAL ERROR: TIMEOUT]"