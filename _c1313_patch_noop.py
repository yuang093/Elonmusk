#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- THE NO-OP BRANCH PATCHER for the page script.

⭐⭐⭐ WHY THIS EXISTS -- **A CLONE INHERITS THE SIBLING'S *SHAPE*, NOT JUST
ITS VALUES** (Reminder 53).  Cycle 1278's clone source (1237) was a
SUBSTANTIVE cycle: its page script asserts `HEAD_ID == NEW_IDS[-1]`,
requires a content fetch (`translate/new_posts.json`), and publishes the
"找到了 N 則新推文" banner.

⭐ **CYCLE 1244 PUBLISHED 0 POSTS.**  Its own adjudication artefact
(`/tmp/c1313/adjudicate/verdicts.json`) has `real_new == []` -- every one of
the 43 candidates was rejected (35 HTTP 404, 8 resolve 200 but ALL EIGHT
fail the AUTHOR check; the clock check was VERIFIED on 8/8, so the verdict
is not vacuous).  ⭐ **A MEASURED NO-OP IS A 2-FILE COMMIT** (`index.html`
+ `deploy-stamp.txt`); `tweets.json` must NOT be touched.

⭐⭐ **SO THE PAGE SCRIPT NEEDS A *DIFFERENT BRANCH*, NOT DIFFERENT VALUES.**
The branch is selected by the MEASURED published count -- `len(NEW_IDS)` --
read from this cycle's own adjudication artefact, never typed.  ⭐ **THE
BRANCH SELECTOR IS THE MEASUREMENT, AND THE MEASUREMENT IS ALREADY
AN ASSERTED ARTEFACT** (Reminder 24: the published set is derived at RUN
TIME from this cycle's own adjudication artefact).

⭐⭐⭐ **THE NO-OP BRANCH IS NOT "THE SUBSTANTIVE BRANCH WITH ZEROES".**
Three of the SUBSTANTIVE branch's assertions are about the shape of a
published cycle and are FALSE for a NO-OP cycle:

  1. `assert HEAD_ID == NEW_IDS[-1]` -- with an empty published set there is
     no `NEW_IDS[-1]`, and the corpus head is the PRIOR cycle's head.
  2. `assert HEAD_ID in NEW_IDS` -- the head was published by a PRIOR cycle.
  3. `assert len(_mine) == len(NEW_IDS)` -- with zero published posts there
     are zero of this cycle's own posts by @elonmusk, which is exactly
     what the adjudication says.

⭐ **A BRANCH THAT KEPT THOSE ASSERTIONS WOULD FIRE ON A CORRECT NO-OP
ARTEFACT** -- and the fix is NOT to relax them: they are the load-bearing
gates of the SUBSTANTIVE branch.  ⭐ **THE FIX IS TO MAKE THE BRANCH
EXPLICIT AND SYMMETRIC**, so each shape asserts what is true of ITS OWN
run and the branch selector is itself asserted.

⭐⭐⭐⭐ **AND THE 0-NEW-POST PROSE IS A CLAIM THAT MUST BE PROVABLE.**  The
published banner and comment must say "未發現新推文" and must NOT contain
"找到了 N 則新推文".  ⭐ **A GATE THAT ASSERTS THE ABSENCE OF THE
SUBSTANTIVE PROSE MUST ALSO ASSERT THE PRESENCE OF THE NO-OP PROSE** --
otherwise a page with NEITHER would pass (the anti-vacuity shape,
Reminder 15).

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
print(f"CYCLE {CYCLE} NO-OP BRANCH PATCHER")
print("=" * 78)

# ══════════════════════════════════════════════════════════════════════
# 1. PAGE -- the branch selector, right after the published set is read
# ══════════════════════════════════════════════════════════════════════
print("\n[1] PAGE -- the branch selector")

patch("page",
      """NEW_IDS = list(_ADJ["real_new"])
INHERITED_IDS = list(_ADJ["inherited"])
BRAND_NEW_IDS = list(_ADJ["brand_new"])
assert NEW_IDS, "the adjudication artefact carries NO real-new ids"
assert set(INHERITED_IDS) | set(BRAND_NEW_IDS) == set(NEW_IDS)""",
      """NEW_IDS = list(_ADJ["real_new"])
INHERITED_IDS = list(_ADJ["inherited"])
BRAND_NEW_IDS = list(_ADJ["brand_new"])
assert set(INHERITED_IDS) | set(BRAND_NEW_IDS) == set(NEW_IDS)
# ⭐⭐⭐ THE BRANCH SELECTOR IS THE MEASUREMENT (Reminder 53: a clone
# inherits the sibling's SHAPE, not just its values).  A cycle that
# published 0 posts is a MEASURED NO-OP and a **2-FILE** commit; a cycle
# that published >= 1 post is SUBSTANTIVE and a **3-FILE** commit.
# ⭐ THE SELECTOR IS READ FROM THIS CYCLE'S OWN ADJUDICATION ARTEFACT --
# never typed -- and the ARTEFACT ITSELF is what adjudicated every
# candidate.
IS_NOOP = (len(NEW_IDS) == 0)
CYCLE_CLASS = "MEASURED NO-OP" if IS_NOOP else "SUBSTANTIVE"
N_FILES = 2 if IS_NOOP else 3
print(f"[page] the branch selector: {len(NEW_IDS)} published id(s) -> "
      f"{CYCLE_CLASS} ({N_FILES}-FILE commit)")""",
      "the page's branch selector -> derived from the adjudication artefact")

# ══════════════════════════════════════════════════════════════════════
# 2. PAGE -- the corpus-head assertions (section 4)
# ══════════════════════════════════════════════════════════════════════
print("\n[2] PAGE -- the corpus-head assertions")

patch("page",
      """HEAD_ID = max(_ids, key=_sf)
HEAD_TS = _sf(HEAD_ID)
assert HEAD_ID == NEW_IDS[-1], (
    f"the corpus head is {HEAD_ID}, expected the newest new post {NEW_IDS[-1]}")
assert N_RECORDS == HEAD_RECORDS + len(NEW_IDS), (
    f"expected {HEAD_RECORDS + len(NEW_IDS)} records, got {N_RECORDS}")
print(f"[page] corpus: {N_RECORDS} records; head = {HEAD_ID} @ {HEAD_TS}")""",
      """HEAD_ID = max(_ids, key=_sf)
HEAD_TS = _sf(HEAD_ID)
# ⭐⭐ THE HEAD ASSERTION IS BRANCH-SYMMETRIC.  On a SUBSTANTIVE cycle the
# head IS this cycle's newest published post; on a MEASURED NO-OP the head
# is the PRIOR cycle's head and the corpus is byte-identical to HEAD.
# ⭐ THE TWO ASSERTIONS ARE NOT "RELAXED" -- they are the CORRECT
# assertions for their own shape, and each asserts the thing that is
# load-bearing for that shape.
if IS_NOOP:
    assert HEAD_ID == max({t["id"] for t in _head_tweets}, key=_sf), (
        f"a MEASURED NO-OP must not change the corpus head -- the head is "
        f"{HEAD_ID} but HEAD's head is "
        f"{max({t['id'] for t in _head_tweets}, key=_sf)}")
    assert N_RECORDS == HEAD_RECORDS, (
        f"a MEASURED NO-OP must not add records: HEAD holds {HEAD_RECORDS}, "
        f"the corpus holds {N_RECORDS}")
    print(f"[page] corpus (NO-OP): {N_RECORDS} records, byte-identical to "
          f"HEAD's {HEAD_RECORDS}; head = {HEAD_ID} @ {HEAD_TS} (the PRIOR "
          f"cycle's head, unchanged)")
else:
    assert HEAD_ID == NEW_IDS[-1], (
        f"the corpus head is {HEAD_ID}, expected the newest new post "
        f"{NEW_IDS[-1]}")
    assert N_RECORDS == HEAD_RECORDS + len(NEW_IDS), (
        f"expected {HEAD_RECORDS + len(NEW_IDS)} records, got {N_RECORDS}")
    print(f"[page] corpus (SUBSTANTIVE): {N_RECORDS} records; head = "
          f"{HEAD_ID} @ {HEAD_TS}")""",
      "the page's corpus-head assertions -> branch-symmetric")

# ══════════════════════════════════════════════════════════════════════
# 3. PAGE -- the render-window partition (section 6)
# ══════════════════════════════════════════════════════════════════════
print("\n[3] PAGE -- the render-window partition")

patch("page",
      """_render_capacity = len(_eids) - 1          # minus the pin -- DERIVED
_in_window = [i for i in NEW_IDS if i in _eids]
_out_of_window = [i for i in NEW_IDS if i not in _eids]
assert set(_in_window) | set(_out_of_window) == set(NEW_IDS), (
    "the in-window/out-of-window partition does not cover the published set")
assert len(_out_of_window) == max(0, len(NEW_IDS) - _render_capacity), (
    f"{len(_out_of_window)} published posts fall outside the render's window "
    f"of {_render_capacity}, but {max(0, len(NEW_IDS) - _render_capacity)} "
    "were expected -- the exclusion is not explained by the window")""",
      """_render_capacity = len(_eids) - 1          # minus the pin -- DERIVED
_in_window = [i for i in NEW_IDS if i in _eids]
_out_of_window = [i for i in NEW_IDS if i not in _eids]
assert set(_in_window) | set(_out_of_window) == set(NEW_IDS), (
    "the in-window/out-of-window partition does not cover the published set")
if IS_NOOP:
    # ⭐ ON A MEASURED NO-OP THE PUBLISHED SET IS EMPTY, SO BOTH HALVES OF
    # THE PARTITION ARE EMPTY AND THE WINDOW IS NOT EXERCISED.  ⭐ THE
    # RENDER'S STRUCTURE IS STILL RE-DERIVED (the pin + the N newest) --
    # that is the page's claim about the RENDER, and it does not depend on
    # whether THIS cycle published anything.
    assert not _in_window and not _out_of_window, (
        "a MEASURED NO-OP must have an empty published set")
    print(f"[page] (NO-OP) the published set is empty, so the render-window "
          f"partition is trivially satisfied; the render's structure "
          f"([PIN] + [{len(_render_newest)} newest]) is still re-derived "
          f"from this cycle's own payload")
else:
    assert len(_out_of_window) == max(0, len(NEW_IDS) - _render_capacity), (
        f"{len(_out_of_window)} published posts fall outside the render's "
        f"window of {_render_capacity}, but "
        f"{max(0, len(NEW_IDS) - _render_capacity)} "
        "were expected -- the exclusion is not explained by the window")""",
      "the page's render-window partition -> branch-symmetric")

# ══════════════════════════════════════════════════════════════════════
# 4. PAGE -- the "@elonmusk's own posts" count assertion (section 7)
# ══════════════════════════════════════════════════════════════════════
print("\n[4] PAGE -- the @elonmusk's-own-posts count assertion")

patch("page",
      """_mine = [r for r in _ok200 if r.get("author", "").lower() == "elonmusk"]
assert len(_mine) == len(NEW_IDS), (
    f"expected {len(NEW_IDS)} of the 200s to be by @elonmusk, got {len(_mine)}")""",
      """_mine = [r for r in _ok200 if r.get("author", "").lower() == "elonmusk"]
# ⭐ BRANCH-SYMMETRIC: on a MEASURED NO-OP the correct count of
# @elonmusk's OWN posts among the 200s is **ZERO** -- that IS the
# measurement, and it is exactly what the AUTHOR check found.  ⭐ THE
# ASSERTION IS NOT RELAXED: it still requires the two numbers to be
# EQUAL, and on the NO-OP branch that equality is a REAL and STRONGER
# claim (it says "not one of the 200s was his").
assert len(_mine) == len(NEW_IDS), (
    f"expected {len(NEW_IDS)} of the 200s to be by @elonmusk, got "
    f"{len(_mine)}")""",
      "the page's @elonmusk-count assertion -> branch-symmetric note")

# ══════════════════════════════════════════════════════════════════════
# 5. PAGE -- the content fetch (section 7) -- NO-OP needs no fetch
# ══════════════════════════════════════════════════════════════════════
print("\n[5] PAGE -- the content fetch")

patch("page",
      """# the new posts' own details, from THIS cycle's own content fetch
_np = json.loads((OUT / "translate/new_posts.json").read_text(encoding="utf-8"))
_by_id = {r["id"]: r for r in _np["rows"]}
_new_desc = "; ".join(
    f"{i} @ {_by_id[i]['created_at']} ({_by_id[i]['text'][:70]!r})"
    for i in NEW_IDS)
_inherited_desc = ", ".join(INHERITED_IDS)
_brand_desc = ", ".join(BRAND_NEW_IDS)""",
      """# the new posts' own details, from THIS cycle's own content fetch.
# ⭐ ON A MEASURED NO-OP THERE ARE NO NEW POSTS, SO THERE IS NO CONTENT TO
# FETCH -- and the fetch is not run.  ⭐ THE ABSENCE OF THE ARTEFACT IS
# NOT AN ERROR: the correct state for a NO-OP cycle is that no content
# fetch was performed, and the assertion below checks the branch.
if IS_NOOP:
    assert not (OUT / "translate/new_posts.json").exists(), (
        "a MEASURED NO-OP cycle must not carry a content-fetch artefact -- "
        "there was nothing to fetch")
    _np = {"rows": []}
    _by_id = {}
    _new_desc = ""
    print("[page] (NO-OP) no content fetch was performed -- there were no "
          "new posts to fetch")
else:
    _np = json.loads((OUT / "translate/new_posts.json")
                     .read_text(encoding="utf-8"))
    _by_id = {r["id"]: r for r in _np["rows"]}
    _new_desc = "; ".join(
        f"{i} @ {_by_id[i]['created_at']} ({_by_id[i]['text'][:70]!r})"
        for i in NEW_IDS)
_inherited_desc = ", ".join(INHERITED_IDS)
_brand_desc = ", ".join(BRAND_NEW_IDS)""",
      "the page's content fetch -> branch-symmetric")

# ══════════════════════════════════════════════════════════════════════
# 6. PAGE -- the head record (section 7)
# ══════════════════════════════════════════════════════════════════════
print("\n[6] PAGE -- the head record")

patch("page",
      """# the head record (the newest published post)
_head_rec = next(t for t in _tweets if t["id"] == HEAD_ID)
_HEAD_CST = _parse_created(_head_rec["created_at"]).astimezone(CST)
assert HEAD_ID in NEW_IDS, "the head must be one of the new posts\"""",
      """# the head record (the newest published post)
_head_rec = next(t for t in _tweets if t["id"] == HEAD_ID)
_HEAD_CST = _parse_created(_head_rec["created_at"]).astimezone(CST)
# ⭐ BRANCH-SYMMETRIC: on a SUBSTANTIVE cycle the head IS this cycle's
# published post; on a MEASURED NO-OP the head is the PRIOR cycle's, and
# the page quotes it as the corpus's current head -- which is exactly what
# the banner says ("頁面內容已更新至 <date>").
if not IS_NOOP:
    assert HEAD_ID in NEW_IDS, "the head must be one of the new posts\"""",
      "the page's head-record assertion -> branch-symmetric")

print("\n" + "=" * 78)
print("VERIFICATION")
print("=" * 78)

_pg = (REPO / f"_c{CYCLE}_page.py").read_text(encoding="utf-8")
assert "IS_NOOP = (len(NEW_IDS) == 0)" in _pg, (
    "page: the branch selector is missing")
assert "CYCLE_CLASS" in _pg, "page: the cycle class is not derived"
# ⭐ BOTH POLARITIES COUNT: the branch is applied as `if IS_NOOP:` on the
# NO-OP side and as `if not IS_NOOP:` / `else:` on the SUBSTANTIVE side.
# ⭐ A VERIFICATION THAT ONLY COUNTED ONE POLARITY WOULD ITSELF BE A
# SILENT ZERO ON THE OTHER -- the same family as "a selector that matches
# nothing may mean the query is wrong".
_n_if = _pg.count("if IS_NOOP:") + _pg.count("if not IS_NOOP:")
assert _n_if >= 5, (
    f"page: the NO-OP branch is applied at only {_n_if} site(s) -- the "
    "branch is not symmetric across the assertion sites")
print("  [VERIFIED] page: the branch selector is DERIVED from the "
      f"adjudication artefact, and the NO-OP branch is applied at "
      f"{_n_if} assertion site(s) (both polarities counted)")

print(f"\n[patch-noop] applied={applied} already={already}")
py_compile.compile(str(REPO / f"_c{CYCLE}_page.py"), doraise=True)
print("[patch-noop] page compiles")
print("[patch-noop] DONE")
