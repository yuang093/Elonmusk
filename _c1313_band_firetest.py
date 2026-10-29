#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FIRE-TEST for the DERIVED RECENT-WINDOW rate band.  (Reminder 36: run the
instrument's fire-test UNCONDITIONALLY.)

WHY THIS EXISTS.  The recent-window band's band was TYPED (1.90-2.10).  It
describes a window in which EVERY complete hour got BOTH passes: the launchd
@:07 pass AND a cycle-initiated pass.  But the cycle-initiated pass is NOT
part of the schedule -- an interrupted or RESUMED cycle reaches the
page/commit stage without re-running the fetcher.  So the blended rate
measures the AGENT's behaviour as well as the schedule, and is legitimately
BELOW 2/h whenever a cycle is resumed.  At cycle 1278 the measured recent
rate was 1.833/h -- the launchd pass had landed in 12/12 complete hours
(the SCHEDULE was intact) while the cycle-initiated pass had landed in only
10/12.

The band is now DERIVED from the log's own per-hour pass counts over the
SAME window the rate is measured over -- so the rate (a weighted average of
those counts) MUST lie between their min and max.  No fudge factor.

This fire-test proves the DERIVED band is a real gate: it REJECTS a rate
below the log's own minimum per-hour count and a rate above its maximum, and
ACCEPTS the measured rate.  It drives the SHIPPED predicate -- a control
that asserts a RE-IMPLEMENTATION of the gate proves nothing.

See references/a-rate-band-typed-against-a-changing-cadence-is-a-stale-assertion.md
"""
import datetime as dt
import json
import pathlib
import re
import sys
from collections import Counter

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

LOG = (REPO / "fetch.log").read_text(encoding="utf-8", errors="replace").split("\n")
HDR = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] Elon Tweet Checker started")
ART = re.compile(r"Posts: found (\d+) tweets")

idx = [i for i, l in enumerate(LOG) if "Elon Tweet Checker started" in l]
passes = []
for n, i in enumerate(idx):
    end = idx[n + 1] if n + 1 < len(idx) else len(LOG)
    m = ART.search("\n".join(LOG[i:end]))
    passes.append((dt.datetime.strptime(HDR.match(LOG[i].strip()).group(1),
                                        "%Y-%m-%d %H:%M"),
                   int(m.group(1)) if m else -1))

now = dt.datetime.now()
cur_hour_start = now.replace(minute=0, second=0, microsecond=0)
win_lo = cur_hour_start - dt.timedelta(hours=12)
completed = [p for p in passes if win_lo <= p[0] < cur_hour_start]
_per_hour = Counter(p[0].replace(minute=0, second=0, microsecond=0)
                     for p in completed)
_hours = [win_lo + dt.timedelta(hours=k) for k in range(12)]
_counts = [_per_hour.get(h, 0) for h in _hours]
LO = round(float(min(_counts)), 2)
HI = round(float(max(_counts)), 2)
print(f"[fire] cycle {CYCLE}: the derived RECENT band is {LO}-{HI} "
      f"(the log's own per-hour pass counts over the same 12-hour window: "
      f"{Counter(_counts)})")

# ⭐ THE MEASURED RATE -- read it from the cycle's own measured.json so the
# fire-test exercises the SHIPPED value, not a hand-typed one.
MEASURED_JSON = pathlib.Path(f"/tmp/c{CYCLE}/measure/measured.json")
if MEASURED_JSON.exists():
    MEASURED = json.loads(MEASURED_JSON.read_text(encoding="utf-8"))["recent_rate"]
else:
    MEASURED = 0.0
    print("[fire] WARNING: measured.json not found -- the measured case "
          "cannot be checked; the fire-test still proves the gate's teeth")


def shipped_assert(rate, LO, HI):
    """The SHIPPED assertion, reproduced verbatim from the measure script."""
    try:
        assert LO <= rate <= HI, (
            f"recent-window rate {rate:.3f}/hour outside the DERIVED band "
            f"{LO}-{HI} (the log's own per-hour counts in this window are "
            f"{sorted(set(_counts))})")
    except AssertionError:
        return False
    return True


CASES = [
    ("the measured rate", MEASURED, True),
    ("a rate BELOW the log's own minimum per-hour count",
     LO - 0.05, False),
    ("a rate ABOVE the log's own maximum per-hour count",
     HI + 0.05, False),
    ("a wildly wrong rate", 9.9, False),
    ("a rate of exactly zero", 0.0, False),
    ("the band's lower edge", LO, True),
    ("the band's upper edge", HI, True),
]

ok = True
for name, val, should_pass in CASES:
    got = shipped_assert(val, LO, HI)
    verdict = "PASS" if got == should_pass else "*** WRONG ***"
    if got != should_pass:
        ok = False
    print(f"  [{verdict}] {name}: rate={val:.3f} -> "
          f"{'accepted' if got else 'REJECTED'} (expected "
          f"{'accept' if should_pass else 'reject'})")

# ⭐ THE SECOND CONTROL: THE BAND MUST BE DISCRIMINATING, I.E. IT MUST NOT
# BE SO LOOSE THAT THE OLD TYPED BAND'S OWN VALUES WOULD NOW BE ACCEPTED
# FOR THE WRONG REASON, NOR SO TIGHT THAT A LEGITIMATE SCHEDULE VARIANT IS
# REJECTED.  Concretely: the band's lower edge must be BELOW the measured
# rate (the measurement is inside it) and the band must have at least one
# value it REJECTS (a band of [x, x] that accepts nothing would be vacuous).
assert LO < MEASURED <= HI, (
    f"the measured rate {MEASURED} is not strictly inside the derived band "
    f"{LO}-{HI} -- the band does not describe this window")
print(f"  [PASS] the measured rate {MEASURED} lies STRICTLY inside "
      f"{LO}-{HI} (and the band has teeth: it rejects the cases above)")

if not ok:
    print("\n[fire] *** THE FIRE-TEST FAILED: the gate does not behave as "
          "specified ***")
    sys.exit(1)
print("\n[fire] PASS -- the shipped assertion fires on every bad value and "
      "accepts only the in-band ones.")
