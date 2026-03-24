#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

python3 -m venv .venv-mlx
source .venv-mlx/bin/activate
pip install --upgrade pip
pip install -r mlx_host/requirements.txt

export MLX_MODEL_NAME="${MLX_MODEL_NAME:-NexVeridian/Qwen3.5-4B-5bit}"
export MLX_HOST="${MLX_HOST:-0.0.0.0}"
export MLX_PORT="${MLX_PORT:-8000}"

python mlx_host/mlx_openai_server.py
