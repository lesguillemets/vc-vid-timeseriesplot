from pathlib import Path

import numpy as np
import polars as pl

from vc_vid_timeseriesplot.gui import create_and_show_gui


def load_video_and_play_with(
    video_path: Path, data: list[np.ndarray | pl.Series] | pl.DataFrame | None = None
) -> None:
    """
    Load a video and play it with timeseries plot.

    Args:
        video_path: Path to the video file
        data: Timeseries data (to be implemented later)
    """
    app, window = create_and_show_gui(video_path)
    app.exec()
