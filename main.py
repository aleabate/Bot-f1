import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8702415894:AAGYC4k6kjlNhZfz-O5IRppsv_O0otCTFL0")
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "1ce5626585c91748bcfa89bd3172133d")

def get_f1_value_bets():
    url = f"https://api.the-odds-api.com/v4/sports/motorsport_formula_one/odds/"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "outrights",
        "oddsFormat": "decimal"
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"Errore recupero dati API: {response.status_code}"
        
    events = response.json()
    if not events:
        return "Nessun evento F1 disponibile al momento su The Odds API."

    value_bets = []

    for event in events:
        for bookmaker in event.get("bookmakers", []):
            book_name = bookmaker.get("title")
            for market in bookmaker.get("markets", []):
                outcomes = market.get("outcomes", [])
                
                all_odds = [o["price"] for o in outcomes if "price" in o]
                if not all_odds:
                    continue
                avg_odd = sum(all_odds) / len(all_odds)

                for outcome in outcomes:
                    driver = outcome.get("name")
                    price = outcome.get("price")
                    
                    if price > avg_odd * 1.15:
                        ev_perc = round(((price / avg_odd) - 1) * 100, 1)
                        value_bets.append(
                            f"🏎 **{driver}**\n"
                            f"📌 Mercato: {market.get('key')}\n"
                            f"🏢 Bookmaker: **{book_name}**\n"
                            f"📈 Quota offerta: **{price}** (Media: {round(avg_odd, 2)})\n"
                            f"🔥 Value/EV: **+{ev_perc}%**\n"
                        )

    if not value_bets:
        return "Nessuna quota fuori mercato trovata al momento per la F1."
        
    return "\n---\n".join(value_bets[:5])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏎 **F1 Quota Errors Bot Attivo!**\n\n"
        "Usa /analisi per cercare immediatamente gli errori di quota (value bet) sulla Formula 1."
    )

async def analisi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 *Scansione quote F1 in corso sulle API...*", parse_mode="Markdown")
    risultato = get_f1_value_bets()
    await update.message.reply_text(risultato, parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analisi", analisi))
    
    print("Bot avviato con successo...")
    app.run_polling()
