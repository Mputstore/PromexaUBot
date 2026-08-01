from pyrogram import Client


def create_client(api_id, api_hash, session_name):
    """
    Membuat Pyrogram Client berdasarkan
    API_ID, API_HASH dan nama session.
    """

    return Client(
        name=f"sessions/{session_name}",
        api_id=int(api_id),
        api_hash=api_hash,
        workdir="."
    )