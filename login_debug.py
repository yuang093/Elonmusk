"""
X.com Login Debug - 診斷登入流程的每一步
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

X_EMAIL = "taeyeon093.bot@gmail.com"
X_PASSWORD = "@#Cctv!!"

def main():
    print("=== X.com 登入診斷 ===\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. 前往登入頁
        print("1️⃣ 前往登入頁...")
        page.goto("https://x.com/i/flow/login", timeout=30000)
        time.sleep(3)
        print(f"   URL: {page.url}")
        
        # 2. 快照所有 input
        print("\n2️⃣ 所有 input 欄位：")
        inputs = page.query_selector_all('input')
        for inp in inputs:
            name = inp.get_attribute('name') or ''
            type_ = inp.get_attribute('type') or ''
            placeholder = inp.get_attribute('placeholder') or ''
            autocomplete = inp.get_attribute('autocomplete') or ''
            id_ = inp.get_attribute('id') or ''
            data_testid = inp.get_attribute('data-testid') or ''
            print(f"   name={name} type={type_} placeholder={placeholder} autocomplete={autocomplete} id={id_} testid={data_testid}")
        
        # 3. 嘗試填入 email（用更廣的 selector）
        print("\n3️⃣ 嘗試填入 email...")
        try:
            # 試各種可能的 selector
            selectors = [
                'input[name="text"]',
                'input[autocomplete="username"]',
                'input[data-testid="ocfEnterTextInput"]',
                'input[type="text"]',
                'input'
            ]
            for sel in selectors:
                try:
                    count = page.locator(sel).count()
                    if count > 0:
                        print(f"   ✅ 找到 selector: {sel} (count={count})")
                        page.fill(sel, X_EMAIL, timeout=3000)
                        print(f"   ✅ 填入成功: {X_EMAIL}")
                        break
                except:
                    pass
        except Exception as e:
            print(f"   ❌ 填入失敗: {e}")
        
        time.sleep(2)
        
        # 4. 點擊下一步
        print("\n4️⃣ 點擊下一步...")
        try:
            # 試各種按鈕
            buttons = page.query_selector_all('button')
            for btn in buttons:
                txt = btn.inner_text().strip()
                if txt:
                    print(f"   button: '{txt}' (testid={btn.get_attribute('data-testid')})")
            
            page.click('button:has-text("下一步"), button:has-text("Next"), [role="button"]:has-text("Next")', timeout=5000)
            print("   ✅ 點擊成功")
        except Exception as e:
            print(f"   ❌ 點擊失敗: {e}")
        
        time.sleep(3)
        print(f"   URL: {page.url}")
        
        # 5. 檢查是否需要 username
        print("\n5️⃣ 檢查是否需要 username...")
        inputs2 = page.query_selector_all('input')
        for inp in inputs2:
            name = inp.get_attribute('name') or ''
            type_ = inp.get_attribute('type') or ''
            placeholder = inp.get_attribute('placeholder') or ''
            autocomplete = inp.get_attribute('autocomplete') or ''
            data_testid = inp.get_attribute('data-testid') or ''
            if name or placeholder:
                print(f"   input: name={name} type={type_} placeholder={placeholder} autocomplete={autocomplete} testid={data_testid}")
        
        # 6. 嘗試填入 username
        try:
            page.fill('input[name="username"], input[autocomplete="username"]', 'taeyeon093_bot', timeout=3000)
            print("   ✅ 填入 username")
            page.click('button:has-text("下一步"), button:has-text("Next")', timeout=5000)
            time.sleep(2)
        except:
            pass
        
        print(f"   URL: {page.url}")
        
        # 7. 嘗試填入密碼
        print("\n7️⃣ 嘗試填入密碼...")
        try:
            # 等密碼欄位出現
            page.wait_for_selector('input[type="password"]', timeout=10000)
            page.fill('input[type="password"]', X_PASSWORD)
            print("   ✅ 密碼填入成功")
            
            # 找登入按鈕
            buttons2 = page.query_selector_all('button')
            for btn in buttons2:
                txt = btn.inner_text().strip()
                if txt and any(k in txt.lower() for k in ['log in', 'sign in', '登入']):
                    print(f"   找到登入按鈕: '{txt}'")
                    btn.click()
                    break
            time.sleep(5)
        except Exception as e:
            print(f"   ❌ 密碼階段失敗: {e}")
        
        print(f"\n📍 最終 URL: {page.url}")
        
        # 8. 截圖
        page.screenshot(path='/tmp/x_login_debug.png')
        print("\n📸 截圖已儲存到 /tmp/x_login_debug.png")

if __name__ == "__main__":
    main()