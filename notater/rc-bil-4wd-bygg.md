# Prosjekt: 4WD FPV-bil med 4250 800KV + H743 + 4× Skywalker 80A

**Deler du har:** 4× 4250 800KV outrunner, DakeFPV H743 FC, 4× Hobbywing Skywalker V2 80A (2–6S, bidirectional).
**Plan:** 3D-printede hjul i TPU 75 som limes rett på motorklokkene (direct drive, ingen gir).

---

## 1. Realitetsberegning: hvor fort går det?

Formel: **fart = (KV × spenning / 60) × π × hjuldiameter** (teoretisk, ubelastet)

| Hjul | 2S (7,4 V) | 3S (11,1 V) | 4S (14,8 V) | 6S (22,2 V) |
|---|---|---|---|---|
| 80 mm | ~75 km/h | ~113 km/h | ~150 km/h | ~225 km/h |
| **100 mm** | **~94 km/h** | ~141 km/h | ~188 km/h | ~283 km/h |
| 120 mm | ~113 km/h | ~169 km/h | ~225 km/h | ~339 km/h |

*(Med belastning ca. 85 % av dette. 800KV på 6S gir ~17 800 rpm – det er dronehastigheter, ikke bilhastigheter.)*

**Anbefaling:** **2S + 80–100 mm hjul** gir 60–90 km/h – mer enn nok, og holder strøm/ESC/varme håndterbart. **Ikke** kjør 6S direkte på hjulene.

**Effekt:** 4250-motorene tåler ~800–1200 W hver på 6S. Fire stk = **3–5 kW** – det er mer enn en elbil trenger. Begrens med:
- lavere spenning (2S/3S)
- throttle-limit i FC/radio (50–60 %)
- myk start (ramp)

---

## 2. Styring: skid steer (differensial)

Bilen svinger ved å gi **venstre/høyre hjulpar ulik hastighet** – ikke servostyring.

### Firmware-valg

| Alternativ | Passer? | Merknad |
|---|---|---|
| **ArduPilot Rover** | ✅ best | Støtter skid steer, waypoints, telemetri, failsafe. **Sjekk at `DAKEFPVH743`-hwdef finnes** – ellers må boardet legges til |
| Betaflight | 🟡 mulig | «Quad»-mikser: yaw = differensial, pitch = gass. Fungerer for lek, men ikke laget for biler |
| iNav | ❌ | ingen rover-modus |

**Anbefalt:** **ArduPilot Rover** hvis H743-boardet støttes (undersøk hwdef først). Da får du:
- `FRAME_CLASS = 2` (skid steer)
- venstre/høyre motorpar på to servo-utganger → Y-kabler til 2+2 ESC
- failsafe, geofence, batteriovervåking, logging

### Kobling (ArduPilot / skid steer)
```
FC SERVO1 → ESC venstre (2 ESC via Y-kabel)
FC SERVO2 → ESC høyre (2 ESC via Y-kabel)
FC UART  → ELRS-mottaker (CRSF)
FC UART  → GPS (valgfritt)
FC 5V    → mottaker
```
- **Alle 4 ESC må ha samme innstillinger** (reverse, timing, cutoff)
- **Bidirectional**: Skywalker V2 80A «bidirectional» støtter framover/bakover – bekreft at den er i **car/boat-modus** (ikke fly-modus med brems)
- **Kalibrer** hver ESC mot FC-utgangen (høy gass ved oppstart)

---

## 3. Hjul: TPU 75 direkte på outrunner – de tre fallgruvene

1. **Sluring/lim** – TPU + CA/epoxy på aluminiumsklokke holder dårlig ved dreiemoment. Motoren blir også varm (50–70 °C), som svekker limet.
   → **Bedre:** print et **nav med M3-bolter** som skrus i motorens propellfester, og en **TPU-ring som dekk** utenpå. Mekanisk feste slår lim.
2. **TPU 75A er for mykt som dekk** – det deformeres ved fart og slites raskt. Bruk **TPU 95A** til slitebane, evt. 75A kun som indre demping.
3. **Balanse** – print hjulene med 3–4 perimetre, 40–60 % infill (gyroid), og sjekk kast. Ubalanse ved 5000+ rpm river lagrene.

**Anbefalt hjuldesign:**
- Nav: PETG/ASA, bolts til motorklokk (M3), sentrert
- Slitebane: TPU 95A, 3–4 mm, printet som ring
- Diameter: **80–100 mm** for 2S

---

## 4. Strøm og varme

| Post | Krav |
|---|---|
| Batteri | 2S–3S, 5000–8000 mAh, ≥ 60C |
| ESC-kjøling | 4× 80A blir varme – monter med luftstrøm, ikke innelukket |
| Ledninger | 12–14 AWG til batteri, 14 AWG til motor |
| Sikring | **Hovedbryter + sikring** (f.eks. 100 A) – 4 motorer kan gi stor kortslutningsstrøm |
| BEC | FC + mottaker fra egen 5V BEC (ikke fra ESC-BEC) |

---

## 5. FPV

- Kamera 5 V + VTX **25 mW** (lovlig) – egen 5 V BEC
- Antenne oppå, borte fra motorledninger
- Briller: 5,8 GHz diversity

---

## 6. Byggerekkefølge

1. [ ] Monter 4 motorer på chassis (utrunnerklokker utover)
2. [ ] Print + monter hjul (nav først, dekk etterpå) – test kast/balanse på benk
3. [ ] Monter 4 ESC, kalibrer hver for seg
4. [ ] FC + firmware (ArduPilot Rover hvis støttet, ellers Betaflight-mikser)
5. [ ] ELRS-mottaker (CRSF), bind til TX16S
6. [ ] Skid steer-konfig + motorretning (venstre/høyre par)
7. [ ] Failsafe + arm-bryter + throttle-limit (50 %)
8. [ ] Benk-test: hjul i luften, sjekk retning, strøm, temperatur
9. [ ] Lavhastighets-test ute, deretter range test
10. [ ] FPV-kamera/VTX + test

---

## 7. Sikkerhet (viktig med 4× outrunner)

- ⚠️ **Aldri** test med hjul på bakken og full gass – fest bilen eller løft den
- ⚠️ Hjul i TPU kan **eksplodere** ved høy rpm – hold avstand ved første test
- ⚠️ 4250-motorer har **mye dreiemoment** – fingre unna
- ⚠️ Bruk **arm-bryter** og **failsafe** (throttle → 0)
- ⚠️ Hovedbryter/sikring før første kjøring

---

## 8. Neste steg – hva jeg trenger å vite

1. **Chassis**: bygger du ramme selv (aluminium/karbon) eller bruker du et kit?
2. **Hjuldiameter** du ser for deg (80/100/120 mm)?
3. **Firmware**: vil du prøve ArduPilot Rover (anbefalt) eller Betaflight-mikser?
4. **Spenning**: 2S eller 3S?
5. Har du **3D-printer** med TPU-erfaring (og hvilken printer)?

Svar, så lager jeg **konkret koblingsskjema + ArduPilot-parametere + hjul-STL-plan**.
