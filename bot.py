from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import random

TOKEN = "8638803031:AAFcqafHFSD_hUTobO0oknmeEsfK4vphkyc"

warns = {}
message_count = {}

welcome_messages = {}
welcome_media = {}

# NEW SYSTEM DATA
afk_users = {}
karma = {}
blacklist_words = ["badword1","badword2"]

jokes = [
"Why don’t programmers like nature? Too many bugs.",
"I told my computer I needed a break, it froze.",
"Debugging: removing bugs.",
"Why do Java devs wear glasses? Because they don’t C#.",
"There are 10 types of people: those who understand binary and those who don’t.",
"Programmer diet: coffee, pizza and more coffee.",
"Why did the developer go broke? Because he used up all his cache.",
"A SQL query walks into a bar and asks: Can I join you?",
"Computers make very fast, very accurate mistakes.",
"I changed my password to incorrect so whenever I forget it says 'Your password is incorrect'."
    "Teacher: Tum late kyun aaye?
Student: Sir, ek aadmi ka 1000 ka note gir gaya tha…
Teacher: Toh tum help kar rahe the?
Student: Nahi sir… main us note ke upar khada tha! 😆" 
]

# ADMIN CHECK
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    member = await context.bot.get_chat_member(chat_id, user_id)

    return member.status in ["administrator", "creator"]

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This Bad Girl is Healthy And Ready To Dominate 💕")

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

♛ Supreme Overseer - @incautious_yuan 

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

# WELCOME NEW MEMBER
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    # jo new member join hua hai usko detect karega
    for user in update.message.new_chat_members:

        # agar admin ne custom message set kiya hai to wo use hoga
        text = welcome_messages.get(chat_id)

        # agar custom message nahi hai to default message
        if not text:
            text = f"Welcome {user.first_name}!"

        await update.message.reply_text(text)

# HELP
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""⚙️ HeavenFall Bot Commands

━━━━━━━━━━━━━━

👤 General Commands

/start
/rules
/network
/admins
/top
/help
/alert

/social
/afk
/karma
/couples
/joke

━━━━━━━━━━━━━━

🛡 Admin Moderation

/warn
/kick
/ban
/mute
/unmute
/tempmute
/purge
/userinfo
/stats
/lock
/unlock

━━━━━━━━━━━━━━

⚠️ Moderation commands are restricted to administrators.
"""
)

# SET WELCOME MESSAGE
async def setwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # admin check
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can set welcome message.")
        return

    chat_id = update.effective_chat.id

    # command ke baad jo text likha hoga wo welcome message ban jayega
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "Usage:\n/setwelcome Welcome message here"
        )
        return

    # message save karna
    welcome_messages[chat_id] = text

    await update.message.reply_text("✅ Welcome message saved successfully.")


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

    # AFK RETURN
    if user.id in afk_users:
        del afk_users[user.id]
        await update.message.reply_text(
            f"🎉 Welcome back {name}! AFK removed."
        )

    # BLACKLIST FILTER
    for word in blacklist_words:
        if word.lower() in update.message.text.lower():
            try:
                await update.message.delete()
            except:
                pass
            await update.message.reply_text("⚠️ Message removed due to blacklist word.")
            break

# AFK
async def afk(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    reason = " ".join(context.args) if context.args else "AFK"

    afk_users[user.id] = reason

    await update.message.reply_text(
        f"😴 {user.first_name} is now AFK\nReason: {reason}"
    )

# KARMA
async def karma_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user.")
        return

    user = update.message.reply_to_message.from_user

    karma[user.id] = karma.get(user.id, 0) + 1

    await update.message.reply_text(
        f"✨ {user.first_name} gained karma!\nTotal: {karma[user.id]}"
    )

# COUPLES
async def couples(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users = list(message_count.values())

    if len(users) < 2:
        await update.message.reply_text("Not enough users yet.")
        return

    pair = random.sample(users, 2)

    await update.message.reply_text(
        f"💘 Couples of the Day 💘\n\n"
        f"{pair[0]['name']} ❤️ {pair[1]['name']}"
    )

# JOKE
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(random.choice(jokes))

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
app.add_handler(CommandHandler("karma", karma_cmd))
app.add_handler(CommandHandler("couples", couples))
app.add_handler(CommandHandler("joke", joke))

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

app.add_handler(CommandHandler("warn", warn))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_messages))

app.job_queue.run_repeating(reset_leaderboard, interval=604800, first=604800)

print("Bot started...")

app.run_polling()
