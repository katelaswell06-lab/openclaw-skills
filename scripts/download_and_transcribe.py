#!/usr/bin/env python3
import argparse
import json
import os
import subprocess

# Placeholder scaffold: keep dependency install in environment explicit.
# Install: yt-dlp, ffmpeg, whisper (or openai-whisper) before using fallback mode.

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--audio-only", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.out, exist_ok=True)
    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                j = json.loads(line)
            except json.JSONDecodeError:
                continue
            vid = j.get("id") or j.get("id_")
            if not vid:
                continue
            url = f"https://www.youtube.com/watch?v={vid}"
            audio_file = os.path.join(args.out, f"{vid}.mp3")
            txt_out = os.path.join(args.out, f"{vid}.txt")
            print(f"Downloading {url}")
            try:
                cmd = ["yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "mp3", "-o", audio_file, url]
                if args.audio_only:
                    cmd.extend(["-x"])
                subprocess.run(cmd, check=True)
                # Transcription step intentionally not auto-run here; plug Whisper command as needed.
                open(txt_out, "w", encoding="utf-8").write(f"Downloaded audio: {audio_file}\nTranscribe step placeholder.\n")
            except FileNotFoundError:
                raise SystemExit("yt-dlp not installed")
            except subprocess.CalledProcessError as e:
                print(f"download failed for {vid}: {e}")

if __name__ == "__main__":
    main()
