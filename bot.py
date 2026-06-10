import re
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8027197776:AAEPpbofCor2jd9IEeLMUkkFmN4hMaZiAXs"

GROUP_ID = -1003553742203

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not text:
        return

    if "You have received ETB" not in text:
        return

    amount_match = re.search(
        r"You have received ETB ([0-9,]+\.[0-9]+)",
        text
    )

    sender_match = re.search(
        r"from (.*?)\(",
        text
    )

    datetime_match = re.search(
        r"on (\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}:\d{2})",
        text
    )

    txn_match = re.search(
        r"transaction number is ([A-Z0-9]+)",
        text
    )

    if not (
        amount_match
        and sender_match
        and datetime_match
        and txn_match
    ):
        return

    amount = amount_match.group(1)
    sender = sender_match.group(1).strip()
    date = datetime_match.group(1)
    time = datetime_match.group(2)
    txn = txn_match.group(1)

    msg = f"""
💰 TELEBIRR PAYMENT

👤 Sender: {sender}
💵 Amount: ETB {amount}
📅 Date: {date}
🕒 Time: {time}
🔖 TXN: {txn}

✅ Verify Payment
"""

    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=msg
    )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

print("Bot running...")

app.run_polling()