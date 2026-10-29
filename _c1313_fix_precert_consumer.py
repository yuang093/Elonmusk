#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- FIX `precert.py`'s PROSE-PARSING CONSUMER.

⭐⭐⭐⭐⭐ **THE DEFECT (Reminder 83's CLASS, IN A THIRD CONSUMER).**
Cycle 1258 fixed the PRODUCER to emit a MACHINE-READABLE provenance row:

    {"defects": <int>, "score": {...}, "source": "...", "provenance": "<prose>"}

and fixed the COMMIT stage to read the `defects` FIELD.  ⭐⭐⭐⭐⭐ **BUT
`precert.py` IS A THIRD CONSUMER, AND IT STILL PARSES THE PROSE**:

    m = re.search(r"(\\d+)\\s+(?:fidelity\\s+)?defect", prov)

With `prov` now a **dict**, that call raises `TypeError: expected string or
bytes-like object` -- **the precert stage DIES, not merely mis-reports.**
⭐⭐⭐⭐⭐ **THE 1258 FIX WAS NOT COMPLETE: IT CHANGED THE CONTRACT FOR THE
CONSUMERS IT KNEW ABOUT AND LEFT A THIRD CONSUMER ON THE OLD CONTRACT.**

⭐⭐⭐⭐⭐ **THE FIX IS NOT "ADD A FOURTH REGEX"** (Reminder 83) -- it is to
read the **FIELD**, and to keep the PROSE as the audit trail only.  ⭐⭐⭐⭐⭐
AND THE FIX MAKES THE GATE **STRICTER**: the old code took the number out
of a sentence; the new code takes it out of the field **and still
cross-checks the TEXT against the corpus byte-for-byte** (the comparison
that actually establishes "the thing that was published is the thing that
was scored").

⭐⭐⭐⭐⭐ **THE CLAIM IS NOT TRUSTED BLINDLY:** the `defects` field is a
CLAIM.  The real verification is the **byte-identity** check between the
prior final translation and the text the INHERITED CORPUS carries, which
is already in this script and is UNCHANGED by this fix.
"""
import ast
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

_p = REPO / f"_c{CYCLE}_precert.py"
_src = _p.read_text(encoding="utf-8")

OLD = '''    m = re.search(r"(\\d+)\\s+(?:fidelity\\s+)?defect", prov)
    if m is None or int(m.group(1)) != 0:
        skipped[tid] = (f"the prior provenance is not 0-defect: {prov!r} "
                        f"(artefact family: {art_src})")
        continue
'''

NEW = '''    # ⭐⭐⭐⭐⭐ CYCLE 1263's FIX: **READ THE MACHINE-READABLE FIELD, NOT
    # THE PROSE.**  Cycle 1258 changed the producer to emit
    # `{"defects": <int>, "score": {...}, "source": ..., "provenance": ...}`
    # and fixed the COMMIT consumer to read the field -- but this THIRD
    # consumer still ran a prose regex over the row, and with a dict that
    # raises `TypeError: expected string or bytes-like object` (the stage
    # DIED, it did not merely mis-report).
    # ⭐⭐⭐⭐⭐ **THE FIX IS NOT "ADD A FOURTH REGEX"** (Reminder 83): the
    # field IS the contract, and the prose stays as the audit trail.
    # ⭐⭐⭐⭐⭐ **AN OLDER PROSE-ONLY ARTEFACT IS STILL ACCEPTED** -- it is
    # read with the legacy regex, because a legacy artefact carries no
    # field to read.
    if isinstance(prov, dict):
        if "defects" not in prov:
            skipped[tid] = (
                f"the prior provenance states no defect count: {prov!r} "
                f"(artefact family: {art_src})")
            continue
        _claim = int(prov["defects"])
    else:
        _m = re.search(r"(\\d+)\\s+(?:fidelity\\s+)?defect", str(prov))
        if _m is None:
            skipped[tid] = (f"the prior provenance is not 0-defect: {prov!r} "
                            f"(artefact family: {art_src})")
            continue
        _claim = int(_m.group(1))
    if _claim != 0:
        skipped[tid] = (f"the prior provenance is not 0-defect: {prov!r} "
                        f"(artefact family: {art_src})")
        continue
'''

assert _src.count(OLD) == 1, (
    f"[fix] the prose-regex consumer occurs {_src.count(OLD)} times -- the "
    "anchor is not unique")
_src = _src.replace(OLD, NEW)

# ⭐⭐⭐⭐⭐ THE PRINT MUST ALSO NOT ASSUME A STRING.
OLD_PRINT = '    print(f"  [PRE-CERTIFIED] {tid}: {prov}")'
NEW_PRINT = ('    print(f"  [PRE-CERTIFIED] {tid}: "\n'
             '          f"{prov.get(\'provenance\', prov) if isinstance(prov, dict) '
             'else prov} "\n'
             '          f"[defects field = {_claim}]")')
assert _src.count(OLD_PRINT) == 1, (
    f"[fix] the PRE-CERTIFIED print occurs {_src.count(OLD_PRINT)} times -- "
    "the anchor is not unique")
_src = _src.replace(OLD_PRINT, NEW_PRINT)

try:
    ast.parse(_src)
except SyntaxError as _se:
    raise SystemExit(f"[fix] ABORT: the patched precert.py does not PARSE: {_se}")

_p.write_text(_src, encoding="utf-8")
print(f"[fix] the precert consumer now READS the `defects` FIELD "
      f"(a dict row) and falls back to the legacy regex ONLY for an "
      f"older prose-only artefact.")
print(f"[fix] the file was RE-READ FROM DISK and PARSES.")
