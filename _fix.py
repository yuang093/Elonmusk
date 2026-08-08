"""Targeted re-translation of truncated translations in tweets.json.

Used when the hourly fetch_tweets.py produced incomplete translations
(e.g. model hit max_tokens ceiling mid-sentence).  Re-runs translation
on those specific IDs only and persists tweets.json in place.

This is the lightweight version of the old _fix.py that the skill
describes — covers only the §25 BYLINE_ONLY + TRUNCATED cases for the
most recent batch (won't touch the 719 historical byline-only entries
that the deleted _fix.py used to clean).
"""
import json
import sys
import os

# Reuse the project's translation functions and prompts
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_tweets import translate_to_chinese, _call_translation_api, TRANSLATION_SYSTEM_PROMPT_STRICT

# IDs from this hour's batch with truncated translations
TRUNCATED_IDS = [
    "2085743491334738340",  # "Suicidal Empathy" — cut at 5 chars
    "2086102094524645839",  # Swedish police — ends with 量
]

# IDs that are byline-only (orig == "Elon Musk") — not really a translation
# failure, just X.com showing only the byline for some retweets.  Mark with
# a clear placeholder so the webpage renders nicely.
BYLINE_ONLY_IDS = [
    "2086103757478109372",
]


def main():
    path = "tweets.json"
    data = json.load(open(path))
    by_id = {t["id"]: t for t in data}

    fixed = 0
    for tid in TRUNCATED_IDS:
        t = by_id.get(tid)
        if not t:
            print(f"  ⚠️ ID {tid} not found, skipping")
            continue
        orig = t.get("original", "")
        old = t.get("translation", "")
        print(f"  🔧 Re-translating {tid} (was {len(old)} chars: {old[-40:]!r})")
        # Use the stricter prompt + higher token budget
        new = _call_translation_api(
            orig,
            TRANSLATION_SYSTEM_PROMPT_STRICT,
            max_tokens=1500,
            temperature=0.3,
        )
        if not new:
            print(f"     ❌ API returned None, keeping original translation")
            continue
        t["translation"] = new
        fixed += 1
        print(f"     ✅ {len(new)} chars: {new[:80]!r}…")

    for tid in BYLINE_ONLY_IDS:
        t = by_id.get(tid)
        if not t:
            continue
        t["translation"] = "【轉推 — X.com 僅顯示作者署名】"
        print(f"  🏷️  Marked byline-only {tid} with placeholder")

    if fixed or any(t["id"] in BYLINE_ONLY_IDS for t in data):
        json.dump(data, open(path, "w"), ensure_ascii=False, indent=2)
        print(f"  💾 Persisted tweets.json ({fixed} re-translated, "
              f"{len(BYLINE_ONLY_IDS)} byline-marked)")
    else:
        print("  ℹ️  Nothing changed")


if __name__ == "__main__":
    main()
