#!/usr/bin/env python3
import argparse
import glob
import os


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--transcripts", required=True)
    p.add_argument("--out", required=True)
    return p.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.out, exist_ok=True)
    out_md = os.path.join(args.out, "module-blueprint.md")

    files = sorted(glob.glob(os.path.join(args.transcripts, "*.txt")))
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Course Draft Blueprint\n\n")
        f.write("## Source transcripts\n\n")
        for fp in files:
            base = os.path.basename(fp)
            f.write(f"- {base}\n")
        f.write("\n## Next steps\n\n")
        f.write("- Turn each transcript into concept cards (problem, approach, implementation, anti-pattern).\n")
        f.write("- Group into modules by dependency graph: fundamentals -> orchestration -> productionization.\n")
        f.write("- Add practical lab tasks per module for team and Zach productization path.\n")

    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
