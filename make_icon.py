"""icon.ico yaratadi (PyInstaller --icon uchun).

Dizayn: to'q navi fonli yumaloq kvadrat + orange "gauge" halqasi (~72%)
+ markazda yashil aksent nuqta. build.bat / build jarayoni chaqiradi.
"""
from PIL import Image, ImageDraw


def make():
    S = 256
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Yumaloq kvadrat fon
    d.rounded_rectangle((6, 6, S - 6, S - 6), radius=54, fill=(26, 29, 39, 255))

    # Gauge halqasi
    cx, cy, r = S // 2, S // 2, 80
    box = (cx - r, cy - r, cx + r, cy + r)
    d.arc(box, start=0, end=360, fill=(45, 50, 66, 255), width=24)          # to'q "track"
    d.arc(box, start=-90, end=-90 + 260, fill=(240, 165, 0, 255), width=24)  # orange progress ~72%

    # Markaz aksent (yashil = "sog'lom")
    d.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=(62, 207, 142, 255))
    d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=(26, 29, 39, 255))

    img.save("icon.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48),
                                (64, 64), (128, 128), (256, 256)])
    # PNG preview ham (ixtiyoriy)
    img.save("icon.png")
    print("icon.ico yaratildi (gauge dizayn)")


if __name__ == "__main__":
    make()
