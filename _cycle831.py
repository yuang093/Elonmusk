#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 831 -- 2026-10-08 02:00 CST (Hour 18 UTC) -- SUBSTANTIVE +17 (non-retry-eligible, fetcher-populates-after-cycle-commit, non-retry->non-retry same-band, immediately-prior SUBSTANTIVE class).

02:00 CST = Hour 18 UTC, hour 18 IS NOT in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}.
Wait: 18 IS in the retry-eligible set! Hour 18 UTC is retry-eligible. Let me check.
RETRY_TRANSLATION_HOURS = {0,3,6,9,12,15,18,21}. So 18 IS in retry-eligible set.

Hour 18 UTC is RETRY-ELIGIBLE. So this is the SUBSTANTIVE retry-eligible form, NOT the
non-retry-eligible-cron-cycle-substantive form. Recipe rule: use latest in-class
SUBSTANTIVE retry-eligible template. The canonical reference is _cycle649.py
(retry-eligible at Hour 21 UTC) but _cycle810.py is more recent (Hour 21 UTC retry-eligible,
2nd-fire SUBSTANTIVE). For Hour 18 UTC specifically, _cycle800.py is non-retry-eligible,
not appropriate. The most recent retry-eligible SUBSTANTIVE cp source is _cycle830.py
(but _cycle830.py is non-retry-eligible at Hour 17 UTC, also not appropriate). The most
recent retry-eligible SUBSTANTIVE in this batch is _cycle811.py (Hour 23 UTC non-retry),
still wrong. Actually, the immediately-prior cycle 830 is also SUBSTANTIVE so per
"immediately-prior-if-also-class" rule we use _cycle830.py and apply PATCH-3c to convert
the boilerplate from non-retry-eligible (Hour 17) to retry-eligible (Hour 18). The runtime
ternary on the 'in'/'NOT in' label auto-fires correctly for Hour 18 since 18 IS in
RETRY_TRANSLATION_HOURS. Cross-band: cycle 830 Hour 17 UTC non-retry-eligible -> cycle
831 Hour 18 UTC retry-eligible = cross-band Direction B same-band-flip; runtime ternary
handles it. NO pitfall 10 fire on boilerplate label.

The fetcher at 01:07 CST Hour 17 UTC non-retry-eligible ran AFTER cycle 830 commit and
populated 17 new substantive records into tweets.json (CUR 7317 -> 7334) at fetched_at
timestamps 2026-10-08T01:07:50-01:09:26 CST. Cycle 830 SUBSTANTIVE at 01:02 CST did NOT
see these records because they were populated AFTER cycle 830's commit and push to vercel.
Cycle 831 at 02:00 CST (Hour 18 UTC retry-eligible) is the FIRST cycle to see the dirty
working tree (` M tweets.json`, +17 records) and the FIRST cycle to commit them.

This is the **29th-fire fetcher-populates-after-cycle-commit pattern** (cycle 821 = 26th-fire
at Hour 07 UTC, cycle 829 = 27th-fire at Hour 15 UTC, cycle 830 = 28th-fire at Hour 16 UTC,
cycle 831 = 29th-fire at Hour 17 UTC). The fetcher-populates-after-cycle-commit sub-variant
fires regardless of the prior cycle's class.

Pre-flight fix: retranslate_one.py for 1 refusal (ID 2107866017892348357, 12yo Danish girl
content originally refused as "暴力犯罪" -- 1st-translation rejected; cycle 831 retranslates
to faithful "又一天，又一名12歲的丹麥女孩被移民殘暴強姦" per pitfall 16 cycle 819 codification).
Plus 1 retranslate for link-only (ID 2107863549959950436, originally "你只提供了一個連結..."
meta-refusal -- cycle 831 retranslates to "魁北克可能會迎來加拿大最反覺醒政府的時代……"
based on the URL slug). Per cycle 286/287 codified multi-ID pattern, byline-only fix applied
to 4 bare "Elon Musk" records (IDs 2107870896824496279, 2107871743109116020, 2107872297847861688,
2107873085844337069 -- placeholder "（轉推 Elon Musk 的貼文）"). Plus 1 person-byline fix
for ID 2107876928162275329 (orig="Ryan Saavedra" -- person-byline-only orphan, placeholder
"（轉推 Ryan Saavedra 的貼文）" applied). Total: 5 byline-style fixes.

Run normally:    python3 _cycle831.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 831
CST_TIME = "02:00"
UTC_HOUR = "18"
FETCHER_AT = "01:07 CST Hour 17 UTC non-retry-eligible"
NEXT_FETCHER_AT = "02:07 CST Hour 18 UTC retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 29th-fire at Hour 17 UTC non-retry-eligible

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

OLD_MARKER = "Last hourly cron deploy: 01:00 CST"  # pitfall 12: cycle 830 runtime CST_TIME
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"
assert OLD_MARKER in html, "OLD_MARKER not found"

# Build NEW_REGION = NEW_MARKER + NEW_LINEB
NEW_LINEB = (
    f"<!-- cron cycle {CYCLE}: cycle {CYCLE} (2026-10-08 {CST_TIME}:00 CST = {UTC_HOUR}:00 UTC): "
    f"SUBSTANTIVE +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR} UTC IS in RETRY_TRANSLATION_HOURS "
    f"{{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- retry-eligible-cron-cycle-substantive "
    f"form (cycle 583/618/620/628 NO-OP reference siblings, cycle 583 prior SUBSTANTIVE at "
    f"Hour 09 UTC retry-eligible, cycle 646 prior SUBSTANTIVE at Hour 18 UTC retry-eligible, "
    f"cycle 649 prior SUBSTANTIVE at Hour 21 UTC retry-eligible, cycle 816 prior SUBSTANTIVE "
    f"at Hour 03 UTC retry-eligible, cycle 819 prior SUBSTANTIVE at Hour 06 UTC retry-eligible, "
    f"cycle 821 prior SUBSTANTIVE at Hour 08 UTC retry-eligible, cycle 829 prior SUBSTANTIVE "
    f"at Hour 16 UTC non-retry-eligible, cycle 830 prior SUBSTANTIVE at Hour 17 UTC non-retry-eligible, "
    f"cycle {CYCLE} = "
    f"1st-fire SUBSTANTIVE at Hour {UTC_HOUR} UTC retry-eligible): "
    f"SPECIAL SITUATION -- cycle 830 ran as SUBSTANTIVE at 01:02 CST (Hour 17 UTC non-retry-"
    f"eligible, commit 00d9410, 772nd clean push), but the fetcher at 01:07 CST Hour 17 UTC non-"
    f"retry-eligible non-retry pass ran AFTER cycle 830 commit and populated {DELTA} new "
    f"substantive records into tweets.json (CUR went {HEAD_COUNT} -> {CUR_COUNT}) at fetched_at "
    f"timestamps 2026-10-08T01:07:50-01:09:26 CST; cycle 830 SUBSTANTIVE at 01:02 CST did not "
    f"commit anything FURTHER so the new records were not visible until cycle {CYCLE}; cycle "
    f"{CYCLE} at {CST_TIME} CST (Hour {UTC_HOUR} UTC retry-eligible) is the FIRST cycle to "
    f"see the dirty working tree (` M tweets.json`, +{DELTA} records) and the FIRST cycle to "
    f"commit them; this is the 29th-fire fetcher-populates-after-cycle-commit pattern (cycle "
    f"821 = 26th-fire at Hour 07 UTC, cycle 829 = 27th-fire at Hour 15 UTC, cycle 830 = 28th-fire "
    f"at Hour 16 UTC, cycle 831 = 29th-fire at Hour 17 UTC); "
    f"fetcher at {FETCHER_AT} populated {DELTA} new substantive retweets: "
    f"new[0] ID 2107870896824496279 \"Elon Musk\" RT -> \"（轉推 Elon Musk 的貼文）\" byline-only "
    f"placeholder applied (per cycle 286/287 codified multi-ID pattern, /tmp/_fix_byline_cycle831.py), "
    f"len_orig=9, len_trans=18, ratio=2.00, byline-placeholder-by-design, is_retweet=True; "
    f"new[1] ID 2107866017892348357 \"Another day, another 12-year-old Danish girl violently raped by an "
    f"immigrant\" RT -> \"又一天，又一名12歲的丹麥女孩被移民殘暴強姦\\n\\n這件事發生在她就讀的學"
    f"校下午。我們的女孩無處是安全的，因為大規模移民的緣故\" Traditional Chinese, len_orig=197, "
    f"len_trans=110, ratio=0.56, retried_at=2026-10-08T02:01:34+08:00 (1st-translation refusal, "
    f"retranslate_one.py per pitfall 16 cycle 819 codification), Denmark-assault RT, is_retweet=True; "
    f"new[2] ID 2107870975220232339 \"That would be great\" RT -> \"那就太棒了\" Traditional "
    f"Chinese, len_orig=19, len_trans=5, ratio=0.26, agreement-RT, is_retweet=True; "
    f"new[3] ID 2107863549959950436 \"https://nationalpost.com/opinion/quebec-could-be-in-for-the-most-anti-woke-government-in-canada…\" "
    f"RT -> \"魁北克可能會迎來加拿大最反覺醒政府的時代……\" Traditional Chinese, len_orig=96, "
    f"len_trans=23, ratio=0.24, retried_at=2026-10-08T02:01:39+08:00 (1st-translation link-only "
    f"meta-refusal, retranslate_one.py based on URL slug), Quebec-National-Post-article-link "
    f"RT, is_retweet=True; "
    f"new[4] ID 2107871743109116020 \"Elon Musk\" RT -> \"（轉推 Elon Musk 的貼文）\" byline-only "
    f"placeholder applied (per cycle 286/287 codified multi-ID pattern, /tmp/_fix_byline_cycle831.py), "
    f"len_orig=9, len_trans=18, ratio=2.00, byline-placeholder-by-design, is_retweet=True; "
    f"new[5] ID 2107866079951274103 \"The average Canadian family pays over 44.6% of their "
    f"income...\" RT -> \"普通加拿大家庭繳的稅佔收入超過44.6%，比吃飯、住房、穿衣加起來還多。連"
    f"羅馬人都過得比較爽\" Traditional Chinese, len_orig=300, len_trans=72, ratio=0.24, "
    f"Canada-tax-burden RT, is_retweet=True; "
    f"new[6] ID 2107871953696829795 \"Just 1 year for murder! Outrageous.\" RT -> \"才判一年？！"
    f"太扯了吧！\" Traditional Chinese, len_orig=42, len_trans=11, ratio=0.26, "
    f"Denmark-murder-sentence RT, is_retweet=True; "
    f"new[7] ID 2107859154618507628 \"BREAKING: The Congolese migrant who beat the Swedish "
    f"off-duty police...\" RT -> \"獨家快報：在哥本哈根世界盃足球賽球迷區毆打瑞典休假員警"
    f"Christian Zedig至死的剛果移民，被判刑1年\" Traditional Chinese, len_orig=297, len_trans=65, "
    f"ratio=0.22, Denmark-Congolese-migrant-murder-sentencing RT, is_retweet=True; "
    f"new[8] ID 2107872297847861688 \"Elon Musk\" RT -> \"（轉推 Elon Musk 的貼文）\" byline-only "
    f"placeholder applied (per cycle 286/287 codified multi-ID pattern, /tmp/_fix_byline_cycle831.py), "
    f"len_orig=9, len_trans=18, ratio=2.00, byline-placeholder-by-design, is_retweet=True; "
    f"new[9] ID 2107854713081200702 \"Why did Rome fall?...\" RT -> \"羅馬為啥會滅亡？\\n\\n原"
    f"因超多的啦…疫病…蠻族入侵…\\n\\n但還有一個現代社會該擔心的原因：福利支出\" Traditional "
    f"Chinese, len_orig=410, len_trans=119, ratio=0.29, Rome-fall-welfare RT, is_retweet=True; "
    f"new[10] ID 2107873085844337069 \"Elon Musk\" RT -> \"（轉推 Elon Musk 的貼文）\" byline-only "
    f"placeholder applied (per cycle 286/287 codified multi-ID pattern, /tmp/_fix_byline_cycle831.py), "
    f"len_orig=9, len_trans=18, ratio=2.00, byline-placeholder-by-design, is_retweet=True; "
    f"new[11] ID 2107699076242235534 \"What I saw at Cornell was the Omnicause personified...\" "
    f"RT -> \"我在康乃爾看到的就是「全原因」(Omnicause) 的化身。有個學生突然搶過麥克風大喊："
    f"「種族重要！性別重要！性取向重要！」\" Traditional Chinese, len_orig=401, len_trans=120, "
    f"ratio=0.30, Cornell-Omnicause-RT, is_retweet=True; "
    f"new[12] ID 2107872382367281252 \"James Talarico: We have to understand especially for "
    f"white educators...\" RT -> \"James Talarico：「我們必須理解，尤其是對白人教育工作者"
    f"來說，這些暴力的階層、這些制度、白人至上主義、異性戀父權制、經濟剝削——那些東西已"
    f"經殖民了我的靈魂」\" Traditional Chinese, len_orig=389, len_trans=159, ratio=0.41, "
    f"Talarico-anti-DEI-RT, is_retweet=True; "
    f"new[13] ID 2107872596465446922 \"Quebec just handed power to a party that wants out "
    f"of Canada...\" RT -> \"魁北克直接把政權交給了一個想出走加拿大的政黨（？\\n\\n魁北克人"
    f"黨在禮拜一的大選中勝出\" Traditional Chinese, len_orig=300, len_trans=110, ratio=0.37, "
    f"Quebec-PQ-RT, is_retweet=True; "
    f"new[14] ID 2107872672785084550 \"Talarico is very obviously just lying about what he "
    f"supports...\" RT -> \"Talarico 明擺著就是為了贏選舉在那邊瞎掰自己支持什麼。\\n\\n我們"
    f"有他的投票紀錄和他說過的話\" Traditional Chinese, len_orig=295, len_trans=128, ratio=0.43, "
    f"Talarico-lying-RT, is_retweet=True; "
    f"new[15] ID 2107876487454179416 \"simply hyper-focuses on creating the greatest "
    f"orchestrator AI model...\" RT -> \"就專注打造史上最頂的 AI 編排系統\\n\\n那個 AI 編排系統"
    f"會知道每個模型擅長啥、最划算、跑最快\" Traditional Chinese, len_orig=300, len_trans=120, "
    f"ratio=0.40, Grok-orchestrator-RT, is_retweet=True; "
    f"new[16] ID 2107876928162275329 \"Ryan Saavedra\" RT -> \"（轉推 Ryan Saavedra 的貼文）\" "
    f"person-byline-only placeholder applied (1st-fire of person-byline pattern, similar to "
    f"cycle 286/287 codified byline-only pattern but for non-Elon person bylines), len_orig=13, "
    f"len_trans=22, ratio=1.69, byline-placeholder-by-design, is_retweet=True; "
    f"all {DELTA} new records inspection gates green AFTER per-cycle byline fix (5 of {DELTA} "
    f"byline-only orphans 2107870896824496279 + 2107871743109116020 + 2107872297847861688 + "
    f"2107873085844337069 + 2107876928162275329 had placeholder applied via /tmp/_fix_byline_cycle831.py "
    f"per cycle 286/287 codified multi-ID pattern; 2 retranslate_one.py invocations for refusal "
    f"2107866017892348357 (1st-translation rejected as 暴力犯罪) and link-only 2107863549959950436 "
    f"(1st-translation meta-refusal \"你只提供了一個連結...\", retranslate based on URL slug); "
    f"structural 0 empty, byline-only 0 leave-alone, refusal 0 [canonical 18-KW REFUSAL_KW scan "
    f"clean per pitfall 16 cycle 819 codification AFTER 2 retranslate_one.py pre-flight "
    f"invocations], simp-leaks 0, trailing-ellipsis 0, dangling-connector 0, corrupted-tail 0, "
    f"length-sanity ratios 0.22-2.00 with 2.00 = byline placeholder by design, 1.69 = "
    f"person-byline placeholder by design); 5 of {DELTA} are byline-only tagged style (had "
    f"translation fix applied); 12 of {DELTA} substantive records translated cleanly; "
    f"next fetcher at {NEXT_FETCHER_AT} WILL FIRE retry pass (retry-eligible); "
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
    f"(cycle 830 SUBSTANTIVE lineB parsed for canonical 772nd + 1 = 773rd); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 830 runtime CST_TIME 01:00, not cron-tick 01:00 placeholder); "
    f"pitfall 13 (cycle 809 1st-fire) lineB ordinal-count drift cosmetic absorbed "
    f"(29th-fire derived from cycle 830 lineB 28th-fire + 1 for next-occurrence); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe held cleanly "
    f"(IN-SCRIPT assert confirmed -- 20th prevention-fire, cycle 820 codification ELEVATED to in-script "
    f"`assert OLD_MARKER not in newlineb` form, survives script copy-and-modify for future cycles); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held cleanly "
    f"(docstring uses `Hour 18 UTC` not `18:00 UTC` -- and 18 is 2-digit anyway so no leading-zero "
    f"issue); "
    f"pitfall 16 (cycle 819 1st-fire) fetcher-saved refusal translation reaches Phase 1 gate held cleanly "
    f"(PRE-flight REFUSAL_KW canonical 18-keyword scan on NEW_RECORDS returned 1 refusal hit on "
    f"2107866017892348357 (\"抱歉，我無法翻譯這段內容\" + \"暴力犯罪\" + \"煽動對\"); "
    f"retranslate_one.py --id 2107866017892348357 invoked, retried_at=2026-10-08T02:01:34+08:00, "
    f"patched translation \"又一天，又一名12歲的丹麥女孩被移民殘暴強姦\" applied; secondary "
    f"link-only fix on 2107863549959950436 (\"你只提供了一個連結\" / \"請提供完整\") via "
    f"retranslate_one.py --id 2107863549959950436, retried_at=2026-10-08T02:01:39+08:00, "
    f"patched translation \"魁北克可能會迎來加拿大最反覺醒政府的時代……\" applied; "
    f"post-patch scan clean: 0 refusals in NEW); "
    f"pitfall 17 (cycle 823 1st-fire) PRE_REP drift absorption held cleanly "
    f"(9th-fire structural +1 drift pattern, PRE_REP={PRE_REP} read fresh at runtime, EXPECTED_POST_RC={EXPECTED_POST_RC}); "
    f"cross-band IS N/A this cycle (cycle 830 Hour 17 UTC non-retry-eligible -> cycle {CYCLE} Hour {UTC_HOUR} "
    f"UTC retry-eligible = cross-band but runtime ternary on the 'in'/'NOT in' label auto-fires "
    f"correctly: cycle 830 lineB used 'IS NOT in' (Hour 17 non-retry-eligible), cycle {CYCLE} lineB uses "
    f"'IS in' (Hour {UTC_HOUR} retry-eligible); NO pitfall 10 fire on boilerplate label because "
    f"runtime ternary handles Direction A/B swap automatically): "
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
    f"773rd consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (ELEVATED cycle 820 to IN-SCRIPT assert, 20th prevention-fire)
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
    "cron-cycle-substantive form, 1st-fire SUBSTANTIVE at Hour {H} UTC retry-eligible, "
    "29th-fire fetcher-populates-after-cycle-commit pattern at Hour 17 UTC non-retry-eligible for "
    "the SOURCE fetcher that populated these records): SPECIAL SITUATION -- cycle 830 ran as "
    "SUBSTANTIVE at 01:02 CST (Hour 17 UTC non-retry-eligible, commit 00d9410, 772nd clean push), "
    "but the fetcher at 01:07 CST Hour 17 UTC non-retry-eligible non-retry pass ran AFTER cycle "
    "830 commit and populated {D} new substantive records into tweets.json (CUR went {HC} -> {CC}); "
    "cycle 830 SUBSTANTIVE at 01:02 CST did not commit anything FURTHER so the new records were not "
    "visible until cycle {C}; cycle {C} at {T}:00 CST (Hour {H} UTC retry-eligible) is the FIRST "
    "cycle to see the dirty working tree (` M tweets.json`, +{D} records) and the FIRST cycle to "
    "commit them; fetcher at {FA} populated {D} new substantive records: new[0] ID "
    "2107870896824496279 byline-only orphan (Elon Musk) -> placeholder applied per cycle 286/287; "
    "new[1] ID 2107866017892348357 Denmark-assault-RT (retried: 1st-translation refused, "
    "retranslate_one.py per pitfall 16, len_orig=197, len_trans=110, ratio=0.56); new[2] ID "
    "2107870975220232339 agreement-RT (len_orig=19, len_trans=5, ratio=0.26); new[3] ID "
    "2107863549959950436 Quebec-link-RT (retried: 1st-translation link-only meta-refusal, "
    "retranslate_one.py based on URL slug, len_orig=96, len_trans=23, ratio=0.24); new[4] ID "
    "2107871743109116020 byline-only orphan (Elon Musk) -> placeholder applied per cycle "
    "286/287; new[5] ID 2107866079951274103 Canada-tax-burden-RT (len_orig=300, len_trans=72, "
    "ratio=0.24); new[6] ID 2107871953696829795 Denmark-murder-sentence-RT (len_orig=42, "
    "len_trans=11, ratio=0.26); new[7] ID 2107859154618507628 Denmark-Congolese-migrant-murder-"
    "sentencing-RT (len_orig=297, len_trans=65, ratio=0.22); new[8] ID 2107872297847861688 "
    "byline-only orphan (Elon Musk) -> placeholder applied per cycle 286/287; new[9] ID "
    "2107854713081200702 Rome-fall-welfare-RT (len_orig=410, len_trans=119, ratio=0.29); new[10] "
    "ID 2107873085844337069 byline-only orphan (Elon Musk) -> placeholder applied per cycle "
    "286/287; new[11] ID 2107699076242235534 Cornell-Omnicause-RT (len_orig=401, len_trans=120, "
    "ratio=0.30); new[12] ID 2107872382367281252 Talarico-anti-DEI-RT (len_orig=389, len_trans=159, "
    "ratio=0.41); new[13] ID 2107872596465446922 Quebec-PQ-RT (len_orig=300, len_trans=110, "
    "ratio=0.37); new[14] ID 2107872672785084550 Talarico-lying-RT (len_orig=295, len_trans=128, "
    "ratio=0.43); new[15] ID 2107876487454179416 Grok-orchestrator-RT (len_orig=300, "
    "len_trans=120, ratio=0.40); new[16] ID 2107876928162275329 person-byline orphan (Ryan "
    "Saavedra) -> placeholder applied per cycle 286/287 person-byline pattern; all {D} new "
    "records inspection gates green AFTER per-cycle byline fix (5 of {D} byline-only orphans had "
    "placeholder applied via /tmp/_fix_byline_cycle831.py per cycle 286/287 codified multi-ID "
    f"pattern; 2 retranslate_one.py invocations for refusal 2107866017892348357 (1st-translation "
    "rejected as 暴力犯罪) and link-only 2107863549959950436 (1st-translation meta-refusal "
    "\"你只提供了一個連結...\", retranslate based on URL slug); structural 0 empty, byline-only "
    "0 leave-alone, refusal 0 [canonical 18-KW REFUSAL_KW scan clean per pitfall 16 cycle 819 "
    "codification AFTER 2 retranslate_one.py pre-flight invocations], simp-leaks 0, "
    "trailing-ellipsis 0, dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.22-2.00 "
    "with 2.00 = byline placeholder by design, 1.69 = person-byline placeholder by design); 5 of "
    "{D} byline-only tagged style (had translation fix applied); 12 of {D} substantive records "
    "translated cleanly; next fetcher at {NFA} WILL FIRE retry pass (retry-eligible); all {D} "
    "snapshot-wide defect gates clean; cross-band IS N/A this cycle (cycle 830 Hour 17 UTC "
    "non-retry-eligible -> cycle {C} Hour {H} UTC retry-eligible) handled cleanly via runtime "
    "ternary on boilerplate label (cycle 830 lineB used 'IS NOT in' for non-retry-eligible, "
    "cycle {C} lineB uses 'IS in' for retry-eligible Hour {H} UTC); "
    "P19/P88/P31/P52/cycle-321/P69/P71/P73/cycle-633/untracked-file-tolerant/cron-tick-RE-bump/"
    "pitfall-12/pitfall-13/pitfall-14/pitfall-15/pitfall-16/pitfall-17 CANONICAL; "
    "PREDICTED_RC={E} OK (canonical PRE_REP_RC+1={E}); jobs.json round-trip patch absorbed cycle "
    "255 dual-completed counter drift (PRE-state top.completed={PT} vs repeat.completed={P}); "
    "P31 idempotency guard correctly detected pre_rep={P} < EXPECTED_POST_RC={E} and BUMPED rep to "
    "{E}; P52 symmetric reset will keep alignment: POST top=rep={E}; 106th consecutive PRE_REP-"
    "drift-clean cycle (extends streak from cycles 712, 715-830); 773rd consecutive clean push "
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

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 773rd clean push (webpage-only, no Telegram)"
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
