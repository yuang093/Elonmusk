"""
Elon Musk Tweet Fetcher & Translator
- Fetch latest tweets from @elonmusk via X API v2
- Translate to Traditional Chinese (casual tone)
- Store in tweets.json
- Send to Telegram
- Designed to run as hourly cron job
"""

import os
import json
import requests
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
REPO_DIR = Path(__file__).parent
TWEETS_FILE = REPO_DIR / "tweets.json"
ENV_FILE   = REPO_DIR / ".env"

# X API v2
X_API_BASE = "https://api.twitter.com/2"

# Telegram
TG_BOT_TOKEN  = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID     = os.getenv("TG_CHAT_ID")

# AI Translation (configurable)
TRANSLATOR_PROVIDER = os.getenv("TRANSLATOR_PROVIDER", "minimax")  # minimax | openai | deepseek
TRANSLATOR_API_KEY  = os.getenv("TRANSLATOR_API_KEY")
TRANSLATOR_MODEL     = os.getenv("TRANSLATOR_MODEL", "auto")

# ── Helpers ─────────────────────────────────────────────────────────────────

def load_env():
    """Load .env file into environment"""
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

def load_tweets():
    if TWEETS_FILE.exists():
        return json.loads(TWEETS_FILE.read_text(encoding="utf-8"))
    return []

def save_tweets(tweets):
    TWEETS_FILE.write_text(
        json.dumps(tweets, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def get_seen_ids(tweets):
    return {t["id"] for t in tweets}

# ── X API ───────────────────────────────────────────────────────────────────

def get_bearer_token():
    token = os.getenv("X_BEARER_TOKEN")
    if not token:
        raise RuntimeError("X_BEARER_TOKEN not set in .env")
    return token

def fetch_elon_tweets(bearer_token, since_id=None, max_results=10):
    """Fetch recent tweets from @elonmusk"""
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    # Step 1: Get user ID for elonmusk
    user_resp = requests.get(
        f"{X_API_BASE}/users/by/username/elonmusk",
        headers=headers,
        params={"user.fields": "id,name,username"}
    )
    user_resp.raise_for_status()
    user_id = user_resp.json()["data"]["id"]
    
    # Step 2: Fetch tweets
    params = {
        "max_results": min(max_results, 10),
        "tweet.fields": "created_at,public_metrics,lang",
        "expansions": "author_id",
        "user.fields": "name,username",
    }
    if since_id:
        params["since_id"] = since_id
    
    tweets_resp = requests.get(
        f"{X_API_BASE}/users/{user_id}/tweets",
        headers=headers,
        params=params
    )
    tweets_resp.raise_for_status()
    return tweets_resp.json().get("data", [])

# ── Translation ──────────────────────────────────────────────────────────────

def translate_to_chinese(text, provider=None):
    """Translate text to Traditional Chinese using configured AI provider"""
    provider = provider or TRANSLATOR_PROVIDER
    
    if provider == "minimax":
        return translate_minimax(text)
    elif provider == "openai":
        return translate_openai(text)
    else:
        return text  # fallback: return original

def translate_minimax(text):
    """Translate via MiniMax API"""
    api_key = os.getenv("MINIMAX_API_KEY") or TRANSLATOR_API_KEY
    if not api_key:
        return text
    
    from openai import OpenAI
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.minimax.chat/v1"
    )
    
    system_prompt = """你是一個翻譯專家。將以下推文翻譯成繁體中文，保持輕鬆、口語化的風格，保留梗和網路用語。只輸出翻譯結果，不要其他解釋。"""
    
    response = client.chat.completions.create(
        model="MiniMax-Text-01",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def translate_openai(text):
    """Translate via OpenAI API"""
    api_key = os.getenv("OPENAI_API_KEY") or TRANSLATOR_API_KEY
    if not api_key:
        return text
    
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一個翻譯專家。將推文翻譯成繁體中文，保持輕鬆、口語化的風格，保留梗和網路用語。只輸出翻譯結果。"},
            {"role": "user", "content": text}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

# ── Telegram ────────────────────────────────────────────────────────────────

def send_telegram(message):
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        print("⚠️ Telegram credentials not set — skipping notification")
        return
    
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_preview": False
    }
    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()

def format_tweet_message(tweet, translation, author):
    """Format tweet for Telegram delivery"""
    created = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00"))
    taiwan_time = created.astimezone(timezone(tz=datetime.now().astimezone().tzinfo))
    time_str = taiwan_time.strftime("%Y-%m-%d %H:%M")
    
    # Engagement
    metrics = tweet.get("public_metrics", {})
    likes = metrics.get("like_count", 0)
    retweets = metrics.get("retweet_count", 0)
    
    # Status indicator
    lang = tweet.get("lang", "unknown")
    
    msg = f"""🦁 <b>Elon Musk</b> | 🕐 {time_str}
━━━━━━━━━━━━━━━━━━
📝 原文：
{tweet["text"]}
━━━━━━━━━━━━━━━━━━
🌏 繁中翻譯：
{translation}
━━━━━━━━━━━━━━━━━━
❤️ {likes:,}  🔁 {retweets:,}  🐦 {lang.upper()}"""
    
    return msg

# ── Main ───────────────────────────────────────────────────────────────────

def main():
    print(f"[{datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')}] Elon Tweet Checker started")
    
    # Load environment
    load_env()
    
    bearer_token = os.getenv("X_BEARER_TOKEN")
    if not bearer_token:
        print("❌ X_BEARER_TOKEN not found in .env")
        return
    
    # Load existing tweets
    tweets = load_tweets()
    seen_ids = get_seen_ids(tweets)
    
    # Get latest tweet ID to use as since_id
    since_id = tweets[0]["id"] if tweets else None
    
    # Fetch new tweets
    try:
        new_tweets_raw = fetch_elon_tweets(bearer_token, since_id=since_id)
    except Exception as e:
        print(f"❌ Failed to fetch tweets: {e}")
        return
    
    # Filter out already-seen tweets (newest first)
    new_tweets = [t for t in new_tweets_raw if t["id"] not in seen_ids]
    
    if not new_tweets:
        print("✅ No new tweets")
        return
    
    print(f"📌 Found {len(new_tweets)} new tweet(s)")
    
    # Process new tweets (newest first)
    for tweet in reversed(new_tweets):  # oldest first for chronological prepend
        text = tweet["text"]
        print(f"  → Translating: {text[:60]}...")
        
        translation = translate_to_chinese(text)
        
        entry = {
            "id": tweet["id"],
            "created_at": tweet["created_at"],
            "original": text,
            "translation": translation,
            "metrics": tweet.get("public_metrics", {}),
            "lang": tweet.get("lang", "unknown"),
            "fetched_at": datetime.now().astimezone().isoformat()
        }
        
        # Prepend to list (newest first)
        tweets.insert(0, entry)
        
        # Send Telegram notification
        msg = format_tweet_message(tweet, translation, "Elon Musk")
        try:
            send_telegram(msg)
            print(f"  ✅ Telegram sent: {tweet['id']}")
        except Exception as e:
            print(f"  ⚠️ Telegram failed: {e}")
        
        time.sleep(1)  # Rate limit buffer
    
    # Save updated tweets
    save_tweets(tweets)
    print(f"✅ Done! Total tweets stored: {len(tweets)}")

if __name__ == "__main__":
    main()