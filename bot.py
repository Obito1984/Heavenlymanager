from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8638803031:AAFcqafHFSD_hUTobO0oknmeEsfK4vphkyc"

warns = {}
message_count = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is online ✅")

# RULES
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""📜 HeavenFall Rules

1️⃣ No NSFW
2️⃣ Respect members
3️⃣ No abusive language
4️⃣ No spam or ads
5️⃣ No scams
6️⃣ Stay on topic

⚠️ 3 warns = auto ban
"""
)

# NETWORK
async def network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""🌐 HeavenFall Network

📢 Main Channel
https://t.me/HeavenFallNetwork

💬 Discussion
https://t.me/heavenfalldiscuss
"""
)

# MESSAGE COUNTER
async def count_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message_count[user.id] = message_count.get(user.id, 0) + 1

# TOP USERS
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not message_count:
        await update.message.reply_text("No activity yet.")
        return

    sorted_users = sorted(message_count.items(), key=lambda x: x[1], reverse=True)

    text = "🏆 Most Active Members (This Week)\n\n"

    for i, (user_id, count) in enumerate(sorted_users[:5], start=1):
        text += f"{i}. {count} messages\n"

    await update.message.reply_text(text)

# WEEKLY RESET
async def reset_leaderboard(context: ContextTypes.DEFAULT_TYPE):
    global message_count
    message_count = {}
    print("Leaderboard reset for the week")

# WARN
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user to warn.")
        return

    user = update.message.reply_to_message.from_user
    user_id = user.id

    warns[user_id] = warns.get(user_id, 0) + 1

    if warns[user_id] >= 3:

        await context.bot.ban_chat_member(update.effective_chat.id, user_id)

        await update.message.reply_text(
            f"🚫 {user.first_name} banned (3 warnings reached)"
        )

        warns[user_id] = 0
        return

    await update.message.reply_text(
        f"⚠️ {user.first_name} warned ({warns[user_id]}/3)"
    )

# KICK
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to user.")
        return

    user_id = update.message.reply_to_message.from_user.id

    await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    await context.bot.unban_chat_member(update.effective_chat.id, user_id)

    await update.message.reply_text("👢 User kicked.")

# BAN
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to user.")
        return

    user_id = update.message.reply_to_message.from_user.id

    await context.bot.ban_chat_member(update.effective_chat.id, user_id)

    await update.message.reply_text("🚫 User banned.")

# MUTE
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to user.")
        return

    user_id = update.message.reply_to_message.from_user.id

    permissions = ChatPermissions(can_send_messages=False)

    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user_id,
        permissions
    )

    await update.message.reply_text("🔇 User muted.")

# UNMUTE
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to user.")
        return

    user_id = update.message.reply_to_message.from_user.id

    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )

    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user_id,
        permissions
    )

    await update.message.reply_text("🔊 User unmuted.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("network", network))

app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(CommandHandler("top", top))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_messages))

# WEEKLY RESET JOB (7 days)
app.job_queue.run_repeating(reset_leaderboard, interval=604800, first=604800)

print("Bot started...")

app.run_polling()
