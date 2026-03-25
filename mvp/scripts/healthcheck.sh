#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f .env ]]; then
  set -a
  source .env
  set +a
fi

OPEN_WEBUI_PORT="${OPEN_WEBUI_PORT:-3000}"
CHROMA_PORT="${CHROMA_PORT:-8001}"
MLX_PORT="${MLX_PORT:-8000}"

echo "Pruefe Open WebUI ..."
curl -fsS "http://127.0.0.1:${OPEN_WEBUI_PORT}/" >/dev/null

echo "Pruefe Chroma ..."
if ! curl -fsS "http://127.0.0.1:${CHROMA_PORT}/api/v2/heartbeat" >/dev/null; then
  curl -fsS "http://127.0.0.1:${CHROMA_PORT}/api/v1/heartbeat" >/dev/null
fi

echo "Pruefe MLX health ..."
curl -fsS "http://127.0.0.1:${MLX_PORT}/health" >/dev/null

echo "Pruefe MLX model list ..."
curl -fsS "http://127.0.0.1:${MLX_PORT}/v1/models" >/dev/null

echo "Alle Healthchecks erfolgreich."
