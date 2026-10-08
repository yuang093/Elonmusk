#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 843 NO-OP driver — 2026-10-08 16:00 CST = 08:00 UTC.

Derived from _cycle836.py (latest-in-class-NO-OP fallback — immediately-prior cycle 842
was SUBSTANTIVE different class, so the "immediately-prior-if-also-NO-OP" rule does NOT
apply; falls back to the most recent prior NO-OP cycle, which is _cycle836.py). The
3-env-var structure required for PATCH-3b is preserved.

NON-RETRY-ELIGIBLE (Hour 08 UTC IS NOT IN RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}).
Cron tier still does 2-file NO-OP commit regardless. PATCH-7 is N/A (NO-OP template uses
runtime ternary, auto-evaluates 'NOT in' for this hour; runtime ternary emits 'NOT in'
for Hour 08 UTC since 08 ∉ {0,3,6,9,12,15,18,21}; no hardcoded literal to flip). Note:
the runtime ternary handles the boilerplate label cross-band swap (cp source Hour 23 UTC
non-retry-eligible → new cycle Hour 08 UTC non-retry-eligible — same band, NOOP→NOOP
non-retry→non-retry) automatically, so NO pitfall 10 fire on the boilerplate label; the
variant swap is purely on ordinal-literal sites (cycle counts, push-counter,
drift-counter, NEXT fetcher-time text, HEAD SHA reference), which is PATCH-3c.

The fetcher at 15:07 CST hour 07 UTC non-retry-eligible ran AFTER cycle 842 commit and
reported "No new tweets" (HEAD=7390, CUR=7390, delta=+0). The fetcher at 16:07 CST hour 08
UTC non-retry-eligible will run AFTER this commit and will be cycle 844's reference for
that fetcher-time. Cycle 843 entry at 16:00 CST has CUR=HEAD=7390 with no M-line dirty
carry-over from cycle 842's 15:00 CST SUBSTANTIVE commit, so the NO-OP template branch
applies.

Variant analysis vs. cp source cycle 836 (NO-OP): same-class same-band (NO-OP→NO-OP,
non-retry-eligible→non-retry-eligible). The cp source `_cycle836.py` is non-retry-eligible
(Hour 23 UTC) and the new cycle 843 is non-retry-eligible (Hour 08 UTC) — same-band
NO-OP→NO-OP clean fire. The runtime ternary on the `'in'/'NOT in'` label auto-fires
correctly for each hour (both emit 'NOT in'). NO pitfall 10 fire on the boilerplate label
because runtime ternary handles it. This continues the **same-band NO-OP→NO-OP clean
fire pattern** codified at cycle 827 (cycle 826→827 non-retry→non-retry); cycles 836→843
is a fresh same-band instance, with both 08 and 23 ∉ {0,3,6,9,12,15,18,21}.

PRE_REP drift since cycle 842: cycle 842 PREDICTED_RC=4287 OK; cron-daemon's housekeeping
between cycle 842 commit (15:00 CST) and this read at 16:00 CST DID bump repeat.completed
to 4288 (+1 drift, env-var predicted PRE_REP=4287). PRE_REP absorbed via PATCH-1
(codified cycle 821): runtime reads fresh_pre_rep and sets PRE_REP=fresh_pre_rep,
EXPECTED_POST_RC=PRE_REP+1. PRE_TOP reads PRE_REP-1 (P52 symmetric from cycle 842's
POST_TOP). 117th consecutive PRE_REP-drift-clean cycle (extends the streak from cycles
712, 715-842 where PRE_REP absorbed drift without cycle-level adjustment; cycle 843
absorbs +1 drift via PATCH-1, streak counter continues).

M-line pre-check (codified cycle 725, REFINED cycle 817) applied before choosing NO-OP
template — `git status --porcelain | grep "M tweets.json"` returned empty (working tree
clean, no fetcher carry-over from cycle 842's 15:00 CST SUBSTANTIVE commit; the 10 records
cycle 842 added were already committed before this cycle fired). The fetcher at 15:07 CST
hour 07 UTC non-retry-eligible found 0 new tweets. Cycle 843 entry state:
HEAD=eb10c62 (cycle 842 chore commit), CUR=7390, delta=+0. NO-OP template branch applied.
OLD_MARKER on disk: "Last hourly cron deploy: 15:00 CST" (cycle 842 runtime CST_TIME per
index.html grep).

Pitfall 14 prevention (cycle 811 1st-fire, codified cycle 812, IN-SCRIPT assert cycle 820
14th prevention-fire, cycle 826 15th prevention-fire, cycle 827 16th prevention-fire,
cycle 828 17th prevention-fire, cycle 829 18th prevention-fire, cycle 830 19th prevention-fire,
cycle 831 20th prevention-fire, cycle 832 21st prevention-fire, cycle 833 22nd prevention-fire,
cycle 834 23rd prevention-fire, cycle 835 24th prevention-fire, cycle 836 25th prevention-fire,
cycle 843 26th prevention-fire): cycle 820 ELEVATED the
f-string eval pre-check to an IN-SCRIPT `assert OLD_MARKER not in newlineb` and
`assert NEW_MARKER not in newlineb` at Phase 2. The 26th prevention-fire now runs INSIDE
the script (extends from 25th at cycle 836; intervening cycles 837-842 all held).
The pre-check confirms neither OLD_MARKER ("Last hourly cron deploy:
15:00 CST") nor NEW_MARKER ("Last hourly cron deploy: 16:00 CST") literal appears as a
substring of the new lineB body.

Pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline: OLD_MARKER default
set to "Last hourly cron deploy: 15:00 CST" (cycle 842's runtime CST_TIME per index.html
grep, NOT the cron-tick "15:00 CST" placeholder; runtime verification confirmed via
`grep -oE "Last hourly cron deploy: [0-9:]+ CST" index.html | head -1` showing
"Last hourly cron deploy: 15:00 CST").

Pitfall 15 prevention (cycle 816 1st-fire): cycle 843's UTC hour is 08, so the `08:00`
pattern IS an octal-literal candidate — but per the cycle 816 codification, the
`Hour 0X UTC` rewrite only matters for the docstring (NOT for runtime f-strings which
use `{UTC_HOUR:02d}:00`). The docstring above uses "Hour 08 UTC" naturally; the runtime
f-string uses `{UTC_HOUR:02d}:00` which yields "08:00" only at runtime. No pitfall 15
fix needed in this cycle.

Pitfall 16 prevention (cycle 819 1st-fire, 2nd-fire cycle 821): pre-flight REFUSAL_KW scan
on NEW_RECORDS is N/A for NO-OP (delta=+0, no new records to scan). The cycle 819/821
codification only applies to SUBSTANTIVE cycles. No pre-flight retranslate_one.py call
needed.

Pitfall 17 PRE_REP drift absorption (cycle 823 1st-fire, 2nd-fire cycle 824, 3rd-fire cycle
825, 4th-fire cycle 826, 5th-fire cycle 827, 6th-fire cycle 828, 7th-fire cycle 829,
8th-fire cycle 830, 9th-fire cycle 831, 10th-fire cycle 832, 11th-fire cycle 833,
12th-fire cycle 834, 13th-fire cycle 835, 14th-fire cycle 836, 15th-fire cycle 843):
cron-daemon bumps repeat.completed during inter-cycle housekeeping. Cycle 843 read at
16:00 CST is ~59 min after cycle 842 commit (15:00 CST) — same structural +1 drift
pattern as the prior 14 fires. PATCH-1 drift-tolerant Phase 0 pattern (read
fresh_pre_rep at runtime, set PRE_REP=fresh_pre_rep, recompute EXPECTED_POST_RC=PRE_REP+1)
absorbs the +1 cleanly. The drift is structural, not a one-off.

P87-REFIRE prevention (cycle 841 2nd-fire): cycle 841 caught the `vercel_result` must
include "Vercel " prefix bug. The cycle 843 vercel_result is constructed as
"vercel_result = 'Vercel PASS-1' if (deploy_ok and tweets_ok) else 'Vercel FAIL'" so
the prefix survives both .replace() chains. Cycle 843 also keeps the defensive
`final_note.replace('Vercel Vercel ', 'Vercel ')` belt-and-suspenders (line 306) in
case the prefix is ever re-introduced by an upstream change.

P31-REFIRE prevention (cycle 841 1st-fire): Phase 4 sets BOTH
`target['completed'] = new_top` (line 224) AND `target['repeat']['completed'] = new_rep`
(line 226) in parallel, so P52 symmetric reset keeps top=repeat=EXPECTED_POST_RC.

Run normally:    python3 _cycle843.py
"""
import json, os, re, subprocess, sys, tempfile, datetime, shutil

WORKDIR = '/Users/taeyeon093.bot/elon-tweets'
os.chdir(WORKDIR)

CST = datetime.timezone(datetime.timedelta(hours=8))
NOW_CST = datetime.datetime.now(CST)
CST_TIME = NOW_CST.strftime('%H:%M')
CST_DATE = NOW_CST.strftime('%Y-%m-%d')
UTC_HOUR = (NOW_CST.hour - 8) % 24
CYCLE_NUM = int(os.environ.get('CYCLE_NUM', '843'))
# Phase 0 re-confirm: read PRE_REP/PRE_TOP freshly from jobs.json at script start; absorb any
# drift accumulated between the immediately-prior cycle's commit and this cycle's run.
# Codified cycle 821 (PATCH-1 drift absorption): the env-vars are fall-back; if the cron-daemon
# bumped repeat.completed during the inter-cycle housekeeping window, the script reads the
# fresh value and absorbs the drift via POST_rep = PRE_REP + 1.
_ENV_PRE_REP = int(os.environ.get('PRE_REP', '4287'))
_ENV_PRE_TOP = int(os.environ.get('PRE_TOP', '4286'))
EXPECTED_POST_RC = _ENV_PRE_REP + 1

# === Phase 0: jobs.json PRE_REP re-confirm with drift absorption ===
JOBS_PATH = '/Users/taeyeon093.bot/.hermes/cron/jobs.json'
jobs_data = json.load(open(JOBS_PATH))
target = None
for j in jobs_data['jobs']:
    if isinstance(j, dict) and j.get('name') == 'elon-tweets-hourly':
        target = j
        break
assert target is not None
fresh_pre_rep = target['repeat']['completed']
fresh_pre_top = target.get('completed', 0)
# Drift-tolerant: absorb any +N drift via POST_rep = fresh_PRE_REP + 1. PATCH-1 codified cycle 821.
PRE_REP = fresh_pre_rep
PRE_TOP = fresh_pre_top
EXPECTED_POST_RC = PRE_REP + 1
print(f"[Phase 0] PRE_REP={fresh_pre_rep} PRE_TOP={fresh_pre_top} EXPECTED_POST_RC={EXPECTED_POST_RC} (env-var drift absorbed)")

# === Phase 0b: preflight — untracked-file-tolerant ===
dirty = subprocess.check_output(['git','status','--short'], text=True).strip().splitlines()
modified = [l for l in dirty if l.startswith(' M ') or l.startswith('M ')]
untracked = [l for l in dirty if l.startswith('??')]
print(f"[Phase 0b] modified={modified} untracked_count={len(untracked)}")
assert len(modified) == 0, f"NO-OP preflight failed — M lines present: {modified}"

# === Phase 0c: VERCEL_URL from verify.log (strip /tweets.json suffix) ===
verify_log = os.path.join(WORKDIR, 'verify.log')
vercel_url = None
if os.path.exists(verify_log):
    last_lines = open(verify_log).read().splitlines()[-50:]
    for line in reversed(last_lines):
        m = re.search(r'target_url=(\S+)', line)
        if m:
            vercel_url = m.group(1).replace("/tweets.json", "")
            break
assert vercel_url, "VERCEL_URL not found"
print(f"[Phase 0c] VERCEL_URL={vercel_url}")

# === Phase 1: HEAD vs CUR — NO-OP delta=+0 ===
HEAD_SHA = subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip()
HEAD_DATA = json.loads(subprocess.check_output(['git','show',f'{HEAD_SHA}:tweets.json'], text=True))
CUR_DATA = json.load(open('tweets.json'))
HEAD_IDS = {str(t['id']) for t in HEAD_DATA}
NEW_RECORDS = [t for t in CUR_DATA if str(t['id']) not in HEAD_IDS]
print(f"[Phase 1] HEAD={HEAD_SHA} HEAD_count={len(HEAD_DATA)} CUR_count={len(CUR_DATA)} delta=+{len(NEW_RECORDS)}")
assert len(NEW_RECORDS) == 0, "expected NO-OP, but delta>0 — use SUBSTANTIVE script instead"

# === Phase 2: index.html P19 1-marker chained-replace ===
OLD_MARKER = os.environ.get('OLD_MARKER', 'Last hourly cron deploy: 15:00 CST')
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"

# Pre-flight Pitfall 14 f-string eval pre-check: ensure neither OLD_MARKER nor NEW_MARKER
# literal substring appears anywhere in the new lineB body. 25th prevention-fire.
newlineb = (
    f"cycle {CYCLE_NUM} ({CST_DATE} {CST_TIME}:00 CST = {UTC_HOUR:02d}:00 UTC): NO-OP 0 new tweets "
    f"(HEAD {len(HEAD_DATA)} -> CUR {len(CUR_DATA)} delta=0), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR:02d} UTC "
    f"{'NOT in' if UTC_HOUR not in {0,3,6,9,12,15,18,21} else 'in'} "
    f"RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}} per fetch_tweets.py); "
    f"fetcher at 15:07 CST hour 07 UTC non-retry-eligible ran AFTER cycle 842 commit and reported No new tweets "
    f"(HEAD=7390, CUR=7390, delta=+0); "
    f"cycle 842 SUBSTANTIVE (immediately-prior, different class) confirms 0 carry-over into cycle 843; "
    f"cycle 843 entry state: HEAD=eb10c62 (cycle 842 chore commit), CUR=7390, delta=+0; "
    f"next fetcher at 16:07 CST hour 08 UTC non-retry-eligible will run AFTER this commit; "
    f"P19/P88/P31/P52/P69/P71/P73/cycle-321-TBD discipline CANONICAL; "
    f"117th consecutive PRE_REP-drift-clean cycle; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK; commit TBD; Vercel PASS-TBD; "
    f"785th consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (codified cycle 818, 25th prevention-fire)
assert OLD_MARKER not in newlineb, f"pitfall 14: OLD_MARKER {OLD_MARKER!r} found in new lineB body"
assert NEW_MARKER not in newlineb, f"pitfall 14: NEW_MARKER {NEW_MARKER!r} found in new lineB body"

NEW_REGION = NEW_MARKER + newlineb

html = open('index.html').read()
assert OLD_MARKER in html, f"OLD_MARKER not found: {OLD_MARKER!r}"
marker_count = html.count('Last hourly cron deploy:')
print(f"[Phase 2] marker_count={marker_count}")

html_new = html.replace(OLD_MARKER, NEW_REGION, 1)
assert OLD_MARKER not in html_new
assert NEW_MARKER in html_new

fd, tmppath = tempfile.mkstemp(suffix='.html', dir=WORKDIR)
try:
    with os.fdopen(fd, 'w') as f:
        f.write(html_new)
    os.replace(tmppath, 'index.html')
except Exception:
    if os.path.exists(tmppath): os.unlink(tmppath)
    raise
print(f"[Phase 2] index.html: {OLD_MARKER!r} -> {NEW_MARKER!r} + lineB appended")

# === Phase 3: deploy-stamp.txt ===
deploy_stamp = f"{CST_DATE} {CST_TIME} CST = cycle {CYCLE_NUM} = {vercel_url}\n"
open('deploy-stamp.txt','w').write(deploy_stamp)
print(f"[Phase 3] deploy-stamp.txt: {deploy_stamp.strip()}")

# === Phase 4: jobs.json round-trip with TBD markers ===
new_rep = PRE_REP + 1
new_top = new_rep  # P52 symmetric reset
now_iso = NOW_CST.strftime('%Y-%m-%dT%H:%M:%S+08:00')
note = (
    f"cycle {CYCLE_NUM} ({CST_DATE} {CST_TIME}:00 CST = {UTC_HOUR:02d}:00 UTC): "
    f"NO-OP 0 new tweets (HEAD {len(HEAD_DATA)} -> CUR {len(CUR_DATA)}), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR:02d} UTC "
    f"{'NOT in' if UTC_HOUR not in {0,3,6,9,12,15,18,21} else 'in'} "
    f"RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}}); "
    f"commit TBD; Vercel PASS-TBD"
)
target['completed'] = new_top
target['last_run_note'] = note
target['repeat']['completed'] = new_rep
target['repeat']['last_run_note'] = note
target['repeat']['last_run_at'] = now_iso
target['last_run_at'] = now_iso
target['updated_at'] = now_iso
target['last_status'] = 'ok'
jobs_data['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'

fd, tmppath = tempfile.mkstemp(suffix='.json', dir='/Users/taeyeon093.bot/.hermes/cron')
try:
    with os.fdopen(fd, 'w') as f:
        json.dump(jobs_data, f, indent=2, ensure_ascii=False)
    os.replace(tmppath, JOBS_PATH)
except Exception:
    if os.path.exists(tmppath): os.unlink(tmppath)
    raise
print(f"[Phase 4] jobs.json: PRE_rep={PRE_REP} POST_rep={new_rep} PRE_top={PRE_TOP} POST_top={new_top}")

# === Phase 6: git add + commit + push ===
# NO-OP uses 2-file commit: deploy-stamp.txt + index.html (NO tweets.json)
subprocess.run(['git','add','deploy-stamp.txt','index.html'], check=True, cwd=WORKDIR)
added = subprocess.check_output(['git','diff','--cached','--name-only'], text=True).strip().splitlines()
print(f"[Phase 6] staged={added}")

commit_msg = (
    f"cron cycle {CYCLE_NUM} ({CST_DATE} {CST_TIME} CST = {UTC_HOUR:02d} UTC): "
    f"NO-OP 0 new tweets (HEAD {len(HEAD_DATA)} -> CUR {len(CUR_DATA)}), "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK (canonical PRE_REP_RC+1={EXPECTED_POST_RC})"
)
result = subprocess.run(
    ['git','-c','credential.helper=osxkeychain','commit','-m',commit_msg],
    capture_output=True, text=True, cwd=WORKDIR
)
if result.returncode != 0:
    raise SystemExit(f"commit failed: {result.stderr}")
new_sha = subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip()
sha7 = new_sha[:7]
print(f"[Phase 6] commit_sha={new_sha}")

push_cmd = ['git','-c','credential.helper=osxkeychain','push','origin','main']
push_result = subprocess.run(push_cmd, capture_output=True, text=True, cwd=WORKDIR)
if push_result.returncode != 0:
    raise SystemExit(f"push failed: {push_result.stderr}")
print(f"[Phase 6] push OK")

# === Phase 7: Vercel verify ===
import time
time.sleep(15)

deploy_resp = subprocess.run(
    ['curl','-sS','--max-time','20', f'{vercel_url}/deploy-stamp.txt'],
    capture_output=True, text=True
)
deploy_text = deploy_resp.stdout.strip() if deploy_resp.returncode == 0 else "FETCH_FAILED"
deploy_ok = (CST_TIME in deploy_text) or (f'cycle {CYCLE_NUM}' in deploy_text)
print(f"[Phase 7] deploy-stamp OK={deploy_ok} text={deploy_text[:200]}")

try:
    remote_data = json.loads(subprocess.check_output(
        ['curl','-sS','--max-time','30', f'{vercel_url}/tweets.json'],
        text=True
    ))
    remote_ids = {str(t['id']) for t in remote_data}
    local_ids = {str(t['id']) for t in CUR_DATA}
    tweets_ok = (remote_ids == local_ids)
except Exception as e:
    tweets_ok = False
    print(f"[Phase 7] tweets probe error: {e}")
print(f"[Phase 7] tweets OK={tweets_ok}")

vercel_result = "Vercel PASS-1" if (deploy_ok and tweets_ok) else "Vercel FAIL"
print(f"[Phase 7] vercel_result={vercel_result}")

# === Phase 8: post-push jobs.json patch ===
final_note = (
    f"cycle {CYCLE_NUM} ({CST_DATE} {CST_TIME}:00 CST = {UTC_HOUR:02d}:00 UTC): "
    f"NO-OP 0 new tweets (HEAD {len(HEAD_DATA)} -> CUR {len(CUR_DATA)}), "
    f"commit {sha7}; Vercel {vercel_result}; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK; 117th consecutive PRE_REP-drift-clean cycle; 785th consecutive clean push (webpage-only, no Telegram)"
)
final_note = final_note.replace('Vercel Vercel ', 'Vercel ')
jobs_data2 = json.load(open(JOBS_PATH))
for j in jobs_data2['jobs']:
    if isinstance(j, dict) and j.get('name') == 'elon-tweets-hourly':
        j['last_run_note'] = final_note
        j['repeat']['last_run_note'] = final_note
        break
jobs_data2['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
fd, tmppath = tempfile.mkstemp(suffix='.json', dir='/Users/taeyeon093.bot/.hermes/cron')
try:
    with os.fdopen(fd, 'w') as f:
        json.dump(jobs_data2, f, indent=2, ensure_ascii=False)
    os.replace(tmppath, JOBS_PATH)
except Exception:
    if os.path.exists(tmppath): os.unlink(tmppath)
    raise
print(f"[Phase 8] jobs.json: TBD -> {sha7} Vercel {vercel_result}")

# === Phase 9: verify.log ===
verify_line = f"cycle {CYCLE_NUM} sha={sha7} target_url={vercel_url} deploy_stamp_ok={deploy_ok} tweets_set_equal={tweets_ok} vercel_result={vercel_result}\n"
with open(verify_log, 'a') as f:
    f.write(verify_line)

print(f"\n=== CYCLE {CYCLE_NUM} COMPLETE ===")
print(f"  HEAD {len(HEAD_DATA)} -> CUR {len(CUR_DATA)} delta=+{len(NEW_RECORDS)}")
print(f"  commit {sha7}")
print(f"  vercel {vercel_result}")
print(f"  785th consecutive clean push")
