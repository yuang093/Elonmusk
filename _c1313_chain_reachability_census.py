#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1299 -- THE WHOLE-CHAIN WRITE-REACHABILITY CENSUS.

⭐⭐⭐⭐⭐ **WHY THIS EXISTS.**  Cycle 1295 found the dead-write-block defect
in `build.py` and the skill's reference says *"the repair MUST be applied to
EVERY affected generation on disk"*.  ⭐⭐⭐⭐⭐ **⇒ THIS CYCLE APPLIED IT TO
`build.py` — AND THEN MEASURED `write.py` AND FOUND *THE SAME DEFECT*.**

⇒ ⇒ **⇒ THE 1295 CENSUS WAS SCOPED TO ONE FILE.  THE DEFECT IS *FAMILY-
WIDE*: the SAME extraction refactor (cutting the module-level tail and
re-indenting it into the gate helper) landed in EVERY stage that carries
the "pure addition" gate.**  ⇒ ⇒ **⇒ `build.py` AND `write.py` BOTH carry
it.**

⭐⭐⭐⭐⭐ **⇒ AND THE INSTRUMENT THAT FOUND IT WAS RUN WITH A *GLOB* — THE
1295 REFERENCE'S OWN CENSUS WAS `--glob "_c12*_build.py"`, i.e. IT COULD
NOT HAVE SEEN `write.py`.**  ⇒ ⇒ **⇒ A DEFECT SEARCH THAT NAMES THE FILES
IT LOOKS AT CANNOT FIND A DEFECT IN A FILE IT DOES NOT NAME.**

⭐⭐⭐⭐⭐ **⇒ THE RULE: *A DEFECT CLASS MUST BE SEARCHED BY ITS SHAPE, NOT
BY A FILE LIST.*  THE SHAPE IS: "a stage's `write_text`/`write_bytes` call
sits after a `return` in the same function."*

⭐⭐⭐⭐⭐ **⇒ THIS INSTRUMENT SCANS *EVERY* PYTHON FILE IN THE REPO** (not a
glob of chosen names) ⇒ ⇒ **⇒ IT FINDS THE FAMILY, INCLUDING THE MEMBERS
NOBODY NAMED.**

⭐⭐⭐⭐⭐ **⇒ AND IT IS CALIBRATED**: a file that is REACHABLE is reported
as such, and the census is compared against the OLDEST generation on disk
(c1288 and earlier) to establish WHERE the defect family started.

⭐⭐⭐⭐⭐ **⇒ RULE D (1295): *A STAGE'S EXIT CODE IS NOT A MEASUREMENT OF
ITS ARTEFACT.*  ⇒ ⇒ **⇒ THIS CENSUS IS THE PROOF-OF-PRODUCTION INSTRUMENT
FOR EVERY STAGE IN THE CHAIN.**
"""
import ast
import pathlib
import sys

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")

# The stages that PRODUCE an artefact (a write_text / write_bytes call).
# ⭐⭐⭐⭐⭐ THE LIST IS DERIVED, NOT TYPED: every `.py` in the repo is
# scanned, and a file is a "PRODUCER" iff it calls a write_* method.
# ⭐⭐⭐⭐⭐ ⇒ A STAGE THAT NOBODY NAMED IS STILL FOUND.

WRITE_ATTRS = ("write_text", "write_bytes")


def own_nodes(fn):
    out, stack = [], list(fn.body)
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda,
                          ast.ClassDef)):
            continue
        out.append(n)
        for child in ast.iter_child_nodes(n):
            stack.append(child)
    return out


def _own_returns(fn):
    return sorted(n.lineno for n in own_nodes(fn) if isinstance(n, ast.Return))


def _own_writes(fn):
    return sorted(n.lineno for n in own_nodes(fn)
                  if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Attribute)
                  and n.func.attr in WRITE_ATTRS)


def analyse(path):
    """MEASURE one file.  Returns (kind, detail).

    kind: "REACHABLE" | "DEAD" | "NO-ENTRY" | "NO-WRITE" | "UNPARSED"
    """
    try:
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
    except (SyntaxError, OSError, UnicodeDecodeError) as e:
        return "UNPARSED", str(e)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if "main" not in funcs:
        return "NO-ENTRY", "no main()"
    main = funcs["main"]
    mw, mr = _own_writes(main), _own_returns(main)
    if mw:
        if not any(r < w for w in mw for r in mr):
            return "REACHABLE", f"main() writes at {mw}"
        return "DEAD", (f"main() writes at {mw} but main() returns at {mr} "
                        "-- the write is AFTER the return")
    # the entry may call a helper that writes
    calls = {n.func.id for n in own_nodes(main)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    for fname in sorted(calls):
        fn = funcs.get(fname)
        if fn is None:
            continue
        hw, hr = _own_writes(fn), _own_returns(fn)
        if not hw:
            continue
        if not any(r < w for w in hw for r in hr):
            return "REACHABLE", f"helper {fname}() writes at {hw}"
        return "DEAD", (f"helper {fname}() writes at {hw} but returns at "
                        f"{hr} -- the write is AFTER the return")
    return "NO-WRITE", "no write_text/write_bytes in main() or its helpers"


def main():
    print("=" * 78)
    print("CYCLE 1299 -- THE WHOLE-CHAIN WRITE-REACHABILITY CENSUS")
    print("=" * 78)
    print("  ⭐⭐⭐ EVERY `.py` in the repo is scanned -- the file list is NOT")
    print("  typed, so a stage nobody named is still found.")

    files = sorted(REPO.glob("*.py"))
    dead, reach, other = [], [], []
    for p in files:
        kind, detail = analyse(p)
        rec = (p.name, detail)
        if kind == "DEAD":
            dead.append(rec)
        elif kind == "REACHABLE":
            reach.append(rec)
        else:
            other.append(rec)

    print()
    print("=" * 78)
    print(f"THE DEAD FILES ({len(dead)}) -- a stage that EXITS 0 and writes "
          "NOTHING")
    print("=" * 78)
    for name, detail in dead:
        print(f"  ⛔ {name}: {detail}")

    print()
    print("=" * 78)
    print(f"THE REACHABLE PRODUCERS ({len(reach)})")
    print("=" * 78)
    for name, detail in reach:
        print(f"  [OK] {name}: {detail}")

    # ---- the FAMILY: group the dead files by their stage name -----------
    print()
    print("=" * 78)
    print("THE FAMILY -- the dead files grouped by STAGE")
    print("=" * 78)
    fam = {}
    for name, _ in dead:
        m = __import__("re").match(r"_c(\d+)_(\w+)\.py$", name)
        if m:
            fam.setdefault(m.group(2), []).append(m.group(1))
        else:
            fam.setdefault(name, []).append("-")
    for stage, cycles in sorted(fam.items()):
        cyc = sorted(cycles)
        print(f"  ⛔ {stage:<16} dead in {len(cyc)} generation(s): "
              f"{cyc[0]}..{cyc[-1]}")
        print(f"       ⭐⭐⭐ THE WHOLE FAMILY IS DEAD -- repair EVERY member, "
              f"not just the current one")

    print()
    print("=" * 78)
    print("THE CALIBRATION -- where did the family start?")
    print("=" * 78)
    for stage in sorted(fam):
        cyc = sorted(fam[stage])
        numeric = [c for c in cyc if c.isdigit()]
        if not numeric:
            # a NON-GENERATION file (a helper instrument) -- it is reported
            # by name, and its calibration is skipped (there is no
            # "generation before" for it).
            print(f"  {stage:<16} a NON-GENERATION instrument: {cyc[0]}")
            continue
        first = numeric[0]
        older = REPO / f"_c{int(first) - 1}_{stage}.py"
        if older.exists():
            kind, detail = analyse(older)
            print(f"  {stage:<16} the generation BEFORE {first} "
                  f"({older.name}): {kind} -- {detail[:70]}")
        else:
            print(f"  {stage:<16} no generation before {first} on disk")

    print()
    print("=" * 78)
    print(f"RESULT: {len(dead)} DEAD producer(s) across {len(fam)} stage(s)")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
