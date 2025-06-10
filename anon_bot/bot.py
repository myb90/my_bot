import os
from flask import Flask, request
import telegram

TOKEN = "8181718229:AAEmQImBRnGeblnStGRfyagJchnJhA-uH4w"
OWNER_ID = 7860053943  # @Lastdau69

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text
        if text == "/start":
            bot.send_message(chat_id=chat_id, text="привет это анонимный бот от Мухина Руслана напиши мне своё сообщение")
        else:
            bot.send_message(chat_id=OWNER_ID, text=f"Новое сообщение:\n{text}")

    return 'ok'

@app.route('/')
def index():
    return 'Анонимный бот запущен.'

if __name__ == '__main__':
    import requests
    requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook", params={"url": URL})
    app.run(host='0.0.0.0', port=5000)
