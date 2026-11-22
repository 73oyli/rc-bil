"""Eksporterer STL for hver del og beregner volum, vekt og printtid (realistisk).
Kjor: python stl-estimater.py
"""
import os, struct, subprocess, io

HERE = os.path.dirname(os.path.abspath(__file__))
SCAD = os.environ.get("OPENSCAD_BIN") or ("C:/Program Files/OpenSCAD/openscad.exe" if os.name == "nt" else "openscad")
STL = os.path.join(HERE, "..", "stl")
os.makedirs(STL, exist_ok=True)

# view, navn, materiale, tetthet g/cm3, solid-faktor (andel av solid volum som ekstruderes),
# gjennomstromning cm3/h (praktisk snitt inkl. travel/akselerasjon)
PARTS = [
    ("chassis", "chassis", "PETG",   1.27, 0.42, 45),
    ("tray",    "tray",    "PETG",   1.27, 0.45, 45),
    ("arm",     "arm",     "PA-CF",  1.12, 0.55, 35),
    ("knuckle", "knuckle", "PA-CF",  1.12, 0.55, 35),
    ("mount",   "mount",   "PETG",   1.27, 0.50, 45),
    ("servo",   "servo",   "PETG",   1.27, 0.45, 45),
    ("gimbal",  "gimbal",  "PETG",   1.27, 0.45, 45),
    ("hub",     "hub",     "PETG",   1.27, 0.50, 45),
    ("tire",    "tire",    "TPU95A", 1.21, 0.90, 12),
    ("bump",    "bump",    "TPU95A", 1.21, 1.00, 12),
]

def export(view, name):
    out = os.path.join(STL, name + ".stl")
    subprocess.run([SCAD, "-o", out, "--export-format", "binstl",
                    "-D", f'view="{view}"', os.path.join(HERE, "..", "scad", "bil-print.scad")],
                   check=True, capture_output=True)
    return out

def stl_volume(path):
    with open(path, "rb") as f:
        data = f.read()
    n = struct.unpack("<I", data[80:84])[0]
    vol = 0.0
    off = 84
    for _ in range(n):
        vals = struct.unpack("<12fH", data[off:off + 50])
        off += 50
        ax, ay, az, bx, by, bz, cx, cy, cz = vals[3:12]
        vol += (ax * (by * cz - bz * cy) - ay * (bx * cz - bz * cx) + az * (bx * cy - by * cx)) / 6.0
    return abs(vol) / 1000.0

def main():
    rows = []
    for (view, name, mat, dens, solid, rate) in PARTS:
        path = export(view, name)
        v = stl_volume(path)
        vp = v * solid
        w = vp * dens
        t = vp / rate
        rows.append((name, mat, v, vp, w, t))
        print(f"{name:8s} {mat:7s} solid {v:7.1f} cm3  printet {vp:7.1f} cm3  {w:6.1f} g  {t:5.2f} h")

    counts = {"chassis":1, "tray":1, "arm":4, "knuckle":4, "mount":4,
              "servo":1, "gimbal":1, "hub":4, "tire":4, "bump":4}
    tot_w = sum(r[4] * counts[r[0]] for r in rows)
    tot_t = sum(r[5] * counts[r[0]] for r in rows)
    print(f"\nTOTAL: {tot_w:.0f} g filament, {tot_t:.1f} t printtid for hele bilen")

    md = ["# Printestimater – 4WD FPV-bil (3D-printet chassis)", "",
          "Volum beregnet fra STL. «Printet volum» = solid volum × solid-faktor "
          "(vegger + infill). Vekt = printet volum × tetthet. Tid = printet volum / gjennomstrømning.", "",
          "| Del | Materiale | Solid (cm3) | Printet (cm3) | Vekt/stk (g) | Tid/stk (h) | Antall | Vekt totalt (g) |",
          "|---|---|---:|---:|---:|---:|---:|---:|"]
    for (name, mat, v, vp, w, t) in rows:
        n = counts[name]
        md.append(f"| {name} | {mat} | {v:.1f} | {vp:.1f} | {w:.1f} | {t:.2f} | {n} | {w*n:.0f} |")
    md += ["", f"**Totalt: ca. {tot_w:.0f} g filament og {tot_t:.1f} timers print** for hele bilen.",
           f"Med svinn/feilprint: ~{tot_w*1.15:.0f} g og ~{tot_t*1.15:.1f} t.", ""]
    with io.open(os.path.join(HERE, "..", "notater", "print-estimater.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print("Skrev notater/print-estimater.md")

if __name__ == "__main__":
    main()
