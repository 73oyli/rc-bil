# Push rc-bil til GitHub (fra Kali-VM)

Repoet er allerede **committet lokalt** på Windows (`Initial commit: 4WD FPV RC-bil – CAD, tegninger, STL, printplan`).
Det som mangler er å få mappen over til Kali og pushe til `https://github.com/73oyli/rc-bil`.

## Steg 1 – start Kali og kopier mappen

På Windows (PowerShell), fra workspace:

```powershell
$ws = "C:\Users\73oyl\Documents\deepseek-harness\default-workspace"
ssh kali "mkdir -p ~/projects"
tar -czf - -C "$ws" "rc bil" | ssh kali "tar -xzf - -C ~/projects && mv ~/projects/'rc bil' ~/projects/rc-bil"
```

## Steg 2 – push fra Kali

```bash
ssh kali 'bash ~/projects/rc-bil/push-til-github.sh'
```

Skriptet:
1. init-er repo hvis det mangler
2. committer endringer
3. `gh repo create rc-bil --public --source=. --remote=origin --push` (hvis gh er autentisert)
4. ellers gir det deg kommandoene for manuell remote

## Alternativ uten gh (SSH-remote)

```bash
ssh kali
cd ~/projects/rc-bil
git remote add origin git@github.com:73oyli/rc-bil.git
git push -u origin main
```

> Repoet må da opprettes manuelt på github.com/new med navn `rc-bil` (uten README/.gitignore).

## Hva som pushes

- `scad/`, `stl/`, `pdf/`, `png/`, `gif/`, `param/`, `python/`, `notater/`, `bilder-bygg/`
- `README.md`, `print-logg.md`
- `.gitignore` (utelukker `*.zip`, `__pycache__` og `*.tmp`)

## Etter push

- Legg gjerne inn en beskrivelse på GitHub: «4WD FPV RC-bil – 3D-printbart chassis, ArduPilot Rover, ELRS»
- Bilder fra bygging legges i `bilder-bygg/` og pushes med vanlig `git add/commit/push`
## Automatisk regenerering (GitHub Actions)

Workflowen [.github/workflows/build-cad.yml](.github/workflows/build-cad.yml) kjører ved push som endrer:

- `scad/**.scad`
- `python/**.py`
- selve workflow-filen

Den installerer OpenSCAD + Pillow på Ubuntu, regenererer:

- `pdf/bil-tegninger.pdf` og `png/pdf-p*.png` (via `python/draw-pdf.py`)
- `stl/*.stl` og `notater/print-estimater.md` (via `python/stl-estimater.py`)

og committer resultatet automatisk med `github-actions[bot]`.

**Merk:** PDF-en genereres med DejaVu-font på Linux, så den kan se litt annerledes ut enn den lokale Windows-versjonen (Segoe UI). Alt annet er identisk.
