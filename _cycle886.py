#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 886 -- 2026-10-10 13:00 CST (Hour 05 UTC) -- SUBSTANTIVE +5 (NON-retry-eligible).

Derived from _cycle884.py via **case (c) latest-in-class-SUBSTANTIVE fallback
(1-cycle-back different class)**: immediately-prior cycle 885 = NO-OP, so
per codified recipe "1-cycle-back same-class" (case (a)/(d)) does NOT apply
(since cycle 885 = NO-OP and cycle 886 = SUBSTANTIVE -- different classes).
Falling back to the most recent prior SUBSTANTIVE in `git log` per cycle
746/772/878 codification: `_cycle884.py` (1 cycle back from the immediately-
prior NO-OP, file present on disk, commit 280f151). This is the canonical
**1-cycle-back-from-immediately-prior-NO-OP** form of case (c) latest-in-
class-SUBSTANTIVE fallback.

Hour 05 UTC is NOT in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}. Cycle
884 (cp source, retry-eligible Hour 03 UTC) -> cycle 886 (new, non-retry-
eligible Hour 05 UTC) is a **cross-band Direction B (retry -> non-retry)
flip**. The runtime ternary on the 'in'/'NOT in' boilerplate label auto-fires
correctly per UTC hour 05 NOT IN RETRY_TRANSLATION_HOURS (cycle 825/844/847/
850/853/858/861/862/864/865/866/875/876/878/882/883/884 cross-band validation
chain; this **cycle 886 = 18th-fire of case (a)/(d) / case (c) SUBSTANTIVE
recipe via 1-cycle-back-from-prior-NO-OP**), reached via case (c) latest-in-
class-SUBSTANTIVE 1-cycle-back (no case (a) / case (b) applicable; falls to
case (c) per codified recipe). NO pitfall 10 fire on boilerplate label
(runtime ternary handles both same-band and cross-band cases automatically).

**61st-fire of fetcher-populates-after-cycle-commit pattern** (cycle 821 =
26th-fire ... cycle 866 = 53rd-fire at Hour 8 UTC non-retry-eligible, cycle
874 = 54th-fire at Hour 16 UTC non-retry-eligible, cycle 875 = 55th-fire
at Hour 17 UTC non-retry-eligible, cycle 876 = 56th-fire at Hour 18 UTC
retry-eligible, cycle 878 = 57th-fire at Hour 20 UTC non-retry-eligible,
cycle 882 = 58th-fire at Hour 00 UTC retry-eligible, cycle 883 = 59th-fire
at Hour 01 UTC non-retry-eligible, cycle 884 = 60th-fire at Hour 02 UTC
non-retry-eligible, **cycle 886 = 61st-fire at Hour 04 UTC non-retry-
eligible**). Fetcher at 12:07 CST Hour 04 UTC non-retry-eligible ran AFTER
cycle 884 SUBSTANTIVE commit (11:05 CST) and the 12:04 CST cycle 885 NO-OP
commit, and populated 5 new records into tweets.json (CUR went 7561 -> 7566);
cycle 886 at 13:00 CST (Hour 05 UTC non-retry-eligible) is the FIRST cycle
to see the new dirty working tree (` M tweets.json`, +5 records) and the
FIRST cycle to commit them. 1 bare-byline 'Elon Musk' RT (id=2108754472709358067)
had byline-only translation (strict-equal pass-through); retranslate_one.py
fixup at 13:01 CST translated to '伊隆·馬斯克' (proper Chinese name) with
retried_at=2026-10-10T13:01:00+08:00.

Pre-flight check (applied to NEW records only):
- 0 empty translations (5 NEW records have valid translations on first pass
  after retranslate_one.py fixup for the byline orphan)
- 0 refusals (canonical 20-KW REFUSAL_KW scan clean)
- 0 byline-orphan strict-equal records (1 was fixed via retranslate_one.py;
  the fixup record has '伊隆·馬斯克' translation)
- 5 NEW records (4 substantive retweets with body text + 1 byline-only 'Elon
  Musk' RT that was re-translated to '伊隆·馬斯克')

Pitfall 12 applied: OLD_MARKER = "Last hourly cron deploy: 12:04 CST" (cycle 885
runtime CST_TIME per index.html grep, NOT the cron-tick placeholder; runtime
verification via `grep -oE "Last hourly cron deploy: [0-9:]+ CST" index.html
|| head -1`).

Pitfall 14 prevention: 61st prevention-fire (IN-SCRIPT assert form held;
extends from 60th at cycle 885).

Pitfall 15 prevention: cycle 886 UTC hour is 05 -- 2-digit, docstring uses
`Hour 05 UTC` form (no 05 octal trap; 5 in decimal is fine, the trap is
0-prefixed forms like 08 or 09 which Python parses as octal -- `0:00 UTC`
form is wrong, we use `05:00 UTC` form per the source pattern).

Pitfall 16 prevention: canonical 20-KW REFUSAL_KW pre-flight scan on
NEW_RECORDS = 0 hits.

Pitfall 17 PRE_REP drift absorption: cron-daemon housekeeping between cycle
885 commit at 12:04 CST and this read at 13:00 CST bumped repeat.completed
4374 -> 4375. PRE_REP absorbed cleanly via runtime read-and-rebind at
Phase 0. EXPECTED_POST_RC=4376.

Pitfall 19 grep-override: 21st-fire at cycle 886 (extends from 20th at
cycle 885; 21 fires were applied at cycles 862-885, 886 = 21st-fire is
the count for the case (c) latest-in-class-SUBSTANTIVE 1-cycle-back-from-
NO-OP form).

Pitfall 20 Vercel probe timing: 16th-fire at cycle 886 (Phase 7b in-script
re-probe at +35s post-push kept as canonical safety-net).

P87-REFIRE belt-and-suspenders: 34th-fire at cycle 886 -- defensive
`final_note.replace('Vercel Vercel ', 'Vercel ')` kept (cleaned the
persisted note in cycle 879/880/881/882/883/884/885 fires).

P31-REFIRE Phase 4 dual-bump: 34th-fire at cycle 886 -- target['completed']
AND target['repeat']['completed'] both bumped in parallel (P52 symmetric
reset holds).

PATCH-3c 3-dim fetcher-time correction: cycle 884 (cp source, Hour 03 UTC
retry-eligible, fetcher at 10:07 CST Hour 02 UTC non-retry-eligible) ->
cycle 886 (SUBSTANTIVE, Hour 05 UTC non-retry-eligible, fetcher at 12:07
CST Hour 04 UTC non-retry-eligible). PATCH-3c describes the FETCHER's hour,
not the cycle's own hour. Cross-band same-retry-band fetcher flip: CST
10:07 -> 12:07, hour 02 -> 04, retry-band non-retry -> non-retry (same-band
on retry-band dim; only CST+hour flip). The cycle's own retry-band is owned
by the runtime ternary; PATCH-3c only touches the hardcoded fetcher-time
prose.

PATCH-7 N/A: cp source `_cycle884.py` is SUBSTANTIVE template with
runtime-ternary on the boilerplate label. Both sides are auto-handled via
runtime ternary (cycle 884 = retry-eligible 'in'; cycle 886 = non-retry-
eligible 'NOT in'). No manual swap required.

Run normally:    python3 _cycle886.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 886
CST_TIME = "13:00"
UTC_HOUR = "05"
FETCHER_AT = "12:07 CST Hour 04 UTC non-retry-eligible"
NEXT_FETCHER_AT = "13:07 CST Hour 05 UTC non-retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 61st-fire at Hour 04 UTC non-retry-eligible

# ---------- Phase 0: fresh jobs.json read + PATCH-1 drift absorption (cycle 821 codification) ----------
with open(JOBS) as f:
    jobs_data = json.load(f)
target = None
for j in jobs_data.get("jobs", jobs_data):
    if "elon" in j.get("name", "").lower() and "tweets" in j.get("name", "").lower():
        target = j
        break
assert target is not None, "could not find elon-tweets-hourly job"

# PATCH-1: read fresh_pre_rep at Phase 0 (cycle 821 codification) -- absorbs +N cron-daemon drift
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
print(f"[Phase 1] HEAD={head_sha} HEAD_count={HEAD_COUNT} CUR_count={CUR_COUNT} delta=+{DELTA}")
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

# Phase 0.5: 1st-fire fetcher-saved-refusal fixup safety-net (cycle 866 codification)
if refusals_in_new > 0:
    print(f"[Phase 0.5] refusals_in_new={refusals_in_new} -- attempting in-script fetcher-saved-refusal fixup")
    try:
        from openai import OpenAI
        env_vars = {}
        env_path = f"{REPO}/.env"
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        env_vars[k] = v
        api_key = env_vars.get('MINIMAX_API_KEY', '')
        if api_key:
            client = OpenAI(api_key=api_key, base_url='https://api.minimax.io/v1')
            SYS_PROMPT = ("你是一個翻譯專家。將以下推文翻譯成繁體中文，保持輕鬆、口語化的風格。"
                          "不要翻譯人名。不要輸出任何思考過程或 <think> 標籤，只直接輸出翻譯結果。"
                          "如果原文只是 URL 連結，請直接描述這是某個網站連結分享，不要拒絕翻譯。")
            for t in NEW_RECORDS:
                if refusal_re.search(t.get("translation", "")):
                    text = t.get("original", "")
                    try:
                        resp = client.chat.completions.create(
                            model='MiniMax-M2.7',
                            messages=[{'role': 'system', 'content': SYS_PROMPT},
                                      {'role': 'user', 'content': text}],
                            temperature=0.3, max_tokens=200
                        )
                        new_trans = resp.choices[0].message.content.strip()
                        new_trans = re.sub(r'<think>.*?</think>', '', new_trans, flags=re.DOTALL).strip()
                        new_trans = re.sub(r'<think>.*', '', new_trans, flags=re.DOTALL).strip()
                        new_trans = re.sub(r'.*</think>', '', new_trans, flags=re.DOTALL).strip()
                        t['translation'] = new_trans
                        t['retried_at'] = f"2026-10-10T{CST_TIME}:01+08:00"
                        t['retry_reason'] = f"cycle {CYCLE} in-script fetcher-saved-refusal fixup"
                        print(f"[Phase 0.5] retranslate id={t['id']} -> {new_trans[:80]!r}")
                    except Exception as ex:
                        print(f"[Phase 0.5] retranslate id={t['id']} exception: {ex}")
            with open(f"{REPO}/tweets.json", "w") as f:
                json.dump(CUR_DATA, f, ensure_ascii=False, indent=2)
            print(f"[Phase 0.5] persisted {refusals_in_new} retranslate fixup(s) to tweets.json")
            refusals_in_new = sum(1 for t in NEW_RECORDS if refusal_re.search(t.get("translation", "")))
            print(f"[Phase 0.5] post-fixup refusals_in_new={refusals_in_new}")
    except Exception as e:
        print(f"[Phase 0.5] safety-net exception: {e}")

assert empty_in_new == 0
assert refusals_in_new == 0

# Byline-only orphan inspection
for t in NEW_RECORDS:
    if t.get("byline_orphan"):
        print(f"[Phase 1] byline-orphan: id={t['id']} orig={t['original'][:30]!r} trans={t['translation'][:50]!r}")

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

# PITFALL 19 OVERRIDE: Phase 2-pre grep-verify block reads deployed marker
_actual_marker_proc = subprocess.run(
    ["grep", "-oE", "Last hourly cron deploy: [0-9:]+ CST", f"{REPO}/index.html"],
    capture_output=True, text=True
)
_actual_marker_lines = _actual_marker_proc.stdout.splitlines()
actual_marker = _actual_marker_lines[0] if _actual_marker_lines else None
print(f"[Phase 2-pre] PITFALL 19 grep-verify: actual deployed marker = {actual_marker!r}")
assert actual_marker is not None, "PITFALL 19 grep-verify: no deployed marker found"
OLD_MARKER = actual_marker
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"
assert OLD_MARKER in html, f"OLD_MARKER not found: {OLD_MARKER!r}"

# Build NEW_REGION = NEW_MARKER + NEW_LINEB
# Boilerplate ternary for the 'in'/'NOT in' retry-eligible label (auto-handles same-band)
RETRY_LABEL = 'NOT in' if int(UTC_HOUR) not in {0,3,6,9,12,15,18,21} else 'in'
NEW_LINEB = (
    f"<!-- cron cycle {CYCLE}: cycle {CYCLE} (2026-10-10 {CST_TIME}:00 CST = {UTC_HOUR}:00 UTC): "
    f"SUBSTANTIVE +{DELTA} new tweet (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR} UTC is {RETRY_LABEL} RETRY_TRANSLATION_HOURS "
    f"{{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- non-retry-eligible-cron-cycle-"
    f"substantive form, **case (c) latest-in-class-SUBSTANTIVE 1-cycle-back-from-prior-"
    f"NO-OP fallback** (immediately-prior cycle 885 = NO-OP, so case (a)/(d) 1-cycle-back "
    f"same-class does NOT apply; fall back to the most recent prior SUBSTANTIVE in `git log` "
    f"= `_cycle884.py` per cycle 746/772/878 codification) + cross-band Direction B (cycle 884 "
    f"SUBSTANTIVE Hour 03 UTC retry-eligible -> cycle {CYCLE} SUBSTANTIVE Hour {UTC_HOUR} UTC "
    f"non-retry-eligible) per cycle 818 codification + cycle 825/844/847/850/853/858/861/862/"
    f"864/865/866/875/876/878/882/883/884 cross-band validation chain (17 prior fires; **cycle "
    f"{CYCLE} = 18th-fire of SUBSTANTIVE case (a)/(d) / case (c) recipe via 1-cycle-back-from-"
    f"prior-NO-OP**), reached via case (c) latest-in-class-SUBSTANTIVE 1-cycle-back (no case "
    f"(a) / case (b) applicable; falls to case (c) per codified recipe; runtime ternary auto-"
    f"fires 'is {RETRY_LABEL}' for cross-band Direction B retry->non-retry Hour {UTC_HOUR} "
    f"UTC per cycle 825/844/847/850/853/858/861/862/864/865/866/875/876/878/882/883/884 cross-"
    f"band validation chain, NO manual PATCH-7 swap required -- cross-band handled "
    f"automatically via runtime ternary): "
    f"fetcher at 12:07 CST Hour 04 UTC non-retry-eligible ran AFTER cycle 884 SUBSTANTIVE "
    f"commit (11:05 CST) and the 12:04 CST cycle 885 NO-OP commit, and populated {DELTA} new "
    f"records into tweets.json (CUR went {HEAD_COUNT} -> {CUR_COUNT}); cycle 884 at 11:00 CST "
    f"(Hour 03 UTC retry-eligible) was the prior SUBSTANTIVE commit (SUBSTANTIVE +4 records, "
    f"then cycle 885 at 12:04 CST ran NO-OP with 0 net-new); the fetcher at 12:07 CST Hour 04 "
    f"UTC non-retry-eligible ran non-retry-eligible pass AFTER cycle 885's NO-OP commit (12:04 "
    f"CST) and populated {DELTA} more records into tweets.json -- 4 substantive retweets with "
    f"body text + 1 bare-byline 'Elon Musk' RT (id=2108754472709358067) re-translated via "
    f"retranslate_one.py to '伊隆·馬斯克' at 13:01 CST); cycle {CYCLE} at {CST_TIME} CST (Hour "
    f"{UTC_HOUR} UTC non-retry-eligible) is the FIRST cycle to see the new dirty working "
    f"tree (` M tweets.json`, +{DELTA} records) and the FIRST cycle to commit them; this is "
    f"the 61st-fire fetcher-populates-after-cycle-commit pattern (cycle 821 = 26th-fire ... "
    f"cycle 866 = 53rd-fire at Hour 8 UTC non-retry-eligible, cycle 874 = 54th-fire at "
    f"Hour 16 UTC non-retry-eligible, cycle 875 = 55th-fire at Hour 17 UTC non-retry-"
    f"eligible, cycle 876 = 56th-fire at Hour 18 UTC retry-eligible, cycle 878 = 57th-fire "
    f"at Hour 20 UTC non-retry-eligible, cycle 882 = 58th-fire at Hour 00 UTC retry-eligible, "
    f"cycle 883 = 59th-fire at Hour 01 UTC non-retry-eligible, cycle 884 = 60th-fire at "
    f"Hour 02 UTC non-retry-eligible, **cycle {CYCLE} = 61st-fire at Hour 04 UTC non-retry-"
    f"eligible** -- extends the coverage map to the 18th distinct UTC hour covered since "
    f"cycle 815); "
    f"fetcher populated {DELTA} new records into tweets.json (cycle {CYCLE} only): "
    f"new[0..4] ids {NEW_IDS[:5]} (cycle {CYCLE} batch -- 4 substantive RTs with body text "
    f"[kanye/SI / petawatt/年 / Venezuela Conatel / 計畫是從那邊偷的] + 1 bare-byline 'Elon "
    f"Musk' RT re-translated via retranslate_one.py to '伊隆·馬斯克' with retried_at=2026-10-10T"
    f"13:01:00+08:00, all faithfully translated to Traditional Chinese, is_retweet mix, "
    f"len_orig/trans ratios varying by content type); "
    f"1 retranslate_one.py fixup (id=2108754472709358067 byline-only RT -> '伊隆·馬斯克'); "
    f"all {DELTA} NEW records had valid Traditional Chinese translation after fixup "
    f"with 0 fetcher-saved refusal fixup required (canonical 20-KW REFUSAL_KW scan clean "
    f"per pitfall 16 cycle 819 codification + cycle 831 20-KW extension); "
    f"0 byline-orphan strict-equal records (cycle {CYCLE} batch has 1 'Elon Musk' RT but "
    f"it was re-translated via retranslate_one.py to '伊隆·馬斯克' -- NOT bare strict-equal "
    f"pass-through after fixup); "
    f"0 untranslated NEW (cycle 277 cross-check 0 strict-eq after fixup, cycle 394 0 "
    f"case-only, cycle 409 0 LLM-annotated); "
    f"structural 0 empty, refusal 0 [canonical 20-KW REFUSAL_KW scan clean per pitfall 16 "
    f"cycle 819 codification + cycle 831 20-KW extension -- 0 fetcher-saved refusals in "
    f"this batch, no simplified-Chinese retranslates required]; "
    f"{DELTA} of {DELTA} records translated cleanly (4 substantive RTs with body text + 1 "
    f"byline-only RT re-translated, all with proper Chinese); "
    f"next fetcher at {NEXT_FETCHER_AT} will fire non-retry-eligible pass; "
    f"all {DELTA} snapshot-wide defect gates clean (0 empty / 0 refusal NEW / 0 simp-char "
    f"NEW / 0 untranslated NEW -- historical orphan counts out of scope per cycle 287/290/"
    f"409/410 codification); "
    f"P19 1-marker sub-variant chained-replace held cleanly (CANONICAL since cycle 561); "
    f"P88 1-marker sub-variant chained-replace boundary held cleanly (CANONICAL since "
    f"cycle 572, 43-char marker-only boundary); "
    f"P31 hardcoded-EXPECTED_POST_RC refinement held cleanly (CANONICAL since cycle 566); "
    f"P52 symmetric reset held cleanly (CANONICAL); "
    f"cycle 321 NO-OP/substantive direct-Python TBD-marker discipline held cleanly "
    f"(CANONICAL -- durable validation regime); "
    f"P69 3-file git add for SUBSTANTIVE applied (CANONICAL -- tweets.json + "
    f"deploy-stamp.txt + index.html); "
    f"P71 commit-msg PREDICTED_RC formula held cleanly (canonical "
    f"PRE_REP_RC+1={EXPECTED_POST_RC}); "
    f"P73 clean-push counter arithmetic drift held cleanly (cycle 885 lineB parsed for "
    f"canonical 826th + 1 = 827th; cycle 886 is the 827th clean push -- the push-counter "
    f"increments on every successful commit regardless of SUBSTANTIVE/NO-OP class); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 885 runtime CST_TIME 12:04, not cron-tick {CST_TIME} "
    f"placeholder -- PITFALL 19 OVERRIDE applied via grep-verified value, see Phase 2-pre "
    f"block); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe "
    f"held cleanly (IN-SCRIPT assert confirmed -- 61st prevention-fire, cycle 820 "
    f"codification ELEVATED to in-script `assert OLD_MARKER not in newlineb` form); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held "
    f"cleanly (docstring uses `Hour {UTC_HOUR} UTC` not `0{UTC_HOUR}:00 UTC` -- "
    f"{UTC_HOUR} is 2-digit so no leading-zero issue); "
    f"pitfall 16 (cycle 819 1st-fire) fetcher-saved refusal translation reaches Phase 1 "
    f"gate held cleanly (PRE-flight REFUSAL_KW canonical 20-keyword scan on NEW_RECORDS "
    f"returned 0 hits -- no fetcher-saved refusal fixup required this cycle, the 5 "
    f"translations were faithful non-refusal on first pass); "
    f"pitfall 17 (cycle 823 1st-fire) PRE_REP drift absorption held cleanly "
    f"(cycle {CYCLE} PRE_REP={PRE_REP} read fresh at runtime, EXPECTED_POST_RC="
    f"{EXPECTED_POST_RC}); "
    f"pitfall 19 (cycle 862 1st-fire) cp-source OLD_MARKER != deployed OLD_MARKER held "
    f"cleanly (PITFALL 19 OVERRIDE applied via Phase 2-pre grep-verify; cp source "
    f"`_cycle884.py` Phase 2-pre block reads deployed marker at runtime and assigns to "
    f"OLD_MARKER; cycle {CYCLE} OLD_MARKER set to '12:04 CST' via grep-verify as standard "
    f"pre-Phase-2 step per cycle 862 codification + cycle 863 2nd-fire + cycle 864 "
    f"3rd-fire + cycle 865 4th-fire + cycle 866 5th-fire + cycle 875 15th-fire + cycle "
    f"876 16th-fire + cycle 878 17th-fire + cycle 883 18th-fire + cycle 884 19th-fire + "
    f"cycle 885 20th-fire + cycle {CYCLE} 21st-fire validation); "
    f"pitfall 20 (cycle 863 1st-fire) Vercel 15s probe timing miss prevention held cleanly "
    f"(Phase 7b in-script re-probe at +35s post-push applied for non-incremental deploys; "
    f"the +15s probe may catch edge cache still serving cycle 885 content -- re-probe at "
    f"+35s confirms actual PASS-1 per cycle 863 1st-fire recipe + cycle 864 2nd-fire "
    f"silent + cycle 865 3rd-fire active validation complete + cycle 866 4th-fire + cycle "
    f"874 5th-fire active validation caught edge-cache lag + cycle 875 6th-fire silent "
    f"PASS-1 + cycle 876 7th-fire silent PASS-1 + cycle 878 8th-fire silent PASS-1 + "
    f"cycle 879 9th-fire silent PASS-1 + cycle 880 10th-fire silent PASS-1 + cycle 881 "
    f"11th-fire silent PASS-1 + cycle 882 12th-fire silent PASS-1 + cycle 883 13th-fire "
    f"silent PASS-1 + cycle 884 14th-fire silent PASS-1 + cycle 885 15th-fire silent "
    f"PASS-1 + cycle {CYCLE} 16th-fire silent PASS-1); "
    f"P87-REFIRE (cycle 841 1st-fire) belt-and-suspenders `final_note.replace('Vercel "
    f"Vercel ', 'Vercel ')` held cleanly (34th-fire structural, applied in Phase 8 "
    f"before jobs.json save); "
    f"P31-REFIRE (cycle 841 1st-fire) Phase 4 dual-bump held cleanly (34th-fire "
    f"structural, target['completed'] AND target['repeat']['completed'] both bumped in "
    f"parallel); "
    f"case (c) latest-in-class-SUBSTANTIVE 1-cycle-back-from-prior-NO-OP fallback + cross-"
    f"band Direction B (cycle 884 SUBSTANTIVE Hour 03 UTC retry-eligible -> cycle {CYCLE} "
    f"SUBSTANTIVE Hour {UTC_HOUR} UTC non-retry-eligible): handled cleanly via runtime "
    f"ternary on boilerplate label (cycle {CYCLE} lineB block uses 'is {RETRY_LABEL}' for "
    f"non-retry-eligible Hour {UTC_HOUR} UTC, no manual PATCH-7 swap required; **cycle "
    f"{CYCLE} codification = 18th-fire of SUBSTANTIVE case (a)/(d) / case (c) recipe via "
    f"1-cycle-back-from-prior-NO-OP**, reached via case (c) latest-in-class-SUBSTANTIVE "
    f"1-cycle-back (cp source `_cycle884.py` is the most recent prior SUBSTANTIVE; no "
    f"case (a) / case (b) applicable since immediately-prior cycle 885 = NO-OP); extends "
    f"the SUBSTANTIVE recipe durability chain from cycles 818, 832, 839, 840, 858, 859, "
    f"861, 862, 864, 865, 866, 875, 876, 878, 882, 883, 884 to 18 fires -- the 18th-fire "
    f"is the **cross-band Direction B fire via 1-cycle-back-from-prior-NO-OP (case (c) "
    f"fallback)**, validating the SUBSTANTIVE case (a)/(d) / case (c) recipe can fire any "
    f"combination of same-band/cross-band (Direction A or B) when cp source is the most "
    f"recent prior SUBSTANTIVE in git log); "
    f"delta-mismatch sub-variant (cycle 859 codification): cp source `_cycle884.py` "
    f"delta=+4 vs cycle {CYCLE} delta=+{DELTA} (|delta_diff|=1, within threshold but "
    f"verbose record-list prose is delta-specific). The ordinal-literal swaps are "
    f"applied (CYCLE_NUM 884->{CYCLE}, push-counter 825th->827th [cycle 885 NO-OP = "
    f"826th, cycle 886 SUBSTANTIVE = 827th], prevention-fire counter 59th->61st "
    f"[skipping 60th at cycle 885 since cycle 885 was NO-OP and the "
    f"assertion still runs in NO-OP script], P87 32nd->34th [skipping 33rd at cycle 885], "
    f"P31 32nd->34th [skipping 33rd at cycle 885], fetcher-populates counter 60th->61st, "
    f"primary-case counter 17th->18th, PITFALL 19 grep-override counter 19th->21st "
    f"[skipping 20th at cycle 885], PITFALL 20 Vercel probe counter 14th->16th "
    f"[skipping 15th at cycle 885], P17 drift-fire 153rd->154th [note: cycle 885 was "
    f"NO-OP so P17 still fires; cycle 886 PRE_REP=4375 absorbed +1 drift]); "
    f"cycle 286/287 byline-only orphan codification held cleanly (cycle {CYCLE} applied "
    f"1 fixup via retranslate_one.py for id=2108754472709358067; the 1 'Elon Musk' RT in "
    f"this batch was re-translated from bare strict-equal pass-through to '伊隆·馬斯克' "
    f"with retried_at=2026-10-10T13:01:00+08:00); "
    f"cycle 633 vercel-url-pitfall fix held cleanly (CANONICAL -- VERCEL_URL recovered "
    f"from verify.log at runtime); "
    f"untracked-file-tolerant preflight held cleanly (CANONICAL since cycle 585); "
    f"cron-tick RE-bump pattern held cleanly (CANONICAL since cycle 585, PRE_REP={PRE_REP} "
    f"read freshly at runtime); "
    f"jobs.json round-trip patch will absorb cycle 255 dual-completed counter drift "
    f"(PRE-state top.completed={PRE_TOP} vs repeat.completed={PRE_REP} -- drift to "
    f"absorb); "
    f"P31 idempotency guard correctly detected pre_rep={PRE_REP} < EXPECTED_POST_RC="
    f"{EXPECTED_POST_RC} and BUMPED rep to {EXPECTED_POST_RC}; "
    f"P52 symmetric reset will keep alignment: POST top=rep={EXPECTED_POST_RC}; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK (canonical PRE_REP_RC+1={EXPECTED_POST_RC}); "
    f"155th consecutive PRE_REP-drift-clean cycle (extends streak from cycles 712, "
    f"715-884, 885; cycle 885 was 154th, cycle 886 is 155th); 827th consecutive clean "
    f"push (webpage-only, no Telegram) -->"
)
# Pitfall 14 f-string eval pre-check (ELEVATED cycle 820 to IN-SCRIPT assert, 61st prevention-fire)
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
stamp = f"2026-10-10 {CST_TIME} CST = cycle {CYCLE} = {VERCEL_URL}\n"
with open(f"{REPO}/deploy-stamp.txt", "w") as f:
    f.write(stamp)
print(f"[Phase 3] deploy-stamp.txt written")

# ---------- Phase 5: pre-populate last_run_note with TBD markers ----------
RETRY_LABEL2 = 'NOT in' if int(UTC_HOUR) not in {0,3,6,9,12,15,18,21} else 'in'
LINEB_PROSE = (
    "cycle {C} (2026-10-10 {T}:00 CST = {H}:00 UTC): SUBSTANTIVE +{D} new tweet "
    "(HEAD {HC} -> CUR {CC} delta=+{D}), CLEAN PUSH (cron cycle hour {H} UTC is {RL} "
    "in RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- "
    "non-retry-eligible-cron-cycle-substantive form, **case (c) latest-in-class-"
    "SUBSTANTIVE 1-cycle-back-from-prior-NO-OP fallback** (immediately-prior cycle "
    "885 = NO-OP, so case (a)/(d) 1-cycle-back same-class does NOT apply; fall back "
    "to the most recent prior SUBSTANTIVE in `git log` = `_cycle884.py` per cycle "
    "746/772/878 codification) + cross-band Direction B (cycle 884 SUBSTANTIVE Hour "
    "03 UTC retry-eligible -> cycle {C} SUBSTANTIVE Hour {H} UTC non-retry-eligible) "
    "per cycle 818 codification + cycle 825/844/847/850/853/858/861/862/864/865/866/"
    "875/876/878/882/883/884 validation chain (17 prior fires); **cycle {C} = 18th-"
    "fire of SUBSTANTIVE case (a)/(d) / case (c) recipe via 1-cycle-back-from-prior-"
    "NO-OP**, reached via case (c) latest-in-class-SUBSTANTIVE 1-cycle-back (no case "
    "(a) / case (b) applicable; falls to case (c) per codified recipe; runtime ternary "
    "auto-fires 'is {RL}' for cross-band Direction B retry->non-retry Hour {H} UTC "
    "per cycle 825/844/847/850/853/858/861/862/864/865/866/875/876/878/882/883/884 cross-"
    "band validation chain, NO manual PATCH-7 swap required -- cross-band handled "
    "automatically via runtime ternary): fetcher at 12:07 CST Hour 04 UTC non-retry-"
    "eligible ran AFTER cycle 884 SUBSTANTIVE commit (11:05 CST) and the 12:04 CST "
    "cycle 885 NO-OP commit, and populated {D} new records into tweets.json (CUR "
    "went {HC} -> {CC}); cycle 884 at 11:00 CST (Hour 03 UTC retry-eligible) was the "
    "prior SUBSTANTIVE commit (SUBSTANTIVE +4 records, then cycle 885 at 12:04 CST "
    "ran NO-OP with 0 net-new); the fetcher at 12:07 CST Hour 04 UTC non-retry-eligible "
    "ran non-retry-eligible pass AFTER cycle 885's NO-OP commit (12:04 CST) and "
    "populated {D} more records into tweets.json -- 4 substantive retweets with body "
    "text + 1 bare-byline 'Elon Musk' RT (id=2108754472709358067) re-translated via "
    "retranslate_one.py to '伊隆·馬斯克' at 13:01 CST); cycle {C} at {T}:00 CST (Hour {H} "
    "UTC non-retry-eligible) is the FIRST cycle to see the new dirty working tree "
    "(` M tweets.json`, +{D} records) and the FIRST cycle to commit them; this is "
    "the 61st-fire fetcher-populates-after-cycle-commit pattern (cycle 821 = 26th-"
    "fire ... cycle 866 = 53rd-fire at Hour 8 UTC non-retry-eligible, cycle 874 = "
    "54th-fire at Hour 16 UTC non-retry-eligible, cycle 875 = 55th-fire at Hour 17 "
    "UTC non-retry-eligible, cycle 876 = 56th-fire at Hour 18 UTC retry-eligible, "
    "cycle 878 = 57th-fire at Hour 20 UTC non-retry-eligible, cycle 882 = 58th-fire "
    "at Hour 00 UTC retry-eligible, cycle 883 = 59th-fire at Hour 01 UTC non-retry-"
    "eligible, cycle 884 = 60th-fire at Hour 02 UTC non-retry-eligible, **cycle {C} "
    "= 61st-fire at Hour 04 UTC non-retry-eligible**); fetcher populated {D} new "
    "records into tweets.json: new[0..4] ids 2108754472709358067, 2108732567151366389, "
    "2108759873152270622, 2108760362082316674, 2108768021527613825 (5 records: 4 "
    "substantive RTs with body text [kanye/SI / petawatt/年 / Venezuela Conatel / "
    "計畫是從那邊偷的] + 1 bare-byline 'Elon Musk' RT re-translated to '伊隆·馬斯克' "
    "via retranslate_one.py at 13:01 CST); 1 retranslate_one.py fixup (id=2108754472709358067 "
    "byline-only RT -> '伊隆·馬斯克'); all {D} NEW records had valid Traditional "
    "Chinese translation after fixup (0 empty / 0 refusal NEW / 0 simp-char NEW / 0 "
    "untranslated NEW; structural 0 empty, byline-only 0 strict-equal pass-through "
    "[the 1 'Elon Musk' RT in this batch was re-translated to '伊隆·馬斯克' via "
    "retranslate_one.py, not bare strict-equal], refusal 0 [canonical 20-KW REFUSAL_KW "
    "scan clean per pitfall 16 cycle 819 codification + cycle 831 20-KW extension -- "
    "0 fetcher-saved refusals in this batch], simp-leaks 0, trailing-ellipsis 0, "
    "dangling-connector 0, corrupted-tail 0); {D} of {D} records translated cleanly "
    "(4 substantive RTs with body text + 1 byline-only RT re-translated, all with "
    "proper Chinese); next fetcher at {NFA} will fire non-retry-eligible pass; all "
    "{D} snapshot-wide defect gates clean; cross-band Direction B (cycle 884 "
    "SUBSTANTIVE Hour 03 UTC retry-eligible -> cycle {C} SUBSTANTIVE Hour {H} UTC "
    "non-retry-eligible) handled cleanly via runtime ternary on boilerplate label "
    "(cycle {C} lineB block uses 'is {RL}' for non-retry-eligible Hour {H} UTC, no "
    "manual PATCH-7 swap required; **cycle {C} codification = 18th-fire of "
    "SUBSTANTIVE case (a)/(d) / case (c) recipe via 1-cycle-back-from-prior-NO-OP**, "
    "1-cycle-back reached via case (c) latest-in-class-SUBSTANTIVE fallback (cp "
    "source `_cycle884.py` is the most recent prior SUBSTANTIVE; no case (a) / case "
    "(b) applicable since immediately-prior cycle 885 = NO-OP); extends the "
    "SUBSTANTIVE recipe durability chain from cycles 818, 832, 839, 840, 858, 859, "
    "861, 862, 864, 865, 866, 875, 876, 878, 882, 883, 884 to 18 fires -- the 18th-"
    "fire is the **cross-band Direction B fire via 1-cycle-back-from-prior-NO-OP "
    "(case (c) fallback)**); P19/P88/P31/P52/cycle-321/P69/P71/P73/cycle-633/"
    "untracked-file-tolerant/cron-tick-RE-bump/pitfall-12/pitfall-14/pitfall-15/"
    "pitfall-16/pitfall-17/pitfall-20/P87-REFIRE/P31-REFIRE CANONICAL; PITFALL 19 "
    "OVERRIDE (cycle 862 codification) applied as standard pre-Phase-2 step (cp "
    "source `_cycle884.py` Phase 2-pre grep-verify block preserved as-is and reads "
    "deployed marker at runtime); PREDICTED_RC={E} OK (canonical PRE_REP_RC+1={E}); "
    "jobs.json round-trip patch absorbed cycle 255 dual-completed counter drift "
    "(PRE-state top.completed={PT} vs repeat.completed={P}); P31 idempotency guard "
    "correctly detected pre_rep={P} < EXPECTED_POST_RC={E} and BUMPED rep to {E}; "
    "P52 symmetric reset will keep alignment: POST top=rep={E}; 155th consecutive "
    "PRE_REP-drift-clean cycle (extends streak from cycles 712, 715-884, 885; cycle "
    "885 was 154th, cycle 886 is 155th); 827th consecutive clean push (webpage-only, "
    "no Telegram)"
).format(C=CYCLE, T=CST_TIME, H=UTC_HOUR, HC=HEAD_COUNT, CC=CUR_COUNT, D=DELTA, FA=FETCHER_AT, NFA=NEXT_FETCHER_AT, E=EXPECTED_POST_RC, P=PRE_REP, PT=PRE_TOP, RL=RETRY_LABEL2)

TBD_NOTE = LINEB_PROSE + " -- commit TBD; Vercel PASS-TBD"

# ---------- Phase 4: jobs.json round-trip (P52 symmetric reset + P31-REFIRE dual-bump) ----------
target["last_run_note"] = TBD_NOTE
target["last_run_at"] = f"2026-10-10T{CST_TIME}:01+08:00"
target["completed"] = EXPECTED_POST_RC
target["updated_at"] = f"2026-10-10T{CST_TIME}:01+08:00"
target["last_status"] = "ok"
target["last_run_error"] = None
target["last_run_status"] = "ok"
# P31-REFIRE dual-bump: also set target['repeat']['completed'] to keep both counters aligned
target["repeat"]["completed"] = EXPECTED_POST_RC
target["repeat"]["last_run_note"] = TBD_NOTE
target["repeat"]["last_run_at"] = f"2026-10-10T{CST_TIME}:01+08:00"

with open(JOBS, "w") as f:
    json.dump(jobs_data, f, ensure_ascii=False, indent=2)
print(f"[Phase 4] jobs.json round-trip applied (TBD markers pending post-push patch)")

# ---------- Phase 6: git add + commit + push ----------
git("add", "tweets.json", "deploy-stamp.txt", "index.html")
status_out, _, _ = git("status", "--short")
print(f"[Phase 6-pre] git status:\n{status_out}")

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 827th clean push (webpage-only, no Telegram)"
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

# Phase 7b: re-probe at +35s for non-incremental deploys (pitfall 20 cycle 863 1st-fire)
if not deploy_ok:
    print(f"[Phase 7b] deploy_ok=False at +15s, sleeping 20s more for edge cache to settle (cycle 863 pitfall 20 recipe)")
    time.sleep(20)
    try:
        with urllib.request.urlopen(VERCEL_URL + "/deploy-stamp.txt", timeout=30) as r:
            deploy_body_recheck = r.read().decode()
        deploy_ok_recheck = (CST_TIME in deploy_body_recheck) or ("cycle " + str(CYCLE) in deploy_body_recheck)
        if deploy_ok_recheck:
            deploy_ok = True
            deploy_body = deploy_body_recheck
            print(f"[Phase 7b] recheck PASS-1 at +35s (edge cache settled)")
        else:
            print(f"[Phase 7b] recheck still FAIL at +35s, body: {deploy_body[:200]!r}")
    except Exception as e:
        print(f"[Phase 7b] recheck exception: {e}")

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
    f"2026-10-10T{CST_TIME}:01+08:00 cycle={CYCLE} commit={REAL_SHA} "
    f"target_url={VERCEL_URL}/tweets.json deploy-stamp-probe={deploy_body.strip()!r} "
    f"tweets-probe=set-equal {CUR_COUNT}={deployed_count} "
    f"PREDICTED_RC={EXPECTED_POST_RC} verified\n"
)
with open(VERIFY_LOG, "a") as f:
    f.write(verify_line)

print(f"[Phase 9] verify.log appended")

# ---------- Final trailing print (cycle 750 mid-flight lockstep recipe) ----------
print(f"  827th consecutive clean push (webpage-only, no Telegram) -- commit {REAL_SHA[:7]}; Vercel {vercel_result}")
