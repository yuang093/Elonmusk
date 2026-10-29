#!/usr/bin/env python3
"""Cycle 1313 triage: characterise the UNCOMMITTED tweets.json delta."""
import json, subprocess, collections, sys

REPO = "/Users/taeyeon093.bot/elon-tweets"

work = json.load(open(f"{REPO}/tweets.json"))
head_raw = subprocess.run(["git", "show", "HEAD:tweets.json"], cwd=REPO,
                          capture_output=True, text=True).stdout
head = json.loads(head_raw)

print("work records :", len(work))
print("head records :", len(head))

ids_work = [r["id"] for r in work]
ids_head = [r["id"] for r in head]
cnt_head = collections.Counter(ids_head)

new_ids = [i for i in ids_work if cnt_head.get(i, 0) == 0]
print("ids NOT in head (new) :", len(new_ids))
dupes = [i for i, c in collections.Counter(ids_work).items() if c > 1]
print("duplicate ids in work  :", len(dupes), dupes[:10])
print("head unique ids       :", len(set(ids_head)))

print("\n--- the new records, in work order ---")
for nid in new_ids:
    idxs = [k for k, v in enumerate(ids_work) if v == nid]
    rec = work[idxs[0]]
    print(f"idx={idxs} id={nid} created={rec.get('created_at')} "
          f"is_quote={rec.get('is_quote')} is_rt={rec.get('is_retweet')} "
          f"pinned={rec.get('pinned')} lang={rec.get('lang')}")
    print(f"   url       : {rec.get('url')}")
    print(f"   fetched_at: {rec.get('fetched_at')}")
    print(f"   metrics   : {rec.get('metrics')}")
    o = rec.get('original', '')
    t = rec.get('translation', '')
    print(f"   original  ({len(o)} ch): {o[:160]!r}")
    print(f"   translation({len(t)} ch): {t[:160]!r}")
    print(f"   transl==orig: {o == t}")
    print()

# head newest
print("--- head newest 3 ---")
for r in head[:3]:
    print(" ", r["id"], r.get("created_at"), r.get("url"))
print("--- head oldest 1 ---")
print(" ", head[-1]["id"], head[-1].get("created_at"))

# new ids vs head newest
print("\nhead newest id:", head[0]["id"], head[0].get("created_at"))
