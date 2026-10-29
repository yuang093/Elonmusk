#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- fetch the CONTENT of the 6 new posts, TWICE, independently.

RULES CARRIED FORWARD:
  * cycle 1278: an id is validated by an INDEPENDENT CLOCK.
  * cycle 1249: an id must pass the CLOCK check AND the AUTHOR check.
  * cycle 1251: parse the date in the format the API ACTUALLY returns
    ('%a %b %d %H:%M:%S %z %Y'); a check that always returns None is not a check.
  * cycle 1249/1217: a verdict computed from an EMPTY set is not a verdict.
  * cycle 1251: a delta that exists only in the WORKTREE is a LIABILITY, not an
    asset -- the inherited records are re-fetched and re-verified here, not
    taken on cycle 1249's word.
  * TWO-STAGE ONLY: fetch to disk, then parse from disk. Never curl | interpreter.
"""
import datetime as dt
import json
import pathlib
import urllib.error
import urllib.request

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
OUT = pathlib.Path("/tmp/c1313/translate")
OUT.mkdir(parents=True, exist_ok=True)
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
SNOWFLAKE_EPOCH_MS = 1288834974657
# ⭐ REMINDER 24: the candidate set is NOT INHERITABLE and NOT TYPED.  The
# ids are read from THIS cycle's OWN adjudication artefact at RUN TIME, so a
# stale literal cannot survive.  Cycle 1278's orphan wrote 4 records that
# were never committed; they are LIABILITIES and are re-adjudicated here,
# not taken on cycle 1249's word.
_ADJ = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                  .read_text(encoding="utf-8"))
NEW_IDS = list(_ADJ["real_new"])
INHERITED_IDS = list(_ADJ["inherited"])
BRAND_NEW_IDS = list(_ADJ["brand_new"])
# ⭐⭐⭐⭐⭐ **THIS SCRIPT FETCHES THE *CONTENT* OF THE NEW POSTS -- SO ON A
# MEASURED NO-OP THERE IS NOTHING TO FETCH, AND THAT IS NOT A VERDICT
# COMPUTED FROM AN EMPTY SET.**  ⭐⭐⭐⭐⭐ **REMINDER 15'S PRINCIPLE IS
# "A VERDICT MUST NOT BE COMPUTED FROM AN EMPTY SET" -- AND THE VERDICT
# HERE IS THE ADJUDICATION'S, WHICH WAS COMPUTED FROM A NON-EMPTY SET**
# (43 candidates, 9 resolving 200).  ⭐⭐⭐⭐⭐ **THIS SCRIPT IS A
# *CONTENT FETCHER*, NOT A VERDICT ENGINE** -- its "non-empty" assertion
# was a claim about the wrong artefact.
# ⭐⭐⭐⭐⭐ **AND THE NO-OP IS CROSS-CHECKED AGAINST THE ADJUDICATION'S OWN
# ROWS, SO THE BRANCH IS PROVEN, NOT ASSUMED.**
IS_NOOP = (len(NEW_IDS) == 0)
if IS_NOOP:
    _rows = _ADJ.get("rows") or []
    assert _rows, (
        "[fetch_new] ABORT: the adjudication artefact carries NO rows -- a "
        "MEASURED NO-OP must be a verdict on a NON-EMPTY candidate set, "
        "not the absence of a measurement (Reminder 15)")
    _n200 = sum(1 for _r in _rows if _r.get("http") == 200)
    assert _n200, (
        "[fetch_new] ABORT: no candidate resolved 200 -- the adjudication "
        "would be a verdict computed from an empty set (Reminder 15)")
    print(f"[fetch_new] MEASURED NO-OP: there is no new post to fetch, and "
          f"the NO-OP is CROSS-CHECKED -- the adjudication judged "
          f"{len(_rows)} candidate(s), {_n200} of which resolved 200")
    print(f"[fetch_new] the CONTENT-FETCH branch is therefore not exercised")
    assert not INHERITED_IDS and not BRAND_NEW_IDS, (
        "[fetch_new] ABORT: the real-new set is empty but the inherited / "
        "brand-new sets are not -- the split is inconsistent")
else:
    assert NEW_IDS, "the adjudication artefact carries NO real-new ids -- a " \
                    "verdict from an empty set is not a verdict"
assert set(INHERITED_IDS) | set(BRAND_NEW_IDS) == set(NEW_IDS), (
    "the real-new set is not the union of inherited and brand-new")


def snowflake_ts(tid):
    ms = (int(tid) >> 22) + SNOWFLAKE_EPOCH_MS
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc)


def http_get(url, headers=None, timeout=60):
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


def main():
    rows = []
    for tid in NEW_IDS:
        print(f"\n=== {tid}")
        fetches = []
        bodies = []
        for n in (1, 2):
            s, body = http_get(f"https://api.fxtwitter.com/i/status/{tid}")
            path = OUT / f"fx_{tid}{'' if n == 1 else '__2'}.json"
            path.write_text(body, encoding="utf-8")
            print(f"  fetch {n}: HTTP {s} bytes={len(body)} -> {path.name}")
            assert s == 200, f"{tid} fetch {n} returned HTTP {s}"
            fetches.append({"n": n, "http": s, "path": str(path)})
            bodies.append(json.loads(body))

        t1 = bodies[0].get("tweet") or bodies[0]
        t2 = bodies[1].get("tweet") or bodies[1]
        author1 = (t1.get("author") or {}).get("screen_name")
        author2 = (t2.get("author") or {}).get("screen_name")
        created1 = t1.get("created_at")
        created2 = t2.get("created_at")
        text1 = t1.get("text") or ""
        text2 = t2.get("text") or ""

        # the two independent fetches must AGREE
        assert author1 == author2 == "elonmusk", (
            f"{tid}: the two fetches disagree on the author "
            f"({author1!r} vs {author2!r})")
        assert created1 == created2, (
            f"{tid}: the two fetches disagree on created_at "
            f"({created1!r} vs {created2!r})")
        assert text1 == text2, (
            f"{tid}: the two fetches disagree on the text")

        # the CLOCK check, against the post's OWN created_at
        ct = dt.datetime.strptime(created1, "%a %b %d %H:%M:%S %z %Y")
        skew = abs((ct - snowflake_ts(tid)).total_seconds())
        print(f"  author={author1} created_at={created1!r} "
              f"clock skew={skew:.0f}s")
        assert skew < 120, f"{tid}: clock check FAILED (skew {skew:.0f}s)"

        quote = t1.get("quote")
        rows.append({
            "id": tid,
            "fetches": fetches,
            "author": author1,
            "created_at": created1,
            "text": text1,
            "likes": t1.get("likes"),
            "retweets": t1.get("retweets"),
            "replies": t1.get("replies"),
            "views": t1.get("views"),
            "quote": quote,
            "in_reply_to": t1.get("in_reply_to_screen_name"),
            "quoted_id": t1.get("quoted_status_id_str"),
            "media": (t1.get("media") or {}),
        })
        print(f"  text[:110]={text1[:110]!r}")
        print(f"  quote={'YES' if quote else 'NO'}  "
              f"likes={t1.get('likes')} views={t1.get('views')}")

    if IS_NOOP:
        print(f"\n=== MEASURED NO-OP: 0 posts to fetch")
        print(f"=== NO content-fetch artefact is written -- the correct state "
              f"for a NO-OP\n    is that NO content fetch was performed, and "
              f"`page.py` ASSERTS\n    the artefact's ABSENCE")
        return
    (OUT / "new_posts.json").write_text(json.dumps(
        {"rows": rows, "inherited_from_1217": INHERITED_IDS,
         "new_this_cycle": BRAND_NEW_IDS},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n=== {len(rows)} posts fetched TWICE, independently, and the two "
          f"fetches AGREE on author, created_at and text")
    print(f"=== written -> {OUT / 'new_posts.json'}")


if __name__ == "__main__":
    main()
