#!/usr/bin/env bash
set -euo pipefail

HANDLE="${1:-indydevdan}"
TAB="${2:-videos}"   # videos | shorts | streams
LIMIT="${3:-0}"      # 0 means all videos in selected tab
OUT="${4:-/home/anthony/apps/openclaw-skills/course-output/indydevdan-full}"
SLEEP_SECONDS="${5:-1.5}"
LIST_SLEEP="${6:-1.0}"

# ensure local user bin is available for yt-dlp (installed to ~/.local/bin)
export PATH="$HOME/.local/bin:${PATH}"

cd /home/anthony/apps/openclaw-skills

printf "Running IndyDevDan extraction (handle=%s, tab=%s, limit=%s)\n" "$HANDLE" "$TAB" "$LIMIT"
printf "Output: %s\n" "$OUT"

python3 scripts/research-youtube-recent.py \
  --handle "$HANDLE" \
  --tab "$TAB" \
  --limit "$LIMIT" \
  --out "$OUT" \
  --sleep-seconds "$SLEEP_SECONDS" \
  --list-sleep "$LIST_SLEEP"

echo -e "\nPilot output files:"
printf "%s\n" "- Index: $OUT/videos.index.jsonl"
printf "%s\n" "- Transcripts: $OUT/transcripts"
printf "%s\n" "- Summary: $OUT/research-summary.json"