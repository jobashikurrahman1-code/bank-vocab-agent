import os
import json
import datetime
import requests
from google import genai

# ==========================================
# CHANGE THIS NUMBER WHENEVER YOU WANT A NEW DAY!
# (Choose from Day 1 up to Day 15)
DAY_NUMBER = 1 
# ==========================================

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
STATE_FILE = "vocab_state.json"

def load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for i in range(0, len(text), 4000):
        requests.post(url, json={"chat_id": CHAT_ID, "text": text[i:i+4000]})

def run_agent():
    vocab = load_state()
    
    # Grab all words belonging strictly to the selected Day number
    target_words = [w for w in vocab if w.get("day") == DAY_NUMBER]

    if not target_words:
        send_telegram(f"❌ Error: No words found for Day {DAY_NUMBER}. Check your vocab_state.json file!")
        return

    prompt = f"""
    You are an expert Bank Exam & GRE/GMAT English Vocabulary Coach.
    The user wants to practice a custom training round for **Day {DAY_NUMBER}**.
    
    Here are the words assigned to Day {DAY_NUMBER}:
    {json.dumps(target_words)}

    INSTRUCTIONS:
    - Create an intensive training round for these words.
    - Provide crisp definitions, high-yield synonyms, antonyms, and professional context for each word.
    - **CRITICAL REQUIREMENT:** Generate a completely fresh practice quiz containing **6 unique questions** mixing:
      1. Direct Synonym/Antonym MCQs (Standard Bank Exam style)
      2. Single-Blank Sentence Completions (Banking/Economic context)
      3. Double-Blank or Logic-Shift Sentence Completions (GRE/GMAT standard)
    - Format cleanly for Telegram (plain text or simple formatting, no broken markdown symbols).
    - Instruct the user to reply directly to this message on Telegram with their answers.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    send_telegram(f"🔥 *SESSION: DAY {DAY_NUMBER} (UNLIMITED ROUND)*\n\n" + response.text)

if __name__ == "__main__":
    run_agent()
