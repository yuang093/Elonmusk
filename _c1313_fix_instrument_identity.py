#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- RE-TARGET THE LIVE INSTRUMENTS AT 1282, AND AUDIT THE
WHOLE BLUEPRINT FOR A STALE `CYCLE` CONSTANT.

⭐⭐⭐⭐⭐ **THE DEFECT: THE INSTRUMENTS THEMSELVES WERE NEVER SWEPT.**

The identity sweep's file set (`RUN_SET` + `ALL`) covers the **CHAIN
STAGES** and the one-shot patchers -- it does **NOT** cover the
**INSTRUMENTS** (the sweeps, the port scripts, the clone scripts).  ⇒
**⇒ THEIR `CYCLE` CONSTANTS WERE NEVER RE-TYPED**, and they kept pointing
at the generation they were copied from.

⭐⭐⭐⭐⭐ **⇒ THE CONSEQUENCE WAS A *SILENTLY STALE MEASUREMENT*:**
`_c1282_docstring_shape.py` carried `CYCLE = "1278"`, so it read
**`_c1278_measure.py`** -- the BASE generation -- and reported the BASE's
docstring defects as if they were THIS cycle's.  ⭐⭐⭐⭐⭐ **⇒ IT REPORTED
TWO "DEFECTS" THAT WERE NOT IN THIS CYCLE'S FILES AT ALL** (the files on
disk carry **zero** occurrences of the pattern it claimed to find).

⭐⭐⭐⭐⭐ **⇒ THE LESSON IS A GENERAL ONE: *AN INSTRUMENT'S OWN IDENTITY IS
PART OF ITS CONTRACT*.**  A sweep that reads `_c{CYCLE}_*.py` is only
measuring THIS cycle's artefacts if its OWN `CYCLE` is THIS cycle's -- and
the file set it covers is not the file set it *reads*.

⭐⭐⭐⭐⭐ **⇒ THE FIX HAS TWO PARTS:**
  (1) RE-TYPE the LIVE instruments' `CYCLE` at this cycle;
  (2) ⭐⭐⭐⭐⭐ **ADD A WHOLE-BLUEPRINT AUDIT** that finds EVERY script with
      a `CYCLE` constant naming a DIFFERENT cycle, and CLASSIFIES it:
      a **LIVE INSTRUMENT** (must be re-typed) vs a **HISTORICAL
      ONE-SHOT PATCHER** (whose `CYCLE` names the cycle it *fixed*, and
      re-typing it would falsify the record).
"""
import ast
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

# ⭐⭐⭐⭐⭐ **THE LIVE INSTRUMENTS -- the scripts THIS CYCLE RUNS as part of
# ITS OWN TAIL.**  ⭐⭐⭐⭐⭐ Each one reads `_c{CYCLE}_*.py`, so each one's
# OWN `CYCLE` must be THIS cycle's or it measures the wrong generation.
LIVE_INSTRUMENTS = [
    "clone", "clone_sweep", "sweep_tokens", "docstring_shape",
    "fix_prose_identity", "fix_halfported_docstrings",
]

print("=" * 78)
print(f"CYCLE {CYCLE} -- RE-TARGET THE LIVE INSTRUMENTS")
print("=" * 78)
_retyped = []
for name in LIVE_INSTRUMENTS:
    fp = REPO / f"_c{CYCLE}_{name}.py"
    if not fp.exists():
        print(f"  [ABSENT] {name}.py")
        continue
    src = fp.read_text(encoding="utf-8")
    m = re.search(r'(?m)^(CYCLE\s*=\s*)"(\d+)"\s*$', src)
    if not m:
        print(f"  [NO CYCLE CONST] {name}.py")
        continue
    if m.group(2) == CYCLE:
        print(f"  [ALREADY] {name}.py: CYCLE = {CYCLE!r}")
        continue
    out = src[:m.start(2)] + CYCLE + src[m.end(2):]
    fp.write_text(out, encoding="utf-8")
    ast.parse(out)
    _retyped.append((name, m.group(2)))
    print(f"  [RE-TYPED] {name}.py: CYCLE {m.group(2)!r} -> {CYCLE!r}")
print(f"  ⇒ {len(_retyped)} live instrument(s) re-targeted")

# ======================================================================
# THE WHOLE-BLUEPRINT AUDIT
# ======================================================================
print()
print("=" * 78)
print("THE WHOLE-BLUEPRINT AUDIT -- every script's `CYCLE` constant")
print("=" * 78)
# ⭐⭐⭐⭐⭐ **THE CLASSIFICATION IS A MEASUREMENT, NOT A LIST.**  A script
# whose `CYCLE` names ANOTHER cycle is EITHER a LIVE INSTRUMENT (wrong --
# it reads the wrong generation) OR a HISTORICAL ONE-SHOT PATCHER (right
# -- its `CYCLE` names the cycle it FIXED, and re-typing it would falsify
# the record of what it repaired).
# ⭐⭐⭐⭐⭐ **⇒ THE DISCRIMINATOR IS *WHETHER THE SCRIPT IS ONE THIS CYCLE
# RUNS*** -- and the RUN SET is DERIVED FROM THE PIPELINE ORDER, not
# remembered.
CHAIN_STAGES = [
    "measure", "page", "struct", "commit", "verify", "jobs", "jobs_verify",
    "render", "render_posts", "select", "write", "build", "translate",
    "precert", "fetch_new", "adjudicate", "paths", "payload", "triage",
    "band_firetest", "fidelity2", "third_instrument", "d_keepcheck",
]
# the one-shot patchers that this lineage CARRIES FOR LINEAGE -- they are
# NOT run (their own `CYCLE` names the cycle they fixed), and the handover
# has said so for many cycles.
HISTORICAL_PATCHERS = [
    "patch_measure", "patch_anchor", "patch_band", "patch_noop",
    "patch_literals", "patch_prose", "patch_commit_noop",
    "fix_precert_consumer", "wrap_rescoring", "fix_page_docstring",
    "fix_docstring_shape", "fix_measure_docstring",
    "fix_halfported_messages", "measure_axes", "measure_stage_set",
    "port_ctl", "port_sweep_tokens",
]
LIVE = set(CHAIN_STAGES) | set(LIVE_INSTRUMENTS)

print("  the scripts with a `CYCLE` constant naming ANOTHER cycle:")
_stale_live, _hist = [], []
for fp in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    name = fp.name[len(f"_c{CYCLE}_"):]
    src = fp.read_text(encoding="utf-8")
    m = re.search(r'(?m)^CYCLE\s*=\s*"(\d+)"\s*$', src)
    if not m or m.group(1) == CYCLE:
        continue
    entry = (name, m.group(1))
    if name in LIVE:
        _stale_live.append(entry)
    else:
        _hist.append(entry)
if _stale_live:
    print("    ⭐⭐⭐⭐⭐ [LIVE INSTRUMENT -- MUST BE RE-TYPED]:")
    for n, c in _stale_live:
        print(f"        {n}.py: CYCLE = {c!r}")
else:
    print("    [OK] every LIVE INSTRUMENT's CYCLE is this cycle's")
print(f"    [HISTORICAL ONE-SHOT PATCHER -- carried for lineage, NOT run "
      f"({len(_hist)}): its CYCLE names the cycle it FIXED, and re-typing "
      f"it would falsify the record]")
for n, c in _hist:
    print(f"        {n}.py: CYCLE = {c!r}")

assert not _stale_live, (
    f"[audit] ABORT: these LIVE instruments still point at another cycle: "
    f"{_stale_live} -- they would measure the WRONG generation's artefacts")

print()
print("=" * 78)
print(f"CYCLE {CYCLE} -- THE LIVE INSTRUMENTS ARE RE-TARGETED")
print("=" * 78)
