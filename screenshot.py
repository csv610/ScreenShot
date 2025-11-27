import platform
import sys
import time
from datetime import datetime
from pathlib import Path

from PIL import ImageGrab


class ScreenShot:
    """Class to capture full-screen or region-based screenshots."""

    def __init__(self, output: str = "screenshot.png", delay: int = 3, timestamp: bool = False) -> None:
        """
        Initialize screenshot settings.

        :param output: Output file name.
        :param delay: Delay in seconds before capturing (must be non-negative).
        :param timestamp: Whether to add a timestamp to the filename.
        :raises ValueError: If delay is negative or output path is invalid.
        """
        self._validate_delay(delay)
        self.output = self._generate_filename(output, timestamp)
        self.delay = delay
        self._check_platform_support()
        self._ensure_output_folder_exists()

    # ===== Public Methods =====

    def capture_screen(self) -> bool:
        """
        Captures the entire screen after a delay.

        :return: True if successful, False otherwise.
        """
        try:
            print(f"Waiting {self.delay} seconds before capturing the full screen...")
            time.sleep(self.delay)

            screenshot = ImageGrab.grab()
            screenshot.save(self.output)
            print(f"Full-screen screenshot saved as {self.output}")
            return True
        except Exception as e:
            print(f"Error capturing full screen: {e}", file=sys.stderr)
            return False

    def capture_area(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """
        Captures a specific area of the screen after a delay.

        :param x1: Top-left X coordinate.
        :param y1: Top-left Y coordinate.
        :param x2: Bottom-right X coordinate.
        :param y2: Bottom-right Y coordinate.
        :return: True if successful, False otherwise.
        :raises ValueError: If coordinates are invalid.
        """
        self._validate_coordinates(x1, y1, x2, y2)

        try:
            print(f"Waiting {self.delay} seconds before capturing the selected area...")
            time.sleep(self.delay)

            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            screenshot.save(self.output)
            print(f"Selected area screenshot saved as {self.output}")
            return True
        except Exception as e:
            print(f"Error capturing area: {e}", file=sys.stderr)
            return False

    def capture_interval(self, interval: float, time_limit: float) -> bool:
        """
        Captures screenshots at regular intervals for a specified duration.

        :param interval: Time in seconds between each screenshot (must be positive).
        :param time_limit: Total duration in seconds for capturing (must be positive).
        :return: True if successful, False otherwise.
        :raises ValueError: If interval or time_limit are invalid.
        """
        self._validate_interval(interval)
        self._validate_time_limit(time_limit)

        try:
            print(f"Waiting {self.delay} seconds before starting interval capture...")
            time.sleep(self.delay)

            start_time = time.time()
            screenshot_count = 0

            print(f"Starting interval capture: {interval}s interval, {time_limit}s duration")

            while time.time() - start_time < time_limit:
                screenshot_count += 1
                # Generate unique filename for each screenshot
                output_path = self._generate_unique_interval_filename(screenshot_count)

                screenshot = ImageGrab.grab()
                screenshot.save(output_path)
                elapsed = time.time() - start_time
                print(f"Screenshot #{screenshot_count} saved as {output_path} (elapsed: {elapsed:.1f}s)")

                # Sleep for the interval, but check if time_limit is exceeded
                remaining_time = time_limit - (time.time() - start_time)
                if remaining_time > 0:
                    time.sleep(min(interval, remaining_time))

            print(f"Interval capture completed: {screenshot_count} screenshots saved")
            return True
        except Exception as e:
            print(f"Error during interval capture: {e}", file=sys.stderr)
            return False

    # ===== Private Helper Methods =====

    def _check_platform_support(self) -> None:
        """Check if the current platform is supported."""
        supported_platforms = ("Windows", "Darwin")  # Windows, macOS
        current_platform = platform.system()
        if current_platform not in supported_platforms:
            raise RuntimeError(
                f"Screenshot capture is not supported on {current_platform}. "
                f"Supported platforms: {', '.join(supported_platforms)}"
            )

    def _generate_filename(self, base_name: str, add_timestamp: bool) -> str:
        """Generate a unique filename with optional timestamp in the output folder."""
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = base_name.replace(".png", f"_{timestamp}.png")

        # Place file in output folder if not already in a subdirectory
        output_path = Path(base_name)
        if output_path.parent == Path("."):
            output_path = Path("output") / base_name

        return str(output_path)

    def _generate_unique_interval_filename(self, index: int) -> str:
        """
        Generate unique filenames for interval screenshots.

        :param index: Screenshot sequence number.
        :return: Unique filename with sequence number.
        """
        output_path = Path(self.output)
        stem = output_path.stem
        suffix = output_path.suffix
        parent = output_path.parent

        # Insert sequence number before extension
        unique_filename = f"{stem}_{index:04d}{suffix}"
        return str(parent / unique_filename)

    def _ensure_output_folder_exists(self) -> None:
        """Ensure the output folder and any parent directories exist."""
        output_path = Path(self.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    # ===== Validation Methods =====

    def _validate_delay(self, delay: int) -> None:
        """Validate that delay is non-negative."""
        if delay < 0:
            raise ValueError(f"Delay must be non-negative, got {delay}")

    @staticmethod
    def _validate_interval(interval: float) -> None:
        """Validate that interval is positive."""
        if interval <= 0:
            raise ValueError(f"Interval must be positive, got {interval}")

    @staticmethod
    def _validate_time_limit(time_limit: float) -> None:
        """Validate that time_limit is positive."""
        if time_limit <= 0:
            raise ValueError(f"Time limit must be positive, got {time_limit}")

    @staticmethod
    def _validate_coordinates(x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Validate screenshot region coordinates.

        :raises ValueError: If coordinates are invalid.
        """
        if not all(isinstance(coord, int) for coord in [x1, y1, x2, y2]):
            raise ValueError("All coordinates must be integers")
        if x1 >= x2:
            raise ValueError(f"x1 ({x1}) must be less than x2 ({x2})")
        if y1 >= y2:
            raise ValueError(f"y1 ({y1}) must be less than y2 ({y2})")
        if any(coord < 0 for coord in [x1, y1, x2, y2]):
            raise ValueError("Coordinates must be non-negative")


