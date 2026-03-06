#!/usr/bin/env python3
import argparse
import json
import os
from typing import Any, Dict

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except Exception as exc:
    raise SystemExit(f"youtube-transcript-api missing: {exc}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--out", required=True)
    return p.parse_args()


def load_videos(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                j = json.loads(line)
            except json.JSONDecodeError:
                # maybe one-line JSON array style; skip for now
                continue
            yield j


def main() -> None:
    args = parse_args()
    os.makedirs(args.out, exist_ok=True)
    for video in load_videos(args.input):
        vid = video.get("id") or video.get("id_", "")
        title = video.get("title") or "untitled"
        if not vid:
            continue
        safe = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in title)[:80]
        out_path = os.path.join(args.out, f"{vid}__{safe}.txt")
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid)
        except Exception as exc:
            print(f"[skip] {vid}: {exc}")
            continue

        with open(out_path, "w", encoding="utf-8") as f:
            for item in transcript:
                text = item.get("text", "").strip()
                start = item.get("start", 0)
                dur = item.get("duration", 0)
                f.write(f"[{start:.1f}-{start+dur:.1f}] {text}\n")

        print(f"saved {out_path}")


if __name__ == "__main__":
    main()
