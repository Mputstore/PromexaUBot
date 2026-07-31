from telegram import Update
from telegram.ext import ContextTypes

from database.orders import get_user_orders


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    orders = get_user_orders(user_id)

    if not orders:
        await query.message.reply_text(
            "📭 *Belum Ada Riwayat*\n\n"
            "Kamu belum pernah membuat order.",
            parse_mode="Markdown"
        )
        return

    total = len(orders)

    text = (
        "╭────────────────╮\n"
        "      📜 *RIWAYAT ORDER*\n"
        "╰────────────────╯\n\n"
    )

    for no, (invoice, paket, harga, status) in enumerate(orders, start=1):

        if status == "Lunas":
            icon = "🟢"

        elif status == "Menunggu Pembayaran":
            icon = "🟡"

        elif status == "Ditolak":
            icon = "🔴"

        else:
            icon = "⚪"

        text += (
            f"*{no}. {paket}*\n"
            f"🧾 `{invoice}`\n"
            f"💰 Rp {harga:,}\n"
            f"{icon} {status}\n\n"
        )

    text += (
        "━━━━━━━━━━━━━━━━━━\n"
        f"📦 *Total Order :* {total}"
    )

    await query.message.reply_text(
        text,
        parse_mode="Markdown"
    )