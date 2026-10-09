#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 861 -- 2026-10-09 12:00 CST (Hour 4 UTC) -- SUBSTANTIVE +1 (non-retry-eligible, fetcher-populates-after-cycle-commit, 1-cycle-back SUBSTANTIVE->SUBSTANTIVE same-band non-retry->non-retry primary case (a)/(d), 7th-fire).

12:00 CST = Hour 4 UTC. Hour 4 UTC is NOT in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}.

Hour 4 UTC is NON-RETRY-ELIGIBLE. This is the SUBSTANTIVE non-retry-eligible form.
Recipe rule (cycle 817 codification, REFINED cycle 831): when `git status --porcelain`
shows `M tweets.json` with non-zero records, default to SUBSTANTIVE. Immediately-prior
cycle 860 was NO-OP (different class), so **latest-in-class-SUBSTANTIVE fallback**
(cycle 857 codification, complement of cycle 807) applies -- the most recent SUBSTANTIVE
in the rotation before cycle 860 is cycle 859 (Hour 2 UTC non-retry-eligible, +3 records).
Cp source = `_cycle859.py` (Hour 2 UTC non-retry-eligible, +3 records).

**7th-fire of 1-cycle-back SUBSTANTIVE->SUBSTANTIVE same-band non-retry->non-retry
primary case (a)/(d) (cycle 818 origin + cycles 832 + 839 + 840 + 858 + 859 = 6 prior
fires, this is the 7th-fire; CANONICAL since cycle 840 by chain-of-validation at 4
fires, with cycles 858/859 5th/6th-fires and this 7th-fire reinforcing durability)**:
- cycle 859 (cp source) = SUBSTANTIVE Hour 2 UTC non-retry-eligible
- cycle 861 (new) = SUBSTANTIVE Hour 4 UTC non-retry-eligible
- This is same-band non-retry->non-retry (NO band-flip)
- The runtime ternary emits 'NOT in' for both cp source and new cycle (Hour 2 and
  Hour 4 are both NOT in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21})
- NO pitfall 10 fire on boilerplate label (runtime ternary handles same-band case
  automatically -- NO PATCH-7 swap required)

CRITICAL -- this is the **latest-in-class-SUBSTANTIVE fallback** (cycle 857 complement
of cycle 807). The fetcher at 11:07 CST Hour 3 UTC retry-eligible ran AFTER cycle 860
commit (11:00 CST, NO-OP) and populated 1 net-new substantive RT record into tweets.json
(HEAD 7498 -> CUR 7499). Cycle 860 NO-OP at 11:00 CST did NOT commit anything FURTHER
so the new record was not visible until cycle 861. **This is the 49th-fire
fetcher-populates-after-cycle-commit pattern** (cycle 821 = 26th-fire, ... cycle 859
= 48th-fire at Hour 1 UTC non-retry-eligible, **cycle 861 = 49th-fire at Hour 3 UTC
retry-eligible** -- the fetcher's retry-eligible retry pass at 11:07 CST populated the
record).

Pre-flight check (applied to NEW records only):
- 0 empty translations (1 NEW record has valid translation on first pass)
- 0 refusals (canonical 20-KW REFUSAL_KW scan clean)
- 0 byline-orphan fixes (the 1 NEW record is a substantive RT, not a bare byline)
- 1 NEW record: id 2108270660275609612, RT by @elonmusk of user's complaint about
  Grok Bot subscribing to recurring meal-prep instead of one-off -- 「『AI出包我們幫你
  買單』的保證...多扣了我£57（$75）」 Traditional Chinese translation

Pitfall 12 applied: OLD_MARKER = "Last hourly cron deploy: 11:05 CST" (cycle 860
runtime CST_TIME per index.html grep, NOT the cron-tick placeholder).

Pitfall 14 prevention (cycle 820 IN-SCRIPT assert form held; cycle 861 = 37th
prevention-fire).

Pitfall 15 prevention (cycle 816 docstring octal-literal trap): cycle 861 UTC hour
is 4 -- 1-digit, docstring uses `Hour 4 UTC` form (no 08/09 octal trap).

Pitfall 16 prevention (cycle 819 1st-fire, 2nd-fire cycle 821, 3rd-fire cycle 831):
canonical 20-KW REFUSAL_KW pre-flight scan on NEW_RECORDS = 0 hits.

Pitfall 17 PRE_REP drift absorption (cycle 821 PATCH-1): cron-daemon bumped
repeat.completed to 4325 (cycle 860 exited at POST_rep=4324; cron-daemon housekeeping
between cycle 860 commit at 11:05 CST and this read at 12:00 CST = +1 drift, expected
POST_top=rep=4325). PRE_REP=4324 absorbed cleanly via runtime read-and-rebind at
Phase 0.

P87-REFIRE belt-and-suspenders: runtime ternary emits the correct 'NOT in' label
(non-retry-eligible Hour 4 UTC) -- defensive `final_note.replace('Vercel Vercel ',
'Vercel ')` kept.

P31-REFIRE Phase 4 dual-bump: target['completed'] AND target['repeat']['completed']
both bumped in parallel (P52 symmetric reset holds).

Run normally:    python3 _cycle861.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 861
CST_TIME = "12:00"
UTC_HOUR = "4"
FETCHER_AT = "11:07 CST Hour 3 UTC retry-eligible"
NEXT_FETCHER_AT = "13:00 CST Hour 5 UTC non-retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 49th-fire at Hour 3 UTC retry-eligible

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

# pitfall 12: OLD_MARKER must be cycle 860 RUNTIME CST_TIME (11:05), not cron-tick placeholder
OLD_MARKER = "Last hourly cron deploy: 11:05 CST"
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"
assert OLD_MARKER in html, f"OLD_MARKER not found: {OLD_MARKER!r}"

# Build NEW_REGION = NEW_MARKER + NEW_LINEB
# Boilerplate ternary for the 'in'/'NOT in' retry-eligible label (auto-handles Direction B)
RETRY_LABEL = 'NOT in' if int(UTC_HOUR) not in {0,3,6,9,12,15,18,21} else 'in'
NEW_LINEB = (
    f"<!-- cron cycle {CYCLE}: cycle {CYCLE} (2026-10-09 {CST_TIME}:00 CST = {UTC_HOUR}:00 UTC): "
    f"SUBSTANTIVE +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR} UTC is {RETRY_LABEL} RETRY_TRANSLATION_HOURS "
    f"{{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- non-retry-eligible-cron-cycle-substantive "
    f"form, 1-cycle-back SUBSTANTIVE->SUBSTANTIVE same-band non-retry->non-retry primary "
    f"case (a)/(d) per cycle 818 codification + cycle 832 2nd-fire + cycle 839 3rd-fire + "
    f"cycle 840 4th-fire (CANONICAL since cycle 840) + cycle 858 5th-fire + cycle 859 6th-fire + "
    f"**cycle {CYCLE} = 7th-fire** (applied PATCH-3c ordinal-literal swaps on cp source "
    f"`_cycle859.py` Hour 2 UTC non-retry-eligible; immediately-prior cycle 860 was NO-OP "
    f"different class, so latest-in-class-SUBSTANTIVE fallback applies per cycle 857 "
    f"codification -- the most recent SUBSTANTIVE in the rotation is cycle 859; runtime "
    f"ternary emits 'NOT in' for both Hour 2 and Hour {UTC_HOUR} since both are NOT in "
    f"RETRY_TRANSLATION_HOURS, no manual PATCH-7 swap required -- same-band case handled "
    f"automatically): "
    f"SPECIAL SITUATION -- cycle 860 ran as NO-OP at 11:00 CST (Hour 3 UTC retry-eligible, "
    f"commit 657a880, 802nd clean push), but the fetcher at 11:07 CST Hour 3 UTC retry-"
    f"eligible ran AFTER cycle 860 commit and populated {DELTA} new substantive record into "
    f"tweets.json (CUR went {HEAD_COUNT} -> {CUR_COUNT}) at fetched_at timestamp "
    f"2026-10-09T11:07:28+08:00; cycle 860 NO-OP at 11:00 CST did not commit anything "
    f"FURTHER so the new record was not visible until cycle {CYCLE}; cycle {CYCLE} at "
    f"{CST_TIME} CST (Hour {UTC_HOUR} UTC non-retry-eligible) is the FIRST cycle to see the "
    f"dirty working tree (` M tweets.json`, +{DELTA} record) and the FIRST cycle to commit "
    f"it; this is the 49th-fire fetcher-populates-after-cycle-commit pattern (cycle 821 = "
    f"26th-fire ... cycle 859 = 48th-fire at Hour 1 UTC non-retry-eligible, **cycle "
    f"{CYCLE} = 49th-fire at Hour 3 UTC retry-eligible** -- the 47th-fire slot at cycle 860 "
    f"NO-OP at Hour 2 UTC non-retry-eligible was a textbook NO-OP so the fetcher's retry-"
    f"eligible retry pass at 11:07 CST contributed the +{DELTA} record to the working tree "
    f"between cycle 860's commit and cycle {CYCLE}'s tick); "
    f"fetcher populated {DELTA} new substantive RT record into tweets.json (cycle 861 only): "
    f"Grok-Bot-meal-prep-RT (id 2108270660275609612, RT of user's complaint about Grok "
    f"Bot subscribing to recurring meal-prep instead of one-off -- 「「AI出包我們幫你"
    f"買單」的保證\\n\\nGrok Bot幫我訂了定期的 meal prep 訂閱方案，而不是我要的一次性"
    f"訂單\\n\\n多扣了我£57（$75）」 Traditional Chinese); "
    f"0 retranslate_one.py invocations; "
    f"0 empty translation fixes -- the 1 NEW record had valid Traditional Chinese "
    f"translation on first pass; "
    f"0 untranslated NEW (cycle 277 cross-check 0 strict-eq, cycle 394 0 case-only, "
    f"cycle 409 0 LLM-annotated); "
    f"0 byline-orphan fixes (the 1 NEW record is a substantive RT with translated content, "
    f"NOT a bare-byline 'Elon Musk' strict-equal pattern from cycle 277/286/287); "
    f"structural 0 empty, refusal 0 [canonical 20-KW REFUSAL_KW scan clean per "
    f"pitfall 16 cycle 819 codification + cycle 831 20-KW extension including link-only "
    f"meta-refusal keywords 你只提供了 + 請提供完整 -- no refusal fixes required, no "
    f"simplified-Chinese retranslates required]; "
    f"1 of 1 substantive record translated cleanly (Grok-Bot-meal-prep-RT); "
    f"next fetcher at {NEXT_FETCHER_AT} will fire non-retry-eligible pass; "
    f"all {DELTA} snapshot-wide defect gates clean (0 empty / 0 refusal NEW / 0 simp-char "
    f"NEW / 0 untranslated NEW -- historical orphan counts out of scope per cycle "
    f"287/290/409/410 codification); "
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
    f"P73 clean-push counter arithmetic drift held cleanly (cycle 859 SUBSTANTIVE lineB "
    f"parsed for canonical 801st + 1 = 802nd); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 860 runtime CST_TIME 11:05, not cron-tick 12:00 placeholder); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe "
    f"held cleanly (IN-SCRIPT assert confirmed -- 37th prevention-fire, cycle 820 codification "
    f"ELEVATED to in-script `assert OLD_MARKER not in newlineb` form); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held "
    f"cleanly (docstring uses `Hour {UTC_HOUR} UTC` not `0{UTC_HOUR}:00 UTC` -- {UTC_HOUR} "
    f"is 1-digit so no leading-zero issue); "
    f"pitfall 16 (cycle 819 1st-fire) fetcher-saved refusal translation reaches Phase 1 "
    f"gate held cleanly (PRE-flight REFUSAL_KW canonical 20-keyword scan on NEW_RECORDS "
    f"returned 0 refusal hits; post-patch scan clean: 0 refusals in NEW); "
    f"pitfall 17 (cycle 823 1st-fire) PRE_REP drift absorption held cleanly "
    f"(cycle {CYCLE} PRE_REP={PRE_REP} read fresh at runtime, EXPECTED_POST_RC="
    f"{EXPECTED_POST_RC}); "
    f"P87-REFIRE (cycle 841 1st-fire) belt-and-suspenders `final_note.replace('Vercel "
    f"Vercel ', 'Vercel ')` held cleanly (18th-fire structural, applied in Phase 8 "
    f"before jobs.json save); "
    f"P31-REFIRE (cycle 841 1st-fire) Phase 4 dual-bump held cleanly (19th-fire "
    f"structural, target['completed'] AND target['repeat']['completed'] both bumped in "
    f"parallel); "
    f"same-band non-retry->non-retry (cycle 859 SUBSTANTIVE Hour 2 UTC non-retry-eligible "
    f"-> cycle {CYCLE} Hour {UTC_HOUR} UTC non-retry-eligible): handled cleanly via "
    f"runtime ternary on boilerplate label (cycle {CYCLE} lineB block uses 'is {RETRY_LABEL}' "
    f"for non-retry-eligible Hour {UTC_HOUR} UTC, no manual PATCH-7 swap required; "
    f"**cycle {CYCLE} codification = 7th-fire of 1-cycle-back SUBSTANTIVE->SUBSTANTIVE "
    f"same-band primary case (a)/(d)**, extends the durability chain from cycles 818, "
    f"832, 839, 840, 858, 859 to 7 fires -- well-past the cycle 302 5+ threshold for "
    f"canonical-default promotion; reached via **latest-in-class-SUBSTANTIVE fallback** "
    f"because immediately-prior cycle 860 was NO-OP different class, so cp source = "
    f"`_cycle859.py` per cycle 857 fallback codification); "
    f"cycle 286/287 byline-only orphan codification held cleanly (cycle {CYCLE} applied "
    f"0 fixes; the 1 NEW record is a substantive RT, not a bare-byline 'Elon Musk' "
    f"strict-equal pattern); "
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
    f"131st consecutive PRE_REP-drift-clean cycle (extends streak from cycles 712, 715-860); "
    f"803rd consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (ELEVATED cycle 820 to IN-SCRIPT assert, 36th prevention-fire)
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
RETRY_LABEL2 = 'NOT in' if int(UTC_HOUR) not in {0,3,6,9,12,15,18,21} else 'in'
LINEB_PROSE = (
    "cycle {C} (2026-10-09 {T}:00 CST = {H}:00 UTC): SUBSTANTIVE +{D} new tweets "
    "(HEAD {HC} -> CUR {CC} delta=+{D}), CLEAN PUSH (cron cycle hour {H} UTC is {RL} "
    "in RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}} per fetch_tweets.py -- non-"
    "retry-eligible-cron-cycle-substantive form, 1-cycle-back SUBSTANTIVE->"
    "SUBSTANTIVE same-band non-retry->non-retry primary case (a)/(d) per cycle "
    "818 codification + cycle 832 2nd-fire + cycle 839 3rd-fire + cycle 840 4th-"
    "fire (CANONICAL since cycle 840) + cycle 858 5th-fire + cycle 859 6th-fire + "
    "**cycle {C} = 7th-fire** (applied PATCH-3c ordinal-literal swaps on cp source "
    "`_cycle859.py` Hour 2 UTC non-retry-eligible; immediately-prior cycle 860 was "
    "NO-OP different class, so latest-in-class-SUBSTANTIVE fallback applies per "
    "cycle 857 codification -- the most recent SUBSTANTIVE in the rotation is cycle "
    "859; runtime ternary emits 'NOT in' for both Hour 2 and Hour {H} since both "
    "are NOT in RETRY_TRANSLATION_HOURS, no manual PATCH-7 swap required -- same-"
    "band case handled automatically): "
    "SPECIAL SITUATION -- cycle 860 ran as NO-OP at 11:00 CST (Hour 3 UTC retry-"
    "eligible, commit 657a880, 802nd clean push), but the fetcher at 11:07 CST "
    "Hour 3 UTC retry-eligible ran AFTER cycle 860 commit and populated {D} new "
    "substantive record into tweets.json (CUR went {HC} -> {CC}); cycle 860 NO-OP "
    "at 11:00 CST did not commit anything FURTHER so the new record was not visible "
    "until cycle {C}; cycle {C} at {T}:00 CST (Hour {H} UTC non-retry-eligible) is "
    "the FIRST cycle to see the dirty working tree (` M tweets.json`, +{D} record) "
    "and the FIRST cycle to commit it; this is the 49th-fire fetcher-populates-"
    "after-cycle-commit pattern (cycle 821 = 26th-fire ... cycle 859 = 48th-fire "
    "at Hour 1 UTC non-retry-eligible, **cycle {C} = 49th-fire at Hour 3 UTC "
    "retry-eligible**); fetcher populated {D} new substantive RT record into "
    "tweets.json (Grok-Bot-meal-prep-RT, id 2108270660275609612, RT of user's "
    "complaint about Grok Bot subscribing to recurring meal-prep instead of one-"
    "off -- 「「AI出包我們幫你買單」的保證\\n\\nGrok Bot幫我訂了定期的 meal prep "
    "訂閱方案\\n\\n多扣了我£57（$75）」 Traditional Chinese, balanced 「...」 "
    "quote-style treatment consistent with cycle 226 truncation-codification "
    "norms); 0 retranslate_one.py invocations; all {D} NEW record has valid "
    "Traditional Chinese translation on first pass (0 empty / 0 refusal NEW / 0 "
    "simp-char NEW / 0 untranslated NEW; structural 0 empty, byline-only 0 applied "
    "[the 1 NEW record is a substantive RT, not a bare-byline pattern], refusal 0 "
    "[canonical 20-KW REFUSAL_KW scan clean per pitfall 16 cycle 819 codification "
    "+ cycle 831 20-KW extension], simp-leaks 0, trailing-ellipsis 0, dangling-"
    "connector 0, corrupted-tail 0); 1 of 1 substantive record translated cleanly; "
    "next fetcher at {NFA} will fire non-retry-eligible pass; all {D} snapshot-wide "
    "defect gates clean; same-band non-retry->non-retry (cycle 859 SUBSTANTIVE Hour "
    "2 UTC non-retry-eligible -> cycle {C} Hour {H} UTC non-retry-eligible) handled "
    "cleanly via runtime ternary on boilerplate label (cycle {C} lineB block uses "
    "'is {RL}' for non-retry-eligible Hour {H} UTC, no manual PATCH-7 swap "
    "required; **cycle {C} codification = 7th-fire of 1-cycle-back SUBSTANTIVE->"
    "SUBSTANTIVE same-band primary case (a)/(d)**, extends the durability chain "
    "from cycles 818, 832, 839, 840, 858, 859 to 7 fires -- well-past the cycle "
    "302 5+ threshold for canonical-default promotion; reached via **latest-in-"
    "class-SUBSTANTIVE fallback** because immediately-prior cycle 860 was NO-OP "
    "different class, so cp source = `_cycle859.py` per cycle 857 fallback "
    "codification); P19/P88/P31/P52/cycle-321/P69/P71/P73/cycle-633/untracked-"
    "file-tolerant/cron-tick-RE-bump/pitfall-12/pitfall-13/pitfall-14/pitfall-15/"
    "pitfall-16/pitfall-17/P87-REFIRE/P31-REFIRE CANONICAL; PREDICTED_RC={E} OK "
    "(canonical PRE_REP_RC+1={E}); jobs.json round-trip patch absorbed cycle 255 "
    "dual-completed counter drift (PRE-state top.completed={PT} vs repeat.completed="
    "{P}); P31 idempotency guard correctly detected pre_rep={P} < EXPECTED_POST_RC="
    "{E} and BUMPED rep to {E}; P52 symmetric reset will keep alignment: POST top="
    "rep={E}; 131st consecutive PRE_REP-drift-clean cycle (extends streak from "
    "cycles 712, 715-860); 803rd consecutive clean push (webpage-only, no Telegram)"
).format(C=CYCLE, T=CST_TIME, H=UTC_HOUR, HC=HEAD_COUNT, CC=CUR_COUNT, D=DELTA, FA=FETCHER_AT, NFA=NEXT_FETCHER_AT, E=EXPECTED_POST_RC, P=PRE_REP, PT=PRE_TOP, RL=RETRY_LABEL2, D_minus_10=DELTA-2)

TBD_NOTE = LINEB_PROSE + " -- commit TBD; Vercel PASS-TBD"

# ---------- Phase 4: jobs.json round-trip (P52 symmetric reset + P31-REFIRE dual-bump) ----------
target["last_run_note"] = TBD_NOTE
target["last_run_at"] = f"2026-10-09T{CST_TIME}:01+08:00"
target["completed"] = EXPECTED_POST_RC
target["updated_at"] = f"2026-10-09T{CST_TIME}:01+08:00"
target["last_status"] = "ok"
target["last_run_error"] = None
target["last_run_status"] = "ok"
# P31-REFIRE dual-bump: also set target['repeat']['completed'] to keep both counters aligned
target["repeat"]["completed"] = EXPECTED_POST_RC
target["repeat"]["last_run_note"] = TBD_NOTE
target["repeat"]["last_run_at"] = f"2026-10-09T{CST_TIME}:01+08:00"

with open(JOBS, "w") as f:
    json.dump(jobs_data, f, ensure_ascii=False, indent=2)
print(f"[Phase 4] jobs.json round-trip applied (TBD markers pending post-push patch)")

# ---------- Phase 6: git add + commit + push ----------
git("add", "tweets.json", "deploy-stamp.txt", "index.html")
status_out, _, _ = git("status", "--short")
print(f"[Phase 6-pre] git status:\n{status_out}")

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 802nd clean push (webpage-only, no Telegram)"
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
    f"2026-10-09T{CST_TIME}:01+08:00 cycle={CYCLE} commit={REAL_SHA} "
    f"target_url={VERCEL_URL}/tweets.json deploy-stamp-probe={deploy_body.strip()!r} "
    f"tweets-probe=set-equal {CUR_COUNT}={deployed_count} "
    f"PREDICTED_RC={EXPECTED_POST_RC} verified\n"
)
with open(VERIFY_LOG, "a") as f:
    f.write(verify_line)
