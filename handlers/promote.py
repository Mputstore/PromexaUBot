from telegram import Update
from telegram.ext import ContextTypes

async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    await update.callback_query.message.reply_text(
        "📢 *Menu Promosi*\n\n"
        "Pilih salah satu fitur di bawah.\n\n"
        "• ➕ Tambah Grup\n"
        "• 📋 Daftar Grup\n"
        "• 🚀 Mulai Promosi\n"
        "• ⏹ Stop Promosi",
        parse_mode="Markdown"
    )
