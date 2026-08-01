from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.sessions import (
    session_exists,
    get_session,
)

from userbot.state import create_state, set_step


async def userbot_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    telegram_user = update.effective_user

    if session_exists(telegram_user.id):

        data = get_session(telegram_user.id)

        phone = data["phone_number"] or "-"
        username = data["username"] or "-"
        first_name = data["first_name"] or "-"
        status = "🟢 Terhubung" if data["is_connected"] else "🔴 Terputus"

        text = (
            "🤖 *USERBOT SAYA*\n\n"
            f"Status : {status}\n"
            f"Nama : {first_name}\n"
            f"Username : @{username}\n"
            f"Nomor : {phone}\n\n"
            "Silakan pilih menu di bawah."
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔄 Login Ulang",
                    callback_data="userbot_login"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚪 Logout",
                    callback_data="userbot_logout"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Kembali",
                    callback_data="back_menu"
                )
            ]
        ])

    else:

        text = (
            "🤖 *USERBOT SAYA*\n\n"
            "Status : ❌ Belum Terhubung\n\n"
            "Silakan hubungkan akun Telegram Anda."
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔑 Atur API",
                    callback_data="userbot_api"
                )
            ],
            [
                InlineKeyboardButton(
                    "📱 Login Telegram",
                    callback_data="userbot_login"
                )
            ],
            [
                InlineKeyboardButton(
                    "📖 Panduan",
                    callback_data="userbot_help"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Kembali",
                    callback_data="back_menu"
                )
            ]
        ])

    await query.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


async def set_api(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    create_state(user_id)
    set_step(user_id, "api_id")

    await query.message.reply_text(
        "🔑 *PENGATURAN API*\n\n"
        "Silakan kirim *API_ID* Telegram Anda.\n\n"
        "Contoh:\n"
        "`12345678`",
        parse_mode="Markdown"
    )