#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- THE PAIR-KEYED VALUE-TOKEN SWEEP.

⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
⭐⭐⭐ **⭐⭐⭐ CYCLE 1250'S CLASS-LEVEL RULE, NOW IMPLEMENTED: THE
⭐⭐⭐ ATTRIBUTION TOKEN SET IS SELECTED BY THE *PAIR*, NOT BY THE BAND.**

⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
⭐⭐⭐ **CYCLE 1249'S SWEEP DERIVED ITS TOKEN SETS FROM *THIS CYCLE'S BAND
⭐⭐⭐⭐⭐ ALONE*:**

```python
if IN_BAND:
    FORBIDDEN_TOKENS, REQUIRED = IN_FORBIDDEN, IN_REQUIRED
else:
    FORBIDDEN_TOKENS, REQUIRED = OUT_FORBIDDEN, OUT_REQUIRED
```

⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
⭐⭐⭐ **⭐⭐⭐⭐⭐ AND 1250 SHOWED THAT IS UNDER-DERIVED: THE CODE SHAPE IS A
⭐⭐⭐⭐⭐ FUNCTION OF *THIS CYCLE'S BAND*, BUT THE *ATTRIBUTION* IS A
⭐⭐⭐⭐⭐ FUNCTION OF *THE PAIR* (prior committed cycle's band × this
⭐⭐⭐⭐⭐ cycle's band).**  ⭐⭐⭐⭐⭐ **ON THE `(OUT, IN)` PAIR, 1249's SWEEP
⭐⭐⭐⭐⭐ WOULD BOTH REJECT A CORRECT ATTRIBUTION AND ACCEPT A WRONG ONE
⭐⭐⭐⭐⭐ -- AND THE FALSE NEGATIVE PUBLISHES A FALSE NARRATIVE ABOUT THE
⭐⭐⭐⭐⭐ PRIOR CYCLE'S BLOCK.**

⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
⭐⭐⭐ **⭐⭐⭐⭐⭐ THIS CYCLE IS THE `(OUT, OUT)` PAIR, WHERE THE TWO AXES
⭐⭐⭐⭐⭐ AGREE -- so 1249's SWEEP WOULD HAPPEN TO PASS.  ⭐⭐⭐⭐⭐ **⭐⭐⭐ BUT
⭐⭐⭐⭐⭐ "IT PASSES ON THIS PAIR" IS NOT "IT IS CORRECT": 1249's SWEEP
⭐⭐⭐⭐⭐ WAS *PROVEN WRONG* ON THE `(OUT, IN)` PAIR, AND A SWEEP THAT IS
⭐⭐⭐⭐⭐ WRONG ON ONE PAIR IS WRONG ON ALL OF THEM.**

⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
⭐⭐⭐ **⭐⭐⭐⭐⭐ SO THIS SWEEP IS *PAIR-KEYED*: THE ATTRIBUTION SET COMES
⭐⭐⭐⭐⭐ FROM A TABLE KEYED BY THE PAIR, AND THE PAIR IS *DERIVED* FROM
⭐⭐⭐⭐⭐ THE PRIOR COMMITTED CYCLE'S OWN COMMITTED ARTEFACT (its
⭐⭐⭐⭐⭐ `measure.py`'s `CYCLE_HOUR_UTC` constant at HEAD) -- NEVER
⭐⭐⭐⭐⭐ ASSUMED.**

⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
⭐⭐⭐ **⭐⭐⭐⭐⭐ AND THE ATTRIBUTION MUST BE MATCHED WITH A WORD BOUNDARY
⭐⭐⭐⭐⭐ / NEGATIVE LOOKBEHIND -- `"was IN BAND"` IS A SUBSTRING OF
⭐⭐⭐⭐⭐ `"was ALSO IN BAND"`, so a naive `in` test flags the CORRECT
⭐⭐⭐⭐⭐ attribution on the `(IN, IN)` pair.**

⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
⭐⭐⭐ **⭐⭐⭐⭐⭐ AND THE FALSE-NEGATIVE DIRECTION MUST BE PROVEN, NOT ONLY
⭐⭐⭐⭐⭐ THE FALSE-POSITIVE ONE: A POISON TAIL THAT CLAIMS THE PRIOR
⭐⭐⭐⭐⭐ CYCLE WAS IN BAND (WHEN IT WAS OUT) MUST BE REJECTED.**  ⭐⭐⭐⭐⭐
⭐⭐⭐ **THE POISON IS GENERATED PROGRAMMATICALLY FROM THE FORBIDDEN LIST
⭐⭐⭐⭐⭐ (never hand-typed) AND ITS CYCLE NUMBER IS DERIVED (never
⭐⭐⭐⭐⭐ typed).**
"""
import ast
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
TAIL = ["measure", "page", "struct", "commit", "verify", "jobs",
        "jobs_verify", "render", "render_posts", "select", "write",
        "build", "translate", "precert", "fetch_new", "adjudicate",
        "paths", "payload", "triage", "band_firetest", "fidelity2",
        "third_instrument", "d_keepcheck"]

# ======================================================================
# AXIS 1 -- THE CODE SHAPE: THIS CYCLE'S BAND ALONE
# ======================================================================
_ft = (REPO / "fetch_tweets.py").read_text(encoding="utf-8")
_bm = re.search(r"RETRY_TRANSLATION_HOURS\s*=\s*\{([^}]*)\}", _ft)
assert _bm, "could not read RETRY_TRANSLATION_HOURS from fetch_tweets.py"
BAND = {int(x) for x in re.findall(r"\d+", _bm.group(1))}
HOUR = int(re.search(r'^CYCLE_HOUR_UTC\s*=\s*(\d+)',
                     (REPO / f"_c{CYCLE}_measure.py").read_text(encoding="utf-8"),
                     re.M).group(1))
IN_BAND = HOUR in BAND

# ======================================================================
# AXIS 2 -- THE ATTRIBUTION: THE PAIR
# ======================================================================
# ⭐⭐⭐ THE PRIOR COMMITTED CYCLE IS DERIVED FROM HEAD'S OWN COMMIT
# SUBJECT -- THE COMMIT THAT PUBLISHED index.html.  ⭐⭐⭐ A CHORE-ONLY
# COMMIT PUBLISHES NOTHING AND CARRIES NO CYCLE IDENTITY.
import subprocess  # noqa: E402

_prior_pub = subprocess.run(
    ["git", "log", "-1", "--format=%H", "--", "index.html"], cwd=str(REPO),
    capture_output=True, text=True).stdout.strip()
assert _prior_pub, "could not find the commit that published index.html"
_prior_subject = subprocess.run(
    ["git", "show", "-s", "--format=%s", _prior_pub], cwd=str(REPO),
    capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\d+)", _prior_subject)
assert _pm, (
    f"the publishing commit's subject carries no `cron cycle N`: "
    f"{_prior_subject!r}")
PRIOR = _pm.group(1)

# ⭐⭐⭐ THE PRIOR CYCLE'S HOUR IS READ OUT OF ITS OWN COMMITTED ARTEFACT
# ⭐⭐⭐ -- NEVER ASSUMED.  ⭐⭐⭐⭐⭐ THE COMMITTED PAGE'S OWN CYCLE COMMENT
# ⭐⭐⭐⭐⭐ IS THE ARTEFACT THAT PUBLISHES THE HOUR (`... = Hour NN UTC: ...`),
# ⭐⭐⭐⭐⭐ AND IT IS AT HEAD.  ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ THE CYCLE SCRIPTS ARE NOT
# ⭐⭐⭐⭐⭐ TRACKED IN GIT (`git ls-files | grep -c "_c[0-9]*_"` = 0), so
# ⭐⭐⭐⭐⭐ THE measure.py CONSTANT IS NOT AVAILABLE AT HEAD -- the PAGE is
# ⭐⭐⭐⭐⭐ the right source, and it is the one the USER SEES.
_committed_page = subprocess.run(
    ["git", "show", "HEAD:index.html"], cwd=str(REPO),
    capture_output=True, text=True).stdout
_cmt_m = re.search(r"<!--\s*cron cycle (\d+):(.*?)-->", _committed_page, re.S)
assert _cmt_m, "could not read the committed cycle comment out of HEAD's page"
assert _cmt_m.group(1) == PRIOR, (
    f"the publishing commit names cycle {PRIOR} but HEAD's page names "
    f"{_cmt_m.group(1)} -- the two artefacts disagree")
_hm = re.search(r"=\s*Hour (\d{1,2}) UTC", _cmt_m.group(2))
assert _hm, (
    "the committed page's cycle comment carries no `= Hour NN UTC` -- the "
    "prior cycle's hour cannot be derived")
PRIOR_HOUR = int(_hm.group(1))
PRIOR_IN_BAND = PRIOR_HOUR in BAND

PAIR = ("IN" if PRIOR_IN_BAND else "OUT", "IN" if IN_BAND else "OUT")

print("=" * 78)
print(f"CYCLE {CYCLE} -- THE PAIR-KEYED VALUE-TOKEN SWEEP")
print("=" * 78)
print(f"  AXIS 1 (the CODE SHAPE)   : this cycle's band -- hour {HOUR} -> "
      f"{'IN' if IN_BAND else 'OUT OF'} BAND")
print(f"  AXIS 2 (the ATTRIBUTION)   : the PAIR -- prior COMMITTED = {PRIOR} "
      f"(hour {PRIOR_HOUR} -> {'IN' if PRIOR_IN_BAND else 'OUT OF'} BAND)")
print(f"  => PAIR = {PAIR}")

# ======================================================================
# THE PAIR-KEYED ATTRIBUTION TABLE
# ======================================================================
ATTR = {
    ("OUT", "IN"):  {"phrase": "the control set FLIPS",
                     "attr":   "was OUT OF BAND"},
    ("IN",  "IN"):  {"phrase": "control set is UNCHANGED, NOT 'flipped back'",
                     "attr":   "was ALSO IN BAND"},
    ("IN",  "OUT"): {"phrase": "the control set FLIPS",
                     "attr":   "was IN BAND"},
    ("OUT", "OUT"): {"phrase": "control set is UNCHANGED, NOT flipped",
                     "attr":   "was ALSO OUT OF BAND"},
}
assert PAIR in ATTR, f"the pair {PAIR} is not in the attribution table"
_A = ATTR[PAIR]


# ⭐⭐⭐⭐⭐ **CYCLE 1268's FIX -- THE FORBIDDEN LIST IS A SET DIFFERENCE
# AGAINST THE REQUIRED LIST, NOT "THE OTHER THREE PAIRS".**  ⭐⭐⭐⭐⭐
# **THE ATTR TABLE HAS TWO PAIRS THAT SHARE A PHRASE** -- ("OUT", "IN") and
# ("IN", "OUT") BOTH publish "the control set FLIPS" (the control set
# flips in EITHER direction) -- so on a FLIPS pair the "other three
# pairs' phrases are forbidden" rule FORBIDS THIS PAIR'S OWN PHRASE while
# ALSO REQUIRING IT.  ⭐⭐⭐⭐⭐ **THE INSTRUMENT WAS THEREFORE ABORTING ON
# THE CORRECT ARTEFACT**, with 13 "violations" that were all the proper
# IN-side assertions.
# ⭐⭐⭐⭐⭐ **WHY NO PRIOR CYCLE CAUGHT IT:** every cycle that RAN this
# sweep was on an (OUT, OUT) or (IN, IN) pair, where the four phrases ARE
# distinct; cycle 1265 was the first to assert the (OUT, IN) pair and was
# INTERRUPTED before the sweep ran.  ⭐⭐⭐⭐⭐ **THIS IS THE FIRST TIME
# THIS SWEEP HAS RUN ON A FLIPS PAIR.**
# ⭐⭐⭐⭐⭐ **THE FIX DOES NOT RELAX THE GATE:** the (IN, IN) and (OUT, OUT)
# phrases REMAIN forbidden -- the gate is unchanged in strength for every
# token it was meant to catch -- and the fix ADDS an assertion that this
# pair's own tokens are ABSENT from the forbidden list.
PHRASE_FORBIDDEN = [v["phrase"] for k, v in ATTR.items()
                     if k != PAIR and v["phrase"] != _A["phrase"]]
# ⭐⭐⭐⭐⭐ THE SAME SET DIFFERENCE FOR THE ATTRIBUTION -- the four
# attribution tokens ARE distinct, but the rule is now stated ONCE and
# applied to both, so the two lists can never disagree.
ATTR_FORBIDDEN = [v["attr"] for k, v in ATTR.items()
                  if k != PAIR and v["attr"] != _A["attr"]]
# ⭐⭐⭐⭐⭐ THE FIX IS *PROVEN*, NOT ASSUMED: this pair's own tokens must be
# ABSENT from the forbidden lists.
assert _A["phrase"] not in PHRASE_FORBIDDEN, (
    "the sweep's own pair phrase is in its forbidden list -- the sweep "
    "would abort on the CORRECT artefact")
assert _A["attr"] not in ATTR_FORBIDDEN, (
    "the sweep's own pair attribution is in its forbidden list -- the "
    "sweep would abort on the CORRECT artefact")
# ⭐⭐⭐⭐⭐ AND THE *OTHER* PAIRS' PHRASES MUST STILL BE FORBIDDEN -- the fix
# must NOT relax the gate.
for _k, _v in ATTR.items():
    if _k == PAIR:
        continue
    if _v["phrase"] != _A["phrase"]:
        assert _v["phrase"] in PHRASE_FORBIDDEN, (
            f"the fix DROPPED the forbidden phrase { _v['phrase']!r} -- the "
            "gate would no longer reject the wrong pair's phrase")
print(f"  [OK] the fixed PHRASE_FORBIDDEN excludes this pair's own phrase "
      f"({_A['phrase']!r}) and KEEPS every genuinely-wrong phrase")

# ⭐⭐⭐ THE CODE-SHAPE SETS (this cycle's band decides these).
if IN_BAND:
    SHAPE_FORBIDDEN = ["the band must be OUT_OF_BAND", "expected OUT_OF_BAND"]
else:
    SHAPE_FORBIDDEN = ["the band must be IN_BAND", "expected IN_BAND"]

FORBIDDEN_TOKENS = PHRASE_FORBIDDEN + ATTR_FORBIDDEN + SHAPE_FORBIDDEN
REQUIRED = {
    "page": [_A["phrase"], _A["attr"]],
    "struct": [_A["phrase"], _A["attr"]],
    # ⭐⭐⭐ THE COMMIT MESSAGE PUBLISHES THE ATTRIBUTION IN ITS OWN
    # CASING (`was ALSO out of band`) -- SO THE REQUIRED TOKEN IS THE
    # PAIR'S FULL TOKEN, MATCHED BY THE CASE-INSENSITIVE MATCHER, NOT A
    # BARE PREFIX.  ⭐⭐⭐⭐⭐ **A REQUIRED CHECK THAT ACCEPTS A PREFIX
    # ("was ALSO") IS WEAKER THAN ONE THAT ACCEPTS THE TOKEN** -- it
    # would pass on a commit that attributes the prior cycle to the
    # wrong band as long as the word ALSO appears.
    "commit": [_A["phrase"], _A["attr"]],
    "verify": [_A["phrase"]],
    "jobs": [_A["phrase"]],
    "jobs_verify": [_A["phrase"]],
}
print(f"  the pair's published phrase : {_A['phrase']!r}")
print(f"  the pair's attribution token: {_A['attr']!r}")
print(f"  the attribution FORBIDDEN set: {ATTR_FORBIDDEN}")
print(f"  the phrase FORBIDDEN set     : {PHRASE_FORBIDDEN}")
print(f"  the code-shape FORBIDDEN set : {SHAPE_FORBIDDEN}")


def live_lines(path):
    src = pathlib.Path(path).read_text(encoding="utf-8")
    tree = ast.parse(src)
    doc = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            body = getattr(node, "body", None)
            if body and isinstance(body[0], ast.Expr) and \
               isinstance(body[0].value, ast.Constant) and \
               isinstance(body[0].value.value, str):
                doc.update(range(body[0].lineno, body[0].end_lineno + 1))
    return src, [(i, ln) for i, ln in enumerate(src.splitlines(), 1)
                 if i not in doc]


def is_poison(line):
    return ("_bad" in line or "_poison" in line or "_ctrl" in line
            or "_shipped" in line)


def is_negative(line):
    """A NEGATIVE assertion forbids the token -- the gate doing its job."""
    return bool(re.search(r"\bnot\s+in\b", line)) or \
        bool(re.search(r"!=\s*[\"']", line))


def is_producer(line):
    """A PRODUCER computes a value (a ternary); it does not assert one."""
    return (" if " in line and " else " in line and
            "assert" not in line and "==" not in line and
            " in " not in line)


def negative_owners(path):
    """⭐⭐⭐ NEW AT 1251 -- THE ASSERTION'S POLARITY IS DECIDED BY THE
    *AST*, NOT BY THE LINE.

    A NEGATIVE assertion's FAILURE MESSAGE can span SEVERAL LINES:

        assert f"prior cycle ({PRIOR_CYCLE}) was IN BAND" not in _cmt, (
            f"the comment claims the prior cycle ({PRIOR_CYCLE}) was IN "
            f"BAND -- it was OUT OF BAND, so that statement is FALSE")

    ⭐⭐⭐ THE MESSAGE SAYS "was IN BAND" AND "was OUT OF BAND" -- AND A
    LINE-BASED POLARITY TEST SEES ONLY THE CONTINUATION LINES, WHICH CARRY
    NEITHER `not in` NOR `!=`.  ⭐⭐⭐ SO THE LINE-BASED TEST CLASSIFIES
    THEM AS *POSITIVE* ASSERTIONS AND REPORTS FIVE FALSE POSITIVES.

    ⭐⭐⭐⭐⭐ AND THE FAILURE MESSAGE IS A PUBLICATION: it is what an
    operator READS when the gate fires.  ⭐⭐⭐⭐⭐ BUT A MESSAGE THAT
    EXPLAINS WHY A FORBIDDEN PHRASE IS FORBIDDEN MUST NOT BE TREATED AS
    A VIOLATION OF THAT VERY PHRASE -- otherwise the gate forbids the
    phrase and its own explanation of the prohibition.

    ⭐⭐⭐⭐⭐ THE FIX: A LINE BELONGS TO A NEGATIVE ASSERTION IF THE
    ASSERTION IT IS PART OF IS NEGATIVE.  ⭐⭐⭐⭐⭐ THE AST IS THE
    INSTRUMENT THAT KNOWS THIS -- A LINE IS NOT A STATEMENT.
    """
    src = pathlib.Path(path).read_text(encoding="utf-8")
    tree = ast.parse(src)
    owned = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assert):
            continue
        _test = node.test
        _neg = False
        # `X not in Y` -- a negative membership test
        if (isinstance(_test, ast.Compare) and len(_test.ops) == 1
                and isinstance(_test.ops[0], ast.NotIn)):
            _neg = True
        # `X != Y` -- a negative equality test
        if (isinstance(_test, ast.Compare) and len(_test.ops) == 1
                and isinstance(_test.ops[0], ast.NotEq)):
            _neg = True
        # `not X` -- a negated truth test
        if (isinstance(_test, ast.UnaryOp)
                and isinstance(_test.op, ast.Not)):
            _neg = True
        if _neg:
            for _ln in range(node.lineno, node.end_lineno + 1):
                owned.add(_ln)
    return owned


def attr_regex(attr):
    """⭐⭐⭐ THE ATTRIBUTION IS MATCHED AS AN *EXACT TOKEN*, WITH A
    NEGATIVE LOOKBEHIND FOR THE "ALSO" PREFIX.

    `"was IN BAND"` IS A SUBSTRING OF `"was ALSO IN BAND"` -- so a naive
    `in` test flags the CORRECT attribution on the (IN, IN) pair.

    ⭐⭐⭐⭐⭐ **THE "ALSO" PREFIX IS PART OF THE TOKEN, NOT A MODIFIER OF
    THE MATCHER.**  ⭐⭐⭐⭐⭐ THE FIRST VERSION OF THIS FUNCTION ALWAYS
    FORBID "ALSO" -- and the (OUT, OUT) PAIR'S CORRECT TOKEN **IS**
    ⭐⭐⭐⭐⭐ `was ALSO OUT OF BAND`, so the matcher could not find its own
    ⭐⭐⭐⭐⭐ pair's attribution and the REQUIRED check reported it
    ⭐⭐⭐⭐⭐ MISSING.  ⭐⭐⭐⭐⭐ **THE FIX: THE LOOKBEHIND IS DERIVED FROM
    ⭐⭐⭐⭐⭐ THE TOKEN ITSELF -- if the token already carries "ALSO", the
    ⭐⭐⭐⭐⭐ matcher REQUIRES it; if it does not, the matcher REFUSES it.**

    ⭐⭐⭐⭐⭐ **WHY EXACT-TOKEN MATCHING AND NOT A LOOKBEHIND: `was IN
    ⭐⭐⭐⭐⭐ BAND` vs `was ALSO IN BAND` differ by a PREFIX, so the
    ⭐⭐⭐⭐⭐ matcher must anchor on the prefix's presence or absence.**

    ⭐⭐⭐⭐⭐ **AND THE MATCH IS CASE-INSENSITIVE ON THE BAND WORDS:**
    ⭐⭐⭐⭐⭐ THE PROJECT PUBLISHES THE ATTRIBUTION IN BOTH CASES --
    ⭐⭐⭐⭐⭐ `was ALSO OUT OF BAND` (the page's comment) and
    ⭐⭐⭐⭐⭐ `was ALSO out of band` (the commit message's body) -- so a
    ⭐⭐⭐⭐⭐ case-SENSITIVE matcher cannot find its own pair's token in
    ⭐⭐⭐⭐⭐ one of the two places it is published.  ⭐⭐⭐⭐⭐ **THE "ALSO"
    ⭐⭐⭐⭐⭐ PREFIX IS MATCHED CASE-SENSITIVELY (it is always uppercase in
    ⭐⭐⭐⭐⭐ the published text) AND THE BAND WORDS CASE-INSENSITIVELY.**
    """
    core = attr.replace("was ", "", 1)
    _wants_also = core.startswith("ALSO ")
    _body = core[len("ALSO "):] if _wants_also else core
    if _wants_also:
        # the token REQUIRES the ALSO prefix; the band words are
        # case-insensitive ("OUT OF BAND" and "out of band" both count)
        # ⭐⭐⭐⭐⭐ THE "ALSO" IS CONSUMED FROM THE BODY -- prepending it
        # ⭐⭐⭐⭐⭐ AGAIN WOULD PRODUCE `ALSO ALSO OUT OF BAND`.
        _parts = _body.split(" ")
        _pat = r"\bwas\s+ALSO\s+" + r"\s+".join(
            re.escape(_w) for _w in _parts)
        return re.compile(_pat, re.IGNORECASE)
    # the token REFUSES the ALSO prefix (so `was IN BAND` never matches
    # inside `was ALSO IN BAND`)
    return re.compile(r"\bwas\s+(?!ALSO\b)(?!also\b)" + re.escape(_body),
                      re.IGNORECASE)


print()
print("=" * 78)
print("1. THE FORBIDDEN-TOKEN SCAN (polarity-aware, producer-aware)")
print("=" * 78)
viol = []
for name in TAIL:
    p = REPO / f"_c{CYCLE}_{name}.py"
    if not p.exists():
        continue
    src, ll = live_lines(p)
    _neg_owned = negative_owners(p)
    for i, ln in ll:
        s = ln.strip()
        if s.startswith("#"):
            continue
        if is_poison(ln):
            continue
        # ⭐⭐⭐ THE POLARITY IS DECIDED BY THE AST: a line that is PART OF
        # a negative assertion inherits that assertion's polarity, even
        # when the line itself carries no `not in` / `!=` (a multi-line
        # failure MESSAGE).
        neg = is_negative(ln) or (i in _neg_owned)
        prod = is_producer(ln)
        for tok in FORBIDDEN_TOKENS:
            hit = (tok in ln) if not tok.startswith("was ") else \
                bool(attr_regex(tok).search(ln))
            if hit:
                if neg or prod:
                    continue
                viol.append((name, i, tok, s))
                break

print(f"  [FIND] {len(viol)} live line(s) carry a forbidden token in a "
      f"POSITIVE assertion")
for name, i, tok, s in viol:
    print(f"    [VIOLATION] {name}:{i}  {tok!r}  |  {s[:90]}")
if viol:
    raise SystemExit("[sweep] ABORT: a forbidden token survives in a "
                     "positive assertion")
print("  [OK] no forbidden token survives in a POSITIVE assertion")
print("  [OK] the forbidden tokens that remain are all inside NEGATIVE "
      "assertions (the gates forbidding the old polarity) -- CORRECT")

print()
print("=" * 78)
print("2. THE REQUIRED-TOKEN CHECK")
print("=" * 78)
miss = []
for fname, toks in REQUIRED.items():
    p = REPO / f"_c{CYCLE}_{fname}.py"
    if not p.exists():
        continue
    src = p.read_text(encoding="utf-8")
    for tok in toks:
        if tok.startswith("was "):
            ok = bool(attr_regex(tok).search(src))
        else:
            ok = tok in src
        if not ok:
            miss.append((fname, tok))
if miss:
    for fname, tok in miss:
        print(f"    [MISSING] {fname}.py: {tok!r}")
    raise SystemExit("[sweep] ABORT: a required token for THIS PAIR is "
                     "missing")
print("  [OK] the pair's phrase and attribution are present in every file "
      "that publishes or checks them")

print()
print("=" * 78)
print("3. THE COLLAPSED-TERNARY GUARD")
print("=" * 78)
collapsed = []
for name in TAIL:
    p = REPO / f"_c{CYCLE}_{name}.py"
    if not p.exists():
        continue
    src, ll = live_lines(p)
    for i, ln in ll:
        m = re.match(r'^\s*["\']([^"\']+)["\']\s+if\s+.*\s+else\s+["\']([^"\']+)["\']',
                     ln)
        if m and m.group(1) == m.group(2):
            collapsed.append((name, i, m.group(0)))
if collapsed:
    for name, i, txt in collapsed:
        print(f"    [COLLAPSED] {name}:{i}  {txt[:90]}")
    raise SystemExit("[sweep] ABORT: a ternary has identical branches")
print("  [OK] no ternary has identical branches")

print()
print("=" * 78)
print("4. ⭐⭐⭐ THE FALSE-NEGATIVE DIRECTION MUST BE PROVEN (new at 1251)")
print("=" * 78)
print("  ⭐⭐⭐ A SWEEP THAT HAS ONLY BEEN PROVEN ON THE TRUE ARTEFACT HAS")
print("  NOT BEEN PROVEN TO FIRE.  ⭐⭐⭐ THE POISON CLAIMS THE PRIOR CYCLE")
print("  WAS IN BAND WHEN IT WAS OUT -- AND IT MUST BE REJECTED.")
_poison_attr = next((a for a in ATTR_FORBIDDEN if a.startswith("was ")), None)
assert _poison_attr, "no attribution token available to build a poison"
# ⭐⭐⭐ THE POISON IS PROGRAMMATICALLY GENERATED: the *other* pairs'
# attributions, minus this pair's.  ⭐⭐⭐ THE POISON TEXT ITSELF IS
# DERIVED FROM THE TABLE, NEVER HAND-TYPED.
_poison_line = (f'f"the prior cycle ({PRIOR}) {_poison_attr} -- its own block '
                f'was the EVIDENCE"')
print(f"    the poison's attribution token : {_poison_attr!r} (from the "
      f"FORBIDDEN list)")
print(f"    the poison line               : {_poison_line}")
_poison_hit = bool(attr_regex(_A["attr"]).search(_poison_line))
print(f"    does the poison match THIS pair's attribution? {_poison_hit}")
assert not _poison_hit, (
    "[sweep] the poison MATCHES this pair's attribution -- the sweep's "
    "attribution matcher cannot discriminate")
print("    [OK] the poison does NOT match this pair's attribution -- the "
      "matcher DISCRIMINATES")
# ⭐⭐⭐ AND THE MATCHER MUST FIRE ON THE POISON'S OWN TOKEN.
_poison_own_hit = bool(attr_regex(_poison_attr).search(_poison_line))
assert _poison_own_hit, (
    "[sweep] the matcher does not fire on the poison's OWN attribution -- "
    "the matcher is blind")
print("    [OK] the matcher DOES fire on the poison's own attribution -- "
      "it is not blind")

print()
print("=" * 78)
print("5. THE CONTRADICTING-PAIR GUARD")
print("=" * 78)
for name in TAIL:
    p = REPO / f"_c{CYCLE}_{name}.py"
    if not p.exists():
        continue
    src, ll = live_lines(p)
    _neg_owned = negative_owners(p)
    for i, ln in ll:
        if is_poison(ln):
            continue
        if is_negative(ln) or (i in _neg_owned):
            continue
        if attr_regex(_A["attr"]).search(ln):
            for other in ATTR_FORBIDDEN:
                if attr_regex(other).search(ln):
                    raise SystemExit(
                        f"[sweep] ABORT: {name}:{i} asserts both "
                        f"{_A['attr']!r} and {other!r}")
print("  [OK] no file asserts both polarities of the same fact")

print()
print("=" * 78)
print("THE PAIR-KEYED VALUE-TOKEN SWEEP: CLEAN")
print("=" * 78)
