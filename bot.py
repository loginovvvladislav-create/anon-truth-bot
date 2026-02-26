# version 2
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

TOKEN = "8793875356:AAHq6CqTB5TpBpR_dYWmlc8d86fHZP5vR_A"

def start(update, context):
    user_id = update.effective_user.id

    keyboard = [
        [InlineKeyboardButton("🔗 Получить ссылку", callback_data="get_link")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "👁 Анонимная правда о тебе\n\n"
        "Я помогу узнать, что о тебе думают на самом деле.\n"
        "Анонимно. Бесплатно. Без имён.\n\n"
        "👇 Нажми кнопку ниже",
        reply_markup=reply_markup
    )

def button_handler(update, context):
    query = update.callback_query
    query.answer()

    if query.data == "get_link":
        user_id = query.from_user.id
        bot_username = context.bot.username
        link = f"https://t.me/{bot_username}?start=anon_{user_id}"

        query.edit_message_text(
            f"🔗 Твоя личная ссылка:\n\n"
            f"{link}\n\n"
            "Отправь её друзьям.\n"
            "Они смогут написать о тебе честно и анонимно."
        )

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(button_handler))

updater.start_polling()
updater.idle()
