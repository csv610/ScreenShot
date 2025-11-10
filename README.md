# ScreenShot

A Python utility for capturing screenshots with flexible options for full-screen, region-based, and interval-based captures.

## Features

- **Full-Screen Capture**: Capture your entire screen with a single command
- **Region Capture**: Capture a specific area of the screen by specifying coordinates
- **Interval Capture**: Capture screenshots at regular intervals over a specified duration
- **Delay Control**: Add a configurable delay before capturing to prepare your screen
- **Timestamp Support**: Automatically append timestamps to filenames to avoid overwrites
- **Cross-Platform**: Works on Windows and macOS

## Requirements

- Python 3.7+
- Pillow (PIL) >= 10.0.0

## Installation

### Automated Setup (Recommended)
```bash
git clone https://github.com/csv610/ScreenShot.git
cd ScreenShot
./setup.sh
```

### Manual Setup
1. Clone the repository:
```bash
git clone https://github.com/csv610/ScreenShot.git
cd ScreenShot
```

2. Create a virtual environment:
```bash
python -m venv screnv
source screnv/bin/activate  # On Windows: screnv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Full-Screen Capture
Capture the entire screen with a 3-second delay:
```bash
python screenshot.py
```

### Region Capture
Capture a specific area (e.g., coordinates 0,0 to 1920,1080):
```bash
python screenshot.py --x1 0 --y1 0 --x2 1920 --y2 1080 --output region.png
```

### Interval Capture
Capture screenshots every 2 seconds for 30 seconds total:
```bash
python screenshot.py --interval 2 --time-limit 30 --output screenshots.png
```

### Command-Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--output` | str | `screenshot.png` | Output file name |
| `--delay` | int | `3` | Delay in seconds before capturing |
| `--timestamp` | flag | - | Append timestamp to filename to avoid overwrites |
| `--x1` | int | - | Top-left X coordinate (for region capture) |
| `--y1` | int | - | Top-left Y coordinate (for region capture) |
| `--x2` | int | - | Bottom-right X coordinate (for region capture) |
| `--y2` | int | - | Bottom-right Y coordinate (for region capture) |
| `--interval` | float | - | Interval in seconds between screenshots (for interval capture) |
| `--time-limit` | float | - | Total duration in seconds for interval capture |

## Examples

```bash
# Capture with 5-second delay
python screenshot.py --delay 5

# Capture with timestamp to avoid overwriting
python screenshot.py --timestamp --output my_screenshot.png

# Capture region with timestamp
python screenshot.py --x1 100 --y1 100 --x2 1000 --y2 800 --timestamp --output region.png

# Capture 10 screenshots, one every second
python screenshot.py --interval 1 --time-limit 10 --output screenshot.png
```

## Platform Support

- ✅ Windows
- ✅ macOS
- ❌ Linux (not currently supported)

## Error Handling

The script validates all inputs and provides helpful error messages for:
- Invalid coordinates
- Negative delays
- Invalid intervals or time limits
- Platform compatibility

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for bugs and feature requests.

## Author

[csv610](https://github.com/csv610)
