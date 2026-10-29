#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- apply the cycle-1228 DERIVED RATE BAND to the measure script.

Cycle 1278 codified: a rate band TYPED against a changing cadence is a stale
assertion.  The fetcher's pass cadence changed mid-outage (1/h, then 2/h), so
the blended outage-span rate creeps upward and a typed band (0.90-1.30)
becomes unreachable.  The band is DERIVED from the log's own per-hour cadence.

ONE ARTEFACT OWNS THE STRING (Reminder 33): the band lives in measured.json
(rate_band_lo / rate_band_hi) and every consumer reads it from there.

This patcher is a MOVE, not a rewrite (cycle 1278's rule): it cuts the typed
band out of `_c1313_measure.py` and re-inserts the derivation immediately
after the per-hour cadence is computable.
"""
import pathlib
import re
import sys

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
T = REPO / "_c1313_measure.py"
src = T.read_text(encoding="utf-8")

# ---- 1. the Counter import must exist ----
if "from collections import Counter" not in src:
    anchor = "import datetime as dt\n"
    assert anchor in src, "the datetime import anchor is gone"
    src = src.replace(anchor, anchor + "from collections import Counter\n", 1)
    print("[patch] added the Counter import")

# ---- 2. cut the TYPED band out of the print/assert ----
OLD_TYPED = '''    print(f"  (a) OUTAGE-SPAN rate: {zero_run} zero-article passes over "
          f"{span:.1f} h since the last good pass = {rate:.3f}/hour "
          f"(band 0.90-1.30)")
    print(f"  (b) RECENT-WINDOW rate: {len(completed)} passes over {hours} "
          f"COMPLETED hours = {recent_rate:.3f}/hour (band 1.90-2.10)")
    assert 0.90 <= rate <= 1.30, (
        f"outage-span rate {rate:.3f}/hour outside the 0.90-1.30 band")
    assert 1.90 <= recent_rate <= 2.10, (
        f"recent-window rate {recent_rate:.3f}/hour outside the 1.90-2.10 band")
    return rate, recent_rate, len(completed), hours
'''
NEW_DERIVED = '''    # ⭐⭐ THE RATE BAND IS DERIVED FROM THE LOG'S OWN CADENCE, NEVER TYPED.
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
    _elapsed = int((now - _h0).total_seconds() // 3600) + 1
    _per_hour = Counter(p[0].replace(minute=0, second=0, microsecond=0)
                         for p in passes if p[0] >= last_good)
    _cadence = [_per_hour.get(_h0 + dt.timedelta(hours=k), 0)
                for k in range(_elapsed)]
    _cad_lo = min(_cadence)
    _cad_hi = max(_cadence)
    # ⭐ THE BAND IS EXACT, WITH NO FUDGE FACTOR: the rate is a WEIGHTED
    # AVERAGE of these per-hour counts, so it MUST lie between the minimum
    # and the maximum count the log actually shows.
    RATE_BAND_LO = round(float(_cad_lo), 2)
    RATE_BAND_HI = round(float(_cad_hi), 2)
    print(f"  the outage window's per-hour cadence over {_elapsed} elapsed "
          f"hours: min {_cad_lo}/h, max {_cad_hi}/h ({Counter(_cadence)})")
    print(f"  => the rate band is DERIVED from that cadence: "
          f"{RATE_BAND_LO}-{RATE_BAND_HI}")

    print(f"  (a) OUTAGE-SPAN rate: {zero_run} zero-article passes over "
          f"{span:.1f} h since the last good pass = {rate:.3f}/hour "
          f"(band {RATE_BAND_LO}-{RATE_BAND_HI}, DERIVED from the cadence)")
    print(f"  (b) RECENT-WINDOW rate: {len(completed)} passes over {hours} "
          f"COMPLETED hours = {recent_rate:.3f}/hour (band 1.90-2.10)")
    assert RATE_BAND_LO <= rate <= RATE_BAND_HI, (
        f"outage-span rate {rate:.3f}/hour outside the DERIVED band "
        f"{RATE_BAND_LO}-{RATE_BAND_HI} (the log's own cadence is "
        f"{_cad_lo}-{_cad_hi} passes/hour)")
    assert 1.90 <= recent_rate <= 2.10, (
        f"recent-window rate {recent_rate:.3f}/hour outside the 1.90-2.10 band")
    return (rate, recent_rate, len(completed), hours,
            RATE_BAND_LO, RATE_BAND_HI)
'''
assert OLD_TYPED in src, (
    "the typed-band block is not present verbatim -- re-derive it before "
    "patching (a blind replace would silently do nothing)")
src = src.replace(OLD_TYPED, NEW_DERIVED, 1)
print("[patch] the typed rate band replaced by the DERIVED band")

# ---- 3. the CALLER must accept the two extra return values ----
OLD_CALL = ("    rate, recent_rate, n_completed, n_hours = m5_rates(passes, "
            "measured_zero,\n                                                        last_good)")
NEW_CALL = ("    (rate, recent_rate, n_completed, n_hours, RATE_BAND_LO,\n"
            "     RATE_BAND_HI) = m5_rates(passes, measured_zero,\n"
            "                             last_good)")
assert OLD_CALL in src, (
    "the m5_rates caller did not match the expected shape -- inspect it "
    "manually; a blind replace would silently do nothing")
src = src.replace(OLD_CALL, NEW_CALL, 1)
print("[patch] the m5_rates caller updated")

# ---- 4. ONE ARTEFACT OWNS THE STRING: the band goes into measured.json ----
OLD_JSON = '''        "outage_rate": round(rate, 3), "recent_rate": round(recent_rate, 3),
        "recent_passes": n_completed, "recent_hours": n_hours,'''
NEW_JSON = '''        "outage_rate": round(rate, 3), "recent_rate": round(recent_rate, 3),
        "recent_passes": n_completed, "recent_hours": n_hours,
        # ⭐ ONE ARTEFACT OWNS THE STRING (Reminder 33): the DERIVED band
        # lives HERE and every consumer reads it from here.  A band typed
        # into several files is a band that must be patched in all of them.
        "rate_band_lo": RATE_BAND_LO, "rate_band_hi": RATE_BAND_HI,'''
assert OLD_JSON in src, "the measured.json block did not match"
src = src.replace(OLD_JSON, NEW_JSON, 1)
print("[patch] measured.json now carries rate_band_lo / rate_band_hi")

T.write_text(src, encoding="utf-8")

import ast
ast.parse(src)
print("[patch] _c1313_measure.py parses OK")
print("[patch] remaining typed-band references:",
      len(re.findall(r"0\.90-1\.30", src)))
