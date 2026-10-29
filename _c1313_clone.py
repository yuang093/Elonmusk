#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- CLONE (from 1278) + THE HOUR PORT, for Hour215.

⭐⭐⭐⭐⭐ **THE PAIR IS (IN, IN) -- A PAIR THAT HAS NEVER BEEN EXERCISED IN
THIS WINDOW.**

  * THIS cycle      = Hour215  -> IN  (`RETRY_TRANSLATION_HOURS =
    {0,3,6,9,12,15,18,21}`, MEASURED from `fetch_tweets.py`)
  * PRIOR COMMITTED = cycle 1278 = Hour212 -> IN  (MEASURED from HEAD's
    committed page, not typed)

⇒ **THE CONTROL SET IS *UNCHANGED*, NOT FLIPPED BACK.**

⭐⭐⭐⭐⭐ **THE BASE IS 1278 -- THE NEWEST *COMMITTED* BLUEPRINT**
(`982f122` = cycle 1278).  ⭐⭐⭐⭐⭐ **1279's blueprint on disk is the
(OUT, OUT) shape AND WAS NEVER COMMITTED** ⇒ it is not a base, and its
half-finished control-set port must NOT be inherited.

⭐⭐⭐⭐⭐ **THE BASE IS LOAD-BEARING IN FIVE WAYS** (all MEASURED below):
  1. the BRANCH-SYMMETRIC class gate (`{CYCLE_CLASS}`, not a hard-coded
     `SUBSTANTIVE`) -- 1275's fix;
  2. 1276's SHAPE-NEUTRAL `page.py` docstring;
  3. 1277's SHAPE-NEUTRAL `struct.py` + `jobs.py` docstrings;
  4. 1278's TWO PROSE-PRINT FIXES (the band-narration print and the
     derived-count print must AGREE with their own asserts);
  5. the four-way provenance branch + the `_BNEW_VERB` grammar fix + the
     machine-readable `precert` field.

⭐⭐⭐⭐⭐ **⇒ THE SHAPE PORT MUST NOT RE-TYPE THE DOCSTRINGS** -- they are
PUBLISHER-scoped and they name NEITHER side.
"""
import ast
import pathlib
import re
import shutil
import subprocess

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
BASE = "1278"        # the newest COMMITTED blueprint
PRIOR = "1278"       # the prior COMMITTED cycle -- Hour 12 = IN BAND
HOUR = 2            # THIS cycle's hour -- IN BAND

print("=" * 78)
print(f"CYCLE {CYCLE} -- CLONE (from {BASE}) + THE HOUR PORT, Hour {HOUR} UTC")
print("=" * 78)
print(f"  this cycle              : hour {HOUR} UTC = IN BAND")
print(f"  prior COMMITTED cycle   : {PRIOR} = Hour 12 = IN BAND")
print("  => the band pair is (IN, IN) -> the control set is UNCHANGED, NOT "
      "'flipped back'")
print(f"  base                    : {BASE} (the newest COMMITTED blueprint)")

BAND_FILES = ["measure", "page", "struct", "commit", "verify", "jobs",
              "jobs_verify"]
FIX_FILES = ["paths", "adjudicate", "payload", "translate", "select", "build",
             "write", "render", "render_posts", "triage", "band_firetest",
             "fidelity2", "third_instrument", "fetch_new", "d_keepcheck",
             "precert"]
LEGACY = ["patch_measure"]
LEGACY_CARRY = ["patch_anchor", "patch_band", "patch_noop", "patch_literals"]
CARRY = ["patch_prose"]
EXTRA = ["measure_axes", "clone_sweep", "measure_stage_set"]
EXTRA_CARRY = ["fix_precert_consumer", "wrap_rescoring", "patch_commit_noop",
               "port_sweep_tokens", "fix_page_docstring", "docstring_shape",
               "fix_docstring_shape", "live_render_test"]

# =====================================================================
# 0. THE BAND -- DERIVED FROM SOURCE, NEVER TYPED
# =====================================================================
print()
print("=" * 78)
print("THE BAND -- DERIVED FROM SOURCE")
print("=" * 78)
_ft = (REPO / "fetch_tweets.py").read_text(encoding="utf-8")
_bm = re.search(r"RETRY_TRANSLATION_HOURS\s*=\s*\{([^}]*)\}", _ft)
assert _bm, "[clone] could not read RETRY_TRANSLATION_HOURS from fetch_tweets.py"
_BAND = {int(x) for x in re.findall(r"\d+", _bm.group(1))}
print(f"  [MEASURED] source-derived RETRY_TRANSLATION_HOURS = {sorted(_BAND)}")
assert HOUR in _BAND, (
    f"[clone] ABORT: hour {HOUR} is NOT in the band -- this cycle's shape "
    "would be the OUT shape, and the (IN, IN) pair would be wrong")
print(f"  [MEASURED] hour {HOUR} -> IN OF BAND")

# =====================================================================
# 1. THE COMPOSITE
# =====================================================================
print()
print("=" * 78)
print("THE COMPOSITE")
print("=" * 78)
cloned, missing = 0, []
for group in (BAND_FILES, FIX_FILES, LEGACY, LEGACY_CARRY, CARRY, EXTRA,
              EXTRA_CARRY):
    for f in group:
        s = REPO / f"_c{BASE}_{f}.py"
        if s.exists():
            shutil.copy2(s, REPO / f"_c{CYCLE}_{f}.py")
            cloned += 1
        else:
            missing.append(f)
print(f"[clone] {cloned} files cloned from {BASE}")
if missing:
    print(f"[clone] the base does NOT carry: {missing}")
assert cloned >= 20, f"[clone] only {cloned} files cloned -- the set is incomplete"

# ---- 1b. THE PRIOR COMMITTED CYCLE -- MEASURED FROM HEAD --------------
print()
print("=" * 78)
print("THE PRIOR COMMITTED CYCLE -- MEASURED FROM HEAD")
print("=" * 78)
_head_subject = subprocess.run(
    ["git", "log", "-1", "--format=%s", "--", "index.html"],
    cwd=REPO, capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\d+)", _head_subject)
assert _pm, f"[clone] could not read the prior cycle from {_head_subject!r}"
MEASURED_PRIOR = _pm.group(1)
assert MEASURED_PRIOR == PRIOR, (
    f"[clone] ABORT: the prior COMMITTED cycle is {MEASURED_PRIOR} (measured "
    f"from HEAD), not {PRIOR} (typed)")
print(f"  [OK] the prior COMMITTED cycle is {MEASURED_PRIOR} [MEASURED from "
      "HEAD's commit subject]")

# ---- 1c. THE PRIOR's HOUR IS MEASURED FROM HEAD's PAGE ---------------
_pg = subprocess.run(["git", "show", "HEAD:index.html"], cwd=REPO,
                     capture_output=True, text=True).stdout
_cmt = re.search(r"<!--\s*cron cycle (\d+):(.*?)-->", _pg, re.S)
assert _cmt, "[clone] could not read HEAD's cycle comment"
assert _cmt.group(1) == PRIOR, (
    f"[clone] HEAD's page names cycle {_cmt.group(1)} but the publishing "
    f"commit names {PRIOR} -- the two artefacts disagree")
_hm = re.search(r"=\s*Hour (\d{1,2}) UTC", _cmt.group(2))
assert _hm, "[clone] HEAD's cycle comment carries no `= Hour NN UTC`"
PRIOR_HOUR = int(_hm.group(1))
assert PRIOR_HOUR in _BAND, (
    f"[clone] ABORT: the prior cycle's measured hour {PRIOR_HOUR} is NOT in "
    "the band -- the pair is not (IN, IN)")
print(f"  [OK] the prior cycle's hour is {PRIOR_HOUR} [MEASURED from HEAD's "
      "committed page] -> IN BAND")
assert PRIOR_HOUR == 12, (
    f"[clone] ABORT: the prior hour measured {PRIOR_HOUR}, expected 12")
print("  ⭐⭐⭐⭐⭐ [OK] THE PAIR IS (IN, IN) -- MEASURED, NOT ASSUMED")

# =====================================================================
# 2. THE HOUR PORT
# =====================================================================
print()
print("=" * 78)
print("THE HOUR PORT -- the hour is RE-TYPED, never left at the base's")
print("=" * 78)
ported, already = [], []
for f in BAND_FILES + FIX_FILES + EXTRA:
    p = REPO / f"_c{CYCLE}_{f}.py"
    if not p.exists():
        continue
    src = p.read_text(encoding="utf-8")
    out = re.sub(r"(?m)^(CYCLE_HOUR_UTC\s*=\s*)\d+$", rf"\g<1>{HOUR}", src)
    out = re.sub(r"(?m)^(HOUR\s*=\s*)\d+$", rf"\g<1>{HOUR}", out)
    if out != src:
        p.write_text(out, encoding="utf-8")
        ported.append(f)
    else:
        already.append(f)
print(f"  [PORTED] the hour -> {HOUR} in: {ported}")
print(f"  [no typed hour] in: {already}")

# ---- 2b. MEASURE BACK FROM DISK -------------------------------------
print()
print("  [MEASURE BACK FROM DISK]")
mh = re.search(r"(?m)^CYCLE_HOUR_UTC\s*=\s*(\d+)\s*$",
               (REPO / f"_c{CYCLE}_measure.py").read_text(encoding="utf-8"))
assert mh, "[clone] the cloned measure.py carries no CYCLE_HOUR_UTC"
assert int(mh.group(1)) == HOUR, (
    f"[clone] ABORT: the cloned measure.py carries CYCLE_HOUR_UTC = "
    f"{mh.group(1)}, expected {HOUR}")
print(f"  [OK] _c{CYCLE}_measure.py carries CYCLE_HOUR_UTC = {mh.group(1)} "
      "(RE-READ FROM DISK)")

# =====================================================================
# 3. EVERY CLONED FILE PARSES
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
assert not bad, f"[clone] these cloned files do NOT parse: {bad}"
print(f"  [OK] all {len(list(REPO.glob(f'_c{CYCLE}_*.py')))} files parse")

# =====================================================================
# 4. THE BASE'S FIXES ARE PRESENT (MEASURED, NOT ASSUMED)
# =====================================================================
print()
print("=" * 78)
print("THE BASE'S FIXES ARE PRESENT (MEASURED)")
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
    ("commit.py", "_BNEW_VERB", "the GRAMMAR fix (one is / ones are)"),
    ("commit.py", '"defects"', "the machine-readable precert field"),
    ("commit.py", "BRAND-NEW one is", "the GRAMMAR fix, applied"),
]
for fname, probe, why in REQUIRED:
    fp = REPO / f"_c{CYCLE}_{fname}"
    assert fp.exists(), f"[clone] ABORT: {fp.name} does not exist"
    ok = probe in fp.read_text(encoding="utf-8")
    assert ok, (
        f"[clone] ABORT: {fp.name} does NOT carry {why} (probe {probe!r}) -- "
        "the base does not own it, so it must be ported as its own step")
    print(f"  [OK] {fname:<12} {why}")

print()
print("=" * 78)
print(f"CYCLE {CYCLE} -- THE CLONE IS COMPLETE AND THE HOUR IS PORTED")
print("=" * 78)
print("  ⭐⭐⭐ NEXT: THE (IN, IN) CONTROL-SET PORT "
      "(`_c1280_port_ctl.py`).")
print("  ⭐⭐⭐ THE SHAPE SOURCE IS _c1236_* (MEASURED by "
      "scripts/measure_pair_polarity.py).")
