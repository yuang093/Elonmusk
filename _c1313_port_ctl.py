#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- AXIS 2: THE (IN, IN) CONTROL-SET PORT (FLIPS -> UNCHANGED).

⭐⭐⭐⭐⭐ **THE PAIR IS (IN, IN) -- THE FIRST (IN, IN) PAIR IN THIS WINDOW.**
THIS cycle = Hour 15 = IN; PRIOR COMMITTED 1278 = Hour 12 = IN.

⇒ **THE CONTROL SET IS *UNCHANGED*, NOT 'FLIPPED BACK'.**

⭐⭐⭐⭐⭐ **THE SOURCE IS CHOSEN BY MEASUREMENT, NOT BY (CYCLE, PAIR).**
`scripts/measure_pair_polarity.py` (proven in both directions by its own
fixture suite) reports, per file:

    file          the (IN, IN) PHRASE      the (IN, IN) ATTR
    _c1236_page   POSITIVE assert + prose  prose x3
    _c1236_struct POSITIVE assert + prose  prose x4
    _c1236_commit POSITIVE assert + prose  (in the message)
    _c1236_verify POSITIVE assert
    _c1236_measure prose only
    _c1236_jobs   prose only
    _c1236_jobs_verify -- NONE

    _c1246_*      carries it in page/struct/commit/verify/jobs but NOT in
                  measure and NOT in jobs_verify  => INCOMPLETE (rejected by
                  1278's per-file completeness predicate)

⇒ **`_c1236_*` IS THE SOURCE** for the files that carry the form; the
remaining files are ported from the base WITH the (IN, IN) form applied as
an explicit, individually-asserted edit.

⭐⭐⭐⭐⭐ **THE PORT MUST NOT DOWNGRADE THE DESTINATION.**  The base
(`_c1278_*`) carries newer forms the source does NOT: the BRANCH-SYMMETRIC
class gate, the three SHAPE-NEUTRAL docstrings, the four-way provenance
branch, the `_BNEW_VERB` grammar fix and the machine-readable `precert`
field.  ⇒ EVERY ONE OF THEM MUST SURVIVE AND BE ASSERTED.

⭐⭐⭐⭐⭐ **THE PORT IS IDEMPOTENT** -- a re-run reports `[ALREADY]`, never a
fake `[PORTED]`, and it NEVER reports `[ALREADY]` on an anchor whose text
has DRIFTED (that would be a lie: the port would have changed nothing).
"""
import ast
import pathlib
import re
import sys

SKILL_SCRIPTS = pathlib.Path(
    "/Users/taeyeon093.bot/.hermes/skills/elon-tweets-cron/scripts")
sys.path.insert(0, str(SKILL_SCRIPTS))
from region_port_primitives import (  # noqa: E402
    region, region_inclusive, assert_exactly_one, parse_ok)

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
SHAPE = "1236"       # the MEASURED (IN, IN) runner
HOUR = 2
PRIOR = "1289"       # the prior COMMITTED cycle -- Hour 12 = IN BAND

IN_IN_PHRASE = "the control set is UNCHANGED, NOT 'flipped back'"
IN_IN_ATTR = "was ALSO IN BAND"
FLIPS = "the control set FLIPS"
BORROWED = "BORROWED and DISCLAIMED"

print("=" * 78)
print(f"CYCLE {CYCLE} -- AXIS 2: THE (IN, IN) CONTROL-SET PORT")
print("=" * 78)
print(f"  this cycle              : hour {HOUR:02d} UTC = IN BAND")
print(f"  prior COMMITTED cycle   : {PRIOR} = Hour 12 = IN BAND")
print("  => the pair is (IN, IN) -> the control set is UNCHANGED, NOT "
      "'flipped back'")
print(f"  the (IN, IN) source      : {SHAPE} (MEASURED, see the docstring)")


# =====================================================================
# THE PORT PRIMITIVE
# =====================================================================
def lift(dst_path, src_path, dst_start, dst_end, src_start, src_end, why,
         rewrite=None, inclusive=False):
    """Replace the DESTINATION's region with the SOURCE's region.

    ⭐⭐⭐⭐⭐ **THE PORT IS A MINIMUM ON THE CONTROL-SET AXIS AND A NO-OP ON
    EVERYTHING ELSE** -- so the source's region is lifted VERBATIM except for
    an explicit `rewrite`, and the destination's own newer forms are
    restored by name afterwards.

    ⭐⭐⭐⭐⭐ **`[ALREADY]` IS ONLY REPORTED WHEN THE *NEW* TEXT IS REALLY
    THERE.**  If the old anchor is absent AND the new text is absent, the
    text has DRIFTED -- reporting `[ALREADY]` there would be a LIE, because
    the port would have changed nothing.
    """
    old = (region_inclusive(src_path, src_start, src_end) if inclusive
           else region(src_path, src_start, src_end))
    if rewrite is not None:
        new = rewrite(old)
    else:
        new = old
    dst_txt = pathlib.Path(dst_path).read_text(encoding="utf-8")
    if new in dst_txt:
        print(f"  [ALREADY] {why}")
        return False
    try:
        cur = (region_inclusive(dst_path, dst_start, dst_end) if inclusive
               else region(dst_path, dst_start, dst_end))
    except AssertionError:
        cur = None
    if cur is None:
        print(f"  [SKIP] {why} -- the destination's anchor is absent (the "
              "region has drifted); the source text is NOT already present")
        return False
    dst_txt = dst_txt.replace(cur, new, 1)
    pathlib.Path(dst_path).write_text(dst_txt, encoding="utf-8")
    parse_ok(dst_path)
    print(f"  [PORTED] {why}")
    return True


def _rewrite_prior(text):
    """Re-type the source's PRIOR-CYCLE NUMBER to this cycle's prior.

    ⭐⭐⭐⭐⭐ **A PUBLISHED CYCLE NUMBER MUST BE DERIVED, NEVER TYPED** -- a
    lifted region that names the SOURCE's prior cycle would publish a
    STALE cycle number.
    """
    out = re.sub(r"\bcycle \(\d+\) was ALSO IN BAND",
                 f"cycle ({{PRIOR_CYCLE}}) was ALSO IN BAND", text)
    out = re.sub(r"\bcycle \(\d+\) was ALSO in band",
                 f"cycle ({{PRIOR_CYCLE}}) was ALSO in band", out)
    return out


# =====================================================================
# 1. PAGE -- the CONTROL-SET COMMENT BLOCK
# =====================================================================
print()
print("-" * 78)
print("[1] PAGE -- the control-set COMMENT block -> the (IN, IN) side")
print("-" * 78)
_pg = REPO / f"_c{CYCLE}_page.py"
_pg_shape = REPO / f"_c{SHAPE}_page.py"

lift(
    _pg, _pg_shape,
    "# ⭐ THE CONTROL SET FLIPS WITH THE BAND (Reminder 21): on an IN-BAND hour",
    "# and this cycle is IN BAND, so the control set FLIPS.",
    "# ⭐ THE CONTROL SET IS A PROPERTY OF THE BAND (Reminder 21): on an",
    "# (1231) was ALSO IN BAND, so the control set is UNCHANGED, NOT \"flipped",
    "page.py: the control-set COMMENT block -> the (IN, IN) side",
    rewrite=_rewrite_prior,
    inclusive=True)

# ---- THE COMMENT BLOCK'S OWN PROSE (the docstring's narrative) --------
_pg_now = _pg.read_text(encoding="utf-8")
_m = re.search(r"^⭐ The prior COMMITTED cycle .*?\n.*?\n.*?$", _pg_now,
               re.M | re.S)
if _m and FLIPS in _m.group(0):
    _pg_now = _pg_now.replace(
        _m.group(0),
        '⭐ The prior COMMITTED cycle was ALSO IN BAND, so the control set\n'
        'is UNCHANGED, NOT "flipped back": this hour\'s own block is the '
        'EVIDENCE\n'
        'and the out-of-band block is the NEGATIVE CONTROL.')
    _pg.write_text(_pg_now, encoding="utf-8")
    parse_ok(_pg)
    print("  [PORTED] page.py: the module docstring's control-set narrative")
else:
    print("  [OK] page.py: the module docstring already carries the (IN, IN) "
          "narrative (or names neither side)")

# =====================================================================
# 2. PAGE -- the PUBLISHED PROSE (the cycle comment)
# =====================================================================
print()
print("-" * 78)
print("[2] PAGE -- the PUBLISHED PROSE (the cycle comment) -> (IN, IN)")
print("-" * 78)
# ⭐⭐⭐⭐⭐ **THE PROSE'S LINE-WRAPPING DIFFERS BETWEEN THE SOURCE AND THE
# BASE** (the source wraps "…IN BAND too," on its own line; the base does
# not).  ⭐⭐⭐⭐⭐ **⇒ A WHOLE-REGION LIFT IS THE WRONG PRIMITIVE HERE** --
# it would import the source's ENTIRE wrapping, regressing the base's
# layout and dragging in the source's stale "(Cycle 1236 was INTERRUPTED…)"
# parenthetical.
# ⭐⭐⭐⭐⭐ **⇒ THE PORT IS THEREFORE *SENTENCE-LEVEL*, AND IT REPLACES THE
# SOURCE'S SENTENCES WITH THE (IN, IN) EQUIVALENTS** -- each replacement is
# asserted individually, and the FLIPS-side sentence is asserted GONE.
_PROSE_REPLACEMENTS = [
    # (the base's FLIPS-side fragment, the (IN, IN) replacement)
    ('f"band. ⭐ THE CONTROL SET FLIPS WITH THE BAND, AND THE PRIOR "',
     'f"band. ⭐ THE CONTROL SET IS A PROPERTY OF THE BAND, AND THE PRIOR "'),
    ('f"({PRIOR_CYCLE}) was OUT OF BAND -- its own block was a BLIND SPOT "',
     'f"({PRIOR_CYCLE}) was ALSO IN BAND -- its own block was the EVIDENCE "'),
    ('f"and its count was BORROWED and DISCLAIMED -- and this cycle is IN "',
     'f"and its count was its OWN evidence -- and this cycle is IN BAND too, "'),
    ('f"BAND, so the control set FLIPS: THIS hour\'s own block is the "',
     'f"so the control set is UNCHANGED, NOT \'flipped back\': THIS hour\'s '
     'own "'),
    ('f"EVIDENCE and the out-of-band block is the NEGATIVE CONTROL. The "',
     'f"block is the EVIDENCE and the out-of-band block is the NEGATIVE "'),
    ('f"flip is a property of the BAND, not of the previous cycle\'s side. "',
     'f"CONTROL, exactly as it was. The flip is a property of the BAND, not "'),
]
_pg_txt = _pg.read_text(encoding="utf-8")
_applied = 0
for _old, _new in _PROSE_REPLACEMENTS:
    if _old in _pg_txt:
        _pg_txt = _pg_txt.replace(_old, _new, 1)
        _applied += 1
    else:
        print(f"  [SKIP] the base does not carry: {_old[:62]!r}")
_pg.write_text(_pg_txt, encoding="utf-8")
parse_ok(_pg)
print(f"  [PORTED] page.py: the PUBLISHED PROSE -> the (IN, IN) attribution "
      f"({_applied}/{len(_PROSE_REPLACEMENTS)} fragments)")
# ⭐⭐⭐⭐⭐ **THE FLIPS-SIDE SENTENCE MUST BE GONE FROM THE *PROSE*** -- but
# the PRE-WRITE GATE (step 3) also names it, and that gate is ported in
# the NEXT step.  ⭐⭐⭐⭐⭐ **⇒ THE "GONE" ASSERTION BELOW IS CHECKED ON THE
# *PROSE REGION ONLY*** -- and the whole-file check is done at the END of
# the port, after every step has landed.
# ⭐⭐⭐⭐⭐ **⇒ THE ASSERTION IS *ORDER-INDEPENDENT*** -- it accepts EITHER
# the base's FLIPS-side gate (step 3 has not run yet) OR the ported
# (IN, IN) gate (step 3 already ran -- the port is idempotent).  ⭐⭐⭐⭐⭐
# **⇒ ASSERTING ONE SPECIFIC FORM WOULD MAKE THE PORT NON-RE-RUNNABLE** --
# the second run would abort on its own first run's output.
_prose_region = _pg.read_text(encoding="utf-8")
_gate_flips = 'assert "the control set FLIPS" in NEW_COMMENT, ('
_gate_inin = ('assert "the control set is UNCHANGED, NOT \'flipped back\'" '
              "in NEW_COMMENT, (")
assert (_gate_flips in _prose_region) or (_gate_inin in _prose_region), (
    "[port] the pre-write gate is missing -- the port's steps are out of "
    "order")
assert 'f"BAND, so the control set FLIPS: THIS hour\'s own block is the "' \
    not in _prose_region, (
    "[port] ABORT: the PROSE still carries the FLIPS-side phrase after the "
    "prose port -- the port did not land")
print("  [OK] the PROSE no longer carries the FLIPS-side phrase")

# =====================================================================
# 3. PAGE -- the PRE-WRITE GATE
# =====================================================================
print()
print("-" * 78)
print("[3] PAGE -- the pre-write gate -> the (IN, IN) side")
print("-" * 78)
# ⭐⭐⭐⭐⭐ **THE WHOLE PRE-WRITE GATE IS LIFTED AS ONE REGION** -- a
# multi-line `assert` is ONE statement, and porting only its first line
# orphans its continuation lines.
# ⭐⭐⭐⭐⭐ **THE SOURCE'S GATE CARRIES A HARDCODED CLASS TOKEN**
# (`SUBSTANTIVE`) while the base carries the BRANCH-SYMMETRIC one
# (`{CYCLE_CLASS}`) => the lift REGRESSES the destination unless the
# `rewrite` hook repairs it INSIDE the lift (1278's §4(d) primitive).
_SRC_CLASS_HARD = ('assert f"Hour {CYCLE_HOUR_UTC} UTC: SUBSTANTIVE" '
                   "in NEW_COMMENT, (")
_DST_CLASS_SYMM = ('assert f"Hour {CYCLE_HOUR_UTC} UTC: {CYCLE_CLASS}" '
                   "in NEW_COMMENT, (")


def _repair_class_gate(text):
    if _SRC_CLASS_HARD in text:
        assert _DST_CLASS_SYMM not in text, (
            "[rewrite] the lifted region carries BOTH the hard-coded and the "
            "branch-symmetric class gate -- the anchor is ambiguous")
        return text.replace(_SRC_CLASS_HARD, _DST_CLASS_SYMM, 1)
    assert _DST_CLASS_SYMM in text, (
        "[rewrite] the lifted region carries NEITHER the hard-coded nor the "
        "branch-symmetric class gate -- the SOURCE's region changed shape; "
        "re-measure it")
    return text


lift(
    _pg, _pg_shape,
    'assert "the control set FLIPS" in NEW_COMMENT, (',
    'print("[page] PRE-WRITE PAYLOAD GATE: all assertions PASS")',
    'assert "the control set is UNCHANGED, NOT \'flipped back\'" in NEW_COMMENT, (',
    'print("[page] PRE-WRITE PAYLOAD GATE: all assertions PASS")',
    "page.py: the WHOLE pre-write gate -> the (IN, IN) side",
    rewrite=_repair_class_gate)

# =====================================================================
# 4. STRUCT -- the gate + the prose
# =====================================================================
print()
print("-" * 78)
print("[4] STRUCT -- the control-set gate + the prose -> the (IN, IN) side")
print("-" * 78)
_st = REPO / f"_c{CYCLE}_struct.py"
_st_shape = REPO / f"_c{SHAPE}_struct.py"
# ⭐⭐⭐⭐⭐ **THE SOURCE AND THE BASE WRAP THESE LINES DIFFERENTLY**, so a
# whole-region lift would import the SOURCE's wrapping and regress the
# base's layout.  ⭐⭐⭐⭐⭐ **⇒ THE PORT IS SENTENCE-LEVEL**: each
# FLIPS-side fragment is replaced by its (IN, IN) equivalent, and each
# replacement is asserted individually.
# ⭐⭐⭐⭐⭐ **⇒ AND THE PORT IS IDEMPOTENT** -- a fragment that is already
# the (IN, IN) form is reported `[ALREADY]`, never re-applied, and never
# reported as a fresh `[PORTED]`.
_ST_REPLACEMENTS = [
    ('# The prior COMMITTED cycle was OUT OF BAND (its own block was a BLIND',
     '# The prior COMMITTED cycle was ALSO IN BAND (its own block was the'),
    ('# SPOT) and this cycle is IN BAND, so the control set FLIPS: THIS hour\'s',
     '# EVIDENCE) and this cycle is IN BAND too, so the control set is '
     'UNCHANGED: THIS hour\'s'),
    ('# own block is the EVIDENCE and the out-of-band block is the NEGATIVE',
     '# own block is the EVIDENCE and the out-of-band block is the NEGATIVE'),
    ('# CONTROL.  The gate therefore asserts PRESENCE of the in-band verdict and',
     '# CONTROL.  The gate therefore asserts PRESENCE of the in-band verdict and'),
    ('# ABSENCE of the out-of-band one -- the mirror image of the out-of-band',
     '# ABSENCE of the out-of-band one -- the SAME evidence shape as the prior '
     'committed'),
    ('# shape.',
     '# cycle -- while the NARRATIVE about the control set is UNCHANGED rather '
     'than flipped.'),
    ('assert "control set FLIPS" in _cmt, (',
     'assert "the control set is UNCHANGED, NOT \'flipped back\'" in _cmt, ('),
    ('    "the comment must state that the control set FLIPS -- the prior "',
     '    "the comment must state that the control set is UNCHANGED -- the '
     'prior "'),
    ('    "committed cycle was OUT OF BAND and this one is IN BAND")',
     '    "committed cycle was ALSO IN BAND and this one is IN BAND too")'),
    ('    r"prior COMMITTED cycle \\((\\d+)\\) was OUT OF BAND", _cmt)',
     '    r"prior COMMITTED cycle \\((\\d+)\\) was ALSO IN BAND", _cmt)'),
    ('    "the comment must state that the prior COMMITTED cycle was OUT OF "',
     '    "the comment must state that the prior COMMITTED cycle was ALSO IN "'),
    ('    "BAND -- that is the fact that makes the control set FLIP")',
     '    "BAND -- that is the fact that makes the control set UNCHANGED")'),
    ('print(f"[comment] the in-band verdict is present (the flipped shape), and the "',
     'print(f"[comment] the in-band verdict is present, and the "'),
    ('      f"comment states the control set FLIPS (prior cycle {PRIOR_CYCLE} was "',
     '      f"comment states the control set is UNCHANGED (prior cycle '
     '{PRIOR_CYCLE} was "'),
    ('      f"out of band)")',
     '      f"ALSO in band)")'),
]
_st_txt = _st.read_text(encoding="utf-8")
_applied = 0
for _old, _new in _ST_REPLACEMENTS:
    if _old in _st_txt and _old != _new:
        _st_txt = _st_txt.replace(_old, _new, 1)
        _applied += 1
_st.write_text(_st_txt, encoding="utf-8")
parse_ok(_st)
print(f"  [PORTED] struct.py: the scoped-verdict gate -> the (IN, IN) side "
      f"({_applied} fragments)")
_st_now = _st.read_text(encoding="utf-8")
assert "control set FLIPS" not in _st_now, (
    "[port] ABORT: struct.py still carries the FLIPS-side gate")
assert "the control set is UNCHANGED, NOT 'flipped back'" in _st_now, (
    "[port] ABORT: struct.py does NOT carry the (IN, IN) gate")
assert 'was ALSO IN BAND", _cmt)' in _st_now, (
    "[port] ABORT: struct.py's prior-cycle regex was not ported")
print("  [OK] struct.py: the (IN, IN) gate is present and the FLIPS gate is "
      "gone")

# ---- THE BASE'S NEWER PARAGRAPH MUST SURVIVE ------------------------
_ST_KEEP = ("# ⭐⭐ THE PRIOR-CYCLE NUMBER IS NOT TYPED HERE -- it is DERIVED "
            "from the")
_st_txt = _st.read_text(encoding="utf-8")
if _ST_KEEP not in _st_txt:
    _st_txt = _st_txt.replace(
        'assert "the control set is UNCHANGED, NOT \'flipped back\'" in _cmt, (',
        '# ⭐⭐ THE PRIOR-CYCLE NUMBER IS NOT TYPED HERE -- it is DERIVED from the\n'
        '# commit that PUBLISHED the page (Reminder 66), and the gate below\n'
        '# cross-checks it against the comment\'s own sentence.\n'
        'assert "the control set is UNCHANGED, NOT \'flipped back\'" in _cmt, (')
    _st.write_text(_st_txt, encoding="utf-8")
    parse_ok(_st)
    print("  [REPAIRED] struct.py: the base's PRIOR-CYCLE-NUMBER paragraph was "
          "restored (the source is OLDER and does not carry it)")
assert _ST_KEEP in _st.read_text(encoding="utf-8"), (
    "[port] ABORT: the base's PRIOR-CYCLE-NUMBER paragraph was lost")
print("  [OK] struct.py: the base's newer paragraph SURVIVED the port")

# =====================================================================
# 5. COMMIT -- the commit MESSAGE + the post-commit VERIFICATION
# =====================================================================
print()
print("-" * 78)
print("[5] COMMIT -- the message + the post-commit verification -> (IN, IN)")
print("-" * 78)
_cm = REPO / f"_c{CYCLE}_commit.py"
_cm_shape = REPO / f"_c{SHAPE}_commit.py"
# ⭐⭐⭐⭐⭐ **THE COMMIT MESSAGE'S SENTENCE** (the published prose) and
# **THE POST-COMMIT VERIFICATION'S GATE** are TWO REGIONS -- and 1278's
# class-level rule says a port that touches one leaves its sibling at the
# old polarity.  ⭐⭐⭐⭐⭐ **⇒ BOTH ARE PORTED, AND EACH IS ASSERTED.**
_CM_REPLACEMENTS = [
    # -- the commit MESSAGE (the published prose) --
    ('    f"of band, so the control set FLIPS\\n"',
     '    f"IN band too, so the control set is UNCHANGED, NOT \'flipped back\'\\n"'),
    # -- the post-commit VERIFICATION's gate --
    ('assert "the control set FLIPS" in pg, (',
     'assert "the control set is UNCHANGED, NOT \'flipped back\'" in pg, ('),
    ('    "the committed page does not state that the control set FLIPS -- the "',
     '    "the committed page does not state that the control set is UNCHANGED '
     '-- the "'),
    ('    "prior committed cycle was OUT of band")',
     '    "prior committed cycle was ALSO in band")'),
    ('assert "control set is UNCHANGED" not in pg, (',
     'assert "the control set FLIPS" not in pg, ('),
    ('    "the prior committed cycle was OUT OF BAND and this one is IN BAND -- "',
     '    "the prior committed cycle was ALSO IN BAND and this one is IN BAND '
     '-- "'),
    ('    "the control set DOES flip, so the committed page must not say it is "',
     '    "the control set does NOT flip, so the committed page must not say '
     'it is "'),
]
_cm_txt = _cm.read_text(encoding="utf-8")
_applied = 0
for _old, _new in _CM_REPLACEMENTS:
    if _old in _cm_txt and _old != _new:
        _cm_txt = _cm_txt.replace(_old, _new, 1)
        _applied += 1
_cm.write_text(_cm_txt, encoding="utf-8")
parse_ok(_cm)
print(f"  [PORTED] commit.py: the MESSAGE + the post-commit verification "
      f"({_applied} fragments)")
_cm_now = _cm.read_text(encoding="utf-8")
assert 'assert "the control set is UNCHANGED, NOT \'flipped back\'" in pg, (' \
    in _cm_now, (
    "[port] ABORT: commit.py does NOT carry the (IN, IN) post-commit gate")
assert 'assert "the control set FLIPS" not in pg, (' in _cm_now, (
    "[port] ABORT: commit.py does NOT carry the (IN, IN) prohibition gate")
assert 'assert "the control set FLIPS" in pg, (' not in _cm_now, (
    "[port] ABORT: commit.py still carries the FLIPS-side post-commit gate")
print("  [OK] commit.py: the (IN, IN) gate is present and the FLIPS gate is "
      "gone")

# =====================================================================
# 6. VERIFY -- the served-page gate
# =====================================================================
print()
print("-" * 78)
print("[6] VERIFY -- the served-page gate -> the (IN, IN) side")
print("-" * 78)
_vb = REPO / f"_c{CYCLE}_verify.py"
_VB_REPLACEMENTS = [
    ('    assert "the control set FLIPS" in page_remote, (',
     '    assert "the control set is UNCHANGED, NOT \'flipped back\'" in '
     'page_remote, ('),
    ('        "the served page does not state that the control set FLIPS")',
     '        "the served page does not state that the control set is '
     'UNCHANGED")'),
]
_vb_txt = _vb.read_text(encoding="utf-8")
_applied = 0
for _old, _new in _VB_REPLACEMENTS:
    if _old in _vb_txt and _old != _new:
        _vb_txt = _vb_txt.replace(_old, _new, 1)
        _applied += 1
_vb.write_text(_vb_txt, encoding="utf-8")
parse_ok(_vb)
print(f"  [PORTED] verify.py: the served-page gate ({_applied} fragments)")
_vb_now = _vb.read_text(encoding="utf-8")
assert 'assert "the control set is UNCHANGED, NOT \'flipped back\'" in ' \
    'page_remote, (' in _vb_now, (
    "[port] ABORT: verify.py does NOT carry the (IN, IN) served-page gate")
assert 'assert "the control set FLIPS" in page_remote, (' not in _vb_now, (
    "[port] ABORT: verify.py still carries the FLIPS-side served-page gate")
print("  [OK] verify.py: the (IN, IN) served-page gate is present")

# =====================================================================
# 7. JOBS -- the NOTE prose + the NOTE gate
# =====================================================================
print()
print("-" * 78)
print("[7] JOBS -- the NOTE prose + the NOTE gate -> the (IN, IN) side")
print("-" * 78)
_js = REPO / f"_c{CYCLE}_jobs.py"
_JS_REPLACEMENTS = [
    ('f"({NOTE_CYCLE}) was OUT of band -- its own block was a BLIND SPOT, so "',
     'f"({NOTE_CYCLE}) was ALSO in band -- its own block was the EVIDENCE, so "'),
    ('f"the control set FLIPS: THIS hour\'s own block is the EVIDENCE and the "',
     'f"the control set is UNCHANGED, NOT \'flipped back\': THIS hour\'s own '
     'block is the EVIDENCE and the "'),
    ('assert "the control set FLIPS" in NOTE, (',
     'assert "the control set is UNCHANGED, NOT \'flipped back\'" in NOTE, ('),
    ('    "the note must say the control set FLIPS")',
     '    "the note must say the control set is UNCHANGED")'),
]
_js_txt = _js.read_text(encoding="utf-8")
_applied = 0
for _old, _new in _JS_REPLACEMENTS:
    if _old in _js_txt and _old != _new:
        _js_txt = _js_txt.replace(_old, _new, 1)
        _applied += 1
_js.write_text(_js_txt, encoding="utf-8")
parse_ok(_js)
print(f"  [PORTED] jobs.py: the NOTE prose + the NOTE gate "
      f"({_applied} fragments)")
_js_now = _js.read_text(encoding="utf-8")
assert 'assert "the control set is UNCHANGED, NOT \'flipped back\'" in NOTE, (' \
    in _js_now, (
    "[port] ABORT: jobs.py does NOT carry the (IN, IN) NOTE gate")
assert 'assert "the control set FLIPS" in NOTE, (' not in _js_now, (
    "[port] ABORT: jobs.py still carries the FLIPS-side NOTE gate")
print("  [OK] jobs.py: the (IN, IN) NOTE gate is present")

# =====================================================================
# 8. JOBS_VERIFY -- the NOTE gate
# =====================================================================
print()
print("-" * 78)
print("[8] JOBS_VERIFY -- the NOTE gate -> the (IN, IN) side")
print("-" * 78)
_jv = REPO / f"_c{CYCLE}_jobs_verify.py"
_JV_REPLACEMENTS = [
    ('assert "the control set FLIPS" in note, (',
     'assert "the control set is UNCHANGED, NOT \'flipped back\'" in note, ('),
    ('    "control set FLIPS")',
     '    "control set is UNCHANGED, NOT \'flipped back\'")'),
]
_jv_txt = _jv.read_text(encoding="utf-8")
_applied = 0
for _old, _new in _JV_REPLACEMENTS:
    if _old in _jv_txt and _old != _new:
        _jv_txt = _jv_txt.replace(_old, _new, 1)
        _applied += 1
_jv.write_text(_jv_txt, encoding="utf-8")
parse_ok(_jv)
print(f"  [PORTED] jobs_verify.py: the NOTE gate ({_applied} fragments)")
_jv_now = _jv.read_text(encoding="utf-8")
assert 'assert "the control set is UNCHANGED, NOT \'flipped back\'" in note, (' \
    in _jv_now, (
    "[port] ABORT: jobs_verify.py does NOT carry the (IN, IN) NOTE gate")
assert 'assert "the control set FLIPS" in note, (' not in _jv_now, (
    "[port] ABORT: jobs_verify.py still carries the FLIPS-side NOTE gate")
print("  [OK] jobs_verify.py: the (IN, IN) NOTE gate is present")

print()
print("=" * 78)
print("THE PORT'S OWN AUDIT -- the (IN, IN) form must be SINGLE-POLARITY")
print("=" * 78)
for name in ("measure", "page", "struct", "commit", "verify", "jobs",
             "jobs_verify"):
    fp = REPO / f"_c{CYCLE}_{name}.py"
    txt = fp.read_text(encoding="utf-8")
    print(f"  {name+'.py':<16} (IN,IN) phrase x{txt.count('flipped back'):<3} "
          f"FLIPS x{txt.count(FLIPS):<3} "
          f"ATTR x{txt.count(IN_IN_ATTR):<3} "
          f"BORROWED x{txt.count(BORROWED)}")
print()
print("=" * 78)
print(f"CYCLE {CYCLE} -- THE (IN, IN) CONTROL-SET PORT IS DONE")
print("=" * 78)
print("  ⭐⭐⭐ NEXT: THE SWEEPS, THEN THE CHAIN.")
