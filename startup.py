"""Windows'da avtoyuklanishga qo'shish (HKCU Run kaliti).

Har ishga tushganda (faqat .exe rejimida) Run kalitiga o'zini yozadi — shunda
keyingi safar komp yonganda o'zi (ko'rinmas holda) ishga tushadi. Bu har bir
kompyuterda qo'lda sozlash zaruratini yo'q qiladi.
"""
import sys

try:
    import winreg
except Exception:  # Windows bo'lmasa
    winreg = None

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "ClaudeTokenMonitor"


def _exe_path():
    # Faqat frozen (.exe) rejimida ma'noli — dev'da o'tkazib yuboramiz
    if getattr(sys, "frozen", False):
        return sys.executable
    return None


def ensure(enabled=True):
    if winreg is None:
        return
    exe = _exe_path()
    if exe is None:
        return
    try:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0,
                                 winreg.KEY_ALL_ACCESS)
        except FileNotFoundError:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_KEY)
        try:
            if enabled:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe}"')
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
        finally:
            winreg.CloseKey(key)
    except Exception:
        pass
