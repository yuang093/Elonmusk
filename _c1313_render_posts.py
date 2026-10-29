#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- the PUBLISHED-POSTS render test.

The general render test asserts the corpus is painted and the head post's
translation is visible.  This one asserts that EACH of the 7 posts published
THIS cycle is actually reachable by a visitor -- because a post that is in
tweets.json but never rendered is a silent publication failure, and the
generic card-count assertion cannot see it.

Run with the PROJECT venv's python (playwright lives there):
    ~/elon-tweets/venv/bin/python3 _c1313_render_posts.py

THE EXPECTED VALUES ARE DERIVED FROM THE COMMITTED TREE AND THIS CYCLE'S OWN
ADJUDICATION ARTEFACT, NEVER TYPED.
"""
import json
import pathlib
import re
import subprocess
import sys

from playwright.sync_api import sync_playwright

REPO = "/Users/taeyeon093.bot/elon-tweets"
CYCLE = "1313"

# ⭐ THE PUBLISHED IDS COME FROM THIS CYCLE'S OWN ADJUDICATION ARTEFACT
_ADJ = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                  .read_text(encoding="utf-8"))
PUBLISHED = list(_ADJ["real_new"])


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


rc, out, err = sh(f"cd {REPO} && git show HEAD:deploy-stamp.txt")
assert rc == 0, err
URL = re.search(r"=\s*(\S+)$", out.strip()).group(1)
rc, out, err = sh(f"cd {REPO} && git show HEAD:tweets.json")
assert rc == 0, err
_BY = {t["id"]: t for t in json.loads(out)}
for pid in PUBLISHED:
    assert pid in _BY, f"{pid} is not in the COMMITTED corpus"
    assert (_BY[pid].get("translation") or "").strip(), (
        f"{pid} is committed with an EMPTY translation")
    assert (_BY[pid].get("original") or "").strip(), (
        f"{pid} is committed with an EMPTY original")
print(f"[render2] url={URL}; {len(PUBLISHED)} published posts, all committed "
      f"with non-empty translations and originals")

errors = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.on("console", lambda m: errors.append(f"{m.type}: {m.text}")
            if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    resp = page.goto(URL, wait_until="networkidle", timeout=90000)
    assert resp is not None and resp.status == 200, "the page did not answer 200"
    page.wait_for_timeout(2500)

    # ---- the rendered card for each published post ----
    # ⭐ THE CARD CARRIES NO ID.  The page's card markup is
    # .tweet-card > .tweet-meta / .tweet-images / .tweet-section x2 /
    # .tweet-metrics -- there is NO per-card id, no data-* attribute and no
    # anchor to the status permalink.  So a card must be located by its
    # CONTENT: the committed ORIGINAL's first paragraph, which is painted in
    # the .tweet-original section.
    for pid in PUBLISHED:
        want = (_BY[pid].get("translation") or "").strip()
        orig = (_BY[pid].get("original") or "").strip()
        # a distinctive slice of the ORIGINAL's own first paragraph
        needle = orig.split("\n\n")[0].strip()[:28]
        assert needle, f"{pid} has an empty original"
        got = page.evaluate(
            """(needle) => {
                const cards = Array.from(document.querySelectorAll('.tweet-card'));
                for (const c of cards) {
                    const o = c.querySelector('.tweet-original');
                    if (o && o.innerText.indexOf(needle) !== -1) {
                        const tr = c.querySelector('.tweet-translation');
                        const t = c.querySelector('.tweet-time');
                        return {
                            translation: tr ? tr.innerText.trim() : '',
                            original: o.innerText.trim(),
                            time: t ? t.innerText.trim() : ''
                        };
                    }
                }
                return null;
            }""", needle)
        assert got is not None, (
            f"the published post {pid} has NO rendered card -- it is in "
            "tweets.json but a visitor cannot see it (a silent publication "
            "failure the generic card-count assertion cannot detect)")
        assert got["translation"].strip(), (
            f"the rendered card for {pid} has an EMPTY translation")
        assert want[:24] in got["translation"], (
            f"the painted translation for {pid} does not match the committed "
            f"one: {got['translation'][:60]!r} vs {want[:60]!r}")
        assert orig.split("\n\n")[0].strip()[:24] in got["original"], (
            f"the painted ORIGINAL for {pid} does not match the committed one")
        print(f"[render2] {pid}: painted card OK (time {got['time']!r}), "
              f"translation matches the committed text "
              f"({len(got['translation'])} chars)")

    # ---- and the ORIGINAL is painted too (the page shows translation ABOVE
    #      original, per the house convention) ----
    txt = page.inner_text("body")
    for pid in PUBLISHED:
        orig = (_BY[pid].get("original") or "").strip()
        first_para = orig.split("\n\n")[0].strip()
        assert first_para[:20] in txt, (
            f"the ORIGINAL's first paragraph for {pid} is not visible on the "
            f"page: {first_para[:40]!r}")
    print(f"[render2] all {len(PUBLISHED)} published posts' originals are "
          f"visible too")

    assert not errors, f"console errors on the page: {errors[:5]}"
    print("[render2] ZERO console errors")
    browser.close()
print("[render2] ALL PUBLISHED-POST RENDER GATES PASS")
sys.exit(0)
