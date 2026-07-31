from telegram import BotCommand


async def set_commands(app):
    commands = [
        BotCommand("start", "🚀 Mulai Bot"),
        BotCommand("menu", "📋 Menu Utama"),
        BotCommand("order", "📦 Buat Order"),
        BotCommand("profile", "👤 Profil Saya"),
        BotCommand("riwayat", "📜 Riwayat Order"),
        BotCommand("pending", "⏳ Order Pending"),
        BotCommand("help", "❓ Bantuan"),
        BotCommand("admin", "👑 Panel Admin"),
    ]

    await app.bot.set_my_commands(commands)