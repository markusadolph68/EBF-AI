#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f .env ]]; then
  set -a
  source .env
  set +a
fi

if command -v python3.13 >/dev/null 2>&1; then
  PYTHON_BIN="python3.13"
elif command -v python3.12 >/dev/null 2>&1; then
  PYTHON_BIN="python3.12"
elif command -v python3.11 >/dev/null 2>&1; then
  PYTHON_BIN="python3.11"
else
  PYTHON_BIN="python3"
fi

echo "Nutze Python: $PYTHON_BIN"

"$PYTHON_BIN" -m venv .venv-ingest
source .venv-ingest/bin/activate
pip install --upgrade pip
pip install -r ingest/requirements.txt

python ingest/ingest_documents.py "$@"
