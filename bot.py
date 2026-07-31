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
from handlers.package import package
from handlers.history import history
from handlers.promote import promote
from handlers.order import order
from handlers.message import save_message
from handlers.admin import admin_panel
from handlers.payment import send_invoice
from handlers.admin_callback import admin_callback
from handlers.verify import verify_payment
from handlers.broadcast import broadcast, process_broadcast
from handlers.commands import set_commands
from handlers.shop import shop


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    print("CALLBACK:", query.data)

    if query.data.startswith("approve|") or query.data.startswith("reject|"):
        await verify_payment(update, context)
        return

    if query.data.startswith("admin_"):
        await admin_callback(update, context)
        return

    if query.data == "order":
        await order(update, context)
        return

    if query.data == "profil":
        await profile(update, context)
        return

    if query.data == "package":
        await package(update, context)
        return

    if query.data == "history":
        await history(update, context)
        return

    if query.data == "promosi":
        await promote(update, context)
        return

    if query.data == "shop":
        await shop(update, context)
        return

 elif query.data == "shop_coin":
        await query.message.reply_text(
        "🪙 *TUKAR COIN*\n\n"
        "Segera hadir.\n\n"
        "Nantinya coin dapat ditukar dengan:\n"
        "• Voucher Diskon\n"
        "• Trial Gratis\n"
        "• Upgrade Membership",
        parse_mode="Markdown"
    )
    return

 elif query.data == "shop_upgrade":
        await query.message.reply_text(
        "⭐ *MEMBERSHIP*\n\n"
        "Segera hadir.\n\n"
        "Level Membership:\n"
        "🥉 Silver\n"
        "🥈 Gold\n"
        "🥇 Platinum",
        parse_mode="Markdown"
    )
    return

 elif query.data == "shop_voucher":
        await query.message.reply_text(
        "🎟 *VOUCHER*\n\n"
        "Belum memiliki voucher.\n\n"
        "Voucher dapat diperoleh dari:\n"
        "• Tukar Coin\n"
        "• Event\n"
        "• Giveaway",
        parse_mode="Markdown"
    )
    return

    if query.data == "coin":
        await query.message.reply_text("💰 Coin kamu: 0")
        return

    if query.data == "setting":
        await query.message.reply_text(
            "⚙️ Menu pengaturan belum tersedia."
        )
        return

    if query.data == "help":
        await query.message.reply_text(
            "❓ Hubungi admin jika membutuhkan bantuan."
        )
        return

    if query.data == "paket_trial":
        await send_invoice(update, context, "Trial", "7 Hari", 5000)
        return

    if query.data == "paket_basic":
        await send_invoice(update, context, "Basic", "30 Hari", 10000)
        return

    if query.data == "paket_premium":
        await send_invoice(update, context, "Premium", "30 Hari", 20000)
        return


app = Application.builder().token(TOKEN).build()

# COMMAND
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin_panel))
app.add_handler(CommandHandler("broadcast", broadcast))

# BUTTON
app.add_handler(CallbackQueryHandler(button))

# PESAN USER (Order, Bukti Pembayaran)
app.add_handler(
    MessageHandler(
        (filters.TEXT | filters.PHOTO) & ~filters.COMMAND,
        save_message,
    ),
    group=0,
)

# BROADCAST ADMIN
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        process_broadcast,
    ),
    group=1,
)

app.post_init = set_commands

print("🤖 PromexaUBot berjalan...")
app.run_polling()