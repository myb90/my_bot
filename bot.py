from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
import asyncio

TOKEN = "8120422656:AAHB8qhwcAZt00xTDDApN1RoIqMnrCWvnSA"
WEBHOOK_URL = "https://my-bot-hy4e.onrender.com"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я работаю через Render и Webhook!")

# Обработчик команды
application.add_handler(CommandHandler("start", start))

# Установка webhook
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

# Обработка запросов Telegram
@app.route("/", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.update_queue.put(update)
    return "ok", 200

# Проверка работоспособности
@app.route("/", methods=["GET"])
def index():
    return "Бот запущен и работает!"

if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=5000)