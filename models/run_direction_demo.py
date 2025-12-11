"""
run_direction_demo.py

Small CLI demo for direction detection.

Usage examples (from repo root):
    python -m models.run_direction_demo --folder demo_audio
    python -m models.run_direction_demo --file demo_audio/Alarm.wav
"""

import argparse
import glob
import os

from models.direction_detector import detect_direction


def run_on_file(file_path: str):
    result = detect_direction(file_path)
    print(f"{os.path.basename(file_path)} -> {result}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Analyse a single audio file.",
    )
    parser.add_argument(
        "--folder",
        type=str,
        default=None,
        help="Analyse all audio files in a folder (default: demo_audio).",
    )
    args = parser.parse_args()

    # Single-file mode
    if args.file:
        run_on_file(args.file)
        return

    # Folder mode
    folder = args.folder or os.path.join(os.path.dirname(__file__), "..", "demo_audio")
    patterns = ["*.wav", "*.mp3", "*.ogg"]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(folder, pattern)))

    if not files:
        print(f"No audio files found in {folder}")
        return

    print(f"Running direction demo on {len(files)} files in {folder}\n")
    for f in sorted(files):
        run_on_file(f)


if __name__ == "__main__":
    main()