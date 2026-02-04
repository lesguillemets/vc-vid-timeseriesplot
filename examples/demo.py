#!/usr/bin/env python3
"""Example script demonstrating the video player GUI.

This script assumes you have a video file available.
You can download a sample video or use your own.

Usage:
    python examples/demo.py /path/to/your/video.mp4
"""

import argparse
import sys
from pathlib import Path

from vc_vid_timeseriesplot import load_video_and_play_with


def main() -> None:
    """Run the demo video player."""
    parser = argparse.ArgumentParser(
        description="Demo video player with timeseries plot (plotting to be added later)"
    )
    parser.add_argument(
        "video_path",
        type=Path,
        help="Path to the video file to play",
    )

    args = parser.parse_args()

    if not args.video_path.exists():
        print(f"Error: Video file not found: {args.video_path}", file=sys.stderr)
        print("\nPlease provide a valid video file path.", file=sys.stderr)
        print("Example: python examples/demo.py /path/to/video.mp4", file=sys.stderr)
        sys.exit(1)

    print(f"Loading video: {args.video_path}")
    print("\nControls:")
    print("  - Click on the right area to jump to a time position")
    print("  - Use Play/Pause button to control playback")
    print("  - Use Frame and Time spinboxes to navigate")
    print()

    # Launch the GUI
    load_video_and_play_with(args.video_path, data=None)


if __name__ == "__main__":
    main()
