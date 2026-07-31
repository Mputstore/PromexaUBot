from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID


async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # USER MENGIRIM BUKTI PEMBAYARAN
    if update.message.photo:

        photo = update.message.photo[-1].file_id

        invoice = context.user_data.get("invoice", "-")
        promosi = context.user_data.get("promosi", "-")

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Terima",
                    callback_data=f"approve|{invoice}"
                ),
                InlineKeyboardButton(
                    "❌ Tolak",
                    callback_data=f"reject|{invoice}"
                )
            ]
        ]

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=(
                "💳 *BUKTI PEMBAYARAN BARU*\n\n"
                f"🧾 Invoice : `{invoice}`\n"
                f"👤 User : @{update.effective_user.username or 'User'}\n"
                f"📢 Promosi : {promosi}"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.message.reply_text(
            "✅ Bukti pembayaran berhasil dikirim.\n\n"
            "Mohon tunggu admin melakukan verifikasi."
        )
        return

    # USER MENGIRIM PROMOSI
    if not context.user_data.get("waiting_promosi", False):
        return

    context.user_data["promosi"] = update.message.text
    context.user_data["waiting_promosi"] = False

    keyboard = [
        [InlineKeyboardButton("🌱 Trial", callback_data="paket_trial")],
        [InlineKeyboardButton("📦 Basic", callback_data="paket_basic")],
        [InlineKeyboardButton("💎 Premium ⭐", callback_data="paket_premium")],
    ]

    await update.message.reply_text(
        "Silakan pilih paket:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )