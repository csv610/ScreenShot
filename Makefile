.PHONY: help install install-dev clean run lint format test venv act check_venv

help:
	@echo "ScreenShot - Screenshot Utility"
	@echo ""
	@echo "Available commands:"
	@echo "  make venv          - Create virtual environment"
	@echo "  make act           - Activate virtual environment"
	@echo "  make install       - Install dependencies"
	@echo "  make install-dev   - Install dependencies with dev tools"
	@echo "  make clean         - Remove cache and build artifacts"
	@echo "  make run           - Run the screenshot utility"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black"
	@echo "  make test          - Run tests (if available)"

venv:
	python3 -m venv shotenv

act:
	bash -c "source shotenv/bin/activate && exec bash"

check_venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Error: Virtual environment not activated"; \
		echo "Run: source shotenv/bin/activate"; \
		exit 1; \
	fi

install: check_venv
	pip install -r requirements.txt

install-dev: check_venv
	pip install -r requirements.txt
	pip install black flake8 pytest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/

run:
	python screenshot.py

lint:
	flake8 screenshot.py --max-line-length=120

format:
	black screenshot.py

test:
	@echo "No tests configured yet"

.DEFAULT_GOAL := help
