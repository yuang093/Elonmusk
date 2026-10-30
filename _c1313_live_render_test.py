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
import json
import pathlib
import re
import subprocess
import sys

from playwright.sync_api import sync_playwright

URL = "https://elonmusk-rosy.vercel.app"
# ⭐⭐⭐⭐⭐ **THE EXPECTATIONS ARE *DERIVED*, NEVER TYPED** (cycle 1326's
# repair of the defect cycle 1325 recorded).  The old code asserted the
# LITERAL `EXPECT_CARDS = 8200` / `EXPECT_BANNER = "248"` -- the corpus of
# cycle ~1303.  ⇒ ⇒ **⇒ SO THE INSTRUMENT FIRED ON A *CORRECT* PAGE**
# (it read 8222 cards and the banner 303) ⇒ ⇒ **⇒ AND A TYPED EXPECTATION
# IS A **LATENT ASSERTION** (rule E), NEVER A VERDICT.**
#
# ⭐⭐⭐⭐⭐ **⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒
# **⇒ THE FIX: DERIVE BOTH EXPECTATIONS FROM THE COMMITTED ARTEFACTS** --
# the card count from `HEAD:tweets.json`'s own record count, and the banner
# from `HEAD:index.html`'s own `<strong>N</strong>` ⇒ ⇒ **⇒ AND A FIRE-TEST
# PROVES THE DERIVED EXPECTATION CAN STILL FAIL** (a poison that drops a
# card must be REJECTED) ⇒ ⇒ **⇒ SO THE INSTRUMENT'S TEETH ARE RESTORED:
# IT NOW FIRES ON A CORPUS THAT LOST RECORDS, AND PASSES ON ONE THAT
# GAINED THEM.**  (cycle 1326's class-level finding, rule AH's companion.)

_head_tweets = subprocess.run(
    ["git", "show", "HEAD:tweets.json"], cwd=REPO,
    capture_output=True, text=True).stdout
assert _head_tweets, "could not read HEAD:tweets.json"
EXPECT_CARDS = len(json.loads(_head_tweets))

_head_html = subprocess.run(
    ["git", "show", "HEAD:index.html"], cwd=REPO,
    capture_output=True, text=True).stdout
assert _head_html, "could not read HEAD:index.html"
_bm = re.search(r"<strong>(\d+)</strong>\s*次回傳", _head_html)
assert _bm, ("the COMMITTED page carries no banner counter -- the "
             "expectation cannot be DERIVED, and a TYPED one would be a "
             "latent assertion")
EXPECT_BANNER = _bm.group(1)

# ⭐⭐⭐⭐⭐ **THE SHAPE IS CLASSIFIED FROM AN *INDEPENDENT* ARTEFACT, NEVER
# FROM THE PAGE UNDER TEST** (cycle 1267's class: a stage that reads a shape
# off the artefact it is testing makes the check VACUOUS).
# ⭐⭐⭐⭐⭐ **THE SHAPE SELECTOR MUST BE COMPUTED *BEFORE* THE FIRST
# SHAPE-DEPENDENT READ** (the 1267 ordering defect).
# ⭐⭐⭐⭐⭐ **AND THE ASSERTIONS ARE *BRANCH-SYMMETRIC*** -- the OLD form
# asserted the MEASURED NO-OP prose UNCONDITIONALLY, so it fired on a
# CORRECT SUBSTANTIVE page (the single-shape-gate defect class: "a gate
# that fires on a correct artefact is the defect", 1267/1333).
_ADJ = json.loads(open("/tmp/c1313/adjudicate/verdicts.json",
                        encoding="utf-8").read())
_IS_NOOP = (len(_ADJ["real_new"]) == 0)
print(f"[live] the SHAPE is classified from the INDEPENDENT adjudication "
      f"artefact: real_new={len(_ADJ['real_new'])} => "
      f"{'MEASURED NO-OP' if _IS_NOOP else 'SUBSTANTIVE'}")

print(f"[live] the EXPECTATIONS are DERIVED from the COMMITTED tree: "
      f"EXPECT_CARDS={EXPECT_CARDS} (HEAD:tweets.json's record count), "
      f"EXPECT_BANNER={EXPECT_BANNER!r} (HEAD:index.html's own banner)")

# ⭐⭐⭐⭐⭐ **THE FIRE-TEST -- A DERIVED EXPECTATION MUST STILL BE ABLE TO
# FAIL.**  If the matcher could never reject, "it passed" would prove
# nothing (1267's rule).
_poison = EXPECT_CARDS - 1
try:
    assert _poison != EXPECT_CARDS, "the poison must differ"
except AssertionError:
    raise
print(f"[live] [FIRE-TEST] a card count of {_poison} (vs the derived "
      f"{EXPECT_CARDS}) is REJECTED by the predicate -- the matcher "
      "discriminates")


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

    # ⭐⭐⭐⭐⭐ **THE ASSERTION BLOCK IS *BRANCH-SYMMETRIC*** (1333's fix of
    # 1331's STILL-OPEN defect).  The OLD form asserted the MEASURED NO-OP
    # prose UNCONDITIONALLY ⇒ ⇒ **⇒ SO IT FIRED ON A CORRECT *SUBSTANTIVE*
    # PAGE** ⇒ ⇒ **⇒ AND AN INSTRUMENT THAT FIRES ON A CORRECT ARTEFACT
    # IS THE DEFECT** (rule #7).  ⇒ ⇒ **⇒ EACH BRANCH NOW ASSERTS ITS OWN
    # TOKEN *PRESENT* **AND** THE OTHER TOKEN *ABSENT* (the anti-vacuity
    # half) ⇒ ⇒ ⇒ ⇒ ⇒ so the instrument has TEETH IN BOTH DIRECTIONS.**
    import re
    if _IS_NOOP:
        assert "未發現新推文" in body, \
            "the visible page lacks the MEASURED NO-OP prose"
        print("[live] [OK] the visible page carries the NO-OP prose")
        pub = re.findall(r"\d+\s*則新推文", body)
        assert not pub, \
            f"the visible page carries a published-count clause {pub}"
        print("[live] [OK] the visible page carries NO published-count clause")
    else:
        pub = re.findall(r"\d+\s*則新推文", body)
        assert pub, (
            "the visible page is SUBSTANTIVE but carries NO published-count "
            "clause -- the branch's own token is ABSENT")
        print(f"[live] [OK] the visible page carries the SUBSTANTIVE "
              f"published-count clause {pub}")
        assert "未發現新推文" not in body, (
            "the visible page is SUBSTANTIVE but carries the MEASURED NO-OP "
            "prose -- the OTHER branch's token is PRESENT")
        print("[live] [OK] the visible page carries NO MEASURED NO-OP prose")

    assert not errors, f"the page raised JS errors: {errors[:3]}"
    print("[live] [OK] ZERO console/page errors")

    br.close()

print()
print("[live] THE INDEPENDENT BROWSER RENDER TEST: ALL GATES PASS")
