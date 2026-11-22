# Byggeplan: RC-bil med FPV (fra bunnen)

Utstyr du allerede har/planlegger: **RadioMaster TX16S MK3 Gemini** (ELRS dual-band), **ER16 PWM-mottaker** (Gemini-X, LBT), evt. **AKK Alpha 25 VTX** (bruk kun 25 mW).

---

## 1. Velg plattform (først av alt)

| Type | Eksempel på kit | Bruk | Ca. pris (NOK) |
|---|---|---|---|
| **Onroad/drift 1/10** | Tamiya TT-02 (kit) | Asfalt, parkeringsplass, FPV-racestil | 1 200–1 600 |
| **Buggy/truggy 1/10** | Tamiya DT-03, LC Racing EMB-1 | Grus, gress, hopp | 1 500–2 500 |
| **Crawler 1/10** | Axial SCX10 III, Traxxas TRX-4 Sport | Terreng, klatre, langsom FPV | 3 000–5 000 |

**Anbefaling for FPV-bil:** start med **1/10 onroad eller buggy** – enkelt, billig, lett å montere kamera, og 25 mW video rekker langt nok.

---

## 2. Elektronikk (drift)

| Del | Krav | Eksempel | Ca. pris |
|---|---|---|---|
| **ESC + motor** | Børsteløs combo, sensored for myk start | Hobbywing QuicRun 10BL120 + 3650-motor | 700–1 000 |
| **Styreservo** | ≥ 10 kg·cm, metallgir | DS3218 / Savox 0231 | 250–400 |
| **Batteri** | 2S eller 3S LiPo (avhengig av ESC) | 2S 5000 mAh 50C | 300–450 |
| **Lader** | LiPo-balanselader | ISDT Q6 / tilsvarende | 400–700 |

> 💡 Hold deg til **2S/3S** – da kan du bruke 5 V VTX/BEC. AKK Alpha 25 (20–35 V) passer ikke uten 6S.

---

## 3. Styring (radio + mottaker)

- **TX16S MK3 Gemini** (ELRS, LBT) → bindes med samme **binding phrase** som ER16
- **ER16 PWM** kobles slik:

| ER16-kanal | Til |
|---|---|
| CH1 | Styreservo |
| CH2 | ESC (gass) |
| CH3 | Lys / horn / vinsj |
| CH4–16 | Ekstra (kamera-pan, diff, vinsj) |

- **Failsafe**: sett i ELRS (throttle → nøytral/0, styring → rett fram)
- **Rates/Expo**: start konservativt (60–70 %)
- **Timer**: 5–8 min på radioen

---

## 4. FPV-video (lovlig!)

| Del | Krav | Eksempel | Ca. pris |
|---|---|---|---|
| **Kamera** | 5 V, 1200TVL analog (eller digital) | RunCam Phoenix 2 / Foxeer Razer | 300–500 |
| **VTX** | **25 mW** (lovlig i Norge), 5 V | Eachine TX805 (25/200/600, bruk 25) | 250–400 |
| **Antenne VTX** | Liten cloverleaf/linear | – | 100–200 |
| **Briller/mottaker** | 5,8 GHz, diversity | Eachine EV800D | 1 200–1 500 |

⚠️ **Lovlig grense i Norge: 25 mW e.i.r.p.** (5725–5875 MHz). AKK Alpha 25 kan brukes, men **bare på 25 mW-innstillingen** – og den krever 20–35 V (6S), så den passer dårlig i en 2S/3S-bil.

💡 Vil du ha digital video: DJI O3/Walksnail i **CE-modus** = også 25 mW.

---

## 5. Strøm og BEC

- **ESC-BEC** gir 5–6 V til servo + ER16 (sjekk at BEC ≥ 5 A hvis servo er sterk)
- **VTX + kamera** på egen **5 V BEC** (unngå støy fra motoren)
- **Filtrering**: ferrittring på videokabel + kondensator over batteri (fjerner «rulleslør» i bildet)
- **Antenneplassering**: oppå bilen, borte fra motor/ESC og karbon

---

## 6. Byggesteg

1. [ ] Bygg chassis etter manualen (differensial, dempere, stag)
2. [ ] Monter motor + ESC, kalibrer ESC til radioen (gass-endepunkter)
3. [ ] Monter servo + styrestag, sett midtpunkt
4. [ ] Koble ER16: CH1 servo, CH2 ESC → bind til radioen → test kanalretninger
5. [ ] Monter kamera + VTX, 5 V BEC, antenne oppå bilen
6. [ ] Test video på benken (25 mW, aldri uten antenne!)
7. [ ] Failsafe-test: skru av radioen → bilen skal stoppe
8. [ ] Range test (gå 100–200 m) før første ordentlige kjøring
9. [ ] Værbeskyttelse: tape/conformal coating på ESC/mottaker, vanntett kamerahus

---

## 7. Lovlighet og sikkerhet

- ✅ **Video: 25 mW** i 5725–5875 MHz (fribruksforskriften / EN 300 440)
- ✅ **Styring: ELRS 868 MHz / 2,4 GHz** (EU868, LBT)
- ❌ Ikke kjør på offentlig vei; hold deg til privat område/park med tillatelse
- ❌ Ikke fly/kjør nær folk, flyplasser eller annen radio
- 🔋 LiPo: bruk balanselader, oppbevar i LiPo-pose, ikke lad uten tilsyn

---

## 8. Omtrentlig totalbudsjett

| Post | NOK |
|---|---|
| Chassis-kit | 1 200–2 500 |
| ESC + motor | 700–1 000 |
| Servo | 250–400 |
| Batteri + lader | 700–1 100 |
| ER16-mottaker | 500 |
| Kamera + VTX + antenne | 650–1 100 |
| Briller | 1 200–1 500 |
| Småtteri (ledninger, BEC, tape) | 300–500 |
| **Totalt** | **~5 500–8 500** |

Vil du holde det billig: analog 25 mW, brukt chassis, og en enkel EV800-brille.

---

## 9. Spørsmål som styrer valgene

1. **Terreng**: asfalt/parkering, grus/gress, eller klatreterreng?
2. **Budsjett**: ~3 000, ~6 000 eller ~10 000 NOK?
3. **Video**: analog (billig, enkelt) eller digital (bedre bilde, dyrere)?
4. **Hastighet**: crawler (rolig) eller rask buggy?

Svar på disse, så spisser jeg handlelisten til én konkret bil.
