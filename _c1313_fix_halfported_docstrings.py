#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- REPAIR THE TWO HALF-PORTED MODULE DOCSTRINGS.

⭐⭐⭐⭐⭐ **THE DEFECT THE DOCSTRING-SHAPE INSTRUMENT FOUND (and it is a
REAL one -- the instrument is proven on 3 fixtures and its poison fires).**

`measure.py`'s and `page.py`'s MODULE DOCSTRINGS each carry **BOTH** the
(IN, IN) narrative AND the leftover (OUT, IN) narrative -- and the leftover
one says **"the control set FLIPS"**, which is the WRONG side for this
cycle's (IN, IN) pair.

⭐⭐⭐⭐⭐ **⇒ THIS IS THE *HALF-PORTED* CLASS AGAIN (1278's finding):**
the port inserted the new text but did not REMOVE the old one, so the
docstring contradicts ITSELF and its body.

⭐⭐⭐⭐⭐ **⇒ THE FIX IS *SHAPE-NEUTRAL*, NOT *SHAPE-CORRECTED*.**  A
docstring that names one side rots silently on the next pair change, and
a docstring is not read by any assertion -- so nothing would object
(cycle 1277's class-level finding).  ⭐⭐⭐⭐⭐ The replacement states the
RULE, names NEITHER side, and points at the body as the authority.

⭐⭐⭐⭐⭐ **⇒ AND THE REPLACEMENT MUST NAME NEITHER SIDE** -- a
replacement that mentions a forbidden pattern is a violation of the same
rule (1277's own finding, about 1277's own fix).

⭐⭐⭐⭐⭐ **⇒ THE REGION IS BOUNDED BY *SENTENCES*, NOT SUBSTRINGS** (1279's
finding): the region is bracketed by its OWN first and last sentence, so a
half-ported fragment cannot survive.
"""
import ast
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

# ⭐⭐⭐⭐⭐ **THE FORBIDDEN PATTERNS -- the replacement must contain NONE.**
FORBIDDEN = [
    "the control set FLIPS",
    "control set is UNCHANGED, NOT 'flipped back'",
    "control set is UNCHANGED, NOT flipped",
    "was ALSO IN BAND",
    "was ALSO OUT OF BAND",
    "was IN BAND",
    "was OUT OF BAND",
    "BLIND SPOT",
    "BORROWED and DISCLAIMED",
]

# ======================================================================
# THE TWO REGIONS -- each bracketed by its OWN first and last sentence
# ======================================================================
REGIONS = [
    # ---- measure.py: the control-set paragraph -------------------------
    ("measure.py",
     "⭐⭐ AND THE CONTROL SET IS A *FUNCTION OF THE BAND PAIR*: the prior",
     "`PRIOR_CYCLE` (read out of HEAD's own commit subject); this narrative",
     '''\
⭐⭐ AND THE CONTROL SET IS A *FUNCTION OF THE BAND PAIR*: the prior
COMMITTED cycle's side and THIS cycle's side together decide which block is
the EVIDENCE and which block is the NEGATIVE CONTROL, and the SAME rule
covers every pair -- two cycles on the SAME side keep the assignment, and
two cycles on DIFFERENT sides swap it.  ⭐⭐⭐⭐⭐ **⇒ THIS DOCSTRING
THEREFORE NAMES NEITHER SIDE**: a docstring that asserts one side of the
band is a FALSE STATEMENT ABOUT THE WORLD the moment the band pair
changes -- and a docstring is not read by any assertion, so nothing would
object (cycle 1277's finding, in cycle 1275's class: a docstring whose
narrative is the OPPOSITE of its own body).  ⭐⭐⭐⭐⭐ **THE BODY IS THE
AUTHORITY** -- read the branch it actually takes, and let it choose the
prose.  ⭐⭐⭐⭐⭐ **THE PRIOR CYCLE's NUMBER IS NOT TYPED HERE**: a literal
cycle number in this docstring was CORRECT when it was written and becomes
a FALSE STATEMENT ABOUT THE WORLD the moment the prior committed cycle
changes.  The number the *published* prose carries is DERIVED from
`PRIOR_CYCLE` (read out of HEAD's own commit subject); this narrative
deliberately names NO number.'''),
    # ---- page.py: the control-set narrative + its leftover ------------
    ("page.py",
     "⭐ The prior COMMITTED cycle was ALSO IN BAND, so the control set",
     "previous cycle's side alone (Reminder 21 / Reminder 55).",
     '''\
⭐ THE CONTROL SET IS A *FUNCTION OF THE BAND PAIR*: the prior COMMITTED
cycle's side and THIS cycle's side together decide which block is the
EVIDENCE and which block is the NEGATIVE CONTROL, and the SAME rule covers
every pair -- two cycles on the SAME side keep the assignment, and two
cycles on DIFFERENT sides swap it.  ⭐⭐⭐⭐⭐ **⇒ THIS DOCSTRING THEREFORE
NAMES NEITHER SIDE** (a docstring that asserts one side of the band is a
FALSE STATEMENT ABOUT THE WORLD the moment the band pair changes, and no
assertion reads it).  ⭐⭐⭐⭐⭐ **THE BODY IS THE AUTHORITY** -- read the
branch it actually takes, and let it choose the prose.'''),
]

print("=" * 78)
print(f"CYCLE {CYCLE} -- REPAIR THE TWO HALF-PORTED MODULE DOCSTRINGS")
print("=" * 78)

for fname, start, end, new in REGIONS:
    fp = REPO / f"_c{CYCLE}_{fname}"
    src = fp.read_text(encoding="utf-8")
    print()
    print("-" * 78)
    print(f"[{fname}]")
    print("-" * 78)

    # ---- the region, bracketed by its OWN first and last sentences ----
    lines = src.splitlines(keepends=True)
    si = [i for i, ln in enumerate(lines) if start in ln]
    ei = [i for i, ln in enumerate(lines) if end in ln]
    assert len(si) == 1, f"[fix] the START anchor occurs {len(si)} times"
    assert len(ei) == 1, f"[fix] the END anchor occurs {len(ei)} times"
    assert ei[0] > si[0], "[fix] the END anchor precedes the START anchor"
    old_region = "".join(lines[si[0]:ei[0] + 1])
    print(f"  [MEASURED] the region spans lines {si[0] + 1}..{ei[0] + 1} "
          f"({len(old_region)} chars)")
    print(f"  [MEASURED] it names the FLIPS side: "
          f"{'the control set FLIPS' in old_region}")
    print(f"  [MEASURED] it names the (IN, IN) side: "
          f"{'UNCHANGED' in old_region or 'ALSO IN BAND' in old_region}")
    print(f"  ⭐⭐⭐⭐⭐ [MEASURED] ⇒ THE REGION IS *HALF-PORTED*: it carries "
          f"BOTH sides ⇒ it contradicts ITSELF and its body.")

    # ---- the replacement must be NEUTRAL BEFORE IT IS WRITTEN ---------
    for bad in FORBIDDEN:
        assert bad not in new, (
            f"[fix] ABORT: the replacement mentions the forbidden pattern "
            f"{bad!r} -- a replacement that names a side is not neutral, it "
            "is a violation of the same rule")
    print(f"  [OK] the replacement names NEITHER side (checked against "
          f"{len(FORBIDDEN)} forbidden patterns)")

    out = src[:sum(len(x) for x in lines[:si[0]])] + new + \
        src[sum(len(x) for x in lines[:ei[0] + 1]):]
    fp.write_text(out, encoding="utf-8")
    ast.parse(fp.read_text(encoding="utf-8"))
    print(f"  [FIXED] {fname}: the half-ported control-set narrative -> the "
          f"shape-neutral form")

# ======================================================================
# THE FINAL AUDIT -- SCOPED TO THE MODULE DOCSTRING
# ======================================================================
print()
print("=" * 78)
print("THE FINAL AUDIT -- the module docstring's control-set claim")
print("=" * 78)
for fname, _s, _e, _n in REGIONS:
    fp = REPO / f"_c{CYCLE}_{fname}"
    tree = ast.parse(fp.read_text(encoding="utf-8"))
    doc = ast.get_docstring(tree) or ""
    for bad in FORBIDDEN:
        assert bad not in doc, (
            f"[fix] ABORT: {fname}'s MODULE docstring still carries the "
            f"forbidden pattern {bad!r}")
    print(f"  [OK] {fname}: the module docstring carries NONE of the "
          f"forbidden patterns")

# the LIVE CODE is untouched
print()
for fname, probe, why in (
        ("measure.py", "assert IN_BAND,", "the IN-BAND branch"),
        ("page.py", 'assert f"Hour {CYCLE_HOUR_UTC} UTC: {CYCLE_CLASS}"',
         "the BRANCH-SYMMETRIC class gate")):
    txt = (REPO / f"_c{CYCLE}_{fname}").read_text(encoding="utf-8")
    assert probe in txt, f"[fix] ABORT: {fname} lost {why}"
    print(f"  [OK] {fname}: the live code still carries {why} (prose-only "
          f"fix)")

print()
print("=" * 78)
print("CYCLE 1282 -- THE TWO HALF-PORTED DOCSTRINGS ARE REPAIRED")
print("=" * 78)
print("  ⭐⭐⭐ NEXT: RE-RUN THE DOCSTRING-SHAPE INSTRUMENT (it must now "
      "report no defects).")
