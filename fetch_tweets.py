"""
Elon Musk Tweet Fetcher & Translator (Browser Edition - Cookies Enabled)
- Fetch latest tweets from @elonmusk via Playwright with cookie auth
- Include original tweets, retweets, and replies
- Translate to Traditional Chinese (casual tone)
- Store in tweets.json
- Send to Telegram
- Designed to run as hourly cron job
"""

import os
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

# ── Config ──────────────────────────────────────────────────────────────────
REPO_DIR = Path(__file__).parent
TWEETS_FILE = REPO_DIR / "tweets.json"
STATE_FILE  = REPO_DIR / ".fetch_state.json"
ENV_FILE    = REPO_DIR / ".env"
COOKIES_FILE = REPO_DIR / ".x_cookies.json"

# ── Helpers ──────────────────────────────────────────────────────────────────

def get_env(key, default=None):
    if not os.environ.get(key) and ENV_FILE.exists():
        load_env()
    return os.getenv(key, default)

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

def load_x_cookies():
    if not COOKIES_FILE.exists():
        return []
    with open(COOKIES_FILE) as f:
        raw = json.load(f)
    clean = []
    for c in raw:
        clean_c = {
            'name': c['name'],
            'value': c['value'],
            'domain': c['domain'],
            'path': c['path'],
            'expires': c.get('expires', -1),
            'httpOnly': c.get('httpOnly', False),
            'secure': c.get('secure', True),
        }
        if c.get('sameSite') in ('Strict', 'Lax', 'None'):
            clean_c['sameSite'] = c['sameSite']
        clean.append(clean_c)
    return clean

# ── Tweet Extraction JS ───────────────────────────────────────────────────────

EXTRACT_JS = """
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

        const isPinned = !!(a.querySelector('[data-testid="pin"]') || a.querySelector('[data-testid="unpin"]'));
        const isRetweet = !!(a.querySelector('[data-testid="retweet"]') || a.querySelector('[data-testid="socialContext"]'));
        const isQuote = !!(a.querySelector('[data-testid="tweetQuote"]'));

        const imgs = Array.from(a.querySelectorAll('img[src*="media"]'));
        const images = imgs.map(img => img.getAttribute('src')).filter(Boolean);

        const spans = a.querySelectorAll('span');
        let longest = '';
        spans.forEach(s => {
            const t = s.textContent || '';
            if (t.length > longest.length) longest = t;
        });

        if (longest.length > 5) {
            results.push({
                id, created_at: datetime, text: longest,
                pinned: isPinned, is_retweet: isRetweet || isQuote,
                is_quote: isQuote,
                images: images
            });
        }
    });
    return results;
}
"""

# ── Browser Fetch ─────────────────────────────────────────────────────────────

def fetch_elon_tweets_via_browser():
    """Use Playwright to scrape elonmusk tweets with cookie auth"""
    tweets_data = []
    cookies = load_x_cookies()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        if cookies:
            context.add_cookies(cookies)
            print(f"  🔐 Loaded {len(cookies)} X.com cookies")
        
        page = context.new_page()
        
        try:
            # ── 1. Scrape "Posts" tab ────────────────────────────────────────────
            page.goto("https://x.com/elonmusk", wait_until="commit", timeout=25000)
            time.sleep(3)
            
            for _ in range(3):
                page.evaluate("window.scrollBy(0, 800)")
                time.sleep(0.7)
            
            posts_data = page.evaluate(EXTRACT_JS)
            tweets_data.extend(posts_data)
            print(f"  📋 Posts: found {len(posts_data)} tweets")
            
            # ── 2. Scrape "With Replies" tab ─────────────────────────────────────
            page.goto("https://x.com/elonmusk/with_replies", wait_until="commit", timeout=25000)
            time.sleep(3)
            
            for _ in range(4):
                page.evaluate("window.scrollBy(0, 800)")
                time.sleep(0.7)
            
            replies_data = page.evaluate(EXTRACT_JS)
            tweets_data.extend(replies_data)
            print(f"  📋 With Replies: found {len(replies_data)} tweets")
            
        finally:
            browser.close()
    
    return tweets_data

# ── Translation ──────────────────────────────────────────────────────────────

def translate_to_chinese(text):
    api_key = get_env("MINIMAX_API_KEY")
    if not api_key:
        return text
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url="https://api.minimax.io/v1")
        
        response = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[
                {"role": "system", "content": "你是一個翻譯專家。將以下推文翻譯成繁體中文，保持輕鬆、口語化的風格，保留梗和網路用語。不要翻譯人名。只輸出翻譯結果，不要其他解釋。"},
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
        return None

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
    original = tweet.get("original", tweet.get("text", ""))
    is_retweet = tweet.get("is_retweet", False)
    is_quote = tweet.get("is_quote", False)
    
    type_marker = ""
    if is_quote:
        type_marker = "❝ 引用 "
    elif is_retweet:
        type_marker = "🔁 轉推 "
    
    msg = f"""{type_marker}🦁 <b>Elon Musk</b> | 🕐 {time_str}
━━━━━━━━━━━━━━━━━━
📝 原文：
{original}
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
    
    tweets = load_tweets()
    seen_ids = get_seen_ids(tweets)
    
    try:
        new_tweets_raw = fetch_elon_tweets_via_browser()
    except Exception as e:
        print(f"❌ Failed to fetch tweets: {e}")
        return
    
    seen_ids = get_seen_ids(tweets)
    new_tweets = []
    for t in new_tweets_raw:
        if t["id"] not in seen_ids:
            new_tweets.append(t)
            seen_ids.add(t["id"])
    
    if not new_tweets:
        print("✅ No new tweets")
        return
    
    print(f"📌 Found {len(new_tweets)} new tweet(s)")
    
    for tweet in reversed(new_tweets):
        text = tweet["text"]
        created = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00"))
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        if created >= today:
            print(f"  → Translating: {text[:60]}...")
            translation = translate_to_chinese(text)
        else:
            print(f"  → Skipping translation (older than today): {text[:60]}...")
            translation = ""
        
        entry = {
            "id": tweet["id"],
            "created_at": tweet["created_at"],
            "original": text,
            "translation": translation,
            "metrics": tweet.get("metrics", {}),
            "lang": "en",
            "pinned": tweet.get("pinned", False),
            "is_retweet": tweet.get("is_retweet", False),
            "is_quote": tweet.get("is_quote", False),
            "images": tweet.get("images", []),
            "fetched_at": datetime.now().astimezone().isoformat(),
            "url": f"https://x.com/elonmusk/status/{tweet['id']}"
        }
        
        tweets.insert(0, entry)
        
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