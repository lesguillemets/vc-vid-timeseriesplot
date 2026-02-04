"""Video and timeseries plot viewer."""

from vc_vid_timeseriesplot.vid_timeseriesplot import load_video_and_play_with

__all__ = ["load_video_and_play_with", "main"]


def main() -> None:
    """Command line entry point."""
    import argparse
    from pathlib import Path

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
