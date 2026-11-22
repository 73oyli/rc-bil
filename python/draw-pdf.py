"""Tegningspakke (PDF) for 4WD FPV-bil med hjuloppheng, styring og pan/tilt-gimbal.
Kjor: python draw-pdf.py  -> bil-tegninger.pdf
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "png")
FONT_R = "C:/Windows/Fonts/segoeui.ttf"
FONT_B = "C:/Windows/Fonts/segoeuib.ttf"
W, H = 2339, 1654

def f(sz, bold=False):
    try:
        return ImageFont.truetype(FONT_B if bold else FONT_R, sz)
    except Exception:
        return ImageFont.load_default()

def page(title, sub=""):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, W - 40, H - 40], outline="#cfd8dc", width=3)
    d.text((W / 2, 80), title, font=f(40, True), fill="#111", anchor="mm")
    if sub:
        d.text((W / 2, 128), sub, font=f(21), fill="#555", anchor="mm")
    d.text((W - 60, H - 58), "Mal i mm | konseptskisse", font=f(18), fill="#777", anchor="rb")
    return img, d

def txt(d, x, y, s, sz=20, anchor="mm", bold=False, fill="#111"):
    d.text((x, y), s, font=f(sz, bold), fill=fill, anchor=anchor)

def box(d, x, y, w, h, fill=None, outline="#111", r=6, wid=2, dash=False):
    if dash:
        d.rounded_rectangle([x, y, x + w, y + h], radius=r, outline=outline, width=wid)
        return
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=wid)

def hdim(d, x1, x2, y, s, col="#0d47a1", sz=18):
    d.line([x1, y, x2, y], fill=col, width=2)
    for x in (x1, x2):
        d.line([x, y - 9, x, y + 9], fill=col, width=2)
    d.polygon([(x1, y), (x1 + 12, y - 4), (x1 + 12, y + 4)], fill=col)
    d.polygon([(x2, y), (x2 - 12, y - 4), (x2 - 12, y + 4)], fill=col)
    txt(d, (x1 + x2) / 2, y - 18, s, sz, bold=True, fill=col)

def vdim(d, y1, y2, x, s, col="#0d47a1", sz=18):
    d.line([x, y1, x, y2], fill=col, width=2)
    for y in (y1, y2):
        d.line([x - 9, y, x + 9, y], fill=col, width=2)
    txt(d, x + 16, (y1 + y2) / 2, s, sz, bold=True, fill=col, anchor="lm")

def wheel_top(d, cx, cy, S, D=100, Wd=32):
    box(d, cx - D / 2 * S, cy - Wd / 2 * S, D * S, Wd * S, fill="#263238", outline="#000", r=10)
    r = 21 * S
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#546e7a", outline="#000", width=2)

# ------------------------------------------------ P1 topp
def p1():
    img, d = page("4WD FPV-BIL - OVERSIKT (topp)",
                  "Aksavstand 300 | sporvidde 210 | ramme 380x200 | hjul 100x32")
    S = 3.0; cx, cy = W / 2, 900
    X = lambda mm: cx + mm * S
    Y = lambda mm: cy + mm * S

    box(d, X(-190), Y(-100), 380 * S, 200 * S, outline="#b0bec5", wid=2, dash=True, r=14)
    for yy in (-85, 85):
        box(d, X(-190), Y(yy - 15), 380 * S, 30 * S, fill="#cfd8dc", outline="#607d8b", r=4)
    for xx in (-175, 0, 175):
        box(d, X(xx - 15), Y(-85), 30 * S, 170 * S, fill="#cfd8dc", outline="#607d8b", r=4)

    for (mx, my, nm) in [(150, 105, "M1"), (150, -105, "M2"), (-150, 105, "M3"), (-150, -105, "M4")]:
        wheel_top(d, X(mx), Y(my), S)
        txt(d, X(mx), Y(my), nm, 15, bold=True, fill="white")

    for (yy, nm) in [(-30, "6S 6500 #1"), (30, "6S 6500 #2")]:
        box(d, X(-75), Y(yy - 25), 150 * S, 50 * S, fill="#2e7d32", outline="#1b5e20", r=5)
        txt(d, X(0), Y(yy), nm, 15, bold=True, fill="white")

    box(d, X(55), Y(-15), 30 * S, 30 * S, fill="#ffc107", outline="#b8860b", r=3)
    txt(d, X(70), Y(0), "FC", 13, bold=True)
    for (ex, ey, nm) in [(115, 55, "ESC1"), (115, -55, "ESC2"), (-115, 55, "ESC3"), (-115, -55, "ESC4")]:
        box(d, X(ex - 18), Y(ey - 11), 36 * S, 22 * S, fill="#ef6c00", outline="#a84300", r=2)
        txt(d, X(ex), Y(ey), nm, 10, bold=True, fill="white")

    box(d, X(105), Y(-12), 40 * S, 20 * S, fill="#7b1fa2", outline="#4a0072", r=3)
    txt(d, X(125), Y(-22), "styreservo", 11, bold=True, fill="#4a0072")
    d.ellipse([X(175) - 10 * S, Y(0) - 10 * S, X(175) + 10 * S, Y(0) + 10 * S], fill="#455a64", outline="#111")
    txt(d, X(175), Y(20), "gimbal", 11, bold=True)

    box(d, X(-205), Y(-10), 16 * S, 20 * S, fill="#455a64", outline="#111", r=2)
    txt(d, X(-232), Y(0), "VTX", 12, bold=True, anchor="rm")
    d.ellipse([X(-120) - 8 * S, Y(-60) - 8 * S, X(-120) + 8 * S, Y(-60) + 8 * S], fill="#6a1b9a", outline="#4a0072")
    txt(d, X(-120), Y(-78), "GPS", 11, bold=True, fill="#4a0072")
    box(d, X(-70), Y(60), 60 * S, 40 * S, outline="#c62828", wid=2, dash=True, r=3)
    txt(d, X(-40), Y(80), "Pi 4B", 11, bold=True, fill="#b71c1c")

    hdim(d, X(-150), X(150), Y(150), "300 (aksavstand)")
    vdim(d, Y(-105), Y(105), X(250), "210")
    txt(d, X(150), Y(-140), "hjul 100", 16, bold=True, fill="#0d47a1")
    img.save(os.path.join(OUT, "pdf-p1.png"))

# ------------------------------------------------ P2 side
def p2():
    img, d = page("SIDEVISNING - hjuloppheng og hoyder",
                  "Bakkeklaring 30 | ramme 30 | batteri 50 | fjaeringsvei 20")
    S = 3.2; cx, gy = W / 2, 1380
    X = lambda mm: cx + mm * S
    Y = lambda mm: gy - mm * S

    d.line([120, gy, W - 120, gy], fill="#222", width=4)
    txt(d, 130, gy + 26, "bakke", 16, anchor="lm", fill="#555")

    for wx in (-150, 150):
        r = 50 * S
        d.ellipse([X(wx) - r, Y(50) - r, X(wx) + r, Y(50) + r], fill="#263238", outline="#000", width=4)
        d.ellipse([X(wx) - 21 * S, Y(50) - 21 * S, X(wx) + 21 * S, Y(50) + 21 * S],
                  fill="#546e7a", outline="#000", width=2)

    box(d, X(-190), Y(60), 380 * S, 30 * S, fill="#cfd8dc", outline="#607d8b", r=3)
    for y in (-60, 60):
        box(d, X(-75), Y(y + 25), 150 * S, 50 * S, fill="#2e7d32", outline="#1b5e20", r=4)

    box(d, X(105), Y(85), 40 * S, 20 * S, fill="#7b1fa2", outline="#4a0072", r=3)
    d.line([X(175), Y(60), X(175), Y(150)], fill="#111", width=5)
    box(d, X(165), Y(170), 25 * S, 25 * S, fill="#37474f", outline="#111", r=3)
    txt(d, X(200), Y(170), "kamera", 12, bold=True)

    for wx in (-150, 150):
        d.line([X(wx - 40), Y(60), X(wx), Y(50)], fill="#000", width=6)
        d.line([X(wx - 25), Y(95), X(wx - 5), Y(55)], fill="#c62828", width=6)

    vdim(d, Y(30), Y(0), X(250), "30")
    vdim(d, Y(60), Y(30), X(285), "30")
    vdim(d, Y(110), Y(60), X(320), "50")
    txt(d, X(150), Y(140), "fjaeringsvei 20", 16, bold=True, fill="#c62828")
    img.save(os.path.join(OUT, "pdf-p2.png"))

# ------------------------------------------------ P3 styring
def p3():
    img, d = page("FORAKSEL OG STYRING (topp, detalj)",
                  "Servo 40x20x38 | styrestag | Ackermann-geometri")
    S = 4.2; cx, cy = 980, 880
    X = lambda mm: cx + mm * S
    Y = lambda mm: cy + mm * S

    # ramme bak forakselen
    for yy in (-85, 85):
        box(d, X(-170), Y(yy - 15), 300 * S, 30 * S, fill="#cfd8dc", outline="#607d8b", r=3)
    box(d, X(140), Y(-100), 30 * S, 200 * S, fill="#cfd8dc", outline="#607d8b", r=3)

    # servo sentralt
    box(d, X(-20), Y(-10), 40 * S, 20 * S, fill="#7b1fa2", outline="#4a0072", r=3)
    txt(d, X(0), Y(-26), "styreservo 40x20x38", 14, bold=True, fill="#4a0072")

    for sy, nm, ang, angtxt in [(-1, "M2", 30, "indre 30 grader"), (1, "M1", 22, "ytre 22 grader")]:
        d.ellipse([X(160) - 9 * S, Y(sy * 105) - 9 * S, X(160) + 9 * S, Y(sy * 105) + 9 * S],
                  fill="#ffd54f", outline="#b8860b", width=3)
        wheel_top(d, X(160), Y(sy * 105), S)
        txt(d, X(160), Y(sy * 105), nm, 14, bold=True, fill="white")
        # styrearm og stag
        d.line([X(160), Y(sy * 105), X(120), Y(sy * 82)], fill="#b8860b", width=7)
        d.line([X(120), Y(sy * 82), X(20), Y(sy * 14)], fill="#0d47a1", width=5)
        # ackermann-linje
        ex = X(160) + 80 * S * math.cos(math.radians(ang))
        ey = Y(sy * 105) - 80 * S * math.sin(math.radians(ang)) * sy
        d.line([X(160), Y(sy * 105), ex, ey], fill="#c62828", width=3)
        txt(d, ex + 30, ey, angtxt, 13, bold=True, fill="#c62828")

    vdim(d, Y(-105), Y(105), X(240), "210 (sporvidde)")
    txt(d, X(-30), Y(40), "styrestag ~120", 14, bold=True, fill="#0d47a1")
    txt(d, X(30), Y(170), "Ackermann: indre hjul svinger mer enn ytre", 17, bold=True)
    txt(d, X(30), Y(192), "TURN_RADIUS 1,2 m", 15, fill="#555")
    img.save(os.path.join(OUT, "pdf-p3.png"))

# ------------------------------------------------ P4 hjuloppheng
def p4():
    img, d = page("HJULOPPHENG (frontvisning, en side)",
                  "Baerearm 45 | demper 70 | fjaeringsvei 20 | motor i navet")
    S = 3.5; gy = 1400
    X = lambda mm: 620 + mm * S
    Y = lambda mm: gy - mm * S

    d.line([160, gy, W - 160, gy], fill="#222", width=4)
    txt(d, 170, gy + 26, "bakke", 15, anchor="lm", fill="#555")

    # hjul
    r = 50 * S
    d.ellipse([X(0) - r, Y(50) - r, X(0) + r, Y(50) + r], fill="#263238", outline="#000", width=4)
    d.ellipse([X(0) - 15 * S, Y(50) - 15 * S, X(0) + 15 * S, Y(50) + 15 * S],
              fill="#546e7a", outline="#000", width=2)
    txt(d, X(0), Y(50), "4250", 13, bold=True, fill="white")

    # ramme (tverrsnitt)
    box(d, X(48), Y(90), 30 * S, 30 * S, fill="#cfd8dc", outline="#607d8b", r=3)
    txt(d, X(63), Y(110), "ramme 30x30", 12, bold=True)

    # baerearm (to stag)
    for dz in (0, 12):
        d.line([X(48), Y(62 + dz), X(0), Y(50 + dz)], fill="#455a64", width=7)
    txt(d, X(24), Y(40), "baerearm 45", 13, bold=True, fill="#37474f")

    # demper
    d.line([X(60), Y(90), X(20), Y(54)], fill="#c62828", width=10)
    txt(d, X(70), Y(96), "demper 70", 13, bold=True, fill="#c62828")

    # mal
    vdim(d, Y(100), Y(50), X(-70), "50 (radius)")
    vdim(d, Y(30), Y(0), X(-105), "30")
    hdim(d, X(0), X(48), Y(-25), "45 (baerearm)")

    # notater
    txt(d, 1150, 700, "motorfeste: 4xM3 i motorklokke", 16, bold=True, anchor="lm")
    txt(d, 1150, 760, "nav printes i PETG/ASA", 15, anchor="lm")
    txt(d, 1150, 810, "dekk i TPU 95A", 15, anchor="lm")
    txt(d, 1150, 880, "demperfeste: 2xM3 ramme + arm", 15, anchor="lm")
    txt(d, 1150, 950, "baerearm: 3D-print PETG eller alu", 15, anchor="lm")
    txt(d, 1150, 1020, "fjaeringsvei 20 mm", 15, anchor="lm", fill="#c62828")
    img.save(os.path.join(OUT, "pdf-p4.png"))

# ------------------------------------------------ P5 gimbal
def p5():
    img, d = page("PAN/TILT-GIMBAL FOR FPV-KAMERA",
                  "Head tracker -> CH7 (pan) / CH8 (tilt) | kamera 25x25")
    S = 4.6; gy = 1350

    def view(cx, label):
        X = lambda mm: cx + mm * S
        Y = lambda mm: gy - mm * S
        txt(d, cx, 1500, label, 26, bold=True)
        d.line([cx - 300, gy, cx + 300, gy], fill="#222", width=3)
        # ramme
        box(d, X(-90), Y(60), 180 * S, 30 * S, fill="#cfd8dc", outline="#607d8b", r=3)
        # mast
        d.line([X(0), Y(60), X(0), Y(150)], fill="#111", width=7)
        # pan-servo
        box(d, X(-12), Y(173), 24 * S, 23 * S, fill="#455a64", outline="#111", r=3)
        # brakett
        box(d, X(-25), Y(196), 50 * S, 6 * S, fill="#78909c", outline="#111", r=2)
        # tilt-servo
        box(d, X(-12), Y(219), 24 * S, 23 * S, fill="#7b1fa2", outline="#111", r=3)
        # kamera
        box(d, X(-13), Y(244), 26 * S, 25 * S, fill="#37474f", outline="#111", r=3)
        return X, Y

    X1, Y1 = view(620, "FRONT")
    X2, Y2 = view(1720, "SIDE")

    txt(d, 620 + 60, Y1(185), "pan-servo", 15, bold=True)
    txt(d, 620 + 60, Y1(230), "tilt-servo", 15, bold=True, fill="#7b1fa2")
    txt(d, 620 + 80, Y1(255), "kamera 25x25", 15, bold=True)
    vdim(d, Y1(244), Y1(60), X1(120), "185 (total)")
    vdim(d, Y1(150), Y1(60), X1(158), "90 (mast)")

    txt(d, 1720 + 70, Y2(173), "pan", 15, bold=True)
    txt(d, 1720 + 70, Y2(219), "tilt", 15, bold=True, fill="#7b1fa2")
    txt(d, 1720 + 70, Y2(244), "kamera", 15, bold=True)
    hdim(d, X2(-25), X2(25), Y2(268), "50 (brakett)")
    img.save(os.path.join(OUT, "pdf-p5.png"))

# ------------------------------------------------ P6 kobling
def p6():
    img, d = page("KOBLINGSSKJEMA - styring + 4WD + gimbal",
                  "Rod = strom | Bla = signal | Gronn = video | Lilla = UART/CRSF")
    RED, BLUE, GREEN, PURPLE = "#c62828", "#1565c0", "#2e7d32", "#6a1b9a"

    def line(*pts, c="#111", w=4):
        for i in range(0, len(pts) - 2, 2):
            d.line([pts[i], pts[i + 1], pts[i + 2], pts[i + 3]], fill=c, width=w)

    box(d, 80, 650, 210, 160, fill="#2e7d32", outline="#1b5e20")
    txt(d, 185, 690, "6S LiPo", 22, bold=True, fill="white")
    txt(d, 185, 725, "2x 6500 mAh", 15, fill="white")
    txt(d, 185, 755, "13 Ah 60C", 15, fill="white")

    box(d, 340, 675, 120, 110, fill="#fff8e1", outline="#ef6c00")
    txt(d, 400, 710, "SIKRING", 15, bold=True)
    txt(d, 400, 740, "100 A", 14)
    box(d, 500, 675, 120, 110, fill="#fff8e1", outline="#ef6c00")
    txt(d, 560, 710, "HOVED-", 15, bold=True)
    txt(d, 560, 740, "BRYTER", 15, bold=True)
    line(290, 730, 340, 730, c=RED)
    line(460, 730, 500, 730, c=RED)
    line(620, 730, 690, 730, c=RED)

    box(d, 690, 470, 30, 620, fill="#b0bec5", outline="#546e7a")
    txt(d, 705, 445, "12V bus", 14, bold=True)

    escs = [(830, 470, "ESC1", "M1"), (830, 600, "ESC2", "M2"),
            (830, 930, "ESC3", "M3"), (830, 1060, "ESC4", "M4")]
    for (x, y, nm, mt) in escs:
        box(d, x, y, 180, 85, fill="#ef6c00", outline="#a84300")
        txt(d, x + 90, y + 30, nm, 16, bold=True, fill="white")
        txt(d, x + 90, y + 58, "80 A - 2-6S", 12, fill="white")
        line(720, y + 42, x, y + 42, c=RED)
        d.ellipse([x + 240, y + 12, x + 300, y + 72], fill="#546e7a", outline="#000", width=2)
        txt(d, x + 270, y + 42, mt, 12, bold=True, fill="white")
        line(x + 180, y + 42, x + 240, y + 42, c="#111")

    box(d, 1180, 620, 280, 190, fill="#ffc107", outline="#b8860b", wid=3)
    txt(d, 1320, 660, "FC DakeFPV H743", 18, bold=True)
    txt(d, 1320, 690, "ArduPilot Rover", 14)
    txt(d, 1320, 720, "FRAME_CLASS = 1", 13)
    txt(d, 1320, 742, "SERVO1 = Steering (26)", 12)
    txt(d, 1320, 764, "SERVO3 = Throttle (70)", 12)

    line(1180, 765, 1110, 765, c=BLUE)
    line(1110, 765, 1110, 512, c=BLUE)
    line(1110, 512, 1010, 512, c=BLUE)
    line(1110, 642, 1010, 642, c=BLUE)
    line(1110, 765, 1110, 972, c=BLUE)
    line(1110, 972, 1010, 972, c=BLUE)
    line(1110, 765, 1110, 1102, c=BLUE)
    line(1110, 1102, 1010, 1102, c=BLUE)
    txt(d, 1010, 455, "Throttle -> Y til alle 4 ESC", 12, fill=BLUE, anchor="lm")

    box(d, 1180, 880, 280, 90, fill="#7b1fa2", outline="#4a0072")
    txt(d, 1320, 908, "STYRESERVO", 16, bold=True, fill="white")
    txt(d, 1320, 936, "SERVO1 - Steering", 12, fill="white")
    line(1180, 700, 1145, 700, c=BLUE)
    line(1145, 700, 1145, 925, c=BLUE)
    line(1145, 925, 1180, 925, c=BLUE)

    box(d, 1530, 880, 210, 110, fill="#e1f5fe", outline="#0277bd")
    txt(d, 1635, 910, "5V BEC 5 A", 16, bold=True)
    txt(d, 1635, 938, "FC + RX + servo", 12)
    line(690, 1140, 1490, 1140, c=RED)
    line(1490, 1140, 1490, 935, c=RED)
    line(1490, 935, 1530, 935, c=RED)
    line(1635, 880, 1635, 810, c=RED)

    box(d, 1530, 500, 240, 100, fill="#e8f5e9", outline="#2e7d32")
    txt(d, 1650, 530, "ELRS RX ER16", 17, bold=True)
    txt(d, 1650, 560, "CRSF | CH7/CH8 = gimbal", 12)
    line(1460, 660, 1495, 660, c=PURPLE)
    line(1495, 660, 1495, 550, c=PURPLE)
    line(1495, 550, 1530, 550, c=PURPLE)

    box(d, 1530, 700, 240, 90, fill="#f3e5f5", outline="#6a1b9a")
    txt(d, 1650, 728, "GPS M100-5883", 16, bold=True)
    txt(d, 1650, 754, "M10 + kompass", 12)
    line(1460, 730, 1530, 745, c=PURPLE)

    box(d, 1530, 1000, 240, 100, fill="#ffebee", outline="#c62828")
    txt(d, 1650, 1030, "Raspberry Pi 4B", 16, bold=True)
    txt(d, 1650, 1058, "MAVLink / video IP", 12)
    line(1460, 770, 1495, 770, c=PURPLE)
    line(1495, 770, 1495, 1050, c=PURPLE)
    line(1495, 1050, 1530, 1050, c=PURPLE)

    box(d, 1530, 1170, 250, 110, fill="#e0f2f1", outline="#00695c")
    txt(d, 1655, 1200, "VTX 25 mW + KAM", 16, bold=True)
    txt(d, 1655, 1228, "5,8 GHz (lovlig)", 12)
    line(1740, 880, 1740, 1170, c=RED, w=2)

    box(d, 1830, 470, 180, 70, fill="#e8eaf6", outline="#3949ab")
    txt(d, 1920, 492, "PAN-servo", 14, bold=True)
    txt(d, 1920, 516, "CH7", 13)
    box(d, 1830, 560, 180, 70, fill="#e8eaf6", outline="#3949ab")
    txt(d, 1920, 582, "TILT-servo", 14, bold=True)
    txt(d, 1920, 606, "CH8", 13)

    txt(d, 80, 1500, "! Fjern +5V (rod) fra 3 av 4 ESC - bare en BEC aktiv | felles jord pakrevd", 18, bold=True, fill="#b71c1c", anchor="lm")
    txt(d, 80, 1540, "! Styreservo: egen 5V hvis kraftig (>3 A) | gimbal-servoer fra RX (CH7/CH8)", 18, bold=True, fill="#b71c1c", anchor="lm")
    img.save(os.path.join(OUT, "pdf-p6.png"))

# ------------------------------------------------ P7 BOM
def p7():
    img, d = page("DELELISTE OG ARDUPILOT-PARAMETERE", "Priser er omtrentlige (NOK, 2026)")
    rows = [
        ("Chassis", "Alu 30x30x2 + 3 mm plater, egen ramme", "1", "600-1200"),
        ("Motor", "4250 800KV (har)", "4", "-"),
        ("ESC", "Hobbywing Skywalker V2 80A (har)", "4", "-"),
        ("FC", "DakeFPV H743 (har)", "1", "-"),
        ("Servo", "Styreservo 25 kg, metallgir", "1", "300-500"),
        ("Dempere", "Oliedemper 70 mm, 1:10", "4", "400-700"),
        ("Hjul", "3D-print: nav PETG + dekk TPU 95A", "4", "200"),
        ("Batteri", "6S 6500 mAh 60C (har 2)", "2", "-"),
        ("GPS", "HGLRC M100-5883 (har)", "1", "-"),
        ("RX", "ELRS ER16 (har)", "1", "-"),
        ("Gimbal", "2x MG90S + print", "1", "200"),
        ("Kamera/VTX", "25 mW 5,8 GHz + kamera", "1", "650-1100"),
        ("Pi", "Raspberry Pi 4B 8GB + 4G (har)", "1", "-"),
        ("Smatteri", "Ledninger, BEC, sikring, bryter", "-", "500"),
    ]
    y = 250
    d.text((140, y), "DEL", font=f(22, True), fill="#111")
    d.text((600, y), "BESKRIVELSE", font=f(22, True), fill="#111")
    d.text((1560, y), "ANT", font=f(22, True), fill="#111")
    d.text((1680, y), "PRIS", font=f(22, True), fill="#111")
    d.line([120, y + 36, W - 120, y + 36], fill="#999", width=2)
    y += 70
    for (a, b, c, e) in rows:
        d.text((140, y), a, font=f(19), fill="#111")
        d.text((600, y), b, font=f(18), fill="#333")
        d.text((1560, y), c, font=f(19), fill="#111")
        d.text((1680, y), e, font=f(19), fill="#111")
        y += 52
    d.line([120, y + 10, W - 120, y + 10], fill="#999", width=2)
    d.text((140, y + 40), "Totalt (nye deler): ca. 2 900 - 4 200 NOK", font=f(24, True), fill="#0d47a1")

    y2 = y + 130
    d.text((140, y2), "ArduPilot Rover - parametere (Ackermann + 6S-begrensning)", font=f(26, True), fill="#111")
    params = [
        "FRAME_CLASS = 1        (Ackermann/styring)",
        "SERVO1_FUNCTION = 26   (Steering)",
        "SERVO3_FUNCTION = 70   (Throttle -> Y til 4 ESC)",
        "MOT_PWM_TYPE = 0       (Normal PWM)",
        "MOT_THR_MAX = 60       (6S-begrensning)",
        "MOT_SLEW_UP/DN = 0.5   (myk start)",
        "CRUISE_SPEED = 3 m/s | TURN_RADIUS = 1.2 m",
        "FS_THR_ENABLE = 1 | FS_ACTION = 2 (stopp)",
        "BATT_MONITOR = 4 | BATT_CAPACITY = 13000",
    ]
    for i, p in enumerate(params):
        d.text((160, y2 + 55 + i * 46), p, font=f(20))
        y2 += 0
    img.save(os.path.join(OUT, "pdf-p7.png"))

# ------------------------------------------------ P8 hjulvinkler
def p8():
    img, d = page("HJULVINKLER, BUMP-STOP OG DEMPERKURVE",
                  "Camber +-10 | toe +-5 | bump-stop 15 mm | progressiv demper")

    def rot_pts(pts, ox, oy, ang):
        a = math.radians(ang)
        out = []
        for (x, y) in pts:
            dx, dy = x - ox, y - oy
            out.append((ox + dx * math.cos(a) - dy * math.sin(a),
                        oy + dx * math.sin(a) + dy * math.cos(a)))
        return out

    # --- CAMBER (frontvisning) ---
    cx, gy = 380, 1180
    txt(d, cx, 250, "CAMBER (front)", 24, bold=True)
    d.line([cx - 260, gy, cx + 260, gy], fill="#222", width=3)
    # referansehjulet (rett)
    d.rounded_rectangle([cx - 16, gy - 100, cx + 16, gy], radius=6, outline="#9e9e9e", width=2)
    # hjulet med camber -8 grader, rotert om kontaktpunktet
    ang = -8
    pts = [(-16, -100), (16, -100), (16, 0), (-16, 0)]
    poly = rot_pts([(cx + x, gy + y) for (x, y) in pts], cx, gy, ang)
    d.polygon(poly, fill="#263238", outline="#000")
    d.ellipse([cx - 5, gy - 55, cx + 5, gy - 45], fill="#90a4ae")
    # vinkelbue
    d.arc([cx - 120, gy - 120, cx + 120, gy + 120], 270, 270 + abs(ang), fill="#c62828", width=3)
    txt(d, cx + 150, gy - 105, "camber -8 grader", 15, bold=True, fill="#c62828")
    txt(d, cx, gy + 40, "kontaktpunkt", 13, fill="#555")
    vdim(d, gy - 100, gy, cx - 80, "100")

    # --- TOE (toppvisning) ---
    tx, ty = 1180, 900
    txt(d, tx, 250, "TOE (bakhjul, topp)", 24, bold=True)
    d.line([tx - 300, ty, tx + 300, ty], fill="#9e9e9e", width=2)
    txt(d, tx + 320, ty, "senterlinje", 13, anchor="lm", fill="#777")
    for sy in (-1, 1):
        wy = ty + sy * 90
        toe = 4
        pts = [(tx - 50, wy - 16), (tx + 50, wy - 16), (tx + 50, wy + 16), (tx - 50, wy + 16)]
        poly = rot_pts(pts, tx, wy, -sy * toe)
        d.polygon(poly, fill="#263238", outline="#000")
        txt(d, tx, wy + sy * 40, "toe-in 4 grader", 13, bold=True, fill="#c62828")
    hdim(d, tx - 50, tx + 50, ty + 190, "100 (hjul)")

    # --- BUMP-STOP + demper ---
    bx = 1900
    txt(d, bx, 250, "BUMP-STOP", 24, bold=True)
    d.line([bx - 40, 1100, bx + 40, 1100], fill="#222", width=4)  # nedre feste
    d.line([bx, 1100, bx, 380], fill="#555", width=10)            # demperlegeme
    for i in range(9):
        y = 1060 - i * 70
        d.line([bx - 26, y, bx + 26, y - 20], fill="#b0bec5", width=3)
        d.line([bx + 26, y - 20, bx - 26, y - 40], fill="#b0bec5", width=3)
    # bump-stop
    d.rounded_rectangle([bx - 22, 420, bx + 22, 500], radius=4, fill="#c62828", outline="#7f0000")
    txt(d, bx + 60, 460, "bump-stop (TPU)", 14, bold=True, fill="#b71c1c")
    vdim(d, 1100, 380, bx - 80, "70 (demper)")
    vdim(d, 1100, 420, bx + 80, "15 (stopp)")

    # --- DEMPERKURVE ---
    ox, oy = 500, 1500
    txt(d, ox + 260, 1230, "DEMPERKURVE (progressiv)", 22, bold=True)
    d.line([ox, oy, ox, oy - 220], fill="#222", width=3)
    d.line([ox, oy, ox + 520, oy], fill="#222", width=3)
    txt(d, ox - 20, oy - 230, "kraft", 14, anchor="rm")
    txt(d, ox + 540, oy + 10, "innfjaering (mm)", 14, anchor="lm")
    pts = []
    for i in range(0, 201):
        xmm = i / 10.0
        f = xmm + 0.035 * xmm ** 3
        px = ox + xmm / 20.0 * 480
        py = oy - (f / 220.0) * 200
        pts.append((px, py))
    d.line(pts, fill="#1565c0", width=4)
    # bump-stop-markering
    bx2 = ox + 15 / 20.0 * 480
    for yy in range(int(oy - 215), int(oy), 14):
        d.line([bx2, yy, bx2, yy + 7], fill="#c62828", width=3)
    txt(d, bx2 + 10, oy - 235, "bump-stop 15 mm", 13, bold=True, fill="#c62828")
    for xm in (0, 5, 10, 15, 20):
        px = ox + xm / 20.0 * 480
        d.line([px, oy, px, oy + 8], fill="#222", width=2)
        txt(d, px, oy + 22, str(xm), 13)

    txt(d, 140, 1580, "Alle fire er sliders i bil-ramme.scad: susp_travel, bump_stop, camber_angle, toe_angle", 15, fill="#555", anchor="lm")
    img.save(os.path.join(OUT, "pdf-p8.png"))

# ------------------------------------------------ P9 3D-print
def p9():
    img, d = page("3D-PRINTET CHASSIS - DELER OG PRINTINNSTILLINGER",
                  "PETG/ASA i chassis, PA-CF/ASA i armer, TPU 95A i dekk og bump-stop")

    parts = [
        ("Chassis (bunn + vegger + ribber)", "1", "PETG/ASA", "30 % gyroid", "flat pa bunn"),
        ("Batteritray", "1", "PETG", "25 %", "flat"),
        ("Baereearm", "4", "PA-CF/ASA", "40 %", "flat, hull opp"),
        ("Spindel / nav", "4", "PA-CF/ASA", "40 %", "flat"),
        ("Motorfeste (utrigger)", "4", "PETG/ASA", "40 %", "flat"),
        ("Servoholder", "1", "PETG", "25 %", "flat"),
        ("Gimbal: mast + 2 braketter", "3", "PETG", "25 %", "staaende"),
        ("Hjul: nav", "4", "PETG/ASA", "40 %", "flat"),
        ("Dekk", "4", "TPU 95A", "100 % vegger", "flat"),
        ("Bump-stop", "4", "TPU 95A", "100 %", "staaende"),
    ]
    y = 250
    cols = [("DEL", 140), ("ANT", 900), ("MATERIALE", 1000), ("INFILL", 1380), ("ORIENTERING", 1650)]
    for (t, x) in cols:
        d.text((x, y), t, font=f(20, True), fill="#111")
    d.line([120, y + 34, W - 120, y + 34], fill="#999", width=2)
    yy = y + 60
    for (a, b, c, e, g) in parts:
        d.text((140, yy), a, font=f(18), fill="#111")
        d.text((900, yy), b, font=f(18), fill="#111")
        d.text((1000, yy), c, font=f(18), fill="#111")
        d.text((1380, yy), e, font=f(18), fill="#111")
        d.text((1650, yy), g, font=f(18), fill="#111")
        yy += 52

    # printplate-skisse
    px, py, pw = 150, 900, 380
    d.text((px, py - 40), "PRINTPLATE 256 x 256 (Bambu A1)", font=f(20, True), fill="#111")
    d.rectangle([px, py, px + pw, py + pw], outline="#555", width=3)
    # ruter (deler)
    d.rectangle([px + 10, py + 10, px + 370, py + 170], outline="#0d47a1", width=2)
    d.text((px + 190, py + 90), "1: chassis", font=f(18), anchor="mm", fill="#0d47a1")
    d.rectangle([px + 10, py + 185, px + 180, py + 300], outline="#2e7d32", width=2)
    d.text((px + 95, py + 242), "2: batteritray", font=f(16), anchor="mm", fill="#2e7d32")
    d.rectangle([px + 190, py + 185, px + 370, py + 300], outline="#ef6c00", width=2)
    d.text((px + 280, py + 242), "3: arm x4", font=f(16), anchor="mm", fill="#ef6c00")
    d.rectangle([px + 10, py + 310, px + 180, py + 370], outline="#6a1b9a", width=2)
    d.text((px + 95, py + 340), "4: spindel x4", font=f(15), anchor="mm", fill="#6a1b9a")
    d.rectangle([px + 190, py + 310, px + 370, py + 370], outline="#c62828", width=2)
    d.text((px + 280, py + 340), "5: motorfeste x4", font=f(15), anchor="mm", fill="#c62828")

    # innstillinger
    sx2 = 700
    d.text((sx2, 900), "PRINTINNSTILLINGER (Bambu A1)", font=f(22, True), fill="#111")
    lines = [
        "PETG: 240 C dyse / 80 C seng - 0,2 mm lag - 4 vegger",
        "ASA/PA-CF: 260-280 C - lukket kabinett - 0,2 mm",
        "TPU 95A: 240 C - 25 mm/s - 0,2 mm - torket filament",
        "Chassis: 30 % gyroid, 5 topp/bunn-lag",
        "Armer/spindler: 40 % gyroid + 5 vegger (belastning)",
        "Ingen support: alle deler designet flate/staende",
        "M3 varmepress-inserts i alle gjengepunkter",
        "M4 pivot-skruer i baereearm + laasemutter",
        "Lager: 608ZZ i nav (valgfritt) eller bronsebushing",
    ]
    for i, s in enumerate(lines):
        d.text((sx2, 950 + i * 48), s, font=f(19), fill="#111")

    txt(d, 140, 1560, "Chassis printes i en del: bunnplate + sidevegger + ribber + motorbroer, uten support", 18, bold=True, fill="#0d47a1", anchor="lm")
    img.save(os.path.join(OUT, "pdf-p9.png"))

# ------------------------------------------------ P10 estimater/toleranser
def p10():
    img, d = page("PRINTESTIMATER OG TOLERANSER",
                  "Vekt/tid per del + anbefalte hullmaal for M3, M4, M6 og 608-lager")

    est = [
        ("Chassis", "PETG", "221", "3,9", "1", "221"),
        ("Batteritray", "PETG", "65", "1,1", "1", "65"),
        ("Baereearm", "PA-CF", "4", "0,1", "4", "18"),
        ("Spindel/nav", "PA-CF", "14", "0,4", "4", "56"),
        ("Motorfeste", "PETG", "11", "0,2", "4", "43"),
        ("Servoholder", "PETG", "8", "0,1", "1", "8"),
        ("Gimbal", "PETG", "14", "0,2", "1", "14"),
        ("Hjulnav", "PETG", "32", "0,6", "4", "128"),
        ("Dekk", "TPU 95A", "71", "4,9", "4", "285"),
        ("Bump-stop", "TPU 95A", "3", "0,2", "4", "11"),
    ]
    d.text((140, 240), "VEKT OG TID", font=f(22, True), fill="#111")
    heads = [("DEL", 140), ("MAT.", 520), ("G/STK", 720), ("T/STK", 830), ("ANT", 950), ("G TOTALT", 1040)]
    for (t, x) in heads:
        d.text((x, 290), t, font=f(18, True), fill="#111")
    d.line([120, 320, 1150, 320], fill="#999", width=2)
    y = 345
    for r in est:
        d.text((140, y), r[0], font=f(17), fill="#111")
        d.text((520, y), r[1], font=f(17), fill="#111")
        d.text((720, y), r[2], font=f(17), fill="#111")
        d.text((830, y), r[3], font=f(17), fill="#111")
        d.text((950, y), r[4], font=f(17), fill="#111")
        d.text((1040, y), r[5], font=f(17), fill="#111")
        y += 42
    d.line([120, y, 1150, y], fill="#999", width=2)
    d.text((140, y + 40), "TOTALT: ca. 850 g filament · ca. 31 timer print", font=f(20, True), fill="#0d47a1")
    d.text((140, y + 78), "Med svinn/feilprint: ~980 g og ~36 timer", font=f(17), fill="#555")

    # toleransetabell
    tx = 1250
    d.text((tx, 240), "TOLERANSER", font=f(22, True), fill="#111")
    rows = [
        ("M3 skrue", "3,0 + 0,20", "3,2", "3,05-3,15", "OK - evt. fit_clear 0,25"),
        ("M3 insert", "4,0 + 0,20", "4,2", "4,0-4,1", "Varmepress, test 4,0-4,4"),
        ("M4 pivot", "4,0 + 0,35", "4,35", "4,2-4,3", "Bevegelig + laasemutter"),
        ("M6 kingpin", "6,0 + 0,20", "6,2", "6,05-6,15", "OK"),
        ("608-lager", "22,0", "22,0", "21,9-22,0", "Presspasning, varm inn"),
    ]
    hh = [("NOMINAL", tx), ("MODELL", tx + 200), ("HULL", tx + 360), ("PRINTET", tx + 450), ("ANBEFALING", tx + 590)]
    for (t, x) in hh:
        d.text((x, 290), t, font=f(16, True), fill="#111")
    d.line([tx - 10, 320, W - 140, 320], fill="#999", width=2)
    yy = 345
    for r in rows:
        d.text((tx, yy), r[0], font=f(16), fill="#111")
        d.text((tx + 200, yy), r[1], font=f(16), fill="#111")
        d.text((tx + 360, yy), r[2], font=f(16), fill="#111")
        d.text((tx + 450, yy), r[3], font=f(16), fill="#111")
        d.text((tx + 590, yy), r[4], font=f(15), fill="#111")
        yy += 48

    # testplate-skisse
    px, py = 1250, 700
    d.text((px, py - 30), "TESTPLATE (print forst)", font=f(20, True), fill="#111")
    d.rectangle([px, py, px + 380, py + 300], outline="#555", width=2)
    for i in range(3):
        d.ellipse([px + 30 + i * 55, py + 40, px + 60 + i * 55, py + 70], outline="#0d47a1", width=2)
    d.text((px + 30, py + 95), "M3: 3,2/3,4/3,6", font=f(15), fill="#0d47a1")
    for i in range(3):
        d.ellipse([px + 230 + i * 45, py + 40, px + 260 + i * 45, py + 70], outline="#2e7d32", width=2)
    d.text((px + 230, py + 95), "insert: 4,0/4,2/4,4", font=f(15), fill="#2e7d32")
    for i in range(2):
        d.ellipse([px + 30 + i * 55, py + 130, px + 60 + i * 55, py + 160], outline="#ef6c00", width=2)
    d.text((px + 30, py + 185), "M4: 4,2/4,4", font=f(15), fill="#ef6c00")
    for i in range(2):
        d.ellipse([px + 200 + i * 55, py + 130, px + 230 + i * 55, py + 160], outline="#6a1b9a", width=2)
    d.text((px + 200, py + 185), "M6: 6,0/6,2", font=f(15), fill="#6a1b9a")
    for i in range(3):
        d.ellipse([px + 30 + i * 70, py + 220, px + 75 + i * 70, py + 265], outline="#c62828", width=2)
    d.text((px + 30, py + 290), "608: 22,0/22,1/22,2", font=f(15), fill="#c62828")

    txt(d, 140, 1560, "Print testplaten først, mål med skyvelaere, juster fit_clear/insert_clear/pivot_clear i bil-print.scad",
        17, bold=True, fill="#0d47a1", anchor="lm")
    img.save(os.path.join(OUT, "pdf-p10.png"))

if __name__ == "__main__":
    p1(); p2(); p3(); p4(); p5(); p6(); p7(); p8(); p9(); p10()
    pages = [Image.open(os.path.join(OUT, f"pdf-p{i}.png")).convert("RGB") for i in range(1, 11)]
    pdf = os.path.join(OUT, "..", "pdf", "bil-tegninger.pdf")
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=200.0)
    print("Skrev", pdf)
