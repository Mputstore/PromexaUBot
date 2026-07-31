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
        await update.message.reply_text("⛔ Kamu tidak memiliki akses.")
        return

    pending = get_pending_orders()
    users = get_total_users()
    income = get_total_income()
    orders = get_all_orders()

    text = (
        "👑 *PROMEXA ADMIN*\n\n"
        "━━━━━━━━━━━━━━\n\n"
        f"📦 Order Pending : *{pending}*\n"
        f"👥 Total User : *{users}*\n"
        f"💰 Pendapatan : *Rp {income:,}*\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "📥 *5 Pesanan Terbaru*\n\n"
    )

    if not orders:
        text += "_Belum ada pesanan._"
    else:
        for invoice, username, layanan, harga, status in orders[:5]:
            user = f"@{username}" if username else "-"
            text += (
                f"🧾 *{invoice}*\n"
                f"👤 {user}\n"
                f"📦 {layanan}\n"
                f"💰 Rp {harga:,}\n"
                f"📌 {status}\n\n"
            )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )