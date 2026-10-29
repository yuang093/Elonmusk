#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- PORT THE NO-OP BRANCH FIX INTO `commit.py`.

⭐⭐⭐⭐⭐ **THE PORT SOURCE IS A (FILE, PREDICATE) PAIR, NOT A CYCLE**
(Reminder 84).

⭐⭐⭐⭐⭐ **THE SOURCE IS MEASURED COMPLETE BEFORE THE LIFT.**  Cycle
1260's on-disk `commit.py` carries the NO-OP fix's patches 1 / 2 / 3a / 3b
but **NOT** 3c (the branch-symmetric defect sentence), **NOT** 3d (the
branch-symmetric provenance paragraph) and **NOT** 4 (the branch-symmetric
commit message) -- cycle 1260 was INTERRUPTED mid-patch.  ⭐⭐⭐⭐⭐ **SO
1260's `commit.py` IS *HALF-PORTED***, and it is the *COMPLETE* source for
the regions it DOES carry.

⭐⭐⭐⭐⭐ **THE TARGET IS CYCLE 1258's `commit.py`** -- the PUBLISHED
form, which is structurally the PRE-fix shape (patches 1/2/3a/3b are
ABSENT there).  So this port applies the fix to the published base.

⭐⭐⭐⭐⭐ **THE PORT IS A WHOLE-REGION LIFT, NOT A FRAGMENT SPLICE**:
Reminder 82 -- a multi-line `assert` is a *STATEMENT*, not a line, and a
fragment-level port orphans its continuation lines.  So each region's
OLD text is taken VERBATIM from the target and its NEW text is taken
VERBATIM from the source, and each is asserted to occur EXACTLY ONCE in
the target.

⭐⭐⭐⭐⭐ **THE PORT IS IDEMPOTENT** (Reminder 75): a resumed cycle
re-runs its own fix scripts, so an already-applied patch reports
[ALREADY] rather than duplicating the block.

⭐⭐⭐⭐⭐ **THE PORT's ANCHORS ARE PATH-AGNOSTIC -- THE IDENTITY SWEEP
OWNS THE PATH TOKEN.**  ⭐⭐⭐⭐⭐ The fixed order is CLONE → PORT → SWEEP,
and the SWEEP is what rewrites `/tmp/cNNNN` and `_cNNNN_`.  ⭐⭐⭐⭐⭐ **SO A
PORT ANCHOR THAT TYPED THE PATH WOULD BE PINNED TO THE *BASE's* PATH**
(the clone is copied from the base, and the sweep has not run yet) -- and
the anchor would then MISS on a clone whose base differs.  ⭐⭐⭐⭐⭐ **THE
ANCHOR IS THEREFORE MATCHED ON THE PATH-AGNOSTIC PART OF THE REGION, AND
THE PATH IS RECONSTRUCTED FROM THE SWEEP'S OWN RULE** (`/tmp/cNNNN`).

⭐⭐⭐⭐⭐ **REMINDER 63: A DOCSTRING IS PROSE.**  The `NEW` text's prose
is this cycle's own; the `OLD` text's prose is the base's -- and the
prose inside a region the sweep will rewrite is handled by the sweep.
"""
import pathlib
import py_compile
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

applied = already = 0

def patch(fname, old, new, why):
    """Idempotent WHOLE-BLOCK patch with a UNIQUE anchor.

    ⭐⭐⭐ THE ANCHOR AND THE REPLACEMENT MUST NOT OVERLAP: if the
    replacement is a SUBSTRING of the anchor, the "already applied" test
    (`n_new == 1`) is satisfied by the anchor itself -- so the helper
    would refuse a patch that has not landed. ⭐⭐⭐ (That refusal is
    CORRECT behaviour and it caught this cycle's own first attempt.)

    ⭐⭐⭐⭐⭐ CYCLE 1261's FIX: **THE ANCHORS ARE PATH-AGNOSTIC.**  The
    fixed order is CLONE -> PORT -> SWEEP, and the SWEEP owns the path
    token (`/tmp/cNNNN` -> `/tmp/cNNNN`).  So the OLD anchor is
    NORMALISED to the CURRENT cycle's path before it is matched -- which
    makes the port independent of WHICH cycle the clone was copied from,
    and keeps the ported NEW text on the CURRENT cycle's path.
    """
    global applied, already
    p = REPO / f"_c{CYCLE}_{fname}.py"
    src = p.read_text(encoding="utf-8")
    # ⭐⭐⭐ NORMALISE the path token in THE FILE and in BOTH anchors to THIS
    # cycle's path, so the comparison happens in a CANONICAL space where the
    # path token is settled.  ⭐⭐⭐⭐⭐ This is exactly what the identity
    # SWEEP does with `/tmp/cNNNN` -- so the port does not fight the sweep,
    # it merely makes the port INDEPENDENT of which cycle the clone was
    # copied from.  ⭐⭐⭐⭐⭐ The `_cNNNN_` instrument token is NOT touched
    # here: that is the SWEEP's token, and the sweep runs LAST.
    _path_re = re.compile(r"/tmp/c\d{4}")
    src = _path_re.sub(f"/tmp/c{CYCLE}", src)
    old = _path_re.sub(f"/tmp/c{CYCLE}", old)
    new = _path_re.sub(f"/tmp/c{CYCLE}", new)
    n_old = src.count(old)
    n_new = src.count(new)
    if n_old == 1 and n_new == 0 and new not in old:
        src = src.replace(old, new)
        p.write_text(src, encoding="utf-8")
        py_compile.compile(str(p), doraise=True)
        print(f"  [APPLIED] {fname}: {why}")
        applied += 1
        return
    if n_old == 0 and n_new == 1:
        print(f"  [ALREADY] {fname}: {why}")
        already += 1
        return
    raise SystemExit(
        f"[patch] ABORT: {fname}: the anchor occurs {n_old} time(s) and the "
        f"replacement {n_new} time(s) -- neither is the expected (1, 0) or "
        f"(0, 1); the anchor is NOT UNIQUE (Reminder 62)")


print("=" * 78)
print(f"CYCLE {CYCLE} -- PORT THE NO-OP BRANCH FIX INTO `commit.py`")
print("=" * 78)
print("  ⭐⭐⭐⭐⭐ THE PORT SOURCE IS THE (FILE, PREDICATE) PAIR")
print("     (_c1260_commit.py, the NO-OP-branch regions) -- and its")
print("     COMPLETENESS was measured by _c1261_clone.py before this")
print("     port ran.")
print("  ⭐⭐⭐⭐⭐ THE TARGET IS _c1261_commit.py (cloned from the")
print("     PUBLISHED base 1258, which is the PRE-fix shape).")

# ======================================================================
# PATCH 1 -- THE VISIBLE-PROSE GATE -> BRANCH-SYMMETRIC
# ======================================================================
print()
print("=" * 78)
print("PATCH 1 -- THE VISIBLE-PROSE GATE (the `找到了 N 則新推文` regex)")
print("=" * 78)
patch("commit",
      """# ⭐ THE PAGE'S PUBLISHED-COUNT PROSE IS READ FROM THE VISIBLE LAYER TOO.
_pv = re.search(r"找到了 (\\d+) 則新推文", _visible)
assert _pv, "the VISIBLE layer does not state the published-post count"
assert int(_pv.group(1)) == _N_PUBLISHED, (
    f"the visible page says {int(_pv.group(1))} 則新推文 but the adjudication "
    f"published {_N_PUBLISHED}")
assert "未發現新推文" not in _visible, (
    "the visible page still carries the 0-new-post prose -- this cycle "
    f"published {_N_PUBLISHED}")
""",
      """# ⭐ THE PAGE'S PUBLISHED-COUNT PROSE IS READ FROM THE VISIBLE LAYER TOO.
# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX (ported from 1260): **THIS GATE IS BRANCH-
# SYMMETRIC.**  The SUBSTANTIVE prose is "找到了 N 則新推文"; the MEASURED
# NO-OP prose is "未發現新推文".  ⭐⭐⭐⭐⭐ The regex below only matches the
# SUBSTANTIVE form, so on a NO-OP it found NOTHING and the gate aborted with
# "the VISIBLE layer does not state the published-post count" -- **a gate
# written for one shape is the most likely place the other shape is
# missing**. ⭐⭐⭐⭐⭐ AND PER THE ANTI-VACUITY RULE (Reminder 15), the NO-OP
# branch asserts **BOTH DIRECTIONS**: its own prose is PRESENT and the
# SUBSTANTIVE prose is ABSENT -- so a page carrying NEITHER would fail.
if _IS_NOOP:
    assert "未發現新推文" in _visible, (
        "the VISIBLE layer does not carry the MEASURED NO-OP prose "
        "('未發現新推文') -- the page must say what was measured")
    assert "找到了 0 則新推文" not in _visible, (
        "the VISIBLE layer carries the SUBSTANTIVE prose ('找到了 0 則新推文') "
        "-- on a MEASURED NO-OP that is a FALSE PUBLICATION: it claims the "
        "paths FOUND 0 tweets, when they found none")
    assert not re.search(r"找到了 \\d+ 則新推文", _visible), (
        "the VISIBLE layer carries a SUBSTANTIVE published-count clause on a "
        "MEASURED NO-OP")
    print("[commit] (NO-OP) the VISIBLE layer carries the NO-OP prose and NO "
          "SUBSTANTIVE published-count clause")
else:
    _pv = re.search(r"找到了 (\\d+) 則新推文", _visible)
    assert _pv, "the VISIBLE layer does not state the published-post count"
    assert int(_pv.group(1)) == _N_PUBLISHED, (
        f"the visible page says {int(_pv.group(1))} 則新推文 but the "
        f"adjudication published {_N_PUBLISHED}")
    assert "未發現新推文" not in _visible, (
        "the visible page still carries the 0-new-post prose -- this cycle "
        f"published {_N_PUBLISHED}")
""",
      "the visible-prose gate -> branch-symmetric (both directions)")

# ======================================================================
# PATCH 2 -- THE PROVENANCE ARTEFACT READ -> BRANCH-SYMMETRIC
# ======================================================================
print()
print("=" * 78)
print("PATCH 2 -- THE PROVENANCE ARTEFACT READ (the cycle-1258 region)")
print("=" * 78)
patch("commit",
      """_PROV = json.loads(pathlib.Path("/tmp/c1313/translate/provenance.json")
                   .read_text(encoding="utf-8"))
assert set(_PROV) == set(_new_ids), (
    f"the provenance artefact covers {sorted(_PROV)} but the published ids "
    f"are {sorted(_new_ids)} -- the two must be the SAME set")
""",
      """# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX (ported from 1260): **THE PROVENANCE REGION IS
# BRANCH-SYMMETRIC.**  ⭐⭐⭐⭐⭐ This region was ADDED to `commit.py` by
# cycle 1258 -- AFTER cycle 1255 had already written this file's NO-OP
# branch -- and it was placed AT TOP LEVEL, so it **INHERITED THE SHAPE
# THAT WAS CURRENT WHEN IT WAS ADDED**: the SUBSTANTIVE shape.
# ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ **THE SHAPE FIX WAS A *REGION*, NOT A *TYPE*** -- so a
# LATER gate in the SAME file did not get it.  ⭐⭐⭐⭐⭐
# ⭐⭐⭐⭐⭐ ON A MEASURED NO-OP THIS REGION READS TWO ARTEFACTS THAT DO NOT
# EXIST (the content-fetch branch never ran, so neither did the translation
# branch) -> FileNotFoundError -> the cycle ABORTS AFTER STAGING.
# ⭐⭐⭐⭐⭐ **THE ABORT IS THE GOOD OUTCOME**: an EMPTY artefact would have
# made this gate PASS and published "all 0 published record(s) scored 0
# defects", a **VACUOUS verification claim about ZERO records**.
# ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ **SO THE FIX IS NOT "RELAX THE GATE" -- IT IS "GIVE THE
# GATE A NO-OP BRANCH THAT PROVES THE ZERO DIFFERENTLY".** ⭐⭐⭐⭐⭐ AND THE
# ARTEFACTS' **ABSENCE IS ITSELF THE CONTRACT** (the same rule the
# content-fetch artefact follows): an EMPTY artefact says "we looked and
# found nothing"; an ABSENT one says "we never looked, because there was
# nothing to look for". ⭐⭐⭐⭐⭐ The second is TRUE and the first is a
# lie about the work done.
_PROV_PATH = pathlib.Path("/tmp/c1313/translate/provenance.json")
_FINAL_PATH = pathlib.Path("/tmp/c1313/translate/translations_final.json")
if _IS_NOOP:
    assert not _PROV_PATH.exists(), (
        "a MEASURED NO-OP must NOT carry a provenance artefact -- there was "
        "nothing to translate, so the translation branch never ran; an "
        "EMPTY provenance artefact would claim a verification that never "
        "happened")
    assert not _FINAL_PATH.exists(), (
        "a MEASURED NO-OP must NOT carry a translations artefact -- there was "
        "nothing to translate, so the translation branch never ran")
    print("[commit] (NO-OP) the provenance and translations artefacts are "
          "ABSENT -- the translation branch never ran, which is STRONGER "
          "than an empty artefact")
else:
    _PROV = json.loads(_PROV_PATH.read_text(encoding="utf-8"))
    assert set(_PROV) == set(_new_ids), (
        f"the provenance artefact covers {sorted(_PROV)} but the published "
        f"ids are {sorted(_new_ids)} -- the two must be the SAME set")
""",
      "the provenance gate -> branch-symmetric (artefacts' ABSENCE is the "
      "contract)")

# ======================================================================
# PATCH 3 -- THE RE-SCORING BLOCK -> BRANCH-SYMMETRIC (as a WHOLE)
# ======================================================================
print()
print("=" * 78)
print("PATCH 3 -- THE RE-SCORING BLOCK (the instrument + the fire-test)")
print("=" * 78)
# ⭐⭐⭐⭐⭐ THE REGION IS WRAPPED BY A **SCRIPT-LEVEL TRANSFORM** (a
# line-range re-indent measured from UNIQUE anchors) -- NOT by a hand-typed
# re-indent of a ~90-line region, which is exactly the kind of edit that
# silently drops or duplicates a line. ⭐⭐⭐⭐⭐ The transform asserts the
# wrap landed BY RE-READING THE FILE FROM DISK.
# ⭐⭐⭐⭐⭐ **AND THE TRANSFORM INSERTS ITS OWN EXPLANATORY COMMENT** (the
# NO-OP branch's header) -- so there is NO separate comment-only patch to
# apply. ⭐⭐⭐⭐⭐ A comment-only patch is a PURE-COSMETIC edit whose only
# effect is to make the NEXT anchor fail to match (because the transform
# has already inserted a similar comment) -- so having BOTH is a
# double-application hazard, and the transform's own comment is the
# authoritative one.
print()
print("=" * 78)
print("PATCH 3b -- WRAP THE REGION (a script-level transform)")
print("=" * 78)
import subprocess
import sys
_wr = subprocess.run([sys.executable, str(REPO / f"_c{CYCLE}_wrap_rescoring.py")],
                     capture_output=True, text=True)
print(_wr.stdout)
if _wr.returncode != 0:
    raise SystemExit(f"[patch] ABORT: the wrap transform failed:\n{_wr.stderr}")
assert _wr.returncode == 0

# ---- the defect sentence is branch-symmetric -------------------------
patch("commit",
      """if _N_DEFECTIVE == 0:
    _DEFECT_SENTENCE = (f"all {_N_PUBLISHED} published record(s) scored 0 "
                        f"defects")
elif _N_DEFECTIVE == _N_PUBLISHED:""",
      """# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX (ported from 1260): **THE DEFECT SENTENCE IS
# BRANCH-SYMMETRIC.**  ⭐⭐⭐⭐⭐ On a MEASURED NO-OP the SUBSTANTIVE
# sentence "all 0 published record(s) scored 0 defects" is **VACUOUS** -- it
# reports a clean score over an EMPTY set, which is a claim about nothing.
# ⭐⭐⭐⭐⭐ (It is also a FALSE PUBLICATION of a verification that never
# ran: the instrument was not even loaded.)  ⭐⭐⭐⭐⭐ The NO-OP sentence
# says what is TRUE: no record was published, so no defect could be
# recorded.
if _IS_NOOP:
    _DEFECT_SENTENCE = (
        "NO RECORD WAS PUBLISHED, SO NO FIDELITY DEFECT COULD BE RECORDED "
        "-- the zero is NOT a claim that the records scored 0 defects")
elif _N_DEFECTIVE == 0:
    _DEFECT_SENTENCE = (f"all {_N_PUBLISHED} published record(s) scored 0 "
                        f"defects")
elif _N_DEFECTIVE == _N_PUBLISHED:""",
      "the defect sentence -> branch-symmetric (a 0-of-0 score is vacuous)")

# ---- the provenance paragraph is branch-symmetric --------------------
patch("commit",
      """_n_inh = len(_adj["inherited"])
_n_bnew = len(_adj["brand_new"])
assert _n_inh + _n_bnew == _nreal, (
    f"the provenance split ({_n_inh} inherited + {_n_bnew} brand-new) does "
    f"not equal the published count ({_nreal})")
if _n_inh == 0:""",
      """_n_inh = len(_adj["inherited"])
_n_bnew = len(_adj["brand_new"])
assert _n_inh + _n_bnew == _nreal, (
    f"the provenance split ({_n_inh} inherited + {_n_bnew} brand-new) does "
    f"not equal the published count ({_nreal})")
# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX (ported from 1260): **THE PROVENANCE PARAGRAPH
# IS BRANCH-SYMMETRIC.**  ⭐⭐⭐⭐⭐ The SUBSTANTIVE paragraph's "the {n}
# BRAND-NEW one is {ids}" grammar reads correctly only when exactly ONE id
# is brand-new, and on a MEASURED NO-OP there are NO ids at all -- so the
# inherited paragraph would publish an EMPTY id list and assert a shape that
# does not exist. ⭐⭐⭐⭐⭐ **A COMMIT MESSAGE IS A PUBLICATION**, so the
# NO-OP paragraph says what was MEASURED: there was nothing to inherit and
# nothing to re-adjudicate.
if _IS_NOOP:
    _prov_para = (
        f"- ⭐ THE PROVENANCE SPLIT IS MEASURED, AND IT IS EMPTY: 0 of the 0 "
        f"were written by an earlier cycle and never committed, so there was "
        f"nothing to inherit and nothing to re-adjudicate. The prior "
        f"COMMITTED cycle ({PRIOR_CYCLE}) published normally, so the "
        f"worktree carried NO worktree-only delta")
elif _n_inh == 0:""",
      "the provenance paragraph -> branch-symmetric")

# ======================================================================
# PATCH 4 -- THE COMMIT MESSAGE -> BRANCH-SYMMETRIC
# ======================================================================
print()
print("=" * 78)
print("PATCH 4 -- THE COMMIT MESSAGE (a commit message IS a publication)")
print("=" * 78)
# ⭐⭐⭐⭐⭐ THE BRANCH-CONDITIONAL LINES ARE **PRE-COMPUTED INTO VARIABLES**
# -- they cannot be spliced into the MSG's implicit-concatenation chain,
# because a `+ (cond if ... else ...)` between two f-strings is a SYNTAX
# ERROR (an f-string is not an expression there). ⭐⭐⭐⭐⭐ **THE VARIABLES
# ARE DERIVED FROM THE SAME MEASUREMENT** (`_nreal`), so the message still
# says what was MEASURED.
patch("commit",
      """MSG = (
    f"chore: hourly cron cycle {CYCLE}, {len(_EXPECTED_FILES)}-FILE commit — \"""",
      """# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX (ported from 1260): **THE COMMIT MESSAGE IS
# BRANCH-SYMMETRIC.**  ⭐⭐⭐⭐⭐ The SUBSTANTIVE message claims "a PURE
# ADDITION of {ids}", "all N published record(s) scored 0 defects" and "each
# published post was fetched TWICE" -- **all three are FALSE on a NO-OP**
# (there is no addition, no record to score and no post to fetch). ⭐⭐⭐⭐⭐
# **A COMMIT MESSAGE IS A PUBLICATION** (cycle 1258's rule), so the NO-OP
# message says what was MEASURED. ⭐⭐⭐⭐⭐ AND THE BRANCH-CONDITIONAL LINES
# ARE PRE-COMPUTED INTO VARIABLES -- a `+ (cond if ... else ...)` spliced
# between two f-strings in an implicit-concatenation chain is a SYNTAX ERROR,
# and the fix is to derive the variables from the SAME MEASUREMENT (`_nreal`).
if _nreal:
    _msg_authors = ", all by @elonmusk"
    _msg_fetch = ("- each published post was fetched TWICE, independently, "
                  "and the two fetches agreed on the author, the created_at "
                  "and the text\\n")
    _msg_gate = ("THIS cycle the calibrated BIDIRECTIONAL instrument's "
                 "fire-test ran UNCONDITIONALLY before any record was "
                 "scored (KNOWN-BAD -> 1 defect, KNOWN-GOOD -> 0), and "
                 f"{_DEFECT_SENTENCE}\\n")
    _msg_corpus = (f"- tweets.json: {recs} records, a PURE ADDITION of "
                   f"{_new_ids_desc}; all {len(_committed)} committed "
                   f"records are BYTE-IDENTICAL\\n")
else:
    _msg_authors = ""
    _msg_fetch = ("- NO POST WAS PUBLISHED, SO NO POST WAS FETCHED -- and no "
                  "post was re-scored for fidelity defects; the zero is "
                  "proved by the adjudication's OWN non-empty candidate set "
                  "and its cross-check, not by a vacuous 0-of-0 "
                  "verification\\n")
    _msg_gate = ("on a MEASURED NO-OP the instrument was NOT loaded, because "
                 "a 0-of-0 re-scoring would be a VACUOUS verification -- "
                 f"{_DEFECT_SENTENCE}\\n")
    _msg_corpus = (f"- tweets.json: {recs} records, BYTE-IDENTICAL to HEAD "
                   f"-- a MEASURED NO-OP adds NOTHING, and all "
                   f"{len(_committed)} committed records survive "
                   f"unchanged\\n")

MSG = (
    f"chore: hourly cron cycle {CYCLE}, {len(_EXPECTED_FILES)}-FILE commit — \"""",
      "the commit message's branch-conditional lines -> pre-computed "
      "variables (derived from the same measurement)")

patch("commit",
      """    f"(authors: {_authors}) -> {_nreal} REAL NEW POSTS, all by @elonmusk\\n"
    f"{_prov_para}\\n"
    f"- published ids: {_new_ids_desc}\\n"
    f"- each published post was fetched TWICE, independently, and the two "
    f"fetches agreed on the author, the created_at and the text\\n"
""",
      """    f"(authors: {_authors}) -> {_nreal} REAL NEW POSTS{_msg_authors}\\n"
    f"{_prov_para}\\n"
    f"- published ids: {_new_ids_desc}\\n"
    f"{_msg_fetch}"
""",
      "the commit message's fetch claims -> branch-symmetric")

patch("commit",
      """    f"- the acceptance gate is ONE-SIDED and is BLIND to a dropped house "
    f"noun; THIS cycle the calibrated BIDIRECTIONAL instrument's fire-test "
    f"ran UNCONDITIONALLY before any record was scored (KNOWN-BAD -> 1 "
    f"defect, KNOWN-GOOD -> 0), and {_DEFECT_SENTENCE}\\n"
    f"- tweets.json: {recs} records, a PURE ADDITION of {_new_ids_desc}; all "
    f"{len(_committed)} committed records are BYTE-IDENTICAL\\n"
""",
      """    f"- the acceptance gate is ONE-SIDED and is BLIND to a dropped house "
    f"noun; {_msg_gate}"
    f"{_msg_corpus}"
""",
      "the commit message's corpus/defect sentences -> branch-symmetric")

print()
print("=" * 78)
print(f"[patch] {applied} patch(es) APPLIED, {already} already present")
print("=" * 78)
print("  ⭐⭐⭐⭐⭐ THE FIX MAKES THE GATE STRICTER, NOT LOOSER: the NO-OP")
print("     branch asserts the artefacts are ABSENT (a stronger claim than")
print("     'the file is empty') and asserts the page's NO-OP prose in BOTH")
print("     directions.")
