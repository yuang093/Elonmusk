#!/usr/bin/env python3
"""Debug - find quote tweet element structure"""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto("https://x.com/elonmusk", timeout=30000)
    page.wait_for_selector('[data-testid="tweet"]', timeout=15000)
    time.sleep(3)
    
    # Scroll to top
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(2)
    
    # Get full HTML around the Cursor tweet if it exists
    html = page.content()
    
    # Search for mntruell in page source
    if "mntruell" in html:
        print("✅ mntruell found in page source!")
        idx = html.find("mntruell")
        print(f"Context: {html[max(0,idx-200):idx+300]}")
    else:
        print("❌ mntruell NOT in page source")
    
    # Also check for Cursor
    if "Cursor" in html:
        print("✅ Cursor found in page source!")
        idx = html.find("Cursor")
        print(f"Context: {html[max(0,idx-100):idx+200]}")
    else:
        print("❌ Cursor NOT in page source")
    
    # Check what "with_replies" page looks like with auth
    # Try to get cookies from the current page session
    cookies = page.context.cookies()
    print(f"\nCookies: {len(cookies)}")
    for c in cookies[:3]:
        print(f"  {c['name']}: {c['value'][:30]}...")
    
    browser.close()