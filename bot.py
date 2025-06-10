import os
from flask import Flask, request
import telegram
from telegram import ReplyKeyboardMarkup

TOKEN = "8120422656:AAEhx04H_ofoP1oRDfBwmjT0MNeRdHt2k6k"
URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# Кнопки
reply_keyboard = [['📸 Получить фото', '📞 Контакт']]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        text = update.message.text
        chat_id = update.message.chat.id

        if text == '/start':
            bot.send_message(chat_id=chat_id,
                             text="Привет! Выберите действие:",
                             reply_markup=markup)

        elif text == '📸 Получить фото':
            try:
                bot.send_photo(chat_id=chat_id, photo=open('static/egor.jpg', 'rb'))
            except Exception as e:
                bot.send_message(chat_id=chat_id, text="Ошибка при отправке фото.")

        elif text == '📞 Контакт':
            bot.send_message(chat_id=chat_id,
                             text="Беру в рот 1000₽ в час, звонить по номеру: +79189376318, рядом слева от меня мой друг такой же сосунок")

    return 'ok'

@app.route('/')
def index():
    return 'Бот работает.'

if __name__ == '__main__':
    import requests
    requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook",
                 params={"url": URL})
    app.run(host='0.0.0.0', port=5000)
