#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."
docker compose down
pkill -f "uvicorn mlx_openai_server:app" || true
