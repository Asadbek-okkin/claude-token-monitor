"""Reset countdown va vaqt formatlash yordamchisi.

Limit "rolling window" — reset oynadagi eng erta xabardan `window_hours`
soat keyin bo'ladi. 5 soatlik uchun "H:MM", haftalik uchun "N kun M soat".
"""
from datetime import datetime, timedelta, timezone


def format_span(seconds):
    """Soniyani odam o'qiy oladigan ko'rinishga o'giradi."""
    seconds = max(0, int(seconds))
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    if days > 0:
        return f"{days} kun {hours} soat"
    return f"{hours}:{minutes:02d}"


# orqaga moslik uchun eski nom
format_hms = format_span


def reset_countdown(earliest_ts, window_hours=5):
    """Reset gacha qolgan vaqtni hisoblaydi.

    earliest_ts — oynadagi eng erta xabar (UTC) yoki None.
    Qaytaradi: (qolgan_soniya, "matn").
    """
    now = datetime.now(timezone.utc)
    if earliest_ts is None:
        secs = window_hours * 3600
    else:
        reset_at = earliest_ts + timedelta(hours=window_hours)
        secs = (reset_at - now).total_seconds()
        if secs < 0:
            secs = 0
    return secs, format_span(secs)


if __name__ == "__main__":
    print(reset_countdown(None, 5))
    print(reset_countdown(datetime.now(timezone.utc) - timedelta(days=2, hours=3), 168))
