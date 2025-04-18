# Makefile for the timy project

# Variables
PYTHON = python3
# PIP = pip3 # No longer needed directly
UV = uv
PACKAGE_NAME = timy
SRC_DIR = src
DIST_DIR = dist
BUILD_DIR = build
VENV_DIR = .venv

# Phony targets (targets that don't represent files)
.PHONY: all install develop clean lint test build run

# Default target
all: install

# Installation
install: clean $(VENV_DIR)
	$(UV) pip install .

# Development installation (editable mode)
develop: clean $(VENV_DIR)
	$(UV) pip install -e .

# Create virtual environment if it doesn't exist
$(VENV_DIR):
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment in $(VENV_DIR)..."; \
		$(UV) venv $(VENV_DIR); \
	fi

# Clean build artifacts and caches
clean:
	rm -rf $(DIST_DIR) $(BUILD_DIR) $(SRC_DIR)/*.egg-info __pycache__ .pytest_cache .ruff_cache $(VENV_DIR)
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

# Linting (using ruff - add it to your dev dependencies if you use it)
lint:
	# $(PYTHON) -m ruff check $(SRC_DIR)
	@echo "Linting step placeholder. Consider adding ruff or flake8."

# Testing (using pytest - add it to your dev dependencies if you use it)
test:
	# $(PYTHON) -m pytest
	@echo "Testing step placeholder. Consider adding pytest and writing tests."

# Build source distribution and wheel
build:
	$(UV) build

# Run the application
run:
	$(PACKAGE_NAME)

# --- Potentially useful for packaging --- 

# Create a source distribution (tarball)
sdist: build
	@echo "Source distribution created in $(DIST_DIR)/"

# Create a wheel distribution
wheel: build
	@echo "Wheel created in $(DIST_DIR)/"

# Note: Creating a Homebrew formula is usually done in a separate tap repository.
# This Makefile provides the build artifacts (sdist/wheel) needed.
# You would typically:
# 1. Create a GitHub release with the sdist/wheel.
# 2. Create/Update a formula file (e.g., timy.rb) in your Homebrew tap repo.
# 3. The formula would download the release asset (usually the sdist tarball)
#    and specify how to build/install it using standard Python setuptools. 