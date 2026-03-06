#!/usr/bin/env bash
set -euo pipefail

HANDLE="${1:-indydevdan}"
TAB="${2:-videos}"   # videos | shorts | streams
LIMIT="${3:-3}"
OUT="${4:-/home/anthony/apps/openclaw-skills/course-output/indydevdan-pilot}"

# ensure local user bin is available for yt-dlp (installed to ~/.local/bin)
export PATH="$HOME/.local/bin:${PATH}"

cd /home/anthony/apps/openclaw-skills

printf "Running IndyDevDan pilot (handle=%s, tab=%s, limit=%s)\n" "$HANDLE" "$TAB" "$LIMIT"
printf "Output: %s\n" "$OUT"

python3 scripts/research-youtube-recent.py \
  --handle "$HANDLE" \
  --tab "$TAB" \
  --limit "$LIMIT" \
  --out "$OUT"

echo -e "\nPilot output files:"
printf "%s\n" "- Index: $OUT/videos.index.jsonl"
printf "%s\n" "- Transcripts: $OUT/transcripts"
printf "%s\n" "- Summary: $OUT/research-summary.json"
