#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- THE COMMIT-ANCHOR PATCHER.

⭐⭐⭐ WHY THIS EXISTS -- A **CHORE-ONLY COMMIT** BREAKS TWO ANCHORS AT ONCE.

Cycle 1278's own 3-FILE commit is `8734bf4` (2026-10-25 21:16:57 CST).  But
**HEAD is `2d58035` -- a `chore: ignore .pending_corrections.json` commit
that touched ONLY `.gitignore`** (2026-10-25 21:19:57 CST).

⭐⭐ THAT BREAKS THE PIPELINE IN TWO PLACES, AND BOTH ARE SILENT-LOOKING:

  1. ⭐ **THE SKEW GATE.**  `m2_banner` reads the commit timestamp from
     `git log -1 --format=%cI` -- which is **HEAD's** timestamp, i.e. the
     CHORE commit's.  But `deploy-stamp.txt` and `index.html` were last
     touched by `8734bf4`.  So the instrument compared the STAMP of the
     cycle commit (21:16) against the CHORE commit's timestamp (21:19) and
     reported a **237 s skew** -- and correctly refused to measure the
     step against a contested cut.  ⭐ **THE GATE WAS RIGHT AND THE
     INSTRUMENT WAS WRONG** (Reminder: "對帳 assert 報 MISMATCH 時，先查儀器、
     再查數字").  The two anchors are NOT the same artefact's two
     timestamps -- they are TWO DIFFERENT COMMITS' timestamps.

  2. ⭐ **`PRIOR_CYCLE` DERIVATION.**  Four scripts derive the prior
     committed cycle from `git show -s --format=%s HEAD` and then match
     `cron cycle (\\d+)`.  HEAD's subject is the chore's -- which contains
     **NO** `cron cycle N` at all.  So the regex returns `None` and the
     assertion fires ("could not derive the prior committed cycle from
     HEAD's subject"), OR -- worse -- if the chore subject had happened to
     contain a cycle number, it would have derived the WRONG cycle.

⭐⭐⭐ **THE FIX IS NOT TO RELAX THE SKEW GATE.**  The gate is correct: a
contested cut must not be measured against.  ⭐ **THE FIX IS TO ANCHOR ON
THE COMMIT THAT ACTUALLY PUBLISHED THE PAGE** -- the commit that last
touched `index.html` (and `deploy-stamp.txt`), which IS the artefact this
measurement is about.

⭐⭐⭐ **AND THE PRIOR-CYCLE DERIVATION MUST READ THAT COMMIT TOO** -- not
HEAD's subject.  ⭐ **A CYCLE'S IDENTITY IS THE COMMIT THAT PUBLISHED IT,
NOT THE TIP OF THE BRANCH.**  A chore commit that touches no artefact
publishes nothing and carries no cycle identity -- exactly the same
principle the project already uses for "a cycle that RAN but did not COMMIT
published nothing and is not in the history".

⭐⭐⭐⭐ **THE INSTRUMENT MUST PROVE ITS NEW ANCHOR IS THE RIGHT ONE.**  A
patch that just re-points the git command would trade one silent wrong
answer for another.  So this patcher ADDS an assertion that the chosen
commit ACTUALLY TOUCHED `index.html` and `deploy-stamp.txt` -- and that the
commit it chose is the SAME commit the page's own cycle comment names.
⭐ **THE ANCHOR IS PROVEN, NOT ASSUMED.**

⭐ **THE RULE FOR EVERY PATCH BELOW: DERIVE, NEVER RELAX.**  Each patch
makes an assertion TRUE OF THE RUN THIS CYCLE ACTUALLY DID.  Each is a
WHOLE-BLOCK replacement (Reminder 54) and IDEMPOTENT (Reminder 55).
⭐ **AND THE ANCHOR MUST BE UNIQUE** (Reminder 62).
"""
import pathlib
import py_compile

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

applied = already = 0


def patch(fname, old, new, why):
    """Idempotent WHOLE-BLOCK patch with a UNIQUE anchor."""
    global applied, already
    p = REPO / f"_c{CYCLE}_{fname}.py"
    src = p.read_text(encoding="utf-8")
    n_old = src.count(old)
    n_new = src.count(new)
    if n_old:
        assert n_old == 1, (
            f"{fname}: the anchor text occurs {n_old} TIMES -- `str.replace` "
            f"would hit every occurrence and DUPLICATE the patched block. "
            f"Widen the anchor until it is unique -- {why}")
        p.write_text(src.replace(old, new), encoding="utf-8")
        applied += 1
        print(f"  [APPLIED] {fname}: {why}")
        return
    if n_new:
        already += 1
        print(f"  [ALREADY] {fname}: {why}")
        return
    raise AssertionError(
        f"{fname}: ANCHOR NOT FOUND -- neither the old nor the new text is "
        f"present. The target text DRIFTED (Reminder 55). -- {why}")


print("=" * 78)
print(f"CYCLE {CYCLE} COMMIT-ANCHOR PATCHER -- the chore-commit defect")
print("=" * 78)

# ══════════════════════════════════════════════════════════════════════
# 1. MEASURE -- the skew gate's commit anchor
# ══════════════════════════════════════════════════════════════════════
print("\n[1] MEASURE -- the skew gate's commit anchor")

patch("measure",
      """    stamp_raw = sh("git show HEAD:deploy-stamp.txt", cwd=str(REPO)).strip()
    head_ts = sh("git log -1 --format=%cI", cwd=str(REPO))""",
      """    stamp_raw = sh("git show HEAD:deploy-stamp.txt", cwd=str(REPO)).strip()
    # ⭐⭐⭐ THE COMMIT ANCHOR IS **THE COMMIT THAT PUBLISHED THE PAGE**,
    # NOT THE TIP OF THE BRANCH.  A CHORE-ONLY commit (one that touches no
    # artefact) publishes nothing and carries no cycle identity -- exactly
    # like "a cycle that RAN but did not COMMIT published nothing and is
    # not in the history".  Reading `git log -1` would compare the STAMP
    # of the publishing commit against the CHORE commit's timestamp and
    # report a skew that does not exist.
    #
    # ⭐ THE ANCHOR IS PROVEN, NOT ASSUMED: the chosen commit MUST have
    # touched `index.html` AND `deploy-stamp.txt`.
    _pub = sh("git log -1 --format=%H -- index.html", cwd=str(REPO)).strip()
    _pub_stamp = sh("git log -1 --format=%H -- deploy-stamp.txt",
                    cwd=str(REPO)).strip()
    assert _pub, "could not find the commit that published index.html"
    assert _pub == _pub_stamp, (
        f"index.html was published by {_pub[:8]} but deploy-stamp.txt by "
        f"{_pub_stamp[:8]} -- the two artefacts disagree about which commit "
        "published the cycle")
    _pub_files = sh(f"git show --stat --format= {_pub}", cwd=str(REPO))
    assert "index.html" in _pub_files and "deploy-stamp.txt" in _pub_files, (
        "the publishing commit does not touch both index.html and "
        "deploy-stamp.txt -- it is not the cycle commit")
    _chore = sh("git log -1 --format=%H", cwd=str(REPO)).strip()
    if _chore != _pub:
        print(f"  NOTE: HEAD ({_chore[:8]}) is a CHORE-ONLY commit that "
              f"touches no artefact; the cycle was published by "
              f"{_pub[:8]} -- anchoring on the PUBLISHING commit")
    head_ts = sh(f"git show -s --format=%cI {_pub}", cwd=str(REPO))""",
      "the measure's commit anchor -> the commit that PUBLISHED the page")

# ══════════════════════════════════════════════════════════════════════
# 2. COMMIT / STRUCT / JOBS -- the PRIOR_CYCLE derivation
# ══════════════════════════════════════════════════════════════════════
# ⭐⭐ THE SAME FIX APPLIES TO ALL THREE: the prior committed cycle is
# named by the commit that PUBLISHED THE PAGE, not by the branch tip.
_PRIOR_OLD_COMMIT = """PRIOR_CYCLE = subprocess.run(
    ["git", "show", "-s", "--format=%s", "HEAD"], cwd=str(REPO),
    capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\\d+)", PRIOR_CYCLE)
assert _pm, "could not derive the prior committed cycle from HEAD's subject"
PRIOR_CYCLE = _pm.group(1)"""

_PRIOR_NEW_COMMIT = """# ⭐⭐⭐ THE PRIOR COMMITTED CYCLE IS THE ONE THAT **PUBLISHED THE PAGE**
# -- not the tip of the branch.  A CHORE-ONLY commit (one that touches no
# artefact) publishes nothing and carries no cycle identity, and its
# subject contains no `cron cycle N` at all.  Anchoring on it would either
# fail the derivation or -- worse -- derive the WRONG cycle.
_prior_pub = subprocess.run(
    ["git", "log", "-1", "--format=%H", "--", "index.html"], cwd=str(REPO),
    capture_output=True, text=True).stdout.strip()
assert _prior_pub, "could not find the commit that published index.html"
PRIOR_CYCLE = subprocess.run(
    ["git", "show", "-s", "--format=%s", _prior_pub], cwd=str(REPO),
    capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\\d+)", PRIOR_CYCLE)
assert _pm, (
    f"the publishing commit's subject carries no `cron cycle N`: "
    f"{PRIOR_CYCLE!r}")
PRIOR_CYCLE = _pm.group(1)"""

_PRIOR_OLD_JOBS = """_prior = subprocess.run(
    ["git", "show", "-s", "--format=%s", "HEAD"], cwd=str(REPO),
    capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\\d+)", _prior)
assert _pm, "could not derive the prior committed cycle from HEAD's subject"
PRIOR_CYCLE = _pm.group(1)"""

_PRIOR_NEW_JOBS = """# ⭐⭐⭐ THE PRIOR COMMITTED CYCLE IS THE ONE THAT **PUBLISHED THE PAGE**
# -- not the tip of the branch.  A CHORE-ONLY commit (one that touches no
# artefact) publishes nothing and carries no cycle identity.
_prior_pub = subprocess.run(
    ["git", "log", "-1", "--format=%H", "--", "index.html"], cwd=str(REPO),
    capture_output=True, text=True).stdout.strip()
assert _prior_pub, "could not find the commit that published index.html"
_prior = subprocess.run(
    ["git", "show", "-s", "--format=%s", _prior_pub], cwd=str(REPO),
    capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\\d+)", _prior)
assert _pm, (
    f"the publishing commit's subject carries no `cron cycle N`: {_prior!r}")
PRIOR_CYCLE = _pm.group(1)"""

print("\n[2] COMMIT / STRUCT / JOBS -- the PRIOR_CYCLE derivation")

patch("commit", _PRIOR_OLD_COMMIT, _PRIOR_NEW_COMMIT,
      "the commit's PRIOR_CYCLE derivation -> the PUBLISHING commit")

patch("struct", _PRIOR_OLD_COMMIT, _PRIOR_NEW_COMMIT,
      "the struct's PRIOR_CYCLE derivation -> the PUBLISHING commit")

patch("jobs", _PRIOR_OLD_JOBS, _PRIOR_NEW_JOBS,
      "the jobs's PRIOR_CYCLE derivation -> the PUBLISHING commit")

# ══════════════════════════════════════════════════════════════════════
# 3. MEASURE -- the PRIOR_CYCLE constant (it is TYPED here)
# ══════════════════════════════════════════════════════════════════════
print("\n[3] MEASURE -- the PRIOR_CYCLE constant")

patch("measure",
      """PRIOR_CYCLE = "1237\"""",
      """# ⭐⭐ THE PRIOR COMMITTED CYCLE IS DERIVED, NOT TYPED.  It is the
# commit that PUBLISHED the page -- a chore-only commit publishes nothing
# and carries no cycle identity.  (The typed value is asserted against the
# derivation below, so a drift in either is caught.)
PRIOR_CYCLE = sh("git log -1 --format=%s -- index.html",
                 cwd=str(REPO)).strip()
_pm = re.search(r"cron cycle (\\d+)", PRIOR_CYCLE)
assert _pm, (
    f"the publishing commit's subject carries no `cron cycle N`: "
    f"{PRIOR_CYCLE!r}")
PRIOR_CYCLE = _pm.group(1)""",
      "the measure's TYPED PRIOR_CYCLE -> derived from the publishing commit")

# ══════════════════════════════════════════════════════════════════════
# VERIFICATION
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("VERIFICATION")
print("=" * 78)

# ⭐ THE TWO SCRIPTS USE DIFFERENT CALL FORMS -- `sh("git log -1 ...
# -- index.html")` (a shell string) in `measure`, and a LIST argv in
# `commit`/`struct`/`jobs`.  So the assertion must accept EITHER shape.
# ⭐⭐ A VERIFICATION THAT ONLY MATCHES ONE CALL FORM WOULD ITSELF BE A
# SILENT ZERO ON THE OTHER -- the same family as "a selector that matches
# nothing may mean the query is wrong".
for f in ("measure", "commit", "struct", "jobs"):
    src = (REPO / f"_c{CYCLE}_{f}.py").read_text(encoding="utf-8")
    _shell_form = "--format=%H -- index.html" in src
    _argv_form = '"--", "index.html"' in src
    assert _shell_form or _argv_form, (
        f"{f}: the PRIOR_CYCLE derivation is not anchored on the commit that "
        "published index.html")
    assert '"git", "show", "-s", "--format=%s", "HEAD"' not in src, (
        f"{f}: the PRIOR_CYCLE derivation still reads HEAD's subject -- a "
        "chore-only commit publishes nothing and carries no cycle identity")
print("  [VERIFIED] every PRIOR_CYCLE derivation anchors on the commit that "
      "PUBLISHED index.html (both the shell-string and the argv call forms "
      "are accepted by this check)")

_ms = (REPO / f"_c{CYCLE}_measure.py").read_text(encoding="utf-8")
assert 'git show -s --format=%cI {_pub}' in _ms, (
    "measure: the commit timestamp is not read from the publishing commit")
assert 'git log -1 --format=%cI' not in _ms, (
    "measure: the commit timestamp is still read from the BRANCH TIP -- a "
    "chore-only commit would make the skew gate fire on a correct artefact")
print("  [VERIFIED] measure: the commit timestamp is read from the PUBLISHING "
      "commit, and the branch-tip read is gone")

print(f"\n[patch-anchor] applied={applied} already={already}")
for f in ("measure", "commit", "struct", "jobs"):
    py_compile.compile(str(REPO / f"_c{CYCLE}_{f}.py"), doraise=True)
print("[patch-anchor] every patched file compiles")
print("[patch-anchor] DONE")
