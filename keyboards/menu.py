from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 Order Jasa Sebar",
                callback_data="order"
            )
        ],

        [
            InlineKeyboardButton(
                "💎 Membership",
                callback_data="package"
            )
        ],

        [
            InlineKeyboardButton(
                "🛒 Shop",
                callback_data="shop"
            ),
            InlineKeyboardButton(
                "🎟 Voucher",
                callback_data="voucher"
            )
        ],

        [
            InlineKeyboardButton(
                "📜 Riwayat",
                callback_data="history"
            ),
            InlineKeyboardButton(
                "👤 Profil",
                callback_data="profil"
            )
        ],

        [
            InlineKeyboardButton(
                "🪙 Coin",
                callback_data="coin"
            ),
            InlineKeyboardButton(
                "💬 Bantuan",
                callback_data="help"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)