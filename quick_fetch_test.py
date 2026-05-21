"""Quick test of cookie-based fetch"""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO_DIR = Path(__file__).parent
COOKIES_FILE = REPO_DIR / ".x_cookies.json"

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

print("=== Quick Fetch Test ===")
cookies = load_x_cookies()
print(f"Loaded {len(cookies)} cookies")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    context.add_cookies(cookies)
    page = context.new_page()
    
    print("Fetching main page...")
    page.goto("https://x.com/elonmusk", wait_until="commit", timeout=20000)
    time.sleep(4)
    
    print(f"URL: {page.url}")
    
    for _ in range(4):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(1)
    
    tweets = page.query_selector_all('[data-testid="tweet"]')
    print(f"Tweets: {len(tweets)}")
    
    # Check logged in
    body = page.evaluate("document.body.innerText")
    print(f"Logged in: {'Sign in to X' not in body}")
    
    print("\nTweets found:")
    for tweet in tweets[:5]:
        link = tweet.query_selector('a[href*="/status/"]')
        if link:
            tid = link.get_attribute('href').split('/')[-1]
            time_el = tweet.query_selector('time')
            dt = time_el.get_attribute('datetime')[:10] if time_el else '?'
            is_rt = bool(tweet.query_selector('[data-testid="socialContext"]'))
            is_quote = bool(tweet.query_selector('[data-testid="tweetQuote"]'))
            marker = "❝" if is_quote else ("🔁" if is_rt else "📝")
            print(f"  {marker} {tid} | {dt}")

print("\n=== Fetching with_replies ===")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    context.add_cookies(cookies)
    page = context.new_page()
    
    page.goto("https://x.com/elonmusk/with_replies", wait_until="commit", timeout=20000)
    time.sleep(4)
    
    for _ in range(5):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(1)
    
    tweets2 = page.query_selector_all('[data-testid="tweet"]')
    print(f"with_replies tweets: {len(tweets2)}")
    
    for tweet in tweets2[:5]:
        link = tweet.query_selector('a[href*="/status/"]')
        if link:
            tid = link.get_attribute('href').split('/')[-1]
            time_el = tweet.query_selector('time')
            dt = time_el.get_attribute('datetime')[:10] if time_el else '?'
            print(f"  {tid} | {dt}")

print("✅ Test complete")