"""Widget'ni faqat Claude bilan ishlaganda ko'rsatish.

Aktiv (foreground) oyna sarlavhasi kuzatiladi. Agar u "Visual Studio Code"
yoki "Claude" (claude.ai brauzer tab / Claude ilovasi) bo'lsa — widget ekranda
ko'rinadi. Boshqa narsada ishlansa, `grace_seconds` o'tgach yashiriladi.
Fon rejimida ishlab turadi (komp yonganda ko'rinmaydi), monitoring/ogohlantirish
esa yashiringan holatda ham davom etadi.

Windows API `ctypes` orqali chaqiriladi — qo'shimcha kutubxona kerak emas.
"""
import os
import time

try:
    import ctypes
    _user32 = ctypes.windll.user32
except Exception:  # Windows bo'lmasa
    _user32 = None


def _foreground_title_pid():
    """Aktiv oyna sarlavhasi va uni ochgan jarayon PID'ini qaytaradi."""
    if _user32 is None:
        return "", 0
    hwnd = _user32.GetForegroundWindow()
    if not hwnd:
        return "", 0
    length = _user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    _user32.GetWindowTextW(hwnd, buf, length + 1)
    pid = ctypes.c_ulong(0)
    _user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return buf.value or "", pid.value


class VisibilityController:
    """Aktiv oynaga qarab widget'ni ko'rsatadi/yashiradi."""

    def __init__(self, widget, config):
        self.widget = widget
        vis = config.get("visibility", {}) or {}
        self.enabled = vis.get("auto_hide", True)
        self.triggers = [t.lower() for t in vis.get(
            "triggers", ["visual studio code", "claude", "cursor"])]
        self.grace = float(vis.get("grace_seconds", 20))
        self.poll_ms = max(1, int(vis.get("poll_seconds", 2))) * 1000
        self.own_pid = os.getpid()
        self.last_match = 0.0
        self.visible = None  # None = hali aniqlanmagan

    def start(self):
        if _user32 is None:
            return
        if self.enabled:
            self._hide()  # komp yonganda ko'rinmasin
        else:
            self._show()
        self.widget.root.after(self.poll_ms, self._tick)

    def set_enabled(self, enabled):
        """Sozlamadan jonli yoqish/o'chirish."""
        self.enabled = bool(enabled)
        if not self.enabled:
            self._show()  # o'chirilsa doim ko'rinsin

    def _matches(self, title):
        t = title.lower()
        return any(trig in t for trig in self.triggers)

    def _tick(self):
        if not self.enabled:
            self._show()
            self.widget.root.after(self.poll_ms, self._tick)
            return
        try:
            title, pid = _foreground_title_pid()
            now = time.time()
            if pid == self.own_pid:
                # o'zimizning widget/popup fokusda — bosib turgan bo'lishi
                # mumkin, ko'rinishni saqlaymiz
                if self.visible:
                    self.last_match = now
            elif self._matches(title):
                self.last_match = now
                self._show()
            elif now - self.last_match > self.grace:
                self._hide()
        except Exception:
            pass
        self.widget.root.after(self.poll_ms, self._tick)

    def _show(self):
        if self.visible:
            return
        self.visible = True
        r = self.widget.root
        try:
            r.deiconify()
            r.attributes("-topmost",
                         self.widget.config["window"].get("always_on_top", True))
        except Exception:
            pass

    def _hide(self):
        if self.visible is False:
            return
        self.visible = False
        try:
            self.widget.root.withdraw()
        except Exception:
            pass
