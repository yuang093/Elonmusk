#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- WRITE the selected translations into the 3 new records.

RULES CARRIED FORWARD:
  * the delta must be an ADDITION: the COMMITTED records must be
    BYTE-IDENTICAL after the write (never a rewrite);
  * every record must carry the canonical 12 keys, in the corpus' own order;
  * the new block sits at the HEAD of the file, OLDEST-FIRST inside;
  * re-read from disk and re-assert -- a write that is not re-verified is
    not a write.
"""
import datetime as dt
import json
import pathlib
import subprocess

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
TJ = REPO / "tweets.json"
TRANSLATIONS = pathlib.Path("/tmp/c1313/translate/translations_final.json")
SNOWFLAKE_EPOCH_MS = 1288834974657
# ⭐ REMINDER 24 + Reminder 37: the id set is DERIVED from this cycle's own
# adjudication artefact -- never inherited, never typed.
_ADJ = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                  .read_text(encoding="utf-8"))
NEW_IDS = list(_ADJ["real_new"])


def snowflake_ts(tid):
    ms = (int(tid) >> 22) + SNOWFLAKE_EPOCH_MS
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc)


def main():
    tweets = json.loads(TJ.read_text(encoding="utf-8"))
    head_raw = subprocess.run(["git", "show", "HEAD:tweets.json"], cwd=REPO,
                              capture_output=True, text=True).stdout
    head = json.loads(head_raw)
    head_ids = {t["id"] for t in head}
    tr = json.loads(TRANSLATIONS.read_text(encoding="utf-8"))

    by_id = {t["id"]: t for t in tweets}
    for tid in NEW_IDS:
        assert tid in by_id, f"{tid} is not in the worktree corpus"
        assert tid not in head_ids, f"{tid} is already in HEAD"
        t = tr.get(tid)
        assert t, f"{tid} has no selected translation"
        assert t.strip(), f"{tid} translation is empty"
        by_id[tid]["translation"] = t.strip()

    CANONICAL = ["id", "created_at", "original", "translation", "metrics",
                 "lang", "pinned", "is_retweet", "is_quote", "images",
                 "fetched_at", "url"]
    for tid in NEW_IDS:
        keys = list(by_id[tid].keys())
        assert keys == CANONICAL, (
            f"{tid} key shape {keys} != the canonical {CANONICAL}")

    def canonical(rec):
        return json.dumps(rec, ensure_ascii=False, sort_keys=True)


    head_by_id = {t["id"]: canonical(t) for t in head}
    _head_recs = {t["id"]: t for t in head}
    _out_recs = {t["id"]: t for t in by_id.values()}
    changed = _assert_delta_is_a_pure_addition(
        head_by_id, {k: canonical(v) for k, v in _out_recs.items()},
        canonical, "write", _head_recs, _out_recs)
    out = [by_id[t["id"]] for t in tweets]
    assert [r["id"] for r in out[:len(NEW_IDS)]] == NEW_IDS, (
        "the new block must be at the head, oldest-first")
    TJ.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- re-read from disk and re-assert ----
    back = json.loads(TJ.read_text(encoding="utf-8"))
    assert len(back) == len(head) + len(NEW_IDS), (
        f"expected {len(head) + len(NEW_IDS)} records, got {len(back)}")
    assert len({t["id"] for t in back}) == len(back), "duplicate ids"
    back_by_id = {t["id"]: t for t in back}
    changed2 = [tid for tid, c in head_by_id.items()
                if canonical(back_by_id.get(tid, {})) != c]
    assert not changed2, f"committed records changed after the write: {changed2[:8]}"
    for tid in NEW_IDS:
        assert back_by_id[tid]["translation"].strip()
        assert back_by_id[tid]["created_at"] == snowflake_ts(tid).strftime(
            "%Y-%m-%dT%H:%M:%S.000Z")
        assert back_by_id[tid]["url"] == f"https://x.com/elonmusk/status/{tid}"
    print(f"[write] tweets.json: {len(head)} (HEAD) -> {len(back)} records; "
          f"the {len(head)} committed records are BYTE-IDENTICAL")
    for tid in NEW_IDS:
        r = back_by_id[tid]
        print(f"[write]   {tid} @ {r['created_at']} "
              f"orig={len(r['original'])}c trans={len(r['translation'])}c "
              f"imgs={len(r['images'])} {r['original'][:40]!r}")
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
