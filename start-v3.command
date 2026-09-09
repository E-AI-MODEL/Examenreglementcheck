#!/bin/bash
set -e
cd "$(dirname "$0")"
PYTHON="${PYTHON:-python3}"
if ! "$PYTHON" -c 'import fastapi,uvicorn,docx,fitz,jsonschema,yaml,multipart' >/dev/null 2>&1; then
  echo "De Python-afhankelijkheden ontbreken nog."
  echo "Voer eerst uit:"
  echo "  $PYTHON -m pip install -r requirements.txt"
  echo
  read -r -p "Druk op Enter om te sluiten..."
  exit 1
fi
echo "Examenreglement-checker v3 start op http://127.0.0.1:8765"
"$PYTHON" run.py
