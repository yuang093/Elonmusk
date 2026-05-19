"""
Elon Musk Tweet Fetcher & Translator (Browser Edition)
- Fetch latest tweets from @elonmusk via Playwright (no API needed)
- Translate to Traditional Chinese (casual tone)
- Store in tweets.json
- Send to Telegram
- Designed to run as hourly cron job
"""

import os
import json
import subprocess
import time
import requests
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

# ── Config ──────────────────────────────────────────────────────────────────
REPO_DIR = Path(__file__).parent
TWEETS_FILE = REPO_DIR / "tweets.json"
STATE_FILE  = REPO_DIR / ".fetch_state.json"
ENV_FILE    = REPO_DIR / ".env"

# ── Helpers ──────────────────────────────────────────────────────────────────

def get_env(key, default=None):
    """Get env var, loading from .env first"""
    if not os.environ.get(key) and ENV_FILE.exists():
        load_env()
    return os.getenv(key, default)

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
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

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

# ── Browser Fetch ─────────────────────────────────────────────────────────────

def fetch_elon_tweets_via_browser():
    """Use Playwright to scrape elonmusk tweets without API"""
    tweets_data = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto("https://x.com/elonmusk", timeout=30000)
            page.wait_for_selector('[data-testid="tweet"]', timeout=15000)
            time.sleep(2)  # let JS hydrate
            
            # Get all tweet data via single JS evaluation
            tweets_data = page.evaluate("""
                () => {
                    const articles = document.querySelectorAll('[data-testid="tweet"]');
                    const results = [];
                    articles.forEach(a => {
                        const link = a.querySelector('a[href*="/status/"]');
                        const timeEl = a.querySelector('time');
                        if (!link || !timeEl) return;
                        const href = link.getAttribute('href');
                        const id = href.split('/').pop();
                        const datetime = timeEl.getAttribute('datetime');
                        // Check if this tweet is pinned (has pin/unpin action)
                        const pinBtn = a.querySelector('[data-testid="pin"]');
                        const unpinBtn = a.querySelector('[data-testid="unpin"]');
                        const isPinned = !!(pinBtn || unpinBtn);
                        const spans = a.querySelectorAll('span');
                        let longest = '';
                        spans.forEach(s => {
                            const t = s.textContent || '';
                            if (t.length > longest.length) longest = t;
                        });
                        if (longest.length > 20) {
                            results.push({ id, created_at: datetime, text: longest, pinned: isPinned });
                        }
                    });
                    return results;
                }
            """)
                    
        finally:
            browser.close()
    
    return tweets_data

# ── Translation ──────────────────────────────────────────────────────────────

def translate_to_chinese(text):
    api_key = get_env("MINIMAX_API_KEY")
    if not api_key:
        return text  # fallback
    
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.minimax.chat/v1"
        )
        
        system_prompt = """你是一個翻譯專家。將以下推文翻譯成繁體中文，保持輕鬆、口語化的風格，保留梗和網路用語。不要翻譯人名。只輸出翻譯結果，不要其他解釋。"""
        
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
    except Exception as e:
        print(f"  ⚠️ Translation failed: {e}")
        return text

# ── Telegram ────────────────────────────────────────────────────────────────

def send_telegram(message):
    bot_token = get_env("TG_BOT_TOKEN")
    chat_id   = get_env("TG_CHAT_ID")
    if not bot_token or not chat_id:
        print("⚠️ Telegram credentials not set")
        return

    import urllib.request
    import urllib.parse

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_preview": "false"
    }).encode()

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"⚠️ Telegram failed: {e}")
        return None

def format_tweet_message(tweet, translation, tweet_id):
    taiwan_tz = datetime.now().astimezone().tzinfo
    created = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00")).astimezone(taiwan_tz)
    time_str = created.strftime("%Y-%m-%d %H:%M")
    
    likes = tweet.get("metrics", {}).get("like_count", 0)
    rts   = tweet.get("metrics", {}).get("retweet_count", 0)
    
    msg = f"""🦁 <b>Elon Musk</b> | 🕐 {time_str}
━━━━━━━━━━━━━━━━━━
📝 原文：
{tweet['original']}
━━━━━━━━━━━━━━━━━━
🌏 繁中翻譯：
{translation}
━━━━━━━━━━━━━━━━━━
❤️ {likes:,}  🔁 {rts:,}  🐦 EN
🔗 https://x.com/elonmusk/status/{tweet_id}"""
    
    return msg

# ── Main ───────────────────────────────────────────────────────────────────

def main():
    print(f"[{datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')}] Elon Tweet Checker started")
    
    load_env()
    
    # Load existing tweets
    tweets = load_tweets()
    seen_ids = get_seen_ids(tweets)
    
    # Fetch new tweets via browser
    try:
        new_tweets_raw = fetch_elon_tweets_via_browser()
    except Exception as e:
        print(f"❌ Failed to fetch tweets via browser: {e}")
        return
    
    # Filter unseen
    new_tweets = [t for t in new_tweets_raw if t["id"] not in seen_ids]
    
    if not new_tweets:
        print("✅ No new tweets")
        return
    
    print(f"📌 Found {len(new_tweets)} new tweet(s)")
    
    for tweet in reversed(new_tweets):  # oldest first
        text = tweet["text"]
        print(f"  → Translating: {text[:60]}...")
        
        translation = translate_to_chinese(text)
        
        entry = {
            "id": tweet["id"],
            "created_at": tweet["created_at"],
            "original": text,
            "translation": translation,
            "metrics": tweet.get("metrics", {}),
            "lang": "en",
            "pinned": tweet.get("pinned", False),
            "fetched_at": datetime.now().astimezone().isoformat(),
            "url": f"https://x.com/elonmusk/status/{tweet['id']}"
        }
        
        tweets.insert(0, entry)
        
        # Send Telegram
        msg = format_tweet_message(tweet, translation, tweet["id"])
        try:
            send_telegram(msg)
            print(f"  ✅ Telegram sent: {tweet['id']}")
        except Exception as e:
            print(f"  ⚠️ Telegram failed: {e}")
        
        time.sleep(1)
    
    save_tweets(tweets)
    print(f"✅ Done! Total tweets stored: {len(tweets)}")

if __name__ == "__main__":
    main()