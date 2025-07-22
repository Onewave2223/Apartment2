import os
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc  # Render требует явный pytz timezone

# 🔐 Получение переменных окружения
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# 🧱 Проверка токена и chat_id
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не задан! Укажи его в переменных окружения.")
if not CHAT_ID:
    raise ValueError("❌ CHAT_ID не задан! Укажи его в переменных окружения.")

try:
    CHAT_ID = int(CHAT_ID)
except ValueError:
    raise ValueError("❌ CHAT_ID должен быть числом!")

ALLOWED_USERS = [CHAT_ID]  # Только один разрешённый пользователь

# 🧾 Логирование
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🤖 Инициализация бота
bot = Bot(token=TOKEN)

# 🧹 Очистка чата
async def clear_chat(context: ContextTypes.DEFAULT_TYPE):
    try:
        updates = await bot.get_updates()
        for update in updates:
            if update.message and update.message.chat.id == CHAT_ID:
                await bot.delete_message(chat_id=CHAT_ID, message_id=update.message.message_id)
        logging.info("✅ Чат успешно очищен.")
    except Exception as e:
        logging.error(f"❌ Ошибка при очистке чата: {e}")

# 🔘 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔️ Извините, доступ запрещён.")
        return
    await update.message.reply_text("✅ Бот работает! Ожидаем новые квартиры...")

# 🚀 Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # ⏰ Планировщик для еженедельной очистки
    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(lambda: app.create_task(clear_chat(None)), trigger='interval', days=7)
    scheduler.start()

    print("✅ Бот запущен. Ожидаем команды...")
    app.run_polling()
