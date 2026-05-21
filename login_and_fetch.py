"""
X.com Login + Tweet Fetcher
先用帳密登入，再抓 /with_replies 分頁的引用推文
"""

import os
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO_DIR = Path(__file__).parent
TWEETS_FILE = REPO_DIR / "tweets.json"
COOKIES_FILE = REPO_DIR / ".x_cookies.json"
STATE_FILE = REPO_DIR / ".fetch_state.json"

X_EMAIL = "taeyeon093.bot@gmail.com"
X_PASSWORD = "@#Cctv!!"

def save_cookies(cookies, path):
    with open(path, 'w') as f:
        json.dump(cookies, f)

def load_cookies(path):
    if Path(path).exists():
        with open(path) as f:
            return json.load(f)
    return None

def login_to_x(p):
    """嘗試登入 X.com 並儲存 cookies"""
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    print("🔐 前往登入頁...")
    page.goto("https://x.com/i/jf/onboarding/web?mode=login", timeout=30000)
    time.sleep(3)
    
    # 填入 username_or_email (不是 "text"!)
    print("📧 填入帳號...")
    page.fill('input[name="username_or_email"]', X_EMAIL, timeout=10000)
    time.sleep(1)
    
    # 點擊 Continue
    print("➡️ 點擊 Continue...")
    page.click('button:has-text("Continue")', timeout=5000)
    time.sleep(3)
    
    # 檢查 URL 決定下一步
    current_url = page.url
    print(f"   URL: {current_url}")
    
    # 可能需要額外驗證（電話/Apple）
    try:
        # 嘗試處理可能的 username 問題
        page.wait_for_selector('input[name="username_or_email"]', timeout=3000)
        # 如果又回到 username 欄位，嘗試輸入 username
        page.fill('input[name="username_or_email"]', 'taeyeon093_bot')
        page.click('button:has-text("Continue")', timeout=5000)
        time.sleep(2)
    except:
        pass
    
    # 填入密碼
    print("🔑 填入密碼...")
    page.fill('input[name="password"]', X_PASSWORD, timeout=10000)
    time.sleep(1)
    
    # 點擊 Log in / Continue
    print("➡️ 點擊登入...")
    try:
        page.click('button:has-text("Log in"), button:has-text("Continue")', timeout=5000)
    except:
        page.click('button', timeout=5000)  # fallback
    time.sleep(5)
    
    # 檢查是否成功
    print(f"   當前 URL: {page.url}")
    if "login" not in page.url.lower() and "flow" not in page.url.lower() and "onboarding" not in page.url.lower():
        print("✅ 登入成功")
        cookies = context.cookies()
        save_cookies(cookies, COOKIES_FILE)
        return context
    else:
        print("❌ 登入失敗")
        return None

def fetch_with_replies(context):
    """用已登入的 context 抓取回覆分頁"""
    page = context.new_page()
    
    print("\n📋 前往 /with_replies 分頁...")
    page.goto("https://x.com/elonmusk/with_replies", timeout=30000)
    time.sleep(5)
    
    # 滾動載入更多
    print("📜 滾動頁面...")
    for i in range(5):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(1)
    
    # 抓推文
    tweets = page.query_selector_all('[data-testid="tweet"]')
    print(f"   找到 {len(tweets)} 篇推文")
    
    results = []
    for tweet in tweets:
        try:
            link = tweet.query_selector('a[href*="/status/"]')
            time_el = tweet.query_selector('time')
            if not link or not time_el:
                continue
            
            href = link.get_attribute('href')
            tweet_id = href.split('/').pop()
            dt = time_el.get_attribute('datetime')
            
            is_quote = bool(tweet.query_selector('[data-testid="quote"]'))
            is_retweet = bool(tweet.query_selector('[data-testid="retweet"]'))
            
            text_el = tweet.query_selector('[data-testid="tweetText"]')
            text = text_el.inner_text() if text_el else ""
            
            results.append({
                "id": tweet_id,
                "datetime": dt,
                "text": text[:200],
                "is_quote": is_quote,
                "is_retweet": is_retweet
            })
        except Exception as e:
            continue
    
    return results

def main():
    print("=== X.com 登入抓取程式 ===\n")
    
    with sync_playwright() as p:
        # 先嘗試用現有 cookies
        cookies = load_cookies(COOKIES_FILE)
        context = None
        
        if cookies:
            print("🔧 嘗試使用已儲存的 cookies...")
            try:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                context.add_cookies(cookies)
                # 驗證 cookies 是否還有效
                test_page = context.new_page()
                test_page.goto("https://x.com/elonmusk", timeout=15000)
                time.sleep(3)
                if "login" not in test_page.url.lower():
                    print("✅ Cookies 有效")
                else:
                    context = None
            except Exception as e:
                print(f"  Cookies 無效: {e}")
                context = None
        
        if not context:
            print("🔐 需要登入...")
            context = login_to_x(p)
        
        if context:
            tweets = fetch_with_replies(context)
            print(f"\n📊 結果：找到 {len(tweets)} 篇推文")
            for t in tweets[:10]:
                marker = "🔁" if t["is_retweet"] else ("❝" if t["is_quote"] else "📝")
                print(f"  {marker} {t['id']} | {t['datetime'][:10]} | RT={t['is_retweet']} Q={t['is_quote']}")
                print(f"     {t['text'][:80]}...")
        else:
            print("❌ 無法完成登入")

if __name__ == "__main__":
    main()