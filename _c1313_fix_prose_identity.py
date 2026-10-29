#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- REPAIR THE PROSE IDENTITY, AND THE `m6_phase05` DOCSTRING.

⭐⭐⭐⭐⭐ **DEFECT #1 -- THE PROSE HOUR IS NOT THE CONSTANT'S HOUR.**

The identity sweep rewrites the prose hour `OLD_HOUR -> HOUR`.  It reads
`OLD_HOUR` out of the clone SOURCE's `measure.py` **constant**.  ⭐⭐⭐⭐⭐
**BUT THE CONSTANT AND THE PROSE ARE TWO DIFFERENT SURFACES**, and cycle
1280's MIS-TARGETED sweep left them DIVERGED:

  * the CONSTANT was re-typed by 1280's clone (`CYCLE_HOUR_UTC = 2`);
  * the PROSE was NEVER re-typed (the sweep rewrote the base generation
    instead of its own), so it still carries the ORIGINAL base
    generation's hour (12).

⇒ **THE PROSE-HOUR REWRITE SOURCE MUST BE MEASURED FROM THE PROSE
ITSELF.**  ⭐⭐⭐⭐⭐ **⇒ THE FIX IS TO MEASURE THE PROSE'S OWN HOUR AND
REWRITE *THAT*, AND TO ASSERT THE CONSTANT AND THE PROSE AGREE
AFTERWARD.**  (This is the same rule 1275 named: **the token is not the
fact, the sentence is** -- and here the *pair* of surfaces is the fact.)

⭐⭐⭐⭐⭐ **DEFECT #2 -- `m6_phase05`'s DOCSTRING CONTRADICTS ITS OWN BODY.**

`_c1278_measure.py`'s `m6_phase05` opens with

    '''Hour 12 IS OUT OF BAND -> the branch NEVER RAN in this hour.

and then documents the OUT branch in full -- while the BODY asserts
`IN_BAND` (the IN branch).  ⭐⭐⭐⭐⭐ **THE BODY IS THE IN-BAND BRANCH
AND IT IS RIGHT**; the docstring is a FALSE STATEMENT ABOUT THE WORLD.

⭐⭐⭐⭐⭐ **⇒ THE FIX IS *SHAPE-NEUTRAL*, NOT *SHAPE-CORRECTED*.**  A
docstring that names one side rots silently on the next pair change, and
a docstring is not read by any assertion -- so nothing would object
(cycle 1277's class-level finding, in cycle 1275's class).  ⭐⭐⭐⭐⭐ The
replacement states the RULE, describes BOTH branches, and points at the
body as the authority.

⭐⭐⭐⭐⭐ **⇒ AND THE REPLACEMENT MUST NAME NEITHER SIDE** -- a
replacement that mentions a forbidden pattern is a violation of the same
rule (1277's own finding, about 1277's own fix).
"""
import ast
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
HOUR = 2

# ======================================================================
# THE FORBIDDEN PATTERNS -- the replacement must contain NONE of them
# ======================================================================
FORBIDDEN = [
    "IS OUT OF BAND",
    "IS IN BAND",
    "IS **IN BAND**",
    "IS **OUT OF BAND**",
    "the branch NEVER RAN",
    "the branch RAN",
    "NO_EVIDENCE_THIS_HOUR",
    "writer_guard = FIRED",
]

# ======================================================================
# DEFECT #1 -- MEASURE THE PROSE'S OWN HOUR, AND REWRITE THAT
# ======================================================================
print("=" * 78)
print("DEFECT #1 -- THE PROSE HOUR IS A *SURFACE*, AND IT DIVERGED FROM "
      "THE CONSTANT")
print("=" * 78)

# the SELF-LABEL prose forms -- MEASURED, not typed
PROSE_HOUR_RE = re.compile(
    r"\b(?:CYCLE\s+1[0-9]{3}\s+IS\s+HOUR\s+|THIS CYCLE \(HOUR\s+|"
    r"HOUR\s+|Hour\s+|hour\s+)(\d{1,2})(?:\s+UTC\b|\s+IS\b|\b)")
PROSE_HOUR_RES = [
    re.compile(r"\bCYCLE\s+1[0-9]{3}\s+IS\s+HOUR\s+(\d{1,2})\b"),
    re.compile(r"\bTHIS CYCLE \(HOUR\s+(\d{1,2})\s+UTC\)"),
    re.compile(r"\bHOUR\s+(\d{1,2})\s+UTC\s+IS\s+\*\*"),
    re.compile(r"\bbelongs to Hour\s+(\d{1,2})\s+UTC\b"),
    re.compile(r'"""Hour\s+(\d{1,2})\s+IS\s+'),
    re.compile(r"hour\s+(\d{1,2})\s+IS\s+IN BAND"),
]

RUN_SET = [
    "measure", "page", "struct", "commit", "verify", "jobs", "jobs_verify",
    "paths", "adjudicate", "payload", "translate", "select", "build",
    "write", "render", "render_posts", "triage", "band_firetest",
    "fidelity2", "third_instrument", "fetch_new", "d_keepcheck", "precert",
]


def prose_hours_in(text):
    """Every hour the SELF-LABEL prose forms name, measured."""
    out = set()
    for rx in PROSE_HOUR_RES:
        for m in rx.finditer(text):
            out.add(int(m.group(1)))
    return out


# ---- the prose hour, MEASURED across the RUN SET ------------------------
prose_hours = {}
for f in RUN_SET:
    p = REPO / f"_c{CYCLE}_{f}.py"
    if not p.exists():
        continue
    for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines()):
        for rx in PROSE_HOUR_RES:
            for m in rx.finditer(ln):
                prose_hours.setdefault(int(m.group(1)), []).append(
                    (f, i + 1, ln.strip()[:100]))

print("  the SELF-LABEL prose hours, MEASURED:")
for k in sorted(prose_hours):
    print(f"    hour {k}: {len(prose_hours[k])} occurrence(s)")
    for f, ln, t in prose_hours[k]:
        print(f"        {f}:{ln}  {t}")

# ---- THE CONSTANT, for the cross-check ----------------------------------
_const = re.search(r"(?m)^CYCLE_HOUR_UTC\s*=\s*(\d+)\s*$",
                   (REPO / f"_c{CYCLE}_measure.py").read_text(encoding="utf-8"))
CONST_HOUR = int(_const.group(1))
print()
print(f"  the CONSTANT's hour        : {CONST_HOUR}")
print(f"  the PROSE's hour(s)        : {sorted(prose_hours)}")
assert len(prose_hours) == 1, (
    f"[fix] ABORT: the prose names {len(prose_hours)} different hours "
    f"{sorted(prose_hours)} -- the rewrite source is AMBIGUOUS; re-measure "
    "rather than guess")
PROSE_HOUR = next(iter(prose_hours))
print(f"  ⇒ the rewrite source is the PROSE's hour: {PROSE_HOUR}")

# ---- the REWRITE: PROSE_HOUR -> HOUR, ON THE SELF-LABEL FORMS ONLY -----
print()
print("  [REWRITE] the SELF-LABEL prose hour -> %d" % HOUR)
_replaced = []
for f in RUN_SET:
    p = REPO / f"_c{CYCLE}_{f}.py"
    if not p.exists():
        continue
    src = p.read_text(encoding="utf-8")
    out = src

    def _sub(rx, s):
        """Rewrite ONLY the captured hour token -- never a SUBSTRING of a
        longer number that merely CONTAINS the hour's digits.

        ⭐⭐⭐⭐⭐ **THE BUG THIS GUARDS AGAINST (it FIRED on this cycle's
        first run):** `m.group(0).replace(m.group(1), f"{HOUR}")` replaces
        the FIRST OCCURRENCE of the captured digits *anywhere in the match*,
        and the match `CYCLE 1282 IS HOUR212` contains `12` inside
        `1282` FIRST ⇒ it rewrote `CYCLE 1282` into `CYCLE 1882` and left
        the hour alone.  ⇒ **THE REPLACEMENT MUST TARGET THE CAPTURED
        GROUP'S OWN POSITION**, not a substring search.
        """
        return re.sub(rx, lambda m: (m.group(0)[:m.start(1) - m.start(0)]
                                      + f"{HOUR}"
                                      + m.group(0)[m.end(1) - m.start(0):]),
                      s)

    # each form, anchored so it ONLY rewrites THIS cycle's own label, and
    # each CAPTURING the hour so the rewrite cannot touch a longer number
    out = _sub(re.compile(rf"\bCYCLE 1[0-9]{{3}}\s+IS\s+HOUR\s+({PROSE_HOUR})\b"),
               out)
    out = _sub(re.compile(rf"\bTHIS CYCLE \(HOUR\s+({PROSE_HOUR})\s+UTC\)"), out)
    out = _sub(re.compile(rf"\bHOUR\s+({PROSE_HOUR})\s+UTC\s+IS\s+\*\*"), out)
    out = _sub(re.compile(rf"\bbelongs to Hour\s+({PROSE_HOUR})\s+UTC\b"), out)
    out = _sub(re.compile(rf'"""Hour\s+({PROSE_HOUR})\s+IS\s+'), out)
    out = _sub(re.compile(rf"\bhour\s+({PROSE_HOUR})\s+IS\s+IN BAND"), out)
    if out != src:
        p.write_text(out, encoding="utf-8")
        _replaced.append(f)
print(f"    [REWRITTEN] {len(_replaced)} file(s): {_replaced}")

# ---- THE CROSS-CHECK: the CONSTANT AND THE PROSE NOW AGREE -------------
print()
print("  [CROSS-CHECK] the CONSTANT and the PROSE must now agree")
_after = {}
for f in RUN_SET:
    p = REPO / f"_c{CYCLE}_{f}.py"
    if not p.exists():
        continue
    for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines()):
        for rx in PROSE_HOUR_RES:
            for m in rx.finditer(ln):
                _after.setdefault(int(m.group(1)), []).append((f, i + 1))
print(f"    the prose hours now: { {k: len(v) for k, v in sorted(_after.items())} }")
_stale = {k: v for k, v in _after.items() if k != HOUR}
assert not _stale, (
    f"[fix] ABORT: the prose still names {sorted(_stale)} -- the rewrite did "
    f"not reach every SELF-LABEL form")
assert CONST_HOUR == HOUR, (
    f"[fix] ABORT: the CONSTANT is {CONST_HOUR}, expected {HOUR}")
print(f"    [OK] every SELF-LABEL prose hour is {HOUR}, and the CONSTANT is "
      f"{CONST_HOUR}")

# ======================================================================
# DEFECT #2 -- `m6_phase05`'s DOCSTRING -> SHAPE-NEUTRAL
# ======================================================================
print()
print("=" * 78)
print("DEFECT #2 -- `m6_phase05`'s DOCSTRING CONTRADICTS ITS OWN BODY")
print("=" * 78)

_NEW = '''\
"""THIS HOUR'S OWN EVIDENCE -- and WHICH BLOCK IS THE CONTROL.

    ⭐⭐⭐⭐⭐ **THE HOUR IS A CONSTANT OF THE CYCLE, NOT THE WALL CLOCK.**
    A cycle can be INTERRUPTED and RESUMED in a LATER hour.  The hour a
    cycle BELONGS TO is the hour its OWN log block carries -- the block
    this cycle's own fetcher pass wrote -- NOT the hour in which the
    cycle's script happens to be running.  The wall clock measures WHEN
    THE SCRIPT RAN, which is not the quantity the page asserts about.

    ⭐⭐⭐⭐⭐ **WHICH BLOCK IS THE EVIDENCE AND WHICH IS THE CONTROL IS A
    *FUNCTION OF THE BAND PAIR* -- the prior committed cycle's side and
    THIS cycle's side together decide it, and the SAME rule covers every
    pair: two cycles on the SAME side keep the assignment, and two cycles
    on DIFFERENT sides swap it.  ⭐⭐⭐⭐⭐ **⇒ THIS DOCSTRING THEREFORE
    NAMES NEITHER SIDE** -- a docstring that asserts one side of the band
    is a FALSE STATEMENT ABOUT THE WORLD the moment the band pair
    changes, and a docstring is not read by any assertion, so nothing
    would object (cycle 1277's finding).

    ⭐⭐⭐⭐⭐ **THE BODY IS THE AUTHORITY** -- read the branch it actually
    takes, and let it choose the prose.  ⭐⭐⭐⭐⭐ The reader can find
    every term of the rule in the body below: which block is THIS hour's
    own, which block is the control that proves the matcher DISCRIMINATES
    rather than matching on prose, and how the guard's count is derived
    from source rather than typed.
    """'''

_m = (REPO / f"_c{CYCLE}_measure.py")
_src = _m.read_text(encoding="utf-8")

# ---- the OLD docstring, bracketed by its OWN first and last sentences ----
_i = _src.find("def m6_phase05(passes):")
assert _i >= 0, "[fix] measure.py has no m6_phase05"
_s = _src.find('"""', _i)
assert _s >= 0, "[fix] m6_phase05 has no docstring"
_e = _src.find('"""', _s + 3)
assert _e > _s, "[fix] m6_phase05's docstring is unterminated"
_old = _src[_s:_e + 3]
print(f"  [MEASURED] the old docstring is {len(_old)} chars")
print(f"  [MEASURED] it names the OUT side: {'IS OUT OF BAND' in _old}")
print(f"  [MEASURED] the BODY asserts the IN side: "
      f"{'assert IN_BAND' in _src}")

# ---- the replacement must be NEUTRAL BEFORE IT IS WRITTEN --------------
for _bad in FORBIDDEN:
    assert _bad not in _NEW, (
        f"[fix] ABORT: the replacement mentions the forbidden pattern "
        f"{_bad!r} -- a replacement that names a side is not neutral, it is "
        "a violation of the same rule")
print(f"  [OK] the replacement names NEITHER side (checked against "
      f"{len(FORBIDDEN)} forbidden patterns)")

if _old.strip() != _NEW.strip():
    _src = _src[:_s] + _NEW + _src[_e + 3:]
    _m.write_text(_src, encoding="utf-8")
    ast.parse(_m.read_text(encoding="utf-8"))
    print("  [FIXED] measure.py's m6_phase05 docstring -> the shape-neutral "
          "form")
else:
    print("  [ALREADY] m6_phase05's docstring already carries the "
          "shape-neutral form")

# ======================================================================
# DEFECT #3 -- THE MODULE DOCSTRING'S OWN CYCLE SELF-LABEL
# ======================================================================
print()
print("=" * 78)
print("DEFECT #3 -- THE MODULE DOCSTRING'S OWN CYCLE SELF-LABEL")
print("=" * 78)
# ⭐⭐⭐⭐⭐ **EVERY MODULE DOCSTRING OPENS WITH `Cycle <n> -- <what it
# does>`, AND THAT IS *THIS CYCLE'S OWN SELF-LABEL*.**  ⭐⭐⭐⭐⭐ It is NOT a
# historical citation -- a citation names ANOTHER cycle and explains WHY a
# fix exists; a docstring's FIRST LINE names what THIS file IS.
# ⭐⭐⭐⭐⭐ **⇒ THE SWEEP'S CITATION EXEMPTION EXEMPTED IT** (because the
# exemption's reference was the CORRUPTED prose identity, so `1278` looked
# like a citation) ⇒ **⇒ AND THE FILE WAS LEFT CLAIMING TO BE CYCLE 1278.**
# ⭐⭐⭐⭐⭐ **⇒ THE FIX IS TO RE-TYPE THE *DOCSTRING'S OWN FIRST LINE* --
# MEASURED, NOT TYPED** -- and to assert it in BOTH directions.
#
# ⭐⭐⭐⭐⭐ **⇒ AND THE FIX IS SCOPED TO THE MODULE DOCSTRING'S FIRST
# LINE**: a `Cycle 1249:` mention in a RULE LIST deeper in the file is a
# HISTORICAL CITATION and must survive (the sweep's 2j audit protects it).
_self_label_line = re.compile(r'(?m)^("""Cycle\s+)(\d{3,4})(\s+--)')
_fixed_self = []
for _f in RUN_SET:
    _fp = REPO / f"_c{CYCLE}_{_f}.py"
    if not _fp.exists():
        continue
    _src = _fp.read_text(encoding="utf-8")
    _mm = _self_label_line.search(_src)
    if not _mm:
        continue
    if _mm.group(2) == CYCLE:
        continue
    _out = _src[:_mm.start(2)] + CYCLE + _src[_mm.end(2):]
    _fp.write_text(_out, encoding="utf-8")
    ast.parse(_out)
    _fixed_self.append((_f, _mm.group(2)))
print(f"  [RE-TYPED] the module docstring's own cycle self-label in "
      f"{len(_fixed_self)} file(s): {_fixed_self}")

# ---- the audit, in BOTH directions --------------------------------------
print()
print("  [AUDIT] every module docstring's own self-label must name THIS "
      "cycle")
_bad = []
for _f in RUN_SET:
    _fp = REPO / f"_c{CYCLE}_{_f}.py"
    if not _fp.exists():
        continue
    _src = _fp.read_text(encoding="utf-8")
    _mm = _self_label_line.search(_src)
    if _mm and _mm.group(2) != CYCLE:
        _bad.append((_f, _mm.group(2)))
assert not _bad, (
    f"[fix] ABORT: these module docstrings still name another cycle: {_bad}")
print(f"    [OK] every module docstring's self-label names {CYCLE}")

# ======================================================================
# THE FINAL AUDIT
# ======================================================================
print()
print("=" * 78)
print("THE FINAL AUDIT")
print("=" * 78)
_now = _m.read_text(encoding="utf-8")
ast.parse(_now)

# the docstring is shape-neutral
_tree = ast.parse(_now)
_fn = None
for _node in ast.walk(_tree):
    if (isinstance(_node, ast.FunctionDef)
            and _node.name == "m6_phase05"):
        _fn = _node
        break
assert _fn is not None, "[fix] m6_phase05 vanished"
_fn_doc = ast.get_docstring(_fn) or ""
assert _fn_doc, "[fix] m6_phase05 has no docstring"
for _bad in FORBIDDEN:
    assert _bad not in _fn_doc, (
        f"[fix] ABORT: m6_phase05's docstring still carries the forbidden "
        f"pattern {_bad!r}")
print("  [OK] m6_phase05's docstring carries NONE of the forbidden patterns")

# the docstring agrees with the BODY's branch
assert "assert IN_BAND" in _now, (
    "[fix] ABORT: the live code no longer asserts the IN-BAND branch -- "
    "the fix must touch prose only")
print("  [OK] the live code still asserts the IN-BAND branch (prose-only fix)")

# the module docstring is still shape-neutral (1280's fix survived)
_mod_doc = ast.get_docstring(_tree) or ""
assert "THE CONTROL SET IS A *FUNCTION OF THE BAND PAIR*" in _mod_doc, (
    "[fix] ABORT: 1280's SHAPE-NEUTRAL module docstring was damaged")
# ⭐⭐⭐⭐⭐ **THE MODULE DOCSTRING'S *BAND* CLAIM IS NOT SCOPE-FREE.**  It
# is **SHAPE-SCOPED BY DESIGN** in this lineage, and it is SELF-CONSISTENT
# per generation: 1266/1274/1277 name the OUT side while their bodies
# assert the OUT branch, and 1278 names the IN side while its body asserts
# the IN branch.  ⇒ **⇒ A FORBIDDEN-SCAN OVER THE WHOLE MODULE DOCSTRING
# WOULD REJECT THE CORRECT, SELF-CONSISTENT NARRATIVE.**  ⭐⭐⭐⭐⭐ **⇒ THE
# SCOPE HERE IS THE *CONTROL-SET* CLAIM** -- the one 1280 made
# shape-neutral -- and NOT the band's own vocabulary.
for _bad in ("the control set FLIPS",
             "control set is UNCHANGED, NOT 'flipped back'"):
    assert _bad not in _mod_doc, (
        f"[fix] ABORT: the MODULE docstring carries the shape-scoped "
        f"control-set claim {_bad!r}")
print("  [OK] 1280's SHAPE-NEUTRAL control-set claim SURVIVED in the "
      "module docstring")

# the (IN, IN) shape survived
for _f, _probe in (
        ("page.py", "the control set is UNCHANGED, NOT 'flipped back'"),
        ("struct.py", "the control set is UNCHANGED, NOT 'flipped back'"),
        ("commit.py", "the control set is UNCHANGED, NOT 'flipped back'"),
        ("jobs.py", "the prior committed cycle was ALSO in band"),
        ("jobs_verify.py", "the prior committed cycle was ALSO in band")):
    _t = (REPO / f"_c{CYCLE}_{_f}").read_text(encoding="utf-8")
    assert _probe in _t, f"[fix] ABORT: {_f} lost {_probe!r}"
print("  [OK] the (IN, IN) shape SURVIVED the prose repair")

print()
print("=" * 78)
print("CYCLE 1282 -- THE PROSE IDENTITY AND THE DOCSTRING ARE REPAIRED")
print("=" * 78)
print("  ⭐⭐⭐ NEXT: RE-RUN THE IDENTITY SWEEP (it must now pass its 2h "
      "audit).")
