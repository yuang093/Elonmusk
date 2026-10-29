#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- deploy stamp + COMMIT + push (3-FILE, SUBSTANTIVE, no
Telegram).

CLONED FROM `_c1313_commit.py` (the SUBSTANTIVE sibling), NOT from
`_c1313_commit.py` (the 0-new-post variant).

RULES CARRIED FORWARD:
  * A SUBSTANTIVE cycle is a 3-FILE commit: index.html + tweets.json +
    deploy-stamp.txt.  The staged set must be asserted EXACTLY.
  * The deploy stamp is written with the minute the COMMIT will land in
    (stamp_minute_align.py), because a minute boundary between the stamp
    write and the commit makes the next cycle's two committed anchors
    disagree.  After the commit the two anchors must agree to the minute.
  * cycle 1278 PITFALL: every git call whose output is PARSED must use an
    ARGUMENT LIST (git_list) -- a `--date=format:%Y-%m-%d %H:%M:%S` argument
    contains a SPACE, so a shell string splits it and git prints NOTHING --
    exit 0, empty stdout, silent death.  And its stdout must be asserted
    non-empty.
  * cycle 1249 PITFALL: the porcelain line is POSitional -- do NOT strip the
    whole line before slicing the path.
  * cycle 1251/1218: the URL is RE-READ from the COMMITTED stamp at HEAD,
    never hand-typed (the Vercel URL is not constant).
  * ⭐ cycle 1249 KNOWN DEFECT, FIXED: the commit message states the banner
    step against the SAME anchor the page builder used -- BOTH the published
    HEAD number AND the re-derived-at-the-cut number -- and the phrase is
    QUOTED FROM THE PAGE by regex, not re-formatted here.
  * ⭐ cycle 1251 RULE: a commit that failed its own verification must be
    UNDONE, NOT PUSHED.  The commit is written BEFORE the tree assertions
    run, so a failure there leaves a commit that exists but was never pushed.
    Detect it (HEAD names this cycle AND is ahead of origin) and SOFT-RESET
    it so the worktree and index survive, then redo it.  Refuse to reset a
    commit that is already pushed.

TWO-STAGE ONLY: nothing here pipes curl into an interpreter.
"""
import datetime as dt
import json
import os
import pathlib
import re
import subprocess

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
# ⭐ DERIVED FROM HEAD's commit subject -- this cycle's prior COMMITTED
# cycle is read from HEAD, not typed.  A cycle that RAN but did not COMMIT
# published nothing and is not in the history.
# ⭐⭐⭐ THE PRIOR COMMITTED CYCLE IS THE ONE THAT **PUBLISHED THE PAGE**
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
_pm = re.search(r"cron cycle (\d+)", PRIOR_CYCLE)
assert _pm, (
    f"the publishing commit's subject carries no `cron cycle N`: "
    f"{PRIOR_CYCLE!r}")
PRIOR_CYCLE = _pm.group(1)
# ⭐ THE EXPECTED VALUE IS DERIVED FROM AN INDEPENDENT ARTEFACT, NOT
# TYPED: the committed page's own cycle comment names the cycle that HEAD
# published.  A typed literal here is a latent assertion about a run's
# shape (Reminder 37) -- and it would have FIRED on a correct artefact
# after the previous cycle's number moved.
_committed_page = subprocess.run(
    ["git", "show", "HEAD:index.html"], cwd=str(REPO),
    capture_output=True, text=True).stdout
_cmt_m = re.search(r"<!--\s*cron cycle (\d+):", _committed_page)
assert _cmt_m, ("could not read the committed cycle number out of HEAD's "
                "page comment")
assert PRIOR_CYCLE == _cmt_m.group(1), (
    f"the prior committed cycle derived from HEAD's SUBJECT is {PRIOR_CYCLE}, "
    f"but HEAD's PAGE names {_cmt_m.group(1)} -- the two artefacts disagree")
CST = dt.timezone(dt.timedelta(hours=8))


def run(cmd, cwd=REPO, env=None):
    r = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True,
                       text=True, env=env)
    return r.returncode, r.stdout, r.stderr


def git(*args):
    return run("git " + " ".join(args))


def git_list(args, expect_out=False):
    """git with an ARGUMENT LIST, not a shell string."""
    r = subprocess.run(["git"] + list(args), cwd=str(REPO), capture_output=True,
                       text=True)
    if expect_out:
        assert r.returncode == 0, (args, r.stderr[:400])
        assert r.stdout.strip() != "", (
            f"git {args} returned EMPTY stdout with exit {r.returncode} -- a "
            "malformed invocation, not an empty result")
    return r.returncode, r.stdout, r.stderr


# ---- 0. the measurement, read back from the measurement script's output ----
_M = json.loads(pathlib.Path("/tmp/c1313/measure/measured.json")
                .read_text(encoding="utf-8"))

# ⭐⭐⭐ THE PRIOR CYCLE'S COMMIT-MESSAGE CORRECTIONS.
# ⭐⭐⭐ **A COMMIT THAT HAS BEEN PUSHED MUST NOT BE AMENDED** -- a
# force-push would leave the remote on a diverged SHA and the next push
# would be non-fast-forward, and Vercel deploys the CODE/DATA, not the
# commit text.  ⭐ **THE CORRECTION BELONGS IN THE NEXT CYCLE'S COMMIT.**
# ⭐ THIS IS WHERE IT LIVES: a corrections file, read at message-build
# time, so the correction travels with the NEXT commit.
# ⭐⭐ THE FILE LIVES IN THE REPO but is **UNTRACKED** (its name starts with
# a dot and it is in `.gitignore`), so it SURVIVES between cycles -- unlike
# a `/tmp/cNNNN/` path, which is wiped by the next cycle's own sweep.
# ⭐⭐ THE CORRECTION IS ITSELF DERIVED, NOT TYPED: it names the prior
# cycle and the sentence being corrected, and it is emitted only when the
# prior commit REALLY carries the bad sentence (so a stale correction file
# cannot publish a correction for a claim that was never made).
_PRIOR_CORRECTIONS = REPO / ".pending_corrections.json"
_CORRECTION_LINES = []
if _PRIOR_CORRECTIONS.exists():
    _corr = json.loads(_PRIOR_CORRECTIONS.read_text(encoding="utf-8"))
    _prior_cmt = subprocess.run(
        ["git", "log", "-1", "--format=%B", f"{_corr['prior_cycle']}"],
        cwd=REPO, capture_output=True, text=True).stdout
    for _c in _corr.get("corrections", []):
        if _c["bad_sentence"] in _prior_cmt:
            _CORRECTION_LINES.append(
                f"- ⭐ CORRECTION to cycle {_corr['prior_cycle']}: the prior "
                f"commit message said {_c['bad_sentence']!r}, which is FALSE. "
                f"{_c['correction']}")
            print(f"[commit] carrying a CORRECTION to cycle "
                  f"{_corr['prior_cycle']}: {_c['bad_sentence']!r}")
        else:
            print(f"[commit] the correction for cycle {_corr['prior_cycle']} "
                  f"is NOT APPLICABLE -- the prior commit does not carry "
                  f"{_c['bad_sentence']!r} (a stale correction file must not "
                  f"publish a correction for a claim that was never made)")
if _CORRECTION_LINES:
    print(f"[commit] {len(_CORRECTION_LINES)} correction line(s) to carry")

_measured_zero = int(_M["measured_zero"])
_old_at_cut = int(_M["old_banner"])
_head_banner = int(_M["head_banner"]) if "head_banner" in _M else None
_landed = int(_M["landed"])
_cut = str(_M["cut"])
assert _M["band"] == "OUT_OF_BAND", (
    f"the measurement says band={_M['band']!r}, expected OUT_OF_BAND")
assert _M["writer_guard"] == "NO_EVIDENCE_THIS_HOUR", (
    f"the measurement says writer_guard={_M['writer_guard']!r}, expected "
    "NO_EVIDENCE_THIS_HOUR")
_HOUR_UTC = int(_M["cycle_hour_utc"])

# ⭐ THE STEP PHRASE IS EXTRACTED FROM THE PAGE, NOT RE-FORMATTED HERE.
_PG = (REPO / "index.html").read_text(encoding="utf-8")
_sm2 = re.search(r"(\d+ published -> \d+ re-derived at the cut \(\d{2}:\d{2}\) "
                 r"-> \d+ measured \(\+\d+ landed\))", _PG)
assert _sm2, (
    "the page does not carry the banner step phrase — the commit message "
    "quotes the page, so the page must carry it")
STEP_PHRASE = _sm2.group(1)
assert STEP_PHRASE.startswith(f"{_old_at_cut} published") or \
    STEP_PHRASE.startswith(f"{_head_banner} published"), (
    f"the page's step phrase starts from {STEP_PHRASE!r}, but HEAD published "
    f"{_head_banner} — the page and the measurement disagree")
assert f"-> {_measured_zero} measured" in STEP_PHRASE, (
    f"the page's step phrase does not end at the measured {_measured_zero}")
print(f"[commit] the banner step, QUOTED FROM THE PAGE: {STEP_PHRASE}")

# ---- 0b. A COMMIT THAT FAILED ITS OWN VERIFICATION MUST BE UNDONE, NOT PUSHED.
_rc0, _log0, _e0 = git_list(["log", "-1", "--format=%H%x00%s"], expect_out=True)
_sha0, _subj0 = _log0.strip().split("\x00", 1)
if f"cycle {CYCLE}" in _subj0:
    _ahead = subprocess.run(
        ["git", "rev-list", "--count", f"origin/main..{_sha0}"],
        cwd=str(REPO), capture_output=True, text=True).stdout.strip()
    print(f"[commit] HEAD ({_sha0[:7]}) already names cycle {CYCLE} and is "
          f"{_ahead} commit(s) ahead of origin -> it failed its own "
          f"verification and was never pushed; resetting it (soft) to redo it")
    assert _ahead != "0", (
        "HEAD names this cycle and is ALREADY PUSHED -- do not reset a pushed "
        "commit; report the discrepancy instead")
    rc, out, err = git("reset", "--soft", "HEAD~1")
    assert rc == 0, f"the soft reset failed: {err[:300]}"
    print("[commit] reset OK; HEAD is now "
          + subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO),
                            capture_output=True, text=True).stdout.strip()[:7])

# ---- 1. the stamp: THIS cycle's number first, then the minute-align ----
rc, out, err = git("show", "HEAD:deploy-stamp.txt")
assert rc == 0, err
_head_stamp = out.strip()
_hm = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) CST = cycle (\d+) = (\S+)",
               _head_stamp)
assert _hm, f"unparseable committed stamp: {_head_stamp!r}"
assert _hm.group(2) == PRIOR_CYCLE, (
    f"HEAD's stamp names cycle {_hm.group(2)}, expected {PRIOR_CYCLE}")
STAMP_URL = _hm.group(3)
_now_cst = dt.datetime.now(CST)
(REPO / "deploy-stamp.txt").write_text(
    f"{_now_cst:%Y-%m-%d %H:%M} CST = cycle {CYCLE} = {STAMP_URL}\n",
    encoding="utf-8")
print(f"[commit] stamp written for cycle {CYCLE} (URL re-read from HEAD: "
      f"{STAMP_URL})")

rc, out, err = run("/usr/bin/python3 ~/.hermes/skills/elon-tweets-cron/scripts/"
                   "stamp_minute_align.py")
print(out.strip())
if err.strip():
    print("[commit] stamp stderr:", err.strip()[:400])
assert rc == 0, "the stamp minute-align failed"

stamp = (REPO / "deploy-stamp.txt").read_text(encoding="utf-8").strip()
print(f"[commit] deploy-stamp.txt = {stamp}")
m = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) CST = cycle (\d+) = (\S+)", stamp)
assert m, f"unparseable stamp: {stamp!r}"
assert m.group(2) == CYCLE, f"the stamp names cycle {m.group(2)}, not {CYCLE}"
assert m.group(3) == STAMP_URL, "the stamp lost the URL"

# ---- 2. assert the CHANGED SET is exactly the THREE files ----
rc, out, err = git("status", "--porcelain")
assert rc == 0, err
changed = []
for ln in out.splitlines():
    if not ln.strip():
        continue
    code, path = ln[:2], ln[3:]      # POSITIONAL -- do not strip the line
    if code == "??":
        continue                       # untracked scratch is NOT part of it
    changed.append(path)
print(f"[commit] tracked changes: {changed}")
# ⭐⭐⭐⭐⭐ CYCLE 1255's FIX -- THE STAGED SET IS DERIVED FROM THE SHAPE,
# NOT TYPED.  ⭐⭐⭐⭐⭐ A SUBSTANTIVE cycle is a **3-FILE** commit
# (index.html + tweets.json + deploy-stamp.txt); a MEASURED NO-OP is a
# **2-FILE** commit (index.html + deploy-stamp.txt) and MUST NOT change the
# corpus.  ⭐⭐⭐⭐⭐ **THE FILE COUNT IS A DERIVED CONSTANT, LIKE EVERY
# OTHER COUNT ON THIS PAGE** (Reminder 37) -- a typed 3 is a LATENT
# ASSERTION ABOUT THE RUN'S SHAPE, and it fires on a CORRECT NO-OP.
_ADJ_PRE = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                      .read_text(encoding="utf-8"))
_IS_NOOP = (len(_ADJ_PRE["real_new"]) == 0)
_CYCLE_CLASS = "MEASURED NO-OP" if _IS_NOOP else "SUBSTANTIVE"
_EXPECTED_FILES = ({"index.html", "deploy-stamp.txt"} if _IS_NOOP
                   else {"index.html", "tweets.json", "deploy-stamp.txt"})
print(f"[commit] the branch selector: {_CYCLE_CLASS} -> a "
      f"{len(_EXPECTED_FILES)}-FILE commit; the expected set is "
      f"{sorted(_EXPECTED_FILES)}")
assert set(changed) == _EXPECTED_FILES, (
    f"the staged set must be EXACTLY {sorted(_EXPECTED_FILES)} (a "
    f"{_CYCLE_CLASS} cycle is a {len(_EXPECTED_FILES)}-FILE commit), got "
    f"{changed}")

# tweets.json MUST differ from HEAD (this cycle published 7 posts) AND the
# committed records must all survive byte-identically.
rc, out, err = git("show", "HEAD:tweets.json")
assert rc == 0, err
_committed = json.loads(out)
_now = json.loads((REPO / "tweets.json").read_text(encoding="utf-8"))
_ADJ = _ADJ_PRE
_N_PUBLISHED = len(_ADJ["real_new"])
if _IS_NOOP:
    # ⭐⭐⭐⭐⭐ A MEASURED NO-OP MUST NOT CHANGE THE CORPUS -- and these
    # TWO ASSERTIONS ARE STRONGER than the SUBSTANTIVE branch's.  ⭐⭐⭐⭐⭐
    # The corpus must be BYTE-IDENTICAL to HEAD and the head must NOT have
    # moved.
    assert len(_now) == len(_committed), (
        f"a MEASURED NO-OP must not add records: HEAD holds {len(_committed)}, "
        f"the corpus holds {len(_now)}")
    assert json.dumps(_now, ensure_ascii=False, sort_keys=True) == \
        json.dumps(_committed, ensure_ascii=False, sort_keys=True), (
        "a MEASURED NO-OP must leave the corpus BYTE-IDENTICAL to HEAD")
    print(f"[commit] (NO-OP) the corpus is byte-identical to HEAD's "
          f"{len(_committed)} records and the head has not moved")
    _new_ids = []
else:
    assert len(_now) == len(_committed) + _N_PUBLISHED, (
        f"tweets.json has {len(_now)} records, expected "
        f"{len(_committed) + _N_PUBLISHED} (HEAD + published)")
    _new_ids = [t["id"] for t in _now
                if t["id"] not in {x["id"] for x in _committed}]
    assert len(_new_ids) == _N_PUBLISHED, (
        f"the worktree delta has {len(_new_ids)} new ids, but the adjudication "
        f"published {_N_PUBLISHED}: {_new_ids}")
    print(f"[commit] tweets.json: {len(_committed)} (HEAD) -> {len(_now)}; "
          f"new ids = {_new_ids}")


def _canon(rec):
    return json.dumps(rec, ensure_ascii=False, sort_keys=True)



# ⭐⭐⭐⭐⭐ **THE "PURE ADDITION" INVARIANT -- WITH ITS *SCOPE*.**
# ⭐⭐⭐⭐⭐ **⇒ AN INVARIANT CAN BE CORRECT AND STILL BE INCOMPLETE -- IT
# NEEDS A *SCOPE*, NOT A *RELAXATION*** (cycle 1288's class-level rule).
# ⭐⭐⭐⭐⭐ **⇒ THE SCOPE IS EXACTLY: a DECLARED, RE-MEASURED, FIELD-LEVEL
# CORRECTION** (`.pending_record_corrections.json`).  ⭐⭐⭐⭐⭐ **⇒ AN
# UNDECLARED DIFFERENCE IS STILL A HARD FAILURE** -- the gate is REFINED,
# never relaxed.
_DECL_PATH = pathlib.Path("/Users/taeyeon093.bot/elon-tweets"
                          "/.pending_record_corrections.json")


def _declared_field_corrections():
    """The DECLARED, field-level corrections -- read from the channel.

    ⭐⭐⭐⭐⭐ **THE `from` VALUE IS *MEASURED* FROM HEAD AND THE `to` VALUE
    IS *MEASURED* FROM THE WORKTREE -- NEVER TYPED** ⇒ ⇒ **⇒ A STALE
    DECLARATION CANNOT AUTHORISE A CHANGE** (it would fail the equality
    check below and abort the chain).
    ⭐⭐⭐⭐⭐ **⇒ AND ONLY THE *FETCHER-OWNED* FIELDS ARE CORRECTABLE** --
    a difference in a field the PIPELINE ITSELF DERIVES is a REAL DEFECT,
    never a correction.
    """
    _CORRECTABLE = ("pinned", "is_retweet", "is_quote", "images")
    if not _DECL_PATH.exists():
        return {}
    try:
        _doc = json.loads(_DECL_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    out = {}
    for _c in _doc.get("record_corrections", []):
        _f = _c.get("field")
        if _f not in _CORRECTABLE:
            continue
        out[(_c.get("id"), _f)] = _c
    return out


def _assert_delta_is_a_pure_addition(head_by_id, out_by_id, canon, label,
                                _head_recs, _out_recs):
    """The 'never a rewrite' gate -- WITH ITS SCOPE.

    ⭐⭐⭐⭐⭐ **⇒ THE ASSERT PRECEDES ANY WRITE** (1288's ordering rule: a
    fix that moved the write before the assertion would be a REGRESSION).
    ⭐⭐⭐⭐⭐ **⇒ RETURNS THE LIST OF *UNDECLARED* DIFFERENCES** (empty ==
    the delta is a pure addition *modulo the declared corrections*).
    """
    _declared = _declared_field_corrections()
    _changed, _undeclared = [], []
    for _tid, _c in head_by_id.items():
        _now = out_by_id.get(_tid)
        if _now == _c:
            continue
        _changed.append(_tid)
        # the difference must be EXACTLY a declared, re-measured field
        _ok = False
        for (_did, _df), _dc in _declared.items():
            if _did != _tid:
                continue
            _head_rec = _head_recs.get(_tid)
            _out_rec = _out_recs.get(_tid)
            if _head_rec is None or _out_rec is None:
                continue
            if _head_rec.get(_df) != _dc.get("from"):
                continue
            if _out_rec.get(_df) != _dc.get("to"):
                continue
            # ⭐⭐⭐⭐⭐ THE DIFFERENCE MUST BE *EXACTLY* THE DECLARED FIELD
            _diff_fields = {k for k in set(_head_rec) | set(_out_rec)
                            if _head_rec.get(k) != _out_rec.get(k)}
            if _diff_fields == {_df}:
                _ok = True
                break
        if not _ok:
            _undeclared.append(_tid)
    assert not _undeclared, (
        f"these COMMITTED records changed in an UNDECLARED way: "
        f"{_undeclared[:8]} -- the delta must be an ADDITION (or exactly a "
        f"DECLARED, RE-MEASURED field correction), never a rewrite")
    return _changed


_committed_by_id = {t["id"]: _canon(t) for t in _committed}
_now_by_id = {t["id"]: _canon(t) for t in _now}
_committed_recs = {t["id"]: t for t in _committed}
_now_recs = {t["id"]: t for t in _now}
_changed_committed = _assert_delta_is_a_pure_addition(
    _committed_by_id, _now_by_id, _canon, "commit",
    _committed_recs, _now_recs)
print(f"[commit] all {len(_committed)} committed records are BYTE-IDENTICAL; "
      f"the delta is a PURE ADDITION of {_new_ids}")

# ---- 3. stage EXACTLY the files this shape requires ----
_STAGE = sorted(_EXPECTED_FILES)
rc, out, err = git("add", *_STAGE)
assert rc == 0, err
rc, out, err = git("diff", "--cached", "--name-only")
assert rc == 0, err
staged = [x.strip() for x in out.splitlines() if x.strip()]
print(f"[commit] staged: {staged}")
assert set(staged) == _EXPECTED_FILES, (
    f"the staged set must be EXACTLY {sorted(_EXPECTED_FILES)}, got {staged}")

# ---- 4. the commit message ----
idx = (REPO / "index.html").read_text(encoding="utf-8")
ban = int(re.search(r"<strong>(\d+)</strong> 次回傳", idx).group(1))
_old_ban = int(re.search(r"<strong>(\d+)</strong> 次回傳",
                         git_list(["show", "HEAD:index.html"],
                                  expect_out=True)[1]).group(1))
_rc, _stamp_h, _e = git_list(["show", "HEAD:deploy-stamp.txt"], expect_out=True)
_rc2, _commit_h, _e2 = git_list(
    ["show", "-s", "--format=%ad", "--date=format:%Y-%m-%d %H:%M:%S", "HEAD"],
    expect_out=True)
_sm = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) CST", _stamp_h.strip())
assert _sm, f"unparseable committed stamp: {_stamp_h!r}"
_skew = abs((dt.datetime.strptime(_commit_h.strip(), "%Y-%m-%d %H:%M:%S")
             - dt.datetime.strptime(_sm.group(1), "%Y-%m-%d %H:%M")).total_seconds())
print(f"[commit] banner {_old_ban} -> {ban}; anchor skew {_skew:.0f} s")
recs = len(_now)
_adj = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                  .read_text(encoding="utf-8"))
_ok200 = sorted([r for r in _adj["rows"] if r["http"] == 200],
                key=lambda r: r["snowflake_ts"])
_authors = " / ".join(sorted({r["author"] for r in _ok200}))
_n404 = sum(1 for r in _adj["rows"] if r["http"] == 404)
_ncand = len(_adj["rows"])
_npaths = len(_adj["answered_paths"]) + len(_adj["unavailable_paths"])
_nans = len(_adj["answered_paths"])
assert _ok200, "no candidate resolved 200 -- the commit message would be vacuous"
_nreal = len(_adj["real_new"])
assert _nreal == _N_PUBLISHED, (
    f"the adjudicated real-new count {_nreal} != the published count "
    f"{_N_PUBLISHED}")
_ids = ", ".join(r["id"] for r in _ok200)
_new_ids_desc = ", ".join(_new_ids)
_guard = int(_M["guard_derived"])
assert _M["band"] == "OUT_OF_BAND", "the band must be OUT_OF_BAND"
assert _M["writer_guard"] == "NO_EVIDENCE_THIS_HOUR", (
    f"the measurement says writer_guard={_M['writer_guard']!r}, expected "
    "NO_EVIDENCE_THIS_HOUR -- on an OUT-OF-BAND hour the branch NEVER "
    "RAN, so the count is BORROWED from the POSITIVE CONTROL, "
    "so there is NO guard evidence for this hour")
assert f"Hour {_HOUR_UTC} UTC" in _PG, (
    f"the page's comment does not name Hour {_HOUR_UTC} UTC -- the commit "
    "message's hour and the page's hour must agree")

# ⭐ THE RENDER'S NEWEST-COUNT IS READ FROM THE VISIBLE LAYER (lxml), NOT
# from the raw HTML -- the phrase exists only in the VISIBLE text, and
# `len(re.findall(..., raw_html))` returned [] on cycle 1278, which
# published a 0-newest subject.
from lxml import html as lxml_html          # noqa: E402
_lx = lxml_html.fromstring(idx)
for _bad in _lx.xpath("//script | //style | //head"):
    _bad.getparent().remove(_bad)
_visible = re.sub(r"\s+", " ", _lx.text_content() or "").strip()
_newn = re.search(r"置頂貼文 1 則 \+ 最新 (\d+) 則", _visible)
assert _newn, (
    "the VISIBLE layer does not state the render's newest-count -- the "
    "count must be read from the layer where the phrase lives")
_render_newest_n = int(_newn.group(1))
print(f"[commit] the render's newest-count, read from the VISIBLE layer: "
      f"{_render_newest_n}")

# ⭐ THE PAGE'S PUBLISHED-COUNT PROSE IS READ FROM THE VISIBLE LAYER TOO.
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
    assert not re.search(r"找到了 \d+ 則新推文", _visible), (
        "the VISIBLE layer carries a SUBSTANTIVE published-count clause on a "
        "MEASURED NO-OP")
    print("[commit] (NO-OP) the VISIBLE layer carries the NO-OP prose and NO "
          "SUBSTANTIVE published-count clause")
else:
    _pv = re.search(r"找到了 (\d+) 則新推文", _visible)
    assert _pv, "the VISIBLE layer does not state the published-post count"
    assert int(_pv.group(1)) == _N_PUBLISHED, (
        f"the visible page says {int(_pv.group(1))} 則新推文 but the "
        f"adjudication published {_N_PUBLISHED}")
    assert "未發現新推文" not in _visible, (
        "the visible page still carries the 0-new-post prose -- this cycle "
        f"published {_N_PUBLISHED}")

# ⭐⭐⭐ THE DEFECT SENTENCE IS **DERIVED FROM THE PROVENANCE ARTEFACT**,
# NEVER TYPED (Reminder 37 / Reminder 53: a typed literal is a latent
# assertion about the run's shape, and it PUBLISHES A FALSE CLAIM when the
# run does not match it).
# ⭐⭐⭐ THIS FIRED ON THIS CYCLE'S FIRST RUN: the sentence was the FIXED
# "all {_N_PUBLISHED} published record(s) scored 0 defects", while ONE of
# the two records carries **1 RECORDED FIDELITY DEFECT** (`with`, at corpus
# keep-rate 2/998).  The commit script never read the provenance artefact
# at all, so it could not have known -- and the false sentence was
# PUBLISHED.  ⭐ **A COMMIT MESSAGE IS A PUBLICATION; A PUBLISHED CLAIM
# MUST BE DERIVED FROM THE ARTEFACT IT DESCRIBES.**  ⭐ Note the deeper
# shape: the defect was RECORDED (never silently dropped -- Reminder 27's
# "derive, never relax"), and the PAGE carries the record of it; only the
# commit message contradicted it.
# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX (ported from 1260): **THE PROVENANCE REGION IS
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
# ⭐⭐⭐⭐⭐ **THE COUNT IS A MACHINE-READABLE FIELD, AND THE FIELD IS
# RE-DERIVED HERE -- NEVER COPIED, NEVER PARSED OUT OF PROSE.**
#
# ⭐⭐⭐⭐⭐ **WHY THIS IS A FIX AND NOT A LOOSENING:** this cycle's FIRST
# commit run was BLOCKED by this very gate on a PERFECTLY VALID artefact,
# because the producer's wording was `RETRY #2 (this cycle); 0 defects`
# and none of the three prose patterns ("scored N defects", "still N
# defects", "N fidelity defect") matched it.  ⭐⭐⭐ **A CONSUMER THAT
# PARSES PROSE IS THE DEFECT** -- the producer's WORDING IS NOT A
# CONTRACT, so a prose parser is a false-positive generator: it rejects
# valid artefacts, and it will reject the next valid artefact too.
#
# ⭐⭐⭐⭐⭐ **AND THE FIELD'S VALUE IS A CLAIM; THE INSTRUMENT'S SCORE IS A
# MEASUREMENT.**  So this consumer RE-SCORES every published record with
# **THIS CYCLE'S OWN instrument** against **THIS CYCLE'S OWN corpus**, and
# ASSERTS the field agrees with the measurement.  ⭐⭐⭐ **THE MEASUREMENT
# WINS**: a disagreement means the field is wrong, and the commit message
# must describe the measured reality.
#
# ⭐⭐⭐⭐⭐ **AND THE RE-SCORING INSTRUMENT MUST BE PROVED ABLE TO FIRE** --
# otherwise "0 defects from every instrument" is vacuous.
# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX (ported from 1260): **THE RE-SCORING BLOCK IS
# NOT EXERCISED ON A MEASURED NO-OP.**  ⭐⭐⭐⭐⭐ There are ZERO published
# records to re-score, so loading the instrument and proving it can fire
# would be a **VACUOUS verification** -- it would prove the instrument
# works, and say nothing about the zero. ⭐⭐⭐⭐⭐ THE NO-OP's PROOF is the
# ZERO's OWN cross-check: the adjudication judged a NON-EMPTY candidate
# set and at least one candidate resolved 200 (asserted above).
if _IS_NOOP:
    _DEFECT_COUNTS = {}
    _N_ZERO = 0
    _N_DEFECTIVE = 0
    print("[commit] (NO-OP) no record was published, so the re-scoring "
          "instrument was NOT loaded -- loading it would be a VACUOUS "
          "verification of the zero")
else:
    import importlib.util                    # noqa: E402


    def _load_module(path, name):
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


    _fid = _load_module(REPO / f"_c{CYCLE}_fidelity2.py", "fid_commit")
    _corpus = json.loads(subprocess.run(
        ["git", "show", "HEAD:tweets.json"], cwd=str(REPO),
        capture_output=True, text=True).stdout)
    _keep, _pair_total, _pair_kept = _fid.build_corpus_stats(_corpus)
    # ⭐⭐⭐ THE RE-SCORING CORPUS IS **HEAD's** corpus (the COMMITTED one), so
    # the measurement is reproducible from the committed state -- not from a
    # worktree that this very cycle has already written to.
    _work = {t["id"]: t for t in json.loads(
        (REPO / "tweets.json").read_text(encoding="utf-8"))}
    _FINAL = json.loads(pathlib.Path("/tmp/c1313/translate/translations_final.json")
                        .read_text(encoding="utf-8"))

    # ---- the instrument must be PROVED ABLE TO FIRE before it is trusted --
    _KNOWN_BAD_ORIG = ("Another 27 Starlink satellites\n\n"
                        "Falcon 9 launches 27 @Starlink satellites from California")
    _KNOWN_BAD = "又有 27 顆星鏈衛星\n\n獵鷹 9 號從加州發射 27 顆衛星"
    _sb = _fid.score(_KNOWN_BAD, _KNOWN_BAD_ORIG, _keep, _pair_total, _pair_kept)
    assert _sb["defects"] > 0, (
        "[commit] the re-scoring instrument reports 0 on a KNOWN-BAD "
        "translation -- it cannot see a defect, so its verdict on the real "
        "records is VACUOUS")
    _KNOWN_GOOD = "又有 27 顆 Starlink 衛星\n\nFalcon 9 從加州發射 27 顆衛星"
    _sg = _fid.score(_KNOWN_GOOD, _KNOWN_BAD_ORIG, _keep, _pair_total, _pair_kept)
    assert _sg["defects"] == 0, (
        f"[commit] the re-scoring instrument flags a KNOWN-GOOD translation: "
        f"{_sg}")
    print(f"[commit] the re-scoring instrument is PROVED ABLE TO FIRE: "
          f"KNOWN-BAD -> {_sb['defects']} defect(s), KNOWN-GOOD -> "
          f"{_sg['defects']}")

    _DEFECT_COUNTS = {}
    for _tid, _p in _PROV.items():
        # ---- (1) the CLAIM: the machine-readable field -------------------
        if isinstance(_p, dict) and "defects" in _p:
            _claim = int(_p["defects"])
        else:
            # ⭐⭐⭐⭐⭐ THE FALLBACK IS FOR AN OLDER ARTEFACT ONLY -- and it is
            # EXPLICITLY LABELLED as such, because a prose parse is a claim
            # about a shape the producer may not have used.
            _m = re.search(r"(\d+)\s+fidelity defect", str(_p))
            if _m is None:
                _m = re.search(r"still\s+(\d+)\s+defects", str(_p))
            if _m is None:
                _m = re.search(r"scored\s+(\d+)\s+defects", str(_p))
            assert _m is not None, (
                f"{_tid}: the provenance states no defect count: {_p!r} -- the "
                "defect count MUST be readable from the artefact, never "
                "assumed")
            _claim = int(_m.group(1))
            print(f"[commit] {_tid}: the provenance is an OLDER PROSE artefact -- "
                  f"the fallback read {_claim} (LABELLED: a prose parse, not a "
                  "machine-readable field)")

        # ---- (2) the MEASUREMENT: re-score with THIS cycle's instrument ---
        assert _tid in _work, f"{_tid} is not in the worktree corpus"
        assert _tid in _FINAL, f"{_tid} is not in the published translations"
        _ms = _fid.score(_FINAL[_tid], _work[_tid]["original"],
                          _keep, _pair_total, _pair_kept)
        _measured = int(_ms["defects"])
        # ⭐⭐⭐⭐⭐ THE MEASUREMENT WINS.  A disagreement is NOT silently
        # reconciled -- it is ASSERTED, because it means the artefact's field
        # is WRONG (and the commit message would publish the wrong claim).
        assert _claim == _measured, (
            f"{_tid}: the provenance's `defects` field claims {_claim} but THIS "
            f"cycle's own instrument MEASURED {_measured} (added={_ms['added']} "
            f"dropped={_ms['dropped']}) -- the MEASUREMENT wins, and the "
            "artefact's field is wrong")
        _DEFECT_COUNTS[_tid] = _measured
    print(f"[commit] the defect counts are MEASURED (re-scored by this cycle's "
          f"own instrument) and AGREE with the artefact's fields: "
          f"{_DEFECT_COUNTS}")
    _N_ZERO = sum(1 for _v in _DEFECT_COUNTS.values() if _v == 0)
    _N_DEFECTIVE = sum(1 for _v in _DEFECT_COUNTS.values() if _v > 0)
    assert _N_ZERO + _N_DEFECTIVE == _N_PUBLISHED, (
        f"the defect split ({_N_ZERO} zero + {_N_DEFECTIVE} defective) does not "
        f"equal the published count ({_N_PUBLISHED})")
    print(f"[commit] defect counts DERIVED from the provenance artefact: "
          f"{_DEFECT_COUNTS} ({_N_ZERO} zero-defect, {_N_DEFECTIVE} with a "
          f"recorded defect)")
# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX (ported from 1260): **THE DEFECT SENTENCE IS
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
elif _N_DEFECTIVE == _N_PUBLISHED:
    _DEFECT_SENTENCE = (
        f"all {_N_PUBLISHED} published record(s) carry a RECORDED fidelity "
        f"defect -- the defect is RECORDED, never silently dropped, and the "
        f"refused exemption was NOT applied")
else:
    # ⭐ DERIVE THE GRAMMAR TOO, NOT JUST THE NUMBERS (Reminder 58).
    _carry = ("record carries" if _N_DEFECTIVE == 1 else "records carry")
    _DEFECT_SENTENCE = (
        f"{_N_ZERO} of the {_N_PUBLISHED} published record(s) scored 0 "
        f"defects and {_N_DEFECTIVE} {_carry} a RECORDED fidelity defect "
        f"-- the defect is RECORDED, never silently dropped")

# ⭐⭐ THE PROVENANCE PARAGRAPH IS **DERIVED FROM THE SPLIT**, NOT COPIED.
# The inherited sentence ("EMPTY THIS TIME ... the {n} BRAND-NEW one is")
# asserts a shape that is FALSE for a cycle whose split is 2-inherited /
# 0-brand-new -- and its "the {n} ... one" grammar only reads correctly when
# exactly ONE id is brand-new.  The prose is chosen by the MEASURED counts,
# so it is true for ANY shape.
_n_inh = len(_adj["inherited"])
_n_bnew = len(_adj["brand_new"])
# ⭐⭐⭐⭐⭐ CYCLE 1272's FIX (from cycle 1271's handover): **THE GRAMMAR IS
# DERIVED FROM THE COUNT IN *EVERY* BRANCH**, not hard-coded in one.
# ⭐⭐⭐⭐⭐ Cycle 1273 published "The 2 BRAND-NEW **one** is" -- the
# `_n_inh == 0` branch hard-coded the SINGULAR; and the `else` branch
# hard-coded the PLURAL, which would be wrong for a cycle with exactly
# ONE brand-new post.  ⭐⭐⭐⭐⭐ **A FIX THAT ADDRESSES ONLY THE SITE THE
# LAST CYCLE HAPPENED TO PUBLISH IS NOT A FIX.**  ⭐⭐⭐⭐⭐ The variable is
# PRE-COMPUTED (not spliced into the f-string chain -- that is a SYNTAX
# ERROR) and it is derived from the SAME `_n_bnew` the counts come from,
# so the two publishers cannot disagree.
_BNEW_VERB = "one is" if _n_bnew == 1 else "ones are"
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
elif _n_inh == 0:
    _prov_para = (
        f"- ⭐ THE PROVENANCE SPLIT IS MEASURED, AND IT IS EMPTY THIS TIME: "
        f"0 of the {_nreal} were written by an earlier cycle and never "
        f"committed, so there was nothing to inherit and nothing to "
        f"re-adjudicate. The prior COMMITTED cycle ({PRIOR_CYCLE}) published "
        f"normally. The {_n_bnew} BRAND-NEW "
        f"{'one is' if _n_bnew == 1 else 'ones are'} "
        f"{', '.join(_adj['brand_new'])} -- the source population MOVES "
        f"every hour, and the earlier cycles' own probes could not have "
        f"seen it")
elif _n_bnew == 0:
    _prov_para = (
        f"- ⭐ THE PROVENANCE SPLIT IS MEASURED, AND IT IS **NOT** EMPTY: "
        f"ALL {_n_inh} of the {_nreal} published posts were written by an "
        f"earlier cycle and NEVER COMMITTED -- they are INHERITED "
        f"worktree-only records, and a worktree-only delta is a LIABILITY, "
        f"not an asset. This cycle RE-DERIVED its own candidate set, "
        f"re-adjudicated every one of them from scratch (an INDEPENDENT "
        f"clock AND an INDEPENDENT author check), and re-fetched each one's "
        f"content TWICE, independently. NOTHING was taken on an earlier "
        f"cycle's word. The inherited ids are "
        f"{', '.join(_adj['inherited'])}")
else:
    _prov_para = (
        f"- ⭐ THE PROVENANCE SPLIT IS MEASURED: {_n_inh} of the {_nreal} "
        f"were written by an earlier cycle and never committed (they are "
        f"INHERITED worktree-only records -- LIABILITIES, not assets -- and "
        f"this cycle re-adjudicated and re-fetched each of them from "
        f"scratch); the remaining {_n_bnew} BRAND-NEW "
        f"{'one is' if _n_bnew == 1 else 'ones are'} "
        f"{', '.join(_adj['brand_new'])} -- the source population MOVES "
        f"every hour, and the earlier cycles' own probes could not have "
        f"seen them")

# ⭐⭐⭐⭐⭐ CYCLE 1261's FIX (ported from 1260): **THE COMMIT MESSAGE IS
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
                  "and the text\n")
    _msg_gate = ("THIS cycle the calibrated BIDIRECTIONAL instrument's "
                 "fire-test ran UNCONDITIONALLY before any record was "
                 "scored (KNOWN-BAD -> 1 defect, KNOWN-GOOD -> 0), and "
                 f"{_DEFECT_SENTENCE}\n")
    _msg_corpus = (f"- tweets.json: {recs} records, a PURE ADDITION of "
                   f"{_new_ids_desc}; all {len(_committed)} committed "
                   f"records are BYTE-IDENTICAL\n")
else:
    _msg_authors = ""
    _msg_fetch = ("- NO POST WAS PUBLISHED, SO NO POST WAS FETCHED -- and no "
                  "post was re-scored for fidelity defects; the zero is "
                  "proved by the adjudication's OWN non-empty candidate set "
                  "and its cross-check, not by a vacuous 0-of-0 "
                  "verification\n")
    _msg_gate = ("on a MEASURED NO-OP the instrument was NOT loaded, because "
                 "a 0-of-0 re-scoring would be a VACUOUS verification -- "
                 f"{_DEFECT_SENTENCE}\n")
    _msg_corpus = (f"- tweets.json: {recs} records, BYTE-IDENTICAL to HEAD "
                   f"-- a MEASURED NO-OP adds NOTHING, and all "
                   f"{len(_committed)} committed records survive "
                   f"unchanged\n")

MSG = (
    f"chore: hourly cron cycle {CYCLE}, {len(_EXPECTED_FILES)}-FILE commit — "
    f"{_CYCLE_CLASS}: "
    f"{_N_PUBLISHED} NEW POSTS published; the render's [PIN] + "
    f"[{_render_newest_n} newest] structure is RE-DERIVED "
    f"and cycle 1278's correction is KEPT\n\n"
    + (("\n".join(_CORRECTION_LINES) + "\n") if _CORRECTION_LINES else "")
    + "\n"
    f"- the fetcher is still blind and its 0 is UNRELIABLE (banner {ban} "
    f"zero-article passes); the independent read path did the work\n"
    f"- {_ncand} candidate ids adjudicated on api.fxtwitter.com (clock AND "
    f"author, both independent): {_n404} HTTP 404, {len(_ok200)} resolve 200 "
    f"(authors: {_authors}) -> {_nreal} REAL NEW POSTS{_msg_authors}\n"
    f"{_prov_para}\n"
    f"- published ids: {_new_ids_desc}\n"
    f"{_msg_fetch}"
    f"- the sort_index counters decoded to this cycle's OWN hour, so the trap "
    f"fired live; every candidate id was enumerated from a NAMED id-bearing "
    f"key and proven textually under it\n"
    f"- Phase 0.5 OUT OF BAND (hour {_HOUR_UTC}): the retry branch NEVER "
    f"RAN in THIS HOUR; "
    f"writer_guard = NO_EVIDENCE_THIS_HOUR; "
    f"the count {_guard} is derived from source and EQUALS the POSITIVE "
    f"CONTROL's reported count -- it is BORROWED and explicitly DISCLAIMED "
    f"as this hour's evidence. The NEGATIVE CONTROL (the most recent "
    f"OUT-OF-BAND block) "
    f"carries NEITHER marker NOR the guard's SKIPPED line, so the matcher "
    f"DISCRIMINATES. The prior COMMITTED cycle ({PRIOR_CYCLE}) was ALSO "
    f"out of band, so the control set is UNCHANGED, NOT flipped\n"
    f"- {_nans} of {_npaths} read paths answered 200; the rest recorded "
    f"UNAVAILABLE (syndication 429), never as agreement\n"
    f"- banner {STEP_PHRASE}, measured from fetch.log and reconciled under "
    f"ALL THREE committed cuts ({_skew:.0f} s skew proven benign); the step is "
    f"stated against BOTH anchors so the arithmetic that closes is "
    f"unambiguous (cycle 1249's known defect, fixed)\n"
    f"- ⭐ THE PAGE BANNER IS REPLACED AS A WHOLE <div>. Cycle 1251's FIRST "
    f"build defined the SUBSTANTIVE banner but substituted only its COUNTER, "
    f"so the VISIBLE prose still read the MEASURED NO-OP wording while the "
    f"cycle comment "
    f"claimed {_nreal} published posts -- a self-contradicting page. The "
    f"PRE-WRITE PAYLOAD GATE now asserts the banner's prose BEFORE the "
    f"write, and the old-region splice matches the cycle comment as a WHOLE "
    f"comment (the old shape swallowed it and left a stray '-->', giving an "
    f"unbalanced page)\n"
    f"- ⭐ THE CYCLE'S HOUR IS DERIVED FROM THE LOG, NOT THE WALL CLOCK. "
    f"A cycle can be INTERRUPTED and RESUMED in a later hour; the wall clock "
    f"measures WHEN THE SCRIPT RAN, not the hour the cycle belongs to. The "
    f"band and the hour now live in measured.json and every consumer reads "
    f"them from there\n"
    f"- ⭐ THE DERIVED RATE BAND EXCLUDES THE IN-PROGRESS HOUR. The "
    f"outage-span rate is {_M['outage_rate']}/hour (band "
    f"{_M['rate_band_lo']}-{_M['rate_band_hi']}, DERIVED from the log's own "
    f"per-hour cadence over COMPLETE hours only) and the recent-window rate "
    f"is {_M['recent_rate']}/hour (band {_M['recent_band_lo']}-"
    f"{_M['recent_band_hi']}, also DERIVED from the log's own per-hour "
    f"counts over the SAME window, over COMPLETED hours only). The band is "
    f"DERIVED, not typed: the typed 1.90-2.10 described a window in which "
    f"every complete hour got BOTH a scheduled pass and a discretionary "
    f"one, and it is STALE\n"
    f"- the acceptance gate is ONE-SIDED and is BLIND to a dropped house "
    f"noun; {_msg_gate}"
    f"{_msg_corpus}"
    f"- the 200-resolving ids, including those by other accounts: {_ids}\n"
    f"- webpage-only, no Telegram\n"
)
(REPO / f".commit_msg_{CYCLE}.txt").write_text(MSG, encoding="utf-8")
print(f"[commit] commit message ({len(MSG)} chars) written")
_subject = MSG.split("\n", 1)[0]
assert len(_subject) < 280, (
    f"Tirith 8: the commit subject is {len(_subject)} chars >= 280")

rc, out, err = git("commit", "-F", f".commit_msg_{CYCLE}.txt")
print(out.strip()[:600])
if err.strip():
    print("[commit] stderr:", err.strip()[:600])
assert rc == 0, "the commit failed"

# ---- 5. the two committed anchors must agree to the minute ----
rc, stamp_head, err = git_list(["show", "HEAD:deploy-stamp.txt"], expect_out=True)
rc2, commit_head, err2 = git_list(
    ["show", "-s", "--format=%ad", "--date=format:%Y-%m-%d %H:%M:%S", "HEAD"],
    expect_out=True)
stamp_head = stamp_head.strip()
commit_head = commit_head.strip()
sm = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) CST", stamp_head)
assert sm, f"unparseable committed stamp: {stamp_head!r}"
cm = dt.datetime.strptime(commit_head, "%Y-%m-%d %H:%M:%S")
print(f"[commit] stamp at HEAD : {stamp_head}")
print(f"[commit] commit at HEAD: {commit_head}")
assert sm and dt.datetime.strptime(sm.group(1), "%Y-%m-%d %H:%M") == \
    cm.replace(second=0), (
    "the two committed run-time anchors disagree after the commit -- the next "
    "cycle would abort on a contested cut")
print("[commit] the two committed anchors AGREE to the minute")

# ---- 6. the committed tree must carry what we intended ----
rc, out, err = git("show", "--stat", "--name-only", "HEAD")
print("[commit] committed files:",
      [x for x in out.splitlines()[1:] if x.strip()])
rc, pg, err = git("show", "HEAD:index.html")
assert rc == 0, err
assert f"<!-- cron cycle {CYCLE}:" in pg, "the committed page lacks this cycle's comment"
assert f"<strong>{ban}</strong> 次回傳" in pg, "the committed page lacks the banner count"
# ⭐⭐⭐⭐⭐ CYCLE 1266's FIX: **THIS POST-COMMIT BLOCK WAS NOT
# BRANCH-SYMMETRIC.**  It asserted the SUBSTANTIVE prose unconditionally
# ("{N} 則新推文" present, "未發現新推文" ABSENT) -- so on a MEASURED
# NO-OP it demanded that the committed page claim a published-post
# count for a cycle that published NOTHING, and simultaneously forbade
# the page from saying what it actually measured.
# ⭐⭐⭐⭐⭐ **THE COMMIT ITSELF SUCCEEDED** (`00423d1`) -- the failure was
# in the verification that runs AFTER it, so the artefact was correct
# and the CHECK was wrong.  ⭐⭐⭐⭐⭐ **A GATE WRITTEN FOR ONE SHAPE IS
# THE MOST LIKELY PLACE THE OTHER SHAPE IS MISSING** -- and the base
# (1263, a SUBSTANTIVE cycle) carries the same defect, so it travels
# with every clone until a NO-OP cycle trips on it.
# ⭐⭐⭐⭐⭐ **THE FIX LIFTS THE WHOLE BRANCH-SYMMETRIC REGION** (not a
# single assertion), and the NO-OP branch asserts **BOTH DIRECTIONS**
# (anti-vacuity, Reminder 15): its own prose is PRESENT and the
# SUBSTANTIVE prose is ABSENT -- so a page carrying NEITHER would fail.
if _IS_NOOP:
    assert "未發現新推文" in pg, (
        "the COMMITTED page does not carry the MEASURED NO-OP prose "
        "('未發現新推文') -- the page must say what was measured")
    assert not re.search(r"找到了 \d+ 則新推文", pg), (
        "the COMMITTED page carries a SUBSTANTIVE published-count clause on "
        "a MEASURED NO-OP -- that is a FALSE PUBLICATION: it claims the "
        "paths FOUND 0 tweets, when they found none")
    print("[commit] (NO-OP) the COMMITTED page carries the NO-OP prose and "
          "NO SUBSTANTIVE published-count clause")
else:
    assert f"{_N_PUBLISHED} 則新推文" in pg, (
        "the committed page does not say how many new tweets it published "
        "-- but this cycle published "
        f"{_N_PUBLISHED} posts")
    assert "未發現新推文" not in pg, (
        "the committed page says 'no new tweets found' -- but this cycle "
        f"published {_N_PUBLISHED} posts")
assert "並不能" in pg and "證明資料被截斷" in pg, "the committed page lacks the correction"
assert "證明是截斷的" not in pg, "the committed page carries the WITHDRAWN claim"
assert "writer_guard = NO_EVIDENCE_THIS_HOUR" in pg, (
    "the committed page lacks this hour's OUT-OF-BAND guard verdict -- the "
    "hour is NOT in RETRY_TRANSLATION_HOURS, so the branch NEVER RAN")
assert "the empty-translation retry branch NEVER RAN" in pg, (
    "the committed page does not record that the branch NEVER RAN this hour")
assert "writer_guard = FIRED" not in pg, (
    "the committed page carries the IN-BAND guard verdict -- this hour "
    "was OUT OF BAND")
assert "POSITIVE CONTROL" in pg, (
    "on an OUT-OF-BAND hour there IS a positive control -- the "
    "committed page must name one")
assert "NEGATIVE CONTROL" in pg, "the committed page does not name the negative control"
assert "control set is UNCHANGED, NOT flipped" in pg, (
    "the committed page does not state that the control set is UNCHANGED -- "
    "the prior committed cycle was ALSO out of band")
assert "BORROWED and explicitly DISCLAIMED" in pg, (
    "on an OUT-OF-BAND hour the count is BORROWED from the positive "
    "control and DISCLAIMED -- the committed page must say so")
assert "NOT borrowed and NOT disclaimed" not in pg, (
    "on an OUT-OF-BAND hour the count is NOT this hour's own evidence -- "
    "the committed page must not claim it is")
assert STEP_PHRASE in pg, (
    "the committed page does not state the banner step against BOTH anchors "
    "(the published one AND the re-derived-at-the-cut one)")
# ⭐ THE COMMITTED PAGE'S COMMENT DELIMITERS MUST BALANCE
assert pg.count("<!--") == pg.count("-->"), (
    f"the committed page has unbalanced comment delimiters "
    f"({pg.count('<!--')} '<!--' vs {pg.count('-->')} '-->')")
# ⭐ AND IT MUST CARRY EXACTLY ONE CYCLE COMMENT
assert len(re.findall(r"<!--\s*cron cycle \d+:", pg)) == 1, (
    "the committed page does not carry exactly ONE cycle comment")
rc, out, err = git("show", "HEAD:deploy-stamp.txt")
assert f"cycle {CYCLE}" in out, "the committed stamp lacks this cycle's number"
# the committed corpus must carry the new records AND all the old ones
rc, out, err = git("show", "HEAD:tweets.json")
_c = json.loads(out)
assert len(_c) == recs, (
    f"the committed corpus has {len(_c)} records, expected {recs}")
assert len({t["id"] for t in _c}) == len(_c), "the committed corpus has duplicate ids"
_committed_ids = {t["id"] for t in _committed}
assert all(i in {t["id"] for t in _c} for i in _new_ids), (
    "a published id is missing from the committed corpus")
assert _committed_ids <= {t["id"] for t in _c}, (
    "a committed record is missing from the committed corpus")
print(f"[commit] the COMMITTED TREE carries the cycle comment, the banner, the "
      f"{_N_PUBLISHED}-post prose, the correction, the IN-BAND guard "
      f"verdict, the "
      f"NEGATIVE CONTROL, BOTH step anchors, and NOT the withdrawn claim; the "
      f"committed corpus carries {recs} records including all {_new_ids}")

# ---- 7. push ----
# ⭐⭐⭐⭐⭐ **CYCLE 1304's REPAIR: THE PUSH MUST BE HEADLESS-SAFE.**
# ⭐⭐⭐⭐⭐ The repo's credential helper list puts `osxkeychain` FIRST, and
# ⭐⭐⭐⭐⭐ `osxkeychain` spawns a GUI `SecurityAgent` prompt when the
# ⭐⭐⭐⭐⭐ keychain has no usable entry ⇒ ⇒ **⇒ IN A CRON SESSION THERE IS
# ⭐⭐⭐⭐⭐ NOBODY TO APPROVE IT ⇒ ⇒ **⇒ THE PUSH WAITS FOREVER** (1293's
# ⭐⭐⭐⭐⭐ first fire: the commit was LOCAL-ONLY and five post-commit stages
# ⭐⭐⭐⭐⭐ never ran).
# ⭐⭐⭐⭐⭐ **⇒ THE FIX IS THE NON-INTERACTIVE HELPER, EXPLICITLY, AT THE
# ⭐⭐⭐⭐⭐ CALL SITE** -- and NOT relied upon as a config ORDERING (1293's
# ⭐⭐⭐⭐⭐ general rule: *in a headless session, any credential/auth/
# ⭐⭐⭐⭐⭐ approval flow that can reach a GUI must be replaced by its
# ⭐⭐⭐⭐⭐ non-interactive equivalent -- and the replacement must be
# ⭐⭐⭐⭐⭐ EXPLICIT AT THE CALL SITE*).
# ⭐⭐⭐⭐⭐ **⇒ `GIT_TERMINAL_PROMPT=0` + `GIT_ASKPASS=/usr/bin/true` ARE
# ⭐⭐⭐⭐⭐ THE OTHER HALF**: they make git fail FAST AND LOUDLY instead of
# ⭐⭐⭐⭐⭐ prompting on a terminal nobody is watching ⇒ ⇒ **⇒ A FAILED
# ⭐⭐⭐⭐⭐ PUSH BECOMES AN ERROR MESSAGE INSTEAD OF A HANG.**
# ⭐⭐⭐⭐⭐ **⇒ AND THE HELPER IS *DERIVED*, NOT TYPED**: the path is read
# ⭐⭐⭐⭐⭐ from the SKILL's own scripts directory if it exists, so a moved
# ⭐⭐⭐⭐⭐ skill does not silently disable the fix.
_CRED_HELPER = pathlib.Path.home() / (
    ".hermes/skills/elon-tweets-cron/scripts/cred-helper.sh")
assert _CRED_HELPER.exists(), (
    f"the non-interactive credential helper is ABSENT ({_CRED_HELPER}) -- "
    "the push would fall through to `osxkeychain`, which can reach a GUI "
    "prompt that no cron session can approve")
_HELPER = ('!f() { printf "protocol=https\\nhost=github.com\\n\\n" | '
           f'{_CRED_HELPER} get; }}; f')
_PUSH_ENV = dict(os.environ)
_PUSH_ENV["GIT_TERMINAL_PROMPT"] = "0"
_PUSH_ENV["GIT_ASKPASS"] = "/usr/bin/true"
print(f"[commit] the push uses the NON-INTERACTIVE credential helper "
      f"(explicitly, at the call site): {_CRED_HELPER}")
# ⭐⭐⭐⭐⭐ RULE O (cycle 1307): THE PUSH IS AN *ARGUMENT LIST*, NOT A
# SHELL STRING.  ⭐⭐⭐⭐⭐ The shell is a MANGLER: it ate the helper value's
# quotes and its `\n` escapes, so git received a helper whose `printf`
# emits ONE line with no `host=` key ⇒ ⇒ it exits 0 with NO credentials
# ⇒ ⇒ git falls through to `osxkeychain` ⇒ ⇒ a GUI `SecurityAgent`
# prompt that no cron session can approve ⇒ ⇒ THE PUSH HANGS.
# ⭐⭐⭐⭐⭐ ⭐ MEASURED IN THIS CYCLE (the pre-flight dry-run) ⇒ ⇒ and the
# repo ALREADY carried the correct form in `git_list()` ⇒ ⇒ ⇒ THIS IS THE
# REPO'S OWN SPECIFICATION, not a new invention.
# ⭐⭐⭐⭐⭐ CYCLE 1312's REPAIR (MEASURED): THE "RESET" MUST COME **FIRST**.
# ⭐⭐⭐⭐⭐ `-c credential.helper=<HELPER>` **APPENDS** to the inherited helper
# list, and git consults helpers IN ORDER and STOPS AT THE FIRST THAT
# ANSWERS ⇒ ⇒ `osxkeychain` (listed FIRST in the system AND global config)
# answers ⇒ ⇒ the custom helper is NEVER invoked ⇒ ⇒ the GUI `SecurityAgent`
# prompt appears ⇒ ⇒ **⇒ THE PUSH HANGS** (measured live at cycle 1313: the
# push hung 600 s and left a `SecurityAgent` process alive for 23 h).
# ⭐⭐⭐⭐⭐ **⇒ AN EMPTY `credential.helper` VALUE RESETS THE LIST ⇒ ⇒ AND IT
# MUST BE PASSED *BEFORE* THE REAL HELPER** ⇒ ⇒ `osxkeychain` is then never
# consulted ⇒ ⇒ the push lands in ~2 s (MEASURED).
# ⭐⭐⭐⭐⭐ PROOF (cycle 1312, `git credential fill` with a probe helper):
# the OLD form ⇒ `username=x-access-token` (osxkeychain answered, the custom
# helper NEVER ran); the RESET form ⇒ `username=probe-user` (the CUSTOM
# helper answered, osxkeychain was NEVER consulted).
_pr = subprocess.run(
    ["git", "-c", "credential.helper=",
     "-c", f"credential.helper={_HELPER}", "push", "origin", "HEAD"],
    cwd=str(REPO), capture_output=True, text=True, env=_PUSH_ENV)
rc, out, err = _pr.returncode, _pr.stdout, _pr.stderr
print(out.strip()[:800])
if err.strip():
    print("[commit] push stderr:", err.strip()[:800])
assert rc == 0, "the push failed"
rc, out, err = git_list(["ls-remote", "origin", "HEAD"], expect_out=True)
_local = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO),
                        capture_output=True, text=True).stdout.strip()
_remote = out.split()[0]
print(f"[commit] local HEAD  = {_local}")
print(f"[commit] remote HEAD = {_remote}")
assert _local == _remote, (
    f"the push did not land: local {_local} != remote {_remote} -- a commit "
    "that is not pushed has published NOTHING")
print("[commit] pushed and CONFIRMED at the remote")
print("[commit] OK")
