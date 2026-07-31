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
from handlers.broadcast import (
    broadcast,
    process_broadcast,
)
from handlers.commands import set_commands
from handlers.shop import shop


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    print("CALLBACK:", query.data)
    await query.answer()

    # Verifikasi pembayaran
    if query.data.startswith("approve|") or query.data.startswith("reject|"):
        await verify_payment(update, context)
        return

    # Menu Admin
    if query.data.startswith("admin_"):
        await admin_callback(update, context)
        return

    if query.data == "order":
        await order(update, context)

    elif query.data == "profil":
        await profile(update, context)

    elif query.data == "package":
        await package(update, context)

    elif query.data == "history":
        await history(update, context)

    elif query.data == "promosi":
        await promote(update, context)

    elif query.data == "shop":
        await shop(update, context)

    elif query.data == "coin":
        await query.message.reply_text(
            "💰 Coin kamu: 0"
        )

    elif query.data == "setting":
        await query.message.reply_text(
            "⚙️ Menu pengaturan belum tersedia."
        )

    elif query.data == "paket_trial":
        await send_invoice(
            update,
            context,
            "Trial",
            "7 Hari",
            5000
        )

    elif query.data == "paket_basic":
        await send_invoice(
            update,
            context,
            "Basic",
            "30 Hari",
            10000
        )

    elif query.data == "paket_premium":
        await send_invoice(
            update,
            context,
            "Premium",
            "30 Hari",
            20000
        )

    elif query.data == "help":
        await query.message.reply_text(
            "❓ Hubungi admin jika membutuhkan bantuan."
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin_panel))
app.add_handler(CommandHandler("broadcast", broadcast))

app.add_handler(CallbackQueryHandler(button))

app.add_handler(
    MessageHandler(
        (filters.TEXT | filters.PHOTO) & ~filters.COMMAND,
        process_broadcast,
    )
)

app.add_handler(
    MessageHandler(
        (filters.TEXT | filters.PHOTO) & ~filters.COMMAND,
        save_message,
    )
)

app.post_init = set_commands

print("🤖 PromexaUBot berjalan...")
app.run_polling()