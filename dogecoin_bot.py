import os, threading
from flask import Flask
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Doge-bot alive!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🚀 Bot is online 24/7 even if you are offline!")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    bot.reply_to(m, f"You said: {m.text}")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
