"""Fikr va takliflar — foydalanuvchi xabarini (va ixtiyoriy skrinshotni)
bot orqali dastur egasining Telegramiga yuboradi.

Bot kaliti `secrets_local.py` da (gitignore). Ekran rasmi PIL.ImageGrab bilan.
Tarmoq ishi fon oqimida — UI qotib qolmasin.
"""
import os
import tempfile
import threading

import version

try:
    import requests
    HAS_REQUESTS = True
except Exception:
    HAS_REQUESTS = False

try:
    import secrets_local as _sec
except Exception:
    _sec = None


def _owner():
    """(bot_token, chat_id) — secrets_local yoki muhit o'zgaruvchilaridan."""
    if _sec is not None:
        return (getattr(_sec, "FEEDBACK_BOT_TOKEN", ""),
                getattr(_sec, "FEEDBACK_CHAT_ID", ""))
    return (os.environ.get("CTM_FB_TOKEN", ""), os.environ.get("CTM_FB_CHAT", ""))


def available():
    """Fikr yuborish sozlanganmi (token bor va requests mavjud)."""
    token, chat = _owner()
    return bool(HAS_REQUESTS and token and chat)


def capture_screen():
    """Butun ekranni rasmga oladi, vaqtinchalik fayl yo'lini qaytaradi."""
    from PIL import ImageGrab
    path = os.path.join(tempfile.gettempdir(), "ctm_feedback.png")
    img = ImageGrab.grab()
    img.save(path)
    return path


def send(text, name="", country="", image_path=None, on_done=None):
    """Fikrni fon oqimida yuboradi; tugagach on_done(ok: bool) chaqiriladi."""
    def worker():
        ok = False
        try:
            token, chat = _owner()
            if HAS_REQUESTS and token and chat:
                try:
                    import i18n
                    lang = i18n.get_language()
                except Exception:
                    lang = "?"
                who = ""
                if name.strip():
                    who += f"👤 Ism: {name.strip()}\n"
                if country.strip():
                    who += f"🌍 Davlat: {country.strip()}\n"
                header = (f"📝 Fikr va taklif (v{version.__version__}, til={lang}):\n"
                          f"{who}\n{text}")
                if image_path and os.path.exists(image_path):
                    url = f"https://api.telegram.org/bot{token}/sendPhoto"
                    with open(image_path, "rb") as f:
                        r = requests.post(url, data={"chat_id": chat, "caption": header[:1024]},
                                          files={"photo": f}, timeout=25)
                    ok = r.ok
                else:
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    r = requests.post(url, data={"chat_id": chat, "text": header}, timeout=15)
                    ok = r.ok
        except Exception:
            ok = False
        if on_done:
            try:
                on_done(ok)
            except Exception:
                pass

    threading.Thread(target=worker, daemon=True).start()
