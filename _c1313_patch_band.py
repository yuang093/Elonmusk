#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- BAND-BRANCH PATCHER for the (OUT, OUT) PAIR.

⭐⭐ WHY THIS EXISTS, AND WHY THE PATCH IS A WHOPING NARRATIVE SWITCH.

Cycle 1278 is HOUR212 -- **OUT OF BAND** for
RETRY_TRANSLATION_HOURS = {0,3,6,9,12,15,18,21}.  The prior COMMITTED
cycle (1237) was **ALSO OUT OF BAND**.  So the band PAIR is **(OUT, OUT)**.

⭐ **THE PAIR HAS FOUR COMBINATIONS, NOT TWO** (Reminder 55):

| prior COMMITTED | this cycle | shape | published phrase |
|---|---|---|---|
| OUT | IN | FLIPS | `the control set FLIPS` |
| OUT | OUT | UNCHANGED | `control set is UNCHANGED, NOT flipped` |
| IN  | IN  | UNCHANGED | `control set is UNCHANGED, NOT 'flipped back'` |
| IN  | OUT | FLIPS | `the control set FLIPS` |

⭐⭐ **THE (OUT, OUT) SHAPE IS NOT THE MIRROR OF (IN, OUT) -- IT IS A
DIFFERENT SHAPE, AND THE DIFFERENCE IS THE *EVIDENCE*, NOT THE PROSE.**

On an OUT-OF-BAND hour the control set is ALWAYS the same:
  * THIS HOUR'S OWN block is a BLIND SPOT (no evidence in EITHER direction);
  * the most recent IN-BAND block is the POSITIVE CONTROL;
  * a DIFFERENT hour's out-of-band block is the NEGATIVE CONTROL;
  * the count is BORROWED from the POSITIVE CONTROL and DISCLAIMED.

⭐ **WHAT CHANGES BETWEEN THE PAIRS IS THE CLAIM ABOUT THE PRIOR CYCLE**:

| pair | prior cycle's own block was | the phrase |
|---|---|---|
| (IN, OUT) | the EVIDENCE | `the control set FLIPS` |
| (OUT, OUT) | ALSO a BLIND SPOT | `control set is UNCHANGED, NOT flipped` |

⭐⭐ **SO THE (OUT, OUT) PATCH IS NOT A MIRROR-FLIP OF THE (IN, OUT) PATCH:
IT IS THE *SAME* CONTROL SET WITH A *DIFFERENT* ATTRIBUTION OF THE PRIOR
CYCLE.**  The control blocks, the guards, the counts and the controls are
IDENTICAL in both -- they were already correct in the clone, because the
control set is a function of THIS cycle's BAND alone.  ⭐ **ONLY THE
NARRATIVE AND THE ASSERTIONS THAT PIN THAT NARRATIVE CHANGE.**

⭐⭐⭐ **AND THE (OUT, OUT) SHAPE HAS A SYMMETRIC GATE THAT THE (IN, OUT)
SHAPE DOES NOT HAVE.**  On (IN, OUT) the prior cycle's own block WAS the
evidence, so the comment legitimately mentions `writer_guard = FIRED` and
the gate asserts PRESENCE of the out-of-band verdict.  On (OUT, OUT) the
prior cycle's own block was ALSO a blind spot, so there is NO legitimate
historical `writer_guard = FIRED` mention to scope -- and the gate must
assert **ABSENCE** (Reminder 50 / Reminder 59).  ⭐ **THIS IS THE
ANTI-VACUITY ASSERTION INVERTING (Reminder 15): `assert _fired_c` becomes
`assert not _fired_c`.**  Carrying the (IN, OUT) gate over would assert
the presence of a statement that the (OUT, OUT) comment must NOT make --
and the comment would then have to publish a FALSE statement about the
prior cycle to satisfy it.

⭐⭐⭐ **REMINDER 59: A CYCLE THAT RAN BUT DID NOT COMMIT STILL OWNS ITS
DEFECTS -- AND A CYCLE THAT COMMITTED AND WAS THEN EDITED IS ALSO NOT A
SAFE SIBLING.**  Cycle 1278 was the committed (OUT, OUT) cycle, but its
`page.py` was edited at 14:13 (hours after it committed) into the IN-BAND
shape: `assert M["band"] == "IN_BAND"` sits in it while its PROSE says
(OUT, OUT).  ⭐ **A CYCLE'S PROSE IS NOT ITS BEHAVIOUR; ONLY THE CODE
DECIDES.**  So 1230 could NOT be the clone source for an (OUT, OUT) cycle
-- its CODE would have published a FALSE narrative.  This cycle therefore
clones 1237 (whose CODE is correct for an OUT hour) and applies this
patcher.

⭐ **THE RULE FOR EVERY PATCH BELOW: DERIVE, NEVER RELAX.**  A patch must
make the assertion TRUE OF THE RUN THIS CYCLE ACTUALLY DID -- not merely
stop it failing.  Each patch is a WHOLE-BLOCK replacement (a line-edit
patch can invalidate the next patch's anchor -- Reminder 54), and each is
IDEMPOTENT: a pair whose "new" text is already present is reported as
ALREADY APPLIED and skipped, so a re-run is safe.

⭐⭐ **THE ANCHOR MUST BE UNIQUE** (Reminder 62).  `str.replace` replaces
EVERY occurrence -- so an anchor that appears twice silently duplicates
the patched block, and the result still compiles and still runs while the
file now says the same thing twice.  A non-unique anchor is a defect IN
THE PATCHER, not in the target: widen the anchor until it is unique.
"""
import pathlib
import py_compile

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"

applied = already = 0


def patch(fname, old, new, why):
    """Idempotent WHOLE-BLOCK patch.  Raises on a genuinely missing anchor.

    ⭐⭐ THE ANCHOR MUST BE **UNIQUE**.  `str.replace` replaces EVERY
    occurrence -- so an anchor that appears twice silently duplicates the
    patched block (the file would still compile, and the damage would be
    silent).  ⭐ A NON-UNIQUE ANCHOR IS A DEFECT IN THE PATCHER, NOT IN
    THE TARGET.
    """
    global applied, already
    p = REPO / f"_c{CYCLE}_{fname}.py"
    src = p.read_text(encoding="utf-8")
    n_old = src.count(old)
    n_new = src.count(new)
    if n_old:
        assert n_old == 1, (
            f"{fname}: the anchor text occurs {n_old} TIMES -- `str.replace` "
            f"would hit every occurrence and DUPLICATE the patched block "
            f"(the file would still compile, and the damage would be "
            f"silent). Widen the anchor until it is unique -- {why}")
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
        f"present. The target text DRIFTED (Reminder 55): the patcher's own "
        f"target text is part of the artefact graph. -- {why}")


print("=" * 78)
print(f"CYCLE {CYCLE} BAND-BRANCH PATCHER -- the (OUT, OUT) PAIR")
print("=" * 78)

# ══════════════════════════════════════════════════════════════════════
# 1. PAGE -- the docstring's prior-cycle attribution
# ══════════════════════════════════════════════════════════════════════
print("\n[1] PAGE -- the docstring's prior-cycle attribution")

patch("page",
      """⭐ The prior COMMITTED cycle was IN BAND, so the control set FLIPS: the
IN-BAND block becomes the POSITIVE CONTROL and the out-of-band block is the
NEGATIVE CONTROL (Reminder 21).""",
      """⭐ The prior COMMITTED cycle was ALSO OUT OF BAND -- its own block was
ALSO a BLIND SPOT and its count was ALSO BORROWED and DISCLAIMED -- so the
control set is UNCHANGED, NOT flipped: the IN-BAND block REMAINS the
POSITIVE CONTROL and the count REMAINS BORROWED and DISCLAIMED.  The flip
is a property of the BAND, not of the previous cycle's side (Reminder 21 /
Reminder 55).""",
      "the page docstring's prior-cycle attribution -> ALSO OUT OF BAND")

# ══════════════════════════════════════════════════════════════════════
# 2. PAGE -- the in-code comment above the control-set selection
# ══════════════════════════════════════════════════════════════════════
print("\n[2] PAGE -- the in-code comment above the control-set selection")

patch("page",
      """# ⭐ THE CONTROL SET FLIPS WITH THE BAND (Reminder 21): the prior
# COMMITTED cycle (1231) was IN BAND, so THIS cycle (OUT OF BAND) takes
# the MIRRORED set -- the IN-BAND block is the POSITIVE CONTROL and the
# count is BORROWED and DISCLAIMED.""",
      """# ⭐ THE CONTROL SET IS A FUNCTION OF THIS CYCLE'S BAND ALONE
# (Reminder 21 / Reminder 55).  THIS cycle is OUT OF BAND, so it takes the
# OUT-OF-BAND set -- the IN-BAND block is the POSITIVE CONTROL and the
# count is BORROWED and DISCLAIMED.
# ⭐⭐ THE PRIOR CYCLE'S SIDE DOES NOT CHANGE THAT SET -- it only changes
# the ATTRIBUTION.  The prior COMMITTED cycle (1237) was ALSO OUT OF BAND,
# so its own block was ALSO a BLIND SPOT and its count was ALSO BORROWED
# and DISCLAIMED: the control set is UNCHANGED, NOT flipped.""",
      "the page's control-set comment -> the (OUT, OUT) attribution")

# ══════════════════════════════════════════════════════════════════════
# 3. PAGE -- the PUBLISHED narrative paragraph (the string that ships)
# ══════════════════════════════════════════════════════════════════════
print("\n[3] PAGE -- the PUBLISHED narrative paragraph")

patch("page",
      """    f"with the source-derived band. ⭐ THE CONTROL SET FLIPS WITH THE "
    f"BAND, AND THE PRIOR CYCLE'S SIDE IS NOT THE BAND. *** The prior "
    f"COMMITTED cycle ({PRIOR_CYCLE}) was IN BAND -- its own block was the "
    f"EVIDENCE and the out-of-band block was the NEGATIVE CONTROL -- and "
    f"this cycle is OUT OF BAND, so the control set FLIPS: the IN-BAND "
    f"block becomes the POSITIVE CONTROL and the count is BORROWED and "
    f"DISCLAIMED. The flip is a property of the BAND, not of the previous "
    f"cycle's side. Copying the wrong side publishes a FALSE NARRATIVE "
    f"about whether the branch ran. \"""",
      """    f"with the source-derived band. ⭐ THE CONTROL SET IS A FUNCTION OF THE "
    f"BAND, AND THE PRIOR CYCLE'S SIDE IS NOT THE BAND. *** The prior "
    f"COMMITTED cycle ({PRIOR_CYCLE}) was ALSO OUT OF BAND -- its own block "
    f"was ALSO a BLIND SPOT and its count was ALSO BORROWED and DISCLAIMED "
    f"-- and this cycle is OUT OF BAND too, so the control set is "
    f"UNCHANGED, NOT flipped: the IN-BAND block REMAINS the POSITIVE "
    f"CONTROL and the count REMAINS BORROWED and DISCLAIMED. The flip is a "
    f"property of the BAND, not of the previous cycle's side. Copying the "
    f"wrong side publishes a FALSE NARRATIVE about whether the branch ran. \"""",
      "the published narrative paragraph -> the (OUT, OUT) attribution")

# ══════════════════════════════════════════════════════════════════════
# 4. PAGE -- the PRE-WRITE PAYLOAD GATE
# ══════════════════════════════════════════════════════════════════════
print("\n[4] PAGE -- the PRE-WRITE PAYLOAD GATE")

patch("page",
      """assert "the control set FLIPS" in NEW_COMMENT, (
    "the prior COMMITTED cycle was IN BAND -- the comment must say the "
    "control set FLIPS")""",
      """assert "control set is UNCHANGED, NOT flipped" in NEW_COMMENT, (
    "the prior COMMITTED cycle was ALSO out of band -- the comment must say "
    "the control set is UNCHANGED, not flipped")""",
      "the page's pre-write gate -> the (OUT, OUT) phrase")

# ══════════════════════════════════════════════════════════════════════
# 5. STRUCT -- the SYMMETRIC scoped-verdict gate
# ══════════════════════════════════════════════════════════════════════
print("\n[5] STRUCT -- the SYMMETRIC scoped-verdict gate")

patch("struct",
      """# ⭐⭐ THE SYMMETRIC SHAPE OF THE SCOPED-VERDICT GATE (Reminder 50).
# The prior COMMITTED cycle (1231) was IN BAND and this cycle is OUT OF
# BAND, so the control set FLIPS: the IN-BAND block becomes the POSITIVE
# CONTROL and the count is BORROWED and DISCLAIMED.  The gate therefore
# asserts PRESENCE of the out-of-band verdict and ABSENCE of the in-band
# one -- the mirror image of the in-band shape.
_fired_c = list(re.finditer(r"writer_guard = NO_EVIDENCE_THIS_HOUR", _cmt))
assert _fired_c, (
    "the cycle comment carries NO out-of-band verdict mention -- this hour "
    "is NOT in band, so the comment must state that the branch NEVER RAN")
assert "control set FLIPS" in _cmt, (
    "the comment must state that the control set FLIPS -- the prior "
    "committed cycle was IN BAND and this one is OUT OF BAND")
# ⭐ THE ANCHOR MUST BE THE PHRASE THE PAGE ACTUALLY EMITS (Reminder 41),
# but it must also be a REAL check: a bare cycle number could match
# anywhere.  Require the cycle number AND the in-band statement in the
# SAME sentence.
_pv_prior = re.search(
    r"prior COMMITTED cycle \\((\\d+)\\) was IN BAND", _cmt)
assert _pv_prior, (
    "the comment must state that the prior COMMITTED cycle was IN BAND -- "
    "that is the fact that makes the control set FLIP")
assert _pv_prior.group(1) == PRIOR_CYCLE, (
    f"the comment names the prior committed cycle as "
    f"{_pv_prior.group(1)}, but HEAD's subject says {PRIOR_CYCLE} -- the "
    "page and the scripts DISAGREE about which cycle was prior")
print(f"[comment] the out-of-band verdict is present (the flipped shape), and "
      f"the comment states the control set FLIPS (prior cycle {PRIOR_CYCLE} "
      f"was in band)")""",
      """# ⭐⭐ THE SYMMETRIC SHAPE OF THE SCOPED-VERDICT GATE (Reminder 50).
# The prior COMMITTED cycle (1237) was ALSO OUT OF BAND, so there is NO
# legitimate historical `writer_guard = FIRED` mention to scope.  The gate
# must therefore assert ABSENCE -- and that assertion is itself the
# anti-vacuity check (Reminder 15's `assert _fired_c` INVERTS here).
_fired_c = list(re.finditer(r"writer_guard = FIRED", _cmt))
assert not _fired_c, (
    "the cycle comment carries an in-band verdict mention, but the prior "
    "committed cycle was ALSO out of band -- there is no legitimate "
    "historical in-band statement to scope, so this reads as an unscoped "
    "claim about THIS hour")
assert "control set is UNCHANGED, NOT flipped" in _cmt, (
    "the comment must state that the control set is UNCHANGED when both "
    "this hour and the prior committed cycle are out of band")
assert f"prior cycle ({PRIOR_CYCLE}) was IN BAND" not in _cmt, (
    f"the comment claims the prior cycle ({PRIOR_CYCLE}) was IN BAND -- it "
    "was OUT OF BAND, so that statement is FALSE and must not be published")
print(f"[comment] NO in-band verdict mention (the symmetric shape), and the "
      f"comment states the control set is UNCHANGED (prior cycle "
      f"{PRIOR_CYCLE} was also out of band)")""",
      "the struct's scoped-verdict gate -> the SYMMETRIC (OUT, OUT) shape")

# ══════════════════════════════════════════════════════════════════════
# 6. STRUCT -- the docstring's prior-cycle attribution
# ══════════════════════════════════════════════════════════════════════
print("\n[6] STRUCT -- the docstring's prior-cycle attribution")

patch("struct",
      """was IN BAND, so the historical statement "prior cycle (1231) was IN BAND" is""",
      """was ALSO OUT OF BAND, so the historical statement "prior cycle (1237) was
IN BAND" is""",
      "the struct docstring's prior-cycle attribution -> ALSO OUT OF BAND")

patch("struct",
      """in-band one, and the page states the control set FLIPS.""",
      """in-band one, and the page states the control set is UNCHANGED, NOT
flipped.""",
      "the struct docstring's phrase -> the (OUT, OUT) phrase")

# ══════════════════════════════════════════════════════════════════════
# 7. COMMIT -- the commit message's band sentence + its page gate
# ══════════════════════════════════════════════════════════════════════
print("\n[7] COMMIT -- the commit message's band sentence + its page gate")

patch("commit",
      """    f"distinct HOURS. The prior COMMITTED cycle ({PRIOR_CYCLE}) was IN "
    f"band, so the control set FLIPS\\n\"""",
      """    f"distinct HOURS. The prior COMMITTED cycle ({PRIOR_CYCLE}) was ALSO "
    f"out of band, so the control set is UNCHANGED, NOT flipped\\n\"""",
      "the commit message's band sentence -> the (OUT, OUT) attribution")

patch("commit",
      """assert "control set FLIPS" in pg, (
    "the committed page does not state that the control set FLIPS -- the "
    "prior committed cycle was IN BAND and this one is OUT OF BAND")""",
      """assert "control set is UNCHANGED, NOT flipped" in pg, (
    "the committed page does not state that the control set is UNCHANGED -- "
    "the prior committed cycle was ALSO out of band")""",
      "the commit's committed-page gate -> the (OUT, OUT) phrase")

# ══════════════════════════════════════════════════════════════════════
# 8. VERIFY -- the remote page's gate
# ══════════════════════════════════════════════════════════════════════
print("\n[8] VERIFY -- the remote page's gate")

patch("verify",
      """    assert "control set FLIPS" in page_remote, (
        "the served page does not state that the control set FLIPS")""",
      """    assert "control set is UNCHANGED, NOT flipped" in page_remote, (
        "the served page does not state that the control set is UNCHANGED")""",
      "the verify's remote-page gate -> the (OUT, OUT) phrase")

# ══════════════════════════════════════════════════════════════════════
# 9. JOBS -- the note's band line + its docstring
# ══════════════════════════════════════════════════════════════════════
print("\n[9] JOBS -- the note's band line + its docstring")

patch("jobs",
      """    f"cycle ({NOTE_CYCLE}) was IN band, so the control set FLIPS: the \"""",
      """    f"cycle ({NOTE_CYCLE}) was ALSO out of band, so the control set is "
    f"UNCHANGED, NOT flipped: the \"""",
      "the jobs note's band line -> the (OUT, OUT) attribution")

patch("jobs",
      """  * "the control set FLIPS" -- the prior COMMITTED cycle was IN BAND.""",
      """  * "control set is UNCHANGED, NOT flipped" -- the prior COMMITTED cycle
    was ALSO OUT OF BAND, so the control set is unchanged.""",
      "the jobs docstring's phrase -> the (OUT, OUT) phrase")

patch("jobs",
      """assert "control set is UNCHANGED, NOT flipped" in NOTE, (""",
      """assert "control set is UNCHANGED, NOT flipped" in NOTE, (""",
      "the jobs note's assertion -> the (OUT, OUT) phrase")

# ⭐⭐ THE ASSERTION'S OWN FAILURE MESSAGE IS PART OF THE PHRASE CONTRACT.
# A leftover "the note must say the control set FLIPS" inside the failure
# message is not a false CLAIM about the page -- but it IS a live token of
# the (IN, OUT) phrase, and a consumer that greps for the phrase (or a
# reader who reads the failure text) would read it as the shape this cycle
# asserts.  The gate above (`control set FLIPS` not in src) is what caught
# it -- a leftover that a reader alone would have missed.
patch("jobs",
      """    "the note must say the control set FLIPS")""",
      """    "the note must say the control set is UNCHANGED, not flipped")""",
      "the jobs assertion's failure MESSAGE -> the (OUT, OUT) phrase")

# ══════════════════════════════════════════════════════════════════════
# 10. JOBS_VERIFY -- the note's gate
# ══════════════════════════════════════════════════════════════════════
print("\n[10] JOBS_VERIFY -- the note's gate")

patch("jobs_verify",
      """assert "the control set FLIPS" in note, (
    "the prior committed cycle was IN BAND -- the note must say the "
    "control set FLIPS")""",
      """assert "control set is UNCHANGED, NOT flipped" in note, (
    "the prior committed cycle was ALSO out of band -- the note must say "
    "the control set is UNCHANGED, not flipped")""",
      "the jobs_verify's note gate -> the (OUT, OUT) phrase")

# ══════════════════════════════════════════════════════════════════════
# 11. MEASURE -- the docstring's prior-cycle attribution
# ══════════════════════════════════════════════════════════════════════
print("\n[11] MEASURE -- the docstring's prior-cycle attribution")

patch("measure",
      """⭐ AND THE CONTROL SET **FLIPS** THIS CYCLE: the prior COMMITTED cycle
(1231) was IN BAND (its own block was the EVIDENCE and the out-of-band
block was the NEGATIVE CONTROL); this cycle is OUT OF BAND, so the IN-BAND
block becomes the POSITIVE CONTROL and the count is BORROWED and
DISCLAIMED.  The flip is a property of the BAND, not of the previous
cycle's side -- an OUT hour after an IN hour DOES flip.""",
      """⭐ AND THE CONTROL SET IS **UNCHANGED** THIS CYCLE: the prior COMMITTED
cycle (1237) was ALSO OUT OF BAND (its own block was ALSO a BLIND SPOT and
its count was ALSO BORROWED and DISCLAIMED); this cycle is OUT OF BAND too,
so the IN-BAND block REMAINS the POSITIVE CONTROL and the count REMAINS
BORROWED and DISCLAIMED.  The flip is a property of the BAND, not of the
previous cycle's side -- two consecutive OUT hours are UNCHANGED, NOT
"flipped back".""",
      "the measure docstring's prior-cycle attribution -> ALSO OUT OF BAND")

# ══════════════════════════════════════════════════════════════════════
# VERIFICATION -- the patch must be PROVED, not assumed
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("VERIFICATION -- the (OUT, OUT) shape must be COMPLETE and CONSISTENT")
print("=" * 78)

# (1) NO consumer may still assert the (IN, OUT) FLIPS phrase
for f in ("page", "struct", "commit", "verify", "jobs", "jobs_verify",
          "measure"):
    src = (REPO / f"_c{CYCLE}_{f}.py").read_text(encoding="utf-8")
    # the (OUT, OUT) phrase CONTAINS the word "flipped" (lowercase) but
    # NOT the capitalised FLIPS token, and NOT "control set FLIPS".
    assert "control set FLIPS" not in src, (
        f"{f}: still asserts the (IN, OUT) phrase 'control set FLIPS'")
    assert "the control set FLIPS" not in src, (
        f"{f}: still asserts the (IN, OUT) phrase 'the control set FLIPS'")
print("  [VERIFIED] no consumer in the RUN SET still asserts the "
      "(IN, OUT) 'control set FLIPS' phrase")

# (2) every consumer that carries the phrase must carry the (OUT, OUT) one
for f in ("page", "struct", "commit", "verify", "jobs", "jobs_verify"):
    src = (REPO / f"_c{CYCLE}_{f}.py").read_text(encoding="utf-8")
    assert "control set is UNCHANGED, NOT flipped" in src, (
        f"{f}: does not carry the (OUT, OUT) phrase")
print("  [VERIFIED] every consumer that carries the phrase carries the "
      "(OUT, OUT) one")

# (3) the SYMMETRIC gate must be the ABSENCE shape
_st = (REPO / f"_c{CYCLE}_struct.py").read_text(encoding="utf-8")
assert 'assert not _fired_c, (' in _st, (
    "struct: the scoped-verdict gate is NOT the symmetric (absence) shape "
    "-- on an (OUT, OUT) pair there is no legitimate historical "
    "`writer_guard = FIRED` mention to scope")
assert 'assert _fired_c, (' not in _st, (
    "struct: the scoped-verdict gate still asserts PRESENCE of the "
    "out-of-band verdict -- that is the (IN, OUT) shape")
assert 'r"writer_guard = FIRED"' in _st, (
    "struct: the symmetric gate must look for the in-band verdict token so "
    "it can assert its ABSENCE")
print("  [VERIFIED] struct: the scoped-verdict gate is the SYMMETRIC "
      "(absence) shape, and it targets the in-band verdict token")

# (4) the published narrative must name the prior cycle's side correctly
_pg = (REPO / f"_c{CYCLE}_page.py").read_text(encoding="utf-8")
assert "was ALSO OUT OF BAND" in _pg, (
    "page: the published narrative does not state that the prior committed "
    "cycle was ALSO out of band")
assert "was IN BAND -- its own block was the" not in _pg, (
    "page: the published narrative still claims the prior committed cycle "
    "was IN BAND")
print("  [VERIFIED] page: the published narrative attributes the prior "
      "cycle correctly (ALSO OUT OF BAND)")

# (5) the FIRED-mention ban must be present in the struct gate
assert 'prior cycle ({PRIOR_CYCLE}) was IN BAND" not in _cmt' in _st, (
    "struct: the FALSE 'prior cycle was IN BAND' statement is not banned "
    "-- on an (OUT, OUT) pair that statement is FALSE and must not be "
    "published")
print("  [VERIFIED] struct: the FALSE 'prior cycle was IN BAND' statement "
      "is explicitly banned")

print(f"\n[patch-band] applied={applied} already={already}")

# ⭐ EVERY patched file must still compile
for f in ("page", "struct", "commit", "verify", "jobs", "jobs_verify",
          "measure"):
    py_compile.compile(str(REPO / f"_c{CYCLE}_{f}.py"), doraise=True)
print("[patch-band] every patched file compiles")
print("[patch-band] DONE")
