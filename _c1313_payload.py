#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- AUTHORITATIVE timeline enumeration + freshness.

The jina html render embeds X's raw GraphQL payload, which carries
    "entry_id":"tweet-<REAL ID>", "rest_id":"<REAL ID>", "sort_index":"<COUNTER>"
The entry_id / rest_id are the REAL post ids.  The sort_index is the payload's
ORDERING COUNTER -- cycle 1278's trap: it decodes to a plausible instant and
looks like a post.  Cycle 1249 showed the counters can decode to "NOW".

RULES CARRIED FORWARD:
  * cycle 1278: enumerate the field whose NAME says "id"; but a payload may
    carry ids under MORE THAN ONE id-bearing key.  Enumerate BOTH and assert
    entry_id subset-of rest_id.
  * cycle 1249: the head id / head ts are DERIVED FROM THE CORPUS.
  * cycle 1251: fetch the render WITH x-no-cache: true (cycle-1204 fix).
  * cycle 1249: MEASURE THE DELTA AGAINST HEAD.  ⭐⭐⭐ **THE DELTA IS
    MEASURED AT RUN TIME, NEVER TYPED** -- a copied record count is a
    LATENT ASSERTION ABOUT THIS RUN'S SHAPE (Reminder 37): this cycle's
    worktree carries a ZERO-record delta against HEAD (8,163 == 8,163),
    while the inherited prose claimed 5.  ⭐⭐ **A WORKTREE-ONLY DELTA IS
    A LIABILITY, NOT AN ASSET** -- those records are NOT published, so they
    must be re-adjudicated as candidates, not assumed published.  ⭐ The
    baseline for "is this id in the corpus?" is therefore HEAD; worktree-
    only ids are reported SEPARATELY as INHERITED.

TWO-STAGE ONLY: fetch to disk, then parse from disk.
"""
import datetime as dt
import json
import pathlib
import re
import subprocess
import time
import urllib.error
import urllib.request

OUT = pathlib.Path("/tmp/c1313/payload")
OUT.mkdir(parents=True, exist_ok=True)
REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
SNOWFLAKE_EPOCH_MS = 1288834974657
JINA = {"x-no-cache": "true", "x-cache-tolerance": "0", "X-Timeout": "45"}


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


def corpus():
    """HEAD = the committed baseline; WORKTREE = what exists on disk only."""
    head_raw = subprocess.run(["git", "show", "HEAD:tweets.json"], cwd=REPO,
                              capture_output=True, text=True).stdout
    head = json.loads(head_raw)
    work = json.loads((REPO / "tweets.json").read_text(encoding="utf-8"))
    return (head, {t["id"] for t in head},
            work, {t["id"] for t in work})


def payload_ids(text):
    """The REAL timeline ids, from entry_id / rest_id (NOT sort_index).

    The payload is embedded as ESCAPED JSON inside a script tag, so the quotes
    are backslash-escaped.
    """
    eids = re.findall(r'\\?"entry_id\\?":\\?"tweet-(\d{15,25})\\?"', text)
    if not eids:
        eids = re.findall(r'entry_id[^0-9]{0,12}tweet-(\d{15,25})', text)
    rids = re.findall(r'\\?"rest_id\\?":\\?"(\d{15,25})\\?"', text)
    if not rids:
        rids = re.findall(r'rest_id[^0-9]{0,12}(\d{15,25})', text)
    sidx = re.findall(r'\\?"sort_index\\?":\\?"(\d{15,25})\\?"', text)
    if not sidx:
        sidx = re.findall(r'sort_index[^0-9]{0,12}(\d{15,25})', text)
    return eids, rids, sidx


def main():
    head, head_ids, work, work_ids = corpus()
    head_id = max(head_ids, key=lambda i: snowflake_ts(i))
    head_ts = snowflake_ts(head_id)
    print(f"HEAD CORPUS {len(head)} records, DERIVED head {head_id} @ "
          f"{head_ts.isoformat()}")
    print(f"WORKTREE {len(work)} records, {len(work_ids - head_ids)} "
          f"written-but-never-committed (INHERITED): "
          f"{sorted(work_ids - head_ids)}\n")

    print("=" * 78)
    print("A. FRESH FETCH (no-cache) + AUTHORITATIVE payload enumeration")
    print("=" * 78)
    st, text = http_get("https://r.jina.ai/https://x.com/elonmusk",
                        headers=dict(JINA, **{"X-Return-Format": "html"}))
    (OUT / "html_a.raw").write_text(text, encoding="utf-8")
    print(f"  HTTP {st} bytes={len(text)}")
    eids, rids, sidx = payload_ids(text)
    print(f"  entry_id tweet-ids : {len(eids)} occurrences, {len(set(eids))} distinct")
    print(f"  rest_id values     : {len(rids)} occurrences, {len(set(rids))} distinct")
    print(f"  sort_index counters: {len(sidx)} occurrences, {len(set(sidx))} distinct")

    real = []
    for e in eids:
        if e not in real:
            real.append(e)
    rset = set(rids)
    print(f"\n  TIMELINE (entry_id order, as the payload orders it):")
    for e in real:
        t = snowflake_ts(e)
        if e in head_ids:
            mark = "IN-HEAD"
        elif e in work_ids:
            mark = "*** INHERITED (worktree only, never committed) ***"
        else:
            mark = "*** NOT IN CORPUS ***"
        where = "NEWER-THAN-HEAD" if t > head_ts else ""
        ctx = re.search(r'.{0,400}tweet-' + re.escape(e) + r'.{0,400}',
                        text, re.S)
        pinned = "PINNED" if (ctx and "pinned" in ctx.group(0).lower()) else ""
        print(f"    {e}  {t.isoformat()}  {mark} {where} {pinned}")

    assert len(real) >= 3, (
        f"only {len(real)} real ids enumerated -- the payload parse found "
        "nothing; a verdict on an empty set is not a verdict")
    assert len(rset) > len(set(real)), (
        "rest_id must be a LARGER population than entry_id; if not, the "
        "enumeration rule itself is broken")
    missing = [e for e in real if e not in rset]
    assert not missing, f"entry_id values not under rest_id: {missing}"
    print(f"  ASSERT OK: entry_id ({len(set(real))}) is a SUBSET of rest_id "
          f"({len(rset)}); the rest_id-only population = {len(rset - set(real))}")

    sset = sorted(set(sidx))
    proven = 0
    for s in sset:
        if re.search(re.escape("sort_index") + r'[^0-9]{0,12}' + re.escape(s), text):
            proven += 1
    print(f"  sort_index counters proven under their own key: {proven}/{len(sset)}")
    assert proven == len(sset), (
        "not every sort_index counter was found under its own key -- the "
        "attribution is not proven, do not conclude")
    for key in ("entry_id", "rest_id", "id_str"):
        bad = [s for s in sset if re.search(
            re.escape(key) + r'[^0-9]{0,12}' + re.escape(s), text)]
        print(f"    counters appearing under '{key}': {len(bad)}")
    for s in sset:
        print(f"    counter {s} -> decodes to {snowflake_ts(s).isoformat()}")

    print("\n" + "=" * 78)
    print("B. THE rest_id POPULATION -- ids that live ONLY under rest_id")
    print("=" * 78)
    extra = sorted(rset - set(real), key=lambda i: snowflake_ts(i))
    notin = [r for r in extra if r not in head_ids]
    print(f"  rest_id-only population: {len(extra)}; not in HEAD: {len(notin)}")
    for r in notin:
        t = snowflake_ts(r)
        newer = "NEWER-THAN-HEAD" if t > head_ts else ""
        tag = "INHERITED" if r in work_ids else "BRAND-NEW"
        print(f"    {r}  {t.isoformat()}  {tag} {newer}")

    print("\n" + "=" * 78)
    print("C. FRESHNESS -- second fetch of the SAME url, compared")
    print("=" * 78)
    time.sleep(40)
    st2, text2 = http_get("https://r.jina.ai/https://x.com/elonmusk",
                           headers=dict(JINA, **{"X-Return-Format": "html"}))
    (OUT / "html_b.raw").write_text(text2, encoding="utf-8")
    e2, r2, s2i = payload_ids(text2)
    real2 = []
    for e in e2:
        if e not in real2:
            real2.append(e)
    print(f"  pass B HTTP {st2} bytes={len(text2)}")
    print(f"  identical timeline (entry_id order): {real == real2}")
    print(f"  payload bytes identical: {text == text2}")
    if text != text2:
        print("  => the payload CHANGED between the two fetches -- the fetch is "
              "LIVE, not cached (view counters move)")
    else:
        print("  => the payload is byte-identical between the two fetches")

    (OUT / "verdicts.json").write_text(
        json.dumps({"real_ids": real, "rest_ids": sorted(rset),
                    "rest_only": extra, "sort_index": sset,
                    "head_id": head_id, "head_ts": head_ts.isoformat(),
                    "head_ids": sorted(head_ids),
                    "inherited": sorted(work_ids - head_ids),
                    "fresh_identical": real == real2},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n=== payload enumeration written -> " + str(OUT / "verdicts.json"))


if __name__ == "__main__":
    main()
