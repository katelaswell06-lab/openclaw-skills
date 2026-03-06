#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-/home/anthony/apps/openclaw-skills/course-output}"
CHANNEL="${2:-indydevdan}"
SITE="${3:-https://agenticengineer.com/tactical-agentic-coding}"

mkdir -p "$OUT_DIR/videos" "$OUT_DIR/transcripts" "$OUT_DIR/modules" "$OUT_DIR/raw"

echo "Course miner initialized"
echo "Output: $OUT_DIR"
echo "Channel: $CHANNEL"
echo "Source: $SITE"

echo "Run these commands in your environment with yt-dlp/youtube-transcript-api installed:"
echo "- yt-dlp --flat-playlist --print-json \"https://www.youtube.com/@$CHANNEL\" > $OUT_DIR/videos/index.json"
echo "- python3 scripts/extract_transcripts.py --input $OUT_DIR/videos/index.json --out $OUT_DIR/transcripts"
echo "Optional: mp4 fallback for missing transcripts"
echo "- python3 scripts/download_and_transcribe.py --input $OUT_DIR/videos/index.json --out $OUT_DIR/transcripts"
