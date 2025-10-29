#!/usr/bin/env python3

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT = os.path.join(SCRIPT_DIR, "noise.sh")

def find_videos(folder):
    videos = []
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".mp4"):
                videos.append(os.path.join(root, f))
    return videos

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ninit.py /path/to/folder")
        return

    folder = sys.argv[1]

    if not os.path.isdir(folder):
        print(f"ERROR: Folder does not exist: {folder}")
        return

    videos = find_videos(folder)

    if not videos:
        print("No .mp4 files found.")
        return

    print(f"Found {len(videos)} videos.")
    print("Starting noise reduction...\n")

    for video in videos:
        print(f"Processing: {video}")
        subprocess.run([SCRIPT, video])

    print("\n✅ All videos processed successfully.")

if __name__ == "__main__":
    main()
