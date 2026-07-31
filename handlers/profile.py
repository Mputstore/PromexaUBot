from telegram import Update
from telegram.ext import ContextTypes

from database.users import get_user


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    telegram_user = update.effective_user

    data = get_user(telegram_user.id)

    username = (
        f"@{telegram_user.username}"
        if telegram_user.username
        else "-"
    )

    if data:

        (
            user_id,
            db_username,
            first_name,
            membership,
            coin,
            expired_at
        ) = data

    else:

        user_id = telegram_user.id
        first_name = telegram_user.first_name or "-"
        membership = "Free"
        coin = 0
        expired_at = "-"

    if not expired_at:
        expired_at = "-"

    text = (
        "╭────────────────╮\n"
        "      👤 *PROFIL AKUN*\n"
        "╰────────────────╯\n\n"

        f"🪪 *Nama*\n"
        f"{first_name}\n\n"

        f"🔗 *Username*\n"
        f"{username}\n\n"

        f"🆔 *User ID*\n"
        f"`{user_id}`\n\n"

        f"⭐ *Membership*\n"
        f"`{membership}`\n\n"

        f"🪙 *Coin*\n"
        f"`{coin}`\n\n"

        f"📅 *Expired*\n"
        f"`{expired_at}`\n\n"

        "━━━━━━━━━━━━━━━━━━\n"
        "❤️ Terima kasih telah menggunakan\n"
        "*PROMEXA UBOT*"
    )

    await query.message.reply_text(
        text,
        parse_mode="Markdown"
    )