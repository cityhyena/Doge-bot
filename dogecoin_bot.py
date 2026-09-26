import os
import json
import telebot

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 8938541719
ADDR = "D9CyxEDc8aEvrhu4HDCTfwz33vL6YtpcYX"

bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()

def load():
    try:
        with open("users.json","r") as f:
            return json.load(f)
    except:
        return {}

def save(db):
    with open("users.json","w") as f:
        json.dump(f,db)

@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id,"BOT LIVE\n/deposit\n/balance\n/withdraw")

@bot.message_handler(commands=["deposit"])
def deposit(m):
    db=load()
    uid=str(m.from_user.id)
    if uid not in db:
        db[uid]={"bal":0}
        save(db)
    bot.send_message(m.chat.id,f"Send DOGE to:\n{ADDR}\nMin 5 DOGE")

@bot.message_handler(commands=["balance"])
def balance(m):
    db=load()
    uid=str(m.from_user.id)
    b=db.get(uid,{}).get("bal",0)
    bot.send_message(m.chat.id,f"Balance: {b} DOGE")

@bot.message_handler(commands=["withdraw"])
def withdraw(m):
    bot.send_message(m.chat.id,"Request received. Admin will process.")
    try:
        bot.send_message(ADMIN_ID,f"WITHDRAW REQ: {m.text} FROM {m.from_user.id}")
    except:
        pass

@bot.message_handler(commands=["addbalance"])
def add(m):
    if m.from_user.id!=ADMIN_ID:
        return
    try:
        a=m.text.split()
        uid=a[1]
        amt=float(a[2])
        db=load()
        if uid not in db:
            db[uid]={"bal":0}
        db[uid]["bal"]=db[uid].get("bal",0)+amt
        save(db)
        bot.reply_to(m,f"Added {amt} to {uid}")
        bot.send_message(int(uid),f"Deposit confirmed +{amt} DOGE")
    except Exception as e:
        bot.reply_to(m,str(e))

bot.infinity_polling(skip_pending=True)
