from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8638803031:AAFcqafHFSD_hUTobO0oknmeEsfK4vphkyc" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is online ✅")

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""📜 HeavenFall Network — Rules

This is a mature community. Please follow the rules.

1️⃣ No NSFW or explicit content
2️⃣ Respect all members
3️⃣ No abusive or offensive language
4️⃣ No spam or advertisements
5️⃣ No scams or misleading links
6️⃣ Keep discussions relevant

⚠️ Violations may lead to warn, mute, kick, or ban.
"""
)

async def network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""🌐 HeavenFall Network

📢 Main Channel
https://t.me/HeavenFallNetwork

💬 Discussion Group
https://t.me/heavenfalldiscuss

📚 Cornhwa Channel
https://t.me/+A3Yuc2VEKTM3NGI1

🔞 Free Corn Videos
https://t.me/+vWLbtR8cinI0ZjI1
https://t.me/+tt6qe26yp2IxZjhl

🎬 Join All Channels
https://t.me/addlist/MAiyE6j8fekzOTY1
"""
)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("network", network))

print("Bot started...")

app.run_polling()
