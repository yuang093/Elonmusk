"""
X.com Login - 修復版 (使用正確的 /i/flow/login URL 和欄位名稱)
"""

import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO_DIR = Path(__file__).parent
COOKIES_FILE = REPO_DIR / ".x_cookies.json"

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

def try_login(p):
    """嘗試登入 X.com"""
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    print("🔐 前往登入頁...")
    page.goto("https://x.com/i/flow/login", timeout=30000)
    time.sleep(4)
    print(f"   URL: {page.url}")
    
    # Step 1: 填入 email/username
    print("\n1️⃣ 填入帳號...")
    try:
        # input name="text" 是 X.com 的登入欄位
        page.fill('input[name="text"]', X_EMAIL, timeout=10000)
        print(f"   ✅ 已填入: {X_EMAIL}")
    except Exception as e:
        print(f"   ❌ 填入失敗: {e}")
        page.screenshot(path='/tmp/x_login_step1.png')
        return None
    
    time.sleep(1)
    
    # Step 2: 點擊 Next
    print("\n2️⃣ 點擊 Next...")
    try:
        page.click('button:has-text("Next"), button[type="submit"]', timeout=5000)
        print("   ✅ 已點擊")
    except Exception as e:
        print(f"   ❌ 點擊失敗: {e}")
    
    time.sleep(3)
    print(f"   URL: {page.url}")
    
    # Step 3: 檢查是否需要密碼（通常直接到密碼頁）
    try:
        pw_field = page.query_selector('input[name="password"]')
        if pw_field:
            print("\n3️⃣ 填入密碼...")
            page.fill('input[name="password"]', X_PASSWORD, timeout=10000)
            print("   ✅ 密碼已填入")
            time.sleep(1)
            
            # 點擊 Log in
            print("\n4️⃣ 點擊登入...")
            page.click('button:has-text("Log in"), button[type="submit"]', timeout=5000)
            print("   ✅ 已點擊")
            time.sleep(5)
    except Exception as e:
        print(f"   密碼階段失敗: {e}")
    
    print(f"\n📍 最終 URL: {page.url}")
    
    # 檢查是否成功
    if "login" not in page.url.lower() and "flow" not in page.url.lower():
        print("✅ 登入成功")
        cookies = context.cookies()
        save_cookies(cookies, COOKIES_FILE)
        return context
    else:
        print("❌ 登入失敗")
        page.screenshot(path='/tmp/x_login_failed.png')
        return None

def main():
    print("=== X.com 登入程式 ===\n")
    
    with sync_playwright() as p:
        # 先試現有 cookies
        cookies = load_cookies(COOKIES_FILE)
        if cookies:
            print("🔧 檢查現有 cookies...")
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            context.add_cookies(cookies)
            page = context.new_page()
            page.goto("https://x.com/elonmusk", timeout=15000)
            time.sleep(3)
            if "login" not in page.url.lower():
                print("✅ Cookies 有效")
                # 測試抓 with_replies
                page.goto("https://x.com/elonmusk/with_replies", timeout=15000)
                time.sleep(3)
                tweets = page.query_selector_all('[data-testid="tweet"]')
                print(f"   /with_replies 找到 {len(tweets)} 篇推文")
                return
            print("   ❌ Cookies 無效，需重新登入")
        
        # 需要登入
        context = try_login(p)
        if context:
            print("\n✅ 登入成功！測試抓取...")
            page = context.new_page()
            page.goto("https://x.com/elonmusk/with_replies", timeout=15000)
            time.sleep(5)
            tweets = page.query_selector_all('[data-testid="tweet"]')
            print(f"   /with_replies 找到 {len(tweets)} 篇推文")
            
            # 嘗試找 Cursor 引用文 (id: 1923967493361774985)
            cursor_link = page.query_selector('a[href*="/status/1923967493361774985"]')
            if cursor_link:
                print("   ✅ 找到 Cursor 引用推文!")
            else:
                print("   ❌ 找不到 Cursor 引用推文")
        else:
            print("\n❌ 登入失敗")

if __name__ == "__main__":
    main()