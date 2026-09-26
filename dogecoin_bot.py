import os
import json
import telebot

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 8938541719
CENTRAL_DOGE_ADDRESS = "D9CyxEDc8aEvrhu4HDCTfwz33vL6YtpcYX"

bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()
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
    text = f"DOGE BOT LIVE!\n\nHi {m.from_user.first_name}!\n\n/deposit - Deposit DOGE\n/balance - Check Balance\n/withdraw - Withdraw\n\nYour ID: {m.from_user.id}\nMin: 5 DOGE"
    bot.send_message(m.chat.id, text)

@bot.message_handler(commands=['deposit'])
def deposit(m):
    get_user(m.from_user.id)
    text = f"DEPOSIT DOGE\n\nSend DOGE to this address:\n{CENTRAL_DOGE_ADDRESS}\n\nAfter sending, wait 1 min and contact admin.\nMin 5 DOGE"
    bot.send_message(m.chat.id, text)

@bot.message_handler(commands=['balance'])
def balance(m):
    u = get_user(m.from_user.id)
    bal = u.get('balance', 0)
    bot.send_message(m.chat.id, f"Your Balance: {bal} DOGE\n\n/deposit to add more\n/withdraw to cash out")

@bot.message_handler(commands=['withdraw'])
def withdraw(m):
    parts = m.text.split()
    if len(parts) < 3:
        bot.reply_to(m, "Use: /withdraw AMOUNT ADDRESS\nExample: /withdraw 10 D9CyxEDc8aEvrhu4HDCTfwz33vL6YtpcYX")
        return
    amount = parts[1]
    addr = parts[2]
    u = get_user(m.from_user.id)
    try:
        if float(amount) > float(u.get('balance', 0)):
            bot.reply_to(m, f"Insufficient balance. You have {u.get('balance',0)} DOGE")
            return
    except:
        bot.reply_to(m, "Invalid amount")
        return
    bot.send_message(m.chat.id, f"Withdrawal Requested: {amount} DOGE to {addr}\nAdmin will process within 24h")
    try:
        bot.send_message(ADMIN_ID, f"NEW WITHDRAW\nUser: {m.from_user.id} @{m.from_user.username}\nAmount: {amount}\nAddr: {addr}\nBalance: {u.get('balance',0)}")
    except:
        pass

@bot.message_handler(commands
