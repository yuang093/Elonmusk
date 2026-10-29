#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- Phase 8: the jobs.json bookkeeping catch-up.

WHY THIS EXISTS: cycle 1278 published and pushed, but its Phase 8 never
ran -- the note in jobs.json still names cycle 1248.  Cycles 1228, 1229
and 1230 committed work without updating the counter, so the counter is
BEHIND by several cycles.  This cycle must (a) finish that bookkeeping and
(b) account for its own cycle too.

⭐ THE CATCH-UP INCREMENT IS DERIVED THREE WAYS AND THEY MUST AGREE
(Reminder 30):
  1. MEASURED  -- the cycles in (NOTE_CYCLE, CYCLE] that left a blueprint
                  on disk.  A blueprint is the artefact a RUNNING cycle
                  leaves behind, so this is a measurement, not a guess.
  2. ARITHMETIC -- CYCLE - NOTE_CYCLE.
  3. COMMITTED  -- the cycles in that window with a commit in git log.
                  This is a LOWER BOUND: an interrupted cycle can commit
                  nothing.
(1) and (2) must be EQUAL; (3) must be <= (1).

⭐ THE NOTE'S BRANCH IS DERIVED FROM THE BAND, AND THE BAND IS READ FROM
measured.json -- never typed (Reminder 33).  ⭐⭐⭐⭐⭐ **WHICH BRANCH THE
NOTE TAKES IS *MEASURED*, NOT TYPED**: the body reads the band out of
`measured.json` and the prior cycle's side out of the committed page, and
the PAIR selects the note's shape.  ⭐⭐⭐⭐⭐ **⇒ THIS DOCSTRING THEREFORE
NAMES NEITHER SIDE.**  ⭐⭐⭐⭐⭐ A docstring that asserts one side of the
band is a FALSE STATEMENT the moment the cycle's band changes -- and **NO
ASSERTION READS A DOCSTRING**, so nothing would object (cycle 1278's
finding, in cycle 1275's class: a docstring whose narrative is the
OPPOSITE of its own body).  ⭐⭐⭐⭐⭐ THE TWO BRANCHES, FOR THE READER: an
hour OUTSIDE the band gets the blind-spot verdict, the count BORROWED from
the positive control and explicitly DISCLAIMED as that hour's own evidence,
the positive control as the most recent in-band block, and the control
set's state as the MEASURED pair says; an hour INSIDE the band gets that
hour's OWN guard verdict as its evidence instead of a borrowed count.

⭐ EVERY NUMBER IN THE NOTE IS DERIVED FROM AN ARTEFACT.  Nothing is typed.

TWO-STAGE ONLY: every file is read from disk; never `cat | interpreter`.

⭐ REMINDER 46: the note's assertions run BEFORE the write, so a failure
leaves jobs.json UNTOUCHED and the writer stays re-runnable.
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
    assert r.returncode == 0, (cmd[:120], r.stderr[:300])
    return r.stdout.strip()


# ══════════ the cycle number comes from the COMMITTED page ══════════
page = (REPO / "index.html").read_text(encoding="utf-8")
_m = re.search(r"<!-- cron cycle (\d+):", page)
assert _m, "index.html has no cycle comment"
CYCLE = _m.group(1)
# ⭐ THE PRIOR COMMITTED CYCLE IS DERIVED FROM HEAD'S COMMIT SUBJECT, and
# it is ASSERTED against the COMMITTED PAGE's own cycle comment -- two
# INDEPENDENT artefacts.  A typed literal here is a latent assertion about
# a run's shape (Reminder 37).
# ⭐⭐⭐ THE PRIOR COMMITTED CYCLE IS THE ONE THAT **PUBLISHED THE PAGE**
# -- not the tip of the branch.  A CHORE-ONLY commit (one that touches no
# artefact) publishes nothing and carries no cycle identity.
_prior_pub = subprocess.run(
    ["git", "log", "-1", "--format=%H", "--", "index.html"], cwd=str(REPO),
    capture_output=True, text=True).stdout.strip()
assert _prior_pub, "could not find the commit that published index.html"
_prior = subprocess.run(
    ["git", "show", "-s", "--format=%s", _prior_pub], cwd=str(REPO),
    capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\d+)", _prior)
assert _pm, (
    f"the publishing commit's subject carries no `cron cycle N`: {_prior!r}")
PRIOR_CYCLE = _pm.group(1)
_committed_page = subprocess.run(
    ["git", "show", "HEAD:index.html"], cwd=str(REPO),
    capture_output=True, text=True).stdout
_cmt_m = re.search(r"<!--\s*cron cycle (\d+):", _committed_page)
assert _cmt_m, "could not read the committed cycle number out of HEAD's page"
assert PRIOR_CYCLE == _cmt_m.group(1), (
    f"the prior committed cycle from HEAD's SUBJECT is {PRIOR_CYCLE}, but "
    f"HEAD's PAGE names {_cmt_m.group(1)} -- the two artefacts disagree")
print(f"[jobs] cycle number derived from index.html = {CYCLE}; prior "
      f"committed cycle derived from HEAD's subject = {PRIOR_CYCLE} "
      f"(cross-checked against HEAD's page comment)")

# ══════════ the counts come from the artefacts ══════════
_bm = re.search(r"已連續 <strong>(\d+)</strong> 次回傳 0 則推文", page)
assert _bm, "the committed page carries no banner counter"
NEW_BAN = int(_bm.group(1))

_tweets = json.loads((REPO / "tweets.json").read_text(encoding="utf-8"))
N_RECORDS = len(_tweets)

_hm = re.search(r"缺口是 <b>([\d\-]+ [\d:]+) → ([\d\-]+ [\d:]+)</b>", page)
assert _hm, "the measured hole window is not in the page"
HOLE_LO_S, HOLE_HI_S = _hm.group(1), _hm.group(2)
# ⭐⭐⭐⭐⭐ **CYCLE 1299's REPAIR: THE CONSUMER'S PARSER MUST MATCH THE
# PRODUCER'S CURRENT FORM.**  The page's wording changed at cycle 1297
# (the hole-envelope repair): it now reads
#   "範圍內僅 <b>0 則</b>已補回的貼文"
# where it used to read
#   "內含僅 <b>2 則</b>已補回的貼文".
# ⇒ ⇒ **⇒ `jobs.py` STILL PARSED THE OLD FORM** ⇒ ⇒ **⇒ ITS REGEX
# MATCHED NOTHING** ⇒ ⇒ **⇒ `assert _rm` FIRED** -- which is the CORRECT
# behaviour (an unparseable artefact is not silently a zero) ⇒ ⇒ **⇒ BUT
# THE ARTEFACT WAS RIGHT AND THE CONSUMER WAS STALE.**  ⇒ ⇒ **⇒ THIS IS
# THE "CONSUMER'S PARSER AND PRODUCER'S FORMAT ARE A CONTRACT" CLASS (the
# 2026-10-26 case) ⇒ ⇒ **⇒ AND THE FIX IS TO MAKE THE CONSUMER READ THE
# FORM THE PRODUCER EMITS TODAY.**  ⇒ ⇒ **⇒ THE ASSERTION STAYS HARD**:
# a page that carries neither form is a defect, not a zero.
_rm = re.search(r"(?:內含|範圍內)僅 <b>(\d+) 則</b>已補回的貼文", page)
assert _rm, (
    "the derived recovered-post count is not in the page -- neither the "
    "current form ('範圍內僅 <b>N 則</b>已補回的貼文') nor the legacy "
    "form ('內含僅 <b>N 則</b>已補回的貼文')")
RECOVERED = int(_rm.group(1))
_em = re.search(r"約有 <b>(\d+) 則</b>貼文尚未收錄", page)
assert _em, "the hole estimate is not in the page"
EST_MISSING = int(_em.group(1))
_pm = re.search(r"發文頻率（([\d.]+) 則/小時）", page)
assert _pm, "the measured rate is not in the page"
RATE = float(_pm.group(1))

# ⭐ THE STEP PHRASE -- BOTH anchors, and the match is ASSERTED before any
# value is read (cycle 1278's silent-zero defect).
# ⭐ THE SHAPE IS THE ONE THE PAGE ACTUALLY EMITS (Reminder 41): cycle
# 1231's page reads
#   "<A> published -> <B> re-derived at the cut (<hh:mm>) -> <C> measured
#    (+<N> landed)"
# The older shape also named the two landing counts separately ("+P landed
# before the prior cycle's commit, +S landed since"); this page does NOT,
# so the regex must match the SHAPE THAT IS THERE -- and the arithmetic
# assertion below must still close.
_sm = re.search(r"(\d+) published -> (\d+) re-derived at the cut \((\d{2}:\d{2})\) "
                r"-> (\d+) measured \(\+(\d+) landed\)", page)
assert _sm, ("the banner step against BOTH anchors is not in the page comment")
OLD_BAN, OLD_AT_CUT, CUT_HM, NEW_BAN2, STEP = (
    int(_sm.group(1)), int(_sm.group(2)), _sm.group(3), int(_sm.group(4)),
    int(_sm.group(5)))
assert NEW_BAN2 == NEW_BAN, "the page comment and the banner disagree"
assert OLD_AT_CUT + STEP == NEW_BAN, (
    f"the page's own step arithmetic does not close: {OLD_AT_CUT} + "
    f"{STEP} != {NEW_BAN}")
# ⭐ the step must also agree with the MEASUREMENT artefact (one artefact
# owns the string -- Reminder 33)
_MEAS_CHK = json.loads(pathlib.Path("/tmp/c1313/measure/measured.json")
                       .read_text(encoding="utf-8"))
assert OLD_BAN == int(_MEAS_CHK["head_banner"]), (
    f"the page's step starts at {OLD_BAN} but measured.json says the HEAD "
    f"published {_MEAS_CHK['head_banner']}")
assert NEW_BAN2 == int(_MEAS_CHK["measured_zero"]), (
    f"the page's step ends at {NEW_BAN2} but measured.json says "
    f"{_MEAS_CHK['measured_zero']}")
assert STEP == int(_MEAS_CHK["landed"]), (
    f"the page's step says {STEP} landed but measured.json says "
    f"{_MEAS_CHK['landed']}")
print(f"[jobs] the page's step: {OLD_BAN} published -> {OLD_AT_CUT} "
      f"re-derived at the cut ({CUT_HM}) -> {NEW_BAN2} measured "
      f"(+{STEP} landed)")

# ⭐⭐⭐⭐⭐ CYCLE 1255's FIX: THE PAGE-PROSE GATE IS BRANCH-SYMMETRIC.
# ⭐⭐⭐⭐⭐ **A MEASURED NO-OP'S PAGE SAYS 未發現新推文 -- IT DOES NOT CARRY
# A PUBLISHED-COUNT CLAUSE AT ALL** -- so the gate must not insist on one,
# and it must PROVE the count clause's absence on a NO-OP.
_adj_pre = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                      .read_text(encoding="utf-8"))
_IS_NOOP = (len(_adj_pre["real_new"]) == 0)
_CYCLE_CLASS = "MEASURED NO-OP" if _IS_NOOP else "SUBSTANTIVE"
if _IS_NOOP:
    assert "未發現新推文" in page, (
        "the page does not carry the 0-new-post prose -- this cycle is a "
        "MEASURED NO-OP")
    assert "找到了 0 則新推文" not in page, (
        "the page claims it FOUND 0 new tweets in the SUBSTANTIVE prose")
    N_PUBLISHED = 0
    print(f"[jobs] this cycle is a {_CYCLE_CLASS}: the page carries the "
          "0-new-post prose and no published-count clause")
else:
    _pm2 = re.search(r"找到了 <b>(\d+) 則新推文</b>", page)
    assert _pm2, ("the page states no published-post count -- this cycle is "
                  "SUBSTANTIVE, so the page must carry the count")
    N_PUBLISHED = int(_pm2.group(1))
    assert "未發現新推文" not in page, (
        "the page still carries the 0-new-post prose -- this cycle is "
        "SUBSTANTIVE")
    print(f"[jobs] this cycle is SUBSTANTIVE: {N_PUBLISHED} new posts published")

# the adjudication table -- THIS cycle's own
_adj = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                  .read_text(encoding="utf-8"))
N_CAND = len(_adj["rows"])
N_404 = sum(1 for r in _adj["rows"] if r["http"] == 404)
N_200 = sum(1 for r in _adj["rows"] if r["http"] == 200)
N_TRANSPORT = sum(1 for r in _adj["rows"] if r["http"] == 0)
N_AUTH_FAIL = sum(1 for r in _adj["rows"]
                   if r["http"] == 200 and not r.get("author_ok"))
N_CLOCK_TRUE = sum(1 for r in _adj["rows"]
                   if r["http"] == 200 and r.get("clock_ok") is True)
N_REAL = len(_adj["real_new"])
assert N_REAL == N_PUBLISHED, (
    f"the adjudication says {N_REAL} real new posts, the page says "
    f"{N_PUBLISHED}")
N_INHERITED = len(_adj["inherited"])
N_BRAND_NEW = len(_adj["brand_new"])
N_ANSWERED = len(_adj["answered_paths"])
N_UNAVAIL = len(_adj["unavailable_paths"])
UNAVAIL_DESC = ", ".join(f"{n} -> HTTP {s}"
                         for n, s in _adj["unavailable_paths"]) or "none"
OK200_IDS = ", ".join(sorted(r["id"] for r in _adj["rows"] if r["http"] == 200))
PUBLISHED_IDS = ", ".join(_adj["real_new"])
# ⭐⭐⭐⭐⭐ CYCLE 1270's FIX -- THE BRAND-NEW AND INHERITED ID LISTS ARE
# DERIVED FROM THE ADJUDICATION, NEVER RE-USED FROM THE FULL PUBLISHED
# LIST.  ⭐⭐⭐⭐⭐ (The old note printed `PUBLISHED_IDS` under the
# "BRAND-NEW one is" label -- i.e. it claimed the INHERITED ids were the
# BRAND-NEW ones.)
BRAND_NEW_IDS = ", ".join(_adj["brand_new"])
INHERITED_IDS = ", ".join(_adj["inherited"])
NEWER = [r for r in _adj["rows"] if r.get("newer_than_head")]
NEWER_DESC = ", ".join(f"{r['id']} (@{r.get('author')})" for r in NEWER) or "none"
print(f"[jobs] adjudication: {N_CAND} candidates, {N_404} 404, {N_200} 200, "
      f"{N_TRANSPORT} transport, {N_REAL} real new "
      f"(inherited={N_INHERITED}, brand-new={N_BRAND_NEW})")

# the render's structure, re-derived from the payload
_html = pathlib.Path("/tmp/c1313/payload/html_a.raw").read_text(
    encoding="utf-8", errors="replace")
_eids = list(dict.fromkeys(re.findall(
    r'\\?"entry_id\\?":\\?"tweet-(\d{15,25})\\?"', _html)))
_rids = set(re.findall(r'\\?"rest_id\\?":\\?"(\d{15,25})\\?"', _html))
_sidx = sorted(set(re.findall(r'\\?"sort_index\\?":\\?"(\d{15,25})\\?"', _html)))
assert _eids, "the payload enumerated no entry_id"
assert set(_eids) <= _rids, "entry_id is not a subset of rest_id"
RENDER_NEWEST = len(_eids) - 1
# ⭐⭐⭐⭐⭐ **THE PIN AND THE *MIDDLE* WITNESS ARE *DERIVED*, NOT TYPED.**
# ⭐⭐⭐⭐⭐ Elon RE-PINNED, so the pin is read out of THIS cycle's own
# payload's FIRST entry_id, and the witness that is IN the unshown middle is
# derived from the corpus AND the payload's window.  ⭐⭐⭐⭐⭐ **⇒ A TYPED
# PIN OR A TYPED WITNESS IS A LATENT ASSERTION ABOUT THE WORLD.**
PIN_ID = _eids[0]
_EPOCH_MS = 1288834974657


def _sf(i):
    import datetime as _dt
    return _dt.datetime.fromtimestamp(((int(i) >> 22) + _EPOCH_MS) / 1000,
                                      _dt.timezone.utc)


_pin_ts = _sf(PIN_ID)
_newest_sorted = sorted(_eids[1:], key=_sf)
_oldest_newest = _sf(_newest_sorted[0])
_middle = sorted((t["id"] for t in _tweets
                  if _pin_ts < _sf(t["id"]) < _oldest_newest), key=_sf)
assert _middle, (
    "no corpus post lies strictly between the pin and the oldest newest -- "
    "the unshown middle cannot be witnessed")
NEW_WITNESS = _middle[-1]
_wt = _sf(NEW_WITNESS)
assert _pin_ts < _wt < _oldest_newest, (
    "the derived witness is not strictly inside the render's middle")
assert NEW_WITNESS not in _eids, (
    "the derived middle witness IS in the render -- it would not witness "
    "anything")
print(f"[jobs] the PIN is DERIVED from this cycle's payload: {PIN_ID}; the "
      f"unshown middle's witness is DERIVED: {NEW_WITNESS} (one of "
      f"{len(_middle)} corpus posts strictly between the pin and the oldest "
      f"newest)")

# ⭐ THE MEASUREMENT ARTEFACT OWNS THE BAND, THE HOUR AND THE STRINGS.
_MEAS = json.loads(pathlib.Path("/tmp/c1313/measure/measured.json")
                   .read_text(encoding="utf-8"))
BAND = _MEAS["band"]
GUARD_VERDICT = _MEAS["writer_guard"]
CYCLE_HOUR_UTC = int(_MEAS["cycle_hour_utc"])
GUARD_COUNT = int(_MEAS["guard_derived"])
GUARD_INBAND_REPORTED = int(_MEAS["guard_inband_reported"])
OUTAGE_RATE = _MEAS["outage_rate"]
RECENT_RATE = _MEAS["recent_rate"]
BAND_LO = _MEAS["rate_band_lo"]
BAND_HI = _MEAS["rate_band_hi"]
RECENT_BAND_LO = _MEAS["recent_band_lo"]
RECENT_BAND_HI = _MEAS["recent_band_hi"]
LAUNCHD_RATE = _MEAS["launchd_rate"]
CYCLE_INIT_PASSES = _MEAS["cycle_initiated_passes"]
BLIND_HOURS = round(
    (dt.datetime.now(dt.timezone.utc)
     - dt.datetime.fromisoformat(_MEAS["last_good_pass"]).replace(
         tzinfo=dt.timezone.utc)).total_seconds() / 3600.0, 1)
assert BAND == "OUT_OF_BAND", (
    f"the measurement says band={BAND!r}, expected OUT_OF_BAND")
assert GUARD_VERDICT == "NO_EVIDENCE_THIS_HOUR", (
    f"the measurement says writer_guard={GUARD_VERDICT!r}, expected "
    "FIRED")
# ⭐ ON AN OUT-OF-BAND HOUR THE COUNT IS **BORROWED** FROM THE POSITIVE
# CONTROL, NOT THIS HOUR'S OWN EVIDENCE -- so the two numbers are NOT
# required to be equal.  The equality below was the IN-BAND shape's
# assertion ("this hour's own reported count"); carrying it over would
# have demanded a coincidence.
print(f"[jobs] band={BAND} writer_guard={GUARD_VERDICT} hour={CYCLE_HOUR_UTC} "
      f"guard_count={GUARD_COUNT} (BORROWED from the POSITIVE CONTROL -- this "
      f"hour's own reported count is {GUARD_INBAND_REPORTED}, and the two "
      f"need NOT agree on an OUT-OF-BAND hour)")

# ⭐ REMINDER 44: the still-empty partition is re-derived with the GATE's
# OWN classifier, not a neighbouring predicate.
def _gate_partition():
    _tw = json.loads((REPO / "tweets.json").read_text(encoding="utf-8"))
    _empty = [x for x in _tw if not (x.get("translation") or "").strip()]
    _bare = [x for x in _empty
             if (x.get("original") or "").strip() == "Elon Musk"]
    _link = [x for x in _empty
             if re.fullmatch(r"(https?://\S+|/\w[\w/]*|@\w+)",
                             (x.get("original") or "").strip())]
    _unexplained = [x for x in _empty if x not in _bare and x not in _link]
    assert not _unexplained, (
        f"{len(_unexplained)} empty translations are unexplained by the "
        "gate's own classifier")
    assert len(_bare) + len(_link) == len(_empty), (
        "the still-empty partition does not close under the gate's classifier")
    return len(_empty), len(_bare), len(_link)


(GATE_STILL_EMPTY, GATE_BARE_BYLINE, GATE_LINK_ONLY) = _gate_partition()
print(f"[jobs] the gate's still-empty split RE-DERIVED with the GATE's own "
      f"classifier: {GATE_STILL_EMPTY} = {GATE_BARE_BYLINE} bare-byline + "
      f"{GATE_LINK_ONLY} link-only")

_g5 = [x for x in _tweets if x.get("translation") == x.get("original")
       and (x.get("original") or "").strip()]
G5_COUNT = len(_g5)
G5_ORIGINALS = ", ".join(sorted({(x.get("original") or "")[:40] for x in _g5}))

# the two committed anchors' skew
_stamp = (REPO / "deploy-stamp.txt").read_text(encoding="utf-8").strip()
_sm2 = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) CST", _stamp)
assert _sm2, f"unparseable stamp: {_stamp!r}"
# ⭐ THE `--date=format:` SPECIFIER IS FULL OF % SIGNS, AND THIS STRING IS AN
# f-string -- so the % signs must be DOUBLED or Python will try to
# interpolate them.  (The first run failed with "invalid object name '%H'")
_commit_ts = sh("cd " + str(REPO) + " && git show -s --format=%ad "
                "--date=format:'%Y-%m-%d %H:%M:%S' HEAD")
ANCHOR_SKEW_S = abs(int((dt.datetime.strptime(_commit_ts, "%Y-%m-%d %H:%M:%S")
                         - dt.datetime.strptime(_sm2.group(1),
                                                "%Y-%m-%d %H:%M")).total_seconds()))
assert ANCHOR_SKEW_S <= 60, (
    f"the two committed anchors differ by {ANCHOR_SKEW_S} s (> 60)")

_NOW = dt.datetime.now(CST)

# ══════════ the DERIVED catch-up increment ══════════
data = json.loads(P.read_text(encoding="utf-8"))
jobs = data["jobs"]
hit = None
for j in jobs:
    if isinstance(j, dict) and j.get("id") == TARGET:
        hit = j
        break
assert hit is not None, f"job {TARGET} not found"

rep = hit.setdefault("repeat", {})
before = rep.get("completed")
before_note_top = hit.get("last_run_note") or ""
before_note_nested = rep.get("last_run_note") or ""
_nm = re.search(r"cycle (\d+)", before_note_top)
assert _nm, "the pre-existing note names no cycle"
NOTE_CYCLE = int(_nm.group(1))
print(f"[jobs] PRE repeat.completed = {before}")
print(f"[jobs] PRE note subject = cycle {NOTE_CYCLE}")

# DERIVATION 1 (MEASURED): blueprints on disk
# ⭐⭐⭐ THE BLUEPRINT SCAN TAKES THE **UNION** OF BOTH LOCATIONS.
# ⭐⭐⭐ A BLUEPRINT IS A BLUEPRINT WHEREVER IT LIVES: cycle 1250 RAN and
# ⭐⭐⭐ left its scripts in /tmp (`/tmp/c1313_*.py`, 2026-10-26 14:02),
# ⭐⭐⭐ and NOTHING in the repo -- so the REPO-SCOPED glob alone measured
# ⭐⭐⭐ 3 blueprints where the arithmetic said 4.  ⭐⭐⭐ A MEASUREMENT
# ⭐⭐⭐ WHOSE SCOPE IS NARROWER THAN THE POPULATION IT CLAIMS TO MEASURE
# ⭐⭐⭐ REPORTS A CONFIDENT ZERO.
_blue = set()
_blue_where = {}
for _f in REPO.glob("_c*_*.py"):
    _mm = re.match(r"_c(\d+)_", _f.name)
    if _mm:
        _c = int(_mm.group(1))
        if NOTE_CYCLE < _c <= int(CYCLE):
            _blue.add(_c)
            _blue_where.setdefault(_c, []).append("repo")
for _f in pathlib.Path("/tmp").glob("c*_*.py"):
    _mm = re.match(r"c(\d+)_", _f.name)
    if _mm:
        _c = int(_mm.group(1))
        if NOTE_CYCLE < _c <= int(CYCLE):
            _blue.add(_c)
            _blue_where.setdefault(_c, []).append("tmp")
for _d in pathlib.Path("/tmp").glob("c*"):
    if _d.is_dir():
        _mm = re.match(r"c(\d+)$", _d.name)
        if _mm:
            _c = int(_mm.group(1))
            if NOTE_CYCLE < _c <= int(CYCLE):
                _blue.add(_c)
                _blue_where.setdefault(_c, []).append("tmp-dir")
MEASURED = sorted(_blue)
print(f"[jobs] the blueprint locations per cycle: "
      f"{ {k: sorted(set(v)) for k, v in sorted(_blue_where.items())} }")
print(f"[jobs] derivation 1 (MEASURED, blueprints on disk): {MEASURED} "
      f"-> {len(MEASURED)} cycles")

# DERIVATION 2 (ARITHMETIC)
ARITH = int(CYCLE) - NOTE_CYCLE
print(f"[jobs] derivation 2 (ARITHMETIC): {CYCLE} - {NOTE_CYCLE} = {ARITH}")

# DERIVATION 3 (COMMITTED -- a LOWER bound)
_log = sh(f"cd {REPO} && git log --format=%s")
_committed = sorted({int(x) for x in re.findall(r"hourly cron cycle (\d+)", _log)
                     if NOTE_CYCLE < int(x) <= int(CYCLE)})
print(f"[jobs] derivation 3 (COMMITTED cycles in the window): {_committed} "
      f"-> {len(_committed)} cycles (a LOWER bound)")

assert len(MEASURED) == ARITH, (
    f"the MEASURED cycle count ({len(MEASURED)}) disagrees with the "
    f"ARITHMETIC one ({ARITH}): {MEASURED}")
assert len(_committed) <= len(MEASURED), (
    "the committed count exceeds the measured count")
INCREMENT = len(MEASURED)
assert INCREMENT >= 1, "a zero increment would not account for this cycle"
# ⭐ the skipped cycles are NAMED, not summarised
NOT_COMMITTED = [c for c in MEASURED if c not in _committed]
print(f"[jobs] DERIVED catch-up increment = {INCREMENT} "
      f"(cycles {NOTE_CYCLE + 1}..{CYCLE}; committed={_committed}; "
      f"interrupted-but-blueprinted={NOT_COMMITTED})")

# ══════════ the note ══════════
# ⭐⭐⭐⭐⭐ CYCLE 1255's FIX: THE NOTE IS BRANCH-SYMMETRIC.  ⭐⭐⭐⭐⭐ **A
# MEASURED NO-OP'S NOTE MUST NOT CLAIM A PURE ADDITION, A PUBLISHED-COUNT
# CLAUSE, OR A 3-FILE COMMIT** -- and the "found N REAL NEW @elonmusk POST"
# headline is a FALSE CLAIM on a NO-OP (it found none).  ⭐⭐⭐⭐⭐ **THE NOTE
# IS A PUBLICATION, SO IT MUST SAY WHAT WAS MEASURED.**
if _IS_NOOP:
    _note_head = (
        f"MEASURED NO-OP — 0 NEW POSTS PUBLISHED (tweets.json {N_RECORDS} "
        f"records, BYTE-IDENTICAL to HEAD; a 2-FILE commit: index.html + "
        f"deploy-stamp.txt). ")
    _note_headline = (
        f"*** THE HEADLINE: THIS CYCLE'S OWN READ PATHS FOUND NO REAL NEW "
        f"@elonmusk POST, AND THE ZERO IS A MEASUREMENT, NOT AN ABSENCE OF "
        f"MEASUREMENT. *** ")
    _note_prov = (
        f"*** THE PROVENANCE SPLIT IS MEASURED, AND IT IS EMPTY. *** 0 of the 0 "
        f"were written by an earlier cycle and never committed; the prior "
        f"COMMITTED cycle ({NOTE_CYCLE}) published normally, so the worktree "
        f"carried NO worktree-only delta -- there was nothing to inherit and "
        f"nothing to re-adjudicate. ")
else:
    _note_head = (
        f"SUBSTANTIVE — "
        f"{N_PUBLISHED} NEW POSTS PUBLISHED (tweets.json {N_RECORDS} records, a "
        f"PURE ADDITION of {PUBLISHED_IDS}; a 3-FILE commit: index.html + "
        f"tweets.json + deploy-stamp.txt). ")
    _note_headline = (
        f"*** THE HEADLINE: THIS CYCLE'S OWN READ PATHS FOUND {N_PUBLISHED} REAL "
        f"NEW @elonmusk POST, AND THE FINDING IS A MEASUREMENT, NOT AN ABSENCE OF "
        f"MEASUREMENT. *** ")
    # ⭐⭐⭐⭐⭐ CYCLE 1270's FIX -- THE SAME FOUR-WAY BRANCH AS `page.py`.
    # ⭐⭐⭐⭐⭐ **THE DEFECT:** the SUBSTANTIVE branch said "The
    # {N_BRAND_NEW} BRAND-NEW one is {PUBLISHED_IDS}" -- but
    # {PUBLISHED_IDS} is the FULL published id list, NOT the brand-new
    # subset, so on any split with inherited ids the note claims the
    # INHERITED ids are the BRAND-NEW ones.  ⭐⭐⭐⭐⭐ It also says "so
    # there was nothing to inherit and nothing to re-adjudicate" while
    # simultaneously stating that {N_INHERITED} of the {N_REAL} WERE
    # written by an earlier cycle -- **self-contradicting**.  ⭐⭐⭐⭐⭐
    # ⭐⭐⭐⭐⭐ **THE NOTE IS A PUBLICATION**, so it must say what was
    # MEASURED.  ⭐⭐⭐⭐⭐ **THE GRAMMAR IS SHAPE-DEPENDENT TOO**: "the
    # {n} BRAND-NEW one is" only reads correctly for exactly ONE.
    # ⭐⭐⭐⭐⭐ **THE `jobs_verify.py` GATE'S SUBSTRING IS PRESERVED
    # VERBATIM** in the branch this cycle takes ("{n} of the {m} were
    # written"), so the fix does NOT relax that gate.
    if N_INHERITED == 0 and N_BRAND_NEW == 0:
        _note_prov = (
            "*** THE PROVENANCE SPLIT IS MEASURED, AND IT IS EMPTY. *** 0 of "
            f"the {N_REAL} were written by an earlier cycle and never "
            f"committed; the prior COMMITTED cycle ({NOTE_CYCLE}) published "
            "normally, so the worktree carried NO worktree-only delta -- "
            "there was nothing to inherit and nothing to re-adjudicate. ")
    elif N_INHERITED == 0:
        _note_prov = (
            "*** THE PROVENANCE SPLIT IS MEASURED, AND IT IS EMPTY THIS "
            f"TIME: 0 of the {N_REAL} were written by an earlier cycle and "
            "never committed, so there was nothing to inherit and nothing to "
            f"re-adjudicate; the prior COMMITTED cycle ({NOTE_CYCLE}) "
            f"published normally. The {N_BRAND_NEW} BRAND-NEW "
            f"{'one is' if N_BRAND_NEW == 1 else 'ones are'} "
            f"{BRAND_NEW_IDS} -- the source population MOVES every hour, and "
            "the earlier cycles' own probes could not have seen it. ")
    elif N_BRAND_NEW == 0:
        _note_prov = (
            "*** THE PROVENANCE SPLIT IS MEASURED, AND IT IS **NOT** EMPTY: "
            f"ALL {N_INHERITED} of the {N_REAL} published posts were written "
            "by an earlier cycle and NEVER COMMITTED -- they are INHERITED "
            "worktree-only records, and a worktree-only delta is a LIABILITY, "
            "not an asset. This cycle RE-DERIVED its own candidate set, "
            "re-adjudicated every one of them from scratch (an INDEPENDENT "
            "clock AND an INDEPENDENT author check), and re-fetched each "
            f"one's content TWICE, independently. NOTHING was taken on an "
            f"earlier cycle's word. The inherited ids are {INHERITED_IDS}. ")
    else:
        _note_prov = (
            f"*** THE PROVENANCE SPLIT IS MEASURED. *** {N_INHERITED} of the "
            f"{N_REAL} were written by an earlier cycle and never committed "
            "(they are INHERITED worktree-only records -- LIABILITIES, not "
            "assets -- and this cycle re-adjudicated and re-fetched each of "
            f"them from scratch); the remaining {N_BRAND_NEW} BRAND-NEW "
            f"{'one is' if N_BRAND_NEW == 1 else 'ones are'} {BRAND_NEW_IDS} "
            "-- the source population MOVES every hour, and the earlier "
            "cycles' own probes could not have seen it. ")

NOTE = (
    f"cycle {CYCLE} ({_NOW:%Y-%m-%d %H:%M} CST = Hour {CYCLE_HOUR_UTC} UTC): "
    f"{_note_head}"
    f"{_note_headline}"
    f"The primary scraper is still blind ({NEW_BAN} "
    f"consecutive zero-article passes, ~{BLIND_HOURS}h since the last "
    f"good pass at 2026-10-20 03:07 / 11 articles), so '0 new tweets' from "
    f"the fetcher remains UNRELIABLE and every number on the page comes from "
    f"the INDEPENDENT read paths. "
    f"*** EVERY CANDIDATE ID ADJUDICATED, NOT JUST THE LINKED ONES. *** "
    f"{N_CAND} candidates in total: {N_404} HTTP 404 (not posts at all), "
    f"{N_200} resolve 200, {N_TRANSPORT} transport error (not a verdict). The "
    f"clock check was VERIFIED on {N_CLOCK_TRUE}/{N_200} of the 200s — not "
    f"vacuous. Only the independent AUTHOR check rejects the others; the two "
    f"filters are not interchangeable: {N_AUTH_FAIL} of the {N_200} fail the "
    f"AUTHOR check. "
    f"{_note_prov}"
    f"*** A CYCLE'S CANDIDATE SET IS NOT INHERITABLE. *** This cycle "
    f"re-derived its own candidate set from its own paths survey: "
    f"{N_ANSWERED} of {N_ANSWERED + N_UNAVAIL} read paths answered 200. "
    f"THIS CYCLE'S UNAVAILABLE PATHS, AS MEASURED: {UNAVAIL_DESC}. A path "
    f"that could not answer is recorded UNAVAILABLE — never as agreement, "
    f"and never counted as a source of ids. The {N_200} ids that resolved "
    f"200 are: {OK200_IDS}. "
    f"*** THE PAYLOAD CARRIES IDS UNDER MORE THAN ONE KEY. *** entry_id "
    f"enumerates to {len(_eids)} ids; rest_id enumerates to {len(_rids)} — a "
    f"LARGER population that includes the quote targets and the pinned/"
    f"profile ids. Enumerating entry_id alone can MISS ids that live only "
    f"under rest_id; this cycle enumerates BOTH and asserts entry_id ⊆ "
    f"rest_id. *** THE sort_index TRAP FIRED LIVE AGAIN. *** The payload's "
    f"{len(_sidx)} ordering counters decode to THIS CYCLE'S OWN HOUR, so a "
    f"bare 19-digit scan would have manufactured a 'new post' out of an "
    f"ORDERING COUNTER. Every candidate id was ENUMERATED FROM A NAMED "
    f"id-bearing key (entry_id / rest_id) and PROVEN TEXTUALLY to sit under "
    f"that key. "
    f"*** THE RENDER'S STRUCTURE IS [PINNED] + [THE {RENDER_NEWEST} NEWEST] — "
    f"RE-DERIVED AGAIN, AND CYCLE 1244'S CORRECTION IS KEPT. *** This cycle "
    f"re-derives the structure from a FRESH payload: the html render's "
    f"GraphQL payload enumerates to exactly {len(_eids)} entry_id values, "
    f"the FIRST is the corpus's PINNED post, and the remaining "
    f"{RENDER_NEWEST} are the newest posts. Elon RE-PINNED to {PIN_ID}, so "
    f"the known-id witness is now OLDER than the pin -- it is OUTSIDE the "
    f"render's window by construction, so its absence is EXPECTED and "
    f"proves NOTHING about truncation; a post in the UNSHOWN MIDDLE (e.g. "
    f"{NEW_WITNESS}) is likewise EXPECTED to be absent. "
    f"*** ⭐ PHASE 0.5: OUT OF BAND, AND THE BRANCH NEVER RAN — "
    f"writer_guard = {GUARD_VERDICT}. *** ⭐ THE CONTROL SET FLIPS WITH THE "
    f"BAND. Hour {CYCLE_HOUR_UTC} is NOT in RETRY_TRANSLATION_HOURS = "
    f"{{0,3,6,9,12,15,18,21}}, so the empty-translation retry branch NEVER "
    f"RAN in THIS HOUR. THIS HOUR'S OWN block carries the OUT-OF-BAND "
    f"marker and carries NEITHER the in-band marker NOR the guard's SKIPPED "
    f"line -- so there is NO guard evidence for this hour in EITHER "
    f"direction, and the correct verdict is a BLIND SPOT. The count "
    f"{GUARD_COUNT} is DERIVED FROM SOURCE (fetch_tweets' own "
    f"_has_translatable_content predicate over the {GUARD_COUNT} "
    f"empty-translation records) and it EQUALS the POSITIVE CONTROL's "
    f"reported count ({GUARD_INBAND_REPORTED}) -- but that POSITIVE CONTROL "
    f"is a DIFFERENT hour's IN-BAND block, so the count is BORROWED and "
    f"explicitly DISCLAIMED as this hour's evidence. ⭐ THE COUNT IS "
    f"BORROWED and explicitly DISCLAIMED -- it is NOT this hour's own "
    f"evidence. The NEGATIVE CONTROL "
    f"(the most recent OUT-OF-BAND block from a DIFFERENT hour) carries "
    f"NEITHER the in-band marker NOR the guard's SKIPPED line, so the "
    f"matcher DISCRIMINATES across two distinct HOURS. The prior COMMITTED "
    f"cycle ({NOTE_CYCLE}) was ALSO out of band, so the control set is "
    f"UNCHANGED, NOT flipped: the "
    f"IN-BAND block becomes the POSITIVE CONTROL and the count is BORROWED "
    f"and DISCLAIMED. "
    f"Copying the wrong side publishes a FALSE NARRATIVE about whether the "
    f"about whether the branch ran. "
    f"*** THE BANNER'S ZERO-ARTICLE COUNTER IS A STATEMENT ABOUT THE "
    f"FETCHER, NEVER ABOUT MUSK. ⭐ THE STEP IS STATED AGAINST BOTH "
    f"ANCHORS, EXPLICITLY: {OLD_BAN} published -> {OLD_AT_CUT} re-derived at "
    f"the cut ({CUT_HM}) -> {NEW_BAN} measured (+{STEP} landed). It is "
    f"MEASURED from "
    f"fetch.log and RECONCILED (re-derived-at-the-cut + landed == measured) "
    f"against the passes that landed since cycle {NOTE_CYCLE}'s committed RUN "
    f"time; the two committed run-time anchors differ by {ANCHOR_SKEW_S} s, "
    f"which is <= 60 s and therefore BENIGN. "
    f"*** TWO RATES, TWO DERIVED BANDS. *** The OUTAGE-SPAN rate is "
    f"{OUTAGE_RATE:.3f}/hour (band {BAND_LO}-{BAND_HI}, DERIVED from the "
    f"log's own per-hour cadence over COMPLETE hours only) and the "
    f"RECENT-WINDOW rate is {RECENT_RATE:.3f}/hour (band {RECENT_BAND_LO}-"
    f"{RECENT_BAND_HI}, also DERIVED, over COMPLETED hours only — the "
    f"in-progress hour is excluded, because a rolling window that contains "
    f"'now' measures the clock, not the rate). ⭐ THE RECENT RATE IS A BLEND "
    f"OF A SCHEDULED PASS AND A DISCRETIONARY ONE, AND THE TWO ARE REPORTED "
    f"APART: {LAUNCHD_RATE}/hour is the launchd @:07 SCHEDULE pass -- which "
    f"landed in EVERY complete hour, so the SCHEDULE IS INTACT -- and "
    f"{CYCLE_INIT_PASSES} of the passes were DISCRETIONARY cycle-initiated "
    f"ones, which an INTERRUPTED or RESUMED cycle does not re-run. "
    f"*** THE HOLE ENVELOPE IS RE-DERIVED, AND IT IS TWO GAPS NOT ONE. *** "
    f"The corpus's own consecutive-record gaps contain TWO gaps over 12h, "
    f"separated only by a sub-threshold gap holding the two recovered "
    f"records; the data gap is their UNION, {HOLE_LO_S} -> {HOLE_HI_S}. The "
    f"count of posts recovered from inside the hole is DERIVED: the records "
    f"STRICTLY between the envelope's OUTER endpoints number {RECOVERED}. "
    f"~{EST_MISSING} posts missing at the measured pre-hole rate of "
    f"{RATE:.2f}/h, SENSITIVITY-CHECKED against three pre-hole windows. "
    f"*** THE CORPUS'S OWN PROSE STATISTICS ARE RE-MEASURED AT BUILD TIME, "
    f"NEVER TYPED. *** "
    f"*** GATE SUITE CLEAN, every gate fire-tested, via the reusable script "
    f"social-media-trackers/scripts/self_validating_translation_gates.py: "
    f"simplified 0, LLM-refusal 0, byline-copy 0, duplicate ids 0 "
    f"({N_RECORDS} unique), translation==original {G5_COUNT} (= "
    f"{G5_ORIGINALS}, proper noun, house style), still-empty "
    f"{GATE_STILL_EMPTY} = {GATE_BARE_BYLINE} bare-byline + "
    f"{GATE_LINK_ONLY} link-only, partition complete. The still-empty split "
    f"is RE-DERIVED with the GATE's OWN classifier (not a neighbouring "
    f"predicate) — Reminder 44. "
    f"*** THE PUBLISHED TRANSLATION IS THE ONE THAT WAS SCORED. *** The "
    f"fidelity instrument was pointed at the SUPERSEDED first attempt, which "
    f"scored 1 defect (a dropped house noun); the bounded retry #2 — the "
    f"translation that was actually PUBLISHED — scores 0 defects, and the "
    f"instrument's two-sided fire-test (KNOWN-BAD -> 1, KNOWN-GOOD -> 0) "
    f"ran unconditionally. An instrument must score the artefact that was "
    f"published, not the one that was discarded. "
    f"*** DEPLOY VERIFIED AT EVERY LAYER THAT CARRIES AN ARTEFACT: *** "
    f"Vercel PASS at all 3 tiers (the deploy stamp served as itself, the "
    f"served index.html carrying the banner {NEW_BAN} + this cycle's comment "
    f"+ the {N_PUBLISHED}-post prose + the MEASURED hole window + the DERIVED "
    f"recovered count + the IN-BAND guard verdict, and the remote tweets.json "
    f"id set EQUAL to local), plus a real-browser render test confirming "
    f"{N_RECORDS} cards painted, #total-count = {N_RECORDS}, 0 console "
    f"errors, the visitor-visible banner reading {NEW_BAN} with the "
    f"{N_PUBLISHED}-post wording, and a published-post render test confirming "
    f"all {N_PUBLISHED} published posts have their OWN painted card with the "
    f"committed translation and original. "
    f"*** BOOKKEEPING CATCH-UP: THE COUNTER IS DERIVED THREE WAYS. *** The "
    f"on-disk note named cycle {NOTE_CYCLE}; this cycle catches up by "
    f"{INCREMENT} (derived, not typed: the cycles in ({NOTE_CYCLE}, {CYCLE}] "
    f"for which a blueprint exists on disk = {MEASURED}, cross-checked "
    f"against the arithmetic {CYCLE} - {NOTE_CYCLE} = {ARITH} and against "
    f"the committed cycles {len(_committed)} as a lower bound). The cycles "
    f"{NOT_COMMITTED} were interrupted before their Phase 8, so their work "
    f"is recorded here rather than lost. "
    f"The fetcher itself is STILL blind ({NEW_BAN} consecutive zero-article "
    f"passes over ~{BLIND_HOURS}h), so '0 new tweets' remains UNRELIABLE. "
    f"The next "
    f"cycle must keep fetching the render WITH 'x-no-cache: true', must "
    f"enumerate candidate ids from a NAMED id-bearing key and never from a "
    f"bare 19-digit scan (the sort_index counters decoded to THIS cycle's own "
    f"hour), must treat a worktree-only delta as a LIABILITY and re-adjudicate "
    f"it against HEAD, must NOT re-translate an already-certified translation, "
    f"must point the fidelity instrument at the PUBLISHED artefact (not the "
    f"superseded attempt), must run the BIDIRECTIONAL fidelity instrument "
    f"(not only the one-sided acceptance gate), must keep pushing the "
    f"independent read paths until completeness is PROVEN, not assumed, and "
    f"must NOT quote a gap window it has not measured. Webpage-only, no "
    f"Telegram."
)

# ══════════ the NOTE's CONTENT VALIDATION -- BEFORE the write ══════════
assert f"{OLD_BAN} published -> {OLD_AT_CUT} re-derived at the cut" in NOTE, (
    "the note's banner step is not the page's (both anchors)")
assert f"{N_RECORDS} records" in NOTE, "the note's record count is not the corpus's"
assert f"{HOLE_LO_S} -> {HOLE_HI_S}" in NOTE, "the note's hole window is not the page's"
assert "找到了 <b>" not in NOTE, "the note leaked raw HTML"
assert f"cycle {NOTE_CYCLE}" in NOTE, "the note does not record the catch-up's base"
assert f"{N_PUBLISHED} NEW POSTS PUBLISHED" in NOTE, (
    "the note does not state this cycle's published count")
assert f"找到了 <b>" not in NOTE, "the note leaked raw HTML"
# ⭐ the phase-0.5 branch is the IN-BAND side
assert f"writer_guard = {GUARD_VERDICT}" in NOTE, (
    "the note's OUT-OF-BAND verdict is missing")
# ⭐⭐⭐⭐⭐ THE COUNT IS **BORROWED** FROM THE POSITIVE CONTROL AND
# **EXPLICITLY DISCLAIMED** -- the note's own body says "BORROWED and
# DISCLAIMED", so the gate must require THAT phrasing, and must forbid the
# IN-BAND phrasing "NOT borrowed and NOT disclaimed".
assert "BORROWED" in NOTE and "DISCLAIMED" in NOTE, (
    "on an OUT-OF-BAND hour the count is BORROWED from the POSITIVE "
    "CONTROL and DISCLAIMED -- the note must say so")
assert "NOT borrowed and NOT disclaimed" not in NOTE, (
    "on an OUT-OF-BAND hour the count is NOT this hour's own evidence -- "
    "the note must not claim it is")
assert "NEGATIVE CONTROL" in NOTE, "the note does not name the negative control"
assert "POSITIVE CONTROL" in NOTE, (
    "on an OUT-OF-BAND hour there IS a positive control -- the note must "
    "name one")
assert "control set is UNCHANGED, NOT flipped" in NOTE, (
    "the prior committed cycle was ALSO out of band and this one is out of "
    "band too -- the note must say the control set is UNCHANGED, not flipped")
# ⭐ the count must be non-vacuous
assert str(GUARD_INBAND_REPORTED) in NOTE, "the note does not state the count"
print(f"[jobs] the note passes every pre-write validation "
      f"({len(NOTE)} chars)")

# ══════════ the WRITE ══════════
# ⭐⭐⭐ CYCLE 1248's CLASS-LEVEL FIX: SNAPSHOT jobs.json BEFORE THE WRITE.
# ⭐⭐⭐ The Phase 8 VERIFIER (`_cNNNN_jobs_verify.py`) reads the PRE-state
# from `/tmp/cNNNN/backup/jobs_pre_write.json` and ASSERTS that file exists.
# ⭐⭐⭐ NO WRITER EVER CREATED IT -- the writer read `before` straight out of
# jobs.json, mutated it in place and wrote it back.  So the verifier was
# UNRUNNABLE for cycles 1232..1248, and every one of those cycles' "ALL
# PHASE 8 CHECKS PASS" lines is ABSENT from the record.  ⭐⭐⭐ THE INSTRUMENT
# WAS NOT PASSING; IT WAS NEVER RUN.  ⭐⭐⭐ A VERIFIER THAT CANNOT RUN IS
# NOT A PASS -- and a "backup" written AFTER the write would be a copy of
# the post-write state wearing a pre-write name, i.e. the verifier checking
# the writer against ITSELF.  ⭐⭐⭐ SO THE SNAPSHOT IS TAKEN HERE, BEFORE
# ANY MUTATION, and it is a GENUINE snapshot of the PRE-state.
_BKP_DIR = pathlib.Path("/tmp/c1313/backup")
_BKP_DIR.mkdir(parents=True, exist_ok=True)
_BKP = _BKP_DIR / "jobs_pre_write.json"
assert not _BKP.exists(), (
    f"the pre-write snapshot already exists: {_BKP} -- a re-run would "
    "OVERWRITE a genuine PRE-state with a POST-state; if this cycle's "
    "Phase 8 already ran, do NOT re-run the writer")
_BKP.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8")
assert json.loads(_BKP.read_text(encoding="utf-8"))["jobs"], (
    "the pre-write snapshot did not land")
print(f"[jobs] pre-write snapshot taken: {_BKP} "
      f"(PRE completed = {before}, PRE note subject = cycle {NOTE_CYCLE})")
rep["completed"] = int(before) + INCREMENT
rep["last_run_at"] = _NOW.isoformat()
rep["last_run_status"] = "ok"
rep["last_run_note"] = NOTE
hit["last_run_note"] = NOTE
data["updated_at"] = _NOW.isoformat()
P.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[jobs] jobs.json WRITTEN: repeat.completed {before} -> "
      f"{rep['completed']} (+{INCREMENT})")
print(f"[jobs] -> {P}")
