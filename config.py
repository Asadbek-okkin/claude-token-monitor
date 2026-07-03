"""Sozlamalarni o'qish/saqlash.

config.json exe yoki script yonida saqlanadi. Yetishmasa DEFAULT_CONFIG dan
yaratiladi. Plan preset tizimi: active_plan tanlanadi, limit plans dan olinadi.
"""
import json
import os
import sys

DEFAULT_CONFIG = {
    "window": {
        "x": 50, "y": 50, "width": 300, "height": 270,
        "opacity": 0.93, "always_on_top": True,
    },
    "refresh_interval": 30,

    # Qaysi obunadasiz — shu plan limiti ishlatiladi
    "active_plan": "Pro",

    # Har plan uchun TAXMINIY limitlar (token). Max 5x/20x ko'paytmasi
    # Anthropic'ning rasmiy ma'lumoti; Pro bazasi kalibrlanadigan taxmin.
    # 5 soatlik limitga urilgan paytdagi songa qarab moslang.
    "plans": {
        "Pro":     {"session_5h": 725000,    "weekly": 4500000},
        "Max 5x":  {"session_5h": 3625000,   "weekly": 22500000},
        "Max 20x": {"session_5h": 14500000,  "weekly": 90000000},
    },
    "session_hours": 5,   # 5 soatlik rolling oyna
    "weekly_days": 7,     # haftalik oyna

    "show_weekly": True,  # ikkinchi panel (haftalik) ko'rsatilsinmi

    "notifications": {
        "sound": True, "tray": True, "popup_at_95": True,
        "thresholds": [80, 90, 95],
    },
    "telegram": {"enabled": False, "bot_token": "YOUR_BOT_TOKEN_HERE", "chat_id": "YOUR_CHAT_ID_HERE"},

    # Avtomatik yangilanish (GitHub Releases). auto=true bo'lsa so'ramasdan yangilaydi.
    "update": {"enabled": True, "auto": False, "repo": "Asadbek-okkin/claude-token-monitor"},
    "colors": {
        "bg": "#1a1d27", "text": "#e8eaf0", "accent": "#f0a500",
        "green": "#3ecf8e", "yellow": "#f0a500", "red": "#ef4444",
        "muted": "#7a8099", "panel": "#232733",
    },
}


def base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def config_path():
    return os.path.join(base_dir(), "config.json")


def _merge(default, override):
    result = dict(default)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config():
    path = config_path()
    if not os.path.exists(path):
        save_config(DEFAULT_CONFIG)
        return json.loads(json.dumps(DEFAULT_CONFIG))
    try:
        with open(path, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
        return _merge(DEFAULT_CONFIG, user_cfg)
    except Exception:
        return json.loads(json.dumps(DEFAULT_CONFIG))


def save_config(cfg):
    try:
        with open(config_path(), "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def plan_limits(cfg):
    """Tanlangan planning (session_5h, weekly) limitlarini qaytaradi."""
    plan = cfg.get("active_plan", "Pro")
    plans = cfg.get("plans", {})
    limits = plans.get(plan) or next(iter(plans.values()), {})
    return int(limits.get("session_5h", 250000)), int(limits.get("weekly", 1500000))


def update_window_position(x, y):
    cfg = load_config()
    cfg["window"]["x"] = int(x)
    cfg["window"]["y"] = int(y)
    save_config(cfg)
