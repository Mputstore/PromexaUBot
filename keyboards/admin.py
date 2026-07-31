from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def admin_menu():
    keyboard = [
        [
            InlineKeyboardButton("📦 Order", callback_data="admin_orders"),
            InlineKeyboardButton("👥 User", callback_data="admin_users"),
        ],
        [
            InlineKeyboardButton("💰 Pendapatan", callback_data="admin_income"),
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
        ],
        [
            InlineKeyboardButton("⚙️ Pengaturan", callback_data="admin_setting"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)