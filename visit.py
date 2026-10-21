import telebot
import requests
import os

# 🔐 Bot Token (⚠️ Move this to environment variable or config file in production)
BOT_TOKEN = 'BOT_TOKEN'7951176988:AAHZWBr7iTavC0DT0kxCsgZ_JFXQ8Z_gpvI

# ✅ Group ID allowed to use /visit command
ALLOWED_GROUP_ID = GROUP_ID

bot = telebot.TeleBot(BOT_TOKEN) 

@bot.message_handler(commands=['visit'])
def handle_visit(message):
    # 🔒 Allow only in specific group
    if message.chat.id != ALLOWED_GROUP_ID-1003718158424
        return

    try:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(
                message,
                "❌ Wrong format!\n✅ Use: <code>/visit IND 10320389026</code>",
                parse_mode="HTML"
            )
            return

        region = args[1].strip()
        uid = args[2].strip()

        # ⏳ Show waiting message
        wait_msg = bot.reply_to(message, "⏳ <b>Processing your visit request...</b>", parse_mode="HTML")

        url = f"YOUR-API-GIVEN-JENIL"

        # 🌐 Make request to API with timeout and error handling
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            bot.edit_message_text(
                f"⚠️ API request failed: <code>{str(e)}</code>",
                chat_id=message.chat.id,
                message_id=wait_msg.message_id,
                parse_mode="HTML"
            )
            return

        if response.status_code != 200:
            bot.edit_message_text(
                f"❌ API Error: <b>{response.status_code}</b>",
                chat_id=message.chat.id,
                message_id=wait_msg.message_id,
                parse_mode="HTML"
            )
            return

        if "application/json" not in response.headers.get("Content-Type", ""):
            bot.edit_message_text(
                "⚠️ Unexpected API response format (not JSON).",
                chat_id=message.chat.id,
                message_id=wait_msg.message_id,
                parse_mode="HTML"
            )
            return

        data = response.json()

        if data.get("fail") == 0:
            reply_text = (
                "╭─────────────────────⟡⟡⟡⟡⟡⟡⟡⟡⟡⟡⟡⟡─────────────────────╮\n"
                "┃                    🌌 𝗚𝗔𝗠𝗘𝗥 𝗣𝗥𝗢𝗙𝗜𝗟𝗘 𝗥𝗘𝗣𝗢𝗥𝗧                   ┃\n"
                "╰─────────────────────⟡⟡⟡⟡⟡⟡⟡⟡⟡⟡⟡⟡─────────────────────╯\n\n"
                f"🎮 <b>Name</b>       : <code>{data.get('nickname')}</code>\n"
                f"🆔 <b>UID</b>        : <code>{data.get('uid')}</code>\n"
                f"🌍 <b>Region</b>     : <b>{data.get('region')}</b>\n"
                f"📶 <b>Level</b>      : <b>{data.get('level')}</b>\n"
                f"💖 <b>Likes</b>      : <b>{data.get('likes')}</b>\n"
                f"📩 <b>Visit Status</b> : ✅ <b>{data.get('success')}</b>    ❌ <b>{data.get('fail')}</b>\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🏷 <i>Generated securely by</i> <b>@J4NIL_CODEX</b>"
            )
        else:
            reply_text = "❌ Visit Failed. Please check your UID or Region."

        bot.edit_message_text(
            reply_text,
            chat_id=message.chat.id,
            message_id=wait_msg.message_id,
            parse_mode="HTML"
        )

    except Exception as e:
        bot.reply_to(
            message,
            f"⚠️ Unexpected error: <code>{str(e)}</code>",
            parse_mode="HTML"
        )

# 🚀 Start the bot
bot.polling()