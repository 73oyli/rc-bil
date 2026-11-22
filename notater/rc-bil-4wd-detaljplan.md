# 4WD FPV-bil – detaljplan (egen ramme, 6S begrenset, ArduPilot Rover)

**Deler:** 4× 4250 800KV, DakeFPV H743 (ArduPilot `DAKEFPVH743` ✅), 4× Hobbywing Skywalker V2 80A (2–6S, bidirectional), 3D-printede 100 mm viftehjul (Bambu Lab A1, TPU-erfaring).

---

## 1. Firmware: ArduPilot Rover

Boardet er støttet: last ned **Rover**-firmware for `DAKEFPVH743` (sub-mappe «DAKEFPVH743»).

**Første flash:** hold bootloader-knappen inne mens du plugger USB → DFU → flash `..._with_bl.hex` → deretter vanlige oppdateringer via Mission Planner.

Etter flash:
- **Mission Planner** → velg `Rover`-frame
- **Config → Frame: Skid Steer** (`FRAME_CLASS = 2`)

---

## 2. Koblingsskjema

```
          ┌───────────── 6S LiPo (22.2V) ─────────────┐
          │  [Hovedbryter]  [Sikring 100A]             │
          │                                            │
      ┌───┴───┐        ┌──────────┐       ┌──────────┐ │
      │ESC V1 ├──motor─│ 4250 #1  │       │ 4250 #3  │─┤
      │ 80A   │        └──────────┘       └──────────┘ │
      │ (venstre)                        ┌──────────┐  │
      │ESC V2 ├──motor─│ 4250 #2  │       │ 4250 #4  │──┤
      │ 80A   │        └──────────┘       └──────────┘ │
      └───┬───┘                                        │
          │  Y-kabel (signal+signal, GND)   ┌──────────┐│
          │                                │ESC H1/H2 ││
          └──► FC SERVO1 (ThrottleLeft)    │ (høyre)  ││
                                           └───┬──────┘│
      ┌──────────────┐                          │       │
      │ FC SERVO2    │◄─────────────────────────┘       │
      │ (ThrottleRight)                                 │
      └──────┬───────┘                                  │
             │ 5V BEC (ekstern, 5A)                     │
             ├──► FC, ELRS-mottaker                      │
             └──► kamera + VTX 25mW (egen 5V BEC)        │
                                                       │
      FC UART ──► ELRS RX (CRSF)
      FC UART ──► GPS (valgfritt)
```

**Viktig:**
- **Fjern +5V (rød ledning)** fra 3 av 4 ESC-signalkabler – ellers kjemper fire BEC-er mot hverandre. Behold én (eller bruk ekstern 5V BEC).
- **Felles jord** mellom alle ESC-er, FC og mottaker.
- **Y-kabel** fra SERVO1 til venstre ESC-par, SERVO2 til høyre par.
- **Sikring + hovedbryter** på batteriets plusside.
- **Pre-charge-motstand** (10Ω) anbefales for å unngå gnist ved 6S.

---

## 3. ArduPilot-parametere (startpunkt)

| Parameter | Verdi | Betydning |
|---|---|---|
| `FRAME_CLASS` | 2 | Skid steer |
| `MOT_PWM_TYPE` | 0 | Normal PWM (Skywalker) |
| `SERVO1_FUNCTION` | 73 | ThrottleLeft |
| `SERVO2_FUNCTION` | 74 | ThrottleRight |
| `SERVO3_FUNCTION` | 0 | Deaktivert |
| **`MOT_THR_MAX`** | **60** | **6S-begrensning (60 %)** |
| `MOT_SLEW_UP` | 0.5 | Myk akselerasjon (sek) |
| `MOT_SLEW_DN` | 0.5 | Myk nedbremsing |
| `CRUISE_SPEED` | 3 m/s | Marsjfart |
| `CRUISE_THROTTLE` | 30 | % ved marsj |
| `BRD_SAFETY_DEFLT` | 0 | Ingen sikkerhetsbryter |
| `FS_THR_ENABLE` | 1 | Failsafe på RC-tap |
| `FS_ACTION` | 2 | Stopp ved failsafe |
| `FS_TIMEOUT` | 1.5 s | Tid før failsafe |
| `BATT_MONITOR` | 4 | Spenningsmåling |
| `BATT_CAPACITY` | 6000 | mAh (tilpass) |
| `ARMING_CHECK` | 1 | Alle sjekker |

📄 Ferdig fil: **`ardupilot-rover-skid.param`** (samme mappe) – last inn i Mission Planner → Config → Full Parameter List → Load.

**I tillegg i radioen (TX16S):** begrens gasskanal til **±60 %** som ekstra sikkerhet (Outputs → max/min).

---

## 4. Egen ramme – forslag

| Element | Anbefaling |
|---|---|
| Materiale | 4–5 mm karbon eller 6061 aluminium (to plater: bunn + topp) |
| Akselavstand | **220–260 mm** (100 mm hjul) |
| Sporvidde | 190–210 mm (mellom hjulsentre) |
| Vektmål | 2,5–3,5 kg inkl. batteri |
| Tyngdepunkt | Lavt, 50/50 foran/bak (skid steer) |
| Motorfester | Print i PETG/ASA eller freset alu, 4250-festemønster (25/19 mm) |
| Batteri | Festes sentrert/lavt, stropp + sklisikring |
| ESC-plass | Ut i luftstrømmen, ikke innelukket |
| Kamera | Front, 10–15° ned |
| VTX-antenne | Oppå, vertikalt, borte fra motorledninger |
| Dekning | Tape/conformal coating på FC, ESC-signal, mottaker |

---

## 5. 100 mm viftehjul (Bambu Lab A1)

**Design:**
- **Nav:** PETG/ASA, boltes til motorklokk (M3) – *ikke* lim
- **Vifteblader:** radiale/lette skrå blader som blåser luft over motoren
- **Slitebane:** TPU 95A (75A blir for mykt ved 10 000+ rpm)
- **Bredde:** 30–35 mm for grep
- **Balansering:** print parvis, sjekk kast på motorakselen, bruk «balance weights» i navet om nødvendig

**Print (Bambu A1, TPU):**
- 0,4 mm dyse, 30–40 mm/s, 240–250 °C
- 3 vegger, 20–30 % gyroid
- Tørk TPU (60 °C, 6–8 t) før print – fukt gir dårlig lagheft
- Nav i PETG/ASA: 0,2 mm lag, 4 vegger, 40 %

⚠️ **Vifteblader i TPU kan «ballongere» ved høy rpm** – test først ved 30 % gass på bukk, øk gradvis. Vurder blader i PETG/ASA og TPU kun som slitebane.

---

## 6. 6S-begrensning – tre lag

1. **ArduPilot:** `MOT_THR_MAX = 60`
2. **Radio:** gasskanal begrenset til 60 % (Outputs)
3. **ESC:** programmer myk start og strømbegrensning (Skywalker-meny)

**Forventet toppfart** ved 100 mm hjul og 60 % av 6S: ~**170 km/h teoretisk** – fortsatt mye! Begrens hardere (40 %) i første test, eller bruk 3S.

---

## 7. Testplan

1. [ ] Hjul av, motorer i luften: sjekk retning på alle fire (venstre par = framover)
2. [ ] Kalibrer ESC-er (høy gass ved oppstart) – én om gangen
3. [ ] ArduPilot: motor-test fra Mission Planner (Servo/Relay)
4. [ ] Hjul på, på bukk: 20 % → 40 % gass, sjekk varme/lyd/vibrasjon
5. [ ] Første kjøring: lav hastighet, 2–3 min, sjekk temperatur på ESC/motor
6. [ ] Failsafe-test: skru av radio → bilen stopper
7. [ ] Range test uten FPV, deretter med
8. [ ] FPV + opptak av første tur

---

## 7b. Sensorløse motorer – hva det betyr for oppstart

**Kort svar: ja, det kan gi problemer – men det er håndterbart.** 4250 800KV er **sensorløse** outrunnere, og Skywalker 80A er en **sensorløs** ESC.

**Hva som skjer:** sensorløs ESC må «gjette» rotorposisjonen fra motspenningen. Ved **null/lav fart** er signalet svakt:
- motoren kan **hakke/cogge** i stedet for å starte jevnt
- ved **retningsbytte** (som skid steer gjør hele tiden) kan den miste synkronisering
- store/tunge hjul (100 mm, 4WD) gjør starten tyngre
- **bidirectional**-modus er verst: revers fra stillstand er vanskeligst

**ArduPilot Rover + skid steer** kommanderer ofte lave hastigheter og raske retningsbytter → dette er den vanskeligste bruken for sensorløse ESCs.

### Tiltak (i rekkefølge)

1. **Programmer ESC-ene riktig:** myk start, høy timing, og «car/boat»-modus (ikke fly)
2. **Aldri kommando under ~15–20 %:** sett `MOT_THR_MIN` slik at hjulene alltid har litt dreiemoment – unngå «krypkjøring» nær null
3. **Myk slew:** `MOT_SLEW_UP/DN = 0.5–1.0` (vi har 0.5)
4. **Unngå hyppige retningsbytter:** bruk større svingradius i starten (`TURN_RADIUS`), kjør «rullende» svinger
5. **Test på bukk først:** 20 % → 40 % → 60 %, se etter hakking

### Hvis det fortsatt hakker – tre veier videre

| Løsning | Kostnad | Merknad |
|---|---|---|
| **Bytte til bil-ESC med bedre sensorløs start** (Hobbywing QuicRun 10BL120 sensored) | €40–60/stk | Sensorløs, men car-firmware med «kick start» |
| **Sensored motor + sensored ESC** | €100–150/aksel | Beste lavhastighetskontroll – men nye motorer |
| **VESC (Flipsky 6.6) med FOC** | €60–100/stk | FOC gir mye jevnere start; kan også bruke magnetisk encoder (AS5047) |
| **Hallsensor-kit til 4250** | €15–25/stk | Krever sensored ESC – Skywalker støtter det ikke |

**Anbefaling:** prøv de 4 tiltakene først (gratis). Hakker det fortsatt, gå til **VESC med FOC** – det er den beste kombinasjonen for tung 4WD med lav hastighet.

---

## 7c. Øvrig elektronikk (oppdatert)

| Del | Detaljer | Merknad |
|---|---|---|
| **Batteri** | 2× 6S 6500 mAh 60C i parallell = **13 000 mAh** | ~1,8 kg; 60C gir enorm strømreserve – sikring 100 A er fortsatt nødvendig |
| **Ramme** | Alu firkant **30×30×2 mm** | Bra til bærende rails; bruk 2–3 mm plater i tillegg for stag |
| **GPS** | HGLRC M100-5883 (M10 + QMC5883) | Monter **vekk fra motorer/strømkabler**, gjerne på mast |
| **Telemetri** | Raspberry Pi 4B 8 GB + USB SIM-modem | MAVLink over LTE (Mission Planner), video over IP (GStreamer/WebRTC), fjernstyring |

**Om Raspberry Pi-løsningen:**
- ✅ Telemetri/waypoints via MAVLink over 4G fungerer bra (Mission Planner/QGC)
- ⚠️ **Video over LTE gir 100–300 ms latency** – greit for crawler, dårlig for rask bil
- ⚠️ Pi 4B trenger **5 V/3 A** – egen BEC, og den veier ~50 g + kjøling
- ⚠️ Fjernstyring over nett: bruk MAVLink «manual control» eller eget WebRTC-opplegg – regn med latency
- 💡 Alternativ: bruk Pi-en kun til telemetri/logging, og 5,8 GHz analog video til kjøring

---

## 9. Svinger: hvordan ArduPilot lager ulik hjulhastighet

Skid steer i ArduPilot blander **gass + styring** til to utganger:

```
venstre = gass − styring
høyre   = gass + styring
```

- Svinger du høyre, får **venstre par mer** og **høyre par mindre** (eller revers)
- Blir styringen så stor at en side går over 100 %, **skalerer ArduPilot ned gassen** automatisk
- Fire ESCs er koblet parvis (venstre/høyre), så «ulik hastighet» gjelder **par mot par** – ikke hjul for hjul

### Parametere som styrer svingen

| Parameter | Startverdi | Effekt |
|---|---|---|
| `FRAME_CLASS` | 2 | Skid steer |
| `SERVO1_FUNCTION` | 73 | ThrottleLeft |
| `SERVO2_FUNCTION` | 74 | ThrottleRight |
| `ATC_STR_RAT_MAX` | **90** deg/s | Maks svinghastighet |
| `ATC_STR_ACC_MAX` | **120** deg/s² | Hvor raskt svingen kan endres |
| `ATC_STR_RAT_P` | **0.2** | Hvor hardt den følger ønsket sving |
| `ATC_STR_RAT_FF` | **0.1** | Forhåndskompensering |
| `TURN_RADIUS` | **1.5 m** | Minste svingradius (skid steer) |
| `PIVOT_TURN_ANGLE` | **0** | **0 = slå av pivot-svinger** (viktig for sensorløse motorer!) |
| `PIVOT_TURN_RATE` | 45 deg/s | Brukes bare hvis pivot er på |
| `MOT_THR_MIN` | **8** | Minste gass – unngå at innerhjul stopper helt |
| `MOT_SLEW_UP/DN` | 0.5/0.5 | Myk gassendring |

### Anbefalt strategi for din bil

1. **`PIVOT_TURN_ANGLE = 0`** – unngå sving på stedet (verst for sensorløse motorer)
2. **`TURN_RADIUS = 1.5 m`** – rullende svinger i stedet for pivot
3. **`MOT_THR_MIN = 8`** – innerhjulet går sakte, men stopper ikke
4. **`ATC_STR_RAT_MAX = 90`** – roligere svinger i starten; øk etter hvert
5. **`ATC_STR_ACC_MAX = 120`** – myk overgang inn/ut av sving

### Manuell vs. auto

| Modus | Oppførsel |
|---|---|
| **Manual** | Gass = throttle-stick, sving = yaw-stick; miksing automatisk |
| **Acro** | Yaw-stick = ønsket svingrate (`ATC_STR_RAT_MAX` begrenser) |
| **Auto/Guided** | Navigasjonskontrolleren beregner sving + fart (`CRUISE_SPEED`, `WP_SPEED`) |

### Vil du ha mer avansert fordeling (torque vectoring)?

ArduPilot Rover støtter **ikke** per-hjul vektorisering direkte. Muligheter:
- **Lua-skript** (AP_Scripting støttes på H743): les RC-input, regn ut fire separate pådrag og overstyr `SERVO3/4` med `SRV_Channels:set_output_pwm_chan()`
- **Egen mikser i radioen** (TX16S): fire kanaler ut, men da mister du ArduPilot-navigasjon
- **VESC med CAN**: hvis du bytter til VESC, kan du styre hver motor presist

### Tuning-rekkefølge

1. SITL i Mission Planner (simulering – ingen risiko)
2. Juster `ATC_STR_RAT_*` til svingen følger jevnt
3. Deretter `ATC_SPEED_*` for fart
4. Siste: `TURN_RADIUS` og `PIVOT_TURN_ANGLE` etter kjørestil
5. Husk: **sensorløse motorer** tåler dårlig raske retningsbytter – hold svingene rullende

---

## 8. Gjenstår å avklare

1. **Batteri:** kapasitet/C-rate (f.eks. 6S 6000 mAh 60C)?
2. **Ramme:** har du fres/CNC til alu, eller skal alt printes?
3. **Hjulbredde/vifteform:** skal jeg lage en konkret designbeskrivelse (målliste) for CAD?
4. **GPS/telemetri:** ønsker du waypoints og telemetri i Mission Planner?

Si fra, så lager jeg **CAD-målliste for hjulet**, **full paramfil** og **koblingsskjema som PDF/tegning**.
