import os
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

# 🔐 Токен и ID
BOT_TOKEN = "8127921766:AAFJBcEYYX6UhPjyZFG7-cC5_H8bb72Q_GA"
CHAT_ID = "1905948782"
ALLOWED_USERS = [int(CHAT_ID)]

# 🔧 Логирование
logging.basicConfig(level=logging.INFO)

# 🤖 Бот
bot = Bot(token=BOT_TOKEN)

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

# 🚀 Основной запуск
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(lambda: asyncio.create_task(clear_chat()), trigger="interval", days=7)
    scheduler.start()

    logging.info("🤖 Бот запущен...")
    await app.run_polling()

# 🔁 Запуск с учётом event loop
if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
