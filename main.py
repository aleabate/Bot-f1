from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🏎️ Bot F1 attivo! Invia /analisi per le info.")

async def analisi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📊 Analisi GP in corso... Nessun errore di quota al momento.")

def main():
    # Sostituisci la stringa sotto con il token ricevuto da @BotFather
    TOKEN = "8544206441:AAGAwWbXlISlz4tpqlfq6kn31XeqSSz3IR4"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analisi", analisi))
    print("Bot in ascolto...")
    app.run_polling()

if __name__ == "__main__":
    main()
