from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.users import get_user


async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = get_user(update.effective_user.id)

    coin = 0

    if data:
        coin = data[4]

    keyboard = [
        [
            InlineKeyboardButton(
                "🎁 Tukar Coin",
                callback_data="shop_coin"
            )
        ],
        [
            InlineKeyboardButton(
                "⭐ Upgrade Membership",
                callback_data="shop_upgrade"
            )
        ],
        [
            InlineKeyboardButton(
                "🎟 Voucher",
                callback_data="shop_voucher"
            )
        ]
    ]

    text = (
        "🛒 *PROMEXA SHOP*\n\n"
        f"🪙 Coin kamu : *{coin}*\n\n"
        "Selamat datang di Shop.\n"
        "Gunakan coin untuk mendapatkan berbagai keuntungan.\n\n"
        "✨ Fitur ini akan terus diperbarui."
    )

    await query.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )