# userbot/state.py

"""
State Manager
Menyimpan status sementara setiap user saat proses login.
"""

from typing import Dict

# Penyimpanan sementara di RAM
_login_states: Dict[int, dict] = {}


def create_state(user_id: int):
    """Membuat state baru."""
    _login_states[user_id] = {
        "step": None,
        "api_id": None,
        "api_hash": None,
        "phone": None,
        "phone_code_hash": None,
        "session_name": None,
        "client": None,
    }


def get_state(user_id: int):
    """Mengambil state user."""
    return _login_states.get(user_id)


def state_exists(user_id: int):
    """Cek apakah state ada."""
    return user_id in _login_states


def set_step(user_id: int, step: str):
    """Mengubah langkah login."""
    if not state_exists(user_id):
        create_state(user_id)

    _login_states[user_id]["step"] = step


def get_step(user_id: int):
    """Mengambil langkah login."""
    if not state_exists(user_id):
        return None

    return _login_states[user_id]["step"]


def update_state(user_id: int, **kwargs):
    """Update data state."""
    if not state_exists(user_id):
        create_state(user_id)

    for key, value in kwargs.items():
        _login_states[user_id][key] = value


def clear_state(user_id: int):
    """Menghapus state."""
    if state_exists(user_id):
        del _login_states[user_id]