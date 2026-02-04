import argparse
from pathlib import Path

from vc_vid_timeseriesplot.vid_timeseriesplot import load_video_and_play_with


def main() -> None:
    """
    Command line entry point for video player.

    Command line arguments:
        - --video-path or -p : Path to video file
        - --data-npy: path to npy file to be used as data
            (can be specified multiple times)
        (pl.DataFrame will be used elsewhere)
    """
    parser = argparse.ArgumentParser(
        description="Play video with timeseries plot visualization"
    )
    parser.add_argument(
        "--video-path",
        "-p",
        type=Path,
        required=True,
        help="Path to the video file to play",
    )
    parser.add_argument(
        "--data-npy",
        type=Path,
        action="append",
        help="Path to npy file for timeseries data (can be specified multiple times)",
    )

    args = parser.parse_args()

    # For now, just load the video without data (plotting to be implemented later)
    load_video_and_play_with(args.video_path, data=None)
