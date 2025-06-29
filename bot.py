import telebot
from telebot import types

# ✅ Токен бота
bot = telebot.TeleBot("8065710980:AAHy5QBQ8-u5S777qRMW-Gg35L0Zg7wMEGE")

# ✅ Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📸 Получить видео")
    btn2 = types.KeyboardButton("📞 Контакт")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)

# ✅ Обработка кнопок
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "📸 Получить видео":
        # Путь к новому видео
        video_path = "/data/data/com.termux/files/home/storage/downloads/egor/egorsoso.mp4"
        caption = "Маленьки сосунок постоянно клеится к бабам а вообще он даун Юзтг:@xCJIAB9IH1337x"
        with open(video_path, 'rb') as video:
            bot.send_video(message.chat.id, video, caption=caption)
    elif message.text == "📞 Контакт":
        bot.send_message(message.chat.id, "Беру в рот 1000₽ в час, звонить по номеру: +79189376318, рядом слева от меня мой друг такой же сосунок")
    else:
        bot.send_message(message.chat.id, "Нажми кнопку ниже.")

# ✅ Запуск бота
bot.infinity_polling()
