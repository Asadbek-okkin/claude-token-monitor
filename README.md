# Claude Token Monitor

**Claude Code (VS Code) token sarfini real vaqtda kuzatuvchi kichik, doim ustda turadigan oyna.** Limitga urilib, ish o'rtasida to'xtab qolmaslik uchun.

> 🇺🇿 O'zbekcha · 🇷🇺 Русский · 🇬🇧 English — interfeys 3 tilda.

---

## ⬇️ Yuklab olish (Windows)

**[ClaudeTokenMonitor.exe — eng oxirgi versiya](https://github.com/Asadbek-okkin/claude-token-monitor/releases/latest/download/ClaudeTokenMonitor.exe)**

O'rnatish shart emas: yuklab oling → ustiga 2 marta bosing. Tamom.
*(Windows SmartScreen chiqsa: **More info → Run anyway**.)*

---

## ✨ Imkoniyatlar

- **5 soatlik** va **haftalik** limit — foiz, progress bar va **reset countdown**.
- **Statistika**: 5 soat / 24 soat / hafta / oy kesimida token va xabarlar soni.
- **Ogohlantirish**: limitning 80 / 90 / 95% ida ovoz + tray + **Telegram** xabari.
- **Aqlli ko'rinish**: faqat siz **VS Code** yoki **Claude AI (brauzer)** da ishlayotganingizda ko'rinadi, boshqa paytda o'zi yashirinadi.
- **Avtoyuklanish**: komp yonganda o'zi (ko'rinmas holda) ishga tushadi.
- **Avtomatik yangilanish**: ilova kabi, yangi versiya chiqsa o'zi yangilanadi.
- **3 til**: O'zbekcha / Ruscha / Inglizcha — bir tugma bilan almashadi.
- **Bepul va ochiq kodli.**

---

## 🚀 Foydalanish

1. Dasturni ishga tushiring — kichik oyna paydo bo'ladi (soat yonidagi tray'da ham ikonka).
2. **Statistika** tugmasi — batafsil sarf jadvali.
3. **Sozlama** tugmasi — barcha moslamalar bitta oynada.
4. Oynani sichqoncha bilan ushlab istalgan joyga surib qo'yish mumkin.

### ⚙️ Sozlamalar (Sozlama tugmasi)

| Bo'lim | Tavsif |
|---|---|
| **Til** | O'zbekcha / Русский / English |
| **Reja** | Pro / Max 5x / Max 20x |
| **Limitlar** | 5 soatlik va haftalik token limiti (o'zingizga moslang) |
| **Ovoz** | Ovozli ogohlantirishni yoqish/o'chirish |
| **Avtoyuklanish** | Komp yonganda ishga tushsinmi |
| **Ko'rinish** | Faqat Claude bilan ishlaganda ko'rinsinmi |
| **Telegram** | Ogohlantirishni Telegramga yuborish (bot token + chat ID) |

> **Limitlar taxminiy** — Anthropic aniq raqamlarni e'lon qilmaydi. 5 soatlik limitga urilgan paytdagi songa qarab moslang.

---

## 💬 Fikr va takliflar

Dastur haqidagi fikringiz yoki muammoni bevosita dasturchiga yuborishingiz mumkin:

**Sozlama → 💬 Fikr va takliflar** *(yoki tray menyusidan)* → **Telegram'da yozish**

Telegram suhbati ochiladi ([@Asadbek00_03_24](https://t.me/Asadbek00_03_24)) — fikringizni yozing va xohlasangiz **skrinshot** biriktiring (muammoni tushuntirish oson bo'lishi uchun).

> Ilovada hech qanday maxfiy kalit saqlanmaydi — fikr to'g'ridan-to'g'ri Telegram orqali boradi.

Har qanday taklif, xatolik yoki g'oyani kuting — dastur shu asosda yaxshilanadi. 🙏

---

## 🔄 Avtomatik yangilanish

Dastur vaqti-vaqti bilan yangi versiyani tekshiradi. Chiqqan bo'lsa "Yangilash?" oynasi ko'rsatiladi (yoki jimgina yangilaydi). Ya'ni bir marta o'rnatsangiz, keyin doim eng so'nggi versiyada bo'lasiz.

---

## 🛠 Dasturchilar uchun (manba kodidan yig'ish)

```bash
git clone https://github.com/Asadbek-okkin/claude-token-monitor
cd claude-token-monitor
pip install -r requirements.txt
python main.py            # ishga tushirish
build.bat                 # .exe yig'ish (PyInstaller)
```

Asosiy fayllar: `main.py` (kirish + tray + yangilanish), `widget.py` (UI + sozlama/fikr oynalari), `monitor_code.py` (loglarni o'qish), `notifier.py` (ogohlantirish), `i18n.py` (tarjimalar), `visibility.py` (aqlli ko'rinish), `feedback.py` (fikr yuborish).

> Fikr-mulohaza bot kaliti `secrets_local.py` da saqlanadi va **repoga qo'shilmaydi** (gitignore).

---

## 📄 Litsenziya

Bepul, ochiq kodli. Erkin foydalaning va ulashing.
