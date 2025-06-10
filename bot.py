from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

TOKEN = "8120422656:AAHB8qhwcAZt00xTDDApN1RoIqMnrCWvnSA"

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=1, use_context=True)

# Обработчик команды /start
def start(update, context):
    update.message.reply_text("Привет! Я работаю через Render и webhook.")

# Регистрируем обработчик
dispatcher.add_handler(CommandHandler("start", start))

# Это основной webhook endpoint для Telegram
@app.route("/", methods=["POST"])
def receive_update():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

# Стартовая страница для проверки вручную
@app.route("/", methods=["GET"])
def index():
    return "Бот работает (Render + webhook)"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)