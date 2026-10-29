#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1313 -- PREPARE THE BLUEPRINT.

⭐⭐⭐⭐⭐ **MECHANICALLY DERIVED FROM `_prep1312.py`** (the canonical
(OUT, OUT) prep) by replacing the TWO IDENTITY CONSTANTS (CYCLE, BASE) and
re-authoring the SELF-LABEL prose that names them.

⭐⭐⭐⭐⭐ **WHY CYCLE 1313.**  Cycle 1312 COMMITTED (`e470b2d`) and PUSHED
(debt measured = 0 0), and its five post-commit stages all PASSed ⇒ ⇒
**⇒ 1312 IS THE COMMITTED *AND PUBLISHED* BASE, AND IT IS THE (OUT, OUT)
SHAPE** ⇒ ⇒ **⇒ NO INTERRUPTED GENERATION HAS CONSUMED A NUMBER SINCE
1312** ⇒ ⇒ **⇒ 1313 IS THE NEXT CYCLE, WITH NO GAP TO ACCOUNT FOR.**
⭐⭐⭐⭐⭐ **⇒ AND THE BASE CARRIES CYCLE 1312's OWN REPAIR** -- the
RESET-FIRST push form (`["git", "-c", "credential.helper=", ...]`) ⇒ ⇒
**⇒ THAT REPAIR IS INHERITED BY CONSTRUCTION, NOT BY RE-TYPING.**

⭐⭐⭐⭐⭐ **THE BASE IS `_c1312_*` -- THE COMMITTED *AND PUBLISHED* BASE.**
Cycle 1312 was committed (`e470b2d`), PUSHED (push debt measured = 0 0),
and its five post-commit stages all PASSed ⇒ ⇒ **⇒ IT IS THE (OUT, OUT)
SHAPE AND IT CARRIES 1307's TWO REPAIRS *AND* 1312's RESET-FIRST PUSH
FORM** ⇒ ⇒ **⇒ THE BASE IS CHOSEN BY *(SHAPE, FIXES), NOT BY RECENCY.**

⭐⭐⭐⭐⭐ **⇒ NO SHAPE PORT IS NEEDED** -- this tick's hour is 02 (OUT) and
the prior COMMITTED cycle 1312's own hour is 01 (OUT) ⇒ ⇒ **⇒ THE PAIR IS
(OUT, OUT)** ⇒ ⇒ **⇒ THE CONTROL-SET PORT MUST NOT RUN** (running it would
publish a FALSE attribution about whether the control set flipped).
⭐⭐⭐⭐⭐ **⇒ AND THE HOUR IS *MEASURED*, NOT ASSERTED** -- the prep derives
it from THIS tick's OWN fetch.log block (the guard at step 2), so the "02"
above is a NARRATIVE ABOUT THE EXPECTED VALUE, not a constant the pipeline
depends on.  ⭐⭐⭐⭐⭐ **⇒ THE PREP ABORTS if the measured pair is anything
other than (OUT, OUT)** ⇒ ⇒ **⇒ IT CANNOT PUBLISH A FALSE ATTRIBUTION
ABOUT WHETHER THE CONTROL SET FLIPPED.**

⭐⭐⭐⭐⭐ **THE PREP IS SELF-CLEANING** -- a re-run deletes the whole
`_c1313_*` generation and re-clones.  ⭐⭐ **⇒ THE PREP MUST NOT BE RE-RUN
AFTER THE IDENTITY SWEEP** (the prep is self-cleaning ⇒ re-running it UNDOES
every port that ran after it).

⭐⭐⭐⭐⭐ **THIS FILE LIVES OUTSIDE THE `_cNNNN_*` GLOB ON PURPOSE** --
cycle 1297's lesson: a prep named `_cNNNN_prep.py` is CLONED BY ITSELF
(the clone writes `_cNNNN_prep.py` from the base's `_cNNNN_prep.py` while
the prep is still running) ⇒ ⇒ **⇒ THE RUNNING SCRIPT IS CLOBBERED
MID-RUN.**  The `_prepNNNN.py` convention avoids the glob entirely.

⭐⭐⭐⭐⭐ **THE IDENTITY RE-TYPE IS *LIVE CODE ONLY*** -- docstrings are
prose, and the identity sweep owns the prose (1282's rule: the CONSTANT and
the PROSE are TWO SURFACES).

⭐⭐⭐⭐⭐ **CYCLE 1307's ADDITION: THE STALE DOCSTRING HEAD IS *RE-AUTHORED*
BY THE PREP, NOT LEFT TO THE SWEEP.**  ⇒ ⇒ **⇒ THE PREP MUST RE-AUTHOR IT**
(1277's rule: a SELF-LABEL must be RE-AUTHORED, a CITATION must be
RE-MEASURED -- and this head is a SELF-LABEL).  ⭐⭐⭐⭐⭐ **⇒ AND THE FIX IS
*MEASURED*, NOT TYPED**: the head is rewritten to THIS cycle's number, and
the ASSERTION verifies the *rewritten* value on disk (rule D: the artefact
is re-read from disk).
"""
import ast
import pathlib
import re
import shutil
import subprocess

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
BASE = "1312"
CST_OFFSET = 8

BAND_FILES = ["measure", "page", "struct", "commit", "verify", "jobs",
              "jobs_verify"]
RUN_INSTRUMENTS = ["clone_sweep", "sweep_tokens", "docstring_shape"]

print("=" * 78)
print(f"CYCLE {CYCLE} -- PREPARE (clone from {BASE}, hour measured below)")
print("=" * 78)
_SELF = pathlib.Path(__file__).resolve()

# =====================================================================
# 0. THE INHERITED WORKTREE DELTA -- MEASURED, THEN RESTORED
# =====================================================================
print()
print("=" * 78)
print("0. THE INHERITED WORKTREE DELTA -- MEASURED, THEN RESTORED")
print("=" * 78)
_st = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"],
                      cwd=REPO, capture_output=True, text=True).stdout
_tracked = [ln for ln in _st.splitlines() if ln.strip()]
print(f"  [MEASURED] the inherited tracked-file delta = {_tracked}")
_rc2 = subprocess.run(
    ["git", "diff", "--numstat", "HEAD", "--", "tweets.json"], cwd=REPO,
    capture_output=True, text=True).stdout.strip()
print(f"  [MEASURED] tweets.json numstat against HEAD = {_rc2!r} "
      f"(EMPTY = byte-identical, so there is NO worktree-only record "
      f"liability this cycle)")
assert not _rc2, (
    f"[prep] ABORT: tweets.json differs from HEAD ({_rc2!r}) -- the "
    "worktree carries a worktree-only record delta, which is a LIABILITY "
    "and must be re-adjudicated as candidates, not inherited")
_rc3 = subprocess.run(
    ["git", "checkout", "--", "index.html", "deploy-stamp.txt"], cwd=REPO,
    capture_output=True, text=True)
assert _rc3.returncode == 0, f"[prep] the restore FAILED: {_rc3.stderr}"
_st2 = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"],
                      cwd=REPO, capture_output=True, text=True).stdout
assert not _st2.strip(), (
    f"[prep] the restore left tracked files dirty: {_st2!r}")
print("  [OK] the tracked files are byte-identical to HEAD again -- the "
      "inherited delta is DISCARDED, not inherited")

# =====================================================================
# 1. THE BAND -- DERIVED FROM SOURCE, NEVER TYPED
# =====================================================================
_ft = (REPO / "fetch_tweets.py").read_text(encoding="utf-8")
_bm = re.search(r"RETRY_TRANSLATION_HOURS\s*=\s*\{([^}]*)\}", _ft)
assert _bm, "[prep] could not read RETRY_TRANSLATION_HOURS from fetch_tweets.py"
_BAND = {int(x) for x in re.findall(r"\d+", _bm.group(1))}
print(f"  [MEASURED] source-derived RETRY_TRANSLATION_HOURS = {sorted(_BAND)}")

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
HOUR = (int(_m.group(2)) - CST_OFFSET) % 24

# ⭐⭐⭐⭐⭐ CYCLE 1309's ADDITION -- THE *STALE-PREFLIGHT* TRAP (cycle 1300's
# class: a stale pre-flight reading FALSIFIES THE HOUR).
# ⭐⭐⭐⭐⭐ THE FETCHER FIRES AT MINUTE :07 AND THE CRON TICK AT :00 ⇒ ⇒
# **⇒ BETWEEN :00 AND :07 THE LAST BLOCK IN fetch.log IS THE *PRIOR* HOUR's**
# ⇒ ⇒ **⇒ READING THE LAST BLOCK UNGUARDED MEASURES THE PRIOR HOUR** ⇒ ⇒
# **⇒ AND THE PRIOR HOUR IS IN THE BAND (21) WHILE THIS CYCLE'S HOUR IS NOT
# (22) ⇒ ⇒ **⇒ THE UNGUARDED READING WOULD SELECT THE WRONG SHAPE AND
# PUBLISH A FALSE NARRATIVE ABOUT WHETHER THE BRANCH RAN.**
# ⭐⭐⭐⭐⭐ **⇒ THE FIX IS A *GUARD*, NOT A WAIT INSIDE THE PREP**: the prep
# asserts that the last block's CST hour is THIS tick's own CST hour ⇒ ⇒ if
# the block has not landed yet, the prep ABORTS (and the caller waits) ⇒ ⇒
# **⇒ THE PREP CAN NEVER MEASURE A STALE HOUR.**
import datetime as _dt
_now_cst_hour = _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=CST_OFFSET))).hour
_last_cst_hour = int(_m.group(2))
assert _last_cst_hour == _now_cst_hour, (
    f"[prep] ABORT: the last fetch.log block is {_last!r} (CST hour "
    f"{_last_cst_hour}), but this tick's own CST hour is {_now_cst_hour} "
    "-- the fetcher fires at :07 and the tick at :00, so the LAST block is "
    "the PRIOR hour's until this tick's own block lands. **MEASURING IT "
    "WOULD FALSIFY THE HOUR** (cycle 1300's class). **WAIT FOR THIS TICK's "
    "OWN BLOCK AND RE-RUN.**")
print(f"  [OK] the last fetch.log block IS this tick's own block "
      f"(CST hour {_last_cst_hour} == now) -- the hour measurement is NOT "
      f"a STALE reading")
print(f"  [MEASURED] this tick's OWN fetch.log block = {_last!r} -> "
      f"UTC hour {HOUR}")
IN_BAND = HOUR in _BAND
print(f"  [MEASURED] hour {HOUR} -> {'IN' if IN_BAND else 'OUT'} OF BAND")

# ⭐⭐⭐⭐⭐ **THE BLOCK MUST CARRY THE MARKER FOR *THIS* HOUR'S SIDE.**  On
# an IN-BAND hour the block carries the ⏰ marker AND the guard's SKIPPED
# line; on an OUT-OF-BAND hour it carries NEITHER.  ⭐⭐⭐⭐⭐ **⇒ THIS IS
# THE MEASUREMENT THAT PROVES THE HOUR'S SIDE IS NOT ASSUMED** -- and it is
# checked against the block's OWN header, not against a typed string.
_block = _log.split(_last, 1)[1][:1200]
_in_marker = f"Hour {HOUR:02d} UTC — running empty-translation retry pass"
_out_marker = f"Hour {HOUR:02d} UTC — skipping retry pass"
if IN_BAND:
    assert _in_marker in _block, (
        f"[prep] ABORT: hour {HOUR} is in the band, but this tick's own "
        f"block does not carry the IN-BAND marker {_in_marker!r} -- the "
        "hour's side is NOT what the band says")
    print(f"  [MEASURED] the tick's own block carries the IN-BAND marker (⏰)")
else:
    assert _out_marker in _block, (
        f"[prep] ABORT: hour {HOUR} is out of band, but this tick's own "
        f"block does not carry the OUT-OF-BAND marker {_out_marker!r}")
    assert _in_marker not in _block, (
        "[prep] ABORT: the tick's own block carries BOTH markers")
    print(f"  [MEASURED] the tick's own block carries the OUT-OF-BAND marker "
          f"(⏭️) and NEITHER the in-band marker NOR the guard's SKIPPED "
          f"line -- the branch NEVER RAN (a BLIND SPOT, not a pass)")

# =====================================================================
# 3. THE PRIOR COMMITTED CYCLE -- MEASURED FROM HEAD
# =====================================================================
_head_subject = subprocess.run(
    ["git", "log", "-1", "--format=%s", "--", "index.html"], cwd=REPO,
    capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\d+)", _head_subject)
assert _pm, f"[prep] could not read the prior cycle from {_head_subject!r}"
PRIOR = _pm.group(1)
print(f"  [MEASURED] prior COMMITTED cycle = {PRIOR}")
_pg = subprocess.run(["git", "show", "HEAD:index.html"], cwd=REPO,
                     capture_output=True, text=True).stdout
_cmt = re.search(r"<!--\s*cron cycle (\d+):(.*?)-->", _pg, re.S)
assert _cmt and _cmt.group(1) == PRIOR, (
    "[prep] HEAD's page and its publishing commit disagree on the cycle")
_hm = re.search(r"=\s*Hour (\d{1,2}) UTC", _cmt.group(2))
assert _hm, "[prep] HEAD's cycle comment carries no `= Hour NN UTC`"
PRIOR_HOUR = int(_hm.group(1))
PRIOR_IN = PRIOR_HOUR in _BAND
print(f"  [MEASURED] prior COMMITTED cycle = {PRIOR}, hour = {PRIOR_HOUR} "
      f"-> {'IN' if PRIOR_IN else 'OUT'} OF BAND")
FLIPS = IN_BAND != PRIOR_IN
print(f"  ⭐⭐⭐⭐⭐ [MEASURED] THE PAIR = "
      f"({'IN' if IN_BAND else 'OUT'}, {'IN' if PRIOR_IN else 'OUT'}) => "
      f"the control set {'FLIPS' if FLIPS else 'is UNCHANGED'}")

# ⭐⭐⭐⭐⭐ **THE PAIR ASSERTION IS *MEASURED*, AND THE *BASE* IS CHOSEN BY
# THE MEASURED PAIR.**  The base `_c{BASE}_*` is the (OUT, OUT) shape ⇒ ⇒
# **⇒ IF the measured pair is (OUT, OUT), THE BASE'S SHAPE IS THIS CYCLE'S
# SHAPE ⇒ ⇒ **⇒ NO SHAPE PORT IS NEEDED AND THE CONTROL-SET PORT MUST NOT
# RUN.**  ⭐⭐⭐⭐⭐ IF the pair is anything else, the prep MUST ABORT --
# because the port source would have to be MEASURED, and that is a
# different cycle's work (1287's class-level rule).
if FLIPS:
    print(f"  ⛔ [prep] the measured pair FLIPS -- the (OUT, OUT) base is "
          f"the WRONG shape and a MEASURED port source is required.  "
          f"ABORTING (the port is a separate, measured step).")
    raise SystemExit(2)
print("  ⭐⭐⭐⭐⭐ [OK] the measured pair is (OUT, OUT) -- the base's shape "
      "IS this cycle's shape; NO shape port is needed and the control-set "
      "port MUST NOT run")

# ⭐⭐⭐⭐⭐ **THE PUSH DEBT MUST BE 0** -- the base must be PUBLISHED, not
# just committed (1304's lesson: a commit that exists locally but was never
# pushed is not a base, it is a liability).
_ahead = subprocess.run(
    ["git", "rev-list", "--left-right", "--count", "origin/main...HEAD"],
    cwd=REPO, capture_output=True, text=True).stdout.strip()
print(f"  [MEASURED] push debt (origin/main...HEAD) = {_ahead!r}")
assert _ahead.split() == ["0", "0"], (
    f"[prep] ABORT: the push debt is {_ahead!r} -- the base is NOT "
    "published; a commit that exists locally but was never pushed is a "
    "LIABILITY, not a base")
print("  ⭐⭐⭐⭐⭐ [OK] the base is PUBLISHED (push debt = 0 0)")

# =====================================================================
# 4. A CLEAN SLATE -- the previous partial run's artefacts are discarded
# =====================================================================
for _p in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    _p.unlink()
print(f"[prep] the stale _c{CYCLE}_* artefacts were discarded (a clean "
      f"slate -- the previous partial run's files are not trusted)")

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
# 6. THE IDENTITY RE-TYPE -- LIVE CODE ONLY
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
    src = p.read_text(encoding="utf-8")
    dr = doc_ranges(p)
    lines = src.splitlines(keepends=True)
    out, changed = [], False
    for i, ln in enumerate(lines, 1):
        new = ln
        if not in_doc(i, dr):
            new = new.replace(f"/tmp/c{BASE}", f"/tmp/c{CYCLE}")
            new = new.replace(f"_c{BASE}_", f"_c{CYCLE}_")
            new = re.sub(rf'(?m)^(CYCLE[ \t]*=[ \t]*)"{BASE}"[ \t]*$',
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
      f"self-generation references, CYCLE constants)")

# the HOUR constant -- live code
_hour_files = 0
for p in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    src = p.read_text(encoding="utf-8")
    out = re.sub(r"(?m)^(CYCLE_HOUR_UTC[ \t]*=[ \t]*)\d+([ \t]*(?:#.*)?)$",
                 rf"\g<1>{HOUR}\g<2>", src)
    # ⭐⭐⭐⭐⭐ THE TRAILING-COMMENT FORM IS *ALSO* RE-TYPED (1289's rule:
    # `PRIOR = "1278"  # comment` does not end at the literal ⇒ a regex
    # anchored at `$` SILENTLY MATCHES NOTHING).  ⭐⭐⭐⭐⭐ ONLY THE NUMBER
    # IS REPLACED -- the comment is left VERBATIM, because the comment is a
    # NARRATIVE about the hour and it is the PROSE's business (the sweep's).
    out = re.sub(r"(?m)^(HOUR[ \t]*=[ \t]*)\d+([ \t]*(?:#.*)?)$",
                 rf"\g<1>{HOUR}\g<2>", out)
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

# ⭐⭐⭐⭐⭐ **THE PRIOR-COMMITTED-CYCLE CONSTANT.**  ⭐⭐⭐⭐⭐ This is a LIVE
# constant (not prose) ⇒ ⇒ **⇒ THE PREP RE-TYPES IT TO THE MEASURED
# PRIOR** ⇒ ⇒ **⇒ AND THE IDENTITY SWEEP MUST NOT RE-TYPE IT TO *THIS*
# CYCLE** (that would name the cycle itself as its own predecessor).
for p in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    src = p.read_text(encoding="utf-8")
    out = re.sub(r'(?m)^(PRIOR_CYCLE[ \t]*=[ \t]*)"1[0-9]{3}"[ \t]*$',
                 rf'\g<1>"{PRIOR}"', src)
    if out != src:
        ast.parse(out)
        p.write_text(out, encoding="utf-8")
        print(f"[prep] [PRIOR] {p.name}: PRIOR_CYCLE -> {PRIOR!r}")

# =====================================================================
# 6b. THE STALE DOCSTRING HEAD -- RE-AUTHORED (1277's class)
# =====================================================================
print()
print("=" * 78)
print("6b. THE STALE DOCSTRING HEAD -- RE-AUTHORED (a docstring is a "
      "PUBLICATION)")
print("=" * 78)
_HEAD_RE = re.compile(r'(?m)^(\s*""")Cycle\s+(\d{3,4})\s+--')
_heads = []
for p in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    src = p.read_text(encoding="utf-8")
    m = _HEAD_RE.search(src)
    if not m:
        continue
    old = m.group(2)
    if old == CYCLE:
        continue
    # ⭐⭐⭐⭐⭐ THE FIX IS *MINIMAL AND IN-PLACE*: edit ONLY the captured
    # cycle number -- the closing delimiter is on a DIFFERENT line, so a
    # line-scoped edit cannot destroy the docstring (1283's rule (d)).
    out = src[:m.start(2)] + CYCLE + src[m.end(2):]
    ast.parse(out)
    p.write_text(out, encoding="utf-8")
    _heads.append((p.name, old))
print(f"  [RE-AUTHORED] {len(_heads)} docstring head(s): {_heads}")
# ⭐⭐⭐⭐⭐ **⇒ THE FIX IS VERIFIED *BY RE-READING THE ARTEFACT FROM DISK***
# (rule D: the only proof of a write is the artefact, re-read).
_bad_heads = []
for p in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    src = p.read_text(encoding="utf-8")
    m = _HEAD_RE.search(src)
    if m and m.group(2) != CYCLE:
        _bad_heads.append((p.name, m.group(2)))
assert not _bad_heads, (
    f"[prep] ABORT: a docstring head still names a stale cycle: "
    f"{_bad_heads}")
print(f"  ⭐⭐⭐⭐⭐ [OK] every module docstring head names cycle {CYCLE} "
      f"(re-read from disk)")

# =====================================================================
# 7. EVERY CLONED FILE PARSES
# =====================================================================
print()
print("=" * 78)
print("EVERY CLONED FILE PARSES")
print("=" * 78)
bad = []
for p in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    try:
        ast.parse(p.read_text(encoding="utf-8"))
    except SyntaxError as e:
        bad.append((p.name, str(e)))
assert not bad, f"[prep] these cloned files do NOT parse: {bad}"
print(f"  [OK] all {len(list(REPO.glob(f'_c{CYCLE}_*.py')))} files parse")

# =====================================================================
# 8. THE BASE's FIXES ARE PRESENT (MEASURED, NOT ASSUMED)
# =====================================================================
print()
print("=" * 78)
print("THE BASE's FIXES ARE PRESENT (MEASURED)")
print("=" * 78)
REQUIRED = [
    ("page.py", 'assert f"Hour {CYCLE_HOUR_UTC} UTC: {CYCLE_CLASS}"',
     "the BRANCH-SYMMETRIC class gate (1275)"),
    ("page.py", "PAGE ROTATION.",
     "1276's SHAPE-NEUTRAL page docstring"),
    ("struct.py", "WHICH SHAPE APPLIES IS",
     "1277's SHAPE-NEUTRAL struct docstring"),
    ("jobs.py", "NOTE'S BRANCH IS DERIVED",
     "1277's SHAPE-NEUTRAL jobs docstring"),
    ("commit.py", "_BNEW_VERB",
     "the GRAMMAR fix (one is / ones are)"),
    ("commit.py", '"defects"',
     "the machine-readable precert field"),
    ("commit.py", "BRAND-NEW one is",
     "the GRAMMAR fix, applied"),
    ("build.py", "_assert_delta_is_a_pure_addition",
     "1295's DEAD-WRITE-BLOCK repair (the write block is live again)"),
    ("measure.py", "the COUNT of big gaps is REPORTED, never asserted",
     "1297's HARD-CODED-COUNT repair (the count is a MEASUREMENT)"),
    # ⭐⭐⭐⭐⭐ CYCLE 1307's TWO REPAIRS -- THEY MUST TRAVEL INTO 1313.
    ("page.py", "CYCLE 1307's REPAIR: THE TWO SETS HAVE DIFFERENT "
                "DENOMINATORS",
     "1307's RULE-Q repair (the set-relationship gate)"),
    ("page.py", "_mine_new = [r for r in _mine",
     "1307's RULE-Q repair, applied"),
    ("commit.py", "RULE O (cycle 1307): THE PUSH IS AN *ARGUMENT LIST*",
     "1307's RULE-O repair (the argument-list push)"),
    # ⭐⭐⭐⭐⭐ THE OLD (APPEND-ONLY) PUSH FORM IS *RETIRED AS A REQUIRED
    # PROBE* -- CYCLE 1312's REPAIR *SUPERSEDED* IT (the form is now
    # `["git", "-c", "credential.helper=", ...]`).  ⭐⭐⭐⭐⭐ A REQUIRED probe
    # that demands a form the base DELIBERATELY NO LONGER CARRIES is a
    # STALE POSITIVE GATE -- it fires on a perfectly correct base ⇒ ⇒
    # ⇒ **⇒ THE INVARIANT IS CARRIED BY THE NEGATIVE GATE BELOW** (the old
    # form must be ABSENT), which is the gate that actually encodes 1312's
    # repair ⇒ ⇒ and the POSITIVE gate now demands the REPAIRED form.
    ("commit.py", '["git", "-c", "credential.helper=",',
     "1312's RULE-O-3 repair (the reset-first push form)"),
    ("commit.py", '-c", f"credential.helper={_HELPER}", "push", "origin", "HEAD"]',
     "1312's RULE-O-3 repair, applied"),
    # ⭐⭐⭐⭐⭐ CYCLE 1312's REPAIR -- THE RESET-FIRST PUSH FORM MUST TRAVEL
    # INTO 1313.  ⭐⭐⭐⭐⭐ MEASURED at 1312: `-c credential.helper=<H>`
    # APPENDS to the inherited list, git consults helpers IN ORDER and stops
    # at the first that answers, and `osxkeychain` is FIRST ⇒ ⇒ the custom
    # helper is NEVER invoked ⇒ ⇒ a GUI `SecurityAgent` prompt that no cron
    # session can approve ⇒ ⇒ THE PUSH HANGS (measured live: 600 s, and a
    # `SecurityAgent` orphan alive for 23 h).  ⭐⭐⭐⭐⭐ ⇒ AN EMPTY
    # `credential.helper` RESETS THE LIST ⇒ ⇒ AND THE RESET MUST COME
    # **FIRST** ⇒ ⇒ the push lands in ~2 s (MEASURED).
]
for fname, probe, why in REQUIRED:
    fp = REPO / f"_c{CYCLE}_{fname}"
    assert fp.exists(), f"[prep] ABORT: {fp.name} does not exist"
    ok = probe in fp.read_text(encoding="utf-8")
    assert ok, (
        f"[prep] ABORT: {fp.name} does NOT carry {why} (probe {probe!r}) -- "
        "the base does not own it, so it must be ported as its own step")
    print(f"  [OK] {fname:<12} {why}")

# =====================================================================
# 9. THE BASE's SHAPE IS THIS CYCLE's SHAPE -- CONFIRMED BY CENSUS
# =====================================================================
print()
print("=" * 78)
print("THE BASE's SHAPE IS THIS CYCLE's SHAPE -- CONFIRMED BY CENSUS")
print("=" * 78)
_IN_BAND_NO_PC = "ON AN IN-BAND HOUR THERE IS NO POSITIVE CONTROL"
_OUT_PC_BLOCK = "POSITIVE CONTROL: the most recent IN-BAND block"


def live_probe(path, probe):
    lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    docs = doc_ranges(path)
    return sum(1 for i, ln in enumerate(lines, 1)
               if probe in ln and not any(a <= i <= b for a, b in docs))


def polarity_table(gen):
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
_ref = polarity_table(BASE)
# ⭐⭐⭐⭐⭐ **THE WRONG-SIDE RULE IS *PAIR-AWARE*.**  A file that carries
# the OUT side's markers is CORRECT on an OUT-of-band hour and WRONG on an
# IN-of-band hour.  ⭐⭐⭐⭐⭐ **⇒ THE CHECK MUST ASK "does any band file
# carry the side THIS cycle is NOT on?"** -- not "does any band file carry
# the OUT side?".  (An instrument that demands a fixed side fires on a
# correct artefact -- 1275's class-level rule.)
_THIS_SIDE = "IN" if IN_BAND else "OUT"
_OTHER_SIDE = "OUT" if IN_BAND else "IN"
print(f"  ⭐ this cycle's side is {_THIS_SIDE} (measured); the forbidden "
      f"side is {_OTHER_SIDE}")
_band_ok = True
print(f"    (the reference shape is the base generation _c{BASE}_*)")
for f in BAND_FILES:
    if f not in _tbl:
        continue
    side, c, no_pc, pc = _tbl[f]
    _rs = _ref.get(f, ("<absent>",))[0]
    print(f"    {f:12s} {side:6s} (the base says {_rs:6s}) "
          f"in_pres={c['in_pres']} out_abs={c['out_abs']} "
          f"out_pres={c['out_pres']} in_abs={c['in_abs']} "
          f"noPCreg={no_pc} PCreg={pc}")

# ⭐⭐⭐⭐⭐ **THE MARKER GROUPING IS BY *WHICH SIDE IT ASSERTS*, NOT BY
# WHICH MARKER IT NAMES.**  ⭐⭐⭐⭐⭐ `assert BAND_RE... is None`
# (`in_abs`) *PROHIBITS* the IN marker -- so it is an **OUT-side**
# assertion, not an IN-side one.  ⭐⭐⭐⭐⭐ The OUT side owns
# {out_pres, in_abs, PCreg}; the IN side owns {in_pres, out_abs, noPCreg}.
_OUT_MARKERS = ("out_pres", "in_abs")
_IN_MARKERS = ("in_pres", "out_abs")
for f, (side, c, no_pc, pc) in _tbl.items():
    _marks = _OUT_MARKERS if _OTHER_SIDE == "OUT" else _IN_MARKERS
    _carries_other = any(c[k] for k in _marks)
    _forbidden_pc = pc if _OTHER_SIDE == "OUT" else no_pc
    if _carries_other or _forbidden_pc:
        print(f"    [WRONG SIDE] {f}.py carries the {_OTHER_SIDE}-side "
              f"markers (out_pres={c['out_pres']} in_pres={c['in_pres']} "
              f"in_abs={c['in_abs']} out_abs={c['out_abs']} "
              f"PCreg={pc} noPCreg={no_pc})")
        _band_ok = False
assert _band_ok, (
    "[prep] ABORT: the base generation carries the WRONG side on a band "
    "file -- it is not the (OUT, ...) shape, and cloning it would publish a "
    "FALSE narrative about whether the branch ran")
for f in ("measure", "page"):
    assert _tbl[f][0] == _THIS_SIDE, (
        f"[prep] ABORT: {f}.py owns the own-block construct but does not "
        f"carry this cycle's side ({_THIS_SIDE})")
print(f"  ⭐⭐⭐⭐⭐ [OK] NO band file carries the WRONG side, and the two "
      f"files that OWN the own-block construct (measure, page) are "
      f"{_THIS_SIDE}")

# the CONTROL-SET attribution -- the UNCHANGED form must be PRESENT
# ⭐⭐⭐⭐⭐ **THE FLIPS PROBE MUST BE *POLARITY-AWARE*.**  ⭐⭐⭐⭐⭐ A RAW
# SUBSTRING COUNT CANNOT TELL A PROHIBITION FROM A CLAIM: `commit.py` carries
# `assert "the control set FLIPS" not in pg` -- that is a **NEGATIVE gate**
# (a *prohibition* of the FLIPS wording), which is exactly what an (OUT, OUT)
# cycle MUST carry.
_CTL_UNCHANGED = "the control set is UNCHANGED"
_positive_flips = re.compile(
    r'assert\s+[f]?"[^"]*the control set FLIPS[^"]*"\s+in\s+')
for f in ("page", "struct", "commit", "jobs", "jobs_verify"):
    p = REPO / f"_c{CYCLE}_{f}.py"
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    assert _CTL_UNCHANGED in s, (
        f"[prep] ABORT: {f}.py does not carry the UNCHANGED control-set "
        "attribution -- the base is not the (OUT, OUT) shape")
    bad_f = _positive_flips.findall(s)
    assert not bad_f, (
        f"[prep] ABORT: {f}.py carries the FLIPS attribution as a POSITIVE "
        f"claim ({len(bad_f)} occurrence(s)) -- the base is not the (OUT, OUT) "
        "shape")
print("  ⭐⭐⭐⭐⭐ [OK] the CONTROL-SET attribution is the UNCHANGED form in "
      "page/struct/commit/jobs/jobs_verify, and the FLIPS form appears only "
      "as a NEGATIVE gate")

# ⭐⭐⭐⭐⭐ THE OLD (APPEND-ONLY) PUSH FORM MUST BE ABSENT FROM THE BASE.
# ⭐⭐⭐⭐⭐ This is a NEGATIVE gate on the BASE: a base that carries the
# append-only form would HANG at the push (measured live at 1312) ⇒ ⇒ and
# the hang is INVISIBLE until the 600 s watchdog fires ⇒ ⇒ **⇒ IT IS
# CHECKED HERE, WHERE IT COSTS NOTHING.**
_OLD_PUSH = ('["git", "-c", f"credential.helper={_HELPER}", "push", '
             '"origin", "HEAD"]')
for _f in ("commit",):
    _p = REPO / f"_c{BASE}_{_f}.py"
    if not _p.exists():
        continue
    _n = _p.read_text(encoding="utf-8").count(_OLD_PUSH)
    assert _n == 0, (
        f"[prep] ABORT: _c{BASE}_{_f}.py carries the OLD append-only push "
        f"form {_n} time(s) -- that form NEVER invokes the custom helper "
        "(osxkeychain answers first) and the push WILL hang")
    print(f"  [OK] {_f}.py carries NO old append-only push form (the "
          "RESET-FIRST form is the only one)")

# =====================================================================
# 10. THE STALE-PROSE CENSUS -- the sweep's OWN resolution set
# =====================================================================
print()
print("=" * 78)
print("10. THE STALE-PROSE CENSUS (the sweep's OWN resolution set)")
print("=" * 78)
_PROSE_HOUR_RES = [
    re.compile(r"\bCYCLE\s+1[0-9]{3}\s+IS\s+HOUR\s+(\d{1,2})\b"),
    re.compile(r"\bTHIS CYCLE \(HOUR\s+(\d{1,2})\s+UTC\)"),
    re.compile(r"\bHOUR\s+(\d{1,2})\s+UTC\s+IS\s+\*\*"),
    re.compile(r'"""Hour\s+(\d{1,2})\s+IS\s+'),
    re.compile(r"\bhour\s+(\d{1,2})\s+IS\s+IN BAND"),
]
_FIX_FILES = ["paths", "adjudicate", "payload", "translate", "select", "build",
              "write", "render", "render_posts", "triage", "band_firetest",
              "fidelity2", "third_instrument", "fetch_new", "d_keepcheck",
              "precert"]
_hours = set()
for f in BAND_FILES + _FIX_FILES:
    p = REPO / f"_c{CYCLE}_{f}.py"
    if not p.exists():
        continue
    txt = p.read_text(encoding="utf-8")
    for rx in _PROSE_HOUR_RES:
        for mm in rx.finditer(txt):
            _hours.add(int(mm.group(1)))
# ⭐⭐⭐⭐⭐ THE GATE IS *"EXACTLY ONE HOUR"* -- the sweep's resolution must
# be UNAMBIGUOUS, or the sweep ABORTS on a perfectly correct artefact.
assert len(_hours) == 1, (
    f"[prep] ABORT: the prose's self-label hours are {sorted(_hours)} -- the "
    "identity sweep's resolution would be AMBIGUOUS (it measures OLD_HOUR "
    "from the prose), so it would ABORT on a perfectly correct artefact")
OLD_HOUR = next(iter(_hours))
print(f"  ⭐⭐⭐⭐⭐ [MEASURED] the prose resolves to EXACTLY ONE hour "
      f"(OLD_HOUR = {OLD_HOUR}) in the sweep's own resolution set -- the "
      f"sweep's resolution is UNAMBIGUOUS")

# ⭐⭐⭐⭐⭐ THE PROSE's HOUR MUST BE THE *BASE's* HOUR -- measured from the
# BASE generation's own prose, NOT typed.  ⇒ ⇒ **⇒ THIS IS WHAT MAKES THE
# SWEEP'S REWRITE CORRECT** (it rewrites the base's hour into this cycle's).
_base_hours = set()
for f in BAND_FILES + _FIX_FILES:
    p = REPO / f"_c{BASE}_{f}.py"
    if not p.exists():
        continue
    txt = p.read_text(encoding="utf-8")
    for rx in _PROSE_HOUR_RES:
        for mm in rx.finditer(txt):
            _base_hours.add(int(mm.group(1)))
assert _base_hours == {OLD_HOUR}, (
    f"[prep] ABORT: the base's prose hours are {sorted(_base_hours)} but the "
    f"clone's are {{{OLD_HOUR}}} -- the clone did not faithfully carry the "
    "base's prose, so the sweep would rewrite the WRONG hour")
print(f"  ⭐⭐⭐⭐⭐ [OK] the clone's prose hour == the base's prose hour "
      f"({OLD_HOUR}) -- the sweep will rewrite the RIGHT hour")

# ⭐⭐⭐⭐⭐ THE CONSTANT IS *REPORTED*, NOT *ASSERTED* -- the two surfaces
# are allowed to differ (that divergence is what the sweep repairs), so a
# gate here would fire on a correct artefact.
_const_m = re.search(r"(?m)^CYCLE_HOUR_UTC\s*=\s*(\d+)\s*$",
                     (REPO / f"_c{CYCLE}_measure.py").read_text(encoding="utf-8"))
print(f"  [REPORTED] the clone's measure.py CYCLE_HOUR_UTC constant = "
      f"{_const_m.group(1) if _const_m else '?'} (the prep re-types it to "
      f"{HOUR}); the PROSE still carries {OLD_HOUR} and the SWEEP owns the "
      f"prose rewrite")

# ⭐⭐⭐⭐⭐ **THE SELF-LABEL MUST RESOLVE TO *EXACTLY ONE* CYCLE** -- the
# sweep's PROSE_IDENTITY (the exemption's reference) is measured from it,
# so an AMBIGUITY there would make the sweep ABORT.
_self_labels = set()
for f in BAND_FILES + _FIX_FILES:
    p = REPO / f"_c{CYCLE}_{f}.py"
    if not p.exists():
        continue
    for mm in re.finditer(r"\bCYCLE\s+(\d{3,4})\s+IS\s+HOUR\s+(\d{1,2})",
                           p.read_text(encoding="utf-8")):
        _self_labels.add(mm.group(1))
assert len(_self_labels) == 1, (
    f"[prep] ABORT: the SELF-LABEL names {len(_self_labels)} different "
    f"cycles {sorted(_self_labels)} -- the sweep's PROSE_IDENTITY (the "
    "exemption's reference) would be AMBIGUOUS")
print(f"  ⭐⭐⭐⭐⭐ [OK] the SELF-LABEL resolves to EXACTLY ONE cycle "
      f"({next(iter(_self_labels))}) -- the sweep's PROSE_IDENTITY is "
      f"UNAMBIGUOUS")

print()
print("=" * 78)
print(f"CYCLE {CYCLE} -- THE BLUEPRINT IS PREPARED (no shape port is needed: "
      f"the base's shape IS this cycle's shape)")
print("=" * 78)
print(f"  ⭐⭐⭐ NEXT: THE IDENTITY SWEEP (`_c{CYCLE}_clone_sweep.py`), THE "
      f"PAIR-KEYED VALUE-TOKEN SWEEP, AND THE SHAPE AUDITS.")
print(f"  ⭐⭐⭐ THEN: the chain paths -> payload -> adjudicate -> precert -> "
      f"fetch_new -> ... -> jobs_verify.")
