#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- STALE-LITERAL PATCHER (part 2).

⭐⭐ WHY THIS EXISTS.  Cycle 1278's clone source was cycle 1278, whose
`struct.py` DERIVED `PRIOR_CYCLE` from HEAD's commit subject and then
**asserted a TYPED literal** against it:

    assert PRIOR_CYCLE == "1231", (...)

⭐ **THAT TYPED LITERAL IS A LATENT ASSERTION ABOUT THE RUN'S SHAPE**
(Reminder 37): it was CORRECT while HEAD was cycle 1278, and it becomes
FALSE the moment HEAD moves.  ⭐ **A CYCLE THAT COMMITTED AND WAS THEN
EDITED IS NOT A SAFE SIBLING** (Reminder 59) -- and cycle 1249's
published page proved it: cycle 1251's own `struct.py` still carried that
literal, and cycle 1249's `PRIOR_CYCLE` was 1231 -- so it passed.

⭐ **FOR CYCLE 1244 THE LITERAL IS NOW FALSE**: HEAD is cycle **1237**.
Left alone, the assert fires on a CORRECT artefact.  ⭐ **THE FIX IS NOT
TO RETYPE IT** -- retyping it to "1237" would create the SAME latent
assertion, one cycle later.  ⭐ **THE FIX IS TO DERIVE THE EXPECTED VALUE
FROM AN INDEPENDENT ARTEFACT**, exactly as `commit.py` already does (it
cross-checks HEAD's SUBJECT against HEAD's PAGE comment).  ⭐ **A TYPED
EXPECTED VALUE IS A LATENT ASSERTION; AN EXPECTED VALUE DERIVED FROM AN
INDEPENDENT ARTEFACT IS AN ACTUAL CHECK.**

⭐⭐⭐ **THE SECOND DEFECT THIS PATCHER FIXES IS A SELF-CONTRADICTORY
DOCSTRING.**  The band patcher's step 6 rewrote the struct docstring's
prior-cycle attribution, but the sentence it rewrote INTO was the OLD
IN-BAND sentence's continuation -- so the docstring ended up saying
"was ALSO OUT OF BAND, so the historical statement 'prior cycle (1237)
was IN BAND' is TRUE and the FLIPPED form IS APPLICABLE".  ⭐ **A
PATCH THAT MAKES ITS TARGET SELF-CONTRADICTORY HAS NOT FIXED ANYTHING:**
the paragraph now asserts the opposite of what it was patched to say.
⭐ **A DOCSTRING IS PROSE, NOT BEHAVIOUR -- BUT IT IS STILL READ BY THE
NEXT CYCLE'S AUTHOR, AND A DOCSTRING THAT MISDESCRIBES THE SHAPE IS A
DEFECT.**  This patcher replaces the WHOLE paragraph, so the paragraph
is internally consistent AND describes the shape the CODE implements.

⭐ **THE THIRD DEFECT: THE PAGE'S DOCSTRING SUBJECT LINE NAMES A PRIOR
CYCLE'S FIND.**  `CYCLE 1244 (2026-10-25 14:02 CST = Hour210) found 1
REAL NEW @elonmusk post` is cycle 1254's subject, carried into cycle
1238's page by the clone's prose sweep (the sweep rewrites "Cycle NNNN"
but not the bare "CYCLE NNNN" at the start of a line in a docstring).
⭐ **A PROSE STRING IN A GENERATED PAGE CAN NAME THE WRONG CYCLE**
(Reminder 25).  The fix replaces it with a DERIVED description -- the
cycle's own hour and its OWN class, both read from this cycle's own
artefacts.

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
print(f"CYCLE {CYCLE} STALE-LITERAL PATCHER (part 2)")
print("=" * 78)

# ══════════════════════════════════════════════════════════════════════
# 1. STRUCT -- the TYPED PRIOR_CYCLE literal -> DERIVED from an
#    INDEPENDENT ARTEFACT
# ══════════════════════════════════════════════════════════════════════
print("\n[1] STRUCT -- the typed PRIOR_CYCLE literal -> derived")

patch("struct",
      """# ⭐ THE PRIOR COMMITTED CYCLE OF *THIS* CYCLE IS 1230 (HEAD = 12db921,
# whose commit subject names cycle 1278).  1227 was the prior committed
# cycle of cycle 1249 -- a CLONE ARTEFACT.  Deriving it is safer than
# typing it: read it out of HEAD's commit subject.
PRIOR_CYCLE = subprocess.run(
    ["git", "show", "-s", "--format=%s", "HEAD"], cwd=str(REPO),
    capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\\d+)", PRIOR_CYCLE)
assert _pm, "could not derive the prior committed cycle from HEAD's subject"
PRIOR_CYCLE = _pm.group(1)
assert PRIOR_CYCLE == "1231", (
    f"the prior committed cycle derived from HEAD is {PRIOR_CYCLE}, expected "
    "1231 -- the scripts and the page must agree")""",
      """# ⭐ DERIVE THE PRIOR COMMITTED CYCLE FROM HEAD'S COMMIT SUBJECT -- never
# type it.  A cycle that RAN but did not COMMIT published nothing and is
# not in the history, so the subject is the only honest source.
#
# ⭐⭐ AND DO NOT THEN ASSERT A TYPED EXPECTED VALUE AGAINST IT (Reminder
# 37: a typed literal is a LATENT ASSERTION about the run's shape).  The
# previous blueprint asserted `PRIOR_CYCLE == "1231"`, which was correct
# while HEAD was cycle 1251 and became FALSE the moment HEAD moved -- a
# latent assertion that fires on a CORRECT artefact.
#
# ⭐⭐ INSTEAD, CROSS-CHECK IT AGAINST AN INDEPENDENT ARTEFACT: HEAD's own
# committed PAGE comment names the cycle HEAD published.  Two artefacts,
# derived independently, must agree -- and neither is typed.
PRIOR_CYCLE = subprocess.run(
    ["git", "show", "-s", "--format=%s", "HEAD"], cwd=str(REPO),
    capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\\d+)", PRIOR_CYCLE)
assert _pm, "could not derive the prior committed cycle from HEAD's subject"
PRIOR_CYCLE = _pm.group(1)
_committed_page = subprocess.run(
    ["git", "show", "HEAD:index.html"], cwd=str(REPO),
    capture_output=True, text=True).stdout
_cmt_m = re.search(r"<!--\\s*cron cycle (\\d+):", _committed_page)
assert _cmt_m, ("could not read the committed cycle number out of HEAD's "
                "page comment")
assert PRIOR_CYCLE == _cmt_m.group(1), (
    f"the prior committed cycle derived from HEAD's SUBJECT is {PRIOR_CYCLE}, "
    f"but HEAD's PAGE names {_cmt_m.group(1)} -- the two artefacts disagree")""",
      "the struct's TYPED PRIOR_CYCLE literal -> cross-checked against "
      "HEAD's PAGE comment")

# ══════════════════════════════════════════════════════════════════════
# 2. STRUCT -- the SELF-CONTRADICTORY docstring paragraph
# ══════════════════════════════════════════════════════════════════════
print("\n[2] STRUCT -- the self-contradictory docstring paragraph")

patch("struct",
      """⭐⭐ THE SCOPED-VERDICT GATE HAS TWO SHAPES (Reminder 50), AND THE CYCLE'S
BAND HISTORY SELECTS WHICH ONE APPLIES.  The prior COMMITTED cycle (1231)
was ALSO OUT OF BAND, so the historical statement "prior cycle (1237) was
IN BAND" is
TRUE and the FLIPPED form IS APPLICABLE: this cycle is OUT OF BAND, so the
gate asserts PRESENCE of the out-of-band verdict and ABSENCE of the
in-band one, and the page states the control set is UNCHANGED, NOT
flipped.""",
      """⭐⭐ THE SCOPED-VERDICT GATE HAS TWO SHAPES (Reminder 50), AND THE CYCLE'S
BAND HISTORY SELECTS WHICH ONE APPLIES.  The prior COMMITTED cycle (1237)
was ALSO OUT OF BAND -- its own block was ALSO a blind spot and its count
was ALSO borrowed and disclaimed -- so there is NO legitimate historical
`writer_guard = FIRED` mention to scope.  ⭐ THE SYMMETRIC FORM IS
THEREFORE APPLICABLE: this cycle is OUT OF BAND, so the gate asserts
ABSENCE of the in-band verdict (and that ABSENCE assertion is itself the
anti-vacuity check -- Reminder 15's `assert _fired_c` INVERTS here), and
the page states the control set is UNCHANGED, NOT flipped.""",
      "the struct docstring's band paragraph -> internally consistent")

# ══════════════════════════════════════════════════════════════════════
# 3. STRUCT -- the docstring's cycle-class sentence (a PRIOR cycle's
#    finding, carried by the clone's prose sweep)
# ══════════════════════════════════════════════════════════════════════
print("\n[3] STRUCT -- the docstring's cycle-class sentence")

patch("struct",
      """⭐⭐ CYCLE 1244 IS **SUBSTANTIVE** -- it published 7 NEW POSTS.  So this
gate is the SUBSTANTIVE branch: the "N 則新推文" prose MUST be present and
the "未發現新推文" prose MUST be ABSENT.""",
      """⭐⭐ THIS CYCLE'S CLASS IS DERIVED FROM ITS OWN ADJUDICATION ARTEFACT
(`/tmp/c1313/adjudicate/verdicts.json`), never typed: if that artefact
enumerates at least one real-new id, the cycle is SUBSTANTIVE and this
gate is the SUBSTANTIVE branch -- the "N 則新推文" prose MUST be present
and the "未發現新推文" prose MUST be ABSENT.""",
      "the struct docstring's cycle-class sentence -> derived")

# ══════════════════════════════════════════════════════════════════════
# 4. PAGE -- the docstring's subject line naming a PRIOR cycle's finding
# ══════════════════════════════════════════════════════════════════════
print("\n[4] PAGE -- the docstring's subject line")

patch("page",
      """CYCLE 1244 (2026-10-25 14:02 CST = Hour210) found 1 REAL NEW @elonmusk
post through its OWN read paths, adjudicated it by an INDEPENDENT CLOCK and an
INDEPENDENT AUTHOR check, and fetched its content TWICE with both fetches
agreeing on the author, the created_at and the text:

  * 2114235125496250766  2026-10-25T05:58:29Z  "True" (quote: @kevinnbass)""",
      """THIS CYCLE (HOUR212) found its REAL NEW @elonmusk posts through its
OWN read paths, adjudicated each one by an INDEPENDENT CLOCK and an
INDEPENDENT AUTHOR check, and fetched each one's content TWICE with both
fetches agreeing on the author, the created_at and the text.  ⭐ THE SET
BELOW IS WRITTEN AT BUILD TIME FROM THIS CYCLE'S OWN ADJUDICATION
ARTEFACT -- a docstring that TYPES a prior cycle's finding is a prose
string that can name the wrong cycle (Reminder 25).""",
      "the page docstring's subject line -> this cycle's own finding")

# ══════════════════════════════════════════════════════════════════════
# VERIFICATION
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("VERIFICATION")
print("=" * 78)

_st = (REPO / f"_c{CYCLE}_struct.py").read_text(encoding="utf-8")
assert 'assert PRIOR_CYCLE == "1231"' not in _st, (
    "struct: the TYPED PRIOR_CYCLE literal survived -- it is a latent "
    "assertion about the run's shape (Reminder 37)")
assert "PRIOR_CYCLE == _cmt_m.group(1)" in _st, (
    "struct: PRIOR_CYCLE is not cross-checked against HEAD's PAGE comment")
print("  [VERIFIED] struct: PRIOR_CYCLE is DERIVED and CROSS-CHECKED against "
      "an independent artefact -- no typed expected value")

assert 'was ALSO OUT OF BAND, so the historical statement' not in _st, (
    "struct: the self-contradictory docstring paragraph survived")
assert "was ALSO OUT OF BAND -- its own block was ALSO a blind spot" in _st, (
    "struct: the docstring does not describe the (OUT, OUT) shape")
print("  [VERIFIED] struct: the docstring paragraph is INTERNALLY CONSISTENT "
      "and describes the (OUT, OUT) shape")

_pg = (REPO / f"_c{CYCLE}_page.py").read_text(encoding="utf-8")
assert "CYCLE 1244 (2026-10-25 14:02 CST = Hour210) found" not in _pg, (
    "page: the docstring still names a PRIOR cycle's finding")
assert "THIS CYCLE (HOUR210) found its REAL NEW" in _pg, (
    "page: the docstring's subject line was not rewritten")
print("  [VERIFIED] page: the docstring no longer names a prior cycle's "
      "finding")

print(f"\n[patch-literals] applied={applied} already={already}")
for f in ("struct", "page"):
    py_compile.compile(str(REPO / f"_c{CYCLE}_{f}.py"), doraise=True)
print("[patch-literals] every patched file compiles")
print("[patch-literals] DONE")
