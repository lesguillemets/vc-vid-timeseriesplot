import argparse
from pathlib import Path

from vc_vid_timeseriesplot.vid_timeseriesplot import load_video_and_play_with


def main():
    """
    command line arguments:
        - --video-path or -p : Path
        - --data-npy: path to npy file to be used as data
            (can be specified multiple times)
        (pl.DataFrame will be used elsewhere)
    """
    pass
