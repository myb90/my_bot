import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import asyncio

# --- Конфигурация ---
TOKEN = "8120422656:AAHB8qhwcAZt00xTDDApN1RoIqMnrCWvnSA"
PHOTO_PATH = "/data/data/com.termux/files/home/storage/downloads/egor.jpg"
TEXT = "Беру в рот 1000₽ в час, звонить по номеру: +79189376318, рядом слева от меня мой друг такой же сосунок"
USERS_FILE = "users.txt"

# --- Логирование ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Хранилище активных пользователей ---
active_users = set()

# --- Загрузка пользователей из файла ---
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                user_id = line.strip()
                if user_id:
                    active_users.add(int(user_id))

def save_user(user_id: int):
    if user_id not in active_users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")
        active_users.add(user_id)

# --- Обработчики ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    buttons = [
        [KeyboardButton("📞 Получить номер")],
        [KeyboardButton("🖼️ Получить фото")],
        [KeyboardButton("🚪 Выход")]
    ]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text
    logger.info(f"Пользователь {user_id}: {message_text}")

    if user_id not in active_users:
        return

    if message_text == "📞 Получить номер":
        await update.message.reply_text(TEXT)
    elif message_text == "🖼️ Получить фото":
        try:
            with open(PHOTO_PATH, "rb") as photo:
                await update.message.reply_photo(photo)
        except Exception as e:
            await update.message.reply_text("❌ Фото не найдено.")
            logger.error(f"Ошибка при отправке фото: {e}")
    elif message_text == "🚪 Выход":
        if user_id in active_users:
            active_users.remove(user_id)
            await update.message.reply_text("Вы вышли. Чтобы начать заново, введите /start")
    else:
        await update.message.reply_text("Выберите одну из кнопок.")

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if active_users:
        users_list = "\n".join(str(uid) for uid in active_users)
        await update.message.reply_text(f"Активные пользователи:\n{users_list}")
    else:
        await update.message.reply_text("Нет активных пользователей.")

# --- Запуск ---
def main():
    load_users()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("users", show_users))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 Бот запущен.")
    app.run_polling()

# --- Бесконечный цикл с защитой ---
if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            logger.error(f"❌ Ошибка в боте: {e}")
            asyncio.sleep(3)
