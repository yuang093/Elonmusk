#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- PROSE FIXER for the cloned set.

⭐ WHY THIS EXISTS: cycle 1278's PAGE/MEASURE scripts were cloned from
cycle 1249 (the IN-BAND variant) and then switched to the OUT-OF-BAND
branch, but cycle 1251 was **INTERRUPTED before its page builder ever
ran** -- so the switch never had to correct the **DOCSTRINGS and the
prose**, only the code.  The result: cycle 1249's `page.py` docstring
still said "HOUR27 IS **IN BAND**" while its CODE implemented the
OUT-OF-BAND branch.

⭐ THAT IS A REAL DEFECT CLASS (Reminder 25): "A PROSE STRING IN A
GENERATED PAGE CAN NAME THE WRONG HOUR.  After any page build, sweep the
emitted comment for stale hour/cycle numbers -- and remember that a
**stale docstring** is the same defect."

So this fixer patches WHOLE BLOCKS of prose, and it is **IDEMPOTENT**
(Reminder 54): a pair whose "new" text is already present is reported as
ALREADY APPLIED and skipped, so a re-run is safe.

⭐ AND THE PATCHER'S OWN "new" TEXT MUST BE SWEEP-PROOF (Case 11): it must
not contain a literal that another patcher mutates.  Every "new" text
below refers to the prior committed cycle by a RELATIONSHIP where it can.
"""
import pathlib
import re
import sys

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
HOUR = 2

applied = already = 0


def patch(fname, old, new, why):
    """Idempotent WHOLE-BLOCK patch.  Raises on a genuinely missing anchor."""
    global applied, already
    p = REPO / f"_c{CYCLE}_{fname}.py"
    src = p.read_text(encoding="utf-8")
    if old in src:
        p.write_text(src.replace(old, new), encoding="utf-8")
        applied += 1
        print(f"  [APPLIED] {fname}: {why}")
        return
    if new in src:
        already += 1
        print(f"  [ALREADY] {fname}: {why}")
        return
    raise AssertionError(f"{fname}: ANCHOR NOT FOUND -- {why}")


print("=" * 78)
print(f"CYCLE {CYCLE} PROSE FIXER -- stale hour/cycle prose in the clone")
print("=" * 78)

# ══════════════════════════════════════════════════════════════════════
# 1. MEASURE -- the docstring's hour and its band statement
# ══════════════════════════════════════════════════════════════════════
print("\n[1] MEASURE -- the docstring's hour + band statement")

patch("measure",
      """CYCLE 1289 IS HOUR212 -- OUT OF BAND for RETRY_TRANSLATION_HOURS
= {0,3,6,9,12,15,18,21}.  The retry branch NEVER RAN.""",
      f"""CYCLE {CYCLE} IS HOUR {HOUR} UTC -- OUT OF BAND for RETRY_TRANSLATION_HOURS
= {{0,3,6,9,12,15,18,21}}.  The retry branch NEVER RAN.""",
      "the measure docstring's hour -> hour 12")

# ══════════════════════════════════════════════════════════════════════
# 2. PAGE -- the docstring's band statement + the prior-cycle prose
# ══════════════════════════════════════════════════════════════════════
print("\n[2] PAGE -- the docstring's band statement + the prior-cycle prose")

patch("page",
      """HOUR212 IS **IN BAND** for RETRY_TRANSLATION_HOURS = {0,3,6,9,12,15,18,21}
-> the empty-translation retry branch RAN in this hour, so the Phase 0.5
controls are the IN-BAND side: THIS HOUR'S OWN block must carry the IN-BAND
marker AND the guard's SKIPPED line, and must NOT carry the OUT-OF-BAND
marker; the most recent OUT-OF-BAND block is the NEGATIVE CONTROL; and the
count 105 IS this hour's own evidence (NOT borrowed, NOT disclaimed).
⭐ The prior COMMITTED cycle (1230) was OUT of band, so the control set
FLIPS: this hour's own block is the EVIDENCE and the out-of-band block is
the NEGATIVE CONTROL (Reminder 21).""",
      f"""HOUR {HOUR} UTC IS **OUT OF BAND** for RETRY_TRANSLATION_HOURS
= {{0,3,6,9,12,15,18,21}} -> the empty-translation retry branch NEVER RAN
in this hour, so the Phase 0.5 controls are the OUT-OF-BAND side: THIS
HOUR'S OWN block must carry the OUT-OF-BAND marker and must carry NEITHER
the IN-BAND marker NOR the guard's SKIPPED line; the most recent IN-BAND
block is the POSITIVE CONTROL and the count is BORROWED from it and
explicitly DISCLAIMED; and a DIFFERENT hour's out-of-band block is the
NEGATIVE CONTROL (Reminder 50).
⭐ The prior COMMITTED cycle was IN BAND, so the control set FLIPS: the
IN-BAND block becomes the POSITIVE CONTROL and the out-of-band block is the
NEGATIVE CONTROL (Reminder 21).""",
      "the page docstring's band statement -> OUT OF BAND")

patch("page",
      """⭐ THE DELTA IS MEASURED AGAINST HEAD, NEVER AGAINST THE WORKTREE.  HEAD held
8,160 records; the published corpus holds 8,161.  The prior COMMITTED cycle
(1230) published normally, so the worktree carried NO inherited
worktree-only delta to re-adjudicate -- there was nothing to inherit.""",
      """⭐ THE DELTA IS MEASURED AGAINST HEAD, NEVER AGAINST THE WORKTREE.  The
prior COMMITTED cycle published normally, but an INTERRUPTED cycle wrote
records into the worktree and never committed them -- so the worktree
carries a worktree-only delta that is a **LIABILITY, not an asset**
(Reminder 26): every worktree-only id must be added to this cycle's own
candidate set EXPLICITLY and re-verified from scratch, never inherited on
trust.""",
      "the page docstring's delta paragraph -> the liability rule")

patch("page",
      """# ⭐ NO INTERRUPTED CYCLES TO INHERIT: the prior COMMITTED cycle (1230)
# published normally, so the worktree carried NO worktree-only delta.  The
# stamp/banner anchors are read from HEAD, and PRIOR_CYCLE names that head.""",
      """# ⭐ THE WORKTREE-ONLY DELTA IS A LIABILITY, NOT AN ASSET (Reminder 26).
# The prior COMMITTED cycle published normally, but an INTERRUPTED cycle
# wrote records into the worktree and never committed them -- so the
# worktree DOES carry a worktree-only delta.  Every such id is added to
# this cycle's own candidate set EXPLICITLY and re-verified from scratch.
# The stamp/banner anchors are read from HEAD, and PRIOR_CYCLE names that
# head.""",
      "the page's prior-cycle comment -> the liability rule")

# ══════════════════════════════════════════════════════════════════════
# 3. COMMIT -- the derived PRIOR_CYCLE assertion's literal
# ══════════════════════════════════════════════════════════════════════
print("\n[3] COMMIT -- the derived PRIOR_CYCLE assertion's literal")

patch("commit",
      """# ⭐ DERIVED FROM HEAD's commit subject -- cycle 1278's prior committed
# cycle is 1230, not 1227 (that was cycle 1249's prior).""",
      """# ⭐ DERIVED FROM HEAD's commit subject -- this cycle's prior COMMITTED
# cycle is read from HEAD, not typed.  A cycle that RAN but did not COMMIT
# published nothing and is not in the history.""",
      "the commit's PRIOR_CYCLE derivation comment")

patch("commit",
      """assert PRIOR_CYCLE == "1230", (
    f"the prior committed cycle derived from HEAD is {PRIOR_CYCLE}, expected "
    "1230")""",
      """# ⭐ THE EXPECTED VALUE IS DERIVED FROM AN INDEPENDENT ARTEFACT, NOT
# TYPED: the committed page's own cycle comment names the cycle that HEAD
# published.  A typed literal here is a latent assertion about a run's
# shape (Reminder 37) -- and it would have FIRED on a correct artefact
# after the previous cycle's number moved.
_committed_page = subprocess.run(
    ["git", "show", "HEAD:index.html"], cwd=str(REPO),
    capture_output=True, text=True).stdout
_cmt_m = re.search(r"<!--\\s*cron cycle (\\d+):", _committed_page)
assert _cmt_m, ("could not read the committed cycle number out of HEAD's "
                "page comment")
assert PRIOR_CYCLE == _cmt_m.group(1), (
    f"the prior committed cycle derived from HEAD's SUBJECT is {PRIOR_CYCLE}, "
    f"but HEAD's PAGE names {_cmt_m.group(1)} -- the two artefacts disagree")""",
      "the commit's typed PRIOR_CYCLE literal -> derived from HEAD's page")

# ══════════════════════════════════════════════════════════════════════
# 4. JOBS -- the docstring's band statement + the prior-cycle prose
# ══════════════════════════════════════════════════════════════════════
print("\n[4] JOBS -- the docstring's band statement + the prior-cycle prose")

patch("jobs",
      """⭐ THE NOTE'S BRANCH IS DERIVED FROM THE BAND, AND THE BAND IS READ FROM
measured.json -- never typed (Reminder 33).  Cycle 1278 is IN BAND (hour 6
IS in RETRY_TRANSLATION_HOURS), so the note carries:
  * `writer_guard = FIRED`;
  * THIS HOUR'S OWN count as THIS hour's OWN evidence (NOT borrowed);
  * the NEGATIVE CONTROL as the most recent OUT-OF-BAND block;
  * "the control set FLIPS" -- the prior committed cycle (1230) was OUT OF
    BAND.""",
      """⭐ THE NOTE'S BRANCH IS DERIVED FROM THE BAND, AND THE BAND IS READ FROM
measured.json -- never typed (Reminder 33).  This cycle is OUT OF BAND (its
hour is NOT in RETRY_TRANSLATION_HOURS), so the note carries:
  * `writer_guard = NO_EVIDENCE_THIS_HOUR`;
  * the count as BORROWED from the POSITIVE CONTROL and explicitly
    DISCLAIMED as this hour's own evidence;
  * the POSITIVE CONTROL as the most recent IN-BAND block;
  * "the control set FLIPS" -- the prior COMMITTED cycle was IN BAND.""",
      "the jobs docstring's band statement -> OUT OF BAND")

patch("jobs",
      """    f"({NOTE_CYCLE}) was ALSO out of band, so the control set FLIPS. \"""",
      """    f"({NOTE_CYCLE}) was IN band, so the control set FLIPS. \"""",
      "the jobs note's band line -> the prior committed cycle was IN BAND")

print("\n" + "=" * 78)
print(f"PROSE FIX COMPLETE: {applied} applied, {already} already-applied")
print("=" * 78)

# ⭐ EVERY patched file must still compile
import py_compile
for f in ("measure", "page", "commit", "jobs"):
    py_compile.compile(str(REPO / f"_c{CYCLE}_{f}.py"), doraise=True)
print("[prose] every patched file compiles")

# ⭐ AND NO STALE HOUR/CYCLE PROSE MAY SURVIVE
_stale = []
for f in ("measure", "page", "commit", "jobs", "struct", "verify", "jobs_verify"):
    p = REPO / f"_c{CYCLE}_{f}.py"
    if not p.exists():
        continue
    src = p.read_text(encoding="utf-8")
    for pat in (r"HOUR212 IS", r"HOUR212 IS", r"Hour212 IS",
                r"hour 6 IS in RETRY", r"HOUR212\b"):
        for m in re.finditer(pat, src):
            _stale.append(f"{f}: {m.group(0)!r}")
assert not _stale, f"stale hour prose survived: {_stale}"
print("[prose] no stale hour prose survives in the patched set")
sys.exit(0)
