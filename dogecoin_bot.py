import os, json, requests, telebot

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 8938541719
CENTRAL_DOGE_ADDRESS = "D9CyxEDc8aEvrhu4HDCTfwz33vL6YtpcYX"

bot = telebot.TeleBot(TOKEN)
DB_FILE = "users.json"

def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(f, db)

def get_user(uid):
    db = load_db()
    uid = str(uid)
    if uid not in db:
        db[uid] = {"balance": 0.0}
        save_db(db)
    return db[uid]

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"🐶 *DOGE INVEST BOT LIVE!*\n\nWelcome {m.from_user.first_name}!\n\n💰 /deposit - Deposit DOGE\n📊 /balance - Check Balance\n💸 /withdraw - Withdraw DOGE\n\nYour ID: `{m.from_user.id}`\n\nMin Deposit: 5 DOGE", parse_mode="Markdown")

@bot.message_handler(commands=['deposit'])
def deposit(m):
    get_user(m.from_user.id)
    bot.send_message(m.chat.id, f"💰 *DEPOSIT DOGECOIN*\n\nSend DOGE to:\n\n`{CENTRAL_DOGE_ADDRESS}`\n\nClick to copy address ^^\n\n⚠️ After sending:\n1. Wait for 1 confirmation (~1 min)\n2. Forward TXID to admin or send /balance\n3. Admin will credit you\n\nMinimum: 5 DOGE", parse_mode="Markdown")

@bot.message_handler(commands=['balance'])
def balance(m):
    u = get_user(m.from_user.id)
    bot.send_message(m.chat.id, f"📊 *Your Balance*\n\n💰 {u.get('balance',0)} DOGE\n\n💰 /deposit to add more\n💸 /withdraw to cash out", parse_mode="Markdown")

@bot.message_handler(commands=['withdraw'])
def withdraw(m):
    parts = m.text.split()
    if len(parts) < 3:
        bot.reply_to(m, "❌ Use:\n/withdraw AMOUNT ADDRESS\n\nExample:\n/withdraw 10 D9CyxEDc8aEvrhu4HDCTfwz33vL6YtpcYX")
        return
    amount = parts[1]
    addr = parts[2]
    u = get_user(m.from_user.id)

    # Check balance
    try:
        if float(amount) > float(u.get('balance',0)):
            bot.reply_to(m, f"❌ Insufficient balance. You have {u.get('balance',0)} DOGE")
            return
    except:
        bot.reply_to(m, "❌ Invalid amount")
        return

    bot.send_message(m.chat.id, f"✅ *Withdrawal Requested*\n\nAmount: {amount} DOGE\nTo: `{addr}`\n\n⏳ Admin will process within 24h", parse_mode="Markdown")

    # Notify admin
        try:
        msg = f"NEW WITHDRAWAL\nUser: {m.from_user.id} @{m.from_user.username}\nAmount: {amount} DOGE\nAddr: {addr}\nBal: {u.get('balance',0)}"
        bot.send_message(ADMIN_ID, msg)
    except:
        pass
