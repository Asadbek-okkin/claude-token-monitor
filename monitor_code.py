"""Claude Code token o'quvchi.

~/.claude/projects/**/*.jsonl fayllaridan bir yoki bir nechta vaqt oynasi
uchun tokenlarni yig'adi (rolling window). Bitta fayl skanida ham 5 soatlik,
ham 7 kunlik (haftalik) yig'indini hisoblaydi.
"""
import glob
import json
import os
from datetime import datetime, timedelta, timezone


def _log_files():
    home = os.path.expanduser("~")
    pattern = os.path.join(home, ".claude", "projects", "**", "*.jsonl")
    return glob.glob(pattern, recursive=True)


def _parse_ts(value):
    if not value:
        return None
    try:
        if isinstance(value, str) and value.endswith("Z"):
            value = value[:-1] + "+00:00"
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def _blank():
    return {"input": 0, "output": 0, "cache_creation": 0, "cache_read": 0,
            "total": 0, "messages": 0, "earliest": None}


def read_windows(hours_list=(5, 168)):
    """Bir necha vaqt oynasi uchun tokenlarni bitta skanda yig'adi.

    hours_list — soatlar ro'yxati (masalan (5, 168)).
    Qaytaradi: {hours: {input, output, ..., total, messages, earliest}}.
    """
    now = datetime.now(timezone.utc)
    cutoffs = {h: now - timedelta(hours=h) for h in hours_list}
    oldest_cut = min(cutoffs.values())
    res = {h: _blank() for h in hours_list}

    for path in _log_files():
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)
        except OSError:
            continue
        if mtime < oldest_cut:
            continue  # eng katta oynadan ham eski — o'tkazib yuborish

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    ts = _parse_ts(data.get("timestamp"))
                    usage = (data.get("message") or {}).get("usage") or {}
                    if not usage:
                        continue

                    inp = usage.get("input_tokens", 0) or 0
                    out = usage.get("output_tokens", 0) or 0
                    cc = usage.get("cache_creation_input_tokens", 0) or 0
                    cr = usage.get("cache_read_input_tokens", 0) or 0

                    for h in hours_list:
                        if ts is None or ts >= cutoffs[h]:
                            r = res[h]
                            r["input"] += inp
                            r["output"] += out
                            r["cache_creation"] += cc
                            r["cache_read"] += cr
                            r["messages"] += 1
                            if ts is not None and (r["earliest"] is None or ts < r["earliest"]):
                                r["earliest"] = ts
        except (PermissionError, OSError):
            continue

    for h in hours_list:
        res[h]["total"] = res[h]["input"] + res[h]["output"]
    return res


def read_usage(window_hours=5):
    """Bitta oyna uchun (orqaga moslik)."""
    return read_windows((window_hours,))[window_hours]


if __name__ == "__main__":
    data = read_windows((5, 168))
    for h, label in ((5, "5 soatlik"), (168, "Haftalik (7 kun)")):
        d = data[h]
        print(f"{label}: total={d['total']:,}  in={d['input']:,}  out={d['output']:,}  "
              f"xabar={d['messages']}  eng_erta={d['earliest']}")
