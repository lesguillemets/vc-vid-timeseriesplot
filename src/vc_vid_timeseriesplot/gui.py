"""GUI components for video and timeseries plot viewer."""

from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QMouseEvent
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSpinBox,
    QDoubleSpinBox,
)


class ClickablePlotWidget(QWidget):
    """Widget for the plot area that handles clicks to set video time."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(400)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.video_player: QMediaPlayer | None = None
        self.video_duration_ms: int = 0

        # Placeholder label
        label = QLabel("Plot area\n(Click to set video time)", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(self)
        layout.addWidget(label)

    def set_video_player(self, player: QMediaPlayer) -> None:
        """Set the video player to control."""
        self.video_player = player

    def set_video_duration(self, duration_ms: int) -> None:
        """Set the total video duration in milliseconds."""
        self.video_duration_ms = duration_ms

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse click to set video time."""
        if self.video_player and self.video_duration_ms > 0:
            # Calculate position as proportion of widget height
            click_y = event.position().y()
            widget_height = self.height()
            # Position from top (0.0) to bottom (1.0)
            proportion = click_y / widget_height
            # Set video position
            new_position_ms = int(proportion * self.video_duration_ms)
            self.video_player.setPosition(new_position_ms)


class ControlPanel(QWidget):
    """Control panel with play/pause, frame, and time controls."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.video_player: QMediaPlayer | None = None
        self.fps: float = 30.0  # Default FPS
        self.frame_count: int = 0

        layout = QHBoxLayout(self)

        # Play/Pause button
        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        layout.addWidget(self.play_pause_button)

        # Frame control
        layout.addWidget(QLabel("Frame:"))
        self.frame_spinbox = QSpinBox()
        self.frame_spinbox.setMinimum(0)
        self.frame_spinbox.setMaximum(0)
        self.frame_spinbox.valueChanged.connect(self.on_frame_changed)
        layout.addWidget(self.frame_spinbox)

        # Time control
        layout.addWidget(QLabel("Time (s):"))
        self.time_spinbox = QDoubleSpinBox()
        self.time_spinbox.setMinimum(0.0)
        self.time_spinbox.setMaximum(0.0)
        self.time_spinbox.setDecimals(3)
        self.time_spinbox.setSingleStep(0.1)
        self.time_spinbox.valueChanged.connect(self.on_time_changed)
        layout.addWidget(self.time_spinbox)

        layout.addStretch()

    def set_video_player(self, player: QMediaPlayer) -> None:
        """Set the video player to control."""
        self.video_player = player
        # Connect to playback state changes
        player.playbackStateChanged.connect(self.on_playback_state_changed)
        # Connect to position changes to update spinboxes
        player.positionChanged.connect(self.on_position_changed)
        # Connect to duration changes
        player.durationChanged.connect(self.on_duration_changed)

    def set_fps(self, fps: float) -> None:
        """Set the video frame rate."""
        self.fps = fps

    def set_frame_count(self, frame_count: int) -> None:
        """Set the total frame count."""
        self.frame_count = frame_count
        self.frame_spinbox.setMaximum(frame_count - 1)

    def toggle_play_pause(self) -> None:
        """Toggle play/pause state."""
        if not self.video_player:
            return

        if self.video_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.video_player.pause()
        else:
            self.video_player.play()

    def on_playback_state_changed(self, state: QMediaPlayer.PlaybackState) -> None:
        """Update button text based on playback state."""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_pause_button.setText("Pause")
        else:
            self.play_pause_button.setText("Play")

    def on_position_changed(self, position_ms: int) -> None:
        """Update spinboxes when video position changes."""
        # Block signals to avoid recursion
        self.time_spinbox.blockSignals(True)
        self.frame_spinbox.blockSignals(True)

        time_s = position_ms / 1000.0
        self.time_spinbox.setValue(time_s)

        if self.fps > 0:
            frame = int(time_s * self.fps)
            self.frame_spinbox.setValue(frame)

        self.time_spinbox.blockSignals(False)
        self.frame_spinbox.blockSignals(False)

    def on_duration_changed(self, duration_ms: int) -> None:
        """Update spinbox ranges when duration is known."""
        max_time_s = duration_ms / 1000.0
        self.time_spinbox.setMaximum(max_time_s)

        if self.fps > 0:
            max_frame = int(max_time_s * self.fps)
            self.frame_spinbox.setMaximum(max_frame)
            self.frame_count = max_frame + 1

    def on_frame_changed(self, frame: int) -> None:
        """Handle frame spinbox change."""
        if not self.video_player or self.fps <= 0:
            return

        time_s = frame / self.fps
        position_ms = int(time_s * 1000)
        self.video_player.setPosition(position_ms)

    def on_time_changed(self, time_s: float) -> None:
        """Handle time spinbox change."""
        if not self.video_player:
            return

        position_ms = int(time_s * 1000)
        self.video_player.setPosition(position_ms)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, video_path: Path):
        super().__init__()
        self.setWindowTitle("Video and Timeseries Plot Viewer")
        self.resize(1200, 600)

        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create horizontal layout for video and plot area
        content_layout = QHBoxLayout()

        # Video player (LEFT side)
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumWidth(600)
        content_layout.addWidget(self.video_widget, 1)

        # Plot area (RIGHT side)
        self.plot_widget = ClickablePlotWidget()
        content_layout.addWidget(self.plot_widget, 1)

        main_layout.addLayout(content_layout)

        # Control panel at bottom
        self.control_panel = ControlPanel()
        main_layout.addWidget(self.control_panel)

        # Set up media player
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        # Connect components
        self.plot_widget.set_video_player(self.media_player)
        self.control_panel.set_video_player(self.media_player)

        # Set up video duration tracking
        self.media_player.durationChanged.connect(
            lambda duration: self.plot_widget.set_video_duration(duration)
        )

        # Load video
        self.load_video(video_path)

    def load_video(self, video_path: Path) -> None:
        """Load a video file."""
        if not video_path.exists():
            print(f"Video file not found: {video_path}")
            return

        url = QUrl.fromLocalFile(str(video_path.absolute()))
        self.media_player.setSource(url)
        print(f"Loaded video: {video_path}")


def create_and_show_gui(video_path: Path) -> tuple[QApplication, MainWindow]:
    """Create and show the GUI application."""
    import sys

    app = QApplication(sys.argv)
    window = MainWindow(video_path)
    window.show()
    return app, window
