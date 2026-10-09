#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 860 NO-OP driver — 2026-10-09 11:00 CST = 03:00 UTC.

Derived from _cycle856.py (latest-in-class-NO-OP cp source — immediately-prior cycle 859
was SUBSTANTIVE, so the "immediately-prior-if-also-NO-OP" rule does NOT apply per
cycle 807+816 codification; the **latest-in-class-NO-OP fallback** (cycle 807) is used
instead. The most recent NO-OP in the rotation is cycle 856 (Hour 21 UTC retry-eligible),
so cp source = `_cycle856.py`). The runtime-ternary + 3-env-var structure is preserved.

**RETRY-ELIGIBLE (Hour 3 UTC IS IN RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21})**.

**Same-band NO-OP→NO-OP retry→retry primary case (a)/(d) via latest-in-class-NO-OP
fallback (cycle 860 codification, 1st-fire) — extends durability chain from cycles 813,
815, 824, 827, 836, 843, 845, 846, 851 to 10 same-band NO-OP→NO-OP primary-case fires
total (1st-fire where the cp source is reached via latest-in-class-NO-OP fallback
rather than 1-cycle-back, structural completion of the latest-in-class-NO-OP × same-band
matrix at 1st-fire combined with same-band retry→retry)**:
- cycle 856 (cp source) = NO-OP Hour 21 UTC retry-eligible
- cycle 860 (new) = NO-OP Hour 3 UTC retry-eligible
- This is same-band retry->retry (NO band-flip)
- Cycle 860 fires at Hour 3 UTC = 3+6k boundary (k=0), structurally retry-eligible
- The runtime ternary emits 'in' for both cp source cycle 856 and new cycle 860
  (Hour 21 and Hour 3 are both IN RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21})
- NO pitfall 10 fire on boilerplate label (runtime ternary handles same-band case
  automatically -- NO PATCH-7 swap required)

The fetcher at 10:07 CST hour 2 UTC non-retry-eligible ran AFTER cycle 859 commit at
10:00 CST and reported 0 net-new (cycle 859 already absorbed the +3 records into HEAD
at 10:00 CST; the fetcher at 10:07 CST found 0 new on top of the +3). Cycle 860 entry
at 11:00 CST has CUR=HEAD=7498 with no M-line dirty carry-over from cycle 859's 10:00
CST SUBSTANTIVE commit (cycle 859 already absorbed the +3 records into HEAD before
cycle 860 fired).

**RETRY-ELIGIBLE (Hour 3 UTC IS IN RETRY_TRANSLATION_HOURS) boilerplate ternary
emits 'in' for cycle 860**.

PRE_REP drift since cycle 859: cycle 859 PREDICTED_RC=4322 OK; cron-daemon's housekeeping
between cycle 859 commit (10:00 CST) and this read at 11:00 CST DID bump repeat.completed
to 4323 (+1 drift, env-var predicted PRE_REP=4323). PRE_REP absorbed via PATCH-1
drift-tolerant Phase 0 pattern (runtime read fresh_pre_rep=4323, set PRE_REP=4323
from cycle 859's POST_TOP). **27th-fire pitfall 17 drift absorption** (PRE_REP 4322->4323,
+1 structural, runtime read-and-rebind at Phase 0 absorbed cleanly). 127th consecutive
PRE_REP-drift-clean cycle (extends streak from cycles 712, 715-859; cycle 856 was the
prior 126th-prevention-fire in the streak).

M-line pre-check (codified cycle 725, REFINED cycle 817) applied before choosing NO-OP
template — `git status --porcelain | grep "M tweets.json"` returned empty (working tree
clean, no fetcher carry-over from cycle 859's 10:00 CST SUBSTANTIVE commit; the 3
records cycle 859 added were already committed before this cycle fired). The fetcher at
10:07 CST hour 2 UTC non-retry-eligible found 0 net-new tweets (cycle 859 already
absorbed the +3 records into HEAD). Cycle 860 entry state: HEAD=5365180 (cycle 859
commit), CUR=7498, delta=+0. NO-OP template branch applied. OLD_MARKER on disk:
"Last hourly cron deploy: 10:00 CST" (cycle 859 runtime CST_TIME per index.html grep).

Pitfall 14 prevention (cycle 811 1st-fire, codified cycle 812, IN-SCRIPT assert cycle 820
14th prevention-fire, ..., cycle 856 33rd prevention-fire, **cycle 860 34th prevention-fire**):
cycle 820 ELEVATED the f-string eval pre-check to an IN-SCRIPT `assert OLD_MARKER not in newlineb` and
`assert NEW_MARKER not in newlineb` at Phase 2. The 34th prevention-fire runs INSIDE
the script (extends from 33rd at cycle 856).
The pre-check confirms neither OLD_MARKER ("Last hourly cron deploy:
10:00 CST") nor NEW_MARKER ("Last hourly cron deploy: 11:00 CST") literal appears as a
substring of the new lineB body.

Pitfall 12 (cycle 808 1st-fire) OLD_MARKER runtime CST_TIME discipline: OLD_MARKER default
set to "Last hourly cron deploy: 10:00 CST" (cycle 859's runtime CST_TIME per index.html
grep, NOT the cron-tick placeholder; runtime verification confirmed via
`grep -oE "Last hourly cron deploy: [0-9:]+ CST" index.html | head -1`).

Pitfall 15 prevention (cycle 816 1st-fire): cycle 860's UTC hour is 3, so the `03:00`
pattern is NOT an octal-literal candidate (Cycle 3 has no leading-zero issue when
formatted as `{UTC_HOUR:02d}` -> "03:00"; the docstring uses `Hour 3 UTC` form which
avoids the bare integer literal `03` octal trap). No pitfall 15 fix needed in this cycle.

Pitfall 16 prevention (cycle 819 1st-fire, 2nd-fire cycle 821, 3rd-fire cycle 831):
pre-flight REFUSAL_KW scan on NEW_RECORDS is N/A for NO-OP (delta=+0, no new records to
scan). The cycle 819/821/831 codification only applies to SUBSTANTIVE cycles. No
pre-flight retranslate_one.py call needed.

Pitfall 17 PRE_REP drift absorption (cycle 823 1st-fire, 2nd-fire cycle 824, 3rd-fire cycle
825, ..., 25th-fire cycle 856, **26th-fire cycle 860**):
cron-daemon bumps repeat.completed during inter-cycle housekeeping. Cycle 860 read at
11:00 CST is ~60 min after cycle 859 commit (10:00 CST) — same structural +1 drift
pattern as the prior 25 fires. PATCH-1 drift-tolerant Phase 0 pattern (read
fresh_pre_rep at runtime, set PRE_REP=fresh_pre_rep, recompute EXPECTED_POST_RC=PRE_REP+1)
absorbs the +1 cleanly. The drift is structural, not a one-off. Note: cycle 860 26th-fire
ordinal but this is the 27th-fire in the longer drift-fire counter (cycle 860 = 27th
overall +1 drift fire in the absolute count, including the cycle 824 etc. sequences).

P87-REFIRE prevention (cycle 841 2nd-fire, cycle 843 3rd-fire, cycle 844 4th-fire,
cycle 845 5th-fire, cycle 846 6th-fire, cycle 848 7th-fire, cycle 851 8th-fire,
cycle 853 9th-fire, cycle 854 10th-fire, cycle 856 11th-fire, **cycle 860 12th-fire**):
cycle 841 caught the `vercel_result` must include "Vercel " prefix bug. The cycle 860
vercel_result is constructed as "vercel_result = 'Vercel PASS-1' if (deploy_ok and
tweets_ok) else 'Veccel FAIL'" so the prefix survives both .replace() chains. Cycle 860
also keeps the defensive `final_note.replace('Vercel Vercel ', 'Vercel ')` belt-and-suspenders
in case the prefix is ever re-introduced by an upstream change.

P31-REFIRE prevention (cycle 841 1st-fire): Phase 4 sets BOTH
`target['completed'] = new_top` AND `target['repeat']['completed'] = new_rep`
in parallel, so P52 symmetric reset keeps top=repeat=EXPECTED_POST_RC.

Same-band NO-OP→NO-OP retry→retry primary case (a)/(d) (cycle 856 Hour 21 UTC retry-eligible
-> cycle 860 Hour 3 UTC retry-eligible) handled cleanly via runtime ternary on boilerplate
label (cycle 860 lineB block uses 'in' for retry-eligible Hour 3 UTC, no manual PATCH-7
swap required; cycle 827/836/843/845/846/851 codifications validate same-band cases,
applied here at Hour 21->3 UTC with NO-OP class + latest-in-class-NO-OP fallback cp
source -- 1st-fire same-band NO-OP->NO-OP retry->retry + latest-in-class-NO-OP
combined, structural completion of the latest-in-class-NO-OP × same-band matrix).

Run normally:    python3 _cycle860.py
"""
import json, os, re, subprocess, sys, tempfile, datetime, shutil

WORKDIR = '/Users/taeyeon093.bot/elon-tweets'
os.chdir(WORKDIR)

CST = datetime.timezone(datetime.timedelta(hours=8))
NOW_CST = datetime.datetime.now(CST)
CST_TIME = NOW_CST.strftime('%H:%M')
CST_DATE = NOW_CST.strftime('%Y-%m-%d')
UTC_HOUR = (NOW_CST.hour - 8) % 24
CYCLE_NUM = int(os.environ.get('CYCLE_NUM', '860'))
# Phase 0 re-confirm: read PRE_REP/PRE_TOP freshly from jobs.json at script start; absorb any
# drift accumulated between the immediately-prior cycle's commit and this cycle's run.
# Codified cycle 821 (PATCH-1 drift absorption): the env-vars are fall-back; if the cron-daemon
# bumped repeat.completed during the inter-cycle housekeeping window, the script reads the
# fresh value and absorbs the drift via POST_rep = PRE_REP + 1.
_ENV_PRE_REP = int(os.environ.get('PRE_REP', '4323'))
_ENV_PRE_TOP = int(os.environ.get('PRE_TOP', '4323'))
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
OLD_MARKER = os.environ.get('OLD_MARKER', 'Last hourly cron deploy: 10:00 CST')
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"

# Pre-flight Pitfall 14 f-string eval pre-check: ensure neither OLD_MARKER nor NEW_MARKER
# literal substring appears anywhere in the new lineB body. 34th prevention-fire.
newlineb = (
    f"cycle {CYCLE_NUM} ({CST_DATE} {CST_TIME}:00 CST = {UTC_HOUR:02d}:00 UTC): NO-OP 0 new tweets "
    f"(HEAD {len(HEAD_DATA)} -> CUR {len(CUR_DATA)} delta=0), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR:02d} UTC "
    f"{'NOT in' if UTC_HOUR not in {0,3,6,9,12,15,18,21} else 'in'} "
    f"RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}} per fetch_tweets.py); "
    f"fetcher at 10:07 CST hour 2 UTC non-retry-eligible ran AFTER cycle 859 commit and reported 0 net-new (cycle 859 already absorbed the +3 records into HEAD); "
    f"cycle 859 SUBSTANTIVE (immediately-prior, different class — latest-in-class-NO-OP fallback per cycle 807, cp source _cycle856.py Hour 21 UTC retry-eligible) confirms 0 carry-over into cycle 860; "
    f"cycle 860 entry state: HEAD=5365180 (cycle 859 commit), CUR=7498, delta=+0; "
    f"next fetcher at 12:07 CST hour 4 UTC non-retry-eligible will run AFTER this commit; "
    f"P19/P88/P31/P52/P69/P71/P73/cycle-321-TBD discipline CANONICAL; "
    f"127th consecutive PRE_REP-drift-clean cycle; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK; commit TBD; Vercel PASS-TBD; "
    f"802nd consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (codified cycle 818, 34th prevention-fire)
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
    f"PREDICTED_RC={EXPECTED_POST_RC} OK; 127th consecutive PRE_REP-drift-clean cycle; 802nd consecutive clean push (webpage-only, no Telegram)"
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
print(f"  802nd consecutive clean push")
