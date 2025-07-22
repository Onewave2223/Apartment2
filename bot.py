import os
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

# 🔑 Токен и chat_id
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ALLOWED_USERS = [int(CHAT_ID)]

# Логирование
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)

# 🧹 Очистка чата
async def clear_chat(context: ContextTypes.DEFAULT_TYPE):
    try:
        updates = await bot.get_updates()
        for update in updates:
            if update.message and update.message.chat.id == int(CHAT_ID):
                await bot.delete_message(chat_id=CHAT_ID, message_id=update.message.message_id)
        logging.info("Чат очищен.")
    except Exception as e:
        logging.error(f"Ошибка при очистке чата: {e}")

# 🟢 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("Извините, доступ запрещён.")
        return
    await update.message.reply_text("Бот активен. Ожидаем новые квартиры...")

# 🚀 Основной запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler(timezone=pytz.utc)
    scheduler.add_job(lambda: app.create_task(clear_chat(None)), 'interval', days=7)
    scheduler.start()

    app.run_polling()