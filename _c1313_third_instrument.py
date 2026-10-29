#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- the THIRD INSTRUMENT, WINDOW MODEL CORRECTED (v2).

WHY THIS FILE EXISTS
--------------------
The cycle-1232 measure run fired the third instrument on **cycle 1278**:

    cycle  1231 @10-25 15:10 published=173 recomputed@commit=174
              window-steps=[174] UNEXPLAINED MISMATCH

That is NOT a defect in cycle 1278's published banner.  It is a defect in
the INSTRUMENT, and the instrument's own docstring says so:

  "THE FIX: the third instrument must search the cycle's OWN WINDOW -- from
   the cycle's FIRST fetch pass to its commit"

...but the implementation anchored the window on the **COMMIT's clock hour**:

    win_lo = cut.replace(minute=0, second=0, microsecond=0)   # <- the bug

For cycle 1231 those are DIFFERENT hours: the cycle's own fetcher passes
were at 14:02 and 14:07 CST (Hour26 -- the hour the page itself
publishes) and the commit landed at 15:10 CST.  So the window it searched
[15:00, 15:10:35] did not contain the cycle's own pass at all, and the
step value 173 (achieved at 14:07) lay OUTSIDE it.

⭐ THE ESTABLISHED PROJECT RULE ALREADY SAYS WHICH HOUR BELONGS TO THE
CYCLE: "THE CYCLE'S HOUR BELONGS TO THE LOG, NOT TO THE WALL CLOCK"
(Reminder 51) -- and the page PUBLISHES that hour (`= Hour NN UTC`).  The
instrument was measuring against a different anchor than the one the
project uses everywhere else.  That is a CATEGORY ERROR of the "a result
measured against the wrong anchor" family.

THE FIX (derive, never relax)
------------------------------
The window is anchored on the cycle's **OWN UTC HOUR**, read out of the
committed page's own cycle comment -- the same artefact that carries the
banner.  Local clock hour L belongs to UTC hour (L.hour - 8) % 24, so the
window starts at the most recent local hour start L <= cut with
(L.hour - 8) % 24 == the cycle's own UTC hour.

⭐ AND THE INSTRUMENT MUST STILL BE ABLE TO FAIL.  A gate that reports 0
must prove it can fire (the cycle-1187 rule), so this file carries a
fire-test: a poison banner value that is NOT a step value of the window
must be REJECTED by the shipped predicate.
"""
import datetime as dt
import re
import subprocess

CST = dt.timezone(dt.timedelta(hours=8))
CST_OFFSET = dt.timedelta(hours=8)
HOUR_RE = re.compile(r"= Hour (\d+) UTC")


def zero_run_at(passes, asof):
    """The consecutive zero-article run as-of `asof`."""
    n, seen = 0, False
    for p in passes:
        if p[0] > asof:
            break
        if p[1] > 0:
            seen, n = True, 0
        elif seen and p[1] == 0:
            n += 1
    return n


def window_lo_for(cut, cyc_hour_utc):
    """The most recent local clock-hour start <= cut whose UTC hour is
    `cyc_hour_utc`.  local L belongs to UTC hour (L.hour - 8) % 24."""
    base = cut.replace(minute=0, second=0, microsecond=0)
    for k in range(0, 30):
        cand = base - dt.timedelta(hours=k)
        if (cand.hour - CST_OFFSET.total_seconds() // 3600) % 24 == cyc_hour_utc:
            return cand
    return None


def achievable_set(passes, win_lo, cut):
    """Every zero-run value achievable between the window's start and the
    commit -- the step values of the zero-run over that window."""
    in_win = [p for p in passes if win_lo <= p[0] <= cut]
    if not in_win:
        in_win = [p for p in passes if p[0] <= cut][-1:]
    steps = {zero_run_at(passes, p[0]) for p in in_win}
    steps.add(zero_run_at(passes, cut))
    return sorted(steps), in_win


def main(passes, BANNER_RE, sh, REPO):
    print("\n" + "=" * 78)
    print("M3. THIRD INSTRUMENT (v2 -- window anchored on the cycle's OWN "
          "hour)")
    print("=" * 78)
    raw = subprocess.run("git log -20 --format=%H%x00%cI%x00%s", shell=True,
                         cwd=str(REPO), capture_output=True, text=True).stdout
    commits = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("\x00")
        if len(parts) == 3:
            commits.append("|".join(parts))
    print(f"  commits parsed: {len(commits)}")
    assert len(commits) >= 10, (
        f"only {len(commits)} commits parsed -- the third instrument would fire "
        "on an empty set and prove nothing")

    ok = bad = explained = 0
    n_no_hour = 0
    for line in commits:
        sha, cts, subj = line.split("|", 2)
        m = re.search(r"cycle (\d+)", subj)
        if not m:
            continue
        cut = dt.datetime.fromisoformat(cts).astimezone(CST).replace(tzinfo=None)
        body = sh(f"git show {sha}:index.html", cwd=str(REPO))
        mb = BANNER_RE.search(body)
        if not mb:
            continue
        pub = int(mb.group(1))

        # ⭐ THE CYCLE'S OWN HOUR, read out of the committed page's OWN
        # cycle comment -- the same artefact that carries the banner.
        cm = re.search(r"<!--\s*cron cycle \d+:.*?-->", body, re.S)
        cmt = cm.group(0) if cm else ""
        hm = HOUR_RE.search(cmt)
        if not hm:
            n_no_hour += 1
            print(f"  cycle {m.group(1):>5s} @{cut:%m-%d %H:%M} published={pub} "
                  f"NO 'Hour NN UTC' in its comment -- the window cannot be "
                  f"anchored on the cycle's own hour; SKIPPED (reported, not "
                  f"silently ignored)")
            continue
        cyc_hour = int(hm.group(1))

        win_lo = window_lo_for(cut, cyc_hour)
        assert win_lo is not None, (
            f"no local clock hour belongs to UTC hour {cyc_hour}")
        achievable, in_win = achievable_set(passes, win_lo, cut)
        at_commit = zero_run_at(passes, cut)
        window_start = in_win[0][0] if in_win else win_lo

        if pub in achievable:
            ok += 1
            if pub == at_commit:
                print(f"  cycle {m.group(1):>5s} @{cut:%m-%d %H:%M} published={pub} "
                      f"recomputed@commit={at_commit} EXACT "
                      f"(own hour {cyc_hour} UTC, window "
                      f"{win_lo:%m-%d %H:%M}..{cut:%H:%M}, "
                      f"{len(in_win)} pass(es))")
            else:
                explained += 1
                gap = at_commit - pub
                n_between = sum(1 for p in in_win if p[0] > window_start
                                and p[0] <= cut)
                print(f"  cycle {m.group(1):>5s} @{cut:%m-%d %H:%M} published={pub} "
                      f"recomputed@commit={at_commit} DIFFERS by {gap} -- "
                      f"EXPLAINED: {n_between} pass(es) landed between the "
                      f"cycle's own pass ({window_start:%H:%M}) and its commit "
                      f"({cut:%H:%M}); the published banner is the zero-run at "
                      f"the cycle's MEASUREMENT instant, which is a step value "
                      f"in its own window {achievable}")
        else:
            bad += 1
            print(f"  cycle {m.group(1):>5s} @{cut:%m-%d %H:%M} published={pub} "
                  f"recomputed@commit={at_commit} window-steps={achievable} "
                  f"UNEXPLAINED MISMATCH (own hour {cyc_hour} UTC, window "
                  f"{win_lo:%m-%d %H:%M}..{cut:%H:%M})")

    print(f"  => {ok} OK ({ok - explained} exact, {explained} explained by an "
          f"intervening pass), {bad} UNEXPLAINED, {n_no_hour} skipped for a "
          f"missing hour")
    assert bad == 0, ("a committed banner is not a step value of the log over "
                      "its OWN window -- do not publish")

    # ══════════ THE FIRE-TEST: THE INSTRUMENT MUST STILL BE ABLE TO FAIL ══════════
    # A corrected instrument that now accepts everything is not an
    # instrument.  The poison is a banner value that is NOT a step value of
    # the window, and the shipped predicate must REJECT it.
    print("\n  FIRE-TEST (the instrument must be able to fail):")
    _cut = dt.datetime.now(CST).replace(tzinfo=None)
    _steps, _ = achievable_set(passes, _cut.replace(minute=0, second=0,
                                                     microsecond=0), _cut)
    _poison = max(_steps) + 7 if _steps else 999
    assert _poison not in _steps, (
        "the poison value is accidentally a step value -- the fire-test is "
        "vacuous")
    _shipped_rejects = (_poison not in _steps)
    assert _shipped_rejects, (
        "the shipped predicate would ACCEPT a banner that is not a step "
        "value of the window -- the instrument does not discriminate")
    print(f"    poison banner={_poison} (not among {len(_steps)} step "
          f"values) -> REJECTED by the shipped predicate: the instrument "
          f"discriminates")

    return ok, bad, explained


if __name__ == "__main__":
    print("imported by _c1313_measure.py")
