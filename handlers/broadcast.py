from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID
from database.users import get_all_users

waiting_broadcast = {}


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "⛔ Akses ditolak."
        )
        return

    waiting_broadcast[update.effective_user.id] = True

    await update.message.reply_text(
        "📢 *MODE BROADCAST*\n\n"
        "Silakan kirim pesan yang ingin dikirim ke seluruh pengguna.\n\n"
        "Bisa berupa teks biasa.",
        parse_mode="Markdown"
    )


async def process_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if not waiting_broadcast.get(update.effective_user.id):
        return

    waiting_broadcast.pop(update.effective_user.id)

    users = get_all_users()

    sukses = 0
    gagal = 0

    text = update.message.text

    for user_id, username, first_name in users:

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    "📢 *PENGUMUMAN PROMEXA UBOT*\n\n"
                    f"{text}"
                ),
                parse_mode="Markdown"
            )

            sukses += 1

        except Exception:
            gagal += 1

    await update.message.reply_text(
        "✅ *Broadcast Selesai*\n\n"
        f"📨 Berhasil : `{sukses}`\n"
        f"❌ Gagal : `{gagal}`",
        parse_mode="Markdown"
    )