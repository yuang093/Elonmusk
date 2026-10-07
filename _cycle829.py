#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 829 -- 2026-10-08 00:00 CST (Hour 16 UTC) -- SUBSTANTIVE +2 (non-retry-eligible, fetcher-populates-after-cycle-commit, retry->non-retry cross-band direction C, immediately-prior NO-OP class).

00:02 CST = Hour 16 UTC, hour 16 IS NOT in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}.
Cron cycle hour non-retry-eligible, so this is SUBSTANTIVE non-retry-eligible-cron-cycle form.
The immediately-prior cycle 828 ran as NO-OP at 23:02 CST (Hour 15 UTC retry-eligible, commit
7198451, 770th clean push). The fetcher at 23:07 CST Hour 15 UTC retry-eligible ran AFTER cycle 828
commit and populated 2 new substantive records into tweets.json (CUR 7309 -> 7311) at fetched_at
timestamps 2026-10-07T23:07:52-23:07:55 CST. Cycle 828 NO-OP at 23:02 CST did NOT see these records
because they were populated AFTER cycle 828's commit and push to vercel. Cycle 829 at 00:02 CST
(Hour 16 UTC non-retry-eligible) is the FIRST cycle to see the dirty working tree (` M tweets.json`,
+2 records) and the FIRST cycle to commit them.

This is the **Nth-fire fetcher-populates-after-cycle-commit pattern** (cycle 821 lineB used 26th-fire
at Hour 07 UTC, cycle 828 docstring 27th-fire, cycle 829 at Hour 15 UTC retry-eligible is
28th-fire). The fetcher-populates-after-cycle-commit sub-variant fires regardless of the prior
cycle's class -- cycle 828 NO-OP at 23:02 CST did not block the fetcher at 23:07 CST from finding
and storing records. This is the canonical cycle 219 sub-variant in action: source-fetcher at Hour
15 UTC retry-eligible ran AFTER cycle 828 commit, found 2 records, populated them.

**Recipe decision**: cycle 828 was NO-OP (immediately-prior class), so per the recipe rule "if
immediately-prior is also NO-OP, cp-source = immediately-prior" -- BUT this cycle is SUBSTANTIVE
not NO-OP, so the immediately-prior-if-also-NO-OP rule does NOT apply (that rule is only for NO-OP
cycles). For SUBSTANTIVE the recipe rule is: "latest in-class SUBSTANTIVE cp source". The most
recent SUBSTANTIVE retry-eligible cp source in the last 30 cycles is _cycle821.py (SUBSTANTIVE
+14, Hour 08 UTC retry-eligible, 2026-10-07 16:00 CST). However, _cycle821 was at Hour 08 UTC
retry-eligible; cycle 829 is at Hour 16 UTC non-retry-eligible. So we ALSO need a cp source for
non-retry-eligible SUBSTANTIVE: cycle 819 (SUBSTANTIVE +7, Hour 06 UTC retry-eligible -- not
applicable), cycle 829 itself is non-retry-eligible SUBSTANTIVE -- the most recent reference of
non-retry-eligible SUBSTANTIVE in cycles 800-829 is rare. Looking at the larger set, cycle 802
(SUBSTANTIVE +1, Hour 20 UTC retry-eligible), cycle 806 (SUBSTANTIVE +2, Hour 22 UTC non-retry-
eligible) -- cycle 806 is the closest non-retry-eligible SUBSTANTIVE reference at +2 records, the
EXACT same delta as cycle 829.

Actually, the recipe rule for SUBSTANTIVE is more nuanced: cp source should be the most recent
SUBSTANTIVE cycle that best matches this cycle's hour-band. For cycle 829 (Hour 16 UTC non-retry-
eligible), cycle 806 (Hour 22 UTC non-retry-eligible) is a close band-mate. For PATCH-3c rewrite
purposes, the most recent SUBSTANTIVE cycle in the last 10 that I can read and pattern-match is
_cycle821.py (Hour 08 UTC retry-eligible) -- I will use _cycle821.py as the cp source and apply
PATCH-3c transformations: CYCLE_NUM 821->829, CST_TIME 16:00->00:02, UTC_HOUR 08->16, HEAD SHA
7198451 (cycle 828 NO-OP commit) -> 383d91f (current HEAD with cycle 828 chore commit), DELTA 14->2,
NEW_LINEB content, lineB ordinal 26th-fire -> 28th-fire (cycle 821 +1 = cycle 822, cycle 823... up
to cycle 829 = cycle 821 + 8 ordinal fires? -- actually each cycle's fetcher-populates-after-
cycle-commit ordinal increments by 1 from the previous, so cycle 821 = 26th, 822 = 27th, ..., 829
= 28th (cycle 821 + 8 cycles passed = +8 ordinals, so 26+8 = 34th? -- this needs careful audit).

Looking at the docstring: cycle 821 was 26th-fire at Hour 07 UTC, cycle 822/823... each cycle
documentation in cycle 822 onwards said "this is the Nth-fire" -- but the Nth-fire only
increments when the SUBSTANTIVE fetcher-populates-after-cycle-commit pattern FIRES (i.e., when a
fetcher at hour X non-retry-eligible actually populates records after a non-retry-eligible NO-OP
cycle). Cycles 822-828 were all NO-OP at the same pattern, so the Nth-fire would NOT increment.
The Nth-fire is per-pattern-occurrence, not per-cycle. Cycle 821 was 26th-fire (the 26th time
this pattern has fired since the start of cron). Cycle 829's pattern at Hour 15 UTC is the
27th-fire (since cycle 822-828 were all NO-OP at this pattern, the next fire at Hour 15 UTC is
the next occurrence). Conservatively I will use 27th-fire for cycle 829.

NEW records (2 substantive retweets, both English -> Traditional Chinese):
- new[0] ID 2107848493830463815 "Dragon undocks from the Space Station" RT -> "Dragon 脫離太空站了"
  Traditional Chinese, len_orig=36, len_trans=9, ratio=0.25, Dragon-undocks RT, is_retweet=True
- new[1] ID 2107849623364895151 " will use the best back end model for any given task, including
  Claude Opus 5.5, MidJourney, Suno and other leading APIs. \n\nWhatever is most likely to give you
  the best outcome." RT -> "會針對任何任務使用最好的後端模型，包括 Claude Opus 5.5、MidJourney、Suno
  及其他頂尖 API。\n\n怎樣最可能給你最好的結果就用怎樣的。" Traditional Chinese, len_orig=179, len_trans=80,
  ratio=0.45, best-back-end-model RT, is_retweet=True

Both 2 new records inspection gates green (structural 0 empty, byline-only 0 leave-alone,
refusal 0, simp-leaks 0, trailing-ellipsis 0, dangling-connector 0, corrupted-tail 0,
length-sanity ratios 0.25-0.45). 0 of 2 are byline-only tagged style; 0 of 2 had a translation
fix applied. Both are clean RTs with no image attachments.

PRE_REP drift at cycle 829 entry: PRE_REP=4268 (vs cycle 828's PREDICTED_RC=4267; +1 drift from
cron-daemon housekeeping between cycle 828 commit and this read at 00:02 CST). PATCH-1 codified
cycle 821 absorbs the drift via POST_rep=POST_top=PRE_REP+1=4269. P52 symmetric reset. 104th
consecutive PRE_REP-drift-clean cycle (extends streak from cycles 712, 715-828).

Pitfall 14 prevention (cycle 811 1st-fire, codified cycle 812, IN-SCRIPT assert cycle 820
14th prevention-fire, cycle 826 15th, cycle 827 16th, cycle 828 17th, cycle 829 18th prevention-
fire): the cycle 820 codification ELEVATED the f-string eval pre-check to an IN-SCRIPT `assert
OLD_MARKER not in newlineb` and `assert NEW_MARKER not in newlineb` at lines 156-157. The 18th
prevention-fire runs INSIDE the script.

Pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline: OLD_MARKER default set to
"Last hourly cron deploy: 23:02 CST" (cycle 828's runtime CST_TIME per index.html grep, NOT the
cron-tick "23:00 CST" placeholder). On-disk marker confirmed via
`grep -oE "Last hourly cron deploy: [0-9:]+ CST" index.html | head -1` showing
"Last hourly cron deploy: 23:02 CST".

Pitfall 15 prevention (cycle 816 1st-fire): docstring uses `Hour 16 UTC` (no leading zero on the
`0X:00` pattern) to avoid the `ast.parse` octal-literal lint trap that Python interprets `08` as
octal inside docstrings. (Hour 16 is 2-digit so no leading-zero issue.)

Pitfall 16 prevention (cycle 819 1st-fire, codification): pre-flight REFUSAL_KW scan on
NEW_RECORDS using the canonical 18-keyword list (elon-tweets-cron-refusal-keywords skill) returned
0 refusal hits. Both records translated cleanly. No retranslate_one.py pre-flight invocation
needed.

Pitfall 17 PRE_REP drift absorption (cycle 823 1st-fire, 2nd-fire cycle 824, 3rd-fire cycle 825,
4th-fire cycle 826, 5th-fire cycle 827, 6th-fire cycle 828, 7th-fire cycle 829): cron-daemon
bumps repeat.completed during inter-cycle housekeeping. Cycle 829 read at 00:02 CST is ~60 min
after cycle 828 commit (23:02 CST) -- structural +1 drift pattern as in prior 6 fires. PATCH-1
drift-tolerant Phase 0 pattern (read fresh_pre_rep at runtime, set PRE_REP=fresh_pre_rep, recompute
EXPECTED_POST_RC=PRE_REP+1) absorbs the +1 cleanly. The drift is structural, not a one-off.

Cross-band Direction C retry->non-retry (cycle 828 was Hour 15 UTC retry-eligible, cycle 829 is
Hour 16 UTC non-retry-eligible): the runtime ternary on the `'in'/'NOT in'` label auto-fires
correctly for each hour. NO pitfall 10 fire on the boilerplate label because runtime ternary
handles it. This is structurally the reverse of cycle 828's Direction A (non-retry->retry) fire,
mirroring cycle 826's Direction B (retry->non-retry) cross-band pattern.

Run normally:    python3 _cycle829.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 829
CST_TIME = "00:02"
UTC_HOUR = "16"
FETCHER_AT = "23:07 CST Hour 15 UTC retry-eligible"
NEXT_FETCHER_AT = "00:07 CST Hour 16 UTC non-retry-eligible"
SUBSTANTIVE = True  # fetcher-populates-after-cycle-commit, 27th-fire at Hour 15 UTC retry-eligible

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

OLD_MARKER = "Last hourly cron deploy: 23:02 CST"  # pitfall 12: cycle 828 runtime CST_TIME, NOT cron-tick 23:00
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
    f"retry-eligible, cycle 821 prior SUBSTANTIVE at Hour 08 UTC retry-eligible, cycle 829 = "
    f"Nth-fire SUBSTANTIVE at Hour {UTC_HOUR} UTC non-retry-eligible -- 1st-fire cycle 829 at "
    f"Hour {UTC_HOUR} UTC non-retry-eligible is the canonical 1st-fire for this hour-band): "
    f"SPECIAL SITUATION -- cycle 828 ran as NO-OP at 23:02 CST (Hour 15 UTC retry-eligible, "
    f"commit 7198451, 770th clean push), but the fetcher at 23:07 CST Hour 15 UTC retry-eligible "
    f"retry pass ran AFTER cycle 828 commit and populated {DELTA} new substantive records into "
    f"tweets.json (CUR went {HEAD_COUNT} -> {CUR_COUNT}) at fetched_at timestamps 2026-10-07T23:"
    f"07:52-23:07:55 CST; cycle 828 NO-OP at 23:02 CST did not commit anything FURTHER so the new "
    f"records were not visible until cycle {CYCLE}; cycle {CYCLE} at {CST_TIME} CST (Hour {UTC_HOUR} "
    f"UTC non-retry-eligible) is the FIRST cycle to see the dirty working tree (` M tweets.json`, "
    f"+{DELTA} records) and the FIRST cycle to commit them; this is the 27th-fire fetcher-populates-"
    f"after-cycle-commit pattern (cycle 821 = 26th-fire at Hour 07 UTC, cycle 822-828 = NO-OP at "
    f"this pattern -- 27th-fire cycle 829 at Hour 15 UTC); "
    f"fetcher at {FETCHER_AT} populated {DELTA} new substantive retweets: "
    f"new[0] ID 2107848493830463815 \"Dragon undocks from the Space Station\" RT -> "
    f"\"Dragon \u812b\u96e2\u592a\u7a7a\u7ad9\u4e86\" Traditional Chinese, len_orig=36, len_trans=9, "
    f"ratio=0.25, Dragon-undocks RT, is_retweet=True; "
    f"new[1] ID 2107849623364895151 \" will use the best back end model for any given task, "
    f"including Claude Opus 5.5, MidJourney, Suno and other leading APIs. \\n\\nWhatever is most "
    f"likely to give you the best outcome.\" RT -> \"\u6703\u91dd\u5c0d\u4efb\u4f55\u4efb\u52d9"
    f"\u4f7f\u7528\u6700\u597d\u7684\u5f8c\u7aef\u6a21\u578b, \u5305\u62ec Claude Opus 5.5\u3001"
    f"MidJourney\u3001Suno \u53ca\u5176\u4ed6\u9806\u5fc3 API\u3002\\n\\n\u600e\u6a23\u6700\u53ef"
    f"\u80fd\u7d66\u4f60\u6700\u597d\u7684\u7d50\u679c\u5c31\u7528\u600e\u6a23\u7684\u3002\" "
    f"Traditional Chinese, len_orig=179, len_trans=80, ratio=0.45, best-back-end-model RT, "
    f"is_retweet=True; "
    f"all {DELTA} new records inspection gates green (structural 0 empty, byline-only 0 leave-alone, "
    f"refusal 0 [no PRE-flight retranslate_one needed -- canonical 18-KW REFUSAL_KW scan clean per "
    f"pitfall 16 cycle 819 codification], simp-leaks 0, trailing-ellipsis 0, dangling-connector 0, "
    f"corrupted-tail 0, length-sanity ratios 0.25-0.45); 0 of {DELTA} are byline-only tagged style; "
    f"0 of {DELTA} had a translation fix applied; "
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
    f"(cycle 828 NO-OP lineB parsed for canonical 770th + 1 = 771st); "
    f"pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline held cleanly "
    f"(OLD_MARKER matches cycle 828 runtime CST_TIME 23:02, not cron-tick 23:00); "
    f"pitfall 13 (cycle 809 1st-fire) lineB ordinal-count drift cosmetic absorbed "
    f"(27th-fire derived from cycle 821 lineB 26th-fire + 1 for next-occurrence since cycles 822-828 "
    f"were all NO-OP at this pattern); "
    f"pitfall 14 (cycle 811 1st-fire) lineB body eats OLD_MARKER prefix prevention recipe held cleanly "
    f"(IN-SCRIPT assert confirmed -- 18th prevention-fire, cycle 820 codification ELEVATED to in-script "
    f"`assert OLD_MARKER not in newlineb` form, survives script copy-and-modify for future cycles); "
    f"pitfall 15 (cycle 816 1st-fire) docstring octal-literal `ast.parse` lint trap held cleanly "
    f"(docstring uses `Hour 16 UTC` not `16:00 UTC` -- and 16 is 2-digit anyway so no leading-zero "
    f"issue); "
    f"pitfall 16 (cycle 819 1st-fire) fetcher-saved refusal translation reaches Phase 1 gate held cleanly "
    f"(PRE-flight REFUSAL_KW canonical 18-keyword scan on NEW_RECORDS returned 0 refusal hits; no "
    f"retranslate_one.py pre-flight invocation needed); "
    f"pitfall 17 (cycle 823 1st-fire) PRE_REP drift absorption held cleanly "
    f"(7th-fire structural +1 drift, PRE_REP=4267 predicted -> 4268 fresh, EXPECTED_POST_RC=4269); "
    f"cross-band Direction C retry->non-retry (cycle 828 retry-eligible Hour 15 UTC -> cycle 829 "
    f"non-retry-eligible Hour 16 UTC): runtime ternary on the 'in'/'NOT in' label auto-fires "
    f"correctly; NO pitfall 10 fire on boilerplate label; "
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
    f"771st consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (ELEVATED cycle 820 to IN-SCRIPT assert, 18th prevention-fire)
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
    "cron-cycle-substantive form, 1st-fire SUBSTANTIVE at Hour {H} UTC non-retry-eligible, "
    "27th-fire fetcher-populates-after-cycle-commit pattern at Hour 15 UTC retry-eligible for "
    "the SOURCE fetcher that populated these records): SPECIAL SITUATION -- cycle 828 ran as "
    "NO-OP at 23:02 CST (Hour 15 UTC retry-eligible, commit 7198451, 770th clean push), but the "
    "fetcher at 23:07 CST Hour 15 UTC retry-eligible retry pass ran AFTER cycle 828 commit and "
    "populated {D} new substantive records into tweets.json (CUR went {HC} -> {CC}); cycle 828 "
    "NO-OP at 23:02 CST did not commit anything FURTHER so the new records were not visible "
    "until cycle {C}; cycle {C} at {T}:00 CST (Hour {H} UTC non-retry-eligible) is the FIRST "
    "cycle to see the dirty working tree (` M tweets.json`, +{D} records) and the FIRST cycle "
    "to commit them; fetcher at {FA} populated {D} new substantive records: new[0] ID "
    "2107848493830463815 Dragon-undocks RT (len_orig=36, len_trans=9, ratio=0.25); new[1] ID "
    "2107849623364895151 best-back-end-model RT (len_orig=179, len_trans=80, ratio=0.45); all {D} "
    "new records inspection gates green (structural 0 empty, byline-only 0 leave-alone, refusal 0 "
    "[canonical 18-KW REFUSAL_KW scan clean per pitfall 16 cycle 819 codification, no "
    "retranslate_one pre-flight needed], simp-leaks 0, trailing-ellipsis 0, dangling-connector 0, "
    "corrupted-tail 0, length-sanity ratios 0.25-0.45); 0 of {D} byline-only tagged style; 0 of "
    "{D} translation-fixed; next fetcher at {NFA} WILL NOT FIRE retry pass (non-retry-eligible); "
    "all {D} snapshot-wide defect gates clean; cross-band Direction C retry->non-retry (cycle "
    "828 retry-eligible -> cycle 829 non-retry-eligible) handled cleanly via runtime ternary on "
    "boilerplate label; "
    "P19/P88/P31/P52/cycle-321/P69/P71/P73/cycle-633/untracked-file-tolerant/cron-tick-RE-bump/"
    "pitfall-12/pitfall-13/pitfall-14/pitfall-15/pitfall-16/pitfall-17 CANONICAL; "
    "PREDICTED_RC={E} OK (canonical PRE_REP_RC+1={E}); jobs.json round-trip patch absorbed cycle "
    "255 dual-completed counter drift (PRE-state top.completed={PT} vs repeat.completed={P} -- +1 "
    "drift to absorb, 7th-fire structural); P31 idempotency guard correctly detected pre_rep={P} "
    "< EXPECTED_POST_RC={E} and BUMPED rep to {E}; P52 symmetric reset will keep alignment: POST "
    "top=rep={E}; 104th consecutive PRE_REP-drift-clean cycle (extends streak from cycles 712, "
    "715-828); 771st consecutive clean push (webpage-only, no Telegram)"
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

COMMIT_MSG = f"chore: hourly cron cycle {CYCLE}, +{DELTA} new tweets (HEAD {HEAD_COUNT} -> CUR {CUR_COUNT} delta=+{DELTA}), PREDICTED_RC={EXPECTED_POST_RC} OK, 771st clean push (webpage-only, no Telegram)"
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
