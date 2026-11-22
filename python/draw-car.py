"""Tekniske skisser for 4WD FPV-bil (v2): topp, side og koblingsskjema."""
from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "png")
FONT_R = "C:/Windows/Fonts/segoeui.ttf"
FONT_B = "C:/Windows/Fonts/segoeuib.ttf"

def f(size, bold=False):
    try:
        return ImageFont.truetype(FONT_B if bold else FONT_R, size)
    except Exception:
        return ImageFont.load_default()

def rbox(d, x, y, w, h, fill=None, outline="black", r=6, width=2, dash=False):
    if dash:
        d.rounded_rectangle([x, y, x + w, y + h], radius=r, outline=outline, width=width)
        return
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=width)

def label(d, x, y, text, size=18, anchor="mm", bold=False, fill="black"):
    d.text((x, y), text, font=f(size, bold), fill=fill, anchor=anchor)

def polyline(d, pts, color="black", width=3):
    for i in range(len(pts) - 1):
        d.line([pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]], fill=color, width=width)

# ---------------------------------------------------------------- TOPP
def draw_top():
    W, H = 1800, 1150
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    S = 3.3
    cx, cy = 900, 650
    X = lambda mm: cx + mm * S
    Y = lambda mm: cy + mm * S

    label(d, W / 2, 46, "4WD FPV-BIL — TOPPVISNING", 34, bold=True)
    label(d, W / 2, 88, "Ramme 300×190 mm (30×30×2 alu) · akselavstand 240 · sporvidde 200 · hjul Ø100×32", 18, fill="#555")

    # topplate
    rbox(d, X(-150), Y(-95), 300 * S, 190 * S, outline="#b0bec5", width=2, dash=True, r=10)

    # rails
    for yy in (-70, 70):
        rbox(d, X(-150), Y(yy - 15), 300 * S, 30 * S, fill="#cfd8dc", outline="#607d8b", r=3)
    for xx in (-140, 140):
        rbox(d, X(xx - 15), Y(-65), 30 * S, 130 * S, fill="#cfd8dc", outline="#607d8b", r=3)

    # hjul + motorer
    for (mx, my, nm, side) in [(120, 100, "M1", "L"), (120, -100, "M2", "L"),
                               (-120, 100, "M3", "R"), (-120, -100, "M4", "R")]:
        rbox(d, X(mx - 50), Y(my - 16), 100 * S, 32 * S, fill="#263238", outline="#000", r=8)
        r = 21 * S
        d.ellipse([X(mx) - r, Y(my) - r, X(mx) + r, Y(my) + r], fill="#546e7a", outline="#000", width=2)
        label(d, X(mx), Y(my), nm, 15, bold=True, fill="white")

    # batteri
    rbox(d, X(-100), Y(-55), 150 * S, 50 * S, fill="#2e7d32", outline="#1b5e20", r=4)
    label(d, X(-25), Y(-30), "6S 6500 — pack 1", 15, bold=True, fill="white")
    rbox(d, X(-100), Y(5), 150 * S, 50 * S, fill="#2e7d32", outline="#1b5e20", r=4)
    label(d, X(-25), Y(30), "6S 6500 — pack 2", 15, bold=True, fill="white")

    # FC
    rbox(d, X(62), Y(-15), 30 * S, 30 * S, fill="#ffc107", outline="#b8860b", r=3)
    label(d, X(77), Y(0), "FC", 14, bold=True)

    # ESCs
    for (ex, ey, nm) in [(100, 55, "ESC L1"), (100, -55, "ESC L2"), (-100, 55, "ESC R1"), (-100, -55, "ESC R2")]:
        rbox(d, X(ex - 18), Y(ey - 11), 36 * S, 22 * S, fill="#ef6c00", outline="#a84300", r=2)
        label(d, X(ex), Y(ey), nm, 11, bold=True, fill="white")

    # Pi (stablet over batteri)
    rbox(d, X(-145), Y(-26), 85 * S, 52 * S, outline="#c62828", width=2, dash=True, r=3)
    label(d, X(-102), Y(-8), "Pi 4B", 13, bold=True, fill="#b71c1c")
    label(d, X(-102), Y(14), "(over batteri)", 11, fill="#b71c1c")

    # VTX / kamera / GPS
    rbox(d, X(-172), Y(-12), 16 * S, 24 * S, fill="#455a64", outline="#111", r=2)
    label(d, X(-196), Y(0), "VTX", 13, bold=True, anchor="rm")
    rbox(d, X(160), Y(-12), 16 * S, 24 * S, fill="#37474f", outline="#111", r=2)
    label(d, X(192), Y(0), "KAM", 13, bold=True, anchor="lm")
    d.ellipse([X(140) - 7 * S, Y(-42) - 7 * S, X(140) + 7 * S, Y(-42) + 7 * S], fill="#6a1b9a", outline="#4a0072")
    label(d, X(140), Y(-55), "GPS", 12, bold=True, fill="#4a0072")

    # mål
    y0 = 132
    d.line([X(-120), Y(y0), X(120), Y(y0)], fill="#0d47a1", width=2)
    for xx in (-120, 120):
        d.line([X(xx), Y(y0) - 8, X(xx), Y(y0) + 8], fill="#0d47a1", width=2)
    label(d, X(0), Y(y0 - 14), "240 (akselavstand)", 17, bold=True, fill="#0d47a1")

    x0 = 212
    d.line([X(x0), Y(-100), X(x0), Y(100)], fill="#0d47a1", width=2)
    for yy in (-100, 100):
        d.line([X(x0) - 8, Y(yy), X(x0) + 8, Y(yy)], fill="#0d47a1", width=2)
    label(d, X(x0 + 42), Y(0), "200", 17, bold=True, fill="#0d47a1")

    label(d, X(120), Y(-128), "Ø100 (hjul)", 15, bold=True, fill="#0d47a1")

    # notat
    label(d, 40, H - 40, "Rails: 30×30×2 mm · tverrstag ved x=±140 · Pi stablet over batteri", 15, anchor="lm", fill="#555")
    img.save(os.path.join(OUT, "bil-topp.png"))

# ---------------------------------------------------------------- SIDE
def draw_side():
    W, H = 1800, 900
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    S = 3.4
    cx, gy = 860, 760
    X = lambda mm: cx + mm * S
    Y = lambda mm: gy - mm * S

    label(d, W / 2, 46, "SIDEVISNING — klaring og høyder", 32, bold=True)

    d.line([60, gy, W - 60, gy], fill="#222", width=4)
    label(d, 70, gy + 24, "bakke", 14, anchor="lm", fill="#555")

    for wx in (-120, 120):
        r = 50 * S
        d.ellipse([X(wx) - r, Y(50) - r, X(wx) + r, Y(50) + r], fill="#263238", outline="#000", width=3)
        d.ellipse([X(wx) - 21 * S, Y(50) - 21 * S, X(wx) + 21 * S, Y(50) + 21 * S], fill="#546e7a", outline="#000", width=2)
        label(d, X(wx), Y(50), "motors", 12, anchor="mm", fill="white")

    # ramme
    rbox(d, X(-150), Y(55), 300 * S, 30 * S, fill="#cfd8dc", outline="#607d8b", r=2)
    # batteri (mellom hjulene i X, innenfor rammen i Y)
    rbox(d, X(-70), Y(105), 140 * S, 50 * S, fill="#2e7d32", outline="#1b5e20", r=4)
    label(d, X(0), Y(80), "2× 6S 6500", 15, bold=True, fill="white")
    # FC (stablet over batteri)
    rbox(d, X(-35), Y(120), 30 * S, 15 * S, outline="#b8860b", width=2, dash=True, r=2)
    label(d, X(-20), Y(128), "FC", 11, bold=True, fill="#8d6e00")
    # Pi (stablet)
    rbox(d, X(-65), Y(120), 25 * S, 15 * S, outline="#c62828", width=2, dash=True, r=2)
    label(d, X(-52), Y(128), "Pi", 10, bold=True, fill="#b71c1c")
    # kamera
    rbox(d, X(185), Y(70), 16 * S, 30 * S, fill="#37474f", outline="#111", r=2)
    label(d, X(193), Y(112), "kamera", 12, bold=True)
    d.line([X(193), Y(70), X(193), Y(55)], fill="#111", width=2)
    # VTX + antenne
    rbox(d, X(-190), Y(80), 16 * S, 20 * S, fill="#455a64", outline="#111", r=2)
    label(d, X(-182), Y(68), "VTX", 12, bold=True)
    d.line([X(-190), Y(100), X(-190), Y(195)], fill="#111", width=3)
    label(d, X(-190), Y(205), "antenne", 12)

    def vdim(xmm, y1, y2, txt):
        x = X(xmm)
        d.line([x, Y(y1), x, Y(y2)], fill="#0d47a1", width=2)
        for yy in (y1, y2):
            d.line([x - 8, Y(yy), x + 8, Y(yy)], fill="#0d47a1", width=2)
        label(d, x + 42, (Y(y1) + Y(y2)) / 2, txt, 15, bold=True, fill="#0d47a1", anchor="lm")

    vdim(200, 0, 25, "25")
    vdim(225, 25, 55, "30")
    vdim(250, 55, 105, "50")

    label(d, 40, H - 30, "Bakkeklaring 25 mm · ramme 30 mm · batteri 50 mm · total høyde ~105 mm + antenne", 14, anchor="lm", fill="#555")
    img.save(os.path.join(OUT, "bil-side.png"))

# ---------------------------------------------------------------- KOBLING
def draw_wiring():
    W, H = 1900, 1200
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    RED, BLUE, GREEN, PURPLE = "#c62828", "#1565c0", "#2e7d32", "#6a1b9a"

    label(d, W / 2, 44, "KOBLINGSSKJEMA — 4WD FPV-bil (ArduPilot Rover, skid steer)", 32, bold=True)
    label(d, W / 2, 84, "Rød = strøm · Blå = ESC-signal (PWM) · Grønn = video · Lilla = UART/CRSF", 16, fill="#555")

    # batteri -> sikring -> bryter -> bus
    rbox(d, 60, 500, 200, 150, fill="#2e7d32", outline="#1b5e20")
    label(d, 160, 530, "6S LiPo", 20, bold=True, fill="white")
    label(d, 160, 562, "2× 6500 mAh", 14, fill="white")
    label(d, 160, 588, "= 13 Ah 60C", 14, fill="white")

    rbox(d, 300, 525, 110, 100, fill="#fff8e1", outline="#ef6c00")
    label(d, 355, 558, "SIKRING", 15, bold=True)
    label(d, 355, 584, "100 A", 14)

    rbox(d, 450, 525, 110, 100, fill="#fff8e1", outline="#ef6c00")
    label(d, 505, 558, "HOVED-", 15, bold=True)
    label(d, 505, 584, "BRYTER", 15, bold=True)

    d.line([260, 575, 300, 575], fill=RED, width=4)
    d.line([410, 575, 450, 575], fill=RED, width=4)
    d.line([560, 575, 640, 575], fill=RED, width=4)

    rbox(d, 620, 330, 30, 560, fill="#b0bec5", outline="#546e7a")
    label(d, 635, 305, "12V bus", 14, bold=True)

    # ESC-er
    escs = [(760, 340, "ESC L1", "M1"), (760, 470, "ESC L2", "M2"),
            (760, 730, "ESC R1", "M3"), (760, 860, "ESC R2", "M4")]
    for (x, y, nm, motor) in escs:
        rbox(d, x, y, 170, 80, fill="#ef6c00", outline="#a84300")
        label(d, x + 85, y + 28, nm, 16, bold=True, fill="white")
        label(d, x + 85, y + 55, "80 A · 2–6S", 12, fill="white")
        d.line([650, y + 40, x, y + 40], fill=RED, width=4)
        # motor
        cxm = x + 260
        d.ellipse([cxm - 30, y + 10, cxm + 30, y + 70], fill="#546e7a", outline="#000", width=2)
        label(d, cxm, y + 40, motor, 12, bold=True, fill="white")
        d.line([x + 170, y + 40, cxm - 30, y + 40], fill="#111", width=4)

    # FC
    rbox(d, 1080, 500, 250, 160, fill="#ffc107", outline="#b8860b", width=3)
    label(d, 1205, 530, "FC DakeFPV H743", 18, bold=True)
    label(d, 1205, 558, "ArduPilot Rover", 14)
    label(d, 1205, 586, "SERVO1 → venstre par", 13)
    label(d, 1205, 606, "SERVO2 → høyre par", 13)
    label(d, 1205, 632, "FRAME_CLASS = 2", 13)

    # Y-kabel venstre (SERVO1)
    polyline(d, [(1080, 530), (955, 530), (955, 380), (930, 380)], color=BLUE, width=4)
    polyline(d, [(955, 510), (930, 510)], color=BLUE, width=4)
    label(d, 935, 322, "Y-kabel venstre par", 12, fill=BLUE, anchor="lm")

    # Y-kabel høyre (SERVO2)
    polyline(d, [(1080, 640), (965, 640), (965, 770), (930, 770)], color=BLUE, width=4)
    polyline(d, [(965, 900), (930, 900)], color=BLUE, width=4)
    polyline(d, [(965, 770), (965, 900)], color=BLUE, width=4)
    label(d, 935, 975, "Y-kabel høyre par", 12, fill=BLUE, anchor="lm")

    # BEC
    rbox(d, 1100, 760, 180, 90, fill="#e1f5fe", outline="#0277bd")
    label(d, 1190, 790, "5V BEC 5 A", 16, bold=True)
    label(d, 1190, 816, "(FC + RX)", 13)
    polyline(d, [(650, 960), (1060, 960), (1060, 805), (1100, 805)], color=RED, width=3)
    label(d, 880, 975, "12 V inn", 12, fill=RED)
    polyline(d, [(1190, 760), (1190, 700)], color=RED, width=3)

    # RX / GPS / Pi / VTX
    rbox(d, 1420, 340, 220, 90, fill="#e8f5e9", outline="#2e7d32")
    label(d, 1530, 368, "ELRS RX ER16", 17, bold=True)
    label(d, 1530, 394, "CRSF", 13)
    polyline(d, [(1330, 540), (1370, 540), (1370, 385), (1420, 385)], color=PURPLE, width=3)
    label(d, 1375, 520, "CRSF", 12, fill=PURPLE, anchor="lm")

    rbox(d, 1420, 470, 220, 90, fill="#f3e5f5", outline="#6a1b9a")
    label(d, 1530, 498, "GPS M100-5883", 16, bold=True)
    label(d, 1530, 524, "M10 + kompass", 13)
    polyline(d, [(1330, 600), (1370, 600), (1370, 515), (1420, 515)], color=PURPLE, width=3)

    rbox(d, 1420, 600, 220, 100, fill="#ffebee", outline="#c62828")
    label(d, 1530, 628, "Raspberry Pi 4B", 16, bold=True)
    label(d, 1530, 654, "8 GB + 4G-modem", 13)
    label(d, 1530, 678, "MAVLink / video IP", 12)
    polyline(d, [(1330, 650), (1370, 650), (1370, 655), (1420, 655)], color=PURPLE, width=3)

    rbox(d, 1420, 760, 230, 100, fill="#e0f2f1", outline="#00695c")
    label(d, 1535, 790, "VTX 25 mW + KAM", 16, bold=True)
    label(d, 1535, 816, "5,8 GHz (lovlig)", 13)
    polyline(d, [(1280, 805), (1420, 805)], color=GREEN, width=3)
    label(d, 1350, 790, "video + 5 V", 12, fill=GREEN)
    d.line([1650, 770, 1680, 700], fill="#111", width=3)
    label(d, 1695, 690, "antenne", 12)

    # RX 5V fra BEC
    polyline(d, [(1280, 790), (1340, 790), (1340, 370), (1420, 370)], color=RED, width=2)
    label(d, 1300, 730, "5 V", 12, fill=RED)

    label(d, 40, 1120, "! Fjern +5V (rød ledning) fra 3 av 4 ESC — bare én BEC skal være aktiv", 17, bold=True, fill="#b71c1c", anchor="lm")
    label(d, 40, 1155, "! Felles jord mellom batteri, ESC, FC og mottaker er påkrevd", 17, bold=True, fill="#b71c1c", anchor="lm")

    img.save(os.path.join(OUT, "bil-kobling.png"))

if __name__ == "__main__":
    draw_top()
    draw_side()
    draw_wiring()
    print("OK: bil-topp.png, bil-side.png, bil-kobling.png")
