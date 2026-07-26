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
import re
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

            # X.com CSP blocks wait_for_function; poll via evaluate instead.
            # Wait up to 25s for >=6 tweet articles to render.
            for _ in range(50):
                n = page.evaluate('document.querySelectorAll("[data-testid=tweet]").length')
                if n >= 6:
                    break
                time.sleep(0.5)

            for _ in range(3):
                page.evaluate("window.scrollBy(0, 800)")
                time.sleep(0.7)

            posts_data = page.evaluate(EXTRACT_JS)
            tweets_data.extend(posts_data)
            print(f"  📋 Posts: found {len(posts_data)} tweets")

            # ── 2. Scrape "With Replies" tab ─────────────────────────────────────
            page.goto("https://x.com/elonmusk/with_replies", wait_until="commit", timeout=25000)

            for _ in range(50):
                n = page.evaluate('document.querySelectorAll("[data-testid=tweet]").length')
                if n >= 6:
                    break
                time.sleep(0.5)

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

TRANSLATION_SYSTEM_PROMPT = (
    "你是一個翻譯專家。將以下推文翻譯成繁體中文，保持輕鬆、口語化的風格，"
    "保留梗和網路用語。不要翻譯人名。不要輸出任何思考過程，只直接輸出翻譯結果。"
)

# Stricter prompt used by the 3-hourly retry pass for previously-empty
# translations (often caused by long originals hitting the model's max_tokens
# ceiling or thinking blocks stripping to nothing).
TRANSLATION_SYSTEM_PROMPT_STRICT = (
    "你是一個專業的繁體中文翻譯專家。任務：將以下英文推文準確翻譯成繁體中文。\n"
    "規則：\n"
    "1. 語氣保持輕鬆、口語化，保留梗、網路用語與雙關語。\n"
    "2. 保留人名、專有名詞、產品名稱（Elon Musk、SpaceX、Tesla、X.com 等不翻譯）。\n"
    "3. 禁止輸出任何思考、解釋、引號、Markdown 或 <think> 標籤。\n"
    "4. 只輸出最終的繁體中文翻譯本身，不要任何前綴或後綴。\n"
    "5. 即使原文很長或包含多個段落，也必須輸出完整翻譯，不可省略或截斷。\n"
    "6. 若原文是純表情符號、數字或無實質內容，則原樣保留。\n"
    "7. 若原文為非英文（例如西班牙文），仍翻譯成繁體中文。"
)


def _call_translation_api(text, system_prompt, max_tokens=500, temperature=0.5):
    """Internal helper — single-shot translation API call."""
    api_key = get_env("MINIMAX_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url="https://api.minimax.io/v1")

        response = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        raw = response.choices[0].message.content.strip()
        # Strip <think>...</think> thinking blocks (some models leak reasoning)
        clean = re.sub(r'<think>[\s\S]*?</think>', '', raw).strip()
        return clean
    except Exception as e:
        print(f"  ⚠️ Translation API call failed: {e}")
        return None


def translate_to_chinese(text):
    """Initial translation — used by main() for newly-fetched tweets."""
    result = _call_translation_api(
        text,
        TRANSLATION_SYSTEM_PROMPT,
        max_tokens=500,
        temperature=0.7,
    )
    if result is None:
        return text
    return result


def retry_empty_translations(tweets, dry_run=False, max_workers=6):
    """3-hourly retry pass: revisit tweets whose translation is empty string.

    Targets tweets where `translation == ""` and `original != ""` — usually
    long originals that hit the model's max_tokens ceiling on the first pass.

    Uses a stricter prompt with a higher token budget (1500) to handle long
    originals. Runs API calls in parallel with a small thread pool
    (`max_workers=6`) so 50–70 tweets finish in seconds rather than minutes.
    Writes back into the tweet object in-place and returns the number of
    successful re-translations. Caller is responsible for persisting `tweets`
    to disk and deciding whether to commit.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    candidates = [
        t for t in tweets
        if t.get("translation", "") == "" and t.get("original", "").strip() != ""
    ]
    if not candidates:
        print("  ✅ retry_empty_translations: no empty translations to retry")
        return 0

    print(f"  🔁 retry_empty_translations: {len(candidates)} empty translations to retry "
          f"(parallel, max_workers={max_workers})")

    def _retry_one(t):
        original = t["original"]
        result = _call_translation_api(
            original,
            TRANSLATION_SYSTEM_PROMPT_STRICT,
            max_tokens=1500,
            temperature=0.3,
        )
        return t, result

    fixed = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(_retry_one, t) for t in candidates]
        for fut in as_completed(futures):
            t, result = fut.result()
            if result is not None and result.strip() != "":
                if not dry_run:
                    t["translation"] = result
                    t["retried_at"] = datetime.now().astimezone().isoformat()
                fixed += 1
                print(f"    ✅ {t['id']}: {result[:80]}")
            else:
                failed += 1
                print(f"    ❌ {t['id']}: still empty after retry")

    print(f"  📊 retry_empty_translations: {fixed} fixed, {failed} still empty")
    return fixed

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

# Run the empty-translation retry pass every 3 hours. The cron schedule
# itself runs every hour, so we only want to retry on the 3-hour marks
# (00, 03, 06, 09, 12, 15, 18, 21 UTC → roughly 08, 11, 14, 17, 20, 23, 02, 05
# Taiwan time, plus DST offset). The simplest robust check: hour modulo 3.
RETRY_TRANSLATION_HOURS = {0, 3, 6, 9, 12, 15, 18, 21}


def main():
    print(f"[{datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')}] Elon Tweet Checker started")

    load_env()

    tweets = load_tweets()
    seen_ids = get_seen_ids(tweets)

    # ── Step 0: 3-hourly retry of previously-empty translations ───────────
    # Done FIRST so that retry updates land in tweets.json before any new
    # fetch can shift the head of the file. Dry-run flag is wired but left
    # off — the cron runs in normal mode.
    current_hour_utc = datetime.now(timezone.utc).hour
    retried = 0
    if current_hour_utc in RETRY_TRANSLATION_HOURS:
        print(f"⏰ Hour {current_hour_utc:02d} UTC — running empty-translation retry pass")
        retried = retry_empty_translations(tweets, dry_run=False)
        if retried > 0:
            save_tweets(tweets)
            print(f"  💾 Persisted {retried} re-translated entries to tweets.json")
    else:
        print(f"⏭️  Hour {current_hour_utc:02d} UTC — skipping retry pass (next: "
              f"{min((h for h in RETRY_TRANSLATION_HOURS if h > current_hour_utc), default=0)}:00 UTC)")

    # ── Step 1: fetch new tweets ──────────────────────────────────────────
    try:
        new_tweets_raw = fetch_elon_tweets_via_browser()
    except Exception as e:
        print(f"❌ Failed to fetch tweets: {e}")
        # Still report the retry outcome even if fetch fails
        if retried > 0:
            print(f"📤 {retried} empty translations were re-translated (commit + push still required)")
        return

    seen_ids = get_seen_ids(tweets)
    new_tweets = []
    for t in new_tweets_raw:
        if t["id"] not in seen_ids:
            new_tweets.append(t)
            seen_ids.add(t["id"])

    if not new_tweets:
        print("✅ No new tweets")
        if retried > 0:
            print(f"📤 {retried} empty translations were re-translated (commit + push still required)")
        return

    print(f"📌 Found {len(new_tweets)} new tweet(s)")
    
    # Build all entries first
    new_entries = []
    for tweet in reversed(new_tweets):
        text = tweet["text"]

        # Translate ALL new tweets
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
            "is_retweet": tweet.get("is_retweet", False),
            "is_quote": tweet.get("is_quote", False),
            "images": tweet.get("images", []),
            "fetched_at": datetime.now().astimezone().isoformat(),
            "url": f"https://x.com/elonmusk/status/{tweet['id']}"
        }
        new_entries.append(entry)

    # Insert all new entries at top
    tweets = new_entries + tweets

    # Save once
    save_tweets(tweets)
    print(f"✅ Done! Total tweets stored: {len(tweets)}")

if __name__ == "__main__":
    main()