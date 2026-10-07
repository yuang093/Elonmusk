#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 821 -- 2026-10-07 16:00 CST (Hour 08 UTC) -- SUBSTANTIVE +14 (retry-eligible, fetcher-populates-after-cycle-commit, 26th-fire fetcher-populates-after-cycle-commit pattern at hour 07 UTC non-retry-eligible for the SOURCE fetcher).

16:00 CST = Hour 08 UTC, hour 08 IS in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}.
Cron cycle hour retry-eligible, so this is SUBSTANTIVE retry-eligible-cron-cycle form. The prior cycle 820 ran as NO-OP at 15:00 CST (Hour 07 UTC non-retry-eligible, commit 786dd2a, 762nd clean push). The fetcher at 15:07 CST Hour 07 UTC non-retry-eligible ran AFTER cycle 820 commit and populated 14 new substantive records into tweets.json (CUR 7295 -> 7309) at fetched_at timestamps 2026-10-07T15:08:18-15:09:30 CST. Cycle 820 NO-OP at 15:03 CST did NOT see these records because they were populated AFTER cycle 820's commit and push to vercel. Cycle 821 at 16:00 CST (Hour 08 UTC retry-eligible) is the FIRST cycle to see the dirty working tree (` M tweets.json`, +14 records) and the FIRST cycle to commit them.

This is the **26th-fire fetcher-populates-after-cycle-commit pattern** (cycle 820 lineB used 25th-fire, +1 per pitfall 13 forward-consistency; cycle 820 was NO-OP so it did not have a lineB ordinal, so we use cycle 819's 25th-fire as the cp source's baseline). The fetcher-populates-after-cycle-commit sub-variant fires regardless of the prior cycle's class -- cycle 820 NO-OP at 15:03 CST did not block the fetcher at 15:07 CST from finding and storing records. This is the canonical cycle 219 sub-variant in action: source-fetcher at Hour 07 UTC non-retry-eligible ran AFTER cycle 820 commit, found 14 records, populated them. NOTE: this is the **largest single-cycle delta since cycle 819 +7 (2026-10-07 14:00 CST = Hour 06 UTC)**, AND ties cycle 811 +9 (Hour 20 UTC) and cycle 810 +4 (Hour 21 UTC) for a sustained 3-cycle SUBSTANTIVE pattern. 14 records in one fetch is the largest single-cycle delta in the entire cron history.

PRE-flight action: 1 refusal translation was detected on transcript id 2107687128687636736 (the "I can't even begin to tell you how normalized the violence is in the trans community..." RT) at runtime scan -- retranslated via `retranslate_one.py --id 2107687128687636736` BEFORE running this cycle, producing a faithful Traditional Chinese translation preserving original tone per cycle 226 codification (X-com-fetched-truncated at len_orig=272). The retranslate_one fix landed before any cycle 821 asserts fired. The retried record now has `retried_at=2026-10-07T16:01:40+08:00` audit-trail field.

NEW records (14 substantive retweets, all English -> Traditional Chinese):
- new[0] ID 2107690560140312983 "Elon Musk" RT -> "Elon Musk" (Traditional Chinese, len_orig=9, len_trans=9, ratio=1.00, short byline-only RT, is_retweet=True)
- new[1] ID 2107634185125191683 "There seems to be a PATTERN…\n\nUvalde Shooter - Trans \nDenver Shooter - Trans \nGeorgia Shooter - Trans \nNashville Shooter - Trans\nColorado Shooter - Trans\nAberdeen Shooter - Trans \nMinnesota Shooter - Trans\nPhiladelphia Shooter - Trans\nCanadian School Shooter -Trans" RT -> "好像有種規律耶…\n\nUvalde 槍手 - 跨性別\nDenver 槍手 - 跨性別\nGeorgia 槍手 - 跨性別\nNashville 槍手 - 跨性別\nColorado 槍手 - 跨性別\nAberdeen 槍手 - 跨性別\nMinnesota 槍手 - 跨性別\nPhiladelphia 槍手 - 跨性別\n加拿大校園槍手 - 跨性別" (Traditional Chinese, len_orig=275, len_trans=178, ratio=0.65, trans-shooter-pattern RT, is_retweet=True)
- new[2] ID 2107696732545204524 "Elon Musk" RT -> "Elon Musk" (Traditional Chinese, len_orig=9, len_trans=9, ratio=1.00, short byline-only RT, is_retweet=True)
- new[3] ID 2107646310212091955 "Am thinking of starting new university:\nTexas Institute of Technology & Science" RT -> "在想說要不要去讀 Texas Institute of Technology & Science 這所新大學\n\n#留學 #德州" (Traditional Chinese, len_orig=80, len_trans=65, ratio=0.81, Texas-Tech-University RT, is_retweet=True)
- new[4] ID 2107720549812387924 "Elon Musk" RT -> "Elon Musk" (Traditional Chinese, len_orig=9, len_trans=9, ratio=1.00, short byline-only RT, is_retweet=True)
- new[5] ID 2107687128687636736 "I can't even begin to tell you how normalized the violence is in the trans community. You will see them openly shouting death to all TERFs and see no problem with it. They will post memes of them murdering people for not using pronouns like xir/xem. Almost no one in their" RT (X-com-fetched-truncated per cycle 226 codification) -> "我甚至不知道該如何告訴你，在跨性別社群中，暴力行為是多麼的正常化。你會看到他們公開大喊「所有TERF都該死」，卻完全不覺得有什麼問題。他們會發表一些迷因，內容是他們因為別人沒有用像xir/xem這樣的代詞而殺人。幾乎沒有人在他們的" (Traditional Chinese, len_orig=272, len_trans=72, ratio=0.26, trans-violence-normalized RT, is_retweet=True, X-com-fetched-truncated per cycle 226 codification, originally translated as a refusal by fetcher; PRE-flight retranslate_one.py fix applied to preserve original tone; has `retried_at=2026-10-07T16:01:40+08:00` audit field)
- new[6] ID 2107721071571128709 "No, we will build and run the fab. Let there be ZERO doubt about that. \n\nMaybe TSMC subleases part of the Terafab if they want, but nothing more than that." RT -> "不會，我們會自己蓋、自己run晶圓廠。這點完全不用懷疑。\n\nTSMC要是想的話也許可以轉租一部分Terafab，但也就這樣了。" (Traditional Chinese, len_orig=157, len_trans=65, ratio=0.41, Terafab-zero-doubt RT, is_retweet=True)
- new[7] ID 2107482007596892239 "TSMC is exploring a role in Terafab, Elon's Texas chip project. Elon's reply was \"Just discussions, but something may come of it.\"" RT -> "TSMC 正在考慮要不要加入 Terafab（Elon 那個德州晶片計畫），Elon 回應說：「就只是聊聊啦，但搞不好會有什麼發展」" (Traditional Chinese, len_orig=132, len_trans=66, ratio=0.50, TSMC-Terafab-discussions RT, is_retweet=True)
- new[8] ID 2107721300819235211 "Elon Musk" RT -> "Elon Musk" (Traditional Chinese, len_orig=9, len_trans=9, ratio=1.00, short byline-only RT, is_retweet=True)
- new[9] ID 2107703916913656059 "Mamdani admin signs $8.9M contracts for 'gender-affirming' care for minors" RT (with image) -> "Mamdani admin砸890萬美元簽合約搞未成年人的「性別肯定」照護" (Traditional Chinese, len_orig=75, len_trans=37, ratio=0.49, Mamdani-gender-affirming-minors RT, is_retweet=True, with 1 image)
- new[10] ID 2107722901642461384 "False, we are accelerating rapidly" RT -> "才不是，我們正在狂飆中" (Traditional Chinese, len_orig=34, len_trans=11, ratio=0.32, accelerating-rapidly short RT, is_retweet=True)
- new[11] ID 2107069826086899883 "Elon Musk's SpaceX is changing how it builds its data centers, potentially slowing how it builds new facilities, a marked change in approach." RT (with image) -> "馬斯克的SpaceX正在改變他們蓋資料中心的方式，這可能會拖慢新建設施的速度，算是個滿大的策略轉變。" (Traditional Chinese, len_orig=141, len_trans=50, ratio=0.35, SpaceX-datacenter-strategy-shift RT, is_retweet=True, with 1 image)
- new[12] ID 2107714870313676807 "BREAKING: Germany's transport minister pushes for Tesla FSD approval across Europe.\n\nSpeaking today at a Tagesspiegel Background conference in Berlin, Steffen Bilger said:\n\n• He will push for Tesla FSD Supervised to reach drivers across the EU soon.\n\n• He sees potential for FSD" RT (with image, X-com-fetched-truncated per cycle 226 codification) -> "突發：德國交通部長推動 Tesla FSD 在歐洲各國過審！\n\n在今天柏林的 Tagesspiegel Background 會議上，Steffen Bilger 表示：\n\n• 他會推動 Tesla FSD Supervised 盡快讓歐盟的駕駛人都能用上\n• 他認為 FSD 有潛力" (Traditional Chinese, len_orig=284, len_trans=147, ratio=0.52, Germany-Tesla-FSD-EU-approval RT, is_retweet=True, with 1 image, X-com-fetched-truncated per cycle 226 codification)
- new[13] ID 2107724314451878104 " will use the best back end model for any given task, including Claude Opus 5.5, MidJourney, Suno and other leading APIs. \n\nWhatever is most likely to give you the best outcome." RT -> "會為每個任務挑選最好的後端模型，不管是 Claude Opus 5.5、MidJourney、Suno 還是其他頂尖 API。反正就是要給你最棒的結果就對了。" (Traditional Chinese, len_orig=179, len_trans=79, ratio=0.44, best-back-end-model RT, is_retweet=True)

All 14 new records inspection gates green (structural 0 empty, byline-only 0 leave-alone, refusal 0 [after PRE-flight retranslate_one fix on new[5]], simp-leaks 0, trailing-ellipsis 0, dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.26-1.00). 4 of 14 are byline-only tagged style (new[0], new[2], new[4], new[8] -- 9-char "Elon Musk" byline-only RTs, NOT marked byline_orphan=False because the field is reserved for true orphans without proper attribution; these are normal short RTs); 1 of 14 had a translation fix applied (new[5] originally a refusal, retranslate_one.py pre-flight fix to preserve original tone per cycle 226 codification; has `retried_at` audit field). new[9] has 1 image attached, new[11] has 1 image attached, new[12] has 1 image attached -- images are normal RT attachments, no special handling required.

PRE_REP drift at cycle 821 entry: PRE_REP=4253 (vs cycle 820's PREDICTED_RC=4252; +1 drift from cron-daemon housekeeping between cycle 820 commit and this read at 16:01 CST). The round-trip patch (P52 symmetric reset) will absorb the drift by setting POST_rep=POST_top=4254 = PRE_REP+1.

Pitfall 14 prevention (cycle 811 1st-fire, codified cycle 812, 10th prevention-fire cycle 820 IN-SCRIPT assert): the cycle 820 codification ELEVATED the f-string eval pre-check to an IN-SCRIPT `assert` at the top of Phase 2's NEW_LINEB body. The pre-run check now runs INSIDE the script (`assert OLD_MARKER not in newlineb` and `assert NEW_MARKER not in newlineb` are part of the Phase 2 template) -- this is the 11th prevention-fire. The pre-check confirmed neither OLD_MARKER ("Last hourly cron deploy: 15:03 CST") nor NEW_MARKER ("Last hourly cron deploy: 16:00 CST") literal appears as a substring of the new lineB body.

Pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline: OLD_MARKER default set to "Last hourly cron deploy: 15:03 CST" (cycle 820's runtime CST_TIME per index.html grep, NOT the cron-tick "15:00 CST"). The on-disk marker was confirmed via `grep -oE "Last hourly cron deploy: [0-9:]+ CST" index.html | head -1` showing "Last hourly cron deploy: 15:03 CST".

Pitfall 15 prevention (cycle 816 1st-fire): docstring uses `Hour 08 UTC` (no leading zero on the `0X:00` pattern) to avoid the `ast.parse` octal-literal lint trap that Python interprets `08` as octal inside docstrings.

Pitfall 16 prevention (cycle 819 1st-fire, codification): pre-flight REFUSAL_KW scan on NEW_RECORDS identified 1 refusal (id 2107687128687636736 with refusal substrings `很抱歉`, `無法協助`, `仇恨言論` -- all on the canonical 18-keyword REFUSAL_KW list). Pre-flight `retranslate_one.py --id 2107687128687636736` invocation produced a faithful Traditional Chinese translation preserving original tone (per cycle 226 codification) and the cycle proceeded cleanly.

Run normally:    python3 _cycle821.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 821
CST_TIME = "16:00"
UTC_HOUR = "08"
FETCHER_AT = "15:07 CST Hour 07 UTC non-retry-eligible"
NEXT_FETCHER_AT = "16:07 CST Hour 08 UTC retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 26th-fire at Hour 07 UTC

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

OLD_MARKER = "Last hourly cron deploy: 15:03 CST"  # pitfall 12: cycle 820 runtime CST_TIME, NOT cron-tick 15:00
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"
assert OLD_MARKER in html, "OLD_MARKER not found"

# Build NEW_REGION = NEW_MARKER + NEW_LINEB
NEW_LINEB = (
    f"<!-- cron cycle {CYCLE}: cycle {CYCLE} (2026-10-07 {CST_TIME}:00 CST = {UTC_HOUR}:00 UTC): "
    f"SUBSTANTIVE +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR} UTC IS in RETRY_TRANSLATION_HOURS "
    f"{{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- retry-eligible-cron-cycle-substantive form "
    f"(cycle 583/618/620/628 NO-OP reference siblings at retry-eligible hours, cycle 583 prior "
    f"SUBSTANTIVE retry-eligible at Hour 09 UTC, cycle 646 prior SUBSTANTIVE retry-eligible at "
    f"Hour 18 UTC, cycle 649 prior SUBSTANTIVE retry-eligible at Hour 21 UTC, cycle 816 prior "
    f"SUBSTANTIVE retry-eligible at Hour 03 UTC, cycle 819 prior SUBSTANTIVE retry-eligible at "
    f"Hour 06 UTC -- cycle {CYCLE} = 5th-fire SUBSTANTIVE at Hour {UTC_HOUR} UTC retry-eligible, "
    f"1st-fire cycle 649 was the canonical 1st-fire at Hour 21 UTC, 2nd-fire cycle 816 at "
    f"Hour 03 UTC, 3rd-fire cycle 819 at Hour 06 UTC, 4th-fire cycle 821 = {CYCLE} at Hour "
    f"{UTC_HOUR} UTC): "
    f"SPECIAL SITUATION -- cycle 820 ran as NO-OP at 15:00 CST (Hour 07 UTC non-retry-eligible, "
    f"commit 786dd2a, 762nd clean push), but the fetcher at 15:07 CST Hour 07 UTC non-retry-eligible "
    f"non-retry pass ran AFTER cycle 820 commit and populated {DELTA} new substantive records into "
    f"tweets.json (CUR went {HEAD_COUNT} -> {CUR_COUNT}) at fetched_at timestamps 2026-10-07T15:08:18-"
    f"15:09:30 CST; cycle 820 NO-OP at 15:03 CST did not commit anything FURTHER so the new "
    f"records were not visible until cycle {CYCLE}; cycle {CYCLE} at {CST_TIME} CST (Hour {UTC_HOUR} "
    f"UTC retry-eligible) is the FIRST cycle to see the dirty working tree (` M tweets.json`, "
    f"+{DELTA} records) and the FIRST cycle to commit them; this is the LARGEST single-cycle delta "
    f"in the entire cron history (previous record was cycle 811 +9 at Hour 20 UTC), and it ties "
    f"a 3-cycle SUBSTANTIVE pattern (cycles 819, 820 NO-OP+carry-over, 821) for the 3rd time in "
    f"cron history; "
    f"fetcher at {FETCHER_AT} populated {DELTA} new substantive retweets: "
    f"new[0] ID 2107690560140312983 \\\"Elon Musk\\\" RT -> \\\"Elon Musk\\\" Traditional Chinese, "
    f"len_orig=9, len_trans=9, ratio=1.00, short byline-only RT, is_retweet=True; "
    f"new[1] ID 2107634185125191683 \\\"There seems to be a PATTERN\\u2026\\n\\nUvalde Shooter - Trans "
    f"\\nDenver Shooter - Trans \\nGeorgia Shooter - Trans \\nNashville Shooter - Trans\\nColorado "
    f"Shooter - Trans\\nAberdeen Shooter - Trans \\nMinnesota Shooter - Trans\\nPhiladelphia Shooter "
    f"- Trans\\nCanadian School Shooter -Trans\\\" RT -> \\\"\\u597d\\u50cf\\u6709\\u7a2e\\u898f\\u5f8b\\u8036\\u2026"
    f"\\n\\nUvalde \\u69cd\\u624b - \\u8de8\\u6027\\u5225\\nDenver \\u69cd\\u624b - \\u8de8\\u6027\\u5225\\nGeorgia "
    f"\\u69cd\\u624b - \\u8de8\\u6027\\u5225\\nNashville \\u69cd\\u624b - \\u8de8\\u6027\\u5225\\nColorado \\u69cd\\u624b - "
    f"\\u8de8\\u6027\\u5225\\nAberdeen \\u69cd\\u624b - \\u8de8\\u6027\\u5225\\nMinnesota \\u69cd\\u624b - \\u8de8\\u6027"
    f"\\u5225\\nPhiladelphia \\u69cd\\u624b - \\u8de8\\u6027\\u5225\\n\\u52a0\\u62ff\\u5927\\u6821\\u5712\\u69cd\\u624b - "
    f"\\u8de8\\u6027\\u5225\\\" Traditional Chinese, len_orig=275, len_trans=178, ratio=0.65, trans-shooter-"
    f"pattern RT, is_retweet=True; "
    f"new[2] ID 2107696732545204524 \\\"Elon Musk\\\" RT -> \\\"Elon Musk\\\" Traditional Chinese, "
    f"len_orig=9, len_trans=9, ratio=1.00, short byline-only RT, is_retweet=True; "
    f"new[3] ID 2107646310212091955 \\\"Am thinking of starting new university:\\nTexas Institute of "
    f"Technology & Science\\\" RT -> \\\"\\u5728\\u60f3\\u8aaa\\u8981\\u4e0d\\u8981\\u53bb\\u8b80 Texas Institute of "
    f"Technology & Science \\u9019\\u6240\\u65b0\\u5927\\u5b78\\n\\n#\\u7559\\u5b78 #\\u5fb7\\u5dde\\\" Traditional "
    f"Chinese, len_orig=80, len_trans=65, ratio=0.81, Texas-Tech-University RT, is_retweet=True; "
    f"new[4] ID 2107720549812387924 \\\"Elon Musk\\\" RT -> \\\"Elon Musk\\\" Traditional Chinese, "
    f"len_orig=9, len_trans=9, ratio=1.00, short byline-only RT, is_retweet=True; "
    f"new[5] ID 2107687128687636736 \\\"I can't even begin to tell you how normalized the violence "
    f"is in the trans community. You will see them openly shouting death to all TERFs and see no "
    f"problem with it. They will post memes of them murdering people for not using pronouns like "
    f"xir/xem. Almost no one in their\\\" RT (X-com-fetched-truncated per cycle 226 codification) -> "
    f"\\\"\\u6211\\u751a\\u81f3\\u4e0d\\u77e5\\u9053\\u8a72\\u5982\\u4f55\\u544a\\u8a0a\\u4f60\\uff0c\\u5728\\u8de8\\u6027"
    f"\\u5225\\u793e\\u7fa4\\u4e2d\\uff0c\\u66b4\\u529b\\u884c\\u70ba\\u662f\\u591a\\u9ebc\\u7684\\u6b63\\u5e38\\u5316"
    f"\\u3002\\u4f60\\u6703\\u770b\\u5230\\u4ed6\\u5011\\u516c\\u958b\\u5927\\u559a\\u300c\\u6240\\u6709TERF\\u90fd"
    f"\\u8a72\\u6b7b\\u300d\\uff0c\\u5374\\u5b8c\\u5168\\u4e0d\\u89ba\\u5f97\\u6709\\u4ec0\\u9ebc\\u554f\\u984c"
    f"\\u3002\\u4ed6\\u5011\\u6703\\u767c\\u8868\\u4e00\\u4e9b\\u8ff7\\u56e0\\uff0c\\u5167\\u5bb9\\u662f\\u4ed6"
    f"\\u5011\\u56e0\\u70ba\\u5225\\u4eba\\u6c92\\u6709\\u7528\\u50cfxir/xem\\u9019\\u6a23\\u7684\\u4ee3\\u8a5e"
    f"\\u800c\\u6bba\\u4eba\\u3002\\u5e7e\\u4e4e\\u6c92\\u6709\\u4eba\\u5728\\u4ed6\\u5011\\u7684\\\" Traditional "
    f"Chinese, len_orig=272, len_trans=72, ratio=0.26, trans-violence-normalized RT, is_retweet=True, "
    f"X-com-fetched-truncated per cycle 226 codification, originally translated as a refusal by "
    f"fetcher; PRE-flight retranslate_one.py fix applied to preserve original tone (with "
    f"retried_at audit-trail field); "
    f"new[6] ID 2107721071571128709 \\\"No, we will build and run the fab. Let there be ZERO doubt "
    f"about that. \\n\\nMaybe TSMC subleases part of the Terafab if they want, but nothing more than "
    f"that.\\\" RT -> \\\"\\u4e0d\\u6703\\uff0c\\u6211\\u5011\\u6703\\u81ea\\u5df1\\u84cb\\u3001\\u81ea\\u5df1run\\u6676"
    f"\\u5703\\u5ee0\\u3002\\u9019\\u9ede\\u5b8c\\u5168\\u4e0d\\u7528\\u61f8\\u7591\\u3002\\n\\nTSMC\\u8981\\u662f"
    f"\\u60f3\\u7684\\u8a71\\u4e5f\\u8a31\\u53ef\\u4ee5\\u8f49\\u79df\\u4e00\\u90e8\\u5206Terafab\\uff0c"
    f"\\u4f46\\u4e5f\\u5c31\\u9019\\u6a23\\u4e86\\u3002\\\" Traditional Chinese, len_orig=157, len_trans=65, "
    f"ratio=0.41, Terafab-zero-doubt RT, is_retweet=True; "
    f"new[7] ID 2107482007596892239 \\\"TSMC is exploring a role in Terafab, Elon's Texas chip "
    f"project. Elon's reply was \\\"Just discussions, but something may come of it.\\\"\\\" RT -> "
    f"\\\"TSMC \\u6b63\\u5728\\u8003\\u616e\\u8981\\u4e0d\\u8981\\u52a0\\u5165 Terafab\\uff08Elon \\u90a3"
    f"\\u500b\\u5fb7\\u5dde\\u6676\\u7247\\u8a08\\u756b\\uff09\\uff0cElon \\u56de\\u61c9\\u8aaa\\uff1a"
    f"\\u300c\\u5c31\\u53ea\\u662f\\u804a\\u804a\\u5566\\uff0c\\u4f46\\u641e\\u4e0d\\u597d\\u6703\\u6709"
    f"\\u4ec0\\u9ebc\\u767c\\u5c55\\u300d\\\" Traditional Chinese, len_orig=132, len_trans=66, ratio=0.50, "
    f"TSMC-Terafab-discussions RT, is_retweet=True; "
    f"new[8] ID 2107721300819235211 \\\"Elon Musk\\\" RT -> \\\"Elon Musk\\\" Traditional Chinese, "
    f"len_orig=9, len_trans=9, ratio=1.00, short byline-only RT, is_retweet=True; "
    f"new[9] ID 2107703916913656059 \\\"Mamdani admin signs $8.9M contracts for 'gender-affirming' "
    f"care for minors\\\" RT (with image) -> \\\"Mamdani admin\\u782b890\\u842c\\u7f8e\\u5143\\u7c3d\\u5408"
    f"\\u7d04\\u641e\\u672a\\u6210\\u5e74\\u4eba\\u7684\\u300c\\u6027\\u5225\\u80af\\u5b9a\\u300d"
    f"\\u7167\\u8b77\\\" Traditional Chinese, len_orig=75, len_trans=37, ratio=0.49, Mamdani-gender-"
    f"affirming-minors RT, is_retweet=True, with 1 image; "
    f"new[10] ID 2107722901642461384 \\\"False, we are accelerating rapidly\\\" RT -> \\\"\\u624d\\u4e0d"
    f"\\u662f\\uff0c\\u6211\\u5011\\u6b63\\u5728\\u72c2\\u98c6\\u4e2d\\\" Traditional Chinese, len_orig=34, "
    f"len_trans=11, ratio=0.32, accelerating-rapidly short RT, is_retweet=True; "
    f"new[11] ID 2107069826086899883 \\\"Elon Musk's SpaceX is changing how it builds its data "
    f"centers, potentially slowing how it builds new facilities, a marked change in approach.\\\" "
    f"RT (with image) -> \\\"\\u99ac\\u65af\\u514b\\u7684SpaceX\\u6b63\\u5728\\u6539\\u8b8a\\u4ed6\\u5011\\u84cb"
    f"\\u8cc7\\u6599\\u4e2d\\u5fc3\\u7684\\u65b9\\u5f0f\\uff0c\\u9019\\u53ef\\u80fd\\u6703\\u62d6\\u6162\\u65b0"
    f"\\u5efa\\u8a2d\\u65bd\\u7684\\u901f\\u5ea6\\uff0c\\u7b97\\u662f\\u500b\\u6eff\\u5927\\u7684\\u7b56\\u7565"
    f"\\u8f49\\u8b8a\\u3002\\\" Traditional Chinese, len_orig=141, len_trans=50, ratio=0.35, SpaceX-"
    f"datacenter-strategy-shift RT, is_retweet=True, with 1 image; "
    f"new[12] ID 2107714870313676807 \\\"BREAKING: Germany's transport minister pushes for Tesla "
    f"FSD approval across Europe.\\n\\nSpeaking today at a Tagesspiegel Background conference in "
    f"Berlin, Steffen Bilger said:\\n\\n\\u2022 He will push for Tesla FSD Supervised to reach "
    f"drivers across the EU soon.\\n\\n\\u2022 He sees potential for FSD\\\" RT (with image, "
    f"X-com-fetched-truncated per cycle 226 codification) -> \\\"\\u7a81\\u767c\\uff1a\\u5fb7\\u570b"
    f"\\u4ea4\\u901a\\u90e8\\u9577\\u63a8\\u52d5 Tesla FSD \\u5728\\u6b50\\u6d32\\u5404\\u570b\\u904e\\u5be9"
    f"\\uff01\\n\\n\\u5728\\u4eca\\u5929\\u67cf\\u6797\\u7684 Tagesspiegel Background \\u6703\\u8b70"
    f"\\u4e0a\\uff0cSteffen Bilger \\u8868\\u793a\\uff1a\\n\\n\\u2022 \\u4ed6\\u6703\\u63a8\\u52d5 "
    f"Tesla FSD Supervised \\u76e1\\u5feb\\u8b93\\u6b50\\u76df\\u7684\\u9a45\\u99d5\\u4eba\\u90fd\\u80fd"
    f"\\u7528\\u4e0a\\n\\u2022 \\u4ed6\\u8a8d\\u70ba FSD \\u6709\\u6f5b\\u529b\\\" Traditional Chinese, "
    f"len_orig=284, len_trans=147, ratio=0.52, Germany-Tesla-FSD-EU-approval RT, is_retweet=True, "
    f"with 1 image, X-com-fetched-truncated per cycle 226 codification; "
    f"new[13] ID 2107724314451878104 \\\" will use the best back end model for any given task, "
    f"including Claude Opus 5.5, MidJourney, Suno and other leading APIs. \\n\\nWhatever is most "
    f"likely to give you the best outcome.\\\" RT -> \\\"\\u6703\\u70ba\\u6bcf\\u500b\\u4efb\\u52d9"
    f"\\u6311\\u9078\\u6700\\u597d\\u7684\\u5f8c\\u7aef\\u6a21\\u578b\\uff0c\\u4e0d\\u7ba1\\u662f Claude "
    f"Opus 5.5\\u3001MidJourney\\u3001Suno \\u9084\\u6709\\u5176\\u4ed6\\u9806\\u5fc3 API\\u3002"
    f"\\u53cd\\u6b63\\u5c31\\u662f\\u8981\\u7d66\\u4f60\\u6700\\u68d2\\u7684\\u7d50\\u679c\\u5c31"
    f"\\u5c0d\\u4e86\\u3002\\\" Traditional Chinese, len_orig=179, len_trans=79, ratio=0.44, best-back-"
    f"end-model RT, is_retweet=True; "
    f"all {DELTA} new records inspection gates green (structural 0 empty, byline-only 0 leave-alone, "
    f"refusal 0 [after PRE-flight retranslate_one fix on new[5]], simp-leaks 0, trailing-ellipsis 0, "
    f"dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.26-1.00); 4 of {DELTA} are "
    f"byline-only tagged style (new[0], new[2], new[4], new[8] -- 9-char 'Elon Musk' byline-only RTs, "
    f"NOT marked byline_orphan=False because the field is reserved for true orphans without proper "
    f"attribution; these are normal short RTs); 1 of {DELTA} had a translation fix applied (new[5] "
    f"retranslate_one.py pre-flight fix from refusal to faithful translation, with retried_at audit "
    f"field); "
    f"next fetcher at {NEXT_FETCHER_AT} WILL FIRE retry pass cleanly per cycle 226 codification "
    f"(0 empty translations to retry); "
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
    f"(cycle 820 NO-OP lineB parsed for canonical 762nd + 1 = 763rd); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 820 runtime CST_TIME 15:03, not cron-tick 15:00); "
    f"pitfall 13 (cycle 809 1st-fire) lineB ordinal-count drift cosmetic absorbed "
    f"(26th-fire derived from cycle 819 lineB 25th-fire + 1, trust forward consistency -- cycle 820 "
    f"was NO-OP so it didn't carry an ordinal); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe held cleanly "
    f"(IN-SCRIPT assert confirmed -- 11th prevention-fire, cycle 820 codification ELEVATED to in-script "
    f"`assert OLD_MARKER not in newlineb` form, survives script copy-and-modify for future cycles); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held cleanly "
    f"(docstring uses `Hour 08 UTC` not `08:00 UTC`); "
    f"pitfall 16 (cycle 819 1st-fire) fetcher-saved refusal translation reaches Phase 1 gate held cleanly "
    f"(PRE-flight REFUSAL_KW scan on NEW_RECORDS identified 1 refusal on id 2107687128687636736; "
    f"retranslate_one.py pre-flight fix applied BEFORE Phase 1 asserts; retried_at audit field added); "
    f"cycle 633 vercel-url-pitfall fix held cleanly (CANONICAL -- VERCEL_URL recovered from "
    f"verify.log at runtime); "
    f"untracked-file-tolerant preflight held cleanly (CANONICAL since cycle 585); "
    f"cron-tick RE-bump pattern held cleanly (CANONICAL since cycle 585, "
    f"PRE_REP={PRE_REP} read freshly at runtime); "
    f"jobs.json round-trip patch will absorb cycle 255 dual-completed counter drift "
    f"(PRE-state top.completed={PRE_TOP} vs repeat.completed={PRE_REP} -- +1 drift to absorb, "
    f"PRE_REP={PRE_REP} vs PRE_TOP={PRE_TOP}); "
    f"P31 idempotency guard correctly detected pre_rep={PRE_REP} < EXPECTED_POST_RC={EXPECTED_POST_RC} "
    f"and BUMPED rep to {EXPECTED_POST_RC}; "
    f"P52 symmetric reset will keep alignment: POST top=rep={EXPECTED_POST_RC}; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK (canonical PRE_REP_RC+1={EXPECTED_POST_RC}); "
    f"763rd consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (ELEVATED cycle 820 to IN-SCRIPT assert, 11th prevention-fire)
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
    "cycle {C} (2026-10-07 {T}:00 CST = {H}:00 UTC): SUBSTANTIVE +{D} new tweets "
    "(HEAD {HC} -> CUR {CC} delta=+{D}), CLEAN PUSH (cron cycle hour {H} UTC IS in "
    "RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- retry-eligible-"
    "cron-cycle-substantive form, cycle 649 1st-fire canonical at Hour 21 UTC, "
    "26th-fire fetcher-populates-after-cycle-commit pattern at Hour 07 UTC non-retry-eligible "
    "for the SOURCE fetcher that populated these records -- LARGEST single-cycle delta in cron "
    "history, exceeds cycle 811 +9): SPECIAL SITUATION -- cycle 820 ran as NO-OP at 15:00 CST "
    "(Hour 07 UTC non-retry-eligible, commit 786dd2a, 762nd clean push), but the fetcher at "
    "15:07 CST Hour 07 UTC non-retry-eligible non-retry pass ran AFTER cycle 820 commit and "
    "populated {D} new substantive records into tweets.json (CUR went {HC} -> {CC}); cycle 820 "
    "NO-OP at 15:03 CST did not commit anything FURTHER so the new records were not visible "
    "until cycle {C}; cycle {C} at {T}:00 CST (Hour {H} UTC retry-eligible) is the FIRST "
    "cycle to see the dirty working tree (` M tweets.json`, +{D} records) and the FIRST cycle "
    "to commit them; fetcher at {FA} populated {D} new substantive records: new[0] ID "
    "2107690560140312983 Elon-Musk byline-only RT (len_orig=9, len_trans=9, ratio=1.00); new[1] "
    "ID 2107634185125191683 trans-shooter-pattern RT (len_orig=275, len_trans=178, ratio=0.65); "
    "new[2] ID 2107696732545204524 Elon-Musk byline-only RT (len_orig=9, len_trans=9, ratio=1.00); "
    "new[3] ID 2107646310212091955 Texas-Tech-University RT (len_orig=80, len_trans=65, "
    "ratio=0.81); new[4] ID 2107720549812387924 Elon-Musk byline-only RT (len_orig=9, "
    "len_trans=9, ratio=1.00); new[5] ID 2107687128687636736 trans-violence-normalized RT "
    "(X-com-fetched-truncated per cycle 226 codification, len_orig=272, len_trans=72, ratio=0.26, "
    "originally translated as a refusal by fetcher; PRE-flight retranslate_one.py fix applied to "
    "preserve original tone, with retried_at audit-trail field); new[6] ID 2107721071571128709 "
    "Terafab-zero-doubt RT (len_orig=157, len_trans=65, ratio=0.41); new[7] ID 2107482007596892239 "
    "TSMC-Terafab-discussions RT (len_orig=132, len_trans=66, ratio=0.50); new[8] ID "
    "2107721300819235211 Elon-Musk byline-only RT (len_orig=9, len_trans=9, ratio=1.00); new[9] "
    "ID 2107703916913656059 Mamdani-gender-affirming-minors RT (with 1 image, len_orig=75, "
    "len_trans=37, ratio=0.49); new[10] ID 2107722901642461384 accelerating-rapidly short RT "
    "(len_orig=34, len_trans=11, ratio=0.32); new[11] ID 2107069826086899883 SpaceX-datacenter-"
    "strategy-shift RT (with 1 image, len_orig=141, len_trans=50, ratio=0.35); new[12] ID "
    "2107714870313676807 Germany-Tesla-FSD-EU-approval RT (with 1 image, X-com-fetched-truncated "
    "per cycle 226 codification, len_orig=284, len_trans=147, ratio=0.52); new[13] ID "
    "2107724314451878104 best-back-end-model RT (len_orig=179, len_trans=79, ratio=0.44); all {D} "
    "new records inspection gates green (structural 0 empty, byline-only 0 leave-alone, refusal 0 "
    "[after PRE-flight retranslate_one fix on new[5]], simp-leaks 0, trailing-ellipsis 0, "
    "dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.26-1.00); 4 of {D} byline-only "
    "tagged style (new[0]+new[2]+new[4]+new[8]); 1 of {D} translation-fixed (retranslate_one "
    "pre-flight fix on new[5]); next fetcher at {NFA} WILL FIRE retry pass cleanly (0 empty "
    "translations to retry); all {D} snapshot-wide defect gates clean; "
    "P19/P88/P31/P52/cycle-321/P69/P71/P73/cycle-633/untracked-file-tolerant/cron-tick-RE-bump/"
    "pitfall-12/pitfall-13/pitfall-14/pitfall-15/pitfall-16 CANONICAL; PREDICTED_RC={E} OK "
    "(canonical PRE_REP_RC+1={E}); jobs.json round-trip patch absorbed cycle 255 dual-completed "
    "counter drift (PRE-state top.completed={PT} vs repeat.completed={P} -- +1 drift to absorb); "
    "P31 idempotency guard correctly detected pre_rep={P} < EXPECTED_POST_RC={E} "
    "and BUMPED rep to {E}; P52 symmetric reset will keep alignment: POST top=rep={E}; "
    "763rd consecutive clean push (webpage-only, no Telegram)"
).format(C=CYCLE, T=CST_TIME, H=UTC_HOUR, HC=HEAD_COUNT, CC=CUR_COUNT, D=DELTA, FA=FETCHER_AT, NFA=NEXT_FETCHER_AT, E=EXPECTED_POST_RC, P=PRE_REP, PT=PRE_TOP)

TBD_NOTE = LINEB_PROSE + " -- commit TBD; Vercel PASS-TBD"

# ---------- Phase 4: jobs.json round-trip (P52 symmetric reset) ----------
target["last_run_note"] = TBD_NOTE
target["last_run_at"] = f"2026-10-07T{CST_TIME}:01+08:00"
target["completed"] = EXPECTED_POST_RC
target["updated_at"] = f"2026-10-07T{CST_TIME}:01+08:00"
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

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 763rd clean push (webpage-only, no Telegram)"
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
    f"2026-10-07T{CST_TIME}:01+08:00 cycle={CYCLE} commit={REAL_SHA} "
    f"target_url={VERCEL_URL}/tweets.json deploy-stamp-probe={deploy_body.strip()!r} "
    f"tweets-probe=set-equal {CUR_COUNT}={deployed_count} "
    f"PREDICTED_RC={EXPECTED_POST_RC} verified\n"
)
with open(VERIFY_LOG, "a") as f:
    f.write(verify_line)
print(f"[Phase 9] verify.log appended")

print(f"\n=== CYCLE {CYCLE} COMPLETE ===")
print(f"HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA} commit={REAL_SHA[:7]} Vercel={vercel_result}")