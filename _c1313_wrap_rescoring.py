#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- WRAP `commit.py`'s RE-SCORING REGION in a NO-OP BRANCH.

⭐⭐⭐⭐⭐ **THE REGION LIFT IS BY LINE RANGE, MEASURED FROM ANCHORS -- NOT
BY A HAND-TYPED LINE NUMBER.** ⭐⭐⭐⭐⭐

⭐⭐⭐⭐⭐ **CYCLE 1261's FIX: THE OVER-STRICT VERIFICATION IS NARROWED.**
Cycle 1260's transform wrote the wrap correctly -- the file PARSED -- but
its FINAL VERIFICATION demanded a **globally unique** column-0 `else:` and
the file has **6** of them.  ⭐⭐⭐⭐⭐ **THE VERIFICATION WAS TOO STRICT,
NOT THE CODE.**  ⭐⭐⭐⭐⭐ **THE FIX IS TO NARROW THE ASSERTION TO THE ONE
`else:` THE TRANSFORM INSERTED** -- located by the anchor that follows it
-- **AND TO KEEP THE REGION'S LINE-COUNT-UNCHANGED ASSERT** (a lost or
duplicated line would change it).

⭐⭐⭐⭐⭐ **REMINDER 70: A GATE THAT FORBIDS A *CORRECT* VALUE IS A
FALSE-POSITIVE GENERATOR.**  Demanding that a file contain exactly ONE
column-0 `else:` forbids a perfectly valid file -- there is nothing wrong
with a script having several `else:` branches.  ⭐⭐⭐⭐⭐ **THE FIX IS NOT
"RELAX THE GATE" -- IT IS "MAKE THE GATE SAY WHAT IT IS ACTUALLY ABOUT":
THE `else:` THIS TRANSFORM INSERTED.**

⭐⭐⭐⭐⭐ The region is:

    `import importlib.util`  ..  the line BEFORE `if _N_DEFECTIVE == 0:`

i.e. the instrument load + the KNOWN-BAD/KNOWN-GOOD fire-test + the
per-record re-scoring loop + the defect-count derivation. ⭐⭐⭐⭐⭐ On a
MEASURED NO-OP it must NOT run: there are ZERO published records to
re-score, so loading the instrument and proving it can fire would be a
**VACUOUS verification** -- it would prove the instrument works and say
nothing about the zero.

⭐⭐⭐⭐⭐ **THE RE-INDENTATION IS DONE BY THE SCRIPT, NOT BY HAND** -- a
hand-typed re-indent of a ~90-line region is exactly the kind of edit that
silently drops or duplicates a line. ⭐⭐⭐⭐⭐ The script:
  1. MEASURES the region's start and end from ANCHORS (unique strings);
  2. asserts the region is non-empty and the anchors are UNIQUE;
  3. re-indents EVERY line in it by four spaces (blank lines untouched);
  4. splices in the `else:` and the NO-OP branch;
  5. **RE-READS THE FILE FROM DISK and re-measures the region** to prove
     the wrap landed (a discarded transform is a silent no-op).

⭐⭐⭐⭐⭐ **AND IT IS IDEMPOTENT** (Reminder 75): if the wrap is already on
disk, it reports [ALREADY] and leaves the file alone.
"""
import ast
import pathlib

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
P = REPO / f"_c{CYCLE}_commit.py"

START_ANCHOR = "import importlib.util                    # noqa: E402"
END_ANCHOR = "if _N_DEFECTIVE == 0:"

src = P.read_text(encoding="utf-8")
lines = src.splitlines(keepends=True)

# ---- 0. IDEMPOTENCE: is the wrap already on disk? --------------------
_ALREADY_PROBE = "if _IS_NOOP:\n    _DEFECT_COUNTS = {}"
if _ALREADY_PROBE in src:
    print("[wrap] [ALREADY] the NO-OP wrap is already on disk -- the file is "
          "left UNCHANGED (a resumed cycle must not double-apply)")
    # still re-verify the landing, so [ALREADY] is not an unverified claim
    ast.parse(src)
    print("[wrap] [ALREADY] the file PARSES")
    raise SystemExit(0)

# ---- 1. MEASURE the region's boundaries from UNIQUE anchors ----
si = [i for i, ln in enumerate(lines) if ln.strip() == START_ANCHOR.strip()]
ei = [i for i, ln in enumerate(lines) if ln.strip() == END_ANCHOR.strip()]
assert len(si) == 1, (f"[wrap] the START anchor occurs {len(si)} times -- it "
                      "must be UNIQUE")
assert len(ei) == 1, (f"[wrap] the END anchor occurs {len(ei)} times -- it "
                      "must be UNIQUE")
assert ei[0] > si[0], "[wrap] the END anchor precedes the START anchor"
region = lines[si[0]:ei[0]]
assert len(region) > 60, (
    f"[wrap] the region is only {len(region)} lines -- that is far shorter "
    "than the re-scoring block, so an anchor has probably moved")
print(f"[wrap] the region is lines {si[0]+1}..{ei[0]} "
      f"({len(region)} lines), measured from UNIQUE anchors")

# ---- 2. the NO-OP branch, and the `else:` ----
noop_branch = [
    "# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX (ported from 1260): **THE RE-SCORING BLOCK IS\n"
    "# NOT EXERCISED ON A MEASURED NO-OP.**  ⭐⭐⭐⭐⭐ There are ZERO published\n"
    "# records to re-score, so loading the instrument and proving it can fire\n"
    "# would be a **VACUOUS verification** -- it would prove the instrument\n"
    "# works, and say nothing about the zero. ⭐⭐⭐⭐⭐ THE NO-OP's PROOF is the\n"
    "# ZERO's OWN cross-check: the adjudication judged a NON-EMPTY candidate\n"
    "# set and at least one candidate resolved 200 (asserted above).\n",
    "if _IS_NOOP:\n",
    "    _DEFECT_COUNTS = {}\n",
    "    _N_ZERO = 0\n",
    "    _N_DEFECTIVE = 0\n",
    "    print(\"[commit] (NO-OP) no record was published, so the re-scoring \"\n",
    "          \"instrument was NOT loaded -- loading it would be a VACUOUS \"\n",
    "          \"verification of the zero\")\n",
    "else:\n",
]

# ---- 3. re-indent EVERY line of the region by four spaces ----
indented = []
for ln in region:
    if ln.strip() == "":
        indented.append(ln)
    else:
        indented.append("    " + ln)

out = lines[:si[0]] + noop_branch + indented + lines[ei[0]:]
P.write_text("".join(out), encoding="utf-8")

# ---- 4. RE-READ FROM DISK and prove the wrap landed ----
disk = P.read_text(encoding="utf-8")
ast.parse(disk)
assert "if _IS_NOOP:\n    _DEFECT_COUNTS = {}" in disk, (
    "[wrap] ABORT: the NO-OP branch is not on disk -- the transform did not "
    "land")
# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX: **NARROW THE `else:` ASSERTION TO THE ONE THIS
# TRANSFORM INSERTED.**  ⭐⭐⭐⭐⭐ The `else:` the transform inserted is
# immediately followed by the region's FIRST line (the `import
# importlib.util` line).  So the `else:` is LOCATED BY THAT ANCHOR -- NOT
# by a global uniqueness requirement, which forbids a perfectly valid file
# that has several column-0 `else:` branches.
_dl = disk.splitlines()
# ⭐⭐⭐⭐⭐ AFTER THE WRAP the region's first line is INDENTED by four
# spaces (that is the whole point of the transform) -- so the anchor is
# located IN ITS INDENTED FORM.  ⭐⭐⭐⭐⭐ The pre-wrap form was located at
# column 0 above (`si`), which is what made the region boundary
# measurable in the first place.
_IND_START = "    " + START_ANCHOR
_ins = [i for i, ln in enumerate(_dl) if ln == _IND_START]
assert len(_ins) == 1, (
    f"[wrap] the indented START anchor occurs {len(_ins)} times after the "
    f"wrap -- it must be UNIQUE")
_ei = _ins[0] - 1
assert _dl[_ei] == "else:", (
    f"[wrap] the line before the region's first line is not the inserted "
    f"`else:` -- got {_dl[_ei]!r}")
# ⭐⭐⭐ AND THE `else:` MUST BE THE ONE THE TRANSFORM INSERTED -- i.e. the
# NO-OP branch must be immediately above it.
assert _dl[_ei - 1].strip() == '"verification of the zero")', (
    f"[wrap] the inserted `else:` is not preceded by the NO-OP branch's last "
    f"line -- got {_dl[_ei-1]!r}")
print(f"[wrap] the inserted `else:` is at line {_ei+1}, LOCATED BY THE "
      "ANCHOR that follows it (NOT by a global uniqueness requirement)")
assert _dl[_ei + 1] == _IND_START, (
    f"[wrap] the region's first line is not indented under the `else:` -- "
    f"got {_dl[_ei+1]!r}")
# ⭐⭐⭐⭐⭐ THE BODY'S FIRST `def` IS **NOT** NECESSARILY THE LINE RIGHT
# AFTER THE IMPORT -- there can be blank lines between them (the region is
# copied VERBATIM, blanks included).  ⭐⭐⭐⭐⭐ So the check SKIPS BLANK
# LINES rather than assuming adjacency -- an assertion that assumes
# adjacency would fire on a perfectly correct re-indent.
_bi = _ei + 2
while _bi < len(_dl) and _dl[_bi].strip() == "":
    _bi += 1
assert _bi < len(_dl) and _dl[_bi].startswith("    def _load_module("), (
    f"[wrap] the region's body was NOT re-indented -- got "
    f"{_dl[_bi]!r}")
print(f"[wrap] the region's body starts with the re-indented `def "
      f"_load_module(` at line {_bi+1}")
# the END anchor must be back at column 0 (it is OUTSIDE the else)
_ej = [i for i, ln in enumerate(_dl) if ln.strip() == END_ANCHOR]
assert len(_ej) == 1 and _dl[_ej[0]] == END_ANCHOR, (
    f"[wrap] the END anchor is not at column 0 any more: {_dl[_ej[0]]!r}")
# ⭐⭐⭐⭐⭐ AND THE REGION's LINE COUNT MUST BE **PRESERVED**: the re-indent
# adds no lines and removes none, so the region's line count must equal the
# measured one -- a lost or duplicated line would change it.
_region_now = _dl[_ei + 1:_ej[0]]
assert len(_region_now) == len(region), (
    f"[wrap] the region's line count CHANGED: {len(region)} -> "
    f"{len(_region_now)} -- a line was lost or duplicated")
print(f"[wrap] the wrap landed and the file PARSES")
print(f"[wrap] the END anchor is back at column 0 (line {_ej[0]+1})")
print(f"[wrap] the region's line count is PRESERVED ({len(region)} lines)")
print("  ⭐⭐⭐⭐⭐ THE RE-INDENTATION WAS DONE BY THE SCRIPT, NOT BY HAND -- "
      "a hand-typed re-indent of a ~90-line region is exactly the kind of "
      "edit that silently drops or duplicates a line.")
print("  ⭐⭐⭐⭐⭐ AND THE WRAP WAS VERIFIED BY RE-READING THE FILE FROM "
      "DISK -- a discarded transform is a silent no-op.")
print("  ⭐⭐⭐⭐⭐ AND THE `else:` ASSERTION IS **NARROWED TO THE ONE THIS "
      "TRANSFORM INSERTED** (located by the anchor that follows it) -- "
      "cycle 1260's verification demanded a GLOBALLY UNIQUE column-0 "
      "`else:`, which FORBIDS a perfectly valid file with several `else:` "
      "branches. ⭐⭐⭐⭐⭐ **THE VERIFICATION WAS TOO STRICT, NOT THE "
      "CODE.**")
