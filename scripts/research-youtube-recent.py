#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


def ensure_yt_dlp() -> str:
    # Prefer local binary in PATH or common user install location
    candidates = [
        os.environ.get("YT_DLP_BIN", "yt-dlp"),
        "/home/anthonyoc/.local/bin/yt-dlp",
        "/usr/bin/yt-dlp",
        "yt-dlp",
    ]
    for c in candidates:
        if not c:
            continue
        if os.path.isabs(c) and os.path.exists(c):
            return c
        if "" != c and not os.path.isabs(c):
            return c
    raise FileNotFoundError("yt-dlp binary not found")


def fetch_channel(handle: str, tab: str, limit: int) -> List[dict]:
    ytdlp_bin = ensure_yt_dlp()
    url = f"https://www.youtube.com/@{handle}"
    if tab:
        url = url + "/" + tab

    cmd = [ytdlp_bin, "--flat-playlist", "--print-json", url]
    print(f"Fetching from: {url}")
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {proc.stderr.strip()[:400]}")

    entries = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        vid = payload.get("id")
        title = payload.get("title")
        if not vid or not title:
            continue
        entries.append({
            "video_id": vid,
            "title": title,
            "duration": payload.get("duration"),
            "upload_date": payload.get("upload_date"),
            "url": payload.get("url") or f"https://www.youtube.com/watch?v={vid}",
            "thumbnail": payload.get("thumbnail"),
            "uploader": payload.get("uploader"),
        })
        if len(entries) >= limit:
            break

    return entries


def write_index(entries: List[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")


def write_summary(entries: List[dict], results: List[dict], path: Path) -> None:
    payload = {
        "source": entries,
        "results": results,
        "success_count": sum(1 for r in results if r.get("status") == "ok"),
        "failed_count": sum(1 for r in results if r.get("status") != "ok"),
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def extract_transcripts(entries: List[dict], out_dir: Path) -> List[dict]:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except Exception as exc:
        raise RuntimeError(f"youtube_transcript_api unavailable: {exc}")

    results = []
    out_dir.mkdir(parents=True, exist_ok=True)

    for e in entries:
        vid = e["video_id"]
        title = e["title"]
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in title)[:90] or "untitled"
        out_file = out_dir / f"{vid}__{safe}.txt"
        try:
            transcript = YouTubeTranscriptApi().fetch(vid)
            with out_file.open("w", encoding="utf-8") as f:
                for item in transcript:
                    t0 = item.start
                    dur = item.duration
                    text = item.text.replace("\n", " ")
                    f.write(f"[{t0:.2f}-{t0+dur:.2f}] {text}\n")
            results.append({"video_id": vid, "status": "ok", "transcript_file": str(out_file)})
            print(f"✓ transcript: {vid}")
        except Exception as exc:
            # keep going for remaining videos
            results.append({"video_id": vid, "status": "error", "error": str(exc)})
            print(f"✗ transcript failed: {vid} -> {exc}")

    return results


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--handle", default="indydevdan")
    p.add_argument("--tab", default="videos", choices=["videos", "shorts", "streams"])
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--out", default="/home/anthony/apps/openclaw-skills/course-output/indydevdan")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    out_base = Path(args.out)
    index_path = out_base / "videos.index.jsonl"
    transcript_dir = out_base / "transcripts"
    summary_path = out_base / "research-summary.json"

    try:
        entries = fetch_channel(args.handle, args.tab, args.limit)
        if not entries:
            print("No entries found. Aborting.")
            return 1
        write_index(entries, index_path)
        print(f"Fetched {len(entries)} items -> {index_path}")
        results = extract_transcripts(entries, transcript_dir)
        write_summary(entries, results, summary_path)
        print(f"Done. Summary: {summary_path}")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
