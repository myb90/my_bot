import os
from flask import Flask, request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8120422656:AAHB8qhwcAZt00xTDDApN1RoIqMnrCWvnSA"
URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/"

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# Кнопки
keyboard = [
    [InlineKeyboardButton("📸 Получить фото", callback_data="photo")],
    [InlineKeyboardButton("📞 Контакт", callback_data="contact")]
]
markup = InlineKeyboardMarkup(keyboard)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message and update.message.text == '/start':
        bot.send_message(chat_id=update.message.chat.id,
                         text="Привет! Выберите действие:",
                         reply_markup=markup)

    elif update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat.id

        if query.data == "photo":
            bot.send_photo(chat_id=chat_id, photo=open('static/egor.jpg', 'rb'))
        elif query.data == "contact":
            bot.send_message(chat_id=chat_id, text="Беру в рот 1000₽ в час, звонить по номеру: +79189376318, рядом слева от меня мой друг такой же сосунок")

        bot.answer_callback_query(callback_query_id=query.id)

    return 'ok'

@app.route('/')
def index():
    return 'Бот работает.'

if __name__ == '__main__':
    bot.delete_webhook()
    bot.set_webhook(url=URL + TOKEN)
    app.run(host='0.0.0.0', port=5000)
