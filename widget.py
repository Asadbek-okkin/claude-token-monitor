"""Floating widget UI (tkinter).

Chegara yo'q, shaffof, always-on-top, drag & drop. Ikki panel:
"5 soatlik oyna" va "Haftalik (7 kun)". Har panelda: progress bar (rangi
foizga qarab), foiz, ishlatilgan/limit, QOLGAN token, reset countdown.
"""
import tkinter as tk

import config as cfg_mod


class TokenWidget:
    def __init__(self, config, on_settings=None, on_mute=None, on_quit=None, on_stats=None):
        self.config = config
        self.colors = config["colors"]
        self.on_settings = on_settings
        self.on_mute = on_mute
        self.on_quit = on_quit
        self.on_stats = on_stats
        self.muted = False

        win = config["window"]
        self.root = tk.Tk()
        self.root.title("Claude Token Monitor")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", win.get("always_on_top", True))
        try:
            self.root.attributes("-alpha", win.get("opacity", 0.93))
        except tk.TclError:
            pass
        self.root.geometry(f"{win['width']}x{win['height']}+{win['x']}+{win['y']}")
        self.root.configure(bg=self.colors["bg"])

        self._drag = {"x": 0, "y": 0}
        self._build()

    # ---------- UI ----------
    def _build(self):
        c = self.colors
        plan = self.config.get("active_plan", "Pro")
        ver = self.config.get("_version", "")
        title_text = f"Claude Monitor · {plan}" + (f" · v{ver}" if ver else "")

        header = tk.Frame(self.root, bg=c["panel"], height=30)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        title = tk.Label(header, text=title_text, bg=c["panel"],
                         fg=c["text"], font=("Segoe UI", 9, "bold"))
        title.pack(side="left", padx=8)
        close_btn = tk.Label(header, text="✕", bg=c["panel"], fg=c["muted"],
                             font=("Segoe UI", 10, "bold"), cursor="hand2")
        close_btn.pack(side="right", padx=8)
        close_btn.bind("<Button-1>", lambda e: self._quit())
        for wgt in (header, title):
            wgt.bind("<Button-1>", self._start_drag)
            wgt.bind("<B1-Motion>", self._do_drag)
            wgt.bind("<ButtonRelease-1>", self._end_drag)

        body = tk.Frame(self.root, bg=c["bg"])
        body.pack(fill="both", expand=True, padx=8, pady=2)
        self.code_panel = self._make_panel(body, "5 soatlik oyna")
        self.web_panel = self._make_panel(body, "Haftalik (7 kun)")

        footer = tk.Frame(self.root, bg=c["bg"])
        footer.pack(fill="x", side="bottom", pady=(0, 6), padx=8)
        self.stats_btn = tk.Button(
            footer, text="Statistika", command=self._stats, bg=c["panel"],
            fg=c["accent"], relief="flat", font=("Segoe UI", 8, "bold"), cursor="hand2",
            activebackground=c["accent"], activeforeground="#000000")
        self.stats_btn.pack(side="left", expand=True, fill="x", padx=(0, 3))
        self.settings_btn = tk.Button(
            footer, text="Sozlama", command=self._settings, bg=c["panel"],
            fg=c["text"], relief="flat", font=("Segoe UI", 8), cursor="hand2",
            activebackground=c["accent"], activeforeground="#000000")
        self.settings_btn.pack(side="left", expand=True, fill="x", padx=3)
        self.mute_btn = tk.Button(
            footer, text="Ovoz", command=self._toggle_mute, bg=c["panel"],
            fg=c["text"], relief="flat", font=("Segoe UI", 8), cursor="hand2",
            activebackground=c["accent"], activeforeground="#000000")
        self.mute_btn.pack(side="left", expand=True, fill="x", padx=(3, 0))

    def _make_panel(self, parent, title_text):
        c = self.colors
        panel = {}
        frame = tk.Frame(parent, bg=c["bg"])
        frame.pack(fill="x", pady=3)

        panel["title"] = tk.Label(frame, text=title_text, bg=c["bg"], fg=c["text"],
                                  font=("Segoe UI", 9, "bold"), anchor="w")
        panel["title"].pack(fill="x")

        bar_row = tk.Frame(frame, bg=c["bg"])
        bar_row.pack(fill="x", pady=2)
        panel["canvas"] = tk.Canvas(bar_row, height=14, bg=c["panel"], highlightthickness=0)
        panel["canvas"].pack(side="left", fill="x", expand=True)
        panel["percent"] = tk.Label(bar_row, text="0%", bg=c["bg"], fg=c["text"],
                                    font=("Segoe UI", 9, "bold"), width=5)
        panel["percent"].pack(side="right", padx=(6, 0))

        panel["tokens"] = tk.Label(frame, text="0 / 0", bg=c["bg"], fg=c["muted"],
                                   font=("Segoe UI", 8), anchor="w")
        panel["tokens"].pack(fill="x")
        panel["remaining"] = tk.Label(frame, text="Qolgan: --", bg=c["bg"], fg=c["text"],
                                      font=("Segoe UI", 8, "bold"), anchor="w")
        panel["remaining"].pack(fill="x")
        panel["reset"] = tk.Label(frame, text="Reset: --", bg=c["bg"], fg=c["muted"],
                                  font=("Segoe UI", 8), anchor="w")
        panel["reset"].pack(fill="x")
        return panel

    # ---------- yangilash ----------
    def _color_for(self, percent):
        c = self.colors
        if percent < 60:
            return c["green"]
        if percent < 85:
            return c["yellow"]
        return c["red"]

    def _draw_bar(self, canvas, percent):
        canvas.delete("all")
        canvas.update_idletasks()
        w = canvas.winfo_width()
        if w <= 1:
            w = 180
        h = int(canvas["height"])
        fill_w = int(w * min(percent, 100) / 100)
        canvas.create_rectangle(0, 0, fill_w, h, fill=self._color_for(percent), outline="")

    def update_panel(self, panel, used, maxv, reset_str):
        pct = 0 if maxv <= 0 else min(used / maxv * 100, 100)
        remaining = max(0, maxv - used)
        self._draw_bar(panel["canvas"], pct)
        panel["percent"].config(text=f"{pct:.0f}%", fg=self._color_for(pct))
        panel["tokens"].config(text=f"{used:,} / {maxv:,} token")
        rem_color = self.colors["red"] if remaining == 0 else self._color_for(pct)
        panel["remaining"].config(text=f"Qolgan: {remaining:,} token", fg=rem_color)
        panel["reset"].config(text=f"Reset: {reset_str} qoldi")

    # ---------- drag ----------
    def _start_drag(self, e):
        self._drag["x"] = e.x_root - self.root.winfo_x()
        self._drag["y"] = e.y_root - self.root.winfo_y()

    def _do_drag(self, e):
        self.root.geometry(f"+{e.x_root - self._drag['x']}+{e.y_root - self._drag['y']}")

    def _end_drag(self, e):
        cfg_mod.update_window_position(self.root.winfo_x(), self.root.winfo_y())

    # ---------- tugmalar ----------
    def _settings(self):
        if self.on_settings:
            self.on_settings()

    def _stats(self):
        if self.on_stats:
            self.on_stats()

    def show_stats_popup(self, rows):
        """rows — [(sarlavha, token, xabar, izoh), ...] ko'rinishida."""
        c = self.colors
        win = tk.Toplevel(self.root)
        win.title("Statistika")
        win.configure(bg=c["bg"])
        win.attributes("-topmost", True)
        win.resizable(False, False)

        ver = self.config.get("_version", "")
        stitle = "📊 Token statistikasi" + (f"  ·  v{ver}" if ver else "")
        tk.Label(win, text=stitle, bg=c["bg"], fg=c["accent"],
                 font=("Segoe UI", 12, "bold")).pack(pady=(14, 8), padx=20)

        grid = tk.Frame(win, bg=c["bg"])
        grid.pack(padx=20, pady=4, fill="x")
        headers = ("Davr", "Token", "Xabar")
        for col, htext in enumerate(headers):
            tk.Label(grid, text=htext, bg=c["bg"], fg=c["muted"],
                     font=("Segoe UI", 9, "bold"),
                     anchor="w" if col == 0 else "e").grid(row=0, column=col, sticky="ew", padx=6, pady=(0, 4))
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

        for i, (label, tok, msgs, note) in enumerate(rows, start=1):
            tk.Label(grid, text=label, bg=c["bg"], fg=c["text"],
                     font=("Segoe UI", 10, "bold"), anchor="w").grid(row=i, column=0, sticky="ew", padx=6, pady=3)
            tk.Label(grid, text=f"{tok:,}", bg=c["bg"], fg=c["accent"],
                     font=("Segoe UI", 10), anchor="e").grid(row=i, column=1, sticky="ew", padx=6, pady=3)
            tk.Label(grid, text=f"{msgs:,}", bg=c["bg"], fg=c["muted"],
                     font=("Segoe UI", 10), anchor="e").grid(row=i, column=2, sticky="ew", padx=6, pady=3)
            if note:
                tk.Label(grid, text=note, bg=c["bg"], fg=c["muted"],
                         font=("Segoe UI", 8), anchor="w").grid(row=i, column=0, columnspan=3, sticky="w", padx=6)

        tk.Button(win, text="Yopish", command=win.destroy, bg=c["accent"], fg="#000000",
                  font=("Segoe UI", 9, "bold"), relief="flat", padx=24, pady=6,
                  cursor="hand2").pack(pady=(10, 16))

        win.update_idletasks()
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        pw, ph = win.winfo_width(), win.winfo_height()
        win.geometry(f"+{(sw - pw) // 2}+{(sh - ph) // 2}")

    def _toggle_mute(self):
        self.muted = not self.muted
        self.mute_btn.config(text="Jim" if self.muted else "Ovoz")
        if self.on_mute:
            self.on_mute(self.muted)

    def _quit(self):
        if self.on_quit:
            self.on_quit()
        else:
            self.root.destroy()
