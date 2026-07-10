"""Reset countdown va vaqt formatlash yordamchisi.

Limit "rolling window" — reset oynadagi eng erta xabardan `window_hours`
soat keyin bo'ladi. 5 soatlik uchun "H:MM", haftalik uchun "N kun M soat".
"""
import calendar
from datetime import date, datetime, timedelta, timezone

import i18n


def format_span(seconds):
    """Soniyani odam o'qiy oladigan ko'rinishga o'giradi (til bo'yicha)."""
    seconds = max(0, int(seconds))
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    if days > 0:
        return i18n.t("span_dh", d=days, h=hours)
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


def subscription_days(start_date_str):
    """Obuna boshlangan sanadan keyingi oylik yangilanishgacha necha kun.

    start_date_str: "YYYY-MM-DD" (nuqta/slash ham qabul qilinadi).
    Qaytaradi: (qolgan_kun, "YYYY-MM-DD" yangilanish sanasi) yoki None.
    Pro/Max oylik obuna — yangilanish sotib olingan kun (day-of-month) da.
    """
    if not start_date_str or not str(start_date_str).strip():
        return None
    try:
        parts = str(start_date_str).strip().replace(".", "-").replace("/", "-").split("-")
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
        date(y, m, d)  # validatsiya
    except Exception:
        return None

    today = datetime.now().date()

    def anniversary(yy, mm):
        last = calendar.monthrange(yy, mm)[1]   # oy oxiridan oshmasin (31->28)
        return date(yy, mm, min(d, last))

    nxt = anniversary(today.year, today.month)
    if nxt < today:
        mm, yy = today.month + 1, today.year
        if mm > 12:
            mm, yy = 1, yy + 1
        nxt = anniversary(yy, mm)
    return (nxt - today).days, nxt.isoformat()


if __name__ == "__main__":
    print(reset_countdown(None, 5))
    print(reset_countdown(datetime.now(timezone.utc) - timedelta(days=2, hours=3), 168))
    print(subscription_days("2026-06-20"))
