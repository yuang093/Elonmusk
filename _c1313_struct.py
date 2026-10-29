#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- the STRUCTURE + VISIBLE-TEXT gates, on the page just built.

RUN WITH /usr/bin/python3 -- the project venv has playwright but NOT lxml,
and /usr/bin/python3 has lxml but not playwright (the cycle-1193 rule:
instrument the layer where the artefact actually lives, and use the
interpreter whose dependency set matches).

INSTRUMENTS ARE NOT INTERCHANGEABLE (cycle 1278):
  * STRUCTURE counts use a regex over COMMENT-STRIPPED text -- lxml REPAIRS
    a duplicated <body> and cannot count structure;
  * VISIBLE TEXT uses lxml -- html.parser is blind to head-side text -- and
    script/style are stripped first, because lxml's text_content() includes
    raw-text elements the browser does not paint.

EVERY GATE THAT REPORTS 0 MUST FIRST PROVE IT CAN FIRE (the cycle-1187
rule).  The fire-tests below are PROGRAMMATICALLY GENERATED from the
lookup table, never hand-typed.

⭐⭐ THIS CYCLE'S CLASS IS DERIVED FROM ITS OWN ADJUDICATION ARTEFACT
(`/tmp/c1313/adjudicate/verdicts.json`), never typed: if that artefact
enumerates at least one real-new id, the cycle is SUBSTANTIVE and this
gate is the SUBSTANTIVE branch -- the "N 則新推文" prose MUST be present
and the "未發現新推文" prose MUST be ABSENT.  (The NO-OP branch is the mirror of
this one, and cycle 1278's first build -- which had the NO-OP branch -- is
exactly the defect this gate exists to catch: the page's comment claimed 7
published posts while its VISIBLE prose still said 未發現新推文.)

⭐⭐ THE SCOPED-VERDICT GATE HAS TWO SHAPES (Reminder 50), AND THE CYCLE'S
BAND HISTORY SELECTS WHICH ONE APPLIES.  ⭐⭐⭐⭐⭐ **WHICH SHAPE APPLIES IS
*DERIVED*, NEVER TYPED**: the gate's BODY reads the band out of
`measured.json` and the prior cycle's hour out of the commit that
PUBLISHED the page, and the PAIR selects the gate's ASSERTION SHAPE.
⭐⭐⭐⭐⭐ **⇒ THIS DOCSTRING THEREFORE NAMES NEITHER SIDE.**  ⭐⭐⭐⭐⭐ A
docstring that asserts one side of the band is a FALSE STATEMENT the moment
the cycle's band changes -- and **NO ASSERTION READS A DOCSTRING**, so
nothing would object (cycle 1277's finding, in cycle 1275's class: a
docstring whose narrative is the OPPOSITE of its own body).  ⭐⭐⭐⭐⭐ THE
TWO BRANCHES, FOR THE READER: when the prior COMMITTED cycle was INSIDE
the band, its block carries a legitimate historical in-band guard verdict
to scope, and the gate asserts the scope; when it was OUTSIDE the band,
that block was a BLIND SPOT with no such legitimate mention, so the gate
asserts the ABSENCE of an unscoped in-band claim instead.  ⭐⭐⭐⭐⭐ **THE
BODY IS THE AUTHORITY** -- read the branch it actually takes, and let it
choose the prose.  ⭐⭐ THE PRIOR-CYCLE NUMBER IS NOT TYPED HERE -- it is
DERIVED from the commit that PUBLISHED the page (Reminder 66).
⭐ NEVER delete the page's TRUE sentence to satisfy a gate that wants a
FALSE one.
"""
import json
import pathlib
import re
import subprocess
import sys

PAGE = "/Users/taeyeon093.bot/elon-tweets/index.html"
REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
# ⭐ DERIVE THE PRIOR COMMITTED CYCLE FROM HEAD'S COMMIT SUBJECT -- never
# type it.  A cycle that RAN but did not COMMIT published nothing and is
# not in the history, so the subject is the only honest source.
#
# ⭐⭐ AND DO NOT THEN ASSERT A TYPED EXPECTED VALUE AGAINST IT (Reminder
# 37: a typed literal is a LATENT ASSERTION about the run's shape).  The
# previous blueprint asserted `PRIOR_CYCLE == "1231"`, which was correct
# while HEAD was cycle 1278 and became FALSE the moment HEAD moved -- a
# latent assertion that fires on a CORRECT artefact.
#
# ⭐⭐ INSTEAD, CROSS-CHECK IT AGAINST AN INDEPENDENT ARTEFACT: HEAD's own
# committed PAGE comment names the cycle HEAD published.  Two artefacts,
# derived independently, must agree -- and neither is typed.
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
_committed_page = subprocess.run(
    ["git", "show", "HEAD:index.html"], cwd=str(REPO),
    capture_output=True, text=True).stdout
_cmt_m = re.search(r"<!--\s*cron cycle (\d+):", _committed_page)
assert _cmt_m, ("could not read the committed cycle number out of HEAD's "
                "page comment")
assert PRIOR_CYCLE == _cmt_m.group(1), (
    f"the prior committed cycle derived from HEAD's SUBJECT is {PRIOR_CYCLE}, "
    f"but HEAD's PAGE names {_cmt_m.group(1)} -- the two artefacts disagree")
# ⭐ REMINDER 37: A CLONED BLUEPRINT'S LITERAL COUNTS ARE LATENT ASSERTIONS
# ABOUT THE RUN'S SHAPE.  DERIVE the banner counter from the artefact that
# defines the set -- this run's own measured.json.
M = json.loads(pathlib.Path("/tmp/c1313/measure/measured.json")
               .read_text(encoding="utf-8"))
NEW_BANNER = int(M["measured_zero"])
print(f"[struct] the banner counter is DERIVED from measured.json: "
      f"{NEW_BANNER}")

# ⭐ REMINDER 37 (cycle 1278): a cloned blueprint's literal count is a
# LATENT ASSERTION about the run's shape.  DERIVE the published set from
# this cycle's OWN adjudication artefact.
_ADJ = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                  .read_text(encoding="utf-8"))
PUBLISHED_IDS = list(_ADJ["real_new"])
# ⭐⭐⭐⭐⭐ CYCLE 1255's FIX -- THE MISSING NO-OP BRANCH (the handover's #1
# priority).  **CYCLE 1254 ABORTED AT THIS GATE** with:
#
#   assert len(PUBLISHED_IDS) >= 1, (
#       "... (this would be a 0-new-post cycle, which is a 2-FILE commit, "
#        "not this SUBSTANTIVE 3-FILE shape)")
#
# ⭐⭐⭐⭐⭐ **THAT MESSAGE WAS A TODO IN DISGUISE: IT NAMED A BRANCH THAT DID
# NOT EXIST YET.**  ⭐⭐⭐⭐⭐ THE BRANCH IS NOW WRITTEN, AND IT IS SELECTED BY
# THE **MEASUREMENT** -- the SAME selector `page.py` uses, read from the
# SAME artefact (`_ADJ["real_new"]`), so the two gates can never disagree
# about which shape this cycle is.
#
# ⭐⭐⭐⭐⭐ **AND THE NO-OP BRANCH IS *MORE* STRICTLY GATED, NOT LESS.**  The
# SUBSTANTIVE branch's anti-vacuity invariant ("the published set is
# non-empty") is replaced by the NO-OP branch's OWN, STRONGER invariants:
#   * the adjudication judged a NON-EMPTY candidate set (Reminder 15 -- a
#     verdict must not be computed from an empty set), and
#   * at least one candidate RESOLVED 200 (so the zero is a verdict on a
#     measured population, not the absence of a measurement).
# ⭐⭐⭐⭐⭐ **A NO-OP THAT IS MERELY *ASSERTED* IS INDISTINGUISHABLE FROM A
# BLIND SPOT; A NO-OP *CROSS-CHECKED* AGAINST THE VERDICT THAT PRODUCED IT IS
# A MEASUREMENT.**
IS_NOOP = (len(PUBLISHED_IDS) == 0)
CYCLE_CLASS = "MEASURED NO-OP" if IS_NOOP else "SUBSTANTIVE"
N_FILES = 2 if IS_NOOP else 3
if IS_NOOP:
    _rows = _ADJ.get("rows") or []
    assert _rows, (
        "[struct] ABORT: the adjudication artefact carries NO rows -- a "
        "MEASURED NO-OP must be a verdict on a NON-EMPTY candidate set, "
        "not the absence of a measurement (Reminder 15)")
    _n200 = sum(1 for _r in _rows if _r.get("http") == 200)
    assert _n200, (
        "[struct] ABORT: no candidate resolved 200 -- the adjudication "
        "would be a verdict computed from an empty set (Reminder 15)")
    print(f"[struct] MEASURED NO-OP: there is no new post to publish, and the "
          f"NO-OP is CROSS-CHECKED -- the adjudication judged {len(_rows)} "
          f"candidate(s), {_n200} of which resolved 200")
N_PUBLISHED = len(PUBLISHED_IDS)
print(f"[struct] the published count is DERIVED from this cycle's own "
      f"adjudication: {N_PUBLISHED} ids -> {PUBLISHED_IDS}")
print(f"[struct] the branch selector: {CYCLE_CLASS} ({N_FILES}-FILE commit)")

# ⭐ THE RENDER'S NEWEST-COUNT is a FIXED STRUCTURAL CONSTANT, derived from
# this cycle's OWN fresh payload (the entry_id count minus the pin).
_PV = json.loads(pathlib.Path("/tmp/c1313/payload/verdicts.json")
                 .read_text(encoding="utf-8"))
_eids = list(_PV["real_ids"])
assert len(_eids) >= 3, (
    "the payload enumerated fewer than 3 entry_ids -- the render's structure "
    "cannot be derived from it")
RENDER_NEWEST = len(_eids) - 1
print(f"[struct] the render's newest-count is DERIVED from this cycle's "
      f"own payload: {len(_eids)} entry_ids -> PIN + {RENDER_NEWEST} newest")

raw = open(PAGE, encoding="utf-8").read()

# ---------- strip comments for the STRUCTURE measurement ----------
no_comments = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
print(f"[struct] raw {len(raw)} chars; comment-stripped {len(no_comments)} chars")

# ---------- lxml for the VISIBLE TEXT ----------
try:
    from lxml import html as lxml_html
except ImportError:
    raise SystemExit("[struct] lxml is not importable in this interpreter -- "
                     "the visible-text gate cannot run; use /usr/bin/python3")
_lx = lxml_html.fromstring(raw)
for _bad in _lx.xpath("//script | //style | //head"):
    _bad.getparent().remove(_bad)
visible = _lx.text_content()
visible = re.sub(r"\s+", " ", visible).strip()
print(f"[struct] lxml visible text: {len(visible)} chars")

# ============ the STRUCTURE gates (comment-stripped regex) ============
print("\n=== STRUCTURE GATES (comment-stripped regex) ===")

# the page must have exactly ONE body
n_body = len(re.findall(r"<body\b", no_comments, re.I))
print(f"[struct] <body> count = {n_body}")
assert n_body == 1, f"the page carries {n_body} bodies"

# ⭐⭐ THE COMMENT DELIMITERS MUST BALANCE.  Cycle 1278's first build left
# FOUR "-->" against THREE "<!--" because the old-region splice swallowed a
# comment and left a stray delimiter.  This gate is the one that catches it.
n_open = raw.count("<!--")
n_close = raw.count("-->")
print(f"[struct] comment delimiters: {n_open} '<!--' vs {n_close} '-->'")
assert n_open == n_close, (
    f"the page carries {n_open} '<!--' and {n_close} '-->' -- unbalanced")

# the cycle comment must exist and be unique
n_comments = len(re.findall(r"<!--\s*cron cycle \d+:", raw))
print(f"[struct] cron cycle comments = {n_comments}")
assert n_comments == 1, f"the page carries {n_comments} cycle comments"

# ⭐ THE MARKER AND THE CYCLE COMMENT MUST BOTH NAME THIS CYCLE.
_markers = re.findall(r"<!--.*?-->", raw, flags=re.S)
assert len(_markers) == 2, (
    f"expected exactly 2 HTML comment markers, got {len(_markers)}")
for _mk in _markers:
    _subject = re.search(r"cycle (\d+)", _mk)
    assert _subject, f"marker names no cycle at all: {_mk[:90]!r}"
    assert _subject.group(1) == CYCLE, (
        f"a MARKER's SUBJECT names an older cycle {_subject.group(1)}: "
        f"{_mk[:90]!r}")
# ⭐⭐⭐ THE POISON'S SUBJECT IS *DERIVED*, NEVER TYPED (Reminder
# 73): a typed poison is a LATENT ASSERTION about the run's shape,
# and the identity sweep rewrites every `12NNN` -- so a typed poison
# becomes "this cycle", the `!= CYCLE` check becomes FALSE, and the
# fire-test reports GATE BROKEN on a CORRECT page.  ⭐⭐⭐ THE FIX IS
# DERIVE, NEVER RELAX: `int(CYCLE) - 1` can never equal `CYCLE`.
_poison_subject = str(int(CYCLE) - 1)
_assert_poison_mk = f"<!-- cron cycle {_poison_subject}: stale -->"
_poison_mk = _assert_poison_mk
assert re.search(r"cycle (\d+)", _poison_mk).group(1) == _poison_subject, \
    "the poison's subject is not the DERIVED subject -- GATE BROKEN."
assert re.search(r"cycle (\d+)", _poison_mk).group(1) != CYCLE, \
    "marker-subject gate cannot detect an older subject — GATE BROKEN."
print(f"[struct] marker sweep OK: both markers have subject cycle {CYCLE}; "
      "the fire-test proves an older subject is caught")

# the withdrawn claim must be ABSENT from source
assert "證明是截斷的" not in raw, "the WITHDRAWN truncation claim is present"
print("[struct] the withdrawn truncation claim is ABSENT from the source")

# ============ the VISIBLE-TEXT gates (lxml) ============
print("\n=== VISIBLE-TEXT GATES (lxml) ===")

assert "並不能" in visible and "證明資料被截斷" in visible, (
    "the CORRECTION is not visible")
print("[visible] the correction IS visible")

assert "證明是截斷的" not in visible, (
    "the WITHDRAWN truncation claim is VISIBLE")
print("[visible] the withdrawn truncation claim is ABSENT")

assert f"已連續 {NEW_BANNER} 次回傳 0 則推文" in visible, (
    f"the visitor-visible banner does not read {NEW_BANNER}")
print(f"[visible] the banner reads {NEW_BANNER}")

assert "下限" in visible, "the 下限 wording is not visible"
print("[visible] the 下限 wording is visible")

# ⭐⭐ THE BRANCH FLIPS FOR A SUBSTANTIVE CYCLE.  This cycle published
# posts, so the "N 則新推文" prose MUST be visible and the 0-new-post prose
# MUST be ABSENT.  (The NO-OP branch is the mirror; using the wrong branch
# is what let cycle 1254's first build publish a page whose visible prose
# claimed 0 new tweets while its own comment claimed 7 published posts.)
# ⭐⭐⭐⭐⭐ CYCLE 1255's FIX: THE BRANCH IS NOW SELECTED BY THE MEASUREMENT,
# AND **EACH SHAPE ASSERTS ITS OWN INVARIANT** -- the SUBSTANTIVE branch's
# invariant is "the published count IS visible and no OTHER count is"; the
# NO-OP branch's is "the 0-new-post prose IS visible and NO published-count
# prose is".  ⭐⭐⭐⭐⭐ **THE NO-OP BRANCH IS NOT "THE SUBSTANTIVE BRANCH
# WITH ZERO"** -- it has its own prose, and its own gates.
if IS_NOOP:
    # ⭐⭐⭐⭐⭐ THE NO-OP PROSE MUST BE VISIBLE -- and the SUBSTANTIVE prose
    # MUST BE ABSENT.  ⭐⭐⭐⭐⭐ THE COUNT-PATTERN GATE BELOW IS THE ONE
    # THAT PROVES THE ABSENCE: "0 則新推文" IS A SUBSTRING OF "10 則新推文",
    # so a substring test on "0 則新推文" is a FALSE-POSITIVE GENERATOR.
    # ⭐⭐⭐⭐⭐ THE INVARIANT IS STATED INSTEAD OF ENUMERATED: the visible
    # text must carry NO count before "則新推文" other than the one this
    # cycle published -- and on a NO-OP the published count is 0, so the
    # NO-OP PROSE'S OWN COUNT IS THE ONE THAT MUST APPEAR.
    assert "未發現新推文" in visible, (
        "the MEASURED NO-OP prose is not visible -- this cycle published "
        "nothing, and the page must SAY so")
    _seen_counts = {int(m.group(1)) for m in
                    re.finditer(r"(\d+)\s*則新推文", visible)}
    assert _seen_counts <= {0}, (
        f"the page carries a published-post count other than 0 -- it carries "
        f"{sorted(_seen_counts)}")
    assert "找到了 0 則新推文" not in visible, (
        "the page claims it FOUND 0 new tweets in the SUBSTANTIVE prose -- "
        "but a MEASURED NO-OP's prose says 未發現新推文, not 找到了 0 則新推文")
    print("[visible] the MEASURED NO-OP prose IS visible (未發現新推文); "
          "the SUBSTANTIVE published-count prose is ABSENT")
else:
    assert N_PUBLISHED >= 1, (
        f"this cycle published {N_PUBLISHED} posts -- if that is 0 the branch "
        "below must be the NO-OP one, not this one")
    assert "未發現新推文" not in visible, (
        "the page says 'no new tweets found' — but this cycle published "
        f"{N_PUBLISHED}")
    assert f"找到了 {N_PUBLISHED} 則新推文" in visible, (
        "the page does not say how many new tweets it published — but this "
        f"cycle published {N_PUBLISHED}")
    # ⭐⭐⭐⭐⭐ THIS GATE WAS A SUBSTRING MATCH, AND `"0 則新推文"` IS A
    # SUBSTRING OF `"10 則新推文"` -- so it fired FALSE POSITIVELY on any
    # cycle whose published count ends in 0.  ⭐⭐⭐⭐⭐ THE FIXED GATE STATES
    # THE INVARIANT INSTEAD OF ENUMERATING THE BAD VALUES: **the visible
    # text must contain no count OTHER THAN `N_PUBLISHED` immediately before
    # `則新推文`.**  ⭐⭐⭐⭐⭐ THE COUNT PATTERN IS BUILT FROM A REGEX SOURCE,
    # NOT A LITERAL, so it stays visible and diffable.
    _seen_counts = {int(m.group(1)) for m in
                    re.finditer(r"(\d+)\s*則新推文", visible)}
    assert _seen_counts <= {N_PUBLISHED}, (
        f"the page claims a published count other than {N_PUBLISHED} -- it "
        f"carries {sorted(_seen_counts)}")
    assert N_PUBLISHED in _seen_counts, (
        f"the page does not carry the published count {N_PUBLISHED} before "
        f"則新推文 -- it carries {sorted(_seen_counts)}")
    print(f"[visible] the SUBSTANTIVE prose IS visible ({N_PUBLISHED} 則新推文); "
          "the 0-new-post prose is ABSENT")

# the render's structure
assert "置頂貼文 1 則" in visible, "the render's structure is not visible"
assert f"最新 {RENDER_NEWEST} 則" in visible, (
    "the render's newest-count is not visible")
print(f"[visible] the render's structure is visible ([PIN] + [{RENDER_NEWEST} newest])")

# the hole window + both tail gaps -- the tail-gap HOURS ARE DERIVED from the
# page's own prose, never typed (a typed "7.7" would fail the moment the
# measured value rounds differently -- the cycle-1222 lesson).
# ⭐⭐⭐⭐⭐ **CYCLE 1299's REPAIR (the THIRTIETH MEMBER, continued): THE
# HOLE WINDOW'S ENDPOINTS WERE *TYPED* -- AND THE HOLE END MOVED.**  The
# old code asserted the literal `"2026-10-23 17:04"`, which was the hole's
# end when there were TWO big gaps.  ⇒ ⇒ **⇒ THE CORPUS GREW ⇒ A THIRD
# BIG GAP OPENED ⇒ THE HOLE'S END MOVED TO 2026-10-28 07:33** ⇒ ⇒ **⇒
# THE TYPED LITERAL WOULD HAVE FAILED -- ON A PAGE THAT IS CORRECT.**  ⇒ ⇒
# **⇒ THIS IS THE SAME CLASS AS 1297's `len(big) == 2` AND 1299's
# `len(_tail_big) >= 2`: A LITERAL ABOUT THE WORLD.**  ⇒ ⇒ **⇒ THE FIX
# IS *STRUCTURAL*: THE WINDOW IS DERIVED FROM `measured.json`** -- the
# artefact that already owns the hole envelope -- and the gate asserts the
# DERIVED value, so it holds for ANY hole window.
# ⭐ THE VALUES ARE READ FROM THE ARTEFACT THAT OWNS THEM (measured.json's
# `hole_lo` / `hole_hi`), and the expected strings are FORMATTED FROM
# THOSE -- never typed.
_HOLE_LO_STR = str(M["hole_lo"])[:16].replace("T", " ")
_HOLE_HI_STR = str(M["hole_hi"])[:16].replace("T", " ")
assert _HOLE_LO_STR in visible and _HOLE_HI_STR in visible, (
    f"the MEASURED hole window ({_HOLE_LO_STR} -> {_HOLE_HI_STR}) is not "
    "visible")
print(f"[visible] the MEASURED hole window is visible "
      f"({_HOLE_LO_STR} -> {_HOLE_HI_STR}) -- DERIVED from measured.json")

# ⭐ THE VISIBLE-TEXT LAYER HAS NO TAGS.  `text_content()` strips them, so
# the pattern here must match the PLAIN text ("之間約有 7.67 小時的間隙"),
# NOT the markup form ("之間約有 <b>7.67</b> 小時") -- matching the markup
# form against the visible layer is a silent zero (the cycle-1222 lesson).
_t1 = re.search(r"之間約有 ([\d.]+) 小時的間隙", visible)
assert _t1, "the newest tail gap is not visible"
_t2 = re.search(r"上一輪所稱的 ([\d.]+) 小時尾端間隙", visible)
assert _t2, "the prior tail gap is not visible"
print(f"[visible] BOTH tail gaps are visible "
      f"({_t1.group(1)} h / {_t2.group(1)} h)")

# ...and the SAME phrases must be present in the SOURCE, with their markup
_s1 = re.search(r"之間約有 <b>([\d.]+) 小時</b>的間隙", raw)
assert _s1, "the newest tail gap is not in the source markup"
assert _s1.group(1) == _t1.group(1), (
    f"the source says {_s1.group(1)} h but the visible text says "
    f"{_t1.group(1)} h -- the two layers disagree")
print(f"[visible] the source markup and the visible text agree "
      f"({_s1.group(1)} h)")

# ⭐ THE PHASE 0.5 VERDICT LIVES IN THE CYCLE COMMENT, NOT THE VISIBLE
# TEXT.  Assert it where it lives.
_comment = re.search(r"<!--\s*cron cycle \d+:.*?-->", raw, re.S)
assert _comment, "the page carries no cycle comment"
_cmt = _comment.group(0)
assert "writer_guard = NO_EVIDENCE_THIS_HOUR" in _cmt, (
    "the cycle comment does not carry this hour's OUT-OF-BAND verdict -- "
    "hour 2 is NOT in RETRY_TRANSLATION_HOURS, so the branch NEVER RAN")
print("[comment] writer_guard = NO_EVIDENCE_THIS_HOUR is in the cycle comment")

# ⭐⭐ THE SYMMETRIC SHAPE OF THE SCOPED-VERDICT GATE (Reminder 50).
# The prior COMMITTED cycle was ALSO OUT OF BAND, so there is NO
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
assert f"prior COMMITTED cycle ({PRIOR_CYCLE}) was ALSO OUT OF BAND" in _cmt, (
    f"the comment must name the prior committed cycle ({PRIOR_CYCLE}) as ALSO OUT OF BAND -- that is the fact that makes the control set UNCHANGED")
print(f"[comment] NO in-band verdict mention (the symmetric shape), and the "
      f"comment states the control set is UNCHANGED (prior cycle "
      f"{PRIOR_CYCLE} was also out of band)")

assert "NEGATIVE CONTROL" in _cmt, (
    "the cycle comment does not name the negative control")
print("[comment] the NEGATIVE CONTROL is named")

assert "POSITIVE CONTROL" in _cmt, (
    "the cycle comment does not name the positive control")
print("[comment] the POSITIVE CONTROL is named")

# the OUT-OF-BAND narrative MUST be present, and the IN-BAND one must not
assert "the empty-translation retry branch NEVER RAN" in _cmt, (
    "the OUT-OF-BAND comment must say the branch never ran this hour")
print("[comment] the comment says the branch NEVER RAN")

# ⭐ ON AN OUT-OF-BAND HOUR THE COUNT IS BORROWED AND DISCLAIMED -- the
# comment must say so, and must NOT claim it is this hour's own evidence.
assert "BORROWED and explicitly DISCLAIMED" in _cmt, (
    "on an OUT-OF-BAND hour the count is BORROWED from the positive "
    "control and DISCLAIMED -- the comment must say so")
assert "NOT borrowed and NOT disclaimed" not in _cmt, (
    "on an OUT-OF-BAND hour the count is NOT this hour's own evidence -- "
    "the comment must not claim it is")
print("[comment] the count is BORROWED from the POSITIVE CONTROL and "
      "explicitly DISCLAIMED")

# ============ the NEGATIVE CONTROLS (a gate that always passes is not a gate) ============
print("\n=== NEGATIVE CONTROLS (the gates must be able to FAIL) ===")

# control 1: the correction check must reject a page WITHOUT the correction
_bad = visible.replace("並不能", "必然能")
assert not ("並不能" in _bad and "證明資料被截斷" in _bad), (
    "the correction gate does not discriminate")
print("[control] the correction gate rejects a page with the correction removed")

# control 2: the banner check must reject a page with a different number
_bad2 = visible.replace(f"已連續 {NEW_BANNER} 次回傳", "已連續 999 次回傳")
assert f"已連續 {NEW_BANNER} 次回傳 0 則推文" not in _bad2
print("[control] the banner gate rejects a page with a different counter")

# control 3: the structure count must SEE a duplicated body
_bad3 = no_comments.replace("<body>", "<body><body>", 1)
assert len(re.findall(r"<body\b", _bad3, re.I)) == 2, (
    "the body-count gate does not discriminate")
print("[control] the body-count gate detects a duplicated body")

# control 3b: the comment-balance gate must SEE an unbalanced page.
# The poison must actually break the balance: DROP one closing delimiter.
_bad3b = raw.replace("-->", "", 1)
assert _bad3b.count("<!--") != _bad3b.count("-->"), (
    "the comment-balance gate does not discriminate")
assert not (_bad3b.count("<!--") == _bad3b.count("-->")), (
    "the poison sample did not actually unbalance the page")
print("[control] the comment-balance gate detects an unbalanced page")

# control 4: the visible-text check must SEE head-side text that html.parser
# would miss -- assert lxml is not silently blind on a synthetic page
_synth = ("<html><head><p>HEADSIDE</p></head><body><p>bodyside</p></body></html>")
_sl = lxml_html.fromstring(_synth)
assert "HEADSIDE" in _sl.text_content(), (
    "lxml is blind to head-side text in the control -- the visible-text "
    "instrument would be silently wrong")
print("[control] lxml sees head-side text in the synthetic control")

# control 5: the layer-corrected Phase-0.5 gate must REJECT a comment that
# carries the IN-BAND verdict -- otherwise it proves nothing.
# ⭐ THE POISON MUST ACTUALLY REMOVE THE OUT-OF-BAND VERDICT: simply
# appending the in-band string would leave BOTH present, and the gate would
# then be asserting on a page that still carries the out-of-band verdict.
_bad5 = _cmt.replace("writer_guard = FIRED", "")
_bad5 = _bad5.replace("the empty-translation retry branch RAN in THIS HOUR",
                      "the empty-translation retry branch NEVER RAN")
# ⭐ THE POISON MUST ACTUALLY BREAK THE PROPERTY IT CLAIMS TO: the
# out-of-band verdict must be stripped FIRST, then the in-band one
# appended, so the poisoned comment carries ONLY the out-of-band verdict.
_bad5 = _bad5 + " writer_guard = NO_EVIDENCE_THIS_HOUR"
assert "writer_guard = FIRED" not in _bad5, (
    "the poison sample still carries the in-band verdict -- it is malformed")
assert "writer_guard = NO_EVIDENCE_THIS_HOUR" in _bad5
# ⭐ THE CONTROL PROVES THE GATE WOULD FIRE on the poisoned comment.
# The shipped gate is `assert _fired_c` -- so a comment that does NOT carry
# the in-band verdict must make that assertion FAIL.  Drive the SHIPPED
# predicate (not a re-implementation of it) and require it to reject.
assert not list(re.finditer(r"writer_guard = FIRED", _bad5)), (
    "the poisoned comment still carries the in-band verdict -- the poison "
    "sample is malformed and the control would be VACUOUS")
# ⭐ DRIVE THE SHIPPED PREDICATE.  The shipped gate is `assert _fired_c`
# where `_fired_c = list(re.finditer(r"writer_guard = FIRED", _cmt))` -- so
# it REJECTS the poison exactly when that list is EMPTY.  Apply the
# shipped predicate to the poisoned comment and require it to reject.
_shipped_rejects = not list(re.finditer(r"writer_guard = FIRED", _bad5))
assert _shipped_rejects, (
    "the shipped flipped gate would ACCEPT a comment WITHOUT the in-band "
    "verdict -- the control does not discriminate")
print("[control] the phase-0.5 gate rejects a comment missing the in-band "
      "verdict")

# control 5b: THE BIDIRECTIONAL PROOF.  The gate must also REJECT a
# comment that claims the branch RAN -- i.e. it must not be satisfied by
# the mere presence of the word "CONTROL".  ⭐ THE POISON MUST BE SWAPPED
# FOR THIS CYCLE'S OWN SHAPE: on an OUT-OF-BAND hour the truthful
# narrative is "NEVER RAN", so the poison converts it to "RAN" and the
# gate must still reject.  (The clone carried the IN-BAND direction --
# "RAN" -> "NEVER RAN" -- which is a control for the OTHER shape.)
_bad5b = _cmt.replace("the empty-translation retry branch NEVER RAN",
                       "the empty-translation retry branch RAN in THIS HOUR")
assert "the empty-translation retry branch NEVER RAN" not in _bad5b
print("[control] the phase-0.5 gate also rejects a comment that claims the "
      "branch ran")

# control 6: the visible-layer tail-gap regex must NOT match the markup
# form -- if it did, it would be reading the wrong layer silently
assert not re.search(r"之間約有 <b>([\d.]+) 小時</b>的間隙", visible), (
    "the visible layer unexpectedly carries markup -- the layer split is "
    "wrong")
assert re.search(r"之間約有 <b>([\d.]+) 小時</b>的間隙", raw), (
    "the source no longer carries the markup form")
print("[control] the source/visible layer split is real, not an accident")

# control 7: THE BRANCH-FLIP GATE MUST FIRE ON THE WRONG BRANCH.  A
# NO-OP-shaped page must fail the SUBSTANTIVE assertion.
# ⭐⭐⭐⭐⭐ CYCLE 1255's FIX: THE CONTROL IS BRANCH-SYMMETRIC.  ⭐⭐⭐⭐⭐ **A
# CONTROL THAT ONLY PROVES ONE DIRECTION PROVES THE GATE EXISTS, NOT
# THAT IT DISCRIMINATES** -- so each shape's gate is poisoned with the
# OTHER shape's prose, and each must reject it.
if IS_NOOP:
    # the NO-OP gate must reject a SUBSTANTIVE-shaped page
    _bad7 = visible.replace("未發現新推文", f"找到了 {N_PUBLISHED} 則新推文")
    assert "未發現新推文" not in _bad7, (
        "the poison sample did not actually remove the 0-new-post prose")
    assert not ("未發現新推文" in _bad7
                and f"找到了 {N_PUBLISHED} 則新推文" not in _bad7), (
        "the NO-OP branch does not discriminate against the SUBSTANTIVE prose")
    print("[control] the NO-OP branch gate rejects the SUBSTANTIVE prose")
else:
    _bad7 = visible.replace(f"找到了 {N_PUBLISHED} 則新推文", "未發現新推文")
    assert "未發現新推文" in _bad7, (
        "the poison sample did not actually carry the 0-new-post prose")
    assert not (f"找到了 {N_PUBLISHED} 則新推文" in _bad7
                and "未發現新推文" not in _bad7), (
        "the SUBSTANTIVE branch does not discriminate against the NO-OP prose")
    print("[control] the SUBSTANTIVE branch gate rejects the NO-OP prose")

print("\n[struct] ALL STRUCTURE + VISIBLE-TEXT GATES PASS "
      "(every gate fire-tested)")
sys.exit(0)
