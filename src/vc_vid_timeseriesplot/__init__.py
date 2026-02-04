"""Video and timeseries plot viewer."""

from vc_vid_timeseriesplot.vid_timeseriesplot import load_video_and_play_with

__all__ = ["load_video_and_play_with", "main"]


def main() -> None:
    """Command line entry point."""
    from src.main import main as cli_main

    cli_main()
