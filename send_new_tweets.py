#!/usr/bin/env python3
"""Send tweets fetched in the last N minutes to Telegram."""
import json, urllib.request, urllib.parse
from datetime import datetime, timedelta

env_vars = {}
with open('.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env_vars[k] = v

bot_token = env_vars.get('TG_BOT_TOKEN', '')
chat_id = env_vars.get('TG_CHAT_ID', '')
api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

with open('tweets.json') as f:
    tweets = json.load(f)

cutoff = (datetime.now() - timedelta(minutes=10)).astimezone().isoformat()
new_tweets = [t for t in tweets if t.get('fetched_at', '') >= cutoff]
new_tweets.sort(key=lambda x: x['created_at'])

print(f"Sending {len(new_tweets)} new tweets (cutoff={cutoff})")

taiwan_tz = datetime.now().astimezone().tzinfo
sent = 0
for t in new_tweets:
    created = datetime.fromisoformat(t['created_at'].replace('Z', '+00:00')).astimezone(taiwan_tz)
    time_str = created.strftime('%Y-%m-%d %H:%M')
    original = t.get('original', '')
    translation = t.get('translation', '')
    type_marker = ""
    if t.get('is_quote'):
        type_marker = "❝ 引用 "
    elif t.get('is_retweet'):
        type_marker = "🔁 轉推 "

    msg = f"""{type_marker}🦁 <b>Elon Musk</b> | 🕐 {time_str}
━━━━━━━━━━━━━━━━━━
📝 原文：
{original}
━━━━━━━━━━━━━━━━━━
🌏 繁中翻譯：
{translation}
━━━━━━━━━━━━━━━━━━
🔗 {t.get('url', '')}"""

    data = urllib.parse.urlencode({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(api_url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            if result.get('ok'):
                sent += 1
                print(f"OK Sent: {t['id'][:16]}... | {translation[:50]}")
            else:
                print(f"ERR Failed: {t['id'][:16]}... | {result}")
    except Exception as e:
        print(f"ERR Error: {t['id'][:16]}... | {e}")

print(f"\nDone. Sent {sent}/{len(new_tweets)}")