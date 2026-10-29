#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- FIX `measure.py`'s DOCSTRING to be SHAPE-NEUTRAL.

⭐⭐⭐⭐⭐ **THIS IS 1277's CLASS-LEVEL FINDING, THIRD MEMBER OF THE FAMILY:**
a DOCSTRING IS A PUBLICATION, and one that contradicts its own body is a
FALSE STATEMENT ABOUT THE WORLD.

⭐⭐⭐⭐⭐ **THE DEFECT:** `_c1280_measure.py`'s MODULE DOCSTRING says

    "⭐⭐ AND THE CONTROL SET **FLIPS** THIS CYCLE: the prior COMMITTED
     cycle was OUT OF BAND (its own block was a BLIND SPOT and its count
     was BORROWED and DISCLAIMED), while THIS cycle is IN BAND -- so the
     two sides DIFFER and the control set FLIPS."

⭐⭐⭐⭐⭐ **BUT THIS CYCLE'S PAIR IS (IN, IN)** -- the prior COMMITTED cycle
(1278, Hour 12) was ALSO IN BAND -- so the docstring asserts the **OPPOSITE**
of the pair its own body implements.  ⭐⭐⭐⭐⭐ **⇒ IT IS INHERITED**: the
shape port rewrites the LIVE CODE and leaves the docstring alone.

⭐⭐⭐⭐⭐ **THE FIX IS *SHAPE-NEUTRAL*, NOT *SHAPE-CORRECTED*.**  A
shape-corrected docstring is a latent assertion about the world and it rots
silently on the next pair change.  ⭐⭐⭐⭐⭐ **⇒ THE REPLACEMENT NAMES
NEITHER SIDE AND QUOTES NEITHER FORBIDDEN PHRASE** -- it states the RULE,
describes BOTH branches, and points at the body as the authority.

⭐⭐⭐⭐⭐ **⇒ A REPLACEMENT THAT *MENTIONS* A FORBIDDEN PATTERN IS NOT
NEUTRAL -- IT IS A VIOLATION OF THE SAME RULE** (1277's own finding: the
fix's own assertion fired on the fix).

⭐⭐⭐⭐⭐ **⇒ THE FIX IS IDEMPOTENT** -- a re-run reports `[ALREADY]`, never a
fake `[FIXED]`.
"""
import ast
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

# ⭐⭐⭐⭐⭐ **THE FORBIDDEN PATTERNS -- the replacement must contain NONE of
# them.**  A replacement that names one of these is not neutral.
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

# ⭐⭐⭐⭐⭐ **THE OLD TEXT -- bracketed by its OWN FIRST AND LAST SENTENCES**
# (the region's boundary is a SENTENCE, not a substring).
_OLD_START = "⭐⭐ AND THE CONTROL SET **FLIPS** THIS CYCLE: the prior COMMITTED"
_OLD_END = "number the *published* prose carries is DERIVED from `PRIOR_CYCLE` (read"

# ⭐⭐⭐⭐⭐ **THE NEW TEXT -- names NEITHER side, quotes NEITHER forbidden
# phrase, and points at the body as the authority.**
_NEW = '''\
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
deliberately names NO number.
'''

fp = REPO / f"_c{CYCLE}_measure.py"
src = fp.read_text(encoding="utf-8")

print("=" * 78)
print(f"CYCLE {CYCLE} -- measure.py's DOCSTRING -> SHAPE-NEUTRAL")
print("=" * 78)

if _OLD_START not in src:
    print("  [ALREADY] the docstring does not carry the OLD shape-scoped text")
    # ⭐⭐⭐⭐⭐ **⇒ `[ALREADY]` IS ONLY HONEST WHEN THE NEW TEXT IS REALLY
    # THERE.**  If neither is present, the text DRIFTED and reporting
    # `[ALREADY]` would be a lie.
    assert _NEW.strip() in src, (
        "[fix] ABORT: the OLD docstring text is absent AND the NEW text is "
        "absent -- the text DRIFTED; reporting [ALREADY] here would be a "
        "LIE")
    print("  [OK] the NEW shape-neutral text IS present")
else:
    # ---- the region, bracketed by its own first and last sentences ----
    lines = src.splitlines(keepends=True)
    si = [i for i, ln in enumerate(lines) if _OLD_START in ln]
    ei = [i for i, ln in enumerate(lines) if _OLD_END in ln]
    assert len(si) == 1, f"[fix] the START anchor occurs {len(si)} times"
    assert len(ei) == 1, f"[fix] the END anchor occurs {len(ei)} times"
    assert ei[0] > si[0], "[fix] the END anchor precedes the START anchor"
    old_region = "".join(lines[si[0]:ei[0] + 1])
    print(f"  [MEASURED] the old region spans lines {si[0] + 1}..{ei[0] + 1} "
          f"({len(old_region)} chars)")
    print(f"  [MEASURED] it names the FLIPS side: "
          f"{'the control set FLIPS' in old_region}")

    # ⭐⭐⭐⭐⭐ **THE REPLACEMENT MUST BE NEUTRAL BEFORE IT IS WRITTEN.**
    for _bad in FORBIDDEN:
        assert _bad not in _NEW, (
            f"[fix] ABORT: the replacement mentions the forbidden pattern "
            f"{_bad!r} -- a replacement that names a side is not neutral, it "
            "is a violation of the same rule")
    print(f"  [OK] the replacement names NEITHER side (checked against "
          f"{len(FORBIDDEN)} forbidden patterns)")

    src = src.replace(old_region, _NEW, 1)
    fp.write_text(src, encoding="utf-8")
    ast.parse(fp.read_text(encoding="utf-8"))
    print("  [FIXED] measure.py's docstring -> the shape-neutral form")

# ---- THE FINAL AUDIT -------------------------------------------------
# ⭐⭐⭐⭐⭐ **THE AUDIT IS SCOPED TO THE *MODULE DOCSTRING* ONLY.**  ⭐⭐⭐⭐⭐
# The file ALSO carries `m6_phase05`'s OWN docstring, which documents the
# OUT-of-band branch -- and it legitimately says "BLIND SPOT" because that
# is what that branch means.  ⭐⭐⭐⭐⭐ **⇒ A WHOLE-FILE FORBIDDEN-SCAN IS
# A FALSE-POSITIVE GENERATOR HERE** -- it would reject the CORRECT
# documentation of a branch that this cycle does not take.
# ⭐⭐⭐⭐⭐ **⇒ THE SCOPE IS *THE DOCSTRING THAT WAS CHANGED*** -- the
# module docstring -- and the scope is asserted, not assumed.
_now = fp.read_text(encoding="utf-8")
_tree = ast.parse(_now)
_doc = _tree.body[0]
assert isinstance(_doc, ast.Expr), "[fix] the module docstring is missing"
_doc_text = ast.get_docstring(_tree) or ""
_doc_lines = _now.splitlines()[_doc.lineno - 1:_doc.end_lineno]
for _bad in FORBIDDEN:
    assert _bad not in _doc_text, (
        f"[fix] ABORT: the MODULE DOCSTRING still carries the forbidden "
        f"pattern {_bad!r}")
print("  [OK] the MODULE DOCSTRING carries NONE of the forbidden patterns "
      f"(scope: lines {_doc.lineno}..{_doc.end_lineno})")
assert _NEW.strip() in _doc_text, (
    "[fix] ABORT: the new text is not in the module docstring")
print("  [OK] the shape-neutral text is present in the module docstring")
# ⭐⭐⭐⭐⭐ **AND THE LIVE CODE IS UNTOUCHED BY THE FIX** -- the fix changed
# prose only.  ⭐⭐⭐⭐⭐ **⇒ THE BODY IS STILL THE AUTHORITY.**
assert "def m6_phase05(passes):" in _now, "[fix] the live code was damaged"
assert "BLIND SPOT" in "\n".join(_now.splitlines()[500:520]), (
    "[fix] ABORT: m6_phase05's own docstring was damaged -- the fix must "
    "touch the MODULE docstring only")
print("  [OK] the live code is untouched (m6_phase05's own branch "
      "documentation survives)")
print()
print("=" * 78)
print("THE FIX IS PUBLISHER-SCOPED -- it travels to EVERY band pair")
print("=" * 78)
print("  ⭐⭐⭐ NEXT: RUN THE SWEEPS, THEN THE CHAIN.")
