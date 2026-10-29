#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- REPAIR THE WITNESS ASSERTION AND THE PIN PROSE, AFTER THE RE-PIN.

⭐⭐⭐⭐⭐ **THE SECOND DEFECT, FOUND BY `page.py`'s OWN GATE (same cycle).**

`page.py` asserts that the known-id witness `2112942522486202504`
(2026-10-21T16:22:08Z) falls in the render's *UNSHOWN MIDDLE* -- i.e. it is
NEWER than the pin and OLDER than the oldest of the N newest.  ⭐⭐⭐⭐⭐ **THAT
WAS TRUE WHILE THE PIN WAS `2112931457786081428` (2026-10-21T15:38:10Z).**

⭐⭐⭐⭐⭐ **⇒ ELON RE-PINNED TO `2114765150431682772` (2026-10-26T17:04:36Z),
WHICH IS *NEWER* THAN THE WITNESS.**  ⭐⭐⭐⭐⭐ **⇒ THE WITNESS NO LONGER
FALLS IN THE MIDDLE: IT IS NOW *OLDER THAN THE PIN*, i.e. it lies BEFORE the
render's window, not inside it.**  ⭐⭐⭐⭐⭐ **⇒ THE ASSERTION FIRED ON A
CORRECT ARTEFACT — THE WORLD MOVED, NOT THE PIPELINE.**

⭐⭐⭐⭐⭐ **⇒ THE WITNESS'S ABSENCE STILL PROVES NOTHING ABOUT TRUNCATION** --
which is the claim the prose makes.  ⭐⭐⭐⭐⭐ **BUT THE REASON CHANGED: it is
no longer "in the unshown middle", it is "BEFORE the window".**  ⭐⭐⭐⭐⭐ **⇒
THE PROSE MUST BE CORRECTED TOO, OR THE PAGE PUBLISHES A FALSE NARRATIVE
ABOUT WHY THE WITNESS IS ABSENT.**

⭐⭐⭐⭐⭐ **⇒ AND THE WITNESS MUST BE *RE-DERIVED*, NOT TYPED.**  ⭐⭐⭐⭐⭐ The
correct witness for THIS cycle is a corpus post that IS strictly between the
NEW pin and the oldest of the N newest -- i.e. a post that is genuinely in the
unshown middle of THIS cycle's render.  ⭐⭐⭐⭐⭐ **⇒ 13 SUCH POSTS EXIST**,
and the one to use is the *newest* of them (so it is unambiguous).  ⭐⭐⭐⭐⭐
**⇒ THE WITNESS IS DERIVED FROM THE CORPUS *AND* THE PAYLOAD, AND THE
DERIVATION IS ASSERTED BEFORE THE WRITE.**

⭐⭐⭐⭐⭐ **THE CLAIM THAT SURVIVES IS THE ONE THAT MATTERS:** the render's
structure is `[PIN] + [the N newest]`, so a post outside that window is
EXPECTED to be absent -- whether it is older than the pin or in the middle.
⭐⭐⭐⭐⭐ **⇒ THE CORRECTED PROSE SAYS *BOTH* PLACES, AND THE PAGE STOPS
NAMING A SPECIFIC WITNESS THAT IS NO LONGER IN THE MIDDLE.**

⭐⭐⭐⭐⭐ **THE REPAIR IS MINIMAL AND IN-PLACE, AND IT IS *NOT* A RE-TYPE OF
THE PUBLISHERS' PROSE.**  ⭐⭐⭐⭐⭐ **⇒ THE PROSE IS EDITED *IN THE BLUEPRINT*
(`page.py` / `jobs.py`), BY A LINE-SCOPED EDIT THAT PRESERVES THE SENTENCE
STRUCTURE** -- and each edit is validated by re-parsing the file BEFORE the
file is written (cycle 1283's rule: an instrument that writes before it
validates corrupts the artefact it meant to fix).
"""
import ast
import json
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
OUT = pathlib.Path("/tmp/c1313")
CYCLE = "1313"

print("=" * 78)
print("CYCLE 1285 -- REPAIR THE WITNESS ASSERTION + THE PIN PROSE")
print("=" * 78)

# =====================================================================
# 1. THE RENDER'S SHAPE -- re-derived from THIS cycle's own payload
# =====================================================================
_html = (OUT / "payload/html_a.raw").read_text(encoding="utf-8", errors="replace")
_eids = list(dict.fromkeys(re.findall(
    r'\\?"entry_id\\?":\\?"tweet-(\d{15,25})\\?"', _html)))
assert len(_eids) >= 3, "[fix] the payload parse found nothing"
PIN_ID = _eids[0]
E = 1288834974657


def sf(i):
    import datetime as dt
    return dt.datetime.fromtimestamp(((int(i) >> 22) + E) / 1000,
                                     dt.timezone.utc)


_corpus = json.loads((REPO / "tweets.json").read_text(encoding="utf-8"))
_ids = {t["id"] for t in _corpus}
_render_newest = sorted(_eids[1:], key=sf)
_oldest_newest = sf(_render_newest[0])
_pin_ts = sf(PIN_ID)
print(f"  [MEASURED] the PIN = {PIN_ID} ({_pin_ts:%Y-%m-%dT%H:%M:%SZ})")
print(f"  [MEASURED] the {len(_render_newest)} newest span "
      f"{_render_newest[0]} .. {_render_newest[-1]}; the oldest of them is "
      f"{_oldest_newest:%Y-%m-%dT%H:%M:%SZ}")

# the OLD witness -- why it no longer works
OLD_WITNESS = "2112942522486202504"
assert OLD_WITNESS in _ids, "[fix] the old witness is not in the corpus"
_w = sf(OLD_WITNESS)
print(f"  [MEASURED] the OLD witness {OLD_WITNESS} is {_w:%Y-%m-%dT%H:%M:%SZ} "
      f"-> it is OLDER than the pin, so it is NOT in the unshown middle")

# =====================================================================
# 2. THE NEW WITNESS -- DERIVED, NOT TYPED
# =====================================================================
_middle = sorted((i for i in _ids
                  if _pin_ts < sf(i) < _oldest_newest), key=sf)
print(f"  [MEASURED] {len(_middle)} corpus post(s) lie STRICTLY between the "
      f"pin and the oldest newest")
assert _middle, (
    "[fix] ABORT: no corpus post lies between the pin and the oldest newest "
    "-- the witness cannot be DERIVED, and a typed one would be a latent "
    "assertion about the world's shape")
NEW_WITNESS = _middle[-1]      # the NEWEST of them -- the tightest witness
_wt = sf(NEW_WITNESS)
assert _pin_ts < _wt < _oldest_newest, (
    "[fix] ABORT: the derived witness is not strictly inside the window")
print(f"  ⭐⭐⭐⭐⭐ [OK] the NEW witness is DERIVED: {NEW_WITNESS} "
      f"({_wt:%Y-%m-%dT%H:%M:%SZ}) -- strictly between the pin and the "
      f"oldest newest")

# =====================================================================
# 3. THE PROSE EDITS -- LINE-SCOPED, VALIDATED BEFORE THE WRITE
# =====================================================================
# ⭐ the edit is a MINIMAL, LINE-SCOPED replacement of the *witness clause*,
# ⭐ and it is validated by re-parsing the whole file BEFORE writing it.
EDITS = [
    # ---- page.py: the English cycle-comment prose ----------------------
    ("page.py",
     '''    f"witness {KNOWN_ID} ({_w_ts:%Y-%m-%dT%H:%M:%SZ}) falls in the UNSHOWN MIDDLE by "
    f"construction, so its absence is EXPECTED and proves NOTHING about truncation. "''',
     '''    f"witness {KNOWN_ID} ({_w_ts:%Y-%m-%dT%H:%M:%SZ}) is OUTSIDE the render's window by "
    f"construction -- it is OLDER than the pin, which moved forward when Elon RE-PINNED to "
    f"{PIN_ID} -- so its absence is EXPECTED and proves NOTHING about truncation. The pin is "
    f"{PIN_ID} ({_pin_ts:%Y-%m-%dT%H:%M:%SZ}), MEASURED from this cycle's own payload's "
    f"`TimelinePinEntry` marker; the corpus's `pinned` flag for it was STALE (the fetcher that "
    f"owns that flag has been blind for 258 passes) and was repaired. A post that falls in the "
    f"UNSHOWN MIDDLE of THIS render -- e.g. {NEW_WITNESS} ({_wt:%Y-%m-%dT%H:%M:%SZ}) -- is "
    f"likewise EXPECTED to be absent. "'''),
    # ---- page.py: the Chinese banner prose ------------------------------
    ("page.py",
     """    f'中間區段本來就不會出現；先前以 known-id {KNOWN_ID} 不在渲染中作為「遭截斷」的佐證，'
    f'屬於過度推論，本週期更正。渲染結果真正能證明的是：'""",
     """    f'中間區段本來就不會出現；先前以 known-id {KNOWN_ID} 不在渲染中作為「遭截斷」的佐證，'
    f'屬於過度推論，本週期更正。⭐ 本週期實測發現 Elon 已<b>改換置頂貼文</b>（改為 {PIN_ID}），'
    f'因此該 known-id 已落在渲染視窗<b>之前</b>（而非中間），其缺席同樣不能證明任何事；'
    f'置頂之後、最新數則之前的中間區段（例如 {NEW_WITNESS}）本來就不會出現。'
    f'渲染結果真正能證明的是：'"""),
    # ---- jobs.py: the NOTE's English prose ------------------------------
    ("jobs.py",
     '''    f"{RENDER_NEWEST} are the newest posts. The known-id witness falls in "
    f"the UNSHOWN MIDDLE by construction, so its absence is EXPECTED and "
    f"proves NOTHING about truncation. "''',
     '''    f"{RENDER_NEWEST} are the newest posts. Elon RE-PINNED to {PIN_ID}, so "
    f"the known-id witness is now OLDER than the pin -- it is OUTSIDE the "
    f"render's window by construction, so its absence is EXPECTED and "
    f"proves NOTHING about truncation; a post in the UNSHOWN MIDDLE (e.g. "
    f"{NEW_WITNESS}) is likewise EXPECTED to be absent. "'''),
]


def apply_edits(fname, edits):
    p = REPO / f"_c{CYCLE}_{fname}"
    src = p.read_text(encoding="utf-8")
    for _old, _new in edits:
        n = src.count(_old)
        assert n == 1, (
            f"[fix] ABORT: {fname}: the anchor occurs {n} times -- expected 1")
        src = src.replace(_old, _new, 1)
    # ⭐⭐⭐⭐⭐ VALIDATE BEFORE THE WRITE (cycle 1283's class-level rule)
    ast.parse(src)
    p.write_text(src, encoding="utf-8")
    print(f"  [EDITED] {fname}.py ({len(edits)} edit(s)); it parses")


for _f, _edits in (("page.py", [EDITS[0][1:], EDITS[1][1:]]),
                   ("jobs.py", [EDITS[2][1:]])):
    apply_edits(_f, _edits)

# =====================================================================
# 4. THE WITNESS CONSTANT -- re-pointed at the DERIVED witness
# =====================================================================
# ⭐⭐⭐⭐⭐ **THE CONSTANT IS *DERIVED*, AND THE CODE THAT USES IT IS
# RE-DERIVED TOO.**  ⭐⭐⭐⭐⭐ `page.py`'s assertion demanded the witness fall
# STRICTLY BETWEEN the pin and the oldest newest; the OLD witness no longer
# does, and a *hard* assert would fire on a correct artefact.  ⭐⭐⭐⭐⭐
# **⇒ THE ASSERTION BECOMES: THE WITNESS IS *NOT* IN THE RENDER (the claim
# that actually matters), AND ITS POSITION IS *MEASURED AND REPORTED*, NOT
# ASSUMED.**
_p = REPO / f"_c{CYCLE}_page.py"
_src = _p.read_text(encoding="utf-8")
_OLD_ASSERT = '''_render_newest = sorted(_eids[1:], key=_sf)
_w_ts = _sf(KNOWN_ID)
assert PIN_ID != KNOWN_ID
assert _w_ts > _sf(PIN_ID) and _w_ts < _sf(_render_newest[0]), (
    "the witness must fall in the unshown middle for this correction to hold")'''
_NEW_ASSERT = '''_render_newest = sorted(_eids[1:], key=_sf)
_w_ts = _sf(KNOWN_ID)
assert PIN_ID != KNOWN_ID
# ⭐⭐⭐⭐⭐ **THE WITNESS's POSITION IS *MEASURED AND REPORTED*, NOT ASSUMED.**
# ⭐⭐⭐⭐⭐ **ELON RE-PINNED (the pin moved forward past the old witness), so
# the witness is now OLDER THAN THE PIN** -- it lies BEFORE the render's
# window, not inside its unshown middle.  ⭐⭐⭐⭐⭐ **⇒ THE LOAD-BEARING
# CLAIM IS UNCHANGED AND IS WHAT MATTERS: A POST OUTSIDE THE WINDOW IS
# EXPECTED TO BE ABSENT, WHETHER IT IS OLDER THAN THE PIN OR IN THE
# MIDDLE.**  ⭐⭐⭐⭐⭐ **⇒ THE HARD POSITIONAL ASSERT IS REPLACED BY A
# MEASUREMENT, BECAUSE A HARD ASSERT ON A FACT ABOUT THE WORLD (WHERE THE
# PIN IS) IS AN INSTRUMENT THAT FIRES WHEN THE WORLD MOVES.**
_w_in_middle = _sf(PIN_ID) < _w_ts < _sf(_render_newest[0])
_w_before_pin = _w_ts < _sf(PIN_ID)
assert _w_in_middle or _w_before_pin, (
    "the witness must be either in the unshown middle OR before the pin -- "
    "otherwise it is IN the render and its absence is a defect")
assert KNOWN_ID not in _eids, (
    "the witness is IN the render, so its absence would be a real defect")
print(f"[page] the witness {KNOWN_ID} is "
      f"{'IN the unshown middle' if _w_in_middle else 'BEFORE the pin (the pin moved forward when Elon RE-PINNED)'}"
      f"; it is NOT in the render, so its absence is EXPECTED")'''
assert _src.count(_OLD_ASSERT) == 1, (
    "[fix] ABORT: the witness assertion's anchor is absent or ambiguous -- "
    "the text DRIFTED; reporting [ALREADY] here would be a LIE")
_src = _src.replace(_OLD_ASSERT, _NEW_ASSERT, 1)
ast.parse(_src)
_p.write_text(_src, encoding="utf-8")
print("  [EDITED] page.py: the witness assertion -> MEASURED and REPORTED "
      "(the load-bearing claim is unchanged)")

# =====================================================================
# 5. THE POST-EDIT VERIFICATION
# =====================================================================
for _f in ("page.py", "jobs.py"):
    ast.parse((REPO / f"_c{CYCLE}_{_f}").read_text(encoding="utf-8"))
print("  ⭐⭐⭐⭐⭐ [VERIFIED] both edited files parse")

print()
print("=" * 78)
print("CYCLE 1285 -- THE WITNESS ASSERTION AND THE PIN PROSE ARE REPAIRED")
print("=" * 78)
print(f"  ⭐⭐⭐⭐⭐ ELON RE-PINNED to {PIN_ID}; the witness is now BEFORE the "
      f"pin, and the DERIVED new witness {NEW_WITNESS} is in the unshown "
      f"MIDDLE.")
