from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID

from database.orders import (
    get_all_orders,
    get_pending_orders_list,
    get_paid_orders,
    get_rejected_orders,
    get_total_income,
)


async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        await query.answer(
            "⛔ Akses ditolak.",
            show_alert=True
        )
        return

    # =====================================
    # SEMUA ORDER
    # =====================================

    if query.data == "admin_orders":

        orders = get_all_orders()

        if not orders:
            await query.message.reply_text(
                "📭 Belum ada pesanan."
            )
            return

        text = "📋 *SEMUA ORDER*\n\n"

        for invoice, username, layanan, harga, status in orders:

            user = f"@{username}" if username else "-"

            text += (
                f"🧾 `{invoice}`\n"
                f"👤 {user}\n"
                f"📦 {layanan}\n"
                f"💰 Rp {harga:,}\n"
                f"📌 {status}\n\n"
            )

        await query.message.reply_text(
            text,
            parse_mode="Markdown"
        )

    # =====================================
    # ORDER PENDING
    # =====================================

    elif query.data == "admin_pending":

        orders = get_pending_orders_list()

        if not orders:
            await query.message.reply_text(
                "📭 Tidak ada order pending."
            )
            return

        text = "⏳ *ORDER MENUNGGU PEMBAYARAN*\n\n"

        for invoice, username, layanan, harga, status in orders:

            user = f"@{username}" if username else "-"

            text += (
                f"🧾 `{invoice}`\n"
                f"👤 {user}\n"
                f"📦 {layanan}\n"
                f"💰 Rp {harga:,}\n"
                f"📌 {status}\n\n"
            )

        await query.message.reply_text(
            text,
            parse_mode="Markdown"
        )

    # =====================================
    # ORDER LUNAS
    # =====================================

    elif query.data == "admin_paid":

        orders = get_paid_orders()

        if not orders:
            await query.message.reply_text(
                "📭 Belum ada order lunas."
            )
            return

        text = "✅ *ORDER LUNAS*\n\n"

        for invoice, username, layanan, harga, status in orders:

            user = f"@{username}" if username else "-"

            text += (
                f"🧾 `{invoice}`\n"
                f"👤 {user}\n"
                f"📦 {layanan}\n"
                f"💰 Rp {harga:,}\n"
                f"📌 {status}\n\n"
            )

        await query.message.reply_text(
            text,
            parse_mode="Markdown"
        )

    # =====================================
    # ORDER DITOLAK
    # =====================================

    elif query.data == "admin_rejected":

        orders = get_rejected_orders()

        if not orders:
            await query.message.reply_text(
                "📭 Belum ada order ditolak."
            )
            return

        text = "❌ *ORDER DITOLAK*\n\n"

        for invoice, username, layanan, harga, status in orders:

            user = f"@{username}" if username else "-"

            text += (
                f"🧾 `{invoice}`\n"
                f"👤 {user}\n"
                f"📦 {layanan}\n"
                f"💰 Rp {harga:,}\n"
                f"📌 {status}\n\n"
            )

        await query.message.reply_text(
            text,
            parse_mode="Markdown"
        )

    # =====================================
    # PENDAPATAN
    # =====================================

    elif query.data == "admin_income":

        total = get_total_income()

        await query.message.reply_text(
            (
                "💰 *TOTAL PENDAPATAN*\n\n"
                f"Rp {total:,}"
            ),
            parse_mode="Markdown"
        )