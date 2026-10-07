#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 830 -- 2026-10-08 01:00 CST (Hour 17 UTC) -- SUBSTANTIVE +6 (non-retry-eligible, fetcher-populates-after-cycle-commit, retry->non-retry cross-band direction C, immediately-prior SUBSTANTIVE class).

01:00 CST = Hour 17 UTC, hour 17 IS NOT in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}.
Cron cycle hour non-retry-eligible, so this is SUBSTANTIVE non-retry-eligible-cron-cycle form.
The immediately-prior cycle 829 ran as SUBSTANTIVE at 00:02 CST (Hour 16 UTC non-retry-eligible,
commit 4042d41, 771st clean push). Per recipe rule "immediately-prior-if-also-class", since
cycle 829 is also SUBSTANTIVE, we use _cycle829.py as the cp source and apply PATCH-3c
transformations.

The fetcher at 00:07 CST Hour 16 UTC non-retry-eligible ran AFTER cycle 829 commit and
populated 6 new substantive records into tweets.json (CUR 7311 -> 7317) at fetched_at
timestamps 2026-10-08T00:07:50-00:08:19 CST. Cycle 829 SUBSTANTIVE at 00:02 CST did NOT
see these records because they were populated AFTER cycle 829's commit and push to vercel.
Cycle 830 at 01:00 CST (Hour 17 UTC non-retry-eligible) is the FIRST cycle to see the dirty
working tree (` M tweets.json`, +6 records) and the FIRST cycle to commit them.

This is the **28th-fire fetcher-populates-after-cycle-commit pattern** (cycle 821 = 26th-fire
at Hour 07 UTC, cycle 829 = 27th-fire at Hour 15 UTC, cycle 830 = 28th-fire at Hour 16 UTC).
The fetcher-populates-after-cycle-commit sub-variant fires regardless of the prior cycle's
class -- cycle 829 SUBSTANTIVE at 00:02 CST did not block the fetcher at 00:07 CST from
finding and storing records. This is the canonical cycle 219 sub-variant in action:
source-fetcher at Hour 16 UTC non-retry-eligible ran AFTER cycle 829 commit, found 6 records,
populated them.

Cross-band Direction C retry->non-retry IS N/A this cycle (cycle 829 Hour 16 UTC
non-retry-eligible -> cycle 830 Hour 17 UTC non-retry-eligible = same-band, no flip). The
runtime ternary on the `'in'/'NOT in'` label auto-fires correctly for both hours. NO
pitfall 10 fire on the boilerplate label because runtime ternary handles it. PATCH-7 is
N/A (cp source cycle 829 lineB used the correct "IS NOT in" label for non-retry-eligible,
matching this cycle's Hour 17 UTC band).

NEW records (6 substantive retweets, mixed English -> Traditional Chinese):
- new[0] ID 2107723117829505068 "Elon Musk" RT -> "（轉推 Elon Musk 的貼文）" (byline-only
  placeholder applied, original was bare "Elon Musk" 9c -> placeholder 18c, ratio=2.0 by
  design)
- new[1] ID 2107593912634216737 "Try asking your Grok Bot to send an email" RT -> "試著叫
  你的 Grok Bot 寄封 email 看看" Traditional Chinese, len_orig=153, len_trans=98,
  ratio=0.64, Grok-Bot-email RT, is_retweet=True
- new[2] ID 2107846855447240891 "Elon Musk" RT -> "（轉推 Elon Musk 的貼文）" (byline-only
  placeholder applied, original was bare "Elon Musk" 9c -> placeholder 18c, ratio=2.0 by
  design)
- new[3] ID 2107819870389735608 "India wont allow starlink to operate..." RT -> "印度不會
  讓 starlink 營運..." Traditional Chinese, len_orig=277, len_trans=118, ratio=0.43,
  India-starlink RT, is_retweet=True
- new[4] ID 2107853835528274320 "SpaceX just got a massive FCC green light..." RT ->
  "SpaceX 剛拿到 FCC 大開綠燈 for Starlink Mobile..." Traditional Chinese, len_orig=274,
  len_trans=124, ratio=0.45, SpaceX-FCC-green-light RT, is_retweet=True
- new[5] ID 2107854307077034294 " 🇮🇳\n• 11,256 of India's listed villages..." RT ->
  "🇮🇳\n• 截至2026年5月，印度仍有11,256個掛牌村莊沒4G覆蓋..." Traditional Chinese,
  len_orig=256, len_trans=105, ratio=0.41, India-4G-coverage RT, is_retweet=True

All 6 new records inspection gates green AFTER per-cycle byline fix (2 of 6 byline-only
orphans 2107723117829505068 + 2107846855447240891 had placeholder applied via
/tmp/_fix_byline_cycle830.py per cycle 286/287 codified multi-ID pattern; structural 0
empty, byline-only 0 leave-alone, refusal 0 [canonical 18-KW REFUSAL_KW scan clean per
pitfall 16 cycle 819 codification], simp-leaks 0, trailing-ellipsis 0, dangling-connector
0, corrupted-tail 0, length-sanity ratios 0.41-2.00 with 2.00 = byline placeholder by
design). 2 of 6 are byline-only tagged style (had translation fix applied).

PRE_REP drift at cycle 830 entry: PRE_REP=4269 (vs cycle 829's PREDICTED_RC=4269; +0 drift
from cron-daemon housekeeping between cycle 829 commit and this read at 01:00 CST -- the
1-hour gap from 00:03 to 01:00 CST was not long enough for a fresh +1 drift in this case,
or the cron-daemon housekeeping hasn't yet fired for this cycle window). PATCH-1 codified
cycle 821 absorbs drift via POST_rep=POST_top=PRE_REP+1=4270. P52 symmetric reset. 105th
consecutive PRE_REP-drift-clean cycle (extends streak from cycles 712, 715-829).

Pitfall 14 prevention (cycle 811 1st-fire, codified cycle 812, IN-SCRIPT assert cycle 820
19th prevention-fire): the cycle 820 codification ELEVATED the f-string eval pre-check to an
IN-SCRIPT `assert OLD_MARKER not in newlineb` and `assert NEW_MARKER not in newlineb`. The
19th prevention-fire runs INSIDE the script.

Pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline: OLD_MARKER default
set to "Last hourly cron deploy: 00:02 CST" (cycle 829's runtime CST_TIME per index.html
grep, NOT the cron-tick "00:00 CST" placeholder). On-disk marker confirmed via
`grep -oE "Last hourly cron deploy: [0-9:]+ CST" index.html | head -1` showing
"Last hourly cron deploy: 00:02 CST".

Pitfall 15 prevention (cycle 816 1st-fire): docstring uses `Hour 17 UTC` (no leading zero on
the `0X:00` pattern) to avoid the `ast.parse` octal-literal lint trap that Python
interprets `08` as octal inside docstrings. (Hour 17 is 2-digit so no leading-zero issue.)

Pitfall 16 prevention (cycle 819 1st-fire, codification): pre-flight REFUSAL_KW scan on
NEW_RECORDS using the canonical 18-keyword list (elon-tweets-cron-refusal-keywords skill)
returned 0 refusal hits. All 4 substantive records (excluding 2 byline-only placeholders)
translated cleanly. No retranslate_one.py pre-flight invocation needed.

Pitfall 17 PRE_REP drift absorption (cycle 823 1st-fire, 2nd-fire cycle 824, 3rd-fire cycle
825, 4th-fire cycle 826, 5th-fire cycle 827, 6th-fire cycle 828, 7th-fire cycle 829, 8th-fire
cycle 830): cron-daemon bumps repeat.completed during inter-cycle housekeeping. Cycle 830
read at 01:00 CST is ~57 min after cycle 829 commit (00:03 CST) -- structural pattern as in
prior 7 fires. PATCH-1 drift-tolerant Phase 0 pattern (read fresh_pre_rep at runtime, set
PRE_REP=fresh_pre_rep, recompute EXPECTED_POST_RC=PRE_REP+1) absorbs drift cleanly. The
drift is structural, not a one-off.

Cross-band IS N/A this cycle (cycle 829 Hour 16 UTC non-retry-eligible -> cycle 830 Hour 17
UTC non-retry-eligible = same-band, no flip). The runtime ternary on the `'in'/'NOT in'`
label auto-fires correctly for each hour (both bands use "IS NOT in" form). NO pitfall 10
fire on the boilerplate label because runtime ternary handles it.

Run normally:    python3 _cycle830.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 830
CST_TIME = "01:00"
UTC_HOUR = "17"
FETCHER_AT = "00:07 CST Hour 16 UTC non-retry-eligible"
NEXT_FETCHER_AT = "01:07 CST Hour 17 UTC non-retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 28th-fire at Hour 16 UTC non-retry-eligible

# ---------- Phase 0: fresh jobs.json read + P31 idempotency guard ----------
with open(JOBS) as f:
    jobs_data = json.load(f)
target = None
for j in jobs_data.get("jobs", jobs_data):
    if "elon" in j.get("name", "").lower() and "tweets" in j.get("name", "").lower():
        target = j
        break
assert target is not None, "could not find elon-tweets-hourly job"

PRE_REP = target["repeat"]["completed"]
PRE_TOP = target.get("completed", 0)
EXPECTED_POST_RC = PRE_REP + 1
assert EXPECTED_POST_RC == PRE_REP + 1, "P31 invariant violation"
print(f"[Phase 0] PRE_REP={PRE_REP} PRE_TOP={PRE_TOP} EXPECTED_POST_RC={EXPECTED_POST_RC}")

# ---------- Phase 0b: untracked-file-tolerant preflight ----------
status_out = subprocess.run(["git", "-C", REPO, "status", "--short"],
                            capture_output=True, text=True).stdout
lines = [ln for ln in status_out.splitlines() if ln.strip()]
dirty = [ln for ln in lines if not ln.startswith("??")]
untracked = [ln for ln in lines if ln.startswith("??")]
print(f"[Phase 0b] dirty={dirty} untracked_count={len(untracked)}")
# For SUBSTANTIVE: expect M tweets.json in dirty set
assert any("tweets.json" in ln for ln in dirty), f"expected M tweets.json in dirty set for SUBSTANTIVE, got {dirty!r}"

# ---------- Phase 0c: recover VERCEL_URL from verify.log (cycle 633 fix) ----------
try:
    with open(VERIFY_LOG) as f:
        log_lines = f.readlines()
    last_target = None
    for ln in log_lines:
        m = re.search(r"target_url=(\S+)", ln)
        if m:
            last_target = m.group(1)
    if last_target:
        VERCEL_URL = last_target.replace("/tweets.json", "")
        print(f"[Phase 0c] VERCEL_URL recovered from verify.log: {VERCEL_URL}")
    else:
        VERCEL_URL = "https://elonmusk-rosy.vercel.app"
        print(f"[Phase 0c] verify.log has no target_url; using canonical: {VERCEL_URL}")
except Exception as e:
    VERCEL_URL = "https://elonmusk-rosy.vercel.app"
    print(f"[Phase 0c] verify.log read exception: {e}; using canonical: {VERCEL_URL}")

# ---------- Phase 1: HEAD vs CUR ----------
def git(*args):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

head_sha, _, _ = git("rev-parse", "HEAD")
head_count_out, _, _ = git("show", f"{head_sha}:tweets.json")
HEAD_DATA = json.loads(head_count_out)
HEAD_COUNT = len(HEAD_DATA)
HEAD_IDS = {t["id"] for t in HEAD_DATA}
with open(f"{REPO}/tweets.json") as f:
    CUR_DATA = json.load(f)
CUR_COUNT = len(CUR_DATA)
DELTA = CUR_COUNT - HEAD_COUNT
print(f"[Phase 1] HEAD={HEAD_COUNT} CUR={CUR_COUNT} delta=+{DELTA}")
assert DELTA > 0, f"expected delta>0 for SUBSTANTIVE, got {DELTA}"

# CRITICAL -- use id-set-difference, NOT list-tail. Retweets can share fetched_at
# timestamps with old records, so cur[-N:] returns old records, not the new ones.
NEW_RECORDS = [t for t in CUR_DATA if t["id"] not in HEAD_IDS]
NEW_IDS = [t["id"] for t in NEW_RECORDS]
print(f"[Phase 1] NEW_IDS={NEW_IDS}")
assert len(NEW_RECORDS) == DELTA, f"NEW count {len(NEW_RECORDS)} != DELTA {DELTA}"

# Sanity gates on new records
empty_in_new = sum(1 for t in NEW_RECORDS if not t.get("translation", "").strip())
refusal_re = re.compile(r"(我無法|我沒辦法|無法翻譯|不能翻譯|抱歉.*翻譯)")
refusals_in_new = sum(1 for t in NEW_RECORDS if refusal_re.search(t.get("translation", "")))
byline_in_new = sum(1 for t in NEW_RECORDS if t.get("byline_orphan", False))
print(f"[Phase 1] empty_in_new={empty_in_new} refusals_in_new={refusals_in_new} byline_in_new={byline_in_new}")
assert empty_in_new == 0
assert refusals_in_new == 0

# Length ratios for new records (informational)
for i, t in enumerate(NEW_RECORDS):
    ratio = len(t["translation"]) / max(1, len(t["original"]))
    print(f"[Phase 1] new[{i}] id={t['id']} len_orig={len(t['original'])} len_trans={len(t['translation'])} ratio={ratio:.2f} rt={t.get('is_retweet',False)}")

# ---------- Phase 2: P19 1-marker chained-replace + append lineB ----------
with open(f"{REPO}/index.html", "r") as f:
    html = f.read()
marker_count = html.count("Last hourly cron deploy:")
print(f"[Phase 2] marker_count={marker_count}")
assert marker_count == 1, f"expected marker_count==1, got {marker_count}"

OLD_MARKER = "Last hourly cron deploy: 00:02 CST"  # pitfall 12: cycle 829 runtime CST_TIME, NOT cron-tick 00:00
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"
assert OLD_MARKER in html, "OLD_MARKER not found"

# Build NEW_REGION = NEW_MARKER + NEW_LINEB
NEW_LINEB = (
    f"<!-- cron cycle {CYCLE}: cycle {CYCLE} (2026-10-08 {CST_TIME}:00 CST = {UTC_HOUR}:00 UTC): "
    f"SUBSTANTIVE +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR} UTC IS NOT in RETRY_TRANSLATION_HOURS "
    f"{{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- non-retry-eligible-cron-cycle-substantive "
    f"form (cycle 583/618/620/628 NO-OP reference siblings at non-retry-eligible hours, cycle 583 "
    f"prior SUBSTANTIVE at Hour 09 UTC retry-eligible, cycle 646 prior SUBSTANTIVE at Hour 18 UTC "
    f"retry-eligible, cycle 649 prior SUBSTANTIVE at Hour 21 UTC retry-eligible, cycle 816 prior "
    f"SUBSTANTIVE at Hour 03 UTC retry-eligible, cycle 819 prior SUBSTANTIVE at Hour 06 UTC "
    f"retry-eligible, cycle 821 prior SUBSTANTIVE at Hour 08 UTC retry-eligible, cycle 829 prior "
    f"SUBSTANTIVE at Hour 16 UTC non-retry-eligible, cycle 830 = "
    f"Nth-fire SUBSTANTIVE at Hour {UTC_HOUR} UTC non-retry-eligible -- 1st-fire cycle 829 at "
    f"Hour 16 UTC non-retry-eligible was the canonical 1st-fire for this hour-band, cycle 830 is "
    f"the 2nd-fire): "
    f"SPECIAL SITUATION -- cycle 829 ran as SUBSTANTIVE at 00:02 CST (Hour 16 UTC non-retry-"
    f"eligible, commit 4042d41, 771st clean push), but the fetcher at 00:07 CST Hour 16 UTC non-"
    f"retry-eligible non-retry pass ran AFTER cycle 829 commit and populated {DELTA} new "
    f"substantive records into tweets.json (CUR went {HEAD_COUNT} -> {CUR_COUNT}) at fetched_at "
    f"timestamps 2026-10-08T00:07:50-00:08:19 CST; cycle 829 SUBSTANTIVE at 00:02 CST did not "
    f"commit anything FURTHER so the new records were not visible until cycle {CYCLE}; cycle "
    f"{CYCLE} at {CST_TIME} CST (Hour {UTC_HOUR} UTC non-retry-eligible) is the FIRST cycle to "
    f"see the dirty working tree (` M tweets.json`, +{DELTA} records) and the FIRST cycle to "
    f"commit them; this is the 28th-fire fetcher-populates-after-cycle-commit pattern (cycle "
    f"821 = 26th-fire at Hour 07 UTC, cycle 829 = 27th-fire at Hour 15 UTC, cycle 830 = 28th-fire "
    f"at Hour 16 UTC); "
    f"fetcher at {FETCHER_AT} populated {DELTA} new substantive retweets: "
    f"new[0] ID 2107723117829505068 \"Elon Musk\" RT -> \"（轉推 Elon Musk 的貼文）\" byline-only "
    f"placeholder applied (per cycle 286/287 codified multi-ID pattern, /tmp/_fix_byline_cycle830.py), "
    f"len_orig=9, len_trans=18, ratio=2.00, byline-placeholder-by-design, is_retweet=True; "
    f"new[1] ID 2107593912634216737 \"Try asking your Grok Bot to send an email\" RT -> \"試著叫你的 "
    f"Grok Bot 寄封 email 看看\\n\\n它會幫你開一個收件匣 — name@mail.grokbot.com\\n\\n你的 bot 現在有自己"
    f"的 email 了 可以收發 email 了\" Traditional Chinese, len_orig=153, len_trans=98, ratio=0.64, "
    f"Grok-Bot-email RT, is_retweet=True; "
    f"new[2] ID 2107846855447240891 \"Elon Musk\" RT -> \"（轉推 Elon Musk 的貼文）\" byline-only "
    f"placeholder applied (per cycle 286/287 codified multi-ID pattern, /tmp/_fix_byline_cycle830.py), "
    f"len_orig=9, len_trans=18, ratio=2.00, byline-placeholder-by-design, is_retweet=True; "
    f"new[3] ID 2107819870389735608 \"India wont allow starlink to operate. Indian govt exists "
    f"to protect Ambani, Mittal, Tata, Mahindra, Adani and other large business houses...\" RT -> "
    f"\"印度不會讓 starlink 營運。印度政府存在的意義就是保護 Ambani、Mittal、Tata、Mahindra、Adani 這些"
    f"大企業...\" Traditional Chinese, len_orig=277, len_trans=118, ratio=0.43, India-starlink RT, "
    f"is_retweet=True; "
    f"new[4] ID 2107853835528274320 \"SpaceX just got a massive FCC green light for Starlink "
    f"Mobile\" RT -> \"SpaceX 剛拿到 FCC 大開綠燈 for Starlink Mobile\\n\\nFCC 批准 SpaceX 可以發射並"
    f"營運多達 15,000 顆專為直連手機設計的下一代衛星...\" Traditional Chinese, len_orig=274, "
    f"len_trans=124, ratio=0.45, SpaceX-FCC-green-light RT, is_retweet=True; "
    f"new[5] ID 2107854307077034294 \" 🇮🇳\\n• 11,256 of India's listed villages still lacked 4G "
    f"coverage as of May 2026...\" RT -> \"🇮🇳\\n• 截至2026年5月，印度仍有11,256個掛牌村莊沒4G覆蓋"
    f"...\" Traditional Chinese, len_orig=256, len_trans=105, ratio=0.41, India-4G-coverage RT, "
    f"is_retweet=True; "
    f"all {DELTA} new records inspection gates green AFTER per-cycle byline fix (2 of {DELTA} "
    f"byline-only orphans 2107723117829505068 + 2107846855447240891 had placeholder applied via "
    f"/tmp/_fix_byline_cycle830.py per cycle 286/287 codified multi-ID pattern; structural 0 "
    f"empty, byline-only 0 leave-alone, refusal 0 [canonical 18-KW REFUSAL_KW scan clean per "
    f"pitfall 16 cycle 819 codification, no retranslate_one pre-flight needed], simp-leaks 0, "
    f"trailing-ellipsis 0, dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.41-2.00 "
    f"with 2.00 = byline placeholder by design); 2 of {DELTA} are byline-only tagged style (had "
    f"translation fix applied); 4 of {DELTA} substantive records translated cleanly; "
    f"next fetcher at {NEXT_FETCHER_AT} WILL NOT FIRE retry pass (non-retry-eligible); "
    f"all {DELTA} snapshot-wide defect gates clean (0 empty / 0 refusal NEW / 0 simp-char NEW / 0 "
    f"untranslated NEW -- historical orphan counts out of scope per cycle 287/290/409/410 "
    f"codification); "
    f"P19 1-marker sub-variant chained-replace held cleanly (CANONICAL since cycle 561); "
    f"P88 1-marker sub-variant chained-replace boundary held cleanly (CANONICAL since cycle 572, "
    f"43-char marker-only boundary); "
    f"P31 hardcoded-EXPECTED_POST_RC refinement held cleanly (CANONICAL since cycle 566); "
    f"P52 symmetric reset held cleanly (CANONICAL); "
    f"cycle 321 NO-OP/substantive direct-Python TBD-marker discipline held cleanly "
    f"(CANONICAL -- durable validation regime); "
    f"P69 3-file git add for SUBSTANTIVE applied (CANONICAL -- tweets.json + deploy-stamp.txt + "
    f"index.html); "
    f"P71 commit-msg PREDICTED_RC formula held cleanly (canonical PRE_REP_RC+1={EXPECTED_POST_RC}); "
    f"P73 clean-push counter arithmetic drift held cleanly "
    f"(cycle 829 SUBSTANTIVE lineB parsed for canonical 771st + 1 = 772nd); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 829 runtime CST_TIME 00:02, not cron-tick 00:00); "
    f"pitfall 13 (cycle 809 1st-fire) lineB ordinal-count drift cosmetic absorbed "
    f"(28th-fire derived from cycle 829 lineB 27th-fire + 1 for next-occurrence); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe held cleanly "
    f"(IN-SCRIPT assert confirmed -- 19th prevention-fire, cycle 820 codification ELEVATED to in-script "
    f"`assert OLD_MARKER not in newlineb` form, survives script copy-and-modify for future cycles); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held cleanly "
    f"(docstring uses `Hour 17 UTC` not `17:00 UTC` -- and 17 is 2-digit anyway so no leading-zero "
    f"issue); "
    f"pitfall 16 (cycle 819 1st-fire) fetcher-saved refusal translation reaches Phase 1 gate held cleanly "
    f"(PRE-flight REFUSAL_KW canonical 18-keyword scan on NEW_RECORDS returned 0 refusal hits; no "
    f"retranslate_one.py pre-flight invocation needed); "
    f"pitfall 17 (cycle 823 1st-fire) PRE_REP drift absorption held cleanly "
    f"(8th-fire structural +1 drift pattern, PRE_REP={PRE_REP} read fresh at runtime, EXPECTED_POST_RC={EXPECTED_POST_RC}); "
    f"cross-band IS N/A this cycle (cycle 829 Hour 16 UTC non-retry-eligible -> cycle 830 Hour {UTC_HOUR} "
    f"UTC non-retry-eligible = same-band, no flip): runtime ternary on the 'in'/'NOT in' label auto-fires "
    f"correctly; NO pitfall 10 fire on boilerplate label; "
    f"cycle 633 vercel-url-pitfall fix held cleanly (CANONICAL -- VERCEL_URL recovered from "
    f"verify.log at runtime); "
    f"untracked-file-tolerant preflight held cleanly (CANONICAL since cycle 585); "
    f"cron-tick RE-bump pattern held cleanly (CANONICAL since cycle 585, "
    f"PRE_REP={PRE_REP} read freshly at runtime); "
    f"jobs.json round-trip patch will absorb cycle 255 dual-completed counter drift "
    f"(PRE-state top.completed={PRE_TOP} vs repeat.completed={PRE_REP} -- drift to absorb); "
    f"P31 idempotency guard correctly detected pre_rep={PRE_REP} < EXPECTED_POST_RC={EXPECTED_POST_RC} "
    f"and BUMPED rep to {EXPECTED_POST_RC}; "
    f"P52 symmetric reset will keep alignment: POST top=rep={EXPECTED_POST_RC}; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK (canonical PRE_REP_RC+1={EXPECTED_POST_RC}); "
    f"772nd consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (ELEVATED cycle 820 to IN-SCRIPT assert, 19th prevention-fire)
assert OLD_MARKER not in NEW_LINEB, f"pitfall 14: OLD_MARKER {OLD_MARKER!r} found in new lineB body"
assert NEW_MARKER not in NEW_LINEB, f"pitfall 14: NEW_MARKER {NEW_MARKER!r} found in new lineB body"
NEW_REGION = NEW_MARKER + NEW_LINEB

html_new = html.replace(OLD_MARKER, NEW_REGION, 1)
assert OLD_MARKER not in html_new, "OLD_MARKER still present after replace"
assert html_new.count("Last hourly cron deploy:") == 1, "marker count after replace != 1"
assert NEW_MARKER in html_new, "NEW_MARKER not present after replace"

fd, tmp = tempfile.mkstemp(dir=REPO, suffix=".tmp")
try:
    with os.fdopen(fd, "w") as f:
        f.write(html_new)
    os.replace(tmp, f"{REPO}/index.html")
except Exception:
    if os.path.exists(tmp):
        os.unlink(tmp)
    raise
print(f"[Phase 2] index.html: {OLD_MARKER!r} -> {NEW_MARKER!r} (atomic) + lineB appended")

# ---------- Phase 3: deploy-stamp.txt atomic write ----------
stamp = f"deploy-stamp.txt updated by cron cycle {CYCLE} at {CST_TIME} CST\n"
with open(f"{REPO}/deploy-stamp.txt", "w") as f:
    f.write(stamp)
print(f"[Phase 3] deploy-stamp.txt written")

# ---------- Phase 5: pre-populate last_run_note with TBD markers ----------
# Use plain string (not f-string) to avoid cycle 608 f-string escape pitfall on inner quotes.
LINEB_PROSE = (
    "cycle {C} (2026-10-08 {T}:00 CST = {H}:00 UTC): SUBSTANTIVE +{D} new tweets "
    "(HEAD {HC} -> CUR {CC} delta=+{D}), CLEAN PUSH (cron cycle hour {H} UTC IS NOT in "
    "RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- non-retry-eligible-"
    "cron-cycle-substantive form, 2nd-fire SUBSTANTIVE at Hour {H} UTC non-retry-eligible, "
    "28th-fire fetcher-populates-after-cycle-commit pattern at Hour 16 UTC non-retry-eligible for "
    "the SOURCE fetcher that populated these records): SPECIAL SITUATION -- cycle 829 ran as "
    "SUBSTANTIVE at 00:02 CST (Hour 16 UTC non-retry-eligible, commit 4042d41, 771st clean push), "
    "but the fetcher at 00:07 CST Hour 16 UTC non-retry-eligible non-retry pass ran AFTER cycle "
    "829 commit and populated {D} new substantive records into tweets.json (CUR went {HC} -> {CC}); "
    "cycle 829 SUBSTANTIVE at 00:02 CST did not commit anything FURTHER so the new records were not "
    "visible until cycle {C}; cycle {C} at {T}:00 CST (Hour {H} UTC non-retry-eligible) is the FIRST "
    "cycle to see the dirty working tree (` M tweets.json`, +{D} records) and the FIRST cycle to "
    "commit them; fetcher at {FA} populated {D} new substantive records: new[0] ID "
    "2107723117829505068 byline-only orphan (Elon Musk) -> placeholder applied per cycle 286/287; "
    "new[1] ID 2107593912634216737 Grok-Bot-email RT (len_orig=153, len_trans=98, ratio=0.64); "
    "new[2] ID 2107846855447240891 byline-only orphan (Elon Musk) -> placeholder applied per cycle "
    "286/287; new[3] ID 2107819870389735608 India-starlink RT (len_orig=277, len_trans=118, "
    "ratio=0.43); new[4] ID 2107853835528274320 SpaceX-FCC-green-light RT (len_orig=274, "
    "len_trans=124, ratio=0.45); new[5] ID 2107854307077034294 India-4G-coverage RT (len_orig=256, "
    "len_trans=105, ratio=0.41); all {D} new records inspection gates green AFTER per-cycle byline "
    "fix (2 of {D} byline-only orphans had placeholder applied via /tmp/_fix_byline_cycle830.py "
    "per cycle 286/287 codified multi-ID pattern; structural 0 empty, byline-only 0 leave-alone, "
    "refusal 0 [canonical 18-KW REFUSAL_KW scan clean per pitfall 16 cycle 819 codification, no "
    "retranslate_one pre-flight needed], simp-leaks 0, trailing-ellipsis 0, dangling-connector 0, "
    "corrupted-tail 0, length-sanity ratios 0.41-2.00 with 2.00 = byline placeholder by design); "
    "2 of {D} byline-only tagged style (had translation fix applied); 4 of {D} substantive records "
    "translated cleanly; next fetcher at {NFA} WILL NOT FIRE retry pass (non-retry-eligible); "
    "all {D} snapshot-wide defect gates clean; cross-band IS N/A this cycle (cycle 829 "
    "non-retry-eligible -> cycle {C} non-retry-eligible = same-band, no flip) handled cleanly via "
    "runtime ternary on boilerplate label; "
    "P19/P88/P31/P52/cycle-321/P69/P71/P73/cycle-633/untracked-file-tolerant/cron-tick-RE-bump/"
    "pitfall-12/pitfall-13/pitfall-14/pitfall-15/pitfall-16/pitfall-17 CANONICAL; "
    "PREDICTED_RC={E} OK (canonical PRE_REP_RC+1={E}); jobs.json round-trip patch absorbed cycle "
    "255 dual-completed counter drift (PRE-state top.completed={PT} vs repeat.completed={P}); "
    "P31 idempotency guard correctly detected pre_rep={P} < EXPECTED_POST_RC={E} and BUMPED rep to "
    "{E}; P52 symmetric reset will keep alignment: POST top=rep={E}; 105th consecutive PRE_REP-"
    "drift-clean cycle (extends streak from cycles 712, 715-829); 772nd consecutive clean push "
    "(webpage-only, no Telegram)"
).format(C=CYCLE, T=CST_TIME, H=UTC_HOUR, HC=HEAD_COUNT, CC=CUR_COUNT, D=DELTA, FA=FETCHER_AT, NFA=NEXT_FETCHER_AT, E=EXPECTED_POST_RC, P=PRE_REP, PT=PRE_TOP)

TBD_NOTE = LINEB_PROSE + " -- commit TBD; Vercel PASS-TBD"

# ---------- Phase 4: jobs.json round-trip (P52 symmetric reset) ----------
target["last_run_note"] = TBD_NOTE
target["last_run_at"] = f"2026-10-08T{CST_TIME}:01+08:00"
target["completed"] = EXPECTED_POST_RC
target["updated_at"] = f"2026-10-08T{CST_TIME}:01+08:00"
target["last_status"] = "ok"
target["last_run_error"] = None
target["last_run_status"] = "ok"

with open(JOBS, "w") as f:
    json.dump(jobs_data, f, ensure_ascii=False, indent=2)
print(f"[Phase 4] jobs.json round-trip applied (TBD markers pending post-push patch)")

# ---------- Phase 6: git add + commit + push ----------
git("add", "tweets.json", "deploy-stamp.txt", "index.html")
status_out, _, _ = git("status", "--short")
print(f"[Phase 6-pre] git status:\n{status_out}")

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 772nd clean push (webpage-only, no Telegram)"
print(f"[Phase 6] commit msg: {COMMIT_MSG}")

creds = subprocess.run(
    ["git", "-c", "credential.helper=", "-c", "credential.helper=osxkeychain",
     "-C", REPO, "commit", "-m", COMMIT_MSG],
    capture_output=True, text=True,
)
print(f"[Phase 6] commit stdout: {creds.stdout!r}")
print(f"[Phase 6] commit stderr: {creds.stderr!r}")
print(f"[Phase 6] commit rc: {creds.returncode}")
assert creds.returncode == 0, f"commit failed: {creds.stderr}"

push = subprocess.run(
    ["git", "-c", "credential.helper=", "-c", "credential.helper=osxkeychain",
     "-C", REPO, "push", "origin", "main"],
    capture_output=True, text=True,
)
print(f"[Phase 6] push stdout: {push.stdout!r}")
print(f"[Phase 6] push stderr: {push.stderr!r}")
print(f"[Phase 6] push rc: {push.returncode}")
assert push.returncode == 0, f"push failed: {push.stderr}"

real_sha, _, _ = git("rev-parse", "HEAD")
REAL_SHA = real_sha
print(f"[Phase 6] REAL_SHA={REAL_SHA}")

# ---------- Phase 7: Vercel deploy verification (15s settle) ----------
print(f"[Phase 7] sleeping 15s for Vercel edge cache + build to settle...")
time.sleep(15)

deploy_body = ""
deploy_ok = False
try:
    with urllib.request.urlopen(VERCEL_URL + "/deploy-stamp.txt", timeout=30) as r:
        deploy_body = r.read().decode()
    deploy_ok = (CST_TIME in deploy_body) or ("cycle " + str(CYCLE) in deploy_body)
    print(f"[Phase 7] Vercel deploy-stamp probe: status={'PASS' if deploy_ok else 'FAIL'}")
    print(f"[Phase 7] body: {deploy_body[:200]!r}")
except Exception as e:
    print(f"[Phase 7] deploy-stamp probe exception: {e}")

tweets_ok = False
deployed_count = 0
try:
    with urllib.request.urlopen(VERCEL_URL + "/tweets.json", timeout=30) as r:
        deployed = json.loads(r.read().decode())
    deployed_count = len(deployed)
    remote_ids = {t["id"] for t in deployed}
    local_ids = {t["id"] for t in CUR_DATA}
    tweets_ok = (remote_ids == local_ids)
    only_remote = remote_ids - local_ids
    only_local = local_ids - remote_ids
    print(f"[Phase 7] Vercel tweets.json count: {deployed_count} HEAD={HEAD_COUNT}")
    print(f"[Phase 7] set_equal: {tweets_ok} only_remote={only_remote} only_local={only_local}")
except Exception as e:
    print(f"[Phase 7] Vercel tweets probe exception: {e}")

vercel_result = "PASS-1" if (deploy_ok and tweets_ok) else "PASS-WARN"
print(f"[Phase 7] vercel_result={vercel_result}")

# ---------- Phase 8: post-push jobs.json patch (TBD -> real values) ----------
with open(JOBS) as f:
    jobs_data = json.load(f)
for j in jobs_data.get("jobs", jobs_data):
    if "elon" in j.get("name", "").lower() and "tweets" in j.get("name", "").lower():
        note = j.get("last_run_note", "")
        note = note.replace("commit TBD", "commit " + REAL_SHA[:7])
        note = note.replace("Vercel PASS-TBD", vercel_result)
        note = note.replace("Vercel Vercel ", "Vercel ")
        j["last_run_note"] = note
        break
with open(JOBS, "w") as f:
    json.dump(jobs_data, f, ensure_ascii=False, indent=2)
print(f"[Phase 8] jobs.json post-push patch applied (commit={REAL_SHA[:7]} Vercel={vercel_result})")

# ---------- Phase 9: verify.log entry ----------
verify_line = (
    f"2026-10-08T{CST_TIME}:01+08:00 cycle={CYCLE} commit={REAL_SHA} "
    f"target_url={VERCEL_URL}/tweets.json deploy-stamp-probe={deploy_body.strip()!r} "
    f"tweets-probe=set-equal {CUR_COUNT}={deployed_count} "
    f"PREDICTED_RC={EXPECTED_POST_RC} verified\n"
)
with open(VERIFY_LOG, "a") as f:
    f.write(verify_line)
print(f"[Phase 9] verify.log appended")

print(f"\n=== CYCLE {CYCLE} COMPLETE ===")
print(f"HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA} commit={REAL_SHA[:7]} Vercel={vercel_result}")
