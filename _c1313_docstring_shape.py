#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- THE DOCSTRING/BODY SHAPE-AGREEMENT INSTRUMENT.

⭐⭐⭐⭐⭐ **THE DEFECT CLASS (cycle 1275's finding (A), in a NEW file):**
a MODULE DOCSTRING whose NARRATIVE IS THE OPPOSITE OF ITS OWN BODY.

⭐⭐⭐⭐⭐ **WHY THIS NEEDS ITS OWN INSTRUMENT — THE PAIR-KEYED VALUE-TOKEN
SWEEP *DELIBERATELY* EXCLUDES DOCSTRINGS.**  Its `live_lines()` strips
every docstring line before scanning, so it answers *"does the LIVE CODE
assert the right polarity?"*.  ⭐⭐⭐⭐⭐ **THIS INSTRUMENT ANSWERS A
DIFFERENT QUESTION: *"does the PROSE NEXT TO THE LIVE CODE assert the same
polarity?"*  ⭐⭐⭐⭐⭐ **⇒ THE TWO MUST AGREE, because a docstring is a
PUBLICATION even though no assertion reads it** (cycle 1276's finding).

⭐⭐⭐⭐⭐ **THE CORRECT SHAPE IS MEASURED, NEVER TYPED:** the band comes from
`fetch_tweets.py`'s own `RETRY_TRANSLATION_HOURS`; this cycle's hour from
this cycle's own `measure.py`; the prior cycle's identity AND hour from
HEAD's committed page — the same three sources the pair-keyed sweep uses,
so the two instruments cannot disagree about what the shape IS.

⭐⭐⭐⭐⭐ **⇒ THIS CYCLE'S EXPECTATION IS (OUT, IN) -> "FLIPS"** — and it is
MEASURED, not typed: the prior COMMITTED cycle 1277 was Hour 11 (OUT) and
this cycle is Hour 12 (IN).

⭐⭐⭐⭐⭐ **⭐⭐⭐⭐⭐ AND THE INSTRUMENT'S CONTRACT MUST BE HONOURED FOR THIS
CYCLE'S PAIR:** a docstring's *narrative about a HISTORICAL cycle* (e.g.
"the (OUT, IN) PAIR: the prior COMMITTED cycle was IN BAND" as an
EXPLANATION OF WHY A FIX EXISTS) is NOT this cycle's claim.  ⭐⭐⭐⭐⭐ **⇒
THE CLAIM PATTERNS ARE ANCHORED ON *THIS CYCLE'S* SUBJECT** ("THIS cycle
is ...", "**(...)** PAIR" as a self-description) and the instrument REQUIRES
a negative control (a poisoned docstring) to prove it can fire.

⭐⭐⭐⭐⭐ **⭐⭐⭐⭐⭐ AND A *SHAPE-SCOPED* DOCSTRING IS NOT A DEFECT.**  ⭐⭐⭐⭐⭐
`page.py` and `measure.py` carry **THIS CYCLE'S OWN NARRATIVE** — they
name this cycle's hour, band and guard verdict, and that is CORRECT (it
is what the body computes).  ⭐⭐⭐⭐⭐ **⇒ THE INSTRUMENT MUST NOT FLAG
A DOCSTRING THAT NAMES THIS CYCLE'S OWN SIDE** — it must only flag a
docstring that names the **WRONG** side.  ⭐⭐⭐⭐⭐ **⇒ THE `CLAIM_BAND`
PATTERN IS THEREFORE SCOPED TO "THIS cycle is ..."** — and `page.py` /
`measure.py`'s narratives use the form "HOUR212 IS **IN BAND**",
which is NOT a "THIS cycle is" claim, so it is not flagged either way.
⭐⭐⭐⭐⭐ **⇒ THE INSTRUMENT ANSWERS "IS THE CLAIM *WRONG*?", NEVER "DOES
IT CLAIM?"** — that is the difference between a defect detector and a
shape census.
"""
import ast
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

# =====================================================================
# 1. THE CORRECT SHAPE -- MEASURED, NOT TYPED
# =====================================================================
_ft = (REPO / "fetch_tweets.py").read_text(encoding="utf-8")
_bm = re.search(r"RETRY_TRANSLATION_HOURS\s*=\s*\{([^}]*)\}", _ft)
assert _bm, "[docshape] could not read RETRY_TRANSLATION_HOURS"
BAND = {int(x) for x in re.findall(r"\d+", _bm.group(1))}

_m = re.search(r"(?m)^CYCLE_HOUR_UTC\s*=\s*(\d+)\s*$",
               (REPO / f"_c{CYCLE}_measure.py").read_text(encoding="utf-8"))
assert _m, "[docshape] could not read the clone's CYCLE_HOUR_UTC"
HOUR = int(_m.group(1))
IN_BAND = HOUR in BAND

_page = subprocess.run(["git", "show", "HEAD:index.html"], cwd=str(REPO),
                       capture_output=True, text=True).stdout
_cmt = re.search(r"<!--\s*cron cycle (\d+):(.*?)-->", _page, re.S)
assert _cmt, "[docshape] could not read HEAD's cycle comment"
PRIOR = _cmt.group(1)
_hm = re.search(r"=\s*Hour (\d{1,2}) UTC", _cmt.group(2))
assert _hm, "[docshape] HEAD's cycle comment carries no `= Hour NN UTC`"
PRIOR_HOUR = int(_hm.group(1))
PRIOR_IN_BAND = PRIOR_HOUR in BAND

PAIR = ("IN" if PRIOR_IN_BAND else "OUT", "IN" if IN_BAND else "OUT")
FLIPS = PAIR[0] != PAIR[1]
EXPECT_PHRASE = "FLIPS" if FLIPS else "UNCHANGED"
EXPECT_BAND = "IN" if IN_BAND else "OUT"

print("=" * 78)
print(f"CYCLE {CYCLE} -- THE DOCSTRING/BODY SHAPE-AGREEMENT INSTRUMENT")
print("=" * 78)
print(f"  this cycle: hour {HOUR} -> {'IN' if IN_BAND else 'OUT OF'} BAND")
print(f"  prior COMMITTED {PRIOR}: hour {PRIOR_HOUR} -> "
      f"{'IN' if PRIOR_IN_BAND else 'OUT OF'} BAND")
print(f"  => PAIR {PAIR} -> the correct phrase is {EXPECT_PHRASE!r}, "
      f"the correct band is {EXPECT_BAND!r}")


# =====================================================================
# 2. THE CLAIM PATTERNS -- ANCHORED ON *THIS CYCLE'S* SUBJECT
# =====================================================================
# ⭐⭐⭐⭐⭐ **A HISTORICAL CITATION IS NOT A CLAIM.**  The patterns below are
# deliberately narrow:
#   * `CLAIM_BAND` requires the words "THIS cycle"/"this cycle" — a
#     docstring that says "the prior COMMITTED cycle was OUT OF BAND" is
#     making a statement ABOUT THE PRIOR, not about this cycle;
#   * `CLAIM_PAIR` requires the "**(X, Y)** PAIR" SELF-DESCRIPTION form;
#   * `CLAIM_PHRASE` fires on any "control set FLIPS" / "control set is
#     UNCHANGED" — and that one IS a claim about this cycle's published
#     prose, because the control set's state IS this cycle's shape.
CLAIM_PHRASE = re.compile(r"control set (?:FLIPS|is UNCHANGED)")
CLAIM_BAND = re.compile(r"\b[Tt][Hh][Ii][Ss] cycle is (IN|OUT) BAND\b")
CLAIM_PAIR = re.compile(r"\*\*\((\w+),\s*(\w+)\)\*\* PAIR")

FILES = ["measure", "page", "struct", "commit", "verify", "jobs",
         "jobs_verify", "paths", "payload", "adjudicate", "precert",
         "fetch_new", "select", "build", "write", "render", "render_posts",
         "translate", "triage", "band_firetest", "fidelity2",
         "third_instrument", "d_keepcheck"]


def doc_lines(path):
    """(lineno, text) for the module docstring, as written in the file."""
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    body = tree.body
    if not body or not isinstance(body[0], ast.Expr):
        return []
    node = body[0].value
    if not isinstance(node, ast.Constant):
        return []
    lines = src.splitlines()
    return [(node.lineno + i, lines[node.lineno - 1 + i])
            for i in range(node.end_lineno - node.lineno + 1)]


def claims_of(doc):
    out = {"phrase": None, "band": None, "pair": None}
    for m in CLAIM_PHRASE.finditer(doc):
        out["phrase"] = "FLIPS" if "FLIPS" in m.group(0) else "UNCHANGED"
    for m in CLAIM_BAND.finditer(doc):
        out["band"] = m.group(1)
    for m in CLAIM_PAIR.finditer(doc):
        out["pair"] = (m.group(1), m.group(2))
    return out


def find_defects(files):
    """The core detector -- shared by the audit AND the fire-test, so the
    fire-test exercises THE SAME CODE PATH (cycle 1267's rule)."""
    defects = []
    for name in files:
        p = REPO / f"_c{CYCLE}_{name}.py"
        if not p.exists():
            continue
        src = p.read_text(encoding="utf-8")
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        doc = ast.get_docstring(tree) or ""
        if not doc:
            continue
        cl = claims_of(doc)
        bad = []
        if cl["phrase"] and cl["phrase"] != EXPECT_PHRASE:
            bad.append(("phrase", cl["phrase"], EXPECT_PHRASE))
        if cl["band"] and cl["band"] != EXPECT_BAND:
            bad.append(("band", cl["band"], EXPECT_BAND))
        if cl["pair"] and cl["pair"] != PAIR:
            bad.append(("pair", str(cl["pair"]), str(PAIR)))
        if bad:
            defects.append((name, bad))
    return defects


# =====================================================================
# 3. THE FIRE-TEST -- THE POISON IS PROGRAMMATICALLY GENERATED
# =====================================================================
# ⭐⭐⭐⭐⭐ **THE FIRE-TEST MUST GO THROUGH THE SAME `find_defects()` PATH
# AS THE AUDIT** (cycle 1267's rule: a fire-test that exercises a
# different path is a DIFFERENT PROGRAM).  ⭐⭐⭐⭐⭐ So the poison is a
# REAL FILE on disk, and the audit is re-run over a file list that
# INCLUDES it.
print()
print("=" * 78)
print("1. THE FIRE-TEST (the instrument must be PROVEN able to fire)")
print("=" * 78)
_poison_dir = pathlib.Path(f"/tmp/c{CYCLE}_docshape")
_poison_dir.mkdir(parents=True, exist_ok=True)
_poison_file = _poison_dir / f"_c{CYCLE}_poison_docstring.py"
# ⭐⭐⭐ THE POISON IS BUILT FROM THE MEASURED EXPECTATION, so it is always
# the OPPOSITE of the truth -- programmatically, never hand-typed.
_poison_phrase = ("control set is UNCHANGED" if EXPECT_PHRASE == "FLIPS"
                  else "control set FLIPS")
_poison_band = "OUT" if EXPECT_BAND == "IN" else "IN"
_poison_src = (
    "#!/usr/bin/env python3\n"
    f'"""CYCLE {CYCLE} -- POISON.\n\n'
    f"THIS cycle is {_poison_band} BAND and the {_poison_phrase}.\n"
    '"""\n'
    "print('poison')\n")
_poison_file.write_text(_poison_src, encoding="utf-8")
# the detector reads `_c{CYCLE}_{name}.py` inside the REPO -- so the poison
# is placed under a name the detector will actually pick up, and removed
# right after.
_poison_in_repo = REPO / f"_c{CYCLE}_poison_docstring.py"
_poison_in_repo.write_text(_poison_src, encoding="utf-8")
try:
    _fired = find_defects(FILES + ["poison_docstring"])
finally:
    _poison_in_repo.unlink(missing_ok=True)
_poison_names = [d[0] for d in _fired]
assert "poison_docstring" in _poison_names, (
    "[docshape] ABORT: the poison did NOT fire -- the instrument cannot "
    "detect a wrong docstring shape, so its CLEAN verdict is NOT TRUSTED")
print(f"  [OK] the poison FIRED (detected in {len(_fired)} file(s), including "
      "the poison)")
print("  ⭐⭐⭐⭐⭐ [OK] the fire-test ran through the SAME `find_defects()` "
      "path as the audit.")

# =====================================================================
# 4. THE AUDIT
# =====================================================================
print()
print("=" * 78)
print("2. THE AUDIT -- each blueprint file's DOCSTRING vs THE CORRECT SHAPE")
print("=" * 78)
defects = find_defects(FILES)
for name in FILES:
    p = REPO / f"_c{CYCLE}_{name}.py"
    if not p.exists():
        continue
    doc = ast.get_docstring(ast.parse(p.read_text(encoding="utf-8"))) or ""
    if not doc:
        continue
    cl = claims_of(doc)
    shown = [f"{k}={v}" for k, v in cl.items() if v is not None]
    print(f"  [{'DEFECT' if any(d[0] == name for d in defects) else 'OK    '}]"
          f"  {name}.py  ({', '.join(shown) if shown else 'no shape claim'})")

print()
print("=" * 78)
print(f"3. RESULT: {len(defects)} file(s) carry a DOCSTRING THAT CONTRADICTS "
      "THE SHAPE ITS OWN BODY IMPLEMENTS")
print("=" * 78)
for name, bad in defects:
    p = REPO / f"_c{CYCLE}_{name}.py"
    print(f"\n  --- {name}.py ---")
    for kind, got, want in bad:
        print(f"    [{kind}] the docstring claims {got!r}; the correct shape "
              f"is {want!r}")
    for i, ln in doc_lines(p):
        if CLAIM_PHRASE.search(ln) or CLAIM_BAND.search(ln) or \
                CLAIM_PAIR.search(ln):
            print(f"    L{i}: {ln.strip()[:130]}")

print()
print(f"DEFECT_FILES = {[d[0] for d in defects]}")
if defects:
    print()
    print("[docshape] RESULT: DEFECTS FOUND -- the fix step must land before "
          "the tail runs.")
    sys.exit(1)
print()
print("[docshape] RESULT: CLEAN -- every docstring agrees with its own body.")
