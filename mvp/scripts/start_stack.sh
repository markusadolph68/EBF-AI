#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f .env ]]; then
  set -a
  source .env
  set +a
fi

mkdir -p \
  data/openwebui \
  data/chroma \
  documents/hr \
  documents/vertrieb \
  documents/projekte \
  processed/manifests \
  processed/parsed \
  processed/chunks \
  logs

docker compose up -d

echo "Open WebUI: http://localhost:${OPEN_WEBUI_PORT:-3000}"
echo "Chroma: http://localhost:${CHROMA_PORT:-8001}"
echo "MLX-Server separat starten mit: ./scripts/start_mlx_host.sh"
