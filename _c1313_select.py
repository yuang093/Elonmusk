#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 1313 -- SELECT the translation for each of THIS cycle's new records.

⭐⭐⭐ **THE COUNT IS NEVER TYPED** -- the loop is driven by `NEW_IDS`,
which comes from THIS cycle's own adjudication artefact, and the final
count assertion compares against `len(NEW_IDS)` -- the run's OWN candidate
set, never a subset of it (Reminder 61).  ⭐⭐⭐⭐⭐ **THE LOOP'S DRIVER
MUST BE THE RUN'S OWN CANDIDATE SET, NOT A SUBSET OF IT** -- otherwise a
row whose output was deliberately skipped (the pre-certified branch) is
silently absent from the result, and the result looks complete because it
is internally consistent.  ⭐⭐ The inherited docstring said "the 2 new
records" while this cycle's candidate set has **4** -- a copied count is a
latent assertion about this run's shape (Reminder 37).

⭐ TWO PATHS, CHOSEN BY THE ARTEFACTS:

  A. **PRE-CERTIFIED** (Reminder 32: DO NOT RE-TRANSLATE AN ALREADY-CERTIFIED
     TRANSLATION).  The id's prior provenance is 0-defect AND the text is
     byte-identical to what the corpus actually carried -> the text is
     REUSED.  ⭐ BUT IT IS **RE-SCORED BY THIS CYCLE'S OWN INSTRUMENT**:
     being pre-certified is not "trusted blindly".  If it no longer scores
     0 defects against THIS cycle's corpus, it falls through to the bounded
     retry.  (Reminder 53: the instrument must score the ARTEFACT THAT WAS
     PUBLISHED, and the published artefact here is `translations_final.json`
     from cycle 1278 -- NOT `translations.json`, which is attempt #1.)

  B. **BOUNDED RETRY** -- fresh translation, scored, retried up to
     MAX_ATTEMPTS.  The best-scoring candidate that PASSES THE ACCEPTANCE
     GATE wins; a record that cannot reach 0 defects keeps the best gated
     candidate and the defect count is RECORDED, never silently dropped.

THE INSTRUMENT MUST BE PROVED ABLE TO FIRE (cycle 1278 RULE 4): it is
exercised against a KNOWN-BAD translation and must report the dropped
token, and against a known-good one, and must report 0.  An instrument that
reports 0 for everything proves nothing.

⭐ AND THE INSTRUMENT MUST BE **THIS CYCLE'S OWN** (Reminder 56: an
instrument's identity is part of its contract).  A stale load reads
ANOTHER cycle's paths, so its scores describe a DIFFERENT artefact than the
one published.
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
CYCLE = "1313"
TR_PATH = pathlib.Path("/tmp/c1313/translate/translations.json")
PRECERT = pathlib.Path("/tmp/c1313/translate/precertified.json")
OUT = pathlib.Path("/tmp/c1313/translate/translations_final.json")
MAX_ATTEMPTS = 4
# ⭐ REMINDER 24: the candidate set is DERIVED from this cycle's own
# adjudication artefact -- never inherited, never typed.
_ADJ = json.loads(pathlib.Path("/tmp/c1313/adjudicate/verdicts.json")
                   .read_text(encoding="utf-8"))
NEW_IDS = list(_ADJ["real_new"])


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    sys.path.insert(0, str(pathlib.Path.home()
                           / ".hermes/skills/elon-tweets-cron/scripts"))
    # ⭐ THE INSTRUMENT MUST BE THIS CYCLE'S OWN.
    fid = load_module(REPO / f"_c{CYCLE}_fidelity2.py", "fid2")
    ft = load_module(REPO / "fetch_tweets.py", "ft_src")
    ft.load_env()

    corpus = json.loads(subprocess.run(
        ["git", "show", "HEAD:tweets.json"], cwd=REPO,
        capture_output=True, text=True).stdout)
    keep, pair_total, pair_kept = fid.build_corpus_stats(corpus)

    # ⭐ THE ORIGINALS come from the WORKTREE (this cycle's own build).
    work = {t["id"]: t for t in json.loads(
        (REPO / "tweets.json").read_text(encoding="utf-8"))}
    precert = json.loads(PRECERT.read_text(encoding="utf-8"))
    # the fresh-translation attempt-1 file may not exist for a pre-certified
    # id (it is not translated at all) -- so it is read if present.
    cur = json.loads(TR_PATH.read_text(encoding="utf-8")) if TR_PATH.exists() else {}

    # ---- the gate must be LIVE before it is trusted ----
    ok, why = ft._translation_acceptable("hello", "這是繁中烦")
    assert ok is False and "simplified" in why, "the acceptance gate is NOT live"
    ok2, why2 = ft._translation_acceptable("hello", "這是繁體中文")
    assert ok2 is True, f"the gate rejects clean text: {why2!r}"
    print("[sel] acceptance gate PROVEN LIVE (rejects simplified, accepts clean)")

    # ⭐ THE INSTRUMENT MUST BE PROVED ABLE TO FIRE.
    KNOWN_BAD_ORIG = ("Another 27 Starlink satellites\n\n"
                      "Falcon 9 launches 27 @Starlink satellites from California")
    KNOWN_BAD = "又有 27 顆星鏈衛星\n\n獵鷹 9 號從加州發射 27 顆衛星"
    sb = fid.score(KNOWN_BAD, KNOWN_BAD_ORIG, keep, pair_total, pair_kept)
    print(f"[sel] instrument FIRE-TEST on a KNOWN-BAD translation: "
          f"defects={sb['defects']} dropped={sb['dropped']}")
    assert sb["defects"] > 0, (
        "the fidelity instrument reports 0 on a KNOWN-BAD translation -- it "
        "cannot see the defect, so its verdict on the real records is vacuous")
    KNOWN_GOOD = "又有 27 顆 Starlink 衛星\n\nFalcon 9 從加州發射 27 顆衛星"
    sg = fid.score(KNOWN_GOOD, KNOWN_BAD_ORIG, keep, pair_total, pair_kept)
    print(f"[sel] instrument FIRE-TEST on a KNOWN-GOOD translation: "
          f"defects={sg['defects']}")
    assert sg["defects"] == 0, (
        f"the fidelity instrument flags a KNOWN-GOOD translation: {sg}")
    print("[sel] the instrument is PROVED ABLE TO FIRE in both directions")

    final = {}
    provenance = {}

    for tid in NEW_IDS:
        assert tid in work, f"{tid} is not in the worktree corpus"
        orig = work[tid]["original"]

        # ══════════ PATH A: PRE-CERTIFIED ══════════
        if tid in precert:
            text = precert[tid]
            sc = fid.score(text, orig, keep, pair_total, pair_kept)
            okc, whyc = ft._translation_acceptable(orig, text)
            print(f"\n{tid}")
            print(f"  PRE-CERTIFIED (1229/1232 rule: do NOT re-translate): "
                  f"defects={sc['defects']} added={sc['added']} "
                  f"dropped={sc['dropped']} bad_rate={sc['bad_keep_rate']} "
                  f"gate_ok={okc} {whyc}")
            if okc and sc["defects"] == 0:
                final[tid] = text
                provenance[tid] = {
                    "defects": int(sc["defects"]),
                    "score": {"added": list(sc["added"]),
                              "dropped": [list(d) for d in sc["dropped"]],
                              "bad_keep_rate": [list(b) for b in
                                                sc["bad_keep_rate"]]},
                    "source": "PRE-CERTIFIED",
                    "provenance": (
                        "PRE-CERTIFIED (carried forward from an earlier "
                        "cycle's 0-defect selection; RE-SCORED by this "
                        "cycle's own instrument against this cycle's corpus "
                        "and still 0 defects, and re-accepted by the live "
                        "gate -- NOT re-translated)"),
                }
                print("  => REUSED (re-scored, still 0 defects) -- not "
                      "re-translated")
                continue
            print("  => the pre-certified text no longer scores 0 defects / "
                  "no longer passes the gate -- it falls through to the "
                  "bounded retry")
            cands = [("precertified", text, sc, okc)]
        else:
            # ══════════ PATH B: BOUNDED RETRY ══════════
            _cur = cur.get(tid)
            print(f"\n{tid}")
            if not isinstance(_cur, str) or not _cur.strip():
                print("  NEW(1229)  : REJECTED by the live gate on attempt 1 "
                      "(no usable candidate) -- falling through to the "
                      "bounded retry")
                sc = {"defects": 99, "added": [], "dropped": [],
                      "bad_keep_rate": [], "paras_orig": 0, "paras_trans": 0,
                      "para_delta": 0}
                okc, whyc = False, "rejected on attempt 1"
            else:
                sc = fid.score(_cur, orig, keep, pair_total, pair_kept)
                okc, whyc = ft._translation_acceptable(orig, _cur)
                print(f"  NEW(1229)  : defects={sc['defects']} "
                      f"added={sc['added']} dropped={sc['dropped']} "
                      f"bad_rate={sc['bad_keep_rate']} gate_ok={okc} {whyc}")
            cands = [("new_1229", _cur if isinstance(_cur, str) else "",
                      sc, okc)]

        # ⭐⭐ THE KEPT BRANCH (Reminder 61: CARRYING A FEATURE FORWARD MEANS
        # CARRYING ITS CONTROL FLOW, NOT JUST ITS PLUMBING).
        # ⭐⭐ WITHOUT THIS BRANCH, A CANDIDATE THAT ALREADY SCORES 0 DEFECTS
        # IS PUT THROUGH THE BOUNDED RETRY ANYWAY -- and because the
        # translation API is NON-DETERMINISTIC, re-translating a text that
        # ALREADY PASSED is a DOWNGRADE RISK WITH NO UPSIDE: a re-translation
        # can score WORSE than the text that already scored 0.
        # ⭐⭐ THE KEPT TEXT IS THE CANDIDATE'S OWN, NOT `cur[tid]` -- on
        # PATH A the candidate is the PRE-CERTIFIED text, and `cur` does not
        # even carry that id.
        if okc and sc["defects"] == 0:
            _name, _text, _sc, _ = cands[0]
            final[tid] = _text
            provenance[tid] = {
                "defects": int(sc["defects"]),
                "score": {"added": list(sc["added"]),
                          "dropped": [list(d) for d in sc["dropped"]],
                          "bad_keep_rate": [list(b) for b in
                                            sc["bad_keep_rate"]]},
                "source": _name,
                "provenance": (f"{_name} translation; scored 0 "
                               "defects by the calibrated bidirectional "
                               "instrument and accepted by the live gate"),
            }
            print("  => KEPT this cycle's translation (0 defects)")
            continue

        # ---- RETRY (bounded) ----
        best = None
        for attempt in range(2, MAX_ATTEMPTS + 1):
            r = ft.translate_to_chinese(orig)
            if not r:
                continue
            r = r.strip()
            sr = fid.score(r, orig, keep, pair_total, pair_kept)
            okr, whyr = ft._translation_acceptable(orig, r)
            print(f"  RETRY #{attempt}: defects={sr['defects']} "
                  f"added={sr['added']} dropped={sr['dropped']} "
                  f"bad_rate={sr['bad_keep_rate']} gate_ok={okr} {whyr}")
            cands.append((f"retry{attempt}", r, sr, okr))
            if okr and sr["defects"] == 0:
                final[tid] = r
                provenance[tid] = {
                    "defects": int(sr["defects"]),
                    "score": {"added": list(sr["added"]),
                              "dropped": [list(d) for d in sr["dropped"]],
                              "bad_keep_rate": [list(b) for b in
                                                sr["bad_keep_rate"]]},
                    "source": f"RETRY #{attempt}",
                    "provenance": (
                        f"RETRY #{attempt} (this cycle); 0 defects"),
                }
                best = r
                break

        if best is None:
            # pick the best candidate by defects, but ONLY if it passes the
            # acceptance gate; a defective translation is NOT written.
            gated = [c for c in cands if c[3]]
            if not gated:
                raise SystemExit(f"{tid}: no candidate passes the acceptance "
                                 f"gate -- refuse to fabricate a translation")
            gated.sort(key=lambda c: c[2]["defects"])
            name, text, sc, _ = gated[0]
            print(f"  => no zero-defect candidate; keeping the best that "
                  f"PASSES THE GATE: {name} (defects={sc['defects']} "
                  f"{sc['added']} {sc['dropped']} {sc['bad_keep_rate']})")
            final[tid] = text
            provenance[tid] = {
                "defects": int(sc["defects"]),
                "score": {"added": list(sc["added"]),
                          "dropped": [list(d) for d in sc["dropped"]],
                          "bad_keep_rate": [list(b) for b in
                                            sc["bad_keep_rate"]]},
                "source": f"BEST-OF ({name})",
                "provenance": (f"BEST-OF ({name}); acceptance gate passed; "
                               f"{sc['defects']} fidelity defect(s) RECORDED"),
            }

    # ⭐ REMINDER 37: the count is DERIVED from the cycle's own candidate
    # set, never typed.
    assert len(final) == len(NEW_IDS), (
        f"expected {len(NEW_IDS)} translations, got {len(final)}")
    OUT.write_text(json.dumps(final, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    pathlib.Path("/tmp/c1313/translate/provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8")
    # ⭐⭐⭐⭐⭐ **THE PRODUCER ASSERTS ITS OWN ARTEFACT IS MACHINE-READABLE.**
    # A producer that silently emits prose has moved the defect DOWNSTREAM
    # to whichever consumer happens to parse it -- and there may be several
    # consumers.  So the producer asserts the contract HERE, at the point
    # where the artefact is created.
    for _tid, _p in provenance.items():
        assert isinstance(_p, dict), (
            f"[sel] the provenance for {_tid} is NOT a dict ({type(_p).__name__}"
            ") -- the defect count must be a machine-readable FIELD, never "
            "prose a consumer has to parse")
        assert "defects" in _p and isinstance(_p["defects"], int), (
            f"[sel] the provenance for {_tid} carries no integer `defects` "
            "field")
        assert "provenance" in _p and isinstance(_p["provenance"], str), (
            f"[sel] the provenance for {_tid} lost its human-readable trail")
    print("[sel] the provenance artefact is MACHINE-READABLE: every row "
          "carries an integer `defects` field AND its prose trail")
    print(f"\n[sel] {len(final)} translations selected -> {OUT}")
    for tid, p in provenance.items():
        print(f"   {tid}: {p}")


if __name__ == "__main__":
    main()
