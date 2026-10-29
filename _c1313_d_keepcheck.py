#!/usr/bin/env python3
"""Cycle 1313 -- verify the house-noun keep-rates for the tokens in this
cycle's 5 originals, using the SAME instrument's own derivation."""
import json, re, subprocess
from collections import Counter

REPO = "/Users/taeyeon093.bot/elon-tweets"
corpus = json.loads(subprocess.run(["git", "show", "HEAD:tweets.json"],
                                    cwd=REPO, capture_output=True, text=True).stdout)


def words(text):
    t = re.sub(r"https?://\S+", " ", text)
    t = re.sub(r"@\w+", " ", t)
    return re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", t)


pair_total, pair_kept = Counter(), Counter()
for r in corpus:
    tr = set(w.lower() for w in words(r.get("translation") or ""))
    for w in set(w.lower() for w in words(r.get("original") or "")):
        pair_total[w] += 1
        if w in tr:
            pair_kept[w] += 1

print("TOKEN KEEP-RATES for this cycle's originals (>=5 occurrences):")
for tok in ["elon", "musk", "starlink", "beria", "grok", "ukraine",
            "russia", "supercomputer", "switchgear", "permits", "transformers",
            "supply", "chain", "fuel", "security", "casting", "machines",
            "residential", "priority", "community", "political", "power",
            "noise", "clean", "air", "land", "grid", "access", "normies",
            "lefties", "fascist", "prison", "insane", "vote", "money",
            "long", "press", "like", "send", "someone", "wild", "times",
            "true", "audacity", "europe", "billion", "oil", "gas", "war",
            "hundred", "thousand", "civilian", "early", "stage", "assistance",
            "meaningful", "first", "prolong", "killed", "same", "people",
            "lecture", "extend", "makes", "compute", "work", "anything",
            "missing", "trivial", "seemingly", "binds", "list", "fuller",
            "limitations", "buildout", "sites", "taken", "year", "marginal",
            "development", "site", "worse", "every", "suitable", "large",
            "lathes", "turning", "shafts", "cast", "fuel", "security"]:
    tot = pair_total.get(tok, 0)
    if tot < 5:
        continue
    kept = pair_kept.get(tok, 0)
    rate = kept / tot
    flag = "  <-- DROPPED-ELIGIBLE (rate>=0.80)" if rate >= 0.80 else ""
    if rate < 0.34:
        flag += "  <-- usually-translated (rate<0.34)"
    print(f"  {tok:16s} {kept:5d}/{tot:<5d} = {rate:.3f}{flag}")

print()
print("THE 5 TRANSLATIONS -- latin tokens they KEEP vs the originals' tokens:")
trs = json.load(open("/tmp/c1313/translate/translations_final.json"))
work = {t["id"]: t for t in json.load(open(f"{REPO}/tweets.json"))}
for tid, tr in trs.items():
    orig = work[tid]["original"]
    tw = set(w.lower() for w in words(tr))
    ow = set(w.lower() for w in words(orig))
    print("-" * 70)
    print(tid)
    # tokens the corpus KEEPS (>=0.80) that the translation dropped
    dropped = []
    for w in sorted(ow):
        tot = pair_total.get(w, 0)
        if tot < 5:
            continue
        rate = pair_kept.get(w, 0) / tot
        if rate >= 0.80 and w not in tw:
            dropped.append((w, f"{pair_kept.get(w,0)}/{tot}"))
    print("  DROPPED house nouns (kept by corpus, absent here):", dropped or "NONE")
    added = [w for w in sorted(tw)
             if w not in pair_kept or True]
    # show the latin words the translation actually keeps
    print("  latin words KEPT by the translation:",
          sorted(set(w for w in words(tr))))
