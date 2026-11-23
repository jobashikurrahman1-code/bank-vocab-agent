import os
import json
import datetime
import requests
from google import genai

# ==========================================
# Day number (Change this to 2, 3... when you want next days)
DAY_NUMBER = 1 
# ==========================================

def run_agent():
    api_key = os.environ.get("GEMINI_API_KEY")
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not api_key or not bot_token or not chat_id:
        print("Error: Missing environment secrets!")
        return

    client = genai.Client(api_key=api_key)
    
    state_file = "vocab_state.json"
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            vocab = json.load(f)
    else:
        print("Error: vocab_state.json not found!")
        return

    target_words = [w for w in vocab if w.get("day") == DAY_NUMBER]

    if not target_words:
        msg = f"❌ Error: No words found for Day {DAY_NUMBER}."
    else:
        prompt = f"""
        You are an expert Bank Exam & GRE/GMAT English Vocabulary Coach.
        Create an intensive training round for Day {DAY_NUMBER} using these words:
        {json.dumps(target_words)}

        INSTRUCTIONS:
        - Provide crisp definitions, high-yield synonyms, antonyms, and professional banking context for each word.
        - Generate a fresh practice quiz containing 6 unique questions mixing:
          1. Direct Synonym/Antonym MCQs
          2. Single-Blank Sentence Completions (Banking/Economic context)
          3. Double-Blank Sentence Completions (GRE/GMAT standard)
        - Format cleanly for Telegram.
        - Tell the user to reply directly with their answers.
        """

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        msg = f"🔥 SESSION: DAY {DAY_NUMBER} (UNLIMITED ROUND)\n\n" + response.text

    # Send to Telegram
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    for i in range(0, len(msg), 4000):
        requests.post(url, json={"chat_id": chat_id, "text": msg[i:i+4000]})

if __name__ == "__main__":
    run_agent()
