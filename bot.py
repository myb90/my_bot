from flask import Flask, request
import telegram
import logging
import os

TOKEN = "8120422656:AAHB8qhwcAZt00xTDDApN1RoIqMnrCWvnSA"
bot = telegram.Bot(token=TOKEN)
PHOTO_PATH = "egor.jpg"
TEXT = "Беру в рот 1000₽ в час, звонить по номеру: +79189376318, рядом слева от меня мой друг такой же сосунок"

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    message = update.message
    user_id = message.chat.id
    text = message.text

    if text == "/start":
        keyboard = telegram.ReplyKeyboardMarkup([
            ["📞 Получить номер"],
            ["🖼️ Получить фото"],
            ["🚪 Выход"]
        ], resize_keyboard=True)
        bot.send_message(chat_id=user_id, text="Выберите действие:", reply_markup=keyboard)

    elif text == "📞 Получить номер":
        bot.send_message(chat_id=user_id, text=TEXT)

    elif text == "🖼️ Получить фото":
        try:
            with open(PHOTO_PATH, 'rb') as photo:
                bot.send_photo(chat_id=user_id, photo=photo)
        except Exception as e:
            logging.error(e)
            bot.send_message(chat_id=user_id, text="❌ Фото не найдено.")

    elif text == "🚪 Выход":
        bot.send_message(chat_id=user_id, text="Вы вышли. Чтобы начать заново, введите /start")

    return 'ok'

@app.route('/')
def index():
    return "Бот работает!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
