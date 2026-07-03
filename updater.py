"""Avtomatik yangilanish — GitHub Releases orqali (APK'dagidek).

Ilova ochilganda eng so'nggi relizni tekshiradi; yangisi bo'lsa yangi .exe ni
yuklab oladi, o'zini almashtiradigan .bat ni ishga tushiradi va qayta ochiladi.
Almashtirish bati: joriy jarayon yopilishini kutadi -> eski exe ni yangisiga
almashtiradi -> qayta ishga tushiradi.
"""
import os
import subprocess
import sys

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from version import __version__

CREATE_NO_WINDOW = 0x08000000


def parse_version(v):
    """'v1.2.3' / '1.2.3' -> (1,2,3). Buzuq bo'lsa (0,)."""
    v = (v or "").lstrip("vV").strip()
    out = []
    for part in v.split("."):
        digits = "".join(ch for ch in part if ch.isdigit())
        out.append(int(digits) if digits else 0)
    return tuple(out) if out else (0,)


def current_version():
    return __version__


def is_newer(tag):
    return parse_version(tag) > parse_version(__version__)


ASSET_NAME = "ClaudeTokenMonitor.exe"


def get_latest(repo, timeout=10):
    """Eng so'nggi relizni aniqlaydi (tag, exe_url, notes).

    api.github.com (60 so'rov/soat limitli) o'rniga github.com'ning
    /releases/latest redirect'idan foydalanadi — rate limitga tushmaydi.
    /releases/latest -> 302 -> /releases/tag/<tag>. Yuklab olish manzili
    /releases/latest/download/<asset> doim eng so'nggisiga ishora qiladi.
    """
    if not HAS_REQUESTS or not repo:
        return None, None, ""
    url = f"https://github.com/{repo}/releases/latest"
    try:
        r = requests.get(url, allow_redirects=False, timeout=timeout,
                         headers={"User-Agent": "ClaudeTokenMonitor"})
    except Exception:
        return None, None, ""
    loc = r.headers.get("Location", "")
    if not loc or "/tag/" not in loc:
        return None, None, ""
    tag = loc.rstrip("/").split("/")[-1]  # .../releases/tag/v1.0.0 -> v1.0.0
    if not tag:
        return None, None, ""
    exe_url = f"https://github.com/{repo}/releases/latest/download/{ASSET_NAME}"
    return tag, exe_url, ""


def download(exe_url, dest, timeout=300):
    r = requests.get(exe_url, stream=True, headers={"User-Agent": "ClaudeTokenMonitor"}, timeout=timeout)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 16):
            if chunk:
                f.write(chunk)
    return dest


def write_update_script(exe_path, new_path):
    """Eski exe ni yangisiga almashtiruvchi .bat yaratadi, yo'lini qaytaradi."""
    exe_dir = os.path.dirname(exe_path)
    exe_name = os.path.basename(exe_path)
    bat = os.path.join(exe_dir, "_update.bat")
    with open(bat, "w", encoding="ascii", errors="ignore") as f:
        f.write(
            "@echo off\r\n"
            "timeout /t 2 /nobreak >nul\r\n"
            ":wait\r\n"
            f'tasklist /fi "IMAGENAME eq {exe_name}" | find /i "{exe_name}" >nul '
            "&& (timeout /t 1 /nobreak >nul & goto wait)\r\n"
            f'move /y "{new_path}" "{exe_path}" >nul\r\n'
            # Yangi exe joyiga o'tgach, antivirus skaneri va fayl tizimi tinchlanishi
            # uchun biroz kutamiz — aks holda onefile Python DLL ekstraksiyasi to'qnashadi.
            "timeout /t 4 /nobreak >nul\r\n"
            f'start "" "{exe_path}"\r\n'
            'del "%~f0"\r\n'
        )
    return bat


def apply_update(exe_url):
    """Yangi exe ni yuklab, almashtirish batini ishga tushiradi.

    True = muvaffaqiyat, endi ilovani yopish kerak (bat almashtirib qayta ochadi).
    Faqat .exe (frozen) rejimida ishlaydi.
    """
    if not getattr(sys, "frozen", False):
        return False
    exe_path = sys.executable
    new_path = exe_path + ".new"

    download(exe_url, new_path)
    if not os.path.exists(new_path) or os.path.getsize(new_path) < 1_000_000:
        try:
            os.remove(new_path)
        except OSError:
            pass
        return False

    bat = write_update_script(exe_path, new_path)
    subprocess.Popen(["cmd", "/c", bat], creationflags=CREATE_NO_WINDOW,
                     cwd=os.path.dirname(exe_path), close_fds=True)
    return True
