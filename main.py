"""Claude Token Monitor - kirish nuqtasi.

Plan preset limitiga nisbatan 5 soatlik + haftalik sarf, statistika,
ogohlantirish va avtomatik yangilanish (GitHub Releases).
"""
import os
import sys
import threading
import tkinter as tk

import config as cfg_mod
import i18n
import monitor_code
import monitor_web
import startup
import updater
import version
from notifier import Notifier
from visibility import VisibilityController
from widget import TokenWidget


def build_tray(widget, on_quit, on_check_update, on_set_language):
    try:
        import pystray
        from PIL import Image, ImageDraw
    except Exception:
        return None

    img = Image.new("RGB", (64, 64), "#1a1d27")
    d = ImageDraw.Draw(img)
    d.ellipse((14, 14, 50, 50), fill="#f0a500")
    d.ellipse((26, 26, 38, 38), fill="#1a1d27")

    def show(icon, item):
        widget.root.after(0, widget.root.deiconify)
        widget.root.after(0, lambda: widget.root.attributes("-topmost", True))

    def hide(icon, item):
        widget.root.after(0, widget.root.withdraw)

    def check(icon, item):
        on_check_update(True)

    def quit_(icon, item):
        try:
            icon.stop()
        except Exception:
            pass
        widget.root.after(0, on_quit)

    def make_lang_item(code):
        return pystray.MenuItem(
            i18n.LANG_NAMES[code],
            lambda icon, item: on_set_language(code, icon),
            checked=lambda item, c=code: i18n.get_language() == c,
            radio=True)

    lang_menu = pystray.Menu(*[make_lang_item(c) for c in i18n.LANGUAGES])

    # matnlar callable — til o'zgarganda update_menu() bilan yangilanadi
    menu = pystray.Menu(
        pystray.MenuItem(lambda item: i18n.t("tray_show"), show, default=True),
        pystray.MenuItem(lambda item: i18n.t("tray_check_update"), check),
        pystray.MenuItem(lambda item: i18n.t("tray_language"), lang_menu),
        pystray.MenuItem(lambda item: i18n.t("tray_hide"), hide),
        pystray.MenuItem(lambda item: i18n.t("tray_quit"), quit_),
    )
    return pystray.Icon("claude_token_monitor", img,
                        f"Claude Token Monitor v{version.__version__}", menu)


def _pct(used, maxv):
    return 0 if maxv <= 0 else used / maxv * 100


def main():
    # --version bayrog'i (konsoldan tekshirish uchun)
    if "--version" in sys.argv:
        print(version.__version__)
        return

    config = cfg_mod.load_config()
    config["_version"] = version.__version__  # widget header uchun

    # Interfeys tilini o'rnatish
    i18n.set_language(config.get("language", "uz"))

    # Komp yonganda o'zi (ko'rinmas) ishga tushishi uchun Run kalitiga yozish
    startup.ensure(config.get("autostart", True))

    notifier = Notifier(config)
    running = {"alive": True}
    tray_holder = {"icon": None}
    handlers = {}  # refresh() ni keyinroq bog'lash uchun

    def _persist_config():
        # _version kabi vaqtinchalik (underscore) kalitlarni saqlamaymiz
        data = {k: v for k, v in config.items() if not str(k).startswith("_")}
        cfg_mod.save_config(data)

    def on_set_language(lang, icon=None):
        if lang not in i18n.LANGUAGES:
            return
        i18n.set_language(lang)
        config["language"] = lang
        _persist_config()
        widget.retranslate()
        r = handlers.get("refresh")
        if r:
            widget.root.after(0, r)  # dinamik panellarni darhol yangilash
        if icon is not None:
            try:
                icon.update_menu()
            except Exception:
                pass

    def on_settings():
        try:
            os.startfile(cfg_mod.config_path())
        except Exception:
            pass

    def on_mute(muted):
        notifier.muted = muted

    def on_stats():
        try:
            sess_limit, week_limit = cfg_mod.plan_limits(config)
            sh = int(config.get("session_hours", 5))
            wh = int(config.get("weekly_days", 7)) * 24
            d = monitor_code.read_windows((sh, 24, wh, 720))
            s5, d1, d7, d30 = d[sh], d[24], d[wh], d[720]

            def note(used, mx):
                p = 0 if mx <= 0 else used / mx * 100
                return i18n.t("note_limit", p=f"{p:.0f}", mx=f"{mx:,}")

            rows = [
                (i18n.t("row_5h_now"), s5["total"], s5["messages"], note(s5["total"], sess_limit)),
                (i18n.t("row_today"), d1["total"], d1["messages"], ""),
                (i18n.t("row_weekly"), d7["total"], d7["messages"], note(d7["total"], week_limit)),
                (i18n.t("row_monthly"), d30["total"], d30["messages"], ""),
            ]
            widget.show_stats_popup(rows)
        except Exception:
            pass

    def on_quit():
        running["alive"] = False
        try:
            if tray_holder["icon"]:
                tray_holder["icon"].stop()
        except Exception:
            pass
        try:
            widget.root.destroy()
        except Exception:
            pass

    # ---------- Yangilanish ----------
    def _info_popup(text):
        c = config["colors"]
        win = tk.Toplevel(widget.root)
        win.title(i18n.t("update_title"))
        win.configure(bg=c["bg"])
        win.attributes("-topmost", True)
        win.resizable(False, False)
        tk.Label(win, text=text, bg=c["bg"], fg=c["text"],
                 font=("Segoe UI", 10, "bold")).pack(padx=34, pady=(22, 8))
        tk.Button(win, text=i18n.t("btn_ok"), command=win.destroy, bg=c["accent"], fg="#000000",
                  font=("Segoe UI", 9, "bold"), relief="flat", padx=24, pady=6,
                  cursor="hand2").pack(pady=(0, 16))
        _center(win)

    def _prompt_update(tag, exe_url, notes):
        c = config["colors"]
        win = tk.Toplevel(widget.root)
        win.title(i18n.t("newver_title"))
        win.configure(bg=c["bg"])
        win.attributes("-topmost", True)
        win.resizable(False, False)

        tk.Label(win, text=i18n.t("newver_heading"), bg=c["bg"], fg=c["accent"],
                 font=("Segoe UI", 13, "bold")).pack(pady=(16, 6), padx=26)
        tk.Label(win, text=i18n.t("newver_cur_new", cur=version.__version__, new=tag),
                 bg=c["bg"], fg=c["text"], font=("Segoe UI", 10)).pack()
        if notes:
            tk.Label(win, text=notes.strip()[:220], bg=c["bg"], fg=c["muted"],
                     font=("Segoe UI", 8), wraplength=340, justify="left").pack(pady=6, padx=26)
        status = tk.Label(win, text="", bg=c["bg"], fg=c["yellow"], font=("Segoe UI", 9))
        status.pack()

        btns = tk.Frame(win, bg=c["bg"])
        btns.pack(pady=(8, 16))

        def do_update():
            status.config(text=i18n.t("updating"))
            yes_btn.config(state="disabled")
            later_btn.config(state="disabled")

            def worker():
                try:
                    ok = updater.apply_update(exe_url)
                except Exception:
                    ok = False
                if ok:
                    widget.root.after(0, on_quit)  # bat almashtirib qayta ochadi
                else:
                    widget.root.after(0, lambda: status.config(
                        text=i18n.t("update_err"), fg=c["red"]))

            threading.Thread(target=worker, daemon=True).start()

        yes_btn = tk.Button(btns, text=i18n.t("btn_update"), command=do_update, bg=c["accent"],
                            fg="#000000", font=("Segoe UI", 9, "bold"), relief="flat",
                            padx=20, pady=6, cursor="hand2")
        yes_btn.pack(side="left", padx=6)
        later_btn = tk.Button(btns, text=i18n.t("btn_later"), command=win.destroy, bg=c["panel"],
                              fg=c["text"], font=("Segoe UI", 9), relief="flat",
                              padx=20, pady=6, cursor="hand2")
        later_btn.pack(side="left", padx=6)
        _center(win)

    def _center(win):
        win.update_idletasks()
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        pw, ph = win.winfo_width(), win.winfo_height()
        win.geometry(f"+{(sw - pw) // 2}+{(sh - ph) // 2}")

    def check_updates(manual=False):
        ucfg = config.get("update", {})
        if not ucfg.get("enabled", True) and not manual:
            return
        repo = ucfg.get("repo", "")

        def worker():
            tag, exe_url, notes = updater.get_latest(repo)
            if tag and exe_url and updater.is_newer(tag):
                if ucfg.get("auto", False) and getattr(sys, "frozen", False):
                    try:
                        if updater.apply_update(exe_url):
                            widget.root.after(0, on_quit)
                            return
                    except Exception:
                        pass
                widget.root.after(0, lambda: _prompt_update(tag, exe_url, notes))
            elif manual:
                widget.root.after(0, lambda: _info_popup(i18n.t("up_to_date")))

        threading.Thread(target=worker, daemon=True).start()

    # ---------- Ishga tushirish ----------
    widget = TokenWidget(config, on_settings=on_settings, on_mute=on_mute,
                         on_quit=on_quit, on_stats=on_stats)
    notifier.set_root(widget.root)

    tray_icon = build_tray(widget, on_quit, check_updates, on_set_language)
    if tray_icon is not None:
        tray_holder["icon"] = tray_icon
        notifier.tray_icon = tray_icon
        threading.Thread(target=tray_icon.run, daemon=True).start()

    interval_ms = int(config.get("refresh_interval", 30)) * 1000
    session_hours = int(config.get("session_hours", 5))
    weekly_hours = int(config.get("weekly_days", 7)) * 24
    prev_secs = {"v": None}

    def refresh():
        if not running["alive"]:
            return
        try:
            sess_limit, week_limit = cfg_mod.plan_limits(config)
            data = monitor_code.read_windows((session_hours, weekly_hours))
            sess = data[session_hours]
            week = data[weekly_hours]

            secs, reset_str = monitor_web.reset_countdown(sess["earliest"], session_hours)
            if prev_secs["v"] is not None and secs > prev_secs["v"] + 60:
                notifier.reset_notifications()
            prev_secs["v"] = secs
            widget.update_panel(widget.code_panel, sess["total"], sess_limit, reset_str)
            notifier.check_and_notify(i18n.t("period_5h"), _pct(sess["total"], sess_limit))

            if config.get("show_weekly", True):
                w_secs, w_reset = monitor_web.reset_countdown(week["earliest"], weekly_hours)
                widget.update_panel(widget.web_panel, week["total"], week_limit, w_reset)
                notifier.check_and_notify(i18n.t("period_weekly"), _pct(week["total"], week_limit))
        except Exception:
            pass
        widget.root.after(interval_ms, refresh)

    handlers["refresh"] = refresh  # til o'zgarganda darhol chaqirish uchun
    widget.root.after(500, refresh)

    # Faqat Claude bilan ishlaganda ko'rsatish (aks holda yashiringan turadi)
    visibility = VisibilityController(widget, config)
    visibility.start()

    # ochilganda yangilanishni tekshirish (faqat .exe rejimida nag qilmaslik uchun)
    if getattr(sys, "frozen", False):
        widget.root.after(3000, lambda: check_updates(manual=False))
    widget.root.mainloop()


if __name__ == "__main__":
    main()
