# 🤖 SimDatabaseBot

<p align="center">
Telegram SIM Database Search Bot With VIP System
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.10-blue">
<img src="https://img.shields.io/badge/Telegram-Bot-blue">
<img src="https://img.shields.io/badge/Status-Online-success">
<img src="https://img.shields.io/badge/Version-2.0-orange">
</p>

---

## 📌 About Project

SimDatabaseBot is a powerful Telegram bot that allows users to search SIM owner details with daily free limits and VIP unlimited access.

This bot includes admin controls, payment system, and security protections.

---

## ✨ Main Features

🔍 Fast SIM Search  
💎 VIP Unlimited Searches  
🎁 Daily Reward System  
👥 Force Channel Join  
📊 User Statistics  
🗄 SQLite Database  
📜 Search History  
🛡 Admin Controls  
⏳ Auto Delete Results  

---

## 📜 Commands List

### User Commands

/start → Start bot  
/help → Commands list  
/profile → User info  
/daily → Free searches  
/balance → Check limit  
/search → Search data  
/vip → VIP purchase  
/support → Contact admin  

---

### Admin Commands

/admin → Admin panel  
/stats → Bot stats  
/broadcast → Send message  
/vipadd → Add VIP  
/vipremove → Remove VIP  

---

## 🖼 Screenshots

Add your bot screenshots here:

Example:

```
screenshots/start.png
screenshots/search.png
```

---

## ⚙ Configuration

Edit variables:

```
BOT_TOKEN = YOUR_TOKEN

ADMIN_ID = YOUR_ID

CHANNEL_1 = @CHANNEL
CHANNEL_2 = @CHANNEL

API_URL = YOUR_API

VIP_PRICE = 300

JAZZCASH = NUMBER
EASYPAISA = NUMBER
```

---

## 🛠 Termux Installation

If using Termux:

```
pkg update
pkg upgrade

pkg install python

pkg install git

git clone https://github.com/TermuxT00LsByAnonymous/SIMDatabaseBot.git

cd SimDatabaseBot

pip install -r requirements.txt

python SimDataBase.py
```

---

## 🖥 VPS Deployment

Ubuntu VPS setup:

```
sudo apt update

sudo apt install python3

sudo apt install python3-pip

git clone YOUR_REPO

cd SimDatabaseBot

pip3 install -r requirements.txt

python3 SimDataBase.py
```

For background run:

```
nohup python3 SimDataBase.py &
```

---

## 🗄 Database Structure

Database:
```
bot.db
```

Tables:

users table:
- user_id
- join_date
- searches
- vip_status

history table:
- user_id
- search_data
- date

---

## 🔐 Security Features

✔ Result auto delete  
✔ User tracking  
✔ Admin verification  
✔ Anti spam limits  
✔ Force join protection  

---

## 👨‍💻 Developer

Telegram:
@I_Dont_Know99999

---

## 📈 Future Updates

Possible updates:

API speed improvement  
Auto VIP system  
Referral system  
Coins system  
Web panel  

---

## ⚠ Disclaimer

This project is only for learning purposes.
Developer is not responsible for illegal usage.

---

## ⭐ Support Project

If you like this project:

⭐ Star the repository  
🍴 Fork project  
📢 Share with others  

---

## 📄 License

Personal Use License
