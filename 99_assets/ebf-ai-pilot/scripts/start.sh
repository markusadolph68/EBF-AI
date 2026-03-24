#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

echo "[1/2] Docker Dienste starten..."
docker compose up -d

echo "[2/2] MLX OpenAI Server starten..."
cd app
python3 -m uvicorn mlx_openai_server:app --host 0.0.0.0 --port 8000
