async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
"""📜 **HeavenFall Network — Rules**

This is a **mature community**. Follow the rules to keep the group safe.

1️⃣ No NSFW or explicit content  
2️⃣ Respect all members — no harassment or hate  
3️⃣ No abusive or offensive language  
4️⃣ No spam, ads, or promotions without permission  
5️⃣ No scams or misleading links  
6️⃣ Keep discussions relevant  

⚠️ Breaking rules may result in **warn, mute, kick, or ban**.
"""
    )
