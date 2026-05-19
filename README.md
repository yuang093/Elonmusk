# 🦁 Elon Musk 推文追蹤

自動追蹤 [Elon Musk (@elonmusk)](https://x.com/elonmusk) 的推文，翻譯成繁體中文，即時推播到 Telegram。

---

## 功能

- ✅ 每小時自動檢查新推文
- 🌏 輕鬆風格繁中翻譯（保留梗和網路用語）
- 📱 Telegram 即時推播（新推文不管幾則都翻譯發送）
- 📊 網頁列表展示歷史記錄（原文 + 翻譯）

---

## 部署方式

### 1. GitHub → Vercel 自動部署

把你的 GitHub repository 連動 Vercel：

1. 進入 [vercel.com](https://vercel.com) → New Project
2. Import GitHub → 選擇 `yuang093/Elonmusk` 這個 repo
3. Framework Preset 選 **Other**
4. Build Command 留空
5. Output Directory 填 `.`
6. 點 Deploy

> ⚠️ 注意：目前只有 `index.html` 和 `fetch_tweets.py`，沒有實際部署到 Vercel 的設定。你需要手動連動 repo。

---

## 本地開發 / 測試

### 安裝依賴

```bash
pip install requests python-dotenv
```

### 設定 `.env`

在專案根目錄建立 `.env` 檔案：

```env
# X API v2 (申請：developer.twitter.com)
X_BEARER_TOKEN=your_bearer_token_here

# Telegram Bot
TG_BOT_TOKEN=your_telegram_bot_token
TG_CHAT_ID=your_telegram_chat_id

# 翻譯 API（MiniMax 優先）
MINIMAX_API_KEY=your_minimax_api_key
```

### 手動執行

```bash
python fetch_tweets.py
```

---

## 所需 API Key 說明

| Key | 用途 | 哪裡申請 |
|---|---|---|
| `X_BEARER_TOKEN` | 讀取 Elon 公開推文 | [developer.twitter.com](https://developer.twitter.com) |
| `TG_BOT_TOKEN` | 發送 Telegram 通知 | @BotFather |
| `TG_CHAT_ID` | 你的 Telegram ID | @userinfobot |
| `MINIMAX_API_KEY` | 翻譯推文 | MiniMax Console |

---

## 自行部署 Vercel Python Cron（每小時）

如需在 Vercel 上跑 `fetch_tweets.py`，需使用 **Vercel Cron**：

1. 在 repo 根目錄建立 `vercel.json`
2. 建立 `api/cron.py`（轉發 `fetch_tweets.py` 邏輯）
3. Git push → Vercel 自動部署，Cron 觸發時執行

需要的話可以找我幫你寫這些設定 👍

---

## 目前進度

- [x] 前端網頁（index.html + tweets.json）
- [x] Python 爬蟲翻譯腳本
- [ ] X API Key 設定
- [ ] Telegram Bot 設定
- [ ] Vercel 部署
- [ ] 每小時 Cron Job 啟動

---

有任何問題問我 🙌