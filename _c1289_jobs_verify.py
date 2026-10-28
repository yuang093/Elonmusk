#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1285 -- Phase 8 VERIFIER (a SEPARATE script).

⭐ REMINDER 42: THE PHASE 8 WRITER IS ONE-SHOT -- IT MUST BE VERIFIED WITH
A SEPARATE SCRIPT.  The writer's own assertions run BEFORE its write, so
they cannot check the write landed.  This script reads jobs.json back from
DISK and re-derives every number in it from the committed artefacts.

⭐ REMINDER 46: a one-shot writer's assertions that run AFTER the write
cannot be re-run -- so this verifier READS THE ARTEFACT BACK and checks it
against the committed tree, not against the writer's in-memory state.

TWO-STAGE ONLY: every file is read from disk; never `cat | interpreter`.
"""
import datetime as dt
import json
import pathlib
import re
import subprocess

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
P = pathlib.Path("/Users/taeyeon093.bot/.hermes/cron/jobs.json")
TARGET = "dca30f00381e"
CST = dt.timezone(dt.timedelta(hours=8))


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert r.returncode == 0, (cmd[:140], r.stderr[:300])
    return r.stdout.strip()


# ══════════ read jobs.json back from DISK ══════════
data = json.loads(P.read_text(encoding="utf-8"))
jobs = data["jobs"]
hit = None
for j in jobs:
    if isinstance(j, dict) and j.get("id") == TARGET:
        hit = j
        break
assert hit is not None, f"job {TARGET} not found"
rep = hit["repeat"]
note = rep.get("last_run_note") or ""
top_note = hit.get("last_run_note") or ""
print(f"[verify-jobs] repeat.completed = {rep.get('completed')}")
print(f"[verify-jobs] repeat.last_run_at = {rep.get('last_run_at')}")
print(f"[verify-jobs] repeat.last_run_status = {rep.get('last_run_status')}")
print(f"[verify-jobs] note length = {len(note)}")

# ══════════ 1. the note names THIS cycle ══════════
page = (REPO / "index.html").read_text(encoding="utf-8")
_m = re.search(r"<!-- cron cycle (\d+):", page)
assert _m, "index.html has no cycle comment"
CYCLE = _m.group(1)
_nm = re.search(r"cycle (\d+)", note)
assert _nm, "the written note names no cycle"
assert _nm.group(1) == CYCLE, (
    f"the written note names cycle {_nm.group(1)}, the committed page names "
    f"cycle {CYCLE}")
print(f"[verify-jobs] the note names cycle {CYCLE} (matching the page)")

# ══════════ 2. the counter is derived THREE WAYS, and they agree ══════════
# the PRE-state is recovered from the BACKUP the writer took
BKP = pathlib.Path("/tmp/c1289/backup/jobs_pre_write.json")
assert BKP.exists(), "the pre-write backup is missing -- cannot verify the delta"
_bdata = json.loads(BKP.read_text(encoding="utf-8"))
_bhit = None
for j in _bdata["jobs"]:
    if isinstance(j, dict) and j.get("id") == TARGET:
        _bhit = j
        break
assert _bhit is not None
_before = _bhit["repeat"]["completed"]
_before_note_cycle = int(re.search(r"cycle (\d+)", _bhit["repeat"]["last_run_note"]).group(1))
print(f"[verify-jobs] PRE counter = {_before}, PRE note subject = cycle "
      f"{_before_note_cycle}")

# ⭐⭐⭐ THE BLUEPRINT SCAN TAKES THE **UNION** OF BOTH LOCATIONS -- the
# ⭐⭐⭐ SAME rule the writer uses, so the two instruments agree on what a
# ⭐⭐⭐ blueprint IS (cycle 1249: a rewrite with an exemption and an audit
# ⭐⭐⭐ without one are the same defect).
_blue = set()
_blue_where = {}
for _f in REPO.glob("_c*_*.py"):
    _mm = re.match(r"_c(\d+)_", _f.name)
    if _mm:
        _c = int(_mm.group(1))
        if _before_note_cycle < _c <= int(CYCLE):
            _blue.add(_c)
            _blue_where.setdefault(_c, []).append("repo")
for _f in pathlib.Path("/tmp").glob("c*_*.py"):
    _mm = re.match(r"c(\d+)_", _f.name)
    if _mm:
        _c = int(_mm.group(1))
        if _before_note_cycle < _c <= int(CYCLE):
            _blue.add(_c)
            _blue_where.setdefault(_c, []).append("tmp")
for _d in pathlib.Path("/tmp").glob("c*"):
    if _d.is_dir():
        _mm = re.match(r"c(\d+)$", _d.name)
        if _mm:
            _c = int(_mm.group(1))
            if _before_note_cycle < _c <= int(CYCLE):
                _blue.add(_c)
                _blue_where.setdefault(_c, []).append("tmp-dir")
MEASURED = sorted(_blue)
print(f"[verify-jobs] the blueprint locations per cycle: "
      f"{ {k: sorted(set(v)) for k, v in sorted(_blue_where.items())} }")
ARITH = int(CYCLE) - _before_note_cycle
_log = sh(f"cd {REPO} && git log --format=%s")
_committed = sorted({int(x) for x in re.findall(r"hourly cron cycle (\d+)", _log)
                     if _before_note_cycle < int(x) <= int(CYCLE)})
print(f"[verify-jobs] derivation 1 (blueprints on disk): {MEASURED}")
print(f"[verify-jobs] derivation 2 (arithmetic): {CYCLE} - "
      f"{_before_note_cycle} = {ARITH}")
print(f"[verify-jobs] derivation 3 (committed, lower bound): {_committed}")

assert len(MEASURED) == ARITH, (
    f"the MEASURED count ({len(MEASURED)}) != the ARITHMETIC one ({ARITH})")
assert len(_committed) <= len(MEASURED), (
    "the committed count exceeds the measured count")
INCREMENT = len(MEASURED)

# ══════════ 3. the WRITTEN counter equals PRE + the derived increment ══════════
assert rep["completed"] == _before + INCREMENT, (
    f"the written counter {rep['completed']} != PRE {_before} + derived "
    f"{INCREMENT} = {_before + INCREMENT}")
print(f"[verify-jobs] the written counter {rep['completed']} == PRE "
      f"{_before} + derived {INCREMENT}  OK")

# ══════════ 4. the note states EVERY skipped cycle's work ══════════
_not_committed = [c for c in MEASURED if c not in _committed]
print(f"[verify-jobs] interrupted-but-blueprinted cycles: {_not_committed}")
for _c in _not_committed:
    assert str(_c) in note, (
        f"the note does not record the work of cycle {_c} -- the catch-up "
        "must account for EVERY skipped cycle, not just the count")
assert f"catches up by {INCREMENT}" in note, (
    "the note does not state the derived catch-up increment")

# ══════════ 5. the note's numbers agree with the ARTEFACTS ══════════
_tweets = json.loads((REPO / "tweets.json").read_text(encoding="utf-8"))
N_RECORDS = len(_tweets)
_bm = re.search(r"已連續 <strong>(\d+)</strong> 次回傳 0 則推文", page)
assert _bm, "the committed page carries no banner counter"
NEW_BAN = int(_bm.group(1))
assert f"{NEW_BAN} consecutive zero-article passes" in note, (
    "the note's banner counter is not the page's")
assert f"{N_RECORDS} records" in note, "the note's record count is not the corpus's"

_adj = json.loads(pathlib.Path("/tmp/c1289/adjudicate/verdicts.json")
                  .read_text(encoding="utf-8"))
# ⭐⭐⭐⭐⭐ CYCLE 1255's FIX: THE NOTE-VERIFIER IS BRANCH-SYMMETRIC.  ⭐⭐⭐⭐⭐
# **A MEASURED NO-OP'S NOTE SAYS "FOUND NO REAL NEW @elonmusk POST"** -- it
# does NOT carry the SUBSTANTIVE headline -- and it does NOT carry a
# provenance-split phrase in the SUBSTANTIVE form ("N of the M were
# written"), because there is no addition to attribute.  ⭐⭐⭐⭐⭐ THE
# VERIFIER MUST ASSERT THE SHAPE'S OWN TEXT.
_IS_NOOP = (len(_adj["real_new"]) == 0)

# ⭐⭐⭐⭐⭐ CYCLE 1267's FIX (3rd instance of the single-shape-gate family --
# `page.py` in 1266, `commit.py` in 1266, and NOW `jobs_verify.py`):  ⭐⭐⭐⭐⭐
# THE PUBLISHED-COUNT EXTRACTION BELOW WAS **UNCONDITIONAL** -- it demanded
# the SUBSTANTIVE prose ("找到了 <b>N 則新推文</b>") from a page that, on a
# MEASURED NO-OP, correctly carries the *other* shape's prose instead.  ⭐⭐⭐⭐⭐
# **THE NOTE WAS ALREADY CORRECT** (measured: it carries the MEASURED NO-OP
# header, the NO-OP headline, the 2-FILE commit and BYTE-IDENTICAL) and the
# COUNTER WAS ALREADY CORRECT (5100 == 5097 + 3) -- **the ARTEFACT WAS RIGHT
# AND THE CHECK WAS WRONG.**  ⭐⭐⭐⭐⭐ THE FIX (canonical RULE 3): LIFT THE
# WHOLE REGION, CLASSIFY THE SHAPE **BEFORE** the first shape-dependent read,
# AND ASSERT BOTH DIRECTIONS IN EACH BRANCH (anti-vacuity, Reminder 15) -- so
# the NO-OP branch cannot pass on a page carrying NEITHER shape's prose.  ⭐⭐⭐⭐⭐
# ⭐⭐⭐⭐⭐ AND THE EXTRACTION ITSELF MOVES **INSIDE** EACH BRANCH: a shared
# `_pm2 = re.search(...)` line ABOVE the `if` is, by the audit instrument's
# own definition, an **UNCONDITIONAL** shape token -- the very defect class
# this fix exists to remove.  ⭐⭐⭐⭐⭐ THE SAME IS TRUE OF A SHARED PATTERN
# CONSTANT: hoisting the regex into `_SUBSTANTIVE_RE` above the `if` merely
# moves the unconditional token, it does not remove it.  ⭐⭐⭐⭐⭐ THE CANONICAL
# FORM (the reference file's RULE 3, verbatim) INLINES the pattern in each
# branch.  ⭐⭐⭐⭐⭐ THE BRANCH MUST ALSO ASSERT ITS **OWN** TOKEN PRESENT --
# that is what makes the instrument read the branch as speaking FOR that
# token, and it is the SUBSTANTIVE branch's anti-vacuity half.
# THE SHAPE IS CLASSIFIED FROM THE ADJUDICATION ARTEFACT (this cycle's own
# measurement), NEVER FROM THE PAGE -- reading the shape off the artefact
# under test would make the check vacuous.
if _IS_NOOP:
    # own shape's prose PRESENT ...
    assert "未發現新推文" in page, (
        "a MEASURED NO-OP page must carry the MEASURED NO-OP prose "
        "(未發現新推文) -- the page states no measured outcome")
    # ... and the OTHER shape's prose ABSENT (anti-vacuity: a page carrying
    # NEITHER must not pass this branch)
    assert not re.search(r"找到了 <b>(\d+) 則新推文</b>", page), (
        "a MEASURED NO-OP page must NOT carry the SUBSTANTIVE published-count "
        "prose -- the page states a published-post count")
    assert "MEASURED NO-OP — 0 NEW POSTS PUBLISHED" in note, (
        "the note does not carry the MEASURED NO-OP header")
    assert "0 NEW POSTS PUBLISHED" in note, (
        "the note does not state the measured published count (0)")
    assert "FOUND NO REAL NEW @elonmusk POST" in note, (
        "the note's headline is not the MEASURED NO-OP one -- it must say it "
        "found NO real new post, not that it found 0")
    assert "a 2-FILE commit: index.html + deploy-stamp.txt" in note, (
        "the note does not carry the 2-FILE commit description")
    assert "BYTE-IDENTICAL to HEAD" in note, (
        "the note does not say the corpus is byte-identical to HEAD")
    assert "PURE ADDITION" not in note, (
        "the note claims a PURE ADDITION -- a MEASURED NO-OP added nothing")
    assert "3-FILE commit" not in note, (
        "the note claims a 3-FILE commit -- a MEASURED NO-OP is a 2-FILE one")
    print("[jobs_verify] (NO-OP) the page carries the MEASURED prose and NO "
          "published-count prose; the note carries the MEASURED NO-OP header, "
          "headline, 2-FILE commit and byte-identical corpus")
else:
    _pm2 = re.search(r"找到了 <b>(\d+) 則新推文</b>", page)
    assert _pm2, "the page states no published-post count"
    N_PUBLISHED = int(_pm2.group(1))
    # own shape's prose PRESENT ...
    assert f"{N_PUBLISHED} 則新推文" in page, (
        "a SUBSTANTIVE page must carry the SUBSTANTIVE published-count prose")
    # ... and the OTHER shape's prose ABSENT
    assert "未發現新推文" not in page, (
        "a SUBSTANTIVE page must NOT carry the MEASURED NO-OP prose")
    assert f"{N_PUBLISHED} NEW POSTS PUBLISHED" in note, (
        "the note's published count is not the page's")
    assert "PURE ADDITION" in note, (
        "the note does not describe the corpus as a PURE ADDITION")
    assert "3-FILE commit" in note, (
        "the note does not describe the 3-FILE commit")
    # ⭐⭐⭐⭐⭐ CYCLE 1290 -- THE PROVENANCE-SPLIT CHECK IS *BRANCH-SYMMETRIC*.
    # The PRODUCER (jobs.py) has FOUR branches and each writes a DIFFERENT
    # phrasing; the old check asserted the MIXED branch's phrasing
    # UNCONDITIONALLY, so it fired on a perfectly correct artefact (the
    # cycle-1275 class: an instrument that fires on a correct artefact IS
    # the defect).  The split is read from the INDEPENDENT adjudication
    # artefact, never typed.
    _n_inh = len(_adj["inherited"])
    _n_real = len(_adj["real_new"])
    _n_bn = len(_adj["brand_new"])
    _split_forms = {
        "ALL": f"ALL {_n_inh} of the {_n_real} published posts were written",
        "MIXED": f"{_n_inh} of the {_n_real} were written by an earlier cycle",
        "ZERO": f"0 of the {_n_real} were written by an earlier cycle",
    }
    # the branch this adjudication implies.  NOTE: when _n_inh == 0 the
    # MIXED form and the ZERO form are the SAME STRING -- so the ZERO
    # branch must be selected explicitly, and the "other" list must be
    # de-duplicated (a form that equals the expected one is not a
    # violation).
    if _n_bn == 0 and _n_inh == _n_real and _n_real > 0:
        _expected = _split_forms["ALL"]
        _others = [_split_forms["MIXED"], _split_forms["ZERO"]]
    elif _n_inh == 0:
        _expected = _split_forms["ZERO"]
        _others = [_split_forms["ALL"], _split_forms["MIXED"]]
    else:
        _expected = _split_forms["MIXED"]
        _others = [_split_forms["ALL"], _split_forms["ZERO"]]
    # a form that IS the expected one can never be a violation
    _others = sorted({o for o in _others if o != _expected})
    assert _expected in note, (
        f"the note's provenance split is not the adjudication's: expected "
        f"the split {_n_inh}/{_n_bn} of {_n_real}, whose form is "
        f"{_expected!r}; the note does not carry it")
    for _o in _others:
        assert _o not in note, (
            f"the note carries the WRONG provenance split's form ({_o!r}) "
            f"besides its own ({_expected!r}) -- a note that states two "
            "different splits is self-contradicting")
    print(f"[verify-jobs] the provenance split agrees with the adjudication "
          f"({_n_inh} inherited / {_n_bn} brand-new of {_n_real}); the "
          "other splits' forms are ABSENT")
    print("[jobs_verify] (SUBSTANTIVE) the page carries the published-count "
          f"prose ({N_PUBLISHED}); the note agrees")

assert f"{len(_adj['rows'])} candidates in total" in note, (
    "the note's candidate count is not the adjudication's")
for _i in _adj["real_new"]:
    assert _i in note, f"the note does not name the published id {_i}"

# the Phase 0.5 branch -- the OUT-OF-BAND side
_MEAS = json.loads(pathlib.Path("/tmp/c1289/measure/measured.json")
                   .read_text(encoding="utf-8"))
assert _MEAS["band"] == "OUT_OF_BAND", (
    "measured.json says the band is not OUT_OF_BAND")
assert f"writer_guard = {_MEAS['writer_guard']}" in note, (
    "the note's guard verdict is not measured.json's")
assert "NEGATIVE CONTROL" in note, "the note does not name the negative control"
assert "the control set FLIPS" in note, (
    "the prior committed cycle was in band -- the note must say the "
    "control set FLIPS")
assert "the control set is UNCHANGED, NOT 'flipped back'" not in note, (
    "the prior committed cycle was in band and this one is OUT OF BAND -- "
    "the control set DOES flip, so the note must not say it is UNCHANGED")
assert "BORROWED and explicitly DISCLAIMED" in note, (
    "on an OUT-OF-BAND hour the count is BORROWED from the positive "
    "control and DISCLAIMED -- the note must say so")
assert "NOT borrowed and NOT disclaimed" not in note, (
    "on an OUT-OF-BAND hour the count is NOT borrowed -- the note must "
    "not claim it is")
assert "POSITIVE CONTROL" in note, (
    "on an OUT-OF-BAND hour there IS a positive control -- the note must "
    "name one")
assert f"Hour {_MEAS['cycle_hour_utc']} UTC" in note, (
    "the note does not name the cycle's own hour")
assert f"in RETRY_TRANSLATION_HOURS" in note, (
    "the note does not state the band membership")
print(f"[verify-jobs] the note's Phase 0.5 branch is the OUT-OF-BAND side and "
      f"agrees with measured.json")

# the derived rate bands
assert f"band {_MEAS['rate_band_lo']}-{_MEAS['rate_band_hi']}" in note, (
    "the note's outage-span band is not measured.json's")
assert f"band {_MEAS['recent_band_lo']}-{_MEAS['recent_band_hi']}" in note, (
    "the note's recent-window band is not measured.json's")
assert "1.90-2.10" not in note, (
    "the note carries the STALE typed band -- the band is DERIVED")

# the hole window
_hm = re.search(r"缺口是 <b>([\d\-]+ [\d:]+) → ([\d\-]+ [\d:]+)</b>", page)
assert _hm, "the measured hole window is not in the page"
assert f"{_hm.group(1)} -> {_hm.group(2)}" in note, (
    "the note's hole window is not the page's")

# ══════════ 6. the note is mirrored to BOTH places and they are identical ══════════
assert top_note == note, (
    "the top-level last_run_note and the nested one DIFFER -- one of them "
    "is stale")

# ══════════ 7. the jobs.json file is still VALID JSON and the job is intact ══════════
assert isinstance(data, dict) and "jobs" in data and "updated_at" in data, (
    "jobs.json lost its top-level structure")
assert isinstance(data["jobs"], list), "jobs.json's jobs is not a list"
assert rep.get("last_run_status") == "ok", "the job's last_run_status is not ok"
_ts = dt.datetime.fromisoformat(rep["last_run_at"])
assert abs((dt.datetime.now(CST) - _ts).total_seconds()) < 7200, (
    "the written last_run_at is implausibly old")

# ══════════ 8. the committed tree is UNCHANGED by the bookkeeping ══════════
_git_status = sh(f"cd {REPO} && git status --porcelain --untracked-files=no")
assert _git_status.strip() == "", (
    f"the bookkeeping changed the COMMITTED tree: {_git_status!r} -- Phase 8 "
    "must not touch the repo")
_head = sh(f"cd {REPO} && git rev-parse HEAD")
_subject = sh(f"cd {REPO} && git log -1 --format=%s")
assert f"cycle {CYCLE}" in _subject, (
    f"HEAD does not name cycle {CYCLE}: {_subject!r}")
_ahead = sh(f"cd {REPO} && git rev-list --left-right --count origin/main...HEAD")
print(f"[verify-jobs] HEAD = {_head[:7]}; push debt = {_ahead!r}")
assert _ahead.split() == ["0", "0"], (
    f"the push debt is {_ahead!r} -- the commit was not pushed")
print(f"[verify-jobs] the committed tree is UNCHANGED by the bookkeeping and "
      f"HEAD is pushed")

print("\n[verify-jobs] ALL PHASE 8 CHECKS PASS")
print(f"[verify-jobs] counter {_before} -> {rep['completed']} "
      f"(+{INCREMENT}, derived three ways: blueprints={MEASURED}, "
      f"arithmetic={ARITH}, committed={_committed} as a lower bound)")
print(f"[verify-jobs] the note names cycle {CYCLE}, the published ids, the "
      f"IN-BAND guard verdict, the NEGATIVE CONTROL, and every skipped "
      f"cycle's work ({_not_committed})")
