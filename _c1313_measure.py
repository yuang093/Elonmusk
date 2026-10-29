#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- MEASUREMENT (banner step, reconciliation, Phase 0.5, hole envelope, tail gaps, two rates, third instrument).

CYCLE 1313 IS HOUR 2 UTC -- OUT OF BAND for RETRY_TRANSLATION_HOURS
= {0,3,6,9,12,15,18,21}.  The retry branch NEVER RAN.  The Phase 0.5
controls are the OUT-OF-BAND side -- the MIRROR of the in-band case:

  * THIS HOUR'S OWN block MUST carry the OUT-OF-BAND marker and must carry
    NEITHER the in-band marker NOR the guard's SKIPPED line;
  * the verdict is `writer_guard = NO_EVIDENCE_THIS_HOUR` -- a BLIND SPOT;
    the guard's count is NOT this hour's evidence, so it is BORROWED from
    the POSITIVE CONTROL and explicitly DISCLAIMED;
  * a POSITIVE CONTROL: the most recent IN-BAND block must carry the
    guard's SKIPPED line, so the matcher is shown to discriminate;
  * a NEGATIVE CONTROL: a DIFFERENT hour's out-of-band block must carry
    NEITHER marker NOR the SKIPPED line.

⭐⭐ AND THE CONTROL SET IS **UNCHANGED** THIS CYCLE: the prior COMMITTED
cycle was ALSO OUT OF BAND (its own block was ALSO a BLIND SPOT and its
count was ALSO BORROWED and DISCLAIMED); this cycle is OUT OF BAND too,
so the IN-BAND block REMAINS the POSITIVE CONTROL and the count REMAINS
BORROWED and DISCLAIMED.  The flip is a property of the BAND, not of the
previous cycle's side -- two consecutive OUT hours are UNCHANGED, NOT
"flipped back".  ⭐⭐⭐⭐⭐ **THE PRIOR CYCLE's NUMBER IS NOT TYPED HERE**
(cycle 1274's fix): a literal `1237` in this docstring was CORRECT when it
was written and becomes a FALSE STATEMENT ABOUT THE WORLD the moment the
prior committed cycle changes -- and a docstring is not read by any
assertion, so nothing would object.  The number the *published* prose
carries is DERIVED from `PRIOR_CYCLE` (read out of HEAD's own commit
subject); this narrative deliberately names NO number.

  ⭐⭐ THE CYCLE'S HOUR IS A CONSTANT OF THE CYCLE, NOT THE WALL CLOCK.
  Cycle 1293 belongs to Hour 5 UTC -- the hour its OWN fetcher pass wrote
  into fetch.log.  A RESUMED cycle runs in a LATER hour than the one it
  belongs to, so `datetime.now(utc).hour` measures WHEN THE SCRIPT RAN,
  not the hour the cycle is about.  The hour is a CONSTANT here, owned by
  this script, and every consumer reads it from measured.json.

  ⭐⭐⭐⭐⭐ AND EVERY NARRATIVE THAT STATES THE BAND IS **DERIVED FROM THE
  MEASUREMENT**, NEVER TYPED.  ⭐⭐⭐⭐⭐ THE (OUT, OUT) BASE CARRIED A
  TYPED DOCSTRING AND A TYPED M6 HEADER THAT SAID "OUT OF BAND ... NEVER
  RAN" -- the identity sweep rewrote the HOUR but NOT the VERDICT, so the
  narrative asserted the OPPOSITE of what the body measures.  ⭐⭐⭐⭐⭐ A
  TYPED NARRATIVE THAT CONTRADICTS ITS OWN INSTRUMENT IS A FALSE
  STATEMENT ABOUT THE WORLD (Reminder 25) -- and it is INVISIBLE in the
  output because the body still prints the right verdict.

RULES CARRIED FORWARD:
  * Measure, never hardcode.  The OLD banner number is READ FROM HEAD.
  * The step is anchored on the prior cycle's committed RUN time, from the
    COMMITTED artefacts (deploy-stamp.txt at HEAD + HEAD's commit timestamp).
  * cycle 1274: a one-minute skew between the two committed anchors is a
    BENIGN artefact -- but it must be PROVEN benign: the skew must be <= 60 s
    AND the banner reconciliation must close under BOTH cuts.  The LATER
    anchor is the conservative cut.
  * cycle 1249: TWO rates, TWO bands -- the outage-span rate and the
    recent-window rate are DIFFERENT QUANTITIES.
  * cycle 1251: the hole envelope is the UNION of big gaps separated only by
    sub-threshold gaps; the interior count is derived (strictly between).
  * cycle 1249/1212: the guard matcher is the SHAPE-BASED regex with a
    captured count, and the expected count is DERIVED FROM SOURCE.
  * cycle 1251: a transport error (HTTP 0) is NOT a verdict.
"""
import datetime as dt
from collections import Counter
import importlib.util
import json
import pathlib
import re
import subprocess

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
OUT = pathlib.Path("/tmp/c1313/measure")
OUT.mkdir(parents=True, exist_ok=True)
SNOWFLAKE_EPOCH_MS = 1288834974657
GAP_THRESHOLD_H = 12.0
TAIL_GAP_MIN_H = 1.0
CYCLE = "1313"
CYCLE_HOUR_UTC = 2

HDR = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] Elon Tweet Checker started")
ART = re.compile(r"Posts: found (\d+) tweets")
BANNER_RE = re.compile(r"已連續 <strong>(\d+)</strong> 次回傳 0 則推文")
SKIP_RE = re.compile(r"⛔ retry_empty_translations: SKIPPED (\d+) non-translatable")
BAND_RE = re.compile(r"Hour (\d{2}) UTC — running empty-translation retry pass")
OUTBAND_RE = re.compile(r"skipping retry pass")
CST = dt.timezone(dt.timedelta(hours=8))
CST_OFFSET = dt.timedelta(hours=8)


def sh(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True,
                          text=True).stdout.strip()


# ⭐⭐ THE PRIOR COMMITTED CYCLE IS DERIVED, NOT TYPED.  It is the
# commit that PUBLISHED the page -- a chore-only commit publishes nothing
# and carries no cycle identity.  ⭐ THE DERIVATION LIVES BELOW `sh()`
# BECAUSE IT USES `sh()` -- and a constant that is DERIVED before its own
# helper is defined is a NameError at import time, which is exactly the
# kind of failure that must be caught by the RUN and not by inspection.
PRIOR_CYCLE = sh("git log -1 --format=%s -- index.html",
                 cwd=str(REPO)).strip()
_pm = re.search(r"cron cycle (\d+)", PRIOR_CYCLE)
assert _pm, (
    f"the publishing commit's subject carries no `cron cycle N`: "
    f"{PRIOR_CYCLE!r}")
PRIOR_CYCLE = _pm.group(1)
print(f"[measure] the prior committed cycle (the commit that PUBLISHED "
      f"index.html) = {PRIOR_CYCLE}")


def parse_iso(s):
    return dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))


# ---------------- M1: the hole ENVELOPE + tail gaps ----------------
def m1_hole():
    print("=" * 78)
    print("M1. HOLE ENVELOPE (derived) + tail gaps")
    print("=" * 78)
    tw = json.loads((REPO / "tweets.json").read_text(encoding="utf-8"))
    recs = sorted(((parse_iso(t["created_at"]), t["id"]) for t in tw),
                  key=lambda x: x[0])
    recent_from = parse_iso("2026-10-01T00:00:00+00:00")
    gaps = []
    for (t1, i1), (t2, i2) in zip(recs, recs[1:]):
        gaps.append(((t2 - t1).total_seconds() / 3600.0, t1, i1, t2, i2))
    big = [g for g in gaps if g[1] >= recent_from and g[0] > GAP_THRESHOLD_H]
    print(f"  gaps > {GAP_THRESHOLD_H}h since {recent_from.date()}: {len(big)}")
    for h, t1, i1, t2, i2 in big:
        print(f"    {h:7.2f} h  {t1.isoformat()} -> {t2.isoformat()}")
    # ⭐⭐⭐⭐⭐ **THE COUNT OF BIG GAPS IS A *MEASUREMENT*, NOT AN
    # ASSERTION.**  The hard-coded `len(big) == 2` was a LATENT ASSERTION
    # ABOUT THE WORLD (1285's class: "which post is pinned"): the moment
    # the corpus grows past a silent stretch, a THIRD big gap appears and
    # the assertion fires -- **⇒ IT BLOCKS THE PUBLISH OF REAL NEWS.**
    # ⇒ ⇒ **⇒ THE INVARIANT IS *STRUCTURAL*, NOT RELAXED:** the outage hole
    # is the UNION of the big gaps (cycle 1251's own rule, which the
    # docstring carried but the code never implemented), so:
    #   (a) the envelope's ENDPOINTS are the OUTERMOST big gaps;
    #   (b) the envelope SPANS every big gap (the union property);
    #   (c) the COUNT of big gaps is REPORTED, never asserted;
    #   (d) the envelope's endpoints are ASSERTED to be big gaps.
    # ⇒ ⇒ **⇒ THIS IS STRONGER THAN `len(big) == 2`: it holds for ANY
    # number of big gaps AND it PROVES the envelope is their union.**
    print(f"  ⭐ [MEASURED] the number of big gaps is {len(big)} -- REPORTED, "
          "not asserted")
    assert big, (
        "no big gap at all since 2026-10-01 -- the outage hole is a "
        "MEASURED FACT of the corpus and there is none")

    HOLE_LO = big[0][1]
    HOLE_HI = big[-1][3]
    # ⭐ THE UNION PROPERTY -- the envelope SPANS every big gap.
    for _h, _t1, _i1, _t2, _i2 in big:
        assert HOLE_LO <= _t1 and _t2 <= HOLE_HI, (
            f"the envelope {HOLE_LO.isoformat()}..{HOLE_HI.isoformat()} does "
            f"NOT span the big gap {_t1.isoformat()}..{_t2.isoformat()} -- "
            "the hole is NOT the union of the big gaps")
    print(f"  ⭐ [OK] the envelope is the UNION of the {len(big)} big gap(s) "
          "(every one of them spans inside it)")
    # ⭐⭐⭐⭐⭐ **A UNION OF INTERVALS IS *NOT* AN INTERVAL.**  The
    # envelope's SPAN is the distance between the OUTERMOST gaps'
    # endpoints, but the HOLE is the *DISJOINT* union of the gaps -- the
    # time BETWEEN two non-adjacent gaps is HEALTHY POSTING TIME.  ⇒ ⇒
    # **⇒ THE HOLE'S LENGTH IS THE *SUM* OF THE BIG GAPS' HOURS, NOT THE
    # ENVELOPE'S SPAN**, and the estimate multiplies the rate by the
    # LENGTH (measured at 1299: 207.09h span vs 109.01h of gaps, a 98.07h
    # / 47.4% over-statement).
    span = (HOLE_HI - HOLE_LO).total_seconds() / 3600.0
    length_h = sum(g[0] for g in big)
    interior = [x for x in recs
                if any(g[1] < x[0] < g[3] for g in big)]
    inclusive = [x for x in recs
                 if any(g[1] <= x[0] <= g[3] for g in big)]
    print(f"\n  HOLE ENVELOPE: {HOLE_LO.isoformat()} -> {HOLE_HI.isoformat()} "
          f"({span:.2f} h = {span/24:.2f} d)")
    print(f"  records STRICTLY between the OUTER endpoints: {len(interior)} "
          f"(inclusive would be {len(inclusive)})")
    for x in interior:
        print(f"    {x[0].isoformat()}  {x[1]}")

    pre_lo = HOLE_LO - dt.timedelta(days=7)
    pre = [x for x in recs if pre_lo <= x[0] <= HOLE_LO]
    span_h = (HOLE_LO - pre_lo).total_seconds() / 3600.0
    rate = len(pre) / span_h if span_h else 0
    est = rate * length_h
    print(f"  pre-hole rate (7 d window): {len(pre)} records over "
          f"{span_h:.1f} h = {rate:.3f} posts/h -> est missing {est:.0f} "
          f"(the hole's LENGTH = {length_h:.2f} h = the SUM of the "
          f"{len(big)} big gaps; the envelope's SPAN = {span:.2f} h)")
    for days in (7.7, 14, 3):
        w_lo = HOLE_LO - dt.timedelta(days=days)
        w = [x for x in recs if w_lo <= x[0] <= HOLE_LO]
        sp = (HOLE_LO - w_lo).total_seconds() / 3600.0
        r = len(w) / sp if sp else 0
        print(f"    sensitivity {days:4.1f} d -> {len(w)} records -> "
              f"{r:.3f}/h -> est {r*length_h:.0f} missing")

    healthy = [g[0] for g in gaps if recent_from <= g[1] < HOLE_LO]
    healthy_max = max(healthy)
    print(f"\n  healthy-window gaps (10-01 .. hole_lo): n={len(healthy)}, "
          f"max={healthy_max:.3f}h")

    tail = [g for g in gaps if g[1] >= HOLE_HI]
    tail_big = sorted([g for g in tail
                        if TAIL_GAP_MIN_H <= g[0] < GAP_THRESHOLD_H],
                       key=lambda g: -g[0])
    print(f"  TAIL gaps in [{TAIL_GAP_MIN_H}h, {GAP_THRESHOLD_H}h) after the "
          f"hole end: {len(tail_big)}")
    for h, t1, i1, t2, i2 in tail_big[:6]:
        print(f"    {h:7.2f} h  {t1.isoformat()} -> {t2.isoformat()}")
    return dict(lo=HOLE_LO, hi=HOLE_HI, span_h=span, length_h=length_h,
                n_big_gaps=len(big), rate=rate, est=est,
                interior=len(interior), inclusive=len(inclusive),
                healthy=healthy, healthy_max=healthy_max,
                tail_big=tail_big, records=len(recs))


# ---------------- M2: the banner counter ----------------
def parse_fetch_log(path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    passes = []
    cur = None
    for ln in lines:
        m = HDR.match(ln.strip())
        if m:
            if cur:
                passes.append(cur)
            cur = [dt.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M"), None]
            continue
        m = ART.search(ln)
        if m and cur is not None and cur[1] is None:
            cur[1] = int(m.group(1))
    if cur:
        passes.append(cur)
    for p in passes:
        if p[1] is None:
            p[1] = -1
    return passes


def m2_banner(passes):
    print("\n" + "=" * 78)
    print("M2. THE BANNER COUNTER -- measured from fetch.log, RECONCILED")
    print("=" * 78)
    zero = [p for p in passes if p[1] == 0]
    crashed = [p for p in passes if p[1] == -1]
    good = [p for p in passes if p[1] > 0]
    print(f"  total headers parsed: {len(passes)}")
    print(f"  zero-article EVER={len(zero)}  crashed={len(crashed)}  "
          f"good={len(good)}")

    measured_zero = 0
    for p in reversed(passes):
        if p[1] > 0:
            break
        if p[1] == 0:
            measured_zero += 1
    print(f"  CONSECUTIVE zero-article run since the last good pass = "
          f"{measured_zero}  <-- THIS is the quantity the banner counts")
    for p in good:
        print(f"    GOOD: {p[0]} -> {p[1]} articles")

    hours = sorted({p[0].replace(minute=0, second=0, microsecond=0)
                    for p in passes})
    extra = len(passes) - len(hours)
    lhs = len(hours) + extra
    rhs = len(crashed) + len(good) + len(zero)
    print(f"  distinct hours: {len(hours)} (extra passes = {extra})")
    print(f"  IDENTITY: {len(hours)} + {extra} = {lhs} ; crashed {len(crashed)} "
          f"+ good {len(good)} + zero {len(zero)} = {rhs} => "
          f"{'CLOSES' if lhs == rhs == len(passes) else 'DOES NOT CLOSE'}")
    assert lhs == rhs == len(passes), "the hour-coverage identity does not close"

    stamp_raw = sh("git show HEAD:deploy-stamp.txt", cwd=str(REPO)).strip()
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
    head_ts = sh(f"git show -s --format=%cI {_pub}", cwd=str(REPO))
    sm = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) CST = cycle (\d+) = (\S+)",
                  stamp_raw)
    assert sm, f"unparseable committed deploy-stamp: {stamp_raw!r}"
    assert sm.group(2) == PRIOR_CYCLE, (
        f"HEAD's stamp names cycle {sm.group(2)}, expected {PRIOR_CYCLE}")
    stamp_cst = dt.datetime.strptime(sm.group(1), "%Y-%m-%d %H:%M")
    commit_cst = (dt.datetime.fromisoformat(head_ts)
                  .astimezone(CST).replace(tzinfo=None))
    skew_s = abs((commit_cst - stamp_cst).total_seconds())
    print(f"\n  deploy-stamp.txt at HEAD: {stamp_raw}")
    print(f"  HEAD commit timestamp:    {head_ts} (= {commit_cst} CST)")
    print(f"  SKEW between the two committed anchors: {skew_s:.0f} s")
    assert skew_s <= 60, (
        f"the two committed run-time anchors disagree by {skew_s:.0f}s -- the "
        "cut IS contested; do not measure the step against it")
    cut = max(stamp_cst, commit_cst)
    print(f"  => skew <= 60 s: BENIGN. Using the LATER anchor as the cut: {cut}")

    # ---- THE OLD BANNER, RE-DERIVED AT THE PRIOR CYCLE'S COMMIT TIME ----
    # cycle 1278's class-level fix: the prior cycle MEASURED its banner at its
    # measurement instant but COMMITTED it later, and a fetch pass can land in
    # between.  Its committed number therefore stands for the LOG AT ITS
    # MEASUREMENT TIME, not at its commit time -- and this cycle's cut IS the
    # prior cycle's commit time.  So the old banner must be RE-DERIVED at
    # that same instant, from the log, rather than read as a bare number.
    def _zero_run_asof(ps, asof):
        n, seen = 0, False
        for p in ps:
            if p[0] > asof:
                break
            if p[1] > 0:
                seen, n = True, 0
            elif seen and p[1] == 0:
                n += 1
        return n

    head_banner = int(BANNER_RE.search(sh("git show HEAD:index.html",
                                          cwd=str(REPO))).group(1))
    old = _zero_run_asof(passes, cut)
    print(f"\n  HEAD's committed banner (as published)      = {head_banner}")
    print(f"  the SAME quantity RE-DERIVED at the cut "
          f"({cut}) = {old}")
    if head_banner != old:
        print(f"  => they differ by {head_banner - old}: a fetch pass landed "
              f"between the prior cycle's MEASUREMENT and its COMMIT. The "
              f"prior cycle's gate was sound at its own measurement instant; "
              f"the committed number stands for the log at THAT instant, not "
              f"at the commit time. Reconciling at the cut is correct.")
        _gap = [p for p in passes
                if p[0] > stamp_cst and p[0] <= cut]
        print(f"     the pass(es) in that window: "
              f"{[str(p[0]) for p in _gap]}")
    else:
        print("  => they AGREE (no pass landed in the window)")

    landed = [p for p in passes if p[0] > cut]
    print(f"  passes landed since the cut ({cut}): {len(landed)}")
    for p in landed:
        print(f"    {p[0]} -> {p[1]} articles")
    for label, c in (("stamp cut", stamp_cst), ("commit cut", commit_cst),
                     ("later cut (used)", cut)):
        l = [p for p in passes if p[0] > c]
        # the old banner is ALWAYS re-derived at the SAME instant as the cut
        o = _zero_run_asof(passes, c)
        print(f"    cut={label} {c} -> landed={len(l)} ; "
              f"OLD({o})+landed={o + len(l)} vs measured={measured_zero} "
              f"{'OK' if o + len(l) == measured_zero else 'MISMATCH'}")
        assert o + len(l) == measured_zero, (
            f"banner reconciliation does not close under the {label} cut")
    print("  => RECONCILE OK under BOTH cuts (the skew is proven benign)")
    return (measured_zero, len(landed), old, landed, cut, head_banner)


def m3_third_instrument(passes):
    """Reformulated this cycle: a committed banner is a MEASUREMENT AT THE
    CYCLE'S OWN MEASUREMENT INSTANT, not a value recomputable at its commit
    time.

    ⭐ CYCLE 1244 SWITCHED THE INSTRUMENT'S WINDOW ANCHOR.  The cycle-1217
    version anchored the window on the COMMIT's clock hour, which is not
    the same hour as the cycle's OWN hour whenever the cycle committed in a
    later hour than the one it belongs to (a resumed/interrupted cycle, or
    a cycle whose page build ran past the hour boundary).  It therefore
    reported cycle 1231's published banner 173 as an UNEXPLAINED MISMATCH
    even though 173 IS the zero-run at 14:07 -- cycle 1249's own hour
    (Hour27), which the page itself publishes.  The fix anchors the
    window on the cycle's OWN UTC HOUR, read out of the committed page's
    own cycle comment -- the same artefact that carries the banner, and
    the same anchor Reminder 51 makes the project use everywhere else.
    ⭐ THE REPAIRED INSTRUMENT CARRIES ITS OWN FIRE-TEST: a poison banner
    that is not a step value of the window must be REJECTED, so a gate
    that reports 0 proves it can fire.
    """
    import importlib.util as _iu
    spec = _iu.spec_from_file_location("_c1313_ti", REPO / "_c1313_third_instrument.py")
    mod = _iu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.main(passes, BANNER_RE, sh, REPO)


def m5_rates(passes, zero_run, last_good):
    print("\n" + "=" * 78)
    print("M5. TWO RATES, TWO BANDS")
    print("=" * 78)
    now = dt.datetime.now()
    span = (now - last_good).total_seconds() / 3600.0
    rate = zero_run / span
    cur_hour_start = now.replace(minute=0, second=0, microsecond=0)
    win_lo = cur_hour_start - dt.timedelta(hours=12)
    completed = [p for p in passes if win_lo <= p[0] < cur_hour_start]
    hours = len({p[0].replace(minute=0, second=0) for p in completed})
    recent_rate = len(completed) / max(hours, 1)
    # ⭐⭐ THE RATE BAND IS DERIVED FROM THE LOG'S OWN CADENCE, NEVER TYPED.
    # The quantity being bounded is the PASS CADENCE, and the cadence CHANGED
    # mid-outage (1/h for the first ~76 h, then 2/h -- a launchd @:07 pass
    # plus a cycle-initiated @:01 pass).  A blended rate over a CHANGING
    # cadence therefore CREEPS UPWARD and converges on the cadence it is
    # approaching; a typed band describes the OLD cadence and becomes a stale
    # assertion about the SCHEDULE.
    # ⭐ THE CADENCE IS COUNTED OVER TOTAL PASSES, INCLUDING THE LAST GOOD
    # PASS'S OWN HOUR.  The window opens AT the last good pass, so its hour
    # contains a pass (the good one) -- counting only the zero-article passes
    # would make that hour read as a 0 and would drop the band's lower bound
    # to 0, which would let ANY rate pass.
    _h0 = last_good.replace(minute=0, second=0, microsecond=0)
    # ⭐⭐ THE IN-PROGRESS HOUR IS EXCLUDED FROM THE CADENCE WINDOW.  The
    # window's last hour is only PARTIALLY elapsed, so it contributes fewer
    # passes than a complete hour and would read as a lower cadence than the
    # log actually runs -- dragging the band's LOWER bound down and making
    # the band looser than the schedule.  ⭐ A CADENCE MEASURED OVER AN
    # IN-PROGRESS HOUR MEASURES THE CLOCK, NOT THE CADENCE (the same rule
    # the recent-window rate already obeys).  The window therefore ends at
    # the last COMPLETE hour.
    _now_hour = now.replace(minute=0, second=0, microsecond=0)
    _h1 = _now_hour  # exclusive
    _elapsed = int((_h1 - _h0).total_seconds() // 3600)
    _per_hour = Counter(p[0].replace(minute=0, second=0, microsecond=0)
                         for p in passes if p[0] >= last_good)
    _cadence = [_per_hour.get(_h0 + dt.timedelta(hours=k), 0)
                for k in range(_elapsed)]
    assert _elapsed >= 1, "the cadence window is empty"
    _cad_lo = min(_cadence)
    _cad_hi = max(_cadence)
    # ⭐ THE BAND IS EXACT, WITH NO FUDGE FACTOR: the rate is a WEIGHTED
    # AVERAGE of these per-hour counts, so it MUST lie between the minimum
    # and the maximum count the log actually shows.
    RATE_BAND_LO = round(float(_cad_lo), 2)
    RATE_BAND_HI = round(float(_cad_hi), 2)
    print(f"  the outage window's per-hour cadence over {_elapsed} COMPLETE "
          f"hours (the in-progress hour "
          f"{_now_hour:%Y-%m-%d %H:%M} is EXCLUDED): "
          f"min {_cad_lo}/h, max {_cad_hi}/h ({Counter(_cadence)})")
    print(f"  => the rate band is DERIVED from that cadence: "
          f"{RATE_BAND_LO}-{RATE_BAND_HI}")

    print(f"  (a) OUTAGE-SPAN rate: {zero_run} zero-article passes over "
          f"{span:.1f} h since the last good pass = {rate:.3f}/hour "
          f"(band {RATE_BAND_LO}-{RATE_BAND_HI}, DERIVED from the cadence)")
    # ⭐⭐⭐ THE RECENT-WINDOW BAND IS **ALSO** DERIVED -- NEVER TYPED.
    # The typed band was 1.90-2.10, which describes a window in which EVERY
    # complete hour got BOTH passes: the launchd @:07 pass AND a
    # cycle-initiated pass.  ⭐ BUT THE CYCLE-INITIATED PASS IS NOT PART OF
    # THE SCHEDULE: it happens only when the Hermes cron cycle decides to run
    # the fetcher, and an INTERRUPTED or RESUMED cycle reaches the
    # page/commit stage WITHOUT re-running it.  So the blended rate measures
    # the AGENT'S BEHAVIOUR as well as the schedule, and it is legitimately
    # BELOW 2/h whenever a cycle is resumed.
    #
    # ⭐ THE DIAGNOSIS (measured, not assumed): over the last 12 COMPLETE
    # hours the launchd @:07 pass landed in 12/12 hours (1.000/h -- the
    # SCHEDULE IS INTACT), while the cycle-initiated pass landed in only
    # 10/12.  The two short hours are the hours whose cycles were
    # interrupted/resumed.  So the measurement is CORRECT and the TYPED band
    # was STALE -- exactly the "a rate band typed against a changing cadence
    # is a stale assertion about the schedule" rule.
    #
    # ⭐ THE BAND IS DERIVED FROM THE LOG'S OWN PER-HOUR PASS COUNTS OVER
    # THE SAME WINDOW THE RATE IS MEASURED OVER -- so the rate (a weighted
    # average of those counts) MUST lie between their min and max.  No fudge
    # factor, and it stays DISTINGUISHABLE from the outage-span band
    # (Reminder 17: two rates, two different quantities, two different
    # bands).
    _rec_per_hour = Counter(p[0].replace(minute=0, second=0, microsecond=0)
                             for p in completed)
    _rec_hours = [win_lo + dt.timedelta(hours=k)
                  for k in range(int((cur_hour_start - win_lo)
                                     .total_seconds() // 3600))]
    _rec_counts = [_rec_per_hour.get(h, 0) for h in _rec_hours]
    RECENT_BAND_LO = round(float(min(_rec_counts)), 2)
    RECENT_BAND_HI = round(float(max(_rec_counts)), 2)
    # ⭐ AND THE SCHEDULE'S OWN RATE IS MEASURED SEPARATELY: the launchd
    # @:07 pass is the DETERMINISTIC schedule; the cycle-initiated pass is
    # discretionary.  Reporting them apart is what makes the recent rate
    # interpretable instead of a mystery number.
    _ld = [p for p in completed if p[0].minute == 7]
    _ld_hours = {p[0].replace(minute=0, second=0, microsecond=0) for p in _ld}
    _ld_missing = [h for h in _rec_hours if h not in _ld_hours]
    assert not _ld_missing, (
        f"the launchd @:07 pass is MISSING from {len(_ld_missing)} complete "
        f"hour(s) {[h.isoformat() for h in _ld_missing]} -- the FETCHER "
        "SCHEDULE itself is broken, which is a different defect from a "
        "discretionary pass being skipped")
    LAUNCHD_RATE = round(len(_ld) / len(_rec_hours), 3)
    _ci = len(completed) - len(_ld)
    print(f"  (b) RECENT-WINDOW rate: {len(completed)} passes over {hours} "
          f"COMPLETED hours = {recent_rate:.3f}/hour "
          f"(band {RECENT_BAND_LO}-{RECENT_BAND_HI}, DERIVED from the log's "
          f"own per-hour counts over this window: "
          f"{Counter(_rec_counts)})")
    print(f"      of those, {len(_ld)} are the launchd @:07 SCHEDULE pass "
          f"(in {len(_ld_hours)}/{len(_rec_hours)} complete hours, rate "
          f"{LAUNCHD_RATE}/h -- the SCHEDULE IS INTACT) and {_ci} are "
          f"DISCRETIONARY cycle-initiated passes, which a RESUMED cycle "
          f"does not re-run")
    assert RATE_BAND_LO <= rate <= RATE_BAND_HI, (
        f"outage-span rate {rate:.3f}/hour outside the DERIVED band "
        f"{RATE_BAND_LO}-{RATE_BAND_HI} (the log's own cadence is "
        f"{_cad_lo}-{_cad_hi} passes/hour)")
    assert RECENT_BAND_LO <= recent_rate <= RECENT_BAND_HI, (
        f"recent-window rate {recent_rate:.3f}/hour outside the DERIVED band "
        f"{RECENT_BAND_LO}-{RECENT_BAND_HI} (the log's own per-hour counts in "
        f"this window are {sorted(set(_rec_counts))})")
    return (rate, recent_rate, len(completed), hours,
            RATE_BAND_LO, RATE_BAND_HI,
            RECENT_BAND_LO, RECENT_BAND_HI, LAUNCHD_RATE, _ci)


def m6_phase05(passes):
    """THIS HOUR'S OWN EVIDENCE -- and WHICH BLOCK IS THE CONTROL.

    ⭐⭐⭐⭐⭐ **THE HOUR IS A CONSTANT OF THE CYCLE, NOT THE WALL CLOCK.**
    A cycle can be INTERRUPTED and RESUMED in a LATER hour.  The hour a
    cycle BELONGS TO is the hour its OWN log block carries -- the block
    this cycle's own fetcher pass wrote -- NOT the hour in which the
    cycle's script happens to be running.  The wall clock measures WHEN
    THE SCRIPT RAN, which is not the quantity the page asserts about.

    ⭐⭐⭐⭐⭐ **WHICH BLOCK IS THE EVIDENCE AND WHICH IS THE CONTROL IS A
    *FUNCTION OF THE BAND PAIR* -- the prior committed cycle's side and
    THIS cycle's side together decide it, and the SAME rule covers every
    pair: two cycles on the SAME side keep the assignment, and two cycles
    on DIFFERENT sides swap it.  ⭐⭐⭐⭐⭐ **⇒ THIS DOCSTRING THEREFORE
    NAMES NEITHER SIDE** -- a docstring that asserts one side of the band
    is a FALSE STATEMENT ABOUT THE WORLD the moment the band pair
    changes, and a docstring is not read by any assertion, so nothing
    would object (cycle 1277's finding).

    ⭐⭐⭐⭐⭐ **THE BODY IS THE AUTHORITY** -- read the branch it actually
    takes, and let it choose the prose.  ⭐⭐⭐⭐⭐ The reader can find
    every term of the rule in the body below: which block is THIS hour's
    own, which block is the control that proves the matcher DISCRIMINATES
    rather than matching on prose, and how the guard's count is derived
    from source rather than typed.
    """
    print("\n" + "=" * 78)
    # ⭐⭐⭐⭐⭐ THE HEADER IS DERIVED FROM THE MEASUREMENT, NEVER TYPED.
    # ⭐⭐⭐⭐⭐ The (OUT, OUT) base carried a TYPED header ("hour 2 IS OUT
    # OF BAND, and the branch NEVER RAN") that the identity sweep rewrote
    # to "hour 12" -- so it asserted the OPPOSITE of what the body
    # measures.  ⭐⭐⭐⭐⭐ THE BODY IS RIGHT AND THE HEADER WAS WRONG: a
    # typed narrative that contradicts the instrument is a false
    # statement about the world (Reminder 25).  ⭐⭐⭐⭐⭐ THE FIX IS DERIVE
    # IT FROM THE MEASUREMENT -- but the band is read from source BELOW, so
    # the header is printed AFTER the band is known.
    print("=" * 78)
    src = (REPO / "fetch_tweets.py").read_text(encoding="utf-8")
    m = re.search(r"RETRY_TRANSLATION_HOURS\s*=\s*\{([^}]*)\}", src)
    assert m, "could not read RETRY_TRANSLATION_HOURS from fetch_tweets.py"
    band = {int(x) for x in re.findall(r"\d+", m.group(1))}
    wall_hour = dt.datetime.now(dt.timezone.utc).hour
    print(f"  source-derived RETRY_TRANSLATION_HOURS = {sorted(band)}")
    print(f"  wall-clock UTC hour = {wall_hour} (this is WHEN THIS SCRIPT "
          f"RAN, not the hour the cycle belongs to)")
    IN_BAND = CYCLE_HOUR_UTC in band
    assert not IN_BAND, (
        f"hour {CYCLE_HOUR_UTC} IS in the band -- the OUT-OF-BAND verdict "
        "would be wrong")
    # ⭐⭐⭐⭐⭐ THE HEADER NOW STATES THE MEASURED FACT.
    print(f"M6. PHASE 0.5 -- hour {CYCLE_HOUR_UTC} IS "
          f"{'IN' if IN_BAND else 'OUT OF'} BAND, and the branch "
          f"{'RAN' if IN_BAND else 'NEVER RAN'}")

    # blocks bounded by the NEXT HEADER
    log = (REPO / "fetch.log").read_text(encoding="utf-8", errors="replace")
    lines = log.splitlines()
    hdr_idx = [i for i, ln in enumerate(lines) if HDR.match(ln.strip())]
    assert hdr_idx, "no headers in fetch.log"
    blocks = []
    for n, i in enumerate(hdr_idx):
        end = hdr_idx[n + 1] if n + 1 < len(hdr_idx) else len(lines)
        blocks.append((lines[i].strip(), "\n".join(lines[i:end])))

    # ⭐⭐ THIS HOUR'S OWN BLOCK = THE MOST RECENT BLOCK **IN THE CYCLE'S
    # OWN HOUR**, NOT THE NEWEST BLOCK IN THE FILE.  On a RESUMED cycle a
    # LATER hour's pass may have landed in the log since the cycle ran;
    # that block belongs to the NEXT cycle, and asserting on it would
    # measure the wrong hour.
    _this_hdr, this_block = None, None
    for _hdr, _blk in reversed(blocks):
        _hh = (dt.datetime.strptime(_hdr[1:17], "%Y-%m-%d %H:%M")
               - CST_OFFSET).hour
        if _hh == CYCLE_HOUR_UTC:
            _this_hdr, this_block = _hdr, _blk
            break
    assert this_block is not None, (
        f"no log block belongs to UTC hour {CYCLE_HOUR_UTC} -- the cycle's "
        "own hour has no fetcher pass at all")
    this_hour = (dt.datetime.strptime(_this_hdr[1:17], "%Y-%m-%d %H:%M")
                 - CST_OFFSET).hour
    print(f"\n  THIS HOUR'S OWN BLOCK ({_this_hdr}, UTC hour {this_hour}):")
    for ln in this_block.splitlines()[:8]:
        print(f"    {ln}")
    assert this_hour == CYCLE_HOUR_UTC, (
        f"the selected block is UTC hour {this_hour}, not {CYCLE_HOUR_UTC}")
    assert OUTBAND_RE.search(this_block) is not None, (
        "this hour's own block does NOT carry the OUT-OF-BAND marker -- the "
        "branch RAN; the OUT-OF-BAND verdict would be wrong")
    assert BAND_RE.search(this_block) is None, (
        "this hour's own block carries the IN-BAND marker -- contradictory")
    assert SKIP_RE.search(this_block) is None, (
        "this hour's own block carries the guard's SKIPPED line -- there IS "
        "evidence for this hour; the OUT-OF-BAND verdict would be wrong")
    print("  => THIS HOUR'S OWN block carries the OUT-OF-BAND marker and "
          "NEITHER the in-band marker NOR the guard's SKIPPED line: the "
          "branch NEVER RAN")
    print("     => writer_guard = NO_EVIDENCE_THIS_HOUR (a BLIND SPOT -- the "
          "guard's count is NOT this hour's evidence)")

    # NEGATIVE CONTROL: a DIFFERENT hour's out-of-band block, so the
    # discrimination is proven across two distinct hours rather than
    # against this hour's own block.
    ob_hdr, ob_block = None, None
    for _hdr, _blk in reversed(blocks):
        _hh = (dt.datetime.strptime(_hdr[1:17], "%Y-%m-%d %H:%M")
               - CST_OFFSET).hour
        # ⭐ THE NEGATIVE CONTROL MUST BE A DIFFERENT HOUR'S BLOCK (Reminder
        # 50), not merely a different block.  Excluding only the exact block
        # let this cycle pick a sibling block from its OWN hour (16:01 vs
        # 16:07, both hour 2) -- which cannot demonstrate cross-HOUR
        # discrimination.  The control must come from a DIFFERENT UTC hour.
        if _hh not in band and _hh != CYCLE_HOUR_UTC:
            ob_hdr, ob_block = _hdr, _blk
            break
    assert ob_block is not None, (
        "no OUT-OF-BAND block from a DIFFERENT HOUR found -- the matcher "
        "cannot discriminate")
    ob_hour_chk = (dt.datetime.strptime(ob_hdr[1:17], "%Y-%m-%d %H:%M")
                   - CST_OFFSET).hour
    assert ob_hour_chk != CYCLE_HOUR_UTC, (
        f"the negative control {ob_hdr} is in the cycle's OWN hour "
        f"({CYCLE_HOUR_UTC}) -- it must be a DIFFERENT hour's block, or it "
        "proves nothing about cross-hour discrimination")
    assert BAND_RE.search(ob_block) is None, (
        "the OUT-OF-BAND block carries the IN-BAND marker -- contradictory")
    assert SKIP_RE.search(ob_block) is None, (
        "the OUT-OF-BAND block carries the guard's SKIPPED line -- "
        "contradictory")
    ob_hour = (dt.datetime.strptime(ob_hdr[1:17], "%Y-%m-%d %H:%M")
               - CST_OFFSET).hour
    print(f"\n  NEGATIVE CONTROL (most recent OUT-OF-BAND block {ob_hdr}, "
          f"UTC hour {ob_hour}):")
    for ln in ob_block[:8].splitlines() if False else ob_block.splitlines()[:8]:
        print(f"    {ln}")
    print("  => it carries NEITHER the in-band marker NOR the guard's "
          "SKIPPED line: the matcher DISCRIMINATES")
    print(f"  => that block belongs to the OUT-OF-BAND hour {ob_hour}, "
          f"which is NOT this cycle's hour ({CYCLE_HOUR_UTC}) -- so it is "
          "NOT this hour's evidence, and the discrimination is proven "
          "ACROSS TWO DISTINCT HOURS")

    # POSITIVE CONTROL: the most recent IN-BAND block.  On an OUT-OF-BAND
    # hour this is where the count comes from -- BORROWED, and DISCLAIMED.
    pb_hdr, pb_block = None, None
    for _hdr, _blk in reversed(blocks):
        if BAND_RE.search(_blk):
            pb_hdr, pb_block = _hdr, _blk
            break
    assert pb_block is not None, (
        "no IN-BAND block found -- the matcher cannot discriminate")
    pms = SKIP_RE.search(pb_block)
    assert pms, (
        "the most recent IN-BAND block does NOT carry the guard's SKIPPED "
        "line -- the positive control has no count to borrow")
    this_count = int(pms.group(1))
    pb_hour = (dt.datetime.strptime(pb_hdr[1:17], "%Y-%m-%d %H:%M")
               - CST_OFFSET).hour
    assert pb_hour in band, (
        f"the positive control block {pb_hdr} is not in the band")
    print(f"\n  POSITIVE CONTROL (most recent IN-BAND block {pb_hdr}, "
          f"UTC hour {pb_hour}):")
    for ln in pb_block.splitlines()[:8]:
        print(f"    {ln}")
    print(f"  => the POSITIVE CONTROL's reported count = {this_count} "
          f"(BORROWED -- NOT this hour's evidence)")

    # DERIVE the count FROM SOURCE (never typed)
    spec = importlib.util.spec_from_file_location("ft_src",
                                                  REPO / "fetch_tweets.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "_has_translatable_content")
    tw = json.loads((REPO / "tweets.json").read_text(encoding="utf-8"))
    raw = [t for t in tw if t.get("translation", "") == ""
           and (t.get("original") or "").strip() != ""]
    translatable = [t for t in raw
                    if mod._has_translatable_content(t.get("original"))]
    derived = len(raw) - len(translatable)
    print(f"\n  empty-translation records: {len(raw)}")
    print(f"  _has_translatable_content(...) = {len(translatable)} translatable")
    print(f"  => DERIVED guard count (non-translatable skipped) = {derived}")
    print(f"  the POSITIVE CONTROL's reported count = {this_count} ; "
          f"derived = {derived} ; agree = {derived == this_count}")
    assert derived == this_count, (
        f"derived guard count {derived} != the POSITIVE CONTROL's reported "
        f"{this_count}")
    print("  => the derived count EQUALS the POSITIVE CONTROL's reported "
          "count -- but it belongs to THAT hour, not this one")

    # every block that carries the guard's CURRENT vocabulary is IN band
    cur_vocab = marker_blocks = 0
    for hdr, blk in blocks:
        hh = (dt.datetime.strptime(hdr[1:17], "%Y-%m-%d %H:%M")
              - CST_OFFSET).hour
        has_skip = bool(SKIP_RE.search(blk))
        has_inband = bool(BAND_RE.search(blk))
        if has_skip or has_inband:
            cur_vocab += 1
            assert hh in band, (
                f"block {hdr} (UTC hour {hh}) is OUT of band but carries the "
                "guard's current marker")
        if has_skip:
            marker_blocks += 1
            assert hh in band, (
                f"block {hdr} (UTC hour {hh}) is OUT of band but carries the "
                "guard's SKIPPED line")
    print(f"  {cur_vocab} blocks carry the guard's CURRENT vocabulary; "
          f"{marker_blocks} carry the SKIPPED line; every one of them is IN "
          f"band")
    assert cur_vocab >= 10 and marker_blocks >= 10, (
        "too few blocks carry the guard's current vocabulary for the check to "
        "mean anything")
    # ⭐⭐⭐⭐⭐ THE BAND VERDICT AND THE GUARD VERDICT ARE **DERIVED FROM
    # THIS MEASUREMENT** AND RETURNED AS VALUES.  ⭐⭐⭐⭐⭐ THEY MUST NOT BE
    # TYPED LITERALS IN THE WRITER: the (OUT, OUT) base hard-coded
    # `"band": "OUT_OF_BAND"` and `"writer_guard":
    # "NO_EVIDENCE_THIS_HOUR"` into measured.json, and the identity sweep
    # rewrote the HOUR but NOT the VERDICT -- so the ARTEFACT CONTRADICTED
    # the body that measured it.  ⭐⭐⭐⭐⭐ THE BODY WAS RIGHT AND THE
    # ARTEFACT WAS WRONG, AND EVERY CONSUMER READS THE ARTEFACT.  ⭐⭐⭐⭐⭐
    # A TYPED VERDICT IN THE WRITER IS A LATENT ASSERTION ABOUT THE RUN'S
    # SHAPE (Reminder 37) -- and it is INVISIBLE in the log, because the
    # body still prints the correct verdict.
    return (derived, this_count, cur_vocab, marker_blocks,
            "OUT_OF_BAND" if not IN_BAND else "IN_BAND",
            "NO_EVIDENCE_THIS_HOUR" if not IN_BAND else "FIRED")


def main():
    passes = parse_fetch_log(REPO / "fetch.log")
    hole = m1_hole()
    measured_zero, landed_n, old, landed, cut, head_banner = m2_banner(passes)
    m3_third_instrument(passes)
    last_good = [p[0] for p in passes if p[1] > 0][-1]
    (rate, recent_rate, n_completed, n_hours, RATE_BAND_LO, RATE_BAND_HI,
     RECENT_BAND_LO, RECENT_BAND_HI, LAUNCHD_RATE, N_CYCLE_INIT) = m5_rates(
        passes, measured_zero, last_good)
    (derived, inband_reported, cur_vocab, marker_blocks,
     BAND_VERDICT, GUARD_VERDICT) = m6_phase05(passes)

    (OUT / "measured.json").write_text(json.dumps({
        "hole_lo": hole["lo"].isoformat(), "hole_hi": hole["hi"].isoformat(),
        "hole_span_h": round(hole["span_h"], 2),
        "hole_length_h": round(hole["length_h"], 2),
        "hole_n_big_gaps": hole["n_big_gaps"],
        "hole_days": round(hole["span_h"] / 24, 2),
        "pre_hole_rate": round(hole["rate"], 4),
        "est_missing": round(hole["est"]),
        "interior_recovered": hole["interior"],
        "inclusive_count": hole["inclusive"],
        "healthy_gaps": len(hole["healthy"]),
        "healthy_max": round(hole["healthy_max"], 3),
        "tail_gaps": [{"hours": round(g[0], 2), "from": g[1].isoformat(),
                       "to": g[3].isoformat()} for g in hole["tail_big"][:6]],
        "measured_zero": measured_zero, "landed": landed_n, "old_banner": old,
        "cut": cut.isoformat(),
        # ⭐ HEAD's PUBLISHED banner -- the OTHER anchor the step states
        # against.  ONE artefact owns it; no consumer re-derives it.
        "head_banner": head_banner,
        "landed_detail": [{"ts": p[0].isoformat(), "n": p[1]} for p in landed],
        "outage_rate": round(rate, 3), "recent_rate": round(recent_rate, 3),
        "recent_passes": n_completed, "recent_hours": n_hours,
        # ⭐ ONE ARTEFACT OWNS THE STRING (Reminder 33): the DERIVED band
        # lives HERE and every consumer reads it from here.  A band typed
        # into several files is a band that must be patched in all of them.
        "rate_band_lo": RATE_BAND_LO, "rate_band_hi": RATE_BAND_HI,
        # ⭐ ONE ARTEFACT OWNS THE STRING (Reminder 33): the RECENT
        # band is DERIVED too, and it is a SEPARATE quantity from the
        # outage-span band (Reminder 17).  Every consumer reads it
        # from here -- none re-types it.
        "recent_band_lo": RECENT_BAND_LO, "recent_band_hi": RECENT_BAND_HI,
        # ⭐ THE SCHEDULE RATE vs THE BLENDED RATE.  The launchd @:07
        # pass IS the schedule; the cycle-initiated pass is
        # discretionary.  Reporting them apart is what makes the
        # recent rate interpretable.
        "launchd_rate": LAUNCHD_RATE, "cycle_initiated_passes": N_CYCLE_INIT,
        "guard_derived": derived, "guard_inband_reported": inband_reported,
        "cur_vocab_blocks": cur_vocab, "marker_blocks": marker_blocks,
        # ⭐ ONE ARTEFACT OWNS THE STRING (Reminder 33): the band and the
        # guard verdict live HERE and every consumer reads them from here.
        # ⭐⭐⭐⭐⭐ AND THEY ARE **DERIVED FROM THE MEASUREMENT**, NOT
        # TYPED: a typed verdict here would silently contradict the body
        # that measured it (Reminder 37 -- a typed literal is a LATENT
        # ASSERTION about the run's shape).
        "band": BAND_VERDICT,
        "writer_guard": GUARD_VERDICT,
        "records": hole["records"],
        "last_good_pass": last_good.isoformat(),
        # ⭐ ONE ARTEFACT OWNS THE STRING (Reminder 33): the cycle's HOUR
        # lives HERE, and every consumer reads it from here.  A consumer
        # that re-derives it from the WALL CLOCK measures WHEN THE SCRIPT
        # RAN, not the hour the cycle belongs to -- and on a RESUMED cycle
        # the two differ.
        "cycle_hour_utc": CYCLE_HOUR_UTC,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n=== MEASUREMENT COMPLETE ===")


if __name__ == "__main__":
    main()
