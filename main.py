import logging
import os
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# إعدادات القنوات المطلوبة للاشتراك
REQUIRED_CHANNELS = ['@TiasAmazingWorld', '@AlShaheenNews']

# التحقق من الاشتراك
async def is_subscribed(user_id, bot):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

# استخراج الرابط وتحميل الفيديو
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_subscribed(user_id, context.bot):
        await update.message.reply_text("يرجى الاشتراك في القنوات التالية أولاً:
@TiasAmazingWorld
@AlShaheenNews")
        return

    url = update.message.text.strip()
    if not re.match(r'https?://', url):
        await update.message.reply_text("أرسل رابط صحيح من المواقع المدعومة.")
        return

    # استخدام API خارجية لتحميل الفيديو (مثال فقط)
    response = requests.get(f"https://api.vevioz.com/api/button/download?url={url}")
    if "video" in response.text:
        await update.message.reply_text("تم العثور على الفيديو! لكن خاصية التحميل قيد التطوير.")
    else:
        await update.message.reply_text("تعذر تحميل الفيديو من الرابط. تأكد من صحته.")

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلًا بك في بوت التحميل. أرسل رابط من YouTube أو TikTok أو Instagram أو Pinterest...")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
