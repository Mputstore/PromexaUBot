from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def package(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "🌱 Trial",
                callback_data="paket_trial"
            )
        ],
        [
            InlineKeyboardButton(
                "📦 Basic",
                callback_data="paket_basic"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 Premium ⭐",
                callback_data="paket_premium"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Kembali",
                callback_data="order"
            )
        ],
    ]

    text = (
        "💎 *DAFTAR PAKET PROMEXA UBOT*\n\n"

        "━━━━━━━━━━━━━━\n\n"

        "🌱 *TRIAL*\n"
        "💰 Rp 5.000\n"
        "🗓️ Masa Aktif : 7 Hari\n\n"

        "📦 *BASIC*\n"
        "💰 Rp 10.000\n"
        "🗓️ Masa Aktif : 30 Hari\n\n"

        "💎 *PREMIUM ⭐*\n"
        "👑 Paket Paling Direkomendasikan\n"
        "💰 Rp 20.000\n"
        "🗓️ Masa Aktif : 30 Hari\n\n"

        "━━━━━━━━━━━━━━\n\n"

        "Silakan pilih paket yang ingin dibeli."
    )

    await query.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )