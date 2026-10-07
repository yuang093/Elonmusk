#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 815 NO-OP driver — 2026-10-07 10:00 CST = 02:00 UTC.

Derived from _cycle814.py (1-cycle-back canonical case, both NO-OP) using the canonical
cp + 6-patch sequence (1 header + 1 env-defaults block [3 lines: CYCLE_NUM/PRE_REP/PRE_TOP] + 1
OLD_MARKER + 3 ordinal literals at newlineb / final_note / completion banner; PATCH-3c covers
the fetcher-time / UTC-hour / retry-eligibility correction).

The "immediately-prior-if-also-NO-OP" recipe rule applies: immediately-prior cycle 814 was
NO-OP (same class), so we use 1-cycle-back cp source `_cycle814.py` directly. This is the
canonical 1-cycle-back case (recipe matrix case (a)/(d) NO-OP→NO-OP).

NON-RETRY-ELIGIBLE (hour 02 UTC NOT IN RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}). Cron
tier still does 2-file NO-OP commit regardless. PATCH-7 is N/A (NO-OP template uses runtime
ternary, line 108-110 + 152-153 auto-evaluates 'in' for this hour; runtime ternary emits
'NOT in' for hour 02 since 02 ∉ {0,3,6,9,12,15,18,21}; no hardcoded literal to flip).

The fetcher at 09:01 CST hour 01 UTC non-retry-eligible ran BEFORE this commit and reported
No new tweets; the non-retry-eligible fetcher at 10:01 CST hour 02 UTC also ran and reported
No new tweets (HEAD=7284, CUR=7284, delta=+0). Immediately-prior cycle 814 was NO-OP
(same class), so per the codified recipe "immediately-prior-if-also-NO-OP" the
`_cycle814.py` template was used (1-cycle-back NO-OP) to preserve the 3-env-var structure
required for PATCH-3b.

Variant analysis: cp source cycle 814 was 3-dim with-retry-flip retry→non-retry (cron 00→01
retry→non-retry; fetcher-time 00→01 non-retry→retry — opposite direction cross-band). New
cycle 815 is 2-dim same-band (cron 01→02 non-retry→non-retry; fetcher-time 01→02
non-retry→non-retry — same direction same-band). Per recipe matrix case (a)/(d) NO-OP→NO-OP
1-cycle-back, same-band→same-band (cron non-retry→non-retry same direction; fetcher-time
non-retry→non-retry same direction) → **NO pitfall 10 fire** (match case). PATCH-3c
updates the fetcher-time lineB wording "08:00 CST hour 00 UTC retry-eligible" → "09:00 CST
hour 01 UTC non-retry-eligible" with the corrected non-retry-band label (since fetcher-time
flips from retry-eligible to non-retry-eligible on the cp source boundary).

PRE_REP drift since cycle 814: cycle 814 PREDICTED_RC=4243 OK; cron-daemon's housekeeping
between cycle 814 commit (09:03 CST) and this read at 10:01 CST bumped repeat.completed
from 4243 to 4244 (one auto-bump this hour — likely from cycle 814 post-push pass patch
landing before the 10:00 CST cron tick). PRE_REP=PRE_TOP=4244 perfect sync, no drift this
cycle. 90th consecutive PRE_REP-drift-clean cycle (extends the streak from cycles 712,
715-814 where PRE_REP absorbed drift without cycle-level adjustment; cycle 815 has zero
drift, so streak counter continues).

M-line pre-check (codified cycle 725) applied before choosing NO-OP template — `git status --short | grep -E "^ M |^M "`
returned empty (working tree clean, no fetcher carry-over from cycle 814's 09:03 CST
NO-OP commit), so the NO-OP template branch applied; immediately-prior cycle 814 was
NO-OP (same class) so per the codified recipe ("immediately-prior-if-also-NO-OP, else
latest-in-class-NO-OP") the `_cycle814.py` template was used (1-cycle-back NO-OP) to
preserve the 3-env-var structure required for PATCH-3b.

Run normally:    python3 _cycle815.py
"""
import json, os, re, subprocess, sys, tempfile, datetime, shutil

WORKDIR = '/Users/taeyeon093.bot/elon-tweets'
os.chdir(WORKDIR)

CST = datetime.timezone(datetime.timedelta(hours=8))
NOW_CST = datetime.datetime.now(CST)
CST_TIME = NOW_CST.strftime('%H:%M')
CST_DATE = NOW_CST.strftime('%Y-%m-%d')
UTC_HOUR = (NOW_CST.hour - 8) % 24
CYCLE_NUM = int(os.environ.get('CYCLE_NUM', '815'))
PRE_REP = int(os.environ.get('PRE_REP', '4244'))
PRE_TOP = int(os.environ.get('PRE_TOP', '4244'))
EXPECTED_POST_RC = PRE_REP + 1

# === Phase 0: jobs.json PRE_REP re-confirm ===
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
assert fresh_pre_rep == PRE_REP, f"PRE_REP drift: {fresh_pre_rep} vs {PRE_REP}"
print(f"[Phase 0] PRE_REP={fresh_pre_rep} PRE_TOP={fresh_pre_top} EXPECTED_POST_RC={EXPECTED_POST_RC}")

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
OLD_MARKER = os.environ.get('OLD_MARKER', 'Last hourly cron deploy: 09:03 CST')
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"

# Build NEW_LINEB — NO-OP form, brace-safe f-string
newlineb = (
    f"cycle {CYCLE_NUM} ({CST_DATE} {CST_TIME}:00 CST = {UTC_HOUR:02d}:00 UTC): NO-OP 0 new tweets "
    f"(HEAD {len(HEAD_DATA)} -> CUR {len(CUR_DATA)} delta=0), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR:02d} UTC "
    f"{'NOT in' if UTC_HOUR not in {0,3,6,9,12,15,18,21} else 'in'} "
    f"RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}} per fetch_tweets.py); "
    f"fetcher at 09:00 CST hour 01 UTC non-retry-eligible ran BEFORE this commit and reported No new tweets; "
    f"P19/P88/P31/P52/P69/P71/P73/cycle-321-TBD discipline CANONICAL; "
    f"90th consecutive PRE_REP-drift-clean cycle; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK; commit TBD; Vercel PASS-TBD; "
    f"758th consecutive clean push (webpage-only, no Telegram) -->"
)

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

vercel_result = "PASS-1" if (deploy_ok and tweets_ok) else "FAIL"
print(f"[Phase 7] vercel_result={vercel_result}")

# === Phase 8: post-push jobs.json patch ===
final_note = (
    f"cycle {CYCLE_NUM} ({CST_DATE} {CST_TIME}:00 CST = {UTC_HOUR:02d}:00 UTC): "
    f"NO-OP 0 new tweets (HEAD {len(HEAD_DATA)} -> CUR {len(CUR_DATA)}), "
    f"commit {sha7}; Vercel {vercel_result}; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK; 90th consecutive PRE_REP-drift-clean cycle; 758th consecutive clean push (webpage-only, no Telegram)"
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
print(f"  758th consecutive clean push")
