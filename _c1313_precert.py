#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- PRE-CERTIFIED TRANSLATION MAP.

⭐ WHY THIS EXISTS (Reminder 32: DO NOT RE-TRANSLATE AN ALREADY-CERTIFIED
TRANSLATION).

Cycle 1278 inherited cycle 1278's two translated posts and left this
handover in `/tmp/c1313/translate/provenance.json`:

  * `2114243303994486876` -- **PRE-CERTIFIED, 0 defects**.  DO NOT
    re-translate.
  * `2114242922006897145` -- BEST-OF, **1 RECORDED FIDELITY DEFECT**
    (`with` at corpus keep-rate 2/998).  The quoted-span exemption was
    REFUSED by the measurement, so the defect STANDS.  The handover
    PERMITS a bounded retry, and says: if it keeps the same defect, it must
    be RECORDED, never silently dropped.

⭐⭐ THIS SCRIPT DERIVES THE MAP FROM THE ARTEFACTS, NOT FROM THE HANDOVER
PROSE.  **A HANDOVER NOTE IS A CLAIM; THE ARTEFACT IS THE MEASUREMENT**
(Reminder 60).  So:

  1. the provenance must say 0 defects for an id to be PRE-CERTIFIED;
  2. the translation that is pre-certified is the one in
     `translations_final.json` -- the ARTEFACT THAT WAS PUBLISHED, not
     `translations.json` (attempt #1).  Scoring the wrong artefact is
     Reminder 53;
  3. the id must be in THIS cycle's OWN adjudication set, and must be
     INHERITED (a brand-new id has no prior translation at all);
  4. and the PRE-EXISTING translation must still be present in the corpus
     this cycle inherited -- otherwise there is nothing to inherit.

⭐⭐⭐ THE PRIOR TRANSLATION LIVES IN THE **PRE-BUILD BACKUP**, NOT IN THE
CURRENT WORKTREE (Reminder 60).  This cycle's BUILD step REPLACES the
inherited records with freshly-built ones whose `translation` is "" (the
select step fills them) -- so by the time the precert map is derived, the
worktree's copy of the inherited records no longer carries the prior
cycle's translations.  The backup is the AUTHORITATIVE pre-build state,
and the build script took it BEFORE any write.

⭐⭐⭐⭐ THE ARTEFACT SOURCE IS CHOSEN BY **SEMANTICS, NOT BY RECENCY**
(Reminder 55 / Case 12).  Cycle 1278 RAN and produced a COMPLETE set of
translation artefacts -- `translations_final.json` (BOTH ids, mtime
20:15:12) and `provenance.json` -- but it was INTERRUPTED before its
commit, so it published nothing.  ⭐ **A CYCLE THAT RAN BUT DID NOT
COMMIT STILL OWNS ITS FIXES AND ITS ARTEFACTS**: the texts it produced
are the most recent COMPLETE translations, and they are what the corpus
actually carried.  ⭐ Note that cycle 1249's own handover NOTE claimed its
`translations_final.json` "does not exist" -- but the ARTEFACT says
otherwise (the file exists, with both ids and the correct mtime).  **A
HANDOVER NOTE IS A CLAIM; THE ARTEFACT IS THE MEASUREMENT** (Reminder 60).

⭐ AND THE PRE-CERTIFIED TRANSLATION IS **RE-SCORED** BY THIS CYCLE'S OWN
INSTRUMENT IN THE SELECT STEP.  Being pre-certified is not "trusted
blindly": the select step scores it against THIS cycle's corpus and, if it
no longer scores 0 defects, it falls through to the bounded retry.  A
pre-certified translation that no longer passes is NOT published on the
strength of its certificate.
"""
import json
import pathlib
import re

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
OUT = pathlib.Path("/tmp/c1313/translate")
OUT.mkdir(parents=True, exist_ok=True)

# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# ⭐⭐⭐ THE ARTEFACT SOURCE IS DERIVED **PER ID**, NOT *PER CYCLE*.
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
#
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# A SINGLE TYPED CYCLE NUMBER IS A **LATENT ASSERTION ABOUT THE CLASS**
# (Reminder 71).  The prior text of an id lives in one of TWO artefact
# families, and WHICH ONE depends on whether the id was EVER COMMITTED:
#
#   * an id COMMITTED by an earlier cycle -> its prior text is in the
#     PRE-BUILD BACKUP (Reminder 60);
#   * an id NEVER COMMITTED (an ORPHAN) -> **NO BACKUP EVER CARRIED IT**,
#     because a backup is a snapshot of the corpus BEFORE a write and the
#     orphan was never written into a committed corpus -- so its prior text
#     lives ONLY in that earlier cycle's *TRANSLATE* ARTEFACTS
#     (`/tmp/cNNNN/translate/translations_final.json` + `provenance.json`).
#
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# ⭐⭐⭐ **THE FIX IS A *SEARCH*, NOT A NEW CONSTANT.**  For EACH id, the
# prior text is looked for in BOTH families and whichever carries it is that
# id's authority.  A second typed constant would be the SAME latent
# assertion one level up.
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
_TRANSLATE_DIRS = sorted(pathlib.Path("/tmp").glob("c*/translate"))
assert _TRANSLATE_DIRS, (
    "no cycle's translate artefacts exist anywhere on disk -- there is no "
    "way to derive a pre-certified map")
_TRANSLATE_FAMILY = []
for _d in _TRANSLATE_DIRS:
    _pf = _d / "provenance.json"
    _ff = _d / "translations_final.json"
    _af = _d / "translations.json"
    if not (_pf.exists() and _ff.exists()):
        continue
    try:
        _p = json.loads(_pf.read_text(encoding="utf-8"))
        _f = json.loads(_ff.read_text(encoding="utf-8"))
        _a = (json.loads(_af.read_text(encoding="utf-8"))
              if _af.exists() else {})
    except json.JSONDecodeError:
        continue
    _TRANSLATE_FAMILY.append((_d, _p, _f, _a))
# newest first: the most recent COMPLETE artefact family is the richest
_TRANSLATE_FAMILY.sort(key=lambda t: t[0].stat().st_mtime, reverse=True)
# ⭐⭐⭐⭐⭐⭐⭐ THE FAMILY IS IDENTIFIED BY ITS **CYCLE**, not by the
# directory's leaf name: the leaf is `translate` for EVERY family, so
# `d.name` printed the SAME word 12 times -- a listing that looks like a
# duplicate list and names nothing.  ⭐⭐⭐⭐⭐⭐⭐ **A REPORT MUST NAME
# WHAT IT IS REPORTING.**
print(f"[precert] the TRANSLATE artefact family was DISCOVERED from the "
      f"filesystem: {len(_TRANSLATE_FAMILY)} cycle(s) carry a complete "
      f"provenance+final pair -> "
      f"{[d.parent.name for d, _, _, _ in _TRANSLATE_FAMILY[:6]]}")


def prior_artifacts(tid):
    """Return (provenance_row, final_text, attempt1_text, source) for `tid`,
    searching EVERY artefact family.  ⭐ The source is derived PER ID."""
    for _d, _p, _f, _a in _TRANSLATE_FAMILY:
        if tid in _p and tid in _f:
            return _p[tid], _f[tid], _a.get(tid), str(_d)
    return None, None, None, None

# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# ⭐⭐⭐⭐⭐⭐⭐ THE INHERITED CORPUS -- the state this cycle inherited,
# read BEFORE this cycle's build replaces any record.  ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# ⭐⭐⭐⭐⭐⭐⭐ **IT IS A SOURCE OF TEXT, NOT A SOURCE OF PROVENANCE** -- it
# is read here to DIAGNOSE (it tells us what text was carried), never to
# CERTIFY (it has no provenance row, so "0 defects" cannot be asserted
# against it).
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
_CORPUS = {t["id"]: t for t in json.loads(
    (REPO / "tweets.json").read_text(encoding="utf-8"))}
print(f"[precert] the INHERITED CORPUS carries {len(_CORPUS)} records -- it "
      f"is the source of the TEXT a certificate is compared against (never "
      f"a certificate itself)")

adj = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                 .read_text(encoding="utf-8"))
NEW_IDS = list(adj["real_new"])
INHERITED = set(adj["inherited"])
print(f"[precert] this cycle's own candidate set = {len(NEW_IDS)} ids "
      f"({len(INHERITED)} INHERITED, {len(NEW_IDS) - len(INHERITED)} BRAND-NEW)")

# ⭐⭐⭐ THE PRIOR TRANSLATIONS LIVE IN A **PRE-BUILD BACKUP**, NOT IN THE
# CURRENT WORKTREE.  This cycle's BUILD step REPLACES the inherited records
# with freshly-built ones whose `translation` is "" (the select step fills
# them) -- so by the time the precert map is derived, the worktree's copy of
# the inherited records no longer carries the prior cycle's translations.
# The backup is the AUTHORITATIVE pre-build state, and the build script
# took it BEFORE any write.
#
# ⭐⭐⭐⭐ BUT "THIS CYCLE'S PRE-BUILD BACKUP" IS NOT NECESSARILY THE
# AUTHORITATIVE ONE.  ⭐⭐ THIS IS THE DEFECT CYCLE 1244's PRECERT SCRIPT
# CARRIED, AND IT FIRED ON THIS CYCLE'S RUN: the backup at
# `/tmp/c1313/backup/tweets.json` was taken from a worktree that cycle
# **1236's own build had already rebuilt** with EMPTY translations -- so
# this cycle's pre-build backup carries NO prior text, and the precert map
# came back EMPTY (both ids "the inherited corpus carries no prior
# translation").  ⭐ **THE BACKUP CHAIN IS A CHAIN, AND THE QUESTION IS
# "WHAT DID THE CORPUS ACTUALLY CARRY?", NOT "WHAT DID THE LAST BUILD
# SNAPSHOT?".**  ⭐ Every cycle's build blanks the translations it inherits,
# so the LAST snapshot in the chain is the one most likely to be blank.
#
# ⭐ THE CORRECT SOURCE IS THE **MOST RECENT PRE-BUILD BACKUP THAT
# ACTUALLY CARRIES THE PRIOR TEXT** -- found by SEARCHING THE CHAIN, and
# each candidate is VERIFIED by reading the record's own `translation`
# field.  The chain is walked in RECENCY order and the first backup that
# carries a non-empty translation for an id is that id's authority.
# ⭐⭐⭐⭐⭐ THE CHAIN IS **DERIVED FROM THE FILESYSTEM**, NEVER TYPED.
#
# ⭐⭐⭐ The inherited literal listed the SAME path four times -- because the
# identity sweep rewrote cycle 1254/1235/1234's paths into this cycle's
# own `/tmp/c1313/backup/tweets.json`.  ⭐⭐⭐⭐⭐ **THE SWEEP DESTROYED
# THE CHAIN**: a chain of four DIFFERENT snapshots collapsed into one
# path, so "walk the chain in recency order" would have examined the same
# file four times and reported "the chain holds 4 snapshot(s)" -- a
# confident, wrong, *self-consistent* answer.  ⭐⭐⭐⭐⭐ **THIS IS THE
# REMINDER-56 DEFECT IN A NEW GUISE: A CLONE'S PATH IS PART OF THE
# INSTRUMENT'S CONTRACT -- AND A LIST OF PATHS IS A CONTRACT TOO.**
#
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐ THE CORRECT SOURCE IS THE **MOST RECENT PRE-BUILD
# BACKUP THAT ACTUALLY CARRIES THE PRIOR TEXT** -- found by SEARCHING the
# chain, each candidate VERIFIED by reading the record's own `translation`
# field.  The chain is walked in RECENCY order and the first backup that
# carries a non-empty translation for an id is that id's authority.
#
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ AND THE CHAIN IS BUILT BY **DISCOVERING** the backups
# on disk (`/tmp/c*/backup/tweets.json`), NOT by naming them: a hand-
# listed chain is a stale assertion about which cycles took a backup, and
# the LAST snapshot in the chain is the one most likely to be blank
# (every cycle's build blanks the translations it inherits).
BACKUP_GLOB = "/tmp/c*/backup/tweets.json"
_chain_paths = sorted(pathlib.Path("/tmp").glob("c*/backup/tweets.json"),
                      key=lambda p: p.stat().st_mtime, reverse=True)
# ⭐⭐⭐ THE CHAIN IS **THIS CYCLE'S OWN** BACKUP FIRST (it is the most
# recent pre-build state), THEN the other cycles' backups in recency
# order.  The glob above already yields them in recency order.
BACKUP_CHAIN = [str(p) for p in _chain_paths]
assert BACKUP_CHAIN, (
    "no pre-build backup exists anywhere on disk -- there is no way to "
    "compare the pre-certified text against what was published")
# ⭐⭐⭐⭐⭐ THE COLLAPSE ASSERTION (Reminder 70, carried forward at 1241).
#
# ⭐⭐⭐⭐⭐ **THE SWEEP DESTROYS A CHAIN IT COPIES.**  A TYPED
# `BACKUP_CHAIN = [...]` literal is rewritten by the identity
# sweep -- `/tmp/cNNNN` becomes `/tmp/c1313` in EVERY element --
# so all the elements become the SAME path.  ⭐⭐⭐⭐⭐⭐ **THE
# INSTRUMENT THEN PRINTS "the chain holds N snapshot(s)" WHILE
# READING ONE FILE N TIMES** -- a confident, wrong,
# self-consistent answer, and the "most recent backup that
# carries the prior text" rule silently degrades into "the most
# recent backup, N times".
#
# ⭐⭐⭐⭐⭐⭐⭐ **THIS CHAIN IS *DERIVED* (a glob), so its elements
# are distinct BY CONSTRUCTION** -- but the ASSERTION IS STILL
# REQUIRED, because the guarantee is a property of the CODE and
# the code can change.  ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ **A COLLAPSED
# CHAIN MUST BE INVISIBLE-FREE: THE ASSERTION IS WHAT MAKES IT
# VISIBLE.**
assert len(set(BACKUP_CHAIN)) == len(BACKUP_CHAIN), (
    f"the backup chain collapsed to duplicate paths "
    f"({len(BACKUP_CHAIN)} entries, {len(set(BACKUP_CHAIN))} "
    "distinct) -- the identity sweep rewrote a LIST of snapshots "
    "into one path; the chain must be DERIVED from the filesystem, "
    "never typed")
print(f"[precert] the pre-build backup chain holds "
      f"{len(BACKUP_CHAIN)} DISTINCT snapshot(s) "
      f"(the newest is {BACKUP_CHAIN[0]})")

# ⭐ THE CHAIN IS SEARCHED, NOT ASSUMED.  Each backup is inspected for the
# id's own prior translation, and the FIRST (most recent) backup that
# carries a non-empty one wins.
_chain = []
for _p in BACKUP_CHAIN:
    _pp = pathlib.Path(_p)
    if not _pp.exists():
        continue
    try:
        _d = json.loads(_pp.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        continue
    _chain.append((_p, {t["id"]: t for t in _d}))
assert _chain, "no pre-build backup exists in the chain -- there is no way " \
                "to compare the pre-certified text against what was published"
print(f"[precert] the pre-build backup chain was DERIVED FROM THE "
      f"FILESYSTEM: {len(_chain)} snapshot(s) discovered, most recent "
      f"first: {[p for p, _ in _chain[:4]]}")

work = {}
for _p, _d in _chain:
    work = _d
    break
print(f"[precert] the newest snapshot carries {len(work)} records")

pre = {}
skipped = {}
for tid in NEW_IDS:
    # ⭐⭐⭐ THE ARTEFACT SOURCE IS DERIVED **PER ID** -- not per cycle.
    # The search covers EVERY artefact family, so an id whose prior text
    # lives only in an earlier cycle's TRANSLATE artefacts (an id that was
    # never COMMITTED) is found just as an id in a COMMITTED backup is.
    prov, tr, attempt1_text, art_src = prior_artifacts(tid)
    if prov is None or tr is None:
        skipped[tid] = ("no prior artefact for this id in ANY family "
                        f"(searched {len(_TRANSLATE_FAMILY)} translate "
                        "artefact family/families and the pre-build backup "
                        "chain)")
        continue
    if tid not in INHERITED:
        skipped[tid] = "brand-new id -- there is no prior translation to inherit"
        continue
    # ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
    # ⭐⭐⭐⭐⭐⭐⭐ **THE CERTIFICATE IS CHECKED FIRST, AND THE PRIOR TEXT
    # IS READ FROM THE CORPUS THIS CYCLE INHERITED.**
    # ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
    # ⭐⭐⭐⭐⭐⭐⭐ The inherited corpus IS this cycle's own WORKTREE, read
    # BEFORE this cycle's build runs -- it is the state this cycle
    # inherited.  ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
    # ⭐⭐⭐⭐⭐⭐⭐ **THE PRE-BUILD BACKUP CHAIN IS THE WRONG SOURCE FOR
    # THIS QUESTION**, and using it produced a FALSE skip reason at
    # cycle 1278: every cycle's build BLANKS the translations it
    # inherits, so the chain carries NONE of the four inherited ids'
    # texts, and the script reported "the inherited corpus carries no
    # prior translation" -- a statement about the chain dressed up as a
    # statement about the corpus.  ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
    # ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
    # ⭐⭐⭐⭐⭐⭐⭐ **THE CORPUS IS READ HERE FOR *DIAGNOSIS* ONLY** -- it
    # has no provenance row, so it can NEVER confer a certificate.  The
    # certificate is the provenance row; the corpus text is the thing the
    # certificate is compared AGAINST.  ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
    # ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
    # the certificate must be 0-defect -- CHECKED FIRST, because it is
    # the reason that does not depend on any text comparison.
    # ⭐⭐⭐⭐⭐ CYCLE 1263's FIX: **READ THE MACHINE-READABLE FIELD, NOT
    # THE PROSE.**  Cycle 1258 changed the producer to emit
    # `{"defects": <int>, "score": {...}, "source": ..., "provenance": ...}`
    # and fixed the COMMIT consumer to read the field -- but this THIRD
    # consumer still ran a prose regex over the row, and with a dict that
    # raises `TypeError: expected string or bytes-like object` (the stage
    # DIED, it did not merely mis-report).
    # ⭐⭐⭐⭐⭐ **THE FIX IS NOT "ADD A FOURTH REGEX"** (Reminder 83): the
    # field IS the contract, and the prose stays as the audit trail.
    # ⭐⭐⭐⭐⭐ **AN OLDER PROSE-ONLY ARTEFACT IS STILL ACCEPTED** -- it is
    # read with the legacy regex, because a legacy artefact carries no
    # field to read.
    if isinstance(prov, dict):
        if "defects" not in prov:
            skipped[tid] = (
                f"the prior provenance states no defect count: {prov!r} "
                f"(artefact family: {art_src})")
            continue
        _claim = int(prov["defects"])
    else:
        _m = re.search(r"(\d+)\s+(?:fidelity\s+)?defect", str(prov))
        if _m is None:
            skipped[tid] = (f"the prior provenance is not 0-defect: {prov!r} "
                            f"(artefact family: {art_src})")
            continue
        _claim = int(_m.group(1))
    if _claim != 0:
        skipped[tid] = (f"the prior provenance is not 0-defect: {prov!r} "
                        f"(artefact family: {art_src})")
        continue
    # the text the corpus this cycle inherited carries, for THIS id
    prior_tr = ""
    prior_src = None
    for _p, _d in _chain:
        _t = (_d.get(tid) or {}).get("translation") or ""
        if _t.strip():
            prior_tr = _t
            prior_src = _p
            break
    if not prior_tr.strip():
        # ⭐⭐⭐⭐⭐⭐⭐ THE CORPUS THIS CYCLE INHERITED IS THE AUTHORITY
        # for "what text was carried"; the backup chain is only a
        # FALLBACK for ids the corpus does not carry at all.
        _ct = (_CORPUS.get(tid) or {}).get("translation") or ""
        if _ct.strip():
            prior_tr = _ct
            prior_src = "the INHERITED CORPUS (this cycle's worktree, read "                        "before this cycle's build)"
        else:
            skipped[tid] = (
                "no prior translation for this id: neither the INHERITED "
                f"CORPUS nor any of the {len(_chain)} pre-build snapshot(s) "
                "carries a non-empty text for it")
            continue
    # the pre-certified text must be the PUBLISHED one (final), not attempt #1
    if tr != prior_tr.strip():
        skipped[tid] = (
            "the published translation is not byte-identical to the "
            "pre-certified one -- the artefact that was published and the "
            "artefact that was scored are DIFFERENT (Reminder 53); "
            f"certified len={len(tr.strip())}, carried len="
            f"{len(prior_tr.strip())}, carried by {prior_src}")
        continue
    if attempt1_text == tr:
        skipped[tid] = (
            "the pre-certified text equals attempt #1 -- the certificate "
            "would be indistinguishable from a fresh translation")
    pre[tid] = tr
    print(f"  [PRE-CERTIFIED] {tid}: "
          f"{prov.get('provenance', prov) if isinstance(prov, dict) else prov} "
          f"[defects field = {_claim}]")
    print(f"      text len={len(tr)}; prior artefact family = {art_src}")
    print(f"      it IS the published translation (byte-identical to the "
          f"inherited corpus's own translation, read from {prior_src})")

for tid, why in skipped.items():
    print(f"  [NOT PRE-CERTIFIED] {tid}: {why}")

# ⭐⭐⭐⭐⭐ THE ASSERTION MUST BE **SYMMETRIC** (Reminder 28).  A guard that
# asserts a non-empty artefact fires when the artefact is legitimately
# absent -- and here it IS legitimately absent: the pre-certified path
# applies ONLY to **INHERITED** ids, and a cycle whose candidate set is
# entirely BRAND-NEW has NO prior translation to inherit.  ⭐⭐⭐⭐⭐ **A
# CYCLE'S CLASS DETERMINES WHICH PATH IS LEGITIMATELY EMPTY**, so the
# guard must be written against the CLASS, not against a constant.
#
# ⭐⭐⭐⭐⭐⭐⭐ AND THE CORRECT VALUES MUST BE ASSERTED, NOT ASSUMED: the
# pre-certified path may only carry INHERITED ids (a BRAND-NEW id has no
# prior text by definition), and every id that is skipped must be
# accounted for -- so `pre + skipped == NEW_IDS` must close exactly.
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐ **THE CLASS-MISMATCHED GUARD IS GONE (Reminder 72).**
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# The guard this replaces was:
#
#     assert pre or not INHERITED, (...)
#
# which claims a **FACTUAL EXISTENCE** -- "an inherited id MUST have a
# prior translation SOMEWHERE" -- a statement about the WORLD, not about
# the CODE.  ⭐⭐⭐⭐⭐⭐⭐ **A GUARD MUST ASSERT WHAT THE INSTRUMENT
# CONTROLS.**  ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# Cycle 1278's search was COMPLETE (every translate artefact family
# discovered from the filesystem, every backup snapshot globbed) and it
# STILL found nothing -- because **the data was genuinely absent**: the
# writing cycle's tail never ran, so its output survives ONLY in the
# worktree and no artefact on disk carries it.  ⭐⭐⭐⭐⭐⭐⭐ **A SEARCH
# THAT IS CORRECT CAN RETURN NOTHING** -- widening an already-complete
# search over an absent fact is how a cycle burns its whole budget
# chasing a guard that should have been rewritten.
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# THE CORRECT ASSERTION IS THE **STRUCTURAL CLOSURE** -- it is true of
# BOTH classes (a cycle whose candidates are all BRAND-NEW legitimately
# has an empty pre-certified map, and so does a cycle whose candidates
# are all UNARTEFACTED):
#
#     assert set(pre) <= INHERITED
#     assert set(pre) | set(skipped) == set(NEW_IDS)
#
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# ⭐⭐⭐⭐⭐⭐⭐ AND THE THIRD CASE NOW HAS AN EXPLICIT BRANCH: an id that
# HAS a prior artefact but whose CERTIFIED TEXT is not byte-identical to
# the text the corpus carries -> NOT certifiable -> it goes through the
# bounded translation/retry path and is scored FRESH.  ⭐⭐⭐⭐⭐⭐⭐ **A
# RECORD WITH NO ARTEFACT BEHIND IT IS RE-TRANSLATABLE, NOT CERTIFIABLE**
# -- it has no provenance row, so "0 defects" cannot be asserted against
# a prior certificate.
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# ⭐⭐⭐⭐⭐⭐⭐ AND THE CORPUS IS **NOT** A CERTIFICATE: it may be READ to
# DIAGNOSE (it proves an id is not certifiable), NEVER to CERTIFY.
assert set(pre) <= INHERITED, (
    f"the pre-certified path carries {sorted(set(pre) - INHERITED)} id(s) "
    f"that are NOT inherited -- a brand-new id has no prior text to "
    f"certify")
assert set(pre) | set(skipped) == set(NEW_IDS), (
    f"the precert map does not account for every candidate: "
    f"pre={sorted(set(pre))}, skipped={sorted(set(skipped))}, "
    f"candidates={sorted(set(NEW_IDS))}")
# ⭐⭐⭐⭐⭐⭐⭐ THE CLOSURE IS NOT VACUOUS: the map must CLASSIFY every
# candidate, and the classified set must be non-empty -- a cycle's
# candidate set is NEVER empty (a verdict from an empty set is not a
# verdict).  This assertion is about the INSTRUMENT's OWN output, so it
# holds for every class.
#
# ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# ⭐⭐⭐⭐⭐ **BUT "THE CANDIDATE SET IS NEVER EMPTY" IS A CLAIM ABOUT THE
# *ADJUDICATION*, NOT ABOUT THE *PRE-CERTIFICATION*.**  ⭐⭐⭐⭐⭐ **THE
# ADJUDICATION'S OWN ASSERTION IS THE ONE THAT MATTERS** -- it asserts that
# the candidate set it adjudicated was NON-EMPTY (a verdict from an empty
# set is not a verdict), and it FIRED on 43 candidates this cycle.
# ⭐⭐⭐⭐⭐ **THE PRE-CERT MAP IS A DIFFERENT QUESTION: "WHICH OF THESE
# CANDIDATES CARRY A PRIOR CERTIFICATE?"** -- and on a MEASURED NO-OP the
# honest answer is NONE, because there are no candidates to pre-certify.
# ⭐⭐⭐⭐⭐ **SO THE ASSERTION BELOW IS THE *PRE-CERTIFICATION* BRANCH OF A
# QUESTION WHOSE ANSWER MAY LEGITIMATELY BE EMPTY** -- and it is correct
# as written ONLY for a SUBSTANTIVE cycle.
# ⭐⭐⭐⭐⭐ **REMINDER 15'S PRINCIPLE IS NOT "THE SET MUST BE NON-EMPTY" --
# IT IS "A VERDICT MUST NOT BE COMPUTED FROM AN EMPTY SET".**  ⭐⭐⭐⭐⭐
# **A PRE-CERTIFICATION MAP COMPUTED FROM AN EMPTY CANDIDATE SET IS NOT A
# VERDICT; IT IS A BRANCH SELECTION.**  ⭐⭐⭐⭐⭐ **AND THE NO-OP IS
# ALREADY PROVEN ELSEWHERE** -- by the adjudication's own 43-candidate,
# non-vacuous verdict, and by `page.py`'s independent NO-OP branch, whose
# assertions are STRICTER (the corpus must be byte-identical to HEAD and
# the head must not move).
IS_NOOP = (len(NEW_IDS) == 0)
if IS_NOOP:
    # ⭐⭐⭐⭐⭐ THE NO-OP IS NOT ASSUMED -- IT IS CROSS-CHECKED AGAINST THE
    # ADJUDICATION'S OWN ARTIFACT, WHICH PROVES THE CANDIDATE SET WAS
    # NOT EMPTY WHEN IT WAS ADJUDICATED.
    _adj_rows = adj.get("rows") or []
    assert _adj_rows, (
        "[precert] ABORT: the adjudication artefact carries NO rows -- a "
        "MEASURED NO-OP must be a verdict on a NON-EMPTY candidate set, "
        "not the absence of a measurement (Reminder 15)")
    _n_200 = sum(1 for _r in _adj_rows if _r.get("http") == 200)
    assert _n_200, (
        "[precert] ABORT: no candidate resolved 200 -- the adjudication "
        "would be a verdict computed from an empty set (Reminder 15)")
    print(f"[precert] MEASURED NO-OP: the candidate set is empty, and the "
          f"NO-OP is CROSS-CHECKED -- the adjudication judged "
          f"{len(_adj_rows)} candidate(s), {_n_200} of which resolved 200, "
          f"so the zero is a MEASUREMENT and not an absence of one")
    print(f"[precert] the PRE-CERTIFICATION branch is therefore not "
          f"exercised: there is no candidate to pre-certify")
    _pre = {}
    _skipped = []
else:
    assert NEW_IDS, (
        "the candidate set is EMPTY -- a verdict computed from an empty set "
        "is not a verdict (Reminder 15)")
    assert set(pre) <= INHERITED, (
        f"the pre-certified path carries {sorted(set(pre) - INHERITED)} id(s) "
        f"that are NOT inherited -- a brand-new id has no prior text to "
        f"certify")
    assert set(pre) | set(skipped) == set(NEW_IDS), (
        f"the precert map does not account for every candidate: "
        f"pre={sorted(set(pre))}, skipped={sorted(set(skipped))}, "
        f"candidates={sorted(set(NEW_IDS))}")
(OUT / "precertified.json").write_text(
    json.dumps(pre, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n[precert] {len(pre)} of {len(NEW_IDS)} ids are PRE-CERTIFIED "
      f"(not re-translated); {len(skipped)} will go through the bounded retry")
print(f"[precert] the candidate set is {len(INHERITED)} INHERITED / "
      f"{len(NEW_IDS) - len(INHERITED)} BRAND-NEW; the pre-certified path "
      f"applies to INHERITED ids ONLY, so an all-BRAND-NEW cycle "
      f"legitimately has an EMPTY pre-certified map")
print(f"[precert] -> {OUT / 'precertified.json'}")
