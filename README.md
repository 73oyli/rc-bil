# RC-bil – 4WD FPV-prosjekt

Alt for RC-bilen, sortert etter filtype.

| Mappe | Innhold |
|---|---|
| `scad/` | CAD-modeller (OpenSCAD): `bil-print.scad` (printbart chassis), `bil-ramme.scad` (alu-referanse), `toleranse-test.scad` |
| `pdf/` | `bil-tegninger.pdf` – 10 siders tegningspakke med mål, koblingsskjema, printestimater og toleranser |
| `png/` | Rendringer og skisser (topp/side/kobling, SCAD-frames, PDF-sider, testplate) |
| `gif/` | Animasjoner: styring, fjæring, kombinert, alle bevegelser |
| `stl/` | Klar-til-print STL for alle deler (chassis, arm, spindel, nav, dekk, gimbal …) |
| `zip/` | `stl-deler.zip` – alle STL-filer samlet |
| `param/` | ArduPilot Rover-parametere (`ardupilot-rover-ackermann.param`, `…-skid.param`) |
| `python/` | Skript som genererer tegninger, PDF og printestimater |
| `notater/` | Byggeplaner, detaljplan og printestimater (Markdown) |
| `bilder-bygg/` | Bilder/video av ferdig bygg (navngiving: `ÅÅÅÅ-MM-DD_beskrivelse.jpg`) |
| `print-logg.md` | Logg per print: dato, del, materiale, vekt, tid, resultat + toleransemålinger |

## Slik bruker du det

```powershell
# Regenerer PDF + sider (skriver til ../pdf og ../png)
python "rc bil/python/draw-pdf.py"

# Regenerer tekniske skisser
python "rc bil/python/draw-car.py"

# Eksporter STL + regn ut vekt/tid (skriver til ../stl og ../notater)
python "rc bil/python/stl-estimater.py"
```

## Status

- ✅ Chassis, hjuloppheng, styring (Ackermann), camber/toe, bump-stop
- ✅ Fullt 3D-printbart design (PETG/ASA/PA-CF/TPU), kun skruer/lager i metall
- ✅ Printestimater: ~850 g filament, ~31 t
- ✅ Toleransetabell + testplate for M3/M4/M6/insert/608
- ✅ `print-logg.md` for å logge hvert print og toleransemålinger
- ✅ `bilder-bygg/` for bilder og video under bygging
- 🔜 Neste: print testplaten, mål, juster `fit_clear`/`insert_clear`/`pivot_clear`, eksporter 3MF
