#!/bin/bash

# ScreenShot Setup Script
# Sets up the development environment for the ScreenShot utility

set -e  # Exit on any error

echo "Setting up ScreenShot development environment..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping creation"
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"

echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

echo ""

# Install development tools
echo "Installing development tools..."
pip install black flake8 pytest > /dev/null 2>&1
echo "✓ Development tools installed"

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "Available commands:"
echo "  make help       - Show all available commands"
echo "  make run        - Run the screenshot utility"
echo "  make lint       - Run linting checks"
echo "  make format     - Format code with black"
echo "  make clean      - Clean up cache and build artifacts"
echo ""
