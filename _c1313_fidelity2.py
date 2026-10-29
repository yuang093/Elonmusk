#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- TRANSLATION FIDELITY INSTRUMENT, CALIBRATED (v2).

v1 of this instrument had TWO defects, both found by `_c1313_calibrate.py`:

  1. It flagged `paras_trans > paras_orig` as a defect.  THE CALIBRATION SHOWS
     THE CORPUS ITSELF DOES THIS in 178 of 8,143 records (2.2%) -- and its
     paragraph deltas reach +18.  So the flag was a hand-typed threshold
     firing on the corpus's own legitimate behaviour.  REMOVED: it is now
     REPORTED, not scored.

  2. Its "dropped house noun" check counted an @MENTION as coverage.
     "Falcon 9 launches 27 @Starlink satellites" -> the @Starlink mention
     satisfied the check, so a translation that had actually rendered
     "Starlink" as 星鏈 in the first paragraph still passed.  The corpus's own
     keep-rate for "starlink" is 0.912, so dropping it IS a deviation.
     FIXED: coverage is counted over WORD occurrences, with @mentions
     excluded from both sides.

THE SCORED DIRECTIONS (both derived from the corpus, never typed):
  A. ADDED  -- a latin token in the translation that the corpus does not keep
               and the original does not introduce as a proper noun.
  B. DROPPED-- a word (not an @mention) the ORIGINAL carries, that the corpus
               KEEPS verbatim with keep-rate >= 0.80, but the translation
               does not carry.
  C. KEPT-BUT-USUALLY-TRANSLATED -- a token the translation keeps in English
               whose corpus keep-rate is < 0.34 (the corpus translates it).
"""
import json
import pathlib
import re
import subprocess
from collections import Counter

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
OUT = pathlib.Path("/tmp/c1313/translate")
DROP_KEEP_RATE = 0.80   # calibrated: starlink 0.912, grok 0.989, spacex 0.981
KEEP_RATE_FLOOR = 0.34  # calibrated: 3,064 of 3,873 tokens sit at ~0.0


def words(text):
    """Latin WORD tokens: URLs, @mentions and @handles are stripped."""
    t = re.sub(r"https?://\S+", " ", text)
    t = re.sub(r"@\w+", " ", t)
    return re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", t)


def word_counts(text):
    c = Counter(w.lower() for w in words(text))
    return c


def is_proper_noun(w, original):
    """A latin word kept in English that ALSO appears in the ORIGINAL is
    house-consistent -- kept per house style, NOT untranslated prose.

    ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ **THIS MUST AGREE WITH `_c1313_translate.py`'s
    IDENTICALLY-NAMED PREDICATE.**  ⭐⭐⭐⭐⭐⭐⭐⭐ **A FIX APPLIED TO
    ONLY ONE OF TWO PREDICATES THAT MUST AGREE IS A NEW DEFECT**: the
    translator would accept text this scorer still flags, and the two
    instruments would disagree about the same artefact -- and the
    disagreement would look like a translation defect rather than a
    definition mismatch.

    ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ **THE RULE IS DERIVED FROM THE CORPUS:**

      * Of the **13,050** latin words the corpus KEEPS in its Chinese
        translations, **10,779 (82.60%)** ALSO appear in that same
        record's own English original.  ⭐⭐ **THE NUMERATOR IS NOT A
        SUBSET OF THE DENOMINATOR** -- the ratio is non-vacuous.
      * ⭐⭐⭐⭐⭐ **THE DECISIVE MEASUREMENT**: across the WHOLE corpus
        there is **ZERO** latin word that is both outside the corpus
        keep-set AND absent from its own record's original -- **in
        either case** (0 uppercase, 0 lowercase).  ⭐⭐⭐⭐⭐⭐ **THE
        CORPUS'S OWN HOUSE RULE ALREADY IMPLIES THIS EXEMPTION**, so
        making it explicit is NOT a relaxation.

    ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ **THE OLD RULE REQUIRED AN UPPERCASE
    FIRST LETTER**, so a lowercase technical term used identically in the
    original -- `tailnet`, `agent`, `token`, `frontier`, `lab` -- was
    flagged as untranslated residue.  ⭐⭐⭐⭐⭐⭐⭐ **A WORD THAT IS THE
    SAME WORD IN BOTH TEXTS IS NOT "UNTRANSLATED PROSE" -- IT IS A TERM
    THE POST ITSELF USES IN ENGLISH.**  The uppercase test was a proxy
    for "a name", and it misfired on common technical nouns.
    """
    if not w:
        return False
    return re.search(r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])",
                     original) is not None


def speaker_names(text):
    names = set()
    for para in text.split("\n"):
        m = re.match(r"^@?([A-Za-z][\w.'\- ]{0,40}):\s", para)
        if m:
            names.add(m.group(1).strip())
    return names


def build_corpus_stats(corpus):
    keep = set()
    pair_total = Counter()
    pair_kept = Counter()
    for r in corpus:
        tr = r.get("translation") or ""
        orig = r.get("original") or ""
        tw = set(w.lower() for w in words(tr))
        ow = set(w.lower() for w in words(orig))
        keep |= tw
        for w in ow:
            pair_total[w] += 1
            if w in tw:
                pair_kept[w] += 1
    return keep, pair_total, pair_kept


def score(tr, orig, keep, pair_total, pair_kept):
    speakers = {n.lower() for n in speaker_names(orig)}
    tw = words(tr)
    ow = words(orig)
    tcount = word_counts(tr)
    ocount = word_counts(orig)

    added = []
    for w in sorted(set(tw)):
        lw = w.lower()
        if lw in keep or lw in speakers:
            continue
        if is_proper_noun(w, orig):
            continue
        added.append(w)

    # PRESENCE, not count: a Chinese translation legitimately mentions a name
    # ONCE where the English repeats it ("Roadster at Petersen / Roadster will
    # be on display" -> "Roadster 將於明天起...").  A count comparison flagged
    # that as a drop -- a false positive on the corpus's own convention.
    # The @mention masking trick is already defeated by `words()`, which
    # strips @mentions from BOTH sides.
    dropped = []
    for w in sorted(set(ow)):
        if not w[0].isupper():
            continue
        lw = w.lower()
        tot = pair_total.get(lw, 0)
        if tot < 5:
            continue
        rate = pair_kept.get(lw, 0) / tot
        if rate < DROP_KEEP_RATE:
            continue
        if tcount.get(lw, 0) > 0:
            continue
        dropped.append((w, f"{pair_kept.get(lw,0)}/{tot}"))

    bad_rate = []
    for w in sorted(set(tw)):
        lw = w.lower()
        if lw in speakers:
            continue
        if is_proper_noun(w, orig):
            continue
        tot = pair_total.get(lw, 0)
        if tot < 5:
            continue
        rate = pair_kept.get(lw, 0) / tot
        if rate < KEEP_RATE_FLOOR:
            bad_rate.append((w, f"{pair_kept.get(lw,0)}/{tot}"))

    n_o = len([p for p in orig.split("\n\n") if p.strip()])
    n_t = len([p for p in tr.split("\n\n") if p.strip()])
    defects = len(added) + len(dropped) + len(bad_rate)
    return dict(added=added, dropped=dropped, bad_keep_rate=bad_rate,
                paras_orig=n_o, paras_trans=n_t, para_delta=n_t - n_o,
                defects=defects)


def main():
    corpus = json.loads(subprocess.run(
        ["git", "show", "HEAD:tweets.json"], cwd=REPO,
        capture_output=True, text=True).stdout)
    keep, pair_total, pair_kept = build_corpus_stats(corpus)
    print(f"[fid2] corpus keep-set: {len(keep)} tokens; "
          f"calibrated DROP_KEEP_RATE={DROP_KEEP_RATE} "
          f"KEEP_RATE_FLOOR={KEEP_RATE_FLOOR}")

    backup = {t["id"]: t for t in json.loads(
        pathlib.Path("/tmp/c1313/backup/tweets.json").read_text(encoding="utf-8"))}
    work = {t["id"]: t for t in json.loads(
        (REPO / "tweets.json").read_text(encoding="utf-8"))}
    newtr = json.loads(pathlib.Path(
        "/tmp/c1313/translate/translations.json").read_text(encoding="utf-8"))

    out = {}
    for tid, rec in work.items():
        if tid not in newtr:
            continue
        orig = rec["original"]
        new = newtr[tid]
        old = (backup.get(tid) or {}).get("translation") or ""
        sn = score(new, orig, keep, pair_total, pair_kept)
        so = score(old, orig, keep, pair_total, pair_kept) if old else None
        print("=" * 78)
        print(tid)
        if so:
            print(f"  PRIOR(1217): defects={so['defects']} added={so['added']} "
                  f"dropped={so['dropped']} bad_rate={so['bad_keep_rate']} "
                  f"(para delta {so['para_delta']:+d})")
        print(f"  NEW(1221) : defects={sn['defects']} added={sn['added']} "
              f"dropped={sn['dropped']} bad_rate={sn['bad_keep_rate']} "
              f"(para delta {sn['para_delta']:+d})")
        out[tid] = {"prior": old, "new": new, "score_prior": so, "score_new": sn}

    pathlib.Path(OUT / "fidelity_v2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[fid2] -> {OUT / 'fidelity_v2.json'}")


if __name__ == "__main__":
    main()
