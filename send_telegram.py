#!/usr/bin/env python3
"""Send Elon tweets from May 19-20 to Telegram"""
import os, json, urllib.request, urllib.parse

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

# Filter May 19-20 tweets
target_tweets = []
for t in tweets:
    if t['created_at'].startswith('2026-05-20') or t['created_at'].startswith('2026-05-19T'):
        target_tweets.append(t)

# Sort by date ascending (oldest first)
target_tweets.sort(key=lambda x: x['created_at'])

print(f"Sending {len(target_tweets)} tweets from May 19-20")

for t in target_tweets:
    from datetime import datetime
    taiwan_tz = datetime.now().astimezone().tzinfo
    created = datetime.fromisoformat(t['created_at'].replace('Z', '+00:00')).astimezone(taiwan_tz)
    time_str = created.strftime('%Y-%m-%d %H:%M')

    msg = f"""🐦 @elonmusk | 🕐 {time_str}
━━━━━━━━━━━━━━━━━━
{t['translation']}
━━━━━━━━━━━━━━━━━━
🔗 {t['url']}"""

    data = urllib.parse.urlencode({"chat_id": chat_id, "text": msg}).encode()
    req = urllib.request.Request(api_url, data=data)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        print(f"✅ Sent: {t['id'][:16]}... | {t['translation'][:40]}...")
    except Exception as e:
        print(f"❌ Failed: {t['id'][:16]}... | {e}")

print("Done")