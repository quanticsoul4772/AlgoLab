#!/usr/bin/env sh
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"

exec "$ROOT/.venv/bin/python" "$ROOT/scripts/run.py" "$@"
