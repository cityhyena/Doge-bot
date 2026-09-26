import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🐶 DOGE Bot is LIVE! \n\n💰 Deposit\n📊 Balance\n💸 Withdraw\n\nType /start")

def main():
    if not TOKEN:
        print("ERROR: TOKEN env not set")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
