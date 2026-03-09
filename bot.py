from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8638803031:AAFcqafHFSD_hUTobO0oknmeEsfK4vphkyc"

warns = {}
message_count = {}

# ADMIN CHECK
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat = update.effective_chat

    admins = await context.bot.get_chat_administrators(chat.id)

    admin_ids = [admin.user.id for admin in admins]

    return user_id in admin_ids


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This Bad Girl Is Healthy And Ready To Dominate 💕")


# RULES
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""📜 HeavenFall Community Rules

━━━━━━━━━━━━━━

1️⃣ Respect All Members  
Harassment, hate speech, or discrimination is not tolerated.

2️⃣ No NSFW Content  
Explicit or inappropriate material is prohibited.

3️⃣ No Spam or Advertisements  
Avoid flooding the chat or promoting external groups.

4️⃣ No Abusive Language  
Toxic behavior or personal attacks will result in warnings.

5️⃣ No Scams or Misleading Links  
Scam links or phishing will lead to immediate action.

6️⃣ Stay On Topic  
Keep discussions relevant to the community.

━━━━━━━━━━━━━━

⚠️ Moderation System
• 3 warnings = automatic ban
• Admin decisions are final

Help keep the community friendly and enjoyable.
"""
)


# NETWORK
async def network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""🌐 HeavenFall Network

━━━━━━━━━━━━━━

📢 Main Channel
https://t.me/HeavenFallNetwork

💬 Discussion Group
https://t.me/heavenfalldiscuss

📚 Cornhwa Channel
https://t.me/+A3Yuc2VEKTM3NGI1

🔞 Free Corn Videos
https://t.me/+vWLbtR8cinI0ZjI1
https://t.me/+tt6qe26yp2IxZjhl

━━━━━━━━━━━━━━

🎬 Join All Channels
https://t.me/addlist/MAiyE6j8fekzOTY1
"""
)


# ADMINS
async def admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""👑 HeavenFall Administration

━━━━━━━━━━━━━━

♛ Supreme Overseer
@fang_yuann
Sole Architect of the HeavenFall Network

━━━━━━━━━━━━━━

🛡 Moderation Council

• Moderator — Space Vacant
• Moderator — Space Vacant

━━━━━━━━━━━━━━

⚠️ Contact admins only for serious issues.
"""
)


# HELP
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""⚙️ HeavenFall Bot Commands

━━━━━━━━━━━━━━

👤 General Commands

/start
Check if the bot is online.

/rules
View the official community rules.

/network
See all HeavenFall channels and communities.

/admins
View the group administration team.

/top
Shows the most active members this week.

/help
Displays the full command list.

━━━━━━━━━━━━━━

🛡 Admin Moderation

/warn
Give a warning to a user (3 warns = ban).

/kick
Remove a user from the group.

/ban
Permanently ban a user.

/mute
Stop a user from sending messages.

/unmute
Restore a muted user's permissions.

━━━━━━━━━━━━━━

⚠️ Moderation commands are restricted to administrators.
"""
)


# COUNT MESSAGES
async def count_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    name = user.username if user.username else user.first_name

    if user.id not in message_count:
        message_count[user.id] = {
            "name": name,
            "count": 0
        }

    message_count[user.id]["count"] += 1


# TOP USERS
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not message_count:
        await update.message.reply_text("No activity yet.")
        return

    sorted_users = sorted(
        message_count.values(),
        key=lambda x: x["count"],
        reverse=True
    )

    text = "🏆 Most Active Members (This Week)\n\n"

    for i, user in enumerate(sorted_users[:5], start=1):
        text += f"{i}. {user['name']} — {user['count']} messages\n"

    await update.message.reply_text(text)


# WEEKLY RESET
async def reset_leaderboard(context: ContextTypes.DEFAULT_TYPE):
    global message_count
    message_count = {}
    print("Leaderboard reset for the week")


# WARN
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user to warn.")
        return

    user = update.message.reply_to_message.from_user
    user_id = user.id

    target = await context.bot.get_chat_member(update.effective_chat.id, user_id)

    if target.status in ["administrator", "creator"]:
        await update.message.reply_text("❌ You cannot warn another admin.")
        return

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

    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to user.")
        return

    user_id = update.message.reply_to_message.from_user.id

    target = await context.bot.get_chat_member(update.effective_chat.id, user_id)

    if target.status in ["administrator", "creator"]:
        await update.message.reply_text("❌ You cannot kick another admin.")
        return

    await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    await context.bot.unban_chat_member(update.effective_chat.id, user_id)

    await update.message.reply_text("👢 User kicked.")


# BAN
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to user.")
        return

    user_id = update.message.reply_to_message.from_user.id

    target = await context.bot.get_chat_member(update.effective_chat.id, user_id)

    if target.status in ["administrator", "creator"]:
        await update.message.reply_text("❌ You cannot ban another admin.")
        return

    await context.bot.ban_chat_member(update.effective_chat.id, user_id)

    await update.message.reply_text("🚫 User banned.")


# MUTE
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to user.")
        return

    user_id = update.message.reply_to_message.from_user.id

    target = await context.bot.get_chat_member(update.effective_chat.id, user_id)

    if target.status in ["administrator", "creator"]:
        await update.message.reply_text("❌ You cannot mute another admin.")
        return

    permissions = ChatPermissions(can_send_messages=False)

    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user_id,
        permissions
    )

    await update.message.reply_text("🔇 User muted.")


# UNMUTE
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to user.")
        return

    user_id = update.message.reply_to_message.from_user.id

    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_audios=True,
        can_send_documents=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )

    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user_id,
        permissions=permissions
    )

    await update.message.reply_text("🔊 User unmuted.")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("network", network))
app.add_handler(CommandHandler("admins", admins))
app.add_handler(CommandHandler("help", help))

app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(CommandHandler("top", top))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_messages))

app.job_queue.run_repeating(reset_leaderboard, interval=604800, first=604800)

print("Bot started...")

app.run_polling()
