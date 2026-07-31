from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from keyboards.menu import main_menu
from database.users import save_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Simpan user ke database
    save_user(update.effective_user)

    user = update.effective_user.first_name

    text = f"""
🚀 <b>PROMEXA UBOT</b>

Halo <b>{user}</b> 👋

Selamat datang di layanan <b>Jasa Sebar Telegram</b>.

Kami siap membantu promosi Telegram kamu
dengan cepat, aman, dan terpercaya.

Silakan pilih menu di bawah.

━━━━━━━━━━━━━━
<b>Fast • Easy • Trusted</b>
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )

    await update.message.reply_text(
        "Silakan pilih menu:",
        reply_markup=main_menu()
    )