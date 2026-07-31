from telegram import Update
from telegram.ext import ContextTypes

from database.orders import (
    get_order,
    update_order_status,
)

from database.users import update_membership


async def verify_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    try:
        action, invoice = query.data.split("|", 1)
    except ValueError:
        await query.answer(
            "Data tidak valid.",
            show_alert=True
        )
        return

    order = get_order(invoice)

    if not order:
        await query.edit_message_caption(
            caption="❌ Invoice tidak ditemukan."
        )
        return

    invoice, user_id, username, layanan, harga, status = order

    # ==========================
    # SUDAH DIPROSES
    # ==========================

    if status == "Lunas":

        await query.answer(
            "Order ini sudah disetujui sebelumnya.",
            show_alert=True
        )
        return

    if status == "Ditolak":

        await query.answer(
            "Order ini sudah ditolak.",
            show_alert=True
        )
        return

    # ==========================
    # APPROVE
    # ==========================

    if action == "approve":

        update_order_status(
            invoice,
            "Lunas"
        )

        update_membership(
            user_id,
            layanan
        )

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "🎉 *Pembayaran Berhasil*\n\n"
                f"🧾 Invoice : `{invoice}`\n"
                f"📦 Paket : {layanan}\n\n"
                "✅ Membership telah aktif.\n"
                "🚀 Order akan segera diproses."
            ),
            parse_mode="Markdown"
        )

        await query.edit_message_caption(
            caption=(
                "✅ *PEMBAYARAN DITERIMA*\n\n"
                f"🧾 `{invoice}`\n"
                f"📦 {layanan}\n"
                "📌 Status : Lunas"
            ),
            parse_mode="Markdown"
        )

        return

    # ==========================
    # REJECT
    # ==========================

    if action == "reject":

        update_order_status(
            invoice,
            "Ditolak"
        )

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "❌ *Pembayaran Ditolak*\n\n"
                f"🧾 Invoice : `{invoice}`\n\n"
                "Silakan kirim ulang bukti pembayaran."
            ),
            parse_mode="Markdown"
        )

        await query.edit_message_caption(
            caption=(
                "❌ *PEMBAYARAN DITOLAK*\n\n"
                f"🧾 `{invoice}`"
            ),
            parse_mode="Markdown"
        )