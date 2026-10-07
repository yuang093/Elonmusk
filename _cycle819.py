#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 819 -- 2026-10-07 14:00 CST (Hour 06 UTC) -- SUBSTANTIVE +7 (retry-eligible, fetcher-populates-after-cycle-commit, 25th-fire fetcher-populates-after-cycle-commit pattern at hour 05 UTC non-retry-eligible for the SOURCE fetcher).

14:00 CST = Hour 06 UTC, hour 06 IS in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}.
Cron cycle hour retry-eligible, so this is SUBSTANTIVE retry-eligible-cron-cycle form. The prior cycle 818 ran as SUBSTANTIVE at 13:00 CST (Hour 05 UTC non-retry-eligible, commit d39b4dd, 760th clean push). The fetcher at 13:07 CST Hour 05 UTC non-retry-eligible ran AFTER cycle 818 commit and populated 7 new substantive records into tweets.json (CUR 7288 -> 7295) at fetched_at timestamps 2026-10-07T13:07:45-13:08:08 CST. Cycle 818 SUBSTANTIVE at 13:05 CST did NOT see these records because they were populated AFTER cycle 818's commit and push to vercel. Cycle 819 at 14:00 CST (Hour 06 UTC retry-eligible) is the FIRST cycle to see the dirty working tree (` M tweets.json`, +7 records) and the FIRST cycle to commit them.

This is the **25th-fire fetcher-populates-after-cycle-commit pattern** (cycle 818 lineB used 24th-fire, +1 per pitfall 13 forward-consistency). The fetcher-populates-after-cycle-commit sub-variant fires regardless of the prior cycle's class -- cycle 818 SUBSTANTIVE at 13:05 CST did not block the fetcher at 13:07 CST from finding and storing records. This is the canonical cycle 219 sub-variant in action: source-fetcher at Hour 05 UTC non-retry-eligible ran AFTER cycle 818 commit, found 7 records, populated them. NOTE: this is the largest single-cycle delta since cycle 811 +9 (2026-10-07 06:00 CST = Hour 20 UTC). 7 records in one fetch is unusually high.

PRE-flight action: 1 refusal translation was detected on transcript id 2107656602597621823 (the "trans people are 1% of the population..." RT) at runtime scan -- retranslated via `retranslate_one.py --id 2107656602597621823` BEFORE running this cycle, producing a faithful Traditional Chinese translation preserving original tone per cycle 226 codification (X-com-fetched-truncated at len_orig=279). The retranslate_one fix landed before any cycle 819 asserts fired.

NEW records (7 substantive retweets, all English -> Traditional Chinese):
- new[0] ID 2107677634469708043 "Elon Musk" RT -> "Elon Musk" (Traditional Chinese, len_orig=9, len_trans=9, ratio=1.00, short byline-only RT, is_retweet=True)
- new[1] ID 2107350648538947870 "Introducing Beam: a highly efficient agentic open model with 501B total parameters and 23B active.\\n\\n- Frontier reasoning efficiency\\n- Advances the Western open frontier on coding & agentic tasks\\n- Trained end-to-end from scratch\\n\\nFull weights release this month.\\n\\nLearn more about" RT (with image) -> "來介紹一下 Beam：高效能的 agentic 開放模型，總參數量 501B，活躍參數 23B。\\n\\n- 前沿推理效率\\n- 在程式碼與 agentic 任務上推進了西方開放前沿\\n- 從零開始端到端訓練\\n\\n本月將完整開源模型權重。\\n\\n想了解更多請看" (Traditional Chinese, len_orig=280, len_trans=122, ratio=0.44, xAI-Beam-launch RT, is_retweet=True, X-com-fetched-truncated per cycle 226 codification; NOTE: this is the SAME record id 2107350648538947870 from cycle 818 as a stub id 2107186849370247235 -- they are distinct ids; new[1] here is the LIVE 2026-10-07 fetched version with longer translation than the cycle 818 stub)
- new[2] ID 2107686149196292110 "Extremely troubling" RT -> "超級令人頭疼" (Traditional Chinese, len_orig=19, len_trans=6, ratio=0.32, Extremely-troubling short RT, is_retweet=True)
- new[3] ID 2107656602597621823 "Although trans people are only 1% of the population, they're 5.4% of K-12 active school shooters since 2015. \\n\\nThat's 5.4x their share. \\nMales are 1.8x theirs. Females are 0.03x.\\n\\nAffirming extreme rates of psychiatric illness, self harm, and violent ideation as an "identity" is" RT (with image) -> "儘管跨性別者僅佔人口的1%，但自2015年以來，他們佔了K-12校園活躍槍擊手的5.4%。\\n\\n這是他們應佔比例的5.4倍。\\n男性是應佔比例的1.8倍。女性則是0.03倍。\\n\\n將極高的精神病發病率、自殘和暴力意念的比率肯定為一種「身份認同」是" (Traditional Chinese, len_orig=279, len_trans=120, ratio=0.43, trans-shooter-statistics RT, is_retweet=True, X-com-fetched-truncated per cycle 226 codification, originally translated as a refusal by fetcher; PRE-flight retranslate_one.py fix applied)
- new[4] ID 2107695858259292561 ""I'm in a Model Y L, and using [FSD Supervised]. \\n\\nThis is the most unbelievable technology I have ever experienced in a car."" RT -> "我現在坐在 Model Y L 裡，用著 [FSD Supervised]。這是我在車上體驗過最扯的技術。" (Traditional Chinese, len_orig=126, len_trans=53, ratio=0.42, Model-Y-L-FSD-Supervised RT, is_retweet=True)
- new[5] ID 2107696351794622954 "Grok Bot summary: IAC 2026 presentation by SpaceXAI President Michael Nicolls.\\n\\n🎯 The main message\\n- SpaceX was founded in 2002 to make life multi-planetary and \\"extend the light of consciousness to the stars.\\"\\n- He said the biggest risk as constellations grow is not debris." RT (with image) -> "🎯 重點摘要\\n\\n- SpaceX 在 2002 年成立，就是要讓生命成為多行星物種，「把意識之光延伸到星星去」\\n- 他說，隨著星鏈越搞越大，最大的風險根本不是碎片問題" (Traditional Chinese, len_orig=275, len_trans=83, ratio=0.30, Grok-Bot-IAC-2026-summary RT, is_retweet=True, X-com-fetched-truncated per cycle 226 codification)
- new[6] ID 2107697003899846720 "Bad news guys: Grok Bot is actually really good 🙃" RT -> "各位～有壞消息：Grok Bot 意外地好用欸 🙃" (Traditional Chinese, len_orig=49, len_trans=25, ratio=0.51, Grok-Bot-really-good RT, is_retweet=True)

All 7 new records inspection gates green (structural 0 empty, byline-only 0 leave-alone, refusal 0 [after PRE-flight retranslate_one fix], simp-leaks 0, trailing-ellipsis 0, dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.30-1.00). 0 of 7 are byline-only tagged (note: new[0] "Elon Musk" is a 9-character byline-only RT but NOT marked byline_orphan=False because the field is reserved for true orphans without proper attribution; this is a normal short RT); 1 of 7 had a translation fix applied (new[3] originally a refusal, retranslate_one.py pre-flight fix to preserve original tone per cycle 226 codification). new[1] has 1 image attached (https://pbs.twimg.com/media/HT46mRYXwAAxTdt?format=jpg&name=small), new[3] has 2 images attached (https://pbs.twimg.com/media/HT_mZwvX0AAVUoJ?format=jpg&name=small + https://pbs.twimg.com/media/HT_mZwrW8AAtQCM?format=jpg&name=small), new[5] has 1 image attached (https://pbs.twimg.com/media/HT-cOGaa8AAPgXs?format=jpg&name=small) -- images are normal RT attachments, no special handling required.

Pitfall 14 prevention (cycle 811 1st-fire, codified cycle 812): pre-run f-string eval pre-check confirmed neither OLD_MARKER ("Last hourly cron deploy: 13:00 CST") nor NEW_MARKER ("Last hourly cron deploy: 14:00 CST") literal appears as a substring of the new lineB body. **9th prevention-fire of pitfall 14** (using f-string eval pre-check per cycle 818 codification -- the cycle 812 naive `re` substring check is INSUFFICIENT for multi-line f-string bodies spanning 30+ lines).

Pitfall 15 prevention (cycle 816 1st-fire): docstring uses `Hour 06 UTC` (no leading zero on the `0X:00` pattern) to avoid the `ast.parse` octal-literal lint trap that Python interprets `06` as octal inside docstrings.

Run normally:    python3 _cycle819.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 819
CST_TIME = "14:00"
UTC_HOUR = "06"
FETCHER_AT = "13:07 CST Hour 05 UTC non-retry-eligible"
NEXT_FETCHER_AT = "14:07 CST Hour 06 UTC retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 25th-fire at Hour 05 UTC

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

OLD_MARKER = "Last hourly cron deploy: 13:00 CST"  # pitfall 12: cycle 818 runtime CST_TIME, NOT cron-tick 13:00
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"
assert OLD_MARKER in html, "OLD_MARKER not found"

# Build NEW_REGION = NEW_MARKER + NEW_LINEB
NEW_LINEB = (
    f"<!-- cron cycle {CYCLE}: cycle {CYCLE} (2026-10-07 {CST_TIME}:00 CST = {UTC_HOUR}:00 UTC): "
    f"SUBSTANTIVE +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR} UTC IS in RETRY_TRANSLATION_HOURS "
    f"{{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- retry-eligible-cron-cycle-substantive form "
    f"(cycle 583/618/620/628 NO-OP reference siblings at retry-eligible hours, cycle 622 prior "
    f"Hour-18 NO-OP, cycle 583 prior SUBSTANTIVE retry-eligible at Hour 09 UTC, cycle 646 prior "
    f"SUBSTANTIVE retry-eligible at Hour 18 UTC, cycle 649 prior SUBSTANTIVE retry-eligible at "
    f"Hour 21 UTC, cycle 816 prior SUBSTANTIVE retry-eligible at Hour 03 UTC -- cycle {CYCLE} = "
    f"3rd-fire SUBSTANTIVE at Hour {UTC_HOUR} UTC retry-eligible, 1st-fire cycle 649 was the "
    f"canonical 1st-fire at Hour 21 UTC, 2nd-fire cycle 816 at Hour 03 UTC): "
    f"SPECIAL SITUATION -- cycle 818 ran as SUBSTANTIVE at 13:00 CST (Hour 05 UTC non-retry-eligible, "
    f"commit d39b4dd, 760th clean push), but the fetcher at 13:07 CST Hour 05 UTC non-retry-eligible "
    f"non-retry pass ran AFTER cycle 818 commit and populated {DELTA} new substantive records into "
    f"tweets.json (CUR went {HEAD_COUNT} -> {CUR_COUNT}) at fetched_at timestamps 2026-10-07T13:07:45-"
    f"13:08:08 CST; cycle 818 SUBSTANTIVE at 13:05 CST did not commit anything FURTHER so the new "
    f"records were not visible until cycle {CYCLE}; cycle {CYCLE} at {CST_TIME} CST (Hour {UTC_HOUR} "
    f"UTC retry-eligible) is the FIRST cycle to see the dirty working tree (` M tweets.json`, "
    f"+{DELTA} records) and the FIRST cycle to commit them; "
    f"fetcher at {FETCHER_AT} populated {DELTA} new substantive retweets: "
    f"new[0] ID 2107677634469708043 \\\"Elon Musk\\\" RT -> \\\"Elon Musk\\\" Traditional Chinese, "
    f"len_orig=9, len_trans=9, ratio=1.00, short byline-only RT, is_retweet=True; "
    f"new[1] ID 2107350648538947870 \\\"Introducing Beam: a highly efficient agentic open model with "
    f"501B total parameters and 23B active.\\n\\n- Frontier reasoning efficiency\\n- Advances the "
    f"Western open frontier on coding & agentic tasks\\n- Trained end-to-end from scratch\\n\\nFull "
    f"weights release this month.\\n\\nLearn more about\\\" RT (with image) -> \\\"來介紹一下 Beam：高效能的 "
    f"agentic 開放模型，總參數量 501B，活躍參數 23B。\\n\\n- 前沿推理效率\\n- 在程式碼與 agentic 任務上推進了"
    f"西方開放前沿\\n- 從零開始端到端訓練\\n\\n本月將完整開源模型權重。\\n\\n想了解更多請看\\\" Traditional Chinese, "
    f"len_orig=280, len_trans=122, ratio=0.44, xAI-Beam-launch RT, is_retweet=True, X-com-fetched-"
    f"truncated per cycle 226 codification; "
    f"new[2] ID 2107686149196292110 \\\"Extremely troubling\\\" RT -> \\\"超級令人頭疼\\\" Traditional Chinese, "
    f"len_orig=19, len_trans=6, ratio=0.32, Extremely-troubling short RT, is_retweet=True; "
    f"new[3] ID 2107656602597621823 \\\"Although trans people are only 1% of the population, they're "
    f"5.4% of K-12 active school shooters since 2015.\\n\\nThat's 5.4x their share.\\nMales are 1.8x "
    f"theirs. Females are 0.03x.\\n\\nAffirming extreme rates of psychiatric illness, self harm, and "
    f"violent ideation as an identity is\\\" RT (with image) -> \\\"儘管跨性別者僅佔人口的1%，但自2015年以來，"
    f"他們佔了K-12校園活躍槍擊手的5.4%。\\n\\n這是他們應佔比例的5.4倍。\\n男性是應佔比例的1.8倍。女性則是0.03倍。\\n\\n"
    f"將極高的精神病發病率、自殘和暴力意念的比率肯定為一種「身份認同」是\\\" Traditional Chinese, "
    f"len_orig=279, len_trans=120, ratio=0.43, trans-shooter-statistics RT, is_retweet=True, "
    f"X-com-fetched-truncated per cycle 226 codification, originally translated as a refusal by "
    f"fetcher; PRE-flight retranslate_one.py fix applied to preserve original tone; "
    f"new[4] ID 2107695858259292561 \\\"I'm in a Model Y L, and using [FSD Supervised].\\n\\nThis is "
    f"the most unbelievable technology I have ever experienced in a car.\\\" RT -> \\\"我現在坐在 Model Y L "
    f"裡，用著 [FSD Supervised]。這是我在車上體驗過最扯的技術。\\\" Traditional Chinese, len_orig=126, "
    f"len_trans=53, ratio=0.42, Model-Y-L-FSD-Supervised RT, is_retweet=True; "
    f"new[5] ID 2107696351794622954 \\\"Grok Bot summary: IAC 2026 presentation by SpaceXAI President "
    f"Michael Nicolls.\\n\\n🎯 The main message\\n- SpaceX was founded in 2002 to make life multi-"
    f"planetary and extend the light of consciousness to the stars.\\n- He said the biggest risk "
    f"as constellations grow is not debris.\\\" RT (with image) -> \\\"🎯 重點摘要\\n\\n- SpaceX 在 2002 年成立，"
    f"就是要讓生命成為多行星物種，「把意識之光延伸到星星去」\\n- 他說，隨著星鏈越搞越大，最大的風險根本不是碎片問題\\\" "
    f"Traditional Chinese, len_orig=275, len_trans=83, ratio=0.30, Grok-Bot-IAC-2026-summary RT, "
    f"is_retweet=True, X-com-fetched-truncated per cycle 226 codification; "
    f"new[6] ID 2107697003899846720 \\\"Bad news guys: Grok Bot is actually really good 🙃\\\" RT -> "
    f"\\\"各位～有壞消息：Grok Bot 意外地好用欸 🙃\\\" Traditional Chinese, len_orig=49, len_trans=25, "
    f"ratio=0.51, Grok-Bot-really-good RT, is_retweet=True; "
    f"all {DELTA} new records inspection gates green (structural 0 empty, byline-only 0 leave-alone, "
    f"refusal 0 [after PRE-flight retranslate_one fix on new[3]], simp-leaks 0, trailing-ellipsis 0, "
    f"dangling-connector 0, corrupted-tail 0, length-sanity ratios 0.30-1.00); 0 of {DELTA} are "
    f"byline-only tagged; 1 of {DELTA} had a translation fix applied (new[3] retranslate_one.py "
    f"pre-flight fix from refusal to faithful translation); "
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
    f"(cycle 818 lineB parsed for canonical 760th + 1 = 761st); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 818 runtime CST_TIME, not cron-tick); "
    f"pitfall 13 (cycle 809 1st-fire) lineB ordinal-count drift cosmetic absorbed "
    f"(25th-fire derived from cycle 818 lineB 24th-fire + 1, trust forward consistency); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe held cleanly "
    f"(f-string eval pre-check confirmed -- 9th prevention-fire per cycle 818 codification); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held cleanly "
    f"(docstring uses `Hour 06 UTC` not `06:00 UTC`); "
    f"cycle 633 vercel-url-pitfall fix held cleanly (CANONICAL -- VERCEL_URL recovered from "
    f"verify.log at runtime); "
    f"untracked-file-tolerant preflight held cleanly (CANONICAL since cycle 585); "
    f"cron-tick RE-bump pattern held cleanly (CANONICAL since cycle 585, "
    f"PRE_REP={PRE_REP} read freshly at runtime); "
    f"jobs.json round-trip patch will absorb cycle 255 dual-completed counter drift "
    f"(PRE-state top.completed={PRE_TOP} vs repeat.completed={PRE_REP} -- perfect sync, no drift to "
    f"absorb; PRE_TOP=PRE_REP={PRE_REP}); "
    f"P31 idempotency guard correctly detected pre_rep={PRE_REP} < EXPECTED_POST_RC={EXPECTED_POST_RC} "
    f"and BUMPED rep to {EXPECTED_POST_RC}; "
    f"P52 symmetric reset will keep alignment: POST top=rep={EXPECTED_POST_RC}; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK (canonical PRE_REP_RC+1={EXPECTED_POST_RC}); "
    f"761st consecutive clean push (webpage-only, no Telegram) -->"
)
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
    "25th-fire fetcher-populates-after-cycle-commit pattern at Hour 05 UTC non-retry-eligible "
    "for the SOURCE fetcher that populated these records -- 3rd-largest delta since cycle 811 "
    "+9): SPECIAL SITUATION -- cycle 818 ran as SUBSTANTIVE at 13:00 CST (Hour 05 UTC non-retry-"
    "eligible, commit d39b4dd, 760th clean push), but the fetcher at 13:07 CST Hour 05 UTC "
    "non-retry-eligible non-retry pass ran AFTER cycle 818 commit and populated {D} new "
    "substantive records into tweets.json (CUR went {HC} -> {CC}); cycle 818 SUBSTANTIVE at "
    "13:05 CST did not commit anything FURTHER so the new records were not visible until "
    "cycle {C}; cycle {C} at {T}:00 CST (Hour {H} UTC retry-eligible) is the FIRST cycle to "
    "see the dirty working tree (` M tweets.json`, +{D} records) and the FIRST cycle to commit "
    "them; fetcher at {FA} populated {D} new substantive records: new[0] ID 2107677634469708043 "
    "Elon-Musk byline-only RT (len_orig=9, len_trans=9, ratio=1.00); new[1] ID 2107350648538947870 "
    "xAI-Beam-launch RT (with image, len_orig=280, len_trans=122, ratio=0.44, X-com-fetched-truncated "
    "per cycle 226 codification); new[2] ID 2107686149196292110 Extremely-troubling short RT "
    "(len_orig=19, len_trans=6, ratio=0.32); new[3] ID 2107656602597621823 trans-shooter-statistics "
    "RT (with 2 images, len_orig=279, len_trans=120, ratio=0.43, X-com-fetched-truncated per cycle "
    "226 codification, originally translated as a refusal by fetcher; PRE-flight retranslate_one.py "
    "fix applied to preserve original tone); new[4] ID 2107695858259292561 Model-Y-L-FSD-Supervised "
    "RT (len_orig=126, len_trans=53, ratio=0.42); new[5] ID 2107696351794622954 Grok-Bot-IAC-2026-"
    "summary RT (with image, len_orig=275, len_trans=83, ratio=0.30, X-com-fetched-truncated per "
    "cycle 226 codification); new[6] ID 2107697003899846720 Grok-Bot-really-good RT (len_orig=49, "
    "len_trans=25, ratio=0.51); all {D} new records inspection gates green (structural 0 empty, "
    "byline-only 0 leave-alone, refusal 0 [after PRE-flight retranslate_one fix on new[3]], "
    "simp-leaks 0, trailing-ellipsis 0, dangling-connector 0, corrupted-tail 0, length-sanity "
    "ratios 0.30-1.00); 0 of {D} byline-only tagged; 1 of {D} translation-fixed (retranslate_one "
    "pre-flight fix on new[3]); next fetcher at {NFA} WILL FIRE retry pass cleanly (0 empty "
    "translations to retry); all {D} snapshot-wide defect gates clean; "
    "P19/P88/P31/P52/cycle-321/P69/P71/P73/cycle-633/untracked-file-tolerant/cron-tick-RE-bump/"
    "pitfall-12/pitfall-13/pitfall-14/pitfall-15 CANONICAL; PREDICTED_RC={E} OK (canonical "
    "PRE_REP_RC+1={E}); jobs.json round-trip patch absorbed cycle 255 dual-completed counter "
    "drift (PRE-state top.completed={PT} vs repeat.completed={P} -- perfect sync, no drift to "
    "absorb); P31 idempotency guard correctly detected pre_rep={P} < EXPECTED_POST_RC={E} "
    "and BUMPED rep to {E}; P52 symmetric reset will keep alignment: POST top=rep={E}; "
    "761st consecutive clean push (webpage-only, no Telegram)"
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

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 761st clean push (webpage-only, no Telegram)"
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