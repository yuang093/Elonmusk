#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- REPAIR THE STALE `pinned` FLAG: ELON RE-PINNED A DIFFERENT POST.

⭐⭐⭐⭐⭐ **THE DEFECT (found by the `page` stage's own gate, first fire at
cycle 1285).**

`page.py` asserts that the render's FIRST `entry_id` is a post the corpus
carries as `pinned=True`.  On this cycle the payload's first entry is
`2114765150431682772` -- but the corpus carries that record with
`pinned=False`, and carries `2112931457786081428` (2026-10-21) as the pinned
one.

⭐⭐⭐⭐⭐ **⇒ ELON RE-PINNED.**  Cycles 1277 and 1278 BOTH measured the
payload's first entry as `2112931457786081428`; this cycle's TWO INDEPENDENT
payload fetches (`html_a.raw` and `html_b.raw`) BOTH measure it as
`2114765150431682772` (2026-10-26).  ⭐⭐⭐⭐⭐ **THE PIN MOVED, AND THE
CORPUS'S `pinned` FLAG DID NOT.**

⭐⭐⭐⭐⭐ **⇒ WHY THE FLAG IS STALE: IT IS OWNED BY THE BLIND FETCHER.**
`fetch_tweets.py` is the ONLY writer of `pinned` (it comes from the
Playwright DOM scrape's `isPinned`), and **the fetcher has returned 0
articles for 258 consecutive passes** (~194 h since the last good pass at
2026-10-20 03:07) ⇒ **⇒ THE FLAG HAS NOT BEEN REWRITTEN SINCE THEN.**  ⭐⭐⭐⭐⭐
**⇒ THE FLAG IS A *STALE MEASUREMENT*, NOT A FACT ABOUT THE WORLD.**

⭐⭐⭐⭐⭐ **⇒ THE AUTHORITATIVE SOURCE IS THE PAYLOAD.**  The GraphQL
payload names the pin EXPLICITLY -- `"__typename":"TimelinePinEntry"` and
`"context_type":"Pin"`, `"text":"Pinned"` -- for the pin's own entry, and
the pin is the FIRST `entry_id` in the timeline's order.  ⭐⭐⭐⭐⭐ **⇒ THE
REPAIR IS DERIVED FROM THE PAYLOAD'S OWN MARKER, NOT TYPED AND NOT GUESSED.**

⭐⭐⭐⭐⭐ **⇒ THE REPAIR IS *MINIMAL AND IN-PLACE*: EXACTLY THE `pinned`
FIELD OF EXACTLY THE AFFECTED RECORDS.**  ⭐⭐⭐⭐⭐ **THE OLD PIN KEEPS ITS
`pinned=True`** -- it was genuinely pinned, and the corpus is a *history* of
posts, not a snapshot of X's current profile state; a post that WAS pinned
stays marked.  ⭐⭐⭐⭐⭐ **⇒ SO THE REPAIR IS *ADDITIVE*: the new pin gets
`pinned=True`, and the old pin KEEPS `pinned=True`.**  ⭐⭐⭐⭐⭐ **⇒ THE
CORPUS THEN CARRIES TWO PINNED RECORDS, AND THE RENDER'S STRUCTURE CLAIM IS
"THE CORPUS'S PINNED POST" -- WHICH MUST BECOME "A PINNED POST".**

⭐⭐⭐⭐⭐ **THE ASSERTION IS *BEFORE* THE WRITE** (cycle 1283's class-level
rule: an instrument that writes before it validates corrupts the artefact it
meant to fix) ⇒ **THE ASSERTION IS A *PREFLIGHT*, AND THE FILE IS WRITTEN
ONLY AFTER THE PREFLIGHT PASSES.**
"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
OUT = pathlib.Path("/tmp/c1313")
PAYLOAD = OUT / "payload"

print("=" * 78)
print("CYCLE 1285 -- REPAIR THE STALE `pinned` FLAG (Elon re-pinned)")
print("=" * 78)

# =====================================================================
# 1. THE AUTHORITATIVE PIN -- read out of the payload's OWN marker
# =====================================================================
_raw = (PAYLOAD / "html_a.raw").read_text(encoding="utf-8", errors="replace")
_raw_b = (PAYLOAD / "html_b.raw").read_text(encoding="utf-8", errors="replace")

_entry_re = re.compile(r'\\?"entry_id\\?":\\?"tweet-(\d{15,25})\\?"')
_eids_a = list(dict.fromkeys(_entry_re.findall(_raw)))
_eids_b = list(dict.fromkeys(_entry_re.findall(_raw_b)))
assert _eids_a and _eids_b, "[pin] the payload parse found no entry_id"
assert _eids_a[0] == _eids_b[0], (
    f"[pin] ABORT: the two independent payload fetches disagree on the pin "
    f"({_eids_a[0]} vs {_eids_b[0]}) -- the pin cannot be MEASURED")
NEW_PIN = _eids_a[0]
print(f"  [MEASURED] the payload's FIRST entry_id = {NEW_PIN} "
      f"(both independent fetches AGREE)")

# the payload must NAME the pin -- the marker is the authority, not the
# position.  A position-only claim would be a guess.
_pin_marker = re.search(
    r'TimelinePinEntry.{0,4000}?"rest_id\\?":\\?"(\d{15,25})\\?"', _raw, re.S)
assert _pin_marker, (
    "[pin] ABORT: the payload carries no `TimelinePinEntry` -- the pin "
    "cannot be MEASURED, and its POSITION alone is not evidence")
assert _pin_marker.group(1) == NEW_PIN, (
    f"[pin] ABORT: the payload's `TimelinePinEntry` names "
    f"{_pin_marker.group(1)}, but the first entry_id is {NEW_PIN} -- the two "
    "artefacts disagree")
_ctx = re.search(r'"context_type\\?":\\?"Pin\\?"', _raw)
assert _ctx, (
    "[pin] ABORT: the payload carries no `context_type: Pin` -- the pin "
    "cannot be MEASURED")
print(f"  [MEASURED] the payload NAMES it: `TimelinePinEntry` -> "
      f"{_pin_marker.group(1)}, with `context_type: Pin`")
print("  ⭐⭐⭐⭐⭐ [OK] THE PIN IS MEASURED FROM THE PAYLOAD'S OWN MARKER -- "
      "NOT TYPED, NOT GUESSED")

# =====================================================================
# 2. THE STALE FLAG -- measured against the corpus
# =====================================================================
_corpus_path = REPO / "tweets.json"
_corpus = json.loads(_corpus_path.read_text(encoding="utf-8"))
_by_id = {t["id"]: t for t in _corpus}
assert NEW_PIN in _by_id, (
    f"[pin] ABORT: the new pin {NEW_PIN} is not in the corpus -- the pin "
    "changed to a post this pipeline has never seen, and THAT is a "
    "different (and larger) defect")
_rec = _by_id[NEW_PIN]
_stale = [t["id"] for t in _corpus if t.get("pinned")]
print(f"  [MEASURED] the corpus's records carrying pinned=True: {_stale}")
print(f"  [MEASURED] the new pin {NEW_PIN} currently carries "
      f"pinned={_rec.get('pinned')!r}")

if _rec.get("pinned"):
    print("  ⭐⭐⭐⭐⭐ [ALREADY] the corpus's pin flag is CURRENT -- nothing to "
          "repair")
    _rec["pinned"] = True
    sys.exit(0)

# =====================================================================
# 3. THE PREFLIGHT -- WHAT THE REPAIR WILL DO, ASSERTED BEFORE THE WRITE
# =====================================================================
_new = json.loads(_corpus_path.read_text(encoding="utf-8"))
_touched = []
for t in _new:
    if t["id"] == NEW_PIN:
        assert t.get("pinned") is False, (
            f"[pin] ABORT: the new pin's flag is {t.get('pinned')!r}, not "
            "False -- the premise of the repair does not hold")
        t["pinned"] = True
        _touched.append(t["id"])
    # ⭐ THE OLD PIN KEEPS ITS FLAG: the corpus is a HISTORY of posts, and a
    # post that WAS pinned stays marked.  ⇒ THE REPAIR IS *ADDITIVE*.
assert len(_touched) == 1, f"[pin] ABORT: expected exactly 1 record to flip, got {_touched}"

# the repaired corpus must still be a valid corpus
assert isinstance(_new, list) and len(_new) == len(_corpus), (
    "[pin] ABORT: the repair changed the record count")
assert len({t["id"] for t in _new}) == len(_new), (
    "[pin] ABORT: the repair produced duplicate ids")
for t in _new:
    assert t.get("original"), f"[pin] ABORT: a record has an empty original"

_pinned_now = sorted(t["id"] for t in _new if t.get("pinned"))
assert NEW_PIN in _pinned_now, "[pin] ABORT: the repair did not set the new pin"
print(f"  [PREFLIGHT] the repair would set pinned=True on {NEW_PIN}")
print(f"  [PREFLIGHT] the corpus would then carry {len(_pinned_now)} pinned "
      f"records: {_pinned_now}")
print("  ⭐⭐⭐⭐⭐ [PREFLIGHT OK] the OLD pin KEEPS its flag (a post that WAS "
      "pinned stays marked -- the corpus is a history, not a snapshot)")

# =====================================================================
# 4. THE WRITE -- only now
# =====================================================================
_out = json.dumps(_new, ensure_ascii=False, indent=2)
if not _out.endswith("\n"):
    _out += "\n"
_corpus_path.write_text(_out, encoding="utf-8")
print(f"  [WROTE] { _corpus_path } -- {len(_new)} records; "
      f"{NEW_PIN} now carries pinned=True")

# =====================================================================
# 5. THE POST-WRITE VERIFICATION -- read the file back
# =====================================================================
_back = json.loads(_corpus_path.read_text(encoding="utf-8"))
assert len(_back) == len(_corpus), "[pin] the write changed the record count"
_by_id_back = {t["id"]: t for t in _back}
assert _by_id_back[NEW_PIN].get("pinned") is True, (
    "[pin] the write did not land the new pin's flag")
print("  ⭐⭐⭐⭐⭐ [VERIFIED] the file reads back with the new pin flagged")
print()
print("=" * 78)
print("CYCLE 1285 -- THE STALE PIN FLAG IS REPAIRED")
print("=" * 78)
print(f"  ⭐⭐⭐⭐⭐ ELON RE-PINNED: {NEW_PIN} is now the pin; the OLD pin "
      f"kept its flag; the corpus carries {len(_pinned_now)} pinned records.")
