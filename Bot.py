from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8638803031:AAFcqafHFSD_hUTobO0oknmeEsfK4vphkyc"

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "📜 HeavenFall Rules\n\n• No NSFW spam\n• Respect members\n• No scam links")

async def network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "🌐 HeavenFall Network\n\nMain Channel: https://t.me/HeavenFallNetwork")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("network", network))

app.run_polling()
