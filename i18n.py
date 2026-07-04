"""Ko'p tilli qo'llab-quvvatlash (o'zbek / rus / ingliz).

Global joriy til `_LANG` da saqlanadi. Har modul `i18n.t("kalit", ...)` chaqiradi.
Til o'zgarganda `set_language()` chaqiriladi va UI qayta tarjima qilinadi.
"""

LANGUAGES = ["uz", "ru", "en"]

# Til nomlari (menyu uchun) — har doim o'z tilida yoziladi
LANG_NAMES = {"uz": "O'zbekcha", "ru": "Русский", "en": "English"}

_LANG = "uz"

TRANSLATIONS = {
    "uz": {
        # panellar
        "panel_5h": "5 soatlik oyna",
        "panel_weekly": "Haftalik (7 kun)",
        # tugmalar
        "btn_stats": "Statistika",
        "btn_settings": "Sozlama",
        "btn_sound": "Ovoz",
        "btn_muted": "Jim",
        "btn_close": "Yopish",
        "btn_update": "Yangilash",
        "btn_later": "Keyinroq",
        "btn_ok": "OK",
        "btn_ok_got": "OK — Tushundim",
        # panel matnlari
        "unit_token": "token",
        "tokens_fmt": "{used} / {maxv} token",
        "remaining": "Qolgan: {n} token",
        "remaining_dash": "Qolgan: --",
        "reset_fmt": "Reset: {s} qoldi",
        "reset_dash": "Reset: --",
        # statistika oynasi
        "stats_title": "📊 Token statistikasi",
        "stats_h_period": "Davr",
        "stats_h_token": "Token",
        "stats_h_msg": "Xabar",
        "row_5h_now": "5 soatlik (hozir)",
        "row_today": "Bugun (24 soat)",
        "row_weekly": "Haftalik (7 kun)",
        "row_monthly": "Oylik (30 kun)",
        "note_limit": "limit {p}%  ({mx} token)",
        # davr nomlari (ogohlantirishda)
        "period_5h": "5 soatlik",
        "period_weekly": "Haftalik",
        # tray menyu
        "tray_show": "Ko'rsatish",
        "tray_check_update": "Yangilanishni tekshirish",
        "tray_hide": "Yashirish",
        "tray_quit": "Chiqish",
        "tray_language": "Til / Language",
        # yangilanish oynalari
        "update_title": "Yangilanish",
        "newver_title": "Yangi versiya",
        "newver_heading": "🎉 Yangi versiya chiqdi!",
        "newver_cur_new": "Hozirgi: v{cur}     Yangi: {new}",
        "updating": "Yuklanmoqda... biroz kuting",
        "update_err": "Xato — yoki .exe emas. Qo'lda yuklang.",
        "up_to_date": "Eng so'nggi versiya o'rnatilgan ✓",
        # ogohlantirish
        "notify_tray_title": "Claude Token Monitor — {level}",
        "notify_tray_msg": "{source}: {percent}% ishlatildi! Limit yaqinlashmoqda.",
        "popup_title": "DIQQAT — Token Limiti!",
        "popup_heading": "TOKEN LIMITI YAQINLASHDI!",
        "popup_used": "{source}: {percent}% ishlatildi",
        "popup_advice": "Yangi suhbat boshlang yoki resetni kuting.",
        # telegram
        "tg_reached": "*{source}*: `{percent}%` ga yetdi!",
        "tg_limit_near": "Limit yaqinlashmoqda.",
        "tg_advice": "_Yangi suhbat boshlang yoki resetni kuting._",
        # vaqt
        "span_dh": "{d} kun {h} soat",
        # sozlamalar oynasi
        "settings_title": "⚙️ Sozlamalar",
        "set_sec_general": "Umumiy",
        "set_sec_limits": "Limitlar",
        "set_sec_notify": "Ogohlantirish",
        "set_language": "Til",
        "set_plan": "Reja (obuna)",
        "set_limit_5h": "5 soatlik limit (token)",
        "set_limit_weekly": "Haftalik limit (token)",
        "set_sound": "Ovozli ogohlantirish",
        "set_autostart": "Komp yonganda ishga tushsin",
        "set_autohide": "Faqat Claude bilan ishlaganda ko'rinsin",
        "set_telegram_on": "Telegram ogohlantirish",
        "set_tg_token": "Telegram bot token",
        "set_tg_chat": "Telegram chat ID",
        "btn_save": "Saqlash",
        "btn_cancel": "Bekor qilish",
        "set_saved": "Saqlandi ✓",
        "set_advanced": "Kengaytirilgan (config.json)",
        # fikr va takliflar
        "feedback": "💬 Fikr va takliflar",
        "fb_title": "💬 Fikr va takliflar",
        "fb_hint": "Fikringiz yoki taklifingizni yozing:",
        "fb_capture": "📷 Ekran rasmini olish",
        "fb_choose": "🖼 Rasm tanlash",
        "fb_attached": "Rasm biriktirildi ✓",
        "fb_send": "Yuborish",
        "fb_sending": "Yuborilmoqda...",
        "fb_sent": "Rahmat! Yuborildi ✓",
        "fb_error": "Xato — internet yo'q. Keyinroq urinib ko'ring.",
        "fb_empty": "Iltimos, avval fikr yozing.",
        "fb_name": "Ismingiz",
        "fb_country": "Davlatingiz",
        "set_contact": "Muallif bilan bog'lanish",
        "fb_link_hint": "Fikr va skrinshotni Telegram orqali yuboring. Tugmani bosing — suhbat ochiladi.",
        "fb_open": "Telegram'da yozish",
    },
    "ru": {
        "panel_5h": "5-часовое окно",
        "panel_weekly": "Недельно (7 дней)",
        "btn_stats": "Статистика",
        "btn_settings": "Настройки",
        "btn_sound": "Звук",
        "btn_muted": "Без звука",
        "btn_close": "Закрыть",
        "btn_update": "Обновить",
        "btn_later": "Позже",
        "btn_ok": "OK",
        "btn_ok_got": "OK — Понятно",
        "unit_token": "токенов",
        "tokens_fmt": "{used} / {maxv} токенов",
        "remaining": "Осталось: {n} токенов",
        "remaining_dash": "Осталось: --",
        "reset_fmt": "Сброс через: {s}",
        "reset_dash": "Сброс: --",
        "stats_title": "📊 Статистика токенов",
        "stats_h_period": "Период",
        "stats_h_token": "Токены",
        "stats_h_msg": "Сообщения",
        "row_5h_now": "5 часов (сейчас)",
        "row_today": "Сегодня (24 часа)",
        "row_weekly": "Неделя (7 дней)",
        "row_monthly": "Месяц (30 дней)",
        "note_limit": "лимит {p}%  ({mx} токенов)",
        "period_5h": "5-часовое",
        "period_weekly": "Недельное",
        "tray_show": "Показать",
        "tray_check_update": "Проверить обновления",
        "tray_hide": "Скрыть",
        "tray_quit": "Выход",
        "tray_language": "Язык / Language",
        "update_title": "Обновление",
        "newver_title": "Новая версия",
        "newver_heading": "🎉 Вышла новая версия!",
        "newver_cur_new": "Текущая: v{cur}     Новая: {new}",
        "updating": "Загрузка... подождите",
        "update_err": "Ошибка — или это не .exe. Скачайте вручную.",
        "up_to_date": "Установлена последняя версия ✓",
        "notify_tray_title": "Claude Token Monitor — {level}",
        "notify_tray_msg": "{source}: использовано {percent}%! Лимит близко.",
        "popup_title": "ВНИМАНИЕ — Лимит токенов!",
        "popup_heading": "ЛИМИТ ТОКЕНОВ БЛИЗКО!",
        "popup_used": "{source}: использовано {percent}%",
        "popup_advice": "Начните новый чат или дождитесь сброса.",
        "tg_reached": "*{source}*: достигнуто `{percent}%`!",
        "tg_limit_near": "Лимит близко.",
        "tg_advice": "_Начните новый чат или дождитесь сброса._",
        "span_dh": "{d} дн {h} ч",
        "settings_title": "⚙️ Настройки",
        "set_sec_general": "Общие",
        "set_sec_limits": "Лимиты",
        "set_sec_notify": "Уведомления",
        "set_language": "Язык",
        "set_plan": "План (подписка)",
        "set_limit_5h": "5-часовой лимит (токены)",
        "set_limit_weekly": "Недельный лимит (токены)",
        "set_sound": "Звуковые уведомления",
        "set_autostart": "Запуск при включении ПК",
        "set_autohide": "Показывать только при работе с Claude",
        "set_telegram_on": "Уведомления Telegram",
        "set_tg_token": "Telegram bot token",
        "set_tg_chat": "Telegram chat ID",
        "btn_save": "Сохранить",
        "btn_cancel": "Отмена",
        "set_saved": "Сохранено ✓",
        "set_advanced": "Расширенно (config.json)",
        "feedback": "💬 Отзывы и предложения",
        "fb_title": "💬 Отзывы и предложения",
        "fb_hint": "Напишите отзыв или предложение:",
        "fb_capture": "📷 Снимок экрана",
        "fb_choose": "🖼 Выбрать изображение",
        "fb_attached": "Изображение прикреплено ✓",
        "fb_send": "Отправить",
        "fb_sending": "Отправка...",
        "fb_sent": "Спасибо! Отправлено ✓",
        "fb_error": "Ошибка — нет интернета. Попробуйте позже.",
        "fb_empty": "Пожалуйста, сначала напишите отзыв.",
        "fb_name": "Ваше имя",
        "fb_country": "Ваша страна",
        "set_contact": "Связь с автором",
        "fb_link_hint": "Отправьте отзыв и скриншот через Telegram. Нажмите кнопку — откроется чат.",
        "fb_open": "Написать в Telegram",
    },
    "en": {
        "panel_5h": "5-hour window",
        "panel_weekly": "Weekly (7 days)",
        "btn_stats": "Statistics",
        "btn_settings": "Settings",
        "btn_sound": "Sound",
        "btn_muted": "Muted",
        "btn_close": "Close",
        "btn_update": "Update",
        "btn_later": "Later",
        "btn_ok": "OK",
        "btn_ok_got": "OK — Got it",
        "unit_token": "tokens",
        "tokens_fmt": "{used} / {maxv} tokens",
        "remaining": "Left: {n} tokens",
        "remaining_dash": "Left: --",
        "reset_fmt": "Reset in: {s}",
        "reset_dash": "Reset: --",
        "stats_title": "📊 Token statistics",
        "stats_h_period": "Period",
        "stats_h_token": "Tokens",
        "stats_h_msg": "Messages",
        "row_5h_now": "5-hour (now)",
        "row_today": "Today (24h)",
        "row_weekly": "Weekly (7 days)",
        "row_monthly": "Monthly (30 days)",
        "note_limit": "limit {p}%  ({mx} tokens)",
        "period_5h": "5-hour",
        "period_weekly": "Weekly",
        "tray_show": "Show",
        "tray_check_update": "Check for updates",
        "tray_hide": "Hide",
        "tray_quit": "Exit",
        "tray_language": "Language / Til",
        "update_title": "Update",
        "newver_title": "New version",
        "newver_heading": "🎉 A new version is out!",
        "newver_cur_new": "Current: v{cur}     New: {new}",
        "updating": "Downloading... please wait",
        "update_err": "Error — or not an .exe. Download manually.",
        "up_to_date": "You have the latest version ✓",
        "notify_tray_title": "Claude Token Monitor — {level}",
        "notify_tray_msg": "{source}: {percent}% used! Limit is near.",
        "popup_title": "WARNING — Token Limit!",
        "popup_heading": "TOKEN LIMIT IS NEAR!",
        "popup_used": "{source}: {percent}% used",
        "popup_advice": "Start a new chat or wait for the reset.",
        "tg_reached": "*{source}*: reached `{percent}%`!",
        "tg_limit_near": "Limit is near.",
        "tg_advice": "_Start a new chat or wait for the reset._",
        "span_dh": "{d}d {h}h",
        "settings_title": "⚙️ Settings",
        "set_sec_general": "General",
        "set_sec_limits": "Limits",
        "set_sec_notify": "Notifications",
        "set_language": "Language",
        "set_plan": "Plan (subscription)",
        "set_limit_5h": "5-hour limit (tokens)",
        "set_limit_weekly": "Weekly limit (tokens)",
        "set_sound": "Sound alerts",
        "set_autostart": "Start on PC boot",
        "set_autohide": "Show only when working with Claude",
        "set_telegram_on": "Telegram alerts",
        "set_tg_token": "Telegram bot token",
        "set_tg_chat": "Telegram chat ID",
        "btn_save": "Save",
        "btn_cancel": "Cancel",
        "set_saved": "Saved ✓",
        "set_advanced": "Advanced (config.json)",
        "feedback": "💬 Feedback & suggestions",
        "fb_title": "💬 Feedback & suggestions",
        "fb_hint": "Write your feedback or suggestion:",
        "fb_capture": "📷 Capture screen",
        "fb_choose": "🖼 Choose image",
        "fb_attached": "Image attached ✓",
        "fb_send": "Send",
        "fb_sending": "Sending...",
        "fb_sent": "Thank you! Sent ✓",
        "fb_error": "Error — no internet. Try again later.",
        "fb_empty": "Please write your feedback first.",
        "fb_name": "Your name",
        "fb_country": "Your country",
        "set_contact": "Contact the author",
        "fb_link_hint": "Send your feedback and screenshot via Telegram. Click the button — the chat opens.",
        "fb_open": "Write on Telegram",
    },
}


def detect_os_language(default="en"):
    """Windows interfeys tilidan uz/ru/en ni aniqlaydi (birinchi ishga tushish uchun)."""
    try:
        import ctypes
        primary = ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0x3FF
        # primary language ID: 0x19=rus, 0x09=ingliz, 0x43=o'zbek
        return {0x19: "ru", 0x09: "en", 0x43: "uz"}.get(primary, default)
    except Exception:
        return default


def set_language(lang):
    global _LANG
    if lang in TRANSLATIONS:
        _LANG = lang


def get_language():
    return _LANG


def t(key, **kwargs):
    d = TRANSLATIONS.get(_LANG, TRANSLATIONS["uz"])
    s = d.get(key)
    if s is None:
        s = TRANSLATIONS["uz"].get(key, key)
    if kwargs:
        try:
            s = s.format(**kwargs)
        except Exception:
            pass
    return s
