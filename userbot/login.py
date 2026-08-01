from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    PasswordHashInvalid
)

from userbot.client import create_client
from userbot.state import update_state


def create_login(api_id, api_hash, session_name):
    """
    Membuat client login.
    """

    app = create_client(
        api_id=api_id,
        api_hash=api_hash,
        session_name=session_name
    )

    update_state(
        int(session_name),
        client=app
    )

    return app


async def send_login_code(app, user_id, phone_number):
    """
    Mengirim kode OTP dan menyimpan phone_code_hash.
    """

    await app.connect()

    sent_code = await app.send_code(phone_number)

    update_state(
        user_id,
        phone=phone_number,
        phone_code_hash=sent_code.phone_code_hash,
        client=app
    )

    return True


async def verify_code(
    app,
    phone_number,
    phone_code_hash,
    code
):
    """
    Verifikasi OTP.
    """

    try:

        await app.sign_in(
            phone_number=phone_number,
            phone_code_hash=phone_code_hash,
            phone_code=code
        )

        me = await app.get_me()

        return {
            "success": True,
            "need_password": False,
            "user": me
        }

    except SessionPasswordNeeded:

        return {
            "success": False,
            "need_password": True
        }

    except PhoneCodeInvalid:

        return {
            "success": False,
            "error": "Kode OTP salah."
        }

    except PhoneCodeExpired:

        return {
            "success": False,
            "error": "Kode OTP sudah kedaluwarsa."
        }


async def verify_password(
    app,
    password
):
    """
    Login 2FA.
    """

    try:

        await app.check_password(password)

        me = await app.get_me()

        return {
            "success": True,
            "user": me
        }

    except PasswordHashInvalid:

        return {
            "success": False,
            "error": "Password 2FA salah."
        }


async def logout(app):
    """
    Logout akun Telegram.
    """

    try:

        await app.log_out()

    except Exception:
        pass

    try:

        await app.disconnect()

    except Exception:
        pass


async def get_me(app):
    """
    Mengambil data akun.
    """

    return await app.get_me()