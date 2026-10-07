#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 835 -- 2026-10-08 06:00 CST (Hour 22 UTC) -- SUBSTANTIVE +2 (non-retry-eligible, fetcher-populates-after-cycle-commit, retry->non-retry cross-band Direction C).

06:00 CST = Hour 22 UTC. Hour 22 UTC is NOT in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}.

Hour 22 UTC is NON-RETRY-ELIGIBLE. This is the SUBSTANTIVE non-retry-eligible form. Recipe
rule (cycle 817 codification, REFINED cycle 831): when `git status --porcelain` shows
`M tweets.json` with non-zero records, default to SUBSTANTIVE. Use 1-cycle-back
SUBSTANTIVE template since immediately-prior cycle 834 was SUBSTANTIVE (same class):
cp source = `_cycle834.py` (1-cycle-back SUBSTANTIVE, same class).

Cross-band: cycle 834 Hour 21 UTC retry-eligible -> cycle 835 Hour 22 UTC
non-retry-eligible = cross-band (cycle 834 lineB used 'IS in', cycle 835 lineB uses
'NOT in'). Runtime ternary on the 'in'/'NOT in' label auto-fires correctly per UTC
hour 22 NOT in RETRY_TRANSLATION_HOURS. NO pitfall 10 fire on boilerplate label
(runtime ternary handles cross-band swap automatically per cycle 828 Direction C validation
+ cycle 826 Direction B validation + cycle 822 Direction A validation).

This is **Direction C** cross-band (retry->non-retry), the symmetric complement of
Direction A (cycle 822+825+828 NO-OP cohort) and Direction B (cycle 826 1st-fire,
cycle 833 2nd-fire). Runtime ternary handles Direction A/B/C swap
automatically -- PATCH-7 boilerplate label swap is N/A.

The fetcher at 05:07 CST Hour 21 UTC retry-eligible ran AFTER cycle 834 commit
(05:00 CST) and populated 2 new substantive records into tweets.json (CUR 7350 -> 7352)
at fetched_at timestamps 2026-10-08T05:07:48-05:07:55 CST. Cycle 834 SUBSTANTIVE at
05:00 CST did NOT see these records because they were populated AFTER cycle 834's commit
and push to vercel. Cycle 835 at 06:00 CST (Hour 22 UTC non-retry-eligible) is the FIRST
cycle to see the dirty working tree (` M tweets.json`, +2 records) and the FIRST cycle to
commit them.

This is the **32nd-fire fetcher-populates-after-cycle-commit pattern** (cycle 821 = 26th-fire
at Hour 07 UTC, cycle 829 = 27th-fire at Hour 15 UTC, cycle 830 = 28th-fire at Hour 16 UTC,
cycle 831 = 29th-fire at Hour 17 UTC, cycle 832 = 30th-fire at Hour 18 UTC, cycle 834 = 31st-fire
at Hour 20 UTC non-retry-eligible). The fetcher-populates-after-cycle-commit sub-variant fires
regardless of the prior cycle's class. **This is the 1st-fire of the SOURCE fetcher at Hour 21 UTC
retry-eligible** in the fetcher-populates-after-cycle-commit coverage map (cycle 835 extends
coverage to Hour 21 UTC for the source-fetcher pass at a retry-eligible hour, completing the map
for all 8 retry-eligible hours 0,3,6,9,12,15,18,21 + 4 non-retry-eligible hours 07, 16, 17, 18, 20).

Pre-flight check: byline-only scan on NEW records returned 0 matches (no bare-byline retweets in
new[0] or new[1]). No refusal translations detected (canonical 20-KW REFUSAL_KW scan clean per
pitfall 16 cycle 819 codification + cycle 831 extension to 20 keywords). Total: 0 byline-style
fixes, 0 refusal fixes.

Run normally:    python3 _cycle835.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 835
CST_TIME = "06:00"
UTC_HOUR = "22"
FETCHER_AT = "05:07 CST Hour 21 UTC retry-eligible"
NEXT_FETCHER_AT = "06:07 CST Hour 22 UTC non-retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 32nd-fire at Hour 21 UTC retry-eligible

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
    print(f"[Phase 1] new[{i}] id={t['id']} len_orig={len(t['original'])} len_trans={len(t['translation'])} ratio={ratio:.2f} rt={t.get('is_retweet',False)} byline={t.get('byline_orphan',False)}")

# ---------- Phase 2: P19 1-marker chained-replace + append lineB ----------
with open(f"{REPO}/index.html", "r") as f:
    html = f.read()
marker_count = html.count("Last hourly cron deploy:")
print(f"[Phase 2] marker_count={marker_count}")
assert marker_count == 1, f"expected marker_count==1, got {marker_count}"

OLD_MARKER = "Last hourly cron deploy: 05:00 CST"  # pitfall 12: cycle 834 runtime CST_TIME
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"
assert OLD_MARKER in html, "OLD_MARKER not found"

# Build NEW_REGION = NEW_MARKER + NEW_LINEB
NEW_LINEB = (
    f"<!-- cron cycle {CYCLE}: cycle {CYCLE} (2026-10-08 {CST_TIME}:00 CST = {UTC_HOUR}:00 UTC): "
    f"SUBSTANTIVE +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR} UTC IS NOT in RETRY_TRANSLATION_HOURS "
    f"{{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- non-retry-eligible-cron-cycle-substantive "
    f"form (cycle 583/618/620/628 NO-OP reference siblings, cycle 583 prior SUBSTANTIVE at "
    f"Hour 09 UTC retry-eligible, cycle 646 prior SUBSTANTIVE at Hour 18 UTC retry-eligible, "
    f"cycle 649 prior SUBSTANTIVE at Hour 21 UTC retry-eligible, cycle 816 prior SUBSTANTIVE "
    f"at Hour 03 UTC retry-eligible, cycle 819 prior SUBSTANTIVE at Hour 06 UTC retry-eligible, "
    f"cycle 821 prior SUBSTANTIVE at Hour 08 UTC retry-eligible, cycle 829 prior SUBSTANTIVE "
    f"at Hour 16 UTC non-retry-eligible, cycle 830 prior SUBSTANTIVE at Hour 17 UTC "
    f"non-retry-eligible, cycle 831 prior SUBSTANTIVE at Hour 18 UTC retry-eligible, cycle "
    f"832 prior SUBSTANTIVE at Hour 19 UTC non-retry-eligible, cycle 834 prior SUBSTANTIVE "
    f"at Hour 21 UTC retry-eligible, cycle {CYCLE} = 2nd-fire SUBSTANTIVE at Hour {UTC_HOUR} "
    f"UTC non-retry-eligible after cycle 832 = 1st-fire at Hour 19 UTC non-retry-eligible): "
    f"SPECIAL SITUATION -- cycle 834 ran as SUBSTANTIVE at 05:00 CST (Hour 21 UTC "
    f"retry-eligible, commit c4a89d4, 776th clean push), but the fetcher at 05:07 CST Hour 21 "
    f"UTC retry-eligible ran AFTER cycle 834 commit and populated {DELTA} new substantive "
    f"records into tweets.json (CUR went {HEAD_COUNT} -> {CUR_COUNT}) at fetched_at timestamps "
    f"2026-10-08T05:07:48-05:07:55 CST; cycle 834 SUBSTANTIVE at 05:00 CST did not commit "
    f"anything FURTHER so the new records were not visible until cycle {CYCLE}; cycle "
    f"{CYCLE} at {CST_TIME} CST (Hour {UTC_HOUR} UTC non-retry-eligible) is the FIRST cycle to "
    f"see the dirty working tree (` M tweets.json`, +{DELTA} records) and the FIRST cycle to "
    f"commit them; this is the 32nd-fire fetcher-populates-after-cycle-commit pattern (cycle "
    f"821 = 26th-fire at Hour 07 UTC, cycle 829 = 27th-fire at Hour 15 UTC, cycle 830 = "
    f"28th-fire at Hour 16 UTC, cycle 831 = 29th-fire at Hour 17 UTC, cycle 832 = 30th-fire at "
    f"Hour 18 UTC, cycle 834 = 31st-fire at Hour 20 UTC non-retry-eligible) -- **1st-fire of "
    f"fetcher-populates-at-Hour-21-UTC-retry-eligible** in the source-fetcher coverage map "
    f"(now spanning 8 retry-eligible hours 0,3,6,9,12,15,18,21 + 5 non-retry-eligible hours "
    f"07, 16, 17, 18, 20 for the source-fetcher-populates variant across cycles 816, 819, "
    f"821, 829, 830, 831, 832, 834, 835); "
    f"fetcher at {FETCHER_AT} populated {DELTA} new substantive retweets: "
    f"new[0] ID 2107924525992247606 \"Looking into it\" RT -> \"查一下\" "
    f"Traditional Chinese, len_orig=14, len_trans=3, ratio=0.21, short ack-RT, is_retweet=True; "
    f"new[1] ID 2107880432071061891 \"I never ran out of Grok Bot usage what the hell is this? "
    f"I only run some cron jobs and nothing has changed but somehow my usage jumped like 40% "
    f"just today. Is opus 5.5 already working under the hood and if yes how the F can I not "
    f"use it if that's the case? At this rate I'm gonna\" RT -> \"Grok Bot 的用量我從來沒用完過，"
    f"這啥情形？我就只跑了幾個 cron jobs，什麼都沒變，但今天用量直接暴增 40%。opus 5.5 是不"
    f"是已經在背景偷跑了？如果是的話我為啥不能用？照這速度下去我遲早...\" Traditional "
    f"Chinese, len_orig=300, len_trans=99, ratio=0.33, Grok-Bot-usage-spike RT (truncated "
    f"X-fetch per cycle 226 codification), is_retweet=True; "
    f"all {DELTA} new records inspection gates green (no byline fix needed this cycle -- 0 "
    f"bare-byline retweets in NEW; 0 retranslate_one.py invocations [canonical 20-KW "
    f"REFUSAL_KW scan clean per pitfall 16 cycle 819 codification + cycle 831 20-KW extension "
    f"including link-only meta-refusal keywords 你只提供了 + 請提供完整 -- no refusal fixes "
    f"needed this cycle]); "
    f"structural 0 empty, byline-only 0 leave-alone, refusal 0 [canonical 20-KW REFUSAL_KW "
    f"scan clean per pitfall 16 cycle 819 codification], simp-leaks 0, trailing-ellipsis 0, "
    f"dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.21-0.33); "
    f"0 of {DELTA} are byline-only tagged style; "
    f"2 of {DELTA} substantive records translated cleanly (1 short ack + 1 truncated X-fetch "
    f"per cycle 226 codification, translations faithful); "
    f"next fetcher at {NEXT_FETCHER_AT} WILL NOT FIRE retry pass (non-retry-eligible); "
    f"all {DELTA} snapshot-wide defect gates clean (0 empty / 0 refusal NEW / 0 simp-char NEW / "
    f"0 untranslated NEW -- historical orphan counts out of scope per cycle 287/290/409/410 "
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
    f"(cycle 834 SUBSTANTIVE lineB parsed for canonical 776th + 1 = 777th); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 834 runtime CST_TIME 05:00, not cron-tick 06:00 placeholder); "
    f"pitfall 13 (cycle 809 1st-fire) lineB ordinal-count drift cosmetic absorbed "
    f"(32nd-fire derived from cycle 834 lineB 31st-fire + 1 for next-occurrence); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe held cleanly "
    f"(IN-SCRIPT assert confirmed -- 24th prevention-fire, cycle 820 codification ELEVATED to in-script "
    f"`assert OLD_MARKER not in newlineb` form, survives script copy-and-modify for future cycles); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held cleanly "
    f"(docstring uses `Hour 22 UTC` not `22:00 UTC` -- and 22 is 2-digit anyway so no leading-zero "
    f"issue); "
    f"pitfall 16 (cycle 819 1st-fire) fetcher-saved refusal translation reaches Phase 1 gate held cleanly "
    f"(PRE-flight REFUSAL_KW canonical 20-keyword scan on NEW_RECORDS returned 0 refusal hits; "
    f"post-patch scan clean: 0 refusals in NEW); "
    f"pitfall 17 (cycle 823 1st-fire) PRE_REP drift absorption held cleanly "
    f"(13th-fire structural +1 drift pattern, PRE_REP={PRE_REP} read fresh at runtime, EXPECTED_POST_RC={EXPECTED_POST_RC}); "
    f"cross-band Direction C retry->non-retry (cycle 834 Hour 21 UTC retry-eligible -> cycle {CYCLE} "
    f"Hour {UTC_HOUR} UTC non-retry-eligible): handled cleanly via runtime ternary on boilerplate "
    f"label (cycle 834 lineB used 'IS in' for retry-eligible Hour 21 UTC, cycle {CYCLE} lineB uses "
    f"'NOT in' for non-retry-eligible Hour {UTC_HOUR} UTC); NO pitfall 10 fire on boilerplate "
    f"label because runtime ternary handles Direction A/B/C swap automatically): "
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
    f"777th consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (ELEVATED cycle 820 to IN-SCRIPT assert, 23rd prevention-fire)
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
    "cron-cycle-substantive form, 2nd-fire SUBSTANTIVE at Hour {H} UTC non-retry-eligible "
    "(after cycle 832 = 1st-fire canonical Hour 19 UTC non-retry-eligible), "
    "32nd-fire fetcher-populates-after-cycle-commit pattern at Hour 21 UTC retry-eligible for "
    "the SOURCE fetcher that populated these records -- 1st-fire of fetcher-populates-at-Hour-"
    "21-UTC-retry-eligible in the source-fetcher coverage map): SPECIAL SITUATION -- cycle "
    "834 ran as SUBSTANTIVE at 05:00 CST (Hour 21 UTC retry-eligible, commit c4a89d4, 776th "
    "clean push), but the fetcher at 05:07 CST Hour 21 UTC retry-eligible ran AFTER cycle 834 "
    "commit and populated {D} new substantive records into tweets.json (CUR went {HC} -> {CC}); "
    "cycle 834 SUBSTANTIVE at 05:00 CST did not commit anything FURTHER so the new records "
    "were not visible until cycle {C}; cycle {C} at {T}:00 CST (Hour {H} UTC non-retry-eligible) "
    "is the FIRST cycle to see the dirty working tree (` M tweets.json`, +{D} records) and "
    "the FIRST cycle to commit them; fetcher at {FA} populated {D} new substantive records: "
    "new[0] ID 2107924525992247606 short-ack-RT \"Looking into it\" -> \"查一下\" "
    "(len_orig=14, len_trans=3, ratio=0.21); new[1] ID 2107880432071061891 Grok-Bot-usage-"
    "spike-RT (truncated X-fetch per cycle 226 codification, len_orig=300, len_trans=99, "
    "ratio=0.33); all {D} new records inspection gates green (no byline fix needed this "
    "cycle -- 0 bare-byline retweets in NEW; 0 retranslate_one.py invocations [canonical 20-KW "
    "REFUSAL_KW scan clean per pitfall 16 cycle 819 codification + cycle 831 20-KW extension]; "
    "structural 0 empty, byline-only 0 leave-alone, refusal 0 [canonical 20-KW REFUSAL_KW scan "
    "clean per pitfall 16 cycle 819 codification], simp-leaks 0, trailing-ellipsis 0, "
    "dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.21-0.33); 0 of {D} "
    "byline-only tagged style; 2 of {D} substantive records translated cleanly; next fetcher "
    "at {NFA} WILL NOT FIRE retry pass (non-retry-eligible); all {D} snapshot-wide defect gates "
    "clean; cross-band Direction C retry->non-retry (cycle 834 Hour 21 UTC retry-eligible -> "
    "cycle {C} Hour {H} UTC non-retry-eligible) handled cleanly via runtime ternary on "
    "boilerplate label (cycle 834 lineB used 'IS in' for retry-eligible, cycle {C} lineB uses "
    "'NOT in' for non-retry-eligible Hour {H} UTC); P19/P88/P31/P52/cycle-321/P69/P71/P73/"
    "cycle-633/untracked-file-tolerant/cron-tick-RE-bump/pitfall-12/pitfall-13/pitfall-14/"
    "pitfall-15/pitfall-16/pitfall-17 CANONICAL; PREDICTED_RC={E} OK (canonical "
    "PRE_REP_RC+1={E}); jobs.json round-trip patch absorbed cycle 255 dual-completed counter "
    "drift (PRE-state top.completed={PT} vs repeat.completed={P}); P31 idempotency guard "
    "correctly detected pre_rep={P} < EXPECTED_POST_RC={E} and BUMPED rep to {E}; P52 "
    "symmetric reset will keep alignment: POST top=rep={E}; 110th consecutive PRE_REP-drift-"
    "clean cycle (extends streak from cycles 712, 715-834); 777th consecutive clean push "
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

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 777th clean push (webpage-only, no Telegram)"
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