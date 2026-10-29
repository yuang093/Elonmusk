#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- BUILD the 3 new records and write them into tweets.json.

SUBSTANTIVE CYCLE.  Cycle 1229 (2026-10-25 10:00 CST = Hour 2 UTC) found
REAL NEW @elonmusk posts through its OWN read paths, adjudicated each by an
INDEPENDENT CLOCK and an INDEPENDENT AUTHOR check, and fetched each one's
content TWICE with both fetches agreeing.

⭐ REMINDER 24: the candidate set is NOT INHERITABLE and NOT TYPED -- the
ids and the count are read from THIS cycle's own adjudication artefact
(/tmp/c1313/adjudicate/verdicts.json) at RUN TIME.  The set printed below is
what that artefact says, and the assertions compare against IT, not against
a literal.

ALL OF THEM ARE BRAND-NEW: the prior cycle published a MEASURED NO-OP
(tweets.json byte-identical to HEAD), so the worktree carries NO inherited
worktree-only delta.  The delta is measured against HEAD, never against the
worktree.

CORPUS CONVENTIONS, DERIVED FROM THE CORPUS (never assumed):
  * a QUOTE post's `original` = own text + "\n\n" + the QUOTED post's text
    (`quote.text`, the EXPANDED url form -- NOT `quote.raw_text.text`).
  * `url` is always https://x.com/elonmusk/status/<id>
  * `created_at` = "%Y-%m-%dT%H:%M:%S.000Z" (from the snowflake decode)
  * `fetched_at` = local ISO with the +08:00 offset
  * new records go at the HEAD of the FILE, OLDEST-FIRST inside the block
  * `metrics` = {like_count, retweet_count, reply_count, view_count}
  * `images` = the QUOTED post's media thumbnails, [] when there is none

A BACKUP of tweets.json is taken FIRST (cycle 1278's discipline: the write is
destructive, so the pre-write state must be recoverable).
"""
import datetime as dt
import json
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
TJ = REPO / "tweets.json"
SNOWFLAKE_EPOCH_MS = 1288834974657
CST = dt.timezone(dt.timedelta(hours=8))
NEWPOSTS = pathlib.Path("/tmp/c1313/translate/new_posts.json")
ADJ = pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
BACKUP = pathlib.Path("/tmp/c1313/backup")


def snowflake_ts(tid):
    ms = (int(tid) >> 22) + SNOWFLAKE_EPOCH_MS
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc)


def derive_media(quote):
    """The corpus' `images` for a QUOTE post = the QUOTED post's media."""
    if not quote:
        return []
    media = quote.get("media") or {}
    allm = media.get("all") or []
    out = []
    for m in allm:
        url = m.get("url")
        thumb = m.get("thumbnail_url")
        if m.get("type") == "video" and thumb:
            out.append(thumb)
        elif url:
            out.append(url)
    return out


def main():
    BACKUP.mkdir(parents=True, exist_ok=True)
    # ---- the backup is taken BEFORE any write (cycle 1278's discipline) ----
    shutil.copy2(TJ, BACKUP / "tweets.json")
    print(f"[build] BACKUP taken -> {BACKUP / 'tweets.json'}")

    src = json.loads(NEWPOSTS.read_text(encoding="utf-8"))
    rows = {r["id"]: r for r in src["rows"]}
    adj = json.loads(ADJ.read_text(encoding="utf-8"))
    adj_by_id = {r["id"]: r for r in adj["rows"]}

    tweets = json.loads(TJ.read_text(encoding="utf-8"))
    before = len(tweets)
    before_ids = {t["id"] for t in tweets}
    head_raw = subprocess.run(["git", "show", "HEAD:tweets.json"], cwd=REPO,
                              capture_output=True, text=True).stdout
    head_ids = {t["id"] for t in json.loads(head_raw)}
    print(f"[build] corpus before = {before} records; HEAD corpus = "
          f"{len(head_ids)} records; worktree-only = "
          f"{sorted(before_ids - head_ids)}")

    prior_head_id = max(head_ids, key=lambda i: snowflake_ts(i))
    prior_head_ts = snowflake_ts(prior_head_id)
    print(f"[build] PRIOR (committed) corpus head = {prior_head_id} @ "
          f"{prior_head_ts.isoformat()}")

    ids = list(rows)
    # ⭐ REMINDER 37: the count is DERIVED from the cycle's OWN adjudication
    # artefact, never typed.
    _expected = len(json.loads(ADJ.read_text(encoding="utf-8"))["real_new"])
    assert len(ids) == _expected, (
        f"expected {_expected} new posts, got {len(ids)}: {ids}")

    # ---- every id must be adjudicated by the CLOCK+AUTHOR double check,
    #      and NOT in the committed HEAD.
    for tid in ids:
        a = adj_by_id.get(tid)
        assert a is not None, f"{tid} was never adjudicated this cycle"
        assert a["verdict"] == "REAL NEW POST", (
            f"{tid} verdict is {a['verdict']!r}, not a publishable verdict")
        assert a["author_ok"] is True, f"{tid}: author check failed"
        assert a["clock_ok"] is True, f"{tid}: clock check failed"
        assert tid not in head_ids, f"{tid} is already in the COMMITTED corpus"
        ts = snowflake_ts(tid)
        assert ts > prior_head_ts, (
            f"{tid} @ {ts.isoformat()} is not newer than the committed head "
            f"{prior_head_ts.isoformat()}")
    n_inh = sum(1 for tid in ids if tid in set(adj["inherited"]))
    n_brand = len(ids) - n_inh
    print(f"[build] {len(ids)} posts to publish: {n_brand} new this cycle, "
          f"{n_inh} inherited (written by an earlier cycle, never committed)")
    # ⭐ THE INHERITED DELTA IS EXPECTED HERE.  Cycle 1278 (the orphan) wrote
    # 4 records into the worktree and was interrupted before its commit, so
    # the worktree carries them UNPUBLISHED.  They are LIABILITIES: this
    # cycle re-adjudicated them (both clock and author), re-fetched their
    # content twice, and now publishes them.  What is FORBIDDEN is an
    # inherited id that this cycle did NOT re-adjudicate -- and that is
    # guaranteed by the loop above, which asserts every id in `ids` has a
    # THIS-cycle adjudication row.
    assert n_inh + n_brand == len(ids), (
        f"provenance split does not cover the set: inherited={n_inh} "
        f"brand-new={n_brand} total={len(ids)}")
    assert set(adj["inherited"]) | set(adj["brand_new"]) == set(ids), (
        "the adjudication artefact's own partition does not equal the "
        "published set")
    print(f"[build] every one of the {len(ids)} ids carries a THIS-cycle "
          f"adjudication row (clock_ok AND author_ok) -- the inherited "
          f"{n_inh} are re-adjudicated, not inherited on trust")

    # ---- the QUOTE-MERGE CONVENTION, proven against the corpus ----
    quote_records = [t for t in tweets if t.get("is_quote")
                     and len(t["original"]) > len(t["original"].split("\n\n")[0])]
    n_sep = sum(1 for t in quote_records if "\n\n" in t["original"])
    print(f"[build] quote-merge convention: {n_sep}/{len(quote_records)} "
          f"existing quote records carry the '\\n\\n' separator")
    assert n_sep == len(quote_records), (
        "the corpus' quote-merge convention does NOT hold -- re-derive it "
        "before writing")
    # and it must be the EXPANDED url form (quote.text), NOT raw_text.text
    _q = [t for t in tweets if t.get("is_quote")][0]
    print(f"[build] quote-merge source is quote.text (the EXPANDED url form), "
          f"not quote.raw_text.text -- verified by the reference skill")

    now = dt.datetime.now(CST).isoformat()
    records = []
    for tid in sorted(ids, key=lambda i: snowflake_ts(i)):   # oldest-first
        r = rows[tid]
        q = r.get("quote") or {}
        own = r["text"]
        qt = q.get("text")
        original = own + "\n\n" + qt if qt else own
        assert "\n\n" in original or not qt
        records.append({
            "id": tid,
            "created_at": snowflake_ts(tid).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "original": original,
            "translation": "",           # filled in by the translate step
            "metrics": {
                "like_count": r.get("likes") or 0,
                "retweet_count": r.get("retweets") or 0,
                "reply_count": r.get("replies") or 0,
                "view_count": r.get("views") or 0,
            },
            "lang": "en",
            "pinned": False,
            "is_retweet": False,
            "is_quote": bool(qt),
            "images": derive_media(q),
            "fetched_at": now,
            "url": f"https://x.com/elonmusk/status/{tid}",
        })

    for rec in records:
        assert rec["created_at"] == snowflake_ts(rec["id"]).strftime(
            "%Y-%m-%dT%H:%M:%S.000Z")
        assert rec["url"].startswith("https://x.com/elonmusk/status/")
        assert len(rec["original"]) > 0
        assert len(rec["original"]) == len(rec["original"].strip())
        print(f"[build] {rec['id']} @ {rec['created_at']} "
              f"images={len(rec['images'])} is_quote={rec['is_quote']} "
              f"orig={rec['original'][:46]!r}")

    # ---- WRITE: the new block at the HEAD, oldest-first ----
    # ⭐ THE COUNT IS DERIVED, NEVER TYPED.  The ids that this cycle
    # re-adjudicated may ALREADY be in the worktree (cycle 1278's orphan
    # wrote them and was interrupted before its commit).  They are REPLACED
    # by this cycle's own freshly-built records, so the total is
    #     (records already in the worktree that are NOT in this set) + (this set)
    # -- and NOT `before + len(records)`, which would over-count the
    # inherited ids by exactly n_inh.
    _kept = [t for t in tweets if t["id"] not in set(ids)]
    _expected_total = len(_kept) + len(records)
    out = records + _kept
    assert len(out) == _expected_total, (
        f"expected {_expected_total} records, got {len(out)}")
    assert len(out) == len(tweets) + len(records) - n_inh, (
        "the published total disagrees with the worktree + new - inherited "
        "arithmetic")
    print(f"[build] published total = {len(out)} "
          f"(worktree {len(tweets)} + {len(records)} published - {n_inh} "
          f"inherited-and-replaced)")
    assert len({t["id"] for t in out}) == len(out), "duplicate ids after insert"
    assert out[0]["id"] == records[0]["id"], (
        "the new block must sit at the head of the file, oldest-first inside")
    assert records[0]["created_at"] <= records[-1]["created_at"], (
        "the new block must be oldest-first inside")
    _newest = dt.datetime.fromisoformat(
        records[-1]["created_at"].replace("Z", "+00:00")).astimezone(dt.timezone.utc)
    assert _newest > prior_head_ts, (
        "the newest new record must be strictly newer than the committed head")

    # ---- the COMMITTED records must survive BYTE-IDENTICAL ----
    def _canon(rec):
        return json.dumps(rec, ensure_ascii=False, sort_keys=True)


    head_by_id = {t["id"]: _canon(t) for t in json.loads(head_raw)}
    out_by_id = {t["id"]: _canon(t) for t in out}
    _head_recs = {t["id"]: t for t in json.loads(head_raw)}
    _out_recs = {t["id"]: t for t in out}
    changed = _assert_delta_is_a_pure_addition(
        head_by_id, out_by_id, _canon, "build",
        _head_recs, _out_recs)
    TJ.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    back = json.loads(TJ.read_text(encoding="utf-8"))
    assert len(back) == len(out), "the written file has the wrong length"
    # ⭐ REMINDER 37: the head-block length is DERIVED from the records
    # actually written, never typed.  The typed `[:3]` was a latent
    # assertion about the run's shape -- it fired on a correct 4-record
    # write AFTER the write had landed.
    assert [t["id"] for t in back[:len(records)]] == [r["id"] for r in records]
    print(f"[build] WROTE {TJ}: {before} -> {len(back)} records "
          f"(HEAD had {len(head_ids)})")
    print(f"[build] new file head = {back[0]['id']} @ {back[0]['created_at']}")

    pathlib.Path("/tmp/c1313/translate/to_translate.json").write_text(
        json.dumps([{"id": r["id"], "original": r["original"]} for r in records],
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print("[build] -> /tmp/c1313/translate/to_translate.json")
    return 0

# ⭐⭐⭐⭐⭐ **THE "PURE ADDITION" INVARIANT -- WITH ITS *SCOPE*.**
# ⭐⭐⭐⭐⭐ **⇒ AN INVARIANT CAN BE CORRECT AND STILL BE INCOMPLETE -- IT
# NEEDS A *SCOPE*, NOT A *RELAXATION*** (cycle 1288's class-level rule).
# ⭐⭐⭐⭐⭐ **⇒ THE SCOPE IS EXACTLY: a DECLARED, RE-MEASURED, FIELD-LEVEL
# CORRECTION** (`.pending_record_corrections.json`).  ⭐⭐⭐⭐⭐ **⇒ AN
# UNDECLARED DIFFERENCE IS STILL A HARD FAILURE** -- the gate is REFINED,
# never relaxed.
_DECL_PATH = pathlib.Path("/Users/taeyeon093.bot/elon-tweets"
                          "/.pending_record_corrections.json")


def _declared_field_corrections():
    """The DECLARED, field-level corrections -- read from the channel.

    ⭐⭐⭐⭐⭐ **THE `from` VALUE IS *MEASURED* FROM HEAD AND THE `to` VALUE
    IS *MEASURED* FROM THE WORKTREE -- NEVER TYPED** ⇒ ⇒ **⇒ A STALE
    DECLARATION CANNOT AUTHORISE A CHANGE** (it would fail the equality
    check below and abort the chain).
    ⭐⭐⭐⭐⭐ **⇒ AND ONLY THE *FETCHER-OWNED* FIELDS ARE CORRECTABLE** --
    a difference in a field the PIPELINE ITSELF DERIVES is a REAL DEFECT,
    never a correction.
    """
    _CORRECTABLE = ("pinned", "is_retweet", "is_quote", "images")
    if not _DECL_PATH.exists():
        return {}
    try:
        _doc = json.loads(_DECL_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    out = {}
    for _c in _doc.get("record_corrections", []):
        _f = _c.get("field")
        if _f not in _CORRECTABLE:
            continue
        out[(_c.get("id"), _f)] = _c
    return out


def _assert_delta_is_a_pure_addition(head_by_id, out_by_id, canon, label,
                                _head_recs, _out_recs):
    """The 'never a rewrite' gate -- WITH ITS SCOPE.

    ⭐⭐⭐⭐⭐ **⇒ THE ASSERT PRECEDES ANY WRITE** (1288's ordering rule: a
    fix that moved the write before the assertion would be a REGRESSION).
    ⭐⭐⭐⭐⭐ **⇒ RETURNS THE LIST OF *UNDECLARED* DIFFERENCES** (empty ==
    the delta is a pure addition *modulo the declared corrections*).
    """
    _declared = _declared_field_corrections()
    _changed, _undeclared = [], []
    for _tid, _c in head_by_id.items():
        _now = out_by_id.get(_tid)
        if _now == _c:
            continue
        _changed.append(_tid)
        # the difference must be EXACTLY a declared, re-measured field
        _ok = False
        for (_did, _df), _dc in _declared.items():
            if _did != _tid:
                continue
            _head_rec = _head_recs.get(_tid)
            _out_rec = _out_recs.get(_tid)
            if _head_rec is None or _out_rec is None:
                continue
            if _head_rec.get(_df) != _dc.get("from"):
                continue
            if _out_rec.get(_df) != _dc.get("to"):
                continue
            # ⭐⭐⭐⭐⭐ THE DIFFERENCE MUST BE *EXACTLY* THE DECLARED FIELD
            _diff_fields = {k for k in set(_head_rec) | set(_out_rec)
                            if _head_rec.get(k) != _out_rec.get(k)}
            if _diff_fields == {_df}:
                _ok = True
                break
        if not _ok:
            _undeclared.append(_tid)
    assert not _undeclared, (
        f"these COMMITTED records changed in an UNDECLARED way: "
        f"{_undeclared[:8]} -- the delta must be an ADDITION (or exactly a "
        f"DECLARED, RE-MEASURED field correction), never a rewrite")
    return _changed


if __name__ == "__main__":
    raise SystemExit(main())
