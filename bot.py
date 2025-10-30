import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота и настройки
BOT_TOKEN = "8493344031:AAEVTIolohAk1lD6skMX5Pv2ADo6avVBjvE"
ADMIN_ID = 6644276942
CHAT_ID = "-1003074821645"
REGISTRATION_THREAD_ID = 931
WELCOME_THREAD_ID = 1294

# Клавиатура с командами
def get_main_keyboard():
    keyboard = [
        ["🎮 Начать регистрацию", "📞 Позвать админа"],
        ["💬 Перейти в чат", "ℹ️ Помощь"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\nДобро пожаловать!",
        reply_markup=get_main_keyboard()
    )

# Обработка сообщений
async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    text = update.message.text
    user = update.effective_user
    
    if update.message.chat.type != "private":
        return
    
    if user_data.get('registration_step') == 'waiting_data':
        registration_info = f"📝 НОВАЯ РЕГИСТРАЦИЯ\n\nОт: {user.first_name}\nДанные:\n{text}"
        
        try:
            await context.bot.send_message(
                chat_id=CHAT_ID,
                message_thread_id=REGISTRATION_THREAD_ID,
                text=registration_info
            )
            await update.message.reply_text("✅ Регистрация успешна!", reply_markup=get_main_keyboard())
            user_data.clear()
            return
        except Exception as e:
            await update.message.reply_text("❌ Ошибка отправки.", reply_markup=get_main_keyboard())
            user_data.clear()
            return
    
    if text == "🎮 Начать регистрацию":
        registration_format = "🎮 РЕГИСТРАЦИЯ\n\nОтправьте данные в формате:\nИмя: ...\nНикнейм: ...\nActivision ID: ..."
        await update.message.reply_text(registration_format)
        user_data['registration_step'] = 'waiting_data'
    
    elif text == "📞 Позвать админа":
        user = update.effective_user
        admin_call = f"📢 АДМИН! {user.first_name} зовет вас!"
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_call)
            await update.message.reply_text("✅ Админ уведомлен!")
        except:
            await update.message.reply_text("❌ Не удалось уведомить админа")
    
    elif text == "💬 Перейти в чат":
        await update.message.reply_text(
            "💬 Наш чат:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Перейти в чат", url="https://t.me/The_bakeryy")]])
        )
    
    elif text == "ℹ️ Помощь":
        await update.message.reply_text("Используйте кнопки для навигации")
    
    else:
        await update.message.reply_text("Используйте кнопки для навигации")

# Приветствие новых участников
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.message.chat_id) != CHAT_ID.replace("-100", "-100"):
        return
        
    for new_member in update.message.new_chat_members:
        welcome_text = f"🎉 Добро пожаловать, {new_member.first_name}!\n\nДля регистрации напишите боту: @Spaykibot"
        
        try:
            await context.bot.send_message(
                chat_id=CHAT_ID,
                message_thread_id=WELCOME_THREAD_ID,
                text=welcome_text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🤖 Написать боту", url="https://t.me/Spaykibot")]
                ])
            )
        except:
            pass

# Запуск бота
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))
    
    print("🚀 Бот запущен на Railway!")
    application.run_polling()

if __name__ == "__main__":
    main()
