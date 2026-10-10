#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 889 byline-only orphan fixup -- 2 records (id=2108779379455103133, id=2108813515003977798).

Per cycle 272/286/287/889 codification: byline-only RTs that came through the
fetcher as bare strict-equal pass-through ('Elon Musk' = 'Elon Musk') get
overlaid with the placeholder `（轉推 Elon Musk 的貼文）`.

The fetcher at 15:07 CST Hour 07 UTC non-retry-eligible ran AFTER cycle 888
NO-OP commit (15:04 CST) and populated 4 new records into tweets.json; 2 of
them are bare-byline 'Elon Musk' RTs with strict-equal pass-through translation.
This fixup is applied BEFORE the cycle 889 commit per cycle 287 multi-ID pattern.
"""
import json

REPO = "/Users/taeyeon093.bot/elon-tweets"
TARGET_IDS = {
    "2108779379455103133",  # "Elon Musk" byline-only
    "2108813515003977798",  # "Elon Musk" byline-only
}
PLACEHOLDER = "（轉推 Elon Musk 的貼文）"

with open(f"{REPO}/tweets.json") as f:
    data = json.load(f)

fixed = 0
for t in data:
    if t["id"] in TARGET_IDS:
        if t.get("translation") != PLACEHOLDER:
            t["translation"] = PLACEHOLDER
            fixed += 1
            print(f"  fixed id={t['id']} -> {PLACEHOLDER!r}")

with open(f"{REPO}/tweets.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"applied {fixed} byline-only fixup(s) (TARGET_IDS={len(TARGET_IDS)})")
