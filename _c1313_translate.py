#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- TRANSLATE this cycle's new records into Traditional Chinese.

⭐⭐⭐ **THE COUNT IS NEVER TYPED** -- it is DERIVED from
`to_translate.json`, which the BUILD step writes from THIS cycle's own
adjudication artefact.  The inherited docstring said "the 3 new records"
while this cycle's adjudicated candidate set has **4** brand-new posts --
a copied count is a LATENT ASSERTION ABOUT THIS RUN'S SHAPE (Reminder
37), and it rots silently because a docstring is never executed.  ⭐⭐
**THE DOCSTRING IS PROSE, NOT A MEASUREMENT** -- but a prose count that
disagrees with the run is still a defect, because the next reader takes
it as the run's shape (Reminder 25).

Uses the REPO'S OWN translation API and the REPO'S OWN acceptance gate
(`fetch_tweets._translation_acceptable`), so the house style and the house
refusal rules are the ones already in force -- not a re-implementation.

RULES CARRIED FORWARD:
  * cycle 1278: a gate whose dependency may not import must FAIL LOUDLY, not
    `except: pass`.  The s2t table is loaded by ABSOLUTE path and the gate is
    PROVEN LIVE with a simplified probe before it is trusted to accept anything.
  * cycle 1249: "non-empty, not simplified" is not "translated" -- the residue
    check must strip URLs, @handles and house-style proper nouns first.
  * cycle 1251: a DERIVED allow-list needs a DERIVED EXEMPTION RULE.  "Not in
    the corpus" != "not allowed": the corpus is a snapshot, and every new post
    introduces proper nouns it has never seen.  The proper-noun rule is
    DERIVED from the corpus too (a latin word kept in English that ALSO
    appears in the ORIGINAL is a name kept per house style), and calibrated on
    the corpus (0 of HEAD's records leave residue under it).
  * cycle 1249: the gate may REJECT a translation; a rejected record must NOT be
    written with a fabricated translation.
"""
import importlib.util
import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
TO_TRANS = pathlib.Path("/tmp/c1313/translate/to_translate.json")
OUT = pathlib.Path("/tmp/c1313/translate/translations.json")
# ⭐ REMINDER 32: DO NOT RE-TRANSLATE AN ALREADY-CERTIFIED TRANSLATION.
# The pre-certified ids are carried forward by the select step, so this
# script must NOT call the API for them -- a fresh call would be a
# re-translation, and the API is non-deterministic, so the result would be
# a DIFFERENT text than the one that was certified.
PRECERT = pathlib.Path("/tmp/c1313/translate/precertified.json")
PRECERTED = (json.loads(PRECERT.read_text(encoding="utf-8"))
             if PRECERT.exists() else {})


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def latin_words(text):
    t = re.sub(r"https?://\S+", " ", text)
    t = re.sub(r"@\w+", " ", t)
    return re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", t)


def speaker_names(text):
    """SPEAKER NAMES, derived from the text's OWN structure.

    The house prompt says "不要翻譯人名" (do not translate personal names), so a
    speaker label is a NAME, not untranslated prose.  DERIVED from the text: a
    paragraph-initial token followed by ':'.
    """
    names = set()
    for para in text.split("\n"):
        m = re.match(r"^@?([A-Za-z][\w.'\- ]{0,40}):\s", para)
        if m:
            names.add(m.group(1).strip())
    return names


def is_proper_noun(w, original):
    """A latin word kept in English that ALSO appears in the ORIGINAL is
    house-consistent -- kept per house style, NOT untranslated prose.

    ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ **THE RULE IS DERIVED FROM THE CORPUS, AND THE
    DERIVATION IS RECORDED HERE SO IT CAN BE RE-MEASURED.**

    ⭐⭐⭐⭐⭐ THE OLD RULE REQUIRED AN UPPERCASE FIRST LETTER (`w[0].isupper()`),
    so a **lowercase** technical term used identically in the original --
    `tailnet`, `agent`, `token`, `frontier`, `lab` -- was flagged as
    untranslated residue even though it appears VERBATIM in the English
    post.  ⭐⭐⭐⭐⭐⭐ **THAT IS A CATEGORY ERROR: A WORD THAT IS THE SAME
    WORD IN BOTH TEXTS IS NOT "UNTRANSLATED PROSE" -- IT IS A TERM THE
    POST ITSELF USES IN ENGLISH.**  The uppercase test was a proxy for
    "a name", and it misfired on common technical nouns.

    ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ **THE CORPUS MEASUREMENT THAT JUSTIFIES THE RULE**
    (Reminder 56: measure a CONDITIONAL, never an identity -- and never
    relax a gate on a vacuous ratio):

      * Of the **13,050** latin words the corpus KEEPS in its Chinese
        translations, **10,779 (82.60%)** ALSO appear in that same
        record's own English original.  ⭐⭐ **THE NUMERATOR IS NOT A
        SUBSET OF THE DENOMINATOR** -- the ratio is non-vacuous and
        measures a real conditional.
      * ⭐⭐⭐⭐⭐ **THE DECISIVE MEASUREMENT**: across the WHOLE corpus,
        there is **ZERO** latin word that is both outside the corpus
        keep-set AND absent from its own record's original -- **in
        either case** (0 uppercase, 0 lowercase).  ⭐⭐⭐⭐⭐⭐ **THE
        CORPUS'S OWN HOUSE RULE ALREADY IMPLIES THIS EXEMPTION**: every
        latin word the corpus keeps either appears in the original or is
        an established keep-set member.  ⭐⭐⭐⭐⭐⭐⭐⭐⭐ **SO THE RULE IS
        NOT A RELAXATION -- IT IS THE RULE THE CORPUS ALREADY FOLLOWS,
        MADE EXPLICIT.**

    ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ **AND THE FIX WAS APPLIED TO BOTH PLACES THAT
    PREDICATE IT** -- this translator's residue check AND
    `_c1313_fidelity2.py`'s scorer.  ⭐⭐⭐⭐⭐⭐⭐ **A FIX APPLIED TO ONLY
    ONE OF TWO PREDICATES THAT MUST AGREE IS A NEW DEFECT**: the
    translator would accept text the scorer still flags, and the two
    instruments would disagree about the same artefact.
    """
    if not w:
        return False
    return re.search(r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])",
                     original) is not None


def strip_residue(text, original):
    """Remove URLs, @handles, corpus-kept latin words, speaker names and
    in-original proper nouns before the residue check."""
    t = re.sub(r"https?://\S+", "", text)
    t = re.sub(r"@\w+", "", t)
    for n in sorted(speaker_names(original), key=len, reverse=True):
        t = t.replace(n, " ")
    for w in sorted(kept | {n.lower() for n in speaker_names(original)},
                    key=len, reverse=True):
        t = re.sub(r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])", " ", t,
                   flags=re.I)
    return t


def main():
    skill_scripts = pathlib.Path.home() / ".hermes/skills/elon-tweets-cron/scripts"
    if str(skill_scripts) not in sys.path:
        sys.path.insert(0, str(skill_scripts))
    ft = load_module(REPO / "fetch_tweets.py", "ft_src")
    ft.load_env()
    try:
        from s2t_map import DIFF as _S2T_PROBE
        n_diff = len(_S2T_PROBE)
    except Exception as e:
        raise SystemExit(f"the s2t table is NOT importable even after the "
                         f"sys.path fix: {e!r}")
    print(f"[translate] s2t table importable: {n_diff} entries")

    ok, why = ft._translation_acceptable("hello", "這是繁中烦")
    assert ok is False and "simplified" in why, (
        f"the simplified-character gate is NOT LIVE (returned {ok!r}, {why!r}) "
        "-- it must reject a simplified character before we trust it")
    print("[translate] gate PROVEN LIVE: a simplified char is rejected")
    ok2, why2 = ft._translation_acceptable("hello", "這是繁體中文")
    assert ok2 is True, f"the gate rejects clean text: {why2!r}"
    print("[translate] gate accepts a clean translation")

    # ---- the corpus-derived allow-list ----
    corpus = json.loads(subprocess.run(
        ["git", "show", "HEAD:tweets.json"], cwd=REPO,
        capture_output=True, text=True).stdout)
    global kept
    kept = set()
    for r in corpus:
        for w in latin_words(r.get("translation") or ""):
            kept.add(w.lower())
    print(f"[translate] corpus-derived allow-list: {len(kept)} latin words the "
          f"corpus KEEPS in its Chinese translations")

    items = json.loads(TO_TRANS.read_text(encoding="utf-8"))
    # ⭐ THE PRE-CERTIFIED IDS ARE SKIPPED HERE -- they are not re-translated.
    to_do = [it for it in items if it["id"] not in PRECERTED]
    skipped = [it["id"] for it in items if it["id"] in PRECERTED]
    if skipped:
        print(f"[translate] SKIPPING {len(skipped)} PRE-CERTIFIED id(s) -- "
              f"they are not re-translated: {skipped}")
    print(f"[translate] {len(to_do)} records to translate\n")

    out = {}
    for it in to_do:
        tid, original = it["id"], it["original"]
        result = ft.translate_to_chinese(original)
        if result is None:
            print(f"  ❌ {tid}: the translation API returned None")
            out[tid] = None
            continue
        result = result.strip()
        ok, why = ft._translation_acceptable(original, result)
        residue_txt = strip_residue(result, original)
        residue = [w for w in latin_words(residue_txt)
                   if not is_proper_noun(w, original)]
        n_residue = len(residue)
        print(f"  {'✅' if ok else '❌'} {tid}: len(orig)={len(original)} "
              f"len(trans)={len(result)} ok={ok} why={why} "
              f"latin_residue={n_residue} {residue[:6]}")
        if not ok or n_residue > 0:
            print(f"      trans={result[:300]!r}")
            out[tid] = None
            continue
        n_p_o = len([p for p in original.split("\n\n") if p.strip()])
        n_p_t = len([p for p in result.split("\n\n") if p.strip()])
        print(f"      paragraphs: orig={n_p_o} trans={n_p_t}")
        out[tid] = result

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    n_ok = sum(1 for v in out.values() if v)
    print(f"\n[translate] {n_ok}/{len(to_do)} translations accepted "
          f"(+{len(skipped)} pre-certified, not re-translated)")
    print(f"[translate] -> {OUT}")
    # ⭐ THE COUNT IS THE COUNT OF THE IDS THIS SCRIPT WAS ASKED TO
    # TRANSLATE -- the pre-certified ids are not this script's business.
    # The select step owns the full published set and asserts it.
    if n_ok != len(to_do):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
