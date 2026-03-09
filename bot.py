from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8638803031:AAFcqafHFSD_hUTobO0oknmeEsfK4vphkyc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is online ✅")

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""📜 HeavenFall Rules

• No NSFW spam
• No abusive language
• No scam links
• Respect all members
"""
)

async def network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""🌐 HeavenFall Network

📢 Main Channel
https://t.me/HeavenFallNetwork

💬 Discussion Group
https://t.me/heavenfalldiscuss
"""
)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("network", network))

print("Bot started...")

app.run_polling()
