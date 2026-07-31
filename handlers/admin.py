from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID

from database.orders import (
    get_pending_orders,
    get_total_income,
    get_total_users,
    get_all_orders,
)


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "⛔ Kamu tidak memiliki akses ke panel admin."
        )
        return

    pending = get_pending_orders()
    users = get_total_users()
    income = get_total_income()
    orders = get_all_orders()

    total_order = len(orders)

    text = (
        "╭────────────────╮\n"
        "      👑 *ADMIN PANEL*\n"
        "╰────────────────╯\n\n"

        f"👥 *Total User*\n"
        f"`{users}`\n\n"

        f"📦 *Total Order*\n"
        f"`{total_order}`\n\n"

        f"⏳ *Pending*\n"
        f"`{pending}`\n\n"

        f"💰 *Pendapatan*\n"
        f"`Rp {income:,}`\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"
        "📋 *5 ORDER TERBARU*\n\n"
    )

    if not orders:

        text += "_Belum ada order._"

    else:

        for invoice, username, layanan, harga, status in orders[:5]:

            if status == "Lunas":
                icon = "🟢"
            elif status == "Menunggu Pembayaran":
                icon = "🟡"
            elif status == "Ditolak":
                icon = "🔴"
            else:
                icon = "⚪"

            user = f"@{username}" if username else "-"

            text += (
                f"🧾 `{invoice}`\n"
                f"👤 {user}\n"
                f"📦 {layanan}\n"
                f"💰 Rp {harga:,}\n"
                f"{icon} {status}\n\n"
            )

    text += (
        "━━━━━━━━━━━━━━━━━━\n"
        "🚀 *PROMEXA UBOT V1 STABLE*"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )