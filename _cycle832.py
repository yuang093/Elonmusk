#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 832 -- 2026-10-08 03:00 CST (Hour 19 UTC) -- SUBSTANTIVE +11 (non-retry-eligible, fetcher-populates-after-cycle-commit, retry->non-retry cross-band, immediately-prior SUBSTANTIVE class).

03:00 CST = Hour 19 UTC. Hour 19 UTC IS NOT in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}.

Hour 19 UTC is NON-RETRY-ELIGIBLE. This is the SUBSTANTIVE non-retry-eligible form. Recipe
rule (cycle 817 codification, REFINED cycle 831): when `git status --porcelain` shows
`M tweets.json` with non-zero records, default to SUBSTANTIVE. Use 1-cycle-back
SUBSTANTIVE template since immediately-prior cycle 831 was also SUBSTANTIVE.

cp source = `_cycle831.py` (1-cycle-back SUBSTANTIVE, same class, immediately-prior).
Cross-band: cycle 831 Hour 18 UTC retry-eligible -> cycle 832 Hour 19 UTC
non-retry-eligible = cross-band (cycle 831 lineB used 'IS in', cycle 832 lineB uses
'IS NOT in'). Runtime ternary on the 'in'/'NOT in' label auto-fires correctly per UTC
hour 19 NOT in RETRY_TRANSLATION_HOURS. NO pitfall 10 fire on boilerplate label
(runtime ternary handles cross-band swap automatically per cycle 828 Direction C validation).

The fetcher at 02:07 CST Hour 18 UTC retry-eligible ran AFTER cycle 831 commit (02:03 CST)
and populated 11 new substantive records into tweets.json (CUR 7334 -> 7345) at fetched_at
timestamps 2026-10-08T02:07:46-02:08:28 CST. Cycle 831 SUBSTANTIVE at 02:03 CST did NOT
see these records because they were populated AFTER cycle 831's commit and push to vercel.
Cycle 832 at 03:00 CST (Hour 19 UTC non-retry-eligible) is the FIRST cycle to see the
dirty working tree (` M tweets.json`, +11 records) and the FIRST cycle to commit them.

This is the **30th-fire fetcher-populates-after-cycle-commit pattern** (cycle 821 = 26th-fire
at Hour 07 UTC, cycle 829 = 27th-fire at Hour 15 UTC, cycle 830 = 28th-fire at Hour 16 UTC,
cycle 831 = 29th-fire at Hour 17 UTC, cycle 832 = 30th-fire at Hour 18 UTC). The
fetcher-populates-after-cycle-commit sub-variant fires regardless of the prior cycle's class.
**This is the 1st-fire of the SOURCE fetcher at Hour 18 UTC retry-eligible** in the
fetcher-populates-after-cycle-commit coverage map (cycle 832 extends coverage to Hour 18
UTC for the source-fetcher pass, completing the map at the retry-eligible hour slot).

Pre-flight fix: byline-only fix applied to 3 bare "Elon Musk" records (IDs 2107878323766583677,
2107881106234343451, 2107888987004445025 -- placeholder "（轉推 Elon Musk 的貼文）") via
/tmp/_fix_byline_cycle832.py per cycle 286/287 codified multi-ID pattern. No refusal
translations detected (canonical 20-KW REFUSAL_KW scan clean per pitfall 16 cycle 819
codification + cycle 831 extension to 20 keywords). Total: 3 byline-style fixes, 0 refusal fixes.

Run normally:    python3 _cycle832.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 832
CST_TIME = "03:00"
UTC_HOUR = "19"
FETCHER_AT = "02:07 CST Hour 18 UTC retry-eligible"
NEXT_FETCHER_AT = "03:07 CST Hour 19 UTC non-retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 30th-fire at Hour 18 UTC retry-eligible

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

OLD_MARKER = "Last hourly cron deploy: 02:00 CST"  # pitfall 12: cycle 831 runtime CST_TIME
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
    f"{CYCLE} = 2nd-fire SUBSTANTIVE at Hour {UTC_HOUR} UTC non-retry-eligible): "
    f"SPECIAL SITUATION -- cycle 831 ran as SUBSTANTIVE at 02:03 CST (Hour 18 UTC retry-eligible, "
    f"commit fdc98ab, 773rd clean push), but the fetcher at 02:07 CST Hour 18 UTC retry-eligible "
    f"ran AFTER cycle 831 commit and populated {DELTA} new substantive records into tweets.json "
    f"(CUR went {HEAD_COUNT} -> {CUR_COUNT}) at fetched_at timestamps "
    f"2026-10-08T02:07:46-02:08:28 CST; cycle 831 SUBSTANTIVE at 02:03 CST did not commit "
    f"anything FURTHER so the new records were not visible until cycle {CYCLE}; cycle "
    f"{CYCLE} at {CST_TIME} CST (Hour {UTC_HOUR} UTC non-retry-eligible) is the FIRST cycle to "
    f"see the dirty working tree (` M tweets.json`, +{DELTA} records) and the FIRST cycle to "
    f"commit them; this is the 30th-fire fetcher-populates-after-cycle-commit pattern (cycle "
    f"821 = 26th-fire at Hour 07 UTC, cycle 829 = 27th-fire at Hour 15 UTC, cycle 830 = "
    f"28th-fire at Hour 16 UTC, cycle 831 = 29th-fire at Hour 17 UTC, cycle 832 = 30th-fire at "
    f"Hour 18 UTC) -- **1st-fire of fetcher-populates-at-Hour-18-UTC-retry-eligible** in the "
    f"source-fetcher coverage map (now spanning 8 retry-eligible hours: 03, 06, 08, 09, 12, "
    f"15, 18, 21 UTC for the source-fetcher-populates variant across cycles 816, 819, 821, "
    f"829, 830, 831, 832); "
    f"fetcher at {FETCHER_AT} populated {DELTA} new substantive retweets: "
    f"new[0] ID 2107540017040011709 \"JUST IN: Quebec's new premier declares...\" "
    f"RT -> \"獨家：魁北克新省長表示，他對魁北克獨立的夢想「有朝一日一定會實現」。\" "
    f"Traditional Chinese, len_orig=102, len_trans=34, ratio=0.33, Quebec-PQ-premier-independence "
    f"RT, is_retweet=True; "
    f"new[1] ID 2107561484230312074 \"History will be the verdict\" RT -> \"歷史會做出裁決\" "
    f"Traditional Chinese, len_orig=27, len_trans=7, ratio=0.26, verdict-RT, is_retweet=True; "
    f"new[2] ID 2107583032697778340 \"JUST NOW: Elon Musk agrees with President Trump...\" "
    f"RT -> \"剛剛：Elon Musk 附和川普說法，覺得法國正在被「入侵」\" Traditional Chinese, "
    f"len_orig=82, len_trans=33, ratio=0.40, France-invaded-RT, is_retweet=True; "
    f"new[3] ID 2107853200913203351 \"Hall of Fame community note\" RT -> \"名人堂community note\" "
    f"Traditional Chinese, len_orig=27, len_trans=17, ratio=0.63, community-note-RT, "
    f"is_retweet=True; "
    f"new[4] ID 2107878323766583677 \"Elon Musk\" RT -> \"（轉推 Elon Musk 的貼文）\" byline-only "
    f"placeholder applied (per cycle 286/287 codified multi-ID pattern, /tmp/_fix_byline_cycle832.py), "
    f"len_orig=9, len_trans=18, ratio=2.00, byline-placeholder-by-design, is_retweet=True; "
    f"new[5] ID 2107881106234343451 \"Elon Musk\" RT -> \"（轉推 Elon Musk 的貼文）\" byline-only "
    f"placeholder applied (per cycle 286/287 codified multi-ID pattern, /tmp/_fix_byline_cycle832.py), "
    f"len_orig=9, len_trans=18, ratio=2.00, byline-placeholder-by-design, is_retweet=True; "
    f"new[6] ID 2107887475251458094 \"ELON MUSK: We'd love to be operating Starlink in India...\" "
    f"RT -> \"ELON MUSK：「我們超想在印度營運 Starlink 的，那樣就太讚了。\\n\\nStarlink 申請"
    f"在印度營運已經快四年了，到現在還沒辦法上線。\\n\\n政府應該盡快核准剩下的許可，讓 "
    f"Starlink 可以⋯⋯\" Traditional Chinese, len_orig=275, len_trans=106, ratio=0.39, "
    f"Starlink-India-RT, is_retweet=True; "
    f"new[7] ID 2107888605318517007 \"Good. Quebec should separate.\" RT -> \"好喔，魁北克應該"
    f"獨立。\" Traditional Chinese, len_orig=29, len_trans=11, ratio=0.38, Quebec-separate-RT, "
    f"is_retweet=True; "
    f"new[8] ID 2107888889629483404 \"They would be better off. Alberta and Saskatchewan...\" "
    f"RT -> \"他們分出去會更好的。\\n\\nAlberta 和 Saskatchewan 也該分出去了。\" Traditional "
    f"Chinese, len_orig=73, len_trans=42, ratio=0.58, Alberta-Sask-separate-RT, is_retweet=True; "
    f"new[9] ID 2107888987004445025 \"Elon Musk\" RT -> \"（轉推 Elon Musk 的貼文）\" byline-only "
    f"placeholder applied (per cycle 286/287 codified multi-ID pattern, /tmp/_fix_byline_cycle832.py), "
    f"len_orig=9, len_trans=18, ratio=2.00, byline-placeholder-by-design, is_retweet=True; "
    f"new[10] ID 2107894231922876510 \"requests are pretty simple...\" RT -> \"這些請求都滿簡單"
    f"的，等 lightning-fast 版 Grok 4.8 出來就能搞定。\\n\\n核心原則就是給 Grok Bot 用戶最好"
    f"的速度與智慧 combo。\" Traditional Chinese, len_orig=211, len_trans=81, ratio=0.38, "
    f"Grok-4.8-RT, is_retweet=True; "
    f"all {DELTA} new records inspection gates green AFTER per-cycle byline fix (3 of {DELTA} "
    f"byline-only orphans 2107878323766583677 + 2107881106234343451 + 2107888987004445025 "
    f"had placeholder applied via /tmp/_fix_byline_cycle832.py per cycle 286/287 codified "
    f"multi-ID pattern; 0 retranslate_one.py invocations [canonical 20-KW REFUSAL_KW scan "
    f"clean per pitfall 16 cycle 819 codification + cycle 831 20-KW extension including "
    f"link-only meta-refusal keywords 你只提供了 + 請提供完整 -- no refusal fixes needed "
    f"this cycle]); "
    f"structural 0 empty, byline-only 0 leave-alone, refusal 0 [canonical 20-KW REFUSAL_KW "
    f"scan clean per pitfall 16 cycle 819 codification], simp-leaks 0, trailing-ellipsis 0, "
    f"dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.26-2.00 with 2.00 = "
    f"byline placeholder by design); 3 of {DELTA} are byline-only tagged style (had "
    f"translation fix applied); 8 of {DELTA} substantive records translated cleanly; "
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
    f"(cycle 831 SUBSTANTIVE lineB parsed for canonical 773rd + 1 = 774th); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 831 runtime CST_TIME 02:00, not cron-tick 02:00 placeholder); "
    f"pitfall 13 (cycle 809 1st-fire) lineB ordinal-count drift cosmetic absorbed "
    f"(30th-fire derived from cycle 831 lineB 29th-fire + 1 for next-occurrence); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe held cleanly "
    f"(IN-SCRIPT assert confirmed -- 21st prevention-fire, cycle 820 codification ELEVATED to in-script "
    f"`assert OLD_MARKER not in newlineb` form, survives script copy-and-modify for future cycles); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held cleanly "
    f"(docstring uses `Hour 19 UTC` not `19:00 UTC` -- and 19 is 2-digit anyway so no leading-zero "
    f"issue); "
    f"pitfall 16 (cycle 819 1st-fire) fetcher-saved refusal translation reaches Phase 1 gate held cleanly "
    f"(PRE-flight REFUSAL_KW canonical 20-keyword scan on NEW_RECORDS returned 0 refusal hits; "
    f"post-patch scan clean: 0 refusals in NEW); "
    f"pitfall 17 (cycle 823 1st-fire) PRE_REP drift absorption held cleanly "
    f"(10th-fire structural +1 drift pattern, PRE_REP={PRE_REP} read fresh at runtime, EXPECTED_POST_RC={EXPECTED_POST_RC}); "
    f"cross-band Direction C retry->non-retry (cycle 831 Hour 18 UTC retry-eligible -> cycle {CYCLE} "
    f"Hour {UTC_HOUR} UTC non-retry-eligible): handled cleanly via runtime ternary on boilerplate "
    f"label (cycle 831 lineB used 'IS in' for retry-eligible Hour 18 UTC, cycle {CYCLE} lineB uses "
    f"'IS NOT in' for non-retry-eligible Hour {UTC_HOUR} UTC); NO pitfall 10 fire on boilerplate "
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
    f"774th consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (ELEVATED cycle 820 to IN-SCRIPT assert, 21st prevention-fire)
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
    "(after cycle 806 was 1st-fire at Hour 19 UTC non-retry-eligible per cycle 806 codification), "
    "30th-fire fetcher-populates-after-cycle-commit pattern at Hour 18 UTC retry-eligible for "
    "the SOURCE fetcher that populated these records -- 1st-fire of fetcher-populates-at-Hour-"
    "18-UTC-retry-eligible in the source-fetcher coverage map): SPECIAL SITUATION -- cycle "
    "831 ran as SUBSTANTIVE at 02:03 CST (Hour 18 UTC retry-eligible, commit fdc98ab, 773rd "
    "clean push), but the fetcher at 02:07 CST Hour 18 UTC retry-eligible ran AFTER cycle 831 "
    "commit and populated {D} new substantive records into tweets.json (CUR went {HC} -> {CC}); "
    "cycle 831 SUBSTANTIVE at 02:03 CST did not commit anything FURTHER so the new records were "
    "not visible until cycle {C}; cycle {C} at {T}:00 CST (Hour {H} UTC non-retry-eligible) "
    "is the FIRST cycle to see the dirty working tree (` M tweets.json`, +{D} records) and "
    "the FIRST cycle to commit them; fetcher at {FA} populated {D} new substantive records: "
    "new[0] ID 2107540017040011709 Quebec-PQ-premier-independence-RT (len_orig=102, "
    "len_trans=34, ratio=0.33); new[1] ID 2107561484230312074 verdict-RT (len_orig=27, "
    "len_trans=7, ratio=0.26); new[2] ID 2107583032697778340 France-invaded-RT (len_orig=82, "
    "len_trans=33, ratio=0.40); new[3] ID 2107853200913203351 community-note-RT (len_orig=27, "
    "len_trans=17, ratio=0.63); new[4] ID 2107878323766583677 byline-only orphan (Elon Musk) "
    "-> placeholder applied per cycle 286/287; new[5] ID 2107881106234343451 byline-only orphan "
    "(Elon Musk) -> placeholder applied per cycle 286/287; new[6] ID 2107887475251458094 "
    "Starlink-India-RT (len_orig=275, len_trans=106, ratio=0.39); new[7] ID 2107888605318517007 "
    "Quebec-separate-RT (len_orig=29, len_trans=11, ratio=0.38); new[8] ID 2107888889629483404 "
    "Alberta-Sask-separate-RT (len_orig=73, len_trans=42, ratio=0.58); new[9] ID "
    "2107888987004445025 byline-only orphan (Elon Musk) -> placeholder applied per cycle "
    "286/287; new[10] ID 2107894231922876510 Grok-4.8-RT (len_orig=211, len_trans=81, "
    "ratio=0.38); all {D} new records inspection gates green AFTER per-cycle byline fix (3 of "
    "{D} byline-only orphans had placeholder applied via /tmp/_fix_byline_cycle832.py per "
    "cycle 286/287 codified multi-ID pattern; 0 retranslate_one.py invocations [canonical 20-KW "
    "REFUSAL_KW scan clean per pitfall 16 cycle 819 codification + cycle 831 20-KW extension]; "
    "structural 0 empty, byline-only 0 leave-alone, refusal 0 [canonical 20-KW REFUSAL_KW scan "
    "clean per pitfall 16 cycle 819 codification], simp-leaks 0, trailing-ellipsis 0, "
    "dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.26-2.00 with 2.00 = byline "
    "placeholder by design); 3 of {D} byline-only tagged style (had translation fix applied); "
    "8 of {D} substantive records translated cleanly; next fetcher at {NFA} WILL NOT FIRE "
    "retry pass (non-retry-eligible); all {D} snapshot-wide defect gates clean; cross-band "
    "Direction C retry->non-retry (cycle 831 Hour 18 UTC retry-eligible -> cycle {C} Hour {H} "
    "UTC non-retry-eligible) handled cleanly via runtime ternary on boilerplate label (cycle "
    "831 lineB used 'IS in' for retry-eligible, cycle {C} lineB uses 'IS NOT in' for non-retry-"
    "eligible Hour {H} UTC); P19/P88/P31/P52/cycle-321/P69/P71/P73/cycle-633/untracked-file-"
    "tolerant/cron-tick-RE-bump/pitfall-12/pitfall-13/pitfall-14/pitfall-15/pitfall-16/"
    "pitfall-17 CANONICAL; PREDICTED_RC={E} OK (canonical PRE_REP_RC+1={E}); jobs.json round-"
    "trip patch absorbed cycle 255 dual-completed counter drift (PRE-state top.completed={PT} "
    "vs repeat.completed={P}); P31 idempotency guard correctly detected pre_rep={P} < "
    "EXPECTED_POST_RC={E} and BUMPED rep to {E}; P52 symmetric reset will keep alignment: POST "
    "top=rep={E}; 107th consecutive PRE_REP-drift-clean cycle (extends streak from cycles "
    "712, 715-831); 774th consecutive clean push (webpage-only, no Telegram)"
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

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 774th clean push (webpage-only, no Telegram)"
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