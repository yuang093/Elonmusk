#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- adjudicate EVERY candidate id by clock AND author.

RULES CARRIED FORWARD:
  * cycle 1278: validate an id by an INDEPENDENT CLOCK (the snowflake decode
    must agree with the post's OWN created_at) -- never by shape alone.
  * cycle 1249: an id must pass the clock check AND the author check -- two
    independent filters; passing one is not passing the other.
  * cycle 1251: a clock check that ALWAYS returns None is not a clock check.
    api.fxtwitter.com returns Twitter's OWN date format:
        'Fri Oct 23 14:08:42 +0000 2026'
    Parse that format FIRST and ASSERT the clock verdict is not None.
  * cycle 1249: adjudicate EVERY candidate id, not just the linked ones.
  * cycle 1251: a verdict computed from an EMPTY set is not a verdict.
  * cycle 1249: the corpus head is DERIVED, never hardcoded.
  * cycle 1251: MEASURE THE DELTA AGAINST HEAD.  A record that exists only in
    the worktree was WRITTEN BUT NEVER COMMITTED -- it is a LIABILITY, not an
    asset.  It must be re-adjudicated here as a candidate; it is publishable
    if it passes clock AND author AND is not in HEAD.
  * cycle 1249: a candidate set is NOT INHERITABLE -- re-derived every cycle.

TWO-STAGE ONLY: fetch to disk, then parse from disk.  Never curl | interpreter.
"""
import datetime as dt
import json
import pathlib
import re
import subprocess
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
OUT = pathlib.Path("/tmp/c1313/adjudicate")
OUT.mkdir(parents=True, exist_ok=True)
PATHS = pathlib.Path("/tmp/c1313/paths")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
SNOWFLAKE_EPOCH_MS = 1288834974657

KNOWN_ID_WITNESS = "2112942522486202504"

TW_DATE_FORMATS = [
    "%a %b %d %H:%M:%S %z %Y",     # Twitter's OWN format (what fxtwitter returns)
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "%Y-%m-%dT%H:%M:%SZ",
]


def snowflake_ts(tid):
    ms = (int(tid) >> 22) + SNOWFLAKE_EPOCH_MS
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc)


def http_get(url, headers=None, timeout=45):
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


def parse_created_at(s):
    if not s:
        return None
    s = str(s)
    for f in TW_DATE_FORMATS:
        try:
            return dt.datetime.strptime(s, f)
        except ValueError:
            continue
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def clock_check(tid, created_at):
    """The snowflake decode MUST agree with the post's own created_at."""
    ct = parse_created_at(created_at)
    if ct is None:
        return "UNPARSEABLE"
    if ct.tzinfo is None:
        ct = ct.replace(tzinfo=dt.timezone.utc)
    delta = abs((ct - snowflake_ts(tid)).total_seconds())
    return delta < 120


def probe(c):
    s, body = http_get(f"https://api.fxtwitter.com/i/status/{c}")
    return c, s, body


def main():
    head_raw = subprocess.run(["git", "show", "HEAD:tweets.json"], cwd=REPO,
                              capture_output=True, text=True).stdout
    head = json.loads(head_raw)
    head_ids = {t["id"] for t in head}
    work = json.loads((REPO / "tweets.json").read_text(encoding="utf-8"))
    work_ids = {t["id"] for t in work}
    head_id = max(head_ids, key=lambda i: snowflake_ts(i))
    head_ts = snowflake_ts(head_id)
    print(f"HEAD CORPUS {len(head)} records, DERIVED head {head_id} @ "
          f"{head_ts.isoformat()}")
    print(f"WORKTREE {len(work)} records, inherited-only "
          f"{sorted(work_ids - head_ids)}\n")

    report = json.loads((PATHS / "report.json").read_text(encoding="utf-8"))
    linked = {}
    bare = {}
    answered = []
    unavailable = []
    for r in report:
        if r["status"] != 200:
            unavailable.append((r["name"], r["status"]))
            continue
        answered.append(r["name"])
        for i in r["new_linked"]:
            linked.setdefault(i, []).append(r["name"])
        for i in r["new_bare"]:
            bare.setdefault(i, []).append(r["name"])

    # also the payload enumeration (authoritative): entry_id AND rest_id
    pv = json.loads(pathlib.Path("/tmp/c1313/payload/verdicts.json")
                    .read_text(encoding="utf-8"))
    for e in pv["real_ids"]:
        if e not in head_ids:
            linked.setdefault(e, []).append("payload_entry_id")
    for r in pv["rest_ids"]:
        if r not in head_ids:
            linked.setdefault(r, []).append("payload_rest_id")

    # cycle 1278's rule: an inherited worktree-only record must be
    # RE-ADJUDICATED, not assumed published.  Any such record that this
    # cycle's read paths did NOT surface is added EXPLICITLY as a candidate,
    # labelled by its provenance -- so the page can say honestly which
    # records this cycle's own paths produced and which it inherited.
    for w in sorted(work_ids - head_ids):
        linked.setdefault(w, []).append("worktree_only_inherited")
    print(f"  worktree-only inherited ids added as explicit candidates: "
          f"{sorted(work_ids - head_ids)}")
    print(f"  (those this cycle's own paths ALSO surfaced: "
          f"{sorted(set(pv['real_ids']) & (work_ids - head_ids))})")

    cands = sorted(set(linked) | set(bare), key=lambda i: snowflake_ts(i))
    print(f"paths that ANSWERED (200): {len(answered)} -> {answered}")
    print(f"paths UNAVAILABLE: {unavailable}  (recorded as unavailable, "
          f"NEVER as agreement)")
    print(f"candidate ids: linked={len(linked)} bare_only={len(bare)} "
          f"union={len(cands)}")
    print(f"  (the known-id witness {KNOWN_ID_WITNESS} is NOT a candidate; "
          f"it is checked separately)\n")

    assert len(cands) >= 1, (
        "no candidates -- a verdict on an empty set is not a verdict")

    rows = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for c, s, body in ex.map(probe, cands):
            v = {"id": c, "http": s, "linked_in": linked.get(c, []),
                 "bare_in": bare.get(c, []),
                 "snowflake_ts": snowflake_ts(c).isoformat()}
            if s == 200:
                try:
                    j = json.loads(body)
                except Exception:
                    j = {}
                t = j.get("tweet") or j
                v["author"] = (t.get("author") or {}).get("screen_name")
                v["created_at"] = t.get("created_at")
                v["text"] = (t.get("text") or "")[:220]
                v["in_reply_to"] = t.get("in_reply_to_screen_name")
                v["quoted_id"] = t.get("quoted_status_id_str")
                v["clock_ok"] = clock_check(c, v.get("created_at"))
                v["clock_parsed"] = str(parse_created_at(v.get("created_at")))
                v["author_ok"] = (v.get("author") or "").lower() == "elonmusk"
                v["newer_than_head"] = snowflake_ts(c) > head_ts
                v["in_head"] = c in head_ids
                v["inherited"] = c in work_ids and c not in head_ids
                if v["author_ok"] and v["newer_than_head"] and v["clock_ok"] is True:
                    v["verdict"] = "REAL NEW POST"
                elif not v["author_ok"]:
                    v["verdict"] = "QUOTE-TARGET/REPLY/OTHER-AUTHOR"
                else:
                    v["verdict"] = "ALREADY-IN-CORPUS-OR-OLDER"
            else:
                v["verdict"] = "NOT-A-POST (404/err)"
                v["head"] = body[:90]
            rows.append(v)

    for r in rows:
        print(f"  {r['id']}  http={r['http']}  sf={r['snowflake_ts']}  "
              f"author={r.get('author','-')}  clock_ok={r.get('clock_ok','-')}  "
              f"=> {r['verdict']}")

    ok200 = [r for r in rows if r["http"] == 200]
    assert ok200, ("no candidate resolved 200 -- the clock check would fire on "
                   "an empty set")
    n_none = sum(1 for r in ok200 if r["clock_ok"] is None
                 or r["clock_ok"] == "UNPARSEABLE")
    print(f"\n  candidates resolving 200: {len(ok200)}; "
          f"clock verdict UNPARSEABLE/None: {n_none}")
    assert n_none == 0, (
        "the clock check returned UNPARSEABLE for every row -- it is not a "
        "clock check; parse the format the API actually returns")
    n_true = sum(1 for r in ok200 if r["clock_ok"] is True)
    print(f"  clock check VERIFIED on {n_true}/{len(ok200)} rows (not a "
          f"vacuous pass)")

    print("\n" + "=" * 78)
    print("KNOWN-ID WITNESS -- still absent from the renders? (and that is EXPECTED)")
    print("=" * 78)
    w = KNOWN_ID_WITNESS
    s, body = http_get(f"https://api.fxtwitter.com/i/status/{w}")
    print(f"  fxtwitter {w}: HTTP {s}")
    if s == 200:
        j = json.loads(body)
        t = j.get("tweet") or j
        print(f"    author={((t.get('author') or {}).get('screen_name'))!r} "
              f"created_at={t.get('created_at')!r}")
    present = []
    for p in sorted(PATHS.glob("*.raw")):
        txt = p.read_text(encoding="utf-8", errors="replace")
        if w in txt:
            present.append(p.name)
    pv_txt = pathlib.Path("/tmp/c1313/payload/html_a.raw").read_text(
        encoding="utf-8", errors="replace")
    if w in pv_txt:
        present.append("payload/html_a.raw")
    print(f"  present in renders: {present if present else 'NONE'}")
    print("  => the render is [PIN] + [the 4 newest]; the witness falls in the "
          "UNSHOWN MIDDLE, so its absence is EXPECTED (cycle 1278's correction)")

    real_new = [r for r in rows if r["verdict"] == "REAL NEW POST"]
    inherited = [r for r in real_new if r.get("inherited")]
    brand = [r for r in real_new if not r.get("inherited")]
    print(f"\n=== REAL NEW POSTS: {len(real_new)}  "
          f"(INHERITED/uncommitted={len(inherited)}, BRAND-NEW={len(brand)})")
    for r in real_new:
        tag = "INHERITED" if r.get("inherited") else "BRAND-NEW"
        print(f"    {r['id']} @ {r.get('created_at')} author={r.get('author')} "
              f"[{tag}]")
    n404 = sum(1 for r in rows if r["http"] != 200)
    n200 = len(ok200)
    n_auth_fail = sum(1 for r in ok200 if not r.get("author_ok"))
    n_transport = sum(1 for r in rows if r["http"] == 0)
    print(f"=== candidate table: {len(rows)} total, {n404} HTTP 404, "
          f"{n200} resolve 200, {n_transport} transport errors; "
          f"{n_auth_fail} of the 200s fail the AUTHOR check")

    (OUT / "verdicts.json").write_text(json.dumps({
        "head_id": head_id, "head_ts": head_ts.isoformat(),
        "answered_paths": answered, "unavailable_paths": unavailable,
        "rows": rows, "real_new": [r["id"] for r in real_new],
        "inherited": [r["id"] for r in inherited],
        "brand_new": [r["id"] for r in brand],
        "witness": {"id": w, "http": s, "present_in": present},
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n=== adjudication written -> {OUT / 'verdicts.json'}")


if __name__ == "__main__":
    main()
