#!/usr/bin/env python3
import os, json
from openai import OpenAI

env_vars = {}
with open('.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env_vars[k] = v

api_key = env_vars.get('MINIMAX_API_KEY', '')
client = OpenAI(api_key=api_key, base_url='https://api.minimax.io/v1')

with open('tweets.json') as f:
    tweets = json.load(f)

broken = [t for t in tweets if t.get('translation') == t.get('original')]
print(f'Translating {len(broken)} tweets...')

SYSTEM_PROMPT = '你是一個翻譯專家。將以下推文翻譯成繁體中文，保持輕鬆、口語化的風格，保留梗和網路用語。不要翻譯人名。不要輸出任何思考過程，只直接輸出翻譯結果。'

for t in broken:
    text = t['original']
    print(f"  ID: {t['id']}")
    print(f"  Original: {text[:80]}...")
    try:
        resp = client.chat.completions.create(
            model='MiniMax-M2.7',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': text[:800]}
            ],
            temperature=0.7,
            max_tokens=500
        )
        t['translation'] = resp.choices[0].message.content.strip()
        print(f"  Translation: {t['translation'][:80]}...")
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
    print()

with open('tweets.json', 'w') as f:
    json.dump(tweets, f, ensure_ascii=False, indent=2)
print('Saved tweets.json')
