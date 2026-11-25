"""Front page for make.fun news-image-20261124 (Tuesday 24 November 2026).

Draws the page with Pillow at twice the final size, shrinks it, and writes
entry.png (1024 x 1024, RGB PNG) at the repository root. The judge sees only
that file. Every item's sources and dates are listed in README.md.

Run from anywhere:  python tools/make_image.py
Needs Pillow and the Windows fonts in C:/Windows/Fonts.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "entry.png")
SS = 2                                   # draw at 2x, shrink to 1x at the end
W, H = 1024, 1024
FONT_DIR = "C:/Windows/Fonts"
FONT_FILES = {"serif_b": "georgiab.ttf", "sans_b": "arialbd.ttf", "sans": "arial.ttf"}

PAPER = (245, 240, 230)
PANEL = (255, 253, 247)
INK = (24, 24, 22)
MUTED = (92, 88, 80)
RED = (190, 28, 44)
WHITE = (255, 255, 255)
GOLD = (206, 164, 48)
GOLD_DARK = (120, 90, 22)
SEA = (222, 233, 237)
LAND = (218, 209, 189)
GRID = (204, 216, 221)

_fonts = {}


def font(kind, size):
    key = (kind, size)
    if key not in _fonts:
        path = os.path.join(FONT_DIR, FONT_FILES[kind])
        _fonts[key] = ImageFont.truetype(path, round(size * SS))
    return _fonts[key]


def fit_font(kind, s, max_w, start, floor):
    size = start
    while size > floor and font(kind, size).getlength(s) / SS > max_w:
        size -= 1
    return font(kind, size)


def sc(seq):
    return [(x * SS, y * SS) for x, y in seq]


def bx(x0, y0, x1, y1):
    return [x0 * SS, y0 * SS, x1 * SS, y1 * SS]


def rect(d, x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle(bx(x0, y0, x1, y1), fill=fill, outline=outline,
                width=round(width * SS) if outline else 0)


def ell(d, x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.ellipse(bx(x0, y0, x1, y1), fill=fill, outline=outline,
              width=round(width * SS) if outline else 0)


def poly(d, seq, fill=None):
    d.polygon(sc(seq), fill=fill)


def line(d, seq, fill, width=1):
    d.line(sc(seq), fill=fill, width=round(width * SS), joint="curve")


def arc(d, x0, y0, x1, y1, start, end, fill, width=1):
    d.arc(bx(x0, y0, x1, y1), start, end, fill=fill, width=round(width * SS))


def text(d, x, y, s, f, fill=INK, anchor="la"):
    d.text((x * SS, y * SS), s, font=f, fill=fill, anchor=anchor)


def star(cx, cy, r_out, r_in, n=24):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- scenes
# Each scene is drawn on a 226 x 92 canvas whose top-left corner is (x, y).
# paste_scene() shrinks it into the panel.

def scene_ukraine(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(202, 212, 220))
    rect(d, x + 84, y + 16, x + 156, y + 92, fill=(122, 110, 96))
    for r in range(4):
        for c in range(3):
            dark = (r, c) in ((0, 1), (2, 2), (3, 0))
            wx, wy = x + 92 + c * 20, y + 24 + r * 16
            rect(d, wx, wy, wx + 13, wy + 9, fill=(34, 34, 34) if dark else (238, 232, 216))
    for cx, cy, rr in ((170, 22, 10), (182, 15, 9), (194, 21, 11), (205, 28, 8)):
        ell(d, x + cx - rr, y + cy - rr, x + cx + rr, y + cy + rr, fill=(150, 146, 140))
    poly(d, [(x + 206, y + 58), (x + 220, y + 63), (x + 206, y + 68), (x + 202, y + 63)], fill=INK)
    line(d, [(x + 186, y + 66), (x + 202, y + 63)], fill=INK, width=3)
    text(d, x + 10, y + 10, "2 killed", font("sans_b", 20))


def scene_bangladesh(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(218, 232, 220))
    rect(d, x + 10, y + 10, x + 56, y + 42, fill=(0, 106, 78))
    ell(d, x + 23, y + 18, x + 41, y + 36, fill=(244, 42, 65))
    p0, p1, p2 = (x + 18, y + 84), (x + 100, y + 6), (x + 146, y + 36)
    for i in range(0, 31):
        t = i / 30
        px = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        py = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        if i % 2 == 0:
            ell(d, px - 2, py - 2, px + 2, py + 2, fill=INK)
    poly(d, [(x + 140, y + 40), (x + 156, y + 30), (x + 160, y + 34), (x + 146, y + 44)], fill=INK)
    rect(d, x + 150, y + 54, x + 216, y + 90, fill=WHITE, outline=INK, width=2)
    rect(d, x + 150, y + 54, x + 216, y + 66, fill=RED)
    text(d, x + 183, y + 60, "DEC", font("sans_b", 12), fill=WHITE, anchor="mm")
    text(d, x + 183, y + 79, "16", font("serif_b", 26), fill=INK, anchor="mm")


def scene_gaza(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(228, 220, 202))
    rect(d, x + 36, y + 42, x + 118, y + 92, fill=(140, 132, 120))
    poly(d, [(x + 36, y + 42), (x + 54, y + 34), (x + 66, y + 42)], fill=(140, 132, 120))
    for c in range(3):
        for r in range(2):
            rect(d, x + 46 + c * 22, y + 54 + r * 18, x + 58 + c * 22, y + 66 + r * 18, fill=(58, 54, 50))
    poly(d, star(x + 172, y + 44, 32, 14), fill=RED)
    text(d, x + 10, y + 10, "Gaza City", font("sans_b", 20))


def scene_turkey(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(206, 216, 222))
    ell(d, x + 66, y + 44, x + 124, y + 70, fill=(72, 86, 68))
    poly(d, [(x + 118, y + 52), (x + 160, y + 40), (x + 164, y + 46), (x + 122, y + 60)], fill=(72, 86, 68))
    line(d, [(x + 40, y + 38), (x + 150, y + 38)], fill=INK, width=3)
    line(d, [(x + 70, y + 74), (x + 124, y + 74)], fill=INK, width=2)
    line(d, [(x + 104, y + 72), (x + 118, y + 80), (x + 130, y + 84), (x + 144, y + 90)], fill=(96, 96, 96), width=4)
    poly(d, star(x + 150, y + 86, 12, 6, 12), fill=(232, 110, 30))
    text(d, x + 10, y + 10, "5 crew dead", font("sans_b", 20))


def scene_afcon(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(238, 234, 216))
    arc(d, x + 72, y + 20, x + 106, y + 50, 90, 270, GOLD_DARK, 4)
    arc(d, x + 120, y + 20, x + 154, y + 50, 270, 90, GOLD_DARK, 4)
    ell(d, x + 88, y + 12, x + 138, y + 52, fill=GOLD)
    rect(d, x + 106, y + 46, x + 120, y + 74, fill=GOLD)
    rect(d, x + 92, y + 72, x + 134, y + 82, fill=GOLD_DARK)
    rect(d, x + 84, y + 82, x + 142, y + 92, fill=GOLD_DARK)


def scene_colombia(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(222, 236, 226))
    rect(d, x + 20, y + 40, x + 150, y + 92, fill=(236, 232, 222), outline=INK, width=1)
    for i in range(7):
        rect(d, x + 20 + i * 19, y + 30, x + 39 + i * 19, y + 42, fill=RED if i % 2 == 0 else WHITE)
    rect(d, x + 80, y + 62, x + 96, y + 92, fill=(120, 90, 70))
    for hx in (x + 40, x + 60, x + 126):
        ell(d, hx - 4, y + 50, hx + 4, y + 58, fill=INK)
        line(d, [(hx, y + 58), (hx, y + 72)], fill=INK, width=2)
        line(d, [(hx - 7, y + 64), (hx + 7, y + 64)], fill=INK, width=2)
    rect(d, x + 156, y + 56, x + 214, y + 84, fill=(80, 86, 92))
    rect(d, x + 162, y + 61, x + 204, y + 71, fill=(170, 200, 210))
    ell(d, x + 164, y + 78, x + 176, y + 90, fill=INK)
    ell(d, x + 194, y + 78, x + 206, y + 90, fill=INK)
    text(d, x + 10, y + 6, "Hostages", font("sans_b", 20))


def scene_japan(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(238, 236, 230))
    rect(d, x + 10, y + 10, x + 44, y + 34, fill=WHITE, outline=INK, width=1)
    ell(d, x + 21, y + 15, x + 33, y + 29, fill=RED)
    rect(d, x + 108, y + 26, x + 114, y + 84, fill=INK)
    rect(d, x + 88, y + 84, x + 134, y + 92, fill=INK)
    line(d, [(x + 52, y + 30), (x + 170, y + 30)], fill=INK, width=4)
    line(d, [(x + 52, y + 30), (x + 36, y + 62)], fill=INK, width=2)
    line(d, [(x + 52, y + 30), (x + 68, y + 62)], fill=INK, width=2)
    poly(d, [(x + 30, y + 62), (x + 74, y + 62), (x + 66, y + 70), (x + 38, y + 70)], fill=GOLD)
    line(d, [(x + 170, y + 30), (x + 154, y + 58)], fill=INK, width=2)
    line(d, [(x + 170, y + 30), (x + 186, y + 58)], fill=INK, width=2)
    poly(d, [(x + 148, y + 58), (x + 192, y + 58), (x + 184, y + 66), (x + 156, y + 66)], fill=GOLD)
    text(d, x + 216, y + 6, "ICC", font("sans_b", 20), anchor="ra")


def scene_korea(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(218, 228, 238))
    cx, cy = x + 52, y + 84
    for rr in (20, 36, 52):
        arc(d, cx - rr, cy - rr, cx + rr, cy + rr, 200, 340, (60, 90, 120), 2)
    poly(d, [(x + 124, y + 44), (x + 172, y + 32), (x + 166, y + 42), (x + 132, y + 52)], fill=INK)
    poly(d, [(x + 140, y + 42), (x + 130, y + 60), (x + 152, y + 44)], fill=INK)
    for i in range(1, 8):
        t = i / 8
        px = cx + (x + 124 - cx) * t
        py = cy + (y + 44 - cy) * t
        ell(d, px - 2, py - 2, px + 2, py + 2, fill=(60, 90, 120))
    poly(d, [(x + 176, y + 88), (x + 198, y + 52), (x + 220, y + 88)], fill=(246, 196, 40))
    text(d, x + 198, y + 76, "!", font("sans_b", 26), anchor="mm")
    text(d, x + 10, y + 6, "Russian jets", font("sans_b", 18))


def scene_vietnam(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(242, 230, 218))
    for fx, fh in ((80, 26), (98, 34), (116, 26), (134, 18)):
        poly(d, [(x + fx - 9, y + 62), (x + fx, y + 62 - fh), (x + fx + 9, y + 62)], fill=(240, 120, 30))
    poly(d, [(x + 70, y + 64), (x + 150, y + 64), (x + 142, y + 90), (x + 78, y + 90)], fill=(88, 88, 96))
    rect(d, x + 62, y + 58, x + 158, y + 66, fill=(128, 128, 136))
    poly(d, star(x + 192, y + 30, 22, 10, 16), fill=(240, 150, 40))
    text(d, x + 10, y + 6, "6 dead", font("sans_b", 20))


def scene_england(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(236, 236, 226))
    rect(d, x + 104, y + 8, x + 122, y + 70, fill=WHITE, outline=INK, width=2)
    ell(d, x + 96, y + 62, x + 130, y + 96, fill=RED, outline=INK, width=2)
    rect(d, x + 110, y + 22, x + 116, y + 76, fill=RED)
    cx, cy = x + 186, y + 26
    ell(d, cx - 12, cy - 12, cx + 12, cy + 12, fill=(246, 196, 40))
    for i in range(8):
        a = 2 * math.pi * i / 8
        line(d, [(cx + 16 * math.cos(a), cy + 16 * math.sin(a)),
                 (cx + 24 * math.cos(a), cy + 24 * math.sin(a))], fill=(246, 196, 40), width=3)
    text(d, x + 10, y + 64, "5,258", font("sans_b", 26))


def scene_germany(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(230, 230, 236))
    ell(d, x + 72, y + 14, x + 152, y + 74, fill=(190, 190, 198), outline=INK, width=1)
    rect(d, x + 52, y + 70, x + 172, y + 82, fill=(150, 150, 158))
    for cx2 in (70, 96, 122, 148):
        rect(d, x + cx2 - 3, y + 72, x + cx2 + 3, y + 82, fill=(120, 120, 128))
    rect(d, x + 118, y + 54, x + 220, y + 72, fill=RED)
    text(d, x + 169, y + 63, "EXPELLED", font("sans_b", 14), fill=WHITE, anchor="mm")
    text(d, x + 10, y + 6, "Berlin", font("sans_b", 20))


def scene_libya(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(200, 222, 232))
    poly(d, [(x + 40, y + 60), (x + 190, y + 60), (x + 176, y + 76), (x + 54, y + 76)], fill=(70, 74, 80))
    rect(d, x + 92, y + 40, x + 142, y + 60, fill=(110, 116, 122))
    rect(d, x + 104, y + 30, x + 116, y + 40, fill=(110, 116, 122))
    line(d, [(x + 116, y + 30), (x + 116, y + 18)], fill=(70, 74, 80), width=2)
    poly(d, star(x + 52, y + 48, 22, 9, 14), fill=(240, 120, 30))
    for i in range(6):
        arc(d, x + 14 + i * 32, y + 78, x + 34 + i * 32, y + 96, 0, 180, (120, 160, 180), 2)
    text(d, x + 10, y + 6, "Benghazi", font("sans_b", 20))


def scene_australia(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(222, 232, 236))
    poly(d, [(x + 96, y + 16), (x + 162, y + 16), (x + 162, y + 54), (x + 129, y + 86), (x + 96, y + 54)],
         fill=(30, 80, 150))
    poly(d, [(x + 104, y + 24), (x + 154, y + 24), (x + 154, y + 52), (x + 129, y + 77), (x + 104, y + 52)],
         fill=(236, 240, 244))
    text(d, x + 129, y + 48, "5%", font("serif_b", 26), fill=(30, 80, 150), anchor="mm")
    text(d, x + 10, y + 6, "Tech law", font("sans_b", 20))


def scene_riyadh(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(228, 226, 216))
    rect(d, x + 70, y + 24, x + 104, y + 92, fill=(96, 110, 124))
    rect(d, x + 112, y + 38, x + 142, y + 92, fill=(120, 134, 146))
    for r in range(6):
        for c in range(3):
            rect(d, x + 76 + c * 9, y + 32 + r * 10, x + 81 + c * 9, y + 37 + r * 10, fill=(230, 236, 240))
    poly(d, star(x + 96, y + 22, 18, 8, 14), fill=(240, 120, 30))
    text(d, x + 10, y + 6, "Riyadh", font("sans_b", 20))


def scene_yemen(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(230, 214, 178))
    ell(d, x - 30, y + 62, x + 120, y + 120, fill=(214, 194, 154))
    for bx0, bh in ((120, 18), (134, 26), (150, 14), (166, 22), (184, 16)):
        rect(d, x + bx0, y + 60 - bh, x + bx0 + 12, y + 60, fill=(150, 130, 110))
    line(d, [(x + 12, y + 74), (x + 40, y + 66), (x + 62, y + 78), (x + 90, y + 68), (x + 118, y + 80),
             (x + 150, y + 70), (x + 180, y + 82), (x + 214, y + 72)], fill=(70, 52, 34), width=4)
    text(d, x + 10, y + 6, "Aden", font("sans_b", 20))


def scene_hormuz(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(200, 222, 232))
    poly(d, [(x + 40, y + 64), (x + 186, y + 64), (x + 176, y + 80), (x + 52, y + 80)], fill=(60, 66, 72))
    rect(d, x + 70, y + 54, x + 134, y + 64, fill=(180, 60, 40))
    rect(d, x + 140, y + 46, x + 176, y + 64, fill=(220, 220, 220))
    for fx, fh in ((80, 20), (96, 28), (112, 18)):
        poly(d, [(x + fx - 7, y + 54), (x + fx, y + 54 - fh), (x + fx + 7, y + 54)], fill=(240, 120, 30))
    for mx0, my0 in ((70, 86), (120, 88), (162, 84)):
        ell(d, x + mx0 - 4, y + my0 - 4, x + mx0 + 4, y + my0 + 4, fill=INK)
    text(d, x + 10, y + 6, "Hormuz", font("sans_b", 20))


def scene_khan_younis(d, x, y):
    rect(d, x, y, x + 226, y + 92, fill=(228, 220, 202))
    rect(d, x + 40, y + 60, x + 84, y + 92, fill=(140, 132, 120))
    rect(d, x + 88, y + 70, x + 124, y + 92, fill=(120, 112, 102))
    poly(d, [(x + 124, y + 70), (x + 140, y + 60), (x + 150, y + 92), (x + 124, y + 92)], fill=(130, 122, 112))
    for px in (x + 164, x + 180, x + 196):
        ell(d, px - 4, y + 56, px + 4, y + 64, fill=INK)
        line(d, [(px, y + 64), (px, y + 80)], fill=INK, width=2)
        line(d, [(px - 6, y + 70), (px + 6, y + 70)], fill=INK, width=2)
    text(d, x + 10, y + 6, "Khan Younis", font("sans_b", 20))


def paste_scene(img, scene, x, y, w=178, h=70):
    canvas = Image.new("RGB", (226 * SS, 92 * SS), WHITE)
    scene(ImageDraw.Draw(canvas), 0, 0)
    small = canvas.resize((w * SS, h * SS), Image.Resampling.LANCZOS)
    img.paste(small, (x * SS, y * SS))


# ---------------------------------------------------------------- map
MAP_X, MAP_Y, MAP_W, MAP_H = 24, 170, 976, 214
LON0, LON1, LAT_TOP = -85.0, 150.0, 58.0
K = MAP_W / (LON1 - LON0)                # px per degree, same on both axes


def mx(lon):
    return MAP_X + (lon - LON0) * K


def my(lat):
    return MAP_Y + (LAT_TOP - lat) * K


# Coarse outlines (lon, lat). Approximate: they only place the pins.
EURASIA = [
    (-9.5, 43.5), (-9.0, 37.2), (-6.0, 36.1), (-2.0, 36.8), (0.5, 38.7), (3.2, 41.9), (3.2, 43.3),
    (6.5, 43.1), (8.9, 44.2), (10.5, 43.9), (12.4, 41.6), (16.1, 38.2), (18.5, 40.2), (19.5, 41.8),
    (19.2, 39.9), (21.1, 38.4), (23.1, 36.5), (22.6, 40.3), (26.1, 40.8), (26.5, 39.5), (27.5, 37.5),
    (30.5, 36.3), (33.0, 36.2), (36.0, 36.5), (35.8, 35.0), (35.5, 33.0), (35.0, 32.4), (34.5, 31.4),
    (34.5, 28.0), (36.5, 25.0), (39.0, 21.5), (42.5, 16.5), (43.0, 13.5), (45.0, 12.7), (48.0, 14.5),
    (52.0, 16.0), (55.0, 17.0), (57.5, 19.0), (58.0, 22.0), (56.5, 24.5), (52.0, 24.8), (50.5, 25.8),
    (48.8, 29.9), (50.5, 29.3), (54.0, 26.7), (56.4, 27.1), (57.5, 25.5), (61.5, 25.2), (66.5, 25.4),
    (68.0, 23.7), (70.0, 22.0), (72.5, 21.0), (72.8, 19.0), (73.3, 16.5), (75.0, 12.5), (77.5, 8.0),
    (78.2, 9.0), (79.9, 10.3), (80.3, 13.5), (82.3, 17.0), (84.8, 19.8), (86.8, 21.0), (89.0, 21.8),
    (91.8, 22.2), (92.4, 20.5), (94.3, 16.5), (97.6, 16.8), (98.5, 15.5), (98.3, 12.0), (98.6, 9.5),
    (100.3, 6.5), (101.2, 2.6), (103.5, 1.3), (104.2, 1.5), (103.4, 4.0), (102.2, 6.2), (100.5, 10.0),
    (100.8, 12.7), (102.4, 12.3), (104.8, 10.5), (106.5, 9.2), (105.0, 8.6), (106.7, 10.4),
    (108.7, 11.6), (109.3, 13.3), (108.9, 15.5), (107.7, 17.2), (106.5, 18.7), (105.8, 19.8),
    (108.1, 21.5), (110.6, 21.2), (113.6, 22.4), (117.0, 23.5), (119.5, 25.5), (121.5, 28.5),
    (122.2, 30.7), (121.2, 31.8), (122.2, 34.5), (119.8, 35.4), (120.7, 37.5), (122.6, 37.1),
    (121.7, 39.5), (124.2, 40.1), (125.5, 39.8), (128.5, 42.0), (130.7, 42.9), (133.0, 42.8),
    (135.5, 43.7), (138.5, 46.5), (140.5, 48.5), (140.3, 52.0), (137.0, 54.5), (140.0, 57.3),
    (140.0, 58.0), (-10.0, 58.0),
]
AFRICA = [
    (-17.0, 21.0), (-16.5, 27.5), (-13.0, 27.7), (-9.8, 30.3), (-9.5, 33.5), (-6.0, 35.8), (-2.0, 35.2),
    (0.0, 36.0), (3.0, 36.8), (10.0, 37.3), (11.0, 33.8), (15.0, 32.3), (20.0, 30.9), (20.0, 32.5),
    (23.0, 32.5), (25.0, 31.6), (29.0, 30.9), (32.3, 31.3), (34.2, 31.3), (34.2, 29.5), (32.5, 30.0),
    (33.0, 27.5), (36.5, 22.0), (38.8, 18.0), (43.0, 12.5), (51.2, 11.8), (48.5, 9.8), (44.5, 10.4),
    (41.0, 4.9), (39.5, -5.0), (30.0, -5.0), (12.0, -5.0), (9.0, -1.0), (9.5, 3.5), (6.0, 4.3),
    (2.0, 6.2), (-2.0, 4.9), (-7.0, 4.5), (-8.5, 4.4), (-11.0, 6.9), (-13.5, 9.5), (-16.5, 12.3),
    (-17.5, 14.7),
]
AMERICAS_N = [
    (-85.0, 29.0), (-81.5, 25.0), (-80.0, 25.3), (-80.2, 27.0), (-80.5, 32.0), (-76.0, 35.0),
    (-74.0, 40.0), (-70.0, 41.7), (-67.0, 44.8), (-64.0, 45.5), (-60.0, 46.2), (-60.5, 47.8),
    (-64.0, 49.0), (-66.0, 50.0), (-72.0, 50.0), (-78.0, 56.0), (-85.0, 58.0),
]
MEXICO_CENTRAL = [
    (-117.0, 32.5), (-111.0, 31.3), (-106.5, 31.8), (-101.0, 29.8), (-97.5, 26.0), (-97.5, 22.0),
    (-96.0, 19.0), (-94.5, 18.2), (-91.0, 18.6), (-90.5, 21.0), (-87.0, 21.5), (-88.5, 16.0),
    (-84.0, 15.9), (-83.3, 11.0), (-81.5, 9.0), (-79.5, 9.6), (-77.5, 8.7), (-77.3, 7.5),
    (-80.5, 7.8), (-83.0, 8.5), (-85.7, 10.8), (-87.5, 13.0), (-91.5, 13.8), (-95.0, 15.7),
    (-98.0, 16.2), (-101.0, 17.3), (-105.0, 20.5), (-106.5, 23.2), (-109.5, 25.0), (-112.5, 28.5),
    (-114.5, 31.0), (-115.5, 30.0), (-112.0, 27.5), (-110.0, 23.2), (-112.5, 24.5), (-114.7, 28.0),
]
SOUTH_AMERICA_N = [
    (-77.3, 7.5), (-77.5, 4.0), (-79.0, 1.0), (-80.0, -1.0), (-81.0, -5.0), (-76.0, -14.0),
    (-70.0, -18.0), (-71.0, -25.0), (-72.0, -33.0), (-72.0, -42.0), (-74.0, -50.0), (-72.0, -54.0),
    (-68.0, -50.0), (-65.0, -41.0), (-58.0, -34.0), (-53.0, -34.0), (-48.0, -26.0), (-41.0, -22.0),
    (-39.0, -14.0), (-35.0, -9.0), (-35.0, -6.0), (-44.0, -2.0), (-50.0, 1.0), (-52.0, 5.0),
    (-60.0, 8.0), (-62.0, 10.5), (-68.0, 10.5), (-71.0, 11.5), (-72.0, 12.0), (-75.0, 11.2),
    (-77.3, 9.0),
]
ISLANDS = [
    [(-5.5, 50.0), (1.5, 51.0), (1.7, 52.8), (-0.5, 53.5), (-1.7, 55.5), (-2.0, 57.5), (-5.0, 58.0),
     (-6.0, 56.5), (-5.0, 55.0), (-3.0, 54.5), (-3.0, 53.0), (-4.6, 52.2), (-5.2, 51.7), (-3.0, 51.4)],
    [(-10.0, 51.6), (-6.0, 52.1), (-6.0, 54.5), (-8.0, 55.3), (-10.0, 54.2)],
    [(130.9, 33.9), (135.0, 33.5), (140.0, 35.0), (141.5, 38.0), (142.0, 39.5), (141.5, 41.5),
     (140.0, 40.5), (139.5, 38.0), (137.0, 37.0), (135.0, 35.6), (131.5, 34.5)],
    [(140.0, 41.5), (143.5, 42.0), (145.5, 43.3), (142.0, 45.5), (140.0, 43.5)],
    [(129.5, 33.2), (131.5, 31.5), (131.5, 33.5), (130.0, 34.0)],
    [(124.5, 38.5), (128.5, 38.5), (129.5, 36.5), (129.5, 35.0), (127.5, 34.5), (126.2, 34.5),
     (126.5, 36.5), (125.0, 37.5)],
    [(120.1, 23.0), (121.5, 25.3), (121.9, 25.0), (121.0, 22.0)],
    [(120.0, 18.5), (122.5, 18.5), (122.3, 16.0), (124.0, 13.0), (122.0, 13.5), (120.0, 15.5)],
    [(79.8, 9.8), (81.9, 7.5), (80.3, 6.0)],
    [(95.0, 5.5), (98.0, 4.0), (104.0, -2.0), (106.0, -6.0), (102.0, -4.0), (96.0, 2.0)],
    [(109.0, 1.5), (113.0, 4.0), (117.0, 7.0), (119.0, 5.0), (118.0, 1.0), (116.0, -3.0), (110.0, -3.0)],
]
SEA_PATCHES = [
    [(28.0, 41.5), (28.0, 43.5), (30.0, 46.0), (33.0, 45.5), (36.0, 45.0), (38.0, 44.5), (41.5, 41.5),
     (41.0, 41.0), (36.0, 41.5), (31.0, 41.2), (28.5, 41.2)],
    [(47.0, 45.0), (50.0, 47.0), (53.0, 46.5), (54.0, 41.0), (53.0, 37.0), (50.0, 37.0), (49.0, 40.0),
     (48.0, 42.0)],
]


def draw_map(img):
    layer = Image.new("RGB", (MAP_W * SS, MAP_H * SS), SEA)
    dm = ImageDraw.Draw(layer)

    def local(seq):
        return [((mx(lo) - MAP_X) * SS, (my(la) - MAP_Y) * SS) for lo, la in seq]

    for lon in range(-60, 151, 30):
        xx = (mx(lon) - MAP_X) * SS
        dm.line([(xx, 0), (xx, MAP_H * SS)], fill=GRID, width=SS)
    for lat in range(10, 59, 10):
        yy = (my(lat) - MAP_Y) * SS
        dm.line([(0, yy), (MAP_W * SS, yy)], fill=GRID, width=SS)
    for shape in (EURASIA, AFRICA, AMERICAS_N, MEXICO_CENTRAL, SOUTH_AMERICA_N, *ISLANDS):
        dm.polygon(local(shape), fill=LAND)
    for shape in SEA_PATCHES:
        dm.polygon(local(shape), fill=SEA)
    img.paste(layer, (MAP_X * SS, MAP_Y * SS))


def pin(d, n, lon, lat, dx=0, dy=0, note=None):
    """Numbered pin. Off-map points are pinned to the map edge with a note."""
    x0 = min(max(mx(lon), MAP_X + 26), MAP_X + MAP_W - 26)
    y0 = min(max(my(lat), MAP_Y + 24), MAP_Y + MAP_H - 24)
    cx, cy = x0 + dx, y0 + dy
    if dx or dy:
        line(d, [(x0, y0), (cx, cy)], fill=RED, width=2)
    ell(d, cx - 12, cy - 12, cx + 12, cy + 12, fill=RED, outline=WHITE, width=2)
    text(d, cx, cy, str(n), font("sans_b", 16), fill=WHITE, anchor="mm")
    if note:
        text(d, cx - 18, cy, note, font("sans_b", 15), fill=INK, anchor="rm")


# ---------------------------------------------------------------- stories
# (number, keyword, scene, two detail lines, pin longitude, pin latitude)
STORIES = [
    (1, "UKRAINE", scene_ukraine, ("Zaporizhzhia flats hit:", "2 killed, dozens hurt"), 35.1, 47.8),
    (2, "BANGLADESH", scene_bangladesh, ("Ex-PM Hasina plans to", "return on 16 Dec"), 90.4, 23.8),
    (3, "GAZA", scene_gaza, ("Hamas security chief", "Naeem Abu Nahel killed"), 34.5, 31.5),
    (4, "TURKEY", scene_turkey, ("Military helicopter", "crash: 5 crew killed"), 30.5, 39.8),
    (5, "AFRICA CUP", scene_afcon, ("CAS restores Senegal's", "AFCON 2025 title"), -17.4, 14.7),
    (6, "COLOMBIA", scene_colombia, ("Hostages held in a", "Cartagena supermarket"), -75.5, 10.4),
    (7, "JAPAN", scene_japan, ("Pays 2027 ICC dues", "early amid US sanctions"), 139.7, 35.7),
    (8, "SOUTH KOREA", scene_korea, ("Russian aircraft enter", "air-defence zone; alert"), 130.9, 37.5),
    (9, "VIETNAM", scene_vietnam, ("Hanoi restaurant blast:", "at least 6 dead"), 105.8, 21.0),
    (10, "ENGLAND", scene_england, ("Record 5,258 heat", "deaths this summer"), -0.1, 51.5),
    (11, "GERMANY", scene_germany, ("Berlin MP accused of", "antisemitism; expelled"), 13.4, 52.5),
    (12, "LIBYA", scene_libya, ("Kyiv: Libya ship attack", "was self-defence"), 20.1, 32.1),
    (13, "AUSTRALIA", scene_australia, ("Parliament set to pass", "tech fines up to 5%"), 149.1, -35.3),
    (14, "RIYADH", scene_riyadh, ("Houthi strike, 11 hurt,", "Riyadh's tallest tower"), 46.7, 24.7),
    (15, "YEMEN", scene_yemen, ("Houthis advance toward", "Aden; forces dig in"), 45.0, 12.8),
    (16, "HORMUZ", scene_hormuz, ("Iran says three tankers", "hit mines, caught fire"), 56.3, 26.5),
    (17, "KHAN YOUNIS", scene_khan_younis, ("Israeli strikes in Khan", "Younis kill at least 8"), 34.3, 31.35),
]
COL_X = [24, 220, 416, 612, 808]
ROW_Y = [392, 546, 700, 854]
PW, PH = 188, 146


def panel(d, img, n, key, scene, lines, x, y):
    rect(d, x, y, x + PW, y + PH, fill=PANEL, outline=INK, width=2)
    paste_scene(img, scene, x + 5, y + 5)
    ell(d, x + 5, y + 77, x + 27, y + 99, fill=RED, outline=WHITE, width=1)
    text(d, x + 16, y + 88, str(n), font("sans_b", 14), fill=WHITE, anchor="mm")
    text(d, x + 33, y + 80, key, font("sans_b", 19))
    for i, s in enumerate(lines):
        text(d, x + 7, y + 105 + i * 17, s, font("sans", 15))


def main():
    img = Image.new("RGB", (W * SS, H * SS), PAPER)
    d = ImageDraw.Draw(img)
    count = len(STORIES)

    # masthead
    rect(d, 24, 22, 1000, 25, fill=INK)
    text(d, 24, 34, "THE WORLD IN ONE DAY", font("sans_b", 22), fill=RED)
    text(d, 1000, 34, "24.11.2026", font("sans_b", 22), fill=INK, anchor="ra")
    date_line = "Tuesday 24 November 2026"
    text(d, 24, 50, date_line, fit_font("serif_b", date_line, 976, 76, 40))
    sub = f"{count} stories, each reported on 24 November 2026 by two of AP, Reuters, AFP, BBC, Al Jazeera"
    text(d, 24, 136, sub, fit_font("sans", sub, 976, 20, 14))
    rect(d, 24, 164, 1000, 167, fill=INK)

    # map with numbered pins
    draw_map(img)
    rect(d, MAP_X + 6, MAP_Y + 6, MAP_X + 226, MAP_Y + 30, fill=PANEL)
    text(d, MAP_X + 14, MAP_Y + 9, "WHERE IT HAPPENED", font("sans_b", 18))
    for n, _key, _scene, _lines, lon, lat in STORIES:
        if n == 3:
            pin(d, n, lon, lat)
        elif n == 17:
            pin(d, n, lon, lat, dx=30, dy=22)
        elif n == 13:
            pin(d, n, lon, lat, note="Australia (off map)")
        else:
            pin(d, n, lon, lat)

    # story panels: 5 per row; the last row has two panels and a key
    for i, (n, key, scene, lines, _lon, _lat) in enumerate(STORIES):
        panel(d, img, n, key, scene, lines, COL_X[i % 5], ROW_Y[i // 5])
    kx = COL_X[2]
    rect(d, kx, ROW_Y[3], COL_X[4] + PW, ROW_Y[3] + PH, fill=PANEL, outline=INK, width=2)
    text(d, kx + 14, ROW_Y[3] + 12, "How to read", font("sans_b", 22))
    for i, s in enumerate(("Numbers match the pins. Every story has two sources",
                           "from AP, Reuters, AFP, BBC or Al Jazeera, dated 24 Nov 2026.",
                           "Full sources, links and dates: README.md.")):
        text(d, kx + 14, ROW_Y[3] + 50 + i * 26, s, font("sans", 18))

    text(d, 24, 1004, "Source list, links and dates: README.md in this repository.", font("sans", 16), fill=MUTED)

    img = img.resize((W, H), Image.Resampling.LANCZOS)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes", count, "stories")


if __name__ == "__main__":
    main()
