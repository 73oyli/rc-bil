"""Erstatter p4-funksjonen i draw-pdf.py med en ryddigere frontvisning."""
import io, os, re

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "draw-pdf.py")
src = io.open(p, encoding="utf-8").read()

new = '''# ------------------------------------------------ P4 hjuloppheng
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

'''

start = src.index("# ------------------------------------------------ P4 hjuloppheng")
end = src.index("# ------------------------------------------------ P5 gimbal")
src = src[:start] + new + src[end:]
io.open(p, "w", encoding="utf-8").write(src)
print("p4 erstattet")
