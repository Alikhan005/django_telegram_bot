import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
import django
django.setup()

from shop.models import Product


TELEGRAM_TOKEN = "8036959909:AAHO4G9FMrHjeSzVIBu_qPTe0JXSQOGLcYI"
PAYMENT_NUMBER = "+7 705 729 90 29"


COURSES_FOLDER = "C:/Users/Asus Tuf/Desktop/djnago/courses"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Список товаров", callback_data="list_products")],
        [InlineKeyboardButton("Как оплатить", callback_data="payment_info")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать! Выберите действие:", reply_markup=reply_markup)



async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "list_products":
        courses = os.listdir(COURSES_FOLDER)
        if courses:
            text = "\n".join([f"{i + 1}. {course}" for i, course in enumerate(courses)])
            text += "\n\nНапишите /buy <ID>, чтобы купить товар."
        else:
            text = "Курсы пока не добавлены."
        await query.message.reply_text(text)

    elif query.data == "payment_info":
        await query.message.reply_text(f"Для оплаты переведите сумму на номер {PAYMENT_NUMBER}. После оплаты отправьте фото чека.")



async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        course_id = int(context.args[0])
        courses = os.listdir(COURSES_FOLDER)
        if course_id <= 0 or course_id > len(courses):
            raise IndexError

        course_name = courses[course_id - 1]
        price = 5000  
        await update.message.reply_text(
            f"Вы выбрали курс: {course_name}\nЦена: {price} KZT\n\n"
            f"Для оплаты переведите сумму на номер {PAYMENT_NUMBER}. После оплаты отправьте фото чека."
        )
    except IndexError:
        await update.message.reply_text("Укажите корректный ID курса. Пример: /buy 1")
    except ValueError:
        await update.message.reply_text("ID должен быть числом.")



async def handle_payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
       
        caption = update.message.caption
        if caption and "5000" in caption: 
            await update.message.reply_text("Оплата проверена! Скачайте курс:")
            courses = os.listdir(COURSES_FOLDER)
            for course in courses:
                await update.message.reply_document(document=open(f"{COURSES_FOLDER}/{course}", "rb"))
        else:
            await update.message.reply_text("Неверный чек или сумма! Повторите попытку.")
    else:
        await update.message.reply_text("Пожалуйста, отправьте фото чека.")


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(MessageHandler(filters.PHOTO, handle_payment_proof))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
