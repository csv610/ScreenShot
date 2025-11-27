import argparse
import sys
from screenshot import ScreenShot


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Capture screenshots of the screen with various options.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full-screen capture with default 3-second delay
  python screenshot_cli.py

  # Full-screen with custom output filename (short form)
  python screenshot_cli.py -o my_screenshot.png

  # Full-screen with no delay (short form)
  python screenshot_cli.py -d 0

  # Capture a specific region of the screen
  python screenshot_cli.py --x1 100 --y1 100 --x2 500 --y2 500

  # Capture screenshots at intervals (every 2 seconds for 10 seconds, short form)
  python screenshot_cli.py -i 2 -l 10

  # Add timestamp to filename to avoid overwriting (short form)
  python screenshot_cli.py -t

  # Combine options: full-screen with timestamp, custom delay and output (short form)
  python screenshot_cli.py -o myshot.png -d 1 -t

  # Region capture with timestamp and custom delay (short form)
  python screenshot_cli.py --x1 0 --y1 0 --x2 1920 --y2 1080 -d 1 -t
        """
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="screenshot.png",
        help="Output file name (default: screenshot.png). Saves to output/ folder."
    )

    parser.add_argument(
        "-d", "--delay",
        type=int,
        default=3,
        help="Time in seconds to wait before capturing (default: 3 seconds)."
    )

    parser.add_argument(
        "-t", "--timestamp",
        action="store_true",
        help="Append timestamp to the output filename to avoid overwriting."
    )

    # Region capture arguments
    parser.add_argument(
        "--x1",
        type=int,
        help="Top-left X coordinate (for region capture)."
    )

    parser.add_argument(
        "--y1",
        type=int,
        help="Top-left Y coordinate (for region capture)."
    )

    parser.add_argument(
        "--x2",
        type=int,
        help="Bottom-right X coordinate (for region capture)."
    )

    parser.add_argument(
        "--y2",
        type=int,
        help="Bottom-right Y coordinate (for region capture)."
    )

    # Interval capture arguments
    parser.add_argument(
        "-i", "--interval",
        type=float,
        help="Interval in seconds between screenshots (for interval capture)."
    )

    parser.add_argument(
        "-l", "--time-limit",
        type=float,
        help="Total duration in seconds for interval capture."
    )

    return parser


def validate_arguments(args: argparse.Namespace) -> None:
    """Validate argument combinations."""
    coords_provided = [args.x1, args.y1, args.x2, args.y2]
    interval_provided = args.interval is not None
    time_limit_provided = args.time_limit is not None

    # Check interval capture requirements
    if interval_provided or time_limit_provided:
        if not (interval_provided and time_limit_provided):
            raise ValueError("Both --interval and --time-limit must be provided for interval capture.")

    # Check region capture requirements
    if any(coord is not None for coord in coords_provided):
        if not all(coord is not None for coord in coords_provided):
            raise ValueError("All coordinates (--x1, --y1, --x2, --y2) must be provided for region capture.")


def determine_capture_type(args: argparse.Namespace) -> str:
    """Determine which type of capture to perform."""
    coords_provided = [args.x1, args.y1, args.x2, args.y2]
    interval_provided = args.interval is not None
    time_limit_provided = args.time_limit is not None

    if interval_provided or time_limit_provided:
        return "interval"
    elif all(coord is not None for coord in coords_provided):
        return "region"
    else:
        return "fullscreen"


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        # Validate argument combinations
        validate_arguments(args)

        # Create ScreenShot object
        screenshot = ScreenShot(
            output=args.output,
            delay=args.delay,
            timestamp=args.timestamp
        )

        # Determine and execute the appropriate capture type
        capture_type = determine_capture_type(args)

        if capture_type == "interval":
            success = screenshot.capture_interval(args.interval, args.time_limit)
        elif capture_type == "region":
            success = screenshot.capture_area(args.x1, args.y1, args.x2, args.y2)
        else:  # fullscreen
            success = screenshot.capture_screen()

        return 0 if success else 1

    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
