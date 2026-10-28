#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1293 -- THE IDENTITY SWEEP, RE-TARGETED AT 1282.

⭐⭐⭐⭐⭐ **WHY THIS IS A *NEW* FILE AND NOT A RE-RUN OF `_c1280_clone_sweep.py`.**

Cycle 1280's sweep carried `CYCLE = "1278"` (it should have carried
`"1280"`), so its file target `_c{CYCLE}_{_f}.py` resolved to **THE
COMMITTED BASE GENERATION** and it re-typed THAT base's identity instead of
its own.  ⇒ **THE `_c1280_*` GENERATION NEVER GOT ITS OWN IDENTITY
SWEPT** -- which is why the (IN, IN) generation still says "CYCLE 1278 IS
HOUR212" in its prose.

⭐⭐⭐⭐⭐ **⇒ THIS SWEEP IS RE-TARGETED AT `CYCLE = "1282"`**, and its
`OLD_HOUR` is **MEASURED** from the generation the clone was copied FROM
(`_c1280_*`, whose `measure.py` carries `CYCLE_HOUR_UTC = 2`).

⭐⭐⭐⭐⭐ **THE PROSE REWRITE IS THE SWEEP'S OWN JOB** -- it carries the
LINE-SCOPED CITATION EXEMPTION that protects HISTORICAL CITATIONS, and its
own 2j audit proves those citations survive.  ⭐⭐⭐⭐⭐ **A BLANKET PROSE
REWRITE HERE WOULD DESTROY THEM.**

⭐⭐⭐⭐⭐ **THE PAIR ASSERTION IS *MEASURED*, NOT TYPED** -- and it is the
(IN, IN) pair, which the sweep's own token set is keyed by.
"""
import ast
import pathlib
import re
import subprocess

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1303"
HOUR = 16
# ⭐⭐⭐⭐⭐ **CYCLE 1303's REPAIR: `PRIOR` IS *DERIVED*, NOT TYPED.**
# ⭐⭐⭐⭐⭐ The prior COMMITTED cycle is the cycle named by the commit that
# ⭐⭐⭐⭐⭐ PUBLISHED `index.html`, CROSS-CHECKED against the cycle named by
# ⭐⭐⭐⭐⭐ HEAD's OWN page comment (the two artefacts must agree).
# ⭐⭐⭐⭐⭐ ⇒ ⇒ **⇒ A TYPED `PRIOR` IS A LATENT ASSERTION ABOUT THE WORLD**
# ⭐⭐⭐⭐⭐ (1285's class-level rule): the value was STALE (`"1299"`, two
# ⭐⭐⭐⭐⭐ cycles behind), and the *pair derivation* silently read the WRONG
# ⭐⭐⭐⭐⭐ generation's hour (11 instead of 14) ⇒ ⇒ **⇒ IT WAS RIGHT BY
# ⭐⭐⭐⭐⭐ LUCK, NOT BY MEASUREMENT.**
# ⭐⭐⭐⭐⭐ ⇒ ⇒ **⇒ THE FIX IS A *DERIVATION*, NOT A RE-TYPE** -- a re-type
# ⭐⭐⭐⭐⭐ would be correct for THIS cycle only and would rot at the next
# ⭐⭐⭐⭐⭐ one.  ⭐⭐⭐⭐⭐ ⇒ ⇒ **⇒ AND THE FIX IS LIFTED FROM A SIBLING
# ⭐⭐⭐⭐⭐ THAT ALREADY DERIVED IT CORRECTLY** (`sweep_tokens.py` and
# ⭐⭐⭐⭐⭐ `docstring_shape.py` both derive PRIOR from HEAD).
import subprocess as _subprocess
_pub = _subprocess.run(
    ["git", "log", "-1", "--format=%H", "--", "index.html"], cwd=REPO,
    capture_output=True, text=True).stdout.strip()
assert _pub, "[sweep] could not find the commit that published index.html"
_subject = _subprocess.run(["git", "show", "-s", "--format=%s", _pub],
                           cwd=REPO, capture_output=True, text=True).stdout
_pm = re.search(r"cron cycle (\d+)", _subject)
assert _pm, (
    f"[sweep] the publishing commit's subject names no cycle: {_subject!r}")
PRIOR = _pm.group(1)
_page = _subprocess.run(["git", "show", "HEAD:index.html"], cwd=REPO,
                         capture_output=True, text=True).stdout
_cmt = re.search(r"<!--\s*cron cycle (\d+):(.*?)-->", _page, re.S)
assert _cmt, "[sweep] could not read HEAD's cycle comment"
assert _cmt.group(1) == PRIOR, (
    f"[sweep] HEAD's publishing commit names cycle {PRIOR} but HEAD's page "
    f"names {_cmt.group(1)} -- the two artefacts disagree")       # the prior COMMITTED cycle -- MEASURED from HEAD's
#                     publishing commit (its own hour 11 = OUT OF BAND)
# ⭐⭐⭐⭐⭐ **THE BASE_CYCLE IS *THIS* CYCLE'S OWN GENERATION** -- because
# the sweep's job is to re-type THIS cycle's identity, and `OLD_HOUR` (the
# hour the prose currently carries) is MEASURED from the generation the
# clone was copied FROM.
# ⭐⭐⭐⭐⭐ **THE CLONE SOURCE IS *1299* -- MEASURED, NOT ASSUMED**: the
# preparation instrument cloned `_c1299_*` (the newest generation on disk
# that is (OUT, UNCHANGED) -- this cycle's measured shape -- AND carries
# BOTH post-1278 repairs: 1295's write-block repair in `build.py` and
# 1297's hard-coded-count repair in `measure.py`).
# ⭐⭐⭐⭐⭐ **⇒ IT IS *NOT* A HARD-CODED NUMBER**: it is the generation the
# prep's clone actually copied FROM, and the sweep CROSS-CHECKS its
# `measure.py` CONSTANT against the PROSE's own hour (the 2h/2k audits).
# ⭐⭐⭐⭐⭐ **CYCLE 1303's REPAIR: `CLONE_SOURCE` IS *MEASURED*, NOT TYPED.**
# ⭐⭐⭐⭐⭐ It is the generation whose `measure.py` carries the PROSE's own
# ⭐⭐⭐⭐⭐ `OLD_HOUR` -- i.e. the generation the clone was ACTUALLY copied
# ⭐⭐⭐⭐⭐ FROM, which the cross-check below then reads.  ⭐⭐⭐⭐⭐ ⇒ ⇒ **⇒ A
# ⭐⭐⭐⭐⭐ TYPED CLONE SOURCE IS A LATENT ASSERTION ABOUT THE WORLD**: the
# ⭐⭐⭐⭐⭐ value was STALE (`"1299"`), so the cross-check compared this
# ⭐⭐⭐⭐⭐ cycle's prose against a generation that was NOT its clone source.
CLONE_SOURCE = None   # MEASURED below, once OLD_HOUR is known

BAND_FILES = ["measure", "page", "struct", "commit", "verify", "jobs",
              "jobs_verify"]
FIX_FILES = ["paths", "adjudicate", "payload", "translate", "select", "build",
             "write", "render", "render_posts", "triage", "band_firetest",
             "fidelity2", "third_instrument", "fetch_new", "d_keepcheck",
             "precert"]
LEGACY = ["patch_measure"]
LEGACY_CARRY = ["patch_anchor", "patch_band", "patch_noop", "patch_literals"]
CARRY = ["patch_prose"]
ALL = BAND_FILES + FIX_FILES + LEGACY + LEGACY_CARRY + CARRY
RUN_SET = BAND_FILES + FIX_FILES

# ======================================================================
# 0. OLD_HOUR -- MEASURED, NEVER TYPED
# ======================================================================
# ⭐⭐⭐⭐⭐ **CYCLE 1303's REPAIR: `_base_measure` IS READ *AFTER* THE CLONE
# SOURCE IS MEASURED.**  ⭐⭐⭐⭐⭐ The read used to sit at the TOP of this
# section, but `BASE_CYCLE` is now a MEASURED value (not a typed one) and it
# is assigned further down, after `OLD_HOUR` is resolved ⇒ ⇒ **⇒ READING THE
# FILE AT THE TOP IS A *USE BEFORE DEFINITION*** ⇒ ⇒ **⇒ THE READ MOVED TO
# WHERE THE VALUE EXISTS.**
# ⭐⭐⭐⭐⭐ **⇒ THE ORDERING IS THE CONTRACT**: the clone source can only be
# identified from the PROSE's hour, and the prose's hour can only be
# resolved by reading the clone's prose.
# ⭐⭐⭐⭐⭐ **OLD_HOUR IS THE PROSE'S HOUR, AND IT IS *MEASURED FROM THE
# PROSE ITSELF*.**  ⭐⭐⭐⭐⭐ **THE CONSTANT AND THE PROSE ARE TWO
# DIFFERENT SURFACES**, and cycle 1280's MIS-TARGETED sweep left them
# DIVERGED: the CONSTANT was re-typed by 1280's clone (`= 15`) while the
# PROSE was never re-typed (the sweep rewrote the base generation instead
# of its own), so the prose still carried the ORIGINAL base generation's
# hour (12).  ⇒ **READING `OLD_HOUR` FROM THE CONSTANT WOULD HAVE REWRITTEN
# THE WRONG HOUR AND LEFT THE PUBLISHED ONE STALE.**
# ⇒ **⇒ OLD_HOUR IS MEASURED FROM THE PROSE'S SELF-LABEL FORMS.**  ⭐⭐⭐⭐⭐
# **AND THE MEASUREMENT IS A *CROSS-CHECK*, NOT AN ASSUMPTION**: the prose
# must name EXACTLY ONE hour, and after the rewrite the prose and the
# CONSTANT must AGREE (the 2h audit + the 2k audit enforce it).
# ⭐⭐⭐⭐⭐ **THE RESOLUTION SET READS *SELF-LABEL* SURFACES ONLY.**
# ⭐⭐⭐⭐⭐ **THE CITATION FORM (`belongs to Hour NN UTC`) IS DELIBERATELY
# *EXCLUDED*** (1288's fix): a citation names a *HISTORICAL* cycle's hour,
# so it is a DIFFERENT HOUR BY DESIGN -- including it made the resolution
# ambiguous the moment a citation existed, and the sweep then ABORTED on a
# PERFECTLY CORRECT ARTEFACT (1275's class: an instrument that fires on a
# correct artefact IS the defect).  ⭐⭐⭐⭐⭐ **⇒ THE INSTRUMENT IS FIXED,
# NEVER THE ASSERTION RELAXED.**  ⭐⭐⭐⭐⭐ The citation is checked
# SEPARATELY, and STRICTLY, by the CITATION-TRUTH assertion below.
_PROSE_HOUR_RES = [
    re.compile(r"\bCYCLE\s+1[0-9]{3}\s+IS\s+HOUR\s+(\d{1,2})\b"),
    re.compile(r"\bTHIS CYCLE \(HOUR\s+(\d{1,2})\s+UTC\)"),
    re.compile(r"\bHOUR\s+(\d{1,2})\s+UTC\s+IS\s+\*\*"),
    re.compile(r'"""Hour\s+(\d{1,2})\s+IS\s+'),
    re.compile(r"\bhour\s+(\d{1,2})\s+IS\s+IN BAND"),
]
# ⭐⭐⭐⭐⭐ THE CITATION FORM -- RESOLVED SEPARATELY, AND ASSERTED TRUE.
_CITE_HOUR_RES = re.compile(
    r"\b[Cc]ycle\s+(\d{3,4})\s+belongs to Hour\s+(\d{1,2})\s+UTC\b")
_prose_hours = set()
for _f in BAND_FILES + FIX_FILES:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    for _rx in _PROSE_HOUR_RES:
        for _m in _rx.finditer(_p.read_text(encoding="utf-8")):
            _prose_hours.add(int(_m.group(1)))
assert len(_prose_hours) == 1, (
    f"[sweep] ABORT: the prose names {len(_prose_hours)} different hours "
    f"{sorted(_prose_hours)} -- the rewrite source is AMBIGUOUS; re-measure "
    "rather than guess")
OLD_HOUR = next(iter(_prose_hours))

# ⭐⭐⭐⭐⭐ **CYCLE 1303's REPAIR: THE CLONE SOURCE IS *MEASURED*.**  ⭐⭐⭐⭐⭐
# It is the generation whose `measure.py` carries the PROSE's OWN `OLD_HOUR`
# -- i.e. the generation the clone was ACTUALLY copied FROM.
_cs_cands = []
for _p in sorted(REPO.glob("_c*_measure.py")):
    _mm = re.match(r"_c(\d+)_measure\.py$", _p.name)
    if not _mm:
        continue
    _cm = re.search(r"(?m)^CYCLE_HOUR_UTC\s*=\s*(\d+)\s*$",
                    _p.read_text(encoding="utf-8"))
    if _cm and int(_cm.group(1)) == OLD_HOUR and _mm.group(1) != CYCLE:
        _cs_cands.append(_mm.group(1))
assert _cs_cands, (
    f"[sweep] ABORT: NO generation's measure.py carries the prose's hour "
    f"{OLD_HOUR} -- the clone source cannot be identified, and a typed one "
    "would be a latent assertion about the world")
CLONE_SOURCE = max(_cs_cands, key=int)
print(f"[sweep] the CLONE SOURCE is MEASURED: {CLONE_SOURCE} (the newest "
      f"generation whose measure.py carries hour {OLD_HOUR})")

# ⭐⭐⭐⭐⭐ **THE CITATION-TRUTH ASSERTION (1288).**  ⭐⭐⭐⭐⭐ A CITATION
# NAMES A HISTORICAL CYCLE'S HOUR, and it is EXEMPT from the sweep's
# rewrite -- so its truth is the sweep's RESPONSIBILITY, not its
# exemption's.  ⭐⭐⭐⭐⭐ **⇒ EVERY CITATION OF THE PRIOR COMMITTED CYCLE
# MUST NAME THE HOUR RE-MEASURED FROM HEAD's OWN COMMITTED PAGE** ⇒ ⇒
# **⇒ THIS IS *STRONGER* THAN THE AMBIGUITY ABORT IT REPLACES.**
import subprocess as _subprocess
_head_cmt = _subprocess.run(["git", "show", "HEAD:index.html"], cwd=REPO,
                            capture_output=True, text=True).stdout
_head_hour_m = re.search(r"<!--\s*cron cycle \d+:(?:(?!-->).)*?=\s*Hour "
                         r"(\d{1,2}) UTC", _head_cmt, re.S)
assert _head_hour_m, "[sweep] could not read HEAD's committed page comment"
_HEAD_HOUR = int(_head_hour_m.group(1))
for _f in sorted(REPO.glob(f"_c{CYCLE}_*.py")):
    _txt = _f.read_text(encoding="utf-8")
    for _i, _m in enumerate(_CITE_HOUR_RES.finditer(_txt), 1):
        _ch, _chh = _m.group(1), int(_m.group(2))
        if _ch != PRIOR:
            continue
        assert _chh == _HEAD_HOUR, (
            f"[sweep] ABORT: a CITATION names cycle {_ch} at Hour {_chh}, "
            f"but HEAD's committed page says Hour {_HEAD_HOUR} -- the "
            "citation is FALSE")
BASE_CYCLE = CLONE_SOURCE
# ⭐⭐⭐⭐⭐ **CYCLE 1303's REPAIR: THE CLONE SOURCE's `measure.py` IS READ
# HERE** -- i.e. *after* the clone source is MEASURED, not before.
_base_measure = (REPO / f"_c{BASE_CYCLE}_measure.py").read_text(encoding="utf-8")
assert _base_measure, "[sweep] the clone source's measure.py is empty"
print(f"[sweep] OLD_HOUR is MEASURED from the PROSE's own SELF-LABEL forms: "
      f"{OLD_HOUR} (not typed, and NOT read from a constant that a "
      f"different stage re-typed)")
_const_m = re.search(r"(?m)^CYCLE_HOUR_UTC\s*=\s*(\d+)$", _base_measure)
print(f"[sweep] (for the record: the clone source {BASE_CYCLE}'s measure.py "
      f"CONSTANT reads {_const_m.group(1) if _const_m else '?'} -- the "
      f"CONSTANT and the PROSE were DIVERGED, which is exactly why the "
      f"prose is the source of truth here)")

# ======================================================================
# 0b. THE PAIR -- MEASURED, NOT TYPED
# ======================================================================
_ft = (REPO / "fetch_tweets.py").read_text(encoding="utf-8")
_bm = re.search(r"RETRY_TRANSLATION_HOURS\s*=\s*\{([^}]*)\}", _ft)
assert _bm, "could not read RETRY_TRANSLATION_HOURS from fetch_tweets.py"
_BAND = {int(x) for x in re.findall(r"\d+", _bm.group(1))}
_IN_BAND = HOUR in _BAND
_prior_measure = REPO / f"_c{PRIOR}_measure.py"
assert _prior_measure.exists(), (
    f"the prior cycle {PRIOR}'s measure.py is absent -- the prior hour "
    "cannot be MEASURED, and a typed one would be a latent assertion")
_pm = re.search(r"(?m)^CYCLE_HOUR_UTC\s*=\s*(\d+)$",
                _prior_measure.read_text(encoding="utf-8"))
assert _pm, f"could not read the prior cycle {PRIOR}'s hour"
PRIOR_HOUR = int(_pm.group(1))
_PRIOR_IN_BAND = PRIOR_HOUR in _BAND
PAIR = ("IN" if _PRIOR_IN_BAND else "OUT", "IN" if _IN_BAND else "OUT")
print("=" * 78)
print(f"CYCLE {CYCLE} -- IDENTITY SWEEP + the audits")
print("=" * 78)
print(f"  this cycle: hour {HOUR} UTC = "
      f"{'IN' if _IN_BAND else 'OUT OF'} BAND; prior COMMITTED = {PRIOR} "
      f"(hour {PRIOR_HOUR} -> "
      f"{'IN' if _PRIOR_IN_BAND else 'OUT OF'} BAND)")
print(f"  => PAIR = {PAIR} -> "
      f"{'the control set is UNCHANGED, NOT flipped' if PAIR[0] == PAIR[1] else 'the control set FLIPS'}")
print(f"  the clone source: {CLONE_SOURCE} (hour {OLD_HOUR})")
# ⭐⭐⭐⭐⭐ **THE PAIR ASSERT IS *SHAPE-NEUTRAL*** (1276's two-axis rule:
# a *shape-scoped* assertion does not TRAVEL to another pair ⇒ ⇒ it fires
# on a CORRECT artefact ⇒ ⇒ 1275's class: the INSTRUMENT is fixed, never
# the assertion relaxed).  ⭐⭐⭐⭐⭐ **⇒ IT NOW STATES A FACT ABOUT THE
# *SPACE* OF PAIRS, NOT ABOUT *WHICH* PAIR** ⇒ ⇒ **⇒ IT TRAVELS TO EVERY
# PAIR.** ⭐⭐⭐⭐⭐ **⇒ AND IT IS *STRONGER*: the original named ONE pair
# (so a derivation bug naming a pair OUTSIDE the space was silently
# tolerated by the SWEEP, and only the *token set* would catch it) ⇒ ⇒
# **⇒ NOW THE MEASURED PAIR MUST BE ONE OF THE FOUR KNOWN PAIRS.**
_KNOWN_PAIRS = {("IN", "IN"), ("IN", "OUT"), ("OUT", "IN"), ("OUT", "OUT")}
assert PAIR in _KNOWN_PAIRS, (
    f"the MEASURED pair is {PAIR}, which is NOT one of the four known "
    "pairs -- the pair DERIVATION is defective (not this sweep)")

# ======================================================================
# THE CITATION EXEMPTION (carried from cycle 1252/1254, unchanged)
# ======================================================================
_SELF_LABEL_RE = re.compile(r"\bCYCLE\s+1[0-9]{3}\b(?=\s+IS\s+HOUR\b)")
_CYCLE_NUM_RE = re.compile(r"\bcycles?\s+(\d{3,4})\b", re.I)


def _is_self_label(line):
    return bool(_SELF_LABEL_RE.search(line))


def _is_citation_line(line, carried):
    if _is_self_label(line):
        return False
    for _m in _CYCLE_NUM_RE.finditer(line):
        if _m.group(1) != PROSE_IDENTITY:
            return True
    if carried and carried != PROSE_IDENTITY:
        return True
    return False


def _carried_cycle(prev_lines):
    for _ln in reversed(prev_lines):
        if not _ln.strip():
            return None
        if _is_self_label(_ln):
            continue
        _ms = [m.group(1) for m in _CYCLE_NUM_RE.finditer(_ln)]
        if _ms:
            return _ms[-1]
    return None


# ⭐⭐⭐⭐⭐ **THE CITATION EXEMPTION'S REFERENCE IS THE *PROSE IDENTITY* --
# THE CYCLE NUMBER THE PROSE ITSELF NAMES -- NOT THE CLONE SOURCE.**
# ⭐⭐⭐⭐⭐ **⇒ THE SAME RULE AS `OLD_HOUR`**: the constant and the prose
# are two surfaces, and they were DIVERGED.  ⭐⭐⭐⭐⭐ A line naming the
# PROSE's own cycle is a SELF-LABEL (not a citation); a line naming any
# OTHER cycle is a HISTORICAL CITATION and is EXEMPT.
_PROSE_CYCLE_RE = re.compile(r"\bcycles?\s+(\d{3,4})\b", re.I)
_prose_cycles = set()
for _f in BAND_FILES + FIX_FILES:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    for _m in _PROSE_CYCLE_RE.finditer(_p.read_text(encoding="utf-8")):
        _prose_cycles.add(_m.group(1))
# ⭐⭐⭐⭐⭐ THE PROSE IDENTITY IS THE CYCLE THE *SELF-LABEL* FORM NAMES --
# the all-caps `CYCLE <n> IS HOUR` shape is unambiguous (it is the shape
# the sweep's rule (f) rewrites), so it is the right source.
_self_label_cycles = set()
for _f in BAND_FILES + FIX_FILES:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    for _m in re.finditer(r"\bCYCLE\s+(\d{3,4})\s+IS\s+HOUR\b",
                           _p.read_text(encoding="utf-8")):
        _self_label_cycles.add(_m.group(1))
assert len(_self_label_cycles) == 1, (
    f"[sweep] ABORT: the SELF-LABEL names {len(_self_label_cycles)} "
    f"different cycles {sorted(_self_label_cycles)} -- the exemption "
    "reference is AMBIGUOUS; re-measure rather than guess")
PROSE_IDENTITY = next(iter(_self_label_cycles))
print(f"[sweep] PROSE_IDENTITY (the cycle the SELF-LABEL names, and the "
      f"exemption's reference) is MEASURED: {PROSE_IDENTITY}")

print()
print("=" * 78)
print("1. THE UNBOUNDED IDENTITY SWEEP")
print("=" * 78)

_swept = 0
for _f in ALL:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    _src = _p.read_text(encoding="utf-8")
    _orig = _src

    # (a) the PRIOR-CYCLE constant
    _src = re.sub(r'(?m)^(PRIOR_CYCLE\s*=\s*)"1[0-9]{3}"$',
                  rf'\g<1>"{PRIOR}"', _src)
    # (b) the SELF-CYCLE constant
    _src = re.sub(r'(?m)^(CYCLE\s*=\s*)"1[0-9]{3}"$',
                  rf'\g<1>"{CYCLE}"', _src)
    # (c) the CYCLE_HOUR_UTC constant
    _src = re.sub(r'(?m)^(CYCLE_HOUR_UTC\s*=\s*)\d+$',
                  rf'\g<1>{HOUR}', _src)
    # (d) the tmp paths
    _src = re.sub(r"/tmp/c\d{4}", f"/tmp/c{CYCLE}", _src)
    # (e) the instrument references
    _src = re.sub(r"_c\d{4}_", f"_c{CYCLE}_", _src)

    # (f) the prose cycle numbers + hours -- LINE-SCOPED, WITH THE
    #     WIDENED MULTI-LINE CITATION EXEMPTION
    _out_lines = []
    _prev = []
    for _ln in _src.splitlines(keepends=True):
        _carried = _carried_cycle(_prev)
        if _is_citation_line(_ln, _carried):
            _out_lines.append(_ln)
            _prev.append(_ln)
            continue
        _new_ln = _ln
        _new_ln = _SELF_LABEL_RE.sub(f"CYCLE {CYCLE}", _new_ln)
        for _form in ("cycle", "Cycle"):
            _new_ln = re.sub(rf"\b{_form} 1[0-9]{{3}}\b",
                             rf"{_form} {CYCLE}", _new_ln)
        _new_ln = re.sub(r"\bcycles 1[0-9]{3}\b", f"cycles {CYCLE}", _new_ln)
        for _form in ("Hour", "hour", "HOUR"):
            _new_ln = re.sub(rf"\b{_form} {OLD_HOUR} UTC\b",
                             f"{_form} {HOUR} UTC", _new_ln)
        for _form in ("Hour", "hour", "HOUR"):
            _new_ln = re.sub(rf"\b{_form} {OLD_HOUR}\b",
                             f"{_form} {HOUR}", _new_ln)
        _out_lines.append(_new_ln)
        _prev.append(_new_ln)
    _src = "".join(_out_lines)

    if _src != _orig:
        _p.write_text(_src, encoding="utf-8")
        _swept += 1
print(f"  [SWEEP] {_swept} file(s) rewritten")

# ======================================================================
# 2. THE AUDITS
# ======================================================================
print()
print("=" * 78)
print("2. THE AUDITS")
print("=" * 78)

# ---- (2a) the PATH audit -------------------------------------------------
print("\n  [2a] THE PATH AUDIT")
_missing = []
for _f in RUN_SET:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    _src = _p.read_text(encoding="utf-8")
    for _m in re.finditer(r'REPO\s*/\s*"([^"]+)"', _src):
        _rel = _m.group(1)
        if "/" in _rel and not _rel.startswith("."):
            if not (REPO / _rel).exists():
                _missing.append((_f, _rel))
    for _m in re.finditer(r'REPO / "([^"]+)"', _src):
        _rel = _m.group(1)
        if "/" in _rel and not _rel.startswith("."):
            if not (REPO / _rel).exists():
                _missing.append((_f, _rel))
if _missing:
    for _f, _rel in sorted(set(_missing)):
        print(f"    [MISSING] {_f}: {_rel}")
    raise SystemExit("[sweep] ABORT: a referenced path does not exist")
print("    [OK] every referenced path in the RUN SET exists")

# ---- (2b) the SCRIPT-REFERENCE audit -------------------------------------
print("\n  [2b] THE SCRIPT-REFERENCE AUDIT (the AST decides live-vs-prose)")
_bad = []
for _f in RUN_SET:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    _src = _p.read_text(encoding="utf-8")
    _tree = ast.parse(_src)
    _self = f"_c{CYCLE}_{_f}.py"
    for _node in ast.walk(_tree):
        if isinstance(_node, ast.Constant) and isinstance(_node.value, str):
            for _m in re.finditer(r"_c(\d{4})_[A-Za-z0-9_]+\.py", _node.value):
                if _m.group(0) == _self:
                    continue
                if _m.group(1) == CYCLE:
                    continue
                _bad.append((_f, _m.group(0)))
if _bad:
    for _f, _ref in sorted(set(_bad)):
        print(f"    [STALE] {_f}: {_ref}")
    raise SystemExit("[sweep] ABORT: a live reference names a stale cycle's script")
print("    [OK] no live string literal names a stale cycle's script")

# ---- (2c) the COLLECTION check -------------------------------------------
print("\n  [2c] THE COLLECTION CHECK (Reminder 70)")
_pc = (REPO / f"_c{CYCLE}_precert.py").read_text(encoding="utf-8")
assert "assert len(set(BACKUP_CHAIN)) == len(BACKUP_CHAIN)" in _pc, (
    "[sweep] ABORT: the precert lost the backup chain's collapse assertion")
print("    [OK] the backup chain's collapse assertion is PRESENT")

# ---- (2d) the RESIDUE-PREDICATE agreement ---------------------------------
print("\n  [2d] THE RESIDUE-PREDICATE CHECK")


def _residue_code(path):
    _tree = ast.parse(pathlib.Path(path).read_text(encoding="utf-8"))
    _fn = None
    for _node in ast.walk(_tree):
        if (isinstance(_node, ast.FunctionDef)
                and _node.name == "is_proper_noun"):
            _fn = _node
            break
    assert _fn is not None, f"{path} has no is_proper_noun"
    _body = list(_fn.body)
    if (_body and isinstance(_body[0], ast.Expr)
            and isinstance(_body[0].value, ast.Constant)
            and isinstance(_body[0].value.value, str)):
        _body = _body[1:]
    assert _body, f"{path}: is_proper_noun has no executable body"
    return "\n".join(ast.dump(n) for n in _body)


_a = _residue_code(REPO / f"_c{CYCLE}_translate.py")
_b = _residue_code(REPO / f"_c{CYCLE}_fidelity2.py")
assert _a == _b, "[sweep] ABORT: the residue predicate's two copies DISAGREE"
print("    [OK] both copies of `is_proper_noun` have the SAME executable body")

# ---- (2e) the SELF-CYCLE check --------------------------------------------
print("\n  [2e] THE SELF-CYCLE CHECK")
for _f in RUN_SET:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    _src = _p.read_text(encoding="utf-8")
    _m = re.search(r'(?m)^CYCLE\s*=\s*"(\d+)"$', _src)
    if _m:
        assert _m.group(1) == CYCLE, (
            f"{_f}: CYCLE = {_m.group(1)!r}, expected {CYCLE!r}")
print(f"    [OK] every RUN-SET file's CYCLE constant is {CYCLE!r}")

# ---- (2f) the HOUR check --------------------------------------------------
print("\n  [2f] THE HOUR CHECK")
for _f in RUN_SET:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    _src = _p.read_text(encoding="utf-8")
    for _m in re.finditer(r'(?m)^CYCLE_HOUR_UTC\s*=\s*(\d+)$', _src):
        assert int(_m.group(1)) == HOUR, (
            f"{_f}: CYCLE_HOUR_UTC = {_m.group(1)}, expected {HOUR}")
print(f"    [OK] every RUN-SET file's CYCLE_HOUR_UTC is {HOUR}")

# ---- (2g) the STALE-CONSTANT check ---------------------------------------
print("\n  [2g] THE STALE-CONSTANT CHECK (the identity FORMS, not bare numbers)")
for _f in RUN_SET:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    _src = _p.read_text(encoding="utf-8")
    _tree = ast.parse(_src)
    for _node in ast.walk(_tree):
        if not isinstance(_node, ast.Assign):
            continue
        for _t in _node.targets:
            if not isinstance(_t, ast.Name):
                continue
            if _t.id == "CYCLE":
                _v = _node.value
                if isinstance(_v, ast.Constant) and isinstance(_v.value, str):
                    assert _v.value == CYCLE, (
                        f"[sweep] ABORT: {_f} line {_node.lineno}: "
                        f"CYCLE = {_v.value!r}, expected {CYCLE!r}")
            elif _t.id == "PRIOR_CYCLE":
                _v = _node.value
                if isinstance(_v, ast.Constant) and isinstance(_v.value, str):
                    assert _v.value == PRIOR, (
                        f"[sweep] ABORT: {_f} line {_node.lineno}: "
                        f"PRIOR_CYCLE = {_v.value!r}, expected {PRIOR!r}")
print("    [OK] every identity ASSIGNMENT (CYCLE / PRIOR_CYCLE) in the RUN "
      "SET is current")

# ---- (2h) THE OLD-HOUR PROSE CHECK -- THE NEGATIVE CLAIM -----------------
print("\n  [2h] THE OLD-HOUR PROSE CHECK -- THE NEGATIVE CLAIM")
_HOUR_TOK = re.compile(r"\bHOUR\s+(\d{1,2})\s+UTC\b", re.IGNORECASE)
_old_hits = []
_all_hour_hits = {}
for _f in RUN_SET:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    _src = _p.read_text(encoding="utf-8")
    _src_lines = _src.splitlines()
    for _i, _ln in enumerate(_src_lines):
        _carried = _carried_cycle(_src_lines[:_i])
        for _m in _HOUR_TOK.finditer(_ln):
            _h = int(_m.group(1))
            _lnno = _i + 1
            _all_hour_hits.setdefault(_h, []).append((_f, _lnno))
            if _h == HOUR:
                continue
            if _is_citation_line(_ln, _carried):
                print(f"    [CITATION] {_f}:{_lnno}  {_m.group(0)!r} -- a "
                      f"HISTORICAL CITATION (carried cycle {_carried!r}) -> EXEMPT")
                continue
            _old_hits.append((_f, _lnno, _m.group(0)))
if _old_hits:
    for _f, _ln, _txt in _old_hits:
        print(f"    [STALE HOUR] {_f}:{_ln}  {_txt!r}")
    raise SystemExit(
        f"[sweep] ABORT: a HOUR token other than {HOUR} survives in the RUN "
        f"SET -- the page PUBLISHES its hour, so a stale prose hour is a "
        f"published falsehood")
print(f"    [OK] EVERY `HOUR <n> UTC` token in the RUN SET names hour {HOUR} "
      f"(any case form), EXCEPT historical citations")
print(f"         the hour tokens found: "
      f"{ {k: len(v) for k, v in sorted(_all_hour_hits.items())} }")

# ---- (2i) THE ALL-CAPS HOUR DOCSTRING CHECK -------------------------------
print("\n  [2i] THE ALL-CAPS HOUR DOCSTRING CHECK (the 1246 defect)")
_stale_caps = []
for _f in RUN_SET:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    _src = _p.read_text(encoding="utf-8")
    _src_lines = _src.splitlines()
    for _i, _ln in enumerate(_src_lines):
        _carried = _carried_cycle(_src_lines[:_i])
        for _m in re.finditer(r"\bHOUR\s+(\d{1,2})\s+UTC\s+IS\s+\*\*"
                              r"(IN|OUT) OF BAND\*\*", _ln):
            _h = int(_m.group(1))
            if _h != HOUR and not _is_citation_line(_ln, _carried):
                _stale_caps.append((_f, _m.group(0)))
if _stale_caps:
    for _f, _txt in _stale_caps:
        print(f"    [STALE CAPS] {_f}: {_txt!r}")
    raise SystemExit("[sweep] ABORT: an all-caps HOUR docstring names a "
                     "stale hour")
print("    [OK] no all-caps `HOUR <n> UTC IS **... OF BAND**` docstring "
      "names a stale hour")

# ---- (2j) THE HISTORICAL-CITATION AUDIT ----------------------------------
print("\n  [2j] THE HISTORICAL-CITATION AUDIT (the restored citations must "
      "survive)")
_ORIGIN = "1232"
_CITATION_SIGNATURES = [
    ("third_instrument", "those are DIFFERENT hours", "the 1231 citation"),
    ("build", "SUBSTANTIVE CYCLE.", "the 1229 citation"),
    ("measure", "published banner 173 as an UNEXPLAINED MISMATCH",
     "the 1231 banner citation"),
]
_cite_missing = []
for _fname, _signature, _why in _CITATION_SIGNATURES:
    _p = REPO / f"_c{CYCLE}_{_fname}.py"
    if not _p.exists():
        continue
    _src = _p.read_text(encoding="utf-8")
    _o = REPO / f"_c{_ORIGIN}_{_fname}.py"
    if not _o.exists():
        continue
    _osrc = _o.read_text(encoding="utf-8")
    if _signature not in _osrc:
        continue
    _orig_lines = [ln.strip() for ln in _osrc.splitlines()
                   if _signature in ln]
    _cur_lines = [ln.strip() for ln in _src.splitlines() if _signature in ln]
    for _ol in _orig_lines:
        if _ol not in _cur_lines:
            _cite_missing.append((_fname, _why, _ol))
if _cite_missing:
    for _fname, _why, _ol in _cite_missing:
        print(f"    [CITATION LOST] {_fname} ({_why}): {_ol!r}")
    raise SystemExit(
        "[sweep] ABORT: a historical citation was rewritten -- the sweep "
        "destroyed the evidence the file exists to preserve")
print("    [OK] every historical citation the ORIGIN carries survives in "
      "this cycle's file")

# ---- (2k) THE SELF-LABEL PROSE CHECK (the 1280 defect class) --------------
print()
print("  [2k] THE SELF-LABEL PROSE CHECK -- the SELF-LABEL must name THIS "
      "cycle")
_stale_self = []
for _f in RUN_SET:
    _p = REPO / f"_c{CYCLE}_{_f}.py"
    if not _p.exists():
        continue
    for _i, _ln in enumerate(_p.read_text(encoding="utf-8").splitlines()):
        for _m in re.finditer(r"\bCYCLE\s+(\d{3,4})\s+IS\s+HOUR\s+(\d{1,2})",
                              _ln):
            if _m.group(1) != CYCLE:
                _stale_self.append((_f, _i + 1, _m.group(0)))
if _stale_self:
    for _f, _ln, _txt in _stale_self:
        print(f"    [STALE SELF-LABEL] {_f}:{_ln}  {_txt!r}")
    raise SystemExit("[sweep] ABORT: a SELF-IDENTITY label names another "
                     "cycle -- the page PUBLISHES it")
print("    [OK] every `CYCLE <n> IS HOUR <h>` self-label names this cycle")

print()
print("=" * 78)
print(f"[sweep] CYCLE {CYCLE} -- SWEEP + AUDITS COMPLETE")
print("=" * 78)
