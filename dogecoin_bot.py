import os, json, threading
from flask import Flask
import telebot

TOKEN = os.environ.get("TOKEN")
ADMIN = 8938541719
ADDR = "D9CyxEDc8aEvrhu4HDCTfwz33vL6YtpcYX"

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()

@app.route('/')
def home(): return "BOT LIVE - OK"

def load():
    try:
        with open("users.json","r") as f: return json.load(f)
    except: return {}
def save(d):
    with open("users.json","w") as f: json.dump(f,d)

@bot.message_handler(commands=['start','help'])
def s(m): bot.send_message(m.chat.id, "✅ BOT LIVE!\n\n/deposit - Deposit address\n/balance - Check balance\n/withdraw AMOUNT ADDRESS")

@bot.message_handler(commands=['deposit'])
def d(m): bot.send_message(m.chat.id, f"💰 SEND DOGE TO:\n\n`{ADDR}`\n\nMin: 5 DOGE\nAfter sending, admin will confirm.", parse_mode="Markdown")

@bot.message_handler(commands=['balance'])
def b(m):
    db=load(); bal=db.get(str(m.from_user.id),{}).get('bal',0)
    bot.send_message(m.chat.id, f"💼 Balance: {bal} DOGE")

@bot.message_handler(commands=['addbalance'])
def ab(m):
    if m.from_user.id!=ADMIN: return
    try:
        _,uid,amt=m.text.split(); db=load()
        if uid not in db: db[uid]={"bal":0}
        db[uid]["bal"]+=float(amt); save(db)
        bot.reply_to(m,f"Added {amt} to {uid}")
        bot.send_message(int(uid), f"✅ {amt} DOGE added to your balance!")
    except Exception as e: bot.reply_to(m,str(e))

def run_bot(): bot.infinity_polling(skip_pending=True)
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
