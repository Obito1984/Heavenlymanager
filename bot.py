from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8638803031:AAFcqafHFSD_hUTobO0oknmeEsfK4vphkyc"

# Simple warn storage
warns = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is online ✅")

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""📜 HeavenFall Network — Rules

1️⃣ No NSFW or explicit content
2️⃣ Respect all members
3️⃣ No abusive language
4️⃣ No spam or ads
5️⃣ No scams or malicious links
6️⃣ Stay on topic

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
"""
)

# WARN COMMAND
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user to warn them.")
        return

    user = update.message.reply_to_message.from_user
    user_id = user.id

    warns[user_id] = warns.get(user_id, 0) + 1

    await update.message.reply_text(
        f"⚠️ {user.first_name} has been warned.\nTotal warns: {warns[user_id]}/3"
    )

# KICK COMMAND
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user to kick them.")
        return

    user_id = update.message.reply_to_message.from_user.id

    await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    await context.bot.unban_chat_member(update.effective_chat.id, user_id)

    await update.message.reply_text("👢 User has been kicked.")

# BAN COMMAND
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user to ban them.")
        return

    user_id = update.message.reply_to_message.from_user.id

    await context.bot.ban_chat_member(update.effective_chat.id, user_id)

    await update.message.reply_text("🚫 User has been banned.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("network", network))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("ban", ban))

print("Bot started...")

app.run_polling()
