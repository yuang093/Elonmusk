#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- REPAIR THE TWO HALF-PORTED ASSERT MESSAGES.

⭐⭐⭐⭐⭐ **THE VALUE-TOKEN SWEEP FOUND THEM** (this is the sweep doing its
job, and it is the FIRST TIME IT HAS RUN ON AN (IN, IN) PAIR):

    [VIOLATION] jobs:637        'was OUT OF BAND'
    [VIOLATION] jobs_verify:258 'was OUT OF BAND'

⭐⭐⭐⭐⭐ **⇒ THESE ARE *HALF-PORTED ASSERTS*: THE ASSERT VALUE WAS PORTED
TO THE (IN, IN) SIDE, BUT ITS *MESSAGE* STILL DESCRIBES THE PRIOR CYCLE AS
OUT OF BAND.**  ⭐⭐⭐⭐⭐ **⇒ THAT IS EXACTLY 1278's DEFECT CLASS** -- the
assert VALUE and the assert MESSAGE disagree, and **every gate that
measures only internal consistency sees the file as healthy** (1275's
class-level finding).

⭐⭐⭐⭐⭐ **⇒ AND IT IS INVISIBLE TO A POLARITY-AWARE SWEEP THAT ONLY
READS THE *VALUE*** -- because the message is a STRING CONSTANT inside the
assert's message argument, which the value-token sweep classifies by the
token's presence, and which a reader skims past.

⭐⭐⭐⭐⭐ **⇒ THE FIX PORTS THE MESSAGE TOO**, and it is asserted in BOTH
directions: the (IN, IN) message must be present AND the OUT-side message
must be gone.

⭐⭐⭐⭐⭐ **⇒ THE FIX IS IDEMPOTENT** -- a re-run reports `[ALREADY]`.
"""
import ast
import pathlib

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

# (file, the OUT-side message fragment, the (IN, IN) message fragment)
REPAIRS = [
    ("jobs.py",
     '    "the prior committed cycle was out of band and this one is in band -- "',
     '    "the prior committed cycle was ALSO in band and this one is in band '
     'too -- "'),
    ("jobs_verify.py",
     '    "the prior committed cycle was out of band -- the note must say the "',
     '    "the prior committed cycle was ALSO in band -- the note must say the "'),
]

print("=" * 78)
print(f"CYCLE {CYCLE} -- REPAIR THE TWO HALF-PORTED ASSERT MESSAGES")
print("=" * 78)

for fname, old, new in REPAIRS:
    fp = REPO / f"_c{CYCLE}_{fname}"
    src = fp.read_text(encoding="utf-8")
    if old in src:
        src = src.replace(old, new, 1)
        fp.write_text(src, encoding="utf-8")
        ast.parse(fp.read_text(encoding="utf-8"))
        print(f"  [FIXED] {fname}: the assert MESSAGE -> the (IN, IN) side")
    else:
        assert new in src, (
            f"[fix] ABORT: {fname} carries NEITHER the OUT-side message nor "
            "the (IN, IN) one -- the text DRIFTED; reporting [ALREADY] here "
            "would be a LIE")
        print(f"  [ALREADY] {fname}: the assert MESSAGE already carries the "
              "(IN, IN) side")

print()
print("=" * 78)
print("THE FINAL AUDIT -- the OUT-side message must be GONE, the (IN, IN) one")
print("must be PRESENT, in BOTH files")
print("=" * 78)
for fname, old, new in REPAIRS:
    fp = REPO / f"_c{CYCLE}_{fname}"
    src = fp.read_text(encoding="utf-8")
    assert old not in src, (
        f"[fix] ABORT: {fname} still carries the OUT-side assert MESSAGE")
    assert new in src, (
        f"[fix] ABORT: {fname} does NOT carry the (IN, IN) assert MESSAGE")
    print(f"  [OK] {fname}: the (IN, IN) message is present, the OUT-side one "
          "is gone")
print()
print("  ⭐⭐⭐ NEXT: RE-RUN THE VALUE-TOKEN SWEEP.")
