from flask import Flask
from threading import Thread
import telebot

app = Flask('')
bot = telebot.TeleBot("8120422656:AAHB8qhwcAZt00xTDDApN1RoIqMnrCWvnSA")
PHOTO_PATH = 'egor.jpg'

@app.route('/')
def home():
    return "Я жив!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('📞 Контакт', '📷 Фото')
    bot.send_message(message.chat.id, "Выберите вариант:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '📞 Контакт')
def send_info(m):
    bot.send_message(m.chat.id, "Вот номер: +7 900 000-00-00")

@bot.message_handler(func=lambda m: m.text == '📷 Фото')
def send_photo(m):
    with open(PHOTO_PATH, 'rb') as photo:
        bot.send_photo(m.chat.id, photo)

bot.polling(none_stop=True)
