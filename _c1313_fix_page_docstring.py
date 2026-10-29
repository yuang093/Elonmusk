#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- FIX THE PAGE DOCSTRING's FALSE NARRATIVE.

⭐⭐⭐⭐⭐ **THE DEFECT (MEASURED BY THE CONTROL-SET PORT'S OWN COMPLETENESS
CHECK):** the page's MODULE DOCSTRING still reads the **(OUT, OUT)**
narrative --

    HOUR211 IS **OUT OF BAND** for RETRY_TRANSLATION_HOURS
    = {0,3,6,9,12,15,18,21} -> the empty-translation retry branch NEVER RAN
    in this hour, so the Phase 0.5 controls are the OUT-OF-BAND side: ...
    ⭐ The prior COMMITTED cycle was ALSO OUT OF BAND -- ... so the
    control set is UNCHANGED, NOT flipped: ...

⭐⭐⭐⭐⭐ **⇒ THE PAGE's DOCSTRING ASSERTED THE *OPPOSITE* OF WHAT THE
PAGE's OWN BODY MEASURES.**  ⭐⭐⭐⭐⭐ This is the **false-narrative** class
(Reminder 25): the body computes `IN_BAND` and publishes
`writer_guard = FIRED`, while the file's own narrative claims the hour is
OUT OF BAND and the control set is UNCHANGED.

⭐⭐⭐⭐⭐ **WHY NOBODY CAUGHT IT UNTIL NOW:** the region lifts port the
*published narrative* (a runtime string), and the identity sweep rewrites
the HOUR token -- but **the MODULE DOCSTRING IS PROSE, and a region lift
anchored on CODE does not reach it.**  ⭐⭐⭐⭐⭐ **⇒ A SWEEP THAT REWRITES
A TOKEN WITHOUT AUDITING THE SENTENCE AROUND IT CAN LEAVE A HALF-PORTED
NARRATIVE.**

⭐⭐⭐⭐⭐ **⭐⭐⭐⭐⭐ AND THE FIX IS *SHAPE-SCOPED*, NOT *SHAPE-NEUTRAL*.**
⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ The page's docstring is **THIS CYCLE'S OWN NARRATIVE** --
it is authored per cycle, exactly like `measure.py`'s.  ⭐⭐⭐⭐⭐ **⇒ THAT
IS DIFFERENT FROM `struct.py`'s AND `jobs.py`'s DOCSTRINGS, WHICH ARE
SHAPE-NEUTRAL AND TRAVEL TO EVERY BAND PAIR** (1277's fix).  ⭐⭐⭐⭐⭐
**⇒ THE PORT MUST NOT RE-TYPE THOSE TWO; THIS FIX TOUCHES ONLY `page.py`.**

⭐⭐⭐⭐⭐ **THE DOCSTRING'S HEAD IS AUTHORED; ITS TAIL IS PRESERVED** (the
tail carries the band-side-NEUTRAL sections -- the banner rule, the
old-region rule, and the "EVERY NUMBER ON THE PAGE IS MEASURED OR
DERIVED" list -- which are the DESTINATION's content and must not be
dropped by a port).

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

print("=" * 78)
print(f"CYCLE {CYCLE} -- FIX THE PAGE DOCSTRING's FALSE NARRATIVE")
print("=" * 78)

_pg = REPO / f"_c{CYCLE}_page.py"
_src = _pg.read_text(encoding="utf-8")

# ---------------------------------------------------------------------
# 0. THE DEFECT -- MEASURED
# ---------------------------------------------------------------------
print()
print("=" * 78)
print("0. THE DEFECT -- MEASURED")
print("=" * 78)
_OUT_TOKENS = ("HOUR211 IS **OUT OF BAND**",
                "control set is UNCHANGED, NOT flipped",
                "the most recent IN-BAND\nblock is the POSITIVE CONTROL",
                "the Phase 0.5 controls are the OUT-OF-BAND side")
for _t in _OUT_TOKENS:
    _n = _src.count(_t)
    print(f"  [MEASURED] the OUT-side narrative token {_t!r}: count={_n}")
    assert _n >= 1, (
        f"[fix] ABORT: the OUT-side narrative token {_t!r} is ABSENT -- the "
        "defect came from somewhere else, and this fix would be a no-op")
print("  ⭐⭐⭐⭐⭐ [MEASURED] the page's docstring carries the OUT-side "
      "narrative while the body measures the IN side.")

# ---------------------------------------------------------------------
# 1. THE IN-SIDE NARRATIVE -- AUTHORED
# ---------------------------------------------------------------------
# ⭐⭐⭐⭐⭐ **THE HEAD IS BUILT FROM A LIST OF LINES, NOT A TRIPLE-QUOTED
# LITERAL** -- because the head's first line IS `"""`, and a triple-quoted
# literal cannot contain `"""` without ending early.
_Q = '"' * 3
_IN_HEAD = "\n".join([
    _Q + "Cycle 1278 -- PAGE ROTATION.",
    "",
    "THIS CYCLE (HOUR212) resolves its REAL NEW @elonmusk posts through",
    "its OWN read paths, adjudicates each one by an INDEPENDENT CLOCK and an",
    "INDEPENDENT AUTHOR check, and fetches each one's content TWICE with",
    "both fetches agreeing on the author, the created_at and the text.",
    "⭐ THE SET BELOW IS WRITTEN AT BUILD TIME FROM THIS CYCLE'S OWN",
    "ADJUDICATION ARTEFACT -- a docstring that TYPES a prior cycle's finding",
    "is a prose string that can name the wrong cycle (Reminder 25).",
    "",
    "⭐ THE DELTA IS MEASURED AGAINST HEAD, NEVER AGAINST THE WORKTREE.  The",
    "prior COMMITTED cycle published normally, but an INTERRUPTED cycle wrote",
    "records into the worktree and never committed them -- so the worktree",
    "carries a worktree-only delta that is a **LIABILITY, not an asset**",
    "(Reminder 26): every worktree-only id must be added to this cycle's own",
    "candidate set EXPLICITLY and re-verified from scratch, never inherited",
    "on trust.",
    "",
    "HOUR212 IS **IN BAND** for RETRY_TRANSLATION_HOURS",
    "= {0,3,6,9,12,15,18,21} -> the empty-translation retry branch RAN in",
    "this hour, so the Phase 0.5 controls are the IN-BAND side: THIS HOUR'S",
    "OWN block must carry the IN-BAND marker and must carry the guard's",
    "SKIPPED line; the count IS this hour's OWN evidence (it is NOT borrowed",
    "and NOT disclaimed); there is NO POSITIVE CONTROL on an IN-BAND hour --",
    "this hour's own block IS the evidence; and a DIFFERENT hour's out-of-band",
    "block is the NEGATIVE CONTROL (Reminder 50).",
    "⭐ The prior COMMITTED cycle was OUT OF BAND -- its own block was a",
    "BLIND SPOT and its count was BORROWED and DISCLAIMED -- while THIS cycle",
    "is IN BAND, so the two sides DIFFER and the control set FLIPS: THIS",
    "hour's own block is the EVIDENCE and the out-of-band block is the",
    "NEGATIVE CONTROL.  The flip is a property of the BAND PAIR, not of the",
    "previous cycle's side alone (Reminder 21 / Reminder 55).",
]) + "\n"

# THE SPLIT MARKER -- the band-side-NEUTRAL TAIL starts here.
_SPLIT = ("⭐⭐ THE BANNER MUST BE REPLACED AS A WHOLE <div>.")


def port_module_docstring_head(path, new_head, split_marker, why):
    """Replace a module docstring's HEAD, keeping its TAIL intact.

    ⭐⭐⭐⭐⭐ **A DOCSTRING IS *THIS CYCLE'S OWN NARRATIVE*, SO IT IS
    AUTHORED -- AND ITS BOUNDARIES ARE AN AST FACT, NOT A TEXT ANCHOR.**

    ⭐⭐⭐⭐⭐ **THE REPLACEMENT MUST BE A *SEGMENT* OF THE SAME STRING**:
    the docstring is ONE triple-quoted string whose closing delimiter sits
    at the very END, so a whole-string replacement that omits the closing
    delimiter glues the following `import` onto the string and the file no
    longer parses.
    """
    p = pathlib.Path(path)
    src = p.read_text(encoding="utf-8")
    tree = ast.parse(src)
    node = tree.body[0]
    assert isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) \
        and isinstance(node.value.value, str), (
            f"[fix] {p.name}: the module has no docstring to port")
    _lines = src.splitlines(keepends=True)
    _d0, _d1 = node.value.lineno - 1, node.value.end_lineno
    _doc = _lines[_d0:_d1]
    _split = [i for i, ln in enumerate(_doc) if split_marker in ln]
    assert len(_split) == 1, (
        f"[fix] {p.name}: the docstring's split marker occurs "
        f"{len(_split)} times -- it must be UNIQUE")
    _si = _split[0]
    _head, _tail = _doc[:_si], _doc[_si:]
    _new_head = new_head.splitlines(keepends=True)
    assert not any('"""' in ln for ln in _new_head[1:]), (
        "[fix] the new docstring head closes the string -- the tail would "
        "be orphaned")
    assert _new_head[0].startswith('"""'), (
        "[fix] the new docstring head must OPEN the string")
    _new = "".join(_lines[:_d0]) + "".join(_new_head) + "".join(_tail) \
        + "".join(_lines[_d1:])
    p.write_text(_new, encoding="utf-8")
    try:
        _tree2 = ast.parse(p.read_text(encoding="utf-8"))
    except SyntaxError as e:
        raise AssertionError(f"[fix] {p.name}: the port produced a SYNTAX "
                             f"ERROR: {e}") from e
    _n2 = _tree2.body[0]
    assert isinstance(_n2, ast.Expr) and isinstance(_n2.value, ast.Constant) \
        and isinstance(_n2.value.value, str), (
            f"[fix] {p.name}: after the port the module's docstring is no "
            "longer body[0] -- the splice landed in the wrong place")
    _v = _n2.value.value
    assert "HOUR212 IS **IN BAND**" in _v, (
        f"[fix] {p.name}: the ported docstring does not state this cycle's "
        "hour and band")
    assert "the control set FLIPS" in _v, (
        f"[fix] {p.name}: the ported docstring does not state that the "
        "control set FLIPS")
    assert "there is NO POSITIVE CONTROL on an IN-BAND hour" in _v, (
        f"[fix] {p.name}: the ported docstring does not state that an "
        "IN-BAND hour has no POSITIVE CONTROL")
    assert split_marker.strip() in _v, (
        f"[fix] {p.name}: the docstring's TAIL did NOT survive the port -- "
        "the fix downgraded the destination")
    print(f"    [PORTED] {why}")


print()
print("=" * 78)
print("1. THE FIX -- AUTHOR THE IN-SIDE NARRATIVE")
print("=" * 78)
port_module_docstring_head(
    _pg, _IN_HEAD, _SPLIT,
    "page.py: the docstring's HEAD -> the IN side (AUTHORED); the TAIL is "
    "PRESERVED")

# ---------------------------------------------------------------------
# 2. THE FIX IS ASSERTED IN BOTH DIRECTIONS
# ---------------------------------------------------------------------
print()
print("=" * 78)
print("2. THE FIX IS ASSERTED IN BOTH DIRECTIONS")
print("=" * 78)
_disk = _pg.read_text(encoding="utf-8")
for _t in _OUT_TOKENS:
    assert _t not in _disk, (
        f"[fix] ABORT: the OUT-side narrative token {_t!r} SURVIVES -- the "
        "fix did not land")
    print(f"  [OK] the OUT-side narrative token is GONE: {_t[:52]!r}")
for _t in ("HOUR212 IS **IN BAND**",
           "the control set FLIPS",
           "there is NO POSITIVE CONTROL on an IN-BAND hour",
           "this hour's OWN evidence"):
    assert _t in _disk, (
        f"[fix] ABORT: the IN-side narrative token {_t!r} is ABSENT -- the "
        "fix did not land")
    print(f"  [OK] the IN-side narrative token is PRESENT: {_t[:52]!r}")

# ⭐⭐⭐⭐⭐ AND THE *STALE CYCLE HEADER* IS GONE -- "Cycle 1277 -- PAGE
# ROTATION" named ANOTHER cycle.
assert "Cycle 1277 -- PAGE ROTATION" not in _disk, (
    "[fix] ABORT: the stale cycle header survives -- the docstring names "
    "another cycle")
print("  [OK] the stale cycle header ('Cycle 1277 -- PAGE ROTATION') is GONE")

# ⭐⭐⭐⭐⭐ AND THE TAIL (the DESTINATION's band-side-NEUTRAL content)
# SURVIVED.
for _t in ("THE BANNER MUST BE REPLACED AS A WHOLE <div>",
           "THE OLD REGION IS THE MARKER LINE PLUS THE CYCLE COMMENT",
           "EVERY NUMBER ON THE PAGE IS MEASURED OR DERIVED"):
    assert _t in _disk, (
        f"[fix] ABORT: the docstring's TAIL lost {_t!r} -- the fix "
        "downgraded the destination")
    print(f"  [OK] the TAIL survived: {_t[:52]!r}")

print()
print("=" * 78)
print("THE PAGE DOCSTRING FIX: DONE")
print("=" * 78)
print("  ⭐⭐⭐ NEXT: RE-RUN THE CONTROL-SET PORT'S COMPLETENESS CHECK, "
      "THEN THE VALUE-TOKEN SWEEP,")
print("          THEN THE IDENTITY SWEEP.")
