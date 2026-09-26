import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = 8870690869:AAGFMWTtTsgN9VY0p64Qg6lMQk0y64nlIEA
ADMIN_ID = 8938541719

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Deposit $10", callback_data='deposit')],
        [InlineKeyboardButton("📊 Balance", callback_data='balance')],
        [InlineKeyboardButton("💸 Withdraw", callback_data='withdraw')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🐶 Welcome to DOGE Bot!\nChoose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'deposit':
        await query.edit_message_text("💰 Send DOGE to:\n`DH5yaieqoZN36fDVciNyRueRG4D5CB9Bw1`\n\nAfter sending, type /deposit <txid>")
    elif query.data == 'balance':
        await query.edit_message_text("📊 Your balance: 0 DOGE")
    elif query.data == 'withdraw':
        await query.edit_message_text("💸 Send your DOGE wallet address to withdraw.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
