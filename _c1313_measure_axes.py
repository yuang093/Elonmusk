#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- MEASURE THE COST OF PORTING EACH AXIS (Reminder 74).

⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
⭐⭐⭐ **REMINDER 74: "CHEAPEST" IS A MEASUREMENT, NOT AN INTUITION.**

This cycle is HOUR201 -> OUT OF BAND for
`RETRY_TRANSLATION_HOURS = {0,3,6,9,12,15,18,21}`; the prior COMMITTED
cycle (1245) ran on Hour21 -> IN BAND.  The band PAIR is therefore
**(IN, OUT)** -- the control set FLIPS.

THE AXES:
  * axis 1 = the BAND SIDE (this cycle's own hour: IN or OUT) -- it decides
    the control set's ASSERTION SHAPE;
  * axis 2 = the ATTRIBUTION (the prior COMMITTED cycle's side) -- it decides
    the published PROSE;
  * axis 3 = the CODE FIXES (the newest cycle carries them all).

⭐⭐⭐ **THE MEASUREMENT IS AN AST-LEVEL LIVE-CODE DIFF** (docstrings
stripped), chunked on statement boundaries.
"""
import ast
import difflib
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
HOUR = 2
PRIOR = "1245"       # the prior COMMITTED cycle (index.html's publishing commit)
BASE = "1246"        # the NEWEST cycle -- every code fix lives here

BAND_FILES = ["measure", "page", "struct", "commit", "verify", "jobs",
              "jobs_verify"]


def live_dump(path):
    src = pathlib.Path(path).read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body:
            first = body[0]
            if (isinstance(first, ast.Expr)
                    and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                body.pop(0)
    return ast.dump(tree)


def _chunks(dump):
    return re.split(r"(?=\), |ast\.)", dump)


def n_diff(a, b):
    ca = _chunks(live_dump(a))
    cb = _chunks(live_dump(b))
    return sum(1 for l in difflib.unified_diff(ca, cb, lineterm="", n=0)
               if l[:1] in "+-" and not l.startswith(("+++", "---")))


print("=" * 78)
print("CYCLE 1247 -- THE MEASURED DECISION (which axis is expensive?)")
print("=" * 78)
print(f"  this cycle: hour {HOUR} UTC = OUT OF BAND")
print(f"  prior COMMITTED: {PRIOR} = IN BAND  ->  pair (IN, OUT) -> FLIPS")
print(f"  base (the newest, every code fix): {BASE}")
print()

# ---- axis 1: the BAND SIDE -- the OUT-of-band control-set shape ----
# candidates: cycles whose OWN hour was OUT OF BAND
OUT_SIDE = ["1244", "1243", "1241", "1240", "1238", "1235", "1234"]
_costs = []
for src_cycle in OUT_SIDE:
    if not all((REPO / f"_c{src_cycle}_{f}.py").exists() for f in BAND_FILES):
        continue
    cost = sum(n_diff(REPO / f"_c{src_cycle}_{f}.py",
                      REPO / f"_c{BASE}_{f}.py") for f in BAND_FILES)
    _costs.append((cost, src_cycle))
_costs.sort()
print("  AXIS 1 -- the BAND SIDE (port the OUT-of-band control-set SHAPE)")
for cost, src_cycle in _costs:
    print(f"    {src_cycle} (OUT side) -> {BASE}: {cost:5d} live statements")
_band_cost, band_src = _costs[0]
print(f"  => the cheapest OUT-side shape source is {band_src} "
      f"({_band_cost} statements)")

# ---- axis 2: the ATTRIBUTION -- (prior IN, this OUT) ----
# candidates: cycles whose OWN hour was OUT and whose PRIOR was IN
print()
print("  AXIS 2 -- the ATTRIBUTION (the prior COMMITTED cycle was IN BAND)")
for src_cycle in ["1234", "1235", "1238", "1240", "1241", "1243", "1244"]:
    p = REPO / f"_c{src_cycle}_page.py"
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    m = re.search(r'f"\(\{PRIOR_CYCLE\}\) was ([A-Z ]+?) -- its own block was '
                  r'the ([A-Z ]+?)"', s)
    h = re.search(r"(?m)^CYCLE_HOUR_UTC\s*=\s*(\d+)$", s)
    print(f"    {src_cycle}: hour={h.group(1) if h else '?'}  "
          f"attribution={m.groups() if m else 'NOT FOUND'}")

# ---- axis 3: the CODE FIXES ----
print()
print("  AXIS 3 -- the CODE FIXES (1245 -> 1246)")
_fix_cost = sum(n_diff(REPO / f"_c1245_{f}.py",
                        REPO / f"_c{BASE}_{f}.py") for f in BAND_FILES)
print(f"    1245 -> {BASE}: {_fix_cost:5d} live statements")

print()
print("=" * 78)
print("THE DECISION")
print("=" * 78)
print(f"  the BASE is cycle {BASE} (the NEWEST -- every code fix lives there)")
print(f"  the OUT-of-band control-set SHAPE comes from cycle {band_src}")
print(f"  the (prior IN, this OUT) ATTRIBUTION comes from the shape source's")
print(f"    own prose, re-pointed at THIS cycle's prior cycle ({PRIOR})")
print()
print("  ⭐ THE PORT IS THE *SHAPE* PORT: the control set is a function of")
print("    THIS cycle's band ALONE (Reminder 21); the attribution is a")
print("    separate, SMALL prose port.")
