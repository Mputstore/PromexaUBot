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
                callback_data="shop_voucher"
            )
        ],

        [
            InlineKeyboardButton(
                "🤖 Userbot",
                callback_data="userbot"
            ),
            InlineKeyboardButton(
                "👤 Profil",
                callback_data="profil"
            )
        ],

        [
            InlineKeyboardButton(
                "📜 Riwayat",
                callback_data="history"
            ),
            InlineKeyboardButton(
                "⚙️ Pengaturan",
                callback_data="setting"
            )
        ],

        ]

    return InlineKeyboardMarkup(keyboard)