#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- VERCEL DEPLOY VERIFICATION, at EVERY tier that carries an
artefact (the cycle-1190 rule: assert each artefact where it actually lives).

  * deploy stamp        -> the deploy-stamp.txt FILE served directly
  * record count/id set -> the tweets.json DATA endpoint
  * banner markup       -> the served index.html SOURCE
  * what a visitor reads-> the RENDERED DOM (a separate step)

TWO-STAGE ONLY: every fetch is written to disk, then parsed from disk.
Never `curl | interpreter` -- the security scanner blocks it and a cron
session has nobody to approve it.

THE 3-TIER SLEEP RECOVERY: tweets.json is a data endpoint behind a CDN, so
its edge cache can lag the deploy.  The retry is bounded and it REPORTS what
it did rather than silently passing.

⭐ THE EXPECTED VALUES ARE DERIVED FROM THE COMMITTED TREE AND THIS CYCLE'S
OWN ADJUDICATION ARTEFACT -- never typed.  A typed id list goes stale the
moment the next cycle publishes.
"""
import json
import pathlib
import re
import subprocess
import sys
import time

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
OUT = pathlib.Path("/tmp/c1313/verify")
OUT.mkdir(parents=True, exist_ok=True)
CYCLE = "1313"
MAX_WAIT = 180

# ⭐ the published ids come from THIS cycle's adjudication artefact
_ADJ = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                  .read_text(encoding="utf-8"))
PUBLISHED = list(_ADJ["real_new"])
N_PUBLISHED = len(PUBLISHED)


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def fetch(url, dest, extra=()):
    """Fetch to a FILE (two-stage), never into an interpreter."""
    cmd = f"curl -sS -L --max-time 60 {' '.join(extra)} {url} -o {dest}"
    rc, out, err = sh(cmd)
    return rc, err


def main():
    rc, out, err = sh("git show HEAD:deploy-stamp.txt")
    assert rc == 0, err
    stamp_local = out.strip()
    m = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) CST = cycle (\d+) = (\S+)",
                 stamp_local)
    assert m, f"unparseable local stamp: {stamp_local!r}"
    assert m.group(2) == CYCLE, f"the local stamp names cycle {m.group(2)}"
    URL = m.group(3)
    print(f"[verify] target URL (re-read from the COMMITTED stamp): {URL}")

    rc, out, err = sh("git show HEAD:index.html")
    page_local = out
    rc2, tj_local, err2 = sh("git show HEAD:tweets.json")
    recs_local = json.loads(tj_local)
    ids_local = {t["id"] for t in recs_local}
    ban_local = int(re.search(r"<strong>(\d+)</strong> 次回傳",
                               page_local).group(1))
    HEAD_ID = max(ids_local, key=lambda i: int(i))
    print(f"[verify] local: {len(recs_local)} records, banner {ban_local}, "
          f"{len(ids_local)} unique ids, head {HEAD_ID}")

    # ---------- TIER 1: the deploy stamp, served directly ----------
    p_stamp = OUT / "deploy-stamp.txt"
    stamp_remote = ""
    waited = 0
    while True:
        rc, err = fetch(f"{URL}/deploy-stamp.txt", p_stamp)
        assert rc == 0, f"the stamp fetch failed: {err[:300]}"
        stamp_remote = p_stamp.read_text(encoding="utf-8",
                                         errors="replace").strip()
        if stamp_remote == stamp_local:
            break
        print(f"[verify] TIER 1: the served stamp is {stamp_remote!r} (waiting "
              f"for the deploy; {waited}s)")
        if waited >= MAX_WAIT:
            raise SystemExit(
                f"[verify] TIER 1 FAILED after {waited}s: the served stamp is "
                f"{stamp_remote!r}, not the committed {stamp_local!r} -- the "
                "deploy has not landed")
        time.sleep(15)
        waited += 15
    print(f"[verify] TIER 1 deploy-stamp.txt: remote={stamp_remote!r} "
          f"(waited {waited}s)")
    assert f"cycle {CYCLE}" in stamp_remote, "the served stamp lacks this cycle"

    # ---------- TIER 2: the served index.html SOURCE ----------
    p_page = OUT / "index.html"
    rc, err = fetch(f"{URL}/index.html", p_page)
    assert rc == 0, f"the page fetch failed: {err[:300]}"
    page_remote = p_page.read_text(encoding="utf-8", errors="replace")
    ban_remote = int(re.search(r"<strong>(\d+)</strong> 次回傳",
                               page_remote).group(1))
    print(f"[verify] TIER 2 index.html: banner={ban_remote}")
    assert ban_remote == ban_local, (
        f"the served banner {ban_remote} != the committed {ban_local}")
    assert f"<!-- cron cycle {CYCLE}:" in page_remote, (
        "the served page lacks this cycle's comment")
    assert "證明是截斷的" not in page_remote, (
        "the served page carries the WITHDRAWN truncation claim")
    assert "並不能" in page_remote and "證明資料被截斷" in page_remote, (
        "the served page lacks the correction")
    # ⭐⭐⭐⭐⭐ CYCLE 1255's FIX: THE SERVED-PAGE PROSE GATE IS
    # BRANCH-SYMMETRIC.  ⭐⭐⭐⭐⭐ **THE VERIFIER MUST ASSERT THE SHAPE'S
    # OWN PROSE AND PROVE THE OTHER'S ABSENCE** -- on a NO-OP the served
    # page says 未發現新推文 and must NOT say "找到了 N 則新推文"; on a
    # SUBSTANTIVE cycle the reverse.
    if N_PUBLISHED == 0:
        assert "未發現新推文" in page_remote, (
            "the served page does not carry the 0-new-post prose -- this "
            "cycle published nothing")
        assert "找到了 0 則新推文" not in page_remote, (
            "the served page claims it FOUND 0 new tweets in the "
            "SUBSTANTIVE prose -- but this cycle is a MEASURED NO-OP")
    else:
        assert f"{N_PUBLISHED} 則新推文" in page_remote, (
            "the served page does not say how many new tweets it published "
            f"-- this cycle published {N_PUBLISHED} posts")
        assert "未發現新推文" not in page_remote, (
            "the served page says 'no new tweets found' — this cycle "
            f"published {N_PUBLISHED}")
    assert "writer_guard = NO_EVIDENCE_THIS_HOUR" in page_remote, (
        "the served page lacks this hour's OUT-OF-BAND guard verdict — the "
        "hour is NOT in RETRY_TRANSLATION_HOURS, so the branch NEVER RAN")
    assert "writer_guard = FIRED" not in page_remote, (
        "the served page carries the IN-BAND guard verdict — this hour "
        "was OUT OF BAND")
    assert "the empty-translation retry branch NEVER RAN" in page_remote, (
        "the served page does not record that the branch NEVER RAN this hour")
    assert "NEGATIVE CONTROL" in page_remote, (
        "the served page does not name the negative control")
    assert "control set is UNCHANGED, NOT flipped" in page_remote, (
        "the served page does not state that the control set is UNCHANGED")
    assert "the control set FLIPS" not in page_remote, (
        "the prior COMMITTED cycle was ALSO out of band and this one is OUT OF BAND too, "
        "-- the control set is UNCHANGED, so the served page must not say it FLIPS"
        "FLIPS")
    assert "BORROWED and explicitly DISCLAIMED" in page_remote, (
        "on an OUT-OF-BAND hour the count is BORROWED from the positive "
        "control and DISCLAIMED -- the served page must say so")
    assert "NOT borrowed and NOT disclaimed" not in page_remote, (
        "on an OUT-OF-BAND hour the count is NOT this hour's own evidence "
        "-- the served page must not claim it is")
    assert "POSITIVE CONTROL" in page_remote, (
        "on an OUT-OF-BAND hour there IS a positive control -- the served "
        "page must name one")
    assert page_remote.count("<!--") == page_remote.count("-->"), (
        f"the served page has unbalanced comment delimiters "
        f"({page_remote.count('<!--')} vs {page_remote.count('-->')})")
    assert len(re.findall(r"<!--\s*cron cycle \d+:", page_remote)) == 1, (
        "the served page does not carry exactly ONE cycle comment")
    print(f"[verify] TIER 2 PASS: the served page carries the banner "
          f"{ban_remote}, the {N_PUBLISHED}-post prose, the correction, the "
          f"OUT-OF-BAND verdict, the NEGATIVE CONTROL, and exactly one cycle "
          f"comment with balanced delimiters")

    # ---------- TIER 3: the tweets.json DATA endpoint (edge-cache lag) ----------
    p_tj = OUT / "tweets.json"
    got = None
    waited = 0
    ids_remote = set()
    while True:
        rc, err = fetch(f"{URL}/tweets.json", p_tj)
        assert rc == 0, f"the tweets.json fetch failed: {err[:300]}"
        try:
            got = json.loads(p_tj.read_text(encoding="utf-8"))
        except Exception as e:
            got = None
            print(f"[verify] TIER 3: the served tweets.json did not parse "
                  f"({e}); retrying")
        if got is not None:
            ids_remote = {t["id"] for t in got}
            if len(ids_remote) == len(ids_local) and ids_remote == ids_local:
                break
            print(f"[verify] TIER 3: served {len(got)} records / "
                  f"{len(ids_remote)} ids vs local {len(recs_local)} / "
                  f"{len(ids_local)} -- the CDN edge cache may lag; waiting")
        if waited >= MAX_WAIT:
            raise SystemExit(
                f"[verify] TIER 3 FAILED after {waited}s: the served "
                f"tweets.json never matched the committed id set "
                f"(local {len(ids_local)} ids, served "
                f"{len(ids_remote) if got else 0})")
        time.sleep(15)
        waited += 15
    print(f"[verify] TIER 3 tweets.json: {len(got)} records, id set EQUAL to "
          f"local (waited {waited}s)")
    assert len(got) == len(recs_local)
    _by = {t["id"]: t for t in got}
    assert HEAD_ID in ids_remote, f"{HEAD_ID} is missing from the served corpus"
    assert (_by[HEAD_ID].get("translation") or "").strip(), (
        f"{HEAD_ID} is served with an EMPTY translation")
    # this cycle's published ids MUST be served, WITH translations
    for _pid in PUBLISHED:
        assert _pid in ids_remote, (
            f"the published id {_pid} is missing from the served corpus")
        assert (_by[_pid].get("translation") or "").strip(), (
            f"the published id {_pid} is served with an EMPTY translation")
        assert (_by[_pid].get("original") or "").strip(), (
            f"the published id {_pid} is served with an EMPTY original")
    print(f"[verify] the head record {HEAD_ID} AND all {N_PUBLISHED} published "
          f"ids are served WITH their translations and originals")

    print(f"[verify] ALL TIERS PASS: stamp, index.html source, tweets.json "
          f"id set")
    print(f"[verify] -> {OUT}")


if __name__ == "__main__":
    main()
