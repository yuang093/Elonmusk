#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- the RENDER TEST (client-side rendering on the DEPLOYED page).

Run with the PROJECT venv's python (playwright lives there, not in the
Hermes runtime venv):  ~/elon-tweets/venv/bin/python3 _c1313_render.py

THE CYCLE-1190 RULE: **curl verifies the DEPLOYMENT; the BROWSER verifies the
USER.**  The page is client-rendered: `#total-count` is filled in by JS from
`fetch('tweets.json')`, and the banner's numbers live in the HTML.  A gate
that asserts against the HTML source alone is asserting against the wrong
layer.  So this test measures the PAINTED DOM.

THE EXPECTED VALUES ARE DERIVED, NOT TYPED: the record count and the banner
number are read from the COMMITTED tree (git), the head id is derived from
the corpus's own timestamps, and the tail gaps are read from the served
page's own banner text -- so the test cannot pass against a stale
expectation.

What it asserts, on the LIVE deployed page:
  * the cards are PAINTED (client-side JS ran);
  * the card count equals the corpus record count;
  * the visitor-visible banner reads the MEASURED zero-article counter;
  * the SHAPE-DEFING prose is visible and MATCHES the COMMITTED page's
    shape -- the "N 則新推文" prose is visible and the "未發現新推文"
    prose is ABSENT on a SUBSTANTIVE page; the mirror image on a
    MEASURED NO-OP page (the shape is classified from THIS cycle's own
    adjudication, never from the page under test);
  * the CORRECTION is visible and the WITHDRAWN claim is absent;
  * the MEASURED hole window and BOTH tail gaps are visible;
  * the head post's translation is painted (not empty);
  * ZERO console errors.
"""
import datetime as dt
import json
import re
import subprocess
import sys

from playwright.sync_api import sync_playwright

REPO = "/Users/taeyeon093.bot/elon-tweets"
CYCLE = "1313"
SNOWFLAKE_EPOCH_MS = 1288834974657


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


rc, out, err = sh(f"cd {REPO} && git show HEAD:deploy-stamp.txt")
assert rc == 0, err
URL = re.search(r"=\s*(\S+)$", out.strip()).group(1)
rc, out, err = sh(f"cd {REPO} && git show HEAD:tweets.json")
assert rc == 0, err
_RECS = json.loads(out)
EXPECT_CARDS = len(_RECS)
_BY = {t["id"]: t for t in _RECS}
# ⭐ THE HEAD ID IS DERIVED FROM THE CORPUS'S OWN TIMESTAMPS
HEAD_ID = max(_BY, key=lambda i: int(i))
EXPECT_HEAD_TR = _BY[HEAD_ID].get("translation") or ""
assert EXPECT_HEAD_TR.strip(), "the head record has an empty translation"
rc, out, err = sh(f"cd {REPO} && git show HEAD:index.html")
assert rc == 0, err
EXPECT_BAN = int(re.search(r"<strong>(\d+)</strong> 次回傳", out).group(1))

# ⭐⭐⭐⭐⭐ **THE HOLE WINDOW IS *DERIVED*, NOT TYPED** (cycle 1313's
# repair, the THIRTIETH MEMBER of the family).  The old code asserted the
# LITERAL `"2026-10-19 16:27"` / `"2026-10-23 17:04"` -- the hole window
# when there were TWO big gaps.  ⇒ ⇒ **⇒ THE CORPUS GREW ⇒ A THIRD BIG
# GAP OPENED ⇒ THE HOLE'S END MOVED** ⇒ ⇒ **⇒ THE TYPED LITERAL WOULD
# HAVE FAILED ON A PAGE THAT IS CORRECT** ⇒ ⇒ **⇒ THE SAME CLASS AS
# 1297's `len(big) == 2`.  ⇒ ⇒ **⇒ THE VALUES COME FROM THE ARTEFACT
# THAT OWNS THEM** (`measured.json` -- the same artefact `page.py` read
# them from, and the one that owns the hole envelope) ⇒ ⇒ **⇒ SO THE
# RENDER TEST CANNOT PASS AGAINST A STALE EXPECTATION.**
_M = json.loads(open("/tmp/c1313/measure/measured.json",
                     encoding="utf-8").read())
_HOLE_LO_STR = str(_M["hole_lo"])[:16].replace("T", " ")
_HOLE_HI_STR = str(_M["hole_hi"])[:16].replace("T", " ")

# ⭐⭐⭐⭐⭐ **THE SHAPE IS CLASSIFIED FROM AN INDEPENDENT ARTEFACT, NEVER
# FROM THE PAGE UNDER TEST.**  ⭐⭐⭐⭐⭐ The COMMITTED page's shape is
# read from THIS CYCLE'S OWN ADJUDICATION (`verdicts.json` -- the SAME
# source `commit.py` and `jobs_verify.py` use), because reading the shape
# off the artefact you are testing makes the check VACUOUS.
_ADJ = json.loads(open("/tmp/c1313/adjudicate/verdicts.json",
                        encoding="utf-8").read())
_IS_NOOP = (len(_ADJ["real_new"]) == 0)

# ⭐⭐⭐⭐⭐ **THE CANONICAL BRANCH-SYMMETRIC FORM.**  ⭐⭐⭐⭐⭐ The pattern
# is INLINED IN EACH BRANCH -- hoisting it into a shared constant only
# RELOCATES the defect -- and EACH BRANCH ASSERTS ITS OWN TOKEN PRESENT
# (that is what makes the branch speak FOR its token) PLUS THE OTHER
# TOKEN ABSENT (the anti-vacuity half).
if _IS_NOOP:
    assert "未發現新推文" in out, (
        "the committed page is a MEASURED NO-OP but carries no NO-OP prose")
    assert not re.search(r"找到了 <b>(\d+) 則新推文</b>", out), (
        "a MEASURED NO-OP page must NOT carry the SUBSTANTIVE "
        "published-count prose")
    N_PUBLISHED = 0
else:
    _m = re.search(r"找到了 <b>(\d+) 則新推文</b>", out)
    assert _m, "the committed banner does not state the published-post count"
    N_PUBLISHED = int(_m.group(1))
    assert N_PUBLISHED >= 1, (
        f"the committed page states {N_PUBLISHED} published posts -- but "
        "this cycle's own adjudication says it is SUBSTANTIVE")
    assert "未發現新推文" not in out, (
        "a SUBSTANTIVE page must NOT carry the MEASURED NO-OP prose")

# ⭐⭐⭐⭐⭐ **THE COMMITTED PAGE'S SHAPE MUST AGREE WITH THE ADJUDICATION.**
_IS_NOOP_PAGE = ("未發現新推文" in out and
                 not re.search(r"找到了 <b>(\d+) 則新推文</b>", out))
assert _IS_NOOP_PAGE == _IS_NOOP, (
    f"the committed page's shape (NO-OP={_IS_NOOP_PAGE}) disagrees with this "
    f"cycle's own adjudication (NO-OP={_IS_NOOP}) -- the two artefacts "
    "disagree about the world")
# the tail gaps, read from the COMMITTED banner's own prose
_m = re.search(r"之間約有 <b>([\d.]+) 小時</b>的間隙", out)
assert _m, "the committed banner does not name the tail gap"
TAIL1 = _m.group(1)
_m = re.search(r"上一輪所稱的 ([\d.]+) 小時尾端間隙", out)
assert _m, "the committed banner does not name the prior tail gap"
TAIL2 = _m.group(1)
print(f"[render] derived from the COMMITTED tree: url={URL}, "
      f"cards={EXPECT_CARDS}, banner={EXPECT_BAN}, published={N_PUBLISHED}, "
      f"tails={TAIL1}/{TAIL2}, head={HEAD_ID}")

errors = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.on("console", lambda m: errors.append(f"{m.type}: {m.text}")
            if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    resp = page.goto(URL, wait_until="networkidle", timeout=90000)
    print(f"[render] HTTP {resp.status if resp else '?'}")
    page.wait_for_timeout(2500)

    txt = page.inner_text("body")
    print(f"[render] body innerText length = {len(txt)}")

    total = page.eval_on_selector(
        "#total-count", "el => el ? el.innerText.trim() : null")
    print(f"[render] #total-count = {total!r}")

    n_cards = page.eval_on_selector_all(
        ".tweet-card, .tweet, article.card, .card.tweet",
        "els => els.length")
    print(f"[render] painted card elements = {n_cards}")

    banner = page.eval_on_selector(
        "#fetch-outage-banner",
        "el => el ? el.innerText : null")
    print(f"[render] banner text = {(banner or '')[:160]!r}")

    head_tr = page.eval_on_selector_all(
        ".tweet-translation",
        "els => els.length ? els[0].innerText.trim() : null")
    print(f"[render] head post translation = {head_tr!r}")

    # ---- assertions on the VISIBLE page ----
    assert resp is not None and resp.status == 200, "the page did not answer 200"
    assert total is not None, "#total-count is missing from the rendered page"
    assert total.replace(",", "").strip() == str(EXPECT_CARDS), (
        f"#total-count reads {total!r}, expected {EXPECT_CARDS}")
    assert n_cards >= 1, (
        "no tweet cards were painted -- the client-side render did not run")
    assert n_cards == EXPECT_CARDS, (
        f"{n_cards} cards painted, expected {EXPECT_CARDS} -- the render is "
        "not showing the whole corpus")
    assert f"已連續 {EXPECT_BAN} 次回傳 0 則推文" in txt, (
        f"the visitor-visible banner does not read {EXPECT_BAN}")
    assert "下限" in txt, "the 下限 (lower-bound) wording is not visible"
    # ⭐⭐⭐⭐⭐ **THE VISIBLE LAYER IS BRANCH-SYMMETRIC TOO** -- the VISIBLE
    # prose must match the SAME shape the COMMITTED page carries.
    if _IS_NOOP:
        assert "未發現新推文" in txt, (
            "the MEASURED NO-OP prose is not visible")
        assert not re.search(r"找到了 <b>(\d+) 則新推文</b>", txt), (
            "the VISIBLE layer carries the SUBSTANTIVE published-count prose "
            "on a MEASURED NO-OP page")
    else:
        assert f"{N_PUBLISHED} 則新推文" in txt, (
            "the published-post prose is not visible -- this cycle published "
            f"{N_PUBLISHED}")
        assert "未發現新推文" not in txt, (
            "the page says 'no new tweets found' -- this cycle published "
            f"{N_PUBLISHED}")
    assert "並不能" in txt and "證明資料被截斷" in txt, (
        "the CORRECTION of the truncation claim is not visible")
    assert "證明是截斷的" not in txt, (
        "the WITHDRAWN truncation claim is visible on the page")
    assert _HOLE_LO_STR in txt and _HOLE_HI_STR in txt, (
        f"the MEASURED hole window ({_HOLE_LO_STR} -> {_HOLE_HI_STR}) is "
        "not visible")
    assert TAIL1 in txt and TAIL2 in txt, (
        f"one of the two tail gaps is not visible ({TAIL1} / {TAIL2})")
    assert "置頂貼文 1 則" in txt, (
        "the render's measured STRUCTURE is not stated on the page")
    assert head_tr, "the head post's translation is empty -- nothing was painted"
    # the PAINTED translation must be the committed one (not a stub)
    assert EXPECT_HEAD_TR[:12] in head_tr, (
        f"the painted head translation does not match the committed one: "
        f"{head_tr[:60]!r} vs {EXPECT_HEAD_TR[:60]!r}")
    assert not errors, f"console errors on the page: {errors[:5]}"
    print(f"[render] the head post's translation is painted: {head_tr[:60]!r}")
    print("[render] ZERO console errors")
    browser.close()
print("[render] ALL RENDER GATES PASS")
sys.exit(0)
