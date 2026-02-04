# vc-cid-timeseriesplot

This library will provide a function to play a video, along with a time series plot of any data,
with visualising current time on that plot.

## GUI

The gui has

- The video played on the right
- The plot area on the left, where:
  - Plots, eash given as a numpy 1d array or polars Series, that shows how that data changes in time.
     - Assume eash row (or item) in the Series or array corresponds to each frame.
     - Each plot is vertically stacked, and their x axis is shared.
  - A vertical line is shown to denote to the current timepoint in the plot.
    - To reduce redraw time, that line is overlayed on top of the base plot.
    - The right space is clickable; when the use clicks one point, the video will be set to that timepoint.
- In the bottom, you can
  - pause or resume playing
  - set the video time, by time and by frame

It will look like this:

```text
+---------------------------------------------------------------------+
|                                  |                                  |
|                                  |                                  |
|                                  |   Arbitorary number of plots     |
|                                  |                                  |
|      VIDEO ON THE LEFT           |    shown on the right,           |
|                                  |       vertically stacked,        |
|                                  |       x-axis shared.             |
|                                  |  Current playtime is visialised  |
|                                  |     by a vertical line.          |
|----------------------------------+----------------------------------|
|                                                                     |
|       Some buttons for control may appear here                      |
+---------------------------------------------------------------------+
```



## Function

- `load_video_and_play_with(video_path: Path, data: list[np.ndarray | pl.Series] | pl.DataFrame)` will be our main entry point, with additional options emerging later.
  - If list of (np.ndarray or pl.Series) is given, each of that will create a subplot.
  - If a pl.DataFrame is given, all columns from that dataframe will be used for plotting.
