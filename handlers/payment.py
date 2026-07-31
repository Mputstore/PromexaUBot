from telegram import Update
from telegram.ext import ContextTypes

from database.orders import save_order


async def send_invoice(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    paket,
    durasi,
    harga,
):
    query = update.callback_query

    invoice = save_order(
        query.from_user.id,
        query.from_user.username or "",
        paket,
        0,
        durasi,
        harga,
        context.user_data.get("promosi", "")
    )

    context.user_data["invoice"] = invoice
    await query.message.reply_photo(
        photo=open("assets/qris.png", "rb"),
        caption=(
            "🚀 *PROMEXA UBOT*\n\n"

            "🧾 *PROMEXA INVOICE*\n\n"

            f"🆔 Invoice : `{invoice}`\n"
            f"👤 User : @{query.from_user.username or 'User'}\n\n"

            f"📦 Paket : *{paket}*\n"
            f"🗓️ Durasi : *{durasi}*\n"
            f"💰 Total : *Rp {harga:,}*\n\n"

            "━━━━━━━━━━━━━━\n"
            "⏳ *Status : Menunggu Pembayaran*\n"
            "━━━━━━━━━━━━━━\n\n"

            "📲 Silakan scan QRIS di atas.\n"
            "📸 Setelah transfer, kirim bukti pembayaran ke chat ini."
        ),
        parse_mode="Markdown"
    )
