#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- probe read paths for posts NEWER than the corpus head.

RULES CARRIED FORWARD (cycle numbering from the skill snapshot):
  * cycle 1278: validate an id by an INDEPENDENT CLOCK (snowflake decode must
    agree with the post's own created_at) -- never by shape alone.
  * cycle 1249: a DOMAIN KEY is a rate-limit bucket.  A blocked key must be
    retried on a DIFFERENT key of the same site; a blocked path is recorded
    UNAVAILABLE -- never counted as agreement.
  * cycle 1251: a FORMAT CANNOT CARRY WHAT IT STRIPS.  Run >1 format per URL
    and take the UNION of the ids.
  * cycle 1249: an id must pass the clock check AND the author check.
  * cycle 1251: a verdict computed from an EMPTY set is not a verdict.
  * cycle 1249: the head is DERIVED from the corpus, never hardcoded.
  * cycle 1251: keep trying the x.com jina key FIRST; run BOTH formats; take
    the union; and probe the SINGLE-STATUS page too -- it is a third id source.
  * cycle 1249: A CANDIDATE SET IS NOT INHERITABLE -- always re-derive.
  * cycle 1251: MEASURE THE DELTA AGAINST HEAD.  ⭐⭐⭐ **THE DELTA IS
    MEASURED AT RUN TIME, NEVER TYPED** -- a copied record count is a
    LATENT ASSERTION ABOUT THIS RUN'S SHAPE (Reminder 37), and it rots:
    this cycle's worktree carries a ZERO-record delta against HEAD
    (8,163 == 8,163), while the inherited prose claimed 5.  ⭐⭐ **THE
    SCRIPT ITSELF MEASURES `git diff --stat tweets.json` against
    `HEAD:tweets.json`** and reports the worktree-only ids SEPARATELY --
    because a worktree-only delta is a LIABILITY, not an asset: those
    records are NOT published, so they must be re-adjudicated as
    candidates, not assumed published.  ⭐ The corpus baseline for "is
    this id new?" is therefore HEAD:tweets.json.

TWO-STAGE ONLY: every fetch is written to disk, then parsed from disk.
Never curl | interpreter.
"""
import datetime as dt
import json
import pathlib
import re
import subprocess
import urllib.error
import urllib.request

OUT = pathlib.Path("/tmp/c1313/paths")
OUT.mkdir(parents=True, exist_ok=True)
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
SNOWFLAKE_EPOCH_MS = 1288834974657
REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")

JINA_COMMON = {"x-no-cache": "true", "x-cache-tolerance": "0", "X-Timeout": "45"}


def snowflake_ts(tid):
    ms = (int(tid) >> 22) + SNOWFLAKE_EPOCH_MS
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc)


def http_get(url, headers=None, timeout=90):
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return 0, f"{type(e).__name__}: {e}"


def corpus_state():
    """Baseline = HEAD (committed).  Worktree ids reported separately."""
    head_raw = subprocess.run(["git", "show", "HEAD:tweets.json"], cwd=REPO,
                              capture_output=True, text=True).stdout
    head = json.loads(head_raw)
    head_ids = {t["id"] for t in head}
    work = json.loads((REPO / "tweets.json").read_text(encoding="utf-8"))
    work_ids = {t["id"] for t in work}
    ts = sorted(dt.datetime.fromisoformat(t["created_at"].replace("Z", "+00:00"))
                for t in work)
    return head, head_ids, work_ids, ts


ID_RE = re.compile(r"status/(\d{15,25})")
ID_RE_BARE = re.compile(r"\b(\d{19})\b")
LINKED_RE = re.compile(
    r"https?://(?:twitter\.com|x\.com)/([A-Za-z0-9_]{1,15})/status/(\d{15,25})")


def collect_ids(text):
    ids = set(ID_RE.findall(text))
    bare = set(ID_RE_BARE.findall(text))
    authors = {}
    for author, tid in LINKED_RE.findall(text):
        authors.setdefault(tid, set()).add(author.lower())
    return ids, bare, authors


def main():
    head, head_ids, work_ids, ts = corpus_state()
    head_ts = ts[-1]
    worktree_only = sorted(work_ids - head_ids)
    # DERIVED, never hardcoded
    head_id = max(head_ids, key=lambda i: snowflake_ts(i))
    print(f"HEAD CORPUS: {len(head)} records, DERIVED head id {head_id} "
          f"@ {head_ts.isoformat()}")
    print(f"WORKTREE: {len(work_ids)} ids, {len(worktree_only)} written-but-never-"
          f"committed (INHERITED, must be re-adjudicated): {worktree_only}")
    print(f"head id written to {OUT / 'head_id.txt'}")

    PATHS = [
        ("jina_x_markdown", "https://r.jina.ai/https://x.com/elonmusk",
         dict(JINA_COMMON, **{"X-Return-Format": "markdown"})),
        ("jina_x_html", "https://r.jina.ai/https://x.com/elonmusk",
         dict(JINA_COMMON, **{"X-Return-Format": "html",
                              "X-Wait-For-Selector": "article"})),
        ("jina_x_text_format", "https://r.jina.ai/https://x.com/elonmusk",
         dict(JINA_COMMON, **{"X-Return-Format": "text"})),
        ("jina_x_with_replies_markdown",
         "https://r.jina.ai/https://x.com/elonmusk/with_replies",
         dict(JINA_COMMON, **{"X-Return-Format": "markdown"})),
        ("jina_twitter_markdown", "https://r.jina.ai/https://twitter.com/elonmusk",
         dict(JINA_COMMON, **{"X-Return-Format": "markdown"})),
        ("jina_twitter_html", "https://r.jina.ai/https://twitter.com/elonmusk",
         dict(JINA_COMMON, **{"X-Return-Format": "html",
                              "X-Wait-For-Selector": "article"})),
        ("jina_mobile_twitter_markdown",
         "https://r.jina.ai/https://mobile.twitter.com/elonmusk",
         dict(JINA_COMMON, **{"X-Return-Format": "markdown"})),
        ("jina_twitter_with_replies_markdown",
         "https://r.jina.ai/https://twitter.com/elonmusk/with_replies",
         dict(JINA_COMMON, **{"X-Return-Format": "markdown"})),
        ("jina_twitter_media_markdown",
         "https://r.jina.ai/https://twitter.com/elonmusk/media",
         dict(JINA_COMMON, **{"X-Return-Format": "markdown"})),
        ("jina_x_reposts_markdown",
         "https://r.jina.ai/https://x.com/elonmusk/reposts",
         dict(JINA_COMMON, **{"X-Return-Format": "markdown"})),
        ("jina_x_articles_markdown",
         "https://r.jina.ai/https://x.com/elonmusk/articles",
         dict(JINA_COMMON, **{"X-Return-Format": "markdown"})),
        # --- the SINGLE-STATUS page: a THIRD id source (cycle 1278/1212) ---
        ("jina_x_status_probe",
         f"https://r.jina.ai/https://x.com/elonmusk/status/{head_id}",
         dict(JINA_COMMON, **{"X-Return-Format": "markdown"})),
        ("jina_x_status_probe_html",
         f"https://r.jina.ai/https://x.com/elonmusk/status/{head_id}",
         dict(JINA_COMMON, **{"X-Return-Format": "html"})),
        # --- syndication (1208/1209: 429 -> rate-limited, not down) ---
        ("syndication_profile",
         "https://syndication.twitter.com/srv/timeline-profile/screen-name/elonmusk",
         {}),
        ("syndication_profile_2",
         "https://syndication.twitter.com/srv/timeline-profile/screen-name/elonmusk",
         {}),
    ]

    report = []
    for name, url, headers in PATHS:
        status, text = http_get(url, headers=headers)
        raw = OUT / f"{name}.raw"
        raw.write_text(text, encoding="utf-8")
        ids, bare, authors = collect_ids(text)
        # BASELINE = HEAD (cycle 1278 rule): the inherited worktree-only ids
        # MUST appear as candidates so they get re-adjudicated.
        new = sorted(ids - head_ids, key=lambda i: snowflake_ts(i))
        new_bare = sorted(bare - head_ids - ids,
                          key=lambda i: snowflake_ts(i) if i.isdigit() else 0)
        rec = {
            "name": name, "url": url, "status": status,
            "bytes": len(text.encode("utf-8", errors="replace")),
            "n_ids": len(ids), "n_bare": len(bare),
            "n_new_linked": len(new), "n_new_bare": len(new_bare),
            "new_linked": new, "new_bare": new_bare,
            "authors": {k: sorted(v) for k, v in authors.items() if k in new},
        }
        report.append(rec)
        print(f"\n=== {name} :: HTTP {status} :: {rec['bytes']} bytes")
        print(f"    ids={len(ids)} bare19={len(bare)} "
              f"new_linked={len(new)} new_bare={len(new_bare)}")
        if status != 200:
            print(f"    UNAVAILABLE (recorded as unavailable, NOT as agreement): "
                  f"{text[:160]!r}")
        if new:
            print(f"    NEW linked: {new}")
            for i in new:
                tsd = snowflake_ts(i)
                tag = "INHERITED" if i in work_ids else "BRAND-NEW"
                print(f"       {i} -> {tsd.isoformat()} "
                      f"{'AFTER-HEAD' if tsd > head_ts else 'BEFORE-HEAD'} "
                      f"{tag} authors={authors.get(i)}")

    (OUT / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "head_id.txt").write_text(head_id, encoding="utf-8")
    (OUT / "worktree_only.json").write_text(
        json.dumps(worktree_only, indent=2), encoding="utf-8")

    union = set()
    for r in report:
        if r["status"] == 200:
            union |= set(r["new_linked"])
    print(f"\n=== UNION of new linked ids across all 200 paths: {len(union)}")
    for i in sorted(union, key=lambda x: snowflake_ts(x)):
        tag = "INHERITED" if i in work_ids else "BRAND-NEW"
        print(f"    {i} -> {snowflake_ts(i).isoformat()} {tag}")
    n200 = sum(1 for r in report if r["status"] == 200)
    print(f"\n=== paths answering 200: {n200}/{len(report)}")
    for r in report:
        if r["status"] != 200:
            print(f"    UNAVAILABLE: {r['name']} -> HTTP {r['status']}")
    print(f"\n=== HEAD (derived) = {head_id} @ {head_ts.isoformat()}")
    print(f"=== inherited-but-uncommitted = {worktree_only}")


if __name__ == "__main__":
    main()
