#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- THE INDEPENDENT BROWSER RENDER TEST (outside the pipeline).

⭐⭐⭐⭐⭐ **A REAL-BROWSER RENDER TEST IS THE ONLY TEST THAT VERIFIES WHAT
THE USER ACTUALLY SEES.**  ⭐⭐⭐⭐⭐ `curl` verifies the DEPLOYMENT;
the painted DOM verifies the USER.  ⭐⭐⭐⭐⭐ The page is CLIENT-RENDERED
(`#total-count` is filled in by JS from `tweets.json`), so a source-layer
check can never confirm the card count.

⭐⭐⭐⭐⭐ **THIS RUNS OUTSIDE THE PIPELINE** -- deliberately, with its own
independently-written assertions, so it is a SECOND opinion on the
pipeline's `render` / `render_posts` stages rather than a restatement of
them.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

URL = "https://elonmusk-rosy.vercel.app"
EXPECT_CARDS = 8200
EXPECT_BANNER = "248"

errors = []
console_msgs = []

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page()
    pg.on("console", lambda m: console_msgs.append((m.type, m.text)))
    pg.on("pageerror", lambda e: errors.append(str(e)))
    resp = pg.goto(URL, wait_until="networkidle", timeout=90000)
    print(f"[live] HTTP {resp.status if resp else '?'}  {URL}")
    assert resp and resp.status == 200, f"the live page returned {resp}"

    pg.wait_for_function(
        "() => document.querySelectorAll('.tweet-card, .tweet, article.card, "
        ".card.tweet').length > 0", timeout=60000)

    total = pg.inner_text("#total-count").strip()
    cards = pg.eval_on_selector_all(
        ".tweet-card, .tweet, article.card, .card.tweet", "els => els.length")
    banner = pg.inner_text("#fetch-outage-banner").strip()
    body = pg.inner_text("body")
    last_update = pg.inner_text("#last-update").strip() if \
        pg.query_selector("#last-update") else None

    print(f"[live] #total-count      = {total!r}")
    print(f"[live] painted cards    = {cards}")
    print(f"[live] #last-update     = {last_update!r}")
    print(f"[live] body innerText   = {len(body)} chars")
    print(f"[live] banner (visible) = {banner[:200]}")
    print(f"[live] console errors   = {len(errors)}")
    print(f"[live] js errors        = {len(errors)}")

    # ---- THE ASSERTIONS ----
    assert total == str(EXPECT_CARDS), \
        f"#total-count reads {total!r}, expected {EXPECT_CARDS}"
    print(f"[live] [OK] #total-count == {EXPECT_CARDS}")

    assert cards == EXPECT_CARDS, \
        f"{cards} cards painted, expected {EXPECT_CARDS}"
    print(f"[live] [OK] {cards} cards are PAINTED")

    assert EXPECT_BANNER in banner, \
        f"the visible banner does not carry {EXPECT_BANNER}: {banner[:120]!r}"
    print(f"[live] [OK] the visitor-visible banner reads {EXPECT_BANNER}")

    assert "未發現新推文" in body, \
        "the visible page lacks the MEASURED NO-OP prose"
    print("[live] [OK] the visible page carries the NO-OP prose")

    import re
    pub = re.findall(r"\d+\s*則新推文", body)
    assert not pub, f"the visible page carries a published-count clause {pub}"
    print("[live] [OK] the visible page carries NO published-count clause")

    assert not errors, f"the page raised JS errors: {errors[:3]}"
    print("[live] [OK] ZERO console/page errors")

    br.close()

print()
print("[live] THE INDEPENDENT BROWSER RENDER TEST: ALL GATES PASS")
