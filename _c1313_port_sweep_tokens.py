#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- PORT THE PAIR-KEYED VALUE-TOKEN SWEEP.

⭐⭐⭐⭐⭐ **WHY THIS PORT IS ITS OWN STEP (and not part of the clone):**
the pair-keyed sweep is NOT in the clone's file list, because its own
`CYCLE` constant is **LOAD-BEARING** -- it selects which files the sweep
reads (`_c{CYCLE}_measure.py`) and which files it audits
(`_c{CYCLE}_{name}.py`).

⭐⭐⭐⭐⭐ **THE SOURCE IS 1268's COPY, NOT THE BASE'S -- AND THE REASON IS
THE AXIS, NOT RECENCY (Reminder 74 + Reminder 71).**  ⭐⭐⭐⭐⭐
⭐⭐⭐⭐⭐ **1278's BASE IS 1277 AND ITS PAIR IS (OUT, OUT) -- A DIFFERENT
PAIR FROM THIS CYCLE'S (OUT, IN) -- so the set-difference form is NOT
merely equivalent here, it is *REQUIRED*.**  1268's copy carries the
**set-difference** construction of the forbidden lists:

    PHRASE_FORBIDDEN = [v["phrase"] for k, v in ATTR.items()
                        if k != PAIR and v["phrase"] != _A["phrase"]]

⭐⭐⭐⭐⭐ **THAT CONSTRUCTION IS *BAND-SIDE NEUTRAL* AND *STRICTLY
STRONGER*:**
  * on a FLIPS pair the "other three pairs" form would forbid this pair's
    OWN phrase (the (OUT, IN) and (IN, OUT) pairs share the phrase "the
    control set FLIPS") -> the instrument aborts on the CORRECT artefact;
  * the set-difference form ALSO ASSERTS that this pair's own tokens are
    ABSENT from the forbidden list.

⭐⭐⭐⭐⭐ **THE PORT IS EXPLICIT AND ITS RESULT IS ASSERTED.**  A port
that does not land is a silent no-op (cycle 1257's lesson), so every
identity constant is checked after the substitution, and the hour the
ported sweep MEASURES is compared against this cycle's own hour.
"""
import ast
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
HOUR = 2
SRC = REPO / "_c1268_sweep_tokens.py"
DST = REPO / f"_c{CYCLE}_sweep_tokens.py"

print("=" * 78)
print(f"CYCLE {CYCLE} -- PORT THE PAIR-KEYED VALUE-TOKEN SWEEP")
print("=" * 78)

_src = SRC.read_text(encoding="utf-8")

# ---------------------------------------------------------------------
# 1. THE IDENTITY CONSTANT -- THE ONE THAT IS LOAD-BEARING
# ---------------------------------------------------------------------
_m = re.search(r'(?m)^CYCLE\s*=\s*"(\d+)"$', _src)
assert _m, ("[port] ABORT: the source sweep has no CYCLE assignment -- the "
            "port would be a silent no-op")
print(f"  [FOUND] the source's CYCLE = {_m.group(1)!r}  "
      f"⭐⭐⭐ STALE -- it would read _c{_m.group(1)}_measure.py and audit "
      f"_c{_m.group(1)}_*.py)")
assert _m.group(1) != CYCLE, (
    "[port] ABORT: the source already carries this cycle's identity -- "
    "refusing to double-port")

_src = re.sub(r'(?m)^CYCLE\s*=\s*"\d+"$', f'CYCLE = "{CYCLE}"', _src, count=1)

# ---------------------------------------------------------------------
# 1b. THE HOUR -- the sweep may carry it as a typed constant
# ---------------------------------------------------------------------
_hm = re.search(r"(?m)^HOUR\s*=\s*(\d+)$", _src)
if _hm:
    print(f"  [FOUND] the source's HOUR = {_hm.group(1)}")
    _src = re.sub(r"(?m)^HOUR\s*=\s*\d+$", f"HOUR = {HOUR}", _src, count=1)
else:
    print("  [OK] the source carries no typed HOUR -- it MEASURES it")

# ---------------------------------------------------------------------
# 2. THE SET-DIFFERENCE CONSTRUCTION -- VERIFY IT LANDED
# ---------------------------------------------------------------------
print()
print("  [CHECK] the set-difference construction is present:")
for _probe, _label in (
        ('v["phrase"] != _A["phrase"]', "PHRASE_FORBIDDEN set-difference"),
        ('v["attr"] != _A["attr"]', "ATTR_FORBIDDEN set-difference"),
        ('_A["phrase"] not in PHRASE_FORBIDDEN',
         "the own-phrase-absent assertion"),
        ('_A["attr"] not in ATTR_FORBIDDEN',
         "the own-attribution-absent assertion")):
    assert _probe in _src, (
        f"[port] ABORT: the source does NOT carry {_label} ({_probe!r}) -- "
        "the stricter form must be carried")
    print(f"    [PRESENT] {_label}")

# ---------------------------------------------------------------------
# 3. WRITE AND RE-READ FROM DISK -- A DISCARDED SUBSTITUTION IS A SILENT
#    NO-OP (Reminder 84(d))
# ---------------------------------------------------------------------
DST.write_text(_src, encoding="utf-8")
_disk = DST.read_text(encoding="utf-8")
_m2 = re.search(r'(?m)^CYCLE\s*=\s*"(\d+)"$', _disk)
assert _m2, "[port] ABORT: the written sweep has no CYCLE assignment"
assert _m2.group(1) == CYCLE, (
    f"[port] ABORT: the written sweep's CYCLE is {_m2.group(1)!r}, not "
    f"{CYCLE!r} -- the substitution did NOT land")
print(f"  [OK] the written sweep's CYCLE = {_m2.group(1)!r} "
      "(RE-READ FROM DISK -- the substitution LANDED)")
try:
    ast.parse(_disk)
except SyntaxError as _se:
    raise SystemExit(f"[port] ABORT: the written sweep does not PARSE: {_se}")
print("  [OK] the written sweep PARSES")

# ---------------------------------------------------------------------
# 4. THE SWEEP'S OWN HOURLESS PRECONDITION -- the sweep DERIVES its hour
#    from `_c{CYCLE}_measure.py`; that file must EXIST and carry the hour
# ---------------------------------------------------------------------
_mm = re.search(r'_c\{CYCLE\}_measure\.py|f"_c\{CYCLE\}_measure\.py"',
                 _disk)
print(f"  [OK] the sweep reads this cycle's own measure.py: {bool(_mm)}")
_mf = REPO / f"_c{CYCLE}_measure.py"
assert _mf.exists(), (
    f"[port] ABORT: {_mf.name} does not exist -- the sweep would read "
    "another cycle's hour")
_mfh = re.search(r"(?m)^CYCLE_HOUR_UTC\s*=\s*(\d+)\s*$",
                 _mf.read_text(encoding="utf-8"))
assert _mfh, "[port] ABORT: the measure.py carries no CYCLE_HOUR_UTC"
assert int(_mfh.group(1)) == HOUR, (
    f"[port] ABORT: {_mf.name} carries CYCLE_HOUR_UTC = {_mfh.group(1)}, "
    f"expected {HOUR} -- the sweep would measure another cycle's hour")
print(f"  [OK] {_mf.name} carries CYCLE_HOUR_UTC = {_mfh.group(1)} "
      "(== this cycle's hour)")

print()
print("=" * 78)
print(f"[port] CYCLE {CYCLE} value-token sweep ported -> {DST.name}")
print("=" * 78)
print("  ⭐⭐⭐ NEXT: RUN THE DOCSTRING-SHAPE INSTRUMENT, THEN THE IDENTITY "
      "SWEEP, THEN THE VALUE-TOKEN SWEEP.")
