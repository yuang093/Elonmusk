"""
X.com Login Debug v2 - 更穩健的登入流程
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

X_EMAIL = "taeyeon093.bot@gmail.com"
X_PASSWORD = "@#Cctv!!"

def main():
    print("=== X.com 登入診斷 v2 ===\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. 前往登入頁
        print("1️⃣ 前往登入頁...")
        page.goto("https://x.com/i/jf/onboarding/web?mode=login", timeout=30000)
        time.sleep(3)
        print(f"   URL: {page.url}")
        
        # 2. 等待 username 欄位出現
        print("\n2️⃣ 等待 username 欄位...")
        try:
            page.wait_for_selector('input[name="username_or_email"]', timeout=15000)
            print("   ✅ 欄位出現")
        except Exception as e:
            print(f"   ❌ 欄位未出現: {e}")
            page.screenshot(path='/tmp/x_debug_step1.png')
            print("   📸 截圖 /tmp/x_debug_step1.png")
            return
        
        # 3. 填入 email
        print("\n3️⃣ 填入 email...")
        page.fill('input[name="username_or_email"]', X_EMAIL)
        print(f"   ✅ 已填入: {X_EMAIL}")
        time.sleep(1)
        
        # 4. 點擊 Continue
        print("\n4️⃣ 點擊 Continue...")
        page.click('button:has-text("Continue")')
        print("   ✅ 已點擊")
        time.sleep(3)
        print(f"   URL: {page.url}")
        
        # 5. 可能需要輸入 username 或密碼
        print("\n5️⃣ 檢查當前狀態...")
        try:
            # 如果來到密碼階段
            pw_field = page.query_selector('input[name="password"]')
            if pw_field:
                print("   → 來到密碼階段")
                page.fill('input[name="password"]', X_PASSWORD)
                print("   ✅ 密碼已填入")
                time.sleep(1)
                page.click('button:has-text("Log in"), button:has-text("Continue")')
                print("   ✅ 已點擊登入")
                time.sleep(5)
            else:
                print("   → 仍在 username 階段，嘗試 username...")
                try:
                    page.fill('input[name="username_or_email"]', 'taeyeon093_bot')
                    page.click('button:has-text("Continue")')
                    time.sleep(3)
                    # 再檢查密碼
                    pw_field = page.query_selector('input[name="password"]')
                    if pw_field:
                        page.fill('input[name="password"]', X_PASSWORD)
                        time.sleep(1)
                        page.click('button:has-text("Log in"), button:has-text("Continue")')
                        time.sleep(5)
                except Exception as e:
                    print(f"   username 階段失敗: {e}")
        except Exception as e:
            print(f"   階段檢查失敗: {e}")
        
        print(f"\n📍 最終 URL: {page.url}")
        
        # 6. 截圖
        page.screenshot(path='/tmp/x_login_final.png')
        print("\n📸 截圖已儲存到 /tmp/x_login_final.png")
        
        # 7. 嘗試前往 elonmusk 主頁測試
        if "login" not in page.url.lower():
            print("\n7️⃣ 測試是否真的登入成功...")
            page.goto("https://x.com/elonmusk", timeout=15000)
            time.sleep(3)
            print(f"   URL: {page.url}")
            if "login" not in page.url.lower():
                print("   ✅ 真的登入成功！")
                # 儲存 cookies
                cookies = context.cookies()
                with open('/Users/taeyeon093.bot/elon-tweets/.x_cookies.json', 'w') as f:
                    import json
                    json.dump(cookies, f)
                print("   ✅ Cookies 已儲存")
            else:
                print("   ❌ 仍需登入")
        else:
            print("   ❌ 登入失敗")

if __name__ == "__main__":
    main()