#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 890 byline-only orphan fixup -- 1 record (id=2108815681642741943).

Per cycle 272/286/287/889 codification: byline-only RTs that came through the
fetcher as bare strict-equal pass-through ('Elon Musk' = 'Elon Musk') get
overlaid with the placeholder `（轉推 Elon Musk 的貼文）`.

The fetcher at 16:08 CST Hour 08 UTC non-retry-eligible ran AFTER cycle 889
SUBSTANTIVE commit (16:05 CST) and populated 2 new records into tweets.json; 1
of them is a bare-byline 'Elon Musk' RT (id=2108815681642741943, created_at
2026-10-10T07:03:33.000Z, is_retweet=True) with strict-equal pass-through
translation. This fixup is applied BEFORE the cycle 890 commit per cycle 287
multi-ID pattern (1-ID batch this cycle).
"""
import json

REPO = "/Users/taeyeon093.bot/elon-tweets"
TARGET_IDS = {
    "2108815681642741943",  # "Elon Musk" byline-only RT, fetched_at 2026-10-10T16:08:15
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
