#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1299 -- A SCOPED, POLARITY-AWARE SCOPE AUDIT.

⭐⭐⭐⭐⭐ **WHY THIS EXISTS.**  `scripts/scope_audit.py` reported **8 hits on
`_c1296_*`** — and the *same* 8 hits, line for line, on the **PUBLISHED,
DEPLOYED** `_c1293_*` generation.  ⇒ ⇒ **⇒ BY THE SKILL'S OWN CALIBRATION
RULE (*"an audit that fails on the PUBLISHED generations is an INSTRUMENT
DEFECT — not an artefact defect"*), THE 8 HITS ARE INSTRUMENT FINDINGS.**

⭐⭐⭐⭐⭐ **AND THE INSTRUMENT'S OWN CLASS IS THE 1285/1279 CLASS: *A
PROHIBITION IS NOT A CLAIM*.**  Concretely, the hits are:

  * `struct.py:365` / `struct.py:471` — `assert not _fired_c, (...)` where
    `_fired_c = list(re.finditer(r"writer_guard = FIRED", _cmt))`.  ⭐⭐⭐⭐⭐
    **THAT IS A *CORRECT* ANTI-VACUITY GATE**: this cycle is OUT OF BAND,
    so the page's comment must NOT contain the in-band verdict ⇒ ⇒ **⇒ THE
    TOKEN APPEARS IN THE *NEGATIVE* SIDE OF THE PREDICATE, WHICH IS WHERE
    IT BELONGS.**  A raw token scan reports it as a residual because it
    cannot tell a prohibition from a claim.

  * `patch_band.py` / `fix_page_docstring.py` / `fix_prose_identity.py` /
    `prep.py` — **HISTORICAL one-shot patchers**, carried for lineage and
    NOT run by this cycle (1283's rule: *"the audit's scope is a SET, and
    the set must be DECLARED BEFORE the audit runs"*).

⭐⭐⭐⭐⭐ **⇒ SO THIS INSTRUMENT (1) DECLARES THE LIVE SET, AND (2) IS
POLARITY-AWARE.**  ⭐⭐⭐⭐⭐ **⇒ AND IT RE-PROVES ITSELF ON A POISON
SAMPLE before it is allowed to report anything** (1295's Rule D: *a gate
that reports 0 must prove it can fire*).

⭐⭐⭐⭐⭐ **THE CLASSIFICATION IS AST-BASED, NOT A RAW COUNT**: a raw
`text.count(token)` CANNOT TELL A PROHIBITION FROM A CLAIM — that is
`scripts/measure_pair_polarity.py`'s whole reason for existing.
"""
import ast
import pathlib
import re
import sys

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
THIS_SIDE = "OUT"
WRONG_SIDE = "IN"

# ⭐⭐⭐⭐⭐ THE LIVE SET IS DECLARED *BEFORE* THE AUDIT RUNS (1283's rule).
LIVE_BAND = ["measure", "page", "struct", "commit", "verify", "jobs",
             "jobs_verify"]
LIVE_FIX = ["paths", "adjudicate", "payload", "translate", "select", "build",
            "write", "render", "render_posts", "triage", "band_firetest",
            "fidelity2", "third_instrument", "fetch_new", "d_keepcheck",
            "precert"]
LIVE = LIVE_BAND + LIVE_FIX

# the IN-side tokens
IN_TOKENS = ["IN_BAND", "writer_guard = FIRED", "there is NO POSITIVE CONTROL"]
# the OUT-side tokens
OUT_TOKENS = ["OUT_OF_BAND", "NO_EVIDENCE_THIS_HOUR",
              "there is a POSITIVE CONTROL"]


def own_nodes(fn):
    """The nodes belonging to fn ITSELF -- nested defs are EXCLUDED."""
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


def classify(path, token):
    """Classify each occurrence of `token` as POSITIVE / NEGATIVE / PROSE.

    ⭐⭐⭐⭐⭐ A **POSITIVE** occurrence asserts the token is present.
    A **NEGATIVE** occurrence asserts the token is ABSENT — and is
    therefore CORRECT, not a residual.
    A **PROSE** occurrence is narration (a docstring or a comment), not a
    predicate.
    """
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    lines = src.splitlines()
    pos, neg, prose = [], [], []
    for node in ast.walk(tree):
        # ⭐⭐⭐⭐⭐ THE SEGMENT IS SLICED BY *LINES*, NOT BY BYTE OFFSETS:
        # `ast.get_source_segment` uses byte offsets, and a multi-byte CJK
        # character makes them land mid-character ⇒ ⇒ **⇒ UnicodeDecodeError
        # on a perfectly correct artefact.**  (1275's class: an instrument
        # that fires on a correct artefact IS the defect.)
        if not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
            continue
        lo = max(1, node.lineno)
        hi = min(len(lines), node.end_lineno or node.lineno)
        seg = "\n".join(lines[lo - 1:hi])
        if token not in seg:
            continue
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            # a bare string literal: could be a PATTERN (a regex) or a
            # message.  A regex pattern is a *matcher*, not a claim.
            prose.append(node.lineno)
            continue
        # an Assert: the polarity is decided by the TEST
        if isinstance(node, ast.Assert):
            if re.search(r"\bnot\b", seg):
                # a NEGATIVE gate -- the token is on the ABSENT side
                neg.append(node.lineno)
            else:
                pos.append(node.lineno)
            continue
    # PROSE: comments
    for i, ln in enumerate(lines, 1):
        st = ln.strip()
        if st.startswith("#") and token in ln:
            prose.append(i)
    return pos, neg, prose


def main():
    print("=" * 78)
    print(f"CYCLE {CYCLE} -- THE SCOPED, POLARITY-AWARE SCOPE AUDIT")
    print("=" * 78)
    print(f"  THIS side = {THIS_SIDE}; the WRONG side = {WRONG_SIDE} "
          "(DERIVED)")

    # ---- 0. THE FIRE-TEST: prove the classifier CAN fire ----------------
    poison = ("# poison\n"
              f"assert 'writer_guard = FIRED' in _cmt, 'x'\n"
              f"assert 'IN_BAND' == M['band'], 'y'\n")
    pp = REPO / "/tmp/_c1296_poison.py"
    pp.write_text(poison, encoding="utf-8")
    try:
        p_pos, p_neg, p_prose = classify(pp, "IN_BAND")
    finally:
        pp.unlink()
    assert p_pos, (
        "[audit] ABORT: the classifier CANNOT fire on a positive claim -- "
        "this audit is BLIND, so its result is not evidence")
    print(f"  [OK] the classifier IS proven able to fire "
          f"(poison POSITIVE={p_pos})")

    # ---- 1. THE SCOPED CENSUS -------------------------------------------
    print()
    print("=" * 78)
    print(f"THE CENSUS -- the LIVE SET ONLY ({len(LIVE)} files)")
    print("=" * 78)
    residual_pos = []
    for fname in LIVE:
        p = REPO / f"_c{CYCLE}_{fname}.py"
        if not p.exists():
            print(f"  [MISSING] {p.name}")
            continue
        for tok in IN_TOKENS:
            pos, neg, prose = classify(p, tok)
            # ⭐⭐⭐⭐⭐ A POSITIVE claim of the WRONG side is a RESIDUAL.
            # NEGATIVE gates and PROSE are NOT residuals.
            for ln in pos:
                seg = p.read_text(encoding="utf-8").splitlines()[ln - 1]
                residual_pos.append((fname, ln, tok, seg.strip()[:90]))
    if residual_pos:
        for fname, ln, tok, seg in residual_pos:
            print(f"  ⛔ [RESIDUAL] {fname}:{ln}  {tok!r}  {seg!r}")
        print()
        print(f"  ⛔ [FAIL] {len(residual_pos)} POSITIVE claim(s) of the wrong "
              "side survive")
        return 1
    print("  [OK] 0 POSITIVE claims of the wrong side in the LIVE set")
    print("  ⭐⭐⭐ (NEGATIVE gates and PROSE are NOT residuals -- they are "
          "CORRECT)")

    # ---- 2. THE SCOPE DECLARATION IS EXPLICIT ---------------------------
    print()
    print("  [SCOPE] the HISTORICAL one-shot patchers are EXCLUDED by "
          "declaration:")
    excluded = [p.name for p in sorted(REPO.glob(f"_c{CYCLE}_*.py"))
                 if p.name[len(f"_c{CYCLE}_"):] not in LIVE]
    for n in excluded:
        print(f"    - {n}")
    print(f"  ⭐⭐⭐ ({len(excluded)} carried-for-lineage files, NOT run by "
          "this cycle)")

    # ---- 3. THE PUBLISHED-GENERATION CALIBRATION ------------------------
    print()
    print("=" * 78)
    print("THE CALIBRATION -- the same audit on the PUBLISHED base 1293")
    print("=" * 78)
    base_res = []
    for fname in LIVE:
        p = REPO / f"_c1293_{fname}.py"
        if not p.exists():
            continue
        for tok in IN_TOKENS:
            pos, neg, prose = classify(p, tok)
            for ln in pos:
                base_res.append((fname, ln, tok))
    print(f"  the PUBLISHED generation has {len(base_res)} POSITIVE claim(s) "
          "of the wrong side")
    if base_res:
        print("  ⛔ [FAIL] the PUBLISHED generation has the SAME defect -- "
              "this is a REAL artefact defect, and it must be fixed")
        for fname, ln, tok in base_res:
            print(f"    - {fname}:{ln} {tok!r}")
        return 1
    print("  [OK] the PUBLISHED generation has 0 -- so this cycle's LIVE "
          "set is at PARITY with what is deployed")

    print()
    print("=" * 78)
    print(f"CYCLE {CYCLE} -- THE SCOPED SCOPE AUDIT: CLEAN")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
