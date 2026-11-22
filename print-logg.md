# Printlogg og 2-ukers printplan – RC-bil (Bambu Lab A1)

Ferdig utfylt plan med datoer. Fyll inn **Resultat** og **Merknad** etter hvert som du printer.
Planen forutsetter at testplaten printes først og at toleransene justeres før de store delene.

## Printer og profil

| | |
|---|---|
| Printer | Bambu Lab A1 (256×256×256) |
| Dyse | 0,4 mm |
| Laghøyde | 0,2 mm (0,16 for detaljer) |
| Vegger | 4 (chassis), 5 (armer/spindler) |
| Infill | 30 % gyroid (chassis), 40 % (belastede deler) |
| Materialer | PETG, ASA/PA-CF, TPU 95A |

## Printplan – uke 1 (23.–29. november 2026)

| Dato | Dag | Del | Materiale | Planlagt vekt | Planlagt tid | Resultat |
|---|---|---|---|---:|---:|---|
| 23.11 | man | **Testplate (toleranse)** | PETG | 20 g | 0,5 t | ☐ |
| 23.11 | man kveld | **Chassis** (bunn + vegger + ribber) | PETG | 221 g | 3,9 t | ☐ |
| 24.11 | tir | Batteritray | PETG | 65 g | 1,1 t | ☐ |
| 24.11 | tir kveld | Bærearm ×4 | PA-CF | 18 g | 0,4 t | ☐ |
| 25.11 | ons | Spindel/nav ×4 | PA-CF | 56 g | 1,5 t | ☐ |
| 25.11 | ons kveld | Motorfeste ×4 | PETG | 43 g | 0,8 t | ☐ |
| 26.11 | tor | Servoholder + gimbal | PETG | 22 g | 0,3 t | ☐ |
| 26.11 | tor kveld | Hjulnav ×4 | PETG | 128 g | 2,4 t | ☐ |
| 27.11 | fre | Dekk 1–2 (TPU, natt) | TPU 95A | 142 g | 9,8 t | ☐ |
| 28.11 | lør | Dekk 3–4 (TPU, natt) | TPU 95A | 142 g | 9,8 t | ☐ |
| 29.11 | søn | Bump-stop ×4 + kontroll | TPU 95A | 11 g | 0,8 t | ☐ |

**Sum uke 1:** ~848 g filament, ~31 t print (fordelt på 9 dager).

## Printplan – uke 2 (30. november – 6. desember 2026)

| Dato | Dag | Aktivitet | Merknad |
|---|---|---|---|
| 30.11 | man | Montering: chassis + bærearm + spindler | Sjekk at pivotene går fritt |
| 01.12 | tir | Motorer + ESC + FC | Kalibrer ESC én om gangen |
| 02.12 | ons | Styring: servo + styrestag + gimbal | Ackermann 30°/22° |
| 03.12 | tor | Kabling + batteri + BEC | Felles jord, fjern +5V fra 3 ESC |
| 04.12 | fre | ArduPilot Rover + kalibrering | `FRAME_CLASS=1`, `MOT_THR_MAX=60` |
| 05.12 | lør | FPV-test + range-test | 25 mW video, ELRS-binding |
| 06.12 | søn | Første kjøretur + justering | Logg resultat i tabellen under |

## Logg – faktisk resultat

| Dato | Del | Materiale | Faktisk vekt (g) | Faktisk tid (t) | Resultat | Merknad/justering |
|---|---|---|---:|---:|---|---|
| 23.11 | Testplate | PETG | | | | |
| 23.11 | Chassis | PETG | | | | |
| 24.11 | Batteritray | PETG | | | | |
| 24.11 | Bærearm ×4 | PA-CF | | | | |
| 25.11 | Spindel ×4 | PA-CF | | | | |
| 25.11 | Motorfeste ×4 | PETG | | | | |
| 26.11 | Servoholder + gimbal | PETG | | | | |
| 26.11 | Hjulnav ×4 | PETG | | | | |
| 27.11 | Dekk 1–2 | TPU 95A | | | | |
| 28.11 | Dekk 3–4 | TPU 95A | | | | |
| 29.11 | Bump-stop ×4 | TPU 95A | | | | |

**Resultat-koder:** ✅ OK · ⚠️ OK med justering · ❌ feilprint

## Feil og justeringer

| Dato | Problem | Tiltak | Ny verdi |
|---|---|---|---|
| | | | |
| | | | |

## Målinger fra toleranse-testplaten (23.11)

| Hull | Nominell | Målt | Vurdering |
|---|---:|---:|---|
| M3 skrue | 3,2 | | |
| M3 insert | 4,0 / 4,2 / 4,4 | | |
| M4 pivot | 4,2 / 4,4 | | |
| M6 kingpin | 6,0 / 6,2 | | |
| 608-lager | 22,0 / 22,1 / 22,2 | | |

Oppdater deretter i `scad/bil-print.scad`:

```scad
fit_clear    = 0.20;   // M3-skruer
insert_clear = 0.20;   // varmepress-insert
pivot_clear  = 0.35;   // M4 pivot
```

## Milepæler

- [ ] Testplate printet og målt (23.11)
- [ ] Chassis ferdig (23.11)
- [ ] Alle mekaniske deler printet (29.11)
- [ ] Rullende chassis montert (30.11)
- [ ] Elektronikk montert og testet (04.12)
- [ ] FPV + range test OK (05.12)
- [ ] Første kjøretur (06.12)
- [ ] Bilder lagt i `bilder-bygg/`

## Bilder

Legg bilder i `bilder-bygg/` med dato-prefiks, f.eks. `2026-11-23_chassis-ferdig.jpg`.
