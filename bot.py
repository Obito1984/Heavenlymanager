from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import os

TOKEN = "8638803031:AAFcqafHFSD_hUTobO0oknmeEsfK4vphkyc"

warns = {}
message_count = {}
afk_users = {}

# ADMIN CHECK
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    member = await context.bot.get_chat_member(chat_id, user_id)

    return member.status in ["administrator", "creator"]

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This Bad Girl is Healthy And Ready To Dominate 💕")

# AFK
async def afk(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    reason = " ".join(context.args) if context.args else "Away for now."

    afk_users[user.id] = reason

    await update.message.reply_text(
        f"🌙 {user.first_name} has gone AFK.\nReason: {reason}"
    )

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

♛ Supreme Overseer - @fang_yuann

[Sole Architect of the HeavenFall Network] 

━━━━━━━━━━━━━━

🛡 Moderation Council

• Moderator — @Serene_khuc
• Moderator —  @Fakk_07
• Moderator — @yaee_lynnn
• Moderator — @qxm1c

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

/alert
Notify admins if you need help.

/afk
Set yourself as away.

/kang
Steal a sticker and add it to your pack.

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

/tempmute
Temporarily mute a user.

/purge
Delete multiple messages.

/userinfo
View information about a user.

/stats
Show group statistics.

/lock
Lock the chat so nobody can send messages.

/unlock
Unlock the chat again.

━━━━━━━━━━━━━━

⚠️ Moderation commands are restricted to administrators.
"""
)

# ALERT
async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user = update.effective_user

    admins = await context.bot.get_chat_administrators(chat_id)

    text = "🚨 Admin Alert\n\n"

    for admin in admins:
        text += f"[{admin.user.first_name}](tg://user?id={admin.user.id}) "

    text += f"\n\nAlert from {user.first_name}"

    await update.message.reply_text(text, parse_mode="Markdown")

    await update.message.reply_text("✅ Your alert has been sent to the admins.")

# COUNT MESSAGES
async def count_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    name = user.username if user.username else user.first_name

    if user.id in afk_users:
        await update.message.reply_text(
            f"☀️ Welcome back {user.first_name}! You are no longer AFK."
        )
        del afk_users[user.id]

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

# KANG
async def kang(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a sticker to kang it.")
        return

    sticker = update.message.reply_to_message.sticker

    if not sticker:
        await update.message.reply_text("That is not a sticker.")
        return

    user = update.effective_user
    bot = context.bot

    pack_name = f"{user.id}_pack_by_{bot.username}"
    pack_title = f"{user.first_name}'s Kang Pack"

    emoji = sticker.emoji if sticker.emoji else "🔥"

    file = await bot.get_file(sticker.file_id)

    file_path = f"{sticker.file_unique_id}.webp"

    await file.download_to_drive(file_path)

    try:

        await bot.add_sticker_to_set(
            user_id=user.id,
            name=pack_name,
            png_sticker=open(file_path, "rb"),
            emojis=emoji
        )

    except:

        try:

            await bot.create_new_sticker_set(
                user_id=user.id,
                name=pack_name,
                title=pack_title,
                png_sticker=open(file_path, "rb"),
                emojis=emoji
            )

        except Exception as e:
            await update.message.reply_text(f"Failed to kang sticker.\n{e}")
            return

    await update.message.reply_text(
        f"🦝 Sticker Kang'd!\n\nhttps://t.me/addstickers/{pack_name}"
    )

# WEEKLY RESET
async def reset_leaderboard(context: ContextTypes.DEFAULT_TYPE):
    global message_count
    message_count = {}

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("network", network))
app.add_handler(CommandHandler("admins", admins))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("top", top))

app.add_handler(CommandHandler("alert", alert))
app.add_handler(CommandHandler("afk", afk))
app.add_handler(CommandHandler("kang", kang))

app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("kick", kick))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))

app.add_handler(CommandHandler("tempmute", tempmute))
app.add_handler(CommandHandler("purge", purge))
app.add_handler(CommandHandler("userinfo", userinfo))
app.add_handler(CommandHandler("stats", stats))

app.add_handler(CommandHandler("lock", lock))
app.add_handler(CommandHandler("unlock", unlock))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_messages))

app.job_queue.run_repeating(reset_leaderboard, interval=604800, first=604800)

print("Bot started...")

app.run_polling() 
