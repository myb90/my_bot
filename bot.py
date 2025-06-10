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
