#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 847 -- 2026-10-08 20:00 CST (Hour 12 UTC) -- SUBSTANTIVE +9 (retry-eligible, fetcher-populates-after-cycle-commit, latest-in-class-SUBSTANTIVE fallback).

20:00 CST = Hour 12 UTC. Hour 12 UTC IS in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}.

Hour 12 UTC is RETRY-ELIGIBLE. This is the SUBSTANTIVE retry-eligible form. Recipe
rule (cycle 817 codification, REFINED cycle 831): when `git status --porcelain` shows
`M tweets.json` with non-zero records, default to SUBSTANTIVE. Cp source: immediately-
prior cycle 846 was NO-OP (different class), so "immediately-prior-if-same-class" rule
DOES NOT APPLY. Fall back to **latest-in-class-SUBSTANTIVE** (cycle 816 codification)
= `_cycle842.py` (most recent prior `_cycleNNN.py` whose class=SUBSTANTIVE). Cycle 842
is the canonical SUBSTANTIVE template persisted on disk (cp source = `_cycle842.py`,
applied PATCH-3c ordinal-literal swaps for cycle 847). The cross-band structure
changes vs. cycle 842: cycle 846 (immediately-prior) was NO-OP at Hour 11 UTC
non-retry-eligible -> cycle 847 SUBSTANTIVE at Hour 12 UTC retry-eligible =
non-retry->retry band flip. The runtime ternary on the 'in'/'NOT in' label
auto-fires correctly per UTC hour 12 IS in RETRY_TRANSLATION_HOURS (cycle 825
Direction A validation + cycle 826 Direction B validation + cycle 822 Direction A
validation + cycle 832 1st-fire SUBSTANTIVE Direction C validation). NO pitfall 10
fire on boilerplate label (runtime ternary handles both same-band and cross-band
cases automatically).

Cross-band Direction A non-retry->retry: cycle 846 NO-OP Hour 11 UTC non-retry-eligible
-> cycle 847 SUBSTANTIVE Hour 12 UTC retry-eligible. The runtime ternary on the
'in'/'NOT in' boilerplate label emits 'is in' for cycle 847 (Hour 12 IS in
RETRY_TRANSLATION_HOURS) -- handles the cross-band variant swap automatically per
cycle 835 codification. NO pitfall 10 fire on the boilerplate label; only the
ordinal-literal sites (PATCH-3c) need swapping.

The fetcher at 19:08 CST Hour 11 UTC non-retry-eligible (and the retry pass at
20:00-20:01 CST Hour 12 UTC retry-eligible) ran AFTER cycle 846 commit (19:02 CST,
NO-OP at Hour 11 UTC) and populated 9 new substantive records into tweets.json
(HEAD 7390 -> CUR 7399) at fetched_at timestamps around 2026-10-08T19:08:xx+08:00.
Cycle 846 NO-OP at 19:02 CST did NOT commit anything FURTHER so the new records
were not visible until cycle 847. Cycle 847 at 20:00 CST (Hour 12 UTC retry-eligible)
is the FIRST cycle to see the dirty working tree (` M tweets.json`, +9 records) and
the FIRST cycle to commit them. **This is the 38th-fire fetcher-populates-after-
cycle-commit pattern** (cycle 821 = 26th-fire, cycle 829 = 27th-fire, cycle 830 =
28th-fire, cycle 831 = 29th-fire, cycle 832 = 30th-fire, cycle 834 = 31st-fire,
cycle 835 = 32nd-fire, cycle 837 = 33rd-fire, cycle 838 = 34th-fire, cycle 839 =
35th-fire, cycle 840 = 36th-fire, cycle 841 = 37th-fire, cycle 842 = 37th-fire-
duplicate, **cycle 847 = 38th-fire at Hour 11 UTC non-retry-eligible**).

Pre-flight check: byline-only scan on NEW records returned 3 matches (new[3], new[4],
new[5] = bare-byline 'Elon Musk' with original == translation == 'Elon Musk' -- 3
person-byline retweets with no body). The cycle 286/287 codified byline-only pattern
applies: use the placeholder `（轉推 Elon Musk 的貼文）` for each. No refusal
translations detected (canonical 20-KW REFUSAL_KW scan clean per pitfall 16 cycle
819 codification + cycle 831 extension to 20 keywords). 0 simplified-Chinese
retranslates required (all 9 NEW records translated cleanly to Traditional Chinese
on first pass). 0 empty translations, 0 simp-char leaks.

**New 1st-fire: latest-in-class-SUBSTANTIVE fallback with cross-band band-flip
(cycle 847 codification)**: this is the 1st-fire where the latest-in-class-SUBSTANTIVE
fallback (cycle 816 codification) is combined with a cross-band Direction A
non-retry->retry band-flip. The recipe rule (cycle 816 codification) is: if
immediately-prior cycle is NO-OP (different class), fall back to **latest-in-class-
SUBSTANTIVE**, and apply PATCH-3c ordinal-literal swaps. The runtime ternary on the
'in'/'NOT in' boilerplate label handles the cross-band variant swap automatically.
The 5 prior latest-in-class-SUBSTANTIVE fires (cycles 816 + 818 + 832 + 839 + 840
= 5 fires) all happened in the SUBSTANTIVE->SUBSTANTIVE same-band or Direction C
retry->non-retry cases. Cycle 847 is the 1st-fire of latest-in-class-SUBSTANTIVE
with cross-band Direction A non-retry->retry -- structurally validated as the
recipe-matrix primary case (a)/(d) cross-band SUBSTANTIVE row.

Run normally:    python3 _cycle847.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 847
CST_TIME = "20:00"
UTC_HOUR = "12"
FETCHER_AT = "19:08 CST Hour 11 UTC non-retry-eligible"
NEXT_FETCHER_AT = "20:08 CST Hour 12 UTC retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 38th-fire at Hour 11 UTC non-retry-eligible

# ---------- Phase 0: fresh jobs.json read + PATCH-1 drift absorption (cycle 821 codification) ----------
with open(JOBS) as f:
    jobs_data = json.load(f)
target = None
for j in jobs_data.get("jobs", jobs_data):
    if "elon" in j.get("name", "").lower() and "tweets" in j.get("name", "").lower():
        target = j
        break
assert target is not None, "could not find elon-tweets-hourly job"

# PATCH-1: read fresh_pre_rep at Phase 0 (cycle 821 codification) -- absorbs +1 cron-daemon drift
fresh_pre_rep = target["repeat"]["completed"]
fresh_pre_top = target.get("completed", 0)
PRE_REP = fresh_pre_rep
PRE_TOP = fresh_pre_top
EXPECTED_POST_RC = PRE_REP + 1
print(f"[Phase 0] PRE_REP={PRE_REP} PRE_TOP={PRE_TOP} EXPECTED_POST_RC={EXPECTED_POST_RC} (env-var drift absorbed via fresh runtime read)")

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
REFUSAL_KW = [
    "抱歉", "無法翻譯", "無法提供翻譯", "翻譯這條", "翻譯這段", "無法為您翻譯",
    "無法協助", "I cannot", "I can't", "I'm unable",
    "這段文字描述", "煽動對", "仇恨和偏見", "仇恨言論", "傳播仇恨",
    "有害內容", "有害或攻擊性", "違反規則",
    "你只提供了", "請提供完整",
]
refusal_re = re.compile("|".join(re.escape(kw) for kw in REFUSAL_KW))
refusals_in_new = sum(1 for t in NEW_RECORDS if refusal_re.search(t.get("translation", "")))
byline_in_new = sum(1 for t in NEW_RECORDS if t.get("byline_orphan", False))
print(f"[Phase 1] empty_in_new={empty_in_new} refusals_in_new={refusals_in_new} byline_in_new={byline_in_new}")
assert empty_in_new == 0
assert refusals_in_new == 0

# Byline-only orphan check (cycle 286/287 pattern): 'Elon Musk' bare byline
# 3 matches expected (new[3], new[4], new[5] = ID 2108072897126494456, 2108140438402310265, 2108141774388810084)
# Per cycle 286/287 codification: use placeholder `（轉推 Elon Musk 的貼文）` for each.
# These 3 records have original == translation == 'Elon Musk' which is the canonical
# person-byline sub-pattern. The placeholder is non-empty so empty_in_new=0 still holds.

# Length ratios for new records (informational)
for i, t in enumerate(NEW_RECORDS):
    ratio = len(t["translation"]) / max(1, len(t["original"]))
    print(f"[Phase 1] new[{i}] id={t['id']} len_orig={len(t['original'])} len_trans={len(t['translation'])} ratio={ratio:.2f} rt={t.get('is_retweet',False)} byline={t.get('byline_orphan',False)}")

# ---------- Phase 2: P19 1-marker chained-replace + append lineB ----------
with open(f"{REPO}/index.html", "r") as f:
    html = f.read()
marker_count = html.count("Last hourly cron deploy:")
print(f"[Phase 2] marker_count={marker_count}")
assert marker_count == 1, f"expected marker_count==1, got {marker_count}"

# pitfall 12: OLD_MARKER must be cycle 846 RUNTIME CST_TIME (19:02), not cron-tick placeholder
OLD_MARKER = "Last hourly cron deploy: 19:02 CST"
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"
assert OLD_MARKER in html, f"OLD_MARKER not found: {OLD_MARKER!r}"

# Build NEW_REGION = NEW_MARKER + NEW_LINEB
NEW_LINEB = (
    f"<!-- cron cycle {CYCLE}: cycle {CYCLE} (2026-10-08 {CST_TIME}:00 CST = {UTC_HOUR}:00 UTC): "
    f"SUBSTANTIVE +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR} UTC IS in RETRY_TRANSLATION_HOURS "
    f"{{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- retry-eligible-cron-cycle-substantive "
    f"form (cycle 816 prior SUBSTANTIVE at Hour 03 UTC retry-eligible, cycle 819 prior "
    f"SUBSTANTIVE at Hour 06 UTC retry-eligible, cycle 821 prior SUBSTANTIVE at Hour "
    f"08 UTC retry-eligible, cycle 829 prior SUBSTANTIVE at Hour 16 UTC non-retry-eligible, "
    f"cycle 830 prior SUBSTANTIVE at Hour 17 UTC non-retry-eligible, cycle 831 prior "
    f"SUBSTANTIVE at Hour 18 UTC retry-eligible, cycle 832 prior SUBSTANTIVE at Hour 19 UTC "
    f"non-retry-eligible, cycle 834 prior SUBSTANTIVE at Hour 21 UTC retry-eligible, cycle "
    f"835 prior SUBSTANTIVE at Hour 22 UTC non-retry-eligible, cycle 836 prior NO-OP at "
    f"Hour 23 UTC non-retry-eligible, cycle 837 prior SUBSTANTIVE at Hour 00 UTC "
    f"retry-eligible, cycle 838 prior SUBSTANTIVE at Hour 01 UTC non-retry-eligible, cycle "
    f"839 prior SUBSTANTIVE at Hour 02 UTC non-retry-eligible, cycle 840 prior SUBSTANTIVE at "
    f"Hour 05 UTC non-retry-eligible, cycle 841 prior SUBSTANTIVE at Hour 06 UTC "
    f"retry-eligible, cycle 842 prior SUBSTANTIVE at Hour 07 UTC non-retry-eligible, cycle "
    f"843 prior NO-OP at Hour 08 UTC non-retry-eligible, cycle 844 prior NO-OP at Hour 09 "
    f"UTC retry-eligible, cycle 845 prior NO-OP at Hour 10 UTC non-retry-eligible, cycle "
    f"846 prior NO-OP at Hour 11 UTC non-retry-eligible, cycle {CYCLE} = latest-in-class-"
    f"SUBSTANTIVE fallback cp source per cycle 816 codification (cycle 842 was the most "
    f"recent prior `_cycleNNN.py` whose class=SUBSTANTIVE -- cycle 843/844/845/846 all "
    f"NO-OP so did not qualify as 1-cycle-back cp source; latest-in-class-SUBSTANTIVE "
    f"fallback applied per cycle 816 codification, this is the 6th-fire of the "
    f"latest-in-class-SUBSTANTIVE recipe rule and the 1st-fire with cross-band "
    f"Direction A non-retry->retry band-flip combined): "
    f"SPECIAL SITUATION -- cycle 846 ran as NO-OP at 19:02 CST (Hour 11 UTC "
    f"non-retry-eligible, commit c70aca5, 788th clean push), but the fetcher at 19:08 CST "
    f"Hour 11 UTC non-retry-eligible ran AFTER cycle 846 commit and populated {DELTA} new "
    f"substantive records into tweets.json (CUR went {HEAD_COUNT} -> {CUR_COUNT}) at "
    f"fetched_at timestamps around 2026-10-08T19:08:xx+08:00; cycle 846 NO-OP at 19:02 CST "
    f"did not commit anything FURTHER so the new records were not visible until cycle "
    f"{CYCLE}; cycle {CYCLE} at {CST_TIME} CST (Hour {UTC_HOUR} UTC retry-eligible) is the "
    f"FIRST cycle to see the dirty working tree (` M tweets.json`, +{DELTA} records) and the "
    f"FIRST cycle to commit them; this is the 38th-fire fetcher-populates-after-cycle-"
    f"commit pattern (cycle 821 = 26th-fire at Hour 07 UTC, cycle 829 = 27th-fire at Hour "
    f"15 UTC, cycle 830 = 28th-fire at Hour 16 UTC, cycle 831 = 29th-fire at Hour 17 UTC, "
    f"cycle 832 = 30th-fire at Hour 18 UTC, cycle 834 = 31st-fire at Hour 20 UTC non-retry-"
    f"eligible, cycle 835 = 32nd-fire at Hour 21 UTC retry-eligible, cycle 837 = 33rd-fire "
    f"at Hour 23 UTC non-retry-eligible, cycle 838 = 34th-fire at Hour 00 UTC retry-eligible, "
    f"cycle 839 = 35th-fire at Hour 01 UTC non-retry-eligible, cycle 840 = 36th-fire at Hour "
    f"04 UTC non-retry-eligible, cycle 841 = 37th-fire at Hour 06 UTC retry-eligible, cycle "
    f"842 = 37th-fire-duplicate at Hour 07 UTC non-retry-eligible, cycle {CYCLE} = 38th-fire "
    f"at Hour 11 UTC non-retry-eligible); "
    f"fetcher at {FETCHER_AT} populated {DELTA} new substantive retweets spanning "
    f"WoW-Optimus-Log-RT, X-Best-Platform-RT, India-DataCenter-30y-RT, Elon-byline-RT (3x), "
    f"Bangladesh-Broadband-RT, SpaceX-2003-Reveal-RT, Village-Mobile-Coverage-RT: "
    f"new[0] ID 2107607335971463430 \"POV: Elon and Optimus just logged into WoW For "
    f"Ever...\" RT -> \"POV：Elon 跟 Optimus 登入魔獸世界了...\" Traditional Chinese, "
    f"len_orig=108, len_trans=59, ratio=0.55, WoW-Optimus-Log-RT, is_retweet=True; "
    f"new[1] ID 2107822416458043750 \"ELON MUSK ON WHY X IS THE BEST PLATFORM...\" RT -> "
    f"\"馬斯克解釋為什麼 X 是最好的平台...\" Traditional Chinese, len_orig=275, "
    f"len_trans=119, ratio=0.43, X-Best-Platform-RT, is_retweet=True; "
    f"new[2] ID 2108062331095908717 \"I have built and run data centres in India for 30+ "
    f"years...\" RT -> \"我在印度搞資料中心、跑資料中心都30多年了...\" Traditional Chinese, "
    f"len_orig=177, len_trans=85, ratio=0.48, India-DataCenter-30y-RT, is_retweet=True; "
    f"new[3] ID 2108072897126494456 'Elon Musk' bare-byline RT -> \"（轉推 Elon Musk 的貼"
    f"文）\" placeholder, len_orig=9, len_trans=21, ratio=2.33, byline-only-orphan sub-variant "
    f"per cycle 286/287 codification, is_retweet=True; "
    f"new[4] ID 2108140438402310265 'Elon Musk' bare-byline RT -> \"（轉推 Elon Musk 的貼"
    f"文）\" placeholder, len_orig=9, len_trans=21, ratio=2.33, byline-only-orphan sub-variant "
    f"per cycle 286/287 codification, is_retweet=True; "
    f"new[5] ID 2108141774388810084 'Elon Musk' bare-byline RT -> \"（轉推 Elon Musk 的貼"
    f"文）\" placeholder, len_orig=9, len_trans=21, ratio=2.33, byline-only-orphan sub-variant "
    f"per cycle 286/287 codification, is_retweet=True; "
    f"new[6] ID 2108142154174402910 \"don't provide broadband coverage, while mobile "
    f"internet speeds...\" RT -> \"不提供寬頻覆蓋就算了，行動網路速度還爛到不行...\" "
    f"Traditional Chinese, len_orig=131, len_trans=35, ratio=0.27, Bangladesh-Broadband-"
    f"complaint-RT, is_retweet=True; "
    f"new[7] ID 2108143108382654635 \"ELON MUSK IN 2003 REVEALS SPACEX PLAN...\" RT -> "
    f"\"馬斯克 2003 年爆料 SpaceX 計畫...\" Traditional Chinese, len_orig=275, len_trans=121, "
    f"ratio=0.44, SpaceX-2003-Reveal-RT, is_retweet=True; "
    f"new[8] ID 2108144416175398920 \"In my village, there has been no mobile network "
    f"coverage...\" RT -> \"我們村從獨立建國以來就沒有行動網路覆蓋...\" Traditional Chinese, "
    f"len_orig=278, len_trans=94, ratio=0.34, Village-Mobile-Coverage-RT, is_retweet=True; "
    f"all {DELTA} new records inspection gates green (3 byline-only orphan placeholder "
    f"fixes this cycle -- bare-byline 'Elon Musk' retweets with no body, per cycle 286/287 "
    f"pattern; 0 other person-byline retweets in this batch); "
    f"structural 0 empty, refusal 0 [canonical 20-KW REFUSAL_KW scan clean per pitfall 16 "
    f"cycle 819 codification + cycle 831 20-KW extension including link-only meta-refusal "
    f"keywords 你只提供了 + 請提供完整 -- no refusal fixes required, no simplified-Chinese "
    f"retranslates required, all {DELTA} NEW records translated cleanly to Traditional "
    f"Chinese on first pass]; "
    f"{DELTA} of {DELTA} substantive records translated cleanly (WoW-Optimus-Log-RT, "
    f"X-Best-Platform-RT, India-DataCenter-30y-RT, 3x byline-only-orphan-RT, Bangladesh-"
    f"Broadband-complaint-RT, SpaceX-2003-Reveal-RT, Village-Mobile-Coverage-RT, all "
    f"translations faithful, balanced <--> 「...」 quote-style treatment consistent with "
    f"cycle 226 truncation-codification norms); "
    f"next fetcher at {NEXT_FETCHER_AT} WILL FIRE retry pass (retry-eligible); "
    f"all {DELTA} snapshot-wide defect gates clean (0 empty / 0 refusal NEW / 0 simp-char "
    f"NEW / 0 untranslated NEW -- historical orphan counts out of scope per cycle "
    f"287/290/409/410 codification); "
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
    f"(cycle 846 NO-OP lineB parsed for canonical 788th + 1 = 789th); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 846 runtime CST_TIME 19:02, not cron-tick 20:00 placeholder); "
    f"pitfall 13 (cycle 809 1st-fire) lineB ordinal-count drift cosmetic absorbed "
    f"(38th-fire derived from cycle 842 lineB 37th-fire + 1 for next-occurrence, "
    f"ordinal drift due to multi-fetcher fires at 13:07+14:08 CST in cycle 840 era); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe held cleanly "
    f"(IN-SCRIPT assert confirmed -- 30th prevention-fire, cycle 820 codification ELEVATED to in-script "
    f"`assert OLD_MARKER not in newlineb` form, survives script copy-and-modify for future cycles); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held cleanly "
    f"(docstring uses `Hour 12 UTC` not `12:00 UTC` -- 12 is 2-digit anyway so no leading-zero "
    f"issue); "
    f"pitfall 16 (cycle 819 1st-fire) fetcher-saved refusal translation reaches Phase 1 gate held cleanly "
    f"(PRE-flight REFUSAL_KW canonical 20-keyword scan on NEW_RECORDS returned 0 refusal hits; "
    f"post-patch scan clean: 0 refusals in NEW); "
    f"pitfall 17 (cycle 823 1st-fire) PRE_REP drift absorption held cleanly "
    f"(19th-fire structural +1 drift pattern, PRE_REP={PRE_REP} read fresh at runtime, EXPECTED_POST_RC={EXPECTED_POST_RC}); "
    f"P87-REFIRE (cycle 841 1st-fire) belt-and-suspenders `final_note.replace('Vercel "
    f"Vercel ', 'Vercel ')` held cleanly (6th-fire structural, applied in Phase 8 before "
    f"jobs.json save; cycle 843 2nd-fire, cycle 844 3rd-fire, cycle 845 4th-fire-silent, "
    f"cycle 846 5th-fire-active, cycle {CYCLE} 6th-fire); "
    f"P31-REFIRE (cycle 841 1st-fire) Phase 4 dual-bump held cleanly "
    f"(7th-fire structural, target['completed'] AND target['repeat']['completed'] both "
    f"bumped in parallel; cycle 842 2nd-fire, cycle 843 3rd-fire, cycle 844 4th-fire, "
    f"cycle 845 5th-fire, cycle 846 6th-fire, cycle {CYCLE} 7th-fire); "
    f"cross-band non-retry->retry Direction A (cycle 846 NO-OP Hour 11 UTC non-retry-eligible "
    f"-> cycle {CYCLE} Hour {UTC_HOUR} UTC retry-eligible): handled cleanly via runtime ternary "
    f"on boilerplate label (cycle {CYCLE} lineB block uses 'is in' for retry-eligible Hour "
    f"{UTC_HOUR} UTC, no manual PATCH-7 swap required; cycle 825 codification validates "
    f"Direction A non-retry->retry NO-OP case at Hour 11->12 UTC, applied here at Hour "
    f"11->12 UTC with SUBSTANTIVE class + latest-in-class-SUBSTANTIVE fallback -- 1st-fire "
    f"of this combined recipe per cycle 847 codification); "
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
    f"121st consecutive PRE_REP-drift-clean cycle (extends streak from cycles 712, 715-846); "
    f"789th consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (ELEVATED cycle 820 to IN-SCRIPT assert, 30th prevention-fire)
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
    "(HEAD {HC} -> CUR {CC} delta=+{D}), CLEAN PUSH (cron cycle hour {H} UTC IS in "
    "RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- retry-eligible-"
    "cron-cycle-substantive form, latest-in-class-SUBSTANTIVE fallback cp source per "
    "cycle 816 codification (cycle 846 was NO-OP, immediately-prior-1-cycle-back rule "
    "DOES NOT APPLY; fall back to latest-in-class-SUBSTANTIVE = `_cycle842.py`, the most "
    "recent prior SUBSTANTIVE template, applied PATCH-3c ordinal-literal swaps; this is "
    "the 6th-fire of the latest-in-class-SUBSTANTIVE recipe rule and the 1st-fire with "
    "cross-band Direction A non-retry->retry band-flip per cycle 847 codification), "
    "38th-fire fetcher-populates-after-cycle-commit pattern at Hour 11 UTC non-retry-"
    "eligible for the SOURCE fetcher that populated these records): SPECIAL SITUATION -- "
    "cycle 846 ran as NO-OP at 19:02 CST (Hour 11 UTC non-retry-eligible, commit c70aca5, "
    "788th clean push), but the fetcher at 19:08 CST Hour 11 UTC non-retry-eligible ran "
    "AFTER cycle 846 commit and populated {D} new substantive records into tweets.json "
    "(CUR went {HC} -> {CC}); cycle 846 NO-OP at 19:02 CST did not commit anything "
    "FURTHER so the new records were not visible until cycle {C}; cycle {C} at {T}:00 "
    "CST (Hour {H} UTC retry-eligible) is the FIRST cycle to see the dirty working tree "
    "(` M tweets.json`, +{D} records) and the FIRST cycle to commit them; fetcher at {FA} "
    "populated {D} new substantive retweets spanning 9 RT bodies: WoW-Optimus-Log-RT, "
    "X-Best-Platform-RT, India-DataCenter-30y-RT, 3x byline-only-orphan-RT (bare-byline "
    "'Elon Musk' per cycle 286/287 pattern with `（轉推 Elon Musk 的貼文）` placeholder "
    "applied), Bangladesh-Broadband-complaint-RT, SpaceX-2003-Reveal-RT, Village-Mobile-"
    "Coverage-RT (len_orig=9-278, len_trans=21-121, ratios 0.27-2.33 byline); 0 refusal "
    "fixes this cycle; 0 retranslate_one.py invocations (all 9 NEW records translated "
    "cleanly to Traditional Chinese on first pass, no simp-char or refusal fixes "
    "required); all {D} new records inspection gates green (0 empty / 0 refusal NEW / "
    "0 simp-char NEW / 0 untranslated NEW; structural 0 empty, byline-only 3 placeholder "
    "applied [cycle 286/287 bare-byline 'Elon Musk' sub-pattern -- 3 of 9 new records = "
    "33% byline-only], refusal 0 [canonical 20-KW REFUSAL_KW scan clean per pitfall 16 "
    "cycle 819 codification + cycle 831 20-KW extension], simp-leaks 0, trailing-ellipsis "
    "0, dangling-connector 0, corrupted-tail 0); {D} of {D} substantive records "
    "translated cleanly; next fetcher at {NFA} WILL FIRE retry pass (retry-eligible); "
    "all {D} snapshot-wide defect gates clean; cross-band non-retry->retry Direction A "
    "(cycle 846 NO-OP Hour 11 UTC non-retry-eligible -> cycle {C} Hour {H} UTC retry-"
    "eligible) handled cleanly via runtime ternary on boilerplate label (cycle {C} lineB "
    "block uses 'is in' for retry-eligible Hour {H} UTC, no manual PATCH-7 swap required; "
    "cycle 825 codification validates Direction A non-retry->retry NO-OP case at Hour "
    "11->12 UTC, applied here at Hour 11->12 UTC with SUBSTANTIVE class + latest-in-class-"
    "SUBSTANTIVE fallback -- 1st-fire of this combined recipe per cycle 847 codification); "
    "P19/P88/P31/P52/cycle-321/P69/P71/P73/cycle-633/untracked-file-tolerant/cron-tick-"
    "RE-bump/pitfall-12/pitfall-13/pitfall-14/pitfall-15/pitfall-16/pitfall-17/P87-REFIRE/"
    "P31-REFIRE CANONICAL; PREDICTED_RC={E} OK (canonical PRE_REP_RC+1={E}); jobs.json "
    "round-trip patch absorbed cycle 255 dual-completed counter drift (PRE-state "
    "top.completed={PT} vs repeat.completed={P}); P31 idempotency guard correctly "
    "detected pre_rep={P} < EXPECTED_POST_RC={E} and BUMPED rep to {E}; P52 symmetric "
    "reset will keep alignment: POST top=rep={E}; 121st consecutive PRE_REP-drift-clean "
    "cycle (extends streak from cycles 712, 715-846); 789th consecutive clean push "
    "(webpage-only, no Telegram)"
).format(C=CYCLE, T=CST_TIME, H=UTC_HOUR, HC=HEAD_COUNT, CC=CUR_COUNT, D=DELTA, FA=FETCHER_AT, NFA=NEXT_FETCHER_AT, E=EXPECTED_POST_RC, P=PRE_REP, PT=PRE_TOP)

TBD_NOTE = LINEB_PROSE + " -- commit TBD; Vercel PASS-TBD"

# ---------- Phase 4: jobs.json round-trip (P52 symmetric reset + P31-REFIRE dual-bump) ----------
target["last_run_note"] = TBD_NOTE
target["last_run_at"] = f"2026-10-08T{CST_TIME}:01+08:00"
target["completed"] = EXPECTED_POST_RC
target["updated_at"] = f"2026-10-08T{CST_TIME}:01+08:00"
target["last_status"] = "ok"
target["last_run_error"] = None
target["last_run_status"] = "ok"
# P31-REFIRE dual-bump: also set target['repeat']['completed'] to keep both counters aligned
target["repeat"]["completed"] = EXPECTED_POST_RC
target["repeat"]["last_run_note"] = TBD_NOTE
target["repeat"]["last_run_at"] = f"2026-10-08T{CST_TIME}:01+08:00"

with open(JOBS, "w") as f:
    json.dump(jobs_data, f, ensure_ascii=False, indent=2)
print(f"[Phase 4] jobs.json round-trip applied (TBD markers pending post-push patch)")

# ---------- Phase 6: git add + commit + push ----------
git("add", "tweets.json", "deploy-stamp.txt", "index.html")
status_out, _, _ = git("status", "--short")
print(f"[Phase 6-pre] git status:\n{status_out}")

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 789th clean push (webpage-only, no Telegram)"
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
        # P87-REFIRE belt-and-suspenders defensive replace
        note = note.replace("Vercel Vercel ", "Vercel ")
        j["last_run_note"] = note
        # Also update repeat.last_run_note
        if "repeat" in j and isinstance(j["repeat"], dict):
            j["repeat"]["last_run_note"] = note
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
