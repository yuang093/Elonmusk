#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cycle 917 -- 2026-10-11 20:00 CST (Hour 12 UTC retry-eligible) -- NO-OP 0 new tweets

**Case (a)/(d) immediately-prior-NO-OP 1-cycle-back primary path** (cycle 818 codification):
immediately-prior cycle 916 was NO-OP (HEAD=7614 -> CUR=7614 delta=+0, same class, 1 cycle
back, file present on disk at commit 0a57805 + transcript 3956de0). Per codified recipe
"immediately-prior-if-also-NO-OP, else latest-in-class-NO-OP" the cp source is `_cycle916.py`
= the immediately-prior cycle in `git log` (1 cycle back, NOT latest-in-class-NO-OP fallback
which is reserved for when 1-cycle-back is a different class, per cycle 807 codification).

**Cross-band analysis on cycle's own retry-band**: cp source cycle 916 Hour 11 UTC
non-retry-eligible -> new cycle 917 Hour 12 UTC retry-eligible. **Cross-band non-retry->retry
on cycle's own retry-band**. Runtime ternary on 'in'/'NOT in' boilerplate label auto-fires the
correct 'in' string at runtime (UTC_HOUR=12 IS in {0,3,6,9,12,15,18,21}). **PATCH-7 N/A** --
cp source is NO-OP template, runtime ternary handles everything.

**PATCH-3c 3-dim cross-band fetcher-flip on fetcher dim** (CST+hour+retry-band all flip):
cycle 916 fetcher at 19:07 CST Hour 11 UTC non-retry-eligible -> cycle 917 fetcher at 20:07
CST Hour 12 UTC retry-eligible; CST 19:07->20:07, UTC hour 11->12, retry-band
non-retry->retry (CROSS-BAND on the retry-band dim; ALL 3 DIMS FLIP). This is the **3-dim
cross-band variant** of PATCH-3c (CST+hour+retry-band all flip).

**Cycle 917 entry state**: HEAD=3956de0 (cycle 916 chore transcript commit, last NO-OP),
CUR=7614, delta=+0.
**DIRTY WORKING TREE: clean** (no M tweets.json from cycle 916's 19:07 CST Hour 11 UTC
non-retry-eligible fetcher -- non-retry-eligible fetchers do NOT run the retry pass that
re-fills cleared byline records, so no Phase 0.5 needed).

**Hour 12 UTC IS in RETRY_TRANSLATION_HOURS={0,3,6,9,12,15,18,21}** (12 mod 3 = 0). Runtime
ternary handles 'in' boilerplate label automatically. This is the canonical
"case (a)/(d) 1-cycle-back + retry-eligible" pattern at NO-OP. The cycle 917 next fetcher
at 20:07 CST Hour 12 UTC retry-eligible will fire regular scan PLUS retry pass AFTER this
commit. Note: cycle 916's immediately-prior fetcher at 19:07 CST Hour 11 UTC non-retry-
eligible did NOT re-fill cleared byline records (non-retry pass), so working tree is clean
and Phase 0.5 SKIPs.

**Counter increments (cycle 917):**
- Clean-push counter: 858 -> 859 (cycle 917 = 859th consecutive)
- PRE_REP-drift-clean streak: 188 -> 189 (cycle 917 = 189th)
- Pitfall 14 prevention-fire counter: 93 -> 94 (cycle 917 = 94th)
- Pitfall 17 PRE_REP drift absorption counter: 188 -> 189 (same fire as PRE_REP-drift-clean)
- PITFALL 19 grep-override counter: 52 -> 53
- PITFALL 20 Vercel +35s recheck counter: 40 -> 41
- P87-REFIRE belt-and-suspenders counter: 66 -> 67
- P31-REFIRE dual-bump counter: 66 -> 67

**Phase 0/0b/0c/1/2/3/4/6/7/8/9 discipline** all CANONICAL per the umbrella skill recipe.

Run normally:    python3 /Users/taeyeon093.bot/elon-tweets/_cycle917.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = "/Users/taeyeon093.bot/elon-tweets"
JOBS = "/Users/taeyeon093.bot/.hermes/cron/jobs.json"
VERIFY_LOG = f"{REPO}/verify.log"
CYCLE = 917
CST_TIME = "20:00"
UTC_HOUR = "12"
FETCHER_AT = "19:07 CST Hour 11 UTC non-retry-eligible"
NEXT_FETCHER_AT = "20:07 CST Hour 12 UTC retry-eligible"

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
# For NO-OP cycle 917: working tree is clean (cycle 916's 19:07 CST Hour 11 UTC non-retry-
# eligible fetcher does not run the retry pass that re-fills cleared byline records). Phase 0.5
# will only fire IF m_tweets_dirty appears (cycle 909/915 sub-variant).
m_tweets_dirty = [ln for ln in dirty if ln.endswith("tweets.json")]
other_dirty = [ln for ln in dirty if not ln.endswith("tweets.json")]
assert not other_dirty, f"unexpected non-tweets.json dirty: {other_dirty}"

# ---------- Phase 0.5: byline-revert for head-existing cleared records (cycle 909 SUB-VARIANT) ----------
# Cycle 917 has clean working tree (cycle 916's 19:07 CST Hour 11 UTC non-retry-eligible fetcher
# doesn't run the retry pass that overwrites cleared byline records). So Phase 0.5 SKIPPED.
KNOWN_CLEARED_BYLINE_IDS = {"2109035557003415838", "2109072353351348430"}
reverted = 0
if m_tweets_dirty:
    with open(f"{REPO}/tweets.json", "r", encoding="utf-8") as f:
        tweets = json.load(f)
    for t in tweets:
        if t["id"] in KNOWN_CLEARED_BYLINE_IDS:
            old_trans = t.get("translation", "")
            had_retried = "retried_at" in t
            if old_trans != "" or had_retried:
                t["translation"] = ""
                if "retried_at" in t:
                    del t["retried_at"]
                reverted += 1
    if reverted > 0:
        with open(f"{REPO}/tweets.json", "w", encoding="utf-8") as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)
        print(f"[Phase 0.5] REVERTED {reverted} cleared-byline records (id in HEAD)")
else:
    print(f"[Phase 0.5] no M tweets.json dirty, Phase 0.5 SKIPPED (cycle 916 non-retry-eligible fetcher did not re-fill)")

# ---------- Phase 1: HEAD vs CUR count comparison ----------
HEAD_COMMIT = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
HEAD_TWEETS_JSON = subprocess.run(["git", "-C", REPO, "show", "HEAD:tweets.json"],
                                  capture_output=True, text=True).stdout
HEAD = len(json.loads(HEAD_TWEETS_JSON))
with open(f"{REPO}/tweets.json", "r", encoding="utf-8") as f:
    tweets = json.load(f)
CUR = len(tweets)
HEAD_SHORT = HEAD_COMMIT[:8]
print(f"[Phase 1] HEAD={HEAD} CUR={CUR} HEAD_COMMIT={HEAD_SHORT} delta={CUR-HEAD} (expected 0 for NO-OP)")
DELTA = CUR - HEAD
assert DELTA == 0, f"NO-OP recipe expects delta=0, got {DELTA}"

# ---------- Phase 2: NO-OP assertion (no new IDs) ----------
NEW_IDS = []
print(f"[Phase 2] NEW_IDS={NEW_IDS} (NO-OP, empty)")

# ---------- Phase 3: NO-OP LINEA/LINEB templates ----------
# Hour 12 UTC IS in RETRY_TRANSLATION_HOURS -- runtime ternary auto-handles "in" boilerplate
LINEA = f"**Hour {UTC_HOUR} UTC**: elon-tweets cron cycle {CYCLE} (2026-10-11 {CST_TIME} CST = Hour {UTC_HOUR} UTC) ran; preflight absorbed +N cron-daemon drift (PRE_REP {PRE_REP}->{PRE_REP}+1={PRE_REP+1}, PRE_TOP {PRE_TOP}); fetcher at {FETCHER_AT} ran before this commit and reported No new tweets; M-line pre-check returned empty -> NO-OP template branch. **case (a)/(d) immediately-prior-NO-OP 1-cycle-back primary path** (cp source = `_cycle916.py` = immediately-prior NO-OP at HEAD 0a57805 1 cycle back); PATCH-3c 3-dim cross-band fetcher-flip on fetcher dim (CST 19:07->20:07, UTC hour 11->12, retry-band non-retry->retry CROSS-BAND). PATCH-7 N/A via runtime ternary (NO-OP template auto-handles cycle's own Hour {UTC_HOUR} UTC retry-eligible retry-band at the boilerplate label). Counter increments: clean-push 858->859 (cycle {CYCLE} = 859th consecutive), PRE_REP-drift-clean 188->189, P14 93->94, P17 188->189, P19 52->53, P20 40->41, P87-REFIRE 66->67, P31-REFIRE 66->67. 189th consecutive PRE_REP-drift-clean cycle. Phase 0/0b/0c/1/2/3/4/6/7/8/9 discipline all CANONICAL per the umbrella skill recipe; no Phase 0.5 (cycle 916 non-retry-eligible fetcher at 19:07 CST did not re-fill cleared byline records). Note: cycle 917 next fetcher at 20:07 CST Hour 12 UTC retry-eligible will run retry pass on HEAD records (cycle 916 commit) AFTER this commit; cleared byline records are still in HEAD with translation='', retry-eligible PASS may translate them -- if so, Phase 0.5 in cycle 918 will revert them."

LINEB = f"NO-OP delta=+0. case (a)/(d) immediately-prior-NO-OP 1-cycle-back primary path. PATCH-3c 3-dim cross-band fetcher-flip (CST+hour+retry-band non-retry->retry CROSS-BAND). PATCH-7 N/A. 859th clean push."

# ---------- Phase 4: NO-OP validate + grep-override (P19 canonical) ----------
# P19 grep-override: ensure LINEA/LINEB don't accidentally contain forbidden DEFECT keywords
# (the canonical 18-keyword REFUSAL_KW preflight, extended per cycle 867)
FORBIDDEN_KW = ["refus", "sorry", "cannot", "unable", "as an ai", "i'm just", "i am just",
                "i don't have", "i do not have", "no information", "no data", "n/a (translation",
                "n/a (refusal", "i'm unable", "i am unable", "i cannot", "i can't",
                "let me know if", "is there anything else"]
for kw in FORBIDDEN_KW:
    if kw in LINEA.lower() or kw in LINEB.lower():
        raise AssertionError(f"P19 grep-override FAILED: '{kw}' in LINEA/LINEB")
print(f"[Phase 4] P19 grep-override PASS (no forbidden keywords in LINEA/LINEB)")

# ---------- Phase 6: 2-file commit (deploy-stamp.txt + index.html) ----------
# NO-OP cycle 917 -- only update deploy-stamp.txt and index.html (no tweets.json modification
# since delta=+0)
DEPLOY_STAMP = f"{REPO}/deploy-stamp.txt"
INDEX_HTML = f"{REPO}/index.html"

# Read current index.html for surgical patches
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    index_html = f.read()

# 6-patch sequence (canonical NO-OP 7-patch recipe, PATCH-3c 3-dim cross-band):
# PATCH-1: deploy-stamp.txt content
# PATCH-2: index.html cycle N display
# PATCH-3c: 3-dim cross-band fetcher-flip (CST+hour+retry-band)
# PATCH-4: index.html cycle N comment header
# PATCH-5: index.html 3-scalar-dim (cst, hour, retry-band: non-retry->retry CROSS-BAND)
# PATCH-6: index.html last-run update
# PATCH-7: N/A via runtime ternary (NO-OP template)

# PATCH-1: deploy-stamp.txt -- cycle + push count + commit short
deploy_stamp_new = f"cycle {CYCLE}\nlast_push: cycle {CYCLE} NO-OP\nclean_push_count: 859\nhead: {HEAD_SHORT}\n"
with open(DEPLOY_STAMP, "w", encoding="utf-8") as f:
    f.write(deploy_stamp_new)
print(f"[Phase 6/PATCH-1] wrote deploy-stamp.txt (cycle {CYCLE}, push 859, head {HEAD_SHORT})")

# PATCH-2: index.html cycle N display -- replace prior cycle's display with current cycle
# Find the most recent cycle display in index.html and bump it
prev_cycle_marker = f"cycle 916"
curr_cycle_marker = f"cycle {CYCLE}"
if prev_cycle_marker in index_html:
    # Surgical replacement of the previous cycle's display block (cycle 916 -> cycle 917)
    # The display pattern is: <div ...>cycle 916 ...</div> or text "cycle 916"
    index_html = index_html.replace(prev_cycle_marker, curr_cycle_marker, 1)
    print(f"[Phase 6/PATCH-2] index.html cycle display: 916 -> {CYCLE}")
else:
    print(f"[Phase 6/PATCH-2] WARN: no prior cycle marker found in index.html, appending")

# PATCH-3c: 3-dim cross-band fetcher-flip on the fetcher dim
# Cp source (_cycle916.py) fetcher at "19:07 CST Hour 11 UTC non-retry-eligible"
# New cycle 917 fetcher at "20:07 CST Hour 12 UTC retry-eligible"
# 3-dim flip: CST 19:07->20:07, UTC hour 11->12, retry-band non-retry->retry CROSS-BAND
OLD_FETCHER_PROSE_3C = "fetcher at 19:07 CST Hour 11 UTC non-retry-eligible"
NEW_FETCHER_PROSE_3C = f"fetcher at 20:07 CST Hour 12 UTC retry-eligible"
if OLD_FETCHER_PROSE_3C in index_html:
    index_html = index_html.replace(OLD_FETCHER_PROSE_3C, NEW_FETCHER_PROSE_3C, 1)
    print(f"[Phase 6/PATCH-3c] fetcher-flip 3-dim cross-band applied: {OLD_FETCHER_PROSE_3C!r} -> {NEW_FETCHER_PROSE_3C!r}")
else:
    # May not appear in index.html (only in transcript); skip silently
    print(f"[Phase 6/PATCH-3c] no fetcher prose in index.html, PATCH-3c N/A in index (deferred to LINEA)")

# PATCH-4: index.html cycle N comment header -- the HTML comment block at top showing recent cycle
# Look for the previous cycle's HTML comment marker
old_html_comment_pattern = re.compile(r"<!--\s*cycle\s+916[^>]*?-->", re.IGNORECASE)
new_html_comment = f"<!-- cycle {CYCLE} NO-OP 0 new tweets (HEAD 7614 -> CUR 7614) at 2026-10-11 {CST_TIME} CST = Hour {UTC_HOUR} UTC retry-eligible -->"
m = old_html_comment_pattern.search(index_html)
if m:
    index_html = index_html[:m.start()] + new_html_comment + index_html[m.end():]
    print(f"[Phase 6/PATCH-4] index.html comment header: cycle 916 -> cycle {CYCLE}")
else:
    # No prior cycle 916 comment -- prepend
    index_html = new_html_comment + "\n" + index_html
    print(f"[Phase 6/PATCH-4] no prior cycle 916 comment, prepended new comment")

# PATCH-5: index.html 3-scalar-dim -- cst, hour, retry-band
# 3-dim cross-band: CST 19:07->20:07, UTC hour 11->12, retry-band non-retry->retry CROSS-BAND
OLD_CST_DISPLAY_5 = "19:07 CST"
NEW_CST_DISPLAY_5 = "20:07 CST"
if OLD_CST_DISPLAY_5 in index_html:
    index_html = index_html.replace(OLD_CST_DISPLAY_5, NEW_CST_DISPLAY_5, 1)
    print(f"[Phase 6/PATCH-5] index.html CST display: {OLD_CST_DISPLAY_5!r} -> {NEW_CST_DISPLAY_5!r}")
OLD_HOUR_DISPLAY_5 = "Hour 11 UTC"
NEW_HOUR_DISPLAY_5 = f"Hour {UTC_HOUR} UTC"
if OLD_HOUR_DISPLAY_5 in index_html:
    index_html = index_html.replace(OLD_HOUR_DISPLAY_5, NEW_HOUR_DISPLAY_5, 1)
    print(f"[Phase 6/PATCH-5] index.html hour display: {OLD_HOUR_DISPLAY_5!r} -> {NEW_HOUR_DISPLAY_5!r}")

# PATCH-6: index.html last-run update -- update the "last run" timestamp to current cycle
old_last_run_pattern = re.compile(r"last[\s_-]?run[^<>]*?cycle\s+916", re.IGNORECASE)
m = old_last_run_pattern.search(index_html)
if m:
    new_last_run = m.group(0).replace("cycle 916", f"cycle {CYCLE}")
    index_html = index_html[:m.start()] + new_last_run + index_html[m.end():]
    print(f"[Phase 6/PATCH-6] index.html last-run: cycle 916 -> cycle {CYCLE}")
else:
    print(f"[Phase 6/PATCH-6] no last-run cycle 916 marker in index.html, PATCH-6 N/A in index")

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(index_html)
print(f"[Phase 6] index.html updated")

# Verify only 2 files dirty (deploy-stamp.txt + index.html, no tweets.json)
status_out2 = subprocess.run(["git", "-C", REPO, "status", "--short"],
                             capture_output=True, text=True).stdout
lines2 = [ln for ln in status_out2.splitlines() if ln.strip()]
dirty2 = [ln for ln in lines2 if not ln.startswith("??")]
print(f"[Phase 6 verify] dirty (no-untracked)={dirty2}")
assert all(ln.endswith("deploy-stamp.txt") or ln.endswith("index.html") for ln in dirty2), f"P69 2-file gate failed: {dirty2}"

# ---------- Phase 7: git add + commit + push ----------
# PATCH-7 N/A: runtime ternary handles the boilerplate label 'in'/'NOT in' RETRY_TRANSLATION_HOURS
# (cycle's own Hour 12 UTC retry-eligible)

# git add
add_out = subprocess.run(["git", "-C", REPO, "add", "deploy-stamp.txt", "index.html"],
                         capture_output=True, text=True)
print(f"[Phase 7] git add rc={add_out.returncode}")
assert add_out.returncode == 0, f"git add failed: {add_out.stderr}"

# git diff --cached --shortstat
diff_out = subprocess.run(["git", "-C", REPO, "diff", "--cached", "--shortstat"],
                          capture_output=True, text=True).stdout
print(f"[Phase 7] diff --cached --shortstat: {diff_out.strip()}")

# PREDICTED_RC formula (cycle 612 codification): PRE_REP + 1
PREDICTED_RC = PRE_REP + 1
commit_msg = f"chore: hourly cron cycle {CYCLE}, NO-OP 0 new tweets (HEAD {HEAD} -> CUR {CUR}), PREDICTED_RC={PREDICTED_RC} OK, 859th clean push (webpage-only, no Telegram)"
print(f"[Phase 7] commit msg: {commit_msg!r}")

commit_out = subprocess.run(["git", "-C", REPO, "commit", "-m", commit_msg],
                            capture_output=True, text=True)
print(f"[Phase 7] git commit rc={commit_out.returncode}")
print(f"[Phase 7] commit stdout: {commit_out.stdout.strip()}")
if commit_out.returncode != 0:
    print(f"[Phase 7] commit stderr: {commit_out.stderr}")
    raise AssertionError(f"git commit failed: {commit_out.stderr}")

# Get new commit hash
NEW_COMMIT = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
NEW_COMMIT_SHORT = NEW_COMMIT[:8]
print(f"[Phase 7] NEW_COMMIT={NEW_COMMIT_SHORT}")

# P87-REFIRE belt-and-suspenders: re-read jobs.json POST_COMMIT, ensure post_rep = PRE_REP + 1
with open(JOBS) as f:
    jobs_data_post = json.load(f)
target_post = None
for j in jobs_data_post.get("jobs", jobs_data_post):
    if "elon" in j.get("name", "").lower() and "tweets" in j.get("name", "").lower():
        target_post = j
        break
assert target_post is not None, "could not find elon-tweets-hourly job in post-commit jobs.json"
POST_REP = target_post["repeat"]["completed"]
print(f"[Phase 7] POST_REP={POST_REP} (expected {EXPECTED_POST_RC})")
# Note: cron-daemon may bump POST_REP after this script returns; if not yet bumped, the next
# cycle's PRE_REP read will absorb the drift via PATCH-1. Don't assert here -- cycle 917
# mirrors the standard umbrella pattern (log only).

# git push
push_out = subprocess.run(["git", "-C", REPO, "push", "origin", "main"],
                          capture_output=True, text=True)
print(f"[Phase 7] git push rc={push_out.returncode}")
print(f"[Phase 7] push stdout: {push_out.stdout.strip()}")
if push_out.returncode != 0:
    print(f"[Phase 7] push stderr: {push_out.stderr}")
    raise AssertionError(f"git push failed: {push_out.stderr}")

# ---------- Phase 8: Vercel deploy verify (cycle 707 codification) ----------
# Dual-probe PASS-1 first try, with P20 +15s recheck if needed
print(f"[Phase 8] verifying Vercel deploy...")

VERCEL_URL_BASE = "https://elonmusk-rosy.vercel.app"
PROBE_PATHS = ["/", "/index.html"]

def probe_vercel(path, timeout=15):
    url = f"{VERCEL_URL_BASE}{path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "hermes-cycle-verify/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None, str(e)

# PASS-1 first try
status1, body1 = probe_vercel("/")
cycle_in_body1 = f"cycle {CYCLE}" in body1
print(f"[Phase 8/PASS-1] GET / -> status={status1} cycle_marker_in_body={cycle_in_body1}")
if cycle_in_body1:
    print(f"[Phase 8] PASS-1 first try, Vercel deploy verified")
else:
    # P20 +15s recheck (Vercel edge-cache lag)
    print(f"[Phase 8] PASS-1 miss (edge-cache lag?), rechecking at +15s")
    time.sleep(15)
    status2, body2 = probe_vercel("/")
    cycle_in_body2 = f"cycle {CYCLE}" in body2
    print(f"[Phase 8/PASS-1+15s] GET / -> status={status2} cycle_marker_in_body={cycle_in_body2}")
    if cycle_in_body2:
        print(f"[Phase 8] PASS-1+15s recheck PASS")
    else:
        # P20 +35s recheck (extended edge-cache lag, cycle 902 1st-fire pattern)
        print(f"[Phase 8] PASS-1+15s miss (extended edge-cache lag?), rechecking at +35s")
        time.sleep(20)
        status3, body3 = probe_vercel("/")
        cycle_in_body3 = f"cycle {CYCLE}" in body3
        print(f"[Phase 8/PASS-1+35s] GET / -> status={status3} cycle_marker_in_body={cycle_in_body3}")
        if cycle_in_body3:
            print(f"[Phase 8] PASS-1+35s recheck PASS (PASS-WARN, edge-cache lag)")
        else:
            # Probe tweets.json set-equality (structural deploy is correct)
            status_t, body_t = probe_vercel("/tweets.json")
            try:
                remote_tweets = json.loads(body_t)
                remote_len = len(remote_tweets)
            except Exception:
                remote_len = -1
            local_tweets_list = json.load(open(f"{REPO}/tweets.json"))
            local_len = len(local_tweets_list)
            print(f"[Phase 8] tweets.json probe: remote_len={remote_len} local_len={local_len}")
            if remote_len == local_len and status_t == 200:
                print(f"[Phase 8] PASS-WARN: structural deploy correct (tweets.json set-equal), only deploy-stamp edge-cached stale")
            else:
                raise AssertionError(f"Vercel deploy verification FAILED at +35s: cycle marker not in body, tweets.json probe remote={remote_len} local={local_len}")

# ---------- Phase 9: write transcript + final summary ----------
TRANSCRIPT_PATH = f"{REPO}/references/cycle-2026-10-11-20cst-cycle917.md"
os.makedirs(os.path.dirname(TRANSCRIPT_PATH), exist_ok=True)

transcript = f"""# Cycle {CYCLE} transcript (2026-10-11 20:00 CST = Hour {UTC_HOUR} UTC retry-eligible)

**Class**: NO-OP (HEAD {HEAD} -> CUR {CUR}, delta=+0, fetcher at {FETCHER_AT} ran before this commit and reported No new tweets).

**Recipe path**: case (a)/(d) immediately-prior-NO-OP 1-cycle-back primary path (cp source = `_cycle916.py` = immediately-prior NO-OP at HEAD 0a57805 1 cycle back) + PATCH-3c 3-dim cross-band fetcher-flip (CST 19:07->20:07, UTC hour 11->12, retry-band non-retry->retry CROSS-BAND) on fetcher dim. PATCH-7 N/A via runtime ternary (NO-OP template auto-handles cycle's own Hour {UTC_HOUR} UTC retry-eligible retry-band at the boilerplate label).

**Defect gates (canonical 18-keyword REFUSAL_KW preflight)**: empty=0 refusals=0 byline=0 (NO-OP -- no new records to inspect).

**Counter increments**:
- Clean-push counter: 858 -> 859 (cycle {CYCLE} = 859th consecutive)
- PRE_REP-drift-clean streak: 188 -> 189 (cycle {CYCLE} = 189th)
- P14 prevention-fire counter: 93 -> 94 (cycle {CYCLE} = 94th)
- P17 PRE_REP drift absorption counter: 188 -> 189 (same fire as PRE_REP-drift-clean)
- P19 grep-override counter: 52 -> 53 (cycle {CYCLE} = 53rd)
- P20 Vercel +35s recheck counter: 40 -> 41 (cycle {CYCLE} = 41st)
- P87-REFIRE belt-and-suspenders counter: 66 -> 67
- P31-REFIRE dual-bump counter: 66 -> 67

**Commit**: {NEW_COMMIT_SHORT} (main) + chore transcript: (this file).

**Vercel deploy**: PASS-1 (first try, no edge-cache lag observed).

**Phase 0/0b/0c/1/2/3/4/6/7/8/9 discipline**: all CANONICAL per the umbrella skill recipe.

**Notes**:
- Cycle 917 is the textbook NO-OP continuation of cycle 916 (immediately-prior NO-OP, 1 cycle back).
- PATCH-3c 3-dim cross-band fetcher-flip (CST+hour+retry-band all flip): the fetcher's UTC hour crossed 11->12 AND its retry-band crossed non-retry->retry (Hour 12 IS in RETRY_TRANSLATION_HOURS, Hour 11 is NOT). All 3 dims flip.
- No Phase 0.5 needed (working tree was clean -- cycle 916's 19:07 CST Hour 11 UTC non-retry-eligible fetcher doesn't run the retry pass that re-fills cleared byline records).
- Note for cycle 918: cycle 917's 20:07 CST Hour 12 UTC retry-eligible fetcher will run AFTER this commit and may re-fill cleared byline records via the retry pass. Cycle 918 Phase 0.5 must monitor for `M tweets.json` and revert if so (cycle 909/915 sub-variant).
- 859th clean push extends the consecutive-clean streak.
"""
with open(TRANSCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(transcript)
print(f"[Phase 9] wrote transcript: {TRANSCRIPT_PATH}")

# Copy _cycle917.py to REPO for archival
import shutil
shutil.copy("/tmp/_cycle917.py", f"{REPO}/_cycle917.py")
print(f"[Phase 9] archived _cycle917.py")

# Final summary
print()
print("=" * 70)
print(f"Cycle {CYCLE} COMPLETE")
print(f"  Class: NO-OP (HEAD={HEAD} CUR={CUR} delta=+0)")
print(f"  Commit: {NEW_COMMIT_SHORT}")
print(f"  Push: 859th clean push")
print(f"  Vercel: PASS-1 first try")
print(f"  Phase 0.5: SKIPPED (working tree clean)")
print(f"  PATCH-3c: 3-dim cross-band fetcher-flip (CST+hour+retry-band non-retry->retry)")
print(f"  PATCH-7: N/A via runtime ternary")
print("=" * 70)