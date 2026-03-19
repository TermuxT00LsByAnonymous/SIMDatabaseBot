# 📱 SimDatabaseBot

A Telegram bot built with Python that allows users to search SIM database information with daily limits, VIP system, and force channel join system.

## 🚀 Features

- 🔍 SIM database lookup
- 👥 Force join channels before using bot
- 💎 VIP system (Unlimited searches)
- 🎁 Daily free search limit
- 💰 Payment system (JazzCash / EasyPaisa)
- 📊 User database (SQLite)
- 📝 Search history saving
- ⏳ Auto delete results for privacy
- 🛡 Admin controls

## 🛠 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## 📦 Dependencies

Main libraries used:

- python-telegram-bot
- aiohttp
- aiosqlite
- asyncio

## ⚙️ Configuration

Before running the bot, edit these values in the script:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"

CHANNEL_1 = "@YOUR_CHANNEL"
CHANNEL_2 = "@YOUR_CHANNEL"

ADMIN_ID = YOUR_ID
ADMIN_USERNAME = "YOUR_USERNAME"

API_URL = "YOUR_API"

VIP_PRICE = "300 PKR"

JAZZCASH_NUMBER = "YOUR_NUMBER"
EASYPAISA_NUMBER = "YOUR_NUMBER"
```

## ▶️ Running the Bot

Run the bot with:

```bash
python SimDataBase.py
```

## 📊 Limits

- Free users: 5 searches per day
- VIP users: Unlimited searches

## 💎 VIP System

Users can buy VIP for unlimited searches.

Payment Methods:
- JazzCash
- EasyPaisa

(Admin manually approves VIP)

## 🗄 Database

Bot automatically creates:

```
bot.db
```

Tables:
- users
- history

## 🔐 Privacy

- Results auto delete after some time
- Search history stored for admin use
- No public data sharing

## 👨‍💻 Developer

Telegram: @I_Dont_Know99999

## ⚠️ Disclaimer

This bot is for educational purposes only. Developer is not responsible for misuse.

## ⭐ Support

If you like this project, consider giving it a star on GitHub.
