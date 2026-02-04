#!/usr/bin/env python3
"""Demo script to test the video player GUI."""

from pathlib import Path
import sys

# For testing during development, adjust the path if needed
sys.path.insert(0, str(Path(__file__).parent / "src"))

import cv2
import numpy as np
from vc_vid_timeseriesplot.vid_timeseriesplot import load_video_and_play_with


def create_demo_video(output_path: Path, duration_s: float = 10.0, fps: int = 30):
    """Create a simple demo video with changing colours and frame counter."""
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

    total_frames = int(duration_s * fps)

    for frame_num in range(total_frames):
        # Create a frame with changing background colour
        progress = frame_num / total_frames
        # Colour changes from blue to red over time
        b = int(255 * (1 - progress))
        r = int(255 * progress)
        g = 100

        frame = np.full((height, width, 3), [b, g, r], dtype=np.uint8)

        # Add frame counter text
        text = f"Frame {frame_num}/{total_frames - 1}"
        cv2.putText(
            frame,
            text,
            (50, height // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (255, 255, 255),
            3,
        )

        # Add time display
        time_text = f"Time: {frame_num / fps:.2f}s"
        cv2.putText(
            frame,
            time_text,
            (50, height // 2 + 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
        )

        out.write(frame)

    out.release()
    print(f"Created demo video: {output_path}")
    print(f"Duration: {duration_s}s, FPS: {fps}, Total frames: {total_frames}")


if __name__ == "__main__":
    # Create a demo video
    demo_video_path = Path("/tmp/demo_video.mp4")

    if not demo_video_path.exists():
        print("Creating demo video...")
        create_demo_video(demo_video_path, duration_s=10.0, fps=30)
    else:
        print(f"Using existing demo video: {demo_video_path}")

    print("\nStarting video player...")
    print("Controls:")
    print("  - Click on the right area to jump to a time position")
    print("  - Use Play/Pause button to control playback")
    print("  - Use Frame and Time spinboxes to navigate")
    print()

    # Launch the GUI
    load_video_and_play_with(demo_video_path, data=None)
