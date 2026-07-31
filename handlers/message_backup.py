from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Hanya menerima teks promosi jika sedang menunggu promosi
    if not context.user_data.get("waiting_promosi", False):
        return

    text = update.message.text

    # Simpan teks promosi
    context.user_data["promosi"] = text

    keyboard = [
    [InlineKeyboardButton("🌱 Trial", callback_data="paket_trial")],
    [InlineKeyboardButton("📦 Basic", callback_data="paket_basic")],
    [InlineKeyboardButton("💎 Premium ⭐", callback_data="paket_premium")],
]

    await update.message.reply_text(
    "🚀 *PROMEXA UBOT*\n\n"
    "_Fast • Easy • Trusted_\n\n"
    "Pilih paket yang sesuai dengan kebutuhanmu.\n\n"
    "━━━━━━━━━━━━━━\n\n"
    "🌱 *Trial*\n"
    "💰 Rp 5.000\n"
    "🗓️ 7 Hari\n\n"
    "📦 *Basic*\n"
    "💰 Rp 10.000\n"
    "🗓️ 30 Hari\n\n"
    "💎 *Premium ⭐*\n"
    "✨ _Paling Direkomendasikan_\n"
    "💰 Rp 20.000\n"
    "🗓️ 30 Hari\n\n"
    "━━━━━━━━━━━━━━",
    parse_mode="Markdown",
    reply_markup=InlineKeyboardMarkup(keyboard)
)