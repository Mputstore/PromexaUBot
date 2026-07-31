from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TOKEN
from handlers.start import start
from handlers.profile import profile
from handlers.promote import promote
from handlers.order import order
from handlers.message import save_message
from database.orders import save_order


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    print("CALLBACK:", query.data)
    await query.answer()

    if query.data == "order":
        await order(update, context)

    elif query.data == "profil":
        await profile(update, context)

    elif query.data == "promosi":
        await promote(update, context)

    elif query.data == "shop":
        await query.message.reply_text(
            "🛒 Shop masih dalam pengembangan."
        )

    elif query.data == "coin":
        await query.message.reply_text(
            "💰 Coin kamu: 0"
        )

    elif query.data == "setting":
        await query.message.reply_text(
            "⚙️ Menu pengaturan belum tersedia."
        )

    # =========================
    # 🌱 Trial
    # =========================
    elif query.data == "paket_trial":

        invoice = save_order(
    query.from_user.id,
    query.from_user.username or "",
    "Trial",
    0,
    "7 Hari",
    5000,
    context.user_data.get("promosi", "")
)

        await query.message.reply_photo(
    photo=open("assets/qris.png", "rb"),
    caption=(
        "🚀 *PROMEXA UBOT*\n\n"

        "🧾 *PROMEXA INVOICE*\n\n"

        f"🆔 Invoice : `{invoice}`\n"
        f"👤 User : @{query.from_user.username or 'User'}\n\n"

        "🌱 Paket : *Trial*\n"
        "🗓️ Durasi : *7 Hari*\n"
        "💰 Total : *Rp 5.000*\n\n"

        "━━━━━━━━━━━━━━\n"
        "⏳ *Status : Menunggu Pembayaran*\n"
        "━━━━━━━━━━━━━━\n\n"

        "📲 Silakan scan QRIS di atas.\n"
        "📸 Setelah transfer, kirim bukti pembayaran ke chat ini."
    ),
    parse_mode="Markdown"
)
    # =========================
    # 📦 Basic
    # =========================
    elif query.data == "paket_basic":

        invoice = save_order(
            query.from_user.id,
            query.from_user.username or "",
            "Basic",
            0,
            "30 Hari",
            10000,
            context.user_data.get("promosi", "")
        )

        await query.message.reply_photo(
            photo=open("assets/qris.png", "rb"),
            caption=(
                "🚀 *PROMEXA UBOT*\n\n"
                "🧾 *PROMEXA INVOICE*\n\n"
                f"👤 @{query.from_user.username or 'User'}\n\n"
                "📦 Paket : *Basic*\n"
                "🗓️ Durasi : *30 Hari*\n"
                "💰 Total : *Rp 10.000*\n\n"
                "📲 Silakan scan QRIS di atas.\n"
                "📸 Setelah membayar, kirim bukti pembayaran."
            ),
            parse_mode="Markdown"
        )

    # =========================
    # 💎 Premium
    # =========================
    elif query.data == "paket_premium":

        invoice = save_order(
            query.from_user.id,
            query.from_user.username or "",
            "Premium",
            0,
            "30 Hari",
            20000,
            context.user_data.get("promosi", "")
        )

        await query.message.reply_photo(
            photo=open("assets/qris.png", "rb"),
            caption=(
                "🚀 *PROMEXA UBOT*\n\n"
                "🧾 *PROMEXA INVOICE*\n\n"
                f"👤 {query.from_user.mention_markdown_v2()}\n\n"
                "💎 Paket : *Premium ⭐*\n"
                "🗓️ Durasi : *30 Hari*\n"
                "💰 Total : *Rp 20.000*\n\n"
                "📲 Silakan scan QRIS di atas.\n"
                "📸 Setelah membayar, kirim bukti pembayaran."
            ),
            parse_mode="MarkdownV2"
        )

    elif query.data == "help":
        await query.message.reply_text(
            "❓ Hubungi admin jika membutuhkan bantuan."
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_message))

print("🤖 Mput Promote Bot berjalan...")
app.run_polling()