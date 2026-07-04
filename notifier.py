"""Ogohlantirish tizimi: ovoz + tray + popup + Telegram.

3 daraja: 80% (WARNING), 90% (HIGH), 95% (CRITICAL).
Har daraja har manba (Claude Code / claude.ai) uchun faqat BIR MARTA
ogohlantiriladi. Reset bo'lganda tozalanadi.
"""
import threading
import tkinter as tk

import i18n

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class Notifier:
    def __init__(self, config, root=None):
        self.config = config
        self.root = root
        self.tray_icon = None       # widget/main tomonidan o'rnatiladi
        self.muted = False          # "Jim" tugmasi
        self.notified = {}          # {manba: {threshold: bool}}

    def set_root(self, root):
        self.root = root

    # ------- asosiy tekshiruv -------
    def check_and_notify(self, source_name, percent):
        thresholds = sorted(set(self.config.get("notifications", {}).get("thresholds", [80, 90, 95])))
        src = self.notified.setdefault(source_name, {t: False for t in thresholds})

        for t in sorted(thresholds, reverse=True):
            if percent >= t:
                if not src.get(t, False):
                    self._notify_all(source_name, percent, self._level_for(t))
                    for lower in thresholds:  # o'tib ketilgan pastroq darajalar ham "bajarildi"
                        if lower <= t:
                            src[lower] = True
                break  # faqat eng yuqori kesib o'tilgan daraja

    def reset_notifications(self):
        self.notified = {}

    @staticmethod
    def _level_for(threshold):
        if threshold >= 95:
            return "CRITICAL"
        if threshold >= 90:
            return "HIGH"
        return "WARNING"

    # ------- yuborish -------
    def _notify_all(self, source, percent, level):
        threading.Thread(target=self._send_telegram, args=(source, percent, level), daemon=True).start()
        if not self.muted and self.config.get("notifications", {}).get("sound", True):
            self._play_sound(level)
        if self.config.get("notifications", {}).get("tray", True):
            self._show_tray(source, percent, level)
        if level == "CRITICAL" and self.config.get("notifications", {}).get("popup_at_95", True):
            if self.root is not None:
                self.root.after(0, lambda: self._show_popup(source, percent))

    def _play_sound(self, level):
        if not HAS_WINSOUND:
            return
        try:
            if level == "WARNING":
                winsound.Beep(800, 300)
            elif level == "HIGH":
                winsound.Beep(1000, 500)
                winsound.Beep(1000, 500)
            elif level == "CRITICAL":
                for _ in range(3):
                    winsound.Beep(1200, 400)
        except Exception:
            pass

    def _show_tray(self, source, percent, level):
        title = i18n.t("notify_tray_title", level=level)
        msg = i18n.t("notify_tray_msg", source=source, percent=f"{percent:.0f}")
        try:
            if self.tray_icon is not None:
                self.tray_icon.notify(msg, title)
        except Exception:
            pass

    def _show_popup(self, source, percent):
        """Ekran markazida ogohlantirish oynasi (95% da)."""
        try:
            c = self.config.get("colors", {})
            bg = c.get("bg", "#1a1d27")
            popup = tk.Toplevel(self.root)
            popup.title(i18n.t("popup_title"))
            popup.attributes("-topmost", True)
            popup.configure(bg=bg)
            popup.geometry("400x180")

            tk.Label(popup, text=i18n.t("popup_heading"),
                     font=("Segoe UI", 14, "bold"), fg=c.get("red", "#ef4444"), bg=bg).pack(pady=15)
            tk.Label(popup, text=i18n.t("popup_used", source=source, percent=f"{percent:.0f}"),
                     font=("Segoe UI", 11), fg=c.get("text", "#e8eaf0"), bg=bg).pack()
            tk.Label(popup, text=i18n.t("popup_advice"),
                     font=("Segoe UI", 10), fg=c.get("muted", "#7a8099"), bg=bg).pack(pady=5)
            tk.Button(popup, text=i18n.t("btn_ok_got"), command=popup.destroy,
                      bg=c.get("accent", "#f0a500"), fg="#000000",
                      font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8).pack(pady=10)

            popup.update_idletasks()
            sw, sh = popup.winfo_screenwidth(), popup.winfo_screenheight()
            pw, ph = popup.winfo_width(), popup.winfo_height()
            popup.geometry(f"+{(sw - pw) // 2}+{(sh - ph) // 2}")
        except Exception:
            pass

    def _send_telegram(self, source, percent, level):
        cfg = self.config.get("telegram", {})
        if not cfg.get("enabled", False) or not HAS_REQUESTS:
            return
        token = cfg.get("bot_token", "")
        chat_id = cfg.get("chat_id", "")
        if not token or not chat_id or "YOUR_" in str(token):
            return

        icons = {"WARNING": "⚠️", "HIGH": "\U0001f534", "CRITICAL": "\U0001f6a8"}
        text = (
            f"{icons.get(level, '')} *Claude Token Monitor*\n\n"
            f"{i18n.t('tg_reached', source=source, percent=f'{percent:.0f}')}\n"
            f"{i18n.t('tg_limit_near')}\n\n"
            f"{i18n.t('tg_advice')}"
        )
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=5)
        except Exception:
            pass  # internet yo'q bo'lsa jim o'tkazib yuborish