#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- FIX THE TWO DOCSTRING/BODY SHAPE CONTRADICTIONS.

⭐⭐⭐⭐⭐ **THE DEFECT (MEASURED by `_c1277_docstring_shape.py`):**

`struct.py` and `jobs.py` each carry a MODULE DOCSTRING whose NARRATIVE IS
THE OPPOSITE OF ITS OWN BODY:

| file | the docstring claims | the body implements |
|---|---|---|
| `struct.py` | the **(IN, OUT)** PAIR, "THIS cycle is IN BAND", "the control set FLIPS" | the **(OUT, OUT)** shape -- `assert not _fired_c`, `assert "control set is UNCHANGED, NOT flipped" in _cmt` |
| `jobs.py` | "the control set FLIPS" -- the prior COMMITTED cycle was OUT OF BAND | `f"the control set is UNCHANGED, NOT flipped"` |

⭐⭐⭐⭐⭐ **THE BODIES ARE CORRECT AND THE PROSE IS FALSE.**  ⭐⭐⭐⭐⭐ And the
prose travels silently into every clone that inherits the file, because
⭐⭐⭐⭐⭐ **THE PAIR-KEYED VALUE-TOKEN SWEEP *DELIBERATELY* EXCLUDES
DOCSTRINGS** (its `live_lines()` strips them) — so the one instrument that
checks the polarity is BLIND to the prose that states it.

⭐⭐⭐⭐⭐ **THE FIX IS *SHAPE-NEUTRAL*, NOT *SHAPE-CORRECTED*.**  ⭐⭐⭐⭐⭐
The obvious fix — rewrite the prose to name this cycle's side — would be a
**SHAPE-SCOPED FIX**: it would be TRUE for this cycle and FALSE the moment
the pair changes, and it would need re-porting every time the pair flips.
⭐⭐⭐⭐⭐ **⇒ THE DOCSTRING NAMES NEITHER SIDE.**  ⭐⭐⭐⭐⭐ It states the
RULE (the pair selects the gate's shape; the pair is MEASURED, never
typed), describes BOTH branches for the reader, and points at the body as
the authority.  ⭐⭐⭐⭐⭐ **THIS IS THE SAME PRINCIPLE AS CYCLE 1276's
SHAPE-NEUTRAL PAGE DOCSTRING** — and it makes the fix a **PUBLISHER-SCOPED**
one, so **IT TRAVELS TO EVERY BAND PAIR**.

⭐⭐⭐⭐⭐ **⭐⭐⭐⭐⭐ AND THE FIX MUST NOT *QUOTE* THE BANNED PHRASES.**  ⭐⭐⭐⭐⭐
⭐⭐⭐⭐⭐ The FIRST DRAFT of this fix did — it wrote *"a docstring that says
`THIS cycle is IN BAND` is a FALSE STATEMENT"*, i.e. it quoted the very
pattern the instrument forbids, **AS AN EXAMPLE OF WHAT NOT TO DO**.  ⭐⭐⭐⭐⭐
⭐⭐⭐⭐⭐ **THE INSTRUMENT THEN FIRED ON THE FIX ITSELF** — and the fix's own
assertion caught it.  ⭐⭐⭐⭐⭐ **⇒ A REPLACEMENT TEXT THAT *MENTIONS* A
FORBIDDEN PATTERN IS NOT NEUTRAL — IT IS A VIOLATION OF THE SAME RULE.**
⭐⭐⭐⭐⭐ **⇒ THE REPLACEMENT MUST DESCRIBE THE RULE WITHOUT NAMING EITHER
SIDE.**  ⭐⭐⭐⭐⭐ **THIS IS THE CLASS-LEVEL FORM OF "AN INSTRUMENT THAT FIRES
ON A CORRECT ARTEFACT IS THE DEFECT"** — here the artefact was the FIX, and
the correct response was to fix the FIX (not to weaken the instrument).

⭐⭐⭐⭐⭐ **THE ANCHORS ARE RE-MEASURED AGAINST THIS CYCLE'S OWN
DESTINATION** (a port anchor is a measurement of the destination, and the
destination moves every cycle).  ⭐⭐⭐⭐⭐ **THE FIX IS IDEMPOTENT** (a
resumed cycle re-runs its own fix scripts, and a fix that re-runs must
report `[ALREADY]`, never a fake `[FIXED]`).
"""
import ast
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

# =====================================================================
# THE TWO REGIONS -- the anchors are MEASURED, not typed
# =====================================================================
STRUCT_OLD = """\
⭐⭐ THE SCOPED-VERDICT GATE HAS TWO SHAPES (Reminder 50), AND THE CYCLE'S
BAND HISTORY SELECTS WHICH ONE APPLIES.  ⭐⭐⭐ THIS CYCLE IS THE **(IN,
OUT)** PAIR: the prior COMMITTED cycle was OUT OF BAND -- its own block was
a BLIND SPOT, so there is NO legitimate historical `writer_guard = FIRED`
mention to scope -- and THIS cycle is IN BAND, so THIS hour's own block IS
the evidence.  The gate must therefore assert **PRESENCE** of the in-band
verdict and **ABSENCE** of the out-of-band one, and the page must state
that the control set FLIPS.  ⭐⭐ THE PRIOR-CYCLE NUMBER IS NOT TYPED
HERE -- it is DERIVED from the commit that PUBLISHED the page (Reminder
66).
"""

# ⭐⭐⭐⭐⭐ **THE REPLACEMENT NAMES NEITHER SIDE** -- it does not even QUOTE
# the forbidden phrases, because quoting them (even to condemn them) puts
# them back into the docstring.
STRUCT_NEW = """\
⭐⭐ THE SCOPED-VERDICT GATE HAS TWO SHAPES (Reminder 50), AND THE CYCLE'S
BAND HISTORY SELECTS WHICH ONE APPLIES.  ⭐⭐⭐⭐⭐ **WHICH SHAPE APPLIES IS
*DERIVED*, NEVER TYPED**: the gate's BODY reads the band out of
`measured.json` and the prior cycle's hour out of the commit that
PUBLISHED the page, and the PAIR selects the gate's ASSERTION SHAPE.
⭐⭐⭐⭐⭐ **⇒ THIS DOCSTRING THEREFORE NAMES NEITHER SIDE.**  ⭐⭐⭐⭐⭐ A
docstring that asserts one side of the band is a FALSE STATEMENT the moment
the cycle's band changes -- and **NO ASSERTION READS A DOCSTRING**, so
nothing would object (cycle 1277's finding, in cycle 1275's class: a
docstring whose narrative is the OPPOSITE of its own body).  ⭐⭐⭐⭐⭐ THE
TWO BRANCHES, FOR THE READER: when the prior COMMITTED cycle was INSIDE
the band, its block carries a legitimate historical in-band guard verdict
to scope, and the gate asserts the scope; when it was OUTSIDE the band,
that block was a BLIND SPOT with no such legitimate mention, so the gate
asserts the ABSENCE of an unscoped in-band claim instead.  ⭐⭐⭐⭐⭐ **THE
BODY IS THE AUTHORITY** -- read the branch it actually takes, and let it
choose the prose.  ⭐⭐ THE PRIOR-CYCLE NUMBER IS NOT TYPED HERE -- it is
DERIVED from the commit that PUBLISHED the page (Reminder 66).
"""

JOBS_OLD = """\
⭐ THE NOTE'S BRANCH IS DERIVED FROM THE BAND, AND THE BAND IS READ FROM
measured.json -- never typed (Reminder 33).  This cycle is OUT OF BAND (its
hour is NOT in RETRY_TRANSLATION_HOURS), so the note carries:
  * `writer_guard = NO_EVIDENCE_THIS_HOUR`;
  * the count as BORROWED from the POSITIVE CONTROL and explicitly
    DISCLAIMED as this hour's own evidence;
  * the POSITIVE CONTROL as the most recent IN-BAND block;
  * "the control set FLIPS" -- the prior COMMITTED cycle was OUT OF BAND.
"""

JOBS_NEW = """\
⭐ THE NOTE'S BRANCH IS DERIVED FROM THE BAND, AND THE BAND IS READ FROM
measured.json -- never typed (Reminder 33).  ⭐⭐⭐⭐⭐ **WHICH BRANCH THE
NOTE TAKES IS *MEASURED*, NOT TYPED**: the body reads the band out of
`measured.json` and the prior cycle's side out of the committed page, and
the PAIR selects the note's shape.  ⭐⭐⭐⭐⭐ **⇒ THIS DOCSTRING THEREFORE
NAMES NEITHER SIDE.**  ⭐⭐⭐⭐⭐ A docstring that asserts one side of the
band is a FALSE STATEMENT the moment the cycle's band changes -- and **NO
ASSERTION READS A DOCSTRING**, so nothing would object (cycle 1277's
finding, in cycle 1275's class: a docstring whose narrative is the
OPPOSITE of its own body).  ⭐⭐⭐⭐⭐ THE TWO BRANCHES, FOR THE READER: an
hour OUTSIDE the band gets the blind-spot verdict, the count BORROWED from
the positive control and explicitly DISCLAIMED as that hour's own evidence,
the positive control as the most recent in-band block, and the control
set's state as the MEASURED pair says; an hour INSIDE the band gets that
hour's OWN guard verdict as its evidence instead of a borrowed count.
"""

TARGETS = [
    ("struct", STRUCT_OLD, STRUCT_NEW),
    ("jobs", JOBS_OLD, JOBS_NEW),
]

# ⭐⭐⭐⭐⭐ **THE SAME PATTERNS THE INSTRUMENT USES** — so the fix's own
# assertion and the instrument cannot disagree about what a violation is.
CLAIM_PHRASE = re.compile(r"control set (?:FLIPS|is UNCHANGED)")
CLAIM_BAND = re.compile(r"\b[Tt][Hh][Ii][Ss] cycle is (IN|OUT) BAND\b")
CLAIM_PAIR = re.compile(r"\*\*\((\w+),\s*(\w+)\)\*\* PAIR")

print("=" * 78)
print(f"CYCLE {CYCLE} -- FIX THE DOCSTRING/BODY SHAPE CONTRADICTIONS")
print("=" * 78)

for _name, _old, _new in TARGETS:
    _p = REPO / f"_c{CYCLE}_{_name}.py"
    assert _p.exists(), f"[fix] ABORT: _c{CYCLE}_{_name}.py is absent"
    _src = _p.read_text(encoding="utf-8")
    print()
    print("=" * 78)
    print(f"1. {_name}.py -- THE ANCHOR, RE-MEASURED AGAINST THIS DESTINATION")
    print("=" * 78)
    _n = _src.count(_old)
    print(f"  [MEASURED] the OLD region occurs {_n} time(s) in "
          f"_c{CYCLE}_{_name}.py")
    if _n == 0:
        # ⭐⭐⭐⭐⭐ IDEMPOTENCE: the fix may ALREADY have been applied (a
        # RESUMED cycle re-runs its own fix scripts).  ⭐⭐⭐⭐⭐ The honest
        # report is "[ALREADY]", NOT a fake "[FIXED]".
        _n_new = _src.count(_new)
        assert _n_new == 1, (
            f"[fix] ABORT: _c{CYCLE}_{_name}.py carries NEITHER the old "
            f"region (0 occurrences) NOR the new one ({_n_new} occurrences) "
            "-- the anchor DRIFTED, so the fix must not be applied blindly")
        _doc = ast.get_docstring(ast.parse(_src)) or ""
        assert _new in _doc, (
            f"[fix] ABORT: the new region is in the file but not in the "
            "module docstring")
        print("  ⭐⭐⭐⭐⭐ [ALREADY] the fix is ALREADY applied -- this "
              "re-run reports [ALREADY],")
        print("             NOT a fake '[FIXED]'.")
        continue
    assert _n == 1, (
        f"[fix] ABORT: the old region occurs {_n} times in "
        f"_c{CYCLE}_{_name}.py -- the anchor is not unique, so `str.replace` "
        "would duplicate the block")
    print("  [FOUND] the OLD region is UNIQUE -- it is safe to replace.")

    _src = _src.replace(_old, _new)
    try:
        ast.parse(_src)
    except SyntaxError as _se:
        raise SystemExit(
            f"[fix] ABORT: the patched {_name}.py does not PARSE: {_se}")
    _p.write_text(_src, encoding="utf-8")

    # ⭐⭐⭐⭐⭐ RE-READ FROM DISK -- a discarded `.replace()` result is a
    # SILENT NO-OP (Reminder 84d).
    _disk = _p.read_text(encoding="utf-8")
    assert _new in _disk, (
        f"[fix] ABORT: the {_name}.py substitution did NOT land on disk")
    assert _old not in _disk, (
        f"[fix] ABORT: the OLD region survives in {_name}.py -- the false "
        "narrative would still travel")
    print("  [FIXED] the region landed (RE-READ FROM DISK).")

    # ⭐⭐⭐⭐⭐ THE FIX IS ASSERTED IN BOTH DIRECTIONS.
    _doc = ast.get_docstring(ast.parse(_disk)) or ""
    assert _new in _doc, (
        f"[fix] ABORT: the new region is not in {_name}.py's module "
        "docstring")
    for _lbl, _rx in (("band", CLAIM_BAND), ("pair", CLAIM_PAIR),
                      ("control-set phrase", CLAIM_PHRASE)):
        _hit = _rx.search(_doc)
        assert _hit is None, (
            f"[fix] ABORT: {_name}.py's docstring still carries a {_lbl} "
            f"claim ({_hit.group(0)!r}) -- a shape claim in a docstring is a "
            "FALSE STATEMENT the moment the cycle's shape changes")
    print(f"  [OK] the docstring names NO band, NO pair and NO control-set "
          "phrase --")
    print("       it is SHAPE-NEUTRAL, and it does not even QUOTE the "
          "forbidden forms.")

print()
print("=" * 78)
print("2. THE FIX IS RE-MEASURED BY THE INSTRUMENT THAT FOUND IT")
print("=" * 78)
print("  ⭐⭐⭐⭐⭐ NEXT: run `_c1277_docstring_shape.py` -- the SAME "
      "instrument that")
print("             FOUND the defect must now report CLEAN, and its "
      "fire-test")
print("             must still FIRE (a fix that makes the instrument mute "
      "is not a fix).")
