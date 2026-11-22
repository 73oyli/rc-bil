#!/usr/bin/env bash
# Push rc-bil til GitHub fra Kali-VM.
# Bruk:
#   1) Kopier mappen til Kali (se GITHUB.md / README)
#   2) ssh kali 'bash ~/projects/rc-bil/push-til-github.sh'
#
# Forutsetter at gh er autentisert i Kali (gh auth status). Ellers bruk SSH-remote manuelt.
set -euo pipefail

cd "$(dirname "$0")/.."
echo "Repo: $(pwd)"

if [ ! -d .git ]; then
  git init -b main
fi

git add -A
if ! git diff --cached --quiet; then
  git commit -m "4WD FPV RC-bil: CAD, tegninger, STL, printplan"
fi

if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  if git remote get-url origin >/dev/null 2>&1; then
    git push -u origin main
  else
    gh repo create rc-bil --public --source=. --remote=origin --push
  fi
else
  echo "gh er ikke autentisert. Legg til remote manuelt:"
  echo "  git remote add origin git@github.com:73oyli/rc-bil.git"
  echo "  git push -u origin main"
  exit 1
fi

echo "Ferdig: https://github.com/73oyli/rc-bil"
