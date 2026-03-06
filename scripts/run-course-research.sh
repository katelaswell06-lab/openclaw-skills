#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT_DIR/course-output}"
CHANNEL="${2:-indydevdan}"
SITE="${3:-https://agenticengineer.com/tactical-agentic-coding}"

mkdir -p "$OUT_DIR"

printf 'Running course research scaffold\n'
printf 'Output: %s\n' "$OUT_DIR"
printf 'Channel: %s\n' "$CHANNEL"
printf 'Landing: %s\n\n' "$SITE"

bash "$ROOT_DIR/scripts/course-miner.sh" "$OUT_DIR" "$CHANNEL" "$SITE"

