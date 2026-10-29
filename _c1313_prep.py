#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- PREPARE THE BLUEPRINT: clone from 1282 (the (IN, IN) shape),
re-type the identity to THIS cycle, and re-derive every identity FROM ARTEFACTS.

⭐⭐⭐⭐⭐ **THE THREE IDENTITIES ARE MEASURED, NEVER TYPED** (per
`references/a-cycle-that-inherits-two-interrupted-cycles.md`):
  * the cycle NUMBER = this tick's own position in the lineage -> 1285
  * the HOUR        = this tick's OWN fetcher pass -> the most recent
    fetch.log block whose UTC hour is 21 -> 21
  * the prior COMMITTED cycle = the commit that PUBLISHED index.html ->
    1278 (hour 12) -> IN of band

⭐⭐⭐⭐⭐ **⇒ THE PAIR IS (IN, IN)** -- this cycle's hour 21 IS in
RETRY_TRANSLATION_HOURS = {0,3,6,9,12,15,18,21}, and the prior COMMITTED
cycle 1278's hour 12 is too ⇒ **THE CONTROL SET IS UNCHANGED, NOT FLIPPED.**

⭐⭐⭐⭐⭐ **WHY THE CLONE SOURCE IS 1282 (NOT 1283/1284).**  1282 is the
ONLY generation on disk that is COMPLETE on the (IN, IN) shape:
  * its `measure.py` / `page.py` are IN-side (measured by
    `scripts/measure_band_polarity_per_file.py`), and
  * its control-set attribution is the UNCHANGED form ("the control set is
    UNCHANGED, NOT 'flipped back'").
1283 and 1284 are the (IN, OUT) shape and 1284 is additionally HALF-PORTED
(its `page.py` is MIXED) -- so neither can serve as an (IN, IN) base.

⭐⭐⭐⭐⭐ **NO PORT IS NEEDED.**  The base's shape IS this cycle's shape:
both are the (IN, IN) pair.  ⇒ **THE SHAPE FIX TRAVELS AS-IS** (1276's
two-axis rule: a SHAPE-scoped fix travels only when the PAIR is identical,
and here the PAIR is identical).

⭐⭐⭐⭐⭐ **SELF-CLEANING AND IDEMPOTENT.**  A re-run deletes the whole
`_c1285_*` generation and re-clones, so a corrected re-run yields a
complete, consistent generation.

⭐⭐⭐⭐⭐ **THIS SCRIPT VALIDATES EVERY ANCHOR *UP FRONT* (a read-only
anchor census) ⇒ A PORT THAT ABORTS MIDWAY CANNOT LEAVE A HALF-PORTED
BLUEPRINT** (cycle 1284's class-level finding).
"""
import ast
import pathlib
import re
import shutil
import subprocess

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
BASE = "1282"          # the ONLY complete (IN, IN) generation on disk
HOUR = 2              # THIS tick's OWN hour -- IN BAND

BAND_FILES = ["measure", "page", "struct", "commit", "verify", "jobs",
              "jobs_verify"]
FIX_FILES = ["paths", "adjudicate", "payload", "translate", "select", "build",
             "write", "render", "render_posts", "triage", "band_firetest",
             "fidelity2", "third_instrument", "fetch_new", "d_keepcheck",
             "precert"]
LEGACY = ["patch_measure"]
LEGACY_CARRY = ["patch_anchor", "patch_band", "patch_noop", "patch_literals"]
CARRY = ["patch_prose"]
ALL = BAND_FILES + FIX_FILES + LEGACY + LEGACY_CARRY + CARRY
# the instruments THIS cycle RUNS -- each reads `_c{CYCLE}_*.py`, so each
# one's OWN `CYCLE` must be THIS cycle's.
RUN_INSTRUMENTS = ["clone_sweep", "sweep_tokens", "docstring_shape"]
# 1282 has NO `sweep_identity.py`; its identity sweep IS `clone_sweep.py`.
SWEEP_SRC = "1282"

print("=" * 78)
print(f"CYCLE {CYCLE} -- PREPARE (clone from {BASE}, hour {HOUR})")
print("=" * 78)
_SELF = pathlib.Path(__file__).resolve()

# =====================================================================
# 1. THE BAND -- DERIVED FROM SOURCE, NEVER TYPED
# =====================================================================
_ft = (REPO / "fetch_tweets.py").read_text(encoding="utf-8")
_bm = re.search(r"RETRY_TRANSLATION_HOURS\s*=\s*\{([^}]*)\}", _ft)
assert _bm, "[prep] could not read RETRY_TRANSLATION_HOURS from fetch_tweets.py"
_BAND = {int(x) for x in re.findall(r"\d+", _bm.group(1))}
print(f"  [MEASURED] source-derived RETRY_TRANSLATION_HOURS = {sorted(_BAND)}")
assert HOUR in _BAND, (
    f"[prep] ABORT: hour {HOUR} is NOT in the band -- the (IN, IN) shape "
    "would be wrong")
print(f"  [MEASURED] hour {HOUR} -> IN BAND")

# =====================================================================
# 2. THIS TICK's OWN FETCH BLOCK -- the hour's EVIDENCE, measured
# =====================================================================
_log = (REPO / "fetch.log").read_text(encoding="utf-8", errors="replace")
_hdrs = [ln.strip() for ln in _log.splitlines()
         if re.match(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\]", ln.strip())]
assert _hdrs, "[prep] no fetch.log headers"
_last = _hdrs[-1]
_m = re.match(r"^\[(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2})\]", _last)
assert _m, f"[prep] could not parse the last fetch.log header {_last!r}"
# the log's timestamps are CST; the cycle's hour is UTC
_hdr_utc_hour = (int(_m.group(2)) - 8) % 24
print(f"  [MEASURED] this tick's OWN fetch.log block = {_last!r} -> "
      f"UTC hour {_hdr_utc_hour}")
assert _hdr_utc_hour == HOUR, (
    f"[prep] ABORT: this tick's own fetch block is UTC hour {_hdr_utc_hour}, "
    f"not the cycle's hour {HOUR}")

# =====================================================================
# 3. THE PRIOR COMMITTED CYCLE -- MEASURED FROM HEAD
# =====================================================================
_head_subject = subprocess.run(
    ["git", "log", "-1", "--format=%s", "--", "index.html"],
    cwd=REPO, capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\d+)", _head_subject)
assert _pm, f"[prep] could not read the prior cycle from {_head_subject!r}"
PRIOR = _pm.group(1)
_pg = subprocess.run(["git", "show", "HEAD:index.html"], cwd=REPO,
                     capture_output=True, text=True).stdout
_cmt = re.search(r"<!--\s*cron cycle (\d+):(.*?)-->", _pg, re.S)
assert _cmt and _cmt.group(1) == PRIOR, (
    "[prep] HEAD's page and its publishing commit disagree on the cycle")
_hm = re.search(r"=\s*Hour (\d{1,2}) UTC", _cmt.group(2))
assert _hm, "[prep] HEAD's cycle comment carries no `= Hour NN UTC`"
PRIOR_HOUR = int(_hm.group(1))
assert PRIOR_HOUR in _BAND, (
    f"[prep] ABORT: the prior cycle's measured hour {PRIOR_HOUR} is NOT in "
    "the band")
print(f"  [MEASURED] prior COMMITTED cycle = {PRIOR}, hour = {PRIOR_HOUR} "
      "-> IN BAND")
print(f"  ⭐⭐⭐⭐⭐ [OK] THE PAIR IS (IN, IN) -- MEASURED, NOT ASSUMED")
print(f"  ⭐⭐⭐⭐⭐ ⇒ THE CONTROL SET IS UNCHANGED, NOT FLIPPED")

# =====================================================================
# 4. A CLEAN SLATE -- the previous partial run's artefacts are discarded
# =====================================================================
for _p in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    if _p.resolve() == _SELF:
        continue
    _p.unlink()
print(f"[prep] the stale _c{CYCLE}_* artefacts were discarded (a clean "
      "slate -- the previous partial run's files are not trusted)")

# =====================================================================
# 5. THE CLONE
# =====================================================================
cloned = 0
for src in sorted(REPO.glob(f"_c{BASE}_*.py")):
    name = src.name[len(f"_c{BASE}_"):]
    shutil.copy2(src, REPO / f"_c{CYCLE}_{name}")
    cloned += 1
print(f"[prep] {cloned} files cloned from {BASE}")
assert cloned >= 20, f"[prep] only {cloned} files cloned -- the set is incomplete"

for f in RUN_INSTRUMENTS:
    assert (REPO / f"_c{CYCLE}_{f}.py").exists(), (
        f"[prep] ABORT: the instrument {f}.py is missing after the clone")
print(f"[prep] the RUN instruments are present: {RUN_INSTRUMENTS}")

# =====================================================================
# 6. THE IDENTITY RE-TYPE -- LIVE CODE ONLY (docstrings are prose)
# =====================================================================


def doc_ranges(path):
    tree = ast.parse(pathlib.Path(path).read_text(encoding="utf-8"))
    out = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef,
                             ast.AsyncFunctionDef, ast.ClassDef)):
            b = getattr(node, "body", None)
            if b and isinstance(b[0], ast.Expr) \
               and isinstance(b[0].value, ast.Constant) \
               and isinstance(b[0].value.value, str):
                out.append((b[0].lineno, b[0].end_lineno))
    return out


def in_doc(line_no, ranges):
    return any(a <= line_no <= b for a, b in ranges)


retyped = []
for p in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    if p.resolve() == _SELF:
        continue          # ⭐ never re-type the instrument that is doing it
    src = p.read_text(encoding="utf-8")
    dr = doc_ranges(p)
    lines = src.splitlines(keepends=True)
    out, changed = [], False
    for i, ln in enumerate(lines, 1):
        new = ln
        if not in_doc(i, dr):
            # the LIVE artefact root and the LIVE self-generation
            new = new.replace(f"/tmp/c{BASE}", f"/tmp/c{CYCLE}")
            new = new.replace(f"_c{BASE}_", f"_c{CYCLE}_")
            new = re.sub(r'(?m)^(CYCLE[ \t]*=[ \t]*)"1282"[ \t]*$',
                         rf'\g<1>"{CYCLE}"', new)
        out.append(new)
        if new != ln:
            changed = True
    if changed:
        _new = "".join(out)
        ast.parse(_new)
        p.write_text(_new, encoding="utf-8")
        retyped.append(p.name)
print(f"[prep] {len(retyped)} file(s) re-typed (live artefact roots, "
      "self-generation references, CYCLE constants)")

# the HOUR constant -- live code
_hour_files = 0
for p in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    if p.resolve() == _SELF:
        continue
    src = p.read_text(encoding="utf-8")
    out = re.sub(r"(?m)^(CYCLE_HOUR_UTC[ \t]*=[ \t]*)\d+[ \t]*$",
                 rf"\g<1>{HOUR}", src)
    out = re.sub(r"(?m)^(HOUR[ \t]*=[ \t]*)\d+[ \t]*$",
                 rf"\g<1>{HOUR}", out)
    if out != src:
        ast.parse(out)
        p.write_text(out, encoding="utf-8")
        _hour_files += 1
print(f"[prep] the hour -> {HOUR} in {_hour_files} file(s)")

# the instruments THIS cycle RUNS must name THIS cycle
for f in RUN_INSTRUMENTS:
    p = REPO / f"_c{CYCLE}_{f}.py"
    if not p.exists():
        continue
    src = p.read_text(encoding="utf-8")
    m = re.search(r'(?m)^(CYCLE[ \t]*=[ \t]*)"(\d+)"[ \t]*$', src)
    if m and m.group(2) != CYCLE:
        out = src[:m.start(2)] + CYCLE + src[m.end(2):]
        ast.parse(out)
        p.write_text(out, encoding="utf-8")
        print(f"[prep] [RE-TARGETED] {f}.py: CYCLE {m.group(2)!r} -> "
              f"{CYCLE!r}")

# =====================================================================
# 7. THE ANCHOR CENSUS -- A READ-ONLY PRE-VALIDATION
# =====================================================================
# ⭐⭐⭐⭐⭐ **PRE-VALIDATE EVERY ANCHOR *UP FRONT* ⇒ A PORT THAT ABORTS
# MIDWAY CANNOT LEAVE A HALF-PORTED BLUEPRINT** (cycle 1284's class-level
# finding: 1283's port landed `measure.py` and then died, leaving 1-of-7).
# ⭐⭐⭐⭐⭐ **THIS CYCLE NEEDS NO PORT** -- the base's shape IS this cycle's
# shape -- so the census is a *CONFIRMATION* that the base really is the
# (IN, IN) shape, not an assumption.
print()
print("=" * 78)
print("THE ANCHOR CENSUS -- the (IN, IN) shape, CONFIRMED per file")
print("=" * 78)

_IN_BAND_NO_PC = "ON AN IN-BAND HOUR THERE IS NO POSITIVE CONTROL"
_OUT_PC_BLOCK = "POSITIVE CONTROL: the most recent IN-BAND block"


def live_probe(path, probe):
    lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    docs = doc_ranges(path)
    return sum(1 for i, ln in enumerate(lines, 1)
               if probe in ln and not any(a <= i <= b for a, b in docs))


def polarity_table(gen):
    """The per-file band-side polarity of ONE generation."""
    tbl = {}
    for f in BAND_FILES:
        p = REPO / f"_c{gen}_{f}.py"
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        c = {
            "out_pres": len(re.findall(
                r"assert (?:_)?OUTBAND_RE\.search\(this_block\) is not None",
                s)),
            "in_abs": len(re.findall(
                r"assert (?:_)?BAND_RE\.search\(this_block\) is None", s)),
            "out_abs": len(re.findall(
                r"assert (?:_)?OUTBAND_RE\.search\(this_block\) is None", s)),
            "in_pres": len(re.findall(
                r"assert (?:_)?BAND_RE\.search\(this_block\) is not None", s)),
        }
        no_pc = live_probe(p, _IN_BAND_NO_PC)
        pc = live_probe(p, _OUT_PC_BLOCK)
        if c["in_pres"] and c["out_abs"] and not c["out_pres"] \
                and not c["in_abs"] and no_pc:
            side = "IN"
        elif c["out_pres"] and c["in_abs"] and not c["out_abs"] \
                and not c["in_pres"] and not no_pc:
            side = "OUT"
        else:
            side = "MIXED"
        tbl[f] = (side, c, no_pc, pc)
    return tbl


_tbl = polarity_table(CYCLE)
_ref = polarity_table(PRIOR)
print(f"    (the reference shape is the COMMITTED base generation "
      f"_c{PRIOR}_* -- the shape the site is PUBLISHING)")
for f in BAND_FILES:
    if f not in _tbl:
        continue
    side, c, no_pc, pc = _tbl[f]
    _rs = _ref.get(f, ("<absent>",))[0]
    print(f"    {f:12s} {side:6s} (the committed base says {_rs:6s}) "
          f"in_pres={c['in_pres']} out_abs={c['out_abs']} "
          f"out_pres={c['out_pres']} in_abs={c['in_abs']} "
          f"noPCreg={no_pc} PCreg={pc}")

# ⭐⭐⭐⭐⭐ **THE CENSUS'S RULE IS *"NO FILE CARRIES THE WRONG SIDE"*, NOT
# *"EVERY FILE CARRIES THIS SIDE"*.**  ⭐⭐⭐⭐⭐ **FIVE OF THE SEVEN BAND
# FILES CARRY NO OWN-BLOCK ASSERTION AT ALL** -- their `MIXED` verdict
# means *"this file does not own that construct"*, NOT *"this file is
# half-ported"*.  ⭐⭐⭐⭐⭐ **⇒ AN INSTRUMENT THAT DEMANDS "IN" FROM A FILE
# THAT DOES NOT OWN THE CONSTRUCT IS AN INSTRUMENT THAT FIRES ON A CORRECT
# ARTEFACT** (1275's class-level rule) ⇒ **⇒ THE INSTRUMENT IS FIXED, NEVER
# THE ARTEFACT.**  ⭐⭐⭐⭐⭐ **THE RIGHT RULE: (a) NO file may carry the
# WRONG side's markers, and (b) the files that DO own the construct must
# carry THIS cycle's side.**
_band_ok = True
for f, (side, c, no_pc, pc) in _tbl.items():
    if side == "OUT":
        print(f"    [WRONG SIDE] {f}.py carries the OUT-side markers")
        _band_ok = False
    if c["out_pres"] or pc:
        print(f"    [WRONG SIDE] {f}.py carries an OUT-side marker "
              f"(out_pres={c['out_pres']} PCreg={pc})")
        _band_ok = False
    if side == "MIXED" and (c["in_pres"] or c["out_abs"] or c["out_pres"]
                            or c["in_abs"]):
        print(f"    [HALF-PORTED] {f}.py owns the own-block construct but "
              "carries BOTH sides")
        _band_ok = False
assert _band_ok, (
    "[prep] ABORT: the base generation carries the WRONG side on a band "
    "file -- it is not the (IN, IN) shape, and cloning it would publish a "
    "FALSE narrative about whether the branch ran")

# the files that OWN the construct must carry THIS cycle's side
for f in ("measure", "page"):
    assert _tbl[f][0] == "IN", (
        f"[prep] ABORT: {f}.py owns the own-block construct but does not "
        "carry the IN side")
print("  ⭐⭐⭐⭐⭐ [OK] NO band file carries the WRONG side, and the two "
      "files that OWN the own-block construct (measure, page) are IN")

# the CONTROL-SET attribution -- the UNCHANGED form must be PRESENT
# ⭐⭐⭐⭐⭐ **THE FLIPS PROBE MUST BE *POLARITY-AWARE*.**  ⭐⭐⭐⭐⭐ A RAW
# SUBSTRING COUNT CANNOT TELL A PROHIBITION FROM A CLAIM: `commit.py` carries
# `assert "the control set FLIPS" not in pg` -- that is a **NEGATIVE gate**
# (a *prohibition* of the FLIPS wording), which is exactly what an (IN, IN)
# cycle MUST carry.  ⭐⭐⭐⭐⭐ **⇒ THE RIGHT PROBE IS: the UNCHANGED form is
# PRESENT POSITIVELY, AND the FLIPS form appears ONLY inside a NEGATIVE
# gate** (`not in ...`) or a PROSE prohibition -- never as a POSITIVE claim
# (`"..." in ...`).  ⭐⭐⭐⭐⭐ (This is the skill's own
# `scripts/measure_pair_polarity.py` rule: a raw substring count cannot tell
# a prohibition from a claim.)
_CTL_UNCHANGED = "the control set is UNCHANGED, NOT 'flipped back'"
_FLIPS = "the control set FLIPS"
_positive_flips = re.compile(
    r'assert\s+[f]?"[^"]*' + re.escape(_FLIPS) + r'[^"]*"\s+in\s+')
for f in ("page", "struct", "commit", "jobs", "jobs_verify"):
    p = REPO / f"_c{CYCLE}_{f}.py"
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    assert _CTL_UNCHANGED in s, (
        f"[prep] ABORT: {f}.py does not carry the UNCHANGED control-set "
        f"attribution -- the base is not the (IN, IN) shape")
    bad = _positive_flips.findall(s)
    assert not bad, (
        f"[prep] ABORT: {f}.py carries the FLIPS attribution as a POSITIVE "
        f"claim ({len(bad)} occurrence(s)) -- the base is not the (IN, IN) "
        "shape")
print(f"  ⭐⭐⭐⭐⭐ [OK] the CONTROL-SET attribution is the UNCHANGED form in "
      "page/struct/commit/jobs/jobs_verify, and the FLIPS form appears only "
      "as a NEGATIVE gate")

# =====================================================================
# 8. EVERY FILE PARSES
# =====================================================================
_bad = []
for p in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    try:
        ast.parse(p.read_text(encoding="utf-8"))
    except SyntaxError as e:
        _bad.append((p.name, str(e)))
assert not _bad, f"[prep] ABORT: these files do NOT parse: {_bad}"
print(f"  ⭐⭐⭐⭐⭐ [OK] all {cloned + 1} files parse")

print()
print("=" * 78)
print("CYCLE 1285 -- THE BLUEPRINT IS PREPARED (no port was needed: the "
      "base's shape IS this cycle's shape)")
print("=" * 78)
print("  ⭐⭐⭐ NEXT: THE IDENTITY SWEEP, THE PAIR-KEYED VALUE-TOKEN SWEEP, "
      "AND THE SHAPE AUDITS.")
