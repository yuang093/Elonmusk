#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CYCLE 1299 -- RE-TRANSLATE THE ONE REJECTED RECORD (the strict-prompt path).

⭐⭐⭐⭐⭐ **THE SITUATION.**  `translate` accepted 3 of 4 records and REJECTED
one: `2115346748730380385`, whose translation carried the simplified char
`电` (in `电子郵件` ⇒ `電子郵件`).  ⇒ ⇒ **⇒ THE GATE DID ITS JOB** — the
simplified-char check is the house rule and it fired on a real defect.

⭐⭐⭐⭐⭐ **⇒ BUT THE STAGE HAS NO *RETRY* PATH** ⇒ ⇒ **⇒ ONE LLM SAMPLING
LOSS BLOCKS THE WHOLE PUBLISH.**  ⇒ ⇒ **⇒ THE FIX IS A *BOUNDED* RETRY
WITH THE STRICT PROMPT** (the same path the 3-hourly empty-translation
retry already uses) — **NOT A RELAXATION OF THE GATE.**

⭐⭐⭐⭐⭐ **THE DISCIPLINE (from the skill's own history):**
  * the gate is NEVER relaxed — the retried translation must pass the SAME
    `_translation_acceptable` check;
  * the retry is BOUNDED (a small number of attempts) — an unbounded retry
    loop is a hang;
  * the retry RE-MEASURES the result and REJECTS anything that still fails;
  * the output is written to the SAME `translations.json` the `select`
    stage reads, and the FILE is RE-READ FROM DISK afterwards ⇒ ⇒
    **⇒ RULE D: *the ARTEFACT, RE-READ FROM DISK, IS THE PROOF.***

⭐⭐⭐⭐⭐ **AND THE REJECTED TRANSLATION IS NOT SILENTLY DROPPED** — the
retry's every attempt is logged, and if the record still fails after the
bound, the script EXITS NON-ZERO so the publish is blocked (a partial
translation must never be published as if it were complete).
"""
import json
import pathlib
import sys

REPO = pathlib.Path("/Users/taeyeon093.bot/elon-tweets")
TRANS_DIR = pathlib.Path("/tmp/c1313/translate")
TO_TRANS = TRANS_DIR / "to_translate.json"
OUT = TRANS_DIR / "translations.json"

MAX_ATTEMPTS = 4
TARGET = "2115346748730380385"

sys.path.insert(0, str(REPO))


def load_module(path, name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None, (
        f"[retry] could not load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    # ⭐⭐⭐⭐⭐ THE `s2t_map` TABLE MUST BE IMPORTABLE *BEFORE* THE GATE IS
    # USED.  `fetch_tweets._translation_acceptable` does
    #     `try: from s2t_map import DIFF ... except Exception: pass`
    # ⇒ ⇒ **⇒ WHEN THE IMPORT FAILS, THE GATE SILENTLY *ALWAYS PASSES*.**
    # ⇒ ⇒ **⇒ THAT IS A *SILENT ZERO*, AND IT IS EXACTLY WHY THE
    # `translate` STAGE REJECTED A SIMPLIFIED CHAR THAT THIS SCRIPT'S OWN
    # FIRE-TEST SAYS THE GATE SHOULD CATCH.**
    # ⇒ ⇒ **⇒ THE FIX IS TO MAKE THE TABLE IMPORTABLE — NEVER TO RELAX THE
    # GATE.**  (And the fire-test below is what PROVES the gate is live.)
    skill_scripts = pathlib.Path.home() / ".hermes/skills/elon-tweets-cron/scripts"
    if str(skill_scripts) not in sys.path:
        sys.path.insert(0, str(skill_scripts))
    from s2t_map import DIFF as _S2T_PROBE
    print(f"[retry] the s2t table is importable: {len(_S2T_PROBE)} entries")

    ft = load_module(REPO / "fetch_tweets.py", "ft_src")
    ft.load_env()

    items = {it["id"]: it["original"] for it in
             json.loads(TO_TRANS.read_text(encoding="utf-8"))}
    cur = json.loads(OUT.read_text(encoding="utf-8"))

    # ---- the gate must be PROVEN LIVE before we trust it ----------------
    ok, why = ft._translation_acceptable("hello", "這是繁中烦")
    assert ok is False and "simplified" in why, (
        f"[retry] the simplified-character gate is NOT LIVE ({ok!r}, {why!r})")
    print("[retry] the simplified-character gate is PROVEN LIVE")

    # ---- which records are missing / rejected? --------------------------
    missing = [tid for tid in items if not cur.get(tid)]
    if not missing:
        print("[retry] nothing to retry -- every record already has an "
              "accepted translation")
        return 0
    print(f"[retry] {len(missing)} record(s) need a retry: {missing}")

    for tid in missing:
        original = items[tid]
        print()
        print(f"[retry] === {tid} (len(orig)={len(original)}) ===")
        accepted = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            # ⭐⭐⭐ THE STRICT PROMPT + A HIGHER TOKEN BUDGET (the same
            # path the 3-hourly empty-translation retry uses) — ⭐⭐⭐ THE
            # GATE IS NOT RELAXED, THE *REQUEST* IS.
            cand = ft._call_translation_api(
                original,
                ft.TRANSLATION_SYSTEM_PROMPT_STRICT,
                max_tokens=1500,
                temperature=0.3)
            if cand is None:
                print(f"  [retry] attempt {attempt}: the API returned None")
                continue
            cand = cand.strip()
            ok, why = ft._translation_acceptable(original, cand)
            print(f"  [retry] attempt {attempt}: ok={ok} why={why} "
                  f"len={len(cand)}")
            if not ok:
                print(f"           rejected translation: {cand[:160]!r}")
                continue
            accepted = cand
            break
        if accepted is None:
            print(f"[retry] ABORT: {tid} still fails the gate after "
                  f"{MAX_ATTEMPTS} attempts -- the publish is BLOCKED "
                  "(a partial translation must never be published as if it "
                  "were complete)")
            return 1
        cur[tid] = accepted
        print(f"  [retry] ACCEPTED: {tid} (len={len(accepted)})")

    # ---- WRITE, then RE-READ FROM DISK (Rule D) -------------------------
    OUT.write_text(json.dumps(cur, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    back = json.loads(OUT.read_text(encoding="utf-8"))
    assert set(back) == set(items), (
        f"[retry] the translations file does not cover the id set: "
        f"{sorted(set(back) ^ set(items))}")
    empty = [tid for tid, v in back.items() if not (v or "").strip()]
    assert not empty, f"[retry] these ids have an EMPTY translation: {empty}"
    print()
    print(f"[retry] RE-READ FROM DISK: {len(back)} ids, 0 empty "
          f"(the ARTEFACT is the proof)")
    for tid, v in back.items():
        print(f"    {tid}: len={len(v)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
