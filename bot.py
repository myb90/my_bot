import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler

TOKEN = 8120422656:AAHB8qhwcAZt00xTDDApN1RoIqMnrCWvnSA
PHOTO_URL = "https://my-bot-hy4e.onrender.com/static/photo.jpg"  # Заменим позже, если нужно
CONTACT_TEXT = "📞 Контакты:\nИмя: Иван\nТел: +7 999 123-45-67"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# === /start ===
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📷 Получить фото", callback_data="get_photo")],
        [InlineKeyboardButton("📞 Контакт", callback_data="get_contact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# === Обработка кнопок ===
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "get_photo":
        await query.message.reply_photo(PHOTO_URL)
    elif query.data == "get_contact":
        await query.message.reply_text(CONTACT_TEXT)

# === Flask Webhook endpoint ===
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "OK"

@app.route("/")
def index():
    return "Бот работает!"

# === Регистрация хендлеров ===
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))

# === Запуск приложения ===
if __name__ == "__main__":
    application.run_polling()