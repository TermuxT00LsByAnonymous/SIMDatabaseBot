import shutil
import os

# __pycache__ delete karne ka automatic code
for root, dirs, files in os.walk("."):
    for d in dirs:
        if d == "__pycache__":
            shutil.rmtree(os.path.join(root, d))
            print(f"Deleted {os.path.join(root, d)}")

# Baaki imports
import aiohttp
import aiosqlite
import asyncio
import re
from datetime import date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# ----------------- CONFIG -----------------
BOT_TOKEN = "8655740565:AAHGDlK53266pFTp3bTUY42j1n-MSqx9mAQ"
CHANNEL_1 = "@TERMUXTOOLSHUB"
CHANNEL_2 = "@LearnWithHassanOfc"
ADMIN_ID = 7383542259
ADMIN_USERNAME = "I_Dont_Know99999"
API_URL = "https://amscript.xyz/PublicApi/Siminfo.php"
VIP_PRICE = "300 PKR"
JAZZCASH_NUMBER = "03211676081 Iram Shahzadi"
EASYPAISA_NUMBER = "03216774865 Habib Ur Rehman"
DAILY_LIMIT = 5
AUTO_DELETE_SEC = 300
pending_payment = {}
# -----------------------------------------

# ---------------- DATABASE ----------------
async def init_db():
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            vip INTEGER DEFAULT 0,
            daily INTEGER DEFAULT 0,
            last_date TEXT
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS history(
            user_id INTEGER,
            query TEXT
        )
        """)
        await db.commit()

async def add_user(uid):
    async with aiosqlite.connect("bot.db") as db:
        await db.execute(
            "INSERT OR IGNORE INTO users(id,last_date) VALUES(?,?)",
            (uid,str(date.today()))
        )
        await db.commit()
# -----------------------------------------

# ---------------- HELPERS ----------------
def clean_number(text):
    d = re.sub(r"\D","",text)
    if d.startswith("92"):
        d = "0"+d[2:]
    elif len(d)==10:
        d = "0"+d
    return d

async def check_channels(bot, uid):
    m1 = await bot.get_chat_member(CHANNEL_1, uid)
    m2 = await bot.get_chat_member(CHANNEL_2, uid)
    return m1.status in ["member","administrator","creator"] and \
           m2.status in ["member","administrator","creator"]

async def is_vip(uid):
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT vip FROM users WHERE id=?", (uid,)) as c:
            r = await c.fetchone()
            return r and r[0]==1

async def reset_daily(uid):
    today = str(date.today())
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT last_date FROM users WHERE id=?", (uid,)) as c:
            r = await c.fetchone()
        if r and r[0] != today:
            await db.execute("UPDATE users SET daily=0,last_date=? WHERE id=?", (today,uid))
            await db.commit()

async def use_limit(uid):
    await reset_daily(uid)
    if await is_vip(uid):
        return True

    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT daily FROM users WHERE id=?", (uid,)) as c:
            r = await c.fetchone()

        if r and r[0] >= DAILY_LIMIT:
            return False

        await db.execute("UPDATE users SET daily=daily+1 WHERE id=?", (uid,))
        await db.commit()
    return True

async def remaining(uid):
    if await is_vip(uid):
        return "♾ Unlimited"

    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT daily FROM users WHERE id=?", (uid,)) as c:
            r = await c.fetchone()
    return DAILY_LIMIT - (r[0] if r else 0)

async def auto_delete(msg):
    await asyncio.sleep(AUTO_DELETE_SEC)
    try:
        await msg.delete()
    except:
        pass
# -----------------------------------------

# ---------------- COMMANDS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await add_user(uid)
    kb = [
        [InlineKeyboardButton("📢 Join Channel",url=f"https://t.me/{CHANNEL_1.replace('@','')}")],
        [InlineKeyboardButton("⚙️ Join Channel",url=f"https://t.me/{CHANNEL_2.replace('@','')}")],
        [InlineKeyboardButton("✅ Verify",callback_data="verify")]
    ]
    await update.message.reply_text(
        "👋 Welcome\nChannels join karo phir Verify karo.",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if await check_channels(context.bot, q.from_user.id):
        await q.edit_message_text("✅ Verified!\n📥 Number ya CNIC send karo.")
    else:
        await q.edit_message_text("❌ Pehle channels join karo.")

async def again(update, context):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text("📥 Number ya CNIC send karo.")

async def show_history(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute(
            "SELECT query FROM history WHERE user_id=? ORDER BY rowid DESC LIMIT 20",
            (uid,)
        ) as c:
            rows = await c.fetchall()
    if not rows:
        await q.message.reply_text("📜 History empty.")
        return
    txt = "📜 YOUR SEARCH HISTORY\n\n"
    for i,r in enumerate(rows,1):
        txt += f"{i}️⃣ {r[0]}\n"
    await q.message.reply_text(txt)

async def buy_vip(update, context):
    q = update.callback_query
    await q.answer()
    msg=f"""
💎 VIP MEMBERSHIP
Price: {VIP_PRICE}
💳 JazzCash: {JAZZCASH_NUMBER}
💰 Easypaisa: {EASYPAISA_NUMBER}
"""
    kb=[[InlineKeyboardButton("✅ I Have Paid",callback_data="paid")]]
    await q.message.reply_text(msg,reply_markup=InlineKeyboardMarkup(kb))

async def paid(update, context):
    q=update.callback_query
    await q.answer()
    await q.message.reply_text("📥 Admin ko payment screenshot bhejo @I_Dont_Know99999")

async def add_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("UPDATE users SET vip=1 WHERE id=?", (uid,))
        await db.commit()
    await update.message.reply_text("✅ User VIP bana diya.")
    await context.bot.send_message(uid,"🎉 You are VIP now!")

async def remove_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("UPDATE users SET vip=0 WHERE id=?", (uid,))
        await db.commit()
    await update.message.reply_text("❌ VIP removed.")
    await context.bot.send_message(uid,"❌ VIP removed.")

async def admin_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = int(context.args[0])
    text = " ".join(context.args[1:])
    await context.bot.send_message(uid,f"📢 Admin Message:\n\n{text}")
    await update.message.reply_text("✅ Message sent.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not await check_channels(context.bot, uid):
        await update.message.reply_text("❌ Channel join required.")
        return
    if not await use_limit(uid):
        await update.message.reply_text("❌ Daily limit finished.")
        return
    text = update.effective_message.text
    number = clean_number(text)
    loading = await update.message.reply_text("⚡ Initializing Cyber Scan...")
    frames = [
        "🔊 Scanning Name 🕵🏻‍♂️..........",
        "🔊 Matching Number 📱..........",
        "🔊 Searching 🔍 Cnic 💳............",
        "🔊 Searching Adress 🗺️................."
    ]
    for f in frames:
        await asyncio.sleep(0.9)
        try:
            await loading.edit_text(f)
        except:
            pass
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params={"number": number}) as r:
            result = await r.json()
    records = result.get("data", [])
    if not records:
        await loading.edit_text("❌ No record.")
        return
    await loading.delete()
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("INSERT INTO history VALUES(?,?)",(uid,number))
        await db.commit()
    total=len(records)
    for i,item in enumerate(records,1):
        rem=await remaining(uid)
        vip_text="💎 VIP Unlimited" if await is_vip(uid) else "⭐ VIP Available"
        msg=f"""
╔══════════════════════════════════╗
     🔍 𝗦𝗜𝗠 𝗗𝗮𝘁𝗮 𝗥𝗲𝘀𝘂𝗹𝘁
╚══════════════════════════════════╝
🔍𝗥𝗲𝘀𝘂𝗹𝘁 ➜ {i}/{total}
👤 NAME ➤ {item.get('full_name','N/A')}
📱 NUMBER ➤ {item.get('phone','N/A')}
💳 CNIC ➤ {item.get('cnic','N/A')}
🏨 ADDRESS ➤ {item.get('address','N/A')}
⚡ REMAINING ➜ {rem}
💎 VIP STATUS ➜ {vip_text}
🔥 Search Result Completed
⚠️ Auto delete in {AUTO_DELETE_SEC} sec
"""
        kb=[
            [InlineKeyboardButton("🔎 Search Again",callback_data="again")],
            [InlineKeyboardButton("📜 History",callback_data="history")],
            [InlineKeyboardButton("💎 Buy VIP",callback_data="buyvip")],
            [InlineKeyboardButton("📞 Contact Admin",url=f"https://t.me/{ADMIN_USERNAME}")]
        ]
        m=await update.message.reply_text(msg,reply_markup=InlineKeyboardMarkup(kb))
        asyncio.create_task(auto_delete(m))
# -----------------------------------------

# ----------------- APP INIT -----------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addvip", add_vip))
app.add_handler(CommandHandler("removevip", remove_vip))
app.add_handler(CommandHandler("msg", admin_msg))

# CallbackQuery
app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
app.add_handler(CallbackQueryHandler(again, pattern="again"))
app.add_handler(CallbackQueryHandler(show_history, pattern="history"))
app.add_handler(CallbackQueryHandler(buy_vip, pattern="buyvip"))
app.add_handler(CallbackQueryHandler(paid, pattern="paid"))

# Text messages
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

# --------------- MAIN -----------------
async def main():
    await init_db()
    print("🔥 CYBER LEVEL BOT RUNNING...")
    await app.run_polling()

asyncio.run(main())
# -----------------------------------------
