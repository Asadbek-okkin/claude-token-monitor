# Claude Token Monitor

Ekranda suzib yuruvchi (floating) desktop widget — Claude Code token sarfini
real vaqtda kuzatadi, limit chegaralarida ogohlantiradi.

## Imkoniyatlar

- **Claude Code monitor** — `~/.claude/projects/**/*.jsonl` dan oxirgi 5 soatlik
  (rolling window) token sarfini o'qiydi.
- **Floating widget** — chegara yo'q, shaffof, always-on-top, drag & drop bilan
  istalgan joyga siljitiladi. Pozitsiya avtomatik saqlanadi.
- **Progress bar** — rang foizga qarab: yashil (<60%) → sariq (60–85%) → qizil (>85%).
- **3 darajali ogohlantirish:**
  - 80% — ovoz (beep) + tray xabari
  - 90% — kuchliroq ovoz + tray xabari
  - 95% — ekran markazida popup + (sozlangan bo'lsa) Telegram xabari
  - Har daraja faqat **bir marta**; reset bo'lganda tozalanadi.
- **Telegram bot** — limitga yetganda xabar (ixtiyoriy).
- **System tray** — ko'rsatish / yashirish / chiqish.

## Ishga tushirish (test)

```bash
pip install -r requirements.txt
python main.py
```

Faqat token o'quvchini tekshirish:

```bash
python monitor_code.py
```

## .exe ga aylantirish

```bash
build.bat
```

Natija: `dist\ClaudeTokenMonitor.exe`

## Sozlash — config.json

Widget `Sozlama` tugmasi `config.json` ni ochadi. Muhim maydonlar:

- `claude_code.max_tokens` — sizning 5-soatlik limitingiz (o'zingizga moslang).
- `claude_code.window_hours` — rolling window (odatda 5).
- `refresh_interval` — necha soniyada yangilanadi (default 30).
- `telegram.enabled` + `bot_token` + `chat_id` — Telegram xabarlar uchun.

### Telegram sozlash

1. Telegram'da `@BotFather` → `/newbot` → bot token oling.
2. `@userinfobot` ga yozing → `chat_id` ni oling.
3. `config.json`:
   ```json
   "telegram": { "enabled": true, "bot_token": "123:AAF...", "chat_id": "987654321" }
   ```

## Fayllar

| Fayl | Vazifa |
|------|--------|
| `main.py` | Kirish nuqtasi, yangilash sikli, tray |
| `monitor_code.py` | Claude Code token o'quvchi |
| `monitor_web.py` | Reset countdown hisoblagich |
| `widget.py` | Floating window UI |
| `notifier.py` | Ovoz + tray + popup + Telegram |
| `config.py` | Sozlamalarni o'qish/saqlash |
| `config.json` | Foydalanuvchi sozlamalari |
| `make_icon.py` | icon.ico generator |
| `build.bat` | .exe builder |

## Eslatma

- Claude subscription limiti **bitta akkaunt uchun umumiy** — barcha oynalar va
  modellar (Opus/Sonnet/Haiku) shu bitta hovuzdan yeydi. Model faqat sarf
  tezligini o'zgartiradi (Opus eng ko'p, Haiku eng kam).
- `claude.ai` paneli web usage'ni local o'qiy olmaydi, shuning uchun u umumiy
  Claude Code sarfini reja limitiga (`claude_ai.max_tokens`) nisbatan ko'rsatadi.
- Token soni = `input + output` (spec bo'yicha). Cache tokenlari alohida
  yig'iladi lekin asosiy hisobga kirmaydi.
