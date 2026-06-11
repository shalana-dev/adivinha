#!/usr/bin/env bash
# Rode no Git Bash: bash scripts/publicar-github.sh
set -euo pipefail

USER="shalana-dev"

publicar() {
  local dir="$1"
  local repo="$2"
  local desc="$3"

  cd "$dir"

  if [ ! -d .git ]; then
    git init
    git branch -M main
  fi

  git add .
  git commit -m "feat: adiciona projeto com README, assets e documentação" || true

  if git remote get-url origin >/dev/null 2>&1; then
    git push -u origin main
  elif command -v gh >/dev/null 2>&1; then
    gh repo create "${USER}/${repo}" --public --source . --remote origin --description "${desc}" --push
  else
    echo "Instale GitHub CLI (gh) ou crie o repo manualmente:"
    echo "https://github.com/new -> ${repo}"
    git remote add origin "https://github.com/${USER}/${repo}.git"
    git push -u origin main
  fi

  echo "OK: https://github.com/${USER}/${repo}"
}

publicar "/d/Desktop/adivinha" "adivinha" "Jogo web para adivinhar um numero de 1 a 100 com dicas e contador de tentativas."
publicar "/d/Desktop/gorjeta" "gorjeta" "Calculadora de gorjeta para dividir conta entre pessoas com validacao."
