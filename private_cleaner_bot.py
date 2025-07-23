
import os
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import asyncio

# 🔐 Переменные окружения
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ALLOWED_USERS = [int(CHAT_ID)]

# 🔧 Логирование
logging.basicConfig(level=logging.INFO)

# 🤖 Бот
bot = Bot(token=TOKEN)

# 🧹 Очистка чата
async def clear_chat():
    try:
        updates = await bot.get_updates()
        for update in updates:
            if update.message and str(update.message.chat.id) == CHAT_ID:
                await bot.delete_message(chat_id=CHAT_ID, message_id=update.message.message_id)
        logging.info("Чат очищен.")
    except Exception as e:
        logging.error(f"Ошибка при очистке чата: {e}")

# 🟢 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Доступ запрещён.")
        return
    await update.message.reply_text("✅ Бот запущен и работает.")

# 🚀 Запуск
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # ⏰ Планировщик очистки каждую неделю
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(lambda: asyncio.run(clear_chat()), trigger="interval", days=7)
    scheduler.start()

    logging.info("🤖 Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
