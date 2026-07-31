import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 7767428833

users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام رفیق 👋\n\n"
        "الان میتونی هرچی که میخوای رو برای ربات ارسال کنی!\n\n"
        "منتظرم:"
    )


async def receive(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id == ADMIN_ID:
        return

    await update.message.reply_text(
        "پیامتو گرفتیم رفیق 🌚\n\n"
        "محتوای ارسالی پس از بررسی توسط ادمینامون در صورت تایید پاسخ داده میشه یا داخل چنل منتشر میشه.\n"
        "از همراهیت ممنونیم 🤍"
    )

    sent = await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    users[sent.message_id] = update.message.chat_id


async def reply_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message:
        return

    msg_id = update.message.reply_to_message.message_id

    if msg_id in users:
        await context.bot.send_message(
            chat_id=users[msg_id],
            text=update.message.text
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.User(ADMIN_ID) & filters.REPLY, reply_user)
)

app.add_handler(
    MessageHandler(filters.ALL, receive)
)

app.run_polling()
