from telegram.ext import Updater, CommandHandler

TOKEN = "8793875356:AAHq6CqTB5TpBpR_dYWmlc8d86fHZP5vR_A"

def start(update, context):
    update.message.reply_text(
        "👁 Анонимная правда о тебе\n\n"
        "Я помогу узнать, что о тебе думают на самом деле.\n"
        "Анонимно. Бесплатно. Без имён.\n\n"
        "👇 Нажми кнопку ниже"
    )

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))

updater.start_polling()
updater.idle()
