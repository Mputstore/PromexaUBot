from telegram import Update
from telegram.ext import ContextTypes

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📢 *Buat Pesanan*\n\n"
        "Silakan kirim teks promosi yang ingin disebarkan.",
        parse_mode="Markdown"
    )

    context.user_data["waiting_promosi"] = True