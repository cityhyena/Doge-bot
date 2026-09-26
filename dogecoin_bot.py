import os, json, telebot
TOKEN = os.environ.get("TOKEN")
ADMIN = 8938541719
ADDR = "D9CyxEDc8aEvrhu4HDCTfwz33vL6YtpcYX"
bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()

def load():
    try:
        with open("users.json","r") as f: return json.load(f)
    except: return {}
def save(d):
    with open("users.json","w") as f: json.dump(f,d)

@bot.message_handler(commands=['start'])
def s(m):
    bot.send_message(m.chat.id, f"BOT LIVE!\n\n/deposit - Get deposit address\n/balance - Check balance\n/withdraw - Withdraw")

@bot.message_handler(commands=['deposit'])
def dep(m):
    bot.send_message(m.chat.id, f"DEPOSIT DOGE\n\nAddress:\n{ADDR}\n\nMin: 5 DOGE\nAfter you send, contact admin.")

@bot.message_handler(commands=['balance'])
def bal(m):
    db=load()
    b=db.get(str(m.from_user.id),{}).get('bal',0)
    bot.send_message(m.chat.id, f"Your Balance: {b} DOGE")

@bot.message_handler(commands=['withdraw','addbalance'])
def other(m):
    bot.send_message(m.chat.id, "Use /withdraw AMOUNT ADDRESS")

bot.infinity_polling(skip_pending=True)
