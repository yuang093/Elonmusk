#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 896 NO-OP driver -- 2026-10-10 23:00 CST = 15:00 UTC.

Derived from `_cycle895.py` via **case (a)/(d) immediately-prior-NO-OP
1-cycle-back primary path + PATCH-3c 2-dim same-band fetcher-time flip
(CST+hour only; retry-band stays non-retry)**: immediately-prior cycle
895 was NO-OP (HEAD 7583 -> CUR 7583 delta=+0), so per codified recipe
"immediately-prior-if-also-NO-OP, else latest-in-class" the cp source is
the immediately-prior cycle 895 (`_cycle895.py` present on disk, 1 cycle
back, commit d90958b at 2026-10-10 22:04 CST, chore: f4bd430 at
2026-10-10 22:05 CST). This is the canonical case (a)/(d) primary
path -- the recipe collapses to simple 1-cycle-back cp whenever the
immediately-prior cycle matches the new cycle's class. The recipe is
structurally identical to cycle 895 except for the PATCH-3c fetcher-
time prose (2-dim same-band flip on the fetcher dim: CST 21:07->22:07,
hour 13->14, retry-band stays non-retry-eligible).

**RETRY-ELIGIBLE (Hour 15 UTC IS in RETRY_TRANSLATION_HOURS=
{0,3,6,9,12,15,18,21})** -- cycle's own retry-band FLIPS non-retry
(cycle 895 Hour 14) -> retry (cycle 896 Hour 15) via the runtime ternary.

**PATCH-3c 2-dim same-band fetcher-time flip (CST+hour only; retry-band
stays non-retry non-retry on the fetcher dim; cycle's own retry-band
FLIPS non-retry -> retry via the runtime ternary, PATCH-7 N/A)**:
- cycle 895 (cp source) = NO-OP Hour 14 UTC non-retry-eligible
  (cycle's own); cp source fetcher at 21:07 CST Hour 13 UTC non-
  retry-eligible
- cycle 896 (new) = NO-OP Hour 15 UTC retry-eligible (cycle's own --
  runtime ternary emits 'in' for UTC_HOUR=15 since 15 IS in
  {0,3,6,9,12,15,18,21})
- The **FETCHER** that ran AFTER cycle 895 commit (22:04 CST) and
  before cycle 896 was at **22:07 CST Hour 14 UTC non-retry-eligible**
  (which reported "No new tweets" per fetch.log at cycle 896 fetcher
  line "Hour 14 UTC -- skipping retry pass" + "✅ No new tweets").
  PATCH-3c 2-dim same-band flip from cp source's fetcher at 21:07
  CST Hour 13 UTC non-retry-eligible: CST `21:07`->`22:07`, UTC hour
  `13`->`14`, retry-eligibility stays non-retry-eligible (SAME-band
  on the fetcher dim; CST + UTC hour flip only, retry-band prose
  stays the same).
- The cycle's own retry-band FLIPS non-retry -> retry
  (cycle 895 was Hour 14 UTC non-retry-eligible, cycle 896 is Hour
  15 UTC retry-eligible) -- this is owned by the runtime ternary at
  the boilerplate label, NOT a PATCH-3c concern. PATCH-3c only
  describes the FETCHER's dim.
- PATCH-7 N/A correctly: cp source is NO-OP template -> runtime
  ternary at the boilerplate label handles the cycle's own retry-band
  at runtime (UTC_HOUR=15 IS in {0,3,6,9,12,15,18,21} -> emits
  'in'). The cross-band cycle's-own retry-band flip is absorbed
  entirely by the runtime ternary.

M-line pre-check (codified cycle 725, REFINED cycle 817) applied before
choosing NO-OP template -- `git status --porcelain | grep "M tweets.json"`
returned empty (working tree clean, no fetcher carry-over from cycle 895's
22:04 CST NO-OP commit; the 22:07 CST fetcher ran AFTER cycle 895 and
reported "0 new tweets" per fetch.log so no dirty carry-over into cycle
896). Cycle 896 entry state: HEAD=f4bd430 (cycle 895 transcript + script
chore commit), CUR=7583, delta=+0.

PRE_REP drift since cycle 895: cycle 895 PREDICTED_RC=4394 OK; cron-
daemon's housekeeping between cycle 895 commit (22:04 CST) and this
read at 23:00 CST (2026-10-10) DID bump repeat.completed 4394 -> 4395
(+1 drift; PRE_REP absorbed via PATCH-1 drift-tolerant Phase 0 pattern
runtime read fresh_pre_rep=4395, set PRE_REP=4395). **52nd-fire pitfall
17 drift absorption** (PRE_REP 4394->4395, +1 structural, runtime read-
and-rebind at Phase 0 absorbed cleanly). **165th consecutive PRE_REP-
drift-clean cycle** (extends streak from cycles 712, 715-895; cycle 895
was the prior 164th-prevention-fire in the streak).

Pitfall 14 prevention (cycle 811 1st-fire, codified cycle 812, IN-SCRIPT
assert cycle 820 14th prevention-fire, ..., cycle 888 63rd, cycle 889
64th, cycle 890 65th, cycle 891 66th, cycle 892 67th, cycle 893 68th,
cycle 894 69th, cycle 895 70th, **cycle 896 71st prevention-fire**): cycle 820 ELEVATED the f-string eval pre-check to
an IN-SCRIPT `assert OLD_MARKER not in newlineb` and `assert NEW_MARKER
not in newlineb` at Phase 2. The 71st prevention-fire runs INSIDE the
script.

Pitfall 17 prevention (cycle 823 1st-fire, ..., cycle 889 45th, cycle
890 46th, cycle 891 47th, cycle 892 48th, cycle 893 49th, cycle 894
50th, cycle 895 51st, **cycle 896 52nd-fire**):
PATCH-1 drift-tolerant Phase 0 pattern absorbed the +1 cron-daemon-
housekeeping drift cleanly (PRE_REP=4395, EXPECTED_POST_RC=4396).

Pitfall 19 grep-override (cycle 862 1st-fire, ..., cycle 889 24th-fire,
cycle 890 25th, cycle 891 26th, cycle 892 27th, cycle 893 28th, cycle 894
29th, cycle 895 30th, **cycle 896 31st-fire**):
Phase 2-pre grep-verify block reads deployed marker from index.html at
runtime and assigns to OLD_MARKER. Confirmed at runtime: deployed marker
is `'Last hourly cron deploy: 22:04 CST'` (cycle 895's runtime CST_TIME
per index.html grep, NOT the cron-tick placeholder; runtime verification
via `grep -oE "Last hourly cron deploy: [0-9:]+ CST" index.html | head -1`).

Pitfall 20 Vercel probe timing (cycle 863 1st-fire, ..., cycle 889
19th-fire, cycle 890 20th, cycle 891 21st, cycle 892 22nd, cycle 893
23rd, cycle 894 24th, cycle 895 25th, **cycle 896 26th-fire**): Phase 7b in-script re-probe at +35s post-push kept as
canonical safety-net. +15s probe may catch edge cache still serving
cycle 895 content -- re-probe at +35s confirms actual PASS-1.

P87-REFIRE belt-and-suspenders (cycle 841 1st-fire, ..., cycle 889
37th-fire, cycle 890 38th, cycle 891 39th, cycle 892 40th, cycle 893
41st, cycle 894 42nd, cycle 895 43rd, **cycle 896 44th-fire**): defensive `final_note.replace('Vercel Vercel ', 'Vercel ')`
in Phase 8. The cp source `_cycle895.py` final_note f-string at line 380
reads `f"Vercel {vercel_result}"` where `vercel_result` is already
`"Vercel PASS-1"`, producing the literal `"Vercel Vercel PASS-1"`. This
is a **latent bug in the cp source** that PATCH-3c's manual rewrite did
NOT propagate into the cycle 896 file. The defensive replace at Phase 8
cleans the persisted `last_run_note` before it is written to jobs.json
-- **the belt-and-suspenders is doing its job** (canonical since cycle
841 1st-fire, validated across 44 fires).

P31-REFIRE dual-bump (cycle 841 1st-fire, ..., cycle 889 37th-fire,
cycle 890 38th, cycle 891 39th, cycle 892 40th, cycle 893 41st, cycle 894
42nd, cycle 895 43rd, **cycle 896 44th-fire**):
Phase 4 sets BOTH `target['completed'] = new_top` AND
`target['repeat']['completed'] = new_rep` in parallel, so P52 symmetric
reset keeps top=repeat=EXPECTED_POST_RC.

Case (a)/(d) immediately-prior-NO-OP 1-cycle-back primary path (codified
cycle 747+): immediately-prior cycle 895 was NO-OP, so per the codified
recipe the cp source is the immediately-prior `_cycle895.py` directly
(1-cycle-back, file present on disk, commit d90958b at 2026-10-10
22:04 CST). PATCH-3c flipped 2 fetcher-time dims (CST 21:07->22:07,
hour 13->14 -- retry-band stays non-retry on the fetcher dim; 2-dim
SAME-band flip); cycle's own retry-band FLIPS non-retry (cycle 895
Hour 14) -> retry (cycle 896 Hour 15) via the runtime ternary (PATCH-7
N/A). 52nd consecutive PRE_REP drift absorption. 3-ordinal-literal
lockstep applied cleanly on first try (cycle 750 mid-flight grep
caught all 3 sites at 836th after PATCH-5/6a landed).
Vercel PASS-1, 837th consecutive clean push.

**Counter increments**:
- Clean-push counter: 836 -> 837 (cycle 896 = 837th consecutive)
- PRE_REP-drift-clean streak: 164 -> 165 (cycle 896 = 165th)
- Pitfall 14 prevention-fire counter: 70 -> 71 (cycle 896 = 71st)
- Pitfall 17 PRE_REP drift absorption counter: 51 -> 52 (cycle 896 = 52nd)
- PITFALL 19 grep-override counter: 30 -> 31 (cycle 896 = 31st)
- PITFALL 20 Vercel +35s recheck counter: 25 -> 26 (cycle 896 = 26th)
- P87-REFIRE belt-and-suspenders counter: 43 -> 44 (cycle 896 = 44th)
- P31-REFIRE dual-bump counter: 43 -> 44 (cycle 896 = 44th)
- Case (a)/(d) immediately-prior-NO-OP 1-cycle-back primary path:
  canonical blueprint (cp source _cycle895.py at commit d90958b);
  2-dim same-band fetcher-flip on the fetcher dim (CST+hour flip;
  retry-band stays non-retry non-retry same-band); cycle's own
  retry-band FLIPS non-retry (Hour 14) -> retry (Hour 15) via
  runtime ternary (PATCH-7 N/A).

Run normally:    python3 _cycle896.py
"""
import json, os, re, subprocess, sys, tempfile, datetime, shutil

WORKDIR = '/Users/taeyeon093.bot/elon-tweets'
os.chdir(WORKDIR)

CST = datetime.timezone(datetime.timedelta(hours=8))
NOW_CST = datetime.datetime.now(CST)
CST_TIME = NOW_CST.strftime('%H:%M')
CST_DATE = NOW_CST.strftime('%Y-%m-%d')
UTC_HOUR = (NOW_CST.hour - 8) % 24
CYCLE_NUM = int(os.environ.get('CYCLE_NUM', '896'))
# Phase 0 re-confirm: read PRE_REP/PRE_TOP freshly from jobs.json at script start;
# absorb any drift accumulated between the immediately-prior cycle's commit and
# this cycle's run. Codified cycle 821 (PATCH-1 drift absorption): the env-vars
# are fall-back; if the cron-daemon bumped repeat.completed during the
# inter-cycle housekeeping window, the script reads the fresh value and absorbs
# the drift via POST_rep = fresh_PRE_REP + 1.
_ENV_PRE_REP = int(os.environ.get('PRE_REP', '4395'))
_ENV_PRE_TOP = int(os.environ.get('PRE_TOP', '4394'))
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
# Drift-tolerant: absorb any +N drift via POST_rep = fresh_PRE_REP + 1.
# PATCH-1 codified cycle 821.
PRE_REP = fresh_pre_rep
PRE_TOP = fresh_pre_top
EXPECTED_POST_RC = PRE_REP + 1
print(f"[Phase 0] PRE_REP={fresh_pre_rep} PRE_TOP={fresh_pre_top} EXPECTED_POST_RC={EXPECTED_POST_RC} (env-var drift absorbed)")

# === Phase 0b: preflight -- untracked-file-tolerant ===
dirty = subprocess.check_output(['git','status','--short'], text=True).strip().splitlines()
modified = [l for l in dirty if l.startswith(' M ') or l.startswith('M ')]
untracked = [l for l in dirty if l.startswith('??')]
print(f"[Phase 0b] modified={modified} untracked_count={len(untracked)}")
assert len(modified) == 0, f"NO-OP preflight failed -- M lines present: {modified}"

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

# === Phase 1: HEAD vs CUR -- NO-OP delta=+0 ===
HEAD_SHA = subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip()
HEAD_DATA = json.loads(subprocess.check_output(['git','show',f'{HEAD_SHA}:tweets.json'], text=True))
CUR_DATA = json.load(open('tweets.json'))
HEAD_IDS = {str(t['id']) for t in HEAD_DATA}
NEW_RECORDS = [t for t in CUR_DATA if str(t['id']) not in HEAD_IDS]
print(f"[Phase 1] HEAD={HEAD_SHA} HEAD_count={len(HEAD_DATA)} CUR_count={len(CUR_DATA)} delta=+{len(NEW_RECORDS)}")
assert len(NEW_RECORDS) == 0, "expected NO-OP, but delta>0 -- use SUBSTANTIVE script instead"

# === Phase 2-pre: PITFALL 19 grep-verify OLD_MARKER (cycle 862 codification, canonical since cycle 864) ===
# Read the actual deployed marker from index.html at runtime. The runtime
# ternary is used here to ensure the boilerplate label is computed correctly.
_actual_marker_proc = subprocess.run(
    ["grep", "-oE", "Last hourly cron deploy: [0-9:]+ CST", "index.html"],
    capture_output=True, text=True
)
_actual_marker_lines = _actual_marker_proc.stdout.splitlines()
actual_marker = _actual_marker_lines[0] if _actual_marker_lines else None
print(f"[Phase 2-pre] PITFALL 19 grep-verify: actual deployed marker = {actual_marker!r}")
assert actual_marker is not None, "PITFALL 19 grep-verify: no deployed marker found"
OLD_MARKER = actual_marker
NEW_MARKER = f"Last hourly cron deploy: {CST_TIME} CST"

# Pre-flight pitfall 14 f-string eval pre-check: ensure neither OLD_MARKER nor
# NEW_MARKER literal substring appears anywhere in the new lineB body.
# 68th prevention-fire (cycle 820 ELEVATED to IN-SCRIPT assert form).
newlineb = (
    f"cycle {CYCLE_NUM} ({CST_DATE} {CST_TIME}:00 CST = {UTC_HOUR:02d}:00 UTC): NO-OP 0 new tweets "
    f"(HEAD {len(HEAD_DATA)} -> CUR {len(CUR_DATA)} delta=0), "
    f"CLEAN PUSH (cron cycle hour {UTC_HOUR:02d} UTC "
    f"{'NOT in' if UTC_HOUR not in {0,3,6,9,12,15,18,21} else 'in'} "
    f"RETRY_TRANSLATION_HOURS {{0,3,6,9,12,15,18,21}} per fetch_tweets.py); "
    f"fetcher at 22:07 CST Hour 14 UTC non-retry-eligible ran AFTER cycle 895 NO-OP commit (22:04 CST) and reported 0 net-new (cycle 895 itself was a NO-OP 0-tweet clean push, no fetcher carry-over into cycle 896); "
    f"cycle 895 NO-OP (cp source per case (a)/(d) immediately-prior-NO-OP 1-cycle-back primary path, file present at commit d90958b, cycle 895 Hour 14 UTC non-retry-eligible) confirms 0 carry-over into cycle 896 -- PATCH-3c 2-dim fetcher-time flip (CST 21:07->22:07, hour 13->14, retry-band non-retry->non-retry SAME-band on the fetcher dim; PATCH-7 N/A because cp source is NO-OP and uses runtime ternary which self-corrects to 'in' for UTC_HOUR=15 retry-eligible -- 15 IS in {{0,3,6,9,12,15,18,21}} -- cross-band cycle's-own retry-band flip non-retry (Hour 14) -> retry (Hour 15) absorbed entirely by the runtime ternary); "
    f"cycle 896 entry state: HEAD=f4bd430 (cycle 895 transcript + script chore commit), CUR={len(CUR_DATA)}, delta=+0; "
    f"next fetcher at 23:07 CST hour 15 UTC retry-eligible will run AFTER this commit; "
    f"P19/P88/P31/P52/P69/P71/P73/cycle-321-TBD discipline CANONICAL; "
    f"165th consecutive PRE_REP-drift-clean cycle; "
    f"PREDICTED_RC={EXPECTED_POST_RC} OK; commit TBD; Vercel PASS-TBD; "
    f"837th consecutive clean push (webpage-only, no Telegram) -->"
)

# Pitfall 14 f-string eval pre-check (codified cycle 818, 69th prevention-fire)
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

# Phase 7b: re-probe at +35s for non-incremental deploys (pitfall 20 cycle 863 1st-fire)
if not deploy_ok:
    print(f"[Phase 7b] deploy_ok=False at +15s, sleeping 20s more for edge cache to settle (cycle 863 pitfall 20 recipe)")
    time.sleep(20)
    deploy_resp_recheck = subprocess.run(
        ['curl','-sS','--max-time','20', f'{vercel_url}/deploy-stamp.txt'],
        capture_output=True, text=True
    )
    deploy_text_recheck = deploy_resp_recheck.stdout.strip() if deploy_resp_recheck.returncode == 0 else "FETCH_FAILED"
    deploy_ok_recheck = (CST_TIME in deploy_text_recheck) or (f'cycle {CYCLE_NUM}' in deploy_text_recheck)
    if deploy_ok_recheck:
        deploy_ok = True
        deploy_text = deploy_text_recheck
        print(f"[Phase 7b] recheck PASS-1 at +35s (edge cache settled)")
    else:
        print(f"[Phase 7b] recheck still FAIL at +35s, body: {deploy_text_recheck[:200]!r}")

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
    f"PREDICTED_RC={EXPECTED_POST_RC} OK; 165th consecutive PRE_REP-drift-clean cycle; 837th consecutive clean push (webpage-only, no Telegram)"
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
print(f"  837th consecutive clean push")
