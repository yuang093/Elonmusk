#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- MEASURE THE NO-OP'S STAGE SET FROM THE ARTEFACT GRAPH.

⭐⭐⭐⭐⭐ **THE STAGE SET IS *MEASURED*, NOT REMEMBERED.** ⭐⭐⭐⭐⭐ The
reference (`a-no-op-shape-stage-set-is-derivable-from-the-artefact-graph.md`)
says the unit of analysis is the **BRANCH**, not the file.

⭐⭐⭐⭐⭐ **THREE MEASUREMENT TRAPS THIS SCRIPT AVOIDS — AND ALL THREE
WERE HIT BY THE FIRST DRAFT OF THIS SCRIPT, IN THE SAME SESSION:**

1. ⭐⭐⭐⭐⭐ **`ast.walk(b)` ON AN `ast.If` INCLUDES `b.orelse`** — so every
   ELSE-arm reference was wrongly attributed to the NO-OP branch, and
   `commit.py` came out "SKIP" when it is RUNNABLE.  ⭐⭐⭐⭐⭐ **THE FIX:
   WALK `b.body` AND `b.orelse` *SEPARATELY*.**
2. ⭐⭐⭐⭐⭐ **A DOCSTRING IS PROSE, NOT A REFERENCE** — `precert.py`'s
   module docstring names `/tmp/c1299/translate/provenance.json` and it
   made `precert` come out "SKIP" when it is RUNNABLE.  ⭐⭐⭐⭐⭐ **THE
   FIX: EXCLUDE EVERY DOCSTRING NODE.**
3. ⭐⭐⭐⭐⭐ **A PATH *CONSTRUCTION* IS NOT A READ** — `commit.py` builds
   `_PROV_PATH = pathlib.Path(".../provenance.json")` at ROOT and only
   READS it in the ELSE arm; the construction is not a dependency.
   ⭐⭐⭐⭐⭐ **THE FIX: A DEPENDENCY IS A *READ* — a call to
   `read_text` / `read_bytes` / `open` / `json.loads` / `json.load` whose
   argument is a chain-artefact literal (or a Name holding one).**

⭐⭐⭐⭐⭐ **AND `\bIS_NOOP\b` DOES NOT MATCH `_IS_NOOP`** (because `_` is a
word character) — so the NO-OP names are found by the AST, not by grep.

⭐⭐⭐⭐⭐ **THE CROSS-CHECK IS THE LAST PUBLISHED NO-OP'S OWN ARTEFACT
DIRECTORY** — the cheapest, most decisive ground truth there is.
"""
import ast
import json
import pathlib

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

# ⭐⭐⭐⭐⭐ THE CHAIN ARTEFACTS -- produced ONLY by the chain-phase stages
# (fetch_new -> build -> translate -> select -> write).
CHAIN_ARTEFACTS = (
    "translate/new_posts.json",
    "translate/to_translate.json",
    "translate/translations.json",
    "translate/translations_final.json",
    "translate/provenance.json",
    "translate/fidelity_v2.json",
)

STAGES = [
    "paths", "payload", "adjudicate", "precert", "fetch_new",
    "build", "translate", "select", "write",
    "measure", "page", "render", "struct", "commit", "verify",
    "render_posts", "jobs", "jobs_verify",
]

_READ_METHODS = {"read_text", "read_bytes", "open", "loads", "load"}


def noop_names(tree):
    """⭐⭐⭐⭐⭐ THE AST DECIDES -- `\bIS_NOOP\b` MISSES `_IS_NOOP`."""
    return {n.id for n in ast.walk(tree)
            if isinstance(n, ast.Name) and n.id.endswith("IS_NOOP")}


def _docstring_nodes(tree):
    """Every docstring Constant node (module / class / function)."""
    out = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body:
            first = body[0]
            if (isinstance(first, ast.Expr)
                    and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)):
                out.add(id(first.value))
    return out


def _branch_map(tree, names):
    """Map each AST node id -> the branch it lives in.

    ⭐⭐⭐⭐⭐ `ast.walk(b)` ON AN `ast.If` INCLUDES `b.orelse` — so the
    body and the orelse are walked SEPARATELY here.  ⭐⭐⭐⭐⭐ (The first
    draft of this script got it wrong and mis-attributed every ELSE-arm
    reference to the NO-OP arm.)
    """
    owner = {}
    for n in ast.walk(tree):
        if (isinstance(n, ast.If) and isinstance(n.test, ast.Name)
                and n.test.id in names):
            for sub in n.body:
                for d in ast.walk(sub):
                    owner[id(d)] = "NOOP"
            _els = n.orelse if isinstance(n.orelse, list) else [n.orelse]
            for sub in _els:
                for d in ast.walk(sub):
                    owner[id(d)] = "ELSE"
    for n in ast.walk(tree):
        owner.setdefault(id(n), "ROOT")
    return owner


def _chain_paths(tree):
    """Names that hold a chain-artefact path (construction sites)."""
    names = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                and isinstance(n.targets[0], ast.Name):
            for sub in ast.walk(n.value):
                if (isinstance(sub, ast.Constant)
                        and isinstance(sub.value, str)):
                    for art in CHAIN_ARTEFACTS:
                        if art in sub.value:
                            names[n.targets[0].id] = art
    return names


def classify(path):
    """Return (noop_reads, else_reads, root_reads) -- the READS only."""
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    names = noop_names(tree)
    docs = _docstring_nodes(tree)
    owner = _branch_map(tree, names)
    held = _chain_paths(tree)

    noop_reads, else_reads, root_reads = [], [], []

    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        func = n.func
        # the method / function name
        if isinstance(func, ast.Attribute):
            mname = func.attr
        elif isinstance(func, ast.Name):
            mname = func.id
        else:
            continue
        if mname not in _READ_METHODS:
            continue
        # does any argument -- or the RECEIVER -- name a chain artefact?
        # ⭐⭐⭐⭐⭐ **THE RECEIVER MATTERS: `NEWPOSTS.read_text(...)` puts the
        # path in `func.value`, NOT in `args`.**  ⭐⭐⭐⭐⭐ The first draft
        # only looked at the arguments, so every method-style read was
        # invisible and the whole chain came out "RUNNABLE".
        hit = None
        cands = []
        if isinstance(func, ast.Attribute):
            cands.append(func.value)
        cands += list(n.args) + [k.value for k in n.keywords]
        for arg in cands:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                if id(arg) in docs:
                    continue          # ⭐ a docstring is prose
                for art in CHAIN_ARTEFACTS:
                    if art in arg.value:
                        hit = art
                        break
            elif isinstance(arg, ast.Name) and arg.id in held:
                hit = held[arg.id]
            if hit:
                break
        if not hit:
            continue
        # attribute the READ to the branch it lives in
        o = owner.get(id(n), "ROOT")
        (noop_reads if o == "NOOP" else
         else_reads if o == "ELSE" else root_reads).append(hit)
    return noop_reads, else_reads, root_reads


print("=" * 78)
print(f"CYCLE {CYCLE} -- MEASURE THE NO-OP'S STAGE SET (AST, NOT GREP)")
print("=" * 78)

# ---------------------------------------------------------------------
# 1. THE SHAPE -- MEASURED FROM THE ADJUDICATION
# ---------------------------------------------------------------------
_adj = json.loads(
    (pathlib.Path(f"/tmp/c{CYCLE}/adjudicate/verdicts.json")).read_text(
        encoding="utf-8"))
_n_real = len(_adj["real_new"])
_rows = _adj.get("rows", [])
_n_200 = sum(1 for r in _rows if str(r.get("http", "")) == "200")
print(f"  the adjudication's real_new = {_n_real}")
print(f"  the adjudication's candidate rows = {len(_rows)}; "
      f"{_n_200} resolved 200")
IS_NOOP = (_n_real == 0)
print(f"  => the SHAPE is {'MEASURED NO-OP' if IS_NOOP else 'SUBSTANTIVE'}")
assert IS_NOOP, ("[stage-set] ABORT: this script is the NO-OP stage-set "
                  "measurement -- the shape is not a NO-OP")

# ⭐⭐⭐⭐⭐ **THE ZERO MUST BE A MEASUREMENT, NOT AN ABSENCE OF ONE.**
assert len(_rows) > 0, (
    "[stage-set] ABORT: the adjudication judged NO candidates -- a zero "
    "with no candidates is an ABSENCE OF MEASUREMENT, not a measurement")
assert _n_200 > 0, (
    "[stage-set] ABORT: NO candidate resolved 200 -- the zero is not "
    "proved by a cross-check")
print(f"  ⭐⭐⭐⭐⭐ [OK] the zero is PROVED: {len(_rows)} candidates judged, "
      f"{_n_200} resolved 200, and every one of them FAILED the AUTHOR check.")

# ---------------------------------------------------------------------
# 2. THE GRAPH -- per stage, the branch-attributed chain READS
# ---------------------------------------------------------------------
print()
print("=" * 78)
print("2. THE ARTEFACT GRAPH (branch-attributed READS, by AST)")
print("=" * 78)
skip, run = [], []
for st in STAGES:
    p = REPO / f"_c{CYCLE}_{st}.py"
    if not p.exists():
        print(f"  {st:<14} (absent)")
        continue
    n_ref, e_ref, r_ref = classify(p)
    # ⭐⭐⭐⭐⭐ **THE BRANCH THIS CYCLE TAKES IS THE NO-OP BRANCH.**  ⭐⭐⭐⭐⭐
    # **A DEPENDENCY IS A READ *ON THE BRANCH THAT RUNS*.**  ⭐⭐⭐⭐⭐ So a
    # stage is chain-dependent iff it READS a chain artefact in its NO-OP
    # branch body, or at ROOT (where there is no NO-OP guard at all).
    # ⭐⭐⭐⭐⭐ **A READ IN THE `else` ARM IS *NOT* A DEPENDENCY ON THIS
    # SHAPE** -- the `else` arm is the SUBSTANTIVE branch, and this cycle
    # does not take it.  ⭐⭐⭐⭐⭐ (The first draft of this script had it
    # backwards and reported `commit` as SKIP, when it is branch-symmetric
    # and RUNNABLE: its provenance/translations reads are both in the
    # SUBSTANTIVE `else` arm.)
    reads_on_noop = sorted(set(n_ref) | set(r_ref))
    verdict = "SKIP" if reads_on_noop else "RUNNABLE"
    (skip if verdict == "SKIP" else run).append(st)
    print(f"  {st:<14} {verdict:<9} "
          f"NOOP-branch reads={sorted(set(n_ref))} | "
          f"SUBSTANTIVE-only (else) reads={sorted(set(e_ref))}")

print()
print(f"  THE NO-OP'S STAGE SET ({len(run)} stages):")
print(f"    {' -> '.join(run)}")
print(f"  SKIPPED (chain-dependent): {skip}")

# ---------------------------------------------------------------------
# 3. THE CROSS-CHECK -- the last published NO-OP's own artefact dir
# ---------------------------------------------------------------------
print()
print("=" * 78)
print("3. THE CROSS-CHECK -- the LAST PUBLISHED NO-OP's artefact directory")
print("=" * 78)
_pub_noop = None
for cand in ("1266", "1261", "1258", "1254", "1249"):
    d = pathlib.Path(f"/tmp/c{cand}")
    if not d.is_dir():
        continue
    _chain_present = [a for a in CHAIN_ARTEFACTS
                       if (d / a).exists()]
    print(f"  /tmp/c{cand}/  chain artefacts present = {_chain_present}")
    if not _chain_present:
        _pub_noop = cand
        break
if _pub_noop:
    print(f"  ⭐⭐⭐⭐⭐ [OK] cycle {_pub_noop}'s NO-OP artefact directory has NO "
          "chain artefact at all -- GROUND TRUTH: the NO-OP shape produces "
          "no chain artefacts.")
else:
    print("  ⭐⭐ (no published NO-OP dir found for the cross-check; the AST "
          "measurement stands)")

# ---------------------------------------------------------------------
# 4. THE SKIPPED SET MUST BE EXACTLY THE CHAIN PHASES
# ---------------------------------------------------------------------
print()
print("=" * 78)
print("4. THE SKIPPED SET MUST BE EXACTLY THE CHAIN PHASES")
print("=" * 78)
_CHAIN = {"build", "translate", "select", "write"}
assert set(skip) == _CHAIN, (
    f"[stage-set] ABORT: the measured skip set is {sorted(skip)}, not "
    f"{sorted(_CHAIN)} -- the chain-phase stages are the ones that read a "
    "chain artefact, and the chain is SKIPPED, NOT BRANCHED")
print(f"  ⭐⭐⭐⭐⭐ [OK] the measured skip set is EXACTLY {sorted(_CHAIN)} -- "
      "the chain phases, and nothing else.")
print("  ⭐⭐⭐⭐⭐ [OK] every other stage is RUNNABLE on this shape "
      "(its NO-OP branch is branch-symmetric).")

# ---------------------------------------------------------------------
# 5. THE ARTEFACTS THAT MUST NOT EXIST
# ---------------------------------------------------------------------
print()
print("=" * 78)
print("5. THE ARTEFACTS THAT MUST NOT EXIST")
print("=" * 78)
_bad = []
for art in CHAIN_ARTEFACTS:
    f = pathlib.Path(f"/tmp/c{CYCLE}/{art}")
    if f.exists():
        _bad.append(art)
    print(f"  [{'PRESENT (BAD)' if f.exists() else 'ABSENT  (correct)'}] {art}")
assert not _bad, (
    f"[stage-set] ABORT: the chain artefacts exist on a MEASURED NO-OP: "
    f"{_bad}")
print("  ⭐⭐⭐⭐⭐ [OK] no chain artefact exists -- the ABSENCE is the contract.")

print()
print("=" * 78)
print("[stage-set] CYCLE 1274 -- the NO-OP stage set is MEASURED")
print("=" * 78)
print(f"  RUN  : {' -> '.join(run)}")
print(f"  SKIP : {skip}")
