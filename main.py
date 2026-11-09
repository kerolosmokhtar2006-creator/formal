
import sqlite3

def init_db():
    conn = sqlite3.connect('bot_files.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            file_id TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "8229908901:AAEzqfIHe73-q9GbYfkxKZwGF6Bgi8bCI0M"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

MAIN_KEYBOARD = [
    ["🏥 عن العيادة", "📅 حجز موعد"],
    ["📋 الخدمات الطبية", "📞 تواصل معنا"],
]

reply_markup_main = ReplyKeyboardMarkup(
    MAIN_KEYBOARD,
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "مرحباً بك في بوت Formal Clinic 🏥\n\n"
        "اختر من القائمة أدناه للوصول السريع إلى الخدمات:"
    )

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup_main
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "🏥 عن العيادة":
        info_text = (
            "🏥 Formal Clinic\n\n"
            "عيادة متخصصة تقدم أفضل الخدمات الطبية والرعاية الصحية.\n"
            "📍 العنوان: مصر\n"
            "⏰ مواعيد العمل: يومياً من 10 صباحاً حتى 10 مساءً"
        )

        await update.message.reply_text(
            info_text,
            parse_mode="Markdown"
        )

    elif text == "📋 الخدمات الطبية":
        keyboard = [
            [InlineKeyboardButton("استشارة عامة 🩺", callback_data="service_general")],
            [InlineKeyboardButton("متابعة دورية 📊", callback_data="service_followup")],
            [InlineKeyboardButton("كشف مستعجل ⚡", callback_data="service_urgent")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "اختر الخدمة الطبية المطلوبة:",
            reply_markup=reply_markup
        )

    elif text == "📅 حجز موعد":
        keyboard = [
            [InlineKeyboardButton("تأكيد طلب حجز 📝", callback_data="book_now")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "لحجز موعد، يرجى ضغط الزر التالي وإرسال الاسم والحي/المدينة:",
            reply_markup=reply_markup
        )

    elif text == "📞 تواصل معنا":
        contact_text = (
            "📞 طرق التواصل:\n\n"
            "• الهاتف / واتساب: 01000000000\n"
            "• التلغرام: @formal_clinic_27_bot"
        )

        await update.message.reply_text(
            contact_text,
            parse_mode="Markdown"
        )

    else:
        await update.message.reply_text(
            "عذراً، يرجى اختيار أحد الخيارات من القائمة الرئيسية.",
            reply_markup=reply_markup_main
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "service_general":
        await query.edit_message_text(
            "🩺 استشارة عامة: تشخيص شامل وتقييم للحالة الصحية."
        )

    elif query.data == "service_followup":
        await query.edit_message_text(
            "📊 متابعة دورية: متابعة الفحوصات والتحاليل والخطط العلاجية."
        )

    elif query.data == "service_urgent":
        await query.edit_message_text(
            "⚡ كشف مستعجل: مواعيد فورية وتغطية الحالات الطارئة."
        )

    elif query.data == "book_now":
        await query.edit_message_text(
            "✅ تم استقبال طلبك. يرجى كتابة اسمك ورقم هاتفك وسيتم التواصل معك لحجز الموعد."
        )


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.add_handler(
        CallbackQueryHandler(button_callback)
    )

    logger.info("Bot starting...")

    application.run_polling()


init_db()

if __name__ == "__main__":
    main()
