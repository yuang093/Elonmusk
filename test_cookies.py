import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

with open('.x_cookies.json') as f:
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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    context.add_cookies(clean)
    page = context.new_page()
    
    page.goto('https://x.com/elonmusk', wait_until='commit', timeout=20000)
    time.sleep(5)
    print(f'Main page URL: {page.url}')
    
    # Check login status
    body_text = page.evaluate('document.body.innerText')
    if 'Sign in to X' in body_text:
        print('LOGIN FAILED - showing login page')
    else:
        print('LOGGED IN')
    
    # Scroll and get tweets
    for i in range(5):
        page.evaluate('window.scrollBy(0, 800)')
        time.sleep(1)
    
    tweets = page.query_selector_all('[data-testid="tweet"]')
    print(f'Tweets found: {len(tweets)}')
    
    for tweet in tweets[:10]:
        link = tweet.query_selector('a[href*="/status/"]')
        if link:
            tid = link.get_attribute('href').split('/')[-1]
            time_el = tweet.query_selector('time')
            dt = time_el.get_attribute('datetime') if time_el else '?'
            text_el = tweet.query_selector('[data-testid="tweetText"]')
            txt = text_el.inner_text()[:80] if text_el else ''
            is_quote = bool(tweet.query_selector('[data-testid="tweetQuote"]'))
            is_retweet = bool(tweet.query_selector('[data-testid="retweet"]'))
            marker = 'Q' if is_quote else ('RT' if is_retweet else 'OP')
            print(f'  [{marker}] {tid} | {dt[:10]} | {txt}...')
    
    # Check if Cursor tweet exists somewhere
    print('\n=== Searching for Cursor tweet ID: 1923967493361774985 ===')
    # Try searching for it via X search
    page.goto(f'https://x.com/search?q=1923967493361774985&src=typed_query', wait_until='commit', timeout=15000)
    time.sleep(5)
    results = page.query_selector_all('[data-testid="tweet"]')
    print(f'Search results: {len(results)}')