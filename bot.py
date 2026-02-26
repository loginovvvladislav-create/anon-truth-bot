# version 4 – Анонимная правда с анализом и рекламой
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from textblob import TextBlob  # для простого анализа текста

TOKEN = "8793875356:AAHq6CqTB5TpBpR_dYWmlc8d86fHZP5vR_A"

# временное хранилище (позже заменим на БД)
answers = {}

# ----------------------
# функции
# ----------------------

def analyze_answers(user_answers):
    """Простой анализ настроения ответов"""
    polarity = sum(TextBlob(ans).sentiment.polarity for ans in user_answers) / len(user_answers)
    if polarity > 0.1:
        return "😄 В целом положительные отзывы"
    elif polarity < -0.1:
        return "😢 В целом критические отзывы"
    else:
        return "🤔 Смешанные мнения"

def start(update, context):
    args = context.args
    user_id = update.effective_user.id

    # если пришли по анонимной ссылке
    if args and args[0].startswith("anon_"):
        owner_id = args[0].split("_")[1]
        context.user_data["anon_for"] = owner_id

        update.message.reply_text(
            "🕶 Ты пишешь анонимно.\n\n"
            "Ответь честно на вопрос:\n"
            "👉 Что тебе НЕ нравится в этом человеке?"
        )
        return

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

def message_handler(update, context):
    user_data = context.user_data

    # если это анонимный ответ
    if "anon_for" in user_data:
        owner_id = user_data["anon_for"]
        text = update.message.text.strip()

        if not text:
            update.message.reply_text("❌ Пустое сообщение не отправлено.")
            return

        answers.setdefault(owner_id, []).append(text)

        update.message.reply_text(
            "✅ Ответ отправлен анонимно.\n"
            "Спасибо за честность."
        )

        # очищаем состояние
        user_data.clear()
        return

def answers_command(update, context):
    """Команда /answers — показывает последние 5 ответов владельцу ссылки"""
    user_id = update.effective_user.id
    user_answers = answers.get(user_id, [])

    if not user_answers:
        update.message.reply_text("📭 Пока никто не написал о тебе.")
        return

    text = "✉️ Последние анонимные ответы:\n\n"
    for i, ans in enumerate(user_answers[-5:], 1):
        text += f"{i}. {ans}\n\n"

    # простой анализ
    analysis = analyze_answers(user_answers)
    text += f"📊 Анализ: {analysis}\n\n"

    # рекламный блок
    text += "📢 Поддержите бота! Хотите больше фишек? Жмите сюда: [ссылка]"

    update.message.reply_text(text)

# ----------------------
# запуск бота
# ----------------------
updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(button_handler))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
dp.add_handler(CommandHandler("answers", answers_command))

updater.start_polling()
updater.idle()
