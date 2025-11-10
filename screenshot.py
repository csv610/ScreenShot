import time
import argparse
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional
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
        """Generate a unique filename with optional timestamp."""
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = base_name.replace(".png", f"_{timestamp}.png")

        # Ensure directory exists
        output_path = Path(base_name)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return base_name

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture a screenshot of the screen.")

    parser.add_argument("--output", type=str, default="screenshot.png",
                        help="Output file name (default: screenshot.png).")
    parser.add_argument("--delay", type=int, default=3,
                        help="Time in seconds to wait before capturing (default: 3 seconds).")
    parser.add_argument("--timestamp", action="store_true",
                        help="Append timestamp to the output filename to avoid overwriting.")

    # Optional region capture arguments
    parser.add_argument("--x1", type=int, help="Top-left X coordinate (for region capture).")
    parser.add_argument("--y1", type=int, help="Top-left Y coordinate (for region capture).")
    parser.add_argument("--x2", type=int, help="Bottom-right X coordinate (for region capture).")
    parser.add_argument("--y2", type=int, help="Bottom-right Y coordinate (for region capture).")

    # Optional interval capture arguments
    parser.add_argument("--interval", type=float, help="Interval in seconds between screenshots (for interval capture).")
    parser.add_argument("--time-limit", type=float, help="Total duration in seconds for interval capture.")

    args = parser.parse_args()

    try:
        # Create ScreenShot object
        screenshot = ScreenShot(output=args.output, delay=args.delay, timestamp=args.timestamp)

        # Determine capture type (interval, region, or full-screen)
        coords_provided = [args.x1, args.y1, args.x2, args.y2]
        interval_provided = args.interval is not None
        time_limit_provided = args.time_limit is not None

        # Check for interval capture
        if interval_provided or time_limit_provided:
            if not (interval_provided and time_limit_provided):
                parser.error("Both --interval and --time-limit must be provided for interval capture.")
            success = screenshot.capture_interval(args.interval, args.time_limit)
        # Check for region capture
        elif all(coord is not None for coord in coords_provided):
            success = screenshot.capture_area(args.x1, args.y1, args.x2, args.y2)
        elif any(coord is not None for coord in coords_provided):
            parser.error("All coordinates (--x1, --y1, --x2, --y2) must be provided for region capture.")
        # Default to full-screen capture
        else:
            success = screenshot.capture_screen()

        sys.exit(0 if success else 1)
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

