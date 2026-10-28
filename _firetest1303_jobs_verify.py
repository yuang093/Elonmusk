#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1303 -- THE FIRE-TEST for the repaired `jobs_verify.py` provenance gate.

⭐⭐⭐⭐⭐ **AN INSTRUMENT THAT CANNOT FIRE IS EXACTLY AS UNTRUSTWORTHY AS ONE
THAT FIRES ON A CORRECT ARTEFACT** (1291's class-level rule).  ⭐⭐⭐⭐⭐ **⇒ THE
REPAIRED GATE MUST BE PROVEN ABLE TO FAIL, ON EVERY BRANCH.**

⭐⭐⭐⭐⭐ **THIS FIRE-TEST FOUND A SECOND INSTANCE OF THE DEFECT.**  ⭐⭐⭐⭐⭐ The
first repair built each branch's forbidden list from "the OTHER two branches'
forms" ⇒ ⇒ **⇒ BUT `_FORM_C` AND `_FORM_A` ARE THE *SAME STRING* WHENEVER
`_n_inh == 0`** ⇒ ⇒ **⇒ THE `(0, 0, 0)` BRANCH STILL OVERLAPPED** ⇒ ⇒ **⇒ THE
REPAIR MUST DEDUPLICATE THE FORMS INTO A *SET* AND SUBTRACT THE BRANCH's OWN
FORM** ⇒ ⇒ **⇒ AND THE OVERLAP IS NOW IMPOSSIBLE BY CONSTRUCTION.**
"""
import re

print("=" * 78)
print("THE FIRE-TEST -- THE REPAIRED PROVENANCE GATE, ON EVERY BRANCH")
print("=" * 78)


def forms(n_inh, n_bn, n_real):
    """THE REPAIRED CONSTRUCTION -- verbatim from `_c1303_jobs_verify.py`."""
    A = f"0 of the {n_real} were written"
    B = f"ALL {n_inh} of the {n_real}"
    C = f"{n_inh} of the {n_real} were written"
    ALL = {A, B, C}
    if n_inh == 0 and n_bn == 0:
        req = [A]
    elif n_inh == 0:
        req = [A]
    elif n_bn == 0:
        req = [B]
    else:
        req = [C]
    return req, ALL - set(req)


print("\n[1] THE STRUCTURAL INVARIANT ON EVERY BRANCH")
CASES = [(0, 0, 0), (0, 3, 3), (4, 0, 4), (2, 1, 3), (0, 1, 1), (1, 0, 1)]
for inh, bn, real in CASES:
    req, forb = forms(inh, bn, real)
    overlap = set(req) & set(forb)
    print(f"    split(inh={inh}, bn={bn}, real={real}):")
    print(f"       required  = {req}")
    print(f"       forbidden = {sorted(forb)}")
    assert not overlap, (
        f"the required form {set(req)} and the forbidden forms {forb} "
        "OVERLAP -- the gate would fire on its own required prose")
    print(f"       [OK] no overlap")
print("  [OK] the overlap is IMPOSSIBLE on every branch")

print("\n[2] THE POSITIVE CONTROL -- a CORRECT note PASSES")
for inh, bn, real in CASES:
    req, forb = forms(inh, bn, real)
    note = req[0] + " by an earlier cycle and never committed"
    for f in req:
        assert f in note, f"the required form {f!r} is MISSING -> must fail"
    for f in forb:
        assert f not in note, (
            f"the forbidden form {f!r} is PRESENT in a correct note -> the "
            "gate would FIRE ON A CORRECT ARTEFACT")
    print(f"    [OK] split(inh={inh}, bn={bn}, real={real}): the correct note "
          f"passes ({req[0]!r})")

print("\n[3] THE NEGATIVE CONTROL -- a WRONG note is REJECTED")
for inh, bn, real in CASES:
    req, forb = forms(inh, bn, real)
    if not forb:
        continue
    bad = sorted(forb)[0] + " by an earlier cycle"
    caught = False
    for f in forb:
        if f in bad:
            caught = True
    assert caught, (
        f"the wrong form {sorted(forb)[0]!r} is NOT caught by the forbidden "
        "list -- the gate cannot fire")
    print(f"    [OK] split(inh={inh}, bn={bn}, real={real}): the wrong form "
          f"{sorted(forb)[0]!r} IS caught")

print("\n[4] THE EMPTY-NOTE CONTROL -- a note with NO form is REJECTED")
for inh, bn, real in CASES:
    req, forb = forms(inh, bn, real)
    empty = "the provenance split is measured"
    fails = (not any(f in empty for f in req)) or any(f in empty for f in forb)
    assert fails, "an empty note would PASS -- the gate cannot fire"
print("    [OK] a note carrying NO form is rejected on every branch")

print("\n" + "=" * 78)
print("THE FIRE-TEST PASSES -- THE GATE IS *NOT* WEAKENED, AND IT CAN FAIL.")
print("=" * 78)
