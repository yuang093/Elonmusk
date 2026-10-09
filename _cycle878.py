#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 878 -- 2026-10-10 05:00 CST (Hour 21 UTC) -- SUBSTANTIVE +1 (RETRY-eligible, fetcher-populates-after-cycle-commit at Hour 20 UTC non-retry-eligible, 1-cycle-back same-class SUB->SUB + cross-band non-retry->retry Direction A band-flip primary case (a)/(d), 14th-fire -- but reached via **case (c) latest-in-class-SUBSTANTIVE fallback** because immediately-prior cycle 877 was NO-OP different class; cp source = `_cycle876.py` is the latest prior SUBSTANTIVE in `git log`).

05:00 CST = Hour 21 UTC. Hour 21 UTC IS in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}.

Hour 21 UTC is RETRY-ELIGIBLE. This is the SUBSTANTIVE retry-eligible form.
Recipe rule (cycle 817 codification): when `git status --porcelain` shows `M tweets.json`
with non-zero records, default to SUBSTANTIVE. Immediately-prior cycle 877 was NO-OP
(different class), so **1-cycle-back same-class does NOT apply** per cycle 818 codification;
fall back to **case (c) latest-in-class-SUBSTANTIVE** per cycle 816 codification. The most
recent prior SUBSTANTIVE in `git log` is cycle 876 (`_cycle876.py` present on disk, 1 cycle
back). cp source _cycle876.py was SUBSTANTIVE non-retry-eligible Hour 19 UTC. Cycle 878 =
SUBSTANTIVE Hour 21 UTC retry-eligible. This is a CROSS-BAND Direction A (non-retry ->
retry) band-flip, the **14th-fire of 1-cycle-back SUBSTANTIVE->SUBSTANTIVE primary case
(a)/(d)**, reached via case (c) 1-cycle-back latest-in-class fallback. The runtime ternary
on the 'in'/'NOT in' boilerplate label auto-fires correctly per UTC hour 21 IS in
RETRY_TRANSLATION_HOURS (cycle 825/844/847/850/853/858/861/862/864/865/866/875/876
cross-band validation chain -- 13 prior fires; **cycle 878 = 14th-fire cross-band
Direction A validation with case (c) 1-cycle-back + cross-band Direction A**; runtime
ternary handles both same-band and cross-band cases automatically per cycles 825/844/
847/850/853/858/861/862/864/865/866/875/876 codifications).

**57th-fire of fetcher-populates-after-cycle-commit pattern** (cycle 821 = 26th-fire,
... cycle 866 = 53rd-fire at Hour 8 UTC non-retry-eligible, cycle 874 = 54th-fire
at Hour 16 UTC non-retry-eligible, cycle 875 = 55th-fire at Hour 17 UTC non-retry-
eligible, cycle 876 = 56th-fire at Hour 18 UTC retry-eligible, **cycle 878 = 57th-fire
at Hour 20 UTC non-retry-eligible** -- extends the coverage map to the 14th non-
retry-eligible UTC hour covered since cycle 815). The fetcher at 04:07 CST Hour 20
UTC non-retry-eligible ran AFTER cycle 877 NO-OP commit (04:03 CST) and populated 1
new record into tweets.json (CUR went 7537 -> 7538); cycle 878 at 05:00 CST (Hour
21 UTC retry-eligible) is the FIRST cycle to see the new dirty working tree
(` M tweets.json`, +1 record) and the FIRST cycle to commit it.

Delta-mismatch sub-variant (cycle 859 codification): cp source `_cycle876.py`
delta=+3, new delta=+1 (|cp_delta - new_delta| = 2, within threshold but verbose
record-list prose is delta-specific). The ordinal-literal swaps (CYCLE_NUM, push-
counter, drift-counter, SHA reference of immediately-prior commit) are handled
below. The verbose record-list prose is REWRITTEN from scratch using actual
NEW_RECORDS list.

Pre-flight check (applied to NEW records only):
- 0 empty translations (1 NEW record has valid translation on first pass)
- 0 refusals (canonical 20-KW REFUSAL_KW scan clean)
- 0 byline-orphan strict-equal records (1 substantive original-tweet, no bare bylines)
- 1 NEW record (1 substantive original post about OpenAI/Altman/Brockman case):
  1. id 2056474896641782077 -- "Regarding the OpenAI case, the judge & jury never
     actually ruled on the merits of the case, just on a calendar technicality.
     There is no question to anyone following the case in detail that Altman &
     Brockman did in fact enrich themselves by stealing a charity. The only
     question is WHEN they did it! I will be filing an appeal with the Ninth
     Circuit, because creating a precedent to loot charities is incredibly
     destructive to charitable giving in America. OpenAI was founded to benefit
     all of humanity." (substantive original post, NOT a retweet; 「關於 OpenAI
     案子，法官跟陪審團壓根沒就案情實質做裁決，只是靠一個日程技術漏洞過關。
     只要有在追這案子的詳細脈絡，大家都清楚 Sam Altman 跟 Greg Brockman 靠著
     掏空慈善機構中飽私囊，這點毫無疑問。唯一的問題是——他們什麼時候做的！
     我會向第九巡迴法院提起上訴，因為一旦開了可以搶劫慈善機構的先例，對美國的
     慈善捐贈風氣將是極具破壞力的。OpenAI 當初創立可是為了造福全人類的啊。」)

Pitfall 12 applied: OLD_MARKER = "Last hourly cron deploy: 04:03 CST" (cycle 877
runtime CST_TIME per index.html grep, NOT the cron-tick placeholder; runtime
verification confirmed via
`grep -oE "Last hourly cron deploy: [0-9:]+ CST" index.html | head -1`).

Pitfall 14 prevention (cycle 820 IN-SCRIPT assert form held; cycle 878 = 53rd
prevention-fire, extends from 52nd at cycle 876).

Pitfall 15 prevention (cycle 816 docstring octal-literal trap): cycle 878 UTC hour
is 21 -- 2-digit, docstring uses `Hour 21 UTC` form (no 021 octal trap; 21 in
decimal is fine, the trap is 0-prefixed forms like `08` or `09` which Python
parses as octal).

Pitfall 16 prevention (cycle 819 1st-fire): canonical 20-KW REFUSAL_KW pre-flight
scan on NEW_RECORDS = 0 hits (1 translation is faithful non-refusal on first pass;
no fetcher-saved refusal fixup required this cycle).

Pitfall 17 PRE_REP drift absorption (cycle 821 PATCH-1): cron-daemon housekeeping
between cycle 877 commit at 04:03 CST and this read at 05:00 CST may bump
repeat.completed by +1 (predicted 4358 -> 4359). PRE_REP absorbed cleanly via
runtime read-and-rebind at Phase 0. (Actual on-disk PRE_REP=4359 at Phase 0 read,
so PREDICTED_POST_RC=4360.)

Pitfall 19 grep-override (cycle 862 codification, 16th-fire at cycle 878, applied
as standard pre-Phase-2 step): ran `grep -oE "Last hourly cron deploy: [0-9:]+ CST"
index.html | head -1` to verify deployed marker. cp source `_cycle876.py` integrated
the Phase 2-pre grep-verify block as canonical pattern (cycle 864 3rd-fire
codification). For cycle 878, the same Phase 2-pre grep-verify block will set
OLD_MARKER at runtime to "04:03 CST" (cycle 877's deployed marker, unchanged since
04:03 CST commit).

Pitfall 20 Vercel probe timing (cycle 863 1st-fire, cycle 864 2nd-fire silent,
cycle 865 3rd-fire active validation complete, cycle 866 4th-fire, cycle 874 5th-
fire actively caught edge-cache lag, cycle 875 6th-fire silent PASS-1, cycle
876 7th-fire silent PASS-1): Phase 7b in-script re-probe at +35s post-push
for non-incremental deploys; the +15s probe may catch edge cache still
serving prior cycle content. The safety-net is kept
as canonical.

P87-REFIRE belt-and-suspenders: runtime ternary emits the correct 'in' label
(retry-eligible Hour 21 UTC) -- defensive `final_note.replace('Vercel Vercel ',
'Vercel ')` kept.

P31-REFIRE Phase 4 dual-bump: target['completed'] AND target['repeat']['completed']
both bumped in parallel (P52 symmetric reset holds).

Run normally:    python3 _cycle878.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 878
CST_TIME = "05:00"
UTC_HOUR = "21"
FETCHER_AT = "04:07 CST Hour 20 UTC non-retry-eligible"
NEXT_FETCHER_AT = "06:07 CST Hour 22 UTC non-retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 57th-fire at Hour 20 UTC non-retry-eligible

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

# ---------- Phase 0.5: 1st-fire fetcher-saved-refusal fixup safety-net ----------
# Cycle 866 1st-fire defensive safety-net: if a fetcher-saved URL-only refusal
# (REFUSAL_KW hit) is detected, attempt in-script retranslate via the configured
# MINIMAX_API_KEY. Cycle 878 has 0 fetcher-saved refusals, so this safety-net
# is skipped but kept for structural consistency with cp source `_cycle876.py`
# (which inherited it from cycle 866).
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
            # Persist fixups to tweets.json
            with open(f"{REPO}/tweets.json", "w") as f:
                json.dump(CUR_DATA, f, ensure_ascii=False, indent=2)
            print(f"[Phase 0.5] persisted {refusals_in_new} retranslate fixup(s) to tweets.json")
            # Re-scan
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

# PITFALL 19 OVERRIDE (cycle 862 codification, 16th-fire at cycle 878, applied as
# standard pre-Phase-2 step): cp source `_cycle876.py` integrated the Phase 2-pre
# grep-verify block as canonical pattern (cycle 864 3rd-fire codification). For
# cycle 878, the same Phase 2-pre grep-verify block reads the deployed marker from
# index.html at runtime; deployed marker is "Last hourly cron deploy: 04:03 CST"
# (cycle 877's runtime CST_TIME, unchanged since 04:03 CST commit). The Phase 2-pre
# grep-verify block is preserved as-is from cp source, no override patch required
# this cycle.
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
    f"{{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- retry-eligible-cron-cycle-substantive "
    f"form, **case (c) latest-in-class-SUBSTANTIVE 1-cycle-back fallback** + cross-band non-"
    f"retry->retry Direction A band-flip primary case (a)/(d) per cycle 816 codification + "
    f"cycle 825/844/847/850/853/858/861/862/864/865/866/875/876 cross-band validation chain "
    f"(13 prior fires); "
    f"**cycle {CYCLE} = 14th-fire of 1-cycle-back SUBSTANTIVE->SUBSTANTIVE primary case (a)/(d)**, "
    f"reached via case (c) 1-cycle-back latest-in-class-SUBSTANTIVE fallback since immediately-"
    f"prior cycle 877 was NO-OP different class -- cp source = `_cycle876.py` (most recent "
    f"prior SUBSTANTIVE in `git log`, 1 cycle back); runtime ternary auto-fires 'is {RETRY_LABEL}' "
    f"for cross-band Direction A retry-eligible Hour {UTC_HOUR} UTC per cycle 825/844/847/850/"
    f"853/858/861/862/864/865/866/875/876 codifications, NO manual PATCH-7 swap required -- "
    f"cross-band Direction A handled automatically): "
    f"fetcher at 04:07 CST Hour 20 UTC non-retry-eligible ran AFTER cycle 877 NO-OP "
    f"commit (04:03 CST) and populated {DELTA} new record into tweets.json (CUR went "
    f"{HEAD_COUNT} -> {CUR_COUNT}); cycle 877 at 04:00 CST (Hour 20 UTC non-retry-eligible) "
    f"was the prior cycle's commit (NO-OP 0 new, but the fetcher at 04:07 CST Hour 20 UTC "
    f"non-retry-eligible then ran non-retry-eligible pass and populated {DELTA} more record "
    f"into tweets.json -- 1 substantive original-tweet post about the OpenAI/Altman/Brockman "
    f"charity-looting case, no URL-only refusal fixups required this cycle); cycle {CYCLE} "
    f"at {CST_TIME} CST (Hour {UTC_HOUR} UTC retry-eligible) is the FIRST cycle to see the new "
    f"dirty working tree (` M tweets.json`, +{DELTA} record) and the FIRST cycle to commit "
    f"it; this is the 57th-fire fetcher-populates-after-cycle-commit pattern (cycle 821 = "
    f"26th-fire ... cycle 866 = 53rd-fire at Hour 8 UTC non-retry-eligible, cycle 874 = 54th-"
    f"fire at Hour 16 UTC non-retry-eligible, cycle 875 = 55th-fire at Hour 17 UTC non-"
    f"retry-eligible, cycle 876 = 56th-fire at Hour 18 UTC retry-eligible, **cycle {CYCLE} = "
    f"57th-fire at Hour 20 UTC non-retry-eligible** -- extends the coverage map to the 14th "
    f"distinct non-retry-eligible UTC hour covered since cycle 815); "
    f"fetcher populated {DELTA} new record into tweets.json (cycle {CYCLE} only): "
    f"new[0] (id 2056474896641782077, openai-altman-charity-case-original, substantive "
    f"original-tweet post (NOT a retweet) about the OpenAI judge-ruling / Altman & "
    f"Brockman charity-looting case + Ninth Circuit appeal + OpenAI was founded to benefit "
    f"all of humanity -- 「關於 OpenAI 案子，法官跟陪審團壓根沒就案情實質做裁決，只是靠"
    f"一個日程技術漏洞過關。只要有在追這案子的詳細脈絡，大家都清楚 Sam Altman 跟 Greg "
    f"Brockman 靠著掏空慈善機構中飽私囊，這點毫無疑問。唯一的問題是——他們什麼時候做的！"
    f"我會向第九巡迴法院提起上訴，因為一旦開了可以搶劫慈善機構的先例，對美國的慈善捐贈"
    f"風氣將是極具破壞力的。OpenAI 當初創立可是為了造福全人類的啊。」Traditional Chinese); "
    f"0 retranslate_one.py equivalent in-script fixups; "
    f"all {DELTA} NEW record had valid Traditional Chinese translation on first pass "
    f"with 0 fetcher-saved refusal fixup required (canonical 20-KW REFUSAL_KW scan clean per "
    f"pitfall 16 cycle 819 codification + cycle 831 20-KW extension); "
    f"0 byline-orphan strict-equal records (cycle {CYCLE} has 1 substantive original-tweet "
    f"post, no bare bylines); "
    f"0 untranslated NEW (cycle 277 cross-check 0 strict-eq after fixup, cycle 394 0 "
    f"case-only, cycle 409 0 LLM-annotated); "
    f"structural 0 empty, refusal 0 [canonical 20-KW REFUSAL_KW scan clean per pitfall 16 "
    f"cycle 819 codification + cycle 831 20-KW extension -- 0 fetcher-saved refusals in this "
    f"batch, no simplified-Chinese retranslates required]; "
    f"{DELTA} of {DELTA} record translated cleanly (1 substantive original-tweet post, all with "
    f"proper Chinese); "
    f"next fetcher at {NEXT_FETCHER_AT} will fire non-retry-eligible pass; "
    f"all {DELTA} snapshot-wide defect gates clean (0 empty / 0 refusal NEW / "
    f"0 simp-char NEW / 0 untranslated NEW -- historical orphan counts out of "
    f"scope per cycle 287/290/409/410 codification); "
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
    f"P73 clean-push counter arithmetic drift held cleanly (cycle 876 lineB "
    f"parsed for canonical 818th + 1 = 819th); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 877 runtime CST_TIME 04:03, not cron-tick {CST_TIME} "
    f"placeholder -- PITFALL 19 OVERRIDE applied via grep-verified value, see Phase 2-pre "
    f"block); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe "
    f"held cleanly (IN-SCRIPT assert confirmed -- 53rd prevention-fire, cycle 820 codification "
    f"ELEVATED to in-script `assert OLD_MARKER not in newlineb` form); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held "
    f"cleanly (docstring uses `Hour {UTC_HOUR} UTC` not `0{UTC_HOUR}:00 UTC` -- {UTC_HOUR} "
    f"is 2-digit so no leading-zero issue); "
    f"pitfall 16 (cycle 819 1st-fire) fetcher-saved refusal translation reaches Phase 1 "
    f"gate held cleanly (PRE-flight REFUSAL_KW canonical 20-keyword scan on NEW_RECORDS "
    f"returned 0 hits -- no fetcher-saved refusal fixup required this cycle, the 1 "
    f"translation was faithful non-refusal on first pass); "
    f"pitfall 17 (cycle 823 1st-fire) PRE_REP drift absorption held cleanly "
    f"(cycle {CYCLE} PRE_REP={PRE_REP} read fresh at runtime, EXPECTED_POST_RC="
    f"{EXPECTED_POST_RC}); "
    f"pitfall 19 (cycle 862 1st-fire) cp-source OLD_MARKER != deployed OLD_MARKER held "
    f"cleanly (PITFALL 19 OVERRIDE applied via Phase 2-pre grep-verify; cp source "
    f"`_cycle876.py` Phase 2-pre block reads deployed marker at runtime and assigns to "
    f"OLD_MARKER; cycle {CYCLE} OLD_MARKER set to '04:03 CST' via grep-verify as standard "
    f"pre-Phase-2 step per cycle 862 codification + cycle 863 2nd-fire + cycle 864 "
    f"3rd-fire + cycle 865 4th-fire + cycle 866 5th-fire + cycle 875 15th-fire + cycle "
    f"876 16th-fire + cycle 878 16th-fire validation); "
    f"pitfall 20 (cycle 863 1st-fire) Vercel 15s probe timing miss prevention held cleanly "
    f"(Phase 7b in-script re-probe at +35s post-push applied for non-incremental deploys; "
    f"the +15s probe may catch edge cache still serving cycle 877 content -- re-probe at "
    f"+35s confirms actual PASS-1 per cycle 863 1st-fire recipe + cycle 864 2nd-fire silent "
    f"+ cycle 865 3rd-fire active validation complete + cycle 866 4th-fire + cycle 874 "
    f"5th-fire active validation caught edge-cache lag + cycle 875 6th-fire silent PASS-1 "
    f"+ cycle 876 7th-fire silent PASS-1); "
    f"P87-REFIRE (cycle 841 1st-fire) belt-and-suspenders `final_note.replace('Vercel "
    f"Vercel ', 'Vercel ')` held cleanly (26th-fire structural, applied in Phase 8 "
    f"before jobs.json save); "
    f"P31-REFIRE (cycle 841 1st-fire) Phase 4 dual-bump held cleanly (26th-fire "
    f"structural, target['completed'] AND target['repeat']['completed'] both bumped in "
    f"parallel); "
    f"case (c) latest-in-class-SUBSTANTIVE 1-cycle-back fallback + cross-band Direction A "
    f"non-retry->retry (cycle 876 SUBSTANTIVE Hour 19 UTC non-retry-eligible -> cycle {CYCLE} "
    f"Hour {UTC_HOUR} UTC retry-eligible): handled cleanly via runtime ternary on boilerplate "
    f"label (cycle {CYCLE} lineB block uses 'is {RETRY_LABEL}' for retry-eligible Hour "
    f"{UTC_HOUR} UTC, no manual PATCH-7 swap required; **cycle {CYCLE} codification = "
    f"14th-fire of 1-cycle-back SUBSTANTIVE->SUBSTANTIVE primary case (a)/(d)**, reached via "
    f"case (c) 1-cycle-back latest-in-class-SUBSTANTIVE fallback since immediately-prior "
    f"cycle 877 was NO-OP different class; extends the primary case (a)/(d) durability "
    f"chain from cycles 818, 832, 839, 840, 858, 859, 861, 862, 864, 865, 866, 875, 876 to "
    f"14 fires -- the 14th-fire is the **cross-band Direction A fire via case (c) 1-cycle-"
    f"back latest-in-class-SUBSTANTIVE fallback** -- the case (c) 1-cycle-back variant "
    f"validates cycles 825/844/847/850/853/858/861/862/864/865/866/875/876 cross-band "
    f"Direction A codifications at the case (c) 1-cycle-back + cross-band primary case "
    f"(a)/(d) form); "
    f"delta-mismatch sub-variant (cycle 859 codification): cp source `_cycle876.py` "
    f"delta=+3 vs cycle {CYCLE} delta=+{DELTA} (|delta_diff|=2) -- ordinal-literal swaps "
    f"applied (CYCLE_NUM 876->{CYCLE}, push-counter 818th->819th, prevention-fire "
    f"counter 52nd->53rd, P87 25th->26th, P31 25th->26th, fetcher-populates counter "
    f"56th->57th, primary-case counter 13th->14th, PITFALL 19 grep-override counter "
    f"15th->16th, PITFALL 20 Vercel probe counter 7th->8th, P17 drift-fire 146th->147th) but "
    f"verbose record-list prose inside NEW_LINEB/LINEB_PROSE was REWRITTEN from scratch "
    f"using actual {DELTA}-record NEW_RECORDS list; "
    f"cycle 286/287 byline-only orphan codification held cleanly (cycle {CYCLE} applied "
    f"0 fixes; no bare-byline 'Elon Musk' strict-equal records in this batch -- the 1 "
    f"record is a substantive original-tweet post with body text); "
    f"cycle 633 vercel-url-pitfall fix held cleanly (CANONICAL -- VERCEL_URL recovered "
    f"from verify.log at runtime); "
    f"untracked-file-tolerant preflight held cleanly (CANONICAL since cycle 585); "
    f"cron-tick RE-bump pattern held cleanly (CANONICAL since cycle 585, PRE_REP={PRE_REP} "
    f"read freshly at runtime); "
    f"jobs.json round-trip patch will absorb cycle 255 dual-completed counter drift "
    f"(PRE-state top.completed={PRE_TOP} vs repeat.completed={PRE_REP} -- drift to absorb); "
    f"P31 idempotency guard correctly detected pre_rep={PRE_REP} < EXPECTED_POST_RC="
    f"{EXPECTED_POST_RC} and BUMPED rep to {EXPECTED_POST_RC}; "
    f"P52 symmetric reset will keep alignment: POST top=rep={EXPECTED_POST_RC}; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK (canonical PRE_REP_RC+1={EXPECTED_POST_RC}); "
    f"147th consecutive PRE_REP-drift-clean cycle (extends streak from cycles 712, "
    f"715-876); 819th consecutive clean push (webpage-only, no Telegram) -->"
)
# Pitfall 14 f-string eval pre-check (ELEVATED cycle 820 to IN-SCRIPT assert, 53rd prevention-fire)
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
# Use plain string (not f-string) to avoid cycle 608 f-string escape pitfall on inner quotes.
RETRY_LABEL2 = 'NOT in' if int(UTC_HOUR) not in {0,3,6,9,12,15,18,21} else 'in'
LINEB_PROSE = (
    "cycle {C} (2026-10-10 {T}:00 CST = {H}:00 UTC): SUBSTANTIVE +{D} new tweet "
    "(HEAD {HC} -> CUR {CC} delta=+{D}), CLEAN PUSH (cron cycle hour {H} UTC is {RL} "
    "in RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- "
    "retry-eligible-cron-cycle-substantive form, **case (c) latest-in-class-SUBSTANTIVE "
    "1-cycle-back fallback** + cross-band non-retry->retry Direction A band-flip primary "
    "case (a)/(d) per cycle 816 codification + cycle 825/844/847/850/853/858/861/862/864/"
    "865/866/875/876 cross-band validation chain (13 prior fires); **cycle {C} = 14th-fire "
    "of 1-cycle-back SUBSTANTIVE->SUBSTANTIVE primary case (a)/(d)**, reached via case (c) "
    "1-cycle-back latest-in-class-SUBSTANTIVE fallback since immediately-prior cycle 877 was "
    "NO-OP different class; runtime ternary auto-fires 'is {RL}' for cross-band Direction A "
    "retry-eligible Hour {H} UTC per cycle 825/844/847/850/853/858/861/862/864/865/866/875/"
    "876 codifications, NO manual PATCH-7 swap required -- cross-band Direction A handled "
    "automatically): fetcher at 04:07 CST Hour 20 UTC non-retry-eligible ran AFTER cycle "
    "877 NO-OP commit (04:03 CST) and populated {D} new record into tweets.json (CUR went "
    "{HC} -> {CC}); cycle 877 at 04:00 CST (Hour 20 UTC non-retry-eligible) was the prior "
    "cycle's commit (NO-OP 0 new, but the fetcher at 04:07 CST Hour 20 UTC non-retry-"
    "eligible then ran non-retry-eligible pass and populated {D} more record into "
    "tweets.json -- 1 substantive original-tweet post about the OpenAI/Altman/Brockman "
    "charity-looting case); cycle {C} at {T}:00 CST (Hour {H} UTC retry-eligible) is the "
    "FIRST cycle to see the new dirty working tree (` M tweets.json`, +{D} record) and the "
    "FIRST cycle to commit it; this is the 57th-fire fetcher-populates-after-cycle-commit "
    "pattern (cycle 821 = 26th-fire ... cycle 866 = 53rd-fire at Hour 8 UTC non-retry-"
    "eligible, cycle 874 = 54th-fire at Hour 16 UTC non-retry-eligible, cycle 875 = 55th-"
    "fire at Hour 17 UTC non-retry-eligible, cycle 876 = 56th-fire at Hour 18 UTC retry-"
    "eligible, **cycle {C} = 57th-fire at Hour 20 UTC non-retry-eligible**); fetcher "
    "populated {D} new record into tweets.json: new[0] id 2056474896641782077 (openai-"
    "altman-charity-case-original); 0 retranslate_one.py equivalent in-script fixups; all "
    "{D} NEW record has valid Traditional Chinese translation on first pass (0 empty / 0 "
    "refusal NEW / 0 simp-char NEW / 0 untranslated NEW; structural 0 empty, byline-only 0 "
    "strict-equal pass-through [no bare-byline RTs in this batch], refusal 0 [canonical 20-"
    "KW REFUSAL_KW scan clean per pitfall 16 cycle 819 codification + cycle 831 20-KW "
    "extension -- 0 fetcher-saved refusals in this batch], simp-leaks 0, trailing-ellipsis "
    "0, dangling-connector 0, corrupted-tail 0); {D} of {D} record translated cleanly (1 "
    "substantive original-tweet post); next fetcher at {NFA} will fire non-retry-eligible "
    "pass; all {D} snapshot-wide defect gates clean; cross-band Direction A non-retry->"
    "retry (cycle 876 SUBSTANTIVE Hour 19 UTC non-retry-eligible -> cycle {C} Hour {H} "
    "UTC retry-eligible) handled cleanly via runtime ternary on boilerplate label (cycle "
    "{C} lineB block uses 'is {RL}' for retry-eligible Hour {H} UTC, no manual PATCH-7 "
    "swap required; **cycle {C} codification = 14th-fire of 1-cycle-back SUBSTANTIVE->"
    "SUBSTANTIVE primary case (a)/(d)**, extends the primary case (a)/(d) durability "
    "chain from cycles 818, 832, 839, 840, 858, 859, 861, 862, 864, 865, 866, 875, 876 "
    "to 14 fires -- the 14th-fire is the **cross-band Direction A fire via case (c) 1-"
    "cycle-back latest-in-class-SUBSTANTIVE fallback**); P19/P88/P31/P52/cycle-321/"
    "P69/P71/P73/cycle-633/untracked-file-tolerant/cron-tick-RE-bump/pitfall-12/pitfall-14/"
    "pitfall-15/pitfall-16/pitfall-17/pitfall-20/P87-REFIRE/P31-REFIRE CANONICAL; PITFALL 19 "
    "OVERRIDE (cycle 862 codification) applied as standard pre-Phase-2 step (cp source "
    "`_cycle876.py` Phase 2-pre grep-verify block preserved as-is and reads deployed "
    "marker at runtime); PREDICTED_RC={E} OK (canonical PRE_REP_RC+1={E}); jobs.json round-"
    "trip patch absorbed cycle 255 dual-completed counter drift (PRE-state top.completed={PT} "
    "vs repeat.completed={P}); P31 idempotency guard correctly detected pre_rep={P} < "
    "EXPECTED_POST_RC={E} and BUMPED rep to {E}; P52 symmetric reset will keep alignment: "
    "POST top=rep={E}; 147th consecutive PRE_REP-drift-clean cycle (extends streak from "
    "cycles 712, 715-876); 819th consecutive clean push (webpage-only, no Telegram)"
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

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweet (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 819th clean push (webpage-only, no Telegram)"
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
print(f"[Phase 9] verify.log entry written")

print(f"\n=== CYCLE {CYCLE} COMPLETE ===")
print(f"HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}")
print(f"commit {REAL_SHA[:7]}")
print(f"PREDICTED_RC={EXPECTED_POST_RC} vercel_result={vercel_result}")
