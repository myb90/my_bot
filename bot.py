import telebot
from telebot import types

bot = telebot.TeleBot('8065710980:AAHy5QBQ8-u5S777qRMW-Gg35L0Zg7wMEGE')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📸 Получить фото')
    btn2 = types.KeyboardButton('📞 Контакт')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Привет, выбери действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == '📸 Получить фото':
        video_path = '/storage/emulated/0/Download/egor/egorsoso.mp4'
        with open(video_path, 'rb') as video:
            bot.send_video(message.chat.id, video)
    elif message.text == '📞 Контакт':
        text = 'Маленький сосунок постоянно клеится к бабам а вообще он даун Юзтг:@xCJIAB9IH1337x'
        bot.send_message(message.chat.id, text)

bot.polling()
